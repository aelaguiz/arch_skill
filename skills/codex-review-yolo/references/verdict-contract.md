# Verdict Contract

Codex output is long prose by default. The verdict block at the end of the review prompt exists so the final decision is findable and consistent. Always require exactly this shape.

## Required footer

```
VERDICT: approve | not-approved | inconclusive
REQUIRED REPAIRS: <bullets or "none">
OBSERVATIONS: <bullets or "none">
ASSESSMENT: <one paragraph>
```

## Field semantics

- **VERDICT** — one of three literal strings.
  - `approve` — the artifact meets the requested review bar with no required
    repairs for the requested decision.
  - `not-approved` — at least one required repair, missing required proof, or
    unresolved decision affects approval for the requested decision.
  - `inconclusive` — Codex could not inspect the necessary artifact or scope.
- **REQUIRED REPAIRS** — issues that prevent approval for this review objective.
  For file-based reviews, each bullet names the file + line + the specific fix.
  For plan or completion audits, each bullet names the unmet outcome, section,
  or acceptance item. If this field is not `none`, the verdict must be
  `not-approved`.
- **OBSERVATIONS** — informational facts, genuinely out-of-scope follow-ups, or
  risks the controlling request explicitly excludes from the approval decision.
  Observations must not hide duplicate truth, side doors, stale docs/prompts,
  weak proof, or any repair required before approval.
- **ASSESSMENT** — codex's direct assessment of whether the artifact meets the
  requested review goal, based on the evidence it inspected.

## Parsing

Don't write a formal parser. Read the file, find the `VERDICT:` line, skim the
three sections underneath. That's all. The footer is for human (or
LLM-acting-as-human) consumption, not a machine interface.

## Relaying to the user

When reporting back:

1. Lead with the VERDICT, verbatim.
2. Quote the REQUIRED REPAIRS bullets — do not paraphrase. Paraphrasing loses nuance.
3. Summarize OBSERVATIONS if there are many; list verbatim if there are few.
4. Always include the ASSESSMENT line.
5. Note the full final-output file path so the user can read the long-form reasoning.

## When codex doesn't produce the block

If the verdict block is missing or malformed:

- **First try:** re-invoke with a prompt that calls out the failure — "Your last
  response did not include the required VERDICT footer. Produce ONLY the verdict
  block for the work described in <path to prior prompt>."
- **Don't** hand-write a verdict on codex's behalf. Report to the user that codex didn't follow the contract and ask whether to re-run.

## Overriding codex

Codex is a second opinion, not the final word. If its blocking finding is wrong (you read the file and codex is mistaken), say so explicitly: "codex flagged X as blocking, but the file actually does Y — codex was wrong here." Don't silently ignore it. Transparency about disagreement is the whole point of getting a second opinion.
