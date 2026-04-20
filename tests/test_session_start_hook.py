import importlib.util
import io
import json
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


class SessionStartCacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_session_start_cache_test")

    def _invoke(self, tmp: str, payload_text: str, ppid: int):
        cache_root = Path(tmp) / "sessions"
        with mock.patch.object(self.stop, "_SESSION_CACHE_ROOT", cache_root), \
             mock.patch.object(self.stop.os, "getppid", return_value=ppid), \
             mock.patch.object(self.stop.sys, "stdin", io.StringIO(payload_text)), \
             mock.patch.object(self.stop.sys, "stderr", io.StringIO()) as err:
            rc = self.stop.cmd_session_start_cache()
        return rc, cache_root, err.getvalue()

    def test_valid_payload_writes_cache_file(self) -> None:
        payload = json.dumps(
            {
                "session_id": "sess-abc",
                "cwd": "/workspace/example",
                "hook_event_name": "SessionStart",
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            rc, cache_root, _err = self._invoke(tmp, payload, ppid=99099)
            self.assertEqual(rc, 0)
            cache_path = cache_root / "99099.json"
            self.assertTrue(cache_path.exists())
            record = json.loads(cache_path.read_text(encoding="utf-8"))
            self.assertEqual(record["session_id"], "sess-abc")
            self.assertEqual(record["pid"], 99099)
            self.assertEqual(record["cwd"], "/workspace/example")
            self.assertIsInstance(record["armed_at"], int)

    def test_missing_session_id_fails_loud(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rc, cache_root, err = self._invoke(tmp, json.dumps({"cwd": "/tmp"}), ppid=12345)
            self.assertEqual(rc, 2)
            self.assertFalse(cache_root.exists() and any(cache_root.iterdir()))
            self.assertIn("session_id", err)

    def test_malformed_json_fails_loud(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rc, cache_root, err = self._invoke(tmp, "{not json", ppid=12345)
            self.assertEqual(rc, 2)
            self.assertFalse(cache_root.exists() and any(cache_root.iterdir()))
            self.assertIn("invalid SessionStart input", err)

    def test_non_object_payload_fails_loud(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rc, _cache_root, err = self._invoke(
                tmp, json.dumps(["not", "an", "object"]), ppid=12345
            )
            self.assertEqual(rc, 2)
            self.assertIn("JSON object", err)


if __name__ == "__main__":
    unittest.main()
