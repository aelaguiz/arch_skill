import importlib.util
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


def _write_state(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


class StalenessSweepTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_stop_hook_staleness_test")

    def test_expired_other_session_state_is_moved_to_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stale = _write_state(
                root / ".codex/audit-loop-state.sess-old.json",
                {
                    "version": 1,
                    "command": "audit-loop",
                    "session_id": "sess-old",
                    "deadline_at": int(time.time()) - 3600,
                },
            )

            moved = self.stop.staleness_sweep(root, {"session_id": "sess-current"})

            self.assertEqual(len(moved), 1)
            self.assertFalse(stale.exists())
            self.assertTrue(moved[0].exists())
            self.assertIn("_stale", str(moved[0]))

    def test_fresh_state_is_left_alone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = _write_state(
                root / ".codex/audit-loop-state.sess-new.json",
                {
                    "version": 1,
                    "command": "audit-loop",
                    "session_id": "sess-new",
                    "deadline_at": int(time.time()) + 3600,
                },
            )

            moved = self.stop.staleness_sweep(root, {"session_id": "sess-current"})

            self.assertEqual(moved, [])
            self.assertTrue(fresh.exists())

    def test_matching_session_expired_state_is_not_moved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_path = _write_state(
                root / ".claude/arch_skill/wait-state.sess-cur.json",
                {
                    "version": 1,
                    "command": "wait",
                    "session_id": "sess-cur",
                    "deadline_at": int(time.time()) - 3600,
                },
            )

            moved = self.stop.staleness_sweep(root, {"session_id": "sess-cur"})

            self.assertEqual(moved, [])
            self.assertTrue(state_path.exists())

    def test_malformed_state_is_not_moved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            malformed = root / ".codex/audit-loop-state.bad.json"
            malformed.parent.mkdir(parents=True, exist_ok=True)
            malformed.write_text("{ not json", encoding="utf-8")

            moved = self.stop.staleness_sweep(root, {"session_id": "sess-current"})

            self.assertEqual(moved, [])
            self.assertTrue(malformed.exists())

    def test_no_state_roots_is_safe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            moved = self.stop.staleness_sweep(Path(tmp), None)
            self.assertEqual(moved, [])


class SessionCacheSweepTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(
            STOP_HOOK_PATH, "arch_skill_stop_hook_session_cache_sweep_test"
        )

    def _write_cache(self, root: Path, pid: int, armed_at: int) -> Path:
        root.mkdir(parents=True, exist_ok=True)
        path = root / f"{pid}.json"
        path.write_text(
            json.dumps(
                {
                    "session_id": f"sess-{pid}",
                    "pid": pid,
                    "cwd": "/tmp/example",
                    "armed_at": armed_at,
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_dead_pid_cache_is_moved_to_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp) / "sessions"
            path = self._write_cache(cache_root, pid=424242, armed_at=int(time.time()))
            with mock.patch.object(self.stop, "_SESSION_CACHE_ROOT", cache_root), \
                 mock.patch.object(self.stop, "_pid_alive", return_value=False):
                moved = self.stop._sweep_session_cache()
            self.assertEqual(len(moved), 1)
            self.assertFalse(path.exists())
            self.assertIn("_stale", str(moved[0]))

    def test_expired_armed_at_cache_is_moved_to_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp) / "sessions"
            long_ago = int(time.time()) - (2 * 86_400)
            path = self._write_cache(cache_root, pid=999000, armed_at=long_ago)
            with mock.patch.object(self.stop, "_SESSION_CACHE_ROOT", cache_root), \
                 mock.patch.object(self.stop, "_pid_alive", return_value=True):
                moved = self.stop._sweep_session_cache()
            self.assertEqual(len(moved), 1)
            self.assertFalse(path.exists())

    def test_live_recent_cache_is_left_alone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp) / "sessions"
            path = self._write_cache(cache_root, pid=123, armed_at=int(time.time()))
            with mock.patch.object(self.stop, "_SESSION_CACHE_ROOT", cache_root), \
                 mock.patch.object(self.stop, "_pid_alive", return_value=True):
                moved = self.stop._sweep_session_cache()
            self.assertEqual(moved, [])
            self.assertTrue(path.exists())

    def test_missing_cache_root_is_safe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing_root = Path(tmp) / "does-not-exist"
            with mock.patch.object(self.stop, "_SESSION_CACHE_ROOT", missing_root):
                moved = self.stop._sweep_session_cache()
            self.assertEqual(moved, [])

    def test_malformed_cache_is_left_alone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp) / "sessions"
            cache_root.mkdir(parents=True, exist_ok=True)
            bad = cache_root / "bad.json"
            bad.write_text("{not json", encoding="utf-8")
            with mock.patch.object(self.stop, "_SESSION_CACHE_ROOT", cache_root), \
                 mock.patch.object(self.stop, "_pid_alive", return_value=True):
                moved = self.stop._sweep_session_cache()
            self.assertEqual(moved, [])
            self.assertTrue(bad.exists())


if __name__ == "__main__":
    unittest.main()
