"""A stand-in for the real `claude` binary in the runner tests (installed as `<tmp>/fakebin/claude`).

It records the PATH it was started with and which `gws`, `claude`, `sim` and `python3` that PATH reaches (what the
session's Bash tool would reach), into FAKE_CLAUDE_LOG, then replays FAKE_AIM_REPLAY like the fake aim does.
"""
import json
import os
import shutil
import sys
import time


def main():
    log = os.environ.get("FAKE_CLAUDE_LOG")
    if log:
        seen = {name: shutil.which(name) for name in ("gws", "claude", "sim", "python3", "aim")}
        with open(log, "a") as fh:
            fh.write(json.dumps({"argv": sys.argv, "path": os.environ.get("PATH"), "which": seen}) + "\n")
    replay = os.environ.get("FAKE_AIM_REPLAY")
    if not replay:
        return 0
    with open(replay, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            try:
                obj = json.loads(line)
            except ValueError:
                obj = None
            if isinstance(obj, dict) and "t" in obj and ("e" in obj or "raw" in obj):
                line = obj["raw"] if "raw" in obj else json.dumps(obj["e"])
            sys.stdout.write(line + "\n")
            sys.stdout.flush()
            time.sleep(0.002)
    return 0


if __name__ == "__main__":
    sys.exit(main())
