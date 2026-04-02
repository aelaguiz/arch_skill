# `audit-implementation` Command Contract

## What this command does

- verify whether the code really satisfies the plan
- reopen false-complete phases when code work is missing
- distinguish missing code from non-blocking manual QA
- update the main artifact with evidence-anchored audit findings

## Audit North Star

After this command runs:

- the plan doc reflects reality
- false-complete phases are reopened
- missing code work is explicit and evidence-anchored
- manual QA remains visible but non-blocking
- a reader can tell whether the implementation is actually code-complete without hand-waving

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Sections 5, 6, 7, `WORKLOG_PATH`, and `implementation_audit`

## Inputs and `DOC_PATH` resolution

- treat the user ask as steering, constraints, and any relevant context
- if the ask includes a `docs/<...>.md` path, use it
- otherwise resolve `DOC_PATH` from the conversation and repo context
- if the doc path is truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates

## Question policy

- answer anything discoverable from code, tests, fixtures, logs, docs, or repo tooling
- ask only for:
  - product or UX decisions not encoded anywhere
  - external constraints not present in the repo or doc
  - doc-path ambiguity after best effort
  - missing access or permissions
- if a question is unavoidable, state where you looked first

## Reads for alignment

- the full plan doc
- target architecture contracts
- call-site audit and delete list
- phase plan and phase status
- definition of done and evidence expectations
- worklog when present

## Writes

- `arch_skill:block:implementation_audit`
- reopened phase status lines
- `Missing (code):` notes
- `Manual QA (non-blocking):` notes when needed

## Communication contract

- begin work immediately when the command is clear
- do not preface with a mini-plan or restate the ask
- keep console output short and high-signal
- put exhaustive detail in `DOC_PATH`, not in console output

## Hard rules

- docs-only; do not modify code
- code is ground truth
- this is a code-completeness audit, not a bureaucracy audit
- missing manual QA evidence is non-blocking and should not by itself reopen phases
- do not fix the code while auditing; record gaps instead

## Highest-bar audit criteria

Check all of these:

- absolute completeness:
  - if the plan says something is done, it is actually built
- architecture compliance:
  - SSOT is real
  - boundaries and contracts match the plan
  - required deletes and cleanup happened
  - no forbidden shims slipped in
- idiomatic fit:
  - implementation aligns with existing repo patterns unless the plan justified divergence
- call-site completeness:
  - every call site that should have migrated actually migrated

## Evidence split

Split plan evidence expectations into two buckets before judging completeness:

- code-verifiable evidence:
  - code paths
  - call-site migrations
  - deletes and cleanup
  - tests, build signals, instrumentation, assertions, or other programmatic evidence
- manual evidence:
  - screenshots
  - manual QA passes
  - human validation checklists

Only missing code-verifiable evidence can make the audit verdict `NOT COMPLETE`.
Missing manual evidence should become non-blocking follow-up.

## Audit procedure

1. read `DOC_PATH` fully
2. extract the plan's authoritative anchors:
   - target architecture contracts, APIs, names, and paths
   - call-site audit rows or equivalent migration inventory
   - phase plan and any phases marked complete, done, or checked off
   - delete list and cleanup expectations
   - definition-of-done evidence expectations
3. split evidence expectations into:
   - code-verifiable evidence
   - manual non-blocking evidence
4. validate each planned code change against repo reality:
   - verify each planned call-site change in code
   - search for missed call sites or lingering old APIs, patterns, or paths
   - verify SSOT enforcement and boundary compliance
   - verify required deletes and cleanup through repo search, static analysis, build, or typecheck rather than proof tests
   - verify claimed tests, assertions, or automation actually exist and hit the intended failure surface
5. determine phase truth:
   - if a phase is marked complete but code work is missing, reopen it
   - if code is complete but manual QA is pending, do not reopen it
6. write the audit block and any required in-place phase updates

Always name phases as `Phase <n> (<what it does>)` using the phase heading text when available.

## False-complete rules

- reopen a phase only for missing or incorrect code work
- do not reopen a phase solely because screenshots, manual QA, or human verification are still pending
- if the plan says an old path should be deleted, removed, or unreachable, treat that as code work and audit it accordingly
- if the implementation introduced a forbidden shim, fallback, or parallel source of truth, treat that as missing code correctness and reopen the responsible phase

## Update rules

Write or update:

- `arch_skill:block:implementation_audit`

Use this block shape:

```text
<!-- arch_skill:block:implementation_audit:start -->
# Implementation Audit (authoritative)
Date: <YYYY-MM-DD>
Verdict (code): <COMPLETE|NOT COMPLETE>
Manual QA: <pending|complete|n/a> (non-blocking)

## Code blockers (why code is not done)
- <bullets only about missing or incorrect code>

## Reopened phases (false-complete fixes)
- Phase <n> (<what it does>) — reopened because:
  - <missing items>

## Missing items (code gaps; evidence-anchored; no tables)
- <area>
  - Evidence anchors:
    - <path:line>
  - Plan expects:
    - <expected>
  - Code reality:
    - <actual>
  - Fix:
    - <fix>

## Non-blocking follow-ups (manual QA / screenshots / human verification)
- <follow-up item>
<!-- arch_skill:block:implementation_audit:end -->
```

Placement rule:

1. if `arch_skill:block:implementation_audit` already exists, replace inside it
2. otherwise insert the block after `# TL;DR`
3. if no TL;DR exists, insert after frontmatter
4. if no frontmatter exists, insert at the top

If code work is missing, update the affected phase in place with:

- `Status: REOPENED (audit found missing code work)`
- `Missing (code):`

If only manual QA is pending:

- do not reopen the phase
- add or update `Manual QA (non-blocking):`

When reopening a phase:

- use the phase heading text so the reopened phase is human-readable
- keep the missing-code list concrete and anchored to files, symbols, deletes, or tests
- do not erase prior truthful completion notes; correct them with the reopened status

## Verdict rules

- `Verdict (code): COMPLETE` only when no missing or incorrect code work remains
- `Verdict (code): NOT COMPLETE` when any required code work, migration, delete, cleanup, contract enforcement, or anti-shim expectation is unmet
- manual QA pending alone does not force `NOT COMPLETE`

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- otherwise stop after the audit block and any necessary phase reopenings or manual-QA notes are written

## Console contract

- one-line North Star reminder
- one-line punchline
- what the audit found and what changed in the doc
- real blockers or risks
- next action
