#!/usr/bin/env python3
"""Extract user-typed prompts from Codex, Claude Code, and Prime stores on this machine.

Read-only. Never touches auth.json. Writes JSONL to stdout:
{machine, runtime, home, session, ts, cwd, text, pasted}
"""
import glob
import json
import os
import socket
import sys
from datetime import datetime

HOME = os.path.expanduser("~")
MACHINE = socket.gethostname().split(".")[0]
MAX_TEXT = 12000


def emit(runtime, home, session, ts, cwd, text, pasted=""):
    if not text and not pasted:
        return
    sys.stdout.write(json.dumps({
        "machine": MACHINE, "runtime": runtime, "home": home, "session": session,
        "ts": ts, "cwd": cwd, "text": (text or "")[:MAX_TEXT], "pasted": (pasted or "")[:MAX_TEXT],
    }) + "\n")


def iso(ts):
    try:
        if ts > 1e11:
            ts = ts / 1000
        return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


def codex():
    # Codex thread cwd lookup from state db, if present.
    cwds = {}
    db = os.path.join(HOME, ".codex", "state_5.sqlite")
    if os.path.exists(db):
        try:
            import sqlite3
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            for tid, cwd in con.execute("select id, cwd from threads"):
                cwds[tid] = cwd
        except Exception:
            pass
    path = os.path.join(HOME, ".codex", "history.jsonl")
    if not os.path.exists(path):
        return
    for line in open(path, errors="replace"):
        try:
            d = json.loads(line)
        except Exception:
            continue
        sid = d.get("session_id") or d.get("conversation_id")
        emit("codex", "~/.codex", sid, iso(d.get("ts", 0)), cwds.get(sid), d.get("text", ""))


def claude():
    homes = [os.path.join(HOME, ".claude")] + sorted(glob.glob(os.path.join(HOME, ".aimgr", "claude-homes", "*", ".claude")))
    seen = set()
    for h in homes:
        real = os.path.realpath(h)
        if real in seen:
            continue
        seen.add(real)
        path = os.path.join(h, "history.jsonl")
        if not os.path.exists(path):
            continue
        label = h.replace(HOME, "~")
        for line in open(path, errors="replace"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            pasted = []
            for v in (d.get("pastedContents") or {}).values():
                if isinstance(v, dict):
                    c = v.get("content")
                    if not c and v.get("contentHash"):
                        p = os.path.join(h, "paste-cache", v["contentHash"] + ".txt")
                        if os.path.exists(p):
                            try:
                                c = open(p, errors="replace").read()
                            except Exception:
                                c = None
                    if c:
                        pasted.append(c)
            emit("claude", label, d.get("sessionId"), iso(d.get("timestamp", 0)), d.get("project"),
                 d.get("display", ""), "\n---\n".join(pasted))


def prime():
    for root in [os.path.join(HOME, ".prime", "agent", "sessions"), os.path.join(HOME, ".pi", "agent", "sessions")]:
        runtime = "prime" if ".prime" in root else "pi"
        for path in glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True):
            if path.endswith("-debug.jsonl"):
                continue
            try:
                f = open(path, errors="replace")
                head = json.loads(f.readline())
            except Exception:
                continue
            if head.get("type") != "session" or head.get("rlmDepth", 0) not in (0, None):
                continue
            sid, cwd = head.get("id"), head.get("cwd")
            for line in f:
                if '"role":"user"' not in line and '"role": "user"' not in line and "session_slash_command" not in line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("type") == "message" and d.get("message", {}).get("role") == "user":
                    content = d["message"].get("content")
                    if isinstance(content, str):
                        text = content
                    else:
                        text = "\n".join(b.get("text", "") for b in content or [] if b.get("type") == "text")
                    emit(runtime, "~/." + runtime, sid, d.get("timestamp"), cwd, text)


if __name__ == "__main__":
    for fn in (codex, claude, prime):
        try:
            fn()
        except Exception as e:
            sys.stderr.write(f"{fn.__name__}: {e}\n")
