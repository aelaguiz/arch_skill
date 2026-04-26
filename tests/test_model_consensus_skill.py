import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "model-consensus"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def squash(text: str) -> str:
    return " ".join(text.split())


class ModelConsensusSkillTests(unittest.TestCase):
    def test_skill_package_is_prompt_only_and_has_required_references(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").is_file())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").is_file())
        self.assertFalse(
            (SKILL_DIR / "scripts").exists(),
            "model-consensus must stay prompt-only; do not add a scripts runner",
        )

        for relpath in [
            "references/workflow-contract.md",
            "references/prompt-contracts.md",
            "references/model-and-invocation.md",
            "references/repo-grounding.md",
            "references/convergence-and-synthesis.md",
            "references/examples.md",
        ]:
            self.assertTrue((SKILL_DIR / relpath).is_file(), relpath)

    def test_skill_contract_names_parent_agent_runner_and_rejects_harnesses(self):
        body = read(SKILL_DIR / "SKILL.md")
        compact_body = squash(body)
        description = re.search(r'^description: "(.*)"$', body, re.MULTILINE)

        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1)), 1024)
        self.assertIn("The parent agent is the runner", body)
        self.assertIn(
            "Do not add or depend on a deterministic runner",
            compact_body,
        )
        self.assertIn(
            "script, controller, state machine, or harness",
            compact_body,
        )
        self.assertIn("Prompt the models as collaborators", body)
        self.assertIn("Agreement is not accumulation", body)

    def test_prompt_contract_teaches_goals_instead_of_prompt_runner_behavior(self):
        prompt_contracts = read(SKILL_DIR / "references" / "prompt-contracts.md")

        for required in [
            "Mission",
            "System Context",
            "Authoritative Inputs",
            "Repo Grounding",
            "Quality Bar",
            "Output Contract",
            "Stop Instead Of Continuing If",
            "You are not a prompt runner",
            "Adversarial Role",
        ]:
            self.assertIn(required, prompt_contracts)

    def test_invocation_contract_reuses_shared_model_resolution_and_streaming(self):
        invocation = read(SKILL_DIR / "references" / "model-and-invocation.md")

        for required in [
            "skills/_shared/model_resolution.py",
            "codex debug models",
            "Preserve family and numeric version exactly",
            "--disable codex_hooks",
            "codex exec resume",
            "--output-format stream-json",
            "--include-partial-messages",
            "--include-hook-events",
            "--settings '{\"disableAllHooks\":true}'",
            "-r <session_id>",
            "Do not pass `--ephemeral`",
        ]:
            self.assertIn(required, invocation)

    def test_repo_grounding_requires_code_reads_and_single_path_convergence(self):
        repo_grounding = read(SKILL_DIR / "references" / "repo-grounding.md")
        compact_repo_grounding = squash(repo_grounding)

        for required in [
            "consensus is invalid until both child models have read the code",
            "canonical owner paths",
            "patterns to adopt",
            "parallel paths or drift risks",
            "tests or proof surfaces",
            "behavior-preservation constraints",
            "Single-Path Pressure",
            "If you propose a new path",
        ]:
            self.assertIn(required, compact_repo_grounding)

    def test_convergence_contract_rejects_kitchen_sink_synthesis(self):
        convergence = read(
            SKILL_DIR / "references" / "convergence-and-synthesis.md"
        )
        compact_convergence = squash(convergence)

        self.assertIn("Anti-Kitchen-Sink Rule", convergence)
        self.assertIn("not automatically A+B+C", convergence)
        self.assertIn("the same small answer", convergence)
        self.assertIn("no consensus", convergence)
        self.assertIn(
            "add a new architecture that neither model reviewed",
            compact_convergence,
        )

    def test_docs_and_install_surfaces_include_model_consensus(self):
        readme = read(REPO_ROOT / "README.md")
        usage = read(REPO_ROOT / "docs" / "arch_skill_usage_guide.md")
        agents = read(REPO_ROOT / "AGENTS.md")
        makefile = read(REPO_ROOT / "Makefile")

        self.assertIn("`model-consensus`", readme)
        self.assertIn("~/.agents/skills/model-consensus/", readme)
        self.assertIn("~/.claude/skills/model-consensus/", readme)
        self.assertIn("~/.gemini/skills/model-consensus/", readme)
        self.assertIn("### `model-consensus`", usage)
        self.assertIn("Use `$model-consensus`", agents)

        for variable in ["SKILLS", "CLAUDE_SKILLS", "GEMINI_SKILLS"]:
            line = re.search(rf"^{variable} := (.*)$", makefile, re.MULTILINE)
            self.assertIsNotNone(line, variable)
            self.assertIn("model-consensus", line.group(1).split())


if __name__ == "__main__":
    unittest.main()
