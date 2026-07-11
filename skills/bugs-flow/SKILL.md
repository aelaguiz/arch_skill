---
name: bugs-flow
description: "Run the standalone evidence-first bug workflow with a single bug doc: analyze, fix, and review. Use when a request includes symptoms, regressions, Sentry issues, logs, crashes, or 'why is this happening?' and you need to investigate, fix, and verify a bug. Not for feature planning, full-arch work, or open-ended optimization loops."
metadata:
  short-description: "Analyze, fix, and verify bugs"
---

# Bugs Flow

Use this skill for the bug workflow family: analyze, fix, and optionally review.

## When to use

- The ask is a bug report, regression, crash, incident, or Sentry investigation.
- The user has symptoms, logs, traces, QA notes, or a bug doc and wants the issue analyzed or fixed.
- The work should be driven by evidence and a single bug doc rather than by a feature plan.

## When not to use

- The user wants a repo-wide audit pass or leave-it-running defect hunt rather than one known bug. Use `audit-loop`.
- The work is planned feature delivery or architecture planning. Use `arch-step`, `arch-mini-plan`, or `lilarch`.
- The task is open-ended optimization or a broad investigation loop rather than a concrete bug. Use `goal-loop` or `north-star-investigation`.

## Non-negotiables

- Keep one canonical bug doc under `docs/bugs/`.
- Analyze first. Do not modify code in analyze mode.
- Prefer first-party evidence: Sentry, logs, traces, QA notes, repro steps, and code anchors.
- Only move into fix mode when the bug doc is fix-ready.
- Keep fixes minimal and localized. No runtime fallbacks, silent swallowing, or compatibility shims unless explicitly approved.
- The human-authorized outcome is the corrected behavior for the documented
  bug. During analyze/initial planning only, include the smallest evidenced
  directly competing same-contract path needed to fix the shared cause; record
  the closure or `none` and freeze it before fix mode. Apply
  `../_shared/scope-and-convergence.md`.
- Fix and review cannot widen that frozen closure. A newly discovered adjacent
  improvement or owner path needs a human decision; review never reopens generic
  architecture planning.
- Review side work happens only if the user explicitly asks for review or code
  review. Once authorized, prefer a new clean same-host native critic; external
  review remains available when its concrete provider, model, lifecycle,
  isolation, automation, receipt, or other benefit is worth the added process
  and integration cost under the shared agent policy.
- Do not let "review" become an excuse to reopen generic architecture planning.

## First move

1. Read `references/bug-doc-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Read `../_shared/scope-and-convergence.md`.
4. Read `../_shared/agent-orchestration-policy.md` before dispatching an
   implementer or critic.
5. Resolve the mode:
   - analyze
   - fix
   - review
6. Resolve `DOC_PATH` and read it fully if it already exists.
7. If the user asked for fix or review but the doc is not ready, step back and repair the investigation first.
8. Read the mode reference and `references/quality-bar.md`.

## Parent And Child Roles

- The active parent owns the human-authorized bug scope, frozen convergence
  closure, bug-doc writes, decomposition, result accounting, synthesis,
  accepted findings, and final review verdict. Capture current git status and
  the relevant diff before a read-only critic runs, then compare current state
  before accepting its evidence.
- If implementation is delegated, start the implementer as a new clean
  same-host native child by default and preserve its exact handle. In Codex set
  `fork_turns: "none"`; in Claude use a clean named or custom subagent, not a
  bare conversation fork or skill `context: fork` shorthand. Use bounded or
  full inherited context only for a named dependency that exists solely in
  chat; ordinary context travels through the bug doc, exact paths, and a
  bounded brief.
- Each independent review or recheck starts as a different new clean critic
  with the strongest read-only capability available and an explicit no-edit,
  no-write contract. Send every accepted repair finding back to the exact
  implementer that owns the fix; never resume a critic as an implementer and
  never reuse a prior critic for the next independent gate.
- Implementers and critics may not create children or invoke delegation,
  consult, or review skills unless the parent explicitly assigns a bounded
  nested scope and budget. If multiple independent review lenses genuinely
  help, bound fanout by host slots, shared-file or shared-state collision risk,
  and the parent's capacity to inspect and integrate every return.
- External review is a transport choice, not a freshness requirement or a
  prohibited lane. Use it when a concrete benefit is worth its added cost; the
  same clean critic, read-only, return, parent-state-check, and independent
  recheck contracts still apply.

## Workflow

### 1) Analyze mode

- Create or repair the bug doc.
- Ingest evidence and write ranked hypotheses.
- Mark the issue fix-ready only when the likely root cause is concrete enough to act on.

### 2) Fix mode

- Read the bug doc as the spec.
- Write or tighten the fix plan in the doc.
- Implement the smallest credible fix locally.
- If an implementer child owns the fix, preserve its exact handle so accepted
  review repairs resume that same role and scope.
- Update verification, risk level, and outcome in the doc.

### 3) Review mode

- Only when explicitly requested by the user.
- Start a new clean independent critic and audit the implementation against the
  bug doc without letting the critic write files.
- The parent integrates only accepted feedback. Resume the exact implementer
  for those repairs, then use another new clean critic for every independent
  recheck.
- If no explicit review ask exists, do not launch review side work.

## Output expectations

- Update `DOC_PATH` in every mode.
- Keep console output short:
  - Bug North Star reminder
  - punchline
  - what changed
  - tests or evidence gathered
  - risks or blockers
  - next action

## Reference map

- `references/bug-doc-contract.md` - bug doc structure, evidence rules, Sentry handling, and status transitions
- `references/shared-doctrine.md` - evidence discipline, anti-fallback rules, and escalation boundaries
- `references/analyze.md` - create or repair the bug doc and make the issue fix-ready
- `references/fix.md` - implement the smallest credible fix and keep the doc truthful
- `references/review.md` - explicit-review-only audit behavior
- `references/quality-bar.md` - strong vs weak bars for evidence, fix-ready state, and verification
