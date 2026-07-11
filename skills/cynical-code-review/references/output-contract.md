# Output Contract

Every review saves a disk artifact under:

```text
/tmp/cynical-code-review/<scope-slug>-<timestamp>/
```

Use a repo doc path only when the user explicitly asks for one.

The artifact must be readable without chat history. It should contain:

```text
target.md
suspicion-map.md
coverage.md
findings.md
verdict.md
```

Do not add a runner state file, machine protocol, generated schema, workflow
ledger, scorecard, harness output, or checklist executor. These are review
notes for a human and future agent to inspect.

## `target.md`

Record:

- review target in the user's words
- resolved scope: worktree, branch diff, commit range, explicit paths, plan
  scope, or completion claim
- baseline and head/current state when known
- controlling plan, source truth, completion claim, or worklog if supplied
- initial human scope, frozen convergence closure, freeze anchor, later human
  approvals, and review-wave history when recoverable
- local instruction and convention files read
- important exclusions or unresolved target ambiguity

## `suspicion-map.md`

Record the starting theory of how the implementation might be lying:

- implementation story or completion claim
- what code behavior would have to exist for the claim to be true
- source of truth, if any
- proxy evidence that must not be treated as proof
- old authority paths to check
- duplicate truth and split-brain risks
- side doors and adjacent same-contract surfaces
- user job and starting state
- proof/status/doc/test surfaces that may mislead
- environment or target binding facts when relevant
- scope-cycle suspicion and disputed work provenance when applicable

Keep this as a review map, not a second plan.

## `coverage.md`

Record what was reviewed:

- touched files
- changed hunks
- touched symbols
- touched abstractions and canonical owners
- actual control-flow and data-flow paths traced
- old paths, side doors, duplicate helpers, alternate command/API paths,
  fallback readers/writers, generated artifacts, and adjacent same-contract
  surfaces
- behavior or feature surfaces, including the user's starting state when
  relevant
- tests, fixtures, docs, examples, comments, schemas, generated artifacts,
  prompts, config, telemetry, stable IDs, install surfaces, package metadata,
  logs, and status surfaces only where they claim code truth
- native parallel agent usage summary and final state for each launched slice
- known coverage gaps
- scope-provenance coverage or `not applicable`

Keep this as prose and compact lists. It is not a formal checklist engine.

## `findings.md`

Use this shape for each finding:

```markdown
### [REQUIRED REPAIR|OBSERVATION] <short title>

- File: <repo-relative path>
- Symbol / line: <symbol or line>
- Claim being tested: <completion story, plan obligation, or implementation claim>
- Risk: <concrete current-code risk in plain language>
- Evidence: <diff, file, flow, child report, command output, source anchor, or "see file">
- Repair target: <what must change, without writing the patch>
- Cynical review pattern: <catalog pattern>
- Scope provenance: <human anchor | frozen closure anchor | later human approval | missing>
- Scope-cycle evidence: <revision/wave/code chain or none>
- Required disposition: <subtract | human decision | no scope issue>
```

Rules:

- Findings must be tied to current code or the requested review scope.
- Findings must cite evidence the reviewer actually read.
- Any in-scope false completion, old authority path, duplicate truth, side
  door, partial migration, stopped-short user job, fake proof, or scope drift
  that must change before approval is a `REQUIRED REPAIR`.
- Unauthorized post-freeze built scope or scope cycling is always a `REQUIRED
  REPAIR` and forces `not-approved`, even when the latest plan includes it.
- `OBSERVATION` is only for true informational facts, genuinely different
  contracts, excluded follow-ups, or proof/status/doc issues that do not hide a
  current-code gap.
- Do not include suggested patch blocks.
- Do not include generic style advice.
- Do not include missing-test or doc-hygiene findings unless they mask or
  contradict current code reality.
- Empty findings are valid.

## `verdict.md`

Use one verdict:

- `approve`: cynical review completed, suspicion lanes were honestly covered,
  and no required repairs remain in the requested scope
- `not-approved`: one or more required repairs exist in the requested scope
- `coverage-incomplete`: the review could not honestly inspect the code needed
  to test the implementation story

Use this shape:

```markdown
# Cynical Code Review Verdict

VERDICT: approve | not-approved | coverage-incomplete

## Required Repairs

<findings or "No required repairs.">

## Observations

<observations or "No observations.">

## Suspicion Summary

- Claim reviewed:
- Biggest false-completion risks checked:
- Old authority paths:
- Duplicate truth / side doors:
- User job from starting state:
- Proof/doc/status surfaces:
- Target/environment binding:

## Scope Provenance

- Initial human-authorized scope:
- Frozen initial convergence closure and freeze anchor:
- Later human approvals:
- Scope-cycle evidence:
- Required disposition:

## Coverage Summary

- Scope reviewed:
- Native parallel agents:
- Files/hunks/abstractions covered:
- Code paths traced:
- Competing paths, side doors, and adjacent surfaces:
- Proof/docs/generated/prompt/status surfaces:
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
