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
- initial/resume dirty-worktree checkpoint commit when one was created
- active phase and stop boundary
- implementation and review policy
- slices, dependencies, likely collisions, and proof needed
- implementation waves, repair waves, verification waves, and review/consult
  waves
- verification map: plan-required proof, changed and impacted surfaces, tests
  already passing, rerun triggers, and skipped broad checks with rationale
- worker runtime/model, session id, status, and worklog path
- child prompt parallelism posture
- scarce verification assignments
- batch, repair-wave, review-cleanup, and final phase commit checkpoints
- arbiter and thermonuclear review status
- accepted, rejected, and deferred review findings
- retries, issues, attempted responses, results, and next actions
- completion gates
- latest `Progress Snapshot` tables

The ledger must not contain secrets.

Commit checkpoint entries should include the commit hash, short message, and
why it was taken, such as `resume dirty tree`, `batch landed`,
`accepted-review-repair`, or `final phase report`. The ledger does not need a
perfect commit narrative; it just needs enough breadcrumbs to recover progress.

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
Use the `Goal` or `Status` cell to make wave type visible when helpful:
implementation, repair, verification, or review.
Use the `Proof` cell to name the confidence target, such as plan-required
scenario, impacted owner boundary, affected integration path, or already-passing
proof that remains trusted.

### Workers Now

Columns: `Worker`, `Runtime/Model`, `Slice`, `State`, `Current Task`,
`Session`.

Use this table to show how many workers are executing and what each one is
doing. Include idle, blocked, review, and verification workers when they matter
to the next decision. Use `quiet/observing` for a worker with no recent visible
event stream when the slice may legitimately be thinking, running, sleeping, or
waiting. Do not mark that worker `stuck` unless there is evidence beyond
silence.

### Phase Difficulties And Retries

Columns: `Issue`, `Where`, `Impact`, `Retry/Response`, `Current State`,
`Next Action`.

Use this table for the current phase's blockers, failed or struggling workers,
review findings, test failures, merge/collision trouble, resource contention,
unclear ownership, and repeated retries. Each issue should name the affected
worker or slice when known, what response was already tried, the result, and
the next recovery action. For accepted findings, name the repair or
verification wave that owns the response. If no difficulty is known yet,
include one `none observed` row.

Quiet-worker entries should include the last observed signal, how long the
worker has been quiet when known, why waiting is still reasonable, and the next
check point. Treat a couple of quiet minutes as normal; roughly five minutes
without visible events starts inspection, not replacement.

## Verification Map

Keep the verification map lightweight and human-readable. It is not a generated
test plan or deterministic matrix. It should answer:

- What does the plan explicitly require us to prove?
- What changed, and what adjacent behavior could that change affect?
- Which focused checks or scenarios provide high confidence?
- Which expensive or broad checks are intentionally not being run now, and why?
- Which previous passing checks remain valid, and what would force a rerun?

## Prompt-First Artifact Rule

Use ordinary file reads, searches, shell commands, and existing delegation
skills. Keep coordination state readable as plain Markdown so any parent agent,
worker, or reviewer can inspect it directly.
