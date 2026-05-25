#!/usr/bin/env python3
"""Stage receipts for arch-step auto-plan.

This helper is intentionally small. It gates ordered planning stages by writing
and checking one generated receipt block inside DOC_PATH. It does not run the
workflow, install hooks, spawn agents, or judge section quality.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


VERSION = 1
START = "<!-- arch_skill:block:auto_plan_receipts:start -->"
END = "<!-- arch_skill:block:auto_plan_receipts:end -->"
PLANNING_PASSES_END = "<!-- arch_skill:block:planning_passes:end -->"

BLOCK_MARKERS = {
    "research_grounding": "<!-- arch_skill:block:research_grounding:start -->",
    "current_architecture": "<!-- arch_skill:block:current_architecture:start -->",
    "target_architecture": "<!-- arch_skill:block:target_architecture:start -->",
    "call_site_audit": "<!-- arch_skill:block:call_site_audit:start -->",
    "phase_plan": "<!-- arch_skill:block:phase_plan:start -->",
    "consistency_pass": "<!-- arch_skill:block:consistency_pass:start -->",
}


@dataclass(frozen=True)
class Stage:
    name: str
    command: str
    reference: str


STAGES = (
    Stage("research", "research", "arch-research.md"),
    Stage("deep-dive-pass-1", "deep-dive", "arch-deep-dive.md"),
    Stage("deep-dive-pass-2", "deep-dive", "arch-deep-dive.md"),
    Stage("phase-plan", "phase-plan", "arch-phase-plan.md"),
    Stage("consistency-pass", "consistency-pass", "arch-consistency-pass.md"),
)
STAGES_BY_NAME = {stage.name: stage for stage in STAGES}
STAGE_NAMES = tuple(stage.name for stage in STAGES)


class GateError(Exception):
    def __init__(self, message: str, *, next_command: str | None = None) -> None:
        super().__init__(message)
        self.next_command = next_command


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def references_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "references"


def command_ref_hash(stage: Stage) -> str:
    return sha256_text((references_dir() / stage.reference).read_text(encoding="utf-8"))


def strip_receipts_block(text: str) -> str:
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.DOTALL)
    return pattern.sub("", text)


def doc_content_hash(text: str) -> str:
    normalized = re.sub(r"\n{3,}", "\n\n", strip_receipts_block(text)).strip()
    return sha256_text(normalized)


def receipts_digest(receipts: list[dict[str, Any]]) -> str:
    payload = {"version": VERSION, "receipts": receipts}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256_text(canonical)


def state_from_receipts(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": VERSION,
        "digest": receipts_digest(receipts),
        "receipts": receipts,
    }


def extract_receipts_block(text: str) -> str | None:
    start = text.find(START)
    end = text.find(END)
    if start == -1 and end == -1:
        return None
    if start == -1 or end == -1 or end < start:
        raise GateError("malformed auto-plan receipt block")
    return text[start + len(START) : end].strip()


def load_receipts(text: str) -> list[dict[str, Any]]:
    raw = extract_receipts_block(text)
    if raw is None:
        return []
    try:
        state = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise GateError(f"invalid auto-plan receipt JSON: {exc.msg}") from exc

    if state.get("version") != VERSION:
        raise GateError("unsupported auto-plan receipt version")
    receipts = state.get("receipts")
    if not isinstance(receipts, list):
        raise GateError("auto-plan receipt block is missing receipts")
    if state.get("digest") != receipts_digest(receipts):
        raise GateError("auto-plan receipt digest mismatch")

    validate_receipt_order(receipts)
    return receipts


def validate_receipt_order(receipts: list[dict[str, Any]]) -> None:
    if len(receipts) > len(STAGES):
        raise GateError("too many auto-plan receipts")

    open_count = 0
    for index, receipt in enumerate(receipts):
        expected_stage = STAGES[index]
        stage = receipt.get("stage")
        status = receipt.get("status")
        if stage != expected_stage.name:
            raise GateError(
                f"receipt order mismatch at position {index + 1}: expected {expected_stage.name}"
            )
        if status not in {"in_progress", "complete"}:
            raise GateError(f"invalid receipt status for {stage}")
        if status == "in_progress":
            open_count += 1
            if index != len(receipts) - 1:
                raise GateError("only the last auto-plan receipt may be in progress")
        if not isinstance(receipt.get("started_at"), str):
            raise GateError(f"receipt for {stage} is missing started_at")
        if not isinstance(receipt.get("command_ref_hash"), str):
            raise GateError(f"receipt for {stage} is missing command_ref_hash")
        if not isinstance(receipt.get("doc_hash_before"), str):
            raise GateError(f"receipt for {stage} is missing doc_hash_before")
        if status == "complete":
            if not isinstance(receipt.get("completed_at"), str):
                raise GateError(f"receipt for {stage} is missing completed_at")
            if not isinstance(receipt.get("doc_hash_after"), str):
                raise GateError(f"receipt for {stage} is missing doc_hash_after")
    if open_count > 1:
        raise GateError("multiple auto-plan receipts are in progress")


def render_receipts_block(receipts: list[dict[str, Any]]) -> str:
    state = state_from_receipts(receipts)
    return START + "\n" + json.dumps(state, indent=2) + "\n" + END


def replace_or_insert_receipts_block(text: str, receipts: list[dict[str, Any]]) -> str:
    block = render_receipts_block(receipts)
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    if PLANNING_PASSES_END in text:
        return text.replace(PLANNING_PASSES_END, PLANNING_PASSES_END + "\n\n" + block, 1)

    frontmatter = re.match(r"\A---\n.*?\n---\n", text, re.DOTALL)
    if frontmatter:
        end = frontmatter.end()
        return text[:end] + "\n" + block + "\n\n" + text[end:]
    return block + "\n\n" + text


def write_receipts(doc_path: Path, receipts: list[dict[str, Any]]) -> None:
    text = doc_path.read_text(encoding="utf-8")
    doc_path.write_text(replace_or_insert_receipts_block(text, receipts), encoding="utf-8")


def open_receipt(receipts: list[dict[str, Any]]) -> dict[str, Any] | None:
    if receipts and receipts[-1].get("status") == "in_progress":
        return receipts[-1]
    return None


def next_stage(receipts: list[dict[str, Any]]) -> Stage | None:
    current = open_receipt(receipts)
    if current is not None:
        return STAGES_BY_NAME[current["stage"]]
    if len(receipts) >= len(STAGES):
        return None
    return STAGES[len(receipts)]


def require_marker(text: str, marker_name: str) -> None:
    marker = BLOCK_MARKERS[marker_name]
    if marker not in text:
        raise GateError(f"missing {marker_name} block")


def require_planning_pass(text: str, field: str) -> None:
    pattern = re.compile(rf"^\s*{re.escape(field)}:\s*done\s+\d{{4}}-\d{{2}}-\d{{2}}\b", re.MULTILINE)
    if not pattern.search(text):
        raise GateError(f"missing completed planning_passes.{field}")


def extract_block(text: str, marker_name: str) -> str:
    start = f"<!-- arch_skill:block:{marker_name}:start -->"
    end = f"<!-- arch_skill:block:{marker_name}:end -->"
    start_index = text.find(start)
    end_index = text.find(end)
    if start_index == -1 or end_index == -1 or end_index < start_index:
        raise GateError(f"missing {marker_name} block")
    return text[start_index + len(start) : end_index]


def field_value(block: str, label: str) -> str | None:
    lines = block.splitlines()
    for index, line in enumerate(lines):
        match = re.match(rf"\s*-\s*{re.escape(label)}:\s*(.*)\s*$", line)
        if not match:
            continue
        inline_value = match.group(1).strip()
        if inline_value:
            return inline_value.lower()
        for follow in lines[index + 1 :]:
            stripped = follow.strip()
            if not stripped:
                continue
            if stripped.startswith("- "):
                return stripped[2:].strip().lower()
            return stripped.lower()
    return None


def proceed_to_implement_value(block: str) -> str | None:
    match = re.search(
        r"^\s*-\s*Decision: proceed to implement\?\s*(yes|no)\s*$",
        block,
        re.MULTILINE,
    )
    if match:
        return match.group(1).lower()
    return field_value(block, "Decision: proceed to implement?")


def validate_stage_evidence(stage_name: str, text: str) -> None:
    if stage_name == "research":
        require_marker(text, "research_grounding")
        return

    if stage_name in {"deep-dive-pass-1", "deep-dive-pass-2"}:
        require_marker(text, "current_architecture")
        require_marker(text, "target_architecture")
        require_marker(text, "call_site_audit")
        field = "deep_dive_pass_1" if stage_name == "deep-dive-pass-1" else "deep_dive_pass_2"
        require_planning_pass(text, field)
        return

    if stage_name == "phase-plan":
        require_marker(text, "phase_plan")
        return

    if stage_name == "consistency-pass":
        require_marker(text, "consistency_pass")
        block = extract_block(text, "consistency_pass")
        if field_value(block, "Decision-complete") != "yes":
            raise GateError("consistency-pass is not decision-complete")
        if field_value(block, "Unresolved decisions") != "none":
            raise GateError("consistency-pass still has unresolved decisions")
        if proceed_to_implement_value(block) != "yes":
            raise GateError("consistency-pass does not approve implementation")
        return

    raise GateError(f"unknown stage {stage_name}")


def status_line(receipts: list[dict[str, Any]], text: str) -> tuple[int, str]:
    current = open_receipt(receipts)
    if current is not None:
        stage = STAGES_BY_NAME[current["stage"]]
        return 0, f"IN_PROGRESS stage={stage.name} command={stage.command}"

    stage = next_stage(receipts)
    if stage is not None:
        return 0, f"NOT_READY next={stage.command} stage={stage.name} reason=missing_receipt"

    try:
        for known_stage in STAGES:
            validate_stage_evidence(known_stage.name, text)
    except GateError as exc:
        return 1, f"NOT_READY next=auto-plan reason={str(exc).replace(' ', '_')}"
    return 0, "READY next=implement-loop"


def begin_stage(doc_path: Path, stage_name: str) -> str:
    text = doc_path.read_text(encoding="utf-8")
    receipts = load_receipts(text)
    current = open_receipt(receipts)
    requested = STAGES_BY_NAME[stage_name]

    if current is not None:
        current_stage = STAGES_BY_NAME[current["stage"]]
        if current_stage.name == requested.name:
            return f"BEGIN_ALREADY stage={requested.name} command={requested.command}"
        raise GateError(
            f"stage {current_stage.name} is already in progress",
            next_command=current_stage.command,
        )

    expected = next_stage(receipts)
    if expected is None:
        raise GateError("auto-plan receipts are already complete", next_command="implement-loop")
    if expected.name != requested.name:
        raise GateError(f"expected stage {expected.name}", next_command=expected.command)

    receipts.append(
        {
            "stage": requested.name,
            "command": requested.command,
            "status": "in_progress",
            "started_at": now_utc(),
            "command_ref_hash": command_ref_hash(requested),
            "doc_hash_before": doc_content_hash(text),
        }
    )
    write_receipts(doc_path, receipts)
    return f"BEGIN stage={requested.name} command={requested.command}"


def complete_stage(doc_path: Path, stage_name: str) -> str:
    text = doc_path.read_text(encoding="utf-8")
    receipts = load_receipts(text)
    current = open_receipt(receipts)
    requested = STAGES_BY_NAME[stage_name]

    if current is None:
        expected = next_stage(receipts)
        next_command = expected.command if expected is not None else "implement-loop"
        raise GateError("no matching stage receipt is in progress", next_command=next_command)
    if current["stage"] != requested.name:
        current_stage = STAGES_BY_NAME[current["stage"]]
        raise GateError(
            f"stage {current_stage.name} is in progress",
            next_command=current_stage.command,
        )

    after_hash = doc_content_hash(text)
    if after_hash == current["doc_hash_before"]:
        raise GateError("stage did not change DOC_PATH after begin", next_command=requested.command)

    validate_stage_evidence(requested.name, text)
    current["status"] = "complete"
    current["completed_at"] = now_utc()
    current["doc_hash_after"] = after_hash
    write_receipts(doc_path, receipts)

    next_required = next_stage(receipts)
    if next_required is None:
        return f"COMPLETE stage={requested.name} next=implement-loop"
    return f"COMPLETE stage={requested.name} next={next_required.command}"


def ready(doc_path: Path) -> tuple[int, str]:
    text = doc_path.read_text(encoding="utf-8")
    receipts = load_receipts(text)
    code, line = status_line(receipts, text)
    if line.startswith("READY "):
        return code, line
    return 1, line


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gate arch-step auto-plan stages by DOC_PATH receipts.")
    parser.add_argument("action", choices=["begin", "complete", "status", "ready"])
    parser.add_argument("--doc", required=True, type=Path, help="Canonical arch-step DOC_PATH.")
    parser.add_argument("--stage", choices=STAGE_NAMES, help="Stage for begin/complete.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if args.action in {"begin", "complete"} and args.stage is None:
            raise GateError("--stage is required")
        if args.action == "begin":
            print(begin_stage(args.doc, args.stage))
            return 0
        if args.action == "complete":
            print(complete_stage(args.doc, args.stage))
            return 0

        text = args.doc.read_text(encoding="utf-8")
        receipts = load_receipts(text)
        if args.action == "status":
            code, line = status_line(receipts, text)
            print(line)
            return code
        code, line = ready(args.doc)
        print(line)
        return code
    except GateError as exc:
        reason = str(exc).replace(" ", "_")
        if exc.next_command:
            print(f"NOT_READY next={exc.next_command} reason={reason}")
        else:
            print(f"ERROR reason={reason}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
