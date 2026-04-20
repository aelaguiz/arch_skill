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


class LegacyFallbackRemovedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_stop_hook_legacy_removed_test")

    def test_runner_has_no_legacy_fallback_helper(self) -> None:
        self.assertFalse(hasattr(self.stop, "_legacy_fallback_allowed"))

    def test_resolved_controller_state_has_no_is_legacy_attr(self) -> None:
        spec = self.stop.AUDIT_LOOP_STATE_SPEC
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text("{}", encoding="utf-8")
            resolved = self.stop.ResolvedControllerState(spec=spec, state_path=path)
            self.assertFalse(hasattr(resolved, "is_legacy"))

    def test_unsuffixed_claude_state_is_swept_to_stale(self) -> None:
        self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[self.stop.RUNTIME_CLAUDE]
        try:
            with tempfile.TemporaryDirectory() as tmp:
                cwd = Path(tmp).resolve()
                unsuffixed = cwd / ".claude/arch_skill/audit-loop-state.json"
                unsuffixed.parent.mkdir(parents=True, exist_ok=True)
                unsuffixed.write_text(json.dumps({"command": "auto"}), encoding="utf-8")
                moved = self.stop.staleness_sweep(cwd, payload=None, announce=True)
                self.assertFalse(unsuffixed.exists())
                self.assertTrue(
                    any("_stale" in str(p) for p in moved),
                    msg=f"moved={moved}",
                )
        finally:
            self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[self.stop.RUNTIME_CODEX]

    def test_unsuffixed_codex_state_is_swept_to_stale(self) -> None:
        self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[self.stop.RUNTIME_CODEX]
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp).resolve()
            unsuffixed = cwd / ".codex/audit-loop-state.json"
            unsuffixed.parent.mkdir(parents=True, exist_ok=True)
            unsuffixed.write_text(json.dumps({"command": "auto"}), encoding="utf-8")
            moved = self.stop.staleness_sweep(cwd, payload=None, announce=True)
            self.assertFalse(unsuffixed.exists())
            self.assertTrue(
                any("_stale" in str(p) for p in moved),
                msg=f"moved={moved}",
            )

    def test_unsuffixed_state_never_resolves_on_either_runtime(self) -> None:
        for runtime in (self.stop.RUNTIME_CLAUDE, self.stop.RUNTIME_CODEX):
            self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[runtime]
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    cwd = Path(tmp).resolve()
                    state_root = self.stop.ACTIVE_RUNTIME.state_root
                    unsuffixed = cwd / state_root / "audit-loop-state.json"
                    unsuffixed.parent.mkdir(parents=True, exist_ok=True)
                    unsuffixed.write_text(
                        json.dumps({"command": "auto"}), encoding="utf-8"
                    )
                    resolved = self.stop.resolve_active_controller_state(
                        {"cwd": str(cwd)},
                        self.stop.AUDIT_LOOP_STATE_SPEC,
                    )
                    self.assertIsNone(
                        resolved,
                        msg=f"runtime {runtime} resolved unsuffixed state",
                    )
            finally:
                self.stop.ACTIVE_RUNTIME = self.stop.HOOK_RUNTIME_SPECS[self.stop.RUNTIME_CODEX]


if __name__ == "__main__":
    unittest.main()
