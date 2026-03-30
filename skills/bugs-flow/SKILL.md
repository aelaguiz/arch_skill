---
name: bugs-flow
description: "Evidence-first bug investigation, fix, and verification with a single bug doc. Use when a request includes symptoms, regressions, Sentry issues, logs, crashes, or 'why is this happening?' and you need to analyze, fix, and verify a bug. Not for planned feature work, full architecture planning, or open-ended optimization loops."
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

- The work is planned feature delivery or architecture planning. Use `arch-plan`, `arch-mini-plan`, or `lilarch`.
- The task is open-ended optimization or a broad investigation loop rather than a concrete bug. Use `goal-loop` or `north-star-investigation`.

## Non-negotiables

- Keep one canonical bug doc under `docs/bugs/`.
- Analyze first. Do not modify code in analyze mode.
- Prefer first-party evidence: Sentry, logs, traces, QA notes, repro steps, and code anchors.
- Only move into fix mode when the bug doc is fix-ready.
- Keep fixes minimal and localized. No runtime fallbacks, silent swallowing, or compatibility shims unless explicitly approved.
- External cross-model review happens only if the user explicitly asks for review or code review.

## First move

1. Read `references/bug-doc-contract.md`.
2. Resolve the mode:
   - analyze
   - fix
   - review
3. Resolve `DOC_PATH` and read it fully if it already exists.
4. If the user asked for fix or review but the doc is not ready, step back and repair the investigation first.

## Workflow

### 1) Analyze mode

- Create or repair the bug doc.
- Ingest evidence and write ranked hypotheses.
- Mark the issue fix-ready only when the likely root cause is concrete enough to act on.

### 2) Fix mode

- Read the bug doc as the spec.
- Write or tighten the fix plan in the doc.
- Implement the smallest credible fix locally.
- Update verification, risk level, and outcome in the doc.

### 3) Review mode

- Only when explicitly requested by the user.
- Audit the implementation against the bug doc.
- Integrate only the feedback you agree with.
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
