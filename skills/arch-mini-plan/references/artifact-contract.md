# Arch Mini Plan Artifact Contract

## DOC_PATH

- Reuse an existing `docs/<...>.md` when the user gives one or when repo evidence makes the active plan obvious.
- Otherwise create a new canonical plan doc under `docs/`:
  - `docs/<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`
- Keep one doc as the planning SSOT. Do not create a second checklist or mini-plan sidecar.

## New-doc minimum contract

When creating or repairing a mini-plan doc, ensure it has at least:

- YAML frontmatter with:
  - `title`
  - `date`
  - `status`
  - `fallback_policy`
  - `owners`
  - `reviewers`
  - `doc_type`
  - `related`
- a filled `# TL;DR`
- a filled North Star with:
  - claim
  - in scope
  - out of scope
  - definition of done
  - invariants

Do not leave placeholder text in the TL;DR or North Star.

## Required planning blocks

Mini mode must write or repair these blocks in `DOC_PATH`:

- `arch_skill:block:planning_passes`
- `arch_skill:block:research_grounding`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `arch_skill:block:phase_plan`

Optional only when the task truly needs them:

- `arch_skill:block:external_research`
- `arch_skill:block:reference_pack`

Use the same marker shapes that `arch-step` expects so follow-through can continue without migration work.

When the change is agent-backed, these blocks must make capability-first decisions visible enough that `arch-step` can continue without inventing whether prompting, grounding, native capability use, or custom tooling should own the behavior.

## Status rules

- New or unconfirmed docs stay `status: draft`.
- Planning-complete docs move to `status: active`.
- Do not set `status: complete` in mini-plan mode. Implementation belongs to `arch-step`.

## Handoff contract

- The default follow-through is `arch-step implement <DOC_PATH>` when the doc is strong enough to ship against.
- After clean full-arch code audit, the expected docs-cleanup handoff is `arch-docs`.
- If the doc is structurally weak or the work outgrew mini mode, the handoff is `arch-step reformat <DOC_PATH>`.
- Mini mode does not create `WORKLOG_PATH`; execution creates it later.
