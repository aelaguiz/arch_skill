# Artifact Contract

`plan-implement` keeps three artifacts distinct. Use the smallest useful
artifact updates needed to keep implementation fast and resumable.

## Plan Doc

The plan is source of truth for:

- North Star and done-state requirements
- requirements, non-requirements, constraints, and non-constraints
- active scope, stop boundary, phase order, and exclusions
- owner-path, delete, side-door, compatibility, and proof promises
- convergence decisions for adjacent same-contract or same-behavior surfaces
- decisions that change the intended outcome
- completion state when the plan format has checkboxes or phase status

Update the plan when source truth changes. Do not hide decisions in the
implementation log.

Good plan updates:

- mark a plan item complete with code and proof anchors when the outcome is
  true
- carry an ambiguity decision through requirements, architecture, phase order,
  delete list, and proof strategy
- add a required delete or side-door closure discovered from code truth
- remove a false constraint that was creating complexity

Bad plan updates:

- rewriting the plan as a running diary
- checking off tasks because files changed while the outcome remains false
- hiding unresolved ambiguity in notes
- turning the plan into a command log

## Plan Audit Log

The existing plan-audit ledger remains:

```text
<PLAN_STEM>_PLAN_AUDIT.md
```

Use it for:

- unresolved `PLA-*` plan-readiness findings
- `IMP-*` implementation-audit findings
- ambiguity and decision carry-through
- relevant-code coverage that affects plan or implementation approval
- plan-backed code-review verdicts

Do not use it as a task board, proof ledger, or implementation diary.

## Implementation Log

For non-trivial file-backed implementation scopes, create or update:

```text
<PLAN_STEM>_IMPLEMENTATION_LOG.md
```

The implementation log is a speed and resumability artifact. It tells the next
agent what has already been read, changed, proved, reviewed, and what would
make that state stale.

Suggested shape:

```markdown
# Plan Implementation Log

Plan: <path>
Audit log: <path or none>
Active scope: <phase | section | whole plan | user-defined stop boundary>
Last updated: <date/time>
Current checkpoint: <commit/hash/worktree/diff handle if useful>

## Resume Snapshot

- Current state:
- Next useful move:
- Do not redo unless stale:
- Known blockers:
- Native subagents used or useful next:

## Scope Ledger

| Item | Plan anchor | Status | Code anchor | Proof | Review |
| --- | --- | --- | --- | --- | --- |

## Code Read Ledger

| Area | Files/symbols read | Why relevant | Fresh until | Notes |
| --- | --- | --- | --- | --- |

## Proof Freshness Ledger

| Proof | Scope covered | Result/context | Fresh until | Rerun trigger |
| --- | --- | --- | --- | --- |

## Continuous Review Ledger

| Finding | Source | Status | Repair anchor | Notes |
| --- | --- | --- | --- | --- |

## Side Doors And Deletes

Include adjacent same-contract or same-behavior surfaces here when leaving
them live could split the system between old and new behavior.

| Surface | Expected state | Current state | Status | Anchor |
| --- | --- | --- | --- | --- |

## Decision Carry-Through

| Decision | Owner | Plan carry-through | Code carry-through | Status |
| --- | --- | --- | --- | --- |

## Pass Notes

### <date/time> - <short pass title>

- Intent:
- Changed:
- Read:
- Proof:
- Review:
- Next:
```

Keep the `Resume Snapshot` current at meaningful boundaries. It is the fastest
path back into the work after compaction.

## Update Discipline

Update the worklog:

- before first implementation in a non-trivial plan scope
- after finishing a meaningful slice
- after discovering a side door, stale plan fact, or complexity source
- after running, accepting, or invalidating proof
- after native subagent review returns useful findings
- before compaction risk, long-running work, stopping, or completion claims

Update the audit log:

- when a `PLA-*` finding affects implementation
- when an `IMP-*` finding opens, closes, is rejected, or becomes out of scope
- when code truth changes a previous audit conclusion
- before final implementation-audit verdict

Update the plan:

- when a decision becomes source truth
- when completion state changes
- when code truth proves the plan stale
- when the smallest correct implementation requires scope change and the
  decision owner accepts it

Do not update all three artifacts for every event. Use the owning artifact.
