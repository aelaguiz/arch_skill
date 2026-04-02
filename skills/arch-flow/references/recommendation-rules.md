# Arch Flow Recommendation Rules

## Full-arch docs

- If the doc does not exist, recommend `arch-step new`.
- If the doc exists but is too non-canonical to trust, recommend `arch-step reformat`.
- Otherwise recommend the exact next `arch-step` move that matches the earliest missing or weak required stage.

## Arch-mini-plan docs

- If planning blocks are still incomplete, recommend `arch-mini-plan`.
- If the mini plan is ready for build, recommend `arch-step implement`.
- If the mini plan outgrew mini mode or is structurally weak, recommend `arch-step reformat`.

## Lilarch docs

- If the work still fits the compact flow, recommend the next lilarch mode.
- If the doc outgrew 1-3 phase fit, recommend `arch-step reformat`.

## Output rule

- Give one recommendation.
- Name the evidence behind it.
- Do not jump into execution unless the user explicitly asks.
