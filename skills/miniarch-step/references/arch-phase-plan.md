# `phase-plan` Command Contract

## What this command does

- write or sharpen the authoritative phased implementation plan
- convert architecture and audit material into execution order
- keep the phase plan as the one execution checklist

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Sections 5, 6, 7, and 8

## Reads for alignment

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 5) Target Architecture`
- `# 6) Call-Site Audit`
- `planning_passes`

## Writes

- `# 7) Depth-First Phased Implementation Plan (authoritative)`
- `arch_skill:block:phase_plan`

## Hard rules

- docs-only; do not modify code
- if the North Star, requested behavior scope, allowed architectural convergence scope, or any other plan-shaping decision is contradictory, stop and ask the exact blocker question
- if missing work is discovered while planning, add it to the phase plan only when repo truth plus approved scope make it clearly required; if requiredness depends on an unresolved user decision, stop and ask instead of downgrading it by taste
- if adjacent-surface disposition or compatibility posture is still unresolved, stop and ask instead of hiding the fork in Section 7
- before a phase is valid, run an obligation sweep across Section 5, Section 6, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridge removal, and any helper-added ship-blocking work
- every required obligation from that sweep must be represented in `Checklist (must all be done)` or `Exit criteria (all required)`; do not leave standalone required work only in `Work`, `Verification`, `Docs/comments`, migration prose, or surrounding narrative
- for agent-backed systems, prompt, grounding, and native-capability changes get first right of refusal before new harnesses, wrappers, parsers, OCR layers, or scripts
- if a phase includes new tooling for agent-backed behavior, say why prompt-first and capability-first options were insufficient
- do not add scripts, tests, CI checks, or validation steps whose primary job is auditing docs/help, checking keyword absence, policing repo layout, or proving deletions by grep
- only ship-blocking work belongs in the authoritative checklist
- if the change would leave touched live docs, comments, or instructions stale, update-or-delete work for those surfaces belongs in the phase plan
- do not assume backward compatibility by default; the phase plan must encode the chosen preservation, clean-cutover, or approved-bridge story explicitly
- do not turn helper blocks into competing execution checklists
- do not leave the authoritative checklist holding unresolved branches, `if needed` work, or alternative execution paths
- split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later
- earlier phases should establish the most fundamental owner paths, contracts, prompt surfaces, or migration prerequisites, and later phases should clearly build on that foundation
- if two decompositions are both valid, bias toward more phases than fewer
- `Work` explains the coherent unit; for modern docs it is explanatory only and must not carry standalone obligations
- `Checklist` is the exhaustive must-do list inside that phase
- `Exit criteria` must name the exhaustive concrete done-state that auditing will validate, not summary vibes or restated goals
- a phase is not complete on paper unless every checklist item and every exit criterion is satisfied

## Warn-first preflight

Before writing the phase plan:

- inspect `planning_passes` if present
- otherwise infer from research and deep-dive content
- if recommended sequencing is incomplete or unknown, do not stop
- instead warn clearly and continue writing the plan

## Quality bar

- Section 7 must stay the one authoritative execution checklist
- the plan must be foundational-first
- each phase should own one coherent self-contained unit of work that later phases can build upon
- if two decompositions are both valid, the plan should prefer more phases than fewer
- each phase must have goal, work, checklist, verification, docs/comments when needed, exit criteria, and rollback
- each phase must pass an obligation sweep so required work cannot hide outside the authoritative phase-exit surface
- `Checklist` must be exhaustive enough that the implementer cannot escape required work by claiming the phase is "basically done"
- `Exit criteria` must be exhaustive, concrete, and all required
- `Work` must explain the unit without carrying standalone required obligations
- `Verification` must give a credible proof path for the phase claims, but required phase-complete truths belong in `Exit criteria`
- required docs/comments propagation, deletes, migrations, and bridge-removal work must appear in the authoritative phase-exit surface when the phase cannot be complete without them
- refactor-heavy phases must say how preserved behavior will be proven
- agent-backed phases must make capability-first choices explicit before adding custom tooling
- adjacent-surface follow-through and migration or cutover work must be visible in the relevant phases instead of being left implicit
- verification should be credible, proportionate, and non-bureaucratic
- verification must stay tied to shipped behavior, runtime ownership, or real contract boundaries rather than repo-policing heuristics
- required cleanup, deletes, and touched doc/comment reality-sync work should not be buried
- phases must name the actual chosen work to do, not conditional or alternate branches the agent would have to choose between later
- if a phase contains multiple coherent units that could be built and verified separately, split it

## Placement and update rules

Update in this order:

1. replace inside `arch_skill:block:phase_plan` when it exists
2. otherwise update an existing phase-plan or phased-implementation section in place
3. otherwise insert a new top-level Section 7 after Call-Site Audit, after Target Architecture, or after Research/Problem sections

If the doc is canonical, preserve exact Section 7 heading and numbering.

Use this block shape:

```text
<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit and is explanatory only for modern docs. `Checklist (must all be done)` is the authoritative must-do list inside the phase. `Exit criteria (all required)` names the exhaustive concrete done conditions the audit must validate. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Before a phase is valid, run an obligation sweep and move every required promise from architecture, call-site audit, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridges, and required helper follow-through into `Checklist` or `Exit criteria`. The authoritative checklist must name the actual chosen work, not unresolved branches or "if needed" placeholders. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). If a bridge is explicitly approved, timebox it and include removal work; otherwise plan either clean cutover or preservation work directly. Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests and heuristic gates (deletion checks, visual constants, doc-driven gates, keyword or absence gates, repo-shape policing). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

## Phase 1 — <most fundamental coherent unit>

* Goal:
* Work:
* Checklist (must all be done):
* Verification (required proof):
* Docs/comments (propagation; only if needed):
* Exit criteria (all required):
* Rollback:

## Phase N — <next coherent unit built on earlier phases>

* Goal:
* Work:
* Checklist (must all be done):
* Verification (required proof):
* Docs/comments (propagation; only if needed):
* Exit criteria (all required):
* Rollback:
<!-- arch_skill:block:phase_plan:end -->
```

Use `Work` to describe the coherent unit and why it is isolated in that phase. For modern docs, do not hide standalone obligations there. Use `Checklist` for the exhaustive required actions inside that unit. Use `Exit criteria` for the exhaustive concrete done-state that auditing must validate. If a planned item could be left undone while the phase still sounds "basically complete," or if a phase-complete truth appears only in prose, the phase is underspecified and should be split or tightened.
If the change spans a contract family or migration boundary, encode the chosen adjacent-surface follow-through and the chosen cutover, preservation, or approved-bridge work directly in the relevant phase instead of leaving that choice implicit.
Use `Docs/comments` to explain live docs/comments propagation. If deleting or rewriting those surfaces is required for the phase to be complete, also represent that required work in `Checklist` or `Exit criteria`. Do not keep legacy explanation in live surfaces just because Git already preserves the old version.

## Consistency duties beyond local ownership

- if the phase plan changes sequencing, convergence scope, or verification expectations, repair the now-stale claims in TL;DR, Section 0, and Section 8
- if new sequencing or scope decisions replace an earlier assumption, append or update Section 10
- Section 7 must remain the one execution checklist even after helper blocks exist

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if the North Star, requested behavior scope, allowed architectural convergence scope, or any phase-shaping decision is contradictory or unresolved, stop and ask the exact blocker question
- otherwise stop after the authoritative phase plan is updated and any warn-first caveats are surfaced

## Console contract

- one-line North Star reminder
- one-line punchline
- what changed in the phase plan
- warn about missing earlier passes when relevant
- next action
