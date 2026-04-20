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


class ClaudeSessionIdRequiredTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(
            STOP_HOOK_PATH, "arch_skill_stop_hook_claude_session_required_test"
        )

    def _seed_unsuffixed_state(self, cwd: Path, relative: Path) -> Path:
        path = cwd / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"command": "auto"}),
            encoding="utf-8",
        )
        return path

    def test_claude_runtime_rejects_unsuffixed_state(self) -> None:
        self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[
            self.stop.RUNTIME_CLAUDE
        ]
        try:
            with tempfile.TemporaryDirectory() as tmp:
                cwd = Path(tmp)
                self._seed_unsuffixed_state(
                    cwd, Path(".claude/arch_skill/audit-loop-state.json")
                )
                resolved = self.stop.resolve_active_controller_state(
                    {"cwd": str(cwd)},
                    self.stop.AUDIT_LOOP_STATE_SPEC,
                )
                self.assertIsNone(resolved)
        finally:
            self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[
                self.stop.RUNTIME_CODEX
            ]

    def test_codex_runtime_rejects_unsuffixed_state(self) -> None:
        self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[
            self.stop.RUNTIME_CODEX
        ]
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            self._seed_unsuffixed_state(
                cwd, Path(".codex/audit-loop-state.json")
            )
            resolved = self.stop.resolve_active_controller_state(
                {"cwd": str(cwd)},
                self.stop.AUDIT_LOOP_STATE_SPEC,
            )
            self.assertIsNone(resolved)

    def test_claude_session_scoped_path_resolves(self) -> None:
        self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[
            self.stop.RUNTIME_CLAUDE
        ]
        try:
            with tempfile.TemporaryDirectory() as tmp:
                cwd = Path(tmp)
                session_path = cwd / ".claude/arch_skill/audit-loop-state.sess-1.json"
                session_path.parent.mkdir(parents=True, exist_ok=True)
                session_path.write_text(
                    json.dumps(
                        {
                            "command": "auto",
                            "session_id": "sess-1",
                        }
                    ),
                    encoding="utf-8",
                )
                resolved = self.stop.resolve_active_controller_state(
                    {"cwd": str(cwd), "session_id": "sess-1"},
                    self.stop.AUDIT_LOOP_STATE_SPEC,
                )
                self.assertIsNotNone(resolved)
                self.assertEqual(resolved.state_path, session_path.resolve())
        finally:
            self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[
                self.stop.RUNTIME_CODEX
            ]

    def test_codex_session_scoped_path_resolves(self) -> None:
        self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[
            self.stop.RUNTIME_CODEX
        ]
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp).resolve()
            session_path = cwd / ".codex/audit-loop-state.sess-2.json"
            session_path.parent.mkdir(parents=True, exist_ok=True)
            session_path.write_text(
                json.dumps(
                    {
                        "command": "auto",
                        "session_id": "sess-2",
                    }
                ),
                encoding="utf-8",
            )
            resolved = self.stop.resolve_active_controller_state(
                {"cwd": str(cwd), "session_id": "sess-2"},
                self.stop.AUDIT_LOOP_STATE_SPEC,
            )
            self.assertIsNotNone(resolved)
            self.assertEqual(resolved.state_path, session_path)


if __name__ == "__main__":
    unittest.main()
