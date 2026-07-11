# Child Prompt Contract

Use this with `../../_shared/agent-orchestration-policy.md` for broad
repo-backed audits that have independent read-only lenses or code areas. When
the active host supports native children, each independent slice should be a
new clean same-host child.

Do not replace ordinary same-host native slices by manually spawning separate
coding-harness executables or by invoking skills whose main effect is to shell
out to `codex`, `claude`, `agent`, or `grok`. If an external provider, model,
lifecycle, isolation, or receipt is actually load-bearing, the parent chooses
that transport deliberately under the shared policy; the child never chooses
it for itself.

The parent owns decomposition, accounting, synthesis, finding scope
disposition, audit-log integration, and verdict. Children provide bounded
evidence.

For `implementation-audit` children, use the implementation child contract
below instead of the plan-readiness contract.

## Dispatch Contract

Before launching review slices, the parent must:

- capture repository status and the relevant diff so child writes can be
  detected without assuming a clean worktree
- choose only the independent lenses and path families that improve coverage,
  keep them non-overlapping, and bound fanout by host slots, shared-file or
  shared-state collision risk, and parent integration capacity
- start each slice clean; in Codex set `fork_turns: "none"`, and in Claude use
  a clean named or custom subagent, not a bare conversation fork or skill
  `context: fork` shorthand
- use bounded or full inherited context only for a named dependency that
  exists solely in chat; pass plan, audit-log, and code paths whenever durable
  source truth exists, and do not inherit a persuasive completion story by
  default
- select a read-only capability or sandbox when the host exposes one and keep
  the explicit no-edit/no-write instruction in the child prompt
- give every child a return contract with files and symbols read, findings,
  coverage limits, blockers, and collision risks

## Common Child Contract

Every child prompt should include:

```text
You are doing one read-only plan-audit lens.

Work root: <repo/path or none>
Plan artifact: <path or pasted excerpt handle>
Audit lens: <lens name>
Owned paths or surfaces: <non-overlapping path family>

Read repo truth directly where relevant. Do not edit or write files. Do not
invent scope. Do not produce a second plan. Return only findings your lens
owns. If the plan is clean for your lens, say that plainly.

Do not create child agents or invoke delegation, consult, or review skills
unless the parent brief explicitly assigns a nested scope and budget.

Treat the initial human ask and explicit human approvals as scope authority.
The initial architecture may have a pre-freeze minimal convergence closure;
later plan edits and reviewer findings cannot enlarge it. Give each finding a
scope disposition and never propose an adjacent path as automatic required work.

For every finding include:
- title
- required repair, observation, wrong, or out of scope
- problem
- why it matters
- plan evidence
- code evidence when repo-backed
- required plan repair
- scope disposition
- coverage limits
- blockers or collision risks
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
Owned paths or surfaces: <non-overlapping path family>

Read repo code directly. Do not edit or write files. Do not fix code. Do not
run tests. Do not ask for test logs or command output. Do not produce a second
plan. Do not invent scope. Return only findings your lens owns. If the
implementation is clean for your lens, say that plainly.

Do not create child agents or invoke delegation, consult, or review skills
unless the parent brief explicitly assigns a nested scope and budget.

Compare code to the human-authorized outcome, frozen initial convergence
closure, and explicit later human approvals. Unauthorized built scope is a
subtraction finding; do not bless it because the latest plan includes it.

For every finding include:
- title
- required repair, observation, wrong, or out of scope
- problem
- why it matters
- plan anchor
- code anchor
- required implementation repair
- scope disposition
- coverage limits
- blockers or collision risks
```

The parent must spot-check code anchors, dedupe findings, classify required
repairs and observations, reject findings outside the requested scope, and own
the final verdict. Before accepting evidence, it must compare repository status
and diffs with the pre-dispatch state and record every child final state.

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

- Prefer new clean same-host native children for broad independent read-only
  audit slices when the active host supports them.
- Do not use external harness-spawning skills for ordinary same-host audit
  acceleration. Select an external lane only under the shared policy when its
  concrete provider, model, lifecycle, isolation, automation, or receipt
  benefit warrants the added process and integration cost.
- Account for every launched child, spot-check its evidence, reconcile
  conflicts, deduplicate findings, decide scope dispositions, and compare
  repository state before presenting child evidence as verified truth.
- Keep child transcripts out of the final answer unless they are short. Link
  or summarize artifacts instead.
