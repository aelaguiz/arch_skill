import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
STOP_HOOK_PATH = REPO_ROOT / "skills/arch-step/scripts/arch_controller_stop_hook.py"


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _seed_state_file(root: Path, relative: Path) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")
    return path


class DisarmFlagTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_stop_hook_disarm_test")

    def test_disarm_named_controller_only_removes_matching_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            audit_state = _seed_state_file(
                root, Path(".codex/audit-loop-state.abc.json")
            )
            wait_state = _seed_state_file(
                root, Path(".claude/arch_skill/wait-state.xyz.json")
            )

            with mock.patch.object(sys, "stdout", new_callable=io.StringIO):
                rc = self.stop.cmd_disarm("audit-loop", root=root, session_id=None)

            self.assertEqual(rc, 0)
            self.assertFalse(audit_state.exists())
            self.assertTrue(wait_state.exists())

    def test_disarm_with_session_only_removes_that_session(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session_a = _seed_state_file(
                root, Path(".codex/audit-loop-state.aaa.json")
            )
            session_b = _seed_state_file(
                root, Path(".codex/audit-loop-state.bbb.json")
            )

            with mock.patch.object(sys, "stdout", new_callable=io.StringIO):
                rc = self.stop.cmd_disarm("audit-loop", root=root, session_id="aaa")

            self.assertEqual(rc, 0)
            self.assertFalse(session_a.exists())
            self.assertTrue(session_b.exists())

    def test_disarm_unknown_controller_fails_loud(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.object(sys, "stderr", new_callable=io.StringIO) as err:
                rc = self.stop.cmd_disarm("not-a-controller", root=root, session_id=None)
            self.assertEqual(rc, 2)
            self.assertIn("unknown controller", err.getvalue())

    def test_disarm_all_requires_yes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_path = _seed_state_file(
                root, Path(".codex/auto-plan-state.zzz.json")
            )

            with mock.patch.object(sys, "stderr", new_callable=io.StringIO) as err:
                rc = self.stop.cmd_disarm_all(root, confirmed=False)

            self.assertEqual(rc, 2)
            self.assertIn("--yes", err.getvalue())
            self.assertTrue(state_path.exists())

    def test_disarm_all_with_yes_removes_everything(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = _seed_state_file(root, Path(".codex/audit-loop-state.abc.json"))
            b = _seed_state_file(
                root, Path(".claude/arch_skill/wait-state.xyz.json")
            )
            c = _seed_state_file(
                root, Path(".codex/implement-loop-state.qqq.json")
            )

            with mock.patch.object(sys, "stdout", new_callable=io.StringIO):
                rc = self.stop.cmd_disarm_all(root, confirmed=True)

            self.assertEqual(rc, 0)
            self.assertFalse(a.exists())
            self.assertFalse(b.exists())
            self.assertFalse(c.exists())

    def test_cli_list_controllers_prints_registry_table(self) -> None:
        result = subprocess.run(
            [sys.executable, str(STOP_HOOK_PATH), "--list-controllers"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("audit-loop", result.stdout)
        self.assertIn("wait-state.json", result.stdout)
        self.assertIn("name\tstate-file\tdisplay", result.stdout)


if __name__ == "__main__":
    unittest.main()
