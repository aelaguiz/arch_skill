import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_repo_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class ArchDocsPromptContractTests(unittest.TestCase):
    def assert_matches(self, text: str, pattern: str) -> None:
        self.assertRegex(text, re.compile(pattern, re.IGNORECASE | re.DOTALL))

    def test_skill_and_agent_prompt_use_delete_first_30_day_contract(self) -> None:
        skill_text = read_repo_text("skills/arch-docs/SKILL.md")
        agent_text = read_repo_text("skills/arch-docs/agents/openai.yaml")

        self.assert_matches(skill_text, r"older than 30 days.*presumed stale")
        self.assert_matches(skill_text, r"Do not trust what a doc calls itself")
        self.assert_matches(agent_text, r"docs older than 30 days are presumed stale")
        self.assert_matches(agent_text, r"Do not trust .*docs/living.*Status: LIVING.*Last verified")

    def test_cleanup_rules_reject_doc_labels_and_metadata_only_freshness(self) -> None:
        cleanup_text = read_repo_text("skills/arch-docs/references/cleanup-rules.md")

        self.assert_matches(cleanup_text, r"docs/living.*Status: LIVING.*Last verified")
        self.assert_matches(cleanup_text, r"claims to verify")
        self.assert_matches(cleanup_text, r"Metadata-only freshness edits are a docs-cleanup failure")
        self.assert_matches(cleanup_text, r"older than 30 days are presumed stale")

    def test_pass_contract_prefers_fold_forward_over_wrapper_survival(self) -> None:
        pass_text = read_repo_text("skills/arch-docs/references/pass.md")

        self.assert_matches(pass_text, r"Survival Justifications")
        self.assert_matches(pass_text, r"older than 30 days.*survives.*code-grounded current-reader need")
        self.assert_matches(pass_text, r"fold.*best existing evergreen home.*delete the wrapper")
        self.assert_matches(pass_text, r"no doc was made to look current through metadata-only freshness edits")

    def test_canonical_home_judgment_blocks_worklog_to_top_level_promotion(self) -> None:
        canonical_text = read_repo_text("skills/arch-docs/references/canonical-home-judgment.md")

        self.assert_matches(canonical_text, r"readers are likely to seek it out directly")
        self.assert_matches(canonical_text, r"not merely residue from an implementation pass")
        self.assert_matches(canonical_text, r"does not earn a top-level evergreen doc")

    def test_internal_evaluator_and_usage_guide_match_runtime_contract(self) -> None:
        evaluator_text = read_repo_text("skills/arch-docs/references/internal-evaluator.md")
        usage_text = read_repo_text("docs/arch_skill_usage_guide.md")

        self.assert_matches(evaluator_text, r"older than 30 days.*explicit code-grounded current-reader value")
        self.assert_matches(evaluator_text, r"metadata-only freshness edits")
        self.assert_matches(usage_text, r"point-in-time docs older than 30 days as presumptively stale")
        self.assert_matches(usage_text, r"Do not trust .*docs/living.*Status: LIVING.*Last verified")


if __name__ == "__main__":
    unittest.main()
