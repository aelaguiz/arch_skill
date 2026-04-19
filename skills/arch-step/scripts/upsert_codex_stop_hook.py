#!/usr/bin/env python3
"""Install or verify the unified arch_skill Stop hook in Codex hooks.json."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


STATUS_MESSAGE = (
    "arch_skill automatic controllers are running; planning continuations are quick, fresh reviews or docs evaluations can take a few minutes, and delay polls can wait much longer"
)
# Legacy signatures are repair handles only: install collapses any matching
# arch_skill-managed Stop entries to one current runner, and verify rejects a
# managed entry unless it exactly matches expected_group().
LEGACY_STATUS_MESSAGES = {
    "arch_skill automatic controllers are running; planning continuations are quick, fresh audits or docs evaluations can take a few minutes, and delay polls can wait much longer",
    "arch_skill automatic controllers are running; planning continuations are quick, and fresh audits or docs evaluations can take a few minutes",
    "arch suite automatic controller is running; planning continuations are quick, and fresh audits or docs evaluations can take a few minutes",
    "arch-step automatic controller is running; planning continuations are quick, fresh implement-loop audits can take a few minutes",
    "audit-loop automatic controller is running; fresh review passes can take a few minutes",
}
HOOK_SCRIPT_NAME = "arch_controller_stop_hook.py"
HOOK_TIMEOUT_SEC = 90000
HOOK_RUNTIME = "codex"
LEGACY_HOOK_SCRIPT_NAMES = {
    "implement_loop_stop_hook.py",
    "audit_loop_stop_hook.py",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hooks-file", required=True)
    parser.add_argument("--skills-dir", required=True)
    parser.add_argument("--verify", action="store_true")
    return parser.parse_args()


def expected_command(skills_dir: Path) -> str:
    hook_script = skills_dir / "arch-step" / "scripts" / HOOK_SCRIPT_NAME
    return f"python3 {hook_script} --runtime {HOOK_RUNTIME}"


def command_mentions_repo_runner(command: str) -> bool:
    command_parts = command.split()
    return any(
        part.endswith(HOOK_SCRIPT_NAME)
        or any(part.endswith(script_name) for script_name in LEGACY_HOOK_SCRIPT_NAMES)
        for part in command_parts
    )


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


def write_json_file(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def is_repo_managed_group(group: object) -> bool:
    if not isinstance(group, dict):
        return False
    hooks = group.get("hooks")
    if not isinstance(hooks, list):
        return False
    for hook in hooks:
        if not isinstance(hook, dict):
            continue
        command = str(hook.get("command", ""))
        status_message = hook.get("statusMessage")
        if (
            status_message == STATUS_MESSAGE
            or status_message in LEGACY_STATUS_MESSAGES
            or command_mentions_repo_runner(command)
        ):
            return True
    return False


def repo_managed_groups(stop_groups: list[object]) -> list[dict]:
    return [group for group in stop_groups if is_repo_managed_group(group)]


def expected_group(command: str) -> dict:
    return {
        "hooks": [
            {
                "type": "command",
                "command": command,
                "timeoutSec": HOOK_TIMEOUT_SEC,
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
    stop_groups = [group for group in stop_groups if not is_repo_managed_group(group)]
    stop_groups.append(expected_group(command))
    data["hooks"]["Stop"] = stop_groups

    write_json_file(hooks_file, data)


def verify_hook(hooks_file: Path, skills_dir: Path) -> None:
    if not hooks_file.exists():
        raise SystemExit(f"missing hooks file: {hooks_file}")
    data = load_hooks_file(hooks_file)
    stop_groups = data["hooks"].get("Stop", [])
    if not isinstance(stop_groups, list):
        raise SystemExit(f"{hooks_file} must contain a list at hooks.Stop")

    command = expected_command(skills_dir)
    wanted = expected_group(command)
    managed_groups = repo_managed_groups(stop_groups)
    if not managed_groups:
        raise SystemExit(
            "missing arch_skill automatic controller Stop hook entry in "
            f"{hooks_file}; expected command: {command}"
        )
    if len(managed_groups) != 1:
        raise SystemExit(
            "expected exactly one arch_skill-managed Stop hook entry in "
            f"{hooks_file}; found {len(managed_groups)}. Rerun install to remove stale runner paths."
        )
    if managed_groups[0] != wanted:
        raise SystemExit(
            "stale arch_skill Stop hook entry still exists in "
            f"{hooks_file}; expected command: {command}. Rerun install to repair the runner path."
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
