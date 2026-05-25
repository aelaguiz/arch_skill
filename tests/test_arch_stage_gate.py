import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "skills/arch-step/scripts/arch_stage_gate.py"


def load_script():
    spec = importlib.util.spec_from_file_location("arch_stage_gate", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BASE_DOC = """---
title: "Test - Architecture Plan"
date: 2026-05-25
status: active
fallback_policy: forbidden
owners: []
reviewers: []
doc_type: architectural_change
related: []
---

# TL;DR

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: not started
external_research_grounding: not started
deep_dive_pass_2: not started
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star
"""


RESEARCH_BLOCK = """

<!-- arch_skill:block:research_grounding:start -->
# Research Grounding (external + internal "ground truth")
## Internal ground truth (code as spec)
- `src/example.py` - owns the behavior.
## Decision gaps that must be resolved before implementation
- none
<!-- arch_skill:block:research_grounding:end -->
"""


DEEP_BLOCKS = """

<!-- arch_skill:block:current_architecture:start -->
# Current Architecture (as-is)
- Current behavior.
<!-- arch_skill:block:current_architecture:end -->

<!-- arch_skill:block:target_architecture:start -->
# Target Architecture (to-be)
- Target behavior.
<!-- arch_skill:block:target_architecture:end -->

<!-- arch_skill:block:call_site_audit:start -->
# Call-Site Audit (exhaustive change inventory)
- Call site.
<!-- arch_skill:block:call_site_audit:end -->
"""


PHASE_BLOCK = """

<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)
## Phase 1 - First slice
* Checklist (must all be done):
  - Build it.
* Exit criteria (all required):
  - It works.
<!-- arch_skill:block:phase_plan:end -->
"""


CONSISTENCY_BLOCK_YES = """

<!-- arch_skill:block:consistency_pass:start -->
## Consistency Pass
- Reviewers:
  - self-integrator
- Unresolved decisions:
  - none
- Decision-complete:
  - yes
- Decision: proceed to implement? yes
<!-- arch_skill:block:consistency_pass:end -->
"""


class ArchStageGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gate = load_script()

    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.doc_path = Path(self.tmpdir.name) / "PLAN.md"
        self.doc_path.write_text(BASE_DOC, encoding="utf-8")

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def run_gate(self, *args: str) -> tuple[int, str]:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.gate.main([*args, "--doc", str(self.doc_path)])
        return code, stdout.getvalue().strip()

    def append_doc(self, text: str) -> None:
        current = self.doc_path.read_text(encoding="utf-8")
        self.doc_path.write_text(current + text, encoding="utf-8")

    def replace_doc(self, old: str, new: str) -> None:
        current = self.doc_path.read_text(encoding="utf-8")
        self.doc_path.write_text(current.replace(old, new), encoding="utf-8")

    def complete_research(self) -> None:
        code, _ = self.run_gate("begin", "--stage", "research")
        self.assertEqual(code, 0)
        self.append_doc(RESEARCH_BLOCK)
        code, output = self.run_gate("complete", "--stage", "research")
        self.assertEqual(code, 0, output)

    def complete_deep_dive_pass_1(self) -> None:
        code, _ = self.run_gate("begin", "--stage", "deep-dive-pass-1")
        self.assertEqual(code, 0)
        self.append_doc(DEEP_BLOCKS)
        self.replace_doc("deep_dive_pass_1: not started", "deep_dive_pass_1: done 2026-05-25")
        code, output = self.run_gate("complete", "--stage", "deep-dive-pass-1")
        self.assertEqual(code, 0, output)

    def complete_deep_dive_pass_2(self) -> None:
        code, _ = self.run_gate("begin", "--stage", "deep-dive-pass-2")
        self.assertEqual(code, 0)
        self.append_doc("\nSecond deep-dive hardening pass.\n")
        self.replace_doc("deep_dive_pass_2: not started", "deep_dive_pass_2: done 2026-05-25")
        code, output = self.run_gate("complete", "--stage", "deep-dive-pass-2")
        self.assertEqual(code, 0, output)

    def complete_phase_plan(self) -> None:
        code, _ = self.run_gate("begin", "--stage", "phase-plan")
        self.assertEqual(code, 0)
        self.append_doc(PHASE_BLOCK)
        code, output = self.run_gate("complete", "--stage", "phase-plan")
        self.assertEqual(code, 0, output)

    def complete_consistency_pass(self) -> None:
        code, _ = self.run_gate("begin", "--stage", "consistency-pass")
        self.assertEqual(code, 0)
        self.append_doc(CONSISTENCY_BLOCK_YES)
        code, output = self.run_gate("complete", "--stage", "consistency-pass")
        self.assertEqual(code, 0, output)

    def complete_all_stages(self) -> None:
        self.complete_research()
        self.complete_deep_dive_pass_1()
        self.complete_deep_dive_pass_2()
        self.complete_phase_plan()
        self.complete_consistency_pass()

    def test_status_on_new_doc_starts_at_research(self) -> None:
        code, output = self.run_gate("status")
        self.assertEqual(code, 0)
        self.assertIn("NOT_READY next=research stage=research", output)

    def test_complete_without_begin_fails(self) -> None:
        code, output = self.run_gate("complete", "--stage", "research")
        self.assertEqual(code, 2)
        self.assertIn("NOT_READY next=research", output)

    def test_begin_out_of_order_fails(self) -> None:
        code, output = self.run_gate("begin", "--stage", "phase-plan")
        self.assertEqual(code, 2)
        self.assertIn("NOT_READY next=research", output)

    def test_manual_research_block_without_receipt_does_not_unlock_deep_dive(self) -> None:
        self.append_doc(RESEARCH_BLOCK)

        code, output = self.run_gate("status")

        self.assertEqual(code, 0)
        self.assertIn("NOT_READY next=research stage=research", output)

    def test_research_begin_and_complete_unlocks_deep_dive(self) -> None:
        self.complete_research()

        code, output = self.run_gate("status")

        self.assertEqual(code, 0)
        self.assertIn("NOT_READY next=deep-dive stage=deep-dive-pass-1", output)

    def test_deep_dive_passes_need_separate_receipts(self) -> None:
        self.complete_research()
        self.complete_deep_dive_pass_1()

        code, output = self.run_gate("ready")

        self.assertEqual(code, 1)
        self.assertIn("NOT_READY next=deep-dive stage=deep-dive-pass-2", output)

    def test_ready_fails_until_all_receipts_exist(self) -> None:
        self.complete_research()
        self.complete_deep_dive_pass_1()
        self.complete_deep_dive_pass_2()
        self.complete_phase_plan()

        code, output = self.run_gate("ready")

        self.assertEqual(code, 1)
        self.assertIn("NOT_READY next=consistency-pass", output)

    def test_ready_fails_if_consistency_pass_later_says_no(self) -> None:
        self.complete_all_stages()
        self.replace_doc(
            "- Decision: proceed to implement? yes",
            "- Decision: proceed to implement? no",
        )

        code, output = self.run_gate("ready")

        self.assertEqual(code, 1)
        self.assertIn("consistency-pass_does_not_approve_implementation", output)

    def test_ready_passes_with_all_receipts_and_approved_consistency_pass(self) -> None:
        self.complete_all_stages()

        code, output = self.run_gate("ready")

        self.assertEqual(code, 0)
        self.assertEqual(output, "READY next=implement-loop")

    def test_stage_must_change_doc_after_begin(self) -> None:
        code, _ = self.run_gate("begin", "--stage", "research")
        self.assertEqual(code, 0)

        code, output = self.run_gate("complete", "--stage", "research")

        self.assertEqual(code, 2)
        self.assertIn("stage_did_not_change_DOC_PATH_after_begin", output)


if __name__ == "__main__":
    unittest.main()
