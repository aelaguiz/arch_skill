# Repo Grounding

For repo-backed work, consensus is invalid until both child models have read
the code. The point is to reduce bug vectors by creating or preserving one way
of doing things, not to invent a plan from docs alone.

## Required Reads

Tell each model to inspect the smallest sufficient set of repo surfaces:

- repo instructions such as `AGENTS.md`, `CLAUDE.md`, or local package docs
- the feature's canonical owner path
- adjacent modules that already solve related problems
- tests, fixtures, schemas, migrations, or docs that define behavior
- install, routing, or entrypoint files if the plan changes runtime surface
- duplicate, drifting, or legacy pathways that may need adoption or removal

The model does not need to read the whole repo blindly. It must read enough to
defend where the work belongs and which existing patterns should be reused.

## Evidence The Parent Should Demand

Repo-backed replies should name:

- canonical owner paths
- patterns to adopt
- parallel paths or drift risks
- files where new behavior should not be duplicated
- tests or proof surfaces that would catch regressions
- behavior-preservation constraints
- any required docs or install-surface updates

Use `path:line` evidence when the exact location matters. If a model claims
"the repo already has a pattern for this" without naming the path, send it back
for grounding.

## Single-Path Pressure

Both models should ask:

- Can the existing owner absorb this requirement?
- Is there a shared helper, doctrine reference, test utility, or entrypoint
  that should be extended instead of copied?
- Is the proposed plan creating a second source of truth?
- Would this change leave old and new pathways active at the same time?
- Is a refactor needed first so the new work lands in the canonical place?
- Which future bug does this plan prevent by converging paths?

The answer may still be "create a new path", but only after the existing path
has been read and rejected for a stated reason.

## Parent Checks

The parent agent should treat these as repair prompts, not final answers:

- no file paths in a repo-backed proposal
- file paths named but no evidence that adjacent patterns were read
- a new abstraction proposed without comparing it to existing owner modules
- a plan that says "add a mode" but does not inspect routing/install surfaces
- a migration plan that leaves duplicate behavior without a retirement story
- a test plan that does not identify current proof surfaces

Do not let consensus form around ungrounded agreement. If both models skipped
repo reading, both models are wrong.

## Repo Prompt Add-On

Append this to first-pass and revision prompts when a repo is involved:

```text
Repo Requirement
You must read code before recommending a plan. Identify the canonical owner
path, existing patterns to adopt, duplicate or drifting pathways, and tests or
proof surfaces. The goal is to minimize new pathways and converge on one way of
doing the work where possible. If you propose a new path, explain why the
existing path cannot absorb the requirement.
```

## What Good Looks Like

A good repo-grounded answer says, in effect:

- "This belongs in X because X already owns the routing contract."
- "Y has the model-resolution helper; reuse it rather than adding a local alias
  table."
- "Z is a stale or parallel path; either avoid it or retire it explicitly."
- "The proof should touch these existing tests because they already guard the
  behavior."

That kind of answer is better than a polished architecture that could have
been written without opening the repo.
