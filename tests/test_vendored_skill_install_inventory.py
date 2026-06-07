import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "thermo-nuclear-code-quality-review"
REMOVED_SKILL_NAME = "code-review"
VENDOR_ROOT = REPO_ROOT / "vendor/cursor/plugins/cursor-team-kit"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def compact(text: str) -> str:
    return " ".join(text.split())


def make_var_words(makefile: str, variable: str) -> list[str]:
    match = re.search(rf"^{variable} := (.*)$", makefile, re.MULTILINE)
    assert match is not None, variable
    return match.group(1).split()


class VendoredSkillInstallInventoryTests(unittest.TestCase):
    def test_vendored_cursor_team_kit_package_is_present_with_provenance(self) -> None:
        skill_path = VENDOR_ROOT / f"skills/{SKILL_NAME}/SKILL.md"
        manifest_path = VENDOR_ROOT / ".cursor-plugin/plugin.json"
        license_path = VENDOR_ROOT / "LICENSE"

        self.assertTrue(skill_path.is_file())
        self.assertTrue(manifest_path.is_file())
        self.assertTrue(license_path.is_file())

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "cursor-team-kit")
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertIn(SKILL_NAME, read(VENDOR_ROOT / "README.md"))
        self.assertIn(f"name: {SKILL_NAME}", read(skill_path))

    def test_makefile_installs_vendored_skill_on_all_skill_surfaces(self) -> None:
        makefile = read(REPO_ROOT / "Makefile")

        for variable in ["SKILLS", "CLAUDE_SKILLS", "GEMINI_SKILLS"]:
            self.assertIn(SKILL_NAME, make_var_words(makefile, variable))

        self.assertIn(
            "CURSOR_TEAM_KIT_SKILLS_DIR := vendor/cursor/plugins/cursor-team-kit/skills",
            makefile,
        )
        self.assertIn(f"VENDORED_CURSOR_TEAM_KIT_SKILLS := {SKILL_NAME}", makefile)
        self.assertIn("cp -R $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill", makefile)
        self.assertIn("scp -r $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill", makefile)

    def test_docs_and_routing_name_vendored_installed_skill(self) -> None:
        readme = read(REPO_ROOT / "README.md")
        usage = read(REPO_ROOT / "docs/arch_skill_usage_guide.md")
        agents = read(REPO_ROOT / "AGENTS.md")

        for doc in [readme, usage]:
            self.assertIn(f"`{SKILL_NAME}`", doc)
            self.assertIn(f"~/.agents/skills/{SKILL_NAME}/", doc)
            self.assertIn(f"~/.claude/skills/{SKILL_NAME}/", doc)
            self.assertIn(f"~/.gemini/skills/{SKILL_NAME}/", doc)
            self.assertIn("vendor/cursor/plugins/cursor-team-kit/skills/", doc)

        self.assertIn(f"Use `${SKILL_NAME}`", agents)

    def test_removed_code_review_skill_is_purged_from_install_inventory(self) -> None:
        makefile = read(REPO_ROOT / "Makefile")

        self.assertIn(REMOVED_SKILL_NAME, make_var_words(makefile, "REMOVED_SKILLS"))
        for variable in ["SKILLS", "CLAUDE_SKILLS", "GEMINI_SKILLS"]:
            self.assertNotIn(REMOVED_SKILL_NAME, make_var_words(makefile, variable))

        self.assertFalse((REPO_ROOT / f"skills/{REMOVED_SKILL_NAME}").exists())


if __name__ == "__main__":
    unittest.main()
