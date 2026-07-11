# Bugs Flow Shared Doctrine

## Core rules

- Keep one bug doc as the source of truth.
- Investigate before editing code.
- Use first-party evidence before theory.
- Keep fixes minimal and localized.
- Apply `../../_shared/scope-and-convergence.md`. Analyze may define the
  smallest evidenced same-contract closure before fix; fix and review cannot
  add to it after freeze.
- Default to fail-loud behavior. Do not add hidden fallbacks, silent swallowing, or "try the old path too" logic.
- "Systemic" means fix the shared cause at its narrowest owner, not open a
  repo-wide cleanup project.
- When an implementer child is used, start it clean from the bug doc and
  preserve its exact handle for accepted repairs. Every independent review or
  recheck uses a different new clean critic.
- Critics are read-only by the strongest available capability plus explicit
  no-edit/no-write guidance. The parent checks current repository state,
  accounts for every return, owns scope and synthesis, and decides the final
  verdict.
- Children do not create children or invoke delegation, consult, or review
  skills unless the parent explicitly assigned a bounded nested scope and
  budget.

## What counts as first-party evidence

- Sentry issue details and representative events
- logs and traces
- QA repro steps
- repo searches and code anchors
- targeted checks or minimal repros

## What good bug discipline looks like

- Strong:
  - symptoms and impact are concrete
  - likely cause is grounded in actual evidence
  - fix scope is narrow
  - verification matches the failure mode
- Weak:
  - speculative root cause with no anchors
  - broad refactor as a bug fix
  - "return empty value if parsing fails"
  - "if new path fails, fall back to old path"
