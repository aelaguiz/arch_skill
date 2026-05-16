# Repo Grounding

For repo-backed work, consensus is invalid until both child models have read
real evidence. The parent must not pre-select the answer surface for them.
Grounding has two modes:

- Open investigation: preserve discovery freedom. The children choose the code,
  docs, research, tests, commands, and local artifacts needed to explain or
  cross-check the user's question.
- Architecture plan: apply single-path pressure. The children identify the
  owning path and avoid creating duplicate ways to do the work.

## Required Reads

For open investigation, tell each model to start with user-named artifacts and
then choose its own evidence trail. Examples of valid evidence include:

- repo instructions such as `AGENTS.md`, `CLAUDE.md`, or local package docs
- the user-named file, test, command, symptom, report, or branch
- nearby code, docs, tests, fixtures, schemas, configs, and research material
  the child model independently judges relevant
- command output or cheap checks that clarify the evidence without doing the
  implementation work

For architecture planning, tell each model to inspect the smallest sufficient
set of owner surfaces:

- the feature's canonical owner path
- adjacent modules that already solve related problems
- tests, fixtures, schemas, migrations, or docs that define behavior
- install, routing, or entrypoint files if the plan changes runtime surface
- duplicate, drifting, or legacy pathways that may need adoption or removal

The model does not need to read the whole repo blindly. It must read enough to
defend its answer. In investigation mode, that means defending what evidence
supports or falsifies the theory. In architecture mode, that means defending
where the work belongs and which existing patterns should be reused.

## Evidence The Parent Should Demand

All repo-backed replies should name:

- the evidence they actually read
- the evidence trail they chose and why

Investigation replies should also name:

- the claims that are still only theories
- the fastest falsifier or proof surface

Architecture replies should also name:

- canonical owner paths
- patterns to adopt
- parallel paths or drift risks
- files where new behavior should not be duplicated
- tests or proof surfaces that would catch regressions
- behavior-preservation constraints
- any required docs or install-surface updates

Use `path:line` evidence when the exact location matters. If a model claims
"the repo already has a pattern for this" or "the evidence points to this root
cause" without naming the evidence, send it back for grounding.

## Single-Path Pressure

Use this section for architecture or implementation-plan mode. Do not force it
onto open investigations unless the child models discover that duplicated
runtime paths are part of the problem.

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
- path lists that clearly came from the parent rather than child discovery
- file paths named but no explanation of why those files mattered
- investigation replies that accept the parent framing without checking whether
  another evidence path is more likely
- architecture replies with a new abstraction but no comparison to existing
  owner modules
- architecture replies that say "add a mode" but do not inspect routing or
  install surfaces
- migration plans that leave duplicate behavior without a retirement story
- test plans that do not identify current proof surfaces

Do not let consensus form around ungrounded agreement. If both models skipped
repo reading, both models are wrong.

## Repo Prompt Add-On

Append this to first-pass and revision prompts when a repo is involved:

```text
Repo Requirement
You must read real repo evidence before recommending or agreeing. Start from
the user-named artifact or symptom, then choose the code, docs, research, tests,
commands, and local artifacts needed for the goal. Cite what you inspected and
why it matters. In open investigation mode, do not assume the parent has named
the right files, layers, theories, or failure categories. In architecture mode,
also identify canonical owner paths, patterns to adopt, duplicate or drifting
pathways, and tests or proof surfaces.
```

## What Good Looks Like

A good open-investigation answer says, in effect:

- "The user named X, so I started there, but the evidence trail moved to Y."
- "This theory predicts A and is falsified by B."
- "The fastest trap is C because it observes the earliest artifact where the
  symptom can appear."
- "I ruled out D because this file and this command output contradict it."

A good architecture-grounded answer says, in effect:

- "This belongs in X because X already owns the routing contract."
- "Y has the model-resolution helper; reuse it rather than adding a local alias
  table."
- "Z is a stale or parallel path; either avoid it or retire it explicitly."
- "The proof should touch these existing tests because they already guard the
  behavior."

That kind of answer is better than a polished architecture that could have
been written without opening the repo.
