# Output Contract

Every review saves a disk artifact under:

```text
/tmp/exhaustive-code-review/<scope-slug>-<timestamp>/
```

The artifact must be readable without chat history. It should contain these
files:

```text
target.md
coverage.md
findings.md
verdict.md
```

Do not add a runner state file, machine protocol, generated schema, or workflow
ledger. These are review notes for a human and future agent to inspect.

## `target.md`

Record:

- review target in the user's words
- resolved scope: worktree, branch diff, commit range, explicit paths,
  plan-scope, or completion claim
- baseline and head/current state when known
- local instruction and convention files read
- important exclusions or unresolved target ambiguity

## `coverage.md`

Record what was reviewed:

- touched files
- changed hunks
- touched symbols
- touched abstractions and canonical owners
- relevant callers, readers, writers, side doors, old paths, duplicate helpers,
  alternate command/API paths, and adjacent same-contract surfaces
- behavior or feature surfaces
- tests, fixtures, proof, docs, examples, comments, schemas, generated
  artifacts, prompts, config, telemetry, stable IDs, install surfaces, and
  package metadata when relevant
- native parallel agent usage summary
- known coverage gaps

Keep this as prose and compact lists. It is not a formal checklist engine.

## `findings.md`

Use this shape for each finding:

```markdown
### [REQUIRED REPAIR|OBSERVATION] <short title>

- File: <repo-relative path>
- Symbol / line: <symbol or line>
- Risk: <concrete risk in plain language>
- Evidence: <diff, file, child report, command output, source anchor, or "see file">
- Scope disposition: <authorized | frozen-convergence-required | new-scope-needs-human | out-of-scope | unauthorized-built-scope | not applicable>
- Repair target: <what must change, without writing the patch>
- Review pattern: <catalog pattern>
```

Rules:

- Findings must be tied to changed code or the requested review scope.
- Findings must cite evidence the reviewer actually read.
- Any in-scope competing path, duplicate owner, side door, stale truth surface,
  proof gap, or changed-code risk that must change before approval is a
  `REQUIRED REPAIR`.
- For a fixed-scope plan or history-backed change, a reviewer-discovered
  adjacent path is `new-scope-needs-human`, not an instruction to implement
  that path. If it prevents approval, target subtraction or redesign inside the
  frozen boundary, or name the human scope decision required. Repeated review
  agreement does not change the disposition.
- Unauthorized built scope is a `REQUIRED REPAIR` whose default target is
  subtraction, even when later code, tests, or plan text depends on it.
- `OBSERVATION` is only for true informational facts, genuinely different
  contracts, or work excluded by the controlling request or artifact.
- Do not include suggested patch blocks.
- Do not include generic style advice.
- Empty findings are valid.

## `verdict.md`

Use one verdict:

- `approve`: exhaustive review completed, coverage is honest, and no required
  repairs remain in the requested scope
- `not-approved`: one or more required repairs exist in the requested scope
- `coverage-incomplete`: the review could not honestly cover the requested
  scope

Use this shape:

```markdown
# Exhaustive Code Review Verdict

VERDICT: approve | not-approved | coverage-incomplete

## Required Repairs

<findings or "No required repairs.">

## Observations

<observations or "No observations.">

## Coverage Summary

- Scope reviewed:
- Native parallel agents:
- Files/hunks/abstractions covered:
- Competing paths, side doors, and adjacent surfaces:
- Proof/docs/generated/prompt surfaces:
- Coverage gaps:

## Next Action

<one exact repair, rerun, or coverage action>
```

## Chat Reply

After saving the artifact, reply briefly:

- verdict
- required repairs, if any
- notable observations, if material
- artifact path
- one next action from the review

Do not prescribe the user's broader workflow.
