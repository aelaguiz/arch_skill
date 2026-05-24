# Native Subagent Contract

Use native subagents or parallel-agent features provided by the current coding
harness when they save real time. This is different from manually spawning
external coding-harness binaries.

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

Use them when the work is large enough that parallel reading or review beats
the synthesis cost.

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

- give each subagent one tight job
- state whether the subagent may edit or must stay read-only
- include plan path, active scope, implementation log path, and relevant code
  anchors
- require file and symbol anchors
- dedupe and spot-check findings
- reject out-of-scope findings
- update the implementation log and audit log
- keep final completion claims owned by the parent

## External Harness Boundary

Do not manually spawn separate coding-harness executables such as `codex`,
`claude`, or `agent` for ordinary acceleration.

Do not invoke skills whose main effect is to shell out to those binaries unless
the user explicitly asks for external delegation or local instructions require
that path.

Use `plan-swarm` when the user wants delegated external worker swarms. Use
`agent-delegate` when the user wants one explicit external worker.

## Prompt: Code Map Subagent

```text
You are helping implement this plan faster by mapping one code surface.

Plan: <path>
Implementation log: <path or none>
Active scope: <phase/section/checklist item>
Surface: <owner path | callers | side doors | docs/prompts | tests as code>

Read code directly. Do not edit files unless explicitly assigned. Return:
- files/symbols read
- current owner path
- likely side doors or duplicate truth
- comparable patterns
- what should be reread if it changes
- blockers or surprises

Use native parallel-agent features if helpful. Do not manually spawn separate
coding-harness executables.
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

Read the current code directly. Do not edit files. Do not run tests. Do not ask
for logs. Return only findings for this lens:
- title
- blocking or non-blocking
- problem
- plan anchor
- code anchor
- required repair
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
```
