"""A stand-in for `aim` in the runner tests. Never launches a model.

Installed as `<tmp>/fakebin/aim` (with this interpreter in its shebang) and passed to the runner explicitly. Behaviour
comes from environment variables:

    FAKE_AIM_LOG       append one JSON line per call: argv, cwd, selected env, whether stdin is a TTY, what it read
    FAKE_AIM_STATUS    file printed for `aim claude status --json` (exit 1, like aim with any unhealthy account)
    FAKE_AIM_MODE      replay (default) | exec | busy | noeligible | hang | limited; `exec` does what aim does with a
                       session: finds `claude` on its own PATH and execs it with the arguments after `--`
    FAKE_AIM_BUSY      comma-separated labels refused as busy (in replay mode)
    FAKE_AIM_REPLAY    stream-json file to replay (stamped {"t","e"} / {"t","raw"} lines or raw lines)
    FAKE_AIM_DELAY     seconds between lines (default 0.005)
    FAKE_AIM_PAUSE_AT  "INDEX:SECONDS": sleep before emitting line INDEX
    FAKE_AIM_WRITES    JSON list of {"at": INDEX, "file": REL_PATH, "text": TEXT}: append TEXT to the file (relative
                       to the working directory) just before emitting line INDEX
    FAKE_AIM_CHILD     file to write the pid of a `sleep 120` grandchild into (hang mode)
    FAKE_AIM_RUN       a shell command run in the working directory before replaying (the session's PATH, so
                       `notify` and `sim` are the run's wrappers), when the prompt contains FAKE_AIM_RUN_IF
"""
import json
import os
import subprocess
import sys
import time

WATCHED_ENV = ("PATH", "HOME", "CLAUDE_CODE_DISABLE_AUTO_MEMORY", "CLAUDE_CODE_DISABLE_CLAUDE_MDS",
               "ENABLE_CLAUDEAI_MCP_SERVERS", "CLAUDE_CODE_DISABLE_BUNDLED_SKILLS", "CLAUDE_CODE_DISABLE_ARTIFACT",
               "CLAUDE_CODE_DISABLE_WORKFLOWS", "CLAUDE_CODE_DISABLE_CRON")


def record(extra=None):
    path = os.environ.get("FAKE_AIM_LOG")
    if not path:
        return
    try:
        data = sys.stdin.read()
    except (OSError, ValueError):
        data = None
    entry = {"argv": sys.argv, "cwd": os.getcwd(), "env": {k: os.environ.get(k) for k in WATCHED_ENV},
             "stdin_isatty": os.isatty(0) if sys.stdin else None, "stdin_data": data, "pid": os.getpid(),
             "pgid": os.getpgid(0)}
    entry.update(extra or {})
    with open(path, "a") as fh:
        fh.write(json.dumps(entry) + "\n")


def lines_to_emit(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            try:
                obj = json.loads(line)
            except ValueError:
                out.append(line)
                continue
            if isinstance(obj, dict) and "t" in obj and ("e" in obj or "raw" in obj):
                out.append(obj["raw"] if "raw" in obj else json.dumps(obj["e"]))
            else:
                out.append(line)
    return out


def main():
    args = sys.argv[1:]
    if args[:3] == ["claude", "status", "--json"]:
        record()
        with open(os.environ["FAKE_AIM_STATUS"]) as fh:
            sys.stdout.write(fh.read())
        return 1
    if args[:2] != ["claude", "run"]:
        sys.stderr.write("fake aim: unsupported command\n")
        return 2
    label = args[2]
    record({"label": label})
    mode = os.environ.get("FAKE_AIM_MODE", "replay")
    busy = [x for x in os.environ.get("FAKE_AIM_BUSY", "").split(",") if x]
    if mode == "busy" or label in busy:
        sys.stderr.write(f'Claude account "{label}" is busy: another AIM process or machine is using or refreshing it. '
                         "Nothing started here. Wait up to one minute, then try again.\n")
        return 1
    if mode == "exec":
        import shutil

        claude = shutil.which("claude")
        if not claude:
            sys.stderr.write("Could not resolve the installed Claude executable for offline managed launch.\n")
            return 1
        rest = args[args.index("--") + 1:] if "--" in args else []
        os.execv(claude, [claude] + rest)
    if mode == "noeligible":
        sys.stderr.write("no_eligible_pool_account: no Claude account is selectable\n")
        return 1
    if mode == "hang":
        child = subprocess.Popen(["sleep", "120"])
        with open(os.environ["FAKE_AIM_CHILD"], "w") as fh:
            fh.write(str(child.pid))
        sys.stdout.write(json.dumps({"type": "system", "subtype": "init", "tools": []}) + "\n")
        sys.stdout.flush()
        time.sleep(120)
        return 0
    prompt = args[args.index("-p") + 1] if "-p" in args else ""
    if os.environ.get("FAKE_AIM_RUN") and os.environ.get("FAKE_AIM_RUN_IF", "") in prompt:
        subprocess.run(os.environ["FAKE_AIM_RUN"], shell=True, cwd=os.getcwd(), stdout=subprocess.DEVNULL)
    delay = float(os.environ.get("FAKE_AIM_DELAY", "0.005"))
    pause_at, pause_s = None, 0.0
    if os.environ.get("FAKE_AIM_PAUSE_AT"):
        index, seconds = os.environ["FAKE_AIM_PAUSE_AT"].split(":")
        pause_at, pause_s = int(index), float(seconds)
    writes = json.loads(os.environ.get("FAKE_AIM_WRITES", "[]"))
    lines = lines_to_emit(os.environ["FAKE_AIM_REPLAY"])
    if mode == "limited":
        lines.insert(1, json.dumps({"type": "rate_limit_event", "rate_limit_info": {"status": "rejected"}}))
    for index, line in enumerate(lines):
        if index == pause_at:
            time.sleep(pause_s)
        for write in writes:
            if write["at"] == index:
                with open(write["file"], "a") as fh:
                    fh.write(write["text"])
                time.sleep(write.get("sleep", 0.0))
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
        time.sleep(delay)
    return 0


if __name__ == "__main__":
    sys.exit(main())
