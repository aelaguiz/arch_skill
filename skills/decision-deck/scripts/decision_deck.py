#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Decision deck: the owner answers a round of approvals and decisions one per slide; each click lands in a ledger.

Subcommands serve, watch, status, act, reply, text and asks; the spec format, the ledger records and the server
routes are in decision_deck_help.py, printed by --help. Modules: decision_deck_spec.py (spec), decision_deck_ledger.py
(records, watcher), decision_deck_server.py and decision_deck_routes.py (HTTP), decision_deck_render.py and
decision_deck_deck.py (the page), decision_deck_diff.py, decision_deck_marks.py, decision_deck_inline.py and
decision_deck_chart.py (evidence), decision_deck_css.py and decision_deck_css_stage.py (the look),
decision_deck_script.py and its parts (the page script), decision_deck_core.py (shared guards), decision_deck_stamp.py (the check stamp), decision_deck_text.py (the
deck's words as plain text, for a fresh reader), decision_deck_act.py (act, for one or several decisions),
decision_deck_reply.py (the text copy of each ask). decision_deck_check.py renders a round in headless Chromium and
reports what breaks the fit rule; run it before showing a deck.
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import signal
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_core import (  # noqa: E402
    DEFAULT_GRACE_MIN, DEFAULT_HOST, DEFAULT_MAX_HOURS, append_pick, decision_by_id, open_decisions,
    read_server_state, server_running, state_path, validate_bind_host)
from decision_deck_help import HELP  # noqa: E402
from decision_deck_ledger import (  # noqa: E402
    Watcher, current_comment, current_picks, current_skips, deck_state, format_pick_line, format_state_line,
    make_reply, read_records)
from decision_deck_server import make_server, remove_own_state  # noqa: E402
from decision_deck_spec import SpecError, load_spec  # noqa: E402
from decision_deck_stamp import serve_gate  # noqa: E402


# ------------------------------------------------------------------ CLI

def _load_or_exit(path) -> dict:
    try:
        return load_spec(path)
    except SpecError as exc:
        sys.stderr.write(f"{exc}\n")
        raise SystemExit(2)


def _ledger_for(args) -> Path:
    if args.ledger:
        return Path(args.ledger).expanduser()
    if getattr(args, "spec", None):
        return Path(args.spec).expanduser().resolve().parent / "ledger.jsonl"
    raise SystemExit("--ledger is required when --spec is not given")


class _Terminated(Exception):
    """Raised by the SIGTERM handler, so `kill <pid>` unwinds through cmd_serve's cleanup like Ctrl-C."""


def _raise_terminated(signum, frame):
    raise _Terminated()


def cmd_serve(args) -> int:
    spec = _load_or_exit(args.spec)
    try:
        host = validate_bind_host(args.host)
    except ValueError as exc:
        sys.stderr.write(f"decision_deck serve: {exc}\n")
        return 2
    if not serve_gate(spec, args.require_checked):     # a CLEAN check stamp; without one a warning, or a refusal
        return 2
    ledger = _ledger_for(args)
    signal.signal(signal.SIGTERM, _raise_terminated)   # before the state file exists, so an early TERM cleans up too
    srv, reason = None, ""
    try:
        source = (args.source or "").strip()
        srv = make_server(spec, ledger, host, args.port, grace_s=args.grace_min * 60, max_s=args.max_hours * 3600,
                          source=source)
        print(f"URL {srv.url}", flush=True)
        print(f"PID {os.getpid()}  ledger {ledger.resolve()}  state {state_path(ledger).resolve()}", flush=True)
        srv.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        reason = "interrupted"
    except _Terminated:
        reason = (srv.reason if srv else "") or "terminated"
    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)   # a second TERM must not skip the cleanup below
        if srv is not None:
            with srv.lock:                              # no pick lands once the state file is gone
                srv.finished.set()
            srv.server_close()
        remove_own_state(ledger)
    print(f"STOPPED {reason or (srv.reason if srv else '') or 'shut down'}", flush=True)
    return 0


def cmd_watch(args) -> int:
    spec = _load_or_exit(args.spec) if args.spec else None
    ledger = _ledger_for(args)
    w = Watcher(ledger, spec)
    if args.from_end and "ALL_PICKED" in w.poll():  # the picks already there count but are not printed
        print("ALL_PICKED", flush=True)
    seen_server = False
    deadline = time.monotonic() + args.max_hours * 3600
    while True:
        running = server_running(ledger)    # read before the poll, so every pick a stopped server wrote is read
        seen_server = seen_server or running
        for line in w.poll():
            print(line, flush=True)
        if not running and (seen_server or w.all_picked):
            remaining = open_decisions(spec, w.seen) if spec is not None else []
            print("SERVER_STOPPED" + (f" open={','.join(remaining)}" if remaining else ""), flush=True)
            return 0
        if time.monotonic() >= deadline:
            print("WATCH_TIMEOUT", flush=True)
            return 3
        time.sleep(args.poll)


def cmd_status(args) -> int:
    spec = _load_or_exit(args.spec)
    records = read_records(_ledger_for(args))
    latest, skips = current_picks(spec, records), current_skips(spec, records)
    remaining = open_decisions(spec, latest)
    state = deck_state(spec, records)["decisions"]
    if args.json:
        states = {did: {"state": d["status"], "result": d.get("result") or ""}
                  for did, d in state.items() if d["status"]}
        print(json.dumps({"picked": latest, "skipped": skips, "open": remaining, "all_picked": not remaining,
                          "states": states}, indent=2, ensure_ascii=False))
        return 0
    print(f"{spec['title']}: {len(latest)} of {len(spec['decisions'])} picked")
    for dec in spec["decisions"]:
        rec = latest.get(dec["id"])
        print(format_pick_line(rec, spec) if rec else f"OPEN {dec['id']} ({dec['title']})")
        if state[dec["id"]]["status"]:      # what the agent reported doing about it
            print(format_state_line(dec["id"], state[dec["id"]]))
        if dec["id"] in skips:      # a note saved after any pick; the decision is unchanged
            print(format_pick_line(skips[dec["id"]], spec))
    return 0


def _send(args, kind: str, payload: dict, record: dict) -> str:
    """POST one agent line (status or reply) to the running server (token from its state file); else append it to
    the ledger.

    Both carry one request id, so a line the server landed although its answer never came back, then appended
    here as well, still reads once (decision_deck_ledger.read_records drops the repeat)."""
    ledger = _ledger_for(args)
    rid = "s" + secrets.token_hex(12)
    payload, record = dict(payload, rid=rid), dict(record, rid=rid)
    state = read_server_state(ledger)
    if server_running(ledger) and state.get("url") and state.get("token"):
        req = urllib.request.Request(
            state["url"] + "api/status", data=json.dumps(dict(payload, kind=kind)).encode(), method="POST",
            headers={"Content-Type": "application/json", "X-Deck-Token": state["token"]})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return "server"
        except (urllib.error.URLError, OSError) as exc:     # a closing or unreachable server: the ledger still takes it
            sys.stderr.write(f"decision_deck {kind}: server refused ({exc}); writing to the ledger\n")
    append_pick(ledger, record)
    return "ledger"


def cmd_reply(args) -> int:
    spec = _load_or_exit(args.spec)
    try:
        if decision_by_id(spec, args.decision)[1] is None:
            raise ValueError(f"unknown decision {args.decision!r}")
        rec = make_reply(spec, args.decision, args.text,
                         current_comment(spec, read_records(_ledger_for(args)), args.decision))
    except ValueError as exc:
        sys.stderr.write(f"decision_deck reply: {exc}\n")
        return 2
    payload = {"decision_id": rec["decision_id"], "text": rec["text"], "comment_ts": rec.get("comment_ts")}
    via = _send(args, "reply", payload, rec)
    print(f"REPLY {rec['decision_id']} text={json.dumps(rec['text'], ensure_ascii=False)} via {via}", flush=True)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="decision_deck.py", description=HELP, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("serve", help="serve the deck and record every answer and comment",
                       description="Serve the round as one deck page and append each answer and comment to the "
                                   "ledger. Prints 'URL <url>', then 'PID <pid>  ledger <path>  state <path>', and "
                                   "'STOPPED <reason>' when it ends. Run it in the background and open the URL in a "
                                   "browser on a machine that can reach the bind address. A spec with no matching "
                                   "check stamp (decision_deck_check.py CLEAN) gets one stderr warning and is served "
                                   "anyway; --require-checked refuses it. Exit 2 for a bad spec, a refused bind "
                                   "address or a refused unchecked spec.")
    s.add_argument("--spec", required=True, help="spec JSON; images resolve relative to its folder")
    s.add_argument("--ledger", help="JSONL ledger (default: ledger.jsonl beside the spec)")
    s.add_argument("--host", default=DEFAULT_HOST,
                   help="bind address (default 127.0.0.1): loopback or a private-network address (10.0.0.0/8, "
                        "172.16.0.0/12, 192.168.0.0/16, 100.64.0.0/10, fc00::/7) so a phone or another machine on "
                        "that network can open the deck; an IP address, or localhost for 127.0.0.1; 0.0.0.0, ::, "
                        "public addresses and other names are refused")
    s.add_argument("--port", type=int, default=0, help="port (default 0 = a free port, printed in the URL)")
    s.add_argument("--grace-min", type=float, default=DEFAULT_GRACE_MIN,
                   help="minutes to keep serving after the last pick, status or reply made while no decision "
                        "is open (default 15)")
    s.add_argument("--max-hours", type=float, default=DEFAULT_MAX_HOURS,
                   help="maximum lifetime in hours (default 24)")
    s.add_argument("--source", metavar="TEXT",
                   help="a line under the title in the header bar saying where the deck comes from, such as the "
                        "project or agent asking (default: none)")
    s.add_argument("--require-checked", action="store_true",
                   help="refuse (exit 2) a spec without a check stamp matching its bytes and pictures; without it "
                        "such a spec gets one stderr warning and is served")
    s.set_defaults(func=cmd_serve)

    w = sub.add_parser("watch", help="print one line per new pick, comment or Done, for a background watcher",
                       description="Tail the ledger and print, flushed per line as each record lands: 'PICK "
                                   "<decision>=<option> (<label>) note=\"...\" at <time> pick=<ts>' per pick "
                                   "(<time> in this machine's time zone; <ts> names that pick for act --pick-ts), "
                                   "'COMMENT <decision> note=\"...\" at <time>' per comment (empty note = cleared; "
                                   "the decision stays open), 'DONE open=<ids or none> at <time>' when the owner "
                                   "presses Done, and 'SKIP <decision> note=\"...\" at <time>' for a skip line. "
                                   "Records already in the ledger come first unless --from-end. The agent's own "
                                   "status and reply lines are not echoed; records whose decision or option is not "
                                   "in --spec are ignored. With --spec: print ALL_PICKED once, the first time every "
                                   "decision has a pick, and keep printing every later change. The server counts as "
                                   "not running when <ledger stem>.server.json is absent or its pid is dead. Exit 0 "
                                   "with SERVER_STOPPED once a server this watch saw running has stopped, or (with "
                                   "--spec) once every decision is picked and no server is running; with --spec, "
                                   "decisions still open then are named on that line as 'SERVER_STOPPED open=<ids>'. "
                                   "With no server ever seen and decisions open, keep waiting. Without --spec: no "
                                   "ALL_PICKED and no open list. Exits 3 with WATCH_TIMEOUT at --max-hours. A ledger that does not exist "
                                   "yet is waited for; a truncated or replaced one is read again from the top.")
    w.add_argument("--ledger", help="JSONL ledger (default: ledger.jsonl beside --spec); may not exist yet")
    w.add_argument("--spec", help="spec JSON; enables labels from the spec and ALL_PICKED")
    w.add_argument("--poll", type=float, default=0.5, help="seconds between ledger checks (default 0.5)")
    w.add_argument("--from-end", action="store_true",
                   help="do not print the picks already in the ledger; they still count, so ALL_PICKED prints at "
                        "once when they already cover every decision")
    w.add_argument("--max-hours", type=float, default=DEFAULT_MAX_HOURS, help="give up after this long (default 24)")
    w.set_defaults(func=cmd_watch)

    st = sub.add_parser("status", help="latest pick per decision and the open ones",
                        description="Print the latest pick per decision, a STATE line for what the agent "
                                    "reported doing about it, a COMMENT (or, for a skip line, SKIP) line for any note "
                                    "newer than that pick, and the decisions still open. --json keys: picked, "
                                    "skipped, open, all_picked, and states ({decision id: {state, result}} for each "
                                    "decision the agent reported on, the same as the STATE lines).")
    st.add_argument("--spec", required=True, help="spec JSON")
    st.add_argument("--ledger", help="JSONL ledger (default: ledger.jsonl beside the spec)")
    st.add_argument("--json", action="store_true", help="machine-readable output")
    st.set_defaults(func=cmd_status)

    from decision_deck_act import add_act_parser
    add_act_parser(sub, _load_or_exit, _ledger_for, _send)

    r = sub.add_parser("reply", help="the agent answers a comment",
                       description="Append a reply line for one decision; the slide shows it under the comment it "
                                   "answers (the one shown when this runs) and drops it once that comment changes. "
                                   "Through the running server, else straight to the ledger. Prints 'REPLY "
                                   "<decision> text=\"...\" via server|ledger'. Exit 2 for a bad spec or decision "
                                   "or empty text.")
    r.add_argument("decision", help="decision id")
    r.add_argument("--spec", required=True, help="spec JSON")
    r.add_argument("--ledger", help="JSONL ledger (default: ledger.jsonl beside the spec)")
    r.add_argument("--text", required=True, help="the reply")
    r.set_defaults(func=cmd_reply)

    from decision_deck_text import add_text_parser
    add_text_parser(sub, _load_or_exit)
    from decision_deck_reply import add_asks_parser
    add_asks_parser(sub, _load_or_exit)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
