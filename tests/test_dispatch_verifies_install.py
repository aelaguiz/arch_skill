import importlib.util
import json
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


class DispatchVerifiesInstallTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(
            STOP_HOOK_PATH, "arch_skill_stop_hook_dispatch_verify_test"
        )

    def _copy_skills_tree(self, dest: Path) -> Path:
        import shutil

        skills_src = REPO_ROOT / "skills"
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

    def test_verify_fails_loud_when_codex_entry_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            self._patch_paths(fake_home)
            try:
                self.stop._CODEX_HOOKS_FILE.parent.mkdir(parents=True, exist_ok=True)
                self.stop._CODEX_HOOKS_FILE.write_text(
                    json.dumps({"hooks": {"Stop": []}}), encoding="utf-8"
                )

                captured_stderr: list[str] = []
                original_write = sys.stderr.write

                def _capture(msg: str) -> int:
                    captured_stderr.append(msg)
                    return len(msg)

                sys.stderr.write = _capture  # type: ignore[assignment]
                try:
                    with self.assertRaises(SystemExit) as ctx:
                        self.stop.verify_installed_or_die(self.stop.RUNTIME_CODEX)
                finally:
                    sys.stderr.write = original_write  # type: ignore[assignment]

                self.assertEqual(ctx.exception.code, 2)
                joined = "".join(captured_stderr)
                self.assertIn("dispatch-time install verify failed", joined)
                self.assertIn("--ensure-installed --runtime codex", joined)
            finally:
                self._restore_paths()

    def test_verify_fails_loud_when_claude_session_start_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            self._patch_paths(fake_home)
            try:
                self.stop.cmd_ensure_installed(self.stop.RUNTIME_CLAUDE)
                settings = json.loads(
                    self.stop._CLAUDE_SETTINGS_FILE.read_text(encoding="utf-8")
                )
                settings["hooks"].pop("SessionStart", None)
                self.stop._CLAUDE_SETTINGS_FILE.write_text(
                    json.dumps(settings), encoding="utf-8"
                )

                captured_stderr: list[str] = []
                original_write = sys.stderr.write

                def _capture(msg: str) -> int:
                    captured_stderr.append(msg)
                    return len(msg)

                sys.stderr.write = _capture  # type: ignore[assignment]
                try:
                    with self.assertRaises(SystemExit) as ctx:
                        self.stop.verify_installed_or_die(self.stop.RUNTIME_CLAUDE)
                finally:
                    sys.stderr.write = original_write  # type: ignore[assignment]

                self.assertEqual(ctx.exception.code, 2)
                joined = "".join(captured_stderr)
                self.assertIn("--ensure-installed --runtime claude", joined)
            finally:
                self._restore_paths()

    def test_verify_passes_silently_after_ensure_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            self._patch_paths(fake_home)
            try:
                self.stop.cmd_ensure_installed(self.stop.RUNTIME_CODEX)
                self.stop.verify_installed_or_die(self.stop.RUNTIME_CODEX)
            finally:
                self._restore_paths()


if __name__ == "__main__":
    unittest.main()
