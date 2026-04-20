import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = (
    REPO_ROOT / "skills/arch-step/scripts/upsert_claude_session_start_hook.py"
)


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class UpsertClaudeSessionStartHookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.installer = load_module(
            INSTALLER_PATH, "arch_skill_upsert_claude_session_start_hook_test"
        )

    def _skills_dir(self, root: Path) -> Path:
        skills = root / "agents/skills"
        (skills / "arch-step/scripts").mkdir(parents=True, exist_ok=True)
        (skills / "arch-step/scripts/arch_controller_stop_hook.py").write_text(
            "#!/usr/bin/env python3\n", encoding="utf-8"
        )
        return skills

    def test_fresh_settings_gets_one_managed_group(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            settings = root / "claude/settings.json"
            settings.parent.mkdir(parents=True, exist_ok=True)
            skills = self._skills_dir(root)

            self.installer.install_hook(settings, skills)

            data = json.loads(settings.read_text(encoding="utf-8"))
            groups = data["hooks"]["SessionStart"]
            self.assertEqual(len(groups), 1)
            command = groups[0]["hooks"][0]["command"]
            self.assertIn("arch_controller_stop_hook.py", command)
            self.assertIn("--session-start-cache", command)
            self.assertEqual(groups[0]["hooks"][0]["timeout"], self.installer.HOOK_TIMEOUT_SEC)

    def test_install_dedupes_existing_managed_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            settings = root / "claude/settings.json"
            settings.parent.mkdir(parents=True, exist_ok=True)
            skills = self._skills_dir(root)
            stale_command = (
                f"python3 /old/path/arch_controller_stop_hook.py --session-start-cache"
            )
            data = {
                "hooks": {
                    "SessionStart": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": stale_command,
                                    "timeout": 10000,
                                }
                            ]
                        },
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "echo something-else",
                                    "timeout": 5,
                                }
                            ]
                        },
                    ]
                }
            }
            settings.write_text(json.dumps(data), encoding="utf-8")

            self.installer.install_hook(settings, skills)
            new_data = json.loads(settings.read_text(encoding="utf-8"))
            groups = new_data["hooks"]["SessionStart"]
            self.assertEqual(len(groups), 2)
            managed = self.installer.repo_managed_groups(groups)
            self.assertEqual(len(managed), 1)
            command = managed[0]["hooks"][0]["command"]
            self.assertNotIn("/old/path/", command)
            self.assertIn(str(skills), command)

    def test_verify_passes_when_installed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            settings = root / "claude/settings.json"
            settings.parent.mkdir(parents=True, exist_ok=True)
            skills = self._skills_dir(root)
            self.installer.install_hook(settings, skills)
            self.installer.verify_hook(settings, skills)

    def test_verify_fails_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            settings = root / "claude/settings.json"
            settings.parent.mkdir(parents=True, exist_ok=True)
            skills = self._skills_dir(root)
            settings.write_text(json.dumps({"hooks": {}}), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                self.installer.verify_hook(settings, skills)
            self.assertIn("missing arch_skill SessionStart", str(ctx.exception))

    def test_verify_fails_when_stale_command_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            settings = root / "claude/settings.json"
            settings.parent.mkdir(parents=True, exist_ok=True)
            skills = self._skills_dir(root)
            data = {
                "hooks": {
                    "SessionStart": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": (
                                        "python3 /old/arch_controller_stop_hook.py"
                                        " --session-start-cache"
                                    ),
                                    "timeout": 10000,
                                }
                            ]
                        }
                    ]
                }
            }
            settings.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                self.installer.verify_hook(settings, skills)
            self.assertIn("stale SessionStart hook entry", str(ctx.exception))

    def test_verify_fails_when_multiple_managed_groups(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            settings = root / "claude/settings.json"
            settings.parent.mkdir(parents=True, exist_ok=True)
            skills = self._skills_dir(root)
            command = self.installer.expected_command(skills)
            group = self.installer.expected_group(command)
            data = {"hooks": {"SessionStart": [group, group]}}
            settings.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                self.installer.verify_hook(settings, skills)
            self.assertIn("expected exactly one", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
