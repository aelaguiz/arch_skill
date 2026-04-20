#!/usr/bin/env python3
"""Install or verify the arch_skill SessionStart hook in Claude settings.json.

The SessionStart hook caches the Claude session id to disk the moment the CLI
boots, so later parent turns can resolve it via `--current-session`. The install
path holds an exclusive fcntl.flock on the target settings file so concurrent
arms from parallel sessions serialize their read-modify-write.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path


HOOK_SCRIPT_NAME = "arch_controller_stop_hook.py"
HOOK_TIMEOUT_SEC = 10000
COMMAND_SUFFIX = "--session-start-cache"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--settings-file", required=True)
    parser.add_argument("--skills-dir", required=True)
    parser.add_argument("--verify", action="store_true")
    return parser.parse_args()


def expected_command(skills_dir: Path) -> str:
    hook_script = skills_dir / "arch-step" / "scripts" / HOOK_SCRIPT_NAME
    return f"python3 {hook_script} {COMMAND_SUFFIX}"


def command_mentions_repo_runner(command: str) -> bool:
    if COMMAND_SUFFIX not in command:
        return False
    return any(part.endswith(HOOK_SCRIPT_NAME) for part in command.split())


def load_settings_file(settings_file: Path) -> dict:
    if not settings_file.exists():
        return {"hooks": {}}
    raw_text = settings_file.read_text(encoding="utf-8")
    if not raw_text.strip():
        return {"hooks": {}}
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"failed to parse {settings_file}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{settings_file} must contain a top-level JSON object")
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise SystemExit(f"{settings_file} must contain an object at hooks")
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
        if hook.get("type") != "command":
            continue
        command = str(hook.get("command", ""))
        if command_mentions_repo_runner(command):
            return True
    return False


def repo_managed_groups(start_groups: list[object]) -> list[dict]:
    return [group for group in start_groups if is_repo_managed_group(group)]


def expected_group(command: str) -> dict:
    return {
        "hooks": [
            {
                "type": "command",
                "command": command,
                "timeout": HOOK_TIMEOUT_SEC,
            }
        ]
    }


def _open_for_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return open(path, "a+", encoding="utf-8")


def install_hook(settings_file: Path, skills_dir: Path) -> None:
    with _open_for_lock(settings_file) as lock_fd:
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
        data = load_settings_file(settings_file)
        start_groups = data["hooks"].get("SessionStart", [])
        if start_groups is None:
            start_groups = []
        if not isinstance(start_groups, list):
            raise SystemExit(f"{settings_file} must contain a list at hooks.SessionStart")

        command = expected_command(skills_dir)
        start_groups = [group for group in start_groups if not is_repo_managed_group(group)]
        start_groups.append(expected_group(command))
        data["hooks"]["SessionStart"] = start_groups

        write_json_file(settings_file, data)


def verify_hook(settings_file: Path, skills_dir: Path) -> None:
    if not settings_file.exists():
        raise SystemExit(f"missing Claude settings file: {settings_file}")
    data = load_settings_file(settings_file)
    start_groups = data["hooks"].get("SessionStart", [])
    if not isinstance(start_groups, list):
        raise SystemExit(f"{settings_file} must contain a list at hooks.SessionStart")

    command = expected_command(skills_dir)
    wanted = expected_group(command)
    managed_groups = repo_managed_groups(start_groups)
    if not managed_groups:
        raise SystemExit(
            "missing arch_skill SessionStart hook entry in "
            f"{settings_file}; expected command: {command}. "
            "Run `make install` or `arch_controller_stop_hook.py --ensure-installed --runtime claude`."
        )
    if len(managed_groups) != 1:
        raise SystemExit(
            "arch_skill: multiple SessionStart hook entries found in "
            f"{settings_file}; expected exactly one matching: {command}. "
            "Remove the extras manually and rerun install."
        )
    if managed_groups[0] != wanted:
        raise SystemExit(
            "arch_skill: stale SessionStart hook entry in "
            f"{settings_file}; expected command: {command}. "
            "Remove the stale entry manually and rerun install."
        )


def main() -> int:
    args = parse_args()
    settings_file = Path(args.settings_file).expanduser()
    skills_dir = Path(args.skills_dir).expanduser()
    if args.verify:
        verify_hook(settings_file, skills_dir)
    else:
        install_hook(settings_file, skills_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
