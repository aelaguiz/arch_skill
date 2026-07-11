# Arch Flow Recommendation Rules

## Full-arch docs

- If the doc does not exist, recommend `arch-step new`.
- If the doc exists but is too non-canonical to trust, recommend `arch-step reformat`.
- If the code audit is clean and the feature still needs docs cleanup or plan/worklog retirement, recommend `arch-docs`.
- Otherwise recommend the exact next move that matches the earliest missing or weak required stage.
- Never recommend implementation while the Scope and Simplicity Contract is
  missing, contradictory, unfrozen, or exceeded. Route a pre-freeze gap to the
  owning planning step; route post-freeze expansion to a human decision.

## Mini full-arch docs

- If the doc does not exist, recommend `miniarch-step new`.
- If the doc exists but is too non-canonical to trust, recommend `miniarch-step reformat`.
- If the code audit is clean and the feature still needs docs cleanup or plan/worklog retirement, recommend `arch-docs`.
- Otherwise recommend the exact next move that matches the earliest missing or weak required stage.
- Apply the same scope-contract readiness rule as full arch.

## Arch-mini-plan docs

- If planning blocks are still incomplete, recommend `arch-mini-plan`.
- If the mini plan and its frozen scope contract are ready for build, recommend `miniarch-step implement`.
- If the code audit is clean and the feature still needs docs cleanup or plan/worklog retirement, recommend `arch-docs`.
- If the mini plan outgrew the faster full-arch tier or is structurally weak, recommend `arch-step reformat`.

## Lilarch docs

- If the work still fits the compact flow, recommend the next lilarch mode.
- If the doc outgrew 1-3 phase fit but still looks smaller and well-defined, recommend `miniarch-step reformat`.
- If the doc outgrew the faster full-arch tier too, recommend `arch-step reformat`.

## Output rule

- Give one recommendation.
- Name the evidence behind it.
- Do not jump into execution unless the user explicitly asks.
