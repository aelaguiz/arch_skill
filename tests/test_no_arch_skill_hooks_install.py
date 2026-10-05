import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def make_var_words(makefile: str, variable: str) -> list[str]:
    match = re.search(rf"^{variable} := (.*)$", makefile, re.MULTILINE)
    assert match is not None, variable
    return match.group(1).split()


def load_script(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class NoArchSkillHooksInstallTests(unittest.TestCase):
    def test_makefile_removes_hook_only_surface(self) -> None:
        makefile = read(REPO_ROOT / "Makefile")

        self.assertNotIn("codex_install_hook", makefile)
        self.assertNotIn("claude_install_hook", makefile)
        self.assertNotIn("verify_hook_runner", makefile)
        self.assertNotIn("ensure_installed:", makefile)
        self.assertIn("clean_installed_hooks", makefile)
        self.assertIn("--verify-absent", makefile)

        for variable in ["SKILLS", "CLAUDE_SKILLS", "GEMINI_SKILLS"]:
            installed = make_var_words(makefile, variable)
            self.assertNotIn("arch-loop", installed)
            self.assertNotIn("delay-poll", installed)
            self.assertNotIn("wait", installed)

        removed = make_var_words(makefile, "REMOVED_SKILLS")
        self.assertIn("arch-loop", removed)
        self.assertIn("delay-poll", removed)
        self.assertIn("wait", removed)

    def test_utility_owned_eli10_is_neither_installed_nor_purged(self) -> None:
        makefile = read(REPO_ROOT / "Makefile")

        for variable in ["SKILLS", "CLAUDE_SKILLS", "GEMINI_SKILLS"]:
            self.assertNotIn("eli10", make_var_words(makefile, variable))
        self.assertNotIn("eli10", make_var_words(makefile, "REMOVED_SKILLS"))

    def test_codex_cleanup_removes_only_arch_skill_stop_hooks(self) -> None:
        module = load_script(
            REPO_ROOT / "skills/arch-step/scripts/upsert_codex_stop_hook.py"
        )
        unrelated = {"hooks": [{"type": "command", "command": "python3 other.py"}]}
        stale_by_message = {
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 something_else.py",
                    "statusMessage": module.STATUS_MESSAGE,
                }
            ]
        }
        stale_by_runner = {
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 /tmp/arch_controller_stop_hook.py --runtime codex",
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            hooks_file = Path(tmpdir) / "hooks.json"
            hooks_file.write_text(
                json.dumps({"hooks": {"Stop": [unrelated, stale_by_message, stale_by_runner]}}),
                encoding="utf-8",
            )

            module.remove_hook(hooks_file)
            data = json.loads(hooks_file.read_text(encoding="utf-8"))
            module.verify_absent(hooks_file)

        self.assertEqual(data["hooks"]["Stop"], [unrelated])

    def test_claude_cleanup_removes_stop_and_session_start_hooks(self) -> None:
        stop_module = load_script(
            REPO_ROOT / "skills/arch-step/scripts/upsert_claude_stop_hook.py"
        )
        start_module = load_script(
            REPO_ROOT / "skills/arch-step/scripts/upsert_claude_session_start_hook.py"
        )
        unrelated_stop = {"hooks": [{"type": "command", "command": "python3 other.py"}]}
        stale_stop = {
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 /tmp/arch_controller_stop_hook.py --runtime claude",
                }
            ]
        }
        unrelated_start = {"hooks": [{"type": "command", "command": "python3 start.py"}]}
        stale_start = {
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 /tmp/arch_controller_stop_hook.py --session-start-cache",
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            settings_file = Path(tmpdir) / "settings.json"
            settings_file.write_text(
                json.dumps(
                    {
                        "hooks": {
                            "Stop": [unrelated_stop, stale_stop],
                            "SessionStart": [unrelated_start, stale_start],
                        }
                    }
                ),
                encoding="utf-8",
            )

            stop_module.remove_hook(settings_file)
            start_module.remove_hook(settings_file)
            data = json.loads(settings_file.read_text(encoding="utf-8"))
            stop_module.verify_absent(settings_file)
            start_module.verify_absent(settings_file)

        self.assertEqual(data["hooks"]["Stop"], [unrelated_stop])
        self.assertEqual(data["hooks"]["SessionStart"], [unrelated_start])

    def test_removed_hook_sources_are_absent(self) -> None:
        absent_paths = [
            "skills/_shared/controller-contract.md",
            "skills/arch-step/scripts/arch_controller_stop_hook.py",
            "skills/arch-loop/SKILL.md",
            "skills/delay-poll/SKILL.md",
            "skills/wait/SKILL.md",
        ]

        for relative_path in absent_paths:
            self.assertFalse((REPO_ROOT / relative_path).exists(), relative_path)


if __name__ == "__main__":
    unittest.main()
