# Examples And Anti-Examples

Use these as illustrations, not rigid templates.

## Clean Worklog Resume Snapshot

```markdown
## Resume Snapshot

- Current state: Phase 3 owner path is implemented for the primary command;
  legacy direct writer still needs deletion check.
- Next useful move: search old command and fixture entrypoints for direct
  writes before widening to adapters.
- Do not redo unless stale: command-service caller map read at
  `src/commands/*` and `src/session/*`; stale if those files change.
- Known blockers: none.
- Native subagents used or useful next: useful next for docs/prompts drift
  after side-door cleanup.
```

## Clean Proof Freshness Entry

```markdown
| Proof | Scope covered | Result/context | Fresh until | Rerun trigger |
| --- | --- | --- | --- | --- |
| `uv run pytest tests/test_command_service.py` | Primary command routes through canonical service | Passed locally | Command service, metadata schema, adapter registration, or caller routes change | Any touched path above, review finding about command routing, or plan-required final proof |
```

## Continuous Review Finding

```markdown
| Finding | Source | Status | Repair anchor | Notes |
| --- | --- | --- | --- | --- |
| IMP-002 old command still calls direct writer | deletion-and-side-door closure | open | `src/commands/legacy.py` | Blocks Phase 3 approval because the old write path remains reachable |
```

## Good Plan Update

Good: code truth confirms an old adapter already named in the frozen initial
convergence closure; the plan's completion state and proof anchors are updated.

Why it is good: the plan stays source of truth instead of hiding the delete in
the implementation log.

Bad: warm review discovers a different adapter, adds it to the plan, and sends
the implementer to delete it because convergence would be cleaner.

Why it is bad: review discovered new scope after freeze. Record
`new-scope-needs-human`; do not implement it unless a human approves and
re-freezes the plan.

## Anti-Example: Ceremony

Bad: update the plan, audit log, and implementation log after every tiny edit.

Why it is bad: the artifacts become slower than the work.

Better: update the owning artifact at meaningful boundaries.

## Anti-Example: Second Plan

Bad: the implementation log grows a new task list that changes the plan's
requirements.

Why it is bad: future agents now have two competing sources of truth.

Better: source-truth changes go into the plan; execution state goes into the
implementation log.

## Anti-Example: Test Rerun Treadmill

Bad: rerun the same broad suite after compaction because the chat no longer
contains the prior result.

Why it is bad: the implementation log should preserve proof freshness and stale
triggers.

Better: read the proof ledger, inspect whether relevant code changed, and rerun
only if stale or required.

## Anti-Example: Final Review Only

Bad: implement every caller first, then discover at the end that the owner path
or side-door assumption was wrong.

Why it is bad: late architecture findings are expensive.

Better: review the first narrow integrated slice, repair it, then widen.

## Anti-Example: External Harness Creep

Bad: manually shell out to `codex`, `claude`, `agent`, or `grok` because
parallelism sounds useful.

Why it is bad: that turns a lightweight implementation habit into a delegation
workflow.

Better: use native subagents when available. Use `plan-conductor` or
`agent-delegate` only when the user explicitly asks for external workers.
