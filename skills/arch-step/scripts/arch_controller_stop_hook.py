#!/usr/bin/env python3
"""Codex Stop hook for the arch suite automatic controllers."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


IMPLEMENT_LOOP_STATE_RELATIVE_PATH = Path(".codex/implement-loop-state.json")
AUTO_PLAN_STATE_RELATIVE_PATH = Path(".codex/auto-plan-state.json")
ARCH_DOCS_AUTO_STATE_RELATIVE_PATH = Path(".codex/arch-docs-auto-state.json")
ARCH_DOCS_DEFAULT_LEDGER_RELATIVE_PATH = Path(".doc-audit-ledger.md")

IMPLEMENT_LOOP_COMMAND = "implement-loop"
AUTO_PLAN_COMMAND = "auto-plan"
ARCH_DOCS_AUTO_COMMAND = "arch-docs-auto"

AUTO_PLAN_STAGES = (
    "research",
    "deep-dive-pass-1",
    "deep-dive-pass-2",
    "phase-plan",
)

VERDICT_PATTERN = re.compile(r"^Verdict \(code\): (COMPLETE|NOT COMPLETE)\s*$", re.MULTILINE)
PLANNING_PASS_PATTERN = re.compile(
    r"^\s*(deep_dive_pass_1|deep_dive_pass_2|external_research_grounding):\s*(.+?)\s*$",
    re.MULTILINE,
)
DETAIL_LIMIT = 800
BLOCK_MARKERS = {
    "research_grounding": "<!-- arch_skill:block:research_grounding:start -->",
    "current_architecture": "<!-- arch_skill:block:current_architecture:start -->",
    "target_architecture": "<!-- arch_skill:block:target_architecture:start -->",
    "call_site_audit": "<!-- arch_skill:block:call_site_audit:start -->",
    "phase_plan": "<!-- arch_skill:block:phase_plan:start -->",
}
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


def derive_worklog_path(doc_path: Path) -> Path:
    return doc_path.with_name(f"{doc_path.stem}_WORKLOG.md")


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


def validate_session_id(
    payload: dict,
    state_path: Path,
    state: dict,
    command_name: str,
) -> bool:
    session_id = state.get("session_id")
    if session_id is None:
        state["session_id"] = payload.get("session_id")
        write_state(state_path, state)
        return True
    if not isinstance(session_id, str):
        clear_state(state_path)
        block_with_message(
            f"{command_name} controller state had a non-string session_id; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    return session_id == payload.get("session_id")


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


def run_fresh_audit(cwd: Path, doc_path_value: str) -> FreshAuditResult:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    prompt = (
        f"Use $arch-step audit-implementation {doc_path_value}\n"
        "Fresh context only. Update the authoritative implementation audit block and any reopened "
        "phase statuses in DOC_PATH. Keep the final response short."
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


def validate_implement_loop_state(payload: dict, state_path: Path) -> tuple[Path, str] | None:
    cwd = Path(payload["cwd"]).resolve()
    state = load_state(state_path, IMPLEMENT_LOOP_COMMAND)
    if state is None:
        return None
    if state.get("command") != IMPLEMENT_LOOP_COMMAND:
        return None
    if not validate_session_id(payload, state_path, state, IMPLEMENT_LOOP_COMMAND):
        return None
    doc_path_value = state.get("doc_path")
    if not isinstance(doc_path_value, str) or not doc_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "implement-loop controller state was missing doc_path; "
            "the loop was disarmed. Update the plan and worklog truthfully, then stop."
        )
    doc_path = resolve_path(cwd, doc_path_value)
    return doc_path, doc_path_value


def validate_auto_plan_state(payload: dict, state_path: Path) -> tuple[Path, str, dict] | None:
    cwd = Path(payload["cwd"]).resolve()
    state = load_state(state_path, AUTO_PLAN_COMMAND)
    if state is None:
        return None
    if state.get("command") != AUTO_PLAN_COMMAND:
        return None
    session_id = state.get("session_id")
    if isinstance(session_id, str) and session_id != payload.get("session_id"):
        return None
    if session_id is not None and not isinstance(session_id, str):
        clear_state(state_path)
        block_with_message(
            "auto-plan controller state had a non-string session_id; "
            "the controller was disarmed. Update the plan truthfully and stop."
        )

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
    return doc_path, doc_path_value, state


def validate_arch_docs_auto_state(
    payload: dict,
    state_path: Path,
) -> tuple[str, Path, dict] | None:
    cwd = Path(payload["cwd"]).resolve()
    state = load_state(state_path, ARCH_DOCS_AUTO_COMMAND)
    if state is None:
        return None
    if state.get("command") != ARCH_DOCS_AUTO_COMMAND:
        return None
    if not validate_session_id(payload, state_path, state, ARCH_DOCS_AUTO_COMMAND):
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
    return scope_summary, ledger_path, state


def auto_plan_stage_name(stage: str) -> str:
    return {
        "research": "research",
        "deep-dive-pass-1": "deep-dive pass 1",
        "deep-dive-pass-2": "deep-dive pass 2",
        "phase-plan": "phase-plan",
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
    raise RuntimeError(f"unexpected auto-plan stage: {stage}")


def auto_plan_continue_reason(doc_path_value: str, next_stage: str) -> str:
    if next_stage == "deep-dive-pass-1":
        return (
            f"auto-plan finished research for {doc_path_value}. Continue now with the next required command: "
            f"Use $arch-step deep-dive {doc_path_value}. This is deep-dive pass 1 of 2. "
            "Keep .codex/auto-plan-state.json armed and stop naturally when this command finishes."
        )
    if next_stage == "deep-dive-pass-2":
        return (
            f"auto-plan finished deep-dive pass 1 for {doc_path_value}. Continue now with the next required command: "
            f"Use $arch-step deep-dive {doc_path_value}. This is deep-dive pass 2 of 2. "
            "Keep .codex/auto-plan-state.json armed and stop naturally when this command finishes."
        )
    if next_stage == "phase-plan":
        return (
            f"auto-plan finished deep-dive pass 2 for {doc_path_value}. Continue now with the next required command: "
            f"Use $arch-step phase-plan {doc_path_value}. "
            "Keep .codex/auto-plan-state.json armed and stop naturally when this command finishes."
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


def handle_implement_loop(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    state_path = cwd / IMPLEMENT_LOOP_STATE_RELATIVE_PATH
    validated = validate_implement_loop_state(payload, state_path)
    if validated is None:
        return 0

    doc_path, doc_path_value = validated
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
            f"implement the missing code work, update {display_path(worklog_path, cwd)} if it exists, "
            "keep the loop armed, and stop again for another fresh audit."
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
    state_path = cwd / AUTO_PLAN_STATE_RELATIVE_PATH
    validated = validate_auto_plan_state(payload, state_path)
    if validated is None:
        return 0

    doc_path, doc_path_value, state = validated
    if not doc_path.exists():
        clear_state(state_path)
        block_with_message(
            f"auto-plan doc path does not exist: {doc_path_value}. "
            "The controller was disarmed. Update the plan truthfully and stop."
        )

    stage_index = state["stage_index"]
    current_stage = AUTO_PLAN_STAGES[stage_index]
    doc_text = read_doc_text(doc_path)
    if not doc_updated_since_state(doc_path, state_path) or not auto_plan_stage_complete(doc_text, current_stage):
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
            f"auto-plan completed for {doc_path_value}. Research, deep-dive pass 1, deep-dive pass 2, and phase-plan are in place. "
            f"The doc is ready for `Use $arch-step implement-loop {doc_path_value}`.",
            system_message="auto-plan completed; the doc is ready for implement-loop.",
        )

    next_stage = AUTO_PLAN_STAGES[next_index]
    if state.get("session_id") is None:
        state["session_id"] = payload.get("session_id")
    state["stage_index"] = next_index
    write_state(state_path, state)
    block_with_json(
        auto_plan_continue_reason(doc_path_value, next_stage),
        system_message=f"auto-plan finished {auto_plan_stage_name(current_stage)}; continuing to {auto_plan_stage_name(next_stage)}.",
    )


def handle_arch_docs_auto(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    state_path = cwd / ARCH_DOCS_AUTO_STATE_RELATIVE_PATH
    validated = validate_arch_docs_auto_state(payload, state_path)
    if validated is None:
        return 0

    scope_summary, ledger_path, state = validated
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
            f"arch-docs auto ran a fresh child evaluation and found more bounded docs cleanup for {scope_summary}. "
            "Continue now with the next required command: Use $arch-docs. "
            f"Current scope remains {scope_summary}. "
            "Keep .codex/arch-docs-auto-state.json armed and stop naturally when this command finishes."
        )
        if summary:
            reason += f" Evaluator summary: {summary}"
        block_with_json(
            reason,
            system_message="arch-docs auto evaluation finished; another bounded pass remains.",
        )

    clear_state(state_path)
    reason = (
        f"arch-docs auto ran a fresh child evaluation and stopped blocked for {scope_summary}. "
        "Do not keep looping. Explain the blocker and stop."
    )
    if summary:
        reason += f" Evaluator summary: {summary}"
    block_with_json(
        reason,
        system_message="arch-docs auto evaluation stopped blocked.",
    )


def main() -> int:
    payload = load_stop_payload()
    handle_implement_loop(payload)
    handle_auto_plan(payload)
    handle_arch_docs_auto(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
