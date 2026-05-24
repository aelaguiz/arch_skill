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
executor, test scheduler, CI verifier, code-review subprocess launcher, scorer,
state machine, or script-backed completion judge.

## Use When

- The user asks to implement an existing plan, plan phase, plan section,
  checklist, issue-body plan, or documented implementation scope.
- The user wants implementation to stay aligned with plan quality doctrine,
  plan-audit findings, code-review state, and proof freshness.
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
- The user wants a generic branch, diff, or PR reviewed. Use `code-review`.
- The user explicitly wants delegated external worker swarms, resumable child
  sessions, arbiter gates, or phase-swarm orchestration. Use `plan-swarm`.
- The user wants one explicit external worker. Use `agent-delegate`.

## Non-Negotiables

- The plan remains the source of truth. Do not create a second plan in the
  worklog.
- The implementation log is a speed and resumability artifact. Keep it short
  enough for the next agent to read quickly.
- The plan audit log owns `PLA-*` and `IMP-*` review findings. Do not turn it
  into an implementation diary.
- Update artifacts at meaningful boundaries, not after every micro-edit.
- Choose depth-first slices: make one narrow plan truth real, review it while
  warm, verify impact, then widen.
- Proof freshness matters. Reuse passing proof until a real invalidator makes
  it stale; run checks when the plan, changed code, impacted behavior, or a
  review finding gives a reason.
- Use native subagents or parallel-agent features for broad independent read,
  review, or safe low-collision work when available and useful. The parent
  still owns synthesis, source-of-truth updates, and final claims.
- Do not manually spawn separate coding-harness executables such as `codex`,
  `claude`, or `agent` for ordinary acceleration. Do not invoke skills whose
  main effect is to shell out to those binaries unless the user explicitly
  asks for that kind of delegation.
- Do not claim a plan item complete from logs or checkboxes alone. Read code
  anchors and confirm the outcome is true.

## First Move

1. Read `references/artifact-contract.md`.
2. Read `references/progressive-implementation-loop.md`.
3. Resolve the plan artifact, requested scope, stop boundary, repo root, audit
   log path, and implementation log path.
4. Read the plan, existing plan audit log if present, existing implementation
   log if present, local instructions, and current worktree state.
5. Identify the next narrow depth-first slice and the proof or review likely to
   matter.
6. If the scope is broad, decide whether native subagents can save real time
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
   Use native subagents for independent read-only lenses when that saves time.
6. Run, assign, or reuse proof based on impact and freshness. Do not rerun
   checks only because prior context was forgotten.
7. Update the owning artifact: plan for source-truth changes, audit log for
   `PLA-*` or `IMP-*` findings, implementation log for resumability.
8. Widen only after the prior slice's code state, plan state, review state, and
   proof state agree.
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
- `references/output-contract.md` - progress and final report contracts
- `references/examples.md` - examples and anti-examples
