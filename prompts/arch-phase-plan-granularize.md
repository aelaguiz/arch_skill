---
description: "Optional) Phase plan granularize: rewrite the existing phase plan into micro-phases + microtasks (single SSOT; no second checklist)."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin DOC_PATH (optional). Optional: LEVEL=1..5 FOCUS=\"...\">"
---
# /prompts:arch-phase-plan-granularize — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output should be short and high-signal (no logs); see OUTPUT FORMAT for required content.

Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.


# COMMUNICATING WITH USERNAME (IMPORTANT)
- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH, not in console output.


Documentation-only (planning):
- This prompt edits markdown documentation only. DO NOT modify product code.
- Single SSOT rule: do NOT add a second checklist block. Rewrite the existing Phase Plan in-place.
- You may read code and run read-only searches to ground file anchors, call-site groupings, and checks.
- Do not commit/push unless explicitly requested in $ARGUMENTS.


## North Star (authoritative)
Turn an existing Phase Plan into an execution-grade microtask checklist so smaller/dumber coding agents can execute it safely:
- more (micro-)phases than we need,
- each work item is loop-sized (one responsibility),
- file/symbol anchored,
- has a smallest credible verification signal,
- includes explicit delete/cleanup tasks to avoid parallel paths,
- and remains a single source of truth (SSOT) for implementation.


## Inputs / knobs (parse from $ARGUMENTS; no friction)
Optional knobs (best-effort parsing; do not hard-block if missing):
- `LEVEL=1..5`:
  - Level 1: harden phases (add missing call sites/deletes/checks; minimal splitting).
  - Level 2: canonical decomposition (SSOT → migrate one slice → migrate remaining (batches) → delete → check).
  - Level 3: call-site batching + per-file anchors for migrations.
  - Level 4: split tricky boundaries (concurrency/caching/migrations); add “trap checks”.
  - Level 5: maximum microtasking (scaffolding → wire one call site → wire remaining → delete legacy → final check).
- If `LEVEL` is omitted:
  - If the Phase Plan already contains a `arch_skill:phase_plan_granularize` metadata comment, default to `min(current_level + 1, 5)`.
  - Otherwise default to `LEVEL=2` (recommended baseline).
- `FOCUS="..."` (optional): bias the refinement to specific phases/areas (e.g., “Phase 2 migrations only”, “deletes”, “verification”).


## Procedure (deterministic; avoid thrash)

### 1) Resolve DOC_PATH
DOC_PATH:
- If $ARGUMENTS includes a `docs/<...>.md` path, use it.
- Otherwise infer from the conversation.
- If ambiguous, ask me to pick from the top 2–3 candidates.

### 2) Read DOC_PATH fully; locate the Phase Plan
Single SSOT requirement:
- You MUST edit the existing Phase Plan. Do NOT add a new “task breakdown” section elsewhere.

Locate the phase plan section using best-effort:
1) Prefer the block markers:
   - `<!-- arch_skill:block:phase_plan:start -->` … `<!-- arch_skill:block:phase_plan:end -->`
2) Else find a heading containing “Phase Plan” / “Phased Implementation” (case-insensitive).

If you cannot find a Phase Plan:
- STOP and print a short warning + the exact next command to run:
  - `/prompts:arch-phase-plan DOC_PATH`
- Do not invent a new plan format.

### 3) Determine target granularity level (LEVEL)
- Parse `LEVEL=` from $ARGUMENTS if present.
- Else, check inside the Phase Plan for a metadata comment:
  - `<!-- arch_skill:phase_plan_granularize ... -->` (or the multi-line form shown below)
- Select target LEVEL using the rules above.

### 4) Collect grounding inputs (without creating new sources of truth)
Use these as evidence anchors (do not duplicate them verbatim into the phase plan unless it’s small and high-leverage):
- `<!-- arch_skill:block:call_site_audit:start -->` … `end -->` (call sites + migration inventory)
- `<!-- arch_skill:block:reference_pack:start -->` … `end -->` (binding obligations, if present)
- Any explicit “deletes/cleanup” lists already in DOC_PATH
- Repo reality (read-only scans) only to:
  - turn vague items into file-anchored tasks,
  - derive call-site batches if missing,
  - find the smallest relevant checks (build/lint/test commands).

### 5) Rewrite the Phase Plan in-place (microtasks; dependency-ordered)
Rewrite inside the existing Phase Plan block/section. Keep it deterministic:
- Do not re-order phases unless strictly necessary for dependency correctness.
- Prefer preserving phase titles and sequencing, while making “Work” microtasked.
- Add a Phase 0 if missing: setup + inventory refresh + checks.
- Add explicit “delete/cleanup” tasks (no parallel truth).
- For each phase, convert “Work” into microtasks:
  - `* Work (microtasks):`
  - `- [ ] P<phase>.T<n> — <imperative task title>`
  - Include sub-bullets (short):
    - `File anchors:` (paths + symbols)
    - `Steps:` (2–6 bullets max; only when needed)
    - `Verification (smallest signal):` (existing command preferred)
    - `Exit criteria:` (1 line)
    - `Rollback:` (1 line; “n/a” is OK)

Monotonic / re-entrant rule:
- If the Phase Plan already contains checked tasks (`[x]` / `[X]`):
  - Do NOT delete or rewrite those completed lines.
  - Only refine/split unchecked tasks and add new tasks after existing done tasks.

Granularity rules (apply based on target LEVEL):
- Level 1: ensure each phase has explicit call-site anchors (or references), deletes, and a smallest signal.
- Level 2: apply SSOT → migrate one slice → migrate remaining (batches) → delete → check.
- Level 3+: replace “migrate remaining” with multiple tasks, each listing its call-site batch explicitly.
- Level 4+: split risky work into separate microtasks and add a trap check if regressions are likely.
- Level 5: no multi-responsibility tasks remain; every task should feel like a tight coding-agent loop.

Verification policy (same standards as implement prompts):
- Prefer existing checks (typecheck/build/lint + existing targeted tests).
- Avoid negative-value tests (deletion checks, visual constants/goldens, doc-driven gates).
- Manual QA is a short bullet list in Finalization, non-blocking.

### 6) Add/update granularize metadata (inside the Phase Plan block)
Inside the Phase Plan block, add or update this multi-line HTML comment near the top:

`<!--
arch_skill:phase_plan_granularize
level: <LEVEL>
pass_count: <increment>
last_updated: <YYYY-MM-DD>
-->`

Rules:
- If it already exists, update `level`, increment `pass_count`, and set `last_updated` to today.
- If missing, add it with `pass_count: 1`.


## DOC UPDATE RULES (anti-fragile)
Only update the Phase Plan content (single SSOT). Do not add new arch_skill blocks.

Placement rule (in order):
1) If the Phase Plan block markers exist, replace the content inside them:
   - `<!-- arch_skill:block:phase_plan:start -->` … `<!-- arch_skill:block:phase_plan:end -->`
2) Else, update the existing Phase Plan section in place (matching headings).

Do not paste the full updated Phase Plan to the console.


OUTPUT FORMAT (console only; USERNAME-style):
Communicate naturally in English, but include (briefly):
- North Star reminder (1 line)
- Punchline (1 line)
- DOC_PATH + target LEVEL (and whether it auto-incremented)
- What changed (e.g., “phase plan is now microtasked with file anchors + deletes + checks”)
- Issues/Risks (if any)
- Next action (usually: proceed to `/prompts:arch-implement-agent DOC_PATH`)
- Need from USERNAME (only if required)
- Pointers (DOC_PATH)

