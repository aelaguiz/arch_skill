# Proper-Audit Checklist

Use this before calling a plan ready. This is a judgment checklist, not a
checklist executor or deterministic readiness gate.

For `implementation-audit` mode, use the proper implementation-audit checklist
in `implementation-audit-mode.md`. That mode is code review against a plan: it
does not run tests, ask for logs, verify CI, or investigate whether a
completion claim is truthful.

## Artifact Setup

- The plan artifact is resolved.
- The reviewed scope is explicit.
- Local instructions and repo verification rules were read when repo-backed.
- Existing audit log entries were read before a repeat audit.
- A file-backed non-trivial audit has an audit log path.
- The final output names what was not checked, if anything.

## Outcome Contract

- The North Star outcome is identified or marked missing.
- Done-state requirements are identified or marked missing.
- Requirements are separated from tasks.
- Non-requirements are identified or marked missing.
- Hard constraints are identified and evidence-checked.
- Non-constraints are identified where they remove fake complexity.
- Assumptions and beliefs creating complexity are named.
- Code-quality requirements around complexity, abstraction, deletion,
  centralization, drift-proofing, and proof are checked.

## Ambiguity

- Real outcome-changing ambiguity is listed.
- Plausible interpretations are named.
- Architecture impact is explained.
- Repo truth was checked before asking the user.
- Fake ambiguity was ignored.
- Required decisions are stated in the smallest possible set.

## Relevant-Code Coverage

For repo-backed plans:

- Every file and symbol named by the plan was read.
- The current canonical owner path was read.
- The proposed target owner path was read.
- Public caller families were read.
- Representative internal call sites were read.
- Adjacent same-contract or same-behavior paths were searched and read when
  they could keep the system split between old and new behavior.
- Legacy paths, old APIs, fallbacks, flags, scripts, commands, jobs, UI
  affordances, prompts, or generated artifacts that can preserve old behavior
  were searched and read when found.
- Comparable existing patterns were searched and read.
- Persistence, schema, config, fixture, adapter, and generated contract
  surfaces were read when relevant.
- Existing tests, integration tests, manual proof surfaces, and low-value test
  risks were read.
- Touched docs, examples, comments, prompts, and instructions were read when
  they can affect behavior or future routing.
- Unknown relevant-code areas are named explicitly.
- The plan is not approved while relevant-code coverage is unknown.

## Native Subagent Read Quality

- Native subagents or parallel-agent features were used for broad independent
  audit slices when available.
- If native subagents were not used, the audit records the reason: unavailable,
  prohibited by local instructions, or too small to split.
- Native subagents, when used, had non-overlapping scopes.
- Child reports included exact files, symbols, and evidence.
- Parent synthesis spot-checked child evidence.
- Child output did not become the verdict by itself.
- External harness-spawning skills were not used for ordinary acceleration.
- Any external child-agent or delegation skill use was explicitly assigned and
  allowed by local instructions.

## Architecture Quality

- The canonical owner path is named.
- Duplicate truth and parallel implementation paths are identified.
- Existing patterns are inventoried before a new one is approved.
- Related live code is classified as move now, delete now, leave different,
  named follow-up, or user decision, including adjacent surfaces that expose
  the same contract or behavior.
- Caller API shape is checked for misuse resistance.
- Invariants are named and located in code or target code shape.
- State model and partial-state risks are checked.
- Drift-proof coupling is checked across shared dependencies.
- Abstractions are checked for real complexity reduction.
- Layer boundaries and refactor radius are checked.
- Live concept count is checked.
- Legacy paths and side doors are checked for deletion or closure.

## Implementation-Risk Quality

- The plan is depth-first or has a real reason it cannot be.
- The first slice proves a narrow integrated path.
- The highest-risk seam is crossed early.
- Each later expansion has a proof gate before widening.
- Bells, optional modes, and polish are deferred until the core path works.
- Integration proof is required where integration is the real risk.
- Low-value unit-only or mock-only proof is rejected where it would miss actual
  bugs.

## Finding Quality

- Every blocking finding includes consequence, evidence, and required plan
  repair.
- Evidence cites plan and code anchors where possible.
- Findings are deduped across lenses.
- Non-blocking findings are separated from blockers.
- Wrong, resolved, accepted-risk, or out-of-scope findings are labeled with a
  reason.
- The final verdict is not softer than the worst unresolved blocker.

## Loop Readiness

- The audit log current checklist was updated when applicable.
- Stable finding IDs were used.
- Resolved findings were checked off only with evidence.
- Unresolved findings were carried forward.
- Relevant-code coverage was updated.
- The next audit focus is named.
- The final response points to the audit log path when applicable.

## Reconciliation Gate

- Every real ambiguity question has a decision owner.
- Every real constraint or non-constraint question has a decision owner.
- User-owned decisions were answered by the user.
- Agent-owned decisions were made only with explicit permission and enough repo
  evidence.
- Each resolved decision is written back into the plan.
- Plan carry-through was checked across requirements, constraints, target
  architecture, phase order, delete list, compatibility posture, and proof
  strategy.
- No ambiguity or constraint item is marked resolved solely because it was
  discussed in chat or listed in the audit log.
- The plan is not marked ready while any outcome-changing decision remains open
  or uncaptured in the plan.
