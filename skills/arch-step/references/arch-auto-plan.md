# `auto-plan` Command Contract

## What this command does

- takes one approved canonical full-arch doc through the planning arc
- runs `research`, `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`
- uses `DOC_PATH` as the only planning ledger
- uses generated stage receipts in `DOC_PATH` to prove each stage command actually ran
- stops after planning is complete and says the doc is ready for `implement-loop`

Native goal mode supplies the repeated turns. This skill does not install or
arm automation hooks. Outside goal mode, run one bounded stage and end with the exact
next command.

## Planning North Star

Running `auto-plan` should end in one of two honest states:

- `ready`:
  - research grounding is present
  - a complete `research` receipt exists
  - deep-dive pass 1 is present
  - a complete `deep-dive-pass-1` receipt exists
  - deep-dive pass 2 is present
  - a complete `deep-dive-pass-2` receipt exists
  - the authoritative phase plan is present
  - a complete `phase-plan` receipt exists
  - the `consistency-pass` helper block is present, says `Decision-complete: yes`, and says `Decision: proceed to implement? yes`
  - a complete `consistency-pass` receipt exists
  - no unresolved decisions remain in the authoritative artifact
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
- `arch-consistency-pass.md`

## Inputs and `DOC_PATH` resolution

- treat the user ask as steering plus any planning preferences
- if the ask includes a `docs/<...>.md` path, use it
- otherwise resolve `DOC_PATH` from the normal `arch-step` defaults
- if the current session just created or most recently updated one canonical full-arch doc, prefer that doc
- if the doc path is truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates

## Writes

- `DOC_PATH`
- `planning_passes`
- `arch_skill:block:auto_plan_receipts` through `skills/arch-step/scripts/arch_stage_gate.py`

## Hard Rules

- docs-only; do not modify code
- this command owns the bounded planning sequence: `research`, `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`
- use the same `DOC_PATH` for every stage
- choose the next stage from `python3 skills/arch-step/scripts/arch_stage_gate.py status --doc <DOC_PATH>`, not from marker presence alone
- each stage command must run `begin` before its doc edits and `complete` after its doc edits; do not hand-edit `arch_skill:block:auto_plan_receipts`
- existing plan content without a matching complete receipt is not auto-plan-ready; rerun the missing stage command so it can mint the receipt honestly
- the second `deep-dive` pass is required even when external research was not run
- rerunning `auto-plan` on a partially complete doc is legal; resume from the first incomplete stage visible in `DOC_PATH`
- in native goal mode, keep advancing through the next incomplete stage until the planning North Star is met or a true blocker stops the run
- outside native goal mode, run one bounded stage and name the exact next command instead of pretending repetition is automatic
- if a stage stops before it updates the required canonical outputs, stop and report that truth plainly
- if any stage uncovers an unresolved decision that repo truth cannot settle, stop and ask the exact blocker question
- if `consistency-pass` leaves `Decision: proceed to implement? no`, stop and report that the doc is not ready for `implement-loop`
- after successful `consistency-pass`, run `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`; say the doc is decision-complete and ready for `implement-loop` only when it exits 0
- do not auto-run `external-research`, helper commands other than the required `consistency-pass`, `implement`, `implement-loop`, or `audit-implementation`

## Stage Receipt Gate

Use the stage gate before continuing. It validates both a complete receipt and the existing stage evidence:

- `research`:
  - `begin`: `python3 skills/arch-step/scripts/arch_stage_gate.py begin --doc <DOC_PATH> --stage research`
  - `complete`: `python3 skills/arch-step/scripts/arch_stage_gate.py complete --doc <DOC_PATH> --stage research`
  - `arch_skill:block:research_grounding` is present
- `deep-dive` pass 1:
  - `begin`: `python3 skills/arch-step/scripts/arch_stage_gate.py begin --doc <DOC_PATH> --stage deep-dive-pass-1`
  - `complete`: `python3 skills/arch-step/scripts/arch_stage_gate.py complete --doc <DOC_PATH> --stage deep-dive-pass-1`
  - `arch_skill:block:current_architecture` is present
  - `arch_skill:block:target_architecture` is present
  - `arch_skill:block:call_site_audit` is present
  - `planning_passes` marks `deep_dive_pass_1: done <YYYY-MM-DD>`
- `deep-dive` pass 2:
  - `begin`: `python3 skills/arch-step/scripts/arch_stage_gate.py begin --doc <DOC_PATH> --stage deep-dive-pass-2`
  - `complete`: `python3 skills/arch-step/scripts/arch_stage_gate.py complete --doc <DOC_PATH> --stage deep-dive-pass-2`
  - the same three architecture blocks are present
  - `planning_passes` marks `deep_dive_pass_2: done <YYYY-MM-DD>`
- `phase-plan`:
  - `begin`: `python3 skills/arch-step/scripts/arch_stage_gate.py begin --doc <DOC_PATH> --stage phase-plan`
  - `complete`: `python3 skills/arch-step/scripts/arch_stage_gate.py complete --doc <DOC_PATH> --stage phase-plan`
  - `arch_skill:block:phase_plan` is present
- `consistency-pass`:
  - `begin`: `python3 skills/arch-step/scripts/arch_stage_gate.py begin --doc <DOC_PATH> --stage consistency-pass`
  - `complete`: `python3 skills/arch-step/scripts/arch_stage_gate.py complete --doc <DOC_PATH> --stage consistency-pass`
  - `arch_skill:block:consistency_pass` is present
  - the helper block says `Decision-complete: yes`
  - the helper block says `Unresolved decisions: none`
  - the helper block says `Decision: proceed to implement? yes`

## Procedure

1. Read `DOC_PATH` fully and run the same alignment checks required by the planning commands it will invoke.
2. Run `python3 skills/arch-step/scripts/arch_stage_gate.py status --doc <DOC_PATH>`.
3. If it prints `READY next=implement-loop`, run `ready` once and stop with the implementation handoff only if exit 0 confirms it.
4. If it prints `NOT_READY next=research`, run one truthful `research` command with its begin/complete receipt.
5. If it prints `NOT_READY next=deep-dive stage=deep-dive-pass-1`, run one truthful `deep-dive` command with the pass 1 begin/complete receipt.
6. If it prints `NOT_READY next=deep-dive stage=deep-dive-pass-2`, run one truthful `deep-dive` command with the pass 2 begin/complete receipt.
7. If it prints `NOT_READY next=phase-plan`, run one truthful `phase-plan` command with its begin/complete receipt.
8. If it prints `NOT_READY next=consistency-pass`, run one truthful `consistency-pass` command with its begin/complete receipt.
9. In native goal mode, keep taking the next gate-reported stage until the planning North Star is met or a true blocker stops the run.
10. Outside native goal mode, stop after one bounded stage and print the next exact command.

## Console Contract

- one-line North Star reminder
- one-line punchline
- ordinary stage output should stay visible
- the final stop message should name `DOC_PATH` and say it is decision-complete and ready for `implement-loop`, or print the exact blocker question that stopped the run
