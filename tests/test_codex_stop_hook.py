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


if __name__ == "__main__":
    unittest.main()
