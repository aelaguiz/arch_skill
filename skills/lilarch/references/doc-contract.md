# Lilarch Doc Contract

## DOC_PATH

- Reuse an existing `docs/<...>.md` when the user gives one.
- Otherwise create a new compact plan doc under `docs/USERNAME/`.
- Keep one lilarch doc as the SSOT for the change.

## WORKLOG_PATH

- Derive `WORKLOG_PATH` from `DOC_PATH`:
  - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`
- Create it during finish mode if it does not already exist.

## Required blocks

Lilarch-specific:

- `lilarch:block:requirements`
- `lilarch:block:plan_audit`

Compatible arch blocks:

- `arch_skill:block:research_grounding`
- `arch_skill:block:external_research` when needed
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `arch_skill:block:phase_plan`
- `arch_skill:block:implementation_audit`

## Fit guard

Escalate away from `lilarch` when:

- the plan wants more than 3 phases
- the task becomes a broad migration or deep investigation
- the required checkpoints look like full arch work rather than compact feature work

Recommended escalation:

- `arch-mini-plan` when the task is still moderate but wants a one-pass canonical plan
- `arch-plan` when the task is now a real multi-step arch effort
- `bugs-flow` when investigation becomes the dominant problem
