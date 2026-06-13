# Child Prompt Contract

Use this for broad repo-backed audits that have multiple independent read-only
lenses or code areas. Native subagents or parallel-agent features provided by
the current coding harness are the preferred acceleration path and should be
treated as required whenever available.

Do not replace native subagents by manually spawning separate coding-harness
executables, or by invoking skills whose main effect is to shell out to
`codex`, `claude`, `agent`, or `grok`, unless the parent explicitly assigns
that action. Do not turn this into an external delegation workflow.

The parent owns synthesis and verdict. Children provide bounded evidence.

For `implementation-audit` children, use the implementation child contract
below instead of the plan-readiness contract.

## Common Child Contract

Every child prompt should include:

```text
You are doing one read-only plan-audit lens.

Work root: <repo/path or none>
Plan artifact: <path or pasted excerpt handle>
Audit lens: <lens name>

Read repo truth directly where relevant. Do not edit files. Do not invent
scope. Do not produce a second plan. Return only findings your lens owns. If
the plan is clean for your lens, say that plainly.

For every finding include:
- title
- required repair, observation, wrong, or out of scope
- problem
- why it matters
- plan evidence
- code evidence when repo-backed
- required plan repair
- coverage limits
```

When the runtime supports native subagents or parallel-agent features, add:

```text
Maximize parallelism with native subagents or parallel-agent features provided
by your current coding harness. Do not manually spawn separate coding-harness
executables, or invoke skills whose main effect is to shell out to `codex`,
`claude`, or `agent`, from inside this child prompt unless the parent explicitly
assigns that action.
```

## Code-Coverage Mapper

Use this child when the parent needs broad repo mapping.

Prompt focus:

- current and target owner paths
- public and representative internal callers
- legacy and side-door paths
- comparable existing patterns
- schemas, generated artifacts, fixtures, prompts, docs, examples, and tests
- relevant code still unknown

Expected output:

- code areas read
- files/symbols read
- why each area is relevant
- likely missing surfaces
- blockers caused by unread relevant code

## Implementation-Audit Child

Use this child for one read-only code review lens from
`implementation-audit-mode.md`.

Prompt:

```text
You are doing one read-only plan-audit implementation-audit lens.

Work root: <repo/path>
Plan artifact: <path>
Audit log: <path or none>
Requested scope: <full | through phase n | phase n | section>
Audit lens: <lens name>

Read repo code directly. Do not edit files. Do not fix code. Do not run tests.
Do not ask for test logs or command output. Do not produce a second plan. Do
not invent scope. Return only findings your lens owns. If the implementation
is clean for your lens, say that plainly.

For every finding include:
- title
- required repair, observation, wrong, or out of scope
- problem
- why it matters
- plan anchor
- code anchor
- required implementation repair
- coverage limits

Use native subagents or parallel-agent features provided by your current
coding harness when helpful. Do not manually spawn separate coding-harness
executables, or invoke skills whose main effect is to shell out to `codex`,
`claude`, or `agent`, unless the parent explicitly assigns that action.
```

The parent must spot-check code anchors, dedupe findings, classify required
repairs and observations, reject findings outside the requested scope, and own
the final verdict.

## Lens Reviewer

Use this child for one lens or a tight pair of lenses from `review-lenses.md`.

Prompt focus:

- inspect only the assigned lens
- cite exact evidence
- do not broaden into a whole-plan review
- do not recommend workflow changes unless the plan's own quality depends on
  them

Expected output:

- required repairs
- observations or out-of-scope follow-ups
- clean result if no finding
- coverage limits

## Ambiguity Reviewer

Use this child when the plan is likely to be misunderstood.

Prompt focus:

- find only ambiguity that changes the built outcome
- name plausible interpretations
- explain architecture, constraint, delete, proof, or phase-order impact
- identify whether repo truth resolves the ambiguity
- name the decision owner when apparent

Do not list fake ambiguity such as "should the code be good" or questions the
repo already answers.

## Elegance Reviewer

Use this child when the plan may be overbuilt.

Prompt focus:

- simpler owner path
- fewer live concepts
- existing pattern reuse
- deleted branches, wrappers, modes, shims, or side doors
- reduced caller burden
- drift-proof shared dependencies

The output should be a small set of stronger architecture moves, not a kitchen
sink of possible improvements.

## Parent Use Rules

- Use native subagents first for broad independent read-only audit slices.
- Do not use external harness-spawning skills for ordinary audit acceleration.
- Use `fresh-consult` or `agent-delegate` only when the user explicitly asks for
  external model or CLI execution, the parent assigns that action, and local
  instructions allow it.
- Use `agent-delegate` only for concrete read-only local command tasks with
  write scope `none`.
- Spot-check child evidence before presenting it as verified truth.
- Keep child transcripts out of the final answer unless they are short. Link
  or summarize artifacts instead.
