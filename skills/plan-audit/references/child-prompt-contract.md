# Child Prompt Contract

Use this only when the audit is large enough to justify read-only child
reviewers, and only when the user ask and local instructions allow child-agent
use. Do not turn this into a required delegation workflow.

The parent owns synthesis and verdict. Children provide bounded evidence.

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
- blocking or non-blocking
- problem
- why it matters
- plan evidence
- code evidence when repo-backed
- required plan repair
- coverage limits
```

When the runtime supports native parallel agents, add:

```text
Maximize parallelism by using parallel agents. Do not invoke skills that spawn
subagents.
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

## Lens Reviewer

Use this child for one lens or a tight pair of lenses from `review-lenses.md`.

Prompt focus:

- inspect only the assigned lens
- cite exact evidence
- do not broaden into a whole-plan review
- do not recommend workflow changes unless the plan's own quality depends on
  them

Expected output:

- blocking findings
- non-blocking findings
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

- Use `fresh-consult` for cold read-only model opinions when that skill is
  available and allowed.
- Use `agent-delegate` only for concrete read-only local command tasks with
  write scope `none`.
- Do not use child agents if local instructions prohibit delegation without
  explicit user permission.
- Spot-check child evidence before presenting it as verified truth.
- Keep child transcripts out of the final answer unless they are short. Link
  or summarize artifacts instead.
