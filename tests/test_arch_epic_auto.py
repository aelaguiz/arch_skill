import importlib.util
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_RESOLUTION_PATH = REPO_ROOT / "skills/_shared/model_resolution.py"
RUN_ARCH_EPIC_PATH = REPO_ROOT / "skills/arch-epic/scripts/run_arch_epic.py"


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class ArchEpicAutoModeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model_resolution = load_module(
            MODEL_RESOLUTION_PATH,
            "arch_skill_model_resolution",
        )
        cls.run_arch_epic = load_module(
            RUN_ARCH_EPIC_PATH,
            "arch_skill_run_arch_epic",
        )

    def test_claude_family_version_shorthand_preserves_exact_version(self):
        resolved = self.model_resolution.resolve_execution_phrase(
            "Claude Opus 4.7 xhigh"
        )

        self.assertEqual(resolved.runtime, "claude")
        self.assertEqual(resolved.model, "claude-opus-4-7")
        self.assertEqual(resolved.effort, "xhigh")
        self.assertIn("exact model family/version", resolved.resolution_reason)

    def test_claude_fable_5_shorthand_resolves_to_full_model_id(self):
        cases = [
            ("Claude Fable 5 high", "high"),
            ("fable 5 xhigh", "xhigh"),
            ("claude-fable-5 max", "max"),
        ]

        for phrase, effort in cases:
            with self.subTest(phrase=phrase):
                resolved = self.model_resolution.resolve_execution_phrase(phrase)
                self.assertEqual(resolved.runtime, "claude")
                self.assertEqual(resolved.model, "claude-fable-5")
                self.assertEqual(resolved.effort, effort)

    def test_codex_shorthand_resolves_against_available_model_names(self):
        resolved = self.model_resolution.resolve_execution_phrase(
            "codex gpt 5.4 mini high",
            codex_models=["gpt-5.4", "gpt-5.4-mini"],
        )

        self.assertEqual(resolved.runtime, "codex")
        self.assertEqual(resolved.model, "gpt-5.4-mini")
        self.assertEqual(resolved.effort, "high")

    def test_codex_resolution_refuses_version_substitution(self):
        with self.assertRaises(self.model_resolution.ModelResolutionError):
            self.model_resolution.resolve_execution_phrase(
                "codex gpt 5.5 xhigh",
                codex_models=["gpt-5.4", "gpt-5.4-mini"],
            )

    def test_cursor_agent_model_resolves_with_encoded_effort(self):
        resolved = self.model_resolution.resolve_execution_phrase(
            "cursor agent composer-2.5-fast",
            agent_models=["composer-2.5-fast"],
        )

        self.assertEqual(resolved.runtime, "agent")
        self.assertEqual(resolved.model, "composer-2.5-fast")
        self.assertEqual(resolved.effort, "encoded-in-model")

    def test_cursor_agent_gpt_model_is_refused(self):
        with self.assertRaises(self.model_resolution.ModelResolutionError):
            self.model_resolution.resolve_execution_phrase(
                "agent gpt-5.4-xhigh",
                agent_models=["gpt-5.4-xhigh"],
            )

    def test_cursor_agent_resolution_refuses_model_substitution(self):
        with self.assertRaises(self.model_resolution.ModelResolutionError):
            self.model_resolution.resolve_execution_phrase(
                "cursor agent composer-2.5-fast",
                agent_models=["composer-2.5-slow"],
            )

    def test_role_policy_defaults_to_long_run_monitoring_and_allows_same_as(self):
        policy = self.model_resolution.resolve_role_execution_policy(
            {
                "epic_planner": "claude opus 4.7 xhigh",
                "implementation_worker": "codex gpt 5.4 xhigh",
                "repair_worker": "same as implementation",
                "critic": "codex gpt 5.4 mini xhigh",
            },
            codex_models=["gpt-5.4", "gpt-5.4-mini"],
        )

        self.assertEqual(policy["poll_seconds"], 180)
        self.assertEqual(policy["quiet_floor_seconds"], 900)
        self.assertEqual(policy["stuck_floor_seconds"], 1800)
        self.assertEqual(policy["max_runtime_seconds"], 7200)
        self.assertEqual(
            policy["roles"]["repair_worker"]["model"],
            policy["roles"]["implementation_worker"]["model"],
        )
        self.assertEqual(
            policy["roles"]["repair_worker"]["source"],
            "same_as:implementation_worker",
        )
        self.assertIn("execution_sha256", policy)

    def test_role_policy_accepts_claude_fable_for_auto_mode_roles(self):
        policy = self.model_resolution.resolve_role_execution_policy(
            {
                "epic_planner": "claude fable 5 high",
                "implementation_worker": "codex gpt 5.4 xhigh",
                "critic": "codex gpt 5.4 mini xhigh",
            },
            codex_models=["gpt-5.4", "gpt-5.4-mini"],
        )

        self.assertEqual(policy["roles"]["epic_planner"]["runtime"], "claude")
        self.assertEqual(policy["roles"]["epic_planner"]["model"], "claude-fable-5")
        self.assertEqual(policy["roles"]["epic_planner"]["effort"], "high")

    def test_codex_worker_command_is_resumable_and_hook_suppressed(self):
        argv = self.run_arch_epic._codex_worker_argv(
            Path("/repo"),
            "gpt-5.4",
            "xhigh",
            Path("/tmp/final.json"),
            "Do work.",
        )

        self.assertIn("--disable", argv)
        self.assertIn("codex_hooks", argv)
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", argv)
        self.assertNotIn("--ephemeral", argv)
        self.assertIn('model_reasoning_effort="xhigh"', argv)

    def test_codex_critic_command_is_ephemeral_and_hook_suppressed(self):
        argv = self.run_arch_epic._codex_critic_argv(
            Path("/repo"),
            "gpt-5.4-mini",
            "xhigh",
            Path("/tmp/schema.json"),
            Path("/tmp/verdict.json"),
            "Return JSON.",
        )

        self.assertIn("--ephemeral", argv)
        self.assertIn("--disable", argv)
        self.assertIn("codex_hooks", argv)
        self.assertIn("--output-schema", argv)
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", argv)

    def test_claude_commands_pin_model_and_effort(self):
        worker_argv = self.run_arch_epic._claude_worker_argv(
            "claude-opus-4-7",
            "xhigh",
            "Do work.",
        )
        critic_argv = self.run_arch_epic._claude_critic_argv(
            "claude-sonnet-4-6",
            "high",
            '{"type":"object"}',
            "Return JSON.",
        )

        self.assertIn("--settings", worker_argv)
        self.assertIn('{"disableAllHooks":true}', worker_argv)
        self.assertIn("stream-json", worker_argv)
        self.assertEqual(
            worker_argv[worker_argv.index("stream-json") + 1],
            "--verbose",
        )
        self.assertIn("--include-partial-messages", worker_argv)
        self.assertIn("--include-hook-events", worker_argv)
        self.assertIn("--model", worker_argv)
        self.assertIn("claude-opus-4-7", worker_argv)
        self.assertIn("--effort", worker_argv)
        self.assertIn("xhigh", worker_argv)
        self.assertIn("--json-schema", critic_argv)
        self.assertIn("stream-json", critic_argv)
        self.assertEqual(
            critic_argv[critic_argv.index("stream-json") + 1],
            "--verbose",
        )
        self.assertIn("claude-sonnet-4-6", critic_argv)

    def test_default_auto_monitoring_constants_are_long_running(self):
        self.assertEqual(self.run_arch_epic.DEFAULT_AUTO_POLL_SECONDS, 180)
        self.assertEqual(self.run_arch_epic.DEFAULT_QUIET_FLOOR_SECONDS, 900)
        self.assertEqual(self.run_arch_epic.DEFAULT_STUCK_FLOOR_SECONDS, 1800)
        self.assertEqual(self.run_arch_epic.DEFAULT_CHILD_MAX_RUNTIME_SECONDS, 7200)

    def test_auto_run_mode_detaches_long_worker_roles(self):
        selected = self.run_arch_epic._select_child_run_mode(
            requested="auto",
            expected_duration="auto",
            kind="worker",
            role="epic_planner",
        )

        self.assertEqual(selected, "detached")
        self.assertEqual(
            self.run_arch_epic._select_child_run_mode(
                requested="auto",
                expected_duration="short",
                kind="worker",
                role="epic_planner",
            ),
            "foreground",
        )

    def test_foreground_child_streams_events_and_stderr_while_capturing_stdout(self):
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            code, stdout_text = self.run_arch_epic._run_subprocess(
                [
                    sys.executable,
                    "-c",
                    (
                        "import sys; "
                        "print('{\"type\":\"thread.started\",\"thread_id\":\"abc\"}', flush=True); "
                        "print('ERRLINE', file=sys.stderr, flush=True)"
                    ),
                ],
                run_dir / "stream.log",
                run_dir,
            )

            self.assertEqual(code, 0)
            self.assertIn("thread.started", stdout_text)
            self.assertIn("thread.started", (run_dir / "events.jsonl").read_text())
            self.assertIn("ERRLINE", (run_dir / "stderr.log").read_text())
            self.assertIn("[stderr] ERRLINE", (run_dir / "stream.log").read_text())
            self.assertEqual((run_dir / "exit_code").read_text().strip(), "0")

    def test_child_status_uses_quiet_needs_attention_not_hung(self):
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            now = 1_800_000_000.0
            start = now - 2_000
            activity = now - 1_000
            (run_dir / "start_ts").write_text(
                "2027-01-15T08:00:00Z",
                encoding="utf-8",
            )
            (run_dir / "child.pid").write_text(f"{os.getpid()}\n", encoding="utf-8")
            (run_dir / "stream.log").write_text("progress\n", encoding="utf-8")
            os.utime(run_dir / "stream.log", (activity, activity))

            status = self.run_arch_epic._child_status(
                run_dir,
                quiet_floor_seconds=900,
                stuck_floor_seconds=1800,
                max_runtime_seconds=7200,
                now=now,
            )

        serialized = json.dumps(status)
        self.assertEqual(status["state"], "quiet")
        self.assertNotIn("hung", serialized.lower())

    def test_auto_init_narrows_gitignore_marker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "orchestrator"
            root.mkdir()
            epic_doc = root / "docs" / "EPIC_BIG_GOAL_2026-04-26.md"
            epic_doc.parent.mkdir()
            epic_doc.write_text("# Epic\n", encoding="utf-8")
            (root / ".gitignore").write_text(".arch_skill/\n", encoding="utf-8")
            policy_file = root / "policy.json"
            policy_file.write_text(
                json.dumps(
                    {
                        "roles": {
                            "epic_planner": "claude opus 4.7 xhigh",
                            "implementation_worker": "codex gpt 5.4 xhigh",
                            "repair_worker": "same as implementation_worker",
                            "critic": "codex gpt 5.4 mini xhigh",
                        },
                        "codex_models": ["gpt-5.4", "gpt-5.4-mini"],
                    }
                ),
                encoding="utf-8",
            )
            parser = self.run_arch_epic._build_parser()
            args = parser.parse_args(
                [
                    "auto-init",
                    "--epic-doc",
                    str(epic_doc),
                    "--policy-file",
                    str(policy_file),
                    "--orchestrator-root",
                    str(root),
                ]
            )
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(args.func(args), 0)
            [run_dir] = list((root / ".arch_skill" / "arch-epic" / "auto").glob("*/*"))
            state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
            gitignore = (root / ".gitignore").read_text(encoding="utf-8")

        self.assertIn(".arch_skill/arch-epic/", gitignore)
        self.assertNotIn(".arch_skill/\n", gitignore)
        self.assertEqual(
            state["auto_execution"]["auto_run_dir"],
            str(run_dir.resolve()),
        )


if __name__ == "__main__":
    unittest.main()
