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
- if the North Star, requested behavior scope, or allowed architectural convergence scope is contradictory, stop for a quick doc correction
- if missing work is discovered while planning, classify whether it is required convergence, anchored pattern/parity, concrete risk mitigation, optional quality, product scope creep, or architecture theater before adding it to the phase plan
- only ship-blocking work belongs in the authoritative checklist
- do not turn helper blocks into competing execution checklists

## Warn-first preflight

Before writing the phase plan:

- inspect `planning_passes` if present
- otherwise infer from deep-dive and external-research content
- if recommended sequencing is incomplete or unknown, do not stop
- instead warn clearly and continue writing the plan

## Quality bar

- Section 7 must stay the one authoritative execution checklist
- the plan must be foundational-first
- each phase must have goal, work, verification, docs/comments when needed, exit criteria, and rollback
- refactor-heavy phases must say how preserved behavior will be proven
- verification should be small, credible, and non-bureaucratic
- required cleanup and deletes should not be buried

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

> Rule: systematic build, foundational first; every phase has exit criteria + explicit verification plan (tests optional). Refactors, consolidations, and shared-path extractions must preserve existing behavior with the smallest credible signal. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests (deletion checks, visual constants, doc-driven gates). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

## Phase 1 — <foundation>

* Goal:
* Work:
* Verification (smallest signal):
* Docs/comments (propagation; only if needed):
* Exit criteria:
* Rollback:

## Phase N — <end state + cleanup>

* Goal:
* Work:
* Verification (smallest signal):
* Docs/comments (propagation; only if needed):
* Exit criteria:
* Rollback:
<!-- arch_skill:block:phase_plan:end -->
```

## Consistency duties beyond local ownership

- if the phase plan changes sequencing, convergence scope, or verification expectations, repair the smallest stale claims in TL;DR, Section 0, and Section 8
- if new sequencing or scope decisions replace an earlier assumption, append or update Section 10
- Section 7 must remain the one execution checklist even after helper blocks exist

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if the North Star, requested behavior scope, or allowed architectural convergence scope is contradictory, stop for a quick doc correction
- otherwise stop after the authoritative phase plan is updated and any warn-first caveats are surfaced

## Console contract

- one-line North Star reminder
- one-line punchline
- what changed in the phase plan
- warn about missing earlier passes when relevant
- next action
