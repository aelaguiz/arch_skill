#!/usr/bin/env python3
"""Alert Amir about an accepted watcher escalation.

Sends a macOS notification, plays a sound, posts to Slack when configured,
and appends one line to ~/.agent-watcher/alerts.jsonl. Prints one line
saying which channels succeeded.

Slack: set AGENT_WATCHER_SLACK_TARGET (a channel id or user id) in
~/.config/agent-watcher/env. The bot token is read from
~/workspace/secrets/slack_data_foundation.env (SLACK_BOT_TOKEN_DATA_FOUNDATION)
or the environment. Nothing is printed from either file.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True  # keep installed skill dirs free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watcher_lib as W  # noqa: E402

ENV_FILE = Path.home() / ".config" / "agent-watcher" / "env"
SLACK_ENV = Path.home() / "workspace" / "secrets" / "slack_data_foundation.env"
SOUND = "/System/Library/Sounds/Glass.aiff"


def read_env_file(p: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not p.exists():
        return out
    for line in p.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip().removeprefix("export ").strip()
        out[k] = v.strip().strip('"').strip("'")
    return out


def desktop(title: str, message: str) -> str:
    esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
    try:
        subprocess.run(["osascript", "-e", f'display notification "{esc(message)}" with title "{esc(title)}"'],
                       check=True, capture_output=True, timeout=10)
        return "ok"
    except (subprocess.SubprocessError, FileNotFoundError) as exc:
        return f"failed({type(exc).__name__})"


def sound() -> str:
    try:
        if Path(SOUND).exists():
            subprocess.Popen(["afplay", SOUND], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "ok"
        sys.stdout.write("\a")
        return "bell"
    except (OSError, subprocess.SubprocessError) as exc:
        return f"failed({type(exc).__name__})"


def slack(title: str, message: str, detail: str | None) -> str:
    cfg = read_env_file(ENV_FILE)
    target = os.environ.get("AGENT_WATCHER_SLACK_TARGET") or cfg.get("AGENT_WATCHER_SLACK_TARGET")
    if not target:
        return "skipped(no AGENT_WATCHER_SLACK_TARGET)"
    token = os.environ.get("SLACK_BOT_TOKEN_DATA_FOUNDATION") or read_env_file(SLACK_ENV).get("SLACK_BOT_TOKEN_DATA_FOUNDATION")
    if not token:
        return "skipped(no token)"
    text = f"*{title}*\n{message}" + (f"\n`{detail}`" if detail else "")
    body = json.dumps({"channel": target, "text": text, "unfurl_links": False, "unfurl_media": False}).encode()
    req = urllib.request.Request("https://slack.com/api/chat.postMessage", data=body,
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        return "ok" if data.get("ok") else f"failed({data.get('error', 'unknown')})"
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as exc:
        return f"failed({type(exc).__name__})"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--message", required=True, help="one line, under 200 characters, leads with what Amir would act on")
    ap.add_argument("--title", default="Agent watcher")
    ap.add_argument("--detail", default=None, help="path to the escalation packet, appended to Slack and the log")
    ap.add_argument("--session", default=None, help="session key for the log")
    ap.add_argument("--dedup-key", default=None, help="stable key for this drift/halt so repeats can be suppressed")
    ap.add_argument("--no-desktop", action="store_true")
    ap.add_argument("--no-sound", action="store_true")
    ap.add_argument("--no-slack", action="store_true")
    ap.add_argument("--suppressed", action="store_true", help="log only; do not notify (adjudicator rejected or duplicate)")
    ap.add_argument("--log", default=str(W.STATE_ROOT / "alerts.jsonl"))
    args = ap.parse_args(argv)

    results: dict[str, str] = {}
    if not args.suppressed:
        if not args.no_desktop:
            results["desktop"] = desktop(args.title, args.message)
        if not args.no_sound:
            results["sound"] = sound()
        if not args.no_slack:
            results["slack"] = slack(args.title, args.message, args.detail)
    log = Path(args.log).expanduser()
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a") as fh:
        fh.write(json.dumps({"ts": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "title": args.title,
                             "message": args.message, "session": args.session, "dedup_key": args.dedup_key,
                             "detail": args.detail, "suppressed": bool(args.suppressed), "results": results},
                            ensure_ascii=False) + "\n")
    state = "suppressed" if args.suppressed else " ".join(f"{k}={v}" for k, v in results.items())
    print(f"notified {state} log={W.short_path(log)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
