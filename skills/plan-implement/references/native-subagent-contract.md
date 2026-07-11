# Native Subagent Contract

Use this reference with `../../_shared/agent-orchestration-policy.md`. Prefer
same-host native children when they save real time and the active host can do
the job. This is different from manually spawning external coding-harness
binaries.

## Good Uses

Native subagents are useful for:

- broad code mapping
- side-door and legacy-path search
- comparable-pattern reading
- docs, prompts, examples, config, and generated-artifact drift checks
- changed tests reviewed as code
- one implementation-audit lens
- independent low-collision implementation slices when the host supports safe
  native parallel editing

Use them when distinct owned paths or review lenses make the saved serial work
worth the synthesis cost. Let coverage and implementation ownership determine
fanout, bounded by host slots, shared-file or shared-state collision risk, and
the parent's capacity to inspect every return.

## Bad Uses

Do not use native subagents when:

- the task is tiny
- scopes overlap heavily
- the plan scope is not resolved
- explaining the context would cost more than doing the work
- local instructions prohibit subagents
- shared scarce resources would be stampeded

## Parent Responsibilities

The parent agent must:

- capture repository status and the relevant diff before dispatch so later
  writes can be detected without assuming a clean worktree
- give each child one tight job with a non-overlapping lens or owned path
- state whether the subagent may edit or must stay read-only
- include plan path, active scope, implementation log path, and relevant code
  anchors
- include the frozen scope-contract anchor and state that the child cannot add
  adjacent scope
- require file and symbol anchors
- choose starting context explicitly; each new independent child starts clean,
  with Codex using `fork_turns: "none"` and Claude using a clean named or custom
  subagent rather than a bare conversation fork or skill `context: fork`
  shorthand
- use bounded or full inherited context only for a named dependency that
  exists solely in chat; durable plan and log paths should carry ordinary
  context instead of the parent's completion narrative
- select the strongest read-only capability or sandbox available for mapping
  and review children, in addition to their explicit no-edit prompt
- prohibit children from creating children or invoking delegation, consult, or
  review skills unless the brief assigns a nested scope and budget
- account for every child final state, dedupe and spot-check findings, resolve
  conflicts, and compare repository status and diffs with the pre-dispatch
  state before accepting read-only evidence
- reject out-of-scope findings
- update the implementation log and audit log
- keep final completion claims owned by the parent
- preserve the exact implementer handle when continuation is intended, resume
  that implementer for accepted repairs in its owned scope, and launch every
  independent recheck as a new clean critic

## External Harness Boundary

Do not manually spawn separate coding-harness executables such as `codex`,
`claude`, or `agent` for ordinary acceleration.

Do not invoke skills whose main effect is to shell out to those binaries for
ordinary same-host acceleration. An explicitly requested external worker or
conductor remains a valid route when its provider, model, lifecycle, isolation,
automation, or receipt benefit is worth the added process and integration cost.

Use `plan-conductor` when the user wants plan-wide delegated external workers.
Use `agent-delegate` when the user wants one explicit external worker. Resolve
either handoff under the shared policy rather than treating external execution
as forbidden.

## Prompt: Code Map Subagent

```text
You are helping implement this plan faster by mapping one code surface.

Plan: <path>
Implementation log: <path or none>
Active scope: <phase/section/checklist item>
Surface: <owner path | callers | side doors | docs/prompts | tests as code>

Read code directly. This mapping slice is read-only: do not edit or write
files. Do not create child agents or invoke delegation, consult, or review
skills unless the parent brief explicitly assigns a nested scope and budget.
Return:
- files/symbols read
- current owner path
- likely side doors or duplicate truth
- comparable patterns
- what should be reread if it changes
- blockers or surprises
```

## Prompt: Continuous Review Subagent

```text
You are doing one read-only plan-backed implementation review while work is in
progress.

Plan: <path>
Audit log: <path or none>
Implementation log: <path or none>
Scope: <phase/section/slice>
Lens: <plan-audit implementation-audit lens>

Read the current code directly. Do not edit or write files. Do not run tests.
Do not ask for logs. Do not create child agents or invoke delegation, consult,
or review skills unless the parent brief explicitly assigns a nested scope and
budget. Return only findings for this lens:
- title
- required repair, observation, wrong, or out of scope
- problem
- plan anchor
- code anchor
- required repair
- scope disposition: authorized | frozen-convergence-required | new-scope-needs-human | out-of-scope | unauthorized-built-scope
- coverage limits

If clean for this lens, say so plainly.
```

## Prompt: Proof Freshness Subagent

```text
You are checking proof freshness, not rerunning proof.

Plan: <path>
Implementation log: <path>
Changed files: <paths>
Prior proof entries: <entries>

Read code only as needed. Do not run tests. Return:
- which prior proof remains fresh
- which proof is stale and why
- smallest high-value proof to run next
- proof that would be low-value or duplicate

Do not edit or write files. Do not create child agents or invoke delegation,
consult, or review skills unless the parent brief explicitly assigns a nested
scope and budget.
```
