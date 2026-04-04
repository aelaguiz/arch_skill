# Arch Step Shared Doctrine

## Communication contract

- Start console output with a one-line North Star reminder.
- Then give the punchline plainly.
- Then give a short natural-English update.
- Do not dump logs, giant lists, or full inserted sections to the console.
- Put deep detail in `DOC_PATH` or `WORKLOG_PATH`.
- Never be pedantic or ceremony-heavy. Optimize for the real task.

## Worktree and execution discipline

- Do not block on unrelated dirty files.
- Ignore unrecognized changes unless they directly conflict with the task.
- If committing, stage only files you touched unless instructed otherwise.
- When the command is clear, begin the work instead of restating the ask.
- Planning commands are docs-only.
- `implement` may change code and must respect branch discipline.

## Convergence rule

- `arch-step` always works toward one finished full-arch artifact.
- Local ownership is subordinate to artifact convergence.
- If a command updates one part of the plan and can see that nearby sections are now stale, it should repair the smallest safe set of contradictions before exiting.

## Question policy

Use repo evidence first.

You must answer anything discoverable from:

- code
- tests
- fixtures
- logs
- docs
- repo tooling
- referenced materials already in the plan

Allowed questions are narrow:

- true product or UX decisions not encoded anywhere
- external constraints not present in repo or docs
- real doc-path ambiguity after best-effort resolution
- missing access or permissions

If a question is still necessary, say where you looked first.

## DOC_PATH resolution defaults

- Use an explicit `docs/<...>.md` path when present.
- If multiple candidates exist, prefer the most plan-like doc:
  - canonical headings
  - stable `arch_skill:block:` markers
  - frontmatter with `status` or `doc_type`
- Never choose `*_WORKLOG.md` as `DOC_PATH`.
- If ambiguity survives best effort, ask the user to choose from the top 2-3 candidates.

## Scope model

- Requested behavior scope is authoritative for user-visible behavior.
- Architectural convergence scope covers internal refactors needed to route the requested behavior through a canonical path, remove duplicate truth, migrate clearly related adopters, and prevent drift.
- Architectural convergence may broaden touched files, symbols, or nearby adopters, but it must not broaden product capability.
- Bad scope adds new commands, modes, templating, plugin or config layers, dry-run surfaces, speculative tooling, or operational surfaces that were not required by the ask.

## Alignment checks before deeper work

The North Star is an alignment lock, not a mission statement.

- TL;DR should say what is changing and why.
- Section 0 should say what must remain true while we do it.
- Later commands should be able to resolve ordinary tradeoffs from those sections without re-asking the user.

Before substantive planning or implementation:

- North Star must be concrete and scoped
- claim must be falsifiable
- smallest credible acceptance signal must be explicit
- requested behavior scope must be explicit
- allowed architectural convergence scope must be explicit enough to tell convergence from product creep
- scope must not silently expand

If the North Star, requested behavior scope, or allowed architectural convergence scope is unclear or contradictory, stop for a quick doc correction before going deeper.

## Evidence philosophy

- Prefer the smallest credible signal.
- Prefer existing tests, typecheck, lint, build, instrumentation, or log signatures before new harnesses.
- If no cheap programmatic signal exists, use a short manual checklist.
- Manual QA is usually non-blocking until finalization and should not be mistaken for missing code.
- Avoid verification bureaucracy.

Negative-value defaults to avoid:

- deleted-code proof tests
- visual-constant or unstable-golden tests
- doc-inventory gates
- mock-only interaction tests with no behavior assertion
- bespoke harnesses or frameworks added just to create ceremony
- timing-hack tests when a behavior-level check or smaller signal would do

## Behavior-preservation rule

- Any refactor, consolidation, shared-path extraction, or call-site migration must preserve existing behavior.
- Prefer existing behavior-level checks, integration tests, targeted unit tests, builds, typechecks, instrumentation, or stable manual checklists over new machinery.
- If refactor risk is real and no existing signal buys enough confidence, add the smallest behavior-level, structure-insensitive check that would fail for the right reason.
- Do not call convergence work complete until the preservation signal has actually run.

## Architecture doctrine

- Code is ground truth.
- Prefer the most idiomatic existing repo pattern unless there is a concrete reason not to.
- Search for the canonical existing path before designing a new abstraction or code path.
- Single source of truth is the default.
- Avoid parallel implementations, duplicate writers, and shadow contracts.
- Boundaries and invariants should be enforceable, not merely described.
- Prefer hard cutover, explicit deletes, and fail-loud boundaries over compatibility shims.
- Runtime fallbacks or shims are forbidden unless the plan explicitly approves them via `fallback_policy: approved` plus a Decision Log entry with a removal plan.

## Scope-authority defaults

- Treat the plan's scope as authoritative.
- If work is required to converge onto the canonical path, remove duplicate truth, migrate clearly related adopters, or avoid a concrete regression, include it and proceed.
- If work adds new product functionality, alternate ways of doing the same thing, or speculative architecture, exclude it or record it as follow-up.
- If a newly discovered item is ambiguous, default to follow-up, defer, or explicit note rather than silently promoting it into ship-blocking work.
- Only stop and ask when the plan is internally contradictory, such as required work being declared out of scope.

## Warn-first sequencing

Recommended flow:

1. Deep dive pass 1
2. External research when warranted
3. Deep dive pass 2 if external research materially changes the design
4. Phase plan
5. Implement

This is a quality guard, not a hard blocker. Missing passes should be surfaced clearly but should not automatically stop useful work.

## Consistency repair doctrine

- Do not knowingly leave the plan internally contradictory just because the local section you owned is now correct.
- If target architecture changes, check TL;DR, Section 0, Section 1, Section 7, and Section 8 for stale claims.
- If sequencing or verification changes, check TL;DR, Section 0, Section 7, Section 8, and Section 10.
- If rollout or telemetry implications change, check Section 9 and Section 10.
- Prefer minimal truthful edits over broad rewrites.
- Record meaningful drift or approved exceptions in the Decision Log instead of silently rewriting history.

## Authoritative surfaces

- `DOC_PATH` is the one planning source of truth.
- `WORKLOG_PATH` is execution evidence, not a second plan.
- Section 7 is the one authoritative execution checklist.
- Helper blocks may sharpen or constrain the plan, but they must not create competing execution surfaces.
- The Decision Log is append-only and should capture real plan drift, approved exceptions, and meaningful sequencing changes.

## Pattern propagation

- When introducing a new SSOT, contract, lifecycle primitive, or non-obvious sharp edge, note where a short code comment should live at the canonical boundary.
- Prefer a few high-leverage comments over comment spam.
- The point is future drift prevention, not prose volume.

## Quality principle

Presence is not enough.

- A section is only useful when it is concrete enough for later phases to trust.
- A stage is only complete when the sections it owns are both present and strong enough to support downstream decisions.
- Consistency across sections matters as much as local section quality.
