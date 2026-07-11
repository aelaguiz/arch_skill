# Implementation Audit Mode

Use this reference when `plan-audit` is asked to review code that was written
from a plan. This is plan-backed code review, not generic diff review and not
runtime verification.

## Job

Review implemented or claimed-implemented code against the current plan and
the shared `plan-audit` architecture canon.

The question is:

```text
Does this code match the plan's intended architecture and quality bar without
adding duplicate truth, side doors, drift, bad caller shape, or unnecessary
complexity?
```

A second core question is:

```text
Did the implementation make the intended outcome true, or did it only make the
names, wrappers, checkboxes, and phase labels look right?
```

The mode may review:

- the full plan
- all code through a named phase
- one named phase
- one named plan section when the plan format supports it

## Non-Goals

Do not:

- run unit tests, integration tests, build commands, lint commands, or CI
- ask for test logs or command output
- verify whether tests really ran
- investigate whether a completion claim is truthful
- search history looking for hidden intent
- turn the audit into a generic diff or PR review
- manually spawn separate coding-harness executables such as `codex`,
  `claude`, or `agent` for ordinary acceleration
- edit code
- silently rewrite the plan
- create a second implementation plan

If the user, CI surface, or surrounding workflow says tests passed, accept that
as context and keep reviewing code. If no test-pass context exists, still do
not run tests or demand logs.

Changed test files may be read as code when relevant. Review them only for
code review issues such as duplicate business rules, fake contracts,
test-only production paths, misleading fixtures, or drift-prone helpers.

## Inputs

Read:

- the plan artifact in its native format
- the existing `<PLAN_STEM>_PLAN_AUDIT.md`, when present
- the requested review scope
- current worktree state, diff, commit range, branch diff, or changed files
- worklogs, checked boxes, phase labels, or summaries only as scope context
- local instructions and repo code conventions
- current code, generated artifacts, schemas, config, commands, routes,
  prompts, fixtures, docs, examples, and install surfaces that govern the
  behavior

Do not treat scope context as a lie to investigate or a claim to re-validate.
It helps aim the code review; it does not replace reading code.

When the plan, worklog, Decision Log, branch context, or user ask exposes scope
history, reconstruct the human baseline, initial pre-freeze convergence
closure, freeze anchor, and explicit human approvals. This is provenance review,
not an honesty investigation. If required provenance cannot be recovered,
return the existing non-approving coverage verdict instead of inventing it.

## Progressive Review Order

1. Resolve the plan artifact, code root, audit log path, and requested scope.
2. Read the existing audit log before reviewing.
3. Read the plan as written and extract the North Star, done-state
   requirements, requirements, non-requirements, constraints, non-constraints,
   phase boundaries, checklists, exit criteria, delete list, compatibility
   posture, and side-door expectations.
   Also extract human authorization anchors, initial convergence closure,
   scope-freeze anchor, and explicit later human approvals.
4. Reconstruct what code should be reviewed from user text, phase labels,
   worklog notes, checked boxes, commit messages, branch names, or explicit
   paths.
5. Build a changed-behavior map: changed files and symbols, new files, deleted
   files, generated artifacts, migrations, config, prompt or instruction
   changes, changed test files, docs, examples, commands, routes, APIs, UI
   paths, jobs, scripts, or package surfaces.
6. Build the relevant-code map beyond the diff: owner paths, public and
   representative callers, legacy paths, side doors, comparable patterns,
   adjacent same-contract or same-behavior paths, schemas, adapters, generated
   artifacts, fixtures, config, prompts, docs, changed test files, and install
   or command surfaces.
7. For broad independent code lenses, follow `child-prompt-contract.md` and the
   shared agent policy. When the active host supports native children, start
   each slice as a new clean read-only child over a non-overlapping lens or path
   family; the parent owns accounting, repository-state checks, synthesis,
   finding disposition, and verdict.
8. Review plan obligations against code. Classify each due obligation as
   `satisfied by code`, `missing code`, `implemented differently but
   equivalent`, `implemented differently and not equivalent`, `scope cut`, or
   `unclear from code`.
9. Compare apparent completion against real behavior for any planned
   simplification, unification, migration, deletion, or SSOT convergence.
10. Run the implementation lenses below.
11. Update the shared audit log when applicable.
12. Return the code review verdict using `output-contract.md`.

## Implementation Lenses

### `scope-and-baseline`

Check that the review target is clear: plan path, audit log path, scope,
baseline, and local instructions. Block only when the code target cannot be
resolved or required code cannot be read.

### `scope-provenance-and-no-cycling`

For plan-backed work with recoverable scope history, compare the initial human
scope and pre-freeze convergence closure with plan revisions, findings,
worklogs, and final code. A later plan edit cannot retroactively authorize code.
Treat unauthorized built scope as a required `IMP-*` subtraction repair and
force `not-approved`, even if it works or tests pass. A new adjacent path found
by this audit may block approval but cannot be added to repair scope without a
human decision and re-freeze.

### `plan-code-fit`

Check whether the current code fits the current plan contract: requirements,
cleanup promises, delete promises, exit criteria that describe code states,
and behavior-preservation expectations visible in code shape.

Do not investigate intent. If current plan and current code do not line up,
report the code review issue plainly.

### `outcome-realization`

Check whether the code shape supports the plan's North Star outcome. Block
when task checkboxes can be satisfied while the intended architecture or
behavior remains false.

### `intent-vs-reality`

Check whether the implementation made the plan's intended simplification,
unification, migration, deletion, or behavior change true in the running code
shape. Review names, wrappers, new owner labels, phase status, tests, docs, and
prompts as claims, not proof. Follow actual control flow, data flow, caller
paths, and old entrypoints.

Block when the work is implemented in name but not in fact: the old behavior is
still reachable, the new canonical owner does not actually own the invariant,
two truths remain live, a wrapper adds a concept without deleting complexity, a
"unified" path only covers the happy path, or tests/docs prove the new label
instead of the intended behavior. Do not investigate honesty, history, or
private intent; judge the current plan and code evidence.

### `requirement-traceability`

Trace every due requirement, done-state truth, checklist item, exit criterion,
and sub-obligation to code. Block orphan obligations.

### `phase-frontier-review`

For full or through-phase scopes, review the whole ordered frontier. Do not
report one local gap while ignoring later code obligations in scope. For one
phase, include prerequisites and plan-wide contracts touched by the phase.

Missing unit-test output, CI logs, screenshots, or manual validation are out of
scope for blocker decisions.

### `code-and-diff-map`

Compare actual changed behavior to plan expectations. The review unit is the
changed subsystem and affected call sites, not one isolated file.
Include adjacent unchanged paths when they expose the same contract or behavior
through another owner, route, command, schema, prompt, fixture, or generated
artifact.

### `canonical-owner-and-ssot`

Check whether the code converged onto the planned or best canonical owner.
Treat duplicate writers, duplicate readers where one owner should exist, shadow
contracts, wrong-layer logic, direct mutation paths around the owner, or old and
new APIs both live without an approved bridge as required repairs.

### `existing-pattern-fit`

Check whether the implementation followed the best local pattern or justified
divergence. Related code should be migrated now, deleted now, left different
for a real reason, named as follow-up, or marked unresolved. This includes
adjacent same-contract or same-behavior surfaces, not only files touched by the
diff.

### `deletion-and-side-door-closure`

Search for old behavior still reachable through old files, commands, routes,
scripts, jobs, UI affordances, prompts, generated artifacts, fixtures,
examples, docs, compatibility flags, fallback readers or writers, or direct
calls into old APIs. If the plan said delete, the implementation should delete.

### `drift-proof-coupling`

Check whether coupled components can silently diverge: schemas, generated
artifacts, fixtures, adapters, prompts, docs, changed tests, runtime config,
shared constants, validation rules, and API contracts. Prefer one source of
truth, one adapter boundary, shared contracts, or fail-loud validation.

### `caller-invariant-state`

Review from the caller side. Correct usage should be obvious, invalid usage
hard, and callers should not need internal lifecycle knowledge, magic flags, or
partial states that allow impossible combinations.

### `elegance-and-code-judo`

Search for the simpler code shape that deletes concepts. Block fake
abstractions, wrappers, branches, or custom mechanisms that add burden without
removing larger complexity.

### `tiny-team-maintainability`

Check whether a tiny team can own the code: self-documenting names, direct
control flow, one obvious debug path, existing patterns, proven libraries for
solved problems, and no speculative framework or plugin layer.

### `tests-as-code`

Review changed tests only as code. Look for fake contracts, test-only
production paths, hidden duplicate rules, misleading fixtures, or helpers that
hide real behavior. Do not run tests or ask for logs.

### `docs-contract-drift`

Required when implementation changes behavior, commands, install surfaces,
APIs, examples, prompts, telemetry, stable IDs, user-facing contracts, or
instructions. Flag touched or routing-relevant surfaces that now teach the
wrong path.

### `agent-capability`

Required when implementation touches skills, agents, prompts, MCP, model
behavior, or instruction-bearing surfaces. Check that prompt/native capability
got first right of refusal, scripts remain narrow deterministic helpers, and
the implementation did not replace model judgment with unjustified scaffolding.

### `security-boundary`

Required only when changed code touches auth, permissions, secrets, input
validation, deserialization, command execution, file/process/network access,
privacy, or dependency trust. Find only reachable changed-code risks.

### `scope-creep-and-non-requirements`

Check whether implementation added variants, modes, frameworks, compatibility
behavior, or product scope that the plan did not require and that now creates
bug vectors, live concepts, drift surfaces, or maintenance burden.

Give every material finding a shared scope disposition. Only `authorized` and
`frozen-convergence-required` are automatic repair work; `new-scope-needs-human`
is a decision request, and `unauthorized-built-scope` is subtraction work.

## Audit Log Updates

Use the same audit log as plan-readiness audits:

```text
<PLAN_STEM>_PLAN_AUDIT.md
```

Add implementation findings as `IMP-*` entries. Keep plan-readiness findings
as `PLA-*`. Link related IDs instead of duplicating the same issue.

For implementation-audit passes, record:

- Mode: `implementation-audit`
- Scope
- Baseline reviewed
- Test/CI context accepted, if supplied
- Review-child accounting, including context choice and final state
- Pre/post-dispatch repository-state check
- Code areas read
- Obligations checked
- Findings added
- Findings resolved
- Verdict
- Next audit focus

The audit log is a review ledger. It must not become a second implementation
plan, a proof ledger, or a workflow controller.

## Output

Use these verdicts:

- `approve`: no required code review repairs remain in the requested scope
- `not-approved`: required code review repairs exist in the requested scope
- `scope-inconclusive`: the review target cannot be resolved or required code
  surfaces cannot be read

Every required repair must include:

- problem
- why it blocks code review approval
- plan anchor
- code anchor
- required implementation repair
- review lens

Do not include placeholder sections. Do not invent findings because the mode
was invoked. Do not use a middle approval state: if a required repair remains,
the verdict is `not-approved`.

## Proper Implementation-Audit Checklist

Before returning an approval verdict, confirm:

- Plan artifact, requested scope, audit log, local instructions, and baseline
  are resolved.
- Test/CI pass claims were accepted as context when supplied, without rerunning
  or proving them.
- North Star, done-state requirements, phase boundaries, checklists, exit
  criteria, delete list, and side-door expectations were extracted.
- Changed code and relevant unchanged code were read.
- Broad independent read-only slices, when useful, used new clean native
  children under the shared policy; every launched child was accounted for and
  the repository-state check was recorded.
- Every due code obligation was traced to code or a missing/unclear status.
- Name-only completion and false simplification were checked wherever the plan
  promised simplification, unification, migration, deletion, SSOT convergence,
  or behavior change.
- Adjacent same-contract or same-behavior paths were reviewed for split old/new
  behavior where they were in or affected by the requested scope.
- Required deletes, caller migrations, side-door closures, and drift-prone
  contracts were reviewed.
- No unit tests, integration tests, build commands, lint commands, or CI
  commands were run.
- No test logs were requested.
- Changed tests were reviewed only as code, if relevant.
- Required repairs include plan anchors, code anchors, consequence, and
  required repair.
