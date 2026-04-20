import importlib.util
import json
import os
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


class EnsureInstalledTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_stop_hook_ensure_install_test")

    def _copy_skills_tree(self, dest: Path) -> Path:
        skills_src = REPO_ROOT / "skills"
        import shutil

        skills_dest = dest / "skills"
        shutil.copytree(skills_src, skills_dest)
        return skills_dest

    def _patch_paths(self, fake_home: Path) -> None:
        skills_dir = self._copy_skills_tree(fake_home / ".agents")
        runner_path = skills_dir / "arch-step/scripts/arch_controller_stop_hook.py"
        self.stop._INSTALLED_RUNNER_PATH = runner_path
        self.stop._INSTALLED_SKILLS_DIR = skills_dir
        self.stop._CODEX_HOOKS_FILE = fake_home / ".codex/hooks.json"
        self.stop._CLAUDE_SETTINGS_FILE = fake_home / ".claude/settings.json"

    def _restore_paths(self) -> None:
        self.stop._INSTALLED_RUNNER_PATH = Path.home() / ".agents/skills/arch-step/scripts/arch_controller_stop_hook.py"
        self.stop._INSTALLED_SKILLS_DIR = Path.home() / ".agents/skills"
        self.stop._CODEX_HOOKS_FILE = Path.home() / ".codex/hooks.json"
        self.stop._CLAUDE_SETTINGS_FILE = Path.home() / ".claude/settings.json"

    def test_ensure_installed_codex_fresh_writes_canonical_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            self._patch_paths(fake_home)
            try:
                self.stop.cmd_ensure_installed(self.stop.RUNTIME_CODEX)
                hooks = json.loads(self.stop._CODEX_HOOKS_FILE.read_text(encoding="utf-8"))
                stop_groups = hooks["hooks"]["Stop"]
                self.assertEqual(len(stop_groups), 1)
                command = stop_groups[0]["hooks"][0]["command"]
                self.assertIn("arch_controller_stop_hook.py", command)
                self.assertIn("--runtime codex", command)
            finally:
                self._restore_paths()

    def test_ensure_installed_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            self._patch_paths(fake_home)
            try:
                self.stop.cmd_ensure_installed(self.stop.RUNTIME_CODEX)
                first_bytes = self.stop._CODEX_HOOKS_FILE.read_text(encoding="utf-8")
                self.stop.cmd_ensure_installed(self.stop.RUNTIME_CODEX)
                second_bytes = self.stop._CODEX_HOOKS_FILE.read_text(encoding="utf-8")
                self.assertEqual(first_bytes, second_bytes)
            finally:
                self._restore_paths()

    def test_ensure_installed_preserves_third_party_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            self._patch_paths(fake_home)
            try:
                self.stop._CODEX_HOOKS_FILE.parent.mkdir(parents=True, exist_ok=True)
                third_party = {
                    "hooks": {
                        "Stop": [
                            {
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "python3 /tmp/third-party.py",
                                        "timeoutSec": 60,
                                        "statusMessage": "third-party",
                                    }
                                ]
                            }
                        ]
                    }
                }
                self.stop._CODEX_HOOKS_FILE.write_text(
                    json.dumps(third_party, indent=2) + "\n", encoding="utf-8"
                )
                self.stop.cmd_ensure_installed(self.stop.RUNTIME_CODEX)
                hooks = json.loads(self.stop._CODEX_HOOKS_FILE.read_text(encoding="utf-8"))
                stop_groups = hooks["hooks"]["Stop"]
                self.assertEqual(len(stop_groups), 2)
                commands = [g["hooks"][0]["command"] for g in stop_groups]
                self.assertTrue(any("third-party" in c for c in commands))
                self.assertTrue(any("arch_controller_stop_hook.py" in c for c in commands))
            finally:
                self._restore_paths()

    def test_ensure_installed_claude_writes_stop_and_session_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            self._patch_paths(fake_home)
            try:
                self.stop.cmd_ensure_installed(self.stop.RUNTIME_CLAUDE)
                settings = json.loads(self.stop._CLAUDE_SETTINGS_FILE.read_text(encoding="utf-8"))
                stop_groups = settings["hooks"]["Stop"]
                self.assertEqual(len(stop_groups), 1)
                self.assertIn("--runtime claude", stop_groups[0]["hooks"][0]["command"])
                start_groups = settings["hooks"]["SessionStart"]
                self.assertEqual(len(start_groups), 1)
                self.assertIn("--session-start-cache", start_groups[0]["hooks"][0]["command"])
            finally:
                self._restore_paths()

    def test_ensure_installed_requires_runtime_flag(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(STOP_HOOK_PATH), "--ensure-installed"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("--ensure-installed requires --runtime", proc.stderr)

    def test_ensure_installed_rejects_unknown_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            self._patch_paths(fake_home)
            try:
                with self.assertRaises(SystemExit) as ctx:
                    self.stop.ensure_installed("gemini")
                self.assertIn("unknown runtime", str(ctx.exception))
            finally:
                self._restore_paths()


if __name__ == "__main__":
    unittest.main()
