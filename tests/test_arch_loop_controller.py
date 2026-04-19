import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STOP_HOOK_PATH = REPO_ROOT / "skills/arch-step/scripts/arch_controller_stop_hook.py"


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class ArchLoopCapExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")

    def extract(self, raw: str, created_at: int = 1000) -> dict:
        return self.stop.extract_arch_loop_constraints(raw, created_at)

    # --- duration parsing ---

    def test_runtime_cap_hours(self) -> None:
        result = self.extract("Implement and don't stop. Max runtime 5h.")
        self.assertEqual(result["deadline_at"], 1000 + 5 * 3600)
        self.assertIsNone(result["interval_seconds"])
        self.assertIsNone(result["max_iterations"])

    def test_runtime_cap_minutes(self) -> None:
        result = self.extract("Time limit 90 minutes.")
        self.assertEqual(result["deadline_at"], 1000 + 90 * 60)

    def test_runtime_cap_seconds(self) -> None:
        result = self.extract("Stop after 45 seconds.")
        self.assertEqual(result["deadline_at"], 1000 + 45)

    def test_runtime_cap_days(self) -> None:
        result = self.extract("For the next 1 day.")
        self.assertEqual(result["deadline_at"], 1000 + 86400)

    def test_runtime_cap_decimal_hours(self) -> None:
        result = self.extract("Max runtime 1.5h.")
        self.assertEqual(result["deadline_at"], 1000 + 5400)

    def test_runtime_cap_stop_if_not_done_word_form(self) -> None:
        result = self.extract("Stop if you're not done in 3 hours.")
        self.assertEqual(result["deadline_at"], 1000 + 3 * 3600)

    # --- cadence parsing ---

    def test_cadence_every_30_minutes(self) -> None:
        result = self.extract(
            "Every 30 minutes check example.com for the next 6 hours."
        )
        self.assertEqual(result["interval_seconds"], 1800)
        self.assertEqual(result["deadline_at"], 1000 + 6 * 3600)

    def test_cadence_every_10_seconds(self) -> None:
        result = self.extract("Every 10s check the smoke and for the next 30 minutes.")
        self.assertEqual(result["interval_seconds"], 10)

    def test_cadence_check_every_15_min(self) -> None:
        result = self.extract("check every 15 min, for the next 2 hours.")
        self.assertEqual(result["interval_seconds"], 15 * 60)

    def test_cadence_every_an_hour(self) -> None:
        result = self.extract("Every an hour check it, for the next 3 hours.")
        self.assertEqual(result["interval_seconds"], 3600)

    def test_cadence_bare_unit_every_hour(self) -> None:
        result = self.extract("Every hour check example.com for the next 6 hours.")
        self.assertEqual(result["interval_seconds"], 3600)

    # --- iteration parsing ---

    def test_iteration_max_5_iterations(self) -> None:
        result = self.extract("max 5 iterations.")
        self.assertEqual(result["max_iterations"], 5)

    def test_iteration_up_to_3_attempts(self) -> None:
        result = self.extract("up to 3 attempts.")
        self.assertEqual(result["max_iterations"], 3)

    def test_iteration_try_this_once(self) -> None:
        result = self.extract("try this once.")
        self.assertEqual(result["max_iterations"], 1)

    def test_iteration_twice_word_form(self) -> None:
        result = self.extract("only try this twice.")
        self.assertEqual(result["max_iterations"], 2)

    def test_iteration_stop_after_two_attempts(self) -> None:
        # Iteration phrase requires the suffix; without it `stop after`
        # is parsed as a runtime cap instead.
        result = self.extract("Stop after two attempts.")
        self.assertEqual(result["max_iterations"], 2)
        self.assertIsNone(result["deadline_at"])

    # --- strictest-cap selection ---

    def test_runtime_strictest_cap_wins(self) -> None:
        result = self.extract("max runtime 5h, stop if not done in 3h.")
        self.assertEqual(result["deadline_at"], 1000 + 3 * 3600)
        sources = {e["source_text"] for e in result["cap_evidence"]}
        self.assertIn("max runtime 5h", sources)
        self.assertIn("stop if not done in 3h", sources)

    def test_iteration_strictest_cap_wins(self) -> None:
        result = self.extract("up to 5 iterations, no more than 2 loops.")
        self.assertEqual(result["max_iterations"], 2)

    # --- ambiguity + hook-timeout fit ---

    def test_ambiguous_runtime_a_while_fails_loud(self) -> None:
        with self.assertRaises(self.stop.ArchLoopCapError):
            self.extract("Keep trying for a while until the audit passes.")

    def test_ambiguous_cadence_every_few_minutes_fails_loud(self) -> None:
        with self.assertRaises(self.stop.ArchLoopCapError):
            self.extract("every few minutes check it.")

    def test_ambiguous_iteration_a_few_attempts_fails_loud(self) -> None:
        with self.assertRaises(self.stop.ArchLoopCapError):
            self.extract("a few attempts is fine.")

    def test_conflicting_cadence_phrases_fail_loud(self) -> None:
        with self.assertRaises(self.stop.ArchLoopCapError) as ctx:
            self.extract("check every 30 minutes, and also every hour, for the next 6 hours.")
        self.assertIn("every 30 minutes", str(ctx.exception))
        self.assertIn("every hour", str(ctx.exception))

    def test_cadence_exceeding_hook_timeout_fails_loud(self) -> None:
        with self.assertRaises(self.stop.ArchLoopCapError):
            self.extract("Every 2 days check whether the build is green.")

    def test_runtime_window_exceeds_hook_timeout_without_cadence_fails_loud(self) -> None:
        with self.assertRaises(self.stop.ArchLoopCapError):
            self.extract("Max runtime 40h.")

    def test_cadence_overruns_deadline_fails_loud(self) -> None:
        # interval 1800s but deadline only 100s later → cadence cannot fire.
        with self.assertRaises(self.stop.ArchLoopCapError):
            self.extract(
                "Every 30 minutes check host, for 100 seconds.",
                created_at=1000,
            )

    # --- named-skill audits ---

    def test_named_skill_audit_seeded_pending(self) -> None:
        result = self.extract(
            "Implement docs/PLAN.md and get a clean audit by $agent-linter. Max runtime 5h."
        )
        audits = result["required_skill_audits"]
        self.assertEqual(len(audits), 1)
        self.assertEqual(audits[0]["skill"], "agent-linter")
        self.assertEqual(audits[0]["status"], "pending")

    def test_named_skill_audits_deduped(self) -> None:
        result = self.extract(
            "Run $agent-linter; also keep running $agent-linter until it passes."
        )
        skills = [a["skill"] for a in result["required_skill_audits"]]
        self.assertEqual(skills, ["agent-linter"])

    def test_multiple_distinct_named_audits_preserved(self) -> None:
        result = self.extract(
            "Run $agent-linter and $skill-authoring until both are clean."
        )
        skills = sorted(a["skill"] for a in result["required_skill_audits"])
        self.assertEqual(skills, ["agent-linter", "skill-authoring"])

    # --- preconditions ---

    def test_empty_raw_requirements_rejected(self) -> None:
        with self.assertRaises(self.stop.ArchLoopCapError):
            self.extract("")

    def test_non_positive_created_at_rejected(self) -> None:
        with self.assertRaises(self.stop.ArchLoopCapError):
            self.stop.extract_arch_loop_constraints("max runtime 5h", 0)


class ArchLoopStateValidationTests(unittest.TestCase):
    """Exercise `validate_arch_loop_state` directly. Each test writes a state
    file, invokes the validator with a matching payload, and asserts that
    invalid fields fail loud via `block_with_message` (SystemExit 2)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")

    def setUp(self) -> None:
        # The validator calls `require_runtime()` via `controller_state_relative_path`;
        # each test must install a runtime before it runs.
        self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[self.stop.RUNTIME_CODEX]

    def _valid_state(self, **overrides) -> dict:
        state = {
            "version": 1,
            "command": "arch-loop",
            "runtime": "codex",
            "session_id": "session-1",
            "raw_requirements": "Implement this and ship.",
            "created_at": 1000,
            "iteration_count": 0,
            "check_count": 0,
            "deadline_at": 2000,
            "interval_seconds": None,
            "max_iterations": None,
            "next_due_at": None,
            "cap_evidence": [],
            "required_skill_audits": [],
            "last_work_summary": "",
            "last_verification_summary": "",
            "last_continue_mode": "",
            "last_next_task": "",
        }
        state.update(overrides)
        return state

    def _write_state(self, repo_root: Path, state: dict) -> Path:
        relative = self.stop.session_state_relative_path(
            self.stop.ARCH_LOOP_STATE_RELATIVE_PATH, state["session_id"]
        )
        state_path = repo_root / relative
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        return state_path

    def _resolve(self, repo_root: Path, session_id: str):
        payload = {"cwd": str(repo_root), "session_id": session_id}
        return self.stop.resolve_controller_state_for_handler(
            payload, self.stop.ARCH_LOOP_STATE_SPEC
        )

    def _run(self, state: dict):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = self._write_state(repo_root, state)
            payload = {"cwd": str(repo_root), "session_id": state["session_id"]}
            resolved = self.stop.resolve_controller_state_for_handler(
                payload, self.stop.ARCH_LOOP_STATE_SPEC
            )
            return self.stop.validate_arch_loop_state(payload, resolved), state_path

    def test_valid_state_round_trips(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state = self._valid_state()
            state_path = self._write_state(repo_root, state)
            payload = {"cwd": str(repo_root), "session_id": state["session_id"]}
            resolved = self.stop.resolve_controller_state_for_handler(
                payload, self.stop.ARCH_LOOP_STATE_SPEC
            )
            result = self.stop.validate_arch_loop_state(payload, resolved)
            self.assertIsNotNone(result)
            self.assertTrue(state_path.exists())
            loaded_state, loaded_path = result
            self.assertEqual(loaded_state["command"], "arch-loop")
            self.assertEqual(loaded_path.resolve(), state_path.resolve())

    def test_rejects_bad_version(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            self._run(self._valid_state(version=2))
        self.assertEqual(ctx.exception.code, 2)

    def test_rejects_unsupported_runtime(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(runtime="gemini"))

    def test_rejects_missing_raw_requirements(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(raw_requirements=""))

    def test_rejects_non_positive_created_at(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(created_at=0))

    def test_rejects_negative_iteration_count(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(iteration_count=-1))

    def test_rejects_negative_check_count(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(check_count=-1))

    def test_rejects_deadline_not_after_created_at(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(deadline_at=1000))

    def test_rejects_non_positive_interval_seconds(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(interval_seconds=0))

    def test_rejects_interval_exceeding_hook_timeout(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(interval_seconds=100000))

    def test_rejects_non_positive_max_iterations(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(max_iterations=0))

    def test_rejects_next_due_past_deadline(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(next_due_at=9999))

    def test_rejects_unknown_audit_status(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(
                self._valid_state(
                    required_skill_audits=[
                        {"skill": "agent-linter", "status": "bogus"}
                    ]
                )
            )

    def test_rejects_invalid_last_continue_mode(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(last_continue_mode="sideways"))

    def test_rejects_cap_evidence_not_a_list(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(self._valid_state(cap_evidence="runtime=5h"))

    def test_rejects_unknown_cap_evidence_type(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(
                self._valid_state(
                    cap_evidence=[
                        {"type": "mystery", "source_text": "x", "normalized": "y"}
                    ]
                )
            )

    def test_mismatched_session_clears_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self._write_state(repo_root, self._valid_state(session_id="session-2"))
            payload = {"cwd": str(repo_root), "session_id": "session-1"}
            resolved = self.stop.resolve_controller_state_for_handler(
                payload, self.stop.ARCH_LOOP_STATE_SPEC
            )
            # Different session → resolver returns None (session-scoped path
            # for session-1 does not exist, and the legacy unsuffixed path
            # isn't armed either).
            self.assertIsNone(resolved)


class ArchLoopRuntimeStatePathTests(unittest.TestCase):
    """Assert that arch-loop state paths resolve under the runtime-local root."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")

    def test_codex_runtime_uses_dot_codex(self) -> None:
        self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[self.stop.RUNTIME_CODEX]
        relative = self.stop.controller_state_relative_path(self.stop.ARCH_LOOP_STATE_SPEC)
        self.assertEqual(relative, Path(".codex/arch-loop-state.json"))

    def test_claude_runtime_uses_claude_arch_skill(self) -> None:
        self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[self.stop.RUNTIME_CLAUDE]
        relative = self.stop.controller_state_relative_path(self.stop.ARCH_LOOP_STATE_SPEC)
        self.assertEqual(relative, Path(".claude/arch_skill/arch-loop-state.json"))

    def test_session_scoped_suffixing(self) -> None:
        session = self.stop.session_state_relative_path(
            self.stop.ARCH_LOOP_STATE_RELATIVE_PATH, "abc-123"
        )
        self.assertEqual(session, Path(".codex/arch-loop-state.abc-123.json"))


class ArchLoopSleepReasonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")

    def test_sleep_until_next_due(self) -> None:
        current = [10_000]

        def fake_now() -> int:
            return current[0]

        original = self.stop.current_epoch_seconds
        self.stop.current_epoch_seconds = fake_now
        try:
            self.assertEqual(
                self.stop.arch_loop_sleep_reason(next_due_at=10_500, deadline_at=20_000),
                500,
            )
            self.assertEqual(
                self.stop.arch_loop_sleep_reason(next_due_at=10_500, deadline_at=None),
                500,
            )
            # Past-due returns zero.
            self.assertEqual(
                self.stop.arch_loop_sleep_reason(next_due_at=9_000, deadline_at=20_000),
                0,
            )
            # Deadline truncates the wait.
            self.assertEqual(
                self.stop.arch_loop_sleep_reason(next_due_at=15_000, deadline_at=11_000),
                1_000,
            )
        finally:
            self.stop.current_epoch_seconds = original


class ArchLoopDuplicateControllerTests(unittest.TestCase):
    """End-to-end: arming an arch-loop state alongside another controller
    in the same session must halt the Stop hook with a conflict message."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")

    def test_arch_loop_conflicts_with_other_controller(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            arch_loop_relative = self.stop.session_state_relative_path(
                self.stop.ARCH_LOOP_STATE_RELATIVE_PATH, "session-1"
            )
            wait_relative = self.stop.session_state_relative_path(
                self.stop.WAIT_STATE_RELATIVE_PATH, "session-1"
            )
            arch_loop_path = repo_root / arch_loop_relative
            wait_path = repo_root / wait_relative
            arch_loop_path.parent.mkdir(parents=True, exist_ok=True)
            wait_path.parent.mkdir(parents=True, exist_ok=True)
            arch_loop_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "command": "arch-loop",
                        "runtime": "codex",
                        "session_id": "session-1",
                        "raw_requirements": "ship it",
                        "created_at": 100,
                        "iteration_count": 0,
                        "check_count": 0,
                        "deadline_at": 2000,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
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
            self.assertIn(str(arch_loop_relative), payload["stopReason"])
            self.assertIn(str(wait_relative), payload["stopReason"])
            self.assertIn(
                "Multiple suite controller states are armed",
                payload["stopReason"],
            )
            # The conflict gate never deletes state files.
            self.assertTrue(arch_loop_path.exists())
            self.assertTrue(wait_path.exists())


class ArchLoopHandlerLifecycleTests(unittest.TestCase):
    """Exercise handle_arch_loop end-to-end with a mocked fresh evaluator."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")
        cls.stop.ACTIVE_RUNTIME = cls.stop.HOOK_RUNTIME_SPECS[cls.stop.RUNTIME_CODEX]

    # --- helpers ---

    def _valid_state(
        self,
        *,
        session_id: str = "session-arch-loop",
        deadline_at: int | None = 10_000,
        interval_seconds: int | None = None,
        max_iterations: int | None = None,
        iteration_count: int = 0,
        check_count: int = 0,
        next_due_at: int | None = None,
        required_skill_audits: list | None = None,
    ) -> dict:
        state: dict = {
            "version": 1,
            "command": "arch-loop",
            "runtime": "codex",
            "session_id": session_id,
            "raw_requirements": "keep running until the evaluator is happy",
            "created_at": 1_000,
            "iteration_count": iteration_count,
            "check_count": check_count,
        }
        if deadline_at is not None:
            state["deadline_at"] = deadline_at
        if interval_seconds is not None:
            state["interval_seconds"] = interval_seconds
        if max_iterations is not None:
            state["max_iterations"] = max_iterations
        if next_due_at is not None:
            state["next_due_at"] = next_due_at
        if required_skill_audits is not None:
            state["required_skill_audits"] = required_skill_audits
        return state

    def _structured_result(
        self,
        payload: dict | None,
        *,
        returncode: int = 0,
        last_message: str | None = None,
    ):
        if last_message is None and payload is not None:
            last_message = json.dumps(payload)
        return self.stop.FreshStructuredResult(
            process=subprocess.CompletedProcess(
                args=["codex"],
                returncode=returncode,
                stdout="",
                stderr="",
            ),
            last_message=last_message,
            payload=payload,
        )

    def setUp(self) -> None:
        self._tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tempdir.cleanup)

    def _run_handler(
        self,
        *,
        state: dict,
        evaluator_results: list,
        start_time: int = 2_000,
        session_id: str = "session-arch-loop",
    ) -> tuple[int, dict | None, str, Path, list[int], int, dict | None]:
        repo_root = Path(self._tempdir.name).resolve()
        if True:
            relative = self.stop.session_state_relative_path(
                self.stop.ARCH_LOOP_STATE_RELATIVE_PATH, session_id
            )
            state_path = repo_root / relative
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

            result_iter = iter(evaluator_results)
            sleeps: list[int] = []
            fake_now = {"value": start_time}

            def fake_eval(cwd, state_arg, repo_root_arg, prompt_text):
                result = next(result_iter)
                if isinstance(result, Exception):
                    raise result
                return result

            def fake_time():
                return fake_now["value"]

            def fake_sleep(seconds: int):
                sleeps.append(seconds)
                fake_now["value"] += max(0, seconds)

            original_eval = self.stop.run_arch_loop_evaluator
            original_time = self.stop.current_epoch_seconds
            original_sleep = self.stop.sleep_for_seconds
            self.stop.run_arch_loop_evaluator = fake_eval
            self.stop.current_epoch_seconds = fake_time
            self.stop.sleep_for_seconds = fake_sleep

            stdout = io.StringIO()
            stderr = io.StringIO()
            saved_stdout = sys.stdout
            saved_stderr = sys.stderr
            sys.stdout = stdout
            sys.stderr = stderr
            code = None
            try:
                with self.assertRaises(SystemExit) as raised:
                    self.stop.handle_arch_loop(
                        {"cwd": str(repo_root), "session_id": session_id}
                    )
                code = raised.exception.code
            finally:
                self.stop.run_arch_loop_evaluator = original_eval
                self.stop.current_epoch_seconds = original_time
                self.stop.sleep_for_seconds = original_sleep
                sys.stdout = saved_stdout
                sys.stderr = saved_stderr

            stdout_text = stdout.getvalue()
            payload: dict | None = None
            if stdout_text.strip():
                payload = json.loads(stdout_text)

            saved_state: dict | None = None
            if state_path.exists():
                saved_state = json.loads(state_path.read_text(encoding="utf-8"))

            return (
                code,
                payload,
                stderr.getvalue(),
                state_path,
                sleeps,
                fake_now["value"],
                saved_state,
            )

    # --- verdict dispatch ---

    def test_clean_verdict_clears_state_and_stops(self) -> None:
        state = self._valid_state()
        eval_payload = {
            "verdict": "clean",
            "summary": "everything satisfied",
            "satisfied_requirements": ["ship it"],
            "unsatisfied_requirements": [],
            "required_skill_audits": [],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "",
        }
        code, payload, _, state_path, _, _, saved_state = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(eval_payload)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("clean", payload["stopReason"])
        self.assertIn("everything satisfied", payload["stopReason"])
        self.assertFalse(state_path.exists())
        self.assertIsNone(saved_state)

    def test_continue_parent_work_blocks_and_keeps_state(self) -> None:
        state = self._valid_state(max_iterations=3)
        eval_payload = {
            "verdict": "continue",
            "summary": "still needs one more pass",
            "satisfied_requirements": [],
            "unsatisfied_requirements": ["finish the evaluator tests"],
            "required_skill_audits": [],
            "continue_mode": "parent_work",
            "next_task": "wire handle_arch_loop into main()",
            "blocker": "",
        }
        code, payload, _, _, _, _, saved_state = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(eval_payload)],
        )
        self.assertEqual(code, 0)
        self.assertTrue(payload["continue"])
        self.assertEqual(payload["decision"], "block")
        self.assertIn("wire handle_arch_loop into main()", payload["reason"])
        self.assertIsNotNone(saved_state)
        self.assertEqual(saved_state["iteration_count"], 1)
        self.assertEqual(saved_state["last_continue_mode"], "parent_work")
        self.assertEqual(saved_state["last_evaluator_verdict"], "continue")
        self.assertEqual(
            saved_state["last_next_task"], "wire handle_arch_loop into main()"
        )

    def test_continue_wait_recheck_schedules_next_due(self) -> None:
        state = self._valid_state(
            deadline_at=60_000,
            interval_seconds=1_800,
            max_iterations=None,
        )
        wait_payload = {
            "verdict": "continue",
            "summary": "not yet",
            "satisfied_requirements": [],
            "unsatisfied_requirements": ["host still unreachable"],
            "required_skill_audits": [],
            "continue_mode": "wait_recheck",
            "next_task": "retry reachability probe",
            "blocker": "",
        }
        clean_payload = {
            "verdict": "clean",
            "summary": "host now reachable",
            "satisfied_requirements": ["reachable"],
            "unsatisfied_requirements": [],
            "required_skill_audits": [],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "",
        }
        code, payload, _, state_path, sleeps, final_now, _saved = self._run_handler(
            state=state,
            evaluator_results=[
                self._structured_result(wait_payload),
                self._structured_result(clean_payload),
            ],
            start_time=5_000,
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("clean", payload["stopReason"])
        self.assertFalse(state_path.exists())
        # First pass: no sleep (next_due_at not yet armed).
        # After wait_recheck, next_due_at = 5_000 + 1_800 = 6_800, so sleep=1_800.
        self.assertIn(1_800, sleeps)
        self.assertGreaterEqual(final_now, 6_800)

    def test_blocked_verdict_clears_state_and_stops(self) -> None:
        state = self._valid_state()
        eval_payload = {
            "verdict": "blocked",
            "summary": "needs user input",
            "satisfied_requirements": [],
            "unsatisfied_requirements": ["question remains"],
            "required_skill_audits": [],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "confirm which host you meant",
        }
        code, payload, _, state_path, _, _, saved_state = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(eval_payload)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("confirm which host you meant", payload["stopReason"])
        self.assertFalse(state_path.exists())
        self.assertIsNone(saved_state)

    # --- timing caps ---

    def test_deadline_already_past_stops_before_evaluator(self) -> None:
        state = self._valid_state(deadline_at=1_500)
        code, payload, _, state_path, _, _, saved_state = self._run_handler(
            state=state,
            evaluator_results=[],
            start_time=2_000,
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("timed out", payload["stopReason"])
        self.assertFalse(state_path.exists())
        self.assertIsNone(saved_state)

    def test_max_iterations_cap_stops_after_parent_work(self) -> None:
        state = self._valid_state(max_iterations=2, iteration_count=1)
        # Handler increments iteration_count at entry → 2. parent_work hits cap.
        eval_payload = {
            "verdict": "continue",
            "summary": "still not satisfied",
            "satisfied_requirements": [],
            "unsatisfied_requirements": ["one more"],
            "required_skill_audits": [],
            "continue_mode": "parent_work",
            "next_task": "do the final pass",
            "blocker": "",
        }
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(eval_payload)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("max_iterations", payload["stopReason"])
        self.assertFalse(state_path.exists())

    # --- fail-loud cases ---

    def test_missing_evaluator_prompt_stops_loud(self) -> None:
        state = self._valid_state()
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            relative = self.stop.session_state_relative_path(
                self.stop.ARCH_LOOP_STATE_RELATIVE_PATH, "sess"
            )
            state_path = repo_root / relative
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state["session_id"] = "sess"
            state_path.write_text(json.dumps(state) + "\n", encoding="utf-8")

            original_resolver = self.stop.resolve_arch_loop_evaluator_prompt_path
            self.stop.resolve_arch_loop_evaluator_prompt_path = lambda: None
            stdout = io.StringIO()
            saved_stdout = sys.stdout
            sys.stdout = stdout
            try:
                with self.assertRaises(SystemExit) as raised:
                    self.stop.handle_arch_loop(
                        {"cwd": str(repo_root), "session_id": "sess"}
                    )
            finally:
                self.stop.resolve_arch_loop_evaluator_prompt_path = original_resolver
                sys.stdout = saved_stdout
            self.assertEqual(raised.exception.code, 0)
            payload = json.loads(stdout.getvalue())
            self.assertIn("evaluator prompt", payload["stopReason"])
            self.assertFalse(state_path.exists())

    def test_evaluator_non_zero_returncode_fails_loud(self) -> None:
        state = self._valid_state()
        result = self._structured_result(None, returncode=1, last_message="boom")
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[result],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("evaluator process failed", payload["stopReason"])
        self.assertFalse(state_path.exists())

    def test_invalid_json_fails_loud(self) -> None:
        state = self._valid_state()
        result = self._structured_result(
            None, returncode=0, last_message="not json at all"
        )
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[result],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("usable structured JSON", payload["stopReason"])
        self.assertFalse(state_path.exists())

    def test_continue_without_continue_mode_fails_loud(self) -> None:
        state = self._valid_state()
        bad = {
            "verdict": "continue",
            "summary": "no mode",
            "satisfied_requirements": [],
            "unsatisfied_requirements": ["x"],
            "required_skill_audits": [],
            "continue_mode": "none",
            "next_task": "some task",
            "blocker": "",
        }
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(bad)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("continue_mode", payload["stopReason"])
        self.assertFalse(state_path.exists())

    def test_continue_without_next_task_fails_loud(self) -> None:
        state = self._valid_state()
        bad = {
            "verdict": "continue",
            "summary": "no task",
            "satisfied_requirements": [],
            "unsatisfied_requirements": ["x"],
            "required_skill_audits": [],
            "continue_mode": "parent_work",
            "next_task": "",
            "blocker": "",
        }
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(bad)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("next_task", payload["stopReason"])
        self.assertFalse(state_path.exists())

    def test_wait_recheck_without_cadence_fails_loud(self) -> None:
        state = self._valid_state(interval_seconds=None)
        bad = {
            "verdict": "continue",
            "summary": "no cadence armed",
            "satisfied_requirements": [],
            "unsatisfied_requirements": ["x"],
            "required_skill_audits": [],
            "continue_mode": "wait_recheck",
            "next_task": "recheck something",
            "blocker": "",
        }
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(bad)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("wait_recheck", payload["stopReason"])
        self.assertFalse(state_path.exists())

    def test_blocked_without_blocker_fails_loud(self) -> None:
        state = self._valid_state()
        bad = {
            "verdict": "blocked",
            "summary": "no blocker string",
            "satisfied_requirements": [],
            "unsatisfied_requirements": [],
            "required_skill_audits": [],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "",
        }
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(bad)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("blocker", payload["stopReason"])
        self.assertFalse(state_path.exists())

    def test_clean_with_failing_audit_fails_loud(self) -> None:
        state = self._valid_state(
            required_skill_audits=[
                {
                    "skill": "agent-linter",
                    "target": "skills/arch-loop",
                    "requirement": "clean",
                    "status": "pending",
                }
            ],
        )
        bad = {
            "verdict": "clean",
            "summary": "premature clean",
            "satisfied_requirements": ["x"],
            "unsatisfied_requirements": [],
            "required_skill_audits": [
                {
                    "skill": "agent-linter",
                    "status": "fail",
                    "evidence": "lint still reports issues",
                }
            ],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "",
        }
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(bad)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("audit", payload["stopReason"])
        self.assertFalse(state_path.exists())

    def test_clean_with_non_empty_unsatisfied_fails_loud(self) -> None:
        state = self._valid_state()
        bad = {
            "verdict": "clean",
            "summary": "premature clean",
            "satisfied_requirements": ["x"],
            "unsatisfied_requirements": ["still pending"],
            "required_skill_audits": [],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "",
        }
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(bad)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("unsatisfied_requirements", payload["stopReason"])
        self.assertFalse(state_path.exists())

    def test_invalid_verdict_fails_loud(self) -> None:
        state = self._valid_state()
        bad = {
            "verdict": "maybe",
            "summary": "?",
            "satisfied_requirements": [],
            "unsatisfied_requirements": [],
            "required_skill_audits": [],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "",
        }
        code, payload, _, state_path, _, _, _ = self._run_handler(
            state=state,
            evaluator_results=[self._structured_result(bad)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("invalid verdict", payload["stopReason"])
        self.assertFalse(state_path.exists())


class ArchLoopEvaluatorCommandTests(unittest.TestCase):
    """Capture the exact Codex argv used by run_arch_loop_evaluator so the
    arch-loop evaluator contract (Codex yolo + dangerously bypass sandbox +
    disable codex_hooks + --output-schema + -o) cannot silently drift."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")
        cls.stop.ACTIVE_RUNTIME = cls.stop.HOOK_RUNTIME_SPECS[cls.stop.RUNTIME_CODEX]

    def test_codex_command_shape(self) -> None:
        state = {
            "version": 1,
            "command": "arch-loop",
            "runtime": "codex",
            "session_id": "sess",
            "raw_requirements": "keep going until clean",
            "created_at": 1_000,
            "iteration_count": 1,
            "check_count": 0,
        }
        recorded: dict[str, list[str]] = {}

        def fake_run(args, **kwargs):
            recorded["args"] = list(args)
            # Write a minimal valid payload to the last_message path so the
            # helper returns a parsed payload.
            for idx, value in enumerate(args):
                if value == "-o" and idx + 1 < len(args):
                    Path(args[idx + 1]).write_text(
                        json.dumps(
                            {
                                "verdict": "clean",
                                "summary": "ok",
                                "satisfied_requirements": [],
                                "unsatisfied_requirements": [],
                                "required_skill_audits": [],
                                "continue_mode": "none",
                                "next_task": "",
                                "blocker": "",
                            }
                        ),
                        encoding="utf-8",
                    )
            return subprocess.CompletedProcess(
                args=args, returncode=0, stdout="", stderr=""
            )

        original_run = self.stop.subprocess.run
        original_which = self.stop.shutil.which
        self.stop.subprocess.run = fake_run
        self.stop.shutil.which = lambda name: "/usr/local/bin/codex" if name == "codex" else None
        try:
            with tempfile.TemporaryDirectory() as tmp:
                repo_root = Path(tmp).resolve()
                self.stop.run_arch_loop_evaluator(
                    repo_root, state, repo_root, "PROMPT\n"
                )
        finally:
            self.stop.subprocess.run = original_run
            self.stop.shutil.which = original_which

        args = recorded["args"]
        self.assertEqual(args[0], "/usr/local/bin/codex")
        self.assertEqual(args[1], "exec")
        self.assertIn("-p", args)
        self.assertEqual(args[args.index("-p") + 1], "yolo")
        self.assertIn("--ephemeral", args)
        self.assertIn("--disable", args)
        self.assertEqual(args[args.index("--disable") + 1], "codex_hooks")
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertIn("-C", args)
        self.assertEqual(args[args.index("-C") + 1], str(repo_root))
        self.assertIn("--output-schema", args)
        self.assertIn("-o", args)
        # The prompt is always the final positional argument.
        self.assertIn("PROMPT", args[-1])


class ArchLoopPhase6CodexProofTests(unittest.TestCase):
    """Phase 6 Codex lifecycle probes that the previous phases did not cover end
    to end: cadence-armed parent_work wake, cadence-driven deadline overrun
    during a wait_recheck loop, and the canonical $agent-linter named-audit
    obligation in both pass and missing shapes."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")
        cls.stop.ACTIVE_RUNTIME = cls.stop.HOOK_RUNTIME_SPECS[cls.stop.RUNTIME_CODEX]

    def setUp(self) -> None:
        self._tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tempdir.cleanup)

    def _state(self, **overrides) -> dict:
        state: dict = {
            "version": 1,
            "command": "arch-loop",
            "runtime": "codex",
            "session_id": "session-phase6-codex",
            "raw_requirements": "keep going until $agent-linter is clean",
            "created_at": 1_000,
            "iteration_count": 0,
            "check_count": 0,
            "deadline_at": 10_000,
        }
        state.update(overrides)
        return state

    def _run(
        self,
        *,
        state: dict,
        evaluator_results: list,
        start_time: int = 2_000,
        session_id: str = "session-phase6-codex",
    ):
        repo_root = Path(self._tempdir.name).resolve()
        relative = self.stop.session_state_relative_path(
            self.stop.ARCH_LOOP_STATE_RELATIVE_PATH, session_id
        )
        state_path = repo_root / relative
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

        result_iter = iter(evaluator_results)
        sleeps: list[int] = []
        fake_now = {"value": start_time}

        def fake_eval(cwd, state_arg, repo_root_arg, prompt_text):
            return next(result_iter)

        def fake_time():
            return fake_now["value"]

        def fake_sleep(seconds: int):
            sleeps.append(seconds)
            fake_now["value"] += max(0, seconds)

        original_eval = self.stop.run_arch_loop_evaluator
        original_time = self.stop.current_epoch_seconds
        original_sleep = self.stop.sleep_for_seconds
        self.stop.run_arch_loop_evaluator = fake_eval
        self.stop.current_epoch_seconds = fake_time
        self.stop.sleep_for_seconds = fake_sleep

        stdout = io.StringIO()
        saved_stdout = sys.stdout
        sys.stdout = stdout
        code = None
        try:
            with self.assertRaises(SystemExit) as raised:
                self.stop.handle_arch_loop(
                    {"cwd": str(repo_root), "session_id": session_id}
                )
            code = raised.exception.code
        finally:
            self.stop.run_arch_loop_evaluator = original_eval
            self.stop.current_epoch_seconds = original_time
            self.stop.sleep_for_seconds = original_sleep
            sys.stdout = saved_stdout

        payload = json.loads(stdout.getvalue()) if stdout.getvalue().strip() else None
        saved_state = (
            json.loads(state_path.read_text(encoding="utf-8"))
            if state_path.exists()
            else None
        )
        return code, payload, state_path, sleeps, fake_now["value"], saved_state

    def _structured(
        self,
        payload: dict | None,
        *,
        returncode: int = 0,
        last_message: str | None = None,
    ):
        if last_message is None and payload is not None:
            last_message = json.dumps(payload)
        return self.stop.FreshStructuredResult(
            process=subprocess.CompletedProcess(
                args=["codex"], returncode=returncode, stdout="", stderr=""
            ),
            last_message=last_message,
            payload=payload,
        )

    def test_cadence_to_work_wakes_parent_with_concrete_prompt(self) -> None:
        # State arrives armed for cadence. Sleep, then evaluator returns
        # parent_work; the hook must block the parent (continue=true,
        # decision=block) and inject the literal $arch-loop continuation prompt
        # naming the next concrete task.
        state = self._state(
            interval_seconds=1_800,
            next_due_at=4_000,
            check_count=2,
        )
        eval_payload = {
            "verdict": "continue",
            "summary": "host became reachable but smoke test still failing",
            "satisfied_requirements": ["host responds"],
            "unsatisfied_requirements": ["smoke test failing"],
            "required_skill_audits": [],
            "continue_mode": "parent_work",
            "next_task": "rerun the staging smoke test and capture failures",
            "blocker": "",
        }
        code, payload, state_path, sleeps, _, saved = self._run(
            state=state,
            evaluator_results=[self._structured(eval_payload)],
            start_time=2_000,
        )
        self.assertEqual(code, 0)
        self.assertTrue(payload["continue"])
        self.assertEqual(payload["decision"], "block")
        self.assertIn(
            "rerun the staging smoke test and capture failures", payload["reason"]
        )
        # Continuation prompt must literally name the skill so the parent thread
        # routes back to $arch-loop on resume.
        self.assertIn("arch-loop", payload["reason"])
        # Hook slept until next_due_at (4_000) before launching the evaluator.
        self.assertEqual(sleeps[0], 2_000)
        # State must remain armed because the loop is not finished.
        self.assertTrue(state_path.exists())
        self.assertIsNotNone(saved)
        self.assertEqual(saved["last_continue_mode"], "parent_work")
        self.assertEqual(
            saved["last_next_task"],
            "rerun the staging smoke test and capture failures",
        )
        # check_count incremented once because the hook ran a cadence check.
        self.assertEqual(saved["check_count"], 3)

    def test_cadence_window_overruns_deadline_and_clears_state(self) -> None:
        # Cadence loop where the next scheduled check would land past
        # deadline_at. The hook must clear state and stop with a timeout reason.
        state = self._state(
            interval_seconds=2_000,
            next_due_at=4_000,
            deadline_at=5_500,
            check_count=1,
        )
        wait_payload = {
            "verdict": "continue",
            "summary": "still not reachable",
            "satisfied_requirements": [],
            "unsatisfied_requirements": ["host unreachable"],
            "required_skill_audits": [],
            "continue_mode": "wait_recheck",
            "next_task": "retry probe",
            "blocker": "",
        }
        code, payload, state_path, _, _, saved = self._run(
            state=state,
            evaluator_results=[self._structured(wait_payload)],
            start_time=2_000,
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("cadence", payload["stopReason"])
        self.assertIn("deadline", payload["stopReason"])
        self.assertFalse(state_path.exists())
        self.assertIsNone(saved)

    def test_agent_linter_obligation_clean_pass_accepted(self) -> None:
        # Canonical $agent-linter obligation: state declares the audit pending,
        # evaluator returns clean with status=pass and concrete evidence. Handler
        # must accept and clear state.
        state = self._state(
            required_skill_audits=[
                {
                    "skill": "agent-linter",
                    "target": "skills/arch-loop",
                    "requirement": "clean",
                    "status": "pending",
                }
            ],
        )
        eval_payload = {
            "verdict": "clean",
            "summary": "agent-linter is clean against skills/arch-loop",
            "satisfied_requirements": [
                "skills/arch-loop passes $agent-linter"
            ],
            "unsatisfied_requirements": [],
            "required_skill_audits": [
                {
                    "skill": "agent-linter",
                    "status": "pass",
                    "evidence": "agent-linter run on skills/arch-loop SKILL.md returned 0 findings",
                }
            ],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "",
        }
        code, payload, state_path, _, _, saved = self._run(
            state=state,
            evaluator_results=[self._structured(eval_payload)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("clean", payload["stopReason"])
        self.assertIn(
            "agent-linter is clean against skills/arch-loop", payload["stopReason"]
        )
        self.assertFalse(state_path.exists())
        self.assertIsNone(saved)

    def test_agent_linter_obligation_clean_with_missing_evidence_rejected(self) -> None:
        # Same obligation, but the evaluator returns clean while leaving the
        # audit status=missing. The handler must reject the clean verdict, clear
        # state, and stop loud — proving the named-audit gate is real.
        state = self._state(
            required_skill_audits=[
                {
                    "skill": "agent-linter",
                    "target": "skills/arch-loop",
                    "requirement": "clean",
                    "status": "pending",
                }
            ],
        )
        eval_payload = {
            "verdict": "clean",
            "summary": "premature clean without audit evidence",
            "satisfied_requirements": ["skills/arch-loop ships"],
            "unsatisfied_requirements": [],
            "required_skill_audits": [
                {
                    "skill": "agent-linter",
                    "status": "missing",
                    "evidence": "no audit run recorded",
                }
            ],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "",
        }
        code, payload, state_path, _, _, saved = self._run(
            state=state,
            evaluator_results=[self._structured(eval_payload)],
        )
        self.assertEqual(code, 0)
        self.assertFalse(payload["continue"])
        self.assertIn("audit", payload["stopReason"])
        self.assertFalse(state_path.exists())
        self.assertIsNone(saved)


class ArchLoopPhase6ClaudeRuntimeProofTests(unittest.TestCase):
    """Phase 6 probe that the shared runner correctly resolves the Claude state
    namespace at .claude/arch_skill/arch-loop-state.<SESSION_ID>.json and runs
    the same handler end to end under Claude. The evaluator subprocess itself
    stays Codex by design; this test covers the Claude-host continuation path."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_arch_controller_stop_hook")
        cls.stop.ACTIVE_RUNTIME = cls.stop.HOOK_RUNTIME_SPECS[cls.stop.RUNTIME_CLAUDE]

    @classmethod
    def tearDownClass(cls) -> None:
        # Restore Codex as the default so subsequent test classes that pin
        # Codex in their own setUpClass do not race with this one.
        cls.stop.ACTIVE_RUNTIME = cls.stop.HOOK_RUNTIME_SPECS[cls.stop.RUNTIME_CODEX]

    def setUp(self) -> None:
        self._tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tempdir.cleanup)

    def test_claude_runtime_resolves_state_under_claude_arch_skill(self) -> None:
        repo_root = Path(self._tempdir.name).resolve()
        session_id = "session-phase6-claude"
        # Build the Claude-namespaced relative path and prove it lives under
        # `.claude/arch_skill/`, not `.codex/`.
        claude_relative = self.stop.controller_state_relative_path(
            self.stop.ARCH_LOOP_STATE_SPEC
        )
        self.assertEqual(claude_relative.parts[0], ".claude")
        self.assertEqual(claude_relative.parts[1], "arch_skill")
        suffixed = self.stop.session_state_relative_path(claude_relative, session_id)
        self.assertIn(session_id, suffixed.name)

        state = {
            "version": 1,
            "command": "arch-loop",
            "runtime": "claude",
            "session_id": session_id,
            "raw_requirements": "keep going until clean",
            "created_at": 1_000,
            "iteration_count": 0,
            "check_count": 0,
            "deadline_at": 10_000,
        }
        state_path = repo_root / suffixed
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

        eval_payload = {
            "verdict": "clean",
            "summary": "Claude runtime path probe satisfied",
            "satisfied_requirements": ["claude shared runner reachable"],
            "unsatisfied_requirements": [],
            "required_skill_audits": [],
            "continue_mode": "none",
            "next_task": "",
            "blocker": "",
        }
        result = self.stop.FreshStructuredResult(
            process=subprocess.CompletedProcess(
                args=["codex"], returncode=0, stdout="", stderr=""
            ),
            last_message=json.dumps(eval_payload),
            payload=eval_payload,
        )

        sleeps: list[int] = []
        fake_now = {"value": 2_000}

        def fake_eval(cwd, state_arg, repo_root_arg, prompt_text):
            return result

        def fake_time():
            return fake_now["value"]

        def fake_sleep(seconds: int):
            sleeps.append(seconds)
            fake_now["value"] += max(0, seconds)

        original_eval = self.stop.run_arch_loop_evaluator
        original_time = self.stop.current_epoch_seconds
        original_sleep = self.stop.sleep_for_seconds
        self.stop.run_arch_loop_evaluator = fake_eval
        self.stop.current_epoch_seconds = fake_time
        self.stop.sleep_for_seconds = fake_sleep

        stdout = io.StringIO()
        saved_stdout = sys.stdout
        sys.stdout = stdout
        try:
            with self.assertRaises(SystemExit) as raised:
                self.stop.handle_arch_loop(
                    {"cwd": str(repo_root), "session_id": session_id}
                )
        finally:
            self.stop.run_arch_loop_evaluator = original_eval
            self.stop.current_epoch_seconds = original_time
            self.stop.sleep_for_seconds = original_sleep
            sys.stdout = saved_stdout

        self.assertEqual(raised.exception.code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertFalse(payload["continue"])
        self.assertIn("clean", payload["stopReason"])
        # State file lived under `.claude/arch_skill/` and is now cleared.
        self.assertFalse(state_path.exists())


if __name__ == "__main__":
    unittest.main()
