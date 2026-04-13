import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UPSERT_HOOK_PATH = REPO_ROOT / "skills/arch-step/scripts/upsert_codex_stop_hook.py"
STOP_HOOK_PATH = REPO_ROOT / "skills/arch-step/scripts/arch_controller_stop_hook.py"


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class CodexStopHookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.upsert_module = load_module(UPSERT_HOOK_PATH, "arch_skill_upsert_codex_stop_hook")
        cls.stop_module = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")

    def write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def controller_state_path(
        self,
        repo_root: Path,
        relative_path: Path,
        session_id: str | None = None,
    ) -> Path:
        if session_id is None:
            return repo_root / relative_path
        return repo_root / self.stop_module.session_state_relative_path(relative_path, session_id)

    def run_stop_hook(self, repo_root: Path, session_id: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(STOP_HOOK_PATH)],
            input=json.dumps({"cwd": str(repo_root), "session_id": session_id}),
            capture_output=True,
            text=True,
            check=False,
        )

    def run_arch_docs_auto_handler(
        self,
        repo_root: Path,
        session_id: str,
        evaluator_payload: dict,
    ) -> tuple[int, dict, str, Path]:
        state_path = self.controller_state_path(
            repo_root,
            self.stop_module.ARCH_DOCS_AUTO_STATE_RELATIVE_PATH,
            session_id,
        )
        self.write_json(
            state_path,
            {
                "command": "arch-docs-auto",
                "session_id": session_id,
                "scope_kind": "repo",
                "scope_summary": "repo docs surface",
                "pass_index": 0,
                "stop_condition": "clean docs scope",
                "ledger_path": ".doc-audit-ledger.md",
            },
        )
        evaluator_result = self.stop_module.FreshStructuredResult(
            process=subprocess.CompletedProcess(args=["codex"], returncode=0, stdout="", stderr=""),
            last_message=json.dumps(evaluator_payload),
            payload=evaluator_payload,
        )
        original = self.stop_module.run_arch_docs_evaluator
        stdout = io.StringIO()
        stderr = io.StringIO()
        self.stop_module.run_arch_docs_evaluator = lambda *args, **kwargs: evaluator_result
        try:
            saved_stdout = sys.stdout
            saved_stderr = sys.stderr
            sys.stdout = stdout
            sys.stderr = stderr
            with self.assertRaises(SystemExit) as raised:
                self.stop_module.handle_arch_docs_auto(
                    {"cwd": str(repo_root), "session_id": session_id}
                )
        finally:
            self.stop_module.run_arch_docs_evaluator = original
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr
        return raised.exception.code, json.loads(stdout.getvalue()), stderr.getvalue(), state_path

    def run_audit_loop_sim_handler(
        self,
        repo_root: Path,
        session_id: str,
        *,
        controller_fields: dict[str, str],
        review_summary: str | None = None,
        gitignore_text: str | None = None,
        gitignore_created: bool = False,
    ) -> tuple[int, dict, str, Path, Path]:
        state_path = self.controller_state_path(
            repo_root,
            self.stop_module.AUDIT_LOOP_SIM_STATE_RELATIVE_PATH,
            session_id,
        )
        ledger_path = repo_root / "_audit_sim_ledger.md"
        controller_block = "\n".join(
            [
                "<!-- audit_loop_sim:block:controller:start -->",
                f"Verdict: {controller_fields.get('Verdict', '')}",
                f"Next Area: {controller_fields.get('Next Area', '')}",
                f"Stop Reason: {controller_fields.get('Stop Reason', '')}",
                f"Last Review: {controller_fields.get('Last Review', '')}",
                "<!-- audit_loop_sim:block:controller:end -->",
            ]
        )
        ledger_path.write_text(
            "# Audit Sim Ledger\n"
            "Started: 2026-04-11\n"
            "Last updated: 2026-04-11\n\n"
            f"{controller_block}\n",
            encoding="utf-8",
        )
        self.write_json(
            state_path,
            {
                "command": "auto",
                "session_id": session_id,
                "ledger_path": "_audit_sim_ledger.md",
                "gitignore_created": gitignore_created,
                "gitignore_entry_added": True,
            },
        )
        if gitignore_text is not None:
            (repo_root / ".gitignore").write_text(gitignore_text, encoding="utf-8")

        review_result = self.stop_module.FreshAuditResult(
            process=subprocess.CompletedProcess(args=["codex"], returncode=0, stdout="", stderr=""),
            last_message=review_summary,
        )
        original = self.stop_module.run_fresh_sim_review
        stdout = io.StringIO()
        stderr = io.StringIO()
        self.stop_module.run_fresh_sim_review = lambda *args, **kwargs: review_result
        try:
            saved_stdout = sys.stdout
            saved_stderr = sys.stderr
            sys.stdout = stdout
            sys.stderr = stderr
            with self.assertRaises(SystemExit) as raised:
                self.stop_module.handle_audit_loop_sim(
                    {"cwd": str(repo_root), "session_id": session_id}
                )
        finally:
            self.stop_module.run_fresh_sim_review = original
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr
        return (
            raised.exception.code,
            json.loads(stdout.getvalue()),
            stderr.getvalue(),
            state_path,
            ledger_path,
        )

    def structured_result(
        self,
        payload: dict | None,
        *,
        returncode: int = 0,
        last_message: str | None = None,
    ):
        if last_message is None and payload is not None:
            last_message = json.dumps(payload)
        return self.stop_module.FreshStructuredResult(
            process=subprocess.CompletedProcess(
                args=["codex"],
                returncode=returncode,
                stdout="",
                stderr="",
            ),
            last_message=last_message,
            payload=payload,
        )

    def run_delay_poll_handler(
        self,
        repo_root: Path,
        session_id: str,
        *,
        state_payload: dict,
        check_results: list,
        start_time: int,
    ) -> tuple[int, dict, str, Path, list[int], int]:
        state_path = self.controller_state_path(
            repo_root,
            self.stop_module.DELAY_POLL_STATE_RELATIVE_PATH,
            session_id,
        )
        self.write_json(state_path, state_payload)

        result_iter = iter(check_results)
        sleeps: list[int] = []
        fake_now = {"value": start_time}

        def fake_run_delay_poll_check(*args, **kwargs):
            result = next(result_iter)
            if isinstance(result, Exception):
                raise result
            return result

        def fake_time():
            return fake_now["value"]

        def fake_sleep(seconds: int):
            sleeps.append(seconds)
            fake_now["value"] += seconds

        original_run = self.stop_module.run_delay_poll_check
        original_time = self.stop_module.current_epoch_seconds
        original_sleep = self.stop_module.sleep_for_seconds
        stdout = io.StringIO()
        stderr = io.StringIO()
        self.stop_module.run_delay_poll_check = fake_run_delay_poll_check
        self.stop_module.current_epoch_seconds = fake_time
        self.stop_module.sleep_for_seconds = fake_sleep
        try:
            saved_stdout = sys.stdout
            saved_stderr = sys.stderr
            sys.stdout = stdout
            sys.stderr = stderr
            with self.assertRaises(SystemExit) as raised:
                self.stop_module.handle_delay_poll(
                    {"cwd": str(repo_root), "session_id": session_id}
                )
        finally:
            self.stop_module.run_delay_poll_check = original_run
            self.stop_module.current_epoch_seconds = original_time
            self.stop_module.sleep_for_seconds = original_sleep
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr
        return (
            raised.exception.code,
            json.loads(stdout.getvalue()),
            stderr.getvalue(),
            state_path,
            sleeps,
            fake_now["value"],
        )

    def test_install_hook_preserves_unrelated_and_collapses_repo_managed_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            hooks_file = temp_root / "hooks.json"
            skills_dir = temp_root / "installed-skills"
            hooks_file.write_text(
                json.dumps(
                    {
                        "hooks": {
                            "Stop": [
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/third-party-hook.py",
                                            "timeoutSec": 30,
                                            "statusMessage": "third-party hook",
                                        }
                                    ]
                                },
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/implement_loop_stop_hook.py",
                                            "timeoutSec": 1200,
                                            "statusMessage": (
                                                "arch-step automatic controller is running; planning continuations "
                                                "are quick, fresh implement-loop audits can take a few minutes"
                                            ),
                                        }
                                    ]
                                },
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/audit_loop_stop_hook.py",
                                            "timeoutSec": 1200,
                                            "statusMessage": (
                                                "audit-loop automatic controller is running; fresh review passes "
                                                "can take a few minutes"
                                            ),
                                        }
                                    ]
                                },
                            ]
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            self.upsert_module.install_hook(hooks_file, skills_dir)
            written = json.loads(hooks_file.read_text(encoding="utf-8"))
            stop_groups = written["hooks"]["Stop"]

            self.assertEqual(len(stop_groups), 2)
            self.assertEqual(
                stop_groups[0]["hooks"][0]["command"],
                "python3 /tmp/third-party-hook.py",
            )

            managed_groups = self.upsert_module.repo_managed_groups(stop_groups)
            self.assertEqual(len(managed_groups), 1)
            self.assertEqual(
                managed_groups[0],
                self.upsert_module.expected_group(self.upsert_module.expected_command(skills_dir)),
            )

            self.upsert_module.verify_hook(hooks_file, skills_dir)

    def test_verify_hook_fails_when_multiple_repo_managed_entries_remain(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            hooks_file = temp_root / "hooks.json"
            skills_dir = temp_root / "installed-skills"
            expected_group = self.upsert_module.expected_group(
                self.upsert_module.expected_command(skills_dir)
            )
            hooks_file.write_text(
                json.dumps(
                    {
                        "hooks": {
                            "Stop": [
                                expected_group,
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/audit_loop_stop_hook.py",
                                            "timeoutSec": 1200,
                                            "statusMessage": (
                                                "audit-loop automatic controller is running; fresh review passes "
                                                "can take a few minutes"
                                            ),
                                        }
                                    ]
                                },
                            ]
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(SystemExit) as raised:
                self.upsert_module.verify_hook(hooks_file, skills_dir)
            self.assertIn("expected exactly one arch_skill-managed Stop hook entry", str(raised.exception))

    def test_verify_hook_fails_when_repo_managed_timeout_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            hooks_file = temp_root / "hooks.json"
            skills_dir = temp_root / "installed-skills"
            expected_group = self.upsert_module.expected_group(
                self.upsert_module.expected_command(skills_dir)
            )
            stale_group = json.loads(json.dumps(expected_group))
            stale_group["hooks"][0]["timeoutSec"] = 1200
            hooks_file.write_text(
                json.dumps({"hooks": {"Stop": [stale_group]}}, indent=2) + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(SystemExit) as raised:
                self.upsert_module.verify_hook(hooks_file, skills_dir)
            self.assertIn("stale arch_skill Stop hook entry still exists", str(raised.exception))

    def test_stop_hook_blocks_when_same_session_has_multiple_controller_states(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.IMPLEMENT_LOOP_STATE_RELATIVE_PATH,
                    "session-1",
                ),
                {
                    "command": "implement-loop",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN.md",
                },
            )
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.AUDIT_LOOP_STATE_RELATIVE_PATH,
                    "session-1",
                ),
                {
                    "command": "auto",
                    "session_id": "session-1",
                    "ledger_path": "_audit_ledger.md",
                },
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn(".codex/implement-loop-state.session-1.json", payload["stopReason"])
            self.assertIn(".codex/audit-loop-state.session-1.json", payload["stopReason"])

    def test_stop_hook_blocks_when_same_session_has_audit_loop_sim_and_other_controller_states(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                    "session-1",
                ),
                {
                    "command": "auto-plan",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN.md",
                    "stage_index": 0,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.AUDIT_LOOP_SIM_STATE_RELATIVE_PATH,
                    "session-1",
                ),
                {
                    "command": "auto",
                    "session_id": "session-1",
                    "ledger_path": "_audit_sim_ledger.md",
                },
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn(".codex/auto-plan-state.session-1.json", payload["stopReason"])
            self.assertIn(".codex/audit-loop-sim-state.session-1.json", payload["stopReason"])

    def test_stop_hook_ignores_other_session_controller_states(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.ARCH_DOCS_AUTO_STATE_RELATIVE_PATH,
                    "session-2",
                ),
                {
                    "command": "arch-docs-auto",
                    "session_id": "session-2",
                    "scope_kind": "repo",
                    "scope_summary": "repo docs surface",
                    "pass_index": 0,
                    "stop_condition": "clean docs scope",
                    "ledger_path": ".doc-audit-ledger.md",
                },
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            self.assertEqual(process.stdout, "")
            self.assertEqual(process.stderr, "")

    def test_stop_hook_ignores_delay_poll_state_from_other_session(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.DELAY_POLL_STATE_RELATIVE_PATH,
                    "session-2",
                ),
                {
                    "version": 1,
                    "command": "delay-poll",
                    "session_id": "session-2",
                    "interval_seconds": 1800,
                    "armed_at": 100,
                    "deadline_at": 1000,
                    "check_prompt": "See whether branch blah is pushed.",
                    "resume_prompt": "Pull it and integrate it in.",
                    "attempt_count": 0,
                    "last_check_at": None,
                    "last_summary": "",
                },
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            self.assertEqual(process.stdout, "")
            self.assertEqual(process.stderr, "")

    def test_stop_hook_blocks_when_delay_poll_and_other_controller_states_share_session(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.DELAY_POLL_STATE_RELATIVE_PATH,
                    "session-1",
                ),
                {
                    "version": 1,
                    "command": "delay-poll",
                    "session_id": "session-1",
                    "interval_seconds": 1800,
                    "armed_at": 100,
                    "deadline_at": 1000,
                    "check_prompt": "See whether branch blah is pushed.",
                    "resume_prompt": "Pull it and integrate it in.",
                    "attempt_count": 0,
                    "last_check_at": None,
                    "last_summary": "",
                },
            )
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                    "session-1",
                ),
                {
                    "command": "auto-plan",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN.md",
                    "stage_index": 0,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn(".codex/delay-poll-state.session-1.json", payload["stopReason"])
            self.assertIn(".codex/auto-plan-state.session-1.json", payload["stopReason"])

    def test_stop_hook_uses_only_matching_same_mode_session_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            (docs_dir / "PLAN1.md").write_text("Research placeholder\n", encoding="utf-8")
            (docs_dir / "PLAN2.md").write_text("Research placeholder\n", encoding="utf-8")
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                    "session-1",
                ),
                {
                    "command": "auto-plan",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN1.md",
                    "stage_index": 0,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )
            session_two_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-2",
            )
            self.write_json(
                session_two_path,
                {
                    "command": "auto-plan",
                    "session_id": "session-2",
                    "doc_path": "docs/PLAN2.md",
                    "stage_index": 0,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn("docs/PLAN1.md", payload["stopReason"])
            self.assertNotIn("docs/PLAN2.md", payload["stopReason"])
            self.assertTrue(session_two_path.exists())

    def test_stop_hook_blocks_when_session_scoped_and_legacy_state_both_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                    "session-1",
                ),
                {
                    "command": "auto-plan",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN.md",
                    "stage_index": 0,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                ),
                {
                    "command": "auto-plan",
                    "doc_path": "docs/PLAN.md",
                    "stage_index": 0,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn(".codex/auto-plan-state.session-1.json", payload["stopReason"])
            self.assertIn(".codex/auto-plan-state.json", payload["stopReason"])

    def test_stop_hook_legacy_state_still_works(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            state_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
            )
            self.write_json(
                state_path,
                {
                    "command": "auto-plan",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN.md",
                    "stage_index": 0,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )
            time.sleep(0.01)
            (docs_dir / "PLAN.md").write_text(
                "<!-- arch_skill:block:research_grounding:start -->\n",
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["continue"])
            self.assertIn("docs/PLAN.md", payload["reason"])
            self.assertIn(".codex/auto-plan-state.json", payload["reason"])

            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["session_id"], "session-1")
            self.assertEqual(state["stage_index"], 1)

    def test_stop_hook_advances_auto_plan_from_phase_plan_to_consistency_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            state_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-1",
            )
            self.write_json(
                state_path,
                {
                    "command": "auto-plan",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN.md",
                    "stage_index": 3,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )
            time.sleep(0.01)
            (docs_dir / "PLAN.md").write_text(
                "<!-- arch_skill:block:phase_plan:start -->\n",
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["continue"])
            self.assertIn("Use $arch-step consistency-pass docs/PLAN.md", payload["reason"])
            self.assertEqual(
                payload["systemMessage"],
                "auto-plan finished phase-plan; continuing to consistency-pass.",
            )

            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["stage_index"], 4)

    def test_stop_hook_completes_auto_plan_after_consistency_pass_yes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            state_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-1",
            )
            self.write_json(
                state_path,
                {
                    "command": "auto-plan",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN.md",
                    "stage_index": 4,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )
            time.sleep(0.01)
            (docs_dir / "PLAN.md").write_text(
                "\n".join(
                    [
                        "<!-- arch_skill:block:consistency_pass:start -->",
                        "## Consistency Pass",
                        "- Reviewers: explorer 1, explorer 2, self-integrator",
                        "- Scope checked:",
                        "  - full artifact",
                        "- Findings summary:",
                        "  - none",
                        "- Integrated repairs:",
                        "  - none",
                        "- Remaining inconsistencies:",
                        "  - none",
                        "- Decision: proceed to implement? yes",
                        "<!-- arch_skill:block:consistency_pass:end -->",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn("consistency-pass are in place", payload["stopReason"])
            self.assertIn("Use $arch-step implement-loop docs/PLAN.md", payload["stopReason"])
            self.assertEqual(
                payload["systemMessage"],
                "auto-plan completed; the doc is ready for implement-loop.",
            )
            self.assertFalse(state_path.exists())

    def test_stop_hook_disarms_auto_plan_when_consistency_pass_block_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            state_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-1",
            )
            self.write_json(
                state_path,
                {
                    "command": "auto-plan",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN.md",
                    "stage_index": 4,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )
            time.sleep(0.01)
            (docs_dir / "PLAN.md").write_text(
                "# Plan\nConsistency pass did not write its helper block.\n",
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn("stopped before consistency-pass completed", payload["stopReason"])
            self.assertEqual(
                payload["systemMessage"],
                "auto-plan stopped before consistency-pass completed.",
            )
            self.assertFalse(state_path.exists())

    def test_stop_hook_disarms_auto_plan_when_consistency_pass_says_no(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            state_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-1",
            )
            self.write_json(
                state_path,
                {
                    "command": "auto-plan",
                    "session_id": "session-1",
                    "doc_path": "docs/PLAN.md",
                    "stage_index": 4,
                    "stages": list(self.stop_module.AUTO_PLAN_STAGES),
                },
            )
            time.sleep(0.01)
            (docs_dir / "PLAN.md").write_text(
                "\n".join(
                    [
                        "<!-- arch_skill:block:consistency_pass:start -->",
                        "## Consistency Pass",
                        "- Reviewers: explorer 1, explorer 2, self-integrator",
                        "- Scope checked:",
                        "  - full artifact",
                        "- Findings summary:",
                        "  - owner path and phase sequencing still disagree",
                        "- Integrated repairs:",
                        "  - tightened section 7 wording",
                        "- Remaining inconsistencies:",
                        "  - section 5 and section 6 still disagree",
                        "- Decision: proceed to implement? no",
                        "<!-- arch_skill:block:consistency_pass:end -->",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn("does not currently approve implementation", payload["stopReason"])
            self.assertEqual(
                payload["systemMessage"],
                "auto-plan consistency-pass did not approve implementation.",
            )
            self.assertFalse(state_path.exists())

    def test_arch_docs_auto_continue_uses_grounded_repo_wide_wording(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path = self.run_arch_docs_auto_handler(
                repo_root,
                "session-1",
                {
                    "verdict": "continue",
                    "summary": "More stale setup and usage docs remain elsewhere in the repo docs surface.",
                    "next_action": "Use $arch-docs",
                    "needs_another_pass": True,
                    "reason": "Grounded cleanup remains.",
                    "blockers": [],
                },
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertIn("more grounded docs cleanup", payload["reason"])
            self.assertNotIn("more bounded docs cleanup", payload["reason"])
            self.assertNotIn("Current scope remains", payload["reason"])
            self.assertEqual(
                payload["systemMessage"],
                "arch-docs auto evaluation finished; another grounded pass remains.",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["pass_index"], 1)

    def test_arch_docs_auto_blocked_uses_grounded_blocker_wording(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path = self.run_arch_docs_auto_handler(
                repo_root,
                "session-1",
                {
                    "verdict": "blocked",
                    "summary": "The remaining work would be speculative taxonomy cleanup with no grounded canonical home.",
                    "next_action": "Stop and explain the blocker.",
                    "needs_another_pass": False,
                    "reason": "No credible grounded next pass remains.",
                    "blockers": ["speculative taxonomy cleanup"],
                },
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertIn("no credible grounded next pass", payload["reason"])
            self.assertNotIn("bounded", payload["reason"])
            self.assertEqual(
                payload["systemMessage"],
                "arch-docs auto evaluation stopped: no credible grounded next pass.",
            )
            self.assertFalse(state_path.exists())

    def test_audit_loop_sim_continue_keeps_state_armed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path, ledger_path = self.run_audit_loop_sim_handler(
                repo_root,
                "session-1",
                controller_fields={
                    "Verdict": "CONTINUE",
                    "Next Area": "new-user auth plus session restore risk front",
                    "Stop Reason": "",
                    "Last Review": "2026-04-11",
                },
                review_summary="The same auth journey still lacks durable Android closeout.",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertIn("more worthwhile automation work", payload["reason"])
            self.assertIn("Use $audit-loop-sim", payload["reason"])
            self.assertIn("new-user auth plus session restore risk front", payload["reason"])
            self.assertEqual(payload["systemMessage"], "audit-loop-sim review found more work.")
            self.assertTrue(state_path.exists())
            self.assertTrue(ledger_path.exists())

    def test_audit_loop_sim_clean_removes_runtime_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path, ledger_path = self.run_audit_loop_sim_handler(
                repo_root,
                "session-1",
                controller_fields={
                    "Verdict": "CLEAN",
                    "Next Area": "",
                    "Stop Reason": "",
                    "Last Review": "2026-04-11",
                },
                review_summary="No credible major automation risk remains.",
                gitignore_text="_audit_sim_ledger.md\n",
                gitignore_created=True,
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertFalse(payload["continue"])
            self.assertIn("fresh review finished clean", payload["stopReason"])
            self.assertEqual(payload["systemMessage"], "audit-loop-sim completed clean.")
            self.assertFalse(state_path.exists())
            self.assertFalse(ledger_path.exists())
            self.assertFalse((repo_root / ".gitignore").exists())

    def test_audit_loop_sim_blocked_disarms_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path, ledger_path = self.run_audit_loop_sim_handler(
                repo_root,
                "session-1",
                controller_fields={
                    "Verdict": "BLOCKED",
                    "Next Area": "",
                    "Stop Reason": "Backend realism is unavailable on this host.",
                    "Last Review": "2026-04-11",
                },
                review_summary="The repo-managed backend runner is unavailable.",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertFalse(payload["continue"])
            self.assertIn("Backend realism is unavailable on this host.", payload["stopReason"])
            self.assertEqual(payload["systemMessage"], "audit-loop-sim stopped blocked.")
            self.assertFalse(state_path.exists())
            self.assertTrue(ledger_path.exists())

    def test_audit_loop_sim_continue_without_next_area_disarms_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path, ledger_path = self.run_audit_loop_sim_handler(
                repo_root,
                "session-1",
                controller_fields={
                    "Verdict": "CONTINUE",
                    "Next Area": "",
                    "Stop Reason": "",
                    "Last Review": "2026-04-11",
                },
                review_summary="The review forgot to name the next automation front.",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertFalse(payload["continue"])
            self.assertIn("CONTINUE without Next Area", payload["stopReason"])
            self.assertEqual(payload["systemMessage"], "audit-loop-sim review omitted Next Area.")
            self.assertFalse(state_path.exists())
            self.assertTrue(ledger_path.exists())

    def test_delay_poll_ready_immediately_clears_state_and_continues(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            exit_code, payload, stderr, state_path, sleeps, final_time = self.run_delay_poll_handler(
                repo_root,
                "session-1",
                state_payload={
                    "version": 1,
                    "command": "delay-poll",
                    "session_id": "session-1",
                    "interval_seconds": 1800,
                    "armed_at": 100,
                    "deadline_at": 1000,
                    "check_prompt": "Check whether branch blah has been fully pushed yet.",
                    "resume_prompt": "Pull branch blah and integrate it in.",
                    "attempt_count": 0,
                    "last_check_at": None,
                    "last_summary": "",
                },
                check_results=[
                    self.structured_result(
                        {
                            "ready": True,
                            "summary": "Remote now shows the expected branch tip.",
                            "evidence": ["origin/blah points at abc123"],
                        }
                    )
                ],
                start_time=100,
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertEqual(
                payload["systemMessage"],
                "delay-poll condition is now true; continuing the task.",
            )
            self.assertIn("Pull branch blah and integrate it in.", payload["reason"])
            self.assertIn("Remote now shows the expected branch tip.", payload["reason"])
            self.assertFalse(state_path.exists())
            self.assertEqual(sleeps, [])
            self.assertEqual(final_time, 100)

    def test_delay_poll_repeats_until_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            exit_code, payload, stderr, state_path, sleeps, final_time = self.run_delay_poll_handler(
                repo_root,
                "session-1",
                state_payload={
                    "version": 1,
                    "command": "delay-poll",
                    "session_id": "session-1",
                    "interval_seconds": 1800,
                    "armed_at": 100,
                    "deadline_at": 5000,
                    "check_prompt": "Check whether branch blah has been fully pushed yet.",
                    "resume_prompt": "Pull branch blah and integrate it in.",
                    "attempt_count": 0,
                    "last_check_at": None,
                    "last_summary": "",
                },
                check_results=[
                    self.structured_result(
                        {
                            "ready": False,
                            "summary": "Remote still does not show the expected pushed commit.",
                            "evidence": ["origin/blah still points at the old commit"],
                        }
                    ),
                    self.structured_result(
                        {
                            "ready": True,
                            "summary": "Remote now shows the expected pushed commit.",
                            "evidence": ["origin/blah now points at abc123"],
                        }
                    ),
                ],
                start_time=100,
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertEqual(
                payload["systemMessage"],
                "delay-poll condition is now true; continuing the task.",
            )
            self.assertIn("Remote now shows the expected pushed commit.", payload["reason"])
            self.assertEqual(sleeps, [1800])
            self.assertEqual(final_time, 1900)
            self.assertFalse(state_path.exists())

    def test_delay_poll_times_out_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            exit_code, payload, stderr, state_path, sleeps, final_time = self.run_delay_poll_handler(
                repo_root,
                "session-1",
                state_payload={
                    "version": 1,
                    "command": "delay-poll",
                    "session_id": "session-1",
                    "interval_seconds": 1800,
                    "armed_at": 100,
                    "deadline_at": 2000,
                    "check_prompt": "Check whether branch blah has been fully pushed yet.",
                    "resume_prompt": "Pull branch blah and integrate it in.",
                    "attempt_count": 0,
                    "last_check_at": None,
                    "last_summary": "",
                },
                check_results=[
                    self.structured_result(
                        {
                            "ready": False,
                            "summary": "Remote still does not show the expected pushed commit.",
                            "evidence": ["origin/blah still points at the old commit"],
                        }
                    ),
                    self.structured_result(
                        {
                            "ready": False,
                            "summary": "Remote still does not show the expected pushed commit after another poll.",
                            "evidence": ["origin/blah still points at the old commit"],
                        }
                    ),
                ],
                start_time=100,
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertFalse(payload["continue"])
            self.assertEqual(payload["systemMessage"], "delay-poll timed out without success.")
            self.assertIn("timed out before the waited-on condition became true", payload["stopReason"])
            self.assertIn("Remote still does not show the expected pushed commit after another poll.", payload["stopReason"])
            self.assertEqual(sleeps, [1800, 100])
            self.assertEqual(final_time, 2000)
            self.assertFalse(state_path.exists())

    def test_delay_poll_stops_when_checker_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            exit_code, payload, stderr, state_path, sleeps, final_time = self.run_delay_poll_handler(
                repo_root,
                "session-1",
                state_payload={
                    "version": 1,
                    "command": "delay-poll",
                    "session_id": "session-1",
                    "interval_seconds": 1800,
                    "armed_at": 100,
                    "deadline_at": 1000,
                    "check_prompt": "Check whether branch blah has been fully pushed yet.",
                    "resume_prompt": "Pull branch blah and integrate it in.",
                    "attempt_count": 0,
                    "last_check_at": None,
                    "last_summary": "",
                },
                check_results=[
                    self.structured_result(
                        {
                            "ready": False,
                            "summary": "network blocked",
                            "evidence": ["proxy denied the request"],
                        },
                        returncode=1,
                        last_message="network blocked",
                    )
                ],
                start_time=100,
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertFalse(payload["continue"])
            self.assertEqual(payload["systemMessage"], "delay-poll fresh check failed.")
            self.assertIn("delay-poll ran a fresh check, but that check failed.", payload["stopReason"])
            self.assertFalse(state_path.exists())
            self.assertEqual(sleeps, [])
            self.assertEqual(final_time, 100)

    def test_delay_poll_stops_when_checker_output_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            exit_code, payload, stderr, state_path, sleeps, final_time = self.run_delay_poll_handler(
                repo_root,
                "session-1",
                state_payload={
                    "version": 1,
                    "command": "delay-poll",
                    "session_id": "session-1",
                    "interval_seconds": 1800,
                    "armed_at": 100,
                    "deadline_at": 1000,
                    "check_prompt": "Check whether branch blah has been fully pushed yet.",
                    "resume_prompt": "Pull branch blah and integrate it in.",
                    "attempt_count": 0,
                    "last_check_at": None,
                    "last_summary": "",
                },
                check_results=[
                    self.structured_result(
                        None,
                        last_message="not json",
                    )
                ],
                start_time=100,
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertFalse(payload["continue"])
            self.assertEqual(
                payload["systemMessage"],
                "delay-poll fresh check returned unusable output.",
            )
            self.assertIn("did not return usable structured JSON", payload["stopReason"])
            self.assertFalse(state_path.exists())
            self.assertEqual(sleeps, [])
            self.assertEqual(final_time, 100)


if __name__ == "__main__":
    unittest.main()
