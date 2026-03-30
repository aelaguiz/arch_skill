# Arch Plan Doc Contract

This file defines the durable plan-doc contract for `arch-plan`.

## DOC_PATH and WORKLOG_PATH

- `DOC_PATH` is the one canonical plan doc under `docs/`.
- Resolve `DOC_PATH` from the user ask, conversation, or repo evidence.
- If it does not exist and the task needs a new plan, create it under `docs/` using:
  - `docs/<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`
  - derive a short 5-9 word title from the ask
- If an existing doc needs canonicalization rather than replacement, reformat it in place or into a new canonical `docs/<...>.md` path without losing content.
- `WORKLOG_PATH` is derived from `DOC_PATH`:
  - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`
- Planning passes update `DOC_PATH` only.
- Implementation and progress work update both `DOC_PATH` and `WORKLOG_PATH`.

## New-doc minimum contract

When creating or repairing a fresh full-arch doc, ensure it has at least:

- YAML frontmatter with:
  - `title`
  - `date`
  - `status`
  - `fallback_policy`
  - `owners`
  - `reviewers`
  - `doc_type`
  - `related`
- A filled `TL;DR`
- A filled North Star section with:
  - claim
  - in scope
  - out of scope
  - definition of done
  - invariants

Do not leave placeholder text in the North Star or TL;DR.
If the doc is new or still `draft`, stop for North Star confirmation before moving deeper into the flow.

## Worklog cross-links

- `DOC_PATH` should reference `WORKLOG_PATH` near the top once execution begins.
- `WORKLOG_PATH` should link back to `DOC_PATH`.
- Do not create a second planning doc or a competing checklist.

## Status rules

- New or unconfirmed docs stay `status: draft` until the North Star is explicitly confirmed.
- Active planning/execution work uses `status: active`.
- Set `status: complete` only when the implementation is code-complete and the doc reflects reality.

## Required block markers

Keep these block markers stable when they exist:

- `arch_skill:block:planning_passes`
- `arch_skill:block:research_grounding`
- `arch_skill:block:external_research`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `arch_skill:block:phase_plan`
- `arch_skill:block:reference_pack`
- `arch_skill:block:plan_enhancer`
- `arch_skill:block:overbuild_protector`
- `arch_skill:block:review_gate`
- `arch_skill:block:gaps_concerns`
- `arch_skill:block:implementation_audit`

If a matching semantic section exists without the block, update it in place rather than duplicating content.

## Planning-pass bookkeeping

Use the planning-pass block as a warn-first record, not a hard gate:

- `deep_dive_pass_1`
- `external_research_grounding`
- `deep_dive_pass_2`

Missing or incomplete passes should produce a warning, not a refusal to continue.

## Write boundaries

- Doc setup, research, external research, deep dive, phase planning, plan shaping, and audits are docs-only.
- Implementation happens only in execution mode.
- Implementation audits do not "fix it while you're here"; they update the plan truth and reopen missing code work.

## Question policy

Only ask the user when the answer is not discoverable from:

- repo code
- tests
- docs
- logs
- existing tools

Typical allowed questions:

- product or UX decisions not encoded anywhere
- external constraints or dates not in repo/docs
- true `DOC_PATH` ambiguity among a small candidate set
- access or permissions blockers
