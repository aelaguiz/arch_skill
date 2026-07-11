# Output Contract

Every review saves a disk artifact under:

```text
/tmp/cynical-architecture-review/<scope-slug>-<timestamp>/
```

Use a repo doc path only when the user explicitly asks for one.

The artifact must be readable without chat history. It should contain:

```text
target.md
architecture-map.md
complexity-ledger.md
subtraction-map.md
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
- resolved scope: worktree, branch diff, commit range, explicit paths,
  subsystem, plan scope, or architecture claim
- baseline and head/current state when known
- controlling plan, source truth, architecture claim, or worklog if supplied
- initial human scope, frozen convergence closure and freeze anchor, later
  human approvals, and plan/review-wave history when recoverable
- local instruction and convention files read
- important exclusions or unresolved target ambiguity

## `architecture-map.md`

Record:

- intended user experience
- hard constraints and experiment requirements
- non-requirements or future bets identified during review
- current owners and claimed owners
- control-flow and data-flow paths traced
- state, lifecycle, persistence, validation, rendering, routing, config, and
  generated-artifact ownership
- old paths, side doors, direct writers/readers, alternate command/API paths,
  and adjacent same-contract surfaces
- existing repo patterns compared and whether they are canonical, different,
  accidental-but-contained, or wrong-road
- scope-provenance anchors and scope-cycle evidence, or `not applicable`

Keep this as a review map, not a second plan.

## `complexity-ledger.md`

Record the complexity tax the current architecture charges:

- live concepts
- files and packages
- APIs and interfaces
- owner boundaries
- states, modes, flags, and feature gates
- adapters, wrappers, managers, registries, factories, orchestrators, policy
  layers, plugin surfaces, and generic machinery
- generated artifacts and config surfaces
- sync points
- caller obligations and memory contracts
- future-copy surfaces

For each important item, note the human-scope or frozen-closure anchor it claims
to serve. If none is visible, say so; current use is not authorization.

## `subtraction-map.md`

Record the simplification opportunities:

- delete now
- consolidate into an existing owner
- move ownership
- inline or collapse abstraction
- make invalid states impossible
- replace flags/modes with one owner and behavior selection
- make generated truth come from one source
- leave different, with the real contract difference
- named follow-up, only when outside requested scope
- user decision, only when requirements are genuinely unresolved

This is not a rewrite plan. It is the architecture review's map of what should
stop spreading and what smaller shape would preserve the same UX.

## `coverage.md`

Record what was reviewed:

- files and paths inspected
- symbols, owners, and call paths traced
- requirements and constraints mapped
- owner/invariant surfaces
- old paths, side doors, duplicate truth, alternate command/API paths, fallback
  readers/writers, generated artifacts, and adjacent same-contract surfaces
- tests, fixtures, docs, examples, comments, schemas, generated artifacts,
  prompts, config, telemetry, stable IDs, install surfaces, package metadata,
  logs, and status surfaces only where they reveal architecture truth,
  architecture lies, or future-copy risk
- native parallel agent usage summary and final state for each launched slice
- known coverage gaps

Keep this as prose and compact lists. It is not a formal checklist engine.

## `findings.md`

Use this shape for each finding:

```markdown
### [REQUIRED REPAIR|OBSERVATION] <short title>

- File: <repo-relative path>
- Symbol / line: <symbol or line>
- Architecture claim being tested: <claimed owner, abstraction, split, or requirement>
- Risk: <concrete architecture risk in plain language>
- Evidence: <diff, file, flow, child report, command output, source anchor, or "see file">
- Requirement / UX preserved: <what must keep working>
- Simpler architecture target: <delete, consolidate, move ownership, collapse state, or make impossible>
- Cynical architecture pattern: <catalog pattern>
- Scope provenance: <human anchor | frozen closure anchor | later human approval | missing>
- Scope-cycle evidence: <revision/wave/code chain or none>
- Required disposition: <subtract | human decision | no scope issue>
```

Rules:

- Findings must be tied to current code or the requested review scope.
- Findings must cite evidence the reviewer actually read.
- Any in-scope accidental architecture, invalid split ownership, duplicate
  truth, side door, unjustified abstraction, permanent shim, flags-as-owner
  split, state spread, wrong decomposition, or future-copy trap that must
  change before approval is a `REQUIRED REPAIR`.
- Scope-cycled or unauthorized post-freeze architecture is a `REQUIRED REPAIR`
  and forces `not-approved`, even when the latest plan calls it required.
- `OBSERVATION` is only for true informational facts, genuinely different
  contracts, excluded follow-ups, or surfaces that do not create architecture
  risk.
- Do not include suggested patch blocks.
- Do not include generic style advice.
- Do not include missing-test, QA, proof, or doc-hygiene findings unless they
  expose architecture ownership, stale truth, or future-copy risk.
- Empty findings are valid.

## `verdict.md`

Use one verdict:

- `approve`: cynical architecture review completed, architecture suspicion
  lanes were honestly covered, and no required repairs remain in the requested
  scope
- `not-approved`: one or more required architecture repairs exist in the
  requested scope
- `scope-incomplete`: the review could not honestly inspect the code needed to
  judge the architecture

Use this shape:

```markdown
# Cynical Architecture Review Verdict

VERDICT: approve | not-approved | scope-incomplete

## Required Repairs

<findings or "No required repairs.">

## Observations

<observations or "No observations.">

## Architecture Summary

- Intended UX preserved:
- Hard constraints / experiment requirements:
- Current owner shape:
- Biggest accidental-architecture risks checked:
- Old paths / duplicate truth:
- Complexity tax:
- Subtraction opportunities:
- QA/test/docs surfaces considered only as architecture evidence:

## Scope Provenance

- Initial human-authorized scope:
- Frozen initial convergence closure and freeze anchor:
- Later human approvals:
- Durable concepts without authority:
- Scope-cycle evidence and required disposition:

## Coverage Summary

- Scope reviewed:
- Native parallel agents:
- Files/symbols/owners covered:
- Code paths traced:
- Competing paths, side doors, and adjacent surfaces:
- Generated/config/prompt/status surfaces:
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
