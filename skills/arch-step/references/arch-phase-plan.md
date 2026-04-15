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
- for agent-backed systems, prompt, grounding, and native-capability changes get first right of refusal before new harnesses, wrappers, parsers, OCR layers, or scripts
- if a phase includes new tooling for agent-backed behavior, say why prompt-first and capability-first options were insufficient
- do not add scripts, tests, CI checks, or validation steps whose primary job is auditing docs/help, checking keyword absence, policing repo layout, or proving deletions by grep
- only ship-blocking work belongs in the authoritative checklist
- if the change would leave touched live docs, comments, or instructions stale, update-or-delete work for those surfaces belongs in the phase plan
- do not assume backward compatibility by default; the phase plan must encode the chosen preservation, clean-cutover, or approved-bridge story explicitly
- do not turn helper blocks into competing execution checklists
- do not leave the authoritative checklist holding unresolved branches, `if needed` work, or alternative execution paths
- split Section 7 into the smallest reasonable sequence of coherent self-contained units that can be completed, verified, and built on later
- earlier phases should establish the most fundamental owner paths, contracts, prompt surfaces, or migration prerequisites, and later phases should clearly build on that foundation
- if two decompositions are both valid, bias toward more phases than fewer
- `Work` explains the coherent unit; `Checklist` is the exhaustive must-do list inside that phase
- a phase is not complete on paper unless every checklist item and every exit criterion is satisfied

## Warn-first preflight

Before writing the phase plan:

- inspect `planning_passes` if present
- otherwise infer from deep-dive and external-research content
- if recommended sequencing is incomplete or unknown, do not stop
- instead warn clearly and continue writing the plan

## Quality bar

- Section 7 must stay the one authoritative execution checklist
- the plan must be foundational-first
- each phase should own one coherent self-contained unit of work that later phases can build upon
- if two decompositions are both valid, the plan should prefer more phases than fewer
- each phase must have goal, work, checklist, verification, docs/comments when needed, exit criteria, and rollback
- `Checklist` must be exhaustive enough that the implementer cannot escape required work by claiming the phase is "basically done"
- `Exit criteria` must be exhaustive, concrete, and all required
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

> Rule: systematic build, foundational first; split Section 7 into the smallest reasonable sequence of coherent self-contained units that can be completed, verified, and built on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit; `Checklist (must all be done)` is the authoritative must-do list inside the phase; `Exit criteria (all required)` names the concrete done conditions. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). If a bridge is explicitly approved, timebox it and include removal work; otherwise plan either clean cutover or preservation work directly. The authoritative checklist must name the actual chosen work, not unresolved branches or "if needed" placeholders. Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests and heuristic gates (deletion checks, visual constants, doc-driven gates, keyword or absence gates, repo-shape policing). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

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

Use `Work` to describe the coherent unit and why it is isolated in that phase. Use `Checklist` for the exhaustive must-do items inside that unit. If a planned item could be left undone while the phase still sounds "basically complete," the phase is underspecified and should be split or tightened.
If the change spans a contract family or migration boundary, encode the chosen adjacent-surface follow-through and the chosen cutover, preservation, or approved-bridge work directly in the relevant phase instead of leaving that choice implicit.
Use `Docs/comments` to delete dead live docs/comments or rewrite surviving ones to present truth when the phase changes what is real. Do not keep legacy explanation in live surfaces just because Git already preserves the old version.

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
