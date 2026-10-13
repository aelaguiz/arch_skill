import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def make_var_words(variable: str) -> list[str]:
    result = subprocess.run(
        ["make", "-s", "--no-print-directory", "-f", "Makefile", "-f", "-", "print_var"],
        cwd=REPO_ROOT,
        input=f"print_var:\n\t@echo $({variable})\n",
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.split()


def run_make(target: str, agy_home: Path, *extra: str):
    env = os.environ.copy()
    env["HOME"] = str(agy_home.parent)
    return subprocess.run(
        ["make", target, f"AGY_HOME={agy_home}", *extra],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


class AgyInstallTests(unittest.TestCase):
    def test_machine_without_agy_is_skipped_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            agy_home = Path(tmpdir) / ".gemini"

            install = run_make("agy_install_skill", agy_home)
            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertIn("SKIP: no Antigravity CLI home", install.stdout)
            self.assertFalse(agy_home.exists())

            verify = run_make("verify_agy_install", agy_home)
            self.assertEqual(verify.returncode, 0, verify.stderr)

    def test_install_keeps_frontmatter_and_repairs_stale_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            agy_home = Path(tmpdir) / ".gemini"
            (agy_home / "antigravity-cli").mkdir(parents=True)
            skills_dir = agy_home / "config/skills"
            stale_removed = skills_dir / "arch-loop"
            stale_removed.mkdir(parents=True)
            (stale_removed / "SKILL.md").write_text("stale", encoding="utf-8")
            stale_hook = skills_dir / "arch-step/scripts/arch_controller_stop_hook.py"
            stale_hook.parent.mkdir(parents=True)
            stale_hook.write_text("stale", encoding="utf-8")
            neighbor = skills_dir / "someone-elses-skill/SKILL.md"
            neighbor.parent.mkdir(parents=True)
            neighbor.write_text("keep", encoding="utf-8")

            install = run_make("agy_install_skill", agy_home)
            self.assertEqual(install.returncode, 0, install.stderr)

            for skill in make_var_words("GEMINI_SKILLS"):
                skill_md = skills_dir / skill / "SKILL.md"
                self.assertTrue(skill_md.is_file(), skill_md)
                text = read(skill_md)
                self.assertTrue(text.startswith("---\n"), skill_md)
                self.assertRegex(text, re.compile(r"^name: ", re.MULTILINE))
                self.assertRegex(text, re.compile(r"^description: ", re.MULTILINE))
            for skill in make_var_words("NON_GEMINI_SKILLS"):
                self.assertFalse((skills_dir / skill).exists(), skill)
            self.assertFalse(stale_removed.exists())
            self.assertFalse(stale_hook.exists())
            self.assertEqual(read(neighbor), "keep")
            self.assertEqual(
                read(skills_dir / "_shared/agent-orchestration-policy.md"),
                read(REPO_ROOT / "skills/_shared/agent-orchestration-policy.md"),
            )
            leftovers = [
                p
                for p in skills_dir.rglob("*")
                if p.name in {"build", "__pycache__"} or p.suffix == ".pyc"
            ]
            self.assertEqual(leftovers, [], leftovers)

            verify = run_make("verify_agy_install", agy_home)
            self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)

    def test_verify_rejects_skill_without_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            agy_home = Path(tmpdir) / ".gemini"
            (agy_home / "antigravity-cli").mkdir(parents=True)
            install = run_make("agy_install_skill", agy_home)
            self.assertEqual(install.returncode, 0, install.stderr)

            skill_md = agy_home / "config/skills/fresh-consult/SKILL.md"
            skill_md.write_text("# Fresh Consult\n", encoding="utf-8")
            verify = run_make("verify_agy_install", agy_home)
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("lacks the name/description frontmatter", verify.stdout)

    def test_install_runs_agy_target_unless_opted_out(self) -> None:
        noop = [
            "NO_GEMINI=1",
            "NO_HERMES=1",
            "AGENTS_SKILLS_DIR=/tmp/arch-skill-noop-agents",
            "CODEX_SKILLS_DIR=/tmp/arch-skill-noop-codex",
            "CLAUDE_SKILLS_DIR=/tmp/arch-skill-noop-claude",
            "AGY_HOME=/tmp/arch-skill-noop-gemini",
        ]
        for extra, expected in ((noop, True), (noop + ["NO_AGY=1"], False)):
            with self.subTest(no_agy="NO_AGY=1" in extra):
                plan = subprocess.run(
                    ["make", "-n", "install", *extra],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(plan.returncode, 0, plan.stderr)
                self.assertEqual("Antigravity CLI" in plan.stdout, expected)


if __name__ == "__main__":
    unittest.main()
