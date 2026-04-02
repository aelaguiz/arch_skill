# Lilarch Quality Bar

## Requirements block

- Strong:
  - concrete user-visible behavior
  - defaults are explicit
  - non-requirements cut off easy overbuild
- Weak:
  - generic wish list
  - no defaults
  - implied product decisions left unresolved

## Architecture blocks

- Strong:
  - name the real files or modules
  - explain ownership before and after
  - capture the call-site blast radius
- Weak:
  - vague "update UI and backend"
  - no call-site view

## Plan audit

- Strong:
  - says why the plan is safe to implement
  - calls out remaining risk directly
  - catches scope creep before finish mode
- Weak:
  - rubber-stamp approval
  - just repeats the phase plan

## Finish-mode audit

- Strong:
  - checks code reality against the compact doc
  - names missing work if any
- Weak:
  - "looks good"
  - equates partial verification with completion
