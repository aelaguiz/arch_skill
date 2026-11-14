"""Decision deck server: the threaded HTTP server that renders the deck, serves its pictures and records every answer.

Routes are listed in decision_deck_help.py; the request handler is in decision_deck_routes.py.
"""
from __future__ import annotations

import json
import os
import re
import secrets
import socket
import sys
import threading
import time
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_core import (  # noqa: E402,F401  (state_path re-exported for callers of this module)
    DEFAULT_GRACE_MIN, DEFAULT_MAX_HOURS, append_pick, decision_by_id, image_ids, next_open, open_decisions,
    state_path, utc_now, validate_bind_host)
from decision_deck_ledger import (  # noqa: E402
    current_comment, current_picks, current_skips, deck_state, is_skip, make_comment, make_done, make_record,
    make_reply, make_status, read_records, status_pick)

RID_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")     # the page's id for one user action, reused on every retry
BATCH_JOBS_MAX = 256                              # actions in one POST /api/batch


def request_id(payload: dict):
    """The payload's `rid`, or None when it has none; ValueError for one that is not 8 to 64 of [A-Za-z0-9_-]."""
    rid = payload.get("rid")
    if rid is not None and not (isinstance(rid, str) and RID_RE.match(rid)):
        raise ValueError("rid must be 8 to 64 letters, digits, '-' or '_'")
    return rid


def renews(rec: dict) -> bool:
    """Lines that restart the grace once every decision is picked: a pick (not a note), a status, a reply."""
    return rec.get("kind") in ("status", "reply") or (rec.get("kind") == "pick" and not is_skip(rec))


class PageClosed(Exception):
    """A record that arrived after the server decided to stop; the handler answers 410 and records nothing."""


def remove_own_state(ledger) -> None:
    """Remove the state file only when it names this process, never another server's on the same ledger."""
    path = state_path(ledger)
    try:
        if json.loads(path.read_text()).get("pid") == os.getpid():
            path.unlink(missing_ok=True)
    except (OSError, ValueError):
        pass


def _write_state(path: Path, data: dict) -> None:
    """Write the state file whole, then rename (`watch` reads it); owner-only, since it holds the session's token."""
    tmp = path.with_suffix(".json.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(data, indent=2) + "\n")
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)


class DeckServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 128    # a deck page asks for every image at once; a backlog of 5 resets some connections

    def __init__(self, spec, ledger, host, port, grace_s, max_s, source=""):
        from decision_deck_routes import Handler, allowed_hosts  # the handler imports the page renderer
        host = validate_bind_host(host)             # canonical form: "localhost" binds and is named as 127.0.0.1
        if ":" in host:                 # the socket family must match the address; the base class defaults to IPv4
            self.address_family = socket.AF_INET6
        super().__init__((host, port), Handler)
        self.spec = spec
        self.source = source             # the header's source line (serve --source), fixed at serve time
        self.host = host
        self.ledger = Path(ledger)
        self.grace_s = grace_s
        self.max_s = max_s
        self.lock = threading.Lock()
        self.started = time.monotonic()
        self.finished = threading.Event()
        self.reason = ""
        self.token = secrets.token_urlsafe(32)
        self.image_of = image_ids(spec)                                      # spec-relative path -> sha16
        self.images = {sha: rel for rel, sha in self.image_of.items()}      # /img/<sha16> -> spec-relative path
        name = f"[{host}]" if ":" in host else host
        self.url = f"http://{name}:{self.server_address[1]}/"
        self.allowed_hosts = allowed_hosts(host, self.server_address[1])     # Host and Origin checks (routes)
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        # The generation starts from the clock, so a page held across a server restart starts over once too.
        self.gen, self._gen_mark, self._gen_lock = int(time.time() * 1000), None, threading.Lock()
        self.ledger_gen()
        records = read_records(self.ledger)
        self.latest = current_picks(spec, records)
        self.skips = current_skips(spec, records)     # notes newer than a pick; their decisions are unchanged
        self.rids = rid_map(records)                  # survives a restart
        self._seen = (self.gen, len(records), self._stat())     # what the timer has read of the ledger
        self.all_picked_at = time.monotonic() if not open_decisions(spec, self.latest) else None
        _write_state(state_path(self.ledger), {
            "url": self.url, "pid": os.getpid(), "host": host, "port": self.server_address[1],
            "spec": str(spec["path"]), "ledger": str(self.ledger.resolve()), "started": utc_now(),
            "grace_s": grace_s, "max_s": max_s, "token": self.token, "source": source})
        threading.Thread(target=self._timer, name="decision-deck-timer", daemon=True).start()

    def _stat(self):
        try:
            st = self.ledger.stat()
        except FileNotFoundError:
            return None
        return (st.st_ino, st.st_size, st.st_mtime_ns)

    def ledger_gen(self) -> int:
        """The ledger's generation: it goes up when the file is replaced (new inode) or shrinks (truncated), so a
        page holding sequence numbers from the old file knows to start over. A vanished ledger is a change; one
        appearing (for the first time, or again after it vanished) is not a further one."""
        with self._gen_lock:
            st = self._stat()
            mark = (st[0], st[1]) if st else (None, 0)
            last = self._gen_mark
            if last is not None and last[0] is not None and (mark[0] != last[0] or mark[1] < last[1]):
                self.gen += 1
            self._gen_mark = mark
            return self.gen

    def regen(self, gen: int) -> int:
        """A new generation when a caller holds more lines than generation `gen` has: the ledger was rewritten in
        place without being seen to shrink. Within one generation the line count then never falls, so a page can
        drop a reset answer that is behind the lines it already holds."""
        with self._gen_lock:
            if self.gen == gen:
                self.gen += 1
            return self.gen

    def snapshot(self, since: int = 0, gen: int | None = None) -> dict:
        """The deck state read from the ledger file (the agent may append to it directly) and the lines after
        `since`, plus the /api/state keys. A caller holding another generation `gen`, or more lines than the
        ledger has, gets every line and `reset: true`, and starts over."""
        now = self.ledger_gen()
        records = read_records(self.ledger)
        latest = current_picks(self.spec, records)
        if since > len(records) and gen in (None, now):     # holds more lines than there are
            now = self.regen(now)
        reset = (gen is not None and gen != now) or since > len(records)
        since = 0 if reset else max(0, since)
        out = {"picked": latest, "skipped": current_skips(self.spec, records),
               "open": open_decisions(self.spec, latest), "state": deck_state(self.spec, records),
               "n": len(records), "gen": now, "since": since, "lines": records[since:]}
        if reset:
            out["reset"] = True
        return out

    def _land(self, rec: dict) -> dict:
        """Append (the caller holds the lock, and _open has caught up with the ledger) and return the deck state
        after it. The new line is then read back like any other (_follow): picks, request ids and the grace."""
        append_pick(self.ledger, rec)
        self._follow()
        return deck_state(self.spec, read_records(self.ledger))

    def _regrace(self, renewed: bool) -> None:
        """The grace runs only while every decision is picked: cleared when one is open again (a replaced or
        truncated ledger), started fresh when all are picked again, restarted by a renewing line."""
        if open_decisions(self.spec, self.latest):
            self.all_picked_at = None
        elif renewed or self.all_picked_at is None:
            self.all_picked_at = time.monotonic()

    def _follow(self) -> None:
        """Under the lock, from the timer: read lines that reached the ledger by any route (the agent's own
        appends when the server refused or was slow), so they renew the grace by the same rule and keep the
        picks current. A replaced or truncated ledger is read again from the top. The request ids are always the
        ones the ledger holds now, so a retry of an action whose line went with an old ledger lands again. Called
        before and after every append, so no request checks an id against a ledger already replaced."""
        gen, mark = self.ledger_gen(), self._stat()
        seen_gen, seen_n, seen_mark = self._seen
        if (gen, mark) == (seen_gen, seen_mark):
            return
        records = read_records(self.ledger)
        top = gen != seen_gen or len(records) < seen_n
        new = records if top else records[seen_n:]
        self._seen = (gen, len(records), mark)
        self.latest = current_picks(self.spec, records)
        self.skips = current_skips(self.spec, records)
        self.rids = rid_map(records)
        self._regrace(any(renews(r) for r in new))

    def _open(self, what: str) -> None:
        """Under the lock, before recording: refuse once the timer stopped the page, and catch up with the ledger."""
        if self.finished.is_set():  # the timer decided to stop under this lock; nothing lands after that
            raise PageClosed(f"this page has closed; {what} not recorded")
        self._follow()

    def _pick(self, payload: dict) -> tuple:
        """(record, state) for a pick (or a skip line with a note); the caller holds the lock."""
        rid = request_id(payload)
        if rid in self.rids:            # a retry of an answer already landed: the same record, nothing new
            rec = self.rids[rid]
            if rec.get("kind", "pick") not in ("pick", "comment"):
                raise ValueError("rid already names a different kind of record")
            return rec, deck_state(self.spec, read_records(self.ledger))
        rec = make_record(self.spec, payload.get("decision_id"), payload.get("option_id"),
                          payload.get("note", ""), payload.get("ts"))
        rec = dict(rec, rid=rid) if rid else rec
        return rec, self._land(rec)

    def _line(self, kind: str, payload: dict) -> tuple:
        """(record, state) for any other kind; the caller holds the lock."""
        rid = request_id(payload)
        if rid in self.rids:            # a retry of a line already landed: the same record, nothing new
            rec = self.rids[rid]
            if rec.get("kind") != kind:
                raise ValueError("rid already names a different kind of record")
            return rec, deck_state(self.spec, read_records(self.ledger))
        rec = self._make(kind, payload)
        rec = dict(rec, rid=rid) if rid else rec
        return rec, self._land(rec)

    def record(self, payload: dict) -> dict:
        """A pick (or a skip line with a note) from POST /api/pick."""
        with self.lock:                 # stamp and append under one lock, so the ledger stays in `ts` order
            self._open("the pick was")
            rec, state = self._pick(payload)
            remaining = open_decisions(self.spec, self.latest)
            n, _ = decision_by_id(self.spec, rec["decision_id"])
            nxt_n = next_open(self.spec, self.latest, n)     # skip decided pages; none open -> summary
            gen = self.gen
        nxt = f"/d/{nxt_n}" if nxt_n else "/summary"
        return {"ok": True, "record": rec, "next": nxt, "all_picked": not remaining, "open": remaining,
                "decision": state["decisions"][rec["decision_id"]], "state": state, "gen": gen}

    def append(self, kind: str, payload: dict) -> dict:
        """A comment or done from the page, or a status or reply from the agent (the handler checks its token)."""
        with self.lock:
            self._open("nothing was")
            rec, state = self._line(kind, payload)
            gen = self.gen
        out = {"ok": True, "record": rec, "state": state, "gen": gen}
        if kind != "done":
            out["decision"] = state["decisions"][rec["decision_id"]]
        return out

    def batch(self, jobs) -> dict:
        """POST /api/batch: what the page still had unsent when it was left, [{kind: pick|comment|done, body}] in
        the order the owner acted. All land under one lock in that order, so none overtakes another; each lands as
        its own route would (a repeated `rid` lands nothing new) and a bad one is skipped with its error."""
        if not isinstance(jobs, list) or not 0 < len(jobs) <= BATCH_JOBS_MAX:
            raise ValueError(f"jobs must be a list of 1 to {BATCH_JOBS_MAX} actions")
        results = []
        with self.lock:
            self._open("nothing was")
            for job in jobs:
                kind, body = (job.get("kind"), job.get("body")) if isinstance(job, dict) else (None, None)
                try:
                    if not isinstance(body, dict) or kind not in ("pick", "comment", "done"):
                        raise ValueError("each job is {kind: pick|comment|done, body: {...}}")
                    rec, _ = self._pick(body) if kind == "pick" else self._line(kind, body)
                    results.append({"status": 200, "record": rec})
                except ValueError as exc:
                    results.append({"status": 400, "error": str(exc)})
            state, gen = deck_state(self.spec, read_records(self.ledger)), self.gen
        return {"ok": True, "results": results, "state": state, "gen": gen}

    def _make(self, kind: str, payload: dict) -> dict:
        did = payload.get("decision_id")
        if kind == "comment":
            return make_comment(self.spec, did, payload.get("note", ""), payload.get("ts"))
        if kind in ("status", "reply"):     # an unbound line binds to what the ledger shows now
            records = read_records(self.ledger)
            if isinstance(did, str) and decision_by_id(self.spec, did)[1] is not None:
                if "pick_ts" not in payload and kind == "status":
                    payload = dict(payload, pick_ts=status_pick(self.spec, records, did, payload.get("state")))
                if "comment_ts" not in payload:
                    payload = dict(payload, comment_ts=current_comment(self.spec, records, did))
            if kind == "reply":
                return make_reply(self.spec, did, payload.get("text"), payload.get("comment_ts"))
            return make_status(self.spec, did, payload.get("state"), payload.get("result") or "",
                               payload.get("reply"), payload.get("pick_ts"), payload.get("comment_ts"))
        if kind == "done":
            return make_done(self.spec, read_records(self.ledger), payload.get("ts"))
        raise ValueError(f"unknown record kind {kind!r}")

    def _timer(self) -> None:
        while not self.finished.is_set():
            expired = False
            with self.lock:             # decide under record()'s lock, so a pick cannot renew the grace mid-decision
                self._follow()
                now = time.monotonic()
                if now - self.started >= self.max_s:
                    self.reason = "maximum lifetime reached"
                elif self.all_picked_at is not None and now - self.all_picked_at >= self.grace_s:
                    self.reason = "every decision picked; grace period over"
                if self.reason and not self.finished.is_set():
                    self.finished.set()     # record() refuses from here, so every accepted pick is already written
                    expired = True
            if expired:
                remove_own_state(self.ledger)   # only now can `watch` see the server gone and read a final ledger
                self.shutdown()
                return
            time.sleep(min(0.1, max(self.grace_s, 0.01)))


def rid_map(records: list) -> dict:
    """rid -> its record, for the records that carry one."""
    return {r["rid"]: r for r in records if isinstance(r.get("rid"), str)}


def make_server(spec, ledger, host, port, grace_s=DEFAULT_GRACE_MIN * 60, max_s=DEFAULT_MAX_HOURS * 3600, source=""):
    """The deck server, bound and with its state file written; call serve_forever() to run it."""
    return DeckServer(spec, ledger, host, port, grace_s, max_s, source)
