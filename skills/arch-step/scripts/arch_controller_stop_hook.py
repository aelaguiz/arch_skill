#!/usr/bin/env python3
"""Codex Stop hook for the arch suite automatic controllers."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


IMPLEMENT_LOOP_STATE_RELATIVE_PATH = Path(".codex/implement-loop-state.json")
AUTO_PLAN_STATE_RELATIVE_PATH = Path(".codex/auto-plan-state.json")
ARCH_DOCS_AUTO_STATE_RELATIVE_PATH = Path(".codex/arch-docs-auto-state.json")
AUDIT_LOOP_STATE_RELATIVE_PATH = Path(".codex/audit-loop-state.json")
AUDIT_LOOP_SIM_STATE_RELATIVE_PATH = Path(".codex/audit-loop-sim-state.json")
DELAY_POLL_STATE_RELATIVE_PATH = Path(".codex/delay-poll-state.json")
ARCH_DOCS_DEFAULT_LEDGER_RELATIVE_PATH = Path(".doc-audit-ledger.md")
AUDIT_LOOP_DEFAULT_LEDGER_RELATIVE_PATH = Path("_audit_ledger.md")
AUDIT_LOOP_SIM_DEFAULT_LEDGER_RELATIVE_PATH = Path("_audit_sim_ledger.md")

IMPLEMENT_LOOP_COMMAND = "implement-loop"
AUTO_PLAN_COMMAND = "auto-plan"
ARCH_DOCS_AUTO_COMMAND = "arch-docs-auto"
AUDIT_LOOP_COMMAND = "auto"
AUDIT_LOOP_SIM_COMMAND = "auto"
DELAY_POLL_COMMAND = "delay-poll"

IMPLEMENT_LOOP_DISPLAY_NAME = "implement-loop"
AUTO_PLAN_DISPLAY_NAME = "auto-plan"
ARCH_DOCS_AUTO_DISPLAY_NAME = "arch-docs auto"
AUDIT_LOOP_DISPLAY_NAME = "audit-loop auto"
AUDIT_LOOP_SIM_DISPLAY_NAME = "audit-loop-sim auto"
DELAY_POLL_DISPLAY_NAME = "delay-poll"


@dataclass(frozen=True)
class ControllerStateSpec:
    relative_path: Path
    expected_command: str
    display_name: str


@dataclass(frozen=True)
class ResolvedControllerState:
    spec: ControllerStateSpec
    state_path: Path
    is_legacy: bool


IMPLEMENT_LOOP_STATE_SPEC = ControllerStateSpec(
    relative_path=IMPLEMENT_LOOP_STATE_RELATIVE_PATH,
    expected_command=IMPLEMENT_LOOP_COMMAND,
    display_name=IMPLEMENT_LOOP_DISPLAY_NAME,
)
AUTO_PLAN_STATE_SPEC = ControllerStateSpec(
    relative_path=AUTO_PLAN_STATE_RELATIVE_PATH,
    expected_command=AUTO_PLAN_COMMAND,
    display_name=AUTO_PLAN_DISPLAY_NAME,
)
ARCH_DOCS_AUTO_STATE_SPEC = ControllerStateSpec(
    relative_path=ARCH_DOCS_AUTO_STATE_RELATIVE_PATH,
    expected_command=ARCH_DOCS_AUTO_COMMAND,
    display_name=ARCH_DOCS_AUTO_DISPLAY_NAME,
)
AUDIT_LOOP_STATE_SPEC = ControllerStateSpec(
    relative_path=AUDIT_LOOP_STATE_RELATIVE_PATH,
    expected_command=AUDIT_LOOP_COMMAND,
    display_name=AUDIT_LOOP_DISPLAY_NAME,
)
AUDIT_LOOP_SIM_STATE_SPEC = ControllerStateSpec(
    relative_path=AUDIT_LOOP_SIM_STATE_RELATIVE_PATH,
    expected_command=AUDIT_LOOP_SIM_COMMAND,
    display_name=AUDIT_LOOP_SIM_DISPLAY_NAME,
)
DELAY_POLL_STATE_SPEC = ControllerStateSpec(
    relative_path=DELAY_POLL_STATE_RELATIVE_PATH,
    expected_command=DELAY_POLL_COMMAND,
    display_name=DELAY_POLL_DISPLAY_NAME,
)

AUTO_PLAN_STAGES = (
    "research",
    "deep-dive-pass-1",
    "deep-dive-pass-2",
    "phase-plan",
    "consistency-pass",
)

VERDICT_PATTERN = re.compile(r"^Verdict \(code\): (COMPLETE|NOT COMPLETE)\s*$", re.MULTILINE)
PLANNING_PASS_PATTERN = re.compile(
    r"^\s*(deep_dive_pass_1|deep_dive_pass_2|external_research_grounding):\s*(.+?)\s*$",
    re.MULTILINE,
)
CONSISTENCY_PASS_DECISION_PATTERN = re.compile(
    r"^\s*-\s*Decision: proceed to implement\?\s*(yes|no)\s*$",
    re.MULTILINE,
)
DETAIL_LIMIT = 800
BLOCK_MARKERS = {
    "research_grounding": "<!-- arch_skill:block:research_grounding:start -->",
    "current_architecture": "<!-- arch_skill:block:current_architecture:start -->",
    "target_architecture": "<!-- arch_skill:block:target_architecture:start -->",
    "call_site_audit": "<!-- arch_skill:block:call_site_audit:start -->",
    "phase_plan": "<!-- arch_skill:block:phase_plan:start -->",
    "consistency_pass": "<!-- arch_skill:block:consistency_pass:start -->",
}
AUDIT_LOOP_CONTROLLER_START = "<!-- audit_loop:block:controller:start -->"
AUDIT_LOOP_CONTROLLER_END = "<!-- audit_loop:block:controller:end -->"
AUDIT_LOOP_SIM_CONTROLLER_START = "<!-- audit_loop_sim:block:controller:start -->"
AUDIT_LOOP_SIM_CONTROLLER_END = "<!-- audit_loop_sim:block:controller:end -->"
AUDIT_LOOP_VALID_VERDICTS = {"CONTINUE", "CLEAN", "BLOCKED"}
CONTROLLER_STATE_SPECS = (
    IMPLEMENT_LOOP_STATE_SPEC,
    AUTO_PLAN_STATE_SPEC,
    ARCH_DOCS_AUTO_STATE_SPEC,
    AUDIT_LOOP_STATE_SPEC,
    AUDIT_LOOP_SIM_STATE_SPEC,
    DELAY_POLL_STATE_SPEC,
)
ARCH_DOCS_EVAL_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "verdict",
        "summary",
        "next_action",
        "needs_another_pass",
        "reason",
        "blockers",
    ],
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["clean", "continue", "blocked"],
        },
        "summary": {"type": "string"},
        "next_action": {"type": "string"},
        "needs_another_pass": {"type": "boolean"},
        "reason": {"type": "string"},
        "blockers": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}
DELAY_POLL_CHECK_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "ready",
        "summary",
        "evidence",
    ],
    "properties": {
        "ready": {"type": "boolean"},
        "summary": {"type": "string"},
        "evidence": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}


@dataclass
class FreshAuditResult:
    process: subprocess.CompletedProcess[str]
    last_message: str | None


@dataclass
class FreshStructuredResult:
    process: subprocess.CompletedProcess[str]
    last_message: str | None
    payload: dict | None


def load_stop_payload() -> dict:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid stop-hook input JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("invalid stop-hook input: expected a JSON object")
    return payload


def clear_state(state_path: Path) -> None:
    if state_path.exists():
        state_path.unlink()


def write_state(state_path: Path, state: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def current_epoch_seconds() -> int:
    return int(time.time())


def sleep_for_seconds(seconds: int) -> None:
    if seconds > 0:
        time.sleep(seconds)


def block_with_message(message: str) -> None:
    sys.stderr.write(message.strip() + "\n")
    raise SystemExit(2)


def block_with_json(reason: str, system_message: str | None = None) -> None:
    payload: dict[str, object] = {
        "continue": True,
        "decision": "block",
        "reason": reason.strip(),
    }
    if system_message:
        payload["systemMessage"] = system_message.strip()
    sys.stdout.write(json.dumps(payload) + "\n")
    raise SystemExit(0)


def stop_with_json(stop_reason: str, system_message: str | None = None) -> None:
    payload: dict[str, object] = {
        "continue": False,
        "stopReason": stop_reason.strip(),
    }
    if system_message:
        payload["systemMessage"] = system_message.strip()
    sys.stdout.write(json.dumps(payload) + "\n")
    raise SystemExit(0)


def resolve_path(cwd: Path, path_value: str) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = cwd / path
    return path.resolve()


def display_path(path: Path, cwd: Path) -> str:
    try:
        return str(path.relative_to(cwd))
    except ValueError:
        return str(path)


def current_session_id(payload: dict) -> str | None:
    session_id = payload.get("session_id")
    if isinstance(session_id, str) and session_id:
        return session_id
    return None


def session_state_relative_path(relative_path: Path, session_id: str) -> Path:
    return relative_path.with_name(f"{relative_path.stem}.{session_id}{relative_path.suffix}")


def session_state_path(cwd: Path, relative_path: Path, session_id: str) -> Path:
    return cwd / session_state_relative_path(relative_path, session_id)


def derive_worklog_path(doc_path: Path) -> Path:
    return doc_path.with_name(f"{doc_path.stem}_WORKLOG.md")


def load_json_object_quiet(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def state_matches_session(
    state: dict | None,
    expected_command: str,
    session_id: str | None,
    *,
    allow_missing_session_id: bool,
) -> bool:
    if state is None or state.get("command") != expected_command:
        return False
    state_session_id = state.get("session_id")
    if state_session_id is None:
        return allow_missing_session_id
    return isinstance(state_session_id, str) and session_id is not None and state_session_id == session_id


def stop_for_duplicate_controller_states(
    cwd: Path,
    spec: ControllerStateSpec,
    paths: list[Path],
) -> None:
    duplicate_paths = ", ".join(display_path(path, cwd) for path in paths)
    stop_with_json(
        f"Multiple {spec.display_name} controller states are armed for this repo/session: {duplicate_paths}. "
        "Clear the duplicate state files so only one remains armed, then rerun the intended command.",
        system_message="Duplicate arch_skill controller states are armed.",
    )


def legacy_state_is_active_for_session(
    cwd: Path,
    spec: ControllerStateSpec,
    payload: dict,
) -> bool:
    legacy_path = cwd / spec.relative_path
    legacy_state = load_json_object_quiet(legacy_path)
    return state_matches_session(
        legacy_state,
        spec.expected_command,
        current_session_id(payload),
        allow_missing_session_id=True,
    )


def resolve_active_controller_state(
    payload: dict,
    spec: ControllerStateSpec,
) -> ResolvedControllerState | None:
    cwd = Path(payload["cwd"]).resolve()
    session_id = current_session_id(payload)
    session_path = (
        session_state_path(cwd, spec.relative_path, session_id)
        if session_id is not None
        else None
    )
    legacy_path = cwd / spec.relative_path
    legacy_active = legacy_state_is_active_for_session(cwd, spec, payload)
    if session_path is not None and session_path.exists():
        if legacy_active:
            stop_for_duplicate_controller_states(cwd, spec, [session_path, legacy_path])
        return ResolvedControllerState(spec=spec, state_path=session_path, is_legacy=False)
    if legacy_active:
        return ResolvedControllerState(spec=spec, state_path=legacy_path, is_legacy=True)
    return None


def resolve_controller_state_for_handler(
    payload: dict,
    spec: ControllerStateSpec,
) -> ResolvedControllerState | None:
    cwd = Path(payload["cwd"]).resolve()
    session_id = current_session_id(payload)
    session_path = (
        session_state_path(cwd, spec.relative_path, session_id)
        if session_id is not None
        else None
    )
    legacy_path = cwd / spec.relative_path
    legacy_active = legacy_state_is_active_for_session(cwd, spec, payload)
    if session_path is not None and session_path.exists():
        if legacy_active:
            stop_for_duplicate_controller_states(cwd, spec, [session_path, legacy_path])
        return ResolvedControllerState(spec=spec, state_path=session_path, is_legacy=False)
    if legacy_path.exists():
        return ResolvedControllerState(spec=spec, state_path=legacy_path, is_legacy=True)
    return None


def detect_active_controller_states(payload: dict) -> list[str]:
    cwd = Path(payload["cwd"]).resolve()
    active: list[str] = []
    for spec in CONTROLLER_STATE_SPECS:
        resolved_state = resolve_active_controller_state(payload, spec)
        if resolved_state is None:
            continue
        active.append(f"{spec.display_name} ({display_path(resolved_state.state_path, cwd)})")
    return active


def stop_for_conflicting_controller_states(payload: dict) -> None:
    active = detect_active_controller_states(payload)
    if len(active) <= 1:
        return
    armed_states = ", ".join(active)
    stop_with_json(
        "Multiple arch_skill auto controllers are armed for this repo/session: "
        f"{armed_states}. Clear the stale state files so only one controller remains armed, "
        "then rerun the intended command.",
        system_message="Multiple arch_skill auto controllers are armed.",
    )


def load_state(state_path: Path, command_name: str) -> dict | None:
    if not state_path.exists():
        return None
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        clear_state(state_path)
        block_with_message(
            f"{command_name} controller state at {state_path} was invalid JSON; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    if not isinstance(state, dict):
        clear_state(state_path)
        block_with_message(
            f"{command_name} controller state at {state_path} was not a JSON object; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    return state


def summarize_child_output(
    process: subprocess.CompletedProcess[str],
    last_message: str | None,
) -> str | None:
    for detail in (
        last_message,
        process.stderr.strip(),
        process.stdout.strip(),
    ):
        if detail:
            compact = " ".join(detail.split())
            if len(compact) > DETAIL_LIMIT:
                return compact[: DETAIL_LIMIT - 3] + "..."
            return compact
    return None


def load_controller_state(
    cwd: Path,
    resolved_state: ResolvedControllerState | None,
    command_name: str,
    expected_command: str,
) -> tuple[Path, dict, bool] | None:
    if resolved_state is None:
        return None
    state_path = resolved_state.state_path
    state = load_state(state_path, command_name)
    if state is None:
        return None
    if state.get("command") != expected_command:
        if resolved_state.is_legacy:
            return None
        clear_state(state_path)
        block_with_message(
            f"{command_name} controller state at {display_path(state_path, cwd)} had an unexpected command; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    return state_path, state, resolved_state.is_legacy


def validate_session_id(
    payload: dict,
    cwd: Path,
    state_path: Path,
    state: dict,
    command_name: str,
    *,
    allow_claim: bool,
) -> bool:
    payload_session_id = current_session_id(payload)
    if payload_session_id is None:
        clear_state(state_path)
        block_with_message(
            f"{command_name} controller state at {display_path(state_path, cwd)} could not validate session ownership "
            "because the Stop hook payload was missing session_id; the controller was disarmed. "
            "Update the repo truthfully and stop."
        )

    session_id = state.get("session_id")
    if session_id is None:
        if allow_claim:
            state["session_id"] = payload_session_id
            write_state(state_path, state)
            return True
        clear_state(state_path)
        block_with_message(
            f"{command_name} controller state at {display_path(state_path, cwd)} was missing session_id; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    if not isinstance(session_id, str):
        clear_state(state_path)
        block_with_message(
            f"{command_name} controller state at {display_path(state_path, cwd)} had a non-string session_id; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    if session_id != payload_session_id:
        if allow_claim:
            return False
        clear_state(state_path)
        block_with_message(
            f"{command_name} controller state at {display_path(state_path, cwd)} had a mismatched session_id; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    return True


def normalize_optional_string_list(
    state: dict,
    key: str,
    *,
    default: list[str] | None = None,
) -> list[str]:
    value = state.get(key)
    if value is None:
        normalized = list(default or [])
        state[key] = normalized
        return normalized
    if not isinstance(value, list):
        raise ValueError(f"{key} was not a list")
    normalized: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{key} contained a non-string or empty entry")
        normalized.append(item.strip())
    state[key] = normalized
    return normalized


def read_verdict(doc_path: Path) -> str | None:
    if not doc_path.exists():
        return None
    matches = VERDICT_PATTERN.findall(doc_path.read_text(encoding="utf-8"))
    if not matches:
        return None
    return matches[-1]


def read_doc_text(doc_path: Path) -> str:
    return doc_path.read_text(encoding="utf-8")


def parse_planning_passes(doc_text: str) -> dict[str, str]:
    return {match[0]: match[1].strip() for match in PLANNING_PASS_PATTERN.findall(doc_text)}


def pass_is_done(pass_value: str | None) -> bool:
    if pass_value is None:
        return False
    return pass_value.lower().startswith("done")


def doc_updated_since_state(doc_path: Path, state_path: Path) -> bool:
    return doc_path.stat().st_mtime_ns > state_path.stat().st_mtime_ns


def extract_marked_block(doc_text: str, marker_key: str) -> str | None:
    start_marker = BLOCK_MARKERS[marker_key]
    end_marker = start_marker.replace(":start -->", ":end -->")
    start = doc_text.find(start_marker)
    if start == -1:
        return None
    start += len(start_marker)
    end = doc_text.find(end_marker, start)
    if end == -1:
        return None
    return doc_text[start:end]


def consistency_pass_decision(doc_text: str) -> str | None:
    block = extract_marked_block(doc_text, "consistency_pass")
    if block is None:
        return None
    match = CONSISTENCY_PASS_DECISION_PATTERN.search(block)
    if not match:
        return None
    return match.group(1).lower()


def run_fresh_audit(cwd: Path, doc_path_value: str) -> FreshAuditResult:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    prompt = (
        f"Use $arch-step audit-implementation {doc_path_value}\n"
        "Fresh context only. Audit against the approved plan in DOC_PATH, not against any narrower "
        "execution-side rewrite. Update the authoritative implementation audit block and any reopened "
        "phase statuses in DOC_PATH. If implementation weakened requirements, scope, acceptance "
        "criteria, or phase obligations to hide unfinished work, fail it. Keep the final response short."
    )

    with tempfile.TemporaryDirectory(prefix="arch-step-implement-loop-") as temp_dir:
        last_message_path = Path(temp_dir) / "last_message.txt"
        process = subprocess.run(
            [
                codex,
                "exec",
                "--ephemeral",
                "--disable",
                "codex_hooks",
                "--cd",
                str(cwd),
                "--dangerously-bypass-approvals-and-sandbox",
                "-o",
                str(last_message_path),
                prompt,
            ],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        last_message = None
        if last_message_path.exists():
            last_message = last_message_path.read_text(encoding="utf-8").strip() or None
        return FreshAuditResult(process=process, last_message=last_message)


def run_arch_docs_evaluator(
    cwd: Path,
    scope_summary: str,
    state_path: Path,
    ledger_path_value: str,
) -> FreshStructuredResult:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    prompt = (
        "Use $arch-docs for the suite's INTERNAL AUTO EVALUATOR.\n"
        f"SCOPE_SUMMARY: {scope_summary}\n"
        f"STATE_PATH: {display_path(state_path, cwd)}\n"
        f"LEDGER_PATH: {ledger_path_value}\n"
        "Fresh context only. Stay read-only. Read the controller state, the resolved repo docs scope, and the "
        "temporary ledger if it still exists. Return structured JSON only."
    )

    with tempfile.TemporaryDirectory(prefix="arch-docs-auto-eval-") as temp_dir:
        temp_root = Path(temp_dir)
        schema_path = temp_root / "schema.json"
        last_message_path = temp_root / "last_message.json"
        schema_path.write_text(json.dumps(ARCH_DOCS_EVAL_SCHEMA), encoding="utf-8")
        process = subprocess.run(
            [
                codex,
                "exec",
                "--ephemeral",
                "--disable",
                "codex_hooks",
                "--cd",
                str(cwd),
                "--sandbox",
                "read-only",
                "--output-schema",
                str(schema_path),
                "-o",
                str(last_message_path),
                prompt,
            ],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        last_message = None
        payload = None
        if last_message_path.exists():
            last_message = last_message_path.read_text(encoding="utf-8").strip() or None
            if last_message:
                try:
                    parsed = json.loads(last_message)
                except json.JSONDecodeError:
                    parsed = None
                if isinstance(parsed, dict):
                    payload = parsed
        return FreshStructuredResult(process=process, last_message=last_message, payload=payload)


def run_fresh_review(cwd: Path) -> FreshAuditResult:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    prompt = (
        "Use $audit-loop review\n"
        "Fresh context only. Repair or update `_audit_ledger.md`, set the controller verdict truthfully, "
        "and keep the final response short."
    )

    with tempfile.TemporaryDirectory(prefix="audit-loop-review-") as temp_dir:
        last_message_path = Path(temp_dir) / "last_message.txt"
        process = subprocess.run(
            [
                codex,
                "exec",
                "--ephemeral",
                "--disable",
                "codex_hooks",
                "--cd",
                str(cwd),
                "--full-auto",
                "-o",
                str(last_message_path),
                prompt,
            ],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        last_message = None
        if last_message_path.exists():
            last_message = last_message_path.read_text(encoding="utf-8").strip() or None
        return FreshAuditResult(process=process, last_message=last_message)


def run_fresh_sim_review(cwd: Path) -> FreshAuditResult:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    prompt = (
        "Use $audit-loop-sim review\n"
        "Fresh context only. Repair or update `_audit_sim_ledger.md`, set the controller verdict truthfully, "
        "and keep the final response short."
    )

    with tempfile.TemporaryDirectory(prefix="audit-loop-sim-review-") as temp_dir:
        last_message_path = Path(temp_dir) / "last_message.txt"
        process = subprocess.run(
            [
                codex,
                "exec",
                "--ephemeral",
                "--disable",
                "codex_hooks",
                "--cd",
                str(cwd),
                "--full-auto",
                "-o",
                str(last_message_path),
                prompt,
            ],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        last_message = None
        if last_message_path.exists():
            last_message = last_message_path.read_text(encoding="utf-8").strip() or None
        return FreshAuditResult(process=process, last_message=last_message)


def run_delay_poll_check(cwd: Path, check_prompt: str) -> FreshStructuredResult:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    prompt = (
        "Use $delay-poll check\n"
        "Fresh context only. Stay read-only. Evaluate whether the waited-on condition is satisfied yet.\n"
        "<check_prompt>\n"
        f"{check_prompt.strip()}\n"
        "</check_prompt>\n"
        "Return structured JSON only."
    )

    with tempfile.TemporaryDirectory(prefix="delay-poll-check-") as temp_dir:
        temp_root = Path(temp_dir)
        schema_path = temp_root / "schema.json"
        last_message_path = temp_root / "last_message.json"
        schema_path.write_text(json.dumps(DELAY_POLL_CHECK_SCHEMA), encoding="utf-8")
        process = subprocess.run(
            [
                codex,
                "exec",
                "--ephemeral",
                "--disable",
                "codex_hooks",
                "--cd",
                str(cwd),
                "--sandbox",
                "read-only",
                "--output-schema",
                str(schema_path),
                "-o",
                str(last_message_path),
                prompt,
            ],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        last_message = None
        payload = None
        if last_message_path.exists():
            last_message = last_message_path.read_text(encoding="utf-8").strip() or None
            if last_message:
                try:
                    parsed = json.loads(last_message)
                except json.JSONDecodeError:
                    parsed = None
                if isinstance(parsed, dict):
                    payload = parsed
        return FreshStructuredResult(process=process, last_message=last_message, payload=payload)


def validate_implement_loop_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[Path, str, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        IMPLEMENT_LOOP_COMMAND,
        IMPLEMENT_LOOP_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    if not validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        IMPLEMENT_LOOP_COMMAND,
        allow_claim=is_legacy,
    ):
        return None
    doc_path_value = state.get("doc_path")
    if not isinstance(doc_path_value, str) or not doc_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "implement-loop controller state was missing doc_path; "
            "the loop was disarmed. Update the plan and worklog truthfully, then stop."
        )
    doc_path = resolve_path(cwd, doc_path_value)
    return doc_path, doc_path_value, state_path


def validate_auto_plan_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[Path, str, dict, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        AUTO_PLAN_COMMAND,
        AUTO_PLAN_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    if not validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        AUTO_PLAN_COMMAND,
        allow_claim=is_legacy,
    ):
        return None

    doc_path_value = state.get("doc_path")
    if not isinstance(doc_path_value, str) or not doc_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "auto-plan controller state was missing doc_path; "
            "the controller was disarmed. Update the plan truthfully and stop."
        )

    stages = state.get("stages")
    if stages is None:
        state["stages"] = list(AUTO_PLAN_STAGES)
        stages = state["stages"]
    if stages != list(AUTO_PLAN_STAGES):
        clear_state(state_path)
        block_with_message(
            "auto-plan controller state had an unexpected stages list; "
            "the controller was disarmed. Update the plan truthfully and stop."
        )

    stage_index = state.get("stage_index")
    if not isinstance(stage_index, int) or not 0 <= stage_index < len(AUTO_PLAN_STAGES):
        clear_state(state_path)
        block_with_message(
            "auto-plan controller state had an invalid stage_index; "
            "the controller was disarmed. Update the plan truthfully and stop."
        )

    doc_path = resolve_path(cwd, doc_path_value)
    return doc_path, doc_path_value, state, state_path


def validate_arch_docs_auto_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[str, Path, dict, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        ARCH_DOCS_AUTO_COMMAND,
        ARCH_DOCS_AUTO_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    if not validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        ARCH_DOCS_AUTO_COMMAND,
        allow_claim=is_legacy,
    ):
        return None

    scope_kind = state.get("scope_kind")
    if not isinstance(scope_kind, str) or not scope_kind.strip():
        clear_state(state_path)
        block_with_message(
            "arch-docs auto controller state was missing scope_kind; "
            "the controller was disarmed. Update the docs cleanup truthfully and stop."
        )
    scope_kind = scope_kind.strip()
    if scope_kind not in {"explicit-context", "arch-context", "repo"}:
        clear_state(state_path)
        block_with_message(
            "arch-docs auto controller state had an unsupported scope_kind; "
            "the controller was disarmed. Update the docs cleanup truthfully and stop."
        )

    scope_summary = state.get("scope_summary")
    if not isinstance(scope_summary, str) or not scope_summary.strip():
        clear_state(state_path)
        block_with_message(
            "arch-docs auto controller state was missing scope_summary; "
            "the controller was disarmed. Update the docs cleanup truthfully and stop."
        )
    scope_summary = scope_summary.strip()

    pass_index = state.get("pass_index")
    if not isinstance(pass_index, int) or pass_index < 0:
        clear_state(state_path)
        block_with_message(
            "arch-docs auto controller state had an invalid pass_index; "
            "the controller was disarmed. Update the docs cleanup truthfully and stop."
        )

    try:
        context_sources = normalize_optional_string_list(
            state,
            "context_sources",
            default=[],
        )
        context_paths = normalize_optional_string_list(
            state,
            "context_paths",
            default=[],
        )
    except ValueError as exc:
        clear_state(state_path)
        block_with_message(
            f"arch-docs auto controller state was invalid: {exc}; "
            "the controller was disarmed. Update the docs cleanup truthfully and stop."
        )
    write_required = False
    if scope_kind in {"explicit-context", "arch-context"} and not context_sources:
        state["context_sources"] = [scope_kind]
        write_required = True
    if scope_kind in {"explicit-context", "arch-context"} and not context_paths:
        clear_state(state_path)
        block_with_message(
            "arch-docs auto controller state was missing context_paths for a narrowed scope; "
            "the controller was disarmed. Update the docs cleanup truthfully and stop."
        )

    stop_condition = state.get("stop_condition")
    if not isinstance(stop_condition, str) or not stop_condition.strip():
        clear_state(state_path)
        block_with_message(
            "arch-docs auto controller state was missing stop_condition; "
            "the controller was disarmed. Update the docs cleanup truthfully and stop."
        )

    ledger_path_value = state.get("ledger_path")
    if not isinstance(ledger_path_value, str) or not ledger_path_value.strip():
        ledger_path_value = str(ARCH_DOCS_DEFAULT_LEDGER_RELATIVE_PATH)
        state["ledger_path"] = ledger_path_value
        write_required = True

    ledger_path = resolve_path(cwd, ledger_path_value)
    if write_required:
        write_state(state_path, state)
    return scope_summary, ledger_path, state, state_path


def validate_audit_loop_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[Path, str, dict, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        AUDIT_LOOP_DISPLAY_NAME,
        AUDIT_LOOP_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    if not validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        AUDIT_LOOP_DISPLAY_NAME,
        allow_claim=is_legacy,
    ):
        return None

    ledger_path_value = state.get("ledger_path", str(AUDIT_LOOP_DEFAULT_LEDGER_RELATIVE_PATH))
    if not isinstance(ledger_path_value, str) or not ledger_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "audit-loop auto controller state was missing ledger_path; "
            "the controller was disarmed. Update the ledger truthfully and stop."
        )

    ledger_path = resolve_path(cwd, ledger_path_value)
    return ledger_path, ledger_path_value, state, state_path


def validate_audit_loop_sim_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[Path, str, dict, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        AUDIT_LOOP_SIM_DISPLAY_NAME,
        AUDIT_LOOP_SIM_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    if not validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        AUDIT_LOOP_SIM_DISPLAY_NAME,
        allow_claim=is_legacy,
    ):
        return None

    ledger_path_value = state.get("ledger_path", str(AUDIT_LOOP_SIM_DEFAULT_LEDGER_RELATIVE_PATH))
    if not isinstance(ledger_path_value, str) or not ledger_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "audit-loop-sim auto controller state was missing ledger_path; "
            "the controller was disarmed. Update the ledger truthfully and stop."
        )

    ledger_path = resolve_path(cwd, ledger_path_value)
    return ledger_path, ledger_path_value, state, state_path


def validate_delay_poll_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[dict, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        DELAY_POLL_DISPLAY_NAME,
        DELAY_POLL_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    if not validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        DELAY_POLL_DISPLAY_NAME,
        allow_claim=is_legacy,
    ):
        return None

    write_required = False

    version = state.get("version")
    if version is None:
        state["version"] = 1
        write_required = True
    elif version != 1:
        clear_state(state_path)
        block_with_message(
            "delay-poll controller state had an unsupported version; "
            "the controller was disarmed. Update the wait state truthfully and stop."
        )

    interval_seconds = state.get("interval_seconds")
    if not isinstance(interval_seconds, int) or interval_seconds <= 0:
        clear_state(state_path)
        block_with_message(
            "delay-poll controller state was missing a positive interval_seconds; "
            "the controller was disarmed. Update the wait state truthfully and stop."
        )

    armed_at = state.get("armed_at")
    if not isinstance(armed_at, int) or armed_at <= 0:
        clear_state(state_path)
        block_with_message(
            "delay-poll controller state was missing a valid armed_at timestamp; "
            "the controller was disarmed. Update the wait state truthfully and stop."
        )

    deadline_at = state.get("deadline_at")
    if not isinstance(deadline_at, int) or deadline_at <= armed_at:
        clear_state(state_path)
        block_with_message(
            "delay-poll controller state was missing a valid deadline_at timestamp; "
            "the controller was disarmed. Update the wait state truthfully and stop."
        )

    check_prompt = state.get("check_prompt")
    if not isinstance(check_prompt, str) or not check_prompt.strip():
        clear_state(state_path)
        block_with_message(
            "delay-poll controller state was missing check_prompt; "
            "the controller was disarmed. Update the wait state truthfully and stop."
        )
    state["check_prompt"] = check_prompt.strip()

    resume_prompt = state.get("resume_prompt")
    if not isinstance(resume_prompt, str) or not resume_prompt.strip():
        clear_state(state_path)
        block_with_message(
            "delay-poll controller state was missing resume_prompt; "
            "the controller was disarmed. Update the wait state truthfully and stop."
        )
    state["resume_prompt"] = resume_prompt.strip()

    attempt_count = state.get("attempt_count")
    if attempt_count is None:
        state["attempt_count"] = 0
        write_required = True
    elif not isinstance(attempt_count, int) or attempt_count < 0:
        clear_state(state_path)
        block_with_message(
            "delay-poll controller state had an invalid attempt_count; "
            "the controller was disarmed. Update the wait state truthfully and stop."
        )

    last_check_at = state.get("last_check_at")
    if last_check_at is not None:
        if not isinstance(last_check_at, int) or last_check_at < armed_at:
            clear_state(state_path)
            block_with_message(
                "delay-poll controller state had an invalid last_check_at; "
                "the controller was disarmed. Update the wait state truthfully and stop."
            )

    last_summary = state.get("last_summary")
    if last_summary is None:
        state["last_summary"] = ""
        write_required = True
    elif not isinstance(last_summary, str):
        clear_state(state_path)
        block_with_message(
            "delay-poll controller state had a non-string last_summary; "
            "the controller was disarmed. Update the wait state truthfully and stop."
        )

    if write_required:
        write_state(state_path, state)
    return state, state_path


def read_audit_loop_controller_fields(ledger_path: Path) -> dict[str, str] | None:
    if not ledger_path.exists():
        return None
    text = ledger_path.read_text(encoding="utf-8")
    start = text.find(AUDIT_LOOP_CONTROLLER_START)
    end = text.find(AUDIT_LOOP_CONTROLLER_END)
    if start == -1 or end == -1 or end < start:
        return None
    block = text[start + len(AUDIT_LOOP_CONTROLLER_START) : end]
    fields: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def read_audit_loop_sim_controller_fields(ledger_path: Path) -> dict[str, str] | None:
    if not ledger_path.exists():
        return None
    text = ledger_path.read_text(encoding="utf-8")
    start = text.find(AUDIT_LOOP_SIM_CONTROLLER_START)
    end = text.find(AUDIT_LOOP_SIM_CONTROLLER_END)
    if start == -1 or end == -1 or end < start:
        return None
    block = text[start + len(AUDIT_LOOP_SIM_CONTROLLER_START) : end]
    fields: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def clean_gitignore(
    gitignore_path: Path,
    entry: str,
    created_by_skill: bool,
    entry_added: bool,
) -> None:
    if not entry_added or not gitignore_path.exists():
        return

    original_text = gitignore_path.read_text(encoding="utf-8")
    lines = original_text.splitlines()
    kept_lines = [line for line in lines if line.strip() != entry]
    trailing_newline = original_text.endswith("\n")

    if kept_lines:
        new_text = "\n".join(kept_lines)
        if trailing_newline or new_text:
            new_text += "\n"
        gitignore_path.write_text(new_text, encoding="utf-8")
        return

    if created_by_skill:
        gitignore_path.unlink()
    else:
        gitignore_path.write_text("", encoding="utf-8")


def cleanup_audit_loop_runtime_artifacts(cwd: Path, ledger_path: Path, state: dict) -> None:
    if ledger_path.exists():
        ledger_path.unlink()

    gitignore_path = cwd / ".gitignore"
    clean_gitignore(
        gitignore_path=gitignore_path,
        entry=str(AUDIT_LOOP_DEFAULT_LEDGER_RELATIVE_PATH),
        created_by_skill=bool(state.get("gitignore_created")),
        entry_added=bool(state.get("gitignore_entry_added")),
    )


def cleanup_audit_loop_sim_runtime_artifacts(cwd: Path, ledger_path: Path, state: dict) -> None:
    if ledger_path.exists():
        ledger_path.unlink()

    gitignore_path = cwd / ".gitignore"
    clean_gitignore(
        gitignore_path=gitignore_path,
        entry=str(AUDIT_LOOP_SIM_DEFAULT_LEDGER_RELATIVE_PATH),
        created_by_skill=bool(state.get("gitignore_created")),
        entry_added=bool(state.get("gitignore_entry_added")),
    )


def auto_plan_stage_name(stage: str) -> str:
    return {
        "research": "research",
        "deep-dive-pass-1": "deep-dive pass 1",
        "deep-dive-pass-2": "deep-dive pass 2",
        "phase-plan": "phase-plan",
        "consistency-pass": "consistency-pass",
    }[stage]


def auto_plan_stage_complete(doc_text: str, stage: str) -> bool:
    planning_passes = parse_planning_passes(doc_text)
    if stage == "research":
        return BLOCK_MARKERS["research_grounding"] in doc_text
    if stage == "deep-dive-pass-1":
        return (
            BLOCK_MARKERS["current_architecture"] in doc_text
            and BLOCK_MARKERS["target_architecture"] in doc_text
            and BLOCK_MARKERS["call_site_audit"] in doc_text
            and pass_is_done(planning_passes.get("deep_dive_pass_1"))
        )
    if stage == "deep-dive-pass-2":
        return (
            BLOCK_MARKERS["current_architecture"] in doc_text
            and BLOCK_MARKERS["target_architecture"] in doc_text
            and BLOCK_MARKERS["call_site_audit"] in doc_text
            and pass_is_done(planning_passes.get("deep_dive_pass_2"))
        )
    if stage == "phase-plan":
        return BLOCK_MARKERS["phase_plan"] in doc_text
    if stage == "consistency-pass":
        return consistency_pass_decision(doc_text) == "yes"
    raise RuntimeError(f"unexpected auto-plan stage: {stage}")


def auto_plan_stage_blocked(doc_text: str, stage: str) -> bool:
    if stage != "consistency-pass":
        return False
    return consistency_pass_decision(doc_text) == "no"


def auto_plan_continue_reason(doc_path_value: str, next_stage: str, state_path_value: str) -> str:
    if next_stage == "deep-dive-pass-1":
        return (
            f"auto-plan finished research for {doc_path_value}. Continue now with the next required command: "
            f"Use $arch-step deep-dive {doc_path_value}. This is deep-dive pass 1 of 2. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    if next_stage == "deep-dive-pass-2":
        return (
            f"auto-plan finished deep-dive pass 1 for {doc_path_value}. Continue now with the next required command: "
            f"Use $arch-step deep-dive {doc_path_value}. This is deep-dive pass 2 of 2. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    if next_stage == "phase-plan":
        return (
            f"auto-plan finished deep-dive pass 2 for {doc_path_value}. Continue now with the next required command: "
            f"Use $arch-step phase-plan {doc_path_value}. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    if next_stage == "consistency-pass":
        return (
            f"auto-plan finished phase-plan for {doc_path_value}. Continue now with the next required command: "
            f"Use $arch-step consistency-pass {doc_path_value}. This is the required end-to-end consistency cold read. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    raise RuntimeError(f"unexpected next auto-plan stage: {next_stage}")


def arch_docs_eval_summary(result: dict) -> str:
    summary = str(result.get("summary", "")).strip()
    reason = str(result.get("reason", "")).strip()
    next_action = str(result.get("next_action", "")).strip()
    parts = [part for part in (summary, reason) if part]
    if next_action:
        parts.append(f"Next action: {next_action}")
    compact = " ".join(parts)
    if len(compact) > DETAIL_LIMIT:
        return compact[: DETAIL_LIMIT - 3] + "..."
    return compact


def delay_poll_result_summary(summary: str, evidence: list[str]) -> str:
    parts = [summary.strip()]
    cleaned_evidence = [item.strip() for item in evidence if item.strip()]
    if cleaned_evidence:
        parts.append("Evidence: " + "; ".join(cleaned_evidence))
    compact = " ".join(part for part in parts if part)
    if len(compact) > DETAIL_LIMIT:
        return compact[: DETAIL_LIMIT - 3] + "..."
    return compact


def delay_poll_sleep_reason(
    next_due_at: int,
    deadline_at: int,
) -> int:
    now = current_epoch_seconds()
    wait_until = min(next_due_at, deadline_at)
    return max(wait_until - now, 0)


def handle_implement_loop(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, IMPLEMENT_LOOP_STATE_SPEC)
    validated = validate_implement_loop_state(payload, resolved_state)
    if validated is None:
        return 0

    doc_path, doc_path_value, state_path = validated
    if not doc_path.exists():
        clear_state(state_path)
        block_with_message(
            f"implement-loop doc path does not exist: {doc_path_value}. "
            "The loop was disarmed. Update the plan and worklog truthfully, then stop."
        )

    try:
        audit = run_fresh_audit(cwd, doc_path_value)
    except RuntimeError as exc:
        clear_state(state_path)
        block_with_message(
            f"fresh implement-loop audit could not start: {exc}. "
            "The loop was disarmed. Explain the blocker and stop."
        )

    child_summary = summarize_child_output(audit.process, audit.last_message)

    if audit.process.returncode != 0:
        clear_state(state_path)
        failure = child_summary or "unknown child-audit failure"
        block_with_json(
            "implement-loop ran a fresh child audit, but that audit failed. "
            f"Failure: {failure}. Treat the run as blocked, update the plan and worklog truthfully, explain the blocker, and stop.",
            system_message="implement-loop fresh audit failed; review the blocker and stop honestly.",
        )

    verdict = read_verdict(doc_path)
    if verdict == "COMPLETE":
        clear_state(state_path)
        stop_reason = (
            "implement-loop fresh audit finished clean. "
            f"Audit verdict is COMPLETE in {doc_path_value}. "
            f"The next required move is `Use $arch-docs`. Current DOC_PATH: {doc_path_value}."
        )
        if child_summary:
            stop_reason += f" Audit summary: {child_summary}"
        stop_with_json(
            stop_reason,
            system_message="implement-loop fresh audit finished clean; hand off to arch-docs.",
        )

    if verdict == "NOT COMPLETE":
        worklog_path = derive_worklog_path(doc_path)
        reason = (
            "implement-loop ran a fresh child audit and found more code work. "
            f"Read the authoritative Implementation Audit block and reopened phases in {doc_path_value}, "
            f"implement the missing code work, run the smallest credible proof checks for the claimed fixes, "
            f"update {display_path(worklog_path, cwd)} if it exists, keep the loop armed, "
            "and do not rewrite plan requirements, scope, acceptance criteria, or phase obligations while coding. "
            "If the audit shows the plan itself needs to change, stop and repair the plan instead of continuing on a rewritten story, "
            "and only then stop again for another fresh audit."
        )
        if child_summary:
            reason += f" Audit summary: {child_summary}"
        block_with_json(
            reason,
            system_message="implement-loop fresh audit finished; more work remains.",
        )

    clear_state(state_path)
    reason = (
        f"implement-loop ran a fresh child audit, but that audit did not leave a usable verdict in {doc_path_value}. "
        "The loop was disarmed. Treat the run as blocked, update the plan and worklog truthfully, explain the blocker, and stop."
    )
    if child_summary:
        reason += f" Audit summary: {child_summary}"
    block_with_json(
        reason,
        system_message="implement-loop fresh audit finished without a usable verdict.",
    )


def handle_auto_plan(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, AUTO_PLAN_STATE_SPEC)
    validated = validate_auto_plan_state(payload, resolved_state)
    if validated is None:
        return 0

    doc_path, doc_path_value, state, state_path = validated
    state_path_value = display_path(state_path, cwd)
    if not doc_path.exists():
        clear_state(state_path)
        block_with_message(
            f"auto-plan doc path does not exist: {doc_path_value}. "
            "The controller was disarmed. Update the plan truthfully and stop."
        )

    stage_index = state["stage_index"]
    current_stage = AUTO_PLAN_STAGES[stage_index]
    doc_text = read_doc_text(doc_path)
    if not doc_updated_since_state(doc_path, state_path):
        clear_state(state_path)
        stop_with_json(
            f"auto-plan stopped before {auto_plan_stage_name(current_stage)} completed for {doc_path_value}. "
            "The controller was disarmed. Resolve the blocker or finish the stage manually, then rerun "
            f"`Use $arch-step auto-plan {doc_path_value}` if you still want automatic planning continuation.",
            system_message=f"auto-plan stopped before {auto_plan_stage_name(current_stage)} completed.",
        )
    if auto_plan_stage_blocked(doc_text, current_stage):
        clear_state(state_path)
        stop_with_json(
            f"auto-plan stopped after consistency-pass for {doc_path_value}. "
            "The helper block does not currently approve implementation. Resolve the remaining inconsistencies in the main "
            f"artifact, then rerun `Use $arch-step auto-plan {doc_path_value}` if you still want automatic planning continuation.",
            system_message="auto-plan consistency-pass did not approve implementation.",
        )
    if not auto_plan_stage_complete(doc_text, current_stage):
        clear_state(state_path)
        stop_with_json(
            f"auto-plan stopped before {auto_plan_stage_name(current_stage)} completed for {doc_path_value}. "
            "The controller was disarmed. Resolve the blocker or finish the stage manually, then rerun "
            f"`Use $arch-step auto-plan {doc_path_value}` if you still want automatic planning continuation.",
            system_message=f"auto-plan stopped before {auto_plan_stage_name(current_stage)} completed.",
        )

    next_index = stage_index + 1
    if next_index >= len(AUTO_PLAN_STAGES):
        clear_state(state_path)
        stop_with_json(
            f"auto-plan completed for {doc_path_value}. Research, deep-dive pass 1, deep-dive pass 2, phase-plan, and consistency-pass are in place. "
            f"The doc is ready for `Use $arch-step implement-loop {doc_path_value}`.",
            system_message="auto-plan completed; the doc is ready for implement-loop.",
        )

    next_stage = AUTO_PLAN_STAGES[next_index]
    state["stage_index"] = next_index
    write_state(state_path, state)
    block_with_json(
        auto_plan_continue_reason(doc_path_value, next_stage, state_path_value),
        system_message=f"auto-plan finished {auto_plan_stage_name(current_stage)}; continuing to {auto_plan_stage_name(next_stage)}.",
    )


def handle_arch_docs_auto(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, ARCH_DOCS_AUTO_STATE_SPEC)
    validated = validate_arch_docs_auto_state(payload, resolved_state)
    if validated is None:
        return 0

    scope_summary, ledger_path, state, state_path = validated
    state_path_value = display_path(state_path, cwd)
    try:
        evaluator = run_arch_docs_evaluator(
            cwd,
            scope_summary,
            state_path,
            display_path(ledger_path, cwd),
        )
    except RuntimeError as exc:
        clear_state(state_path)
        block_with_message(
            f"fresh arch-docs evaluation could not start: {exc}. "
            "The controller was disarmed. Explain the blocker and stop."
        )

    child_summary = summarize_child_output(evaluator.process, evaluator.last_message)
    if evaluator.process.returncode != 0:
        clear_state(state_path)
        failure = child_summary or "unknown child-evaluator failure"
        block_with_json(
            "arch-docs auto ran a fresh child evaluation, but that evaluation failed. "
            f"Failure: {failure}. Treat the docs cleanup as blocked, explain the blocker, and stop.",
            system_message="arch-docs auto fresh evaluation failed; review the blocker and stop honestly.",
        )

    result = evaluator.payload
    if not isinstance(result, dict):
        clear_state(state_path)
        reason = (
            "arch-docs auto ran a fresh child evaluation, but the evaluator did not return usable structured JSON. "
            "The controller was disarmed. Treat the docs cleanup as blocked, explain the blocker, and stop."
        )
        if child_summary:
            reason += f" Evaluator output: {child_summary}"
        block_with_json(
            reason,
            system_message="arch-docs auto evaluation finished without usable structured output.",
        )

    verdict = result.get("verdict")
    if verdict not in {"clean", "continue", "blocked"}:
        clear_state(state_path)
        block_with_json(
            "arch-docs auto evaluation returned an unexpected verdict. "
            "The controller was disarmed. Treat the docs cleanup as blocked and stop.",
            system_message="arch-docs auto evaluation returned an unexpected verdict.",
        )

    summary = arch_docs_eval_summary(result)

    if verdict == "clean":
        clear_state(state_path)
        stop_reason = (
            f"arch-docs auto finished clean for {scope_summary}. "
            "The docs cleanup stop condition is complete."
        )
        if summary:
            stop_reason += f" Evaluator summary: {summary}"
        stop_with_json(
            stop_reason,
            system_message="arch-docs auto finished clean.",
        )

    if verdict == "continue":
        pass_index = state["pass_index"] + 1
        state["pass_index"] = pass_index
        write_state(state_path, state)
        reason = (
            f"arch-docs auto ran a fresh child evaluation and found more grounded docs cleanup for {scope_summary}. "
            "Continue now with the next required command: Use $arch-docs. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
        if summary:
            reason += f" Evaluator summary: {summary}"
        block_with_json(
            reason,
            system_message="arch-docs auto evaluation finished; another grounded pass remains.",
        )

    clear_state(state_path)
    reason = (
        f"arch-docs auto ran a fresh child evaluation and found no credible grounded next pass for {scope_summary}. "
        "Do not keep looping. Explain the blocker and stop."
    )
    if summary:
        reason += f" Evaluator summary: {summary}"
    block_with_json(
        reason,
        system_message="arch-docs auto evaluation stopped: no credible grounded next pass.",
    )


def handle_audit_loop(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, AUDIT_LOOP_STATE_SPEC)
    validated = validate_audit_loop_state(payload, resolved_state)
    if validated is None:
        return 0

    ledger_path, ledger_path_value, state, state_path = validated
    state_path_value = display_path(state_path, cwd)

    try:
        review = run_fresh_review(cwd)
    except RuntimeError as exc:
        clear_state(state_path)
        stop_with_json(
            f"audit-loop could not start a fresh review pass: {exc}. The controller was disarmed.",
            system_message="audit-loop fresh review could not start.",
        )

    child_summary = summarize_child_output(review.process, review.last_message)
    if review.process.returncode != 0:
        clear_state(state_path)
        reason = "audit-loop ran a fresh review pass, but that review failed."
        if child_summary:
            reason += f" Failure: {child_summary}."
        stop_with_json(
            reason + " Treat the run as blocked, keep the ledger, and stop honestly.",
            system_message="audit-loop fresh review failed.",
        )

    fields = read_audit_loop_controller_fields(ledger_path)
    if not fields:
        clear_state(state_path)
        reason = (
            f"audit-loop fresh review finished, but {ledger_path_value} does not contain a usable controller block. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="audit-loop review left no usable controller block.")

    verdict = fields.get("Verdict", "").strip().upper()
    if verdict not in AUDIT_LOOP_VALID_VERDICTS:
        clear_state(state_path)
        reason = (
            f"audit-loop fresh review finished, but {ledger_path_value} has an invalid verdict. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="audit-loop review left an invalid verdict.")

    if verdict == "CLEAN":
        clear_state(state_path)
        cleanup_audit_loop_runtime_artifacts(cwd, ledger_path, state)
        stop_reason = "audit-loop fresh review finished clean. The audit ledger was removed."
        if child_summary:
            stop_reason += f" Review summary: {child_summary}"
        stop_with_json(stop_reason, system_message="audit-loop completed clean.")

    if verdict == "BLOCKED":
        clear_state(state_path)
        stop_reason = fields.get("Stop Reason") or "audit-loop review marked the loop blocked."
        if child_summary:
            stop_reason += f" Review summary: {child_summary}"
        stop_with_json(stop_reason, system_message="audit-loop stopped blocked.")

    next_area = fields.get("Next Area", "").strip()
    if not next_area:
        clear_state(state_path)
        reason = (
            f"audit-loop review returned CONTINUE without Next Area in {ledger_path_value}. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="audit-loop review omitted Next Area.")

    reason = (
        f"audit-loop fresh review found more worthwhile work. Continue now with `Use $audit-loop`. "
        f"Next area: {next_area}. Keep {state_path_value} armed and stop naturally when this pass finishes."
    )
    if child_summary:
        reason += f" Review summary: {child_summary}"
    block_with_json(reason, system_message="audit-loop review found more work.")


def handle_audit_loop_sim(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, AUDIT_LOOP_SIM_STATE_SPEC)
    validated = validate_audit_loop_sim_state(payload, resolved_state)
    if validated is None:
        return 0

    ledger_path, ledger_path_value, state, state_path = validated
    state_path_value = display_path(state_path, cwd)

    try:
        review = run_fresh_sim_review(cwd)
    except RuntimeError as exc:
        clear_state(state_path)
        stop_with_json(
            f"audit-loop-sim could not start a fresh review pass: {exc}. The controller was disarmed.",
            system_message="audit-loop-sim fresh review could not start.",
        )

    child_summary = summarize_child_output(review.process, review.last_message)
    if review.process.returncode != 0:
        clear_state(state_path)
        reason = "audit-loop-sim ran a fresh review pass, but that review failed."
        if child_summary:
            reason += f" Failure: {child_summary}."
        stop_with_json(
            reason + " Treat the run as blocked, keep the ledger, and stop honestly.",
            system_message="audit-loop-sim fresh review failed.",
        )

    fields = read_audit_loop_sim_controller_fields(ledger_path)
    if not fields:
        clear_state(state_path)
        reason = (
            f"audit-loop-sim fresh review finished, but {ledger_path_value} does not contain a usable controller block. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="audit-loop-sim review left no usable controller block.")

    verdict = fields.get("Verdict", "").strip().upper()
    if verdict not in AUDIT_LOOP_VALID_VERDICTS:
        clear_state(state_path)
        reason = (
            f"audit-loop-sim fresh review finished, but {ledger_path_value} has an invalid verdict. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="audit-loop-sim review left an invalid verdict.")

    if verdict == "CLEAN":
        clear_state(state_path)
        cleanup_audit_loop_sim_runtime_artifacts(cwd, ledger_path, state)
        stop_reason = "audit-loop-sim fresh review finished clean. The audit sim ledger was removed."
        if child_summary:
            stop_reason += f" Review summary: {child_summary}"
        stop_with_json(stop_reason, system_message="audit-loop-sim completed clean.")

    if verdict == "BLOCKED":
        clear_state(state_path)
        stop_reason = fields.get("Stop Reason") or "audit-loop-sim review marked the loop blocked."
        if child_summary:
            stop_reason += f" Review summary: {child_summary}"
        stop_with_json(stop_reason, system_message="audit-loop-sim stopped blocked.")

    next_area = fields.get("Next Area", "").strip()
    if not next_area:
        clear_state(state_path)
        reason = (
            f"audit-loop-sim review returned CONTINUE without Next Area in {ledger_path_value}. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="audit-loop-sim review omitted Next Area.")

    reason = (
        f"audit-loop-sim fresh review found more worthwhile automation work. Continue now with `Use $audit-loop-sim`. "
        f"Next area: {next_area}. Keep {state_path_value} armed and stop naturally when this pass finishes."
    )
    if child_summary:
        reason += f" Review summary: {child_summary}"
    block_with_json(reason, system_message="audit-loop-sim review found more work.")


def handle_delay_poll(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, DELAY_POLL_STATE_SPEC)
    validated = validate_delay_poll_state(payload, resolved_state)
    if validated is None:
        return 0

    state, state_path = validated
    state_path_value = display_path(state_path, cwd)

    while True:
        now = current_epoch_seconds()
        deadline_at = state["deadline_at"]
        last_check_at = state.get("last_check_at")
        interval_seconds = state["interval_seconds"]
        next_due_at = state["armed_at"] if last_check_at is None else last_check_at + interval_seconds

        if now >= deadline_at and now < next_due_at:
            clear_state(state_path)
            stop_reason = (
                "delay-poll timed out before the waited-on condition became true. "
                f"The controller reached its deadline with {state['attempt_count']} completed checks."
            )
            if state["last_summary"].strip():
                stop_reason += f" Last check summary: {state['last_summary'].strip()}"
            stop_with_json(stop_reason, system_message="delay-poll timed out without success.")

        if now < next_due_at:
            sleep_for_seconds(delay_poll_sleep_reason(next_due_at, deadline_at))
            continue

        try:
            check = run_delay_poll_check(cwd, state["check_prompt"])
        except RuntimeError as exc:
            clear_state(state_path)
            stop_with_json(
                f"delay-poll could not start a fresh check: {exc}. The controller was disarmed.",
                system_message="delay-poll fresh check could not start.",
            )

        child_summary = summarize_child_output(check.process, check.last_message)
        if check.process.returncode != 0:
            clear_state(state_path)
            stop_reason = "delay-poll ran a fresh check, but that check failed."
            if child_summary:
                stop_reason += f" Failure: {child_summary}."
            stop_with_json(
                stop_reason + " Treat the wait as blocked and stop honestly.",
                system_message="delay-poll fresh check failed.",
            )

        result = check.payload
        if not isinstance(result, dict):
            clear_state(state_path)
            reason = (
                "delay-poll ran a fresh check, but the checker did not return usable structured JSON. "
                "The controller was disarmed."
            )
            if child_summary:
                reason += f" Checker output: {child_summary}"
            stop_with_json(
                reason,
                system_message="delay-poll fresh check returned unusable output.",
            )

        ready = result.get("ready")
        summary = result.get("summary")
        evidence = result.get("evidence")
        if not isinstance(ready, bool) or not isinstance(summary, str) or not isinstance(evidence, list):
            clear_state(state_path)
            stop_with_json(
                "delay-poll fresh check returned an invalid payload. The controller was disarmed.",
                system_message="delay-poll fresh check returned an invalid payload.",
            )

        cleaned_evidence: list[str] = []
        for item in evidence:
            if not isinstance(item, str) or not item.strip():
                clear_state(state_path)
                stop_with_json(
                    "delay-poll fresh check returned invalid evidence entries. The controller was disarmed.",
                    system_message="delay-poll fresh check returned invalid evidence entries.",
                )
            cleaned_evidence.append(item.strip())

        summary_text = summary.strip()
        if not summary_text:
            clear_state(state_path)
            stop_with_json(
                "delay-poll fresh check returned a blank summary. The controller was disarmed.",
                system_message="delay-poll fresh check returned a blank summary.",
            )

        state["attempt_count"] += 1
        state["last_check_at"] = now
        state["last_summary"] = summary_text
        write_state(state_path, state)

        result_summary = delay_poll_result_summary(summary_text, cleaned_evidence)
        if ready:
            clear_state(state_path)
            reason = (
                f"{state['resume_prompt']} Latest check summary: {result_summary}. "
                f"Resume from this new truth and continue the same task. Former wait state: {state_path_value}."
            )
            block_with_json(
                reason,
                system_message="delay-poll condition is now true; continuing the task.",
            )

        if current_epoch_seconds() >= deadline_at:
            clear_state(state_path)
            stop_reason = (
                "delay-poll timed out before the waited-on condition became true. "
                f"The controller reached its deadline with {state['attempt_count']} completed checks. "
                f"Last check summary: {result_summary}"
            )
            stop_with_json(stop_reason, system_message="delay-poll timed out without success.")


def main() -> int:
    payload = load_stop_payload()
    stop_for_conflicting_controller_states(payload)
    handle_implement_loop(payload)
    handle_auto_plan(payload)
    handle_arch_docs_auto(payload)
    handle_audit_loop(payload)
    handle_audit_loop_sim(payload)
    handle_delay_poll(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
