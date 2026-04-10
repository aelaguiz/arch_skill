#!/usr/bin/env python3
"""Install or verify the arch-step automatic controller Stop hook in Codex hooks.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


STATUS_MESSAGE = (
    "arch-step automatic controller is running; planning continuations are quick, fresh implement-loop audits can take a few minutes"
)
HOOK_SCRIPT_NAME = "implement_loop_stop_hook.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hooks-file", required=True)
    parser.add_argument("--skills-dir", required=True)
    parser.add_argument("--verify", action="store_true")
    return parser.parse_args()


def expected_command(skills_dir: Path) -> str:
    hook_script = skills_dir / "arch-step" / "scripts" / HOOK_SCRIPT_NAME
    return f"python3 {hook_script}"


def load_hooks_file(hooks_file: Path) -> dict:
    if not hooks_file.exists():
        return {"hooks": {}}
    try:
        data = json.loads(hooks_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"failed to parse {hooks_file}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{hooks_file} must contain a top-level JSON object")
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise SystemExit(f"{hooks_file} must contain an object at hooks")
    return data


def is_arch_step_group(group: object) -> bool:
    if not isinstance(group, dict):
        return False
    hooks = group.get("hooks")
    if not isinstance(hooks, list):
        return False
    for hook in hooks:
        if not isinstance(hook, dict):
            continue
        command = str(hook.get("command", ""))
        if hook.get("statusMessage") == STATUS_MESSAGE or command.endswith(HOOK_SCRIPT_NAME):
            return True
    return False


def expected_group(command: str) -> dict:
    return {
        "hooks": [
            {
                "type": "command",
                "command": command,
                "timeoutSec": 1200,
                "statusMessage": STATUS_MESSAGE,
            }
        ]
    }


def install_hook(hooks_file: Path, skills_dir: Path) -> None:
    data = load_hooks_file(hooks_file)
    stop_groups = data["hooks"].get("Stop", [])
    if stop_groups is None:
        stop_groups = []
    if not isinstance(stop_groups, list):
        raise SystemExit(f"{hooks_file} must contain a list at hooks.Stop")

    command = expected_command(skills_dir)
    stop_groups = [group for group in stop_groups if not is_arch_step_group(group)]
    stop_groups.append(expected_group(command))
    data["hooks"]["Stop"] = stop_groups

    hooks_file.parent.mkdir(parents=True, exist_ok=True)
    hooks_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def verify_hook(hooks_file: Path, skills_dir: Path) -> None:
    if not hooks_file.exists():
        raise SystemExit(f"missing hooks file: {hooks_file}")
    data = load_hooks_file(hooks_file)
    stop_groups = data["hooks"].get("Stop", [])
    if not isinstance(stop_groups, list):
        raise SystemExit(f"{hooks_file} must contain a list at hooks.Stop")

    command = expected_command(skills_dir)
    wanted = expected_group(command)
    for group in stop_groups:
        if group == wanted:
            return
    raise SystemExit(
        "missing arch-step automatic controller Stop hook entry in "
        f"{hooks_file}; expected command: {command}"
    )


def main() -> int:
    args = parse_args()
    hooks_file = Path(args.hooks_file).expanduser()
    skills_dir = Path(args.skills_dir).expanduser()
    if args.verify:
        verify_hook(hooks_file, skills_dir)
    else:
        install_hook(hooks_file, skills_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
