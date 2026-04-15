# `implement` Command Contract

## What this command does

- ship the plan end to end
- keep code, plan, and worklog aligned as the run proceeds
- execute systematically against the authoritative checklist
- finish with an honest `complete` or `partial` outcome
- serve as the single full-frontier implementation pass used directly or inside `implement-loop`

## Execution North Star

Running `implement` should leave three things agreeing with each other:

- the code
- `DOC_PATH`
- `WORKLOG_PATH`

By the end of the run:

- phases were executed in order unless a documented sequencing change was necessary
- every in-scope implementation obligation is accounted for
- the plan says what is actually true
- unresolved items are visible instead of implied away
- no newly discovered unresolved decision has been silently guessed or scoped away

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Sections 0, 5, 6, 7, 8, `WORKLOG_PATH`, and `implementation_audit`

## Inputs and `DOC_PATH` resolution

- treat the user ask as steering, constraints, and any random notes that affect execution
- if the ask includes a `docs/<...>.md` path, use it
- otherwise resolve `DOC_PATH` from the conversation and repo context
- if the doc path is truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates

## Question policy

- answer anything discoverable from code, tests, fixtures, logs, docs, or repo tooling
- answer agent-capability questions from prompt files, agent instructions, runtime config, docs, or repo tooling before assuming the model cannot do something
- ask only for:
  - product or UX decisions not encoded anywhere
  - external constraints not present in the repo or doc
  - doc-path ambiguity after best effort
  - missing access or permissions
  - newly discovered plan-shaping decisions that are not encoded anywhere and cannot be settled from repo truth
- if a question is unavoidable, state where you looked first

## Reads for alignment

- the full plan doc
- especially Section 0, Section 5, Section 6, Section 7, and Section 8
- helper blocks that introduce real obligations

## Writes

- product code
- `WORKLOG_PATH`
- phase status and Decision Log in `DOC_PATH`

## Branch and worktree discipline

- never implement directly on the default branch
- if already on `main` or equivalent, create a feature branch before doing the work
- do not let unrelated dirty files block progress

## Communication contract

- begin work immediately when the command is clear
- do not preface with a mini-plan or restate the ask
- keep console output short and high-signal
- put deep detail in `DOC_PATH` or `WORKLOG_PATH`, not in console output

## Hard rules

- read `DOC_PATH` fully before editing code
- this command is a full ordered implementation run across the current approved Section 7 frontier; if the user wants hook-backed fresh auditing after each full-frontier run, use `implement-loop`
- treat the doc as the authoritative spec and checklist
- identify the canonical owner path before designing or extending a code path
- if the work includes refactor, consolidation, or shared-path extraction, identify the preservation signal before editing code
- when the changed behavior is agent-backed, inspect the current prompt and capability path before adding tooling
- for agent-backed behavior, prefer prompt, grounding, and native-capability edits before new harnesses, wrappers, parsers, OCR layers, or scripts
- if a phase proposes new tooling for agent-backed behavior, the plan must explain why prompt-first and capability-first options were insufficient
- treat touched live docs, comments, and instructions as real implementation work when they would become false after the change
- delete dead competing truth surfaces instead of preserving them for posterity; if a touched live doc/comment/instruction still matters, rewrite it to current reality in the same run
- broader docs consolidation, evergreen promotion, and final plan/worklog retirement belong to `arch-docs` after the code audit is clean; do not silently stretch `implement` into that separate docs-cleanup workflow
- do not start coding from a plan that is not decision-complete
- do not silently cut approved behavior or required implementation work because it is larger than expected
- do not rewrite plan requirements, scope, acceptance criteria, or phase obligations during execution to make partial work look intentional; if the approved plan itself needs to change, stop and route back to planning or the user
- build a compact in-memory implementation ledger from:
  - phase tasks
  - call-site audit items
  - migration notes and delete lists
  - live docs/comments/instructions to update or delete
  - include items from consolidation or follow-through sweeps only when the plan marked them as ship-blocking convergence work
- reconcile the ledger at phase boundaries
- no fallbacks or shims unless the plan explicitly approves them
- if the doc is materially non-canonical, repair it or route to `reformat` before treating it as authoritative

## Quick alignment checks

Before meaningful code changes:

- North Star is concrete and scoped
- credible acceptance evidence proportional to the current phase risk is identifiable
- requested behavior in-scope and out-of-scope are explicit
- the canonical owner path is identifiable or explicitly justified
- for agent-backed work, capability-first rationale is explicit before any new tooling
- preservation evidence for refactor-heavy work is identifiable
- Section 7 is real enough to execute
- no unresolved plan-shaping decisions remain in the authoritative artifact

If those are contradictory or unresolved, stop, repair what repo evidence settles, and ask the exact blocker question before continuing.

## Implementation ledger

Build a compact in-memory implementation ledger before editing code.

Derive it from the strongest planning artifacts in this order:

1. phase checklist items and exit criteria, or legacy phase tasks when the checklist field is absent
2. call-site audit rows and change-map entries
3. migration notes and delete lists
4. live docs/comments/instructions to update or delete
5. include items from consolidation or follow-through sweeps only when they are marked as required convergence work

Each ledger item should be concrete enough to classify later as:

- `done`
- `blocked`
- `deferred`
- `still todo`

Preferred mental row shape:

- `<area> | <file/symbol/call site> | <required change> | <status>`

This ledger is working memory, not a second plan doc. Write it down only when it materially helps explain blockers or truth.

## Warn-first preflight

- check the planning-pass block before coding:
  - `<!-- arch_skill:block:planning_passes:start -->`
  - `<!-- arch_skill:block:planning_passes:end -->`
- if the block exists, use it
- if it does not, infer pass completion from research and deep-dive content
- if recommended earlier passes are incomplete or unknown, warn clearly but continue
- continue to respect North Star, scope, and invariants; do not wing it

## Phase-by-phase execution loop

Execute Section 7 in order from the earliest incomplete or reopened phase through later reachable phases.

For each phase:

1. Read the phase goal, work description, checklist items, verification line, docs/comments notes, exit criteria, rollback, and any relevant call-site rows. If a modern phase still strands required obligations only in `Work`, `Verification`, `Docs/comments`, migration notes, or nearby prose, stop and repair the plan instead of guessing.
2. Confirm which canonical path owns the behavior for this phase, which work belongs in prompt or native-capability usage versus deterministic code when agent-backed, and which preservation signal must run if the phase refactors or consolidates code.
3. Mark the phase `Status: IN PROGRESS` once real work starts.
4. Implement the planned checklist items for that phase before moving to later phases.
5. If a later-phase task must be pulled forward to preserve correctness, record the sequencing change in Section 10 and update the affected phase descriptions so Section 7 stays truthful.
6. After each meaningful chunk, and whenever a phase-level claim needs proof, run the required programmatic evidence for that phase. Proof supports continued implementation; it does not authorize stopping early.
7. Reconcile the ledger, every checklist item, every required docs/comments propagation item, the required proof, and every exit criterion against the changed code before leaving the phase.
8. Update `DOC_PATH` and `WORKLOG_PATH` before moving on.

Do not skip ahead just because the happy path works.
Do not stop once one phase, one subset, or one local fix is green if later approved phases are still reachable.
Do not start the next phase while the current phase still has hidden `still todo` items.

## Plan document update rules

Keep Section 7 current as execution proceeds.

Under the current phase heading, add or update only the minimal truthful execution annotations needed:

- `Status: IN PROGRESS` when work has started
- `Status: COMPLETE` only when every checklist item is done, the required proof has actually run, required docs/comments propagation has landed where the phase depends on it, and every exit criterion is actually met
- `Status: BLOCKED` when a real blocker stops the phase
- `Completed work:` for brief high-signal bullets
- `Deferred:` only for explicit carry-forwards the user or approved plan already allowed; never use it to shrink required work discovered during execution
- `Blocked on:` for the current blocking fact
- `Manual QA (non-blocking):` for short end-of-run human checks

Also update only the nearby execution-truth surfaces needed to keep the artifact honest:

- if sequencing or assumptions drift materially, append a Section 10 Decision Log entry
- if a touched live doc, comment, or instruction would otherwise become stale, update or delete it in the same run and keep the phase notes truthful about that work
- do not rewrite TL;DR, Section 0, Section 5, Section 7, or Section 8 to weaken requirements, narrow scope, or lower the acceptance bar during implementation
- if execution reveals that requirements, scope, architecture commitments, or acceptance criteria really need to change, stop and route back to planning or the user instead of editing the plan to fit the current code
- do not decide mid-run that a planned item is out of scope unless the user or already-approved plan text had already excluded it before execution started
- if a planned item's requiredness turns out to depend on an unresolved user decision, stop and ask instead of silently downgrading it
- if the code becomes clean before the broader feature docs are fully consolidated, leave the handoff visible for `arch-docs` instead of burying that remaining docs-cleanup work inside finish notes

## Completeness discipline

Treat the implementation ledger as the completeness contract for the run.
Treat `Exit criteria` as authoritative phase-complete truths, not summary garnish.

At each phase boundary classify every in-scope ledger item as:

- `done`
- `blocked`
- `deferred`
- `still todo`

Do not claim completion while ledger items remain hidden.
Do not use `deferred` to hide originally required work unless that carry-forward was already explicitly allowed before execution began.

At each phase boundary:

- compare the current phase checklist items and exit criteria, or legacy phase tasks, against touched files and symbols
- compare affected call-site rows against code reality
- verify every required checklist item for that phase actually happened
- verify the required proof for that phase actually ran
- verify required deletes or cleanup for that phase actually happened
- verify required live docs/comments/instructions cleanup for that phase actually happened in touched areas
- verify every exit criterion is satisfied concretely rather than inferred from a broad success story
- decide whether any remaining item is `done`, `blocked`, `deferred`, or `still todo`
- keep unresolved items visible in the doc or worklog when relevant

## No-fallback policy

- default: do not add runtime fallbacks, compatibility shims, placeholder behavior, or best-effort paths that hide wrong behavior
- concrete anti-examples include:
  - swallowing errors and returning empty or null
  - silently defaulting to stale or cached data
  - "try old API if new fails"
  - leaving dev-only shims in production
- if correct behavior cannot be implemented with current information or permissions, stop and ask for what is missing or finish only the independent work
- only when the doc explicitly approves a fallback and logs a removal plan may a minimal shim exist
- if a shim is approved, it must include an explicit delete task in the plan

## Verification discipline

- after each meaningful chunk, run the required credible programmatic evidence for the current phase claim
- when `implement` is running inside `implement-loop`, do not hand control back to audit until the current full ordered implementation frontier is done or genuinely blocked and its claimed work has credible proof
- prefer existing checks before new tests or harnesses
- for agent-backed systems, new harnesses or scripts do not count as progress unless the plan justified them against prompt-first and capability-first alternatives
- any refactor, consolidation, or shared-path extraction must run a preservation signal before the phase can be called complete
- write tests only when they buy real confidence
- do not add negative-value proof machinery
- defer manual QA and UI automation to finalization by default
- add short boundary comments for new SSOTs or tricky gotchas when they will actually prevent future drift

Testing discipline:

- default to compile, typecheck, lint, build, existing targeted tests, or instrumentation signatures before writing new tests
- write tests only when they buy real confidence for new logic, regressions, state transitions, user-facing behavior, or behavior preservation during refactor
- prefer structure-insensitive, behavior-level checks over implementation-detail assertions
- do not add tests that only prove deleted code is gone, enforce doc inventories, assert visual constants, or depend on timing hacks
- if an existing negative-value test is blocking the run, prefer deleting it or rewriting it to a behavior-level assertion and record what replaced it

## Avoid blinders

- when you introduce or upgrade a centralized pattern, contract, or SSOT, scan nearby call sites for other adopters that should migrate
- if that work is required to converge onto the same canonical path and avoid drift, do it without asking
- if the plan or user already makes the work explicitly non-blocking, record it as a follow-up with file or symbol anchors and continue
- if requiredness is not derivable from repo truth plus the approved plan, stop and ask instead of making a pruning decision

## Worklog contract

`implement` owns `WORKLOG_PATH`:

- derive it from `DOC_PATH`
- create it if missing
- add plan/worklog cross-links
- initialize it with a minimal header and first entry when new
- append short progress updates at phase boundaries or when reality changes materially

Preferred minimal header when creating it:

```text
# Worklog

Plan doc: <DOC_PATH>

## Initial entry
- Run started.
- Current phase: <phase name>
```

Preferred worklog entry shape:

```text
## Phase <n> (<phase name>) Progress Update
- Work completed:
  - <item>
- Tests run + results:
  - <command> — <result>
- Issues / deviations:
  - <issue>
- Next steps:
  - <step>
```

The worklog is execution evidence only:

- do not turn it into a second plan
- keep entries short
- make sure phase-boundary truth in the worklog matches Section 7
- when running inside `implement-loop`, record the proof signal for claimed fixes before another audit cycle

## Stop conditions

- if a key invariant fails, stop, fix it, and re-run the required proof for the affected claim
- if a real blocker prevents progress, stop and report with evidence anchors

## Finish criteria

- all phases or checklist items needed for this run are resolved
- every in-scope ledger item is `done`, `blocked`, or `deferred` with rationale
- the North Star is satisfied by code and evidence
- no new parallel path or duplicate writer was introduced
- all required preservation checks for refactor-heavy work actually ran
- no stale touched live docs, comments, or instructions were left behind
- the plan reflects reality

Do not call the run `complete` if any planned call site, migration, delete, touched-doc cleanup, or required cleanup remains unresolved.

## Finalization

After implementation work is complete:

1. close only the verification gaps that still matter
2. run UI verification at the end when available; otherwise leave a short manual checklist
3. do not launch another model from this command
4. do a final plan-to-work reconciliation before claiming completion:
   - re-read the implementation-relevant parts of `DOC_PATH`
   - compare them against the ledger and the files or symbols actually touched
   - search for any planned call site, module, delete, migration task, canonical-path convergence task, or touched-doc cleanup task that never got resolved
   - search for any lingering old path, duplicate writer, skipped preservation signal, or stale touched live doc/comment/instruction
   - if anything remains unresolved, either finish it now or mark it explicitly as `deferred` or `blocked` with rationale and report the run as `partial`
5. if the operating context calls for commit/push, do it only after local verification

## Console contract

- start with a one-line North Star reminder
- give the punchline plainly
- summarize the code and doc progress plainly
- state whether the run is `complete` or `partial`
- name the highest-signal checks that were run and what they showed
- name issues or risks if they remain
- give the next action
- if `partial`, name unresolved ledger items plainly and point to the phase or call-site area they affect

## Final output contract

The close-out must say whether the run is:

- `complete`
- `partial`

If `partial`, name unresolved ledger items plainly.
