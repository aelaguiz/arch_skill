#!/usr/bin/env python3
"""Extract events from one coding-agent transcript, incrementally.

Modes:
  anchor  every message from the human plus the restatement surfaces (goal,
          heartbeat, compaction goal, spawn) from the start of the file. Use
          once, when a watcher first meets a session. Returns the EOF cursor.
  since   every event after --cursor (a byte offset), in one bounded page.
          Use on every later check. Returns the new cursor.
  tail    the last N events, read from the end. Use to see current activity
          on a large session without processing its backlog.

Read-only. Prints a header line plus bounded rows; writes the full page to
~/.agent-watcher/sessions/<key>/events/ (or --out DIR).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep installed skill dirs free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watcher_lib as W  # noqa: E402

ROW_LIMITS = {"USER": 900, "USER_INTERRUPT": 300, "USER_QUEUED": 600, "ASSISTANT": 220, "TOOL": 160,
              "GOAL": 500, "HEARTBEAT": 400, "COMPACTION": 400, "SPAWN": 300, "AGENT_MSG": 300,
              "AWAY_SUMMARY": 300, "TASK_COMPLETE": 260, "CHILD_NOTICE": 200, "ASK": 300, "TOOL_ERROR": 160,
              "ABORTED": 80, "META": 160}


def infer_runtime(path: Path) -> str | None:
    s = str(path)
    if "/.codex/" in s:
        return "codex"
    if "/.claude/" in s:
        return "claude"
    if "/.prime/" in s or "/.pi/" in s:
        return "prime"
    return None


def key_for(runtime: str, path: Path, events: list[dict]) -> str:
    sid = None
    for ev in events:
        if ev["kind"] == "META" and ev.get("session_id"):
            sid = ev["session_id"]
            break
    if not sid:
        m = re.search(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$", path.stem)
        sid = m.group(1) if m else path.stem
    return W.session_key(runtime, sid)


def row(ev: dict) -> str:
    kind = ev["kind"]
    lim = ROW_LIMITS.get(kind, 200)
    name = f" {ev['name']}" if ev.get("name") else ""
    extra = ""
    if kind == "META":
        bits = [f"{k}={ev[k]}" for k in ("cwd", "model", "approval", "sandbox", "mode", "session_id") if ev.get(k)]
        extra = " " + " ".join(bits)
    text = W.squash(ev.get("text", ""), lim)
    ts = ev.get("ts", "")[11:19] if ev.get("ts") else "--:--:--"
    return f"{ts} {kind}{name}{extra} | {text}".rstrip(" |")


def summarize(events: list[dict]) -> str:
    u = sum(1 for e in events if e["kind"] in W.USER_KINDS)
    a = sum(1 for e in events if e["kind"] == "ASSISTANT")
    t = sum(1 for e in events if e["kind"] in ("TOOL", "SPAWN"))
    o = len(events) - u - a - t
    return f"{len(events)} events (user {u}, assistant {a}, tool {t}, other {o})"


def span(events: list[dict]) -> str:
    tss = [e["ts"] for e in events if e.get("ts")]
    if not tss:
        return "no timestamps"
    return f"{tss[0][:16]}..{tss[-1][:16]}"


def write_page(out_dir: Path, mode: str, start: int, end: int, events: list[dict]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"{mode}-{start}-{end}.jsonl"
    with open(p, "w") as fh:
        for ev in events:
            fh.write(json.dumps(ev, ensure_ascii=False) + "\n")
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("anchor", "since", "tail"))
    ap.add_argument("--path", required=True, help="transcript file")
    ap.add_argument("--runtime", choices=W.RUNTIMES, help="inferred from the path when omitted")
    ap.add_argument("--cursor", type=int, default=0, help="byte offset to resume from (since)")
    ap.add_argument("--limit", type=int, default=80, help="rows to print (default 80)")
    ap.add_argument("--max-bytes", type=int, default=40_000_000, help="max bytes to read per since page (default 40MB)")
    ap.add_argument("--tail-bytes", type=int, default=3_000_000, help="bytes to read from the end for tail (default 3MB)")
    ap.add_argument("--tail-events", type=int, default=40, help="events to keep for tail (default 40)")
    ap.add_argument("--anchor-users", type=int, default=60, help="max human messages to print in anchor (default 60)")
    ap.add_argument("--out", default=None, help="directory for the full page (default ~/.agent-watcher/sessions/<key>/events)")
    ap.add_argument("--kinds", default=None, help="comma list to print, e.g. USER,ASSISTANT (file keeps everything)")
    args = ap.parse_args(argv)

    path = Path(args.path).expanduser()
    if not path.exists():
        print(f"ERROR session_events: no such file {path}")
        return 2
    runtime = args.runtime or infer_runtime(path)
    if not runtime:
        print("ERROR session_events: cannot infer runtime; pass --runtime")
        return 2
    size = path.stat().st_size
    events: list[dict] = []
    start = 0
    end = size
    more = False

    if args.mode == "anchor":
        seen_user: list[str] = []
        for off, nxt, line in W.iter_lines(path, 0):
            if not W.line_may_anchor(runtime, line):
                end = nxt
                continue
            obj = W.load_json(line)
            end = nxt
            if not obj:
                continue
            for ev in W.classify(runtime, obj):
                if ev["kind"] in W.USER_KINDS:
                    sig = ev["text"][:200]
                    if sig in seen_user[-3:]:
                        continue  # Codex records the same prompt twice
                    seen_user.append(sig)
                    events.append(ev)
                elif ev["kind"] in W.RESTATEMENT_KINDS or ev["kind"] == "META":
                    events.append(ev)
    elif args.mode == "since":
        start = max(0, min(args.cursor, size))
        end = start
        seen_user: list[str] = []
        for off, nxt, line in W.iter_lines(path, start, args.max_bytes):
            obj = W.load_json(line)
            end = nxt
            if not obj:
                continue
            for ev in W.classify(runtime, obj):
                if ev["kind"] in W.USER_KINDS:
                    sig = ev["text"][:200]
                    if sig in seen_user[-3:]:
                        continue
                    seen_user.append(sig)
                events.append(ev)
        more = end < size
    else:  # tail
        lines = W.tail_lines(path, args.tail_bytes)
        start = max(0, size - args.tail_bytes)
        for line in lines:
            obj = W.load_json(line)
            if not obj:
                continue
            events.extend(W.classify(runtime, obj))
        events = events[-args.tail_events:]

    key = key_for(runtime, path, events) if args.mode == "anchor" else key_for(runtime, path, [])
    out_dir = Path(args.out).expanduser() if args.out else W.session_dir(key) / "events"
    page = write_page(out_dir, args.mode, start, end, events)

    last = W.last_meaningful(runtime, W.tail_lines(path, 200_000))
    last_ts = W.parse_ts(last["ts"]) if last and last.get("ts") else None
    header = (f"OK session_events {args.mode} [{runtime}] {key}: {summarize(events)}; span {span(events)}; "
              f"last event {last['kind'] if last else '?'} {W.age_str(last_ts)} ago; cursor {end}"
              + ("; MORE REMAINS" if more else "") + f"; file {W.short_path(page)}")
    print(header)

    kinds = set(args.kinds.split(",")) if args.kinds else None
    printable = [e for e in events if (kinds is None or e["kind"] in kinds)]
    if args.mode == "anchor":
        metas: list[dict] = []
        seen_meta: set[str] = set()
        for e in printable:
            if e["kind"] == "META":
                sig = e.get("name", "") + "|" + "|".join(str(e.get(k, "")) for k in ("cwd", "model", "approval", "mode"))
                if sig not in seen_meta:
                    seen_meta.add(sig)
                    metas.append(e)
        for e in metas[:6]:
            print(row(e))
        users = [e for e in printable if e["kind"] in W.USER_KINDS]
        restate = [e for e in printable if e["kind"] in W.RESTATEMENT_KINDS]
        shown_users = users[: args.anchor_users]
        restate_cap = max(0, args.limit - len(shown_users))
        shown_restate = restate[:restate_cap]
        merged = sorted(shown_users + shown_restate, key=lambda e: e.get("ts", ""))
        for e in merged:
            print(row(e))
        if len(users) > len(shown_users):
            print(f"… {len(users) - len(shown_users)} more human messages in {W.short_path(page)}")
        if len(restate) > len(shown_restate):
            print(f"… {len(restate) - len(shown_restate)} more goal/heartbeat/compaction/spawn events in {W.short_path(page)}")
    else:
        for e in printable[: args.limit]:
            print(row(e))
        if len(printable) > args.limit:
            print(f"… {len(printable) - args.limit} more in {W.short_path(page)}")
    if more:
        print(f"next page: python3 {W.short_path(Path(__file__))} since --path {W.short_path(path)} --cursor {end}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
