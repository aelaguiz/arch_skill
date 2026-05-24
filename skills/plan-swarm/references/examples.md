# Examples

## Cursor Agent Phase Run

User intent:

```text
Finish Phase 14 from docs/PACKS/example-plan.md using Cursor Agent workers.
```

Parent setup note:

```text
Implementation: Cursor Agent, model composer-2.5-fast, max parallel 4.
Review: Codex gpt-5.4 xhigh unless user asks for the same runtime.
Artifacts: docs/PACKS/example-plan_plan_swarm/phase-14/.
Git: commit dirty resume state first if present; commit meaningful worker
batches and final report locally. No push or PR unless explicitly asked.
North star: batch and parallelize. Parent coordinates; workers implement,
repair, and run assigned verification.
```

## Progress Update

```markdown
### Phase Progress

| Phase | Scope | % | Status | Evidence | Note |
| --- | --- | ---: | --- | --- | --- |
| Phase 14 | command metadata, QA adapters, overlays, persistence cleanup | 45% | implementing | contract + 3 active slices | Review not started. |

### Current Phase Work Slices

| Slice | Goal | Worker | Parallelization | Status | Proof |
| --- | --- | --- | --- | --- | --- |
| qa-adapters | Move QA registration to feature-owned adapters. | worker-a | Independent from overlay cleanup; shared QA boundary only. | running | owner-boundary tests |
| command-service | Route execution through command service/session. | worker-b | Serial before legacy deletion. | running | command execution tests |
| overlay-save | Remove raw writer/provider calls in overlays. | worker-c | Parallel with QA adapters; watches command-service API. | running | overlay save checks |
| legacy-cleanup | Delete or wall off direct mutation paths. | waiting | Depends on command-service replacement. | pending | deletion checkpoint |

### Workers Now

| Worker | Runtime/Model | Slice | State | Current Task | Session |
| --- | --- | --- | --- | --- | --- |
| worker-a | agent/composer-2.5-fast | qa-adapters | executing | Feature QA registration | s-qa |
| worker-b | agent/composer-2.5-fast | command-service | executing | Session execution path | s-cmd |
| worker-c | agent/composer-2.5-fast | overlay-save | executing | Overlay persistence calls | s-overlay |

### Phase Difficulties And Retries

| Issue | Where | Impact | Retry/Response | Current State | Next Action |
| --- | --- | --- | --- | --- | --- |
| command API uncertainty | command-service | May block legacy cleanup. | Worker inspected owning service and tests. | Still resolving exact call boundary. | Parent waits before launching cleanup. |
```

## Manual Update Request

When the user asks `status?`, `what is running?`, `where are we?`, or similar
while `plan-swarm` is active, answer with the same `Progress Update` table
bundle. Refresh the table from `swarm-ledger.md`, worker logs, current repo
state, and known child-session results before replying.

```markdown
### Phase Progress

| Phase | Scope | % | Status | Evidence | Note |
| --- | --- | ---: | --- | --- | --- |
| Phase 14 | command metadata, QA adapters, overlays, persistence cleanup | 55% | implementing | 2 slices reported, 1 active | Cleanup still waits on command-service boundary. |

### Current Phase Work Slices

| Slice | Goal | Worker | Parallelization | Status | Proof |
| --- | --- | --- | --- | --- | --- |
| command-service | Route execution through command service/session. | worker-b | Serial before legacy deletion. | running | command execution tests |
| legacy-cleanup | Delete or wall off direct mutation paths. | waiting | Depends on command-service replacement. | pending | deletion checkpoint |
| verify-command-service | Rerun command execution tests after repair wave. | worker-v | Verification lease; waits for command-service repair. | waiting | exact test results |

### Workers Now

| Worker | Runtime/Model | Slice | State | Current Task | Session |
| --- | --- | --- | --- | --- | --- |
| worker-b | agent/composer-2.5-fast | command-service | executing | Session execution path | s-cmd |

### Phase Difficulties And Retries

| Issue | Where | Impact | Retry/Response | Current State | Next Action |
| --- | --- | --- | --- | --- | --- |
| command API uncertainty | command-service | Cleanup waits. | Resumed same healthy worker with narrower prompt. | in progress | Check worker-b report before launching cleanup. |
```

## Worker Prompt Skeleton

```text
Use $agent-delegate with Cursor Agent composer-2.5-fast.

Finish the "qa-adapters" slice from docs/PACKS/example-plan_plan_swarm/phase-14/swarm-ledger.md.

Read the phase contract first. The plan doc remains source of truth. Other
workers may be editing sibling slices, so do not revert unfamiliar changes.
You may inspect adjacent owning code and make task-relevant edits needed to
complete this slice.

Maximize parallelism by using parallel agents. Do not invoke skills that spawn
subagents.

Do not broaden product scope, push, stash, or run the full suite unless the
parent assigns that verification resource. The parent owns commit checkpoints
unless this prompt explicitly assigns you one.

End with the required plan-swarm worker footer.
```

## Repair Wave Prompt Skeleton

```text
Use $agent-delegate with Cursor Agent composer-2.5-fast.

Resume worker-b for the "command-service-repair" repair slice from
docs/PACKS/example-plan_plan_swarm/phase-14/swarm-ledger.md.

Accepted findings in this repair wave:
- command execution bypass: overlay path still calls raw writer instead of
  SurfaceSceneDevCommandService.
- stale direct-save branch: old mutation path remains reachable after session
  execution replacement.

Likely fix path: start at the service/session call boundary and the overlay
save tests. This is a hint, not a script; inspect the owning code and choose
the cleanest implementation that satisfies the phase contract.

Maximize parallelism by using parallel agents. Do not invoke skills that spawn
subagents.

Do not broaden product scope, push, stash, or run the full suite unless the
parent assigns that verification resource. End with the required plan-swarm
worker footer.
```

## Verification Wave Prompt Skeleton

```text
Use $agent-delegate with Cursor Agent composer-2.5-fast.

Run the "verify-command-service" verification slice from
docs/PACKS/example-plan_plan_swarm/phase-14/swarm-ledger.md.

You have the command-service verification lease. Run the listed command
execution tests, inspect failures if any, and report exact commands/results.
Do not edit source unless the verification slice explicitly asks for a repair.

Maximize parallelism by using parallel agents. Do not invoke skills that spawn
subagents.

End with the required plan-swarm worker footer.
```

## Review Triage

```text
Accepted:
- boundary-leak: route to qa-adapters worker; directly violates owner-boundary requirement.
- command execution bypass: route to command-service repair wave with overlay
  save tests as proof.

Rejected:
- none

Deferred:
- old-naming-debt: real debt, but outside the named phase.
```
