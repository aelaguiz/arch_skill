import importlib.util
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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

    def test_claude_fable_5_1_shorthand_resolves_to_full_model_id(self):
        cases = [
            ("Claude Fable 5.1 high", "high"),
            ("fable 5.1 xhigh", "xhigh"),
            ("claude-fable-5-1 max", "max"),
        ]

        for phrase, effort in cases:
            with self.subTest(phrase=phrase):
                resolved = self.model_resolution.resolve_execution_phrase(phrase)
                self.assertEqual(resolved.runtime, "claude")
                self.assertEqual(resolved.model, "claude-fable-5-1")
                self.assertEqual(resolved.effort, effort)

    def test_codex_shorthand_resolves_against_available_model_names(self):
        resolved = self.model_resolution.resolve_execution_phrase(
            "codex gpt 5.4 mini high",
            codex_models=["gpt-5.6-sol", "gpt-5.4-mini"],
        )

        self.assertEqual(resolved.runtime, "codex")
        self.assertEqual(resolved.model, "gpt-5.4-mini")
        self.assertEqual(resolved.effort, "high")

    def test_codex_resolution_refuses_version_substitution(self):
        with self.assertRaises(self.model_resolution.ModelResolutionError):
            self.model_resolution.resolve_execution_phrase(
                "codex gpt-5.6-sol xhigh",
                codex_models=["gpt-5.3-codex", "gpt-5.4-mini"],
            )

    def test_codex_resolution_accepts_preferred_compact_alias(self):
        resolved = self.model_resolution.resolve_execution_phrase(
            "GPT56SOLXI",
            codex_models=["gpt-5.6-sol"],
        )

        self.assertEqual(resolved.runtime, "codex")
        self.assertEqual(resolved.model, "gpt-5.6-sol")
        self.assertEqual(resolved.effort, "xhigh")

    def test_codex_sol_defaults_to_ultra_when_effort_is_omitted(self):
        cases = [
            ("codex", "default"),
            ("sol", "explicit"),
            ("gpt-5.6-sol", "explicit"),
        ]

        for phrase, model_source in cases:
            with self.subTest(phrase=phrase):
                resolved = self.model_resolution.resolve_execution_phrase(
                    phrase,
                    codex_models=["gpt-5.6-sol"],
                )

                self.assertEqual(resolved.runtime, "codex")
                self.assertEqual(resolved.model, "gpt-5.6-sol")
                self.assertEqual(resolved.model_source, model_source)
                self.assertEqual(resolved.effort, "ultra")
                self.assertEqual(
                    resolved.effort_source,
                    "preference_default",
                )

    def test_codex_sol_preserves_explicit_xhigh_override(self):
        resolved = self.model_resolution.resolve_execution_phrase(
            "gpt-5.6-sol xhigh",
            codex_models=["gpt-5.6-sol"],
        )

        self.assertEqual(resolved.effort, "xhigh")
        self.assertEqual(resolved.effort_source, "explicit")

    def test_codex_terra_accepts_explicit_ultra(self):
        resolved = self.model_resolution.resolve_execution_phrase(
            "terra ultra",
            codex_models=["gpt-5.6-terra"],
        )

        self.assertEqual(resolved.model, "gpt-5.6-terra")
        self.assertEqual(resolved.effort, "ultra")
        self.assertEqual(resolved.effort_source, "explicit")

    def test_ultra_is_rejected_where_the_selected_runtime_does_not_support_it(self):
        cases = [
            (
                "Claude Opus 4.7 ultra",
                {},
            ),
            (
                "luna ultra",
                {"codex_models": ["gpt-5.6-luna"]},
            ),
            (
                "cursor agent composer 2.5 ultra",
                {"agent_models": ["composer-2.5-fast"]},
            ),
            (
                "kimi ultra",
                {"kimi_models": ["kimi-code/k3"]},
            ),
        ]

        for phrase, kwargs in cases:
            with self.subTest(phrase=phrase):
                with self.assertRaises(self.model_resolution.ModelResolutionError):
                    self.model_resolution.resolve_execution_phrase(
                        phrase,
                        **kwargs,
                    )

    def test_codex_resolution_rejects_blocked_base_models(self):
        for phrase in (
            "codex gpt 5.4 xhigh",
            "codex gpt-5.5 xhigh",
            "GBT55XI",
        ):
            with self.subTest(phrase=phrase):
                with self.assertRaisesRegex(
                    self.model_resolution.ModelResolutionError,
                    "blocked Codex model",
                ):
                    self.model_resolution.resolve_execution_phrase(
                        phrase,
                        codex_models=["gpt-5.6-sol", "gpt-5.4-mini"],
                    )

    def test_codex_argv_rejects_blocked_base_models(self):
        for model in ("gpt-5.4", "gpt-5.5"):
            with self.subTest(model=model):
                with self.assertRaisesRegex(
                    self.model_resolution.ModelResolutionError,
                    "blocked Codex model",
                ):
                    self.model_resolution.codex_model_or_profile_args(
                        model,
                        "xhigh",
                    )

    def test_codex_accepts_fugu_profiles(self):
        cases = [
            ("Fugu", "fugu", "high"),
            ("Fugu high", "fugu", "high"),
            ("Codex Fugu Ultra", "fugu-ultra", "xhigh"),
            ("Codex Fugu Ultra xhigh", "fugu-ultra", "xhigh"),
            ("sakana fugu-ultra max", "fugu-ultra", "max"),
        ]

        for phrase, model, effort in cases:
            with self.subTest(phrase=phrase):
                resolved = self.model_resolution.resolve_execution_phrase(
                    phrase,
                    codex_models=["gpt-5.6-sol"],
                )
                self.assertEqual(resolved.runtime, "codex")
                self.assertEqual(resolved.model, model)
                self.assertEqual(resolved.codex_profile, model)
                self.assertEqual(resolved.effort, effort)
                self.assertEqual(resolved.model_source, "codex_profile")

    def test_codex_fugu_refuses_unsupported_effort(self):
        for phrase in ("fugu xhigh", "Fugu Ultra ultra"):
            with self.subTest(phrase=phrase):
                with self.assertRaises(self.model_resolution.ModelResolutionError):
                    self.model_resolution.resolve_execution_phrase(
                        phrase,
                        codex_models=["fugu", "fugu-ultra"],
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

    def test_kimi_k3_defaults_to_max_with_model_default_provenance(self):
        for phrase in ("kimi", "Kimi Code", "Kimi K3", "kimi-code/k3"):
            with self.subTest(phrase=phrase):
                resolved = self.model_resolution.resolve_execution_phrase(
                    phrase,
                    kimi_models=["kimi-code/k3"],
                )

                self.assertEqual(resolved.runtime, "kimi")
                self.assertEqual(resolved.model, "kimi-code/k3")
                self.assertEqual(resolved.effort, "max")
                self.assertEqual(resolved.effort_source, "model_default")

    def test_kimi_k3_preserves_every_explicit_effort_override(self):
        for effort in ("low", "medium", "high", "xhigh", "max"):
            with self.subTest(effort=effort):
                resolved = self.model_resolution.resolve_execution_phrase(
                    f"kimi k3 {effort}",
                    kimi_models=["kimi-code/k3"],
                )

                self.assertEqual(resolved.effort, effort)
                self.assertEqual(resolved.effort_source, "explicit")

    def test_kimi_xhigh_alias_normalizes_without_counting_high_twice(self):
        for alias in ("extra-high", "extra high", "x-high", "x high"):
            with self.subTest(alias=alias):
                resolved = self.model_resolution.resolve_execution_phrase(
                    f"kimi k3 {alias}",
                    kimi_models=["kimi-code/k3"],
                )

                self.assertEqual(resolved.effort, "xhigh")
                self.assertEqual(resolved.effort_source, "explicit")

    def test_kimi_contradictory_efforts_fail_instead_of_defaulting(self):
        for phrase in (
            "kimi k3 low high",
            "kimi k3 medium xhigh",
            "kimi k3 extra-high low",
        ):
            with self.subTest(phrase=phrase):
                with self.assertRaisesRegex(
                    self.model_resolution.ModelResolutionError,
                    "multiple distinct effort levels",
                ):
                    self.model_resolution.resolve_execution_phrase(
                        phrase,
                        kimi_models=["kimi-code/k3"],
                    )

    def test_kimi_discovery_reads_top_level_model_alias_keys(self):
        payload = {
            "models": {
                "kimi-code/kimi-for-coding": {"name": "Kimi for coding"},
                "kimi-code/kimi-for-coding-highspeed": {},
                "kimi-code/k3": {"defaultEffort": "max"},
            }
        }
        completed = mock.Mock(returncode=0, stdout=json.dumps(payload))
        with mock.patch.object(
            self.model_resolution.shutil,
            "which",
            return_value="/usr/local/bin/kimi",
        ), mock.patch.object(
            self.model_resolution.subprocess,
            "run",
            return_value=completed,
        ) as run:
            models = self.model_resolution.discover_kimi_models()

        self.assertEqual(
            models,
            [
                "kimi-code/k3",
                "kimi-code/kimi-for-coding",
                "kimi-code/kimi-for-coding-highspeed",
            ],
        )
        self.assertEqual(
            run.call_args.args[0],
            ["kimi", "provider", "list", "--json"],
        )

    def test_kimi_discovery_fails_safe_for_unavailable_or_invalid_catalogs(self):
        completed_cases = [
            mock.Mock(returncode=1, stdout='{"models":{"kimi-code/k3":{}}}'),
            mock.Mock(returncode=0, stdout="not json"),
            mock.Mock(returncode=0, stdout='{"models":[]}'),
        ]
        with mock.patch.object(
            self.model_resolution.shutil,
            "which",
            return_value=None,
        ), mock.patch.object(self.model_resolution.subprocess, "run") as run:
            self.assertEqual(self.model_resolution.discover_kimi_models(), [])
            run.assert_not_called()

        for completed in completed_cases:
            with self.subTest(completed=completed), mock.patch.object(
                self.model_resolution.shutil,
                "which",
                return_value="/usr/local/bin/kimi",
            ), mock.patch.object(
                self.model_resolution.subprocess,
                "run",
                return_value=completed,
            ):
                self.assertEqual(self.model_resolution.discover_kimi_models(), [])

    def test_kimi_resolution_refuses_catalog_without_k3(self):
        with self.assertRaisesRegex(
            self.model_resolution.ModelResolutionError,
            "available Kimi model id",
        ):
            self.model_resolution.resolve_execution_phrase(
                "kimi k3",
                kimi_models=["kimi-code/kimi-for-coding"],
            )

    def test_kimi_resolution_refuses_explicit_non_k3_identity(self):
        for phrase in (
            "kimi-code/kimi-for-coding high",
            "Kimi K2.7 high",
            "K2.7 high",
            "Kimi K4 high",
        ):
            with self.subTest(phrase=phrase):
                with self.assertRaisesRegex(
                    self.model_resolution.ModelResolutionError,
                    "name K3",
                ):
                    self.model_resolution.resolve_execution_phrase(
                        phrase,
                        kimi_models=[
                            "kimi-code/k3",
                            "kimi-code/kimi-for-coding",
                        ],
                    )

    def test_kimi_mixed_provider_phrases_fail_loud(self):
        for phrase in (
            "kimi k3 and grok-4.5 high",
            "kimi k3 codex high",
            "moonshot k3 claude opus 4.7 high",
        ):
            with self.subTest(phrase=phrase):
                with self.assertRaisesRegex(
                    self.model_resolution.ModelResolutionError,
                    "multiple runtime families",
                ):
                    self.model_resolution.resolve_execution_phrase(phrase)

    def test_natural_grok_harness_names_default_to_grok_46(self):
        for phrase in (
            "grok high",
            "Grok CLI medium",
            "Grok Build low",
            "Grok 4.6 high",
            "Grok CLI 4.6 medium",
            "Grok Build 4.6 low",
        ):
            with self.subTest(phrase=phrase):
                resolved = self.model_resolution.resolve_execution_phrase(
                    phrase,
                    grok_models=["grok-4.6", "grok-4.5"],
                )

                self.assertEqual(resolved.runtime, "grok")
                self.assertEqual(resolved.model, "grok-4.6")
                self.assertEqual(resolved.model_source, "default")

    def test_natural_grok_build_refuses_non_46_numeric_versions(self):
        for phrase in (
            "Grok Build 2.5 high",
            "Grok Build version 4.5 medium",
            "Grok Build v3 high",
            "Grok Build model 2.5 high",
        ):
            with self.subTest(phrase=phrase):
                with self.assertRaisesRegex(
                    self.model_resolution.ModelResolutionError,
                    "unsupported numeric version",
                ):
                    self.model_resolution.resolve_execution_phrase(
                        phrase,
                        grok_models=["grok-4.6", "grok-4.5"],
                    )

    def test_natural_grok_ignores_unrelated_later_numbers(self):
        for phrase, effort in (
            ("Grok Build high for 2 reviewers", "high"),
            ("Grok CLI medium with 3 passes", "medium"),
            ("Grok high in 2026", "high"),
            ("Grok Build 4.6 low for 2 reviewers", "low"),
        ):
            with self.subTest(phrase=phrase):
                resolved = self.model_resolution.resolve_execution_phrase(
                    phrase,
                    grok_models=["grok-4.6", "grok-4.5"],
                )

                self.assertEqual(resolved.model, "grok-4.6")
                self.assertEqual(resolved.effort, effort)

    def test_explicit_grok_slug_stays_exact(self):
        resolved = self.model_resolution.resolve_execution_phrase(
            "grok-build high",
            grok_models=["grok-build", "grok-4.6", "grok-4.5"],
        )

        self.assertEqual(resolved.model, "grok-build")
        self.assertEqual(resolved.model_source, "explicit")

    def test_explicit_grok_45_slug_stays_exact(self):
        resolved = self.model_resolution.resolve_execution_phrase(
            "grok-4.5 high",
            grok_models=["grok-4.6", "grok-4.5"],
        )

        self.assertEqual(resolved.model, "grok-4.5")
        self.assertEqual(resolved.model_source, "explicit")

    def test_grok_catalog_models_reject_efforts_outside_cli_catalog(self):
        for model in ("grok-4.6", "grok-4.5"):
            for effort in ("xhigh", "max", "ultra"):
                with self.subTest(model=model, effort=effort):
                    with self.assertRaisesRegex(
                        self.model_resolution.ModelResolutionError,
                        "supports only: high, low, medium",
                    ):
                        self.model_resolution.resolve_execution_phrase(
                            f"{model} {effort}",
                            grok_models=["grok-4.6", "grok-4.5"],
                        )

    def test_role_policy_defaults_to_long_run_monitoring_and_allows_same_as(self):
        policy = self.model_resolution.resolve_role_execution_policy(
            {
                "epic_planner": "claude opus 4.7 xhigh",
                "implementation_worker": "codex gpt-5.6-sol xhigh",
                "repair_worker": "same as implementation",
                "critic": "codex gpt 5.4 mini xhigh",
            },
            codex_models=["gpt-5.6-sol", "gpt-5.4-mini"],
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
                "epic_planner": "claude fable 5.1 high",
                "implementation_worker": "codex gpt-5.6-sol xhigh",
                "critic": "codex gpt 5.4 mini xhigh",
            },
            codex_models=["gpt-5.6-sol", "gpt-5.4-mini"],
        )

        self.assertEqual(policy["roles"]["epic_planner"]["runtime"], "claude")
        self.assertEqual(policy["roles"]["epic_planner"]["model"], "claude-fable-5-1")
        self.assertEqual(policy["roles"]["epic_planner"]["effort"], "high")

    def test_arch_policy_file_threads_kimi_catalog_and_default_effort(self):
        with tempfile.TemporaryDirectory() as td:
            policy_path = Path(td) / "policy.json"
            policy_path.write_text(
                json.dumps(
                    {
                        "roles": {
                            "epic_planner": "kimi k3",
                            "implementation_worker": "kimi code high",
                            "critic": "same as epic_planner",
                        },
                        "kimi_models": ["kimi-code/k3"],
                    }
                ),
                encoding="utf-8",
            )

            policy = self.run_arch_epic._policy_from_file(policy_path)

        self.assertEqual(policy["roles"]["epic_planner"]["runtime"], "kimi")
        self.assertEqual(policy["roles"]["epic_planner"]["effort"], "max")
        self.assertEqual(
            policy["roles"]["epic_planner"]["effort_source"],
            "model_default",
        )
        self.assertEqual(
            policy["roles"]["implementation_worker"]["effort"],
            "high",
        )
        self.assertEqual(policy["roles"]["critic"]["source"], "same_as:epic_planner")

    def test_codex_worker_command_is_resumable_and_hook_suppressed(self):
        argv = self.run_arch_epic._codex_worker_argv(
            Path("/repo"),
            "gpt-5.6-sol",
            "ultra",
            Path("/tmp/final.json"),
            "Do work.",
        )

        self.assertIn("--disable", argv)
        self.assertIn("codex_hooks", argv)
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", argv)
        self.assertNotIn("--ephemeral", argv)
        self.assertIn("--model", argv)
        self.assertIn("gpt-5.6-sol", argv)
        self.assertIn('model_reasoning_effort="ultra"', argv)

    def test_shared_kimi_cli_primitives_are_canonical(self):
        self.assertEqual(
            self.model_resolution.KIMI_EFFORT_ENV,
            "KIMI_MODEL_THINKING_EFFORT",
        )
        self.assertEqual(
            self.model_resolution.KIMI_NO_AUTO_UPDATE_ENV,
            "KIMI_CODE_NO_AUTO_UPDATE",
        )
        self.assertEqual(
            self.model_resolution.kimi_model_args("kimi-code/k3"),
            ["-m", "kimi-code/k3"],
        )

    def test_codex_worker_command_uses_profile_for_fugu_default_effort(self):
        argv = self.run_arch_epic._codex_worker_argv(
            Path("/repo"),
            "fugu-ultra",
            "xhigh",
            Path("/tmp/final.json"),
            "Do work.",
            codex_profile="fugu-ultra",
        )

        self.assertIn("-p", argv)
        self.assertIn("fugu-ultra", argv)
        self.assertNotIn("--model", argv)
        self.assertNotIn('model_reasoning_effort="xhigh"', argv)

    def test_codex_worker_command_can_override_fugu_profile_effort(self):
        argv = self.run_arch_epic._codex_worker_argv(
            Path("/repo"),
            "fugu-ultra",
            "high",
            Path("/tmp/final.json"),
            "Do work.",
            codex_profile="fugu-ultra",
        )

        self.assertIn("-p", argv)
        self.assertIn("fugu-ultra", argv)
        self.assertNotIn("--model", argv)
        self.assertIn('model_reasoning_effort="high"', argv)

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
        self.assertIn("--model", argv)
        self.assertIn("gpt-5.4-mini", argv)
        self.assertIn("--output-schema", argv)
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", argv)

    def test_codex_critic_command_uses_profile_for_fugu(self):
        argv = self.run_arch_epic._codex_critic_argv(
            Path("/repo"),
            "fugu-ultra",
            "xhigh",
            Path("/tmp/schema.json"),
            Path("/tmp/verdict.json"),
            "Return JSON.",
            codex_profile="fugu-ultra",
        )

        self.assertIn("--ephemeral", argv)
        self.assertIn("-p", argv)
        self.assertIn("fugu-ultra", argv)
        self.assertNotIn("--model", argv)
        self.assertNotIn('model_reasoning_effort="xhigh"', argv)

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

    def test_kimi_worker_command_pins_model_effort_and_exact_resume(self):
        prompt = "Implement this exact scope."
        argv = self.run_arch_epic._kimi_worker_argv(
            "kimi-code/k3",
            "medium",
            prompt,
            session_id="session_abc123",
        )

        self.assertEqual(argv[0], "env")
        self.assertIn("KIMI_CODE_NO_AUTO_UPDATE=1", argv)
        self.assertIn("KIMI_MODEL_THINKING_EFFORT=medium", argv)
        self.assertEqual(argv[argv.index("-m") + 1], "kimi-code/k3")
        self.assertEqual(argv[argv.index("-r") + 1], "session_abc123")
        self.assertEqual(argv[argv.index("-p") + 1], prompt)
        self.assertEqual(argv[argv.index("--output-format") + 1], "stream-json")
        self.assertNotIn("--cwd", argv)

    def test_kimi_critic_command_carries_inline_schema_prompt(self):
        prompt = self.run_arch_epic._prompt_with_schema(
            "Review this.",
            {"type": "object", "required": ["verdict"]},
        )
        argv = self.run_arch_epic._kimi_critic_argv(
            "kimi-code/k3",
            "max",
            prompt,
        )

        self.assertEqual(argv[argv.index("-p") + 1], prompt)
        self.assertIn("## JSON Schema", prompt)
        self.assertNotIn("-r", argv)

    def test_kimi_parser_collects_assistant_text_and_resume_hint(self):
        stream = "\n".join(
            [
                "not json",
                json.dumps({"role": "assistant", "content": "hello "}),
                json.dumps({"role": "assistant", "content": "world"}),
                json.dumps(
                    {
                        "role": "meta",
                        "type": "session.resume_hint",
                        "session_id": "session_xyz",
                        "command": "kimi -r session_xyz",
                    }
                ),
            ]
        )

        final = self.run_arch_epic._parse_kimi_final_json(stream)

        self.assertEqual(final["result"], "hello world")
        self.assertEqual(final["session_id"], "session_xyz")
        self.assertEqual(
            self.run_arch_epic._parse_kimi_session_id(stream),
            "session_xyz",
        )

    def test_kimi_parser_rejects_errors_and_empty_assistant_output(self):
        cases = [
            json.dumps(
                {
                    "role": "meta",
                    "type": "session.resume_hint",
                    "session_id": "session_only",
                }
            ),
            "\n".join(
                [
                    json.dumps({"role": "assistant", "content": "partial"}),
                    json.dumps({"role": "error", "content": "failed"}),
                ]
            ),
            json.dumps({"role": "assistant", "content": "   "}),
        ]
        for stream in cases:
            with self.subTest(stream=stream):
                self.assertIsNone(
                    self.run_arch_epic._parse_kimi_final_json(stream)
                )

    def test_grok_parser_requires_nonempty_text_and_rejects_errors(self):
        session_only = json.dumps({"type": "end", "sessionId": "grok-session"})
        explicit_error = "\n".join(
            [
                json.dumps({"type": "text", "data": "partial"}),
                json.dumps({"type": "error", "error": "failed"}),
            ]
        )
        success = "\n".join(
            [
                json.dumps({"type": "text", "data": "done"}),
                json.dumps({"type": "end", "sessionId": "grok-session"}),
            ]
        )
        nonterminal_session = "\n".join(
            [
                json.dumps(
                    {
                        "type": "text",
                        "data": "done",
                        "sessionId": "not-authoritative",
                    }
                ),
                json.dumps({"type": "end"}),
            ]
        )

        self.assertIsNone(self.run_arch_epic._parse_grok_final_json(session_only))
        self.assertIsNone(self.run_arch_epic._parse_grok_final_json(explicit_error))
        self.assertEqual(
            self.run_arch_epic._parse_grok_final_json(success),
            {
                "type": "grok_result",
                "result": "done",
                "session_id": "grok-session",
            },
        )
        self.assertIsNone(
            self.run_arch_epic._parse_grok_final_json(nonterminal_session)[
                "session_id"
            ]
        )

    def test_critic_spawn_parser_accepts_kimi_runtime(self):
        parser = self.run_arch_epic._build_parser()
        args = parser.parse_args(
            [
                "critic-spawn",
                "--epic-doc",
                "/tmp/epic.md",
                "--sub-plan-name",
                "one",
                "--sub-plan-doc-path",
                "/tmp/sub-plan.md",
                "--prompt-file",
                "/tmp/prompt.md",
                "--schema-file",
                "/tmp/schema.json",
                "--model",
                "kimi-code/k3",
                "--effort",
                "max",
                "--runtime",
                "kimi",
            ]
        )

        self.assertEqual(args.runtime, "kimi")

    def test_kimi_worker_finalization_persists_result_and_session(self):
        with tempfile.TemporaryDirectory() as td:
            try_dir = Path(td) / "workers" / "implementation_worker" / "one" / "try-1"
            try_dir.mkdir(parents=True)
            final_path = try_dir / "stdout.final.json"
            (try_dir / "metadata.json").write_text(
                json.dumps(
                    {
                        "runtime": "kimi",
                        "role": "implementation_worker",
                        "sub_plan_name": "one",
                        "final_path": str(final_path),
                        "input_session_id": None,
                    }
                ),
                encoding="utf-8",
            )
            (try_dir / "events.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps({"role": "assistant", "content": "complete"}),
                        json.dumps(
                            {
                                "role": "meta",
                                "type": "session.resume_hint",
                                "session_id": "session_final",
                            }
                        ),
                    ]
                ),
                encoding="utf-8",
            )

            session_id = self.run_arch_epic._finalize_worker_try_dir(try_dir)
            final = json.loads(final_path.read_text(encoding="utf-8"))

        self.assertEqual(session_id, "session_final")
        self.assertEqual(final["result"], "complete")

    def test_kimi_worker_finalization_requires_new_resume_hint(self):
        with tempfile.TemporaryDirectory() as td:
            try_dir = Path(td) / "workers" / "implementation_worker" / "one" / "try-2"
            try_dir.mkdir(parents=True)
            (try_dir / "metadata.json").write_text(
                json.dumps(
                    {
                        "runtime": "kimi",
                        "role": "implementation_worker",
                        "sub_plan_name": "one",
                        "final_path": str(try_dir / "stdout.final.json"),
                        "input_session_id": "session_previous",
                    }
                ),
                encoding="utf-8",
            )
            (try_dir / "events.jsonl").write_text(
                json.dumps({"role": "assistant", "content": "complete"}),
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(
                SystemExit
            ) as raised:
                self.run_arch_epic._finalize_worker_try_dir(try_dir)

            receipt = (try_dir / "session_id.txt").read_text(encoding="utf-8")

        self.assertEqual(raised.exception.code, 4)
        self.assertEqual(receipt, "UNRECOVERABLE\n")

    def test_kimi_critic_finalization_extracts_json_verdict(self):
        with tempfile.TemporaryDirectory() as td:
            critic_dir = Path(td) / "critic"
            critic_dir.mkdir()
            final_path = critic_dir / "stdout.final.json"
            verdict_path = critic_dir / "verdict.json"
            (critic_dir / "metadata.json").write_text(
                json.dumps(
                    {
                        "runtime": "kimi",
                        "final_path": str(final_path),
                        "verdict_path": str(verdict_path),
                    }
                ),
                encoding="utf-8",
            )
            (critic_dir / "events.jsonl").write_text(
                json.dumps(
                    {
                        "role": "assistant",
                        "content": '{"verdict":"PASS","findings":[]}',
                    }
                ),
                encoding="utf-8",
            )

            returned_path = self.run_arch_epic._finalize_critic_run_dir(critic_dir)
            verdict = json.loads(verdict_path.read_text(encoding="utf-8"))

        self.assertEqual(returned_path, verdict_path)
        self.assertEqual(verdict, {"findings": [], "verdict": "PASS"})

    def test_kimi_worker_dispatch_uses_target_repo_as_subprocess_cwd(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            run_dir = base / "run"
            run_dir.mkdir()
            target_repo = base / "target"
            target_repo.mkdir()
            prompt_path = base / "prompt.md"
            prompt_path.write_text("Implement.", encoding="utf-8")
            (run_dir / "state.json").write_text(
                json.dumps(
                    {
                        "auto_execution": {
                            "roles": {
                                "implementation_worker": {
                                    "runtime": "kimi",
                                    "model": "kimi-code/k3",
                                    "effort": "max",
                                }
                            }
                        },
                        "latest_worker_attempts": {},
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(
                self.run_arch_epic,
                "_run_subprocess",
                return_value=(0, ""),
            ) as run, contextlib.redirect_stdout(io.StringIO()):
                code = self.run_arch_epic._run_worker(
                    run_dir=run_dir,
                    target_repo=target_repo,
                    role="implementation_worker",
                    sub_plan_name="one",
                    prompt_file=prompt_path,
                    try_k=1,
                    run_mode="detached",
                )

        self.assertEqual(code, 0)
        self.assertEqual(
            Path(run.call_args.kwargs["cwd"]).resolve(),
            target_repo.resolve(),
        )
        self.assertTrue(run.call_args.kwargs["detached"])
        self.assertIn("kimi", run.call_args.args[0])

    def test_kimi_auto_critic_dispatch_uses_target_repo_as_subprocess_cwd(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            run_dir = base / "run"
            run_dir.mkdir()
            target_repo = base / "target"
            target_repo.mkdir()
            prompt_path = base / "prompt.md"
            prompt_path.write_text("Review.", encoding="utf-8")
            schema_path = base / "schema.json"
            schema_path.write_text('{"type":"object"}', encoding="utf-8")
            (run_dir / "state.json").write_text(
                json.dumps(
                    {
                        "auto_execution": {
                            "roles": {
                                "critic": {
                                    "runtime": "kimi",
                                    "model": "kimi-code/k3",
                                    "effort": "max",
                                }
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            args = self.run_arch_epic.argparse.Namespace(
                run_dir=str(run_dir),
                target_repo=str(target_repo),
                role="critic",
                gate="completion",
                sub_plan_name="one",
                prompt_file=str(prompt_path),
                schema_file=str(schema_path),
                run_mode="detached",
                expected_duration="short",
            )
            with mock.patch.object(
                self.run_arch_epic,
                "_run_subprocess",
                return_value=(0, ""),
            ) as run, contextlib.redirect_stdout(io.StringIO()):
                code = self.run_arch_epic.cmd_auto_critic_spawn(args)
            submitted_prompt = run.call_args.args[0][
                run.call_args.args[0].index("-p") + 1
            ]
            [persisted_prompt_path] = list(
                (run_dir / "critics" / "completion" / "one").glob(
                    "run-*/prompt.kimi.md"
                )
            )
            persisted_prompt = persisted_prompt_path.read_text(encoding="utf-8")
            self.assertEqual(persisted_prompt, submitted_prompt)
            self.assertIn("## JSON Schema", persisted_prompt)

        self.assertEqual(code, 0)
        self.assertEqual(
            Path(run.call_args.kwargs["cwd"]).resolve(),
            target_repo.resolve(),
        )
        self.assertTrue(run.call_args.kwargs["detached"])
        argv = run.call_args.args[0]
        self.assertIn("kimi", argv)
        self.assertIn("## JSON Schema", argv[argv.index("-p") + 1])

    def test_kimi_standalone_critic_dispatch_uses_orchestrator_root_cwd(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            epic_path = root / "epic.md"
            epic_path.write_text("# Epic", encoding="utf-8")
            sub_plan_path = root / "sub-plan.md"
            sub_plan_path.write_text("# Sub-plan", encoding="utf-8")
            prompt_path = root / "prompt.md"
            prompt_path.write_text("Review.", encoding="utf-8")
            schema_path = root / "schema.json"
            schema_path.write_text('{"type":"object"}', encoding="utf-8")
            parser = self.run_arch_epic._build_parser()
            args = parser.parse_args(
                [
                    "critic-spawn",
                    "--epic-doc",
                    str(epic_path),
                    "--sub-plan-name",
                    "one",
                    "--sub-plan-doc-path",
                    str(sub_plan_path),
                    "--prompt-file",
                    str(prompt_path),
                    "--schema-file",
                    str(schema_path),
                    "--model",
                    "kimi-code/k3",
                    "--effort",
                    "max",
                    "--runtime",
                    "kimi",
                    "--orchestrator-root",
                    str(root),
                    "--run-mode",
                    "detached",
                ]
            )
            with mock.patch.object(
                self.run_arch_epic,
                "_run_subprocess",
                return_value=(0, ""),
            ) as run, contextlib.redirect_stdout(io.StringIO()):
                code = args.func(args)
            submitted_prompt = run.call_args.args[0][
                run.call_args.args[0].index("-p") + 1
            ]
            [persisted_prompt_path] = list(
                (root / ".arch_skill" / "arch-epic" / "critics" / "one").glob(
                    "run-*/prompt.kimi.md"
                )
            )
            persisted_prompt = persisted_prompt_path.read_text(encoding="utf-8")
            self.assertEqual(persisted_prompt, submitted_prompt)
            self.assertIn("## JSON Schema", persisted_prompt)

        self.assertEqual(code, 0)
        self.assertEqual(Path(run.call_args.kwargs["cwd"]).resolve(), root.resolve())
        self.assertTrue(run.call_args.kwargs["detached"])
        self.assertIn("kimi", run.call_args.args[0])

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
                            "implementation_worker": "codex gpt-5.6-sol xhigh",
                            "repair_worker": "same as implementation_worker",
                            "critic": "codex gpt 5.4 mini xhigh",
                        },
                        "codex_models": ["gpt-5.6-sol", "gpt-5.4-mini"],
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
