# Lilarch Shared Doctrine

## Core rules

- One compact doc is the planning source of truth.
- Code is ground truth. Anchor claims in files, symbols, tests, logs, or explicit UX docs.
- Start and plan modes are docs-only.
- Finish mode implements locally and keeps the worklog honest.
- Ask only the clarifying questions that block safe planning.
- Default to hard cutover and explicit deletes. Do not hide risk behind runtime shims.

## Small-feature discipline

- Lilarch is for contained feature work, not miniature architecture theater.
- Keep the doc short enough that an implementer can hold the whole plan in working memory.
- Requirements should resolve decisions, not restate the user prompt.
- Plan audits are quality gates, not second plans.

## What strong lilarch looks like

- Strong:
  - 1-3 phases
  - a short but concrete requirements block
  - current and target architecture with direct call-site impact
  - explicit defaults and explicit non-requirements
  - finish mode that either ships or escalates cleanly
- Weak:
  - pseudo-full-arch doc hiding inside lilarch
  - open product questions left in the phase plan
  - "cleanup later" everywhere with no ownership
