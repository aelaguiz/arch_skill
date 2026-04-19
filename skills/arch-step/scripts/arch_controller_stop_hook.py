#!/usr/bin/env python3
"""Runtime-aware Stop hook for the arch suite automatic controllers."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


RUNTIME_CODEX = "codex"
RUNTIME_CLAUDE = "claude"
SUPPORTED_RUNTIMES = (RUNTIME_CODEX, RUNTIME_CLAUDE)
# Claude child runs must keep normal host auth but must not recurse through hooks.
CLAUDE_CHILD_SETTINGS_JSON = json.dumps({"disableAllHooks": True})

IMPLEMENT_LOOP_STATE_FILE = Path("implement-loop-state.json")
AUTO_PLAN_STATE_FILE = Path("auto-plan-state.json")
MINIARCH_STEP_IMPLEMENT_LOOP_STATE_FILE = Path("miniarch-step-implement-loop-state.json")
MINIARCH_STEP_AUTO_PLAN_STATE_FILE = Path("miniarch-step-auto-plan-state.json")
ARCH_DOCS_AUTO_STATE_FILE = Path("arch-docs-auto-state.json")
AUDIT_LOOP_STATE_FILE = Path("audit-loop-state.json")
COMMENT_LOOP_STATE_FILE = Path("comment-loop-state.json")
AUDIT_LOOP_SIM_STATE_FILE = Path("audit-loop-sim-state.json")
DELAY_POLL_STATE_FILE = Path("delay-poll-state.json")
CODE_REVIEW_STATE_FILE = Path("code-review-state.json")
WAIT_STATE_FILE = Path("wait-state.json")
ARCH_LOOP_STATE_FILE = Path("arch-loop-state.json")
IMPLEMENT_LOOP_STATE_RELATIVE_PATH = Path(".codex") / IMPLEMENT_LOOP_STATE_FILE
AUTO_PLAN_STATE_RELATIVE_PATH = Path(".codex") / AUTO_PLAN_STATE_FILE
MINIARCH_STEP_IMPLEMENT_LOOP_STATE_RELATIVE_PATH = Path(".codex") / MINIARCH_STEP_IMPLEMENT_LOOP_STATE_FILE
MINIARCH_STEP_AUTO_PLAN_STATE_RELATIVE_PATH = Path(".codex") / MINIARCH_STEP_AUTO_PLAN_STATE_FILE
ARCH_DOCS_AUTO_STATE_RELATIVE_PATH = Path(".codex") / ARCH_DOCS_AUTO_STATE_FILE
AUDIT_LOOP_STATE_RELATIVE_PATH = Path(".codex") / AUDIT_LOOP_STATE_FILE
COMMENT_LOOP_STATE_RELATIVE_PATH = Path(".codex") / COMMENT_LOOP_STATE_FILE
AUDIT_LOOP_SIM_STATE_RELATIVE_PATH = Path(".codex") / AUDIT_LOOP_SIM_STATE_FILE
DELAY_POLL_STATE_RELATIVE_PATH = Path(".codex") / DELAY_POLL_STATE_FILE
CODE_REVIEW_STATE_RELATIVE_PATH = Path(".codex") / CODE_REVIEW_STATE_FILE
WAIT_STATE_RELATIVE_PATH = Path(".codex") / WAIT_STATE_FILE
ARCH_LOOP_STATE_RELATIVE_PATH = Path(".codex") / ARCH_LOOP_STATE_FILE
ARCH_DOCS_DEFAULT_LEDGER_RELATIVE_PATH = Path(".doc-audit-ledger.md")
AUDIT_LOOP_DEFAULT_LEDGER_RELATIVE_PATH = Path("_audit_ledger.md")
COMMENT_LOOP_DEFAULT_LEDGER_RELATIVE_PATH = Path("_comment_ledger.md")
AUDIT_LOOP_SIM_DEFAULT_LEDGER_RELATIVE_PATH = Path("_audit_sim_ledger.md")

IMPLEMENT_LOOP_COMMAND = "implement-loop"
AUTO_PLAN_COMMAND = "auto-plan"
MINIARCH_STEP_IMPLEMENT_LOOP_COMMAND = "miniarch-step-implement-loop"
MINIARCH_STEP_AUTO_PLAN_COMMAND = "miniarch-step-auto-plan"
ARCH_DOCS_AUTO_COMMAND = "arch-docs-auto"
AUDIT_LOOP_COMMAND = "auto"
COMMENT_LOOP_COMMAND = "auto"
AUDIT_LOOP_SIM_COMMAND = "auto"
DELAY_POLL_COMMAND = "delay-poll"
CODE_REVIEW_COMMAND = "code-review"
WAIT_COMMAND = "wait"
ARCH_LOOP_COMMAND = "arch-loop"

IMPLEMENT_LOOP_DISPLAY_NAME = "implement-loop"
AUTO_PLAN_DISPLAY_NAME = "auto-plan"
MINIARCH_STEP_IMPLEMENT_LOOP_DISPLAY_NAME = "miniarch-step implement-loop"
MINIARCH_STEP_AUTO_PLAN_DISPLAY_NAME = "miniarch-step auto-plan"
ARCH_DOCS_AUTO_DISPLAY_NAME = "arch-docs auto"
AUDIT_LOOP_DISPLAY_NAME = "audit-loop auto"
COMMENT_LOOP_DISPLAY_NAME = "comment-loop auto"
AUDIT_LOOP_SIM_DISPLAY_NAME = "audit-loop-sim auto"
DELAY_POLL_DISPLAY_NAME = "delay-poll"
CODE_REVIEW_DISPLAY_NAME = "code-review"
WAIT_DISPLAY_NAME = "wait"
ARCH_LOOP_DISPLAY_NAME = "arch-loop"

# Deterministic code owns elapsed time, interval cadence, and iteration counts for
# arch-loop. The external Codex evaluator owns qualitative requirement-satisfaction
# judgment. These two authorities are intentionally split; neither may claim the
# other's decisions as its own.
ARCH_LOOP_STATE_VERSION = 1
# Upper bound on a single hook-owned wait window. Matches the per-command `timeout`
# installed by `upsert_codex_stop_hook.py` and `upsert_claude_stop_hook.py` (90000s).
# Cadence or deadline requests that exceed this ceiling must fail loud at arm time
# instead of silently becoming manual reminders.
ARCH_LOOP_INSTALLED_HOOK_TIMEOUT_SECONDS = 90000


@dataclass(frozen=True)
class HookRuntimeSpec:
    name: str
    state_root: Path


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


HOOK_RUNTIME_SPECS = {
    RUNTIME_CODEX: HookRuntimeSpec(name=RUNTIME_CODEX, state_root=Path(".codex")),
    RUNTIME_CLAUDE: HookRuntimeSpec(
        name=RUNTIME_CLAUDE,
        state_root=Path(".claude/arch_skill"),
    ),
}
ACTIVE_RUNTIME: HookRuntimeSpec | None = None


IMPLEMENT_LOOP_STATE_SPEC = ControllerStateSpec(
    relative_path=IMPLEMENT_LOOP_STATE_FILE,
    expected_command=IMPLEMENT_LOOP_COMMAND,
    display_name=IMPLEMENT_LOOP_DISPLAY_NAME,
)
AUTO_PLAN_STATE_SPEC = ControllerStateSpec(
    relative_path=AUTO_PLAN_STATE_FILE,
    expected_command=AUTO_PLAN_COMMAND,
    display_name=AUTO_PLAN_DISPLAY_NAME,
)
MINIARCH_STEP_IMPLEMENT_LOOP_STATE_SPEC = ControllerStateSpec(
    relative_path=MINIARCH_STEP_IMPLEMENT_LOOP_STATE_FILE,
    expected_command=MINIARCH_STEP_IMPLEMENT_LOOP_COMMAND,
    display_name=MINIARCH_STEP_IMPLEMENT_LOOP_DISPLAY_NAME,
)
MINIARCH_STEP_AUTO_PLAN_STATE_SPEC = ControllerStateSpec(
    relative_path=MINIARCH_STEP_AUTO_PLAN_STATE_FILE,
    expected_command=MINIARCH_STEP_AUTO_PLAN_COMMAND,
    display_name=MINIARCH_STEP_AUTO_PLAN_DISPLAY_NAME,
)
ARCH_DOCS_AUTO_STATE_SPEC = ControllerStateSpec(
    relative_path=ARCH_DOCS_AUTO_STATE_FILE,
    expected_command=ARCH_DOCS_AUTO_COMMAND,
    display_name=ARCH_DOCS_AUTO_DISPLAY_NAME,
)
AUDIT_LOOP_STATE_SPEC = ControllerStateSpec(
    relative_path=AUDIT_LOOP_STATE_FILE,
    expected_command=AUDIT_LOOP_COMMAND,
    display_name=AUDIT_LOOP_DISPLAY_NAME,
)
COMMENT_LOOP_STATE_SPEC = ControllerStateSpec(
    relative_path=COMMENT_LOOP_STATE_FILE,
    expected_command=COMMENT_LOOP_COMMAND,
    display_name=COMMENT_LOOP_DISPLAY_NAME,
)
AUDIT_LOOP_SIM_STATE_SPEC = ControllerStateSpec(
    relative_path=AUDIT_LOOP_SIM_STATE_FILE,
    expected_command=AUDIT_LOOP_SIM_COMMAND,
    display_name=AUDIT_LOOP_SIM_DISPLAY_NAME,
)
DELAY_POLL_STATE_SPEC = ControllerStateSpec(
    relative_path=DELAY_POLL_STATE_FILE,
    expected_command=DELAY_POLL_COMMAND,
    display_name=DELAY_POLL_DISPLAY_NAME,
)
CODE_REVIEW_STATE_SPEC = ControllerStateSpec(
    relative_path=CODE_REVIEW_STATE_FILE,
    expected_command=CODE_REVIEW_COMMAND,
    display_name=CODE_REVIEW_DISPLAY_NAME,
)
WAIT_STATE_SPEC = ControllerStateSpec(
    relative_path=WAIT_STATE_FILE,
    expected_command=WAIT_COMMAND,
    display_name=WAIT_DISPLAY_NAME,
)
ARCH_LOOP_STATE_SPEC = ControllerStateSpec(
    relative_path=ARCH_LOOP_STATE_FILE,
    expected_command=ARCH_LOOP_COMMAND,
    display_name=ARCH_LOOP_DISPLAY_NAME,
)

AUTO_PLAN_STAGES = (
    "research",
    "deep-dive-pass-1",
    "deep-dive-pass-2",
    "phase-plan",
    "consistency-pass",
)
MINIARCH_STEP_AUTO_PLAN_STAGES = (
    "research",
    "deep-dive",
    "phase-plan",
)

MINIARCH_STEP_AUDIT_MODEL = "gpt-5.4-mini"
MINIARCH_STEP_AUDIT_MODEL_REASONING_EFFORT = "xhigh"

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
COMMENT_LOOP_CONTROLLER_START = "<!-- comment_loop:block:controller:start -->"
COMMENT_LOOP_CONTROLLER_END = "<!-- comment_loop:block:controller:end -->"
AUDIT_LOOP_SIM_CONTROLLER_START = "<!-- audit_loop_sim:block:controller:start -->"
AUDIT_LOOP_SIM_CONTROLLER_END = "<!-- audit_loop_sim:block:controller:end -->"
LOOP_VALID_VERDICTS = {"CONTINUE", "CLEAN", "BLOCKED"}
CONTROLLER_STATE_SPECS = (
    IMPLEMENT_LOOP_STATE_SPEC,
    AUTO_PLAN_STATE_SPEC,
    MINIARCH_STEP_IMPLEMENT_LOOP_STATE_SPEC,
    MINIARCH_STEP_AUTO_PLAN_STATE_SPEC,
    ARCH_DOCS_AUTO_STATE_SPEC,
    AUDIT_LOOP_STATE_SPEC,
    COMMENT_LOOP_STATE_SPEC,
    AUDIT_LOOP_SIM_STATE_SPEC,
    DELAY_POLL_STATE_SPEC,
    CODE_REVIEW_STATE_SPEC,
    WAIT_STATE_SPEC,
    ARCH_LOOP_STATE_SPEC,
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
ARCH_LOOP_EVAL_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "verdict",
        "summary",
        "satisfied_requirements",
        "unsatisfied_requirements",
        "required_skill_audits",
        "continue_mode",
        "next_task",
        "blocker",
    ],
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["clean", "continue", "blocked"],
        },
        "summary": {"type": "string"},
        "satisfied_requirements": {
            "type": "array",
            "items": {"type": "string"},
        },
        "unsatisfied_requirements": {
            "type": "array",
            "items": {"type": "string"},
        },
        "required_skill_audits": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["skill", "status", "evidence"],
                "properties": {
                    "skill": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": [
                            "pass",
                            "fail",
                            "missing",
                            "not_requested",
                            "inapplicable",
                        ],
                    },
                    "evidence": {"type": "string"},
                },
            },
        },
        "continue_mode": {
            "type": "string",
            "enum": ["parent_work", "wait_recheck", "none"],
        },
        "next_task": {"type": "string"},
        "blocker": {"type": "string"},
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--runtime",
        choices=SUPPORTED_RUNTIMES,
        required=True,
        help="Host runtime that invoked this Stop hook. Rerun make install to repair stale hook entries.",
    )
    return parser.parse_args()


def require_runtime() -> HookRuntimeSpec:
    if ACTIVE_RUNTIME is None:
        raise RuntimeError("active hook runtime is not configured")
    return ACTIVE_RUNTIME


def controller_state_relative_path(spec: ControllerStateSpec) -> Path:
    # The installer owns host runtime identity. The shared dispatcher only
    # resolves state within that runtime's namespace and never guesses.
    runtime = require_runtime()
    return runtime.state_root / spec.relative_path


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


def claim_legacy_state_for_session(
    state_path: Path,
    state: dict,
    payload_session_id: str,
) -> Path:
    claimed_path = state_path.with_name(
        f"{state_path.stem}.{payload_session_id}{state_path.suffix}"
    )
    state["session_id"] = payload_session_id
    write_state(claimed_path, state)
    if claimed_path != state_path:
        clear_state(state_path)
    return claimed_path


def current_epoch_seconds() -> int:
    return int(time.time())


def sleep_for_seconds(seconds: int) -> None:
    if seconds > 0:
        time.sleep(seconds)


_WAIT_DURATION_COMPONENT_RE = re.compile(r"([0-9]+)([smhd])")
_WAIT_DURATION_FULL_RE = re.compile(r"^(?:[0-9]+[smhd])+$")
_WAIT_UNIT_MULTIPLIERS = {"s": 1, "m": 60, "h": 3600, "d": 86400}


def parse_wait_duration(text: str) -> int:
    """Parse a `wait` skill duration string into integer seconds.

    Grammar: one or more `<N><unit>` components concatenated, where `N` is a
    positive integer and `unit` is `s`, `m`, `h`, or `d`. Components are
    summed. Order is not enforced. Whitespace is rejected; the caller is
    responsible for stripping outer whitespace.
    """
    if not isinstance(text, str):
        raise ValueError("wait duration must be a string")
    if not text:
        raise ValueError("wait duration is empty")
    if text != text.strip() or any(ch.isspace() for ch in text):
        raise ValueError(f"wait duration has whitespace: {text!r}")
    if not _WAIT_DURATION_FULL_RE.match(text):
        raise ValueError(
            f"wait duration does not match grammar <N>(s|m|h|d)[<N>(s|m|h|d)...]: {text!r}"
        )
    total = 0
    seen_units: set[str] = set()
    for value_text, unit in _WAIT_DURATION_COMPONENT_RE.findall(text):
        if unit in seen_units:
            raise ValueError(f"wait duration has duplicate unit {unit!r}: {text!r}")
        seen_units.add(unit)
        value = int(value_text)
        if value <= 0:
            raise ValueError(
                f"wait duration component must be positive: {value_text}{unit}"
            )
        total += value * _WAIT_UNIT_MULTIPLIERS[unit]
    if total <= 0:
        raise ValueError(f"wait duration sums to non-positive seconds: {text!r}")
    return total


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


def session_state_relative_path(state_relative_path: Path, session_id: str) -> Path:
    return state_relative_path.with_name(
        f"{state_relative_path.stem}.{session_id}{state_relative_path.suffix}"
    )


def session_state_path(cwd: Path, spec: ControllerStateSpec, session_id: str) -> Path:
    return cwd / session_state_relative_path(controller_state_relative_path(spec), session_id)


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


def legacy_state_is_active_for_session(
    cwd: Path,
    spec: ControllerStateSpec,
    payload: dict,
) -> bool:
    legacy_path = cwd / controller_state_relative_path(spec)
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
        session_state_path(cwd, spec, session_id)
        if session_id is not None
        else None
    )
    legacy_path = cwd / controller_state_relative_path(spec)
    if session_path is not None and session_path.exists():
        return ResolvedControllerState(spec=spec, state_path=session_path, is_legacy=False)
    if legacy_state_is_active_for_session(cwd, spec, payload):
        return ResolvedControllerState(spec=spec, state_path=legacy_path, is_legacy=True)
    return None


def resolve_controller_state_for_handler(
    payload: dict,
    spec: ControllerStateSpec,
) -> ResolvedControllerState | None:
    cwd = Path(payload["cwd"]).resolve()
    session_id = current_session_id(payload)
    session_path = (
        session_state_path(cwd, spec, session_id)
        if session_id is not None
        else None
    )
    legacy_path = cwd / controller_state_relative_path(spec)
    if session_path is not None and session_path.exists():
        return ResolvedControllerState(spec=spec, state_path=session_path, is_legacy=False)
    if legacy_path.exists():
        return ResolvedControllerState(spec=spec, state_path=legacy_path, is_legacy=True)
    return None


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
) -> Path | None:
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
            return claim_legacy_state_for_session(
                state_path,
                state,
                payload_session_id,
            )
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
            return None
        clear_state(state_path)
        block_with_message(
            f"{command_name} controller state at {display_path(state_path, cwd)} had a mismatched session_id; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    if allow_claim:
        return claim_legacy_state_for_session(
            state_path,
            state,
            payload_session_id,
        )
    return state_path


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


def format_skill_invocation(invocation: str) -> str:
    runtime = require_runtime()
    if runtime.name == RUNTIME_CLAUDE:
        return f"/{invocation}"
    return f"Use ${invocation}"


def normalize_claude_process_result(
    process: subprocess.CompletedProcess[str],
) -> tuple[subprocess.CompletedProcess[str], str | None, dict | None]:
    stdout_text = process.stdout.strip()
    if not stdout_text:
        return process, None, None

    try:
        parsed = json.loads(stdout_text)
    except json.JSONDecodeError:
        return process, stdout_text or None, None

    if not isinstance(parsed, dict):
        return process, stdout_text or None, None

    normalized_process = process
    if parsed.get("is_error") is True and process.returncode == 0:
        normalized_process = subprocess.CompletedProcess(
            process.args,
            1,
            process.stdout,
            process.stderr,
        )

    last_message = None
    result_text = parsed.get("result")
    if isinstance(result_text, str) and result_text.strip():
        last_message = result_text.strip()

    payload = parsed.get("structured_output")
    if not isinstance(payload, dict):
        payload = None

    if payload is not None and last_message is None:
        last_message = json.dumps(payload, separators=(",", ":"))

    return normalized_process, last_message, payload


def run_codex_text_child(
    cwd: Path,
    prompt: str,
    *,
    temp_prefix: str,
    model: str | None = None,
    model_reasoning_effort: str | None = None,
) -> FreshAuditResult:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    with tempfile.TemporaryDirectory(prefix=temp_prefix) as temp_dir:
        last_message_path = Path(temp_dir) / "last_message.txt"
        command = [
            codex,
            "exec",
            "--ephemeral",
            "--disable",
            "codex_hooks",
            "--cd",
            str(cwd),
            "--dangerously-bypass-approvals-and-sandbox",
        ]
        if model:
            command.extend(["--model", model])
        if model_reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{model_reasoning_effort}"'])
        command.extend(["-o", str(last_message_path), prompt])

        process = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        last_message = None
        if last_message_path.exists():
            last_message = last_message_path.read_text(encoding="utf-8").strip() or None
        return FreshAuditResult(process=process, last_message=last_message)


def run_codex_structured_child(
    cwd: Path,
    prompt: str,
    *,
    schema: dict,
    temp_prefix: str,
) -> FreshStructuredResult:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    with tempfile.TemporaryDirectory(prefix=temp_prefix) as temp_dir:
        temp_root = Path(temp_dir)
        schema_path = temp_root / "schema.json"
        last_message_path = temp_root / "last_message.json"
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
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


def run_claude_text_child(
    cwd: Path,
    prompt: str,
    *,
    model_reasoning_effort: str | None = None,
) -> FreshAuditResult:
    claude = shutil.which("claude")
    if not claude:
        raise RuntimeError("`claude` is not available on PATH for the Stop hook")

    command = [
        claude,
        "-p",
        "--output-format",
        "json",
        "--dangerously-skip-permissions",
        "--settings",
        CLAUDE_CHILD_SETTINGS_JSON,
    ]
    if model_reasoning_effort:
        command.extend(["--effort", model_reasoning_effort])
    command.append(prompt)

    process = subprocess.run(
        command,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    normalized_process, last_message, _ = normalize_claude_process_result(process)
    return FreshAuditResult(process=normalized_process, last_message=last_message)


def run_claude_structured_child(
    cwd: Path,
    prompt: str,
    *,
    schema: dict,
) -> FreshStructuredResult:
    claude = shutil.which("claude")
    if not claude:
        raise RuntimeError("`claude` is not available on PATH for the Stop hook")

    command = [
        claude,
        "-p",
        "--output-format",
        "json",
        "--dangerously-skip-permissions",
        "--settings",
        CLAUDE_CHILD_SETTINGS_JSON,
        "--json-schema",
        json.dumps(schema),
    ]
    command.append(prompt)

    process = subprocess.run(
        command,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    normalized_process, last_message, payload = normalize_claude_process_result(process)
    return FreshStructuredResult(
        process=normalized_process,
        last_message=last_message,
        payload=payload,
    )


def run_fresh_audit(
    cwd: Path,
    doc_path_value: str,
    *,
    skill_name: str = "arch-step",
    temp_prefix: str = "arch-step-implement-loop-",
    model: str | None = None,
    model_reasoning_effort: str | None = None,
) -> FreshAuditResult:
    prompt = (
        f"{format_skill_invocation(f'{skill_name} audit-implementation {doc_path_value}')}\n"
        "Fresh context only. Audit against the full approved ordered plan frontier in DOC_PATH, not against "
        "any narrower execution-side rewrite. Update the authoritative implementation audit block and any "
        "reopened phase statuses in DOC_PATH. If implementation weakened requirements, scope, acceptance "
        "criteria, or phase obligations to hide unfinished work, fail it. Group remaining missing work as "
        "the real remaining frontier instead of one tiny gap. Keep the final response short."
    )
    runtime = require_runtime()
    if runtime.name == RUNTIME_CLAUDE:
        return run_claude_text_child(
            cwd,
            prompt,
            model_reasoning_effort=model_reasoning_effort,
        )
    return run_codex_text_child(
        cwd,
        prompt,
        temp_prefix=temp_prefix,
        model=model,
        model_reasoning_effort=model_reasoning_effort,
    )


def run_arch_docs_evaluator(
    cwd: Path,
    scope_summary: str,
    state_path: Path,
    ledger_path_value: str,
) -> FreshStructuredResult:
    prompt = (
        f"{format_skill_invocation('arch-docs')} for the suite's INTERNAL AUTO EVALUATOR.\n"
        f"SCOPE_SUMMARY: {scope_summary}\n"
        f"STATE_PATH: {display_path(state_path, cwd)}\n"
        f"LEDGER_PATH: {ledger_path_value}\n"
        "Fresh context only. Stay read-only. Read the controller state, the resolved repo docs scope, and the "
        "temporary ledger if it still exists. Return structured JSON only."
    )
    runtime = require_runtime()
    if runtime.name == RUNTIME_CLAUDE:
        return run_claude_structured_child(
            cwd,
            prompt,
            schema=ARCH_DOCS_EVAL_SCHEMA,
        )
    return run_codex_structured_child(
        cwd,
        prompt,
        schema=ARCH_DOCS_EVAL_SCHEMA,
        temp_prefix="arch-docs-auto-eval-",
    )


def run_arch_loop_evaluator(
    cwd: Path,
    state: dict,
    repo_root: Path,
    prompt_text: str,
) -> FreshStructuredResult:
    # arch-loop is intentionally Codex-only even when the visible parent runtime
    # is Claude. The skill's evaluator-prompt contract names Codex xhigh as the
    # fresh external auditor; the Stop hook must not silently downgrade that
    # decision to the host runtime. Launch with `-p yolo`, `--ephemeral`,
    # `--disable codex_hooks`, and `--dangerously-bypass-approvals-and-sandbox`
    # exactly as the references document.
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    compact_state = {
        key: state.get(key)
        for key in (
            "version",
            "runtime",
            "command",
            "session_id",
            "created_at",
            "iteration_count",
            "check_count",
            "deadline_at",
            "interval_seconds",
            "max_iterations",
            "next_due_at",
            "cap_evidence",
            "required_skill_audits",
            "last_continue_mode",
            "last_next_task",
            "last_evaluator_verdict",
            "last_evaluator_summary",
        )
        if state.get(key) is not None
    }
    last_work_summary = state.get("last_work_summary") or ""
    last_verification_summary = state.get("last_verification_summary") or ""

    prompt_sections = [
        prompt_text.strip(),
        "---",
        "## Structured inputs",
        "REPO_ROOT: " + str(repo_root),
        "RAW_REQUIREMENTS:",
        state.get("raw_requirements", "").strip(),
        "CONTROLLER_STATE (compact JSON):",
        json.dumps(compact_state, indent=2, sort_keys=True),
        "LAST_WORK_SUMMARY:",
        last_work_summary,
        "LAST_VERIFICATION_SUMMARY:",
        last_verification_summary,
    ]
    prompt = "\n".join(prompt_sections)

    with tempfile.TemporaryDirectory(prefix="arch-loop-eval-") as temp_dir:
        temp_root = Path(temp_dir)
        schema_path = temp_root / "schema.json"
        last_message_path = temp_root / "last_message.json"
        schema_path.write_text(json.dumps(ARCH_LOOP_EVAL_SCHEMA), encoding="utf-8")
        process = subprocess.run(
            [
                codex,
                "exec",
                "-p",
                "yolo",
                "--ephemeral",
                "--disable",
                "codex_hooks",
                "--dangerously-bypass-approvals-and-sandbox",
                "-C",
                str(repo_root),
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
        return FreshStructuredResult(
            process=process,
            last_message=last_message,
            payload=payload,
        )


def run_fresh_review(cwd: Path) -> FreshAuditResult:
    prompt = (
        f"{format_skill_invocation('audit-loop review')}\n"
        "Fresh context only. Repair or update `_audit_ledger.md`, set the controller verdict truthfully, "
        "and keep the final response short."
    )
    runtime = require_runtime()
    if runtime.name == RUNTIME_CLAUDE:
        return run_claude_text_child(cwd, prompt)
    return run_codex_text_child(cwd, prompt, temp_prefix="audit-loop-review-")


def run_fresh_comment_review(cwd: Path) -> FreshAuditResult:
    prompt = (
        f"{format_skill_invocation('comment-loop review')}\n"
        "Fresh context only. Repair or update `_comment_ledger.md`, set the controller verdict truthfully, "
        "and keep the final response short."
    )
    runtime = require_runtime()
    if runtime.name == RUNTIME_CLAUDE:
        return run_claude_text_child(cwd, prompt)
    return run_codex_text_child(cwd, prompt, temp_prefix="comment-loop-review-")


def run_fresh_sim_review(cwd: Path) -> FreshAuditResult:
    prompt = (
        f"{format_skill_invocation('audit-loop-sim review')}\n"
        "Fresh context only. Repair or update `_audit_sim_ledger.md`, set the controller verdict truthfully, "
        "and keep the final response short."
    )
    runtime = require_runtime()
    if runtime.name == RUNTIME_CLAUDE:
        return run_claude_text_child(cwd, prompt)
    return run_codex_text_child(cwd, prompt, temp_prefix="audit-loop-sim-review-")


CODE_REVIEW_RUNNER_RELATIVE_PATH = (
    Path("skills") / "code-review" / "scripts" / "run_code_review.py"
)
CODE_REVIEW_TARGET_MODES = (
    "uncommitted-diff",
    "branch-diff",
    "commit-range",
    "paths",
    "completion-claim",
)


def resolve_code_review_runner_path() -> Path | None:
    # Claude-hosted Stop hooks intentionally reuse this dispatcher, but the
    # review subprocess itself must remain Codex (see SKILL.md references).
    # The dispatcher only locates the runner; it never reimplements review.
    candidates = [
        Path(__file__).resolve().parents[2] / "code-review" / "scripts" / "run_code_review.py",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def resolve_arch_loop_evaluator_prompt_path() -> Path | None:
    # Mirrors resolve_code_review_runner_path: the arch-loop skill ships its
    # evaluator prompt at skills/arch-loop/references/evaluator-prompt.md. The
    # Stop hook loads it verbatim and feeds it to the fresh Codex child.
    candidates = [
        Path(__file__).resolve().parents[2]
        / "arch-loop"
        / "references"
        / "evaluator-prompt.md",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def build_code_review_runner_args(
    runner_path: Path,
    state: dict,
    repo_root: Path,
) -> list[str]:
    target = state["target"]
    args: list[str] = [
        sys.executable,
        str(runner_path),
        "--repo-root",
        str(repo_root),
        "--target",
        target["mode"],
    ]
    if target["mode"] in ("branch-diff", "commit-range"):
        args += ["--base", target["base"], "--head", target["head"]]
    elif target["mode"] == "paths":
        args += ["--paths", *target["paths"]]
    elif target["mode"] == "completion-claim":
        args += [
            "--claim-doc",
            target["claim_doc"],
            "--claim-phase",
            str(target["claim_phase"]),
        ]
    objective = state.get("objective")
    if isinstance(objective, str) and objective.strip():
        args += ["--objective", objective.strip()]
    output_root = state.get("output_root")
    if isinstance(output_root, str) and output_root.strip():
        args += ["--output-root", output_root.strip()]
    host_runtime = state.get("host_runtime")
    if isinstance(host_runtime, str) and host_runtime.strip():
        args += ["--host-runtime", host_runtime.strip()]
    return args


def extract_code_review_verdict(run_dir: Path) -> tuple[str | None, Path | None]:
    synthesis = run_dir / "synthesis.final.txt"
    if not synthesis.is_file():
        return None, None
    try:
        text = synthesis.read_text(encoding="utf-8")
    except OSError:
        return None, synthesis
    match = re.search(r"^VERDICT:\s*(\S+)\s*$", text, re.MULTILINE)
    verdict = match.group(1).strip() if match else None
    return verdict, synthesis


def locate_code_review_run_dir(
    stdout: str,
    stderr: str,
    output_root: Path | None,
) -> Path | None:
    match = re.search(r"wrote synthesis verdict to (\S+)", stdout + "\n" + stderr)
    if match:
        synthesis_path = Path(match.group(1))
        if synthesis_path.is_file():
            return synthesis_path.parent
    if output_root and output_root.is_dir():
        candidates = sorted(
            (p for p in output_root.iterdir() if p.is_dir()),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if candidates:
            return candidates[0]
    return None


def run_delay_poll_check(cwd: Path, check_prompt: str) -> FreshStructuredResult:
    prompt = (
        f"{format_skill_invocation('delay-poll check')}\n"
        "Fresh context only. Stay read-only. Evaluate whether the waited-on condition is satisfied yet.\n"
        "<check_prompt>\n"
        f"{check_prompt.strip()}\n"
        "</check_prompt>\n"
        "Return structured JSON only."
    )
    runtime = require_runtime()
    if runtime.name == RUNTIME_CLAUDE:
        return run_claude_structured_child(
            cwd,
            prompt,
            schema=DELAY_POLL_CHECK_SCHEMA,
        )
    return run_codex_structured_child(
        cwd,
        prompt,
        schema=DELAY_POLL_CHECK_SCHEMA,
        temp_prefix="delay-poll-check-",
    )


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
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        IMPLEMENT_LOOP_COMMAND,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path
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
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        AUTO_PLAN_COMMAND,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

    doc_path_value = state.get("doc_path")
    if not isinstance(doc_path_value, str) or not doc_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "auto-plan controller state was missing doc_path; "
            "the controller was disarmed. Update the plan truthfully and stop."
        )

    doc_path = resolve_path(cwd, doc_path_value)
    return doc_path, doc_path_value, state, state_path


def validate_miniarch_step_implement_loop_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[Path, str, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        MINIARCH_STEP_IMPLEMENT_LOOP_COMMAND,
        MINIARCH_STEP_IMPLEMENT_LOOP_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        MINIARCH_STEP_IMPLEMENT_LOOP_COMMAND,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path
    doc_path_value = state.get("doc_path")
    if not isinstance(doc_path_value, str) or not doc_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "miniarch-step implement-loop controller state was missing doc_path; "
            "the loop was disarmed. Update the plan and worklog truthfully, then stop."
        )
    doc_path = resolve_path(cwd, doc_path_value)
    return doc_path, doc_path_value, state_path


def validate_miniarch_step_auto_plan_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[Path, str, dict, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        MINIARCH_STEP_AUTO_PLAN_COMMAND,
        MINIARCH_STEP_AUTO_PLAN_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        MINIARCH_STEP_AUTO_PLAN_COMMAND,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

    doc_path_value = state.get("doc_path")
    if not isinstance(doc_path_value, str) or not doc_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "miniarch-step auto-plan controller state was missing doc_path; "
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
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        ARCH_DOCS_AUTO_COMMAND,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

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
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        AUDIT_LOOP_DISPLAY_NAME,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

    ledger_path_value = state.get("ledger_path", str(AUDIT_LOOP_DEFAULT_LEDGER_RELATIVE_PATH))
    if not isinstance(ledger_path_value, str) or not ledger_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "audit-loop auto controller state was missing ledger_path; "
            "the controller was disarmed. Update the ledger truthfully and stop."
        )

    ledger_path = resolve_path(cwd, ledger_path_value)
    return ledger_path, ledger_path_value, state, state_path


def validate_comment_loop_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[Path, str, dict, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        COMMENT_LOOP_DISPLAY_NAME,
        COMMENT_LOOP_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        COMMENT_LOOP_DISPLAY_NAME,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

    ledger_path_value = state.get("ledger_path", str(COMMENT_LOOP_DEFAULT_LEDGER_RELATIVE_PATH))
    if not isinstance(ledger_path_value, str) or not ledger_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "comment-loop auto controller state was missing ledger_path; "
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
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        AUDIT_LOOP_SIM_DISPLAY_NAME,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

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
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        DELAY_POLL_DISPLAY_NAME,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

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


def validate_code_review_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[dict, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        CODE_REVIEW_DISPLAY_NAME,
        CODE_REVIEW_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        CODE_REVIEW_DISPLAY_NAME,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

    version = state.get("version")
    if version != 1:
        clear_state(state_path)
        block_with_message(
            "code-review controller state had an unsupported version; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )

    repo_root = state.get("repo_root")
    if not isinstance(repo_root, str) or not repo_root.strip():
        clear_state(state_path)
        block_with_message(
            "code-review controller state was missing repo_root; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    repo_root_path = Path(repo_root).expanduser().resolve()
    if not repo_root_path.is_dir():
        clear_state(state_path)
        block_with_message(
            f"code-review controller state pointed at a missing repo_root ({repo_root}); "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    state["repo_root"] = str(repo_root_path)

    target = state.get("target")
    if not isinstance(target, dict):
        clear_state(state_path)
        block_with_message(
            "code-review controller state was missing a target object; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    mode = target.get("mode")
    if mode not in CODE_REVIEW_TARGET_MODES:
        clear_state(state_path)
        block_with_message(
            f"code-review controller state had an unsupported target.mode ({mode}); "
            "the controller was disarmed. Update the repo truthfully and stop."
        )
    if mode in ("branch-diff", "commit-range"):
        base = target.get("base")
        head = target.get("head")
        if not isinstance(base, str) or not base.strip() or not isinstance(head, str) or not head.strip():
            clear_state(state_path)
            block_with_message(
                f"code-review controller state target mode {mode} required non-empty base and head refs; "
                "the controller was disarmed. Update the repo truthfully and stop."
            )
        target["base"] = base.strip()
        target["head"] = head.strip()
    elif mode == "paths":
        paths = target.get("paths")
        if not isinstance(paths, list) or not paths:
            clear_state(state_path)
            block_with_message(
                "code-review controller state target mode paths required a non-empty paths list; "
                "the controller was disarmed. Update the repo truthfully and stop."
            )
        cleaned_paths: list[str] = []
        for item in paths:
            if not isinstance(item, str) or not item.strip():
                clear_state(state_path)
                block_with_message(
                    "code-review controller state had a non-string or empty path; "
                    "the controller was disarmed. Update the repo truthfully and stop."
                )
            cleaned_paths.append(item.strip())
        target["paths"] = cleaned_paths
    elif mode == "completion-claim":
        claim_doc = target.get("claim_doc")
        claim_phase = target.get("claim_phase")
        if not isinstance(claim_doc, str) or not claim_doc.strip():
            clear_state(state_path)
            block_with_message(
                "code-review controller state target mode completion-claim required claim_doc; "
                "the controller was disarmed. Update the repo truthfully and stop."
            )
        if not isinstance(claim_phase, int) or claim_phase <= 0:
            clear_state(state_path)
            block_with_message(
                "code-review controller state target mode completion-claim required a positive integer claim_phase; "
                "the controller was disarmed. Update the repo truthfully and stop."
            )
        target["claim_doc"] = claim_doc.strip()

    objective = state.get("objective")
    if objective is not None and not isinstance(objective, str):
        clear_state(state_path)
        block_with_message(
            "code-review controller state had a non-string objective; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )

    output_root = state.get("output_root")
    if output_root is not None and (not isinstance(output_root, str) or not output_root.strip()):
        clear_state(state_path)
        block_with_message(
            "code-review controller state had an invalid output_root; "
            "the controller was disarmed. Update the repo truthfully and stop."
        )

    host_runtime = state.get("host_runtime")
    if host_runtime is not None and host_runtime not in SUPPORTED_RUNTIMES:
        clear_state(state_path)
        block_with_message(
            f"code-review controller state had an unsupported host_runtime ({host_runtime}); "
            "the controller was disarmed. Update the repo truthfully and stop."
        )

    return state, state_path


_WAIT_FORBIDDEN_DELAY_POLL_FIELDS = (
    "interval_seconds",
    "check_prompt",
    "attempt_count",
    "last_check_at",
    "last_summary",
)


def validate_wait_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[dict, Path] | None:
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        WAIT_DISPLAY_NAME,
        WAIT_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        WAIT_DISPLAY_NAME,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

    version = state.get("version")
    if version != 1:
        clear_state(state_path)
        block_with_message(
            "wait controller state had an unsupported version; "
            "the controller was disarmed. Re-run the wait skill with a valid duration and prompt."
        )

    armed_at = state.get("armed_at")
    if not isinstance(armed_at, int) or armed_at <= 0:
        clear_state(state_path)
        block_with_message(
            "wait controller state was missing a positive armed_at timestamp; "
            "the controller was disarmed. Re-run the wait skill with a valid duration and prompt."
        )

    deadline_at = state.get("deadline_at")
    if not isinstance(deadline_at, int) or deadline_at <= armed_at:
        clear_state(state_path)
        block_with_message(
            "wait controller state was missing a valid deadline_at timestamp (must be > armed_at); "
            "the controller was disarmed. Re-run the wait skill with a valid duration and prompt."
        )

    resume_prompt = state.get("resume_prompt")
    if not isinstance(resume_prompt, str) or not resume_prompt.strip():
        clear_state(state_path)
        block_with_message(
            "wait controller state was missing resume_prompt; "
            "the controller was disarmed. Re-run the wait skill with a valid duration and prompt."
        )
    state["resume_prompt"] = resume_prompt.strip()

    for forbidden in _WAIT_FORBIDDEN_DELAY_POLL_FIELDS:
        if forbidden in state:
            clear_state(state_path)
            block_with_message(
                f"wait controller state carried the delay-poll-only field {forbidden!r}; "
                "wait is a pure one-shot delay and does not share that schema. "
                "The controller was disarmed. Re-arm the wait skill with the documented wait schema only."
            )

    return state, state_path


# --- arch-loop cap/cadence extraction and state validation ---
#
# Deterministic code owns elapsed time, interval cadence, and iteration counts.
# The external Codex evaluator owns qualitative requirement-satisfaction judgment.
# These parsers intentionally match only unambiguous phrase families from
# `skills/arch-loop/references/cap-extraction.md`. Anything likely-but-ambiguous
# produces an `ArchLoopCapError` so the skill can stop loudly before arming.

_ARCH_LOOP_DURATION_UNITS_SECONDS = {
    "s": 1, "sec": 1, "second": 1, "seconds": 1,
    "m": 60, "min": 60, "mins": 60, "minute": 60, "minutes": 60,
    "h": 3600, "hr": 3600, "hrs": 3600, "hour": 3600, "hours": 3600,
    "d": 86400, "day": 86400, "days": 86400,
}

_ARCH_LOOP_WORD_COUNTS = {
    "once": 1,
    "twice": 2,
    "thrice": 3,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

_ARCH_LOOP_NUMBER_PATTERN = r"(\d+(?:\.\d+)?)"
_ARCH_LOOP_UNIT_PATTERN = (
    r"(s|sec|second|seconds|m|min|mins|minute|minutes|"
    r"h|hr|hrs|hour|hours|d|day|days)\b"
)
_ARCH_LOOP_DURATION_PHRASE = rf"{_ARCH_LOOP_NUMBER_PATTERN}\s*{_ARCH_LOOP_UNIT_PATTERN}"

_ARCH_LOOP_DURATION_REGEXES = [
    re.compile(
        rf"\b(?:max(?:imum)?\s+runtime|time\s+limit|stop\s+after|"
        rf"stop\s+if(?:\s+you(?:'re|\s+are)?)?\s+not\s+done\s+in|"
        rf"for\s+the\s+next|for)\s+{_ARCH_LOOP_DURATION_PHRASE}",
        re.IGNORECASE,
    ),
]

_ARCH_LOOP_CADENCE_REGEXES = [
    re.compile(
        rf"\b(?:every|check\s+every)\s+{_ARCH_LOOP_DURATION_PHRASE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\b(?:every|check\s+every)\s+(?:(an?|1)\s+)?{_ARCH_LOOP_UNIT_PATTERN}",
        re.IGNORECASE,
    ),
]

_ARCH_LOOP_ITERATION_REGEX = re.compile(
    r"\b(?:max(?:imum)?|up\s+to|no\s+more\s+than|only\s+try(?:\s+this)?|try(?:\s+this)?)\s+"
    r"(\d+|once|twice|thrice|one|two|three|four|five|six|seven|eight|nine|ten)"
    r"(?:\s+(?:iterations?|passes|attempts?|loops?|times?))?",
    re.IGNORECASE,
)
_ARCH_LOOP_ITERATION_STOP_AFTER_REGEX = re.compile(
    r"\bstop\s+after\s+"
    r"(\d+|once|twice|thrice|one|two|three|four|five|six|seven|eight|nine|ten)"
    r"\s+(?:iterations?|passes|attempts?|loops?|times?)\b",
    re.IGNORECASE,
)

_ARCH_LOOP_AMBIGUOUS_RUNTIME_PATTERNS = [
    re.compile(r"\b(?:max(?:imum)?\s+runtime|time\s+limit|stop\s+after|for\s+the\s+next|for)\s+"
               r"(?:a\s+while|a\s+few|some)\b", re.IGNORECASE),
]

_ARCH_LOOP_AMBIGUOUS_CADENCE_PATTERNS = [
    re.compile(r"\bevery\s+(?:so\s+often|now\s+and\s+then)\b", re.IGNORECASE),
    re.compile(r"\bperiodically\b", re.IGNORECASE),
    re.compile(r"\bevery\s+few\b", re.IGNORECASE),
]

_ARCH_LOOP_AMBIGUOUS_ITERATION_PATTERNS = [
    re.compile(r"\b(?:a\s+few|several)\s+(?:iterations?|passes|attempts?|loops?|times)\b",
               re.IGNORECASE),
]

_ARCH_LOOP_NAMED_AUDIT_REGEX = re.compile(r"\$([a-z][a-z0-9-]*)", re.IGNORECASE)


class ArchLoopCapError(ValueError):
    """Raised when arch-loop cap/cadence text is ambiguous or cannot be enforced."""


def _arch_loop_duration_seconds(number: str, unit: str) -> int:
    unit_seconds = _ARCH_LOOP_DURATION_UNITS_SECONDS[unit.lower()]
    total = float(number) * unit_seconds
    return int(total)


def _arch_loop_parse_iteration_count(token: str) -> int:
    token = token.lower()
    if token.isdigit():
        return int(token)
    if token in _ARCH_LOOP_WORD_COUNTS:
        return _ARCH_LOOP_WORD_COUNTS[token]
    raise ArchLoopCapError(f"iteration count is ambiguous ({token!r})")


def extract_arch_loop_constraints(
    raw_requirements: str,
    created_at: int,
    *,
    installed_hook_timeout_seconds: int = ARCH_LOOP_INSTALLED_HOOK_TIMEOUT_SECONDS,
) -> dict:
    """Extract unambiguous runtime/cadence/iteration caps from the user's prose.

    Returns a dict with the deterministic fields to write into arch-loop state:

        {
          "deadline_at": int | None,
          "interval_seconds": int | None,
          "max_iterations": int | None,
          "cap_evidence": [{"type": ..., "source_text": ..., "normalized": ...}],
          "required_skill_audits": [{"skill": ..., "status": "pending", ...}],
        }

    Raises `ArchLoopCapError` when text is likely-but-ambiguous, when multiple
    cadence phrases disagree, or when a requested cadence/window cannot fit
    inside the installed Stop-hook timeout. Unrecognized prose is silently
    ignored (it stays as free-form `raw_requirements`); only likely-cap text
    that we cannot safely disambiguate raises.
    """
    if not isinstance(raw_requirements, str) or not raw_requirements.strip():
        raise ArchLoopCapError("raw_requirements is empty; cannot extract caps")
    if not isinstance(created_at, int) or created_at <= 0:
        raise ArchLoopCapError("created_at must be a positive epoch-seconds integer")

    text = raw_requirements

    # Ambiguous likely-caps fail loud before we try to parse.
    for pattern in _ARCH_LOOP_AMBIGUOUS_RUNTIME_PATTERNS:
        match = pattern.search(text)
        if match:
            raise ArchLoopCapError(
                f"runtime cap is ambiguous ({match.group(0)!r}); "
                "restate the cap with a clear duration and unit."
            )
    for pattern in _ARCH_LOOP_AMBIGUOUS_CADENCE_PATTERNS:
        match = pattern.search(text)
        if match:
            raise ArchLoopCapError(
                f"cadence is ambiguous ({match.group(0)!r}); "
                "restate the cadence with a clear interval and unit."
            )
    for pattern in _ARCH_LOOP_AMBIGUOUS_ITERATION_PATTERNS:
        match = pattern.search(text)
        if match:
            raise ArchLoopCapError(
                f"iteration cap is ambiguous ({match.group(0)!r}); "
                "restate with a clear count."
            )

    cap_evidence: list[dict] = []

    # --- runtime/window duration caps ---
    runtime_candidates: list[tuple[int, str]] = []
    for regex in _ARCH_LOOP_DURATION_REGEXES:
        for match in regex.finditer(text):
            number, unit = match.group(1), match.group(2)
            try:
                seconds = _arch_loop_duration_seconds(number, unit)
            except (KeyError, ValueError) as exc:
                raise ArchLoopCapError(
                    f"could not parse duration {match.group(0)!r}: {exc}"
                )
            if seconds <= 0:
                raise ArchLoopCapError(
                    f"duration {match.group(0)!r} must be positive"
                )
            runtime_candidates.append((seconds, match.group(0)))

    deadline_at = None
    if runtime_candidates:
        # Strictest runtime cap wins: smallest duration (earliest deadline).
        strictest_seconds = min(s for s, _ in runtime_candidates)
        for seconds, source in runtime_candidates:
            normalized_deadline = created_at + seconds
            cap_evidence.append({
                "type": "runtime",
                "source_text": source,
                "normalized": f"deadline_at={normalized_deadline}",
            })
        deadline_at = created_at + strictest_seconds
        total_window = deadline_at - created_at
        if total_window > installed_hook_timeout_seconds:
            # A runtime window that exceeds the installed hook timeout is only
            # safe if the user also armed a cadence that lets the hook wake,
            # recheck, and reschedule within the timeout. That check is deferred
            # until the cadence value is known; we continue here and apply the
            # combined fit check below.
            pass

    # --- cadence ---
    cadence_candidates: list[tuple[int, str]] = []
    for regex in _ARCH_LOOP_CADENCE_REGEXES:
        for match in regex.finditer(text):
            # Match shapes: number+unit, indefinite-article+unit, or bare unit.
            groups = match.groups()
            if groups[0] and groups[1] and groups[0][0].isdigit():
                number, unit = groups[0], groups[1]
            elif groups[1]:
                number, unit = "1", groups[1]
            else:
                continue
            try:
                seconds = _arch_loop_duration_seconds(number, unit)
            except (KeyError, ValueError) as exc:
                raise ArchLoopCapError(
                    f"could not parse cadence {match.group(0)!r}: {exc}"
                )
            if seconds <= 0:
                raise ArchLoopCapError(
                    f"cadence {match.group(0)!r} must be positive"
                )
            cadence_candidates.append((seconds, match.group(0)))

    distinct_cadences = {seconds for seconds, _ in cadence_candidates}
    if len(distinct_cadences) > 1:
        phrases = ", ".join(source for _, source in cadence_candidates)
        raise ArchLoopCapError(
            f"cadence is ambiguous (multiple different cadence phrases: {phrases}); "
            "cadence is not a strictest-cap. Restate with one interval."
        )

    interval_seconds = None
    if cadence_candidates:
        interval_seconds = cadence_candidates[0][0]
        # Collapse duplicate identical phrases into one evidence entry per source.
        seen_sources: set[str] = set()
        for seconds, source in cadence_candidates:
            if source in seen_sources:
                continue
            seen_sources.add(source)
            cap_evidence.append({
                "type": "cadence",
                "source_text": source,
                "normalized": f"interval_seconds={seconds}",
            })

    # --- hook-timeout fit (cadence and runtime combined) ---
    if interval_seconds is not None and interval_seconds >= installed_hook_timeout_seconds:
        raise ArchLoopCapError(
            f"cadence interval_seconds={interval_seconds} exceeds the installed "
            f"Stop-hook timeout ({installed_hook_timeout_seconds}s); "
            "shorten the interval or use a different workflow."
        )
    if deadline_at is not None and interval_seconds is None:
        total_window = deadline_at - created_at
        if total_window > installed_hook_timeout_seconds:
            raise ArchLoopCapError(
                f"runtime window {total_window}s exceeds the installed Stop-hook "
                f"timeout ({installed_hook_timeout_seconds}s) and no cadence is armed; "
                "add a cadence or shorten the window."
            )
    if deadline_at is not None and interval_seconds is not None:
        if created_at + interval_seconds > deadline_at:
            raise ArchLoopCapError(
                f"cadence interval_seconds={interval_seconds} does not fit before "
                f"deadline_at={deadline_at}; shorten the interval or extend the window."
            )

    # --- iteration caps ---
    iteration_candidates: list[tuple[int, str]] = []
    for regex in (_ARCH_LOOP_ITERATION_REGEX, _ARCH_LOOP_ITERATION_STOP_AFTER_REGEX):
        for match in regex.finditer(text):
            token = match.group(1)
            try:
                count = _arch_loop_parse_iteration_count(token)
            except ArchLoopCapError:
                raise
            if count <= 0:
                raise ArchLoopCapError(
                    f"iteration cap {match.group(0)!r} must be positive"
                )
            iteration_candidates.append((count, match.group(0)))

    max_iterations = None
    if iteration_candidates:
        # Strictest iteration cap wins: smallest count.
        max_iterations = min(count for count, _ in iteration_candidates)
        for count, source in iteration_candidates:
            cap_evidence.append({
                "type": "iterations",
                "source_text": source,
                "normalized": f"max_iterations={count}",
            })

    # --- named skill audits ---
    required_skill_audits: list[dict] = []
    seen_audit_skills: set[str] = set()
    for match in _ARCH_LOOP_NAMED_AUDIT_REGEX.finditer(text):
        skill = match.group(1).lower()
        if skill in seen_audit_skills:
            continue
        seen_audit_skills.add(skill)
        required_skill_audits.append({
            "skill": skill,
            "target": "",
            "requirement": raw_requirements.strip(),
            "status": "pending",
            "latest_summary": "",
            "evidence_path": "",
        })

    return {
        "deadline_at": deadline_at,
        "interval_seconds": interval_seconds,
        "max_iterations": max_iterations,
        "cap_evidence": cap_evidence,
        "required_skill_audits": required_skill_audits,
    }


_ARCH_LOOP_AUDIT_STATUS_DISPLAY = ("pending", "pass", "fail", "missing", "inapplicable")
_ARCH_LOOP_VALID_AUDIT_STATUSES = set(_ARCH_LOOP_AUDIT_STATUS_DISPLAY)
_ARCH_LOOP_VALID_CONTINUE_MODES = {"", "parent_work", "wait_recheck", "none"}
_ARCH_LOOP_EVAL_AUDIT_STATUSES = {
    "pass",
    "fail",
    "missing",
    "not_requested",
    "inapplicable",
}
_ARCH_LOOP_EVAL_VERDICTS = {"clean", "continue", "blocked"}
_ARCH_LOOP_EVAL_CONTINUE_MODES = {"parent_work", "wait_recheck", "none"}
_ARCH_LOOP_CLEAN_AUDIT_STATUSES = {"pass", "inapplicable"}


def validate_arch_loop_state(
    payload: dict,
    resolved_state: ResolvedControllerState | None,
) -> tuple[dict, Path] | None:
    """Validate arch-loop state, clear+block on any invalid field."""
    cwd = Path(payload["cwd"]).resolve()
    loaded = load_controller_state(
        cwd,
        resolved_state,
        ARCH_LOOP_DISPLAY_NAME,
        ARCH_LOOP_COMMAND,
    )
    if loaded is None:
        return None
    state_path, state, is_legacy = loaded
    claimed_path = validate_session_id(
        payload,
        cwd,
        state_path,
        state,
        ARCH_LOOP_DISPLAY_NAME,
        allow_claim=is_legacy,
    )
    if claimed_path is None:
        return None
    state_path = claimed_path

    write_required = False

    version = state.get("version")
    if version != ARCH_LOOP_STATE_VERSION:
        clear_state(state_path)
        block_with_message(
            "arch-loop controller state had an unsupported version; "
            "the controller was disarmed. Re-arm arch-loop with version "
            f"{ARCH_LOOP_STATE_VERSION} state."
        )

    runtime = state.get("runtime")
    if runtime not in SUPPORTED_RUNTIMES:
        clear_state(state_path)
        block_with_message(
            f"arch-loop controller state had an unsupported runtime ({runtime!r}); "
            "the controller was disarmed. Re-arm arch-loop with runtime codex or claude."
        )

    raw_requirements = state.get("raw_requirements")
    if not isinstance(raw_requirements, str) or not raw_requirements.strip():
        clear_state(state_path)
        block_with_message(
            "arch-loop controller state was missing raw_requirements; "
            "the controller was disarmed. Re-arm arch-loop with the literal user request."
        )

    created_at = state.get("created_at")
    if not isinstance(created_at, int) or created_at <= 0:
        clear_state(state_path)
        block_with_message(
            "arch-loop controller state was missing a positive created_at timestamp; "
            "the controller was disarmed. Re-arm arch-loop truthfully."
        )

    iteration_count = state.get("iteration_count")
    if iteration_count is None:
        state["iteration_count"] = 0
        write_required = True
    elif not isinstance(iteration_count, int) or iteration_count < 0:
        clear_state(state_path)
        block_with_message(
            "arch-loop controller state had an invalid iteration_count; "
            "the controller was disarmed. Re-arm arch-loop truthfully."
        )

    check_count = state.get("check_count")
    if check_count is None:
        state["check_count"] = 0
        write_required = True
    elif not isinstance(check_count, int) or check_count < 0:
        clear_state(state_path)
        block_with_message(
            "arch-loop controller state had an invalid check_count; "
            "the controller was disarmed. Re-arm arch-loop truthfully."
        )

    deadline_at = state.get("deadline_at")
    if deadline_at is not None:
        if not isinstance(deadline_at, int) or deadline_at <= created_at:
            clear_state(state_path)
            block_with_message(
                "arch-loop controller state had an invalid deadline_at "
                "(must be a positive epoch-seconds integer later than created_at); "
                "the controller was disarmed. Re-arm arch-loop truthfully."
            )

    interval_seconds = state.get("interval_seconds")
    if interval_seconds is not None:
        if not isinstance(interval_seconds, int) or interval_seconds <= 0:
            clear_state(state_path)
            block_with_message(
                "arch-loop controller state had an invalid interval_seconds "
                "(must be a positive integer); the controller was disarmed. "
                "Re-arm arch-loop truthfully."
            )
        if interval_seconds >= ARCH_LOOP_INSTALLED_HOOK_TIMEOUT_SECONDS:
            clear_state(state_path)
            block_with_message(
                f"arch-loop cadence interval_seconds={interval_seconds} exceeds "
                f"the installed Stop-hook timeout ({ARCH_LOOP_INSTALLED_HOOK_TIMEOUT_SECONDS}s); "
                "the controller was disarmed. Shorten the cadence or use a different workflow."
            )

    max_iterations = state.get("max_iterations")
    if max_iterations is not None:
        if not isinstance(max_iterations, int) or max_iterations <= 0:
            clear_state(state_path)
            block_with_message(
                "arch-loop controller state had an invalid max_iterations "
                "(must be a positive integer); the controller was disarmed. "
                "Re-arm arch-loop truthfully."
            )

    next_due_at = state.get("next_due_at")
    if next_due_at is not None:
        if not isinstance(next_due_at, int) or next_due_at <= 0:
            clear_state(state_path)
            block_with_message(
                "arch-loop controller state had an invalid next_due_at; "
                "the controller was disarmed. Re-arm arch-loop truthfully."
            )
        if deadline_at is not None and next_due_at > deadline_at:
            clear_state(state_path)
            block_with_message(
                "arch-loop controller state had next_due_at later than deadline_at; "
                "the controller was disarmed. Re-arm arch-loop truthfully."
            )

    cap_evidence = state.get("cap_evidence")
    if cap_evidence is not None:
        if not isinstance(cap_evidence, list):
            clear_state(state_path)
            block_with_message(
                "arch-loop controller state had a non-list cap_evidence; "
                "the controller was disarmed. Re-arm arch-loop truthfully."
            )
        for entry in cap_evidence:
            if not isinstance(entry, dict):
                clear_state(state_path)
                block_with_message(
                    "arch-loop cap_evidence entries must be objects; "
                    "the controller was disarmed. Re-arm arch-loop truthfully."
                )
            if entry.get("type") not in {"runtime", "cadence", "iterations"}:
                clear_state(state_path)
                block_with_message(
                    "arch-loop cap_evidence entry had an unknown type; "
                    "the controller was disarmed. Re-arm arch-loop truthfully."
                )

    required_skill_audits = state.get("required_skill_audits")
    if required_skill_audits is not None:
        if not isinstance(required_skill_audits, list):
            clear_state(state_path)
            block_with_message(
                "arch-loop controller state had a non-list required_skill_audits; "
                "the controller was disarmed. Re-arm arch-loop truthfully."
            )
        for audit in required_skill_audits:
            if not isinstance(audit, dict):
                clear_state(state_path)
                block_with_message(
                    "arch-loop required_skill_audits entries must be objects; "
                    "the controller was disarmed. Re-arm arch-loop truthfully."
                )
            status = audit.get("status")
            if status not in _ARCH_LOOP_VALID_AUDIT_STATUSES:
                clear_state(state_path)
                block_with_message(
                    f"arch-loop required_skill_audits entry had an unknown status ({status!r}); "
                    f"expected one of: {', '.join(_ARCH_LOOP_AUDIT_STATUS_DISPLAY)}. "
                    "the controller was disarmed. Re-arm arch-loop truthfully."
                )
            skill_name = audit.get("skill")
            if not isinstance(skill_name, str) or not skill_name.strip():
                clear_state(state_path)
                block_with_message(
                    "arch-loop required_skill_audits entry was missing skill; "
                    "the controller was disarmed. Re-arm arch-loop truthfully."
                )

    last_continue_mode = state.get("last_continue_mode")
    if last_continue_mode is not None:
        if not isinstance(last_continue_mode, str) or last_continue_mode not in _ARCH_LOOP_VALID_CONTINUE_MODES:
            clear_state(state_path)
            block_with_message(
                f"arch-loop controller state had an invalid last_continue_mode "
                f"({last_continue_mode!r}); the controller was disarmed. "
                "Re-arm arch-loop truthfully."
            )

    if write_required:
        write_state(state_path, state)
    return state, state_path


def arch_loop_sleep_reason(next_due_at: int, deadline_at: int | None) -> int:
    """Return seconds to sleep until the next cadence due time.

    Mirrors `delay_poll_sleep_reason` but also supports an optional
    `deadline_at` of None (no runtime cap) so arch-loop can honor pure-cadence
    configurations.
    """
    now = current_epoch_seconds()
    wait_until = next_due_at
    if deadline_at is not None:
        wait_until = min(wait_until, deadline_at)
    return max(wait_until - now, 0)


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


def read_comment_loop_controller_fields(ledger_path: Path) -> dict[str, str] | None:
    if not ledger_path.exists():
        return None
    text = ledger_path.read_text(encoding="utf-8")
    start = text.find(COMMENT_LOOP_CONTROLLER_START)
    end = text.find(COMMENT_LOOP_CONTROLLER_END)
    if start == -1 or end == -1 or end < start:
        return None
    block = text[start + len(COMMENT_LOOP_CONTROLLER_START) : end]
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


def cleanup_comment_loop_runtime_artifacts(cwd: Path, ledger_path: Path, state: dict) -> None:
    if ledger_path.exists():
        ledger_path.unlink()

    gitignore_path = cwd / ".gitignore"
    clean_gitignore(
        gitignore_path=gitignore_path,
        entry=str(COMMENT_LOOP_DEFAULT_LEDGER_RELATIVE_PATH),
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


def next_incomplete_auto_plan_stage(doc_text: str) -> str | None:
    for stage in AUTO_PLAN_STAGES:
        if not auto_plan_stage_complete(doc_text, stage):
            return stage
    return None


def auto_plan_stage_blocked(doc_text: str, stage: str) -> bool:
    if stage != "consistency-pass":
        return False
    return consistency_pass_decision(doc_text) == "no"


def auto_plan_continue_reason(doc_path_value: str, next_stage: str, state_path_value: str) -> str:
    if next_stage == "deep-dive-pass-1":
        return (
            f"auto-plan is armed for {doc_path_value}. The first incomplete planning stage in the doc is deep-dive pass 1. "
            "Continue now with the next required command: "
            f"{format_skill_invocation(f'arch-step deep-dive {doc_path_value}')}. This is deep-dive pass 1 of 2. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    if next_stage == "deep-dive-pass-2":
        return (
            f"auto-plan is armed for {doc_path_value}. The first incomplete planning stage in the doc is deep-dive pass 2. "
            "Continue now with the next required command: "
            f"{format_skill_invocation(f'arch-step deep-dive {doc_path_value}')}. This is deep-dive pass 2 of 2. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    if next_stage == "phase-plan":
        return (
            f"auto-plan is armed for {doc_path_value}. The first incomplete planning stage in the doc is phase-plan. "
            "Continue now with the next required command: "
            f"{format_skill_invocation(f'arch-step phase-plan {doc_path_value}')}. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    if next_stage == "consistency-pass":
        return (
            f"auto-plan is armed for {doc_path_value}. The first incomplete planning stage in the doc is consistency-pass. "
            "Continue now with the next required command: "
            f"{format_skill_invocation(f'arch-step consistency-pass {doc_path_value}')}. This is the required end-to-end consistency cold read. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    raise RuntimeError(f"unexpected next auto-plan stage: {next_stage}")


def miniarch_step_auto_plan_stage_name(stage: str) -> str:
    return {
        "research": "research",
        "deep-dive": "deep-dive",
        "phase-plan": "phase-plan",
    }[stage]


def miniarch_step_auto_plan_stage_complete(doc_text: str, stage: str) -> bool:
    planning_passes = parse_planning_passes(doc_text)
    if stage == "research":
        return BLOCK_MARKERS["research_grounding"] in doc_text
    if stage == "deep-dive":
        return (
            BLOCK_MARKERS["current_architecture"] in doc_text
            and BLOCK_MARKERS["target_architecture"] in doc_text
            and BLOCK_MARKERS["call_site_audit"] in doc_text
            and pass_is_done(planning_passes.get("deep_dive_pass_1"))
        )
    if stage == "phase-plan":
        return BLOCK_MARKERS["phase_plan"] in doc_text
    raise RuntimeError(f"unexpected miniarch-step auto-plan stage: {stage}")


def next_incomplete_miniarch_step_auto_plan_stage(doc_text: str) -> str | None:
    for stage in MINIARCH_STEP_AUTO_PLAN_STAGES:
        if not miniarch_step_auto_plan_stage_complete(doc_text, stage):
            return stage
    return None


def miniarch_step_auto_plan_continue_reason(
    doc_path_value: str,
    next_stage: str,
    state_path_value: str,
) -> str:
    if next_stage == "deep-dive":
        return (
            f"miniarch-step auto-plan is armed for {doc_path_value}. The first incomplete planning stage in the doc is deep-dive. "
            "Continue now with the next required command: "
            f"{format_skill_invocation(f'miniarch-step deep-dive {doc_path_value}')}. This is the one required deep-dive pass. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    if next_stage == "phase-plan":
        return (
            f"miniarch-step auto-plan is armed for {doc_path_value}. The first incomplete planning stage in the doc is phase-plan. "
            "Continue now with the next required command: "
            f"{format_skill_invocation(f'miniarch-step phase-plan {doc_path_value}')}. "
            f"Keep {state_path_value} armed and stop naturally when this command finishes."
        )
    raise RuntimeError(f"unexpected next miniarch-step auto-plan stage: {next_stage}")


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
            f"The next required move is `{format_skill_invocation('arch-docs')}`. Current DOC_PATH: {doc_path_value}."
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
            "resume from the earliest reopened or incomplete phase, continue linearly through the remaining "
            "approved phases, run the required credible proof for the claimed work as you go, "
            f"update {display_path(worklog_path, cwd)} if it exists, keep the loop armed, "
            "and do not rewrite plan requirements, scope, acceptance criteria, or phase obligations while coding. "
            "If the audit shows the plan itself needs to change, stop and repair the plan instead of continuing on a rewritten story, "
            "and only then stop again for another fresh audit after the current reachable frontier is done or genuinely blocked."
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

    doc_text = read_doc_text(doc_path)
    next_stage = next_incomplete_auto_plan_stage(doc_text)
    if next_stage is None:
        clear_state(state_path)
        stop_with_json(
            f"auto-plan completed for {doc_path_value}. Research, deep-dive pass 1, deep-dive pass 2, phase-plan, and consistency-pass are in place. "
            f"The doc is ready for `{format_skill_invocation(f'arch-step implement-loop {doc_path_value}')}`.",
            system_message="auto-plan completed; the doc is ready for implement-loop.",
        )

    if auto_plan_stage_blocked(doc_text, next_stage):
        clear_state(state_path)
        stop_with_json(
            f"auto-plan stopped after consistency-pass for {doc_path_value}. "
            "The helper block does not currently approve implementation. Resolve the remaining inconsistencies in the main "
            f"artifact, then rerun `{format_skill_invocation(f'arch-step auto-plan {doc_path_value}')}` if you still want automatic planning continuation.",
            system_message="auto-plan consistency-pass did not approve implementation.",
        )

    if next_stage == "research":
        clear_state(state_path)
        stop_with_json(
            f"auto-plan stopped before research completed for {doc_path_value}. "
            "The controller was disarmed. Resolve the blocker or finish the stage manually, then rerun "
            f"`{format_skill_invocation(f'arch-step auto-plan {doc_path_value}')}` if you still want automatic planning continuation.",
            system_message="auto-plan stopped before research completed.",
        )

    changed = False
    if "stage_index" in state:
        state.pop("stage_index", None)
        changed = True
    if "stages" in state:
        state.pop("stages", None)
        changed = True
    if changed:
        write_state(state_path, state)

    block_with_json(
        auto_plan_continue_reason(doc_path_value, next_stage, state_path_value),
        system_message=f"auto-plan continuing with {auto_plan_stage_name(next_stage)}.",
    )


def handle_miniarch_step_implement_loop(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(
        payload,
        MINIARCH_STEP_IMPLEMENT_LOOP_STATE_SPEC,
    )
    validated = validate_miniarch_step_implement_loop_state(payload, resolved_state)
    if validated is None:
        return 0

    doc_path, doc_path_value, state_path = validated
    if not doc_path.exists():
        clear_state(state_path)
        block_with_message(
            f"miniarch-step implement-loop doc path does not exist: {doc_path_value}. "
            "The loop was disarmed. Update the plan and worklog truthfully, then stop."
        )

    try:
        audit = run_fresh_audit(
            cwd,
            doc_path_value,
            skill_name="miniarch-step",
            temp_prefix="miniarch-step-implement-loop-",
            model=MINIARCH_STEP_AUDIT_MODEL,
            model_reasoning_effort=MINIARCH_STEP_AUDIT_MODEL_REASONING_EFFORT,
        )
    except RuntimeError as exc:
        clear_state(state_path)
        block_with_message(
            f"fresh miniarch-step implement-loop audit could not start: {exc}. "
            "The loop was disarmed. Explain the blocker and stop."
        )

    child_summary = summarize_child_output(audit.process, audit.last_message)

    if audit.process.returncode != 0:
        clear_state(state_path)
        failure = child_summary or "unknown child-audit failure"
        block_with_json(
            "miniarch-step implement-loop ran a fresh child audit, but that audit failed. "
            f"Failure: {failure}. Treat the run as blocked, update the plan and worklog truthfully, explain the blocker, and stop.",
            system_message="miniarch-step implement-loop fresh audit failed; review the blocker and stop honestly.",
        )

    verdict = read_verdict(doc_path)
    if verdict == "COMPLETE":
        clear_state(state_path)
        stop_reason = (
            "miniarch-step implement-loop fresh audit finished clean. "
            f"Audit verdict is COMPLETE in {doc_path_value}. "
            f"The next required move is `{format_skill_invocation('arch-docs')}`. Current DOC_PATH: {doc_path_value}."
        )
        if child_summary:
            stop_reason += f" Audit summary: {child_summary}"
        stop_with_json(
            stop_reason,
            system_message="miniarch-step implement-loop fresh audit finished clean; hand off to arch-docs.",
        )

    if verdict == "NOT COMPLETE":
        worklog_path = derive_worklog_path(doc_path)
        reason = (
            "miniarch-step implement-loop ran a fresh child audit and found more code work. "
            f"Read the authoritative Implementation Audit block and reopened phases in {doc_path_value}, "
            "resume from the earliest reopened or incomplete phase, continue linearly through the remaining "
            "approved phases, run the required credible proof for the claimed work as you go, "
            f"update {display_path(worklog_path, cwd)} if it exists, keep the loop armed, "
            "and do not rewrite plan requirements, scope, acceptance criteria, or phase obligations while coding. "
            "If the audit shows the plan itself needs to change, stop and repair the plan instead of continuing on a rewritten story, "
            "and only then stop again for another fresh audit after the current reachable frontier is done or genuinely blocked."
        )
        if child_summary:
            reason += f" Audit summary: {child_summary}"
        block_with_json(
            reason,
            system_message="miniarch-step implement-loop fresh audit finished; more work remains.",
        )

    clear_state(state_path)
    reason = (
        f"miniarch-step implement-loop ran a fresh child audit, but that audit did not leave a usable verdict in {doc_path_value}. "
        "The loop was disarmed. Treat the run as blocked, update the plan and worklog truthfully, explain the blocker, and stop."
    )
    if child_summary:
        reason += f" Audit summary: {child_summary}"
    block_with_json(
        reason,
        system_message="miniarch-step implement-loop fresh audit finished without a usable verdict.",
    )


def handle_miniarch_step_auto_plan(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(
        payload,
        MINIARCH_STEP_AUTO_PLAN_STATE_SPEC,
    )
    validated = validate_miniarch_step_auto_plan_state(payload, resolved_state)
    if validated is None:
        return 0

    doc_path, doc_path_value, state, state_path = validated
    state_path_value = display_path(state_path, cwd)
    if not doc_path.exists():
        clear_state(state_path)
        block_with_message(
            f"miniarch-step auto-plan doc path does not exist: {doc_path_value}. "
            "The controller was disarmed. Update the plan truthfully and stop."
        )

    doc_text = read_doc_text(doc_path)
    next_stage = next_incomplete_miniarch_step_auto_plan_stage(doc_text)
    if next_stage is None:
        clear_state(state_path)
        stop_with_json(
            f"miniarch-step auto-plan completed for {doc_path_value}. Research, deep-dive, and phase-plan are in place. "
            f"The doc is ready for `{format_skill_invocation(f'miniarch-step implement-loop {doc_path_value}')}`.",
            system_message="miniarch-step auto-plan completed; the doc is ready for implement-loop.",
        )

    if next_stage == "research":
        clear_state(state_path)
        stop_with_json(
            f"miniarch-step auto-plan stopped before research completed for {doc_path_value}. "
            "The controller was disarmed. Resolve the blocker or finish the stage manually, then rerun "
            f"`{format_skill_invocation(f'miniarch-step auto-plan {doc_path_value}')}` if you still want automatic planning continuation.",
            system_message="miniarch-step auto-plan stopped before research completed.",
        )

    changed = False
    if "stage_index" in state:
        state.pop("stage_index", None)
        changed = True
    if "stages" in state:
        state.pop("stages", None)
        changed = True
    if changed:
        write_state(state_path, state)

    block_with_json(
        miniarch_step_auto_plan_continue_reason(doc_path_value, next_stage, state_path_value),
        system_message=(
            "miniarch-step auto-plan continuing with "
            f"{miniarch_step_auto_plan_stage_name(next_stage)}."
        ),
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
            f"Continue now with the next required command: {format_skill_invocation('arch-docs')}. "
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
    if verdict not in LOOP_VALID_VERDICTS:
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
        f"audit-loop fresh review found more worthwhile work. Continue now with `{format_skill_invocation('audit-loop')}`. "
        f"Next area: {next_area}. Keep {state_path_value} armed and stop naturally when this pass finishes."
    )
    if child_summary:
        reason += f" Review summary: {child_summary}"
    block_with_json(reason, system_message="audit-loop review found more work.")


def handle_comment_loop(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, COMMENT_LOOP_STATE_SPEC)
    validated = validate_comment_loop_state(payload, resolved_state)
    if validated is None:
        return 0

    ledger_path, ledger_path_value, state, state_path = validated
    state_path_value = display_path(state_path, cwd)

    try:
        review = run_fresh_comment_review(cwd)
    except RuntimeError as exc:
        clear_state(state_path)
        stop_with_json(
            f"comment-loop could not start a fresh review pass: {exc}. The controller was disarmed.",
            system_message="comment-loop fresh review could not start.",
        )

    child_summary = summarize_child_output(review.process, review.last_message)
    if review.process.returncode != 0:
        clear_state(state_path)
        reason = "comment-loop ran a fresh review pass, but that review failed."
        if child_summary:
            reason += f" Failure: {child_summary}."
        stop_with_json(
            reason + " Treat the run as blocked, keep the ledger, and stop honestly.",
            system_message="comment-loop fresh review failed.",
        )

    fields = read_comment_loop_controller_fields(ledger_path)
    if not fields:
        clear_state(state_path)
        reason = (
            f"comment-loop fresh review finished, but {ledger_path_value} does not contain a usable controller block. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="comment-loop review left no usable controller block.")

    verdict = fields.get("Verdict", "").strip().upper()
    if verdict not in LOOP_VALID_VERDICTS:
        clear_state(state_path)
        reason = (
            f"comment-loop fresh review finished, but {ledger_path_value} has an invalid verdict. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="comment-loop review left an invalid verdict.")

    if verdict == "CLEAN":
        clear_state(state_path)
        cleanup_comment_loop_runtime_artifacts(cwd, ledger_path, state)
        stop_reason = "comment-loop fresh review finished clean. The comment ledger was removed."
        if child_summary:
            stop_reason += f" Review summary: {child_summary}"
        stop_with_json(stop_reason, system_message="comment-loop completed clean.")

    if verdict == "BLOCKED":
        clear_state(state_path)
        stop_reason = fields.get("Stop Reason") or "comment-loop review marked the loop blocked."
        if child_summary:
            stop_reason += f" Review summary: {child_summary}"
        stop_with_json(stop_reason, system_message="comment-loop stopped blocked.")

    next_area = fields.get("Next Area", "").strip()
    if not next_area:
        clear_state(state_path)
        reason = (
            f"comment-loop review returned CONTINUE without Next Area in {ledger_path_value}. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="comment-loop review omitted Next Area.")

    reason = (
        f"comment-loop fresh review found more worthwhile comment work. Continue now with `{format_skill_invocation('comment-loop')}`. "
        f"Next area: {next_area}. Keep {state_path_value} armed and stop naturally when this pass finishes."
    )
    if child_summary:
        reason += f" Review summary: {child_summary}"
    block_with_json(reason, system_message="comment-loop review found more work.")


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
    if verdict not in LOOP_VALID_VERDICTS:
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
        f"audit-loop-sim fresh review found more worthwhile automation work. Continue now with `{format_skill_invocation('audit-loop-sim')}`. "
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


def handle_code_review(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, CODE_REVIEW_STATE_SPEC)
    validated = validate_code_review_state(payload, resolved_state)
    if validated is None:
        return 0

    state, state_path = validated
    state_path_value = display_path(state_path, cwd)

    runner_path = resolve_code_review_runner_path()
    if runner_path is None:
        clear_state(state_path)
        stop_with_json(
            "code-review controller was armed but the runner script "
            f"({CODE_REVIEW_RUNNER_RELATIVE_PATH}) could not be located from the installed dispatcher. "
            "The controller was disarmed.",
            system_message="code-review runner script missing.",
        )

    repo_root = Path(state["repo_root"]).resolve()
    args_list = build_code_review_runner_args(runner_path, state, repo_root)

    # Intentional exception: this dispatcher is runtime-aware, but the review
    # subprocess itself always shells out to Codex via the runner. Claude is
    # allowed to host the hook; it is not allowed to be the reviewer.
    try:
        process = subprocess.run(
            args_list,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        clear_state(state_path)
        stop_with_json(
            f"code-review runner could not start: {exc}. The controller was disarmed.",
            system_message="code-review runner could not start.",
        )
    except OSError as exc:
        clear_state(state_path)
        stop_with_json(
            f"code-review runner failed to launch: {exc}. The controller was disarmed.",
            system_message="code-review runner failed to launch.",
        )

    output_root_value = state.get("output_root")
    output_root_path = Path(output_root_value).resolve() if output_root_value else None
    run_dir = locate_code_review_run_dir(process.stdout, process.stderr, output_root_path)

    child_summary = " ".join((process.stderr or "").strip().split())
    if len(child_summary) > DETAIL_LIMIT:
        child_summary = child_summary[: DETAIL_LIMIT - 3] + "..."

    if process.returncode != 0:
        clear_state(state_path)
        reason = (
            f"code-review runner exited non-zero (code {process.returncode}). Former state: {state_path_value}."
        )
        if run_dir is not None:
            reason += f" Preserved artifacts: {run_dir}."
        if child_summary:
            reason += f" Stderr: {child_summary}"
        stop_with_json(reason, system_message="code-review runner failed.")

    verdict, synthesis_path = extract_code_review_verdict(run_dir) if run_dir is not None else (None, None)

    clear_state(state_path)

    if run_dir is None:
        reason = (
            "code-review runner finished without reporting a run directory. "
            f"Former state: {state_path_value}."
        )
        if child_summary:
            reason += f" Stdout/stderr: {child_summary}"
        stop_with_json(reason, system_message="code-review runner left no run directory.")

    if verdict is None:
        reason = (
            "code-review runner finished but synthesis.final.txt did not contain a VERDICT line. "
            f"Run directory: {run_dir}. Former state: {state_path_value}."
        )
        stop_with_json(reason, system_message="code-review synthesis missing VERDICT line.")

    synthesis_value = str(synthesis_path) if synthesis_path is not None else str(run_dir / "synthesis.final.txt")
    stop_reason = (
        f"code-review finished with VERDICT: {verdict}. "
        f"Synthesis: {synthesis_value}. Run directory: {run_dir}."
    )
    stop_with_json(stop_reason, system_message=f"code-review verdict: {verdict}.")


def handle_wait(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, WAIT_STATE_SPEC)
    validated = validate_wait_state(payload, resolved_state)
    if validated is None:
        return 0

    state, state_path = validated
    state_path_value = display_path(state_path, cwd)
    deadline_at = state["deadline_at"]
    resume_prompt = state["resume_prompt"]

    remaining = max(0, deadline_at - current_epoch_seconds())
    sleep_for_seconds(remaining)

    clear_state(state_path)
    reason = (
        f"{resume_prompt} The requested wait elapsed. "
        f"Former wait state: {state_path_value}."
    )
    block_with_json(
        reason,
        system_message="wait elapsed; continuing the task.",
    )


def _arch_loop_stop_invalid_output(
    state_path: Path,
    reason: str,
    *,
    system_message: str,
) -> None:
    clear_state(state_path)
    stop_with_json(reason, system_message=system_message)


def _arch_loop_continuation_prompt(
    next_task: str,
    state_path_value: str,
) -> str:
    invocation = format_skill_invocation(ARCH_LOOP_COMMAND)
    return (
        f"arch-loop evaluator says the loop needs another parent pass. Run {invocation} "
        f"and do exactly this next task: {next_task}. After you finish, end the turn so the "
        f"installed Stop hook re-runs the fresh evaluator. Loop state: {state_path_value}."
    )


def handle_arch_loop(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    resolved_state = resolve_controller_state_for_handler(payload, ARCH_LOOP_STATE_SPEC)
    validated = validate_arch_loop_state(payload, resolved_state)
    if validated is None:
        return 0

    state, state_path = validated
    state_path_value = display_path(state_path, cwd)

    # A parent turn just completed. Increment iteration_count once per Stop-hook
    # entry and persist before we consult the evaluator, so a crash mid-run
    # cannot silently rewind the iteration cap.
    state["iteration_count"] = int(state.get("iteration_count") or 0) + 1
    write_state(state_path, state)

    prompt_path = resolve_arch_loop_evaluator_prompt_path()
    if prompt_path is None:
        clear_state(state_path)
        stop_with_json(
            "arch-loop controller was armed but the evaluator prompt "
            "(skills/arch-loop/references/evaluator-prompt.md) could not be located "
            "from the installed dispatcher. The controller was disarmed.",
            system_message="arch-loop evaluator prompt missing.",
        )
    try:
        prompt_text = prompt_path.read_text(encoding="utf-8")
    except OSError as exc:
        clear_state(state_path)
        stop_with_json(
            f"arch-loop evaluator prompt could not be read: {exc}. "
            "The controller was disarmed.",
            system_message="arch-loop evaluator prompt unreadable.",
        )

    repo_root = cwd

    while True:
        now = current_epoch_seconds()
        deadline_at = state.get("deadline_at")
        interval_seconds = state.get("interval_seconds")
        max_iterations = state.get("max_iterations")
        next_due_at = state.get("next_due_at")

        if deadline_at is not None and now >= deadline_at:
            clear_state(state_path)
            stop_with_json(
                "arch-loop timed out: the runtime deadline elapsed before the evaluator "
                f"returned clean. Iterations completed: {state['iteration_count']}, "
                f"cadence checks completed: {state.get('check_count') or 0}. "
                f"Former loop state: {state_path_value}.",
                system_message="arch-loop timed out without a clean verdict.",
            )

        if next_due_at is not None and now < next_due_at:
            sleep_for_seconds(arch_loop_sleep_reason(next_due_at, deadline_at))
            continue

        if next_due_at is not None:
            state["check_count"] = int(state.get("check_count") or 0) + 1
            write_state(state_path, state)

        try:
            evaluator_result = run_arch_loop_evaluator(cwd, state, repo_root, prompt_text)
        except RuntimeError as exc:
            clear_state(state_path)
            stop_with_json(
                f"arch-loop could not launch the fresh Codex evaluator: {exc}. "
                "The controller was disarmed.",
                system_message="arch-loop fresh evaluator could not start.",
            )

        child_summary = summarize_child_output(
            evaluator_result.process,
            evaluator_result.last_message,
        )
        if evaluator_result.process.returncode != 0:
            clear_state(state_path)
            reason = "arch-loop ran the fresh evaluator, but the evaluator process failed."
            if child_summary:
                reason += f" Failure: {child_summary}."
            stop_with_json(
                reason + " The controller was disarmed.",
                system_message="arch-loop fresh evaluator failed.",
            )

        verdict_payload = evaluator_result.payload
        if not isinstance(verdict_payload, dict):
            reason = (
                "arch-loop fresh evaluator did not return usable structured JSON."
            )
            if child_summary:
                reason += f" Evaluator output: {child_summary}"
            _arch_loop_stop_invalid_output(
                state_path,
                reason + " The controller was disarmed.",
                system_message="arch-loop fresh evaluator returned unusable output.",
            )

        verdict = verdict_payload.get("verdict")
        if verdict not in _ARCH_LOOP_EVAL_VERDICTS:
            _arch_loop_stop_invalid_output(
                state_path,
                "arch-loop fresh evaluator returned an invalid verdict "
                f"({verdict!r}). The controller was disarmed.",
                system_message="arch-loop fresh evaluator returned invalid verdict.",
            )

        summary_text = verdict_payload.get("summary")
        if not isinstance(summary_text, str) or not summary_text.strip():
            _arch_loop_stop_invalid_output(
                state_path,
                "arch-loop fresh evaluator returned an empty summary. "
                "The controller was disarmed.",
                system_message="arch-loop fresh evaluator returned empty summary.",
            )

        satisfied = verdict_payload.get("satisfied_requirements")
        unsatisfied = verdict_payload.get("unsatisfied_requirements")
        eval_audits = verdict_payload.get("required_skill_audits")
        if (
            not isinstance(satisfied, list)
            or not isinstance(unsatisfied, list)
            or not isinstance(eval_audits, list)
        ):
            _arch_loop_stop_invalid_output(
                state_path,
                "arch-loop fresh evaluator returned malformed requirement or audit "
                "arrays. The controller was disarmed.",
                system_message="arch-loop fresh evaluator returned malformed arrays.",
            )
        for audit in eval_audits:
            if (
                not isinstance(audit, dict)
                or audit.get("status") not in _ARCH_LOOP_EVAL_AUDIT_STATUSES
            ):
                _arch_loop_stop_invalid_output(
                    state_path,
                    "arch-loop fresh evaluator returned an audit entry with an "
                    "invalid status. The controller was disarmed.",
                    system_message="arch-loop fresh evaluator returned bad audit status.",
                )

        summary_clean = summary_text.strip()
        continue_mode = verdict_payload.get("continue_mode")
        next_task = verdict_payload.get("next_task")
        blocker = verdict_payload.get("blocker")

        if verdict == "clean":
            for audit in eval_audits:
                if audit.get("status") not in _ARCH_LOOP_CLEAN_AUDIT_STATUSES:
                    _arch_loop_stop_invalid_output(
                        state_path,
                        "arch-loop evaluator returned clean but at least one "
                        "required_skill_audits entry was not pass or inapplicable. "
                        "The controller was disarmed.",
                        system_message=(
                            "arch-loop clean verdict contradicted audit statuses."
                        ),
                    )
            if unsatisfied:
                listed = "; ".join(str(item) for item in unsatisfied if isinstance(item, str))
                _arch_loop_stop_invalid_output(
                    state_path,
                    "arch-loop evaluator returned clean but unsatisfied_requirements "
                    f"is non-empty ({listed}). The controller was disarmed.",
                    system_message=(
                        "arch-loop clean verdict contradicted unsatisfied_requirements."
                    ),
                )
            clear_state(state_path)
            stop_with_json(
                f"arch-loop evaluator returned clean: {summary_clean}. "
                f"Former loop state: {state_path_value}.",
                system_message="arch-loop reached a clean verdict.",
            )

        if verdict == "blocked":
            if not isinstance(blocker, str) or not blocker.strip():
                _arch_loop_stop_invalid_output(
                    state_path,
                    "arch-loop evaluator returned blocked without a blocker string. "
                    "The controller was disarmed.",
                    system_message="arch-loop blocked verdict missing blocker.",
                )
            clear_state(state_path)
            stop_with_json(
                f"arch-loop evaluator returned blocked: {blocker.strip()}. "
                f"Summary: {summary_clean}. Former loop state: {state_path_value}.",
                system_message="arch-loop blocked; user resolution required.",
            )

        # verdict == "continue"
        if continue_mode not in {"parent_work", "wait_recheck"}:
            _arch_loop_stop_invalid_output(
                state_path,
                "arch-loop evaluator returned continue without a valid continue_mode. "
                "The controller was disarmed.",
                system_message="arch-loop continue verdict missing continue_mode.",
            )
        if not isinstance(next_task, str) or not next_task.strip():
            _arch_loop_stop_invalid_output(
                state_path,
                "arch-loop evaluator returned continue without a next_task. "
                "The controller was disarmed.",
                system_message="arch-loop continue verdict missing next_task.",
            )

        state["last_evaluator_verdict"] = verdict
        state["last_evaluator_summary"] = summary_clean
        state["last_continue_mode"] = continue_mode
        state["last_next_task"] = next_task.strip()

        if continue_mode == "parent_work":
            if max_iterations is not None and state["iteration_count"] >= max_iterations:
                clear_state(state_path)
                stop_with_json(
                    "arch-loop reached its max_iterations cap "
                    f"({max_iterations}) before the evaluator returned clean. "
                    f"Last summary: {summary_clean}. "
                    f"Former loop state: {state_path_value}.",
                    system_message="arch-loop max_iterations cap reached.",
                )
            write_state(state_path, state)
            block_with_json(
                _arch_loop_continuation_prompt(next_task.strip(), state_path_value),
                system_message="arch-loop continuing with a bounded parent pass.",
            )

        # wait_recheck
        if interval_seconds is None:
            _arch_loop_stop_invalid_output(
                state_path,
                "arch-loop evaluator returned wait_recheck but no cadence "
                "interval_seconds is armed. The controller was disarmed.",
                system_message="arch-loop wait_recheck without armed cadence.",
            )
        scheduled = current_epoch_seconds() + interval_seconds
        if deadline_at is not None and scheduled > deadline_at:
            clear_state(state_path)
            stop_with_json(
                "arch-loop timed out: the next scheduled cadence check would land "
                f"after the runtime deadline ({deadline_at}). "
                f"Last summary: {summary_clean}. "
                f"Former loop state: {state_path_value}.",
                system_message="arch-loop cadence would overrun the deadline.",
            )
        state["next_due_at"] = scheduled
        write_state(state_path, state)
        # loop back; the top of the while will sleep until next_due_at and
        # re-run the evaluator without waking the parent.


def collect_active_state_paths_for_session(payload: dict) -> list[Path]:
    cwd = Path(payload["cwd"]).resolve()
    session_id = current_session_id(payload)
    paths: list[Path] = []
    for spec in CONTROLLER_STATE_SPECS:
        relative = controller_state_relative_path(spec)
        if session_id is not None:
            session_path = cwd / session_state_relative_path(relative, session_id)
            if session_path.exists():
                paths.append(session_path)
        legacy_path = cwd / relative
        if legacy_path.exists() and state_matches_session(
            load_json_object_quiet(legacy_path),
            spec.expected_command,
            session_id,
            allow_missing_session_id=True,
        ):
            paths.append(legacy_path)
    return paths


def block_when_multiple_controller_states_armed(payload: dict) -> None:
    cwd = Path(payload["cwd"]).resolve()
    paths = collect_active_state_paths_for_session(payload)
    if len(paths) < 2:
        return
    listed = ", ".join(display_path(p, cwd) for p in paths)
    stop_with_json(
        "Multiple suite controller states are armed for this session: "
        f"{listed}. Resolve the conflict by clearing the stale state files, "
        "then rerun the intended controller.",
        system_message="multiple suite controller states armed for this session.",
    )


def main() -> int:
    global ACTIVE_RUNTIME
    args = parse_args()
    ACTIVE_RUNTIME = HOOK_RUNTIME_SPECS[args.runtime]
    payload = load_stop_payload()
    block_when_multiple_controller_states_armed(payload)
    handle_miniarch_step_implement_loop(payload)
    handle_implement_loop(payload)
    handle_miniarch_step_auto_plan(payload)
    handle_auto_plan(payload)
    handle_arch_docs_auto(payload)
    handle_audit_loop(payload)
    handle_comment_loop(payload)
    handle_audit_loop_sim(payload)
    handle_delay_poll(payload)
    handle_code_review(payload)
    handle_wait(payload)
    handle_arch_loop(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
