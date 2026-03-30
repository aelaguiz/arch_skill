---
name: lilarch
description: "Small-feature 1-3 phase flow: create or repair a compact plan doc, lock requirements and defaults, write a tight implementation plan, implement locally, and self-audit. Use when a request is a contained feature or improvement that can realistically ship in 1-3 phases. Not for broad migrations, one-pass mini plans (`arch-mini-plan`), bug investigations (`bugs-flow`), or open-ended loops."
metadata:
  short-description: "Compact 1-3 phase feature flow"
---

# Lilarch

Use this skill for contained feature work that is too small for the full arch flow but still benefits from a real doc-backed plan.

## When to use

- The change is a small feature or improvement.
- The work should fit in 1-3 phases.
- The user wants the "little arch" workflow rather than the full arch plan.

## When not to use

- The task is a migration, a broad refactor, or clearly larger than 3 phases.
- The user wants a compressed one-pass arch plan instead of a start/plan/finish flow. Use `arch-mini-plan`.
- Investigation dominates because the root cause is unknown. Use `bugs-flow` or `north-star-investigation`.

## Non-negotiables

- Keep one compact `DOC_PATH` as the SSOT for the change.
- `lilarch-start` and `lilarch-plan` behavior is docs-only. Code changes only happen in finish mode.
- Ask the small set of clarifying questions that must be answered before planning. Do not bulldoze past unresolved requirements.
- Keep the plan to 1-3 phases. If it grows beyond that, escalate instead of pretending the fit is still good.
- Implementation stays local. Do not launch external review unless the user explicitly asks for review.
- No runtime fallbacks or compatibility shims unless explicitly approved in the doc.

## First move

1. Read `references/doc-contract.md`.
2. Resolve whether you are in:
   - start mode
   - plan mode
   - finish mode
3. Resolve `DOC_PATH` and read it fully if it exists.
4. Check that the work still fits `lilarch`.

## Workflow

### 1) Start mode

- Create or repair the compact plan doc.
- Draft the North Star, requirements, non-requirements, defaults, and the small list of clarifying questions.
- Stop for answers if those questions are required to plan safely.

### 2) Plan mode

- Update the minimal research grounding.
- Write the current architecture, target architecture, call-site audit, and a 1-3 phase plan.
- Run the internal lilarch plan audit and tighten the doc before implementation.

### 3) Finish mode

- Implement locally against the doc.
- Keep a lightweight `WORKLOG_PATH`.
- Self-audit for completeness and mark the doc complete only when the code is actually complete.

## Output expectations

- Update `DOC_PATH` in every mode.
- Update `WORKLOG_PATH` during finish mode.
- Keep the console summary short and practical:
  - North Star reminder
  - punchline
  - what changed
  - blockers or remaining questions
  - next action

## Reference map

- `references/doc-contract.md` - lilarch doc, blocks, worklog, and escalation rules
