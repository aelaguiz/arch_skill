import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_POLICY = REPO_ROOT / "skills/_shared/agent-orchestration-policy.md"


def run_make(target: str, home: Path, overrides: dict[str, Path]):
    env = os.environ.copy()
    env["HOME"] = str(home)
    args = ["make", target]
    args.extend(f"{name}={path}" for name, path in overrides.items())
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


class SharedPolicyInstallTests(unittest.TestCase):
    def test_scoped_copy_preserves_neighbors_and_previous_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "skills"
            policy = destination / "_shared/agent-orchestration-policy.md"
            policy.parent.mkdir(parents=True)
            policy.write_text("local policy\n", encoding="utf-8")
            neighbor = destination / "local-only/SKILL.md"
            neighbor.parent.mkdir()
            neighbor.write_text("keep this package\n", encoding="utf-8")
            sibling = policy.parent / "local-reference.md"
            sibling.write_text("keep this reference\n", encoding="utf-8")

            result = subprocess.run(
                [
                    "make", "agents_install_files",
                    f"AGENTS_SKILLS_DIR={destination}",
                    "FILES=_shared/agent-orchestration-policy.md "
                    "thermo-nuclear-code-quality-review/agents/openai.yaml",
                ],
                cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(policy.read_bytes(), SOURCE_POLICY.read_bytes())
            overlay = "thermo-nuclear-code-quality-review/agents/openai.yaml"
            self.assertEqual(
                (destination / overlay).read_bytes(),
                (REPO_ROOT / "skills" / overlay).read_bytes(),
            )
            self.assertEqual(neighbor.read_text(), "keep this package\n")
            self.assertEqual(sibling.read_text(), "keep this reference\n")
            backups = list(Path(tmpdir).glob(
                "skill-backups/arch_skill.*/_shared/agent-orchestration-policy.md"
            ))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), "local policy\n")

    def test_verify_rejects_stale_policy_for_primary_runtime_roots(self) -> None:
        cases = [
            ("agents_install_skill", "verify_agents_install", "AGENTS_SKILLS_DIR"),
            ("claude_install_skill", "verify_claude_install", "CLAUDE_SKILLS_DIR"),
            ("gemini_install_skill", "verify_gemini_install", "GEMINI_SKILLS_DIR"),
        ]

        for install_target, verify_target, destination_var in cases:
            with (
                self.subTest(destination=destination_var),
                tempfile.TemporaryDirectory() as tmpdir,
            ):
                home = Path(tmpdir)
                overrides = {
                    "AGENTS_SKILLS_DIR": home / ".agents/skills",
                    "CODEX_SKILLS_DIR": home / ".codex/skills",
                    "CODEX_HOOKS_FILE": home / ".codex/hooks.json",
                    "CLAUDE_SKILLS_DIR": home / ".claude/skills",
                    "CLAUDE_SETTINGS_FILE": home / ".claude/settings.json",
                    "GEMINI_SKILLS_DIR": home / ".gemini/skills",
                }

                install = run_make(install_target, home, overrides)
                self.assertEqual(install.returncode, 0, install.stderr)

                policy = (
                    overrides[destination_var]
                    / "_shared/agent-orchestration-policy.md"
                )
                self.assertEqual(policy.read_bytes(), SOURCE_POLICY.read_bytes())

                policy.write_text("stale policy\n", encoding="utf-8")
                verify = run_make(verify_target, home, overrides)

                self.assertNotEqual(verify.returncode, 0)
                self.assertIn(f"ERROR: missing or stale {policy}", verify.stdout)


if __name__ == "__main__":
    unittest.main()
