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
- `../../_shared/agent-orchestration-policy.md`
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
- if a planning stage benefits from child planners, use new clean same-host
  native roles when the active host can satisfy the required capabilities;
  child use is optional and must follow the native planning contract below
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

## Native planning child contract

Use child planners only for genuinely independent planning lenses that can be
synthesized into the same `DOC_PATH`. The parent chooses the bounded lenses,
available concurrency, and integration order. Do not add children merely to
make a small stage look more rigorous.

Start every planner as a new clean same-host native child from `DOC_PATH`, its
non-overlapping lens, the relevant references, and the return contract below.
In Codex, set `fork_turns: "none"`. In Claude Code, use a clean named or custom
subagent rather than a conversation fork. Request a read-only capability when
the host exposes one and also say: inspect and propose only; do not edit or
write files, apply patches, commit, or create children. The parent captures
relevant repo state before dispatch, checks it after returns, resolves
disagreements, and alone updates the canonical plan.

Each planner returns whether its bounded lens completed, evidence with path or
section anchors, the proposed planning conclusions or repairs, checks
performed, unresolved assumptions, and confirmation that it made no writes or
children. Keep fanout proportional to independent lenses, host slots,
collision risk, and the parent's capacity to inspect every return. Nested
fanout requires an explicit parent-assigned scope and budget; this planning
contract assigns none.

`gpt-5.4-mini` with `xhigh` reasoning is the preferred miniarch planning
profile only when the active native schema can select and confirm both. If it
cannot, use the inherited native capability and report only what the host can
confirm. When exact model identity is load-bearing, an external exact-model
session is still available, but the dispatch must explain the concrete benefit
that makes its model/profile guarantee worth the added process, integration,
and shared-state cost. Do not externalize a role merely to preserve an
unexplained preference.

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
