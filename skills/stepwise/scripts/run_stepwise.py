#!/usr/bin/env python3
"""Stepwise orchestration plumbing.

This script is deterministic infrastructure for the stepwise skill. It does
NOT make judgments about strictness, manifests, verdicts, advance/resume, or
stop discipline. Those decisions live in the orchestrator's prose reasoning.

Subcommands:

  init-run     Create the run directory and initial state.json.
  step-spawn   Spawn a fresh step sub-session (claude or codex).
  step-resume  Resume an existing step sub-session with a repair prompt.
  step-diagnose
               Resume an existing step sub-session with a read-only
               diagnostic prompt and write diagnostic artifacts.
  critic-spawn Spawn an ephemeral critic sub-session with a structured schema.
  latest-session
               Print the latest session metadata for a step.
  upstream-for Print manifest-declared upstream artifacts for a step.
  report-scaffold
               Print or write a deterministic report.md scaffold.

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


def _parse_json_object_arg(value: str | None, field: str) -> dict[str, Any] | None:
    if value is None:
        return None
    try:
        payload = json.loads(value)
    except json.JSONDecodeError as e:
        _die(f"{field} is not valid JSON: {e}")
    if not isinstance(payload, dict):
        _die(f"{field} must be a JSON object")
    return payload


def _ensure_stepwise_runs_gitignore_marker(orch_root: Path) -> None:
    """Ignore local run logs without hiding the visible learnings ledger."""
    gi = orch_root / ".gitignore"
    marker = ".arch_skill/stepwise/runs/"
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


def _schema_allows_null(schema: Any) -> bool:
    if not isinstance(schema, dict):
        return False
    schema_type = schema.get("type")
    if schema_type == "null":
        return True
    if isinstance(schema_type, list) and "null" in schema_type:
        return True
    if isinstance(schema.get("enum"), list) and None in schema["enum"]:
        return True
    for key in ("anyOf", "oneOf"):
        options = schema.get(key)
        if isinstance(options, list) and any(_schema_allows_null(o) for o in options):
            return True
    return False


def _schema_with_null(schema: dict[str, Any]) -> dict[str, Any]:
    if _schema_allows_null(schema):
        return schema
    out = dict(schema)
    schema_type = out.get("type")
    if isinstance(schema_type, str):
        out["type"] = [schema_type, "null"]
        return out
    if isinstance(schema_type, list):
        out["type"] = [*schema_type, "null"]
        return out
    enum = out.get("enum")
    if isinstance(enum, list):
        out["enum"] = [*enum, None]
        return out
    any_of = out.get("anyOf")
    if isinstance(any_of, list):
        out["anyOf"] = [*any_of, {"type": "null"}]
        return out
    return {"anyOf": [out, {"type": "null"}]}


def _codex_strict_schema(schema: Any) -> Any:
    """Normalize JSON Schema for Codex structured output.

    Recent Codex/OpenAI structured-output validation requires every object
    property to be listed in `required`. Preserve optional-field semantics by
    making formerly optional properties required-but-nullable.
    """
    if isinstance(schema, list):
        return [_codex_strict_schema(item) for item in schema]
    if not isinstance(schema, dict):
        return schema

    out: dict[str, Any] = {}
    for key, value in schema.items():
        if key in {"properties", "items", "anyOf", "oneOf", "allOf"}:
            continue
        out[key] = value

    for key in ("anyOf", "oneOf", "allOf"):
        options = schema.get(key)
        if isinstance(options, list):
            out[key] = [_codex_strict_schema(option) for option in options]

    if "items" in schema:
        out["items"] = _codex_strict_schema(schema["items"])

    properties = schema.get("properties")
    if isinstance(properties, dict):
        original_required = set(schema.get("required", []))
        normalized_props: dict[str, Any] = {}
        for name, prop_schema in properties.items():
            normalized_prop = _codex_strict_schema(prop_schema)
            if name not in original_required and isinstance(normalized_prop, dict):
                normalized_prop = _schema_with_null(normalized_prop)
            normalized_props[name] = normalized_prop
        out["properties"] = normalized_props
        out["required"] = list(properties.keys())
        out["additionalProperties"] = False
    elif "required" in schema:
        out["required"] = schema["required"]

    return out


def _nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_str_list(value: Any, field: str, *, require_nonempty: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return [f"{field} must be an array"]
    if require_nonempty and not value:
        errors.append(f"{field} must be a non-empty array")
    for i, item in enumerate(value):
        if not _nonempty_str(item):
            errors.append(f"{field}[{i}] must be a non-empty string")
    return errors


def _validate_step_verdict(verdict: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(verdict, dict):
        return ["verdict must be a JSON object"]

    stale_fields = {"resume_hint", "route_to_step_n", "required_fixes", "do_not_redo"}
    for key in sorted(stale_fields & set(verdict)):
        if key == "resume_hint":
            errors.append(
                "resume_hint is no longer accepted; critics observe only and "
                "Stepwise authors repairs"
            )
        elif key == "route_to_step_n":
            errors.append(
                "route_to_step_n is no longer accepted; Stepwise diagnoses "
                "upstream root cause"
            )
        else:
            errors.append(f"{key} is no longer accepted in StepVerdict")

    required = [
        "step_n",
        "verdict",
        "checks",
        "observed_breach",
        "evidence_pointers",
        "contract_clauses_implicated",
        "summary",
        "abstain_reason",
    ]
    allowed = set(required)
    for key in verdict:
        if key not in allowed and key not in stale_fields:
            errors.append(f"unexpected field: {key}")
    for key in required:
        if key not in verdict:
            errors.append(f"missing required field: {key}")

    step_n = verdict.get("step_n")
    if not isinstance(step_n, int) or step_n < 1:
        errors.append("step_n must be an integer >= 1")

    outcome = verdict.get("verdict")
    if outcome not in {"pass", "fail", "abstain"}:
        errors.append("verdict must be pass, fail, or abstain")

    checks = verdict.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be an array")
    else:
        allowed_names = {
            "skill_order_adherence",
            "no_substep_skipped",
            "artifact_exists",
            "no_fabrication",
            "doctrine_quote_fidelity",
        }
        allowed_statuses = {"pass", "fail", "inapplicable"}
        for i, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"checks[{i}] must be an object")
                continue
            if check.get("name") not in allowed_names:
                errors.append(f"checks[{i}].name is not a known check")
            if check.get("status") not in allowed_statuses:
                errors.append(
                    f"checks[{i}].status must be pass, fail, or inapplicable"
                )
            if not _nonempty_str(check.get("evidence")):
                errors.append(f"checks[{i}].evidence must be a non-empty string")

    if not _nonempty_str(verdict.get("summary")):
        errors.append("summary must be a non-empty string")

    observed_breach = verdict.get("observed_breach")
    if observed_breach is not None and not _nonempty_str(observed_breach):
        errors.append("observed_breach must be null or a non-empty string")
    errors.extend(
        _nonempty_str_list(
            verdict.get("evidence_pointers"),
            "evidence_pointers",
            require_nonempty=False,
        )
    )
    errors.extend(
        _nonempty_str_list(
            verdict.get("contract_clauses_implicated"),
            "contract_clauses_implicated",
            require_nonempty=False,
        )
    )

    evidence_pointers = verdict.get("evidence_pointers")
    contract_clauses = verdict.get("contract_clauses_implicated")
    abstain_reason = verdict.get("abstain_reason")
    if outcome == "pass":
        if observed_breach is not None:
            errors.append("observed_breach must be null when verdict=pass")
        if abstain_reason is not None:
            errors.append("abstain_reason must be null when verdict=pass")
    elif outcome == "fail":
        if not _nonempty_str(observed_breach):
            errors.append("observed_breach must be a non-empty string on fail")
        if not isinstance(evidence_pointers, list) or not evidence_pointers:
            errors.append("evidence_pointers must be non-empty on fail")
        if not isinstance(contract_clauses, list) or not contract_clauses:
            errors.append("contract_clauses_implicated must be non-empty on fail")
        if abstain_reason is not None:
            errors.append("abstain_reason must be null when verdict=fail")
    elif outcome == "abstain":
        if observed_breach is not None:
            errors.append("observed_breach must be null when verdict=abstain")
        if not _nonempty_str(abstain_reason):
            errors.append("abstain_reason must be a non-empty string on abstain")

    return errors


# ---- init-run -------------------------------------------------------------


def _execution_from_init_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.execution_json:
        try:
            execution = json.loads(args.execution_json)
        except json.JSONDecodeError as e:
            _die(f"execution json is not valid JSON: {e}")
        if not isinstance(execution, dict):
            _die("execution json must be an object")
        return execution

    if args.models_json:
        try:
            models = json.loads(args.models_json)
        except json.JSONDecodeError as e:
            _die(f"models json is not valid JSON: {e}")
        if not isinstance(models, dict):
            _die("models json must be an object")
        return {
            "schema_version": 1,
            "execution_defaults": {
                "step": {
                    "model": models.get("step_model"),
                    "effort": models.get("step_effort"),
                    "source": "legacy --models-json",
                },
                "critic": {
                    "model": models.get("critic_model"),
                    "effort": models.get("critic_effort"),
                    "source": "legacy --models-json",
                },
            },
            "execution_preferences": [],
        }

    _die("one of --execution-json or --models-json is required")


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

    execution = _execution_from_init_args(args)
    execution_hash = _sha256_hex(json.dumps(execution, sort_keys=True))

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
        "diagnostic_turn_cap": args.diagnostic_turn_cap,
        "execution": execution,
        "execution_sha256": execution_hash,
        "progress": [],
    }
    _write_json(run_dir / "state.json", state)

    _ensure_stepwise_runs_gitignore_marker(orch_root)

    print(str(run_dir))
    return 0


# ---- subprocess helpers ---------------------------------------------------


def _ensure_try_dir(run_dir: Path, step_n: int, try_k: int) -> Path:
    d = run_dir / "steps" / str(step_n) / f"try-{try_k}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _try_dir(run_dir: Path, step_n: int, try_k: int) -> Path:
    return run_dir / "steps" / str(step_n) / f"try-{try_k}"


def _write_try_origin(
    try_dir: Path,
    *,
    kind: str,
    session_mode: str,
    consumes_repair_bounce: bool,
    triggered_by: dict[str, Any] | None,
    created_by_subcommand: str,
    session_id: str,
    prompt_path: Path,
) -> None:
    _write_json(
        try_dir / "origin.json",
        {
            "schema_version": 1,
            "created_at": _utc_now_iso(),
            "kind": kind,
            "session_mode": session_mode,
            "consumes_repair_bounce": consumes_repair_bounce,
            "triggered_by": triggered_by,
            "created_by_subcommand": created_by_subcommand,
            "session_id": session_id,
            "prompt_path": str(prompt_path),
        },
    )


def _ensure_critic_dir(run_dir: Path, step_n: int, try_k: int) -> Path:
    d = run_dir / "steps" / str(step_n) / f"try-{try_k}" / "critic"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _ensure_diagnostic_dir(run_dir: Path, step_n: int, try_k: int) -> Path:
    d = run_dir / "steps" / str(step_n) / f"try-{try_k}" / "diagnostic"
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
    stamp_prefix: str | None = None,
) -> tuple[int, str]:
    """Run a subprocess with stdin closed, streaming stdout+stderr to a file.

    Returns (exit_code, stdout_text). stdout_text is also on disk at
    stdout_stream_path (combined with stderr).
    """
    start_name = f"{stamp_prefix}.start_ts" if stamp_prefix else "start_ts"
    end_name = f"{stamp_prefix}.end_ts" if stamp_prefix else "end_ts"
    exit_name = f"{stamp_prefix}.exit_code" if stamp_prefix else "exit_code"
    _write_text(out_dir / start_name, _utc_now_iso())
    with open(os.devnull, "rb") as devnull, open(stdout_stream_path, "wb") as out:
        proc = subprocess.Popen(
            argv,
            stdin=devnull,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
        )
        chunks: list[bytes] = []
        assert proc.stdout is not None
        for chunk in iter(lambda: proc.stdout.read(8192), b""):
            chunks.append(chunk)
            out.write(chunk)
            out.flush()
        proc.stdout.close()
        returncode = proc.wait()
        stdout_bytes = b"".join(chunks)
    _write_text(out_dir / end_name, _utc_now_iso())
    _write_text(out_dir / exit_name, str(returncode) + "\n")
    return returncode, stdout_bytes.decode("utf-8", errors="replace")


def _load_json_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _die(f"JSON file missing: {path}")
    except json.JSONDecodeError as e:
        _die(f"JSON file is not valid JSON: {path}: {e}")


def _latest_try_k(run_dir: Path, step_n: int) -> int | None:
    step_dir = run_dir / "steps" / str(step_n)
    if not step_dir.is_dir():
        return None
    tries: list[int] = []
    for child in step_dir.iterdir():
        if child.is_dir() and child.name.startswith("try-"):
            try:
                tries.append(int(child.name.removeprefix("try-")))
            except ValueError:
                continue
    return max(tries) if tries else None


def _latest_session_id(run_dir: Path, step_n: int) -> str | None:
    try_k = _latest_try_k(run_dir, step_n)
    if try_k is None:
        return None
    sid_path = _try_dir(run_dir, step_n, try_k) / "session_id.txt"
    if not sid_path.is_file():
        return None
    sid = sid_path.read_text(encoding="utf-8").strip()
    return sid if sid and sid != "UNRECOVERABLE" else None


def _latest_try_metadata(run_dir: Path, step_n: int) -> dict[str, Any]:
    try_k = _latest_try_k(run_dir, step_n)
    if try_k is None:
        return {
            "step_n": step_n,
            "latest_try_k": None,
            "try_dir": None,
            "session_id": None,
            "session_id_path": None,
            "origin_kind": None,
            "consumes_repair_bounce": None,
        }

    tdir = _try_dir(run_dir, step_n, try_k)
    sid_path = tdir / "session_id.txt"
    sid = sid_path.read_text(encoding="utf-8").strip() if sid_path.is_file() else None
    if sid == "UNRECOVERABLE":
        sid = None

    origin_path = tdir / "origin.json"
    origin: dict[str, Any] = {}
    if origin_path.is_file():
        loaded = _load_json_file(origin_path)
        if isinstance(loaded, dict):
            origin = loaded

    return {
        "step_n": step_n,
        "latest_try_k": try_k,
        "try_dir": str(tdir),
        "session_id": sid,
        "session_id_path": str(sid_path) if sid_path.is_file() else None,
        "origin_path": str(origin_path) if origin_path.is_file() else None,
        "origin_kind": origin.get("kind"),
        "consumes_repair_bounce": origin.get("consumes_repair_bounce"),
    }


def _manifest_steps_by_artifact(run_dir: Path) -> dict[str, int]:
    manifest = _load_json_file(run_dir / "manifest.json")
    out: dict[str, int] = {}
    for step in manifest.get("steps", []):
        if not isinstance(step, dict):
            continue
        n = step.get("n")
        artifact = step.get("expected_artifact")
        if isinstance(n, int) and isinstance(artifact, dict):
            selector = artifact.get("selector")
            if isinstance(selector, str) and selector:
                out[selector] = n
    return out


def _manifest_step_by_n(run_dir: Path, step_n: int) -> dict[str, Any] | None:
    manifest = _load_json_file(run_dir / "manifest.json")
    for step in manifest.get("steps", []):
        if isinstance(step, dict) and step.get("n") == step_n:
            return step
    return None


def _input_selector_candidate(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    prefix = "source:"
    if stripped.lower().startswith(prefix):
        candidate = stripped[len(prefix):].strip()
        if candidate.startswith("/"):
            return candidate
    return stripped or None


def _extract_claude_result_event(payload) -> dict | None:
    """Return the result event from Claude JSON or stream-json output."""
    if isinstance(payload, dict):
        if (
            payload.get("type") == "result"
            or "result" in payload
            or "structured_output" in payload
        ):
            return payload
        return None
    if isinstance(payload, list):
        for ev in reversed(payload):
            if isinstance(ev, dict) and ev.get("type") == "result":
                return ev
    return None


def _extract_verdict_from_final(final) -> dict | None:
    """Pull the critic's structured verdict from a final payload of either
    shape (dict or event-stream list)."""
    ev = _extract_claude_result_event(final)
    if ev is None:
        return None
    v = ev.get("structured_output")
    return v if isinstance(v, dict) else None


def _parse_claude_session_id(stdout_text: str) -> str | None:
    """Return the session id from the last parseable Claude result event."""
    for line in reversed(stdout_text.strip().splitlines()):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        ev = _extract_claude_result_event(payload)
        if ev is None:
            continue
        sid = ev.get("session_id")
        if isinstance(sid, str) and sid:
            return sid
    return None


def _parse_claude_final_json(stdout_text: str) -> dict | None:
    for line in reversed(stdout_text.strip().splitlines()):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        ev = _extract_claude_result_event(payload)
        if ev is not None:
            return ev
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
    triggered_by = _parse_json_object_arg(args.origin_trigger_json, "--origin-trigger-json")
    if args.origin_kind == "respawn-after-upstream" and triggered_by is None:
        _die("--origin-trigger-json is required for respawn-after-upstream")
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    target_repo = str(Path(args.target_repo).resolve())
    try_dir = _ensure_try_dir(run_dir, args.step_n, args.try_k)
    prompt_path = try_dir / "prompt.md"
    _write_text(prompt_path, prompt)

    final_path = try_dir / "stdout.final.json"
    stream_path = try_dir / "stream.log"

    if args.runtime == "claude":
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
        _write_try_origin(
            try_dir,
            kind=args.origin_kind,
            session_mode="fresh-session",
            consumes_repair_bounce=False,
            triggered_by=triggered_by,
            created_by_subcommand="step-spawn",
            session_id="UNRECOVERABLE",
            prompt_path=prompt_path,
        )
        _die(
            f"session id not captured (runtime={args.runtime}, exit={code})",
            code=4,
        )
    _write_text(try_dir / "session_id.txt", sid + "\n")
    _write_try_origin(
        try_dir,
        kind=args.origin_kind,
        session_mode="fresh-session",
        consumes_repair_bounce=False,
        triggered_by=triggered_by,
        created_by_subcommand="step-spawn",
        session_id=sid,
        prompt_path=prompt_path,
    )

    print(sid)
    return 0 if code == 0 else code


# ---- step-resume ----------------------------------------------------------


def cmd_step_resume(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "state.json").is_file():
        _die(f"run_dir has no state.json: {run_dir}")
    triggered_by = _parse_json_object_arg(args.origin_trigger_json, "--origin-trigger-json")
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    target_repo = str(Path(args.target_repo).resolve())
    try_dir = _ensure_try_dir(run_dir, args.step_n, args.try_k)
    prompt_path = try_dir / "prompt.md"
    _write_text(prompt_path, prompt)
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
            "stream-json",
            "--include-partial-messages",
            "--include-hook-events",
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
    _write_try_origin(
        try_dir,
        kind="repair-resume",
        session_mode="same-session",
        consumes_repair_bounce=True,
        triggered_by=triggered_by,
        created_by_subcommand="step-resume",
        session_id=out_sid,
        prompt_path=prompt_path,
    )
    print(out_sid)
    return 0 if code == 0 else code


# ---- step-diagnose --------------------------------------------------------


def cmd_step_diagnose(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "state.json").is_file():
        _die(f"run_dir has no state.json: {run_dir}")
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    target_repo = str(Path(args.target_repo).resolve())
    diag_dir = _ensure_diagnostic_dir(run_dir, args.step_n, args.try_k)
    sid = args.session_id
    if not sid or sid == "UNRECOVERABLE":
        _die(f"refusing to diagnose without a valid session id: {sid!r}")

    prefix = f"turn-{args.round_k}.with-step-{args.with_step_m}"
    prompt_path = diag_dir / f"{prefix}.prompt.md"
    response_path = diag_dir / f"{prefix}.response.md"
    final_path = diag_dir / f"{prefix}.stdout.final.json"
    stream_path = diag_dir / f"{prefix}.stream.log"
    session_path = diag_dir / f"{prefix}.session_id.txt"
    _write_text(prompt_path, prompt)

    if args.runtime == "claude":
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
            str(response_path),
            prompt,
        ]
        resume_cwd = None
    else:
        _die(f"unknown runtime: {args.runtime}")

    _write_invocation_sh(diag_dir / f"{prefix}.invocation.sh", argv, resume_cwd)
    code, stdout_text = _run_subprocess(
        argv,
        stream_path,
        diag_dir,
        cwd=resume_cwd,
        stamp_prefix=prefix,
    )

    out_sid: str | None
    if args.runtime == "claude":
        final = _parse_claude_final_json(stdout_text)
        if final is None:
            _die(
                "claude stdout did not parse as JSON; see diagnostic stream log",
                code=3,
            )
        _write_json(final_path, final)
        result_text = final.get("result")
        _write_text(
            response_path,
            result_text if isinstance(result_text, str) else json.dumps(final, indent=2),
        )
        out_sid = _parse_claude_session_id(stdout_text) or sid
    else:
        out_sid = _parse_codex_thread_id(stdout_text) or sid
        if not response_path.is_file():
            _die(f"codex diagnostic did not write -o file: {response_path}", code=5)

    _write_text(session_path, out_sid + "\n")
    print(str(response_path))
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
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        _die(f"critic schema file is not valid JSON: {e}")
    target_repo = str(Path(args.target_repo).resolve())
    crit_dir = _ensure_critic_dir(run_dir, args.step_n, args.try_k)

    # save prompt verbatim for audit
    _write_text(crit_dir / "prompt.md", prompt)

    final_path = crit_dir / "stdout.final.json"
    stream_path = crit_dir / "stream.log"
    verdict_path = crit_dir / "verdict.json"

    if args.runtime == "claude":
        schema_inline = json.dumps(schema, separators=(",", ":"))
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
            args.model,
            "--effort",
            args.effort,
            "--json-schema",
            schema_inline,
            prompt,
        ]
        critic_cwd = target_repo
    elif args.runtime == "codex":
        codex_schema_path = crit_dir / "schema.codex.json"
        _write_json(codex_schema_path, _codex_strict_schema(schema))
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
            str(codex_schema_path),
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
        verdict = _extract_verdict_from_final(final)
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

    validation_errors = _validate_step_verdict(verdict)
    if validation_errors:
        _write_json(crit_dir / "verdict.validation_errors.json", validation_errors)
        _die(
            "critic verdict failed semantic validation: "
            + "; ".join(validation_errors),
            code=6,
        )

    print(str(verdict_path))
    return 0 if code == 0 else code


# ---- metadata helpers -----------------------------------------------------


def cmd_latest_session(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "state.json").is_file():
        _die(f"run_dir has no state.json: {run_dir}")
    print(json.dumps(_latest_try_metadata(run_dir, args.step_n), indent=2, sort_keys=True))
    return 0


def cmd_upstream_for(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "state.json").is_file():
        _die(f"run_dir has no state.json: {run_dir}")
    step = _manifest_step_by_n(run_dir, args.step_n)
    if step is None:
        _die(f"manifest has no step n={args.step_n}")

    artifact_to_step = _manifest_steps_by_artifact(run_dir)
    inputs = step.get("inputs", [])
    if not isinstance(inputs, list):
        _die(f"manifest step {args.step_n} inputs must be an array")

    matches: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []
    for raw_input in inputs:
        candidate = _input_selector_candidate(raw_input)
        if candidate is None:
            unmatched.append(
                {
                    "input": raw_input,
                    "normalized_selector": None,
                    "reason": "input is not a non-empty string",
                }
            )
            continue
        upstream_step_n = artifact_to_step.get(candidate)
        if upstream_step_n is None:
            unmatched.append(
                {
                    "input": raw_input,
                    "normalized_selector": candidate,
                    "reason": "no matching expected_artifact.selector",
                }
            )
            continue
        if upstream_step_n >= args.step_n:
            unmatched.append(
                {
                    "input": raw_input,
                    "normalized_selector": candidate,
                    "reason": "matching artifact is not from an earlier step",
                    "matched_step_n": upstream_step_n,
                }
            )
            continue

        latest = _latest_try_metadata(run_dir, upstream_step_n)
        matches.append(
            {
                "input": raw_input,
                "normalized_selector": candidate,
                "upstream_step_n": upstream_step_n,
                "selector": candidate,
                "latest_try_k": latest["latest_try_k"],
                "session_id": latest["session_id"],
                "session_id_path": latest["session_id_path"],
                "origin_kind": latest["origin_kind"],
                "consumes_repair_bounce": latest["consumes_repair_bounce"],
            }
        )

    print(
        json.dumps(
            {
                "step_n": args.step_n,
                "matches": matches,
                "unmatched": unmatched,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _latest_verdict_summary(run_dir: Path, step_n: int, try_k: int | None) -> str:
    if try_k is None:
        return "pending"
    verdict_path = _try_dir(run_dir, step_n, try_k) / "critic" / "verdict.json"
    if not verdict_path.is_file():
        return "no critic verdict recorded"
    verdict = _load_json_file(verdict_path)
    if not isinstance(verdict, dict):
        return "critic verdict is malformed"
    status = verdict.get("verdict", "unknown")
    summary = verdict.get("summary")
    if isinstance(summary, str) and summary.strip():
        return f"{status}: {summary.strip()}"
    return str(status)


def _md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _render_report_scaffold(run_dir: Path) -> str:
    state = _load_json_file(run_dir / "state.json")
    manifest = _load_json_file(run_dir / "manifest.json")
    if not isinstance(state, dict):
        _die("state.json must contain a JSON object")
    if not isinstance(manifest, dict):
        _die("manifest.json must contain a JSON object")

    steps = manifest.get("steps", [])
    if not isinstance(steps, list):
        _die("manifest steps must be an array")

    lines = [
        "# Stepwise Run Report",
        "",
        f"Run id: {state.get('run_id', '')}",
        f"Target: {state.get('target_repo_path', manifest.get('target_repo_path', ''))}",
        f"Process: {manifest.get('target_process', '')}",
        f"Profile: {state.get('profile', manifest.get('profile', ''))}",
        "",
        "## Per-step Status",
        "",
        "| Step | Label | Latest Try | Origin | Status |",
        "|---|---|---:|---|---|",
    ]

    for step in steps:
        if not isinstance(step, dict):
            continue
        step_n = step.get("n")
        if not isinstance(step_n, int):
            continue
        latest = _latest_try_metadata(run_dir, step_n)
        latest_try = latest["latest_try_k"]
        origin = latest["origin_kind"] or ""
        status = _latest_verdict_summary(run_dir, step_n, latest_try)
        lines.append(
            f"| {step_n} | {_md_cell(step.get('label', ''))} | "
            f"{latest_try or ''} | {_md_cell(origin)} | {_md_cell(status)} |"
        )

    lines.extend(
        [
            "",
            "## Notable Critic Observations",
            "",
            "- Fill from critic verdict evidence and summaries.",
            "",
            "## Diagnostic Root Cause",
            "",
            "- Fill from diagnostic/root-cause.md if the run halted or repaired upstream.",
            "",
            "## Learnings",
            "",
            "- Applied accepted learnings:",
            "- Candidate learnings written:",
            "- Near-misses considered and dismissed:",
            "",
            "## Attempt-Origin Notes",
            "",
            "- Note any repair resumes and downstream respawns after upstream repair.",
            "",
            "## Pending Work",
            "",
            "- Fill only if the run halted or intentionally left later steps pending.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def cmd_report_scaffold(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "state.json").is_file():
        _die(f"run_dir has no state.json: {run_dir}")
    report = _render_report_scaffold(run_dir)
    if args.write:
        path = run_dir / "report.md"
        _write_text(path, report)
        print(str(path))
    else:
        print(report, end="")
    return 0


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
    init.add_argument("--diagnostic-turn-cap", type=int, default=10)
    init.add_argument("--execution-json", default=None,
                      help="JSON object with execution defaults and preferences")
    init.add_argument(
        "--models-json",
        default=None,
        help=(
            "Deprecated compatibility input for step_model, step_effort, "
            "critic_model, critic_effort"
        ),
    )
    init.set_defaults(func=cmd_init_run)

    step = sub.add_parser("step-spawn", help="Spawn a fresh step sub-session")
    for a in ["--run-dir", "--target-repo", "--prompt-file", "--model", "--effort"]:
        step.add_argument(a, required=True)
    step.add_argument("--runtime", required=True, choices=["claude", "codex"])
    step.add_argument("--step-n", required=True, type=int)
    step.add_argument("--try-k", required=True, type=int)
    step.add_argument(
        "--origin-kind",
        choices=["fresh", "respawn-after-upstream"],
        default="fresh",
    )
    step.add_argument(
        "--origin-trigger-json",
        default=None,
        help="JSON object naming the diagnostic or upstream repair that caused this spawn",
    )
    step.set_defaults(func=cmd_step_spawn)

    resume = sub.add_parser("step-resume", help="Resume an existing step session")
    for a in ["--run-dir", "--target-repo", "--prompt-file", "--model",
              "--effort", "--session-id"]:
        resume.add_argument(a, required=True)
    resume.add_argument("--runtime", required=True, choices=["claude", "codex"])
    resume.add_argument("--step-n", required=True, type=int)
    resume.add_argument("--try-k", required=True, type=int)
    resume.add_argument(
        "--origin-trigger-json",
        default=None,
        help="JSON object naming the diagnostic record that caused this repair",
    )
    resume.set_defaults(func=cmd_step_resume)

    diagnose = sub.add_parser(
        "step-diagnose",
        help="Resume a worker session read-only and record diagnostic artifacts",
    )
    for a in ["--run-dir", "--target-repo", "--prompt-file", "--model",
              "--effort", "--session-id"]:
        diagnose.add_argument(a, required=True)
    diagnose.add_argument("--runtime", required=True, choices=["claude", "codex"])
    diagnose.add_argument("--step-n", required=True, type=int)
    diagnose.add_argument("--try-k", required=True, type=int)
    diagnose.add_argument("--round-k", required=True, type=int)
    diagnose.add_argument("--with-step-m", required=True, type=int)
    diagnose.set_defaults(func=cmd_step_diagnose)

    critic = sub.add_parser("critic-spawn", help="Spawn an ephemeral critic")
    for a in ["--run-dir", "--target-repo", "--prompt-file", "--model",
              "--effort", "--schema-file"]:
        critic.add_argument(a, required=True)
    critic.add_argument("--runtime", required=True, choices=["claude", "codex"])
    critic.add_argument("--step-n", required=True, type=int)
    critic.add_argument("--try-k", required=True, type=int)
    critic.set_defaults(func=cmd_critic_spawn)

    latest = sub.add_parser(
        "latest-session",
        help="Print latest try/session metadata for a step as JSON",
    )
    latest.add_argument("--run-dir", required=True)
    latest.add_argument("--step-n", required=True, type=int)
    latest.set_defaults(func=cmd_latest_session)

    upstream = sub.add_parser(
        "upstream-for",
        help="Print manifest-declared upstream artifacts and latest sessions for a step",
    )
    upstream.add_argument("--run-dir", required=True)
    upstream.add_argument("--step-n", required=True, type=int)
    upstream.set_defaults(func=cmd_upstream_for)

    report = sub.add_parser(
        "report-scaffold",
        help="Print or write a deterministic report.md scaffold",
    )
    report.add_argument("--run-dir", required=True)
    report.add_argument("--write", action="store_true")
    report.set_defaults(func=cmd_report_scaffold)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
