---
description: "Ralph enhance pass: re-review DOC_PATH + existing PROMPT.md/@fix_plan.md/@AGENT.md and make tasks more granular + complete (no code edits)."
argument-hint: "<Optional. Slang ok. Include docs/<...>.md or specs/<...>.md to pin DOC_PATH.>"
---
# /prompts:arch-ralph-enhance — $ARGUMENTS
Execution rule: ignore unrelated dirty git files; if committing, stage only what you touched.
Do not preface with a plan. Begin work immediately.

Hard gate (Ralph bootstrap must already exist; do NOT create these files):
- Ralph is “set up” iff BOTH exist at repo root:
  - `PROMPT.md`
  - `@fix_plan.md`
- If either is missing: STOP immediately and print ONLY:
  - `ERROR: Ralph is not set up in this repo (expected PROMPT.md + @fix_plan.md at repo root). Run Ralph setup/bootstrap first, then rerun /prompts:arch-ralph-enhance.`

Core rule (UPDATE ONLY; do not regenerate):
- You MUST UPDATE the existing Ralph files in-place.
- Do NOT replace them with templates.
- Do NOT rewrite them “from scratch”.
- Preserve their current structure/formatting; make minimal, surgical edits to the specific parts described below.
- If an expected anchor section is missing and you can’t safely patch it, STOP and report what anchor is missing (do not invent a new file format).

Goal:
Do a “second pass” on an existing Ralph setup:
- Re-read the plan/spec doc (DOC_PATH) and the current Ralph control files.
- Make the Ralph loop more effective: tasks are smaller, more explicit, more idiomatic, and more complete.
- Find what’s missing (coverage gaps, call sites, cleanup/deletes, invariants, checks).
- Ensure the plan won’t get stuck on manual QA / screenshot proof burdens.

This prompt edits ONLY:
- `PROMPT.md`
- `@fix_plan.md`
- `@AGENT.md` (if it exists)
DO NOT modify product code. You may read code/search to ground file anchors and call-site completeness.

$ARGUMENTS is freeform steering. Treat it as intent + constraints + random thoughts.

DOC_PATH:
- If $ARGUMENTS includes a `docs/<...>.md` or `specs/<...>.md` path, use it.
- Else, if `@fix_plan.md` already contains a “Spec (SSOT)” reference, use that.
- Else infer from conversation/repo.
- If ambiguous, ask the user to pick from the top 2–3 candidates.

Question policy (strict: no cryptic questions):
- Do NOT ask technical questions you can answer by reading the plan, code, tests, or existing Ralph files. Go look and decide.
- Ask only when DOC_PATH is ambiguous or a true product/UX scope decision is required.
- Never ask vague “what do you want to do?” questions. Pick the most idiomatic default, encode it into tasks, and proceed.
- If you must ask, include full context (what file, what section, what you found, your recommended default).

Manual QA / screenshots policy (non-blocking; no harness):
- Do NOT require screenshots/recordings/harnesses to declare code-complete.
- Manual QA can be listed as a human follow-up, but MUST NOT block EXIT_SIGNAL.
- In `@fix_plan.md`: manual QA must NOT appear as checkboxes. Put manual QA in a non-blocking follow-ups section using plain bullets (no `[ ]`).

What “good” looks like (second-pass criteria)
You are upgrading the Ralph files so they meet these standards:

1) Granularity (loop-sized)
- Each checkbox task is small enough to complete in a single Ralph loop.
- Each task has one responsibility and is anchored to code (file paths + symbols where possible).
- Avoid monster tasks (“implement X”). Split into tasks like: add API, add decoder, wire call site, delete old path, run check.

2) Completeness (coverage)
- Every plan phase has coverage in the fix plan.
- Call sites are explicitly audited (tasks include “find all call sites” + “migrate each call site” + “delete old path”).
- Drift-proofing exists (central SSOT pattern; no parallel paths; deletes/cleanup explicitly listed).

3) Idiomatic + enforceable
- Tasks drive the most idiomatic architecture by repo standards (not just “make it work”).
- Invariants are stated in PROMPT.md so the loop fails loudly when violated (tests/checks, typecheck, lint, build).

4) Execution clarity
- Phase references must be human-readable: never “Phase 2” with no meaning.
  - Always: `Phase N (<short descriptor so a human remembers what it is>)`

DO THIS WORK (read → diagnose gaps → patch Ralph files)

A) Read + diagnose
1) Read DOC_PATH fully (treat as authoritative SSOT).
2) Read `PROMPT.md`, `@fix_plan.md`, and `@AGENT.md` (if present).
3) Identify problems to fix, with evidence anchors:
   - Tasks too big / vague
   - Missing call sites / missing cleanup/deletes
   - Phases unnamed/unclear (e.g., “Phase 2” with no descriptor)
   - Manual QA incorrectly blocking completion (checkboxes or “must screenshot”)
   - Checks missing (typecheck/lint/tests/build) where they would prevent churn

B) Update `@fix_plan.md` (in-place; preserve style; refine and expand tasks)
Rules:
- Prefer adding specificity over adding more tasks; split only when a task cannot be done in one loop.
- Keep tasks ordered by dependency and plan phase order (no skipping).
- Explicitly add call-site audit tasks when the plan implies migrations.
- Explicitly add delete/cleanup tasks where the plan demands “no parallel path”.
- Insert small “quality backpressure” tasks at the right time (typecheck/lint/tests/build), but keep them incremental.

Checklist for each phase group you touch:
- Phase header includes descriptor: `Phase N (<descriptor>)`
- Tasks list contains:
  - <create/adjust primitive or SSOT>
  - <migrate one bounded slice / one set of call sites>
  - <delete old path / cleanup>
  - <run a relevant check>

Manual QA placement:
- Add/maintain a `Manual QA (HITL, non-blocking)` section using bullets only.
- Manual QA bullets can reference “Amir run” or “human check later” without blocking.

C) Update `PROMPT.md` (in-place; preserve the `---RALPH_STATUS---` block exactly)
Patch only what improves execution:
- Ensure it points to DOC_PATH as the SSOT.
- Ensure it instructs the loop to:
  - pick the first unchecked autonomous checkbox in `@fix_plan.md`
  - do ONE checkbox per loop
  - refresh memory of DOC_PATH’s North Star + scope before each loop
- Ensure completion semantics won’t be blocked by HITL follow-ups:
  - Manual QA must be bullets (not checkboxes) and explicitly “non-blocking”.

D) Update `@AGENT.md` (ONLY if it already exists; do not create it)
- Update SSOT reference to DOC_PATH.
- Update “how to run checks” commands to repo norms.
- Update “key code locations” using DOC_PATH anchors and any verified call-site sweep you did (read-only).

Stop conditions:
- If DOC_PATH is ambiguous: ask user to choose.
- If required anchors in PROMPT.md/@fix_plan.md are missing and you can’t patch safely: stop and report what’s missing.
- Otherwise do not ask questions.

CONSOLE OUTPUT FORMAT (summary only):
Summary:
- DOC_PATH: <path>
- Updated:
  - `PROMPT.md`
  - `@fix_plan.md`
  - `@AGENT.md` (<updated|skipped missing>)
- Upgrades made:
  - <1–5 bullets: granularity/coverage/idiomatic/checks>
Open questions:
- <ONLY doc-path ambiguity or missing required anchors>
