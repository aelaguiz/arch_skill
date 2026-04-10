#!/usr/bin/env python3
"""Codex Stop hook for arch-step automatic controllers."""

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
IMPLEMENT_LOOP_COMMAND = "implement-loop"
AUTO_PLAN_COMMAND = "auto-plan"
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


@dataclass
class FreshAuditResult:
    process: subprocess.CompletedProcess[str]
    last_message: str | None


def load_stop_payload() -> dict:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid stop-hook input JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("invalid stop-hook input: expected a JSON object")
    return payload


def load_state(state_path: Path, command_name: str) -> dict | None:
    if not state_path.exists():
        return None
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        clear_state(state_path)
        block_with_message(
            f"arch-step {command_name} state was invalid JSON; the controller was disarmed. "
            "Fix the state contract, update the plan and worklog truthfully, and stop."
        )
    if not isinstance(state, dict):
        clear_state(state_path)
        block_with_message(
            f"arch-step {command_name} state was not a JSON object; the controller was disarmed. "
            "Fix the state contract, update the plan and worklog truthfully, and stop."
        )
    return state


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


def resolve_doc_path(cwd: Path, doc_path_value: str) -> Path:
    doc_path = Path(doc_path_value)
    if not doc_path.is_absolute():
        doc_path = cwd / doc_path
    return doc_path.resolve()


def derive_worklog_path(doc_path: Path) -> Path:
    return doc_path.with_name(f"{doc_path.stem}_WORKLOG.md")


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
            f"arch-step {command_name} state had a non-string session_id; the controller was disarmed. "
            "Update the plan and worklog truthfully, then stop."
        )
    return session_id == payload.get("session_id")


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
            "arch-step implement-loop state was missing doc_path; the loop was disarmed. "
            "Update the plan and worklog truthfully, then stop."
        )
    doc_path = resolve_doc_path(cwd, doc_path_value)
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
            "arch-step auto-plan state had a non-string session_id; the controller was disarmed. "
            "Update the plan truthfully, then stop."
        )

    doc_path_value = state.get("doc_path")
    if not isinstance(doc_path_value, str) or not doc_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "arch-step auto-plan state was missing doc_path; the controller was disarmed. "
            "Update the plan truthfully, then stop."
        )

    stages = state.get("stages")
    if stages is None:
        state["stages"] = list(AUTO_PLAN_STAGES)
        stages = state["stages"]
    if stages != list(AUTO_PLAN_STAGES):
        clear_state(state_path)
        block_with_message(
            "arch-step auto-plan state had an unexpected stages list; the controller was disarmed. "
            "Update the plan truthfully, then stop."
        )

    stage_index = state.get("stage_index")
    if not isinstance(stage_index, int) or not 0 <= stage_index < len(AUTO_PLAN_STAGES):
        clear_state(state_path)
        block_with_message(
            "arch-step auto-plan state had an invalid stage_index; the controller was disarmed. "
            "Update the plan truthfully, then stop."
        )

    doc_path = resolve_doc_path(cwd, doc_path_value)
    return doc_path, doc_path_value, state


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
            f"arch-step implement-loop doc path does not exist: {doc_path_value}. "
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
            f"Audit verdict is COMPLETE in {doc_path_value}."
        )
        if child_summary:
            stop_reason += f" Audit summary: {child_summary}"
        stop_with_json(
            stop_reason,
            system_message="implement-loop fresh audit finished clean.",
        )

    if verdict == "NOT COMPLETE":
        worklog_path = derive_worklog_path(doc_path)
        reason = (
            "implement-loop ran a fresh child audit and found more code work. "
            f"Read the authoritative Implementation Audit block and reopened phases in {doc_path_value}, "
            f"implement the missing code work, update {worklog_path.relative_to(cwd)} if it exists, "
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
            f"arch-step auto-plan doc path does not exist: {doc_path_value}. "
            "The controller was disarmed. Update the plan truthfully, then stop."
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


def main() -> int:
    payload = load_stop_payload()
    handle_implement_loop(payload)
    handle_auto_plan(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
