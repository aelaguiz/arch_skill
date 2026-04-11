# `auto-plan` Command Contract

## What this command does

- take one approved canonical full-arch doc through the planning arc automatically
- run `research`, then `deep-dive`, then `deep-dive` again, then `phase-plan`
- use the installed Codex runtime continuation support to move stage to stage
- stop after planning is complete and hand off cleanly to `implement-loop`
- keep `DOC_PATH` and loop state aligned while the controller is armed

## Planning North Star

Running `auto-plan` should end in one of two honest states:

- `ready`:
  - research grounding is present
  - deep-dive pass 1 is present
  - deep-dive pass 2 is present
  - the authoritative phase plan is present
  - no implementation has started
  - the final message says the doc is ready for `implement-loop`
- `blocked`:
  - the controller state is cleared
  - the blocker or early stop is explicit
  - the run stops instead of silently pretending the planning arc finished

User-facing invocation is just `auto-plan`. If the installed runtime support for real automatic sequencing is absent or disabled, this command must fail loud instead of pretending prompt-only chaining is the same feature.

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Section 3, Section 4, Section 5, Section 6, Section 7, and `planning_passes`
- `arch-research.md`
- `arch-deep-dive.md`
- `arch-phase-plan.md`

## Inputs and `DOC_PATH` resolution

- treat the user ask as steering plus any planning preferences
- if the ask includes a `docs/<...>.md` path, use it
- otherwise resolve `DOC_PATH` from the normal `arch-step` defaults
- if the current session just created or most recently updated one canonical full-arch doc, prefer that doc
- if the doc path is truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates

## Writes

- `DOC_PATH`
- `planning_passes`
- `.codex/auto-plan-state.<SESSION_ID>.json`

## Required runtime preflight

Before arming the controller, verify all of these:

- Codex runtime is the active host
- the installed Codex runtime support for this repo's automatic controller surface is present
- the installed `arch-step` runner exists under `~/.agents/skills/arch-step/`
- `codex features list` shows `codex_hooks` enabled
- the target doc exists and frontmatter `status` is `active` or `complete`

If any check fails, name the broken prerequisite and stop.

Do not downgrade to prompt-only same-session chaining.

## Active planning-state contract

Resolve `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/auto-plan-state.<SESSION_ID>.json` before the first research pass.

Minimal shape:

```json
{
  "version": 1,
  "command": "auto-plan",
  "session_id": "<SESSION_ID>",
  "doc_path": "docs/<PLAN>.md",
  "stage_index": 0,
  "stages": ["research", "deep-dive-pass-1", "deep-dive-pass-2", "phase-plan"]
}
```

Lifecycle:

- create or refresh it after preflight and before the research pass
- write the current `session_id` into the state file at arm time
- leave it armed while automatic planning is active
- advance `stage_index` only after the required canonical outputs for that stage were updated
- delete it when phase-plan finishes
- delete it before stopping on a blocker, ambiguity, or other early stop so the controller does not re-enter falsely

## Hard rules

- docs-only; do not modify code
- this command is a bounded controller over `research`, `deep-dive`, `deep-dive`, and `phase-plan`; do not invent a second planning surface
- `auto-plan` is one command; if the required runtime continuation support is absent or disabled, fail loud
- use the same `DOC_PATH` for every stage in the controller
- the second `deep-dive` pass is required for this controller even when external research was not run
- in Codex, the installed runtime continuation path owns stage-to-stage continuation
- planning stages stay in the same visible session; do not hide them in silent child planning runs
- if a stage stops before it updates the required canonical outputs, clear `.codex/auto-plan-state.<SESSION_ID>.json`, stop, and report that truth plainly
- after `phase-plan`, clear `.codex/auto-plan-state.<SESSION_ID>.json`, stop, and say the doc is ready for `implement-loop`
- do not auto-run `external-research`, helper commands, `implement`, `implement-loop`, or `audit-implementation`

## Stage completion signals

Use these signals before continuing automatically:

- `research`:
  - `arch_skill:block:research_grounding` is present and was updated in this stage
- `deep-dive` pass 1:
  - `arch_skill:block:current_architecture` is present
  - `arch_skill:block:target_architecture` is present
  - `arch_skill:block:call_site_audit` is present
  - `planning_passes` marks `deep_dive_pass_1: done <YYYY-MM-DD>`
- `deep-dive` pass 2:
  - the same three architecture blocks are present
  - `planning_passes` marks `deep_dive_pass_2: done <YYYY-MM-DD>`
- `phase-plan`:
  - `arch_skill:block:phase_plan` is present and was updated in this stage

## Controller procedure

1. Read `DOC_PATH` fully and run the same alignment checks required by the planning commands it will invoke.
2. Run the runtime preflight. If the installed continuation path or `codex_hooks` is unavailable, fail loud.
3. Resolve `SESSION_ID` from `CODEX_THREAD_ID`, then create or refresh `.codex/auto-plan-state.<SESSION_ID>.json` for the current Codex session and `DOC_PATH`.
4. Run one truthful `research` pass using the `research` contract.
5. Let Codex try to stop. The installed runtime should:
   - no-op when no active auto-plan state matches the current session
   - after `research`, continue to `deep-dive` pass 1
   - after `deep-dive` pass 1, continue to `deep-dive` pass 2
   - after `deep-dive` pass 2, continue to `phase-plan`
   - after `phase-plan`, clear state and stop with the `implement-loop` handoff message
6. On each hook-driven continuation, run the literal next planning command against the same `DOC_PATH`, keep the controller state aligned, and stop naturally after the stage finishes.
7. If a stage ends early, does not update the required canonical outputs, or the next move is no longer credible, clear `.codex/auto-plan-state.<SESSION_ID>.json`, stop, and report that state plainly.

## Console contract

- one-line North Star reminder
- one-line punchline
- ordinary stage output should stay visible because the planning commands run in the same session
- the final stop message should name `DOC_PATH` and say it is ready for `implement-loop`
