# Artifact Contract

`plan-implement` keeps three artifacts distinct. Use the smallest useful
artifact updates needed to keep implementation fast and resumable.

## Plan Doc

The plan is source of truth for:

- North Star and done-state requirements
- requirements, non-requirements, constraints, and non-constraints
- active scope, stop boundary, phase order, and exclusions
- owner-path, delete, side-door, compatibility, and proof promises
- initial pre-freeze convergence closure and explicit later human approvals
- decisions that change the intended outcome
- completion state when the plan format has checkboxes or phase status

Update the plan when source truth changes. Do not hide decisions in the
implementation log.

Good plan updates:

- mark a plan item complete with code and proof anchors when the outcome is
  true
- carry an ambiguity decision through requirements, architecture, phase order,
  delete list, and proof strategy
- add a completion anchor for a delete or side-door closure already present in
  the frozen convergence closure
- remove a false constraint that was creating complexity

Bad plan updates:

- rewriting the plan as a running diary
- checking off tasks because files changed while the outcome remains false
- hiding unresolved ambiguity in notes
- turning the plan into a command log
- adding a newly discovered adjacent path after freeze or editing the plan to
  ratify work that was already built without human approval

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
- plan-backed code review verdicts

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
Scope contract anchor: <plan section/revision>
Scope status: <frozen | human decision needed | legacy boundary unresolved>
Last updated: <date/time>
Current checkpoint: <commit/hash/worktree/diff handle if useful>

## Resume Snapshot

- Current state:
- Next useful move:
- Do not redo unless stale:
- Known blockers:
- Native subagents used or useful next:

## Scope Ledger

| Item | Plan anchor | Scope disposition | Status | Code anchor | Proof | Review |
| --- | --- | --- | --- | --- | --- | --- |

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

Include only adjacent surfaces already named in the frozen closure, plus
observations clearly labeled `new-scope-needs-human` or `out-of-scope`. This
ledger points to the plan contract; it does not copy or enlarge it.

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
- when code truth proves an in-scope plan fact stale without changing scope
- when the relevant human decision owner explicitly approves a scope change;
  record the approval and re-freeze before implementation resumes

Do not update all three artifacts for every event. Use the owning artifact.
