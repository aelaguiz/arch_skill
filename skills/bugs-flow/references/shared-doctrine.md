# Bugs Flow Shared Doctrine

## Core rules

- Keep one bug doc as the source of truth.
- Investigate before editing code.
- Use first-party evidence before theory.
- Keep fixes minimal and localized.
- Apply `skills/_shared/scope-and-convergence.md`. Analyze may define the
  smallest evidenced same-contract closure before fix; fix and review cannot
  add to it after freeze.
- Default to fail-loud behavior. Do not add hidden fallbacks, silent swallowing, or "try the old path too" logic.
- "Systemic" means fix the shared cause at its narrowest owner, not open a
  repo-wide cleanup project.

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
