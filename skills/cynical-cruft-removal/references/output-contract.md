# Output Contract

Every review saves a disk artifact under:

```text
/tmp/cynical-cruft-removal/<scope-slug>-<timestamp>/
```

Use a repo doc path only when the user explicitly asks for one.

The artifact must be readable without chat history. It should contain:

```text
target.md
live-root-map.md
purpose-map.md
reference-graph-notes.md
low-value-catalog.md
test-bloat-report.md
deletion-candidates.md
keep-decisions.md
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
- resolved scope: current repo, worktree, branch diff, commit range, explicit
  paths, subsystem, test suite, dependency set, generated artifact set,
  docs/examples/prompt surface, or user-named suspicious area
- baseline and head/current state when known
- controlling plan, source truth, cleanup claim, or worklog if supplied
- explicit exclusions
- local instruction and convention files read
- unresolved target ambiguity

## `live-root-map.md`

Record current roots that can prove value:

- product/user workflows
- runtime entrypoints
- public APIs and package exports
- plugin hooks and integration contracts
- build, install, deploy, release, and migration paths
- supported CLI commands and scripts
- security, safety, compliance, data-retention, and compatibility obligations
- tests that protect current behavior
- docs, examples, and prompts that a current reader genuinely needs
- generated artifacts consumed by live roots

If a likely root is missing or uninspectable, say so. Do not silently treat
unknown roots as evidence of absence.

## `purpose-map.md`

Record:

- artifact or cluster
- claimed purpose
- actual current purpose
- live root proving purpose, if any
- suspicious keep reason
- current owner, if found
- current keep/delete leaning

Keep this as a review map, not a second plan.

## `reference-graph-notes.md`

Record references that may prove or fake liveness:

- code references
- test references
- docs, examples, and prompt references
- generated references
- config, build, package, and script references
- asset, CSS, locale, route, template, and telemetry references
- data/schema references when relevant
- self-referential islands
- references rejected as weak proof

For important candidates, state whether the reference comes from a live root or
from another suspect artifact.

## `low-value-catalog.md`

Group suspicious artifacts by type:

- dead code
- low-value live code
- tests
- docs/examples/prompts
- generated artifacts
- dependencies
- build/config/package metadata
- assets/locale/style artifacts
- data/telemetry/ops surfaces

For each group, state the evidence that makes the group suspicious.

## `test-bloat-report.md`

This is not a coverage report.

Record tests that should go away, tests that should be rewritten only if the
underlying current behavior still matters, and tests that keep dead code alive.

Useful categories:

- delete with dead code
- delete as fake coverage
- delete or rewrite around current invariant
- keep, because current behavior or invariant is clear
- unsafe to judge without a named missing fact

Do not ask for more tests unless the user explicitly requested test strategy.

## `deletion-candidates.md`

Record every delete, consolidate, quarantine, and owner-check candidate.

For each candidate, include:

- item or cluster
- deletion class
- current references
- why references do not prove value
- current live-purpose result
- expected risk if removed
- exact owner check, if any
- recommended action

## `keep-decisions.md`

Record suspicious artifacts that survived review and why.

This file prevents a bad report shape where only delete candidates are visible
and the user cannot tell whether the reviewer checked obvious near misses.

Each keep decision must name the current root and current purpose. Do not keep
an artifact because it is familiar, exported, documented, tested, old, or
possibly useful someday.

## `coverage.md`

Record what was reviewed:

- files and paths inspected
- root maps and entrypoints checked
- import, call, reference, and export paths traced
- tests, fixtures, docs, examples, comments, schemas, generated artifacts,
  prompts, configs, package metadata, lockfiles, telemetry names, assets,
  styles, locale keys, install surfaces, logs, and status surfaces inspected
  where they affect deletion judgment
- git history used
- native parallel agent usage summary and final state for each launched slice
- known coverage gaps

Keep this as prose and compact lists. It is not a formal checklist engine.

## `findings.md`

Use this shape for each finding:

```markdown
### [DELETE|CONSOLIDATE|QUARANTINE|OWNER CHECK|KEEP|OBSERVATION] <short title>

- Item: <repo-relative path, symbol, artifact, or cluster>
- Current references: <where it is mentioned>
- Why references do not prove value: <stale/self-referential/test/docs/generated/etc.>
- Live purpose test: <passed/failed/unclear, with reason>
- Deletion class: <delete now/delete after owner check/quarantine/consolidate/keep>
- Evidence read: <files, flows, commands, history, source anchors, or child report>
- Expected risk if removed: <real breakage risk, not vague fear>
- Recommended action: <delete/rewrite/consolidate/quarantine/owner-check/keep>
```

Rules:

- Findings must be tied to current repo evidence or the requested review scope.
- Findings must cite evidence the reviewer actually read.
- Findings should name clusters when code, tests, docs, examples, generated
  files, configs, and package exports keep each other alive.
- `DELETE`, `CONSOLIDATE`, `QUARANTINE`, and `OWNER CHECK` are the main useful
  finding types.
- `KEEP` is only for suspicious artifacts that looked deletable but have a
  current root and current purpose.
- `OBSERVATION` is only for true informational facts, genuinely different
  contracts, excluded follow-ups, or surfaces that do not affect deletion
  judgment.
- Do not include suggested patch blocks.
- Do not include generic style advice.
- Do not include missing-test, QA, proof, or doc-hygiene findings unless they
  expose low-value artifacts that should go away.
- Empty findings are valid.

## `verdict.md`

Use one verdict:

- `cruft-found`: one or more material low-value artifacts or clusters should be
  deleted, consolidated, quarantined, or owner-checked for removal
- `no-material-cruft-found`: review completed, hidden cruft lanes were honestly
  covered, and no material low-value removal candidate was found
- `scope-incomplete`: the review could not inspect enough roots, references,
  or owner surfaces to make deletion judgment honestly
- `unsafe-to-judge`: external contract, data, migration, compliance, or
  production-state risk blocks deletion judgment until a specific owner
  question is answered

Use this shape:

```markdown
# Cynical Cruft Removal Verdict

VERDICT: cruft-found | no-material-cruft-found | scope-incomplete | unsafe-to-judge

## Top Deletion Clusters

<clusters or "No material deletion clusters.">

## Owner Checks

<specific owner checks or "No owner checks.">

## Keep Decisions

<suspicious keep decisions or "No notable keep decisions.">

## Cruft Summary

- Target reviewed:
- Live roots inspected:
- Biggest low-value categories checked:
- Self-referential islands:
- Test-hostage code:
- Docs/examples/prompts as stale support:
- Generated/config/package/dependency surfaces:
- Data/telemetry/ops surfaces:

## Coverage Summary

- Scope reviewed:
- Native parallel agents:
- Files/symbols/artifacts covered:
- Roots and paths traced:
- References rejected as weak proof:
- Git history used:
- Coverage gaps:

## Next Action

<one exact delete, owner-check, quarantine, rerun, or coverage action>
```

## Chat Reply

After saving the artifact, reply briefly:

- verdict
- top deletion clusters, if any
- owner checks, if any
- notable keep decisions, if material
- artifact path
- one next action from the review

Do not paste the full report unless the user asks. Do not prescribe the user's
broader workflow.
