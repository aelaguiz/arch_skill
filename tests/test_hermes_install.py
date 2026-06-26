import re
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HERMES_SUBDIR = "arch_skill"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def make_var_words(makefile: str, variable: str) -> list[str]:
    match = re.search(rf"^{variable} := (.*)$", makefile, re.MULTILINE)
    assert match is not None, variable
    return match.group(1).split()


def run_make(target: str, hermes_home: Path, extra: list[str] | None = None):
    return subprocess.run(
        ["make", target, f"HERMES_HOME={hermes_home}", *(extra or [])],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


class HermesInstallInventoryTests(unittest.TestCase):
    def test_makefile_wires_hermes_surface_into_install_and_verify(self) -> None:
        makefile = read(REPO_ROOT / "Makefile")

        self.assertIn("HERMES_HOME ?= $(HOME)/.hermes", makefile)
        self.assertIn(f"HERMES_SKILLS_SUBDIR := {HERMES_SUBDIR}", makefile)
        self.assertIn("ifeq ($(NO_HERMES),1)", makefile)
        self.assertIn("INSTALL_HERMES := hermes_install_skill", makefile)
        self.assertIn("VERIFY_HERMES := verify_hermes_install", makefile)

        install_line = re.search(r"^install: (.*)$", makefile, re.MULTILINE)
        assert install_line is not None
        self.assertIn("$(INSTALL_HERMES)", install_line.group(1))

        verify_line = re.search(r"^verify_install: (.*)$", makefile, re.MULTILINE)
        assert verify_line is not None
        self.assertIn("$(VERIFY_HERMES)", verify_line.group(1))

    def test_hermes_targets_reuse_canonical_inventory_and_prune_internals(self) -> None:
        makefile = read(REPO_ROOT / "Makefile")
        hermes_install = makefile.split("hermes_install_skill:")[1].split(
            "\nverify_install:"
        )[0]

        # Single source of truth: no parallel HERMES skill list exists.
        self.assertNotRegex(makefile, r"^HERMES_SKILLS :=", re.MULTILINE)
        for variable in [
            "$(REMOVED_SKILLS)",
            "$(SKILLS)",
            "$(LOCAL_SKILLS)",
            "$(VENDORED_SKILLS)",
            "$(SHARED_DIRS)",
        ]:
            self.assertIn(variable, hermes_install)

        self.assertIn("cp -R $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill", hermes_install)
        self.assertIn("upsert_*hook.py", hermes_install)
        self.assertIn("arch_controller_stop_hook.py", hermes_install)
        self.assertIn("$(HERMES_HOME)/profiles/*/", hermes_install)

    def test_no_hermes_gate_drops_hermes_targets(self) -> None:
        plan = subprocess.run(
            ["make", "-n", "install", "NO_HERMES=1", "NO_GEMINI=1",
             "AGENTS_SKILLS_DIR=/tmp/arch-skill-noop-agents",
             "CODEX_SKILLS_DIR=/tmp/arch-skill-noop-codex",
             "CLAUDE_SKILLS_DIR=/tmp/arch-skill-noop-claude",
             "HERMES_HOME=/tmp/arch-skill-noop-hermes"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertNotIn("Hermes", plan.stdout)


class HermesInstallFunctionalTests(unittest.TestCase):
    def assert_root_installed(self, root: Path) -> None:
        makefile = read(REPO_ROOT / "Makefile")
        dest = root / HERMES_SUBDIR

        for skill in make_var_words(makefile, "SKILLS"):
            self.assertTrue(
                (dest / skill / "SKILL.md").is_file(), f"{dest}/{skill}/SKILL.md"
            )
        for skill in make_var_words(makefile, "REMOVED_SKILLS"):
            self.assertFalse((dest / skill).exists(), f"{dest}/{skill}")

        self.assertTrue((dest / "_shared/depth-first-planning.md").is_file())
        self.assertTrue((dest / "_shared/model_resolution.py").is_file())

        leftovers = [
            p
            for p in dest.rglob("*")
            if p.name in {"build", "prompts", "__pycache__", "arch_controller_stop_hook.py"}
            or p.suffix == ".pyc"
            or (p.name.startswith("upsert_") and p.name.endswith("hook.py"))
        ]
        self.assertEqual(leftovers, [], leftovers)

    def test_install_populates_and_repairs_all_existing_hermes_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            hermes_home = Path(tmpdir) / ".hermes"
            default_root = hermes_home / "skills"
            profile_root = hermes_home / "profiles" / "work" / "skills"
            default_root.mkdir(parents=True)
            profile_root.mkdir(parents=True)

            # Pre-seed stale state install must repair: removed skill packages
            # and a hook script that older manual copies shipped.
            stale_removed = default_root / HERMES_SUBDIR / "arch-loop"
            stale_removed.mkdir(parents=True)
            (stale_removed / "SKILL.md").write_text("stale", encoding="utf-8")
            stale_collision = default_root / HERMES_SUBDIR / "code-review"
            stale_collision.mkdir(parents=True)
            stale_hook_dir = default_root / HERMES_SUBDIR / "arch-step" / "scripts"
            stale_hook_dir.mkdir(parents=True)
            (stale_hook_dir / "arch_controller_stop_hook.py").write_text(
                "stale", encoding="utf-8"
            )

            install = run_make("hermes_install_skill", hermes_home)
            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertIn(f"OK: Hermes skills installed to {default_root}", install.stdout)
            self.assertIn(f"OK: Hermes skills installed to {profile_root}", install.stdout)

            self.assert_root_installed(default_root)
            self.assert_root_installed(profile_root)

            verify = run_make("verify_hermes_install", hermes_home)
            self.assertEqual(verify.returncode, 0, verify.stderr + verify.stdout)
            self.assertIn(
                f"OK: Hermes skills verified at {default_root / HERMES_SUBDIR}",
                verify.stdout,
            )
            self.assertIn(
                f"OK: Hermes skills verified at {profile_root / HERMES_SUBDIR}",
                verify.stdout,
            )

    def test_missing_hermes_home_skips_install_and_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            hermes_home = Path(tmpdir) / "no-such-hermes"

            install = run_make("hermes_install_skill", hermes_home)
            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertIn("SKIP: no Hermes skill roots", install.stdout)
            self.assertFalse(hermes_home.exists())

            verify = run_make("verify_hermes_install", hermes_home)
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertIn("OK: no Hermes skill roots", verify.stdout)

    def test_verify_fails_loudly_on_stale_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            hermes_home = Path(tmpdir) / ".hermes"
            stale = hermes_home / "skills" / HERMES_SUBDIR / "arch-loop"
            stale.mkdir(parents=True)

            verify = run_make("verify_hermes_install", hermes_home)
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("ERROR:", verify.stdout)


if __name__ == "__main__":
    unittest.main()
