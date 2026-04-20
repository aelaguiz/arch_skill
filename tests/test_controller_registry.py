import importlib.util
import sys
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


class ControllerRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stop = load_module(STOP_HOOK_PATH, "arch_skill_stop_hook_registry_test")

    def test_registry_is_non_empty(self) -> None:
        self.assertGreater(len(self.stop.CONTROLLERS), 0)

    def test_every_controller_has_required_fields(self) -> None:
        for name, controller in self.stop.CONTROLLERS.items():
            with self.subTest(controller=name):
                self.assertIsInstance(name, str)
                self.assertTrue(name, msg="controller key must be non-empty")
                self.assertEqual(name, controller.name)
                self.assertTrue(controller.spec.expected_command, "spec.expected_command empty")
                self.assertTrue(str(controller.spec.relative_path), "spec.relative_path empty")
                self.assertTrue(controller.display, "display empty")
                self.assertTrue(controller.dispatch_name, "dispatch_name empty")
                handler = getattr(self.stop, controller.dispatch_name, None)
                self.assertTrue(
                    callable(handler),
                    f"dispatch handler {controller.dispatch_name} is not callable on the module",
                )

    def test_state_filenames_are_unique(self) -> None:
        seen: dict[str, str] = {}
        for name, controller in self.stop.CONTROLLERS.items():
            filename = str(controller.spec.relative_path)
            self.assertNotIn(
                filename,
                seen,
                f"state file '{filename}' reused by {name} and {seen.get(filename)}",
            )
            seen[filename] = name

    def test_every_known_controller_is_in_registry(self) -> None:
        expected = {
            "implement-loop",
            "auto-plan",
            "miniarch-step-implement-loop",
            "miniarch-step-auto-plan",
            "arch-docs-auto",
            "audit-loop",
            "comment-loop",
            "audit-loop-sim",
            "delay-poll",
            "code-review",
            "wait",
            "arch-loop",
        }
        self.assertEqual(expected, set(self.stop.CONTROLLERS.keys()))


if __name__ == "__main__":
    unittest.main()
