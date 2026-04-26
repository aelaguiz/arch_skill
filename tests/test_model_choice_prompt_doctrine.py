import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

MODEL_CHOICE_DOCS = [
    "skills/arch-epic/references/model-and-effort.md",
    "skills/stepwise/references/model-and-effort.md",
    "skills/fresh-consult/references/model-and-invocation.md",
    "skills/model-consensus/references/model-and-invocation.md",
]

CLARIFICATION_LINE = (
    "If the user says `gpt 5.4` or a `gpt-5.4` variant while choosing a model,"
)


def read(relpath: str) -> str:
    return (REPO_ROOT / relpath).read_text(encoding="utf-8")


class ModelChoicePromptDoctrineTests(unittest.TestCase):
    def test_gpt_54_is_taught_as_prompt_clarification_not_alias_rule(self):
        for relpath in MODEL_CHOICE_DOCS:
            with self.subTest(relpath=relpath):
                body = read(relpath)

                self.assertIn(CLARIFICATION_LINE, body)
                self.assertIn("whether they meant `gpt-5.5`", body)
                self.assertIn("explicitly\n  want `gpt-5.4`", body)
                self.assertIn("not an alias rule", body)
                self.assertIn("do not rewrite\n  the version yourself", body)

    def test_user_choice_examples_do_not_present_gpt_54_as_ordinary_choice(self):
        checked_docs = [
            "skills/arch-epic/references/examples.md",
            "skills/model-consensus/references/examples.md",
            "docs/arch_skill_usage_guide.md",
        ]
        stale_examples = [
            "Codex gpt-5.4",
            "Codex gpt 5.4",
            "gpt 5.4 mini high",
            "gpt 5.4 mini xhigh",
        ]

        for relpath in checked_docs:
            with self.subTest(relpath=relpath):
                body = read(relpath)
                for stale in stale_examples:
                    self.assertNotIn(stale, body)
