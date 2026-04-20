import importlib.util
import io
import json
import sys
import tempfile
import time
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


class CurrentSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_current_session_test")

    def _run(
        self,
        cache_root: Path,
        *,
        start_pid: int,
        walker: dict[int, tuple[int, str]],
    ):
        def fake_ps(pid: int):
            return walker.get(pid)

        out = io.StringIO()
        err = io.StringIO()
        with mock.patch.object(self.stop, "_SESSION_CACHE_ROOT", cache_root), \
             mock.patch.object(self.stop.os, "getppid", return_value=start_pid), \
             mock.patch.object(self.stop, "_ps_lookup", side_effect=fake_ps), \
             mock.patch.object(self.stop.sys, "stdout", out), \
             mock.patch.object(self.stop.sys, "stderr", err):
            rc = self.stop.cmd_current_session()
        return rc, out.getvalue(), err.getvalue()

    def _write_cache(self, cache_root: Path, cli_pid: int, session_id: str) -> Path:
        cache_root.mkdir(parents=True, exist_ok=True)
        path = cache_root / f"{cli_pid}.json"
        path.write_text(
            json.dumps(
                {
                    "session_id": session_id,
                    "pid": cli_pid,
                    "cwd": "/tmp/example",
                    "armed_at": int(time.time()),
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_cache_hit_prints_session_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp)
            self._write_cache(cache_root, cli_pid=42000, session_id="sess-live")
            walker = {
                101: (202, "python3"),
                202: (303, "sh"),
                303: (42000, "bash"),
                42000: (1, "claude"),
            }
            rc, out, err = self._run(cache_root, start_pid=101, walker=walker)
            self.assertEqual(rc, 0)
            self.assertEqual(out.strip(), "sess-live")
            self.assertEqual(err, "")

    def test_missing_cache_emits_loud_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp)
            walker = {
                101: (202, "python3"),
                202: (42000, "bash"),
                42000: (1, "claude"),
            }
            rc, _out, err = self._run(cache_root, start_pid=101, walker=walker)
            self.assertEqual(rc, 2)
            self.assertIn("SessionStart hook cache missing", err)
            self.assertIn("Restart the Claude Code session", err)
            self.assertIn("make install", err)

    def test_missing_claude_ancestor_emits_loud_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp)
            walker = {
                101: (202, "python3"),
                202: (1, "tmux"),
            }
            rc, _out, err = self._run(cache_root, start_pid=101, walker=walker)
            self.assertEqual(rc, 2)
            self.assertIn("SessionStart hook cache missing", err)

    def test_malformed_cache_emits_loud_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp)
            cache_root.mkdir(parents=True, exist_ok=True)
            (cache_root / "42000.json").write_text("{ not json", encoding="utf-8")
            walker = {
                101: (42000, "bash"),
                42000: (1, "claude"),
            }
            rc, _out, err = self._run(cache_root, start_pid=101, walker=walker)
            self.assertEqual(rc, 2)
            self.assertIn("SessionStart hook cache missing", err)

    def test_resolver_picks_matching_pid_when_multiple_cache_files_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp)
            self._write_cache(cache_root, cli_pid=10000, session_id="sess-other")
            self._write_cache(cache_root, cli_pid=20000, session_id="sess-mine")
            walker = {
                500: (600, "python3"),
                600: (20000, "bash"),
                20000: (1, "claude"),
            }
            rc, out, _err = self._run(cache_root, start_pid=500, walker=walker)
            self.assertEqual(rc, 0)
            self.assertEqual(out.strip(), "sess-mine")


if __name__ == "__main__":
    unittest.main()
