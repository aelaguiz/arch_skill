#!/usr/bin/env python3
"""Stepwise orchestration plumbing.

This script is deterministic infrastructure for the stepwise skill. It does
NOT make judgments about strictness, manifests, verdicts, advance/resume, or
stop discipline. Those decisions live in the orchestrator's prose reasoning.

Subcommands:

  init-run     Create the run directory and initial state.json.
  step-spawn   Spawn a fresh step sub-session (claude or codex).
  step-resume  Resume an existing step sub-session with a resume prompt.
  critic-spawn Spawn an ephemeral critic sub-session with a structured schema.

All subcommands exit non-zero with a plain-English message when their
expected output shape does not appear. They never swallow errors silently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _die(msg: str, code: int = 2) -> None:
    print(f"run_stepwise: {msg}", file=sys.stderr)
    sys.exit(code)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, payload: Any) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


# ---- init-run -------------------------------------------------------------


def cmd_init_run(args: argparse.Namespace) -> int:
    orch_root = Path(args.orchestrator_root).resolve()
    if not orch_root.is_dir():
        _die(f"orchestrator root is not a directory: {orch_root}")
    target = Path(args.target_repo).resolve()
    if not target.is_dir():
        _die(f"target repo is not a directory: {target}")
    raw_path = Path(args.raw_instructions_file).resolve()
    if not raw_path.is_file():
        _die(f"raw instructions file missing: {raw_path}")

    raw = raw_path.read_text(encoding="utf-8")
    raw_hash = _sha256_hex(raw)
    short_hash = _sha256_hex(raw + str(target))[:8]
    run_id = f"{_utc_now_stamp()}-{short_hash}"

    run_dir = orch_root / ".arch_skill" / "stepwise" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    _write_text(run_dir / "raw_instructions.txt", raw)

    models = json.loads(args.models_json) if args.models_json else {}
    models_hash = _sha256_hex(json.dumps(models, sort_keys=True))

    state = {
        "schema_version": 1,
        "run_id": run_id,
        "started_at": _utc_now_iso(),
        "ended_at": None,
        "status": "in_progress",
        "raw_instructions": raw,
        "raw_instructions_sha256": raw_hash,
        "target_repo_path": str(target),
        "profile": args.profile,
        "forced_checks": json.loads(args.forced_checks_json)
        if args.forced_checks_json
        else [],
        "stop_discipline": args.stop_discipline,
        "per_step_retry_cap": args.per_step_retry_cap,
        "models": models,
        "models_sha256": models_hash,
        "progress": [],
    }
    _write_json(run_dir / "state.json", state)

    # ensure .gitignore has .arch_skill/
    gi = orch_root / ".gitignore"
    marker = ".arch_skill/"
    if gi.exists():
        lines = gi.read_text(encoding="utf-8").splitlines()
        if marker not in lines:
            with gi.open("a", encoding="utf-8") as f:
                f.write(f"\n{marker}\n")
    else:
        gi.write_text(f"{marker}\n", encoding="utf-8")

    print(str(run_dir))
    return 0


# ---- subprocess helpers ---------------------------------------------------


def _ensure_try_dir(run_dir: Path, step_n: int, try_k: int) -> Path:
    d = run_dir / "steps" / str(step_n) / f"try-{try_k}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _ensure_critic_dir(run_dir: Path, step_n: int, try_k: int) -> Path:
    d = run_dir / "steps" / str(step_n) / f"try-{try_k}" / "critic"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write_invocation_sh(path: Path, argv: list[str], cwd: str | None) -> None:
    def quote(s: str) -> str:
        return "'" + s.replace("'", "'\\''") + "'"

    line = " ".join(quote(a) for a in argv)
    prefix = f"cd {quote(cwd)} && " if cwd else ""
    _write_text(
        path, "#!/bin/sh\n" + prefix + "exec " + line + " < /dev/null\n"
    )
    path.chmod(0o755)


def _run_subprocess(
    argv: list[str],
    stdout_stream_path: Path,
    out_dir: Path,
    cwd: str | None = None,
) -> tuple[int, str]:
    """Run a subprocess with stdin closed, streaming stdout+stderr to a file.

    Returns (exit_code, stdout_text). stdout_text is also on disk at
    stdout_stream_path (combined with stderr).
    """
    _write_text(out_dir / "start_ts", _utc_now_iso())
    with open(os.devnull, "rb") as devnull, open(stdout_stream_path, "wb") as out:
        proc = subprocess.run(
            argv,
            stdin=devnull,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            check=False,
        )
        out.write(proc.stdout)
    _write_text(out_dir / "end_ts", _utc_now_iso())
    _write_text(out_dir / "exit_code", str(proc.returncode) + "\n")
    return proc.returncode, proc.stdout.decode("utf-8", errors="replace")


def _parse_claude_session_id(stdout_text: str) -> str | None:
    """Claude -p --output-format json prints one JSON object to stdout."""
    try:
        payload = json.loads(stdout_text.strip().splitlines()[-1])
        sid = payload.get("session_id")
        if isinstance(sid, str) and sid:
            return sid
    except (json.JSONDecodeError, IndexError):
        pass
    return None


def _parse_claude_final_json(stdout_text: str) -> dict | None:
    try:
        return json.loads(stdout_text.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return None


def _parse_codex_thread_id(stdout_text: str) -> str | None:
    for line in stdout_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "thread.started" and isinstance(
            ev.get("thread_id"), str
        ):
            return ev["thread_id"]
    return None


# ---- step-spawn -----------------------------------------------------------


def cmd_step_spawn(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "state.json").is_file():
        _die(f"run_dir has no state.json: {run_dir}")
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    target_repo = str(Path(args.target_repo).resolve())
    try_dir = _ensure_try_dir(run_dir, args.step_n, args.try_k)

    final_path = try_dir / "stdout.final.json"
    stream_path = try_dir / "stream.log"

    if args.runtime == "claude":
        argv = [
            "claude",
            "-p",
            "--output-format",
            "json",
            "--dangerously-skip-permissions",
            "--settings",
            '{"disableAllHooks":true}',
            "--model",
            args.model,
            "--effort",
            args.effort,
            prompt,
        ]
        spawn_cwd = target_repo
    elif args.runtime == "codex":
        argv = [
            "codex",
            "exec",
            "--cd",
            target_repo,
            "--dangerously-bypass-approvals-and-sandbox",
            "--skip-git-repo-check",
            "--model",
            args.model,
            "-c",
            f'model_reasoning_effort="{args.effort}"',
            "--json",
            "-o",
            str(final_path),
            prompt,
        ]
        spawn_cwd = None
    else:
        _die(f"unknown runtime: {args.runtime}")

    _write_invocation_sh(try_dir / "invocation.sh", argv, spawn_cwd)
    code, stdout_text = _run_subprocess(argv, stream_path, try_dir, cwd=spawn_cwd)

    sid: str | None
    if args.runtime == "claude":
        # Claude writes the whole result to stdout; also persist as final.
        final = _parse_claude_final_json(stdout_text)
        if final is None:
            _die(
                "claude stdout did not parse as JSON; see stream.log",
                code=3,
            )
        _write_json(final_path, final)
        sid = _parse_claude_session_id(stdout_text)
    else:
        sid = _parse_codex_thread_id(stdout_text)

    if sid is None:
        _write_text(try_dir / "session_id.txt", "UNRECOVERABLE\n")
        _die(
            f"session id not captured (runtime={args.runtime}, exit={code})",
            code=4,
        )
    _write_text(try_dir / "session_id.txt", sid + "\n")

    print(sid)
    return 0 if code == 0 else code


# ---- step-resume ----------------------------------------------------------


def cmd_step_resume(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "state.json").is_file():
        _die(f"run_dir has no state.json: {run_dir}")
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    target_repo = str(Path(args.target_repo).resolve())
    try_dir = _ensure_try_dir(run_dir, args.step_n, args.try_k)
    sid = args.session_id
    if not sid or sid == "UNRECOVERABLE":
        _die(f"refusing to resume without a valid session id: {sid!r}")

    final_path = try_dir / "stdout.final.json"
    stream_path = try_dir / "stream.log"

    if args.runtime == "claude":
        argv = [
            "claude",
            "-p",
            "--output-format",
            "json",
            "--dangerously-skip-permissions",
            "--settings",
            '{"disableAllHooks":true}',
            "--model",
            args.model,
            "--effort",
            args.effort,
            "-r",
            sid,
            prompt,
        ]
        resume_cwd = target_repo
    elif args.runtime == "codex":
        argv = [
            "codex",
            "exec",
            "resume",
            sid,
            "--dangerously-bypass-approvals-and-sandbox",
            "--skip-git-repo-check",
            "--json",
            "-o",
            str(final_path),
            prompt,
        ]
        resume_cwd = None
    else:
        _die(f"unknown runtime: {args.runtime}")

    _write_invocation_sh(try_dir / "invocation.sh", argv, resume_cwd)
    code, stdout_text = _run_subprocess(argv, stream_path, try_dir, cwd=resume_cwd)

    out_sid: str | None
    if args.runtime == "claude":
        final = _parse_claude_final_json(stdout_text)
        if final is None:
            _die(
                "claude stdout did not parse as JSON; see stream.log",
                code=3,
            )
        _write_json(final_path, final)
        out_sid = _parse_claude_session_id(stdout_text) or sid
    else:
        out_sid = _parse_codex_thread_id(stdout_text) or sid

    _write_text(try_dir / "session_id.txt", out_sid + "\n")
    print(out_sid)
    return 0 if code == 0 else code


# ---- critic-spawn ---------------------------------------------------------


def cmd_critic_spawn(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "state.json").is_file():
        _die(f"run_dir has no state.json: {run_dir}")
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    schema_path = Path(args.schema_file).resolve()
    if not schema_path.is_file():
        _die(f"critic schema file missing: {schema_path}")
    target_repo = str(Path(args.target_repo).resolve())
    crit_dir = _ensure_critic_dir(run_dir, args.step_n, args.try_k)

    # save prompt verbatim for audit
    _write_text(crit_dir / "prompt.md", prompt)

    final_path = crit_dir / "stdout.final.json"
    stream_path = crit_dir / "stream.log"
    verdict_path = crit_dir / "verdict.json"

    if args.runtime == "claude":
        schema_inline = schema_path.read_text(encoding="utf-8").strip()
        argv = [
            "claude",
            "-p",
            "--output-format",
            "json",
            "--dangerously-skip-permissions",
            "--settings",
            '{"disableAllHooks":true}',
            "--model",
            args.model,
            "--effort",
            args.effort,
            "--json-schema",
            schema_inline,
            prompt,
        ]
        critic_cwd = target_repo
    elif args.runtime == "codex":
        argv = [
            "codex",
            "exec",
            "--cd",
            target_repo,
            "--ephemeral",
            "--dangerously-bypass-approvals-and-sandbox",
            "--skip-git-repo-check",
            "--model",
            args.model,
            "-c",
            f'model_reasoning_effort="{args.effort}"',
            "--output-schema",
            str(schema_path),
            "--json",
            "-o",
            str(final_path),
            prompt,
        ]
        critic_cwd = None
    else:
        _die(f"unknown runtime: {args.runtime}")

    _write_invocation_sh(crit_dir / "invocation.sh", argv, critic_cwd)
    code, stdout_text = _run_subprocess(argv, stream_path, crit_dir, cwd=critic_cwd)

    if args.runtime == "claude":
        final = _parse_claude_final_json(stdout_text)
        if final is None:
            _die(
                "claude stdout did not parse as JSON; see stream.log",
                code=3,
            )
        _write_json(final_path, final)
        verdict = final.get("structured_output")
        if not isinstance(verdict, dict):
            _die(
                "claude critic returned no structured_output; see stdout.final.json",
                code=5,
            )
        _write_json(verdict_path, verdict)
    else:
        # codex writes structured JSON to final_path directly
        if not final_path.is_file():
            _die(
                f"codex critic did not write -o file: {final_path}",
                code=5,
            )
        try:
            verdict = json.loads(final_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            _die(f"codex critic output is not valid JSON: {e}", code=5)
        _write_json(verdict_path, verdict)

    print(str(verdict_path))
    return 0 if code == 0 else code


# ---- arg parsing ----------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="run_stepwise")
    sub = p.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init-run", help="Create run directory and state.json")
    init.add_argument("--orchestrator-root", required=True)
    init.add_argument("--target-repo", required=True)
    init.add_argument("--raw-instructions-file", required=True)
    init.add_argument("--profile", required=True,
                      choices=["strict", "balanced", "lenient"])
    init.add_argument("--forced-checks-json", default="[]")
    init.add_argument("--stop-discipline", required=True,
                      choices=["halt_and_ask", "skip_and_continue",
                               "escalate_to_user"])
    init.add_argument("--per-step-retry-cap", type=int, required=True)
    init.add_argument("--models-json", required=True,
                      help='JSON object with step_model, step_effort, critic_model, critic_effort')
    init.set_defaults(func=cmd_init_run)

    step = sub.add_parser("step-spawn", help="Spawn a fresh step sub-session")
    for a in ["--run-dir", "--target-repo", "--prompt-file", "--model", "--effort"]:
        step.add_argument(a, required=True)
    step.add_argument("--runtime", required=True, choices=["claude", "codex"])
    step.add_argument("--step-n", required=True, type=int)
    step.add_argument("--try-k", required=True, type=int)
    step.set_defaults(func=cmd_step_spawn)

    resume = sub.add_parser("step-resume", help="Resume an existing step session")
    for a in ["--run-dir", "--target-repo", "--prompt-file", "--model",
              "--effort", "--session-id"]:
        resume.add_argument(a, required=True)
    resume.add_argument("--runtime", required=True, choices=["claude", "codex"])
    resume.add_argument("--step-n", required=True, type=int)
    resume.add_argument("--try-k", required=True, type=int)
    resume.set_defaults(func=cmd_step_resume)

    critic = sub.add_parser("critic-spawn", help="Spawn an ephemeral critic")
    for a in ["--run-dir", "--target-repo", "--prompt-file", "--model",
              "--effort", "--schema-file"]:
        critic.add_argument(a, required=True)
    critic.add_argument("--runtime", required=True, choices=["claude", "codex"])
    critic.add_argument("--step-n", required=True, type=int)
    critic.add_argument("--try-k", required=True, type=int)
    critic.set_defaults(func=cmd_critic_spawn)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
