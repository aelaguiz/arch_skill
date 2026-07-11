# Unblocking rules

Unblocking means repairing known orchestration or evidence-access problems
without changing target-repo work. It is not permission for Stepwise to do a
worker's job.

## Orchestrator-owned unblocks

Stepwise may repair:

- malformed run-directory prompt files when the intended text is clear from
  confirmed inputs,
- malformed descriptors copied from the manifest,
- missing run-directory directories,
- schema normalization needed by the selected runtime,
- command flag drift in the external wrapper,
- missing prompt captures or diagnostic directory setup,
- external session-id lookup from already captured stream logs or native child
  handle recovery from host receipts.

Record the repair in the run directory before continuing.

Stepwise may not:

- edit target-repo files,
- fabricate worker evidence,
- rewrite an owner runbook,
- convert a critic observation into a pass,
- invent a repair instruction without a valid source tag.

## Worker-owned unblocks

Workers may repair safe blockers inside their step scope:

- check an exact path before claiming it is missing,
- run a help/list/read-only command before claiming a primitive is unavailable,
- read the owner-declared support path before switching to repo-wide discovery,
- stop with exact evidence when an owner primitive or prerequisite is truly
  unavailable.

## Critic-owned unblocks

Critics do not repair. They may inspect paths and read-only predicates already
provided in their prompt before failing or abstaining. If evidence remains
unavailable, they record the missing evidence and abstain.

## Diagnosis-owned unblocks

During the diagnose-and-repair protocol, Stepwise may use read-only diagnostic
turns to clarify:

- what the worker believed the step required,
- which owner clause supported that belief,
- which input looked wrong,
- whether an upstream session produced bad input,
- whether a proposed rule is actually in owner doctrine.

Diagnostic turns cannot modify files and do not consume repair bounces.

## Fail loud

Fail loud when:

- the same orchestration defect recurs after one bounded repair,
- a required continuation handle cannot be recovered,
- the critic writes to disk,
- the StepVerdict contains stale prescriptive fields,
- repair would require claiming an event happened before it actually happened,
- owner doctrine is ambiguous and no safe source-tagged repair exists.
