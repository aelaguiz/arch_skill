#!/usr/bin/env python3
"""arch-epic orchestration plumbing.

This script is deterministic infrastructure for the arch-epic skill.
It does NOT make judgments about decomposition, scope changes,
verdicts, or routing. Those decisions live in the orchestrator's
prose reasoning.

Subcommands:

  critic-spawn   Spawn a fresh ephemeral critic sub-session (claude
                 or codex), capture the EpicVerdict JSON, and write
                 run-directory artifacts.
  resolve-execution
                 Resolve automatic-mode role execution policy.
  auto-init      Create an automatic-mode run directory and state.json.
  worker-spawn   Spawn a resumable automatic-mode worker sub-session.
  worker-resume  Resume an automatic-mode worker sub-session.
  auto-critic-spawn
                 Spawn a structured critic inside an automatic-mode run.
  auto-status    Print compact automatic-mode state.
  report-scaffold
                 Write or print a deterministic automatic-mode report.
  child-status   Classify a spawned child from process state and stream recency.
  child-tail     Print the latest child stream lines.
  child-wait     Wait with long-run polling expectations.
  child-finalize Parse completed child output into session/verdict artifacts.

The script exits non-zero with a plain-English message whenever its
expected output shape does not appear. It never swallows errors.
"""

from __future__ import annotations

import argparse
import json
import os
import selectors
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SHARED_DIR = Path(__file__).resolve().parents[2] / "_shared"
if str(_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_DIR))

from model_resolution import (  # noqa: E402
    ModelResolutionError,
    resolve_role_execution_policy,
)


REQUIRED_AUTO_ROLE_GROUPS = [
    "epic_planner",
    "implementation_worker",
    "critic",
]
LEGACY_AUTO_ROLE_GROUPS = [
    "repair_worker",
]
AUTO_ROLE_GROUPS = REQUIRED_AUTO_ROLE_GROUPS + LEGACY_AUTO_ROLE_GROUPS
DEFAULT_AUTO_POLL_SECONDS = 180
DEFAULT_QUIET_FLOOR_SECONDS = 900
DEFAULT_STUCK_FLOOR_SECONDS = 1800
DEFAULT_CHILD_MAX_RUNTIME_SECONDS = 7200
LONG_RUNNING_AUTO_ROLES = {"epic_planner", "implementation_worker", "repair_worker"}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def _die(msg: str, code: int = 2) -> None:
    print(f"run_arch_epic: {msg}", file=sys.stderr)
    sys.exit(code)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, payload) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _die(f"JSON file not found: {path}")
    except json.JSONDecodeError as e:
        _die(f"JSON file is not valid JSON: {path}: {e}")


def _shell_quote(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"


def _write_invocation_sh(path: Path, argv: list[str], cwd: str | None) -> None:
    line = " ".join(_shell_quote(a) for a in argv)
    prefix = f"cd {_shell_quote(cwd)} && " if cwd else ""
    _write_text(
        path, "#!/bin/sh\n" + prefix + "exec " + line + " < /dev/null\n"
    )
    path.chmod(0o755)


def _ensure_arch_epic_gitignore_marker(orch_root: Path) -> None:
    """Ignore arch-epic run logs without hiding other .arch_skill content."""

    gi = orch_root / ".gitignore"
    marker = ".arch_skill/arch-epic/"
    old_marker = ".arch_skill/"
    if not gi.exists():
        gi.write_text(f"{marker}\n", encoding="utf-8")
        return

    lines = gi.read_text(encoding="utf-8").splitlines()
    new_lines: list[str] = []
    changed = False
    for line in lines:
        if line == old_marker:
            if marker not in new_lines:
                new_lines.append(marker)
            changed = True
        else:
            new_lines.append(line)

    if marker not in new_lines:
        new_lines.append(marker)
        changed = True

    if changed:
        gi.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")


def _run_subprocess(
    argv: list[str],
    stdout_stream_path: Path,
    out_dir: Path,
    cwd: str | None = None,
    *,
    detached: bool = False,
) -> tuple[int, str]:
    """Run a child with stdin closed and durable live output artifacts."""
    if detached:
        return _spawn_detached_subprocess(argv, stdout_stream_path, out_dir, cwd=cwd)

    _write_text(out_dir / "start_ts", _utc_now_iso())
    events_path = out_dir / "events.jsonl"
    stderr_path = out_dir / "stderr.log"
    stdout_stream_path.write_text("", encoding="utf-8")
    events_path.write_text("", encoding="utf-8")
    stderr_path.write_text("", encoding="utf-8")

    stdout_parts: list[str] = []
    with open(os.devnull, "rb") as devnull:
        proc = subprocess.Popen(
            argv,
            stdin=devnull,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            text=True,
            bufsize=1,
        )
        _write_text(out_dir / "child.pid", str(proc.pid) + "\n")
        heartbeat = {
            "pid": proc.pid,
            "status": "running",
            "started_at": _utc_now_iso(),
            "last_output_at": None,
            "last_event_at": None,
            "last_event_kind": None,
            "event_count": 0,
            "output_bytes": 0,
            "mode": "foreground",
        }
        _write_json(out_dir / "heartbeat.json", heartbeat)

        sel = selectors.DefaultSelector()
        if proc.stdout is not None:
            sel.register(proc.stdout, selectors.EVENT_READ, "stdout")
        if proc.stderr is not None:
            sel.register(proc.stderr, selectors.EVENT_READ, "stderr")

        with open(stdout_stream_path, "a", encoding="utf-8") as stream, open(
            events_path, "a", encoding="utf-8"
        ) as events, open(stderr_path, "a", encoding="utf-8") as stderr_file:

            def handle_line(source: str, line: str) -> None:
                now = _utc_now_iso()
                heartbeat["last_output_at"] = now
                heartbeat["output_bytes"] = int(heartbeat["output_bytes"]) + len(
                    line.encode("utf-8", errors="replace")
                )
                if source == "stdout":
                    stdout_parts.append(line)
                    events.write(line)
                    events.flush()
                    stream.write(line)
                    stream.flush()
                    heartbeat["event_count"] = int(heartbeat["event_count"]) + 1
                    heartbeat["last_event_at"] = now
                    heartbeat["last_event_kind"] = _classify_event_line(line)
                else:
                    stderr_file.write(line)
                    stderr_file.flush()
                    stream.write("[stderr] " + line)
                    stream.flush()
                _write_json(out_dir / "heartbeat.json", heartbeat)

            while True:
                selected = sel.select(timeout=0.25)
                for key, _ in selected:
                    line = key.fileobj.readline()
                    if not line:
                        try:
                            sel.unregister(key.fileobj)
                        except Exception:
                            pass
                        continue
                    handle_line(key.data, line)

                if proc.poll() is not None:
                    for key in list(sel.get_map().values()):
                        for line in key.fileobj.readlines():
                            handle_line(key.data, line)
                        try:
                            sel.unregister(key.fileobj)
                        except Exception:
                            pass
                    break

        code = proc.wait()
        if proc.stdout is not None:
            proc.stdout.close()
        if proc.stderr is not None:
            proc.stderr.close()

    _write_text(out_dir / "end_ts", _utc_now_iso())
    _write_text(out_dir / "exit_code", str(code) + "\n")
    heartbeat["status"] = "completed" if code == 0 else "failed"
    heartbeat["ended_at"] = _utc_now_iso()
    heartbeat["exit_code"] = code
    _write_json(out_dir / "heartbeat.json", heartbeat)
    _write_json(out_dir / "monitor.json", _child_status(out_dir))
    return code, "".join(stdout_parts)


def _spawn_detached_subprocess(
    argv: list[str],
    stdout_stream_path: Path,
    out_dir: Path,
    cwd: str | None = None,
) -> tuple[int, str]:
    """Start a long-running child without keeping this orchestrator blocked.

    The wrapper owns stdout/stderr redirection, so `events.jsonl`,
    `stderr.log`, and `stream.log` keep growing after this Python process exits.
    `child-status` reads those artifacts later instead of guessing from a
    missing final file.
    """

    events_path = out_dir / "events.jsonl"
    stderr_path = out_dir / "stderr.log"
    runner_path = out_dir / "detached-runner.sh"
    for path in [stdout_stream_path, events_path, stderr_path]:
        path.write_text("", encoding="utf-8")
    _write_text(out_dir / "start_ts", _utc_now_iso())

    command = " ".join(_shell_quote(a) for a in argv)
    lines = [
        "#!/bin/bash",
        "set +e",
    ]
    if cwd:
        lines.extend(
            [
                f"if ! cd {_shell_quote(cwd)}; then",
                "  code=127",
                "  date -u '+%Y-%m-%dT%H:%M:%SZ' > "
                + _shell_quote(str(out_dir / "end_ts")),
                "  printf '%s\\n' \"$code\" > "
                + _shell_quote(str(out_dir / "exit_code")),
                "  exit \"$code\"",
                "fi",
            ]
        )
    lines.extend(
        [
            "date -u '+%Y-%m-%dT%H:%M:%SZ' > "
            + _shell_quote(str(out_dir / "start_ts")),
            f": > {_shell_quote(str(stdout_stream_path))}",
            f": > {_shell_quote(str(events_path))}",
            f": > {_shell_quote(str(stderr_path))}",
            "(",
            "  "
            + command
            + " < /dev/null "
            + f"> >(tee -a {_shell_quote(str(events_path))} >> {_shell_quote(str(stdout_stream_path))}) "
            + f"2> >(tee -a {_shell_quote(str(stderr_path))} | sed 's/^/[stderr] /' >> {_shell_quote(str(stdout_stream_path))})",
            ")",
            "code=$?",
            "date -u '+%Y-%m-%dT%H:%M:%SZ' > "
            + _shell_quote(str(out_dir / "end_ts")),
            "printf '%s\\n' \"$code\" > " + _shell_quote(str(out_dir / "exit_code")),
            "exit \"$code\"",
            "",
        ]
    )
    _write_text(runner_path, "\n".join(lines))
    runner_path.chmod(0o755)

    with open(os.devnull, "rb") as devnull, open(os.devnull, "wb") as devnull_out:
        proc = subprocess.Popen(
            ["/bin/bash", str(runner_path)],
            stdin=devnull,
            stdout=devnull_out,
            stderr=devnull_out,
            start_new_session=True,
        )

    _write_text(out_dir / "child.pid", str(proc.pid) + "\n")
    heartbeat = {
        "pid": proc.pid,
        "status": "running",
        "started_at": _utc_now_iso(),
        "last_output_at": None,
        "last_event_at": None,
        "last_event_kind": None,
        "event_count": 0,
        "output_bytes": 0,
        "mode": "detached",
    }
    _write_json(out_dir / "heartbeat.json", heartbeat)
    _write_json(out_dir / "monitor.json", _child_status(out_dir))
    return 0, ""


def _classify_event_line(line: str) -> str:
    try:
        ev = json.loads(line)
    except json.JSONDecodeError:
        return "stdout"
    event_type = ev.get("type")
    nested = ev.get("event")
    if isinstance(nested, dict) and isinstance(nested.get("type"), str):
        event_type = f"{event_type}:{nested['type']}" if event_type else nested["type"]
    lowered = json.dumps(ev, sort_keys=True).lower()
    if any(token in lowered for token in ["tool_use", "tool_result", "bash", "command_execution"]):
        return "tool"
    if any(token in lowered for token in ["thinking", "assistant", "agent_message", "message_delta"]):
        return "assistant"
    return str(event_type or "event")


def _parse_utc_iso(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        ).timestamp()
    except ValueError:
        return None


def _read_optional_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return None


def _read_optional_int(path: Path) -> int | None:
    text = _read_optional_text(path)
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _pid_running(pid: int | None) -> bool:
    if pid is None or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _latest_activity_ts(child_dir: Path) -> float | None:
    latest: float | None = None
    for name in [
        "stream.log",
        "events.jsonl",
        "stderr.log",
        "stdout.final.json",
        "verdict.json",
    ]:
        path = child_dir / name
        if not path.exists():
            continue
        mtime = path.stat().st_mtime
        latest = mtime if latest is None else max(latest, mtime)
    return latest


def _event_stats(child_dir: Path) -> dict[str, Any]:
    events_path = child_dir / "events.jsonl"
    count = 0
    last_type = None
    last_kind = None
    if events_path.exists():
        with open(events_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                count += 1
                last_kind = _classify_event_line(line)
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                last_type = ev.get("type")
                nested = ev.get("event")
                if isinstance(nested, dict) and isinstance(nested.get("type"), str):
                    last_type = f"{last_type}:{nested['type']}" if last_type else nested["type"]
    stream_path = child_dir / "stream.log"
    stderr_path = child_dir / "stderr.log"
    return {
        "event_count": count,
        "last_event_type": last_type,
        "last_event_kind": last_kind,
        "stream_bytes": stream_path.stat().st_size if stream_path.exists() else 0,
        "stderr_bytes": stderr_path.stat().st_size if stderr_path.exists() else 0,
    }


def _child_status(
    child_dir: Path,
    *,
    quiet_floor_seconds: int = DEFAULT_QUIET_FLOOR_SECONDS,
    stuck_floor_seconds: int = DEFAULT_STUCK_FLOOR_SECONDS,
    max_runtime_seconds: int = DEFAULT_CHILD_MAX_RUNTIME_SECONDS,
    now: float | None = None,
) -> dict[str, Any]:
    now = time.time() if now is None else now
    pid = _read_optional_int(child_dir / "child.pid")
    exit_code = _read_optional_int(child_dir / "exit_code")
    start_ts = _parse_utc_iso(_read_optional_text(child_dir / "start_ts"))
    end_ts = _parse_utc_iso(_read_optional_text(child_dir / "end_ts"))
    latest_activity = _latest_activity_ts(child_dir)
    runtime_seconds = None
    if start_ts is not None:
        runtime_seconds = int((end_ts or now) - start_ts)
    silence_seconds = None
    if latest_activity is not None:
        silence_seconds = int(now - latest_activity)
    running = _pid_running(pid) and exit_code is None
    reason = None

    if exit_code is not None:
        state = "completed" if exit_code == 0 else "failed"
        reason = "exit_code_recorded"
    elif pid is None:
        state = "missing_process"
        reason = "no_child_pid_recorded"
    elif running:
        if runtime_seconds is not None and runtime_seconds > max_runtime_seconds:
            state = "needs_attention"
            reason = "max_runtime_exceeded_without_exit"
        elif silence_seconds is None:
            state = "running"
            reason = "process_alive_no_output_yet"
        elif silence_seconds <= quiet_floor_seconds:
            state = "running"
            reason = "recent_stream_activity"
        elif silence_seconds <= stuck_floor_seconds:
            state = "quiet"
            reason = "no_recent_stream_activity_but_within_long_run_floor"
        else:
            state = "needs_attention"
            reason = "no_stream_activity_past_stuck_floor"
    else:
        state = "process_exited_without_exit_code"
        reason = "pid_not_running_and_no_exit_code"

    stats = _event_stats(child_dir)
    return {
        "state": state,
        "reason": reason,
        "pid": pid,
        "process_running": running,
        "exit_code": exit_code,
        "runtime_seconds": runtime_seconds,
        "silence_seconds": silence_seconds,
        "quiet_floor_seconds": quiet_floor_seconds,
        "stuck_floor_seconds": stuck_floor_seconds,
        "max_runtime_seconds": max_runtime_seconds,
        "last_activity_at": datetime.fromtimestamp(latest_activity, timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        if latest_activity is not None
        else None,
        **stats,
    }


def _tail_file(path: Path, lines: int) -> str:
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(content[-lines:]) + ("\n" if content else "")


def _select_child_run_mode(
    *,
    requested: str,
    expected_duration: str,
    kind: str,
    role: str | None = None,
) -> str:
    if requested in {"foreground", "detached"}:
        return requested
    if expected_duration == "short":
        return "foreground"
    if expected_duration == "long":
        return "detached"
    if kind == "worker" and role in LONG_RUNNING_AUTO_ROLES:
        return "detached"
    return "foreground"


def _extract_claude_result_event(payload: Any) -> dict | None:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list):
        for ev in reversed(payload):
            if isinstance(ev, dict) and ev.get("type") == "result":
                return ev
    return None


def _parse_claude_result_event(stdout_text: str) -> dict | None:
    try:
        payload = json.loads(stdout_text.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return None
    return _extract_claude_result_event(payload)


def _parse_claude_session_id(stdout_text: str) -> str | None:
    event = _parse_claude_result_event(stdout_text)
    if event is None:
        return None
    sid = event.get("session_id")
    return sid if isinstance(sid, str) and sid else None


def _parse_codex_thread_id(stdout_text: str) -> str | None:
    for line in stdout_text.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "thread.started" and isinstance(
            ev.get("thread_id"), str
        ):
            return ev["thread_id"]
    return None


def _parse_claude_final_json(stdout_text: str) -> dict | None:
    """Return Claude's final result event from JSON or stream-json stdout.

    In current Claude Code, `--output-format stream-json` emits JSONL and
    finishes with a `type=result` event. Older JSON mode printed a single
    object. Accept both shapes so old artifacts remain readable.
    """
    return _parse_claude_result_event(stdout_text)


def _extract_claude_structured_verdict(final: dict) -> dict | None:
    """Return the critic's structured verdict from a Claude `-p --output-format
    json --json-schema ...` response.

    Claude populates `structured_output` reliably when the model answers
    in one shot. When the critic uses tools (reading files) before
    answering, Claude sometimes returns the conforming JSON as text in
    `result` (often wrapped in ```json fences). Accept either path.
    """
    so = final.get("structured_output")
    if isinstance(so, dict):
        return so
    result = final.get("result")
    if not isinstance(result, str):
        return None
    text = result.strip()
    if text.startswith("```"):
        # strip opening fence (with optional language tag) and closing fence
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    try:
        obj = json.loads(text.strip())
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def _slugify(name: str) -> str:
    out = []
    for ch in name.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in ("_", "-", " "):
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "sub-plan"


def _policy_from_file(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    if not isinstance(payload, dict):
        _die("execution policy input must be a JSON object")
    roles = payload.get("roles")
    if not isinstance(roles, dict):
        _die("execution policy input must contain object field: roles")
    missing = [role for role in REQUIRED_AUTO_ROLE_GROUPS if role not in roles]
    if missing:
        _die("execution policy missing required role(s): " + ", ".join(missing))
    role_sources: dict[str, str] = {}
    for role in AUTO_ROLE_GROUPS:
        if role not in roles:
            continue
        value = roles.get(role)
        if not isinstance(value, str) or not value.strip():
            _die(f"execution policy role {role!r} must be a non-empty string")
        role_sources[role] = value
    poll_seconds = payload.get("poll_seconds", DEFAULT_AUTO_POLL_SECONDS)
    quiet_floor_seconds = payload.get(
        "quiet_floor_seconds", DEFAULT_QUIET_FLOOR_SECONDS
    )
    stuck_floor_seconds = payload.get(
        "stuck_floor_seconds", DEFAULT_STUCK_FLOOR_SECONDS
    )
    max_runtime_seconds = payload.get(
        "max_runtime_seconds", DEFAULT_CHILD_MAX_RUNTIME_SECONDS
    )
    for key, value in [
        ("poll_seconds", poll_seconds),
        ("quiet_floor_seconds", quiet_floor_seconds),
        ("stuck_floor_seconds", stuck_floor_seconds),
        ("max_runtime_seconds", max_runtime_seconds),
    ]:
        if not isinstance(value, int):
            _die(f"execution policy {key} must be an integer")
    codex_models = payload.get("codex_models")
    if codex_models is not None:
        if not isinstance(codex_models, list) or not all(
            isinstance(item, str) for item in codex_models
        ):
            _die("execution policy codex_models must be an array of strings")
    try:
        return resolve_role_execution_policy(
            role_sources,
            codex_models=codex_models,
            poll_seconds=poll_seconds,
            quiet_floor_seconds=quiet_floor_seconds,
            stuck_floor_seconds=stuck_floor_seconds,
            max_runtime_seconds=max_runtime_seconds,
        )
    except ModelResolutionError as e:
        _die(str(e))


def _auto_run_root(orchestrator_root: Path, epic_doc: Path) -> Path:
    slug = _slugify(epic_doc.stem.removeprefix("EPIC_"))
    return orchestrator_root / ".arch_skill" / "arch-epic" / "auto" / slug


def _read_state(run_dir: Path) -> dict[str, Any]:
    state = _load_json(run_dir / "state.json")
    if not isinstance(state, dict):
        _die(f"state.json must contain a JSON object: {run_dir / 'state.json'}")
    return state


def _state_role_execution(state: dict[str, Any], role: str) -> dict[str, str]:
    policy = state.get("auto_execution")
    if not isinstance(policy, dict):
        _die("auto state is missing auto_execution object")
    roles = policy.get("roles")
    if not isinstance(roles, dict):
        _die("auto_execution is missing roles object")
    block = roles.get(role)
    if not isinstance(block, dict):
        _die(f"auto_execution has no role policy for {role!r}")
    out: dict[str, str] = {}
    for key in ["runtime", "model", "effort"]:
        value = block.get(key)
        if not isinstance(value, str) or not value:
            _die(f"role {role!r} policy missing {key}")
        out[key] = value
    return out


def _display_role_groups(roles: dict[str, Any]) -> list[str]:
    return REQUIRED_AUTO_ROLE_GROUPS + [
        role for role in LEGACY_AUTO_ROLE_GROUPS if role in roles
    ]


def _codex_worker_argv(
    target_repo: Path,
    model: str,
    effort: str,
    final_path: Path,
    prompt: str,
) -> list[str]:
    return [
        "codex",
        "exec",
        "--cd",
        str(target_repo),
        "--disable",
        "codex_hooks",
        "--dangerously-bypass-approvals-and-sandbox",
        "--skip-git-repo-check",
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "--json",
        "-o",
        str(final_path),
        prompt,
    ]


def _claude_worker_argv(
    model: str,
    effort: str,
    prompt: str,
    *,
    session_id: str | None = None,
) -> list[str]:
    argv = [
        "claude",
        "-p",
        "--output-format",
        "stream-json",
        "--include-partial-messages",
        "--include-hook-events",
        "--dangerously-skip-permissions",
        "--settings",
        '{"disableAllHooks":true}',
        "--model",
        model,
        "--effort",
        effort,
    ]
    if session_id:
        argv.extend(["-r", session_id])
    argv.append(prompt)
    return argv


def _codex_worker_resume_argv(
    session_id: str,
    final_path: Path,
    prompt: str,
) -> list[str]:
    return [
        "codex",
        "exec",
        "resume",
        session_id,
        "--disable",
        "codex_hooks",
        "--dangerously-bypass-approvals-and-sandbox",
        "--skip-git-repo-check",
        "--json",
        "-o",
        str(final_path),
        prompt,
    ]


def _codex_critic_argv(
    target_repo: Path,
    model: str,
    effort: str,
    schema_path: Path,
    final_path: Path,
    prompt: str,
) -> list[str]:
    return [
        "codex",
        "exec",
        "--cd",
        str(target_repo),
        "--ephemeral",
        "--disable",
        "codex_hooks",
        "--dangerously-bypass-approvals-and-sandbox",
        "--skip-git-repo-check",
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "--output-schema",
        str(schema_path),
        "--json",
        "-o",
        str(final_path),
        prompt,
    ]


def _claude_critic_argv(
    model: str,
    effort: str,
    schema_inline: str,
    prompt: str,
) -> list[str]:
    return [
        "claude",
        "-p",
        "--output-format",
        "stream-json",
        "--include-partial-messages",
        "--include-hook-events",
        "--dangerously-skip-permissions",
        "--settings",
        '{"disableAllHooks":true}',
        "--model",
        model,
        "--effort",
        effort,
        "--json-schema",
        schema_inline,
        prompt,
    ]


def cmd_resolve_execution(args: argparse.Namespace) -> int:
    policy = _policy_from_file(Path(args.policy_file).resolve())
    if args.output:
        _write_json(Path(args.output).resolve(), policy)
        print(str(Path(args.output).resolve()))
    else:
        print(json.dumps(policy, indent=2, sort_keys=True))
    return 0


def cmd_auto_init(args: argparse.Namespace) -> int:
    epic_doc = Path(args.epic_doc).resolve()
    if not epic_doc.is_file():
        _die(f"epic doc not found: {epic_doc}")
    orchestrator_root = (
        Path(args.orchestrator_root).resolve() if args.orchestrator_root else Path.cwd()
    )
    if not orchestrator_root.is_dir():
        _die(f"orchestrator root is not a directory: {orchestrator_root}")
    _ensure_arch_epic_gitignore_marker(orchestrator_root)
    policy = _policy_from_file(Path(args.policy_file).resolve())
    run_id = _utc_now_stamp()
    run_dir = _auto_run_root(orchestrator_root, epic_doc) / f"run-{run_id}"
    run_dir.mkdir(parents=True, exist_ok=False)
    policy_with_run_dir = dict(policy)
    policy_with_run_dir["auto_run_dir"] = str(run_dir)
    state = {
        "schema_version": 1,
        "run_id": run_id,
        "started_at": _utc_now_iso(),
        "epic_doc": str(epic_doc),
        "orchestrator_root": str(orchestrator_root),
        "status": "active",
        "current_sub_plan": None,
        "auto_execution": policy_with_run_dir,
        "latest_worker_attempts": {},
        "events": [],
    }
    _write_json(run_dir / "state.json", state)
    _write_json(run_dir / "execution_policy.json", policy_with_run_dir)
    print(str(run_dir))
    return 0


def _worker_try_dir(run_dir: Path, role: str, sub_plan_name: str, try_k: int) -> Path:
    return (
        run_dir
        / "workers"
        / role
        / _slugify(sub_plan_name)
        / f"try-{try_k}"
    )


def _critic_run_dir(run_dir: Path, gate: str, sub_plan_name: str) -> Path:
    return (
        run_dir
        / "critics"
        / _slugify(gate)
        / _slugify(sub_plan_name)
        / f"run-{_utc_now_stamp()}"
    )


def _read_child_stdout_text(child_dir: Path) -> str:
    events_path = child_dir / "events.jsonl"
    if events_path.exists():
        return events_path.read_text(encoding="utf-8", errors="replace")
    stream_path = child_dir / "stream.log"
    if stream_path.exists():
        return stream_path.read_text(encoding="utf-8", errors="replace")
    return ""


def _update_metadata(child_dir: Path, updates: dict[str, Any]) -> dict[str, Any]:
    path = child_dir / "metadata.json"
    if path.exists():
        payload = _load_json(path)
        if not isinstance(payload, dict):
            payload = {}
    else:
        payload = {}
    payload.update(updates)
    _write_json(path, payload)
    return payload


def _record_worker_attempt(try_dir: Path, updates: dict[str, Any]) -> None:
    """Persist the latest resumable worker attempt for parent orchestration."""

    try:
        run_dir = try_dir.parents[3]
    except IndexError:
        return
    state_path = run_dir / "state.json"
    if not state_path.exists():
        return
    state = _load_json(state_path)
    if not isinstance(state, dict):
        return
    latest = state.get("latest_worker_attempts")
    if not isinstance(latest, dict):
        latest = {}
        state["latest_worker_attempts"] = latest
    metadata_path = try_dir / "metadata.json"
    metadata = _load_json(metadata_path) if metadata_path.exists() else {}
    if not isinstance(metadata, dict):
        metadata = {}
    role = str(updates.get("role") or metadata.get("role") or "unknown")
    sub_plan_name = str(
        updates.get("sub_plan_name") or metadata.get("sub_plan_name") or "unknown"
    )
    key = f"{role}:{_slugify(sub_plan_name)}"
    current = latest.get(key)
    if not isinstance(current, dict):
        current = {}
    current.update(
        {
            "role": role,
            "sub_plan_name": sub_plan_name,
            "try_dir": str(try_dir),
            "updated_at": _utc_now_iso(),
        }
    )
    current.update(updates)
    latest[key] = current
    _write_json(state_path, state)


def _finalize_worker_try_dir(try_dir: Path) -> str:
    metadata = _load_json(try_dir / "metadata.json")
    if not isinstance(metadata, dict):
        _die(f"metadata.json must contain an object: {try_dir / 'metadata.json'}")
    runtime = metadata.get("runtime")
    final_path = Path(str(metadata.get("final_path", try_dir / "stdout.final.json")))
    input_session_id = metadata.get("input_session_id")
    if not isinstance(input_session_id, str):
        input_session_id = None
    stdout_text = _read_child_stdout_text(try_dir)

    if runtime == "claude":
        final = _parse_claude_result_event(stdout_text)
        if final is None:
            _write_text(try_dir / "session_id.txt", "UNRECOVERABLE\n")
            _die("claude worker stdout did not include a result event; see stream.log", code=3)
        _write_json(final_path, final)
        out_sid = _parse_claude_session_id(stdout_text) or input_session_id
    elif runtime == "codex":
        out_sid = _parse_codex_thread_id(stdout_text) or input_session_id
    else:
        _die(f"unknown worker runtime in metadata: {runtime!r}")

    if not out_sid:
        _write_text(try_dir / "session_id.txt", "UNRECOVERABLE\n")
        _die(f"worker session id not captured (runtime={runtime})", code=4)
    _write_text(try_dir / "session_id.txt", out_sid + "\n")
    _update_metadata(
        try_dir,
        {
            "session_id": out_sid,
            "finalized_at": _utc_now_iso(),
            "finalized": True,
        },
    )
    _record_worker_attempt(
        try_dir,
        {
            "status": "finalized",
            "session_id": out_sid,
            "finalized_at": _utc_now_iso(),
        },
    )
    return out_sid


def _finalize_critic_run_dir(crit_dir: Path) -> Path:
    metadata = _load_json(crit_dir / "metadata.json")
    if not isinstance(metadata, dict):
        _die(f"metadata.json must contain an object: {crit_dir / 'metadata.json'}")
    runtime = metadata.get("runtime")
    final_path = Path(str(metadata.get("final_path", crit_dir / "stdout.final.json")))
    verdict_path = Path(str(metadata.get("verdict_path", crit_dir / "verdict.json")))
    stdout_text = _read_child_stdout_text(crit_dir)

    if runtime == "claude":
        final = _parse_claude_result_event(stdout_text)
        if final is None:
            _die("claude critic stdout did not include a result event; see stream.log", code=3)
        _write_json(final_path, final)
        verdict = _extract_claude_structured_verdict(final)
        if verdict is None:
            _die("claude critic produced no schema-conforming JSON", code=5)
        _write_json(verdict_path, verdict)
    elif runtime == "codex":
        if not final_path.is_file():
            _die(f"codex critic did not write -o file: {final_path}", code=5)
        verdict = _load_json(final_path)
        _write_json(verdict_path, verdict)
    else:
        _die(f"unknown critic runtime in metadata: {runtime!r}")

    _update_metadata(
        crit_dir,
        {
            "finalized_at": _utc_now_iso(),
            "finalized": True,
            "verdict_path": str(verdict_path),
        },
    )
    return verdict_path


def _run_worker(
    *,
    run_dir: Path,
    target_repo: Path,
    role: str,
    sub_plan_name: str,
    prompt_file: Path,
    try_k: int,
    session_id: str | None = None,
    run_mode: str = "auto",
    expected_duration: str = "auto",
) -> int:
    state = _read_state(run_dir)
    execution = _state_role_execution(state, role)
    prompt = prompt_file.read_text(encoding="utf-8")
    try_dir = _worker_try_dir(run_dir, role, sub_plan_name, try_k)
    try_dir.mkdir(parents=True, exist_ok=False)
    _write_text(try_dir / "prompt.md", prompt)
    _write_json(try_dir / "execution.json", execution)
    final_path = try_dir / "stdout.final.json"
    stream_path = try_dir / "stream.log"

    runtime = execution["runtime"]
    if runtime == "claude":
        argv = _claude_worker_argv(
            execution["model"],
            execution["effort"],
            prompt,
            session_id=session_id,
        )
        cwd = str(target_repo)
    elif runtime == "codex":
        if session_id:
            argv = _codex_worker_resume_argv(session_id, final_path, prompt)
        else:
            argv = _codex_worker_argv(
                target_repo,
                execution["model"],
                execution["effort"],
                final_path,
                prompt,
            )
        cwd = None
    else:
        _die(f"unknown worker runtime: {runtime}")

    _write_invocation_sh(try_dir / "invocation.sh", argv, cwd)
    selected_run_mode = _select_child_run_mode(
        requested=run_mode,
        expected_duration=expected_duration,
        kind="worker",
        role=role,
    )
    _write_json(
        try_dir / "metadata.json",
        {
            "kind": "worker",
            "role": role,
            "sub_plan_name": sub_plan_name,
            "try_k": try_k,
            "runtime": runtime,
            "model": execution["model"],
            "effort": execution["effort"],
            "session_id": None,
            "input_session_id": session_id,
            "resumed": session_id is not None,
            "run_mode": selected_run_mode,
            "expected_duration": expected_duration,
            "final_path": str(final_path),
            "stream_path": str(stream_path),
            "events_path": str(try_dir / "events.jsonl"),
            "stderr_path": str(try_dir / "stderr.log"),
            "finalized": False,
        },
    )
    _record_worker_attempt(
        try_dir,
        {
            "status": "running",
            "role": role,
            "sub_plan_name": sub_plan_name,
            "try_k": try_k,
            "resumed": session_id is not None,
            "input_session_id": session_id,
            "started_at": _utc_now_iso(),
        },
    )

    code, _stdout_text = _run_subprocess(
        argv,
        stream_path,
        try_dir,
        cwd=cwd,
        detached=selected_run_mode == "detached",
    )
    if selected_run_mode == "detached":
        print(str(try_dir))
        return 0

    out_sid = _finalize_worker_try_dir(try_dir)
    print(out_sid)
    return 0 if code == 0 else code


def cmd_worker_spawn(args: argparse.Namespace) -> int:
    return _run_worker(
        run_dir=Path(args.run_dir).resolve(),
        target_repo=Path(args.target_repo).resolve(),
        role=args.role,
        sub_plan_name=args.sub_plan_name,
        prompt_file=Path(args.prompt_file).resolve(),
        try_k=args.try_k,
        run_mode=args.run_mode,
        expected_duration=args.expected_duration,
    )


def cmd_worker_resume(args: argparse.Namespace) -> int:
    return _run_worker(
        run_dir=Path(args.run_dir).resolve(),
        target_repo=Path(args.target_repo).resolve(),
        role=args.role,
        sub_plan_name=args.sub_plan_name,
        prompt_file=Path(args.prompt_file).resolve(),
        try_k=args.try_k,
        session_id=args.session_id,
        run_mode=args.run_mode,
        expected_duration=args.expected_duration,
    )


def cmd_auto_critic_spawn(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    target_repo = Path(args.target_repo).resolve()
    state = _read_state(run_dir)
    execution = _state_role_execution(state, args.role)
    schema_path = Path(args.schema_file).resolve()
    if not schema_path.is_file():
        _die(f"critic schema file not found: {schema_path}")
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    crit_dir = _critic_run_dir(run_dir, args.gate, args.sub_plan_name)
    crit_dir.mkdir(parents=True, exist_ok=False)
    _write_text(crit_dir / "prompt.md", prompt)
    _write_json(crit_dir / "execution.json", execution)
    final_path = crit_dir / "stdout.final.json"
    stream_path = crit_dir / "stream.log"
    verdict_path = crit_dir / "verdict.json"

    runtime = execution["runtime"]
    if runtime == "claude":
        schema_inline = json.dumps(
            json.loads(schema_path.read_text(encoding="utf-8")),
            separators=(",", ":"),
        )
        argv = _claude_critic_argv(
            execution["model"],
            execution["effort"],
            schema_inline,
            prompt,
        )
        cwd = str(target_repo)
    elif runtime == "codex":
        argv = _codex_critic_argv(
            target_repo,
            execution["model"],
            execution["effort"],
            schema_path,
            final_path,
            prompt,
        )
        cwd = None
    else:
        _die(f"unknown critic runtime: {runtime}")

    _write_invocation_sh(crit_dir / "invocation.sh", argv, cwd)
    selected_run_mode = _select_child_run_mode(
        requested=args.run_mode,
        expected_duration=args.expected_duration,
        kind="critic",
        role=args.role,
    )
    _write_json(
        crit_dir / "metadata.json",
        {
            "kind": "auto_critic",
            "gate": args.gate,
            "role": args.role,
            "sub_plan_name": args.sub_plan_name,
            "runtime": runtime,
            "model": execution["model"],
            "effort": execution["effort"],
            "run_mode": selected_run_mode,
            "expected_duration": args.expected_duration,
            "final_path": str(final_path),
            "stream_path": str(stream_path),
            "events_path": str(crit_dir / "events.jsonl"),
            "stderr_path": str(crit_dir / "stderr.log"),
            "verdict_path": str(verdict_path),
            "finalized": False,
        },
    )
    code, _stdout_text = _run_subprocess(
        argv,
        stream_path,
        crit_dir,
        cwd=cwd,
        detached=selected_run_mode == "detached",
    )
    if selected_run_mode == "detached":
        print(str(crit_dir))
        return 0

    finalized_verdict_path = _finalize_critic_run_dir(crit_dir)
    print(str(finalized_verdict_path))
    return 0 if code == 0 else code


def cmd_child_status(args: argparse.Namespace) -> int:
    child_dir = Path(args.try_dir).resolve()
    if not child_dir.is_dir():
        _die(f"child run directory not found: {child_dir}")
    status = _child_status(
        child_dir,
        quiet_floor_seconds=args.quiet_floor_seconds,
        stuck_floor_seconds=args.stuck_floor_seconds,
        max_runtime_seconds=args.max_runtime_seconds,
    )
    _write_json(child_dir / "monitor.json", status)
    if args.json:
        print(json.dumps(status, indent=2, sort_keys=True))
    else:
        print(
            f"{status['state']}: pid={status.get('pid')} "
            f"runtime={status.get('runtime_seconds')}s "
            f"silence={status.get('silence_seconds')}s "
            f"events={status.get('event_count')} "
            f"reason={status.get('reason')}"
        )
    return 0


def cmd_child_tail(args: argparse.Namespace) -> int:
    child_dir = Path(args.try_dir).resolve()
    if not child_dir.is_dir():
        _die(f"child run directory not found: {child_dir}")
    print(_tail_file(child_dir / "stream.log", args.lines), end="")
    return 0


def cmd_child_wait(args: argparse.Namespace) -> int:
    child_dir = Path(args.try_dir).resolve()
    if not child_dir.is_dir():
        _die(f"child run directory not found: {child_dir}")
    while True:
        status = _child_status(
            child_dir,
            quiet_floor_seconds=args.quiet_floor_seconds,
            stuck_floor_seconds=args.stuck_floor_seconds,
            max_runtime_seconds=args.max_runtime_seconds,
        )
        _write_json(child_dir / "monitor.json", status)
        print(
            f"{status['state']}: runtime={status.get('runtime_seconds')}s "
            f"silence={status.get('silence_seconds')}s "
            f"events={status.get('event_count')} "
            f"reason={status.get('reason')}"
        )
        if status["state"] == "completed":
            return 0
        if status["state"] in {
            "failed",
            "missing_process",
            "process_exited_without_exit_code",
            "needs_attention",
        }:
            return 1
        time.sleep(args.poll_seconds)


def cmd_child_finalize(args: argparse.Namespace) -> int:
    child_dir = Path(args.try_dir).resolve()
    if not child_dir.is_dir():
        _die(f"child run directory not found: {child_dir}")
    status = _child_status(child_dir)
    if status["state"] not in {"completed", "failed"}:
        _die(f"child is not ready to finalize; current state={status['state']}")
    metadata = _load_json(child_dir / "metadata.json")
    if not isinstance(metadata, dict):
        _die(f"metadata.json must contain an object: {child_dir / 'metadata.json'}")
    kind = metadata.get("kind")
    if kind == "worker":
        print(_finalize_worker_try_dir(child_dir))
    elif kind in {"critic", "auto_critic"}:
        print(str(_finalize_critic_run_dir(child_dir)))
    else:
        _die(f"unknown child kind in metadata: {kind!r}")
    return 0 if status["state"] == "completed" else 1


def cmd_child_terminate(args: argparse.Namespace) -> int:
    child_dir = Path(args.try_dir).resolve()
    pid = _read_optional_int(child_dir / "child.pid")
    if pid is None:
        _die(f"child.pid not found or invalid under {child_dir}")
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    _write_text(child_dir / "terminated_at", _utc_now_iso())
    _write_text(child_dir / "terminate_reason", args.reason.strip() + "\n")
    status = _child_status(child_dir)
    status["state"] = "terminate_requested"
    status["reason"] = args.reason.strip()
    _write_json(child_dir / "monitor.json", status)
    print(f"terminate_requested: pid={pid}")
    return 0


def cmd_auto_status(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = _read_state(run_dir)
    policy = state.get("auto_execution", {})
    roles = policy.get("roles", {}) if isinstance(policy, dict) else {}
    print(f"Run: {run_dir}")
    print(f"Status: {state.get('status', 'unknown')}")
    print(f"Epic doc: {state.get('epic_doc', '')}")
    print(f"Poll seconds: {policy.get('poll_seconds', '') if isinstance(policy, dict) else ''}")
    print(
        "Quiet/stuck/max seconds: "
        f"{policy.get('quiet_floor_seconds', '') if isinstance(policy, dict) else ''}/"
        f"{policy.get('stuck_floor_seconds', '') if isinstance(policy, dict) else ''}/"
        f"{policy.get('max_runtime_seconds', '') if isinstance(policy, dict) else ''}"
    )
    print("Roles:")
    if isinstance(roles, dict):
        for role in _display_role_groups(roles):
            block = roles.get(role, {})
            if isinstance(block, dict):
                print(
                    f"- {role}: {block.get('runtime', '?')} "
                    f"{block.get('model', '?')} {block.get('effort', '?')}"
                )
    return 0


def _render_report(state: dict[str, Any]) -> str:
    policy = state.get("auto_execution", {})
    roles = policy.get("roles", {}) if isinstance(policy, dict) else {}
    lines = [
        "# Arch-Epic Automatic Run Report",
        "",
        f"Run id: {state.get('run_id', '')}",
        f"Status: {state.get('status', '')}",
        f"Epic doc: {state.get('epic_doc', '')}",
        f"Poll seconds: {policy.get('poll_seconds', '') if isinstance(policy, dict) else ''}",
        (
            "Quiet/stuck/max seconds: "
            f"{policy.get('quiet_floor_seconds', '') if isinstance(policy, dict) else ''}/"
            f"{policy.get('stuck_floor_seconds', '') if isinstance(policy, dict) else ''}/"
            f"{policy.get('max_runtime_seconds', '') if isinstance(policy, dict) else ''}"
        ),
        "",
        "## Role Execution",
        "",
        "| Role | Runtime | Model | Effort | Source |",
        "|---|---|---|---|---|",
    ]
    if isinstance(roles, dict):
        for role in _display_role_groups(roles):
            block = roles.get(role, {})
            if isinstance(block, dict):
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            role,
                            str(block.get("runtime", "")),
                            str(block.get("model", "")),
                            str(block.get("effort", "")),
                            str(block.get("source", "")),
                        ]
                    )
                    + " |"
                )
    lines.extend(
        [
            "",
            "## Sub-Plan Status",
            "",
            "- Fill from the epic Decomposition and critic verdict artifacts.",
            "",
            "## Blocking Findings",
            "",
            "- none recorded in this scaffold",
            "",
            "## Artifact Roots",
            "",
            "- workers/: worker prompts, transcripts, and session ids",
            "- critics/: gate verdicts and structured outputs",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def cmd_report_scaffold(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = _read_state(run_dir)
    report = _render_report(state)
    if args.write:
        path = run_dir / "report.md"
        _write_text(path, report)
        print(str(path))
    else:
        print(report, end="")
    return 0


def cmd_critic_spawn(args: argparse.Namespace) -> int:
    epic_doc = Path(args.epic_doc).resolve()
    if not epic_doc.is_file():
        _die(f"epic doc not found: {epic_doc}")

    sub_plan_doc_path = Path(args.sub_plan_doc_path).resolve()
    if not sub_plan_doc_path.is_file():
        _die(f"sub-plan doc not found: {sub_plan_doc_path}")

    schema_path = Path(args.schema_file).resolve()
    if not schema_path.is_file():
        _die(f"critic schema file not found: {schema_path}")

    prompt = Path(args.prompt_file).read_text(encoding="utf-8")

    orch_root = Path(args.orchestrator_root).resolve() if args.orchestrator_root else Path.cwd()
    if not orch_root.is_dir():
        _die(f"orchestrator root is not a directory: {orch_root}")

    slug = _slugify(args.sub_plan_name)
    run_id = _utc_now_stamp()
    run_dir = orch_root / ".arch_skill" / "arch-epic" / "critics" / slug / f"run-{run_id}"
    run_dir.mkdir(parents=True, exist_ok=False)

    _ensure_arch_epic_gitignore_marker(orch_root)

    _write_text(run_dir / "prompt.md", prompt)

    final_path = run_dir / "stdout.final.json"
    stream_path = run_dir / "stream.log"
    verdict_path = run_dir / "verdict.json"

    if args.runtime == "claude":
        # Claude's --json-schema is flaky on multi-line pretty-printed
        # JSON (model may emit prose-wrapped JSON in `result` instead of
        # populating `structured_output`). Minify the schema.
        schema_inline = json.dumps(
            json.loads(schema_path.read_text(encoding="utf-8")),
            separators=(",", ":"),
        )
        argv = _claude_critic_argv(args.model, args.effort, schema_inline, prompt)
        subprocess_cwd = str(orch_root)
    elif args.runtime == "codex":
        argv = _codex_critic_argv(
            orch_root,
            args.model,
            args.effort,
            schema_path,
            final_path,
            prompt,
        )
        subprocess_cwd = None
    else:
        _die(f"unknown runtime: {args.runtime}")

    _write_invocation_sh(run_dir / "invocation.sh", argv, subprocess_cwd)
    selected_run_mode = _select_child_run_mode(
        requested=args.run_mode,
        expected_duration=args.expected_duration,
        kind="critic",
        role="critic",
    )
    _write_json(
        run_dir / "metadata.json",
        {
            "kind": "critic",
            "sub_plan_name": args.sub_plan_name,
            "runtime": args.runtime,
            "model": args.model,
            "effort": args.effort,
            "run_mode": selected_run_mode,
            "expected_duration": args.expected_duration,
            "final_path": str(final_path),
            "stream_path": str(stream_path),
            "events_path": str(run_dir / "events.jsonl"),
            "stderr_path": str(run_dir / "stderr.log"),
            "verdict_path": str(verdict_path),
            "finalized": False,
        },
    )
    code, _stdout_text = _run_subprocess(
        argv,
        stream_path,
        run_dir,
        cwd=subprocess_cwd,
        detached=selected_run_mode == "detached",
    )
    if selected_run_mode == "detached":
        print(str(run_dir))
        return 0

    finalized_verdict_path = _finalize_critic_run_dir(run_dir)
    print(str(finalized_verdict_path))
    return 0 if code == 0 else code


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="run_arch_epic")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_child_run_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--run-mode",
            choices=["auto", "foreground", "detached"],
            default="auto",
            help=(
                "foreground streams until completion; detached returns the child "
                "run directory and leaves stream artifacts growing on disk; auto "
                "uses detached for long worker roles"
            ),
        )
        parser.add_argument(
            "--expected-duration",
            choices=["auto", "short", "long"],
            default="auto",
            help="Duration hint for auto run-mode selection.",
        )

    def add_monitor_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--try-dir", required=True)
        parser.add_argument(
            "--quiet-floor-seconds",
            type=int,
            default=DEFAULT_QUIET_FLOOR_SECONDS,
        )
        parser.add_argument(
            "--stuck-floor-seconds",
            type=int,
            default=DEFAULT_STUCK_FLOOR_SECONDS,
        )
        parser.add_argument(
            "--max-runtime-seconds",
            type=int,
            default=DEFAULT_CHILD_MAX_RUNTIME_SECONDS,
        )

    resolve = sub.add_parser(
        "resolve-execution",
        help="Resolve automatic-mode role execution policy",
    )
    resolve.add_argument("--policy-file", required=True)
    resolve.add_argument("--output", default=None)
    resolve.set_defaults(func=cmd_resolve_execution)

    auto_init = sub.add_parser(
        "auto-init",
        help="Create an arch-epic automatic-mode run directory",
    )
    auto_init.add_argument("--epic-doc", required=True)
    auto_init.add_argument("--policy-file", required=True)
    auto_init.add_argument("--orchestrator-root", default=None)
    auto_init.set_defaults(func=cmd_auto_init)

    worker_spawn = sub.add_parser(
        "worker-spawn",
        help="Spawn a resumable automatic-mode worker",
    )
    for a in ["--run-dir", "--target-repo", "--role", "--sub-plan-name", "--prompt-file"]:
        worker_spawn.add_argument(a, required=True)
    worker_spawn.add_argument("--try-k", type=int, default=1)
    add_child_run_args(worker_spawn)
    worker_spawn.set_defaults(func=cmd_worker_spawn)

    worker_resume = sub.add_parser(
        "worker-resume",
        help="Resume an automatic-mode worker",
    )
    for a in [
        "--run-dir",
        "--target-repo",
        "--role",
        "--sub-plan-name",
        "--prompt-file",
        "--session-id",
    ]:
        worker_resume.add_argument(a, required=True)
    worker_resume.add_argument("--try-k", type=int, required=True)
    add_child_run_args(worker_resume)
    worker_resume.set_defaults(func=cmd_worker_resume)

    auto_critic = sub.add_parser(
        "auto-critic-spawn",
        help="Spawn an automatic-mode structured critic",
    )
    for a in [
        "--run-dir",
        "--target-repo",
        "--gate",
        "--sub-plan-name",
        "--prompt-file",
        "--schema-file",
    ]:
        auto_critic.add_argument(a, required=True)
    auto_critic.add_argument("--role", default="critic")
    add_child_run_args(auto_critic)
    auto_critic.set_defaults(func=cmd_auto_critic_spawn)

    child_status = sub.add_parser(
        "child-status",
        help="Classify a spawned child from process state and stream recency",
    )
    add_monitor_args(child_status)
    child_status.add_argument("--json", action="store_true")
    child_status.set_defaults(func=cmd_child_status)

    child_tail = sub.add_parser(
        "child-tail",
        help="Print the latest lines from a child stream.log",
    )
    child_tail.add_argument("--try-dir", required=True)
    child_tail.add_argument("--lines", type=int, default=80)
    child_tail.set_defaults(func=cmd_child_tail)

    child_wait = sub.add_parser(
        "child-wait",
        help="Wait for a child using long-run monitor expectations",
    )
    add_monitor_args(child_wait)
    child_wait.add_argument(
        "--poll-seconds",
        type=int,
        default=DEFAULT_AUTO_POLL_SECONDS,
    )
    child_wait.set_defaults(func=cmd_child_wait)

    child_finalize = sub.add_parser(
        "child-finalize",
        help="Parse completed child output into session/verdict artifacts",
    )
    child_finalize.add_argument("--try-dir", required=True)
    child_finalize.set_defaults(func=cmd_child_finalize)

    child_terminate = sub.add_parser(
        "child-terminate",
        help="Request SIGTERM for a child and record an explicit reason",
    )
    child_terminate.add_argument("--try-dir", required=True)
    child_terminate.add_argument("--reason", required=True)
    child_terminate.set_defaults(func=cmd_child_terminate)

    auto_status = sub.add_parser(
        "auto-status",
        help="Print compact automatic-mode run status",
    )
    auto_status.add_argument("--run-dir", required=True)
    auto_status.set_defaults(func=cmd_auto_status)

    report = sub.add_parser(
        "report-scaffold",
        help="Print or write an automatic-mode report scaffold",
    )
    report.add_argument("--run-dir", required=True)
    report.add_argument("--write", action="store_true")
    report.set_defaults(func=cmd_report_scaffold)

    critic = sub.add_parser(
        "critic-spawn",
        help="Spawn a fresh ephemeral critic sub-session",
    )
    for a in [
        "--epic-doc",
        "--sub-plan-name",
        "--sub-plan-doc-path",
        "--prompt-file",
        "--schema-file",
        "--model",
        "--effort",
    ]:
        critic.add_argument(a, required=True)
    critic.add_argument(
        "--runtime", required=True, choices=["claude", "codex"]
    )
    critic.add_argument(
        "--orchestrator-root",
        required=False,
        default=None,
        help="Root where .arch_skill/arch-epic/critics/<slug>/run-<ts>/ lives. Defaults to cwd.",
    )
    add_child_run_args(critic)
    critic.set_defaults(func=cmd_critic_spawn)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
