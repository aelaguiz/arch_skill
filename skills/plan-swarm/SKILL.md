---
name: plan-swarm
description: "Prompt-first implementation swarm orchestrator for finishing a named phase or phase range from an existing plan document. The parent agent extracts the phase contract, decomposes it into independently delegable work slices, uses agent-delegate to run/resume parallel Codex, Claude, or Cursor Agent workers, coordinates scarce verification manually, writes worklogs next to the plan, and gates completion through delegated arbiter plus thermonuclear review. Do NOT use for creating plans, one-shot delegation, strict ordered processes, or review-only work."
metadata:
  short-description: "Parallel plan-phase implementation orchestrator"
---

# Plan Swarm

Use this skill when the user wants to implement an existing plan document faster
by splitting one approved phase into independent work slices, running capable
implementation workers in parallel, and holding phase closure behind real
review and proof.

This is a prompt-first orchestration skill. The parent agent is the
orchestrator: it reasons about the phase, launches and resumes workers through
existing capabilities such as `$agent-delegate`, inspects the real worktree,
and keeps the human worklogs current.

## Use When

- The user names an existing plan doc and asks to finish one phase quickly.
- A plan phase has independent owner surfaces that can be delegated in
  parallel.
- The user asks for Codex, Claude, or Cursor Agent workers to implement plan
  slices.
- A phase needs an external arbiter and strict maintainability pass before it
  can be called done.

## Do Not Use When

- The plan does not exist yet. Use `$arch-step`, `$miniarch-step`, or
  `$arch-mini-plan`.
- The work is a multi-plan epic decomposition. Use `$arch-epic`.
- The workflow is a strict ordered process from another repo's doctrine. Use
  `$stepwise`.
- The user only wants one child worker. Use `$agent-delegate`.
- The user only wants a review or second opinion. Use `$fresh-consult` or
  `$code-review`.
- The user wants worktrees, commits, pushes, PRs, or detached workers. Those
  are not v1 defaults and require an explicit separate ask.

## Non-Negotiables

- One active phase or explicit phase range at a time.
- The plan doc remains source of truth. The swarm ledger is schedule and
  evidence, not a second plan.
- Stop at the requested boundary. Do not continue into final-pack signoff when
  the user asked for one phase.
- Cursor Agent implementation defaults to `composer-2.5-fast` only when the
  user explicitly chooses Cursor Agent.
- Review runtime/model/effort must be explicit, or the user must say review is
  same as implementation.
- Workers are prompted like capable engineers, not micromanaged checklist
  executors.
- Parent coordinates scarce verification resources; workers do not all run the
  full suite at once.
- Parent gives periodic and user-requested Markdown table updates from the
  swarm ledger so the user can see phase progress, current chunks, active
  workers, and current difficulties at a glance.
- Related repairs resume the same healthy worker session by default.
- Arbiter review is delegated and observation-only.
- Thermonuclear maintainability review is required before phase closure unless
  the user explicitly disables it.
- Accepted findings become repair slices. Rejected or deferred findings need a
  recorded scope or evidence rationale.
- Never claim completion from worker self-certification alone.

## First Move

1. Read `references/workflow-contract.md`.
2. Read `references/phase-contract.md`.
3. Read `references/decomposition-and-scheduling.md`.
4. Resolve the plan path, active phase, stop boundary, work root,
   implementation policy, review policy, and max parallelism.
5. Read the active phase plus plan-level Definition of Done items relevant to
   owner boundaries, validation, persistence, cleanup, and review.
6. Write a compact phase contract and swarm ledger next to the plan before
   launching workers.
7. Send the first progress update with the required tables.
8. Launch independent workers with `$agent-delegate`, then keep the ledger,
   worklogs, session ids, proof, and review triage current by hand.

## Workflow

1. Extract the phase contract from the plan and repo evidence.
2. Decompose into slices by owner boundary, dependency, proof, cleanup, and
   scarce-resource boundaries.
3. Launch as many independent slices in parallel as the worktree and resource
   constraints can safely support.
4. After each batch, inspect worker reports, changed files, resource use, and
   repo state before launching more work.
5. Update the ledger and send a table update whenever workers launch, finish,
   block, retry, hit an issue, or move into review/repair.
6. Route valid gaps back to workers, usually by resuming the related session.
7. Launch an observation-only arbiter to compare implementation against the
   phase contract and architectural cleanliness.
8. Run thermonuclear maintainability review. Triage findings as accepted,
   rejected, or deferred.
9. Repair accepted findings, verify proportionally, write the final phase
   report, and stop at the requested boundary.

## Progress Updates

Give concise Markdown table updates after phase-contract creation, after each
worker batch launches or finishes, after review gates, and before final report.
When the user asks for an update, status, what is running, what is blocked, or
where the phase stands while `plan-swarm` is active, answer with the same table
format. Refresh from the swarm ledger, worker logs, current repo state, and
known child-session results before answering. Do not fake precision: percent
is a judgment estimate backed by evidence.

Each update includes:

- `Phase Progress`: `Phase`, `Scope`, `%`, `Status`, `Evidence`, `Note`
- `Current Phase Work Slices`: `Slice`, `Goal`, `Worker`,
  `Parallelization`, `Status`, `Proof`
- `Workers Now`: `Worker`, `Runtime/Model`, `Slice`, `State`,
  `Current Task`, `Session`
- `Phase Difficulties And Retries`: `Issue`, `Where`, `Impact`,
  `Retry/Response`, `Current State`, `Next Action`

Use the difficulties table for blockers, failed or struggling workers, review
findings, test failures, merge/collision trouble, scarce-resource contention,
unclear ownership, and repeated retries. If no difficulty is known yet, include
one `none observed` row instead of omitting the table.

Percent guidance:

- `0%`: not started
- `10-30%`: contract and decomposition underway
- `40-70%`: implementation slices actively landing
- `80-90%`: implementation done; review, verification, or repair in progress
- `100%`: contract covered, accepted findings repaired or triaged, proof
  recorded, and stop boundary honored

## Output

Report compactly:

- active phase and stop boundary
- progress tables when a phase, batch, review, or final-report boundary changes
- the same progress tables when the user manually asks for an update during a
  `plan-swarm` run
- implementation and review policies
- slices launched, completed, blocked, or waiting
- difficulties, retries, issues, and next recovery action
- verification commands and proof gaps
- arbiter and thermonuclear findings triage
- files changed and worklog paths
- next action

## Reference Map

- `workflow-contract.md` - parent-agent lifecycle and stop discipline
- `phase-contract.md` - how to extract the active phase without inventing scope
- `decomposition-and-scheduling.md` - parallel slice design and launch judgment
- `worker-prompt-contract.md` - implementation worker prompt shape and footer
- `arbiter-and-review.md` - delegated arbiter, thermonuclear gate, and triage
- `resource-leases.md` - scarce verification resources
- `session-reuse.md` - when to resume or respawn workers
- `run-state-and-artifacts.md` - human worklog layout and ledger expectations
- `examples.md` - compact orchestration and worker prompt examples
