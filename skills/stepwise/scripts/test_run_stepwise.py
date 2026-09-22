"""Regression tests for Stepwise deterministic plumbing.

Run: `python3 skills/stepwise/scripts/test_run_stepwise.py`
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_source_tags as cst  # noqa: E402
import run_stepwise as rs  # noqa: E402
import stepwise_learnings as sl  # noqa: E402


_PASS_VERDICT = {
    "step_n": 2,
    "verdict": "pass",
    "checks": [
        {
            "name": "artifact_exists",
            "status": "pass",
            "evidence": "file exists and header matches",
        }
    ],
    "observed_breach": None,
    "evidence_pointers": [],
    "contract_clauses_implicated": [],
    "summary": "Step 2 produced outline.md with the expected header.",
    "abstain_reason": None,
}

_RESULT_EVENT = {
    "type": "result",
    "subtype": "success",
    "is_error": False,
    "session_id": "aa86534c-57f3-4b99-8f34-c48821a3f327",
    "stop_reason": "end_turn",
    "result": "diagnostic answer",
    "structured_output": _PASS_VERDICT,
}

_STREAM_EVENTS = [
    {"type": "system", "subtype": "init", "session_id": "aa86534c-57f3-4b99-8f34-c48821a3f327"},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "..."}]}},
    {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read"}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "..."}]}},
    _RESULT_EVENT,
]


_PASS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": list(_PASS_VERDICT.keys()),
    "properties": {
        "step_n": {"type": "integer"},
        "verdict": {"enum": ["pass", "fail", "abstain"]},
        "checks": {"type": "array", "items": {"type": "object"}},
        "observed_breach": {"type": ["string", "null"]},
        "evidence_pointers": {"type": "array", "items": {"type": "string"}},
        "contract_clauses_implicated": {
            "type": "array",
            "items": {"type": "string"},
        },
        "summary": {"type": "string"},
        "abstain_reason": {"type": ["string", "null"]},
    },
}


def _stdout_from(obj) -> str:
    return "\n".join(["(prior lifecycle noise)", json.dumps(obj)])


class ClaudeShapeParsing(unittest.TestCase):
    def test_result_event_dict_passthrough(self):
        self.assertIs(rs._extract_claude_result_event(_RESULT_EVENT), _RESULT_EVENT)

    def test_result_event_list_shape(self):
        self.assertIs(rs._extract_claude_result_event(_STREAM_EVENTS), _RESULT_EVENT)

    def test_parse_session_id_from_dict_and_list(self):
        self.assertEqual(
            rs._parse_claude_session_id(_stdout_from(_RESULT_EVENT)),
            "aa86534c-57f3-4b99-8f34-c48821a3f327",
        )
        self.assertEqual(
            rs._parse_claude_session_id(_stdout_from(_STREAM_EVENTS)),
            "aa86534c-57f3-4b99-8f34-c48821a3f327",
        )

    def test_parse_session_id_ignores_trailing_stderr_noise(self):
        stdout = _stdout_from(_RESULT_EVENT) + "\nnon-json stderr warning\n"
        self.assertEqual(
            rs._parse_claude_session_id(stdout),
            "aa86534c-57f3-4b99-8f34-c48821a3f327",
        )
        self.assertEqual(rs._parse_claude_final_json(stdout), _RESULT_EVENT)

    def test_extract_verdict_from_final(self):
        self.assertEqual(rs._extract_verdict_from_final(_RESULT_EVENT), _PASS_VERDICT)
        self.assertEqual(rs._extract_verdict_from_final(_STREAM_EVENTS), _PASS_VERDICT)


class KimiShapeParsing(unittest.TestCase):
    def test_concatenates_assistant_content_and_uses_only_resume_hint_id(self):
        stdout = "\n".join(
            [
                "combined stderr noise",
                json.dumps(
                    {
                        "role": "meta",
                        "type": "unrelated",
                        "session_id": "wrong-session",
                    }
                ),
                json.dumps(
                    {
                        "role": "assistant",
                        "content": "first ",
                        "session_id": "also-wrong",
                    }
                ),
                json.dumps({"role": "tool", "content": "ignored"}),
                json.dumps({"role": "assistant", "content": "second"}),
                json.dumps(
                    {
                        "role": "meta",
                        "type": "session.resume_hint",
                        "session_id": "kimi-session-1",
                    }
                ),
            ]
        )

        self.assertEqual(
            rs._parse_kimi_final_json(stdout),
            {
                "type": "kimi_result",
                "result": "first second",
                "session_id": "kimi-session-1",
            },
        )
        self.assertEqual(rs._parse_kimi_session_id(stdout), "kimi-session-1")

    def test_final_text_without_resume_hint_is_valid_but_not_resumable(self):
        stdout = json.dumps({"role": "assistant", "content": "critic result"})

        self.assertEqual(
            rs._parse_kimi_final_json(stdout),
            {
                "type": "kimi_result",
                "result": "critic result",
                "session_id": None,
            },
        )
        self.assertIsNone(rs._parse_kimi_session_id(stdout))

    def test_rejects_explicit_errors_and_empty_or_missing_final_text(self):
        cases = {
            "no assistant": json.dumps(
                {
                    "role": "meta",
                    "type": "session.resume_hint",
                    "session_id": "kimi-session-1",
                }
            ),
            "empty assistant": json.dumps({"role": "assistant", "content": "  \n"}),
            "type error": "\n".join(
                [
                    json.dumps({"role": "assistant", "content": "partial"}),
                    json.dumps({"type": "error", "message": "failed"}),
                ]
            ),
            "role error": "\n".join(
                [
                    json.dumps({"role": "assistant", "content": "partial"}),
                    json.dumps({"role": "error", "content": "failed"}),
                ]
            ),
        }
        for label, stdout in cases.items():
            with self.subTest(label=label):
                self.assertIsNone(rs._parse_kimi_final_json(stdout))


class GrokShapeParsing(unittest.TestCase):
    def test_concatenates_text_and_captures_end_session(self):
        stdout = "\n".join(
            [
                "combined stderr noise",
                json.dumps(
                    {
                        "type": "text",
                        "data": "first ",
                        "sessionId": "wrong-session",
                    }
                ),
                json.dumps({"type": "thought", "data": "ignored"}),
                json.dumps({"type": "text", "data": "second"}),
                json.dumps({"type": "end", "sessionId": "grok-session-1"}),
            ]
        )

        self.assertEqual(
            rs._parse_grok_final_json(stdout),
            {
                "type": "grok_result",
                "result": "first second",
                "session_id": "grok-session-1",
            },
        )

    def test_rejects_errors_session_only_and_empty_text(self):
        cases = {
            "error": "\n".join(
                [
                    json.dumps({"type": "text", "data": "partial"}),
                    json.dumps({"type": "error", "data": "failed"}),
                    json.dumps({"type": "end", "sessionId": "grok-session-1"}),
                ]
            ),
            "session only": json.dumps(
                {"type": "end", "sessionId": "grok-session-1"}
            ),
            "empty text": "\n".join(
                [
                    json.dumps({"type": "text", "data": "  \n"}),
                    json.dumps({"type": "end", "sessionId": "grok-session-1"}),
                ]
            ),
            "noise only": "not json\nstill not json\n",
        }
        for label, stdout in cases.items():
            with self.subTest(label=label):
                self.assertIsNone(rs._parse_grok_final_json(stdout))


class StepVerdictValidation(unittest.TestCase):
    def test_valid_observational_pass(self):
        self.assertEqual(rs._validate_step_verdict(_PASS_VERDICT), [])

    def test_valid_observational_fail(self):
        verdict = {
            "step_n": 3,
            "verdict": "fail",
            "checks": [
                {
                    "name": "skill_order_adherence",
                    "status": "fail",
                    "evidence": "owner runbook read happened after write",
                }
            ],
            "observed_breach": "The worker edited before owner-doctrine evidence was loaded.",
            "evidence_pointers": ["steps/3/try-1/stream.log"],
            "contract_clauses_implicated": ["owner SKILL.md: read doctrine before edit"],
            "summary": "The attempt failed doctrine order.",
            "abstain_reason": None,
        }
        self.assertEqual(rs._validate_step_verdict(verdict), [])

    def test_stale_resume_hint_is_rejected(self):
        verdict = dict(_PASS_VERDICT)
        verdict["resume_hint"] = {"headline": "old", "required_fixes": [], "do_not_redo": []}
        errors = rs._validate_step_verdict(verdict)
        self.assertTrue(any("resume_hint is no longer accepted" in e for e in errors))

    def test_stale_route_to_step_is_rejected(self):
        verdict = dict(_PASS_VERDICT)
        verdict["route_to_step_n"] = 1
        errors = rs._validate_step_verdict(verdict)
        self.assertTrue(any("route_to_step_n is no longer accepted" in e for e in errors))

    def test_fail_requires_observation_evidence_and_clause(self):
        verdict = {
            "step_n": 2,
            "verdict": "fail",
            "checks": [],
            "observed_breach": "",
            "evidence_pointers": [],
            "contract_clauses_implicated": [],
            "summary": "Failed.",
            "abstain_reason": None,
        }
        errors = rs._validate_step_verdict(verdict)
        self.assertIn("observed_breach must be null or a non-empty string", errors)
        self.assertIn("observed_breach must be a non-empty string on fail", errors)
        self.assertIn("evidence_pointers must be non-empty on fail", errors)
        self.assertIn("contract_clauses_implicated must be non-empty on fail", errors)


class SubprocessRunner(unittest.TestCase):
    def test_run_subprocess_captures_combined_output(self):
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            stream_path = out_dir / "stream.log"
            code, stdout_text = rs._run_subprocess(
                [
                    sys.executable,
                    "-c",
                    "import sys; print('stdout-line'); print('stderr-line', file=sys.stderr)",
                ],
                stream_path,
                out_dir,
            )

            self.assertEqual(code, 0)
            self.assertIn("stdout-line", stdout_text)
            self.assertIn("stderr-line", stdout_text)
            self.assertEqual(stream_path.read_text(encoding="utf-8"), stdout_text)
            self.assertEqual((out_dir / "exit_code").read_text(encoding="utf-8"), "0\n")


class ClaudeInvocationFlags(unittest.TestCase):
    def _run_and_capture_argv(self, args_list: list[str]) -> list[str]:
        old_run_subprocess = rs._run_subprocess
        captured: dict[str, list[str]] = {}

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            captured["argv"] = argv
            stdout = json.dumps(_RESULT_EVENT)
            stdout_stream_path.write_text(stdout, encoding="utf-8")
            return 0, stdout

        parser = rs._build_parser()
        args = parser.parse_args(args_list)
        try:
            rs._run_subprocess = fake_run
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(args.func(args), 0)
        finally:
            rs._run_subprocess = old_run_subprocess
        return captured["argv"]

    def assert_claude_stream_json_verbose(self, argv: list[str]) -> None:
        self.assertIn("--output-format", argv)
        self.assertIn("stream-json", argv)
        self.assertEqual(argv[argv.index("stream-json") + 1], "--verbose")

    def test_step_spawn_adds_verbose_to_claude_stream_json(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "prompt.md"
            prompt.write_text("do the step\n", encoding="utf-8")

            argv = self._run_and_capture_argv(
                [
                    "step-spawn",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "haiku",
                    "--effort", "low",
                    "--runtime", "claude",
                    "--step-n", "1",
                    "--try-k", "1",
                ]
            )

        self.assert_claude_stream_json_verbose(argv)

    def test_step_resume_adds_verbose_to_claude_stream_json(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "repair.md"
            prompt.write_text("repair the step\n", encoding="utf-8")

            argv = self._run_and_capture_argv(
                [
                    "step-resume",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "haiku",
                    "--effort", "low",
                    "--runtime", "claude",
                    "--step-n", "1",
                    "--try-k", "2",
                    "--session-id", "session-1",
                ]
            )

        self.assert_claude_stream_json_verbose(argv)

    def test_step_diagnose_adds_verbose_to_claude_stream_json(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "diagnose.md"
            prompt.write_text("diagnose the step\n", encoding="utf-8")

            argv = self._run_and_capture_argv(
                [
                    "step-diagnose",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "haiku",
                    "--effort", "low",
                    "--runtime", "claude",
                    "--step-n", "1",
                    "--try-k", "2",
                    "--session-id", "session-1",
                    "--round-k", "1",
                    "--with-step-m", "1",
                ]
            )

        self.assert_claude_stream_json_verbose(argv)

    def test_critic_spawn_adds_verbose_to_claude_stream_json(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "critic.md"
            prompt.write_text("judge the step\n", encoding="utf-8")
            schema_file = root / "schema.json"
            schema_file.write_text(
                json.dumps(
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": list(_PASS_VERDICT.keys()),
                        "properties": {
                            "step_n": {"type": "integer"},
                            "verdict": {"enum": ["pass", "fail", "abstain"]},
                            "checks": {"type": "array", "items": {"type": "object"}},
                            "observed_breach": {"type": ["string", "null"]},
                            "evidence_pointers": {"type": "array", "items": {"type": "string"}},
                            "contract_clauses_implicated": {"type": "array", "items": {"type": "string"}},
                            "summary": {"type": "string"},
                            "abstain_reason": {"type": ["string", "null"]},
                        },
                    }
                ),
                encoding="utf-8",
            )

            argv = self._run_and_capture_argv(
                [
                    "critic-spawn",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "haiku",
                    "--effort", "low",
                    "--runtime", "claude",
                    "--schema-file", str(schema_file),
                    "--step-n", "1",
                    "--try-k", "1",
                ]
            )

        self.assert_claude_stream_json_verbose(argv)


class KimiInvocationFlags(unittest.TestCase):
    @staticmethod
    def _kimi_stdout(
        result: str,
        session_id: str | None = "kimi-session-new",
    ) -> str:
        events = [
            "combined stderr warning",
            json.dumps({"role": "assistant", "content": result}),
        ]
        if session_id is not None:
            events.append(
                json.dumps(
                    {
                        "role": "meta",
                        "type": "session.resume_hint",
                        "session_id": session_id,
                    }
                )
            )
        return "\n".join(events)

    def _run_and_capture(
        self,
        args_list: list[str],
        *,
        result: str,
        session_id: str | None = "kimi-session-new",
        expected_exit: int | None = None,
    ) -> dict[str, object]:
        old_run_subprocess = rs._run_subprocess
        captured: dict[str, object] = {}

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            captured["argv"] = argv
            captured["cwd"] = cwd
            captured["stamp_prefix"] = stamp_prefix
            stdout = self._kimi_stdout(result, session_id)
            stdout_stream_path.write_text(stdout, encoding="utf-8")
            return 0, stdout

        parser = rs._build_parser()
        args = parser.parse_args(args_list)
        try:
            rs._run_subprocess = fake_run
            with (
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                if expected_exit is None:
                    self.assertEqual(args.func(args), 0)
                else:
                    with self.assertRaises(SystemExit) as raised:
                        args.func(args)
                    self.assertEqual(raised.exception.code, expected_exit)
        finally:
            rs._run_subprocess = old_run_subprocess
        return captured

    def test_step_spawn_uses_exact_argv_and_preserves_shell_metacharacters(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "prompt.md"
            prompt_text = "do $(touch nope); `echo bad` '$HOME' \"quoted\"\nnext line\n"
            prompt.write_text(prompt_text, encoding="utf-8")

            captured = self._run_and_capture(
                [
                    "step-spawn",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "kimi-code/k3",
                    "--effort", "max",
                    "--runtime", "kimi",
                    "--step-n", "1",
                    "--try-k", "1",
                ],
                result="completed",
            )

            self.assertEqual(
                captured["argv"],
                [
                    "env",
                    "KIMI_CODE_NO_AUTO_UPDATE=1",
                    "KIMI_MODEL_THINKING_EFFORT=max",
                    "kimi",
                    "-m",
                    "kimi-code/k3",
                    "-p",
                    prompt_text,
                    "--output-format",
                    "stream-json",
                ],
            )
            self.assertEqual(captured["cwd"], str(target.resolve()))
            final = json.loads(
                (run_dir / "steps" / "1" / "try-1" / "stdout.final.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(final["result"], "completed")
            self.assertEqual(final["session_id"], "kimi-session-new")
            self.assertEqual(
                (run_dir / "steps" / "1" / "try-1" / "session_id.txt").read_text(
                    encoding="utf-8"
                ),
                "kimi-session-new\n",
            )

    def test_step_resume_uses_exact_session_and_refreshes_receipts(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "repair.md"
            prompt.write_text("repair the step\n", encoding="utf-8")

            captured = self._run_and_capture(
                [
                    "step-resume",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "kimi-code/k3",
                    "--effort", "high",
                    "--runtime", "kimi",
                    "--step-n", "1",
                    "--try-k", "2",
                    "--session-id", "kimi-session-old",
                ],
                result="repaired",
                session_id="kimi-session-refreshed",
            )

            self.assertEqual(
                captured["argv"],
                [
                    "env",
                    "KIMI_CODE_NO_AUTO_UPDATE=1",
                    "KIMI_MODEL_THINKING_EFFORT=high",
                    "kimi",
                    "-r",
                    "kimi-session-old",
                    "-m",
                    "kimi-code/k3",
                    "-p",
                    "repair the step\n",
                    "--output-format",
                    "stream-json",
                ],
            )
            self.assertNotIn("-c", captured["argv"])
            self.assertEqual(captured["cwd"], str(target.resolve()))
            try_dir = run_dir / "steps" / "1" / "try-2"
            self.assertEqual(
                (try_dir / "session_id.txt").read_text(encoding="utf-8"),
                "kimi-session-refreshed\n",
            )
            self.assertEqual(
                json.loads((try_dir / "stdout.final.json").read_text(encoding="utf-8"))[
                    "result"
                ],
                "repaired",
            )

    def test_step_diagnose_resumes_in_target_cwd_and_writes_response(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "diagnose.md"
            prompt.write_text("diagnose only\n", encoding="utf-8")

            captured = self._run_and_capture(
                [
                    "step-diagnose",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "kimi-code/k3",
                    "--effort", "low",
                    "--runtime", "kimi",
                    "--step-n", "2",
                    "--try-k", "1",
                    "--session-id", "kimi-session-2",
                    "--round-k", "3",
                    "--with-step-m", "1",
                ],
                result="diagnostic response",
                session_id="kimi-session-2",
            )

            self.assertEqual(
                captured["argv"],
                [
                    "env",
                    "KIMI_CODE_NO_AUTO_UPDATE=1",
                    "KIMI_MODEL_THINKING_EFFORT=low",
                    "kimi",
                    "-r",
                    "kimi-session-2",
                    "-m",
                    "kimi-code/k3",
                    "-p",
                    "diagnose only\n",
                    "--output-format",
                    "stream-json",
                ],
            )
            self.assertEqual(captured["cwd"], str(target.resolve()))
            self.assertEqual(captured["stamp_prefix"], "turn-3.with-step-1")
            diag_dir = run_dir / "steps" / "2" / "try-1" / "diagnostic"
            self.assertEqual(
                (diag_dir / "turn-3.with-step-1.response.md").read_text(
                    encoding="utf-8"
                ),
                "diagnostic response",
            )
            self.assertEqual(
                (diag_dir / "turn-3.with-step-1.session_id.txt").read_text(
                    encoding="utf-8"
                ),
                "kimi-session-2\n",
            )

    def test_continuation_commands_require_a_fresh_resume_hint(self):
        for command in ("step-spawn", "step-resume", "step-diagnose"):
            with self.subTest(command=command), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                run_dir = root / "run"
                target = root / "target"
                run_dir.mkdir()
                target.mkdir()
                (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
                prompt = root / "prompt.md"
                prompt.write_text("turn without hint\n", encoding="utf-8")
                args_list = [
                    command,
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "kimi-code/k3",
                    "--effort", "max",
                    "--runtime", "kimi",
                    "--step-n", "1",
                    "--try-k", "1",
                ]
                if command in {"step-resume", "step-diagnose"}:
                    args_list.extend(["--session-id", "kimi-session-old"])
                if command == "step-diagnose":
                    args_list.extend(["--round-k", "1", "--with-step-m", "1"])

                captured = self._run_and_capture(
                    args_list,
                    result="completed without receipt",
                    session_id=None,
                    expected_exit=4,
                )

                if command == "step-diagnose":
                    receipt_path = (
                        run_dir
                        / "steps"
                        / "1"
                        / "try-1"
                        / "diagnostic"
                        / "turn-1.with-step-1.session_id.txt"
                    )
                else:
                    receipt_path = (
                        run_dir / "steps" / "1" / "try-1" / "session_id.txt"
                    )
                self.assertEqual(
                    receipt_path.read_text(encoding="utf-8"),
                    "UNRECOVERABLE\n",
                )
                if command == "step-resume":
                    origin = json.loads(
                        (
                            run_dir / "steps" / "1" / "try-1" / "origin.json"
                        ).read_text(encoding="utf-8")
                    )
                    self.assertEqual(origin["session_id"], "UNRECOVERABLE")
                if command == "step-spawn":
                    self.assertNotIn("-r", captured["argv"])
                else:
                    self.assertIn("-r", captured["argv"])

    def test_critic_inlines_schema_and_writes_verdict_receipts(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "critic.md"
            prompt.write_text("judge the step\n", encoding="utf-8")
            schema_file = root / "schema.json"
            schema_file.write_text(json.dumps(_PASS_SCHEMA), encoding="utf-8")

            captured = self._run_and_capture(
                [
                    "critic-spawn",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "kimi-code/k3",
                    "--effort", "max",
                    "--runtime", "kimi",
                    "--schema-file", str(schema_file),
                    "--step-n", "4",
                    "--try-k", "1",
                ],
                result=json.dumps(_PASS_VERDICT),
                session_id=None,
            )

            argv = captured["argv"]
            self.assertIsInstance(argv, list)
            submitted_prompt = argv[argv.index("-p") + 1]
            self.assertIn("judge the step", submitted_prompt)
            self.assertIn("## JSON Schema", submitted_prompt)
            self.assertIn(
                json.dumps(_PASS_SCHEMA, indent=2, sort_keys=True),
                submitted_prompt,
            )
            self.assertNotIn("--json-schema", argv)
            self.assertEqual(captured["cwd"], str(target.resolve()))
            critic_dir = run_dir / "steps" / "4" / "try-1" / "critic"
            self.assertEqual(
                (critic_dir / "prompt.kimi.md").read_text(encoding="utf-8"),
                submitted_prompt,
            )
            self.assertEqual(
                json.loads((critic_dir / "verdict.json").read_text(encoding="utf-8")),
                _PASS_VERDICT,
            )
            self.assertEqual(
                json.loads(
                    (critic_dir / "stdout.final.json").read_text(encoding="utf-8")
                )["type"],
                "kimi_result",
            )


class CodexProfileInvocationFlags(unittest.TestCase):
    def _capture_step_spawn_argv(self, args_list: list[str]) -> list[str]:
        old_run_subprocess = rs._run_subprocess
        captured: dict[str, list[str]] = {}

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            captured["argv"] = argv
            stdout = json.dumps({"type": "thread.started", "thread_id": "thread-1"})
            stdout_stream_path.write_text(stdout, encoding="utf-8")
            return 0, stdout

        parser = rs._build_parser()
        args = parser.parse_args(args_list)
        try:
            rs._run_subprocess = fake_run
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(args.func(args), 0)
        finally:
            rs._run_subprocess = old_run_subprocess
        return captured["argv"]

    def _capture_critic_spawn_argv(self, args_list: list[str]) -> list[str]:
        old_run_subprocess = rs._run_subprocess
        captured: dict[str, list[str]] = {}

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            captured["argv"] = argv
            final_path = Path(argv[argv.index("-o") + 1])
            final_path.write_text(json.dumps(_PASS_VERDICT), encoding="utf-8")
            stdout_stream_path.write_text("", encoding="utf-8")
            return 0, ""

        parser = rs._build_parser()
        args = parser.parse_args(args_list)
        try:
            rs._run_subprocess = fake_run
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(args.func(args), 0)
        finally:
            rs._run_subprocess = old_run_subprocess
        return captured["argv"]

    def test_step_spawn_uses_codex_profile_for_fugu_default_effort(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "prompt.md"
            prompt.write_text("do the step\n", encoding="utf-8")

            argv = self._capture_step_spawn_argv(
                [
                    "step-spawn",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "fugu-ultra",
                    "--effort", "xhigh",
                    "--runtime", "codex",
                    "--codex-profile", "fugu-ultra",
                    "--step-n", "1",
                    "--try-k", "1",
                ]
            )

        self.assertIn("-p", argv)
        self.assertIn("fugu-ultra", argv)
        self.assertNotIn("--model", argv)
        self.assertNotIn('model_reasoning_effort="xhigh"', argv)

    def test_step_spawn_can_override_codex_profile_effort(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "prompt.md"
            prompt.write_text("do the step\n", encoding="utf-8")

            argv = self._capture_step_spawn_argv(
                [
                    "step-spawn",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "fugu-ultra",
                    "--effort", "high",
                    "--runtime", "codex",
                    "--codex-profile", "fugu-ultra",
                    "--step-n", "1",
                    "--try-k", "1",
                ]
            )

        self.assertIn("-p", argv)
        self.assertIn("fugu-ultra", argv)
        self.assertNotIn("--model", argv)
        self.assertIn('model_reasoning_effort="high"', argv)

    def test_critic_spawn_uses_codex_profile_for_fugu(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "run"
            target = root / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = root / "critic.md"
            prompt.write_text("judge the step\n", encoding="utf-8")
            schema_file = root / "schema.json"
            schema_file.write_text(json.dumps({"type": "object"}), encoding="utf-8")

            argv = self._capture_critic_spawn_argv(
                [
                    "critic-spawn",
                    "--run-dir", str(run_dir),
                    "--target-repo", str(target),
                    "--prompt-file", str(prompt),
                    "--model", "fugu-ultra",
                    "--effort", "xhigh",
                    "--runtime", "codex",
                    "--codex-profile", "fugu-ultra",
                    "--schema-file", str(schema_file),
                    "--step-n", "1",
                    "--try-k", "1",
                ]
            )

        self.assertIn("--ephemeral", argv)
        self.assertIn("-p", argv)
        self.assertIn("fugu-ultra", argv)
        self.assertNotIn("--model", argv)


class CodexSchemaNormalization(unittest.TestCase):
    def test_optional_schema_fields_become_required_nullable(self):
        schema = {
            "type": "object",
            "required": ["step_n", "verdict", "checks", "summary"],
            "properties": {
                "step_n": {"type": "integer"},
                "verdict": {"enum": ["pass", "fail", "abstain"]},
                "checks": {"type": "array", "items": {"type": "object", "properties": {}}},
                "observed_breach": {"type": "string"},
                "evidence_pointers": {"type": "array", "items": {"type": "string"}},
                "contract_clauses_implicated": {"type": "array", "items": {"type": "string"}},
                "summary": {"type": "string"},
                "abstain_reason": {"type": "string"},
            },
        }
        normalized = rs._codex_strict_schema(schema)
        self.assertEqual(set(normalized["required"]), set(normalized["properties"]))
        self.assertEqual(
            normalized["properties"]["observed_breach"]["type"],
            ["string", "null"],
        )
        self.assertEqual(
            normalized["properties"]["abstain_reason"]["type"],
            ["string", "null"],
        )

    def test_critic_spawn_uses_observational_schema(self):
        old_run_subprocess = rs._run_subprocess
        captured = {}

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            schema_path = Path(argv[argv.index("--output-schema") + 1])
            final_path = Path(argv[argv.index("-o") + 1])
            final_path.write_text(json.dumps(_PASS_VERDICT), encoding="utf-8")
            captured["schema_path"] = schema_path
            return 0, ""

        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": list(_PASS_VERDICT.keys()),
            "properties": {
                "step_n": {"type": "integer"},
                "verdict": {"enum": ["pass", "fail", "abstain"]},
                "checks": {"type": "array", "items": {"type": "object", "properties": {}}},
                "observed_breach": {"type": ["string", "null"]},
                "evidence_pointers": {"type": "array", "items": {"type": "string"}},
                "contract_clauses_implicated": {"type": "array", "items": {"type": "string"}},
                "summary": {"type": "string"},
                "abstain_reason": {"type": ["string", "null"]},
            },
        }

        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run"
            target = Path(td) / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = Path(td) / "prompt.md"
            prompt.write_text("judge step\n", encoding="utf-8")
            schema_file = Path(td) / "schema.json"
            schema_file.write_text(json.dumps(schema), encoding="utf-8")

            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "critic-spawn",
                    "--run-dir",
                    str(run_dir),
                    "--target-repo",
                    str(target),
                    "--prompt-file",
                    str(prompt),
                    "--model",
                    "gpt-6-sol",
                    "--effort",
                    "high",
                    "--schema-file",
                    str(schema_file),
                    "--runtime",
                    "codex",
                    "--step-n",
                    "1",
                    "--try-k",
                    "1",
                ]
            )

            try:
                rs._run_subprocess = fake_run
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(args.func(args), 0)
            finally:
                rs._run_subprocess = old_run_subprocess

            normalized = json.loads(captured["schema_path"].read_text(encoding="utf-8"))

        self.assertEqual(set(normalized["required"]), set(normalized["properties"]))
        self.assertNotIn("resume_hint", normalized["properties"])


class InitRunAndPromptArtifacts(unittest.TestCase):
    def test_init_run_narrows_gitignore_and_stores_diagnostic_cap(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "orchestrator"
            target = Path(td) / "target"
            root.mkdir()
            target.mkdir()
            (root / ".gitignore").write_text(".arch_skill/\n", encoding="utf-8")
            raw = Path(td) / "raw.txt"
            raw.write_text("run process\n", encoding="utf-8")
            execution = {
                "schema_version": 2,
                "execution_defaults": {
                    "step": {
                        "runtime": "codex",
                        "model": "gpt-6-sol",
                        "effort": "high",
                        "source": "user",
                    },
                    "critic": {
                        "runtime": "codex",
                        "model": "gpt-5.4-mini",
                        "effort": "high",
                        "source": "user",
                    },
                },
                "execution_preferences": [],
            }
            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "init-run",
                    "--orchestrator-root",
                    str(root),
                    "--target-repo",
                    str(target),
                    "--raw-instructions-file",
                    str(raw),
                    "--profile",
                    "balanced",
                    "--stop-discipline",
                    "halt_and_ask",
                    "--per-step-retry-cap",
                    "5",
                    "--execution-json",
                    json.dumps(execution),
                ]
            )
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(args.func(args), 0)
            [run_dir] = list((root / ".arch_skill" / "stepwise" / "runs").iterdir())
            state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
            gitignore = (root / ".gitignore").read_text(encoding="utf-8")

        self.assertEqual(state["diagnostic_turn_cap"], 10)
        self.assertIn(".arch_skill/stepwise/runs/", gitignore)
        self.assertNotIn(".arch_skill/\n", gitignore)

    def test_step_spawn_saves_prompt(self):
        old_run_subprocess = rs._run_subprocess

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            payload = dict(_RESULT_EVENT)
            stdout = json.dumps(payload)
            stdout_stream_path.write_text(stdout, encoding="utf-8")
            return 0, stdout

        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run"
            target = Path(td) / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = Path(td) / "prompt.md"
            prompt.write_text("do the step\n", encoding="utf-8")
            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "step-spawn",
                    "--run-dir",
                    str(run_dir),
                    "--target-repo",
                    str(target),
                    "--prompt-file",
                    str(prompt),
                    "--model",
                    "haiku",
                    "--effort",
                    "low",
                    "--runtime",
                    "claude",
                    "--step-n",
                    "1",
                    "--try-k",
                    "1",
                ]
            )
            try:
                rs._run_subprocess = fake_run
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(args.func(args), 0)
            finally:
                rs._run_subprocess = old_run_subprocess

            self.assertEqual(
                (run_dir / "steps" / "1" / "try-1" / "prompt.md").read_text(encoding="utf-8"),
                "do the step\n",
            )
            origin = json.loads(
                (run_dir / "steps" / "1" / "try-1" / "origin.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(origin["kind"], "fresh")
            self.assertEqual(origin["session_mode"], "fresh-session")
            self.assertFalse(origin["consumes_repair_bounce"])

    def test_step_resume_records_repair_origin(self):
        old_run_subprocess = rs._run_subprocess

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            payload = dict(_RESULT_EVENT)
            stdout = json.dumps(payload)
            stdout_stream_path.write_text(stdout, encoding="utf-8")
            return 0, stdout

        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run"
            target = Path(td) / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = Path(td) / "repair.md"
            prompt.write_text("repair the step\n", encoding="utf-8")
            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "step-resume",
                    "--run-dir",
                    str(run_dir),
                    "--target-repo",
                    str(target),
                    "--prompt-file",
                    str(prompt),
                    "--model",
                    "haiku",
                    "--effort",
                    "low",
                    "--runtime",
                    "claude",
                    "--step-n",
                    "1",
                    "--try-k",
                    "2",
                    "--session-id",
                    "session-1",
                    "--origin-trigger-json",
                    '{"diagnostic_path":"steps/1/try-1/diagnostic/root-cause.md"}',
                ]
            )
            try:
                rs._run_subprocess = fake_run
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(args.func(args), 0)
            finally:
                rs._run_subprocess = old_run_subprocess

            origin = json.loads(
                (run_dir / "steps" / "1" / "try-2" / "origin.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(origin["kind"], "repair-resume")
            self.assertEqual(origin["session_mode"], "same-session")
            self.assertTrue(origin["consumes_repair_bounce"])
            self.assertEqual(
                origin["triggered_by"]["diagnostic_path"],
                "steps/1/try-1/diagnostic/root-cause.md",
            )

    def test_step_spawn_records_respawn_origin(self):
        old_run_subprocess = rs._run_subprocess

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            payload = dict(_RESULT_EVENT)
            stdout = json.dumps(payload)
            stdout_stream_path.write_text(stdout, encoding="utf-8")
            return 0, stdout

        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run"
            target = Path(td) / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = Path(td) / "prompt.md"
            prompt.write_text("fresh downstream\n", encoding="utf-8")
            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "step-spawn",
                    "--run-dir",
                    str(run_dir),
                    "--target-repo",
                    str(target),
                    "--prompt-file",
                    str(prompt),
                    "--model",
                    "haiku",
                    "--effort",
                    "low",
                    "--runtime",
                    "claude",
                    "--step-n",
                    "5",
                    "--try-k",
                    "2",
                    "--origin-kind",
                    "respawn-after-upstream",
                    "--origin-trigger-json",
                    '{"upstream_step_n":4,"diagnostic_path":"steps/5/try-1/diagnostic/root-cause.md"}',
                ]
            )
            try:
                rs._run_subprocess = fake_run
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(args.func(args), 0)
            finally:
                rs._run_subprocess = old_run_subprocess

            origin = json.loads(
                (run_dir / "steps" / "5" / "try-2" / "origin.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(origin["kind"], "respawn-after-upstream")
            self.assertFalse(origin["consumes_repair_bounce"])


class MetadataHelpers(unittest.TestCase):
    def test_latest_session_and_upstream_for_report_exact_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run"
            run_dir.mkdir()
            (run_dir / "state.json").write_text(
                json.dumps(
                    {
                        "run_id": "run-1",
                        "target_repo_path": str(Path(td) / "target"),
                        "profile": "strict",
                    }
                ),
                encoding="utf-8",
            )
            artifact = str(Path(td) / "target" / "outline.md")
            manifest = {
                "target_process": "Demo process",
                "steps": [
                    {
                        "n": 1,
                        "label": "Write outline",
                        "inputs": [],
                        "expected_artifact": {"selector": artifact},
                    },
                    {
                        "n": 2,
                        "label": "Use outline",
                        "inputs": [f"source: {artifact}", "source: /not/produced.md"],
                        "expected_artifact": {"selector": str(Path(td) / "target" / "brief.md")},
                    },
                ],
            }
            rs._write_json(run_dir / "manifest.json", manifest)
            tdir = run_dir / "steps" / "1" / "try-1"
            tdir.mkdir(parents=True)
            (tdir / "session_id.txt").write_text("session-1\n", encoding="utf-8")
            rs._write_json(
                tdir / "origin.json",
                {
                    "kind": "fresh",
                    "consumes_repair_bounce": False,
                    "session_mode": "fresh-session",
                },
            )

            parser = rs._build_parser()
            latest_args = parser.parse_args(
                ["latest-session", "--run-dir", str(run_dir), "--step-n", "1"]
            )
            with contextlib.redirect_stdout(io.StringIO()) as latest_out:
                self.assertEqual(latest_args.func(latest_args), 0)
            latest = json.loads(latest_out.getvalue())
            self.assertEqual(latest["session_id"], "session-1")
            self.assertEqual(latest["origin_kind"], "fresh")

            upstream_args = parser.parse_args(
                ["upstream-for", "--run-dir", str(run_dir), "--step-n", "2"]
            )
            with contextlib.redirect_stdout(io.StringIO()) as upstream_out:
                self.assertEqual(upstream_args.func(upstream_args), 0)
            upstream = json.loads(upstream_out.getvalue())
            self.assertEqual(upstream["matches"][0]["upstream_step_n"], 1)
            self.assertEqual(upstream["matches"][0]["session_id"], "session-1")
            self.assertEqual(upstream["unmatched"][0]["reason"], "no matching expected_artifact.selector")

            report_args = parser.parse_args(
                ["report-scaffold", "--run-dir", str(run_dir)]
            )
            with contextlib.redirect_stdout(io.StringIO()) as report_out:
                self.assertEqual(report_args.func(report_args), 0)
            report = report_out.getvalue()
            self.assertIn("## Per-step Status", report)
            self.assertIn("Write outline", report)


class DiagnosticCommand(unittest.TestCase):
    def test_step_diagnose_writes_diagnostic_turn_without_new_try(self):
        old_run_subprocess = rs._run_subprocess

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            final_path = Path(argv[argv.index("-o") + 1])
            final_path.write_text("I understand the issue.\n", encoding="utf-8")
            stdout_stream_path.write_text(
                '{"type":"thread.started","thread_id":"thread-1"}\n',
                encoding="utf-8",
            )
            return 0, '{"type":"thread.started","thread_id":"thread-1"}\n'

        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run"
            target = Path(td) / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            (run_dir / "steps" / "6" / "try-1").mkdir(parents=True)
            prompt = Path(td) / "diag.md"
            prompt.write_text("Diagnostic conversation only.\n", encoding="utf-8")
            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "step-diagnose",
                    "--run-dir",
                    str(run_dir),
                    "--target-repo",
                    str(target),
                    "--prompt-file",
                    str(prompt),
                    "--model",
                    "gpt-6-sol",
                    "--effort",
                    "high",
                    "--session-id",
                    "thread-1",
                    "--runtime",
                    "codex",
                    "--step-n",
                    "6",
                    "--try-k",
                    "1",
                    "--round-k",
                    "2",
                    "--with-step-m",
                    "4",
                ]
            )
            try:
                rs._run_subprocess = fake_run
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(args.func(args), 0)
            finally:
                rs._run_subprocess = old_run_subprocess

            diag = run_dir / "steps" / "6" / "try-1" / "diagnostic"
            self.assertTrue((diag / "turn-2.with-step-4.prompt.md").is_file())
            self.assertTrue((diag / "turn-2.with-step-4.response.md").is_file())
            self.assertFalse((run_dir / "steps" / "6" / "try-2").exists())


class SourceTagChecker(unittest.TestCase):
    def test_numbered_repair_steps_require_source_tags(self):
        with tempfile.TemporaryDirectory() as td:
            good = Path(td) / "good.md"
            bad = Path(td) / "bad.md"
            good.write_text("1. Do thing. [source: manifest]\n", encoding="utf-8")
            bad.write_text("1. Do thing.\n", encoding="utf-8")
            self.assertEqual(cst.check_file(good), [])
            self.assertEqual(len(cst.check_file(bad)), 1)

    def test_evidence_and_diagnosis_are_not_operational_authority(self):
        with tempfile.TemporaryDirectory() as td:
            for tag in ("critic evidence", "confirmed diagnosis"):
                prompt = Path(td) / f"{tag.replace(' ', '-')}.md"
                prompt.write_text(
                    f"1. Apply the proposed repair. [source: {tag}]\n",
                    encoding="utf-8",
                )
                self.assertEqual(len(cst.check_file(prompt)), 1, tag)

    def test_hard_boundary_bullets_require_source_tags_but_evidence_does_not(self):
        with tempfile.TemporaryDirectory() as td:
            good = Path(td) / "good.md"
            bad = Path(td) / "bad.md"
            good.write_text(
                "\n".join(
                    [
                        "## Hard boundaries",
                        "- Stay in this step. [source: manifest]",
                        "",
                        "## Evidence to leave",
                        "- scan result",
                    ]
                ),
                encoding="utf-8",
            )
            bad.write_text(
                "\n".join(
                    [
                        "## Hard boundaries",
                        "- Stay in this step.",
                        "",
                        "## Evidence to leave",
                        "- scan result",
                    ]
                ),
                encoding="utf-8",
            )
            self.assertEqual(cst.check_file(good), [])
            self.assertEqual(len(cst.check_file(bad)), 1)


class LearningLedger(unittest.TestCase):
    def _entry(self) -> dict:
        return {
            "schema_version": 1,
            "source": {
                "run_id": "run-1",
                "step_n": 6,
                "try_k": 1,
                "diagnostic_path": "steps/6/try-1/diagnostic/",
            },
            "scope": {
                "owner_skill": "$lesson-copy-discipline",
                "failure_class": "copy-gate",
                "surface": "copy",
                "support_skills": [],
            },
            "observation": "Worker treated placeholder cleanup as non-copy.",
            "underlying_principle": "Learner-visible placeholder cleanup is copy work.",
            "applicability_test": "Apply when a worker inserts learner-visible copy.",
            "contraindications": "Do not apply to non-visible metadata cleanup.",
            "process_change_suggestion": "Ask the worker whether it made a copy exception.",
            "promotion_target": "skills/stepwise/references/examples.md",
        }

    def test_append_is_idempotent_and_transition_updates_status(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "learnings"
            entry_file = Path(td) / "entry.json"
            entry_file.write_text(json.dumps(self._entry()), encoding="utf-8")

            parser = sl._build_parser()
            append_args = parser.parse_args(
                ["--root", str(root), "append", "--entry-file", str(entry_file)]
            )
            with contextlib.redirect_stdout(io.StringIO()) as out1:
                self.assertEqual(append_args.func(append_args), 0)
            first_id = out1.getvalue().strip()
            with contextlib.redirect_stdout(io.StringIO()) as out2:
                self.assertEqual(append_args.func(append_args), 0)
            self.assertEqual(out2.getvalue().strip(), first_id)

            accept_args = parser.parse_args(["--root", str(root), "accept", first_id])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(accept_args.func(accept_args), 0)

            events = sl._current_by_id(sl._events(root))
            self.assertEqual(events[first_id]["status"], "accepted")

    def test_append_rejects_empty_scope(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "learnings"
            entry = self._entry()
            entry["scope"] = {}
            entry_file = Path(td) / "entry.json"
            entry_file.write_text(json.dumps(entry), encoding="utf-8")

            parser = sl._build_parser()
            append_args = parser.parse_args(
                ["--root", str(root), "append", "--entry-file", str(entry_file)]
            )
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    append_args.func(append_args)

    def test_record_application_auto_accepts_after_two_successes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "learnings"
            entry_file = Path(td) / "entry.json"
            entry_file.write_text(json.dumps(self._entry()), encoding="utf-8")
            parser = sl._build_parser()
            append_args = parser.parse_args(
                ["--root", str(root), "append", "--entry-file", str(entry_file)]
            )
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(append_args.func(append_args), 0)
            learning_id = out.getvalue().strip()

            for run_id in ["run-a", "run-b"]:
                record_args = parser.parse_args(
                    [
                        "--root",
                        str(root),
                        "record-application",
                        learning_id,
                        "--outcome",
                        "success",
                        "--run-id",
                        run_id,
                        "--diagnostic-path",
                        "steps/1/try-1/diagnostic/root-cause.md",
                    ]
                )
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(record_args.func(record_args), 0)

            events = sl._current_by_id(sl._events(root))
            self.assertEqual(events[learning_id]["applied_success_count"], 2)
            self.assertEqual(events[learning_id]["status"], "accepted")

    def test_record_null_and_promote_with_provenance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "learnings"
            entry_file = Path(td) / "entry.json"
            entry_file.write_text(json.dumps(self._entry()), encoding="utf-8")
            parser = sl._build_parser()
            append_args = parser.parse_args(
                ["--root", str(root), "append", "--entry-file", str(entry_file)]
            )
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(append_args.func(append_args), 0)
            learning_id = out.getvalue().strip()

            null_args = parser.parse_args(
                [
                    "--root",
                    str(root),
                    "record-application",
                    learning_id,
                    "--outcome",
                    "null",
                    "--run-id",
                    "run-c",
                    "--diagnostic-path",
                    "steps/1/try-1/diagnostic/root-cause.md",
                    "--note",
                    "near miss",
                ]
            )
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(null_args.func(null_args), 0)

            promote_args = parser.parse_args(
                [
                    "--root",
                    str(root),
                    "promote",
                    learning_id,
                    "--target-path",
                    "skills/stepwise/references/examples.md",
                    "--summary",
                    "Added the principle to the upstream traversal example.",
                ]
            )
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(promote_args.func(promote_args), 0)

            events = sl._current_by_id(sl._events(root))
            self.assertEqual(events[learning_id]["applied_null_count"], 1)
            self.assertEqual(events[learning_id]["status"], "promoted")
            self.assertEqual(
                events[learning_id]["promotion"]["target_path"],
                "skills/stepwise/references/examples.md",
            )

    def test_sync_from_md_accepts_known_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "learnings"
            entry_file = Path(td) / "entry.json"
            entry_file.write_text(json.dumps(self._entry()), encoding="utf-8")
            parser = sl._build_parser()
            append_args = parser.parse_args(
                ["--root", str(root), "append", "--entry-file", str(entry_file)]
            )
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(append_args.func(append_args), 0)
            learning_id = out.getvalue().strip()
            (root / "accepted.md").write_text(f"# Accepted\n\n## {learning_id}\n", encoding="utf-8")

            sync_args = parser.parse_args(["--root", str(root), "sync-from-md"])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(sync_args.func(sync_args), 0)

            events = sl._current_by_id(sl._events(root))
            self.assertEqual(events[learning_id]["status"], "accepted")


if __name__ == "__main__":
    unittest.main()
