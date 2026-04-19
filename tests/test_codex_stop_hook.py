import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UPSERT_HOOK_PATH = REPO_ROOT / "skills/arch-step/scripts/upsert_codex_stop_hook.py"
STOP_HOOK_PATH = REPO_ROOT / "skills/arch-step/scripts/arch_controller_stop_hook.py"
CODE_REVIEW_RUNNER_PATH = REPO_ROOT / "skills/code-review/scripts/run_code_review.py"
HOOK_CONTRACT_TEXT_PATHS = [
    Path("README.md"),
    Path("docs/arch_skill_usage_guide.md"),
    Path("skills/arch-step/SKILL.md"),
    Path("skills/arch-step/agents/openai.yaml"),
    Path("skills/arch-step/references/arch-auto-plan.md"),
    Path("skills/arch-step/references/arch-implement-loop.md"),
    Path("skills/audit-loop/SKILL.md"),
    Path("skills/audit-loop/agents/openai.yaml"),
    Path("skills/audit-loop/references/auto.md"),
    Path("skills/comment-loop/SKILL.md"),
    Path("skills/comment-loop/agents/openai.yaml"),
    Path("skills/comment-loop/references/auto.md"),
    Path("skills/audit-loop-sim/SKILL.md"),
    Path("skills/audit-loop-sim/agents/openai.yaml"),
    Path("skills/audit-loop-sim/references/auto.md"),
]
REQUIRED_HOOKS_FILE_TEXT = "~/.codex/hooks.json"
REQUIRED_RUNNER_PATH_TEXT = "~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py"
FORBIDDEN_HOOK_PATH_TEXTS = (
    "~/.codex/hooks/arch_controller_stop_hook.py",
    "/Users/example/.codex/hooks/arch_controller_stop_hook.py",
)
AUTO_PLAN_CLEANUP_CONTRACT_TEXT_PATHS = [
    Path("README.md"),
    Path("docs/arch_skill_usage_guide.md"),
    Path("skills/arch-step/SKILL.md"),
    Path("skills/arch-step/references/arch-auto-plan.md"),
    Path("skills/miniarch-step/SKILL.md"),
    Path("skills/miniarch-step/references/arch-auto-plan.md"),
]
FORBIDDEN_PARENT_CLEANUP_TEXTS = (
    "delete it before stopping",
    "clear the runtime-local controller state",
    "clear the runtime-local auto-plan state",
    "clear the armed auto-plan state",
    "clear the armed miniarch-step auto-plan state",
    "must stop, clear controller state",
)


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
        cls.code_review_module = load_module(
            CODE_REVIEW_RUNNER_PATH,
            "arch_skill_code_review_runner",
        )
        cls.stop_module.ACTIVE_RUNTIME = cls.stop_module.HOOK_RUNTIME_SPECS[
            cls.stop_module.RUNTIME_CODEX
        ]

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

    def auto_plan_state(
        self,
        *,
        session_id: str = "session-1",
        doc_path: str = "docs/PLAN.md",
        legacy_progress: bool = False,
        stage_index: int = 0,
    ) -> dict:
        state = {
            "command": "auto-plan",
            "session_id": session_id,
            "doc_path": doc_path,
        }
        if legacy_progress:
            state["stage_index"] = stage_index
            state["stages"] = list(self.stop_module.AUTO_PLAN_STAGES)
        return state

    def miniarch_step_auto_plan_state(
        self,
        *,
        session_id: str = "session-1",
        doc_path: str = "docs/PLAN.md",
    ) -> dict:
        return {
            "command": "miniarch-step-auto-plan",
            "session_id": session_id,
            "doc_path": doc_path,
        }

    def auto_plan_doc_text(
        self,
        *,
        research: bool = False,
        deep_dive_pass_1: bool = False,
        deep_dive_pass_2: bool = False,
        phase_plan: bool = False,
        consistency_decision: str | None = None,
    ) -> str:
        lines = ["# Plan"]
        if research:
            lines.append(self.stop_module.BLOCK_MARKERS["research_grounding"])
        if deep_dive_pass_1 or deep_dive_pass_2:
            lines.extend(
                [
                    self.stop_module.BLOCK_MARKERS["current_architecture"],
                    self.stop_module.BLOCK_MARKERS["target_architecture"],
                    self.stop_module.BLOCK_MARKERS["call_site_audit"],
                ]
            )
        if deep_dive_pass_1:
            lines.append("deep_dive_pass_1: done 2026-04-13")
        if deep_dive_pass_2:
            lines.append("deep_dive_pass_2: done 2026-04-13")
        if phase_plan:
            lines.append(self.stop_module.BLOCK_MARKERS["phase_plan"])
        if consistency_decision is not None:
            lines.extend(
                [
                    self.stop_module.BLOCK_MARKERS["consistency_pass"],
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
                    f"- Decision: proceed to implement? {consistency_decision}",
                    self.stop_module.BLOCK_MARKERS["consistency_pass"].replace(":start -->", ":end -->"),
                ]
            )
        return "\n".join(lines) + "\n"

    def run_stop_hook(self, repo_root: Path, session_id: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(STOP_HOOK_PATH), "--runtime", "codex"],
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

    def run_comment_loop_handler(
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
            self.stop_module.COMMENT_LOOP_STATE_RELATIVE_PATH,
            session_id,
        )
        ledger_path = repo_root / "_comment_ledger.md"
        controller_block = "\n".join(
            [
                "<!-- comment_loop:block:controller:start -->",
                f"Verdict: {controller_fields.get('Verdict', '')}",
                f"Next Area: {controller_fields.get('Next Area', '')}",
                f"Stop Reason: {controller_fields.get('Stop Reason', '')}",
                f"Last Review: {controller_fields.get('Last Review', '')}",
                "<!-- comment_loop:block:controller:end -->",
            ]
        )
        ledger_path.write_text(
            "# Comment Ledger\n"
            "Started: 2026-04-13\n"
            "Last updated: 2026-04-13\n\n"
            f"{controller_block}\n",
            encoding="utf-8",
        )
        self.write_json(
            state_path,
            {
                "command": "auto",
                "session_id": session_id,
                "ledger_path": "_comment_ledger.md",
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
        original = self.stop_module.run_fresh_comment_review
        stdout = io.StringIO()
        stderr = io.StringIO()
        self.stop_module.run_fresh_comment_review = lambda *args, **kwargs: review_result
        try:
            saved_stdout = sys.stdout
            saved_stderr = sys.stderr
            sys.stdout = stdout
            sys.stderr = stderr
            with self.assertRaises(SystemExit) as raised:
                self.stop_module.handle_comment_loop(
                    {"cwd": str(repo_root), "session_id": session_id}
                )
        finally:
            self.stop_module.run_fresh_comment_review = original
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr
        return (
            raised.exception.code,
            json.loads(stdout.getvalue()),
            stderr.getvalue(),
            state_path,
            ledger_path,
        )

    def run_implement_loop_handler(
        self,
        repo_root: Path,
        session_id: str,
        *,
        verdict: str,
        audit_summary: str | None = None,
    ) -> tuple[int, dict, str, Path, Path]:
        state_path = self.controller_state_path(
            repo_root,
            self.stop_module.IMPLEMENT_LOOP_STATE_RELATIVE_PATH,
            session_id,
        )
        docs_dir = repo_root / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        doc_path = docs_dir / "PLAN.md"
        doc_path.write_text(
            "# Plan\n"
            "## Implementation Audit\n"
            f"Verdict (code): {verdict}\n",
            encoding="utf-8",
        )
        self.write_json(
            state_path,
            {
                "command": "implement-loop",
                "session_id": session_id,
                "doc_path": "docs/PLAN.md",
            },
        )

        audit_result = self.stop_module.FreshAuditResult(
            process=subprocess.CompletedProcess(args=["codex"], returncode=0, stdout="", stderr=""),
            last_message=audit_summary,
        )
        original = self.stop_module.run_fresh_audit
        stdout = io.StringIO()
        stderr = io.StringIO()
        self.stop_module.run_fresh_audit = lambda *args, **kwargs: audit_result
        try:
            saved_stdout = sys.stdout
            saved_stderr = sys.stderr
            sys.stdout = stdout
            sys.stderr = stderr
            with self.assertRaises(SystemExit) as raised:
                self.stop_module.handle_implement_loop(
                    {"cwd": str(repo_root), "session_id": session_id}
                )
        finally:
            self.stop_module.run_fresh_audit = original
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr
        return (
            raised.exception.code,
            json.loads(stdout.getvalue()),
            stderr.getvalue(),
            state_path,
            doc_path,
        )

    def run_miniarch_step_implement_loop_handler(
        self,
        repo_root: Path,
        session_id: str,
        *,
        verdict: str,
        audit_summary: str | None = None,
    ) -> tuple[int, dict, str, Path, Path, tuple[tuple, dict]]:
        state_path = self.controller_state_path(
            repo_root,
            self.stop_module.MINIARCH_STEP_IMPLEMENT_LOOP_STATE_RELATIVE_PATH,
            session_id,
        )
        docs_dir = repo_root / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        doc_path = docs_dir / "PLAN.md"
        doc_path.write_text(
            "# Plan\n"
            "## Implementation Audit\n"
            f"Verdict (code): {verdict}\n",
            encoding="utf-8",
        )
        self.write_json(
            state_path,
            {
                "command": "miniarch-step-implement-loop",
                "session_id": session_id,
                "doc_path": "docs/PLAN.md",
            },
        )

        audit_result = self.stop_module.FreshAuditResult(
            process=subprocess.CompletedProcess(args=["codex"], returncode=0, stdout="", stderr=""),
            last_message=audit_summary,
        )
        calls: list[tuple[tuple, dict]] = []

        def fake_run_fresh_audit(*args, **kwargs):
            calls.append((args, kwargs))
            return audit_result

        original = self.stop_module.run_fresh_audit
        stdout = io.StringIO()
        stderr = io.StringIO()
        self.stop_module.run_fresh_audit = fake_run_fresh_audit
        try:
            saved_stdout = sys.stdout
            saved_stderr = sys.stderr
            sys.stdout = stdout
            sys.stderr = stderr
            with self.assertRaises(SystemExit) as raised:
                self.stop_module.handle_miniarch_step_implement_loop(
                    {"cwd": str(repo_root), "session_id": session_id}
                )
        finally:
            self.stop_module.run_fresh_audit = original
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr
        self.assertEqual(len(calls), 1)
        return (
            raised.exception.code,
            json.loads(stdout.getvalue()),
            stderr.getvalue(),
            state_path,
            doc_path,
            calls[0],
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

    def capture_codex_exec_args(self, callback) -> list[str]:
        recorded: dict[str, list[str]] = {}

        def fake_run(args, **kwargs):
            recorded["args"] = list(args)
            if "-o" in args:
                output_path = Path(args[args.index("-o") + 1])
                output_path.write_text("", encoding="utf-8")
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="", stderr="")

        original_which = self.stop_module.shutil.which
        original_run = self.stop_module.subprocess.run
        self.stop_module.shutil.which = lambda name: "/usr/bin/codex" if name == "codex" else None
        self.stop_module.subprocess.run = fake_run
        try:
            callback()
        finally:
            self.stop_module.shutil.which = original_which
            self.stop_module.subprocess.run = original_run

        return recorded["args"]

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

    def test_hook_contract_docs_anchor_preflight_to_hooks_json(self) -> None:
        for relative_path in HOOK_CONTRACT_TEXT_PATHS:
            with self.subTest(path=str(relative_path)):
                text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(REQUIRED_HOOKS_FILE_TEXT, text)
                self.assertIn(REQUIRED_RUNNER_PATH_TEXT, text)
                for forbidden_text in FORBIDDEN_HOOK_PATH_TEXTS:
                    self.assertNotIn(forbidden_text, text)

    def test_auto_plan_contracts_do_not_make_parent_delete_controller_state(self) -> None:
        for relative_path in AUTO_PLAN_CLEANUP_CONTRACT_TEXT_PATHS:
            with self.subTest(path=str(relative_path)):
                text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                for forbidden_text in FORBIDDEN_PARENT_CLEANUP_TEXTS:
                    self.assertNotIn(forbidden_text, text)

    def test_code_review_run_dirs_do_not_collide_for_same_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir)
            target = self.code_review_module.ReviewTarget(
                mode="paths",
                paths=["skills/arch-step/scripts/arch_controller_stop_hook.py"],
            )
            original_datetime = self.code_review_module._dt.datetime

            class FixedDateTime:
                @classmethod
                def now(cls):
                    return original_datetime(2026, 4, 19, 12, 0, 0)

            self.code_review_module._dt.datetime = FixedDateTime
            try:
                first = self.code_review_module.make_run_dir(output_root, None, target)
                second = self.code_review_module.make_run_dir(output_root, None, target)
            finally:
                self.code_review_module._dt.datetime = original_datetime

            self.assertNotEqual(first, second)
            self.assertTrue(first.exists())
            self.assertTrue(second.exists())

    def test_run_fresh_review_uses_unsandboxed_exec(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            args = self.capture_codex_exec_args(
                lambda: self.stop_module.run_fresh_review(Path(temp_dir))
            )

        self.assertIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("--full-auto", args)
        self.assertEqual(args[-1].splitlines()[0], "Use $audit-loop review")

    def test_run_fresh_comment_review_uses_unsandboxed_exec(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            args = self.capture_codex_exec_args(
                lambda: self.stop_module.run_fresh_comment_review(Path(temp_dir))
            )

        self.assertIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("--full-auto", args)
        self.assertEqual(args[-1].splitlines()[0], "Use $comment-loop review")

    def test_run_fresh_sim_review_uses_unsandboxed_exec(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            args = self.capture_codex_exec_args(
                lambda: self.stop_module.run_fresh_sim_review(Path(temp_dir))
            )

        self.assertIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("--full-auto", args)
        self.assertEqual(args[-1].splitlines()[0], "Use $audit-loop-sim review")

    def test_run_fresh_audit_default_does_not_pin_model(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            args = self.capture_codex_exec_args(
                lambda: self.stop_module.run_fresh_audit(Path(temp_dir), "docs/PLAN.md")
            )

        self.assertIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("--model", args)
        self.assertNotIn('model_reasoning_effort="xhigh"', args)
        self.assertEqual(args[-1].splitlines()[0], "Use $arch-step audit-implementation docs/PLAN.md")

    def test_run_fresh_audit_can_pin_miniarch_model_and_effort(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            args = self.capture_codex_exec_args(
                lambda: self.stop_module.run_fresh_audit(
                    Path(temp_dir),
                    "docs/PLAN.md",
                    skill_name="miniarch-step",
                    temp_prefix="miniarch-step-implement-loop-",
                    model=self.stop_module.MINIARCH_STEP_AUDIT_MODEL,
                    model_reasoning_effort=(
                        self.stop_module.MINIARCH_STEP_AUDIT_MODEL_REASONING_EFFORT
                    ),
                )
            )

        self.assertIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertIn("--model", args)
        self.assertEqual(
            args[args.index("--model") + 1],
            self.stop_module.MINIARCH_STEP_AUDIT_MODEL,
        )
        self.assertIn("-c", args)
        self.assertIn(
            'model_reasoning_effort="xhigh"',
            args,
        )
        self.assertEqual(
            args[-1].splitlines()[0],
            "Use $miniarch-step audit-implementation docs/PLAN.md",
        )

    def test_run_arch_docs_evaluator_stays_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            args = self.capture_codex_exec_args(
                lambda: self.stop_module.run_arch_docs_evaluator(
                    repo_root,
                    "repo docs surface",
                    repo_root / ".codex/arch-docs-auto-state.session-1.json",
                    ".doc-audit-ledger.md",
                )
            )

        self.assertIn("--sandbox", args)
        self.assertEqual(args[args.index("--sandbox") + 1], "read-only")
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertEqual(args[-1].splitlines()[0], "Use $arch-docs for the suite's INTERNAL AUTO EVALUATOR.")

    def test_run_delay_poll_check_stays_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            args = self.capture_codex_exec_args(
                lambda: self.stop_module.run_delay_poll_check(
                    repo_root,
                    "See whether the waited-on condition is satisfied yet.",
                )
            )

        self.assertIn("--sandbox", args)
        self.assertEqual(args[args.index("--sandbox") + 1], "read-only")
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertEqual(args[-1].splitlines()[0], "Use $delay-poll check")

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
                self.auto_plan_state(),
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

    def test_stop_hook_blocks_when_same_session_has_comment_loop_and_other_controller_states(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.COMMENT_LOOP_STATE_RELATIVE_PATH,
                    "session-1",
                ),
                {
                    "command": "auto",
                    "session_id": "session-1",
                    "ledger_path": "_comment_ledger.md",
                },
            )
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

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn(".codex/comment-loop-state.session-1.json", payload["stopReason"])
            self.assertIn(".codex/implement-loop-state.session-1.json", payload["stopReason"])

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
                self.auto_plan_state(),
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
                self.auto_plan_state(doc_path="docs/PLAN1.md"),
            )
            session_two_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-2",
            )
            self.write_json(
                session_two_path,
                self.auto_plan_state(session_id="session-2", doc_path="docs/PLAN2.md"),
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
                self.auto_plan_state(),
            )
            self.write_json(
                self.controller_state_path(
                    repo_root,
                    self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                ),
                {
                    "command": "auto-plan",
                    "doc_path": "docs/PLAN.md",
                },
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn(".codex/auto-plan-state.session-1.json", payload["stopReason"])
            self.assertIn(".codex/auto-plan-state.json", payload["stopReason"])

    def test_stop_hook_migrates_legacy_state_to_session_scoped_path(self) -> None:
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
                self.auto_plan_state(legacy_progress=True),
            )
            (docs_dir / "PLAN.md").write_text(
                self.auto_plan_doc_text(research=True),
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["continue"])
            self.assertIn("Use $arch-step deep-dive docs/PLAN.md", payload["reason"])
            self.assertIn(".codex/auto-plan-state.session-1.json", payload["reason"])
            self.assertEqual(
                payload["systemMessage"],
                "auto-plan continuing with deep-dive pass 1.",
            )

            session_state_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-1",
            )
            self.assertFalse(state_path.exists())
            state = json.loads(session_state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["session_id"], "session-1")
            self.assertNotIn("stage_index", state)
            self.assertNotIn("stages", state)

    def test_stop_hook_reconciles_minimal_auto_plan_state_from_doc_truth(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            state_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-1",
            )
            self.write_json(state_path, self.auto_plan_state())
            (docs_dir / "PLAN.md").write_text(
                self.auto_plan_doc_text(research=True),
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["continue"])
            self.assertIn("Use $arch-step deep-dive docs/PLAN.md", payload["reason"])
            self.assertEqual(
                payload["systemMessage"],
                "auto-plan continuing with deep-dive pass 1.",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state, self.auto_plan_state())

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
            self.write_json(state_path, self.auto_plan_state())
            (docs_dir / "PLAN.md").write_text(
                self.auto_plan_doc_text(
                    research=True,
                    deep_dive_pass_1=True,
                    deep_dive_pass_2=True,
                    phase_plan=True,
                ),
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["continue"])
            self.assertIn("Use $arch-step consistency-pass docs/PLAN.md", payload["reason"])
            self.assertEqual(
                payload["systemMessage"],
                "auto-plan continuing with consistency-pass.",
            )

            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state, self.auto_plan_state())

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
            self.write_json(state_path, self.auto_plan_state())
            (docs_dir / "PLAN.md").write_text(
                self.auto_plan_doc_text(
                    research=True,
                    deep_dive_pass_1=True,
                    deep_dive_pass_2=True,
                    phase_plan=True,
                    consistency_decision="yes",
                ),
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

    def test_stop_hook_completes_miniarch_auto_plan_after_phase_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            state_path = self.controller_state_path(
                repo_root,
                self.stop_module.MINIARCH_STEP_AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-1",
            )
            self.write_json(state_path, self.miniarch_step_auto_plan_state())
            (docs_dir / "PLAN.md").write_text(
                self.auto_plan_doc_text(
                    research=True,
                    deep_dive_pass_1=True,
                    phase_plan=True,
                ),
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn("Research, deep-dive, and phase-plan are in place", payload["stopReason"])
            self.assertIn("Use $miniarch-step implement-loop docs/PLAN.md", payload["stopReason"])
            self.assertNotIn("consistency-pass", payload["stopReason"])
            self.assertEqual(
                payload["systemMessage"],
                "miniarch-step auto-plan completed; the doc is ready for implement-loop.",
            )
            self.assertFalse(state_path.exists())

    def test_stop_hook_miniarch_auto_plan_continues_from_research_to_deep_dive(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            state_path = self.controller_state_path(
                repo_root,
                self.stop_module.MINIARCH_STEP_AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-1",
            )
            self.write_json(state_path, self.miniarch_step_auto_plan_state())
            (docs_dir / "PLAN.md").write_text(
                self.auto_plan_doc_text(research=True),
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["continue"])
            self.assertIn("Use $miniarch-step deep-dive docs/PLAN.md", payload["reason"])
            self.assertNotIn("consistency-pass", payload["reason"])
            self.assertEqual(
                payload["systemMessage"],
                "miniarch-step auto-plan continuing with deep-dive.",
            )
            self.assertTrue(state_path.exists())

    def test_handle_implement_loop_continuation_resumes_full_remaining_frontier(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path, doc_path = self.run_implement_loop_handler(
                repo_root,
                "session-1",
                verdict="NOT COMPLETE",
                audit_summary="later approved phases still need code work",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertIn("docs/PLAN.md", payload["reason"])
            self.assertIn("resume from the earliest reopened or incomplete phase", payload["reason"])
            self.assertIn("continue linearly through the remaining approved phases", payload["reason"])
            self.assertIn("current reachable frontier is done or genuinely blocked", payload["reason"])
            self.assertNotIn("smallest credible proof", payload["reason"])
            self.assertEqual(
                payload["systemMessage"],
                "implement-loop fresh audit finished; more work remains.",
            )
            self.assertTrue(state_path.exists())

    def test_handle_miniarch_implement_loop_uses_pinned_fresh_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            (
                exit_code,
                payload,
                stderr,
                state_path,
                _doc_path,
                audit_call,
            ) = self.run_miniarch_step_implement_loop_handler(
                repo_root,
                "session-1",
                verdict="NOT COMPLETE",
                audit_summary="more miniarch code work remains",
            )

            _args, kwargs = audit_call
            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertEqual(kwargs["skill_name"], "miniarch-step")
            self.assertEqual(kwargs["temp_prefix"], "miniarch-step-implement-loop-")
            self.assertEqual(kwargs["model"], self.stop_module.MINIARCH_STEP_AUDIT_MODEL)
            self.assertEqual(
                kwargs["model_reasoning_effort"],
                self.stop_module.MINIARCH_STEP_AUDIT_MODEL_REASONING_EFFORT,
            )
            self.assertTrue(state_path.exists())

    def test_stop_hook_disarms_auto_plan_when_research_is_still_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            docs_dir.mkdir()
            state_path = self.controller_state_path(
                repo_root,
                self.stop_module.AUTO_PLAN_STATE_RELATIVE_PATH,
                "session-1",
            )
            self.write_json(state_path, self.auto_plan_state())
            (docs_dir / "PLAN.md").write_text(
                "# Plan\nResearch never landed in the canonical doc.\n",
                encoding="utf-8",
            )

            process = self.run_stop_hook(repo_root, "session-1")

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn("stopped before research completed", payload["stopReason"])
            self.assertEqual(
                payload["systemMessage"],
                "auto-plan stopped before research completed.",
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
            self.write_json(state_path, self.auto_plan_state())
            (docs_dir / "PLAN.md").write_text(
                self.auto_plan_doc_text(
                    research=True,
                    deep_dive_pass_1=True,
                    deep_dive_pass_2=True,
                    phase_plan=True,
                    consistency_decision="no",
                ),
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

    def test_comment_loop_continue_keeps_state_armed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path, ledger_path = self.run_comment_loop_handler(
                repo_root,
                "session-1",
                controller_fields={
                    "Verdict": "CONTINUE",
                    "Next Area": "payment lifecycle invariants and retry gotchas",
                    "Stop Reason": "",
                    "Last Review": "2026-04-13",
                },
                review_summary="The canonical payment owner path still lacks its authoritative convention comment.",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertIn("more worthwhile comment work", payload["reason"])
            self.assertIn("Use $comment-loop", payload["reason"])
            self.assertIn("payment lifecycle invariants and retry gotchas", payload["reason"])
            self.assertEqual(payload["systemMessage"], "comment-loop review found more work.")
            self.assertTrue(state_path.exists())
            self.assertTrue(ledger_path.exists())

    def test_comment_loop_clean_removes_runtime_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path, ledger_path = self.run_comment_loop_handler(
                repo_root,
                "session-1",
                controller_fields={
                    "Verdict": "CLEAN",
                    "Next Area": "",
                    "Stop Reason": "",
                    "Last Review": "2026-04-13",
                },
                review_summary="No credible high-impact explanation gap remains.",
                gitignore_text="_comment_ledger.md\n",
                gitignore_created=True,
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertFalse(payload["continue"])
            self.assertIn("fresh review finished clean", payload["stopReason"])
            self.assertEqual(payload["systemMessage"], "comment-loop completed clean.")
            self.assertFalse(state_path.exists())
            self.assertFalse(ledger_path.exists())
            self.assertFalse((repo_root / ".gitignore").exists())

    def test_comment_loop_blocked_disarms_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path, ledger_path = self.run_comment_loop_handler(
                repo_root,
                "session-1",
                controller_fields={
                    "Verdict": "BLOCKED",
                    "Next Area": "",
                    "Stop Reason": "The behavior is still ambiguous and belongs to audit-loop first.",
                    "Last Review": "2026-04-13",
                },
                review_summary="The highest-priority front would freeze an unsettled contract into comments.",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertFalse(payload["continue"])
            self.assertIn(
                "The behavior is still ambiguous and belongs to audit-loop first.",
                payload["stopReason"],
            )
            self.assertEqual(payload["systemMessage"], "comment-loop stopped blocked.")
            self.assertFalse(state_path.exists())
            self.assertTrue(ledger_path.exists())

    def test_comment_loop_continue_without_next_area_disarms_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            exit_code, payload, stderr, state_path, ledger_path = self.run_comment_loop_handler(
                repo_root,
                "session-1",
                controller_fields={
                    "Verdict": "CONTINUE",
                    "Next Area": "",
                    "Stop Reason": "",
                    "Last Review": "2026-04-13",
                },
                review_summary="The review forgot to name the next explanation front.",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertFalse(payload["continue"])
            self.assertIn("CONTINUE without Next Area", payload["stopReason"])
            self.assertEqual(payload["systemMessage"], "comment-loop review omitted Next Area.")
            self.assertFalse(state_path.exists())
            self.assertTrue(ledger_path.exists())

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


class WaitDurationParserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop_module = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")

    def test_parse_wait_duration_accepts_90s(self) -> None:
        self.assertEqual(self.stop_module.parse_wait_duration("90s"), 90)

    def test_parse_wait_duration_accepts_30m(self) -> None:
        self.assertEqual(self.stop_module.parse_wait_duration("30m"), 1800)

    def test_parse_wait_duration_accepts_1h(self) -> None:
        self.assertEqual(self.stop_module.parse_wait_duration("1h"), 3600)

    def test_parse_wait_duration_accepts_2d(self) -> None:
        self.assertEqual(self.stop_module.parse_wait_duration("2d"), 172800)

    def test_parse_wait_duration_accepts_1h30m(self) -> None:
        self.assertEqual(self.stop_module.parse_wait_duration("1h30m"), 5400)

    def test_parse_wait_duration_accepts_2h15m30s(self) -> None:
        self.assertEqual(self.stop_module.parse_wait_duration("2h15m30s"), 8130)

    def test_parse_wait_duration_accepts_unordered_components(self) -> None:
        self.assertEqual(self.stop_module.parse_wait_duration("30s1h"), 3630)

    def test_parse_wait_duration_rejects_empty(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("")

    def test_parse_wait_duration_rejects_leading_whitespace(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration(" 1h")

    def test_parse_wait_duration_rejects_trailing_whitespace(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("1h ")

    def test_parse_wait_duration_rejects_embedded_whitespace(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("1 h")

    def test_parse_wait_duration_rejects_unknown_unit_w(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("1w")

    def test_parse_wait_duration_rejects_unknown_unit_y(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("1y")

    def test_parse_wait_duration_rejects_unknown_unit_ms(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("1ms")

    def test_parse_wait_duration_rejects_zero_component(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("0m")

    def test_parse_wait_duration_rejects_negative_component(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("-1h")

    def test_parse_wait_duration_rejects_duplicate_unit(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("1h2h")

    def test_parse_wait_duration_rejects_natural_language_half_an_hour(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("half an hour")

    def test_parse_wait_duration_rejects_natural_language_30_minutes(self) -> None:
        with self.assertRaises(ValueError):
            self.stop_module.parse_wait_duration("30 minutes")


class WaitHandlerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop_module = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")
        cls.stop_module.ACTIVE_RUNTIME = cls.stop_module.HOOK_RUNTIME_SPECS[
            cls.stop_module.RUNTIME_CODEX
        ]

    def _write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def _session_wait_state_path(self, repo_root: Path, session_id: str) -> Path:
        relative = self.stop_module.WAIT_STATE_RELATIVE_PATH
        return repo_root / self.stop_module.session_state_relative_path(relative, session_id)

    def _run_handle_wait(
        self,
        repo_root: Path,
        session_id: str,
        *,
        start_time: int,
    ) -> tuple[int, dict, str, list[int], int]:
        sleeps: list[int] = []
        fake_now = {"value": start_time}

        def fake_time() -> int:
            return fake_now["value"]

        def fake_sleep(seconds: int) -> None:
            sleeps.append(seconds)
            if seconds > 0:
                fake_now["value"] += seconds

        original_time = self.stop_module.current_epoch_seconds
        original_sleep = self.stop_module.sleep_for_seconds
        self.stop_module.current_epoch_seconds = fake_time
        self.stop_module.sleep_for_seconds = fake_sleep
        stdout = io.StringIO()
        stderr = io.StringIO()
        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        sys.stdout = stdout
        sys.stderr = stderr
        try:
            try:
                self.stop_module.handle_wait(
                    {"cwd": str(repo_root), "session_id": session_id}
                )
                exit_code = 0
            except SystemExit as exc:
                exit_code = int(exc.code) if exc.code is not None else 0
        finally:
            self.stop_module.current_epoch_seconds = original_time
            self.stop_module.sleep_for_seconds = original_sleep
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr
        stdout_text = stdout.getvalue()
        payload = json.loads(stdout_text) if stdout_text.strip() else {}
        return exit_code, payload, stderr.getvalue(), sleeps, fake_now["value"]

    def _valid_wait_state(
        self,
        *,
        session_id: str = "session-1",
        armed_at: int = 100,
        deadline_at: int = 700,
        resume_prompt: str = "say the wait fired",
    ) -> dict:
        return {
            "version": 1,
            "command": "wait",
            "session_id": session_id,
            "armed_at": armed_at,
            "deadline_at": deadline_at,
            "resume_prompt": resume_prompt,
        }

    def test_handle_wait_pre_deadline_sleeps_then_fires(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = self._session_wait_state_path(repo_root, "session-1")
            self._write_json(state_path, self._valid_wait_state(armed_at=100, deadline_at=700))
            exit_code, payload, stderr, sleeps, final_time = self._run_handle_wait(
                repo_root, "session-1", start_time=100
            )
            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertEqual(payload["decision"], "block")
            self.assertIn("say the wait fired", payload["reason"])
            self.assertIn("The requested wait elapsed", payload["reason"])
            self.assertEqual(payload["systemMessage"], "wait elapsed; continuing the task.")
            self.assertEqual(sleeps, [600])
            self.assertEqual(final_time, 700)
            self.assertFalse(state_path.exists())

    def test_handle_wait_past_deadline_fires_without_sleep(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = self._session_wait_state_path(repo_root, "session-1")
            self._write_json(state_path, self._valid_wait_state(armed_at=100, deadline_at=700))
            exit_code, payload, stderr, sleeps, final_time = self._run_handle_wait(
                repo_root, "session-1", start_time=9_000
            )
            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertTrue(payload["continue"])
            self.assertEqual(sleeps, [0])
            self.assertEqual(final_time, 9_000)
            self.assertFalse(state_path.exists())

    def test_handle_wait_ignores_state_from_other_session(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = self._session_wait_state_path(repo_root, "session-2")
            self._write_json(state_path, self._valid_wait_state(session_id="session-2"))
            exit_code, payload, stderr, sleeps, final_time = self._run_handle_wait(
                repo_root, "session-1", start_time=100
            )
            self.assertEqual(exit_code, 0)
            self.assertEqual(payload, {})
            self.assertEqual(stderr, "")
            self.assertEqual(sleeps, [])
            self.assertEqual(final_time, 100)
            self.assertTrue(state_path.exists())

    def test_handle_wait_clears_state_before_firing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = self._session_wait_state_path(repo_root, "session-1")
            self._write_json(state_path, self._valid_wait_state(armed_at=100, deadline_at=150))

            original_block = self.stop_module.block_with_json
            observed: dict[str, bool] = {}

            def recording_block(reason: str, system_message: str | None = None) -> None:
                observed["state_gone_at_block"] = not state_path.exists()
                original_block(reason, system_message)

            self.stop_module.block_with_json = recording_block
            try:
                self._run_handle_wait(repo_root, "session-1", start_time=100)
            finally:
                self.stop_module.block_with_json = original_block
            self.assertTrue(observed.get("state_gone_at_block"))
            self.assertFalse(state_path.exists())

    def _assert_forbidden_field_rejected(self, field_name: str, value: object) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = self._session_wait_state_path(repo_root, "session-1")
            state = self._valid_wait_state()
            state[field_name] = value
            self._write_json(state_path, state)
            exit_code, payload, stderr, sleeps, final_time = self._run_handle_wait(
                repo_root, "session-1", start_time=100
            )
            self.assertEqual(exit_code, 2)
            self.assertEqual(payload, {})
            self.assertIn(field_name, stderr)
            self.assertIn("delay-poll-only field", stderr)
            self.assertEqual(sleeps, [])
            self.assertFalse(state_path.exists())

    def test_handle_wait_rejects_interval_seconds(self) -> None:
        self._assert_forbidden_field_rejected("interval_seconds", 1800)

    def test_handle_wait_rejects_check_prompt(self) -> None:
        self._assert_forbidden_field_rejected("check_prompt", "check something")

    def test_handle_wait_rejects_attempt_count(self) -> None:
        self._assert_forbidden_field_rejected("attempt_count", 0)

    def test_handle_wait_rejects_last_check_at(self) -> None:
        self._assert_forbidden_field_rejected("last_check_at", None)

    def test_handle_wait_rejects_last_summary(self) -> None:
        self._assert_forbidden_field_rejected("last_summary", "")

    def test_handle_wait_rejects_bad_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = self._session_wait_state_path(repo_root, "session-1")
            state = self._valid_wait_state()
            state["version"] = 2
            self._write_json(state_path, state)
            exit_code, _, stderr, _, _ = self._run_handle_wait(
                repo_root, "session-1", start_time=100
            )
            self.assertEqual(exit_code, 2)
            self.assertIn("unsupported version", stderr)
            self.assertFalse(state_path.exists())

    def test_handle_wait_rejects_deadline_not_after_armed_at(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = self._session_wait_state_path(repo_root, "session-1")
            self._write_json(
                state_path,
                self._valid_wait_state(armed_at=500, deadline_at=500),
            )
            exit_code, _, stderr, _, _ = self._run_handle_wait(
                repo_root, "session-1", start_time=100
            )
            self.assertEqual(exit_code, 2)
            self.assertIn("deadline_at", stderr)
            self.assertFalse(state_path.exists())

    def test_handle_wait_rejects_empty_resume_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = self._session_wait_state_path(repo_root, "session-1")
            state = self._valid_wait_state()
            state["resume_prompt"] = "   "
            self._write_json(state_path, state)
            exit_code, _, stderr, _, _ = self._run_handle_wait(
                repo_root, "session-1", start_time=100
            )
            self.assertEqual(exit_code, 2)
            self.assertIn("resume_prompt", stderr)
            self.assertFalse(state_path.exists())


class WaitConflictGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop_module = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")

    def test_arming_wait_beside_another_controller_halts_with_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            wait_relative = self.stop_module.session_state_relative_path(
                self.stop_module.WAIT_STATE_RELATIVE_PATH, "session-1"
            )
            delay_relative = self.stop_module.session_state_relative_path(
                self.stop_module.DELAY_POLL_STATE_RELATIVE_PATH, "session-1"
            )
            wait_path = repo_root / wait_relative
            delay_path = repo_root / delay_relative
            wait_path.parent.mkdir(parents=True, exist_ok=True)
            wait_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "command": "wait",
                        "session_id": "session-1",
                        "armed_at": 100,
                        "deadline_at": 200,
                        "resume_prompt": "continue",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            delay_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "command": "delay-poll",
                        "session_id": "session-1",
                        "interval_seconds": 1800,
                        "armed_at": 100,
                        "deadline_at": 1000,
                        "check_prompt": "checker",
                        "resume_prompt": "resume",
                        "attempt_count": 0,
                        "last_check_at": None,
                        "last_summary": "",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            process = subprocess.run(
                [sys.executable, str(STOP_HOOK_PATH), "--runtime", "codex"],
                input=json.dumps({"cwd": str(repo_root), "session_id": "session-1"}),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn(str(wait_relative), payload["stopReason"])
            self.assertIn(str(delay_relative), payload["stopReason"])
            self.assertIn("Multiple suite controller states are armed", payload["stopReason"])
            self.assertTrue(wait_path.exists())
            self.assertTrue(delay_path.exists())


if __name__ == "__main__":
    unittest.main()
