"""Decision deck ledger: the record kinds (pick, comment, status, reply, done), skip lines, the reducer and the watcher.

One JSON line per record, appended under a lock (decision_deck_core.append_pick):
  pick    {kind, decision_id, option_id, label, note, client_ts, ts, rid?}  the owner's answer; the latest one counts
  comment {kind, decision_id, note, client_ts, ts, rid?}                  an empty note clears; the decision stays open
  status  {kind, decision_id, state: acting|done|failed, result, reply?, pick_ts?, comment_ts?, ts, rid?}  the agent's
  reply   {kind, decision_id, text, comment_ts?, ts, rid?}                the agent's answer to a comment
  done    {kind, open: [ids], client_ts, ts, rid?}                        the owner finished the round; gates nothing
A line without "kind" reads as a pick, and one with option_id "skip" (a skip with a note) as a comment.
`rid` is the page's id for one user action, the same on every retry: a second line with a `rid` already read is a
duplicate and is dropped. `pick_ts` names the pick a status is about (that pick's `ts`) and `comment_ts` the comment a
reply answers; a status or reply about an answer or comment since replaced is history and changes nothing shown.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_core import (  # noqa: E402
    NOTE_MAX, SKIP_ID, SKIP_LABEL, decision_by_id, local_time, open_decisions, option_by_id, utc_now)
from decision_deck_spec import takes_note  # noqa: E402

KINDS = ("pick", "comment", "status", "reply", "done")
STATES = ("acting", "done", "failed")
TEXT_MAX = 2000                         # a status result or a reply


def _s(rec: dict, key: str) -> bool:
    return isinstance(rec.get(key), str)


def normalize(raw) -> dict | None:
    """The record with its `kind` set (kindless lines included), or None when it is not a well-formed record."""
    if not isinstance(raw, dict):
        return None
    kind = raw.get("kind")
    if kind is None:
        if not (_s(raw, "decision_id") and _s(raw, "option_id")):
            return None
        return dict(raw, kind="comment" if raw["option_id"] == SKIP_ID else "pick")
    if kind == "done":
        ok = isinstance(raw.get("open"), list) and all(isinstance(x, str) for x in raw["open"])
        return dict(raw) if ok else None
    if kind not in KINDS or not _s(raw, "decision_id"):
        return None
    ok = {"pick": _s(raw, "option_id"), "comment": isinstance(raw.get("note", ""), str),
          "status": raw.get("state") in STATES, "reply": _s(raw, "text") and raw["text"].strip()}[kind]
    return dict(raw) if ok else None


def parse_line(line: str) -> dict | None:
    try:
        return normalize(json.loads(line))
    except json.JSONDecodeError:
        return None


def fresh(rec: dict, rids: set) -> bool:
    """False for a repeat of a user action already read (same `rid`); records the rid of a first one in `rids`."""
    rid = rec.get("rid")
    if not isinstance(rid, str):
        return True
    if rid in rids:
        return False
    rids.add(rid)
    return True


def read_records(ledger: Path) -> list[dict]:
    """Every well-formed record in the ledger, of every kind, in file order, each user action once; a missing ledger
    is empty. A record's position in this list (1-based) is its sequence number `n`."""
    try:
        text = Path(ledger).read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    rids: set = set()
    return [r for r in (parse_line(ln) for ln in text.splitlines() if ln.strip()) if r and fresh(r, rids)]


def read_picks(ledger: Path) -> list[dict]:
    """The pick and comment records (picks, comments and skip lines), in file order."""
    return [r for r in read_records(ledger) if r["kind"] in ("pick", "comment")]


def is_skip(rec: dict) -> bool:
    """True for a note left without picking: a skip line or a comment record."""
    return rec.get("option_id") == SKIP_ID or rec.get("kind") == "comment"


def in_spec(spec: dict, rec: dict) -> bool:
    """True when the record's decision (and a pick's option) is in the current spec; a done record always is.

    A ledger outlives spec edits; a record naming a removed decision or option is stale and counts nowhere.
    """
    rec = rec if "kind" in rec else (normalize(rec) or {})
    if rec.get("kind") == "done":
        return True
    _, dec = decision_by_id(spec, rec.get("decision_id"))
    if dec is None:
        return False
    return rec.get("kind") != "pick" or option_by_id(dec, rec.get("option_id")) is not None


def _kind(rec: dict) -> str:
    return rec.get("kind") or ("comment" if rec.get("option_id") == SKIP_ID else "pick")


def latest_picks(records: list[dict]) -> dict[str, dict]:
    """decision_id -> its latest pick; a later pick for a decision supersedes the earlier one. Notes never count."""
    return {r["decision_id"]: r for r in records if _kind(r) == "pick"}


def latest_skips(records: list[dict]) -> dict[str, dict]:
    """decision_id -> its latest note (skip or comment) made after that decision's latest pick.

    A later pick or an empty comment clears it; a note never replaces a pick and never closes a decision.
    """
    skips: dict[str, dict] = {}
    for rec in records:
        kind = _kind(rec)
        if kind == "comment" and str(rec.get("note") or "").strip():
            skips[rec["decision_id"]] = rec
        elif kind in ("comment", "pick"):
            skips.pop(rec["decision_id"], None)
    return skips


def current_picks(spec: dict, records: list[dict]) -> dict[str, dict]:
    """decision_id -> latest pick, counting only records that are `in_spec`."""
    return latest_picks([r for r in records if in_spec(spec, r)])


def current_skips(spec: dict, records: list[dict]) -> dict[str, dict]:
    """decision_id -> latest note not superseded by a later pick, counting only records that are `in_spec`."""
    return latest_skips([r for r in records if in_spec(spec, r)])


def _bound(rec: dict, key: str, current) -> bool:
    """True when a session line is about what the slide shows now: it names nothing (an older line), or names it."""
    ref = rec.get(key)
    return ref is None or ref == current


def deck_state(spec: dict, records: list[dict]) -> dict:
    """What every slide, dot and the summary show: per decision its answer, comment, the session's status and reply.

    A new pick clears the status (a change after Done is a new answer the session acts on again). A pick carries the
    comment box, so like a comment it sets the comment, and an empty one clears it (the rule current_skips
    follows); a changed comment drops the reply to the old one. A status counts only for the pick it names
    (`pick_ts`) and a reply only for the comment it names (`comment_ts`). `pick_ts` and `comment_ts` here are the
    current pick's and comment's. `n` is the number of records read, the cursor for /api/state?since=n.
    """
    out = {d["id"]: {"choice": None, "label": "", "note": "", "ts": None, "comment": "", "status": None,
                     "result": "", "reply": "", "pick_ts": None, "comment_ts": None} for d in spec["decisions"]}
    done = None
    for rec in records:
        if not in_spec(spec, rec):
            continue
        kind = _kind(rec)
        if kind == "done":
            done = {"open": rec["open"], "ts": rec.get("ts")}
            continue
        d = out[rec["decision_id"]]
        if kind in ("pick", "comment"):
            note = str(rec.get("note") or "")
            if note != d["comment"]:
                d.update(comment=note, reply="", comment_ts=rec.get("ts"))
            if kind == "pick":
                opt = option_by_id(decision_by_id(spec, rec["decision_id"])[1], rec["option_id"])
                d.update(choice=rec["option_id"], label=opt["label"], note=note, ts=rec.get("ts"), status=None,
                         result="", pick_ts=rec.get("ts"))
        elif kind == "status":
            if not _bound(rec, "pick_ts", d["pick_ts"]):
                continue                        # about an answer the owner has since changed
            d.update(status=rec["state"], result=str(rec.get("result") or ""))
            if rec.get("reply") and _bound(rec, "comment_ts", d["comment_ts"]):
                d.update(reply=str(rec["reply"]))
        elif _bound(rec, "comment_ts", d["comment_ts"]):
            d.update(reply=rec["text"])
    return {"decisions": out, "done": done, "n": len(records)}


def decision_picks(spec: dict, records: list[dict], decision_id: str) -> list[dict]:
    """The decision's picks in ledger order (in the spec only)."""
    return [r for r in records if _kind(r) == "pick" and r["decision_id"] == decision_id and in_spec(spec, r)]


def status_pick(spec: dict, records: list[dict], decision_id: str, state: str, option: str | None = None,
                pick_ts: str | None = None):
    """The `ts` of the pick a new status line is about (None when the decision has no pick yet).

    `pick_ts` names it exactly (the `pick=<ts>` that ends its PICK line); `option` names the latest pick of that
    option. Without either, `acting` takes the latest pick, and done or failed the pick that the decision's most
    recent `acting` line named, even after a done or failed for it: a late or corrected result for work the agent
    started stays with that work and never marks an answer given since. With no acting line, the latest pick.
    ValueError for a `pick_ts` or `option` that names no pick on this decision.
    """
    picks = decision_picks(spec, records, decision_id)
    if pick_ts is not None:
        if not any(r.get("ts") == pick_ts for r in picks):
            raise ValueError(f"decision {decision_id} has no pick at {pick_ts}")
        return pick_ts
    if option is not None:
        named = [r for r in picks if r["option_id"] == option]
        if not named:
            raise ValueError(f"decision {decision_id} has no pick of option {option!r}")
        return named[-1].get("ts")
    acting = [r for r in records if _kind(r) == "status" and r["decision_id"] == decision_id
              and r["state"] == "acting" and isinstance(r.get("pick_ts"), str)]
    if state != "acting" and acting:
        return acting[-1]["pick_ts"]
    return picks[-1].get("ts") if picks else None


def current_comment(spec: dict, records: list[dict], decision_id: str):
    """The `ts` of the record that set the decision's comment now shown (None when there is none)."""
    return deck_state(spec, records)["decisions"][decision_id]["comment_ts"]


# ------------------------------------------------------------------ builders

def _decision(spec: dict, decision_id) -> dict:
    _, dec = decision_by_id(spec, decision_id) if isinstance(decision_id, str) else (None, None)
    if dec is None:
        raise ValueError(f"unknown decision {decision_id!r}")
    return dec


def _bounded(text, name: str, limit: int) -> str:
    text = text if isinstance(text, str) else ""
    if len(text) > limit:
        raise ValueError(f"{name} is longer than {limit} characters")
    return text.strip()


def make_record(spec: dict, decision_id, option_id, note, client_ts) -> dict:
    """A validated pick record; raises ValueError for an unknown decision or option or an over-long note.

    Option id `skip` (SKIP_ID) is a skip with a note: it keeps the kindless line shape, reads as a comment
    and needs a non-empty note on a decision that takes one, since a bare skip records nothing.
    """
    dec = _decision(spec, decision_id)
    if option_id == SKIP_ID:
        label = SKIP_LABEL
    else:
        opt = option_by_id(dec, option_id) if isinstance(option_id, str) else None
        if opt is None:
            raise ValueError(f"unknown option {option_id!r} for decision {decision_id}")
        label = opt["label"]
    note = _bounded(note, "note", NOTE_MAX) if takes_note(dec) else ""
    if option_id == SKIP_ID and not note:
        raise ValueError(f"a skip records a note, and decision {decision_id} has none to record")
    rec = {"decision_id": decision_id, "option_id": option_id, "label": label, "note": note, "ts": utc_now(),
           "client_ts": client_ts if isinstance(client_ts, str) else None}
    return rec if option_id == SKIP_ID else {"kind": "pick", **rec}


def make_comment(spec: dict, decision_id, note, client_ts) -> dict:
    dec = _decision(spec, decision_id)
    if not takes_note(dec):
        raise ValueError(f"decision {decision_id} takes no note")
    return {"kind": "comment", "decision_id": decision_id, "note": _bounded(note, "note", NOTE_MAX),
            "client_ts": client_ts if isinstance(client_ts, str) else None, "ts": utc_now()}


def _ref(value, name: str):
    if value is not None and not isinstance(value, str):
        raise ValueError(f"{name} must be a record's ts string or null")
    return value


def make_status(spec: dict, decision_id, state, result="", reply=None, pick_ts=None, comment_ts=None) -> dict:
    """A status line; `pick_ts` binds it to that pick and `comment_ts` binds its reply to that comment."""
    _decision(spec, decision_id)
    if state not in STATES:
        raise ValueError(f"state must be one of {', '.join(STATES)}")
    rec = {"kind": "status", "decision_id": decision_id, "state": state,
           "result": _bounded(result, "result", TEXT_MAX), "ts": utc_now()}
    if _ref(pick_ts, "pick_ts") is not None:
        rec["pick_ts"] = pick_ts
    if reply is not None and _bounded(reply, "reply", TEXT_MAX):
        rec["reply"] = _bounded(reply, "reply", TEXT_MAX)
        if _ref(comment_ts, "comment_ts") is not None:
            rec["comment_ts"] = comment_ts
    return rec


def make_reply(spec: dict, decision_id, text, comment_ts=None) -> dict:
    """A reply line; `comment_ts` binds it to the comment it answers."""
    _decision(spec, decision_id)
    text = _bounded(text, "text", TEXT_MAX)
    if not text:
        raise ValueError("a reply needs text")
    rec = {"kind": "reply", "decision_id": decision_id, "text": text, "ts": utc_now()}
    if _ref(comment_ts, "comment_ts") is not None:
        rec["comment_ts"] = comment_ts
    return rec


def make_done(spec: dict, records: list[dict], client_ts) -> dict:
    return {"kind": "done", "open": open_decisions(spec, current_picks(spec, records)),
            "client_ts": client_ts if isinstance(client_ts, str) else None, "ts": utc_now()}


# ------------------------------------------------------------------ lines for watch and status

def _q(text) -> str:
    return json.dumps(" ".join(str(text or "").split()), ensure_ascii=False)


def format_skip_line(rec: dict) -> str:
    return f"SKIP {rec['decision_id']} note={_q(rec.get('note'))} at {local_time(rec.get('ts'))}"


def format_comment_line(rec: dict) -> str:
    return f"COMMENT {rec['decision_id']} note={_q(rec.get('note'))} at {local_time(rec.get('ts'))}"


def format_done_line(rec: dict) -> str:
    return f"DONE open={','.join(rec.get('open') or []) or 'none'} at {local_time(rec.get('ts'))}"


def format_state_line(did: str, d: dict) -> str:
    return f"STATE {did} {d['status']} result={_q(d.get('result'))}"


def format_pick_line(rec: dict, spec: dict | None = None) -> str:
    """The watch line for a pick, a skip line (SKIP), a comment (COMMENT) or a done record (DONE)."""
    kind = _kind(rec)
    if kind == "done":
        return format_done_line(rec)
    if kind == "comment":
        return format_skip_line(rec) if rec.get("option_id") == SKIP_ID else format_comment_line(rec)
    label = rec.get("label") or ""
    if spec is not None:
        _, dec = decision_by_id(spec, rec["decision_id"])
        opt = option_by_id(dec, rec["option_id"]) if dec else None
        label = opt["label"] if opt else label
    ident = f" pick={rec['ts']}" if isinstance(rec.get("ts"), str) else ""     # what `act --pick-ts` takes
    return (f"PICK {rec['decision_id']}={rec['option_id']} ({' '.join(label.split())}) "
            f"note={_q(rec.get('note'))} at {local_time(rec.get('ts'))}{ident}")


class Watcher:
    """Tails the ledger by byte offset and turns each new complete line into one output line.

    Prints PICK, SKIP (skip lines), COMMENT and DONE lines as each lands; the agent's own status and reply
    lines are not echoed. ALL_PICKED is emitted once, the first time every spec decision has a pick; later changes
    still print. A truncated or replaced ledger (smaller than the offset, or a new inode) starts over from the top.
    """

    def __init__(self, ledger: Path, spec: dict | None):
        self.ledger = Path(ledger)
        self.spec = spec
        self._reset()

    def _reset(self) -> None:
        self.offset = 0
        self.inode = None
        self.seen: dict[str, dict] = {}
        self.rids: set = set()          # user actions already printed; a retried duplicate prints nothing
        self.announced = False          # ALL_PICKED already emitted

    @property
    def all_picked(self) -> bool:
        return self.spec is not None and not open_decisions(self.spec, self.seen)

    def poll(self) -> list[str]:
        try:
            st = self.ledger.stat()
        except FileNotFoundError:
            return []
        if st.st_size < self.offset or (self.inode is not None and st.st_ino != self.inode):
            self._reset()
        self.inode = st.st_ino
        out = []
        if st.st_size > self.offset:
            with self.ledger.open("rb") as fh:
                fh.seek(self.offset)
                chunk = fh.read(st.st_size - self.offset)
            end = chunk.rfind(b"\n")     # only complete lines; a partial one waits for the next poll
            if end >= 0:
                self.offset += end + 1
                for raw in chunk[: end + 1].splitlines():
                    rec = parse_line(raw.decode("utf-8", "replace"))
                    if rec is None or not fresh(rec, self.rids) or rec["kind"] in ("status", "reply"):
                        continue
                    if self.spec is not None and not in_spec(self.spec, rec):
                        continue
                    if rec["kind"] == "pick":
                        self.seen[rec["decision_id"]] = rec
                    out.append(format_pick_line(rec, self.spec))
        if self.all_picked and not self.announced:
            out.append("ALL_PICKED")
            self.announced = True
        return out
