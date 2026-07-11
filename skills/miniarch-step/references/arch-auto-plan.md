# `auto-plan` Command Contract

## What this command does

- takes one approved canonical mini full-arch doc through the planning arc
- runs `research`, `deep-dive`, and `phase-plan`
- uses `DOC_PATH` as the only planning ledger
- stops after `phase-plan` is complete and says the doc is ready for `implement-loop`

Native goal mode supplies the repeated turns. This skill does not install or
arm automation hooks. Outside goal mode, run one bounded stage and end with the
exact next command.

## Planning North Star

Running `auto-plan` should end in one of two honest states:

- `ready`:
  - research grounding is present
  - one deep-dive pass is present
  - the authoritative phase plan is present
  - no unresolved decisions remain in the authoritative artifact
  - the Scope and Simplicity Contract has human anchors, an initial closure or
    explicit `none`, a freeze boundary, and every phase item serves that frozen
    contract or enough proof
  - no implementation has started
  - the final message says the doc is decision-complete and ready for `implement-loop`
- `blocked`:
  - the blocker or early stop is explicit
  - the run stops instead of silently pretending the planning arc finished

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
- otherwise resolve `DOC_PATH` from the normal `miniarch-step` defaults
- if the current session just created or most recently updated one canonical full-arch doc, prefer that doc
- if the doc path is truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates

## Writes

- `DOC_PATH`
- `planning_passes`

## Hard Rules

- docs-only; do not modify code
- this command owns the bounded planning sequence: `research`, `deep-dive`, and `phase-plan`
- if a planning stage explicitly uses parallel agents, spawn those agents with model `gpt-5.4-mini` and reasoning effort `xhigh`
- use the same `DOC_PATH` for every stage
- rerunning `auto-plan` on a partially complete doc is legal; resume from the first incomplete stage visible in `DOC_PATH`
- in native goal mode, keep advancing through the next incomplete stage until the planning North Star is met or a true blocker stops the run
- outside native goal mode, run one bounded stage and name the exact next command instead of pretending repetition is automatic
- if a stage stops before it updates the required canonical outputs, stop and report that truth plainly
- if any stage uncovers an unresolved decision that repo truth cannot settle, stop and ask the exact blocker question
- after successful `phase-plan`, say the doc is decision-complete and ready for `implement-loop`
- do not emit the implementation handoff when the Scope and Simplicity Contract
  is missing, vague, unfrozen, contradicted by Section 7, or exceeded by planned
  machinery or adjacent work

## Stage Completion Signals

Use these signals before continuing:

- `research`:
  - `arch_skill:block:research_grounding` is present
- `deep-dive`:
  - `arch_skill:block:current_architecture` is present
  - `arch_skill:block:target_architecture` is present
  - `arch_skill:block:call_site_audit` is present
  - `planning_passes` marks `deep_dive_pass_1: done <YYYY-MM-DD>`
- `phase-plan`:
  - `arch_skill:block:phase_plan` is present
  - the plan has no unresolved architecture-shaping decisions
  - Section 7 phases have exhaustive checklists and exit criteria for the approved scope
  - Section 7 contains no item outside the frozen Scope and Simplicity Contract

## Procedure

1. Read `DOC_PATH` fully and run the same alignment checks required by the planning commands it will invoke.
2. Use `DOC_PATH` as the planning ledger.
3. If the doc has no planning progress yet, run one truthful `research` pass.
4. If the doc already has partial progress, do not rerun completed stages; continue from the first incomplete stage.
5. If the first incomplete stage is `deep-dive`, run `deep-dive`.
6. If the first incomplete stage is `phase-plan`, run `phase-plan`.
7. In native goal mode, keep taking the next incomplete stage until the planning North Star is met or a true blocker stops the run.
8. Outside native goal mode, stop after one bounded stage and print the next exact command.

## Console Contract

- one-line North Star reminder
- one-line punchline
- ordinary stage output should stay visible
- the final stop message should name `DOC_PATH` and say it is decision-complete and ready for `implement-loop`, or print the exact blocker question that stopped the run
