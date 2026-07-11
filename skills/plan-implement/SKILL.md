---
name: plan-implement
description: "Implement an existing plan, phase, section, or checklist faster by keeping the plan, audit log, implementation log, proof freshness, and warm plan-backed code review aligned while coding. Use when the user wants plan-backed implementation with less duplicate rereading, fewer repeated checks, compaction-safe progress, native subagent acceleration when available, and continuous review against plan-audit quality doctrine. Not for creating plans, generic code review, external worker swarms, CI policing, deterministic runners, or manually spawning coding-harness executables."
metadata:
  short-description: "Plan-backed implementation with resumable review state"
---

# Plan Implement

Use this skill when the user wants code implemented from an existing plan,
phase, section, checklist, issue plan, or design doc while preserving plan
truth, review state, proof freshness, and resumability.

The job is to go faster by wasting less motion: fewer repeated code reads,
fewer duplicate checks, fewer late review surprises, and less context loss
after compaction.

This is a doctrine-only, prompt-first implementation skill. It must not become
a deterministic harness, runner, controller, workflow engine, checklist
executor, test scheduler, CI verifier, code review subprocess launcher, scorer,
state machine, or script-backed completion judge.

## Use When

- The user asks to implement an existing plan, plan phase, plan section,
  checklist, issue-body plan, or documented implementation scope.
- The user wants implementation to stay aligned with plan quality doctrine,
  plan-audit findings, review state, and proof freshness.
- The user wants progress to survive compaction without rereading the same
  plan and code surfaces repeatedly.
- The user wants native subagents or parallel-agent features used for
  independent read, review, or safe low-collision implementation slices when
  the current coding harness supports them.

## Do Not Use When

- The plan does not exist yet. Use the repo's planning skill or normal planning
  flow.
- The user wants a plan audited before implementation. Use `plan-audit`.
- The user wants code already written for a plan reviewed without new
  implementation. Use `plan-audit implementation-audit`.
- The user wants a generic branch, diff, or PR reviewed. Use the host agent's
  normal review response.
- The user explicitly wants delegated external workers, resumable child
  sessions, or plan-wide worker orchestration with the parent acting as
  conductor and cynical reviewer. Route to `plan-conductor` under the shared
  agent policy.
- The user wants one explicit external worker. Route to `agent-delegate` under
  the shared agent policy.

## Non-Negotiables

- The plan remains the source of truth. Do not create a second plan in the
  worklog.
- The implementation log is a speed and resumability artifact. Keep it short
  enough for the next agent to read quickly.
- The plan audit log owns `PLA-*` and `IMP-*` review findings. Do not turn it
  into an implementation diary.
- Update artifacts at meaningful boundaries, not after every micro-edit.
- Choose depth-first slices: make one narrow frozen plan truth real, review it
  while warm, verify impact, then advance through breadth already authorized by
  the plan. Depth-first sequencing is not permission to widen scope.
- Proof freshness matters. Reuse passing proof until a real invalidator makes
  it stale; run checks when the plan, changed code, impacted behavior, or a
  review finding gives a reason.
- Apply `../_shared/agent-orchestration-policy.md` whenever implementation
  uses child agents.
- Use a coverage-led set of children for broad independent mapping, review, or
  safe low-collision implementation work when useful. Start each new
  independent child as a clean same-host native child when the active host
  supports it; keep lenses and owned paths non-overlapping and bound fanout by
  host slots, shared-file or shared-state collision risk, and parent
  integration capacity.
- Use bounded or full inherited context only for a named decision that exists
  solely in chat. Prefer plan, audit-log, implementation-log, and code paths
  over inheriting the parent's framing or completion story.
- Use the strongest read-only capability available for mapping and review
  children, also tell them not to edit or write, and have the parent compare
  repository status and diffs with the pre-dispatch state before accepting
  their evidence.
- Children do not create children or invoke delegation, consult, or review
  skills unless the parent explicitly assigns a nested scope and budget.
- The parent owns child accounting, evidence spot-checking, deduplication,
  integration, finding scope disposition, source-of-truth updates, proof
  claims, and final completion claims.
- Resume the exact implementer child for an accepted repair in its owned
  scope. Every independent recheck uses a new clean critic rather than the
  implementer's or an earlier critic's context.
- Do not manually spawn separate coding-harness executables such as `codex`,
  `claude`, or `agent` for ordinary acceleration. This lightweight lane may
  still hand an explicitly requested external worker or conductor to
  `agent-delegate` or `plan-conductor` under the shared policy; external
  execution is a deliberate route, not a blanket ban.
- Do not claim a plan item complete from logs or checkboxes alone. Read code
  anchors and confirm the outcome is true.
- Apply `../_shared/scope-and-convergence.md`. Before the first edit,
  recover the human baseline, initial minimal convergence closure, freeze
  boundary, and explicit later human approvals. If a legacy plan cannot support
  a defensible boundary, stop for one human scope decision.
- A warm review, subagent, test, worklog, or plan edit cannot expand scope.
  Give every material finding a shared scope disposition. Only `authorized` and
  `frozen-convergence-required` enter required implementation work; a newly
  discovered adjacent path is `new-scope-needs-human`, and already-built excess
  is subtraction work.

## First Move

1. Read `references/artifact-contract.md`.
2. Read `references/progressive-implementation-loop.md`.
3. Read `../_shared/scope-and-convergence.md`.
4. Read `../_shared/agent-orchestration-policy.md` before creating or
   resuming any child.
5. Resolve the plan artifact, requested scope, stop boundary, repo root, audit
   log path, and implementation log path.
6. Read the plan, existing plan audit log if present, existing implementation
   log if present, local instructions, and current worktree state.
7. Identify the next narrow depth-first slice and the proof or review likely to
   matter.
8. If the scope is broad, decide whether native children can save real time
   for independent mapping or review slices.

## Workflow

1. Resolve and restate the active plan scope. Do not silently widen.
2. Build the local truth cache: relevant plan anchors, code areas read,
   comparable patterns, side doors, proof already fresh, proof likely needed,
   and review lenses likely to matter.
3. Create or update `<PLAN_STEM>_IMPLEMENTATION_LOG.md` for non-trivial
   file-backed implementation scopes.
4. Implement the smallest useful depth-first slice using the repo's existing
   patterns and owner paths.
5. Review while the work is warm using plan-audit implementation-audit lenses.
   When children save time, use new clean native critics for independent
   read-only lenses. Send accepted repairs back to the exact implementer that
   owns the code, then use a different new clean critic for an independent
   recheck.
6. Run, assign, or reuse proof based on impact and freshness. Do not rerun
   checks only because prior context was forgotten.
7. Update the owning artifact: plan for source-truth changes, audit log for
   `PLA-*` or `IMP-*` findings, implementation log for resumability.
8. Advance to the next already-authorized slice only after the prior slice's
   code, plan, review, and proof state agree. New breadth requires human approval
   and re-freeze.
9. At the requested stop boundary, perform a final lightweight plan-backed
   implementation check and report remaining gaps plainly.

## Output Expectations

Return concise implementation status:

- active plan scope and stop boundary
- implementation log path and audit log path when applicable
- what changed
- what plan items moved state
- proof run, supplied, reused, stale, or intentionally not run
- review findings opened, repaired, rejected, or still open
- relevant code read and relevant code still unknown
- next useful move

For ongoing work, prefer a short progress update over a full report. The
implementation log carries detail so the chat can stay readable.

## Reference Map

- `references/artifact-contract.md` - plan, audit-log, and implementation-log ownership
- `references/progressive-implementation-loop.md` - ordered implementation loop
- `references/proof-freshness.md` - proof reuse, invalidators, and rerun triggers
- `references/continuous-review.md` - warm plan-backed review during implementation
- `references/native-subagent-contract.md` - native subagent use and prompt shapes
- `../_shared/agent-orchestration-policy.md` - transport, starting context,
  continuation, isolation, topology, and parent-integration policy
- `references/output-contract.md` - progress and final report contracts
- `references/examples.md` - examples and anti-examples
