# Lilarch Doc Contract

## DOC_PATH

- Reuse an existing `docs/<...>.md` when the user gives one or when repo evidence makes the active compact plan obvious.
- Otherwise create a new compact plan doc under `docs/USERNAME/`.
- Keep one lilarch doc as the SSOT for the change.

## New-doc minimum contract

When creating or repairing a fresh lilarch doc, ensure it has at least:

- YAML frontmatter with:
  - `title`
  - `date`
  - `status`
  - `owners`
  - `reviewers`
  - `fallback_policy`
  - `related`
- a filled `# TL;DR`
- a North Star with:
  - claim
  - in scope
  - out of scope
  - definition of done
- a requirements block
- a plan-audit block

When the change is agent-backed, the requirements or architecture notes must make clear whether the primary lever is prompt/capability work or deterministic code. Do not leave that decision implicit.

## WORKLOG_PATH

- Derive `WORKLOG_PATH` from `DOC_PATH`:
  - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`
- Create it during finish mode if it does not already exist.
- Cross-link the worklog and doc once execution starts.

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

## Status rules

- New or unresolved docs stay `status: draft`.
- Ready-to-build or active work uses `status: active`.
- Set `status: complete` only after finish mode confirms the code and doc agree.

## Fit guard

Escalate away from `lilarch` when:

- the plan wants more than 3 real phases
- the task becomes a broad migration or deep investigation
- the required checkpoints look like full arch work rather than compact feature work
- the doc needs stronger artifact repair than a compact flow should own

Recommended escalation:

- `arch-mini-plan` when the task is still moderate but wants a one-pass canonical plan
- `miniarch-step reformat <DOC_PATH>` when the task outgrew 1-3 phases but still looks like smaller well-defined full-arch work
- `arch-step reformat <DOC_PATH>` when the task is now broader or more ambiguous real full-arch work
- `bugs-flow` when investigation becomes the dominant problem
