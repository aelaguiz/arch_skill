# Worklogs And Artifacts

The parent agent keeps lightweight human artifacts next to the plan. These are
coordination notes, not a second plan and not machine-owned state.

## Layout

```text
<plan-dir>/<plan-basename>_plan_swarm/<phase-slug>/
  phase-contract.md
  swarm-ledger.md
  worker-<slice-id>.md
  arbiter-review.md
  thermo-triage.md
  final-phase-report.md
```

## Ledger Truth

`swarm-ledger.md` tracks:

- plan path and start hash
- active phase and stop boundary
- implementation and review policy
- slices, dependencies, likely collisions, and proof needed
- worker runtime/model, session id, status, and worklog path
- scarce verification assignments
- arbiter and thermonuclear review status
- accepted, rejected, and deferred review findings
- retries, issues, attempted responses, results, and next actions
- completion gates
- latest `Progress Snapshot` tables

The ledger must not contain secrets.

## Progress Snapshot

`swarm-ledger.md` must include a `Progress Snapshot` section with these four
Markdown tables. Keep the tables short enough to scan.

### Phase Progress

Columns: `Phase`, `Scope`, `%`, `Status`, `Evidence`, `Note`.

Use one row for the active phase when the user requested one phase. Use one row
per requested phase when the user requested a phase range. Percent values are
human estimates, not computed metrics.

### Current Phase Work Slices

Columns: `Slice`, `Goal`, `Worker`, `Parallelization`, `Status`, `Proof`.

This is the visible chunking table. It shows what work exists, who owns it, why
it can run now or must wait, and what proof will close it.

### Workers Now

Columns: `Worker`, `Runtime/Model`, `Slice`, `State`, `Current Task`,
`Session`.

Use this table to show how many workers are executing and what each one is
doing. Include idle, blocked, review, and verification workers when they matter
to the next decision.

### Phase Difficulties And Retries

Columns: `Issue`, `Where`, `Impact`, `Retry/Response`, `Current State`,
`Next Action`.

Use this table for the current phase's blockers, failed or struggling workers,
review findings, test failures, merge/collision trouble, resource contention,
unclear ownership, and repeated retries. Each issue should name the affected
worker or slice when known, what response was already tried, the result, and
the next recovery action. If no difficulty is known yet, include one
`none observed` row.

## Prompt-First Artifact Rule

Use ordinary file reads, searches, shell commands, and existing delegation
skills. Keep coordination state readable as plain Markdown so any parent agent,
worker, or reviewer can inspect it directly.
