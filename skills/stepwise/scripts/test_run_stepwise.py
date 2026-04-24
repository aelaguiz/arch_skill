"""Regression tests for Claude stdout shape normalization in run_stepwise.

Claude `-p --output-format json` emits either a single top-level result dict
OR a list of stream events (when `--json-schema` is combined with tool use).
The three parsers the orchestrator relies on must handle both shapes. These
tests pin that behavior.

Run: `python3 skills/stepwise/scripts/test_run_stepwise.py`
"""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

# Import the module under test without executing argparse.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_stepwise as rs  # noqa: E402


# A minimal result event mirroring the real shape captured from a critic run
# with tool use: the orchestrator only needs type=result + session_id +
# structured_output. Other fields exist in production but are irrelevant here.
_RESULT_EVENT = {
    "type": "result",
    "subtype": "success",
    "is_error": False,
    "session_id": "aa86534c-57f3-4b99-8f34-c48821a3f327",
    "stop_reason": "end_turn",
    "structured_output": {
        "step_n": 2,
        "verdict": "pass",
        "checks": [
            {
                "name": "artifact_exists",
                "status": "pass",
                "evidence": "file exists and header matches",
            }
        ],
        "summary": "Step 2 produced outline.md with the expected header.",
    },
}

# A list-shape payload: several non-result events preceded by one result.
_STREAM_EVENTS = [
    {"type": "system", "subtype": "init", "session_id": "aa86534c-57f3-4b99-8f34-c48821a3f327"},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "..."}]}},
    {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read"}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "..."}]}},
    _RESULT_EVENT,
]


def _stdout_from(obj) -> str:
    """Simulate subprocess stdout: Claude's last line holds the JSON payload."""
    return "\n".join(["(prior lifecycle noise)", json.dumps(obj)])


class ExtractClaudeResultEvent(unittest.TestCase):
    def test_dict_passthrough(self):
        self.assertIs(rs._extract_claude_result_event(_RESULT_EVENT), _RESULT_EVENT)

    def test_list_finds_result_event(self):
        got = rs._extract_claude_result_event(_STREAM_EVENTS)
        self.assertIs(got, _RESULT_EVENT)

    def test_list_with_noise_after_result(self):
        # Defensive: if non-result events follow the result, we still find it.
        noisy = _STREAM_EVENTS + [{"type": "meta", "note": "extra"}]
        got = rs._extract_claude_result_event(noisy)
        self.assertIs(got, _RESULT_EVENT)

    def test_list_with_no_result_returns_none(self):
        self.assertIsNone(
            rs._extract_claude_result_event([{"type": "system"}, {"type": "assistant"}])
        )

    def test_garbage_returns_none(self):
        self.assertIsNone(rs._extract_claude_result_event(None))
        self.assertIsNone(rs._extract_claude_result_event("unexpected"))
        self.assertIsNone(rs._extract_claude_result_event(42))


class ParseClaudeSessionId(unittest.TestCase):
    def test_dict_shape(self):
        self.assertEqual(
            rs._parse_claude_session_id(_stdout_from(_RESULT_EVENT)),
            "aa86534c-57f3-4b99-8f34-c48821a3f327",
        )

    def test_list_shape_regression(self):
        """Before the fix, a list payload crashed in `.get('session_id')`.
        After the fix, we extract the session id from the embedded result
        event."""
        self.assertEqual(
            rs._parse_claude_session_id(_stdout_from(_STREAM_EVENTS)),
            "aa86534c-57f3-4b99-8f34-c48821a3f327",
        )

    def test_missing_session_id(self):
        dict_without = {"type": "result", "subtype": "success"}
        self.assertIsNone(rs._parse_claude_session_id(_stdout_from(dict_without)))

    def test_invalid_json(self):
        self.assertIsNone(rs._parse_claude_session_id("not json at all"))


class ParseClaudeFinalJson(unittest.TestCase):
    def test_dict_shape_returns_dict(self):
        got = rs._parse_claude_final_json(_stdout_from(_RESULT_EVENT))
        self.assertIsInstance(got, dict)
        self.assertEqual(got.get("type"), "result")

    def test_list_shape_returns_extracted_event(self):
        """Before the fix, callers expected a dict but got the raw list.
        After the fix, we return the extracted result event."""
        got = rs._parse_claude_final_json(_stdout_from(_STREAM_EVENTS))
        self.assertIsInstance(got, dict)
        self.assertEqual(got.get("session_id"), "aa86534c-57f3-4b99-8f34-c48821a3f327")


class ExtractVerdictFromFinal(unittest.TestCase):
    def test_dict_final(self):
        verdict = rs._extract_verdict_from_final(_RESULT_EVENT)
        self.assertIsInstance(verdict, dict)
        self.assertEqual(verdict.get("verdict"), "pass")

    def test_list_final_regression(self):
        """Before the fix, cmd_critic_spawn crashed here on list payloads."""
        verdict = rs._extract_verdict_from_final(_STREAM_EVENTS)
        self.assertIsInstance(verdict, dict)
        self.assertEqual(verdict.get("verdict"), "pass")
        self.assertEqual(verdict.get("step_n"), 2)

    def test_missing_structured_output(self):
        # Result event without structured_output → None, not a crash.
        ev = {"type": "result", "session_id": "x"}
        self.assertIsNone(rs._extract_verdict_from_final(ev))

    def test_no_result_event(self):
        self.assertIsNone(rs._extract_verdict_from_final([{"type": "system"}]))


class InitRunExecutionPolicy(unittest.TestCase):
    def test_init_run_stores_execution_policy_and_hash(self):
        execution = {
            "schema_version": 2,
            "execution_defaults": {
                "step": {
                    "runtime": "codex",
                    "model": "gpt-5.4",
                    "effort": "high",
                    "source": "user prompt",
                },
                "critic": {
                    "runtime": "codex",
                    "model": "gpt-5.4-mini",
                    "effort": "xhigh",
                    "source": "user prompt",
                },
            },
            "execution_preferences": [
                {
                    "source_quote": "copywriting steps using Claude Opus 4.7",
                    "applies_to": "steps whose outcome is learner-facing copy",
                    "step_execution": {
                        "runtime": "claude",
                        "model": "opus-4-7",
                    },
                    "resolution_rationale": (
                        "The user named a semantic class; resolve it after "
                        "manifest drafting."
                    ),
                }
            ],
        }

        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "orchestrator"
            target = Path(td) / "target"
            root.mkdir()
            target.mkdir()
            raw = Path(td) / "raw.txt"
            raw.write_text("run process with copywriting on Claude\n", encoding="utf-8")

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
                    "2",
                    "--execution-json",
                    json.dumps(execution),
                ]
            )

            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(args.func(args), 0)
            runs_dir = root / ".arch_skill" / "stepwise" / "runs"
            run_dirs = list(runs_dir.iterdir())
            self.assertEqual(len(run_dirs), 1)
            state = json.loads((run_dirs[0] / "state.json").read_text(encoding="utf-8"))

        self.assertEqual(state["execution"], execution)
        self.assertEqual(
            state["execution_sha256"],
            rs._sha256_hex(json.dumps(execution, sort_keys=True)),
        )
        self.assertNotIn("models", state)
        self.assertNotIn("models_sha256", state)


class CodexSchemaNormalization(unittest.TestCase):
    def test_optional_schema_fields_become_required_nullable(self):
        schema = {
            "type": "object",
            "required": ["step_n", "verdict", "checks", "summary"],
            "properties": {
                "step_n": {"type": "integer"},
                "verdict": {"enum": ["pass", "fail", "abstain"]},
                "checks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "status"],
                        "properties": {
                            "name": {"type": "string"},
                            "status": {"enum": ["pass", "fail", "inapplicable"]},
                            "evidence": {"type": "string"},
                        },
                    },
                },
                "resume_hint": {
                    "type": "object",
                    "required": ["headline"],
                    "properties": {
                        "headline": {"type": "string"},
                        "required_fixes": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "do_not_redo": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
                "route_to_step_n": {"type": "integer", "minimum": 1},
                "abstain_reason": {"type": "string"},
                "summary": {"type": "string"},
            },
        }

        normalized = rs._codex_strict_schema(schema)

        self.assertEqual(
            normalized["required"],
            [
                "step_n",
                "verdict",
                "checks",
                "resume_hint",
                "route_to_step_n",
                "abstain_reason",
                "summary",
            ],
        )
        self.assertFalse(normalized["additionalProperties"])
        self.assertEqual(
            normalized["properties"]["resume_hint"]["type"],
            ["object", "null"],
        )
        self.assertEqual(
            normalized["properties"]["route_to_step_n"]["type"],
            ["integer", "null"],
        )
        item_schema = normalized["properties"]["checks"]["items"]
        self.assertEqual(item_schema["required"], ["name", "status", "evidence"])
        self.assertEqual(
            item_schema["properties"]["evidence"]["type"],
            ["string", "null"],
        )

    def test_critic_spawn_writes_and_uses_codex_normalized_schema(self):
        old_run_subprocess = rs._run_subprocess
        captured = {}

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None):
            captured["argv"] = argv
            schema_path = Path(argv[argv.index("--output-schema") + 1])
            final_path = Path(argv[argv.index("-o") + 1])
            stdout_stream_path.write_text(
                '{"type":"thread.started","thread_id":"t"}\n',
                encoding="utf-8",
            )
            final_path.write_text(
                json.dumps(
                    {
                        "step_n": 1,
                        "verdict": "pass",
                        "checks": [
                            {
                                "name": "artifact_exists",
                                "status": "pass",
                                "evidence": "artifact exists",
                            }
                        ],
                        "resume_hint": None,
                        "route_to_step_n": None,
                        "abstain_reason": None,
                        "summary": "The step passed.",
                    }
                ),
                encoding="utf-8",
            )
            captured["schema_path"] = schema_path
            return 0, ""

        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["step_n", "verdict", "checks", "summary"],
            "properties": {
                "step_n": {"type": "integer"},
                "verdict": {"enum": ["pass", "fail", "abstain"]},
                "checks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["name", "status", "evidence"],
                        "properties": {
                            "name": {"type": "string"},
                            "status": {"enum": ["pass", "fail", "inapplicable"]},
                            "evidence": {"type": "string"},
                        },
                    },
                },
                "resume_hint": {"type": "object", "properties": {}},
                "route_to_step_n": {"type": "integer", "minimum": 1},
                "abstain_reason": {"type": "string"},
                "summary": {"type": "string"},
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
                    "gpt-5.4",
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

            self.assertEqual(captured["schema_path"].name, "schema.codex.json")
            normalized = json.loads(captured["schema_path"].read_text(encoding="utf-8"))

        self.assertEqual(set(normalized["required"]), set(normalized["properties"]))
        self.assertEqual(
            normalized["properties"]["route_to_step_n"]["type"],
            ["integer", "null"],
        )


class StepVerdictValidation(unittest.TestCase):
    def test_valid_pass_verdict(self):
        verdict = {
            "step_n": 1,
            "verdict": "pass",
            "checks": [
                {
                    "name": "artifact_exists",
                    "status": "pass",
                    "evidence": "file exists",
                }
            ],
            "resume_hint": None,
            "route_to_step_n": None,
            "abstain_reason": None,
            "summary": "Step passed.",
        }
        self.assertEqual(rs._validate_step_verdict(verdict), [])

    def test_valid_fail_verdict_requires_operational_hint(self):
        verdict = {
            "step_n": 2,
            "verdict": "fail",
            "checks": [
                {
                    "name": "no_fabrication",
                    "status": "fail",
                    "evidence": "claim lacks backing evidence",
                }
            ],
            "resume_hint": {
                "headline": "The artifact was claimed but not written.",
                "required_fixes": ["Write the declared artifact."],
                "do_not_redo": [],
            },
            "route_to_step_n": None,
            "abstain_reason": None,
            "summary": "Step failed.",
        }
        self.assertEqual(rs._validate_step_verdict(verdict), [])

    def test_fail_without_resume_hint_is_invalid(self):
        verdict = {
            "step_n": 2,
            "verdict": "fail",
            "checks": [],
            "resume_hint": None,
            "route_to_step_n": None,
            "abstain_reason": None,
            "summary": "Step failed.",
        }
        errors = rs._validate_step_verdict(verdict)
        self.assertIn("resume_hint must be an object on fail", errors)


if __name__ == "__main__":
    unittest.main()
