---
description: "Ralph retarget: update existing PROMPT.md/@fix_plan.md/@AGENT.md from a plan doc (manual QA non-blocking). Hard-bails if Ralph bootstrap missing."
argument-hint: "<Slang ok. Include docs/<...>.md or specs/<...>.md that is the plan/spec (SSOT).>"
---
# /prompts:arch-ralph-retarget — $ARGUMENTS
Execution rule: ignore unrelated dirty git files; if committing, stage only what you touched.
Do not preface with a plan. Begin work immediately.

Hard gate (Ralph bootstrap must already exist; do NOT create these files):
- Ralph is “set up” iff BOTH exist at repo root:
  - `PROMPT.md`
  - `@fix_plan.md`
- If either is missing: STOP immediately and print ONLY:
  - `ERROR: Ralph is not set up in this repo (expected PROMPT.md + @fix_plan.md at repo root). Run Ralph setup/bootstrap first, then rerun /prompts:arch-ralph-retarget.`

Core rule (UPDATE ONLY; do not regenerate):
- You MUST UPDATE the existing Ralph files in-place.
- Do NOT replace them with templates.
- Do NOT rewrite them “from scratch”.
- Preserve their current structure/formatting; make minimal, surgical edits to the specific sections described below.
- If an expected anchor section is missing and you can’t safely patch it, STOP and report what anchor is missing (do not invent a new file format).

Goal:
Given a planning/spec doc (DOC_PATH), retarget the repo’s existing Ralph setup to execute that plan.
This prompt edits ONLY:
- `PROMPT.md`
- `@fix_plan.md`
- `@AGENT.md` (if it exists)
- a copied spec file in `specs/` (see SPEC_PATH below)
- archival backups + clearing Ralph loop state files
DO NOT modify product code.

DOC_PATH:
- If $ARGUMENTS contains a `docs/<...>.md` or `specs/<...>.md` path, use it.
- Otherwise infer from conversation/repo.
- If ambiguous, ask the user to pick from the top 2–3 candidates.

SPEC_PATH (canonical SSOT; always materialize in `specs/`):
- Ralph should always reference a spec in `specs/` as SSOT (not `docs/`).
- Always ensure the SSOT doc exists at: `SPEC_PATH = specs/<DOC_BASENAME>.md`
  - Ensure `specs/` exists (create it if missing).
  - If `SPEC_PATH` does not exist: copy `DOC_PATH` → `SPEC_PATH` (exact copy; do not rewrite contents).
  - If `SPEC_PATH` exists:
    - If `DOC_PATH` and `SPEC_PATH` contents are identical: keep `SPEC_PATH` as-is.
    - If contents differ: STOP and ask which should be SSOT (show both paths + recommend creating a new uniquely named spec file in `specs/`).

From this point on:
- Treat `SPEC_PATH` as the authoritative “Spec (SSOT)” for Ralph.
- Treat `DOC_PATH` as the source doc that was copied (keep it as a reference anchor if helpful, but do not use it as SSOT).

Read SPEC_PATH and extract (as ground truth):
- TL;DR outcome
- Non-negotiables / invariants
- UX in-scope + out-of-scope
- Phase plan (depth-first phases)
- Call-site audit / migration map / delete list (if present)
- Evidence expectations, but treat manual QA as non-blocking (see policy below)

Ground truth policy (inescapable; repeat it everywhere it matters):
- Before writing tasks, identify the “ground truth set” for this plan:
  - Spec SSOT: `SPEC_PATH`
  - Source doc (copied into specs): `DOC_PATH` (only if different from SPEC_PATH)
  - Any additional docs referenced by SPEC_PATH that constrain behavior (list the exact doc paths)
  - Code anchors (entry points / primitives / central SSOT implementation) with file paths
  - If parity work: upstream reference file(s) (e.g., RN tokens, existing canonical implementations) with file paths
- When you update Ralph files, you MUST embed these references so the loop can’t drift:
  - In `PROMPT.md`: add/patch a short `Ground truth / References:` list (or equivalent existing section) that includes the exact paths above.
  - In `@fix_plan.md`: the `Spec (SSOT)` line must reference `SPEC_PATH`, and each `## Phase N (...)` should mention the relevant spec anchor once (e.g., `Spec anchor: SPEC_PATH — <section name>`). Each `###` subsection should include at least one code anchor path.
- If the spec is ambiguous, link to the exact paragraph/section that is ambiguous and propose a default; do not ask a contextless question.

Manual QA / screenshots policy (non-blocking; no harness):
- Do NOT require screenshots/recordings/harnesses to declare code-complete.
- Manual QA can be listed as a human follow-up, but MUST NOT block EXIT_SIGNAL.
- In `@fix_plan.md`: manual QA must NOT appear as checkboxes that gate completion. Put manual QA in a non-blocking follow-ups section using plain bullets (no `[ ]`).

Task granularity examples (from your sandbox1/psmobile `@fix_plan.md` — follow this style):
GOOD (granular, loop-sized; one responsibility; anchored in code):
- `Add getChallenges() to apps/mobile/src/services/playVsAi/api/serviceClientCore.ts (GET /v1/challenges)`
- `Add decodeGetChallengesResponse to apps/mobile/src/services/playVsAi/api/decode.ts`
- `Wire Lobby challenge row tap → startChallengeSession(challengeId) → renders PlayVsAiJourneyScreen`
- `Refactor usePlayVsAiSession: subscribe/unsubscribe only; do not startSession() on mount`
- `Run make typecheck` (as a dedicated item after types/decoder work)

BAD (do NOT put these as checkboxes; too big or not autonomous):
- `Phase 2 — Play tab lobby (no auto-start)` ← fine as a heading/group, NOT a task checkbox
- `Implement the lobby` / `do onboarding` / `finish Phase 3` ← too vague; no file anchors; not loop-sized
- `Manual QA: entering Play tab shows Lobby; nothing starts until tap` ← belongs in non-blocking HITL follow-ups, not gating completion
- `Take screenshots / build screenshot harness` ← explicitly out; do not create proof harness busywork

Ralph task shape (be explicit; do NOT generate “big phase blocks”):

GOOD attributes (what you must produce):
- One checkbox = one loop-sized change (finishable in one Ralph cycle).
- Every checkbox is code-anchored (file path + symbol/function/route where possible).
- Prefer the canonical decomposition: **introduce SSOT → migrate one bounded slice → migrate remaining call sites → delete old path → run a check**.
- Phases are allowed, but phase headings must be human-readable:
  - Always: `Phase N (<descriptor>)` (never “Phase 2” with no meaning).
- `@fix_plan.md` MUST be structured into sections:
  - `## Phase 1 (<descriptor>)`
    - `### <subsystem / slice>`
      - `- [ ] <loop-sized task>`
  - Do NOT dump everything into one giant phase list; split into subsections per subsystem/slice.
  - If a subsection would exceed ~6–10 checkboxes, split it further.
- Manual QA is a non-blocking follow-up section using bullets only (no checkboxes).
- Avoid “High/Medium/Low priority” buckets; convert to phased, dependency-ordered work.

BAD smells (fix these during retarget):
- “Do X + Y + Z” in a single checkbox (multiple responsibilities).
- “Update call sites” without enumerating call sites or providing a sweep task.
- “Align parity” tasks with no decomposition into SSOT + migrations + deletes.
- “Performance optimization” / “extended feature set” style filler tasks.
- Any screenshot/video/harness requirements.

Concrete example: rewrite “priority buckets / big phase blocks” into phase sections + loop-sized tasks (this is the structure you should write into `@fix_plan.md`)

BAD structure (priority buckets + huge checkboxes; causes stalls + vague questions):
## High Priority (Phase 1 — global primitives)
- [ ] Replace StableHeader PNG icons with painter widgets + `'∞'` formatting in `apps/flutter/lib/ui/components/stable_header.dart`
- [ ] Align Flutter motion tokens to RN `apps/mobile/src/motion/tokens.ts` in `apps/flutter/lib/design_system/app_motion.dart` and update call sites using non-RN tokens

GOOD structure (phases + subsections + loop-sized tasks):
## Phase 1 (Global primitives: StableHeader + motion tokens)

### StableHeader icons + `∞` formatting
- [ ] Audit StableHeader icon call sites + PNG references (list paths) (Flutter)
- [ ] Add painter widget for ONE StableHeader icon in `apps/flutter/lib/ui/components/stable_header.dart` (no other changes)
- [ ] Switch that ONE icon to painter rendering in `apps/flutter/lib/ui/components/stable_header.dart`
- [ ] Add a `formatStableHeaderStreakCount()` helper and use it from `apps/flutter/lib/ui/components/stable_header.dart` (`∞` case + normal ints)
- [ ] Convert remaining StableHeader PNG icons → painter, then delete the PNG rendering path

### Motion token parity (mirror RN → migrate → delete old path)
- [ ] Mirror RN motion tokens into `apps/flutter/lib/design_system/app_motion.dart` (SSOT mapping only; no call sites yet)
- [ ] Migrate ONE bounded call-site cluster to the mirrored tokens (e.g., StableHeader animations only)
- [ ] Migrate remaining parity-critical call sites to mirrored tokens, then delete/stop-export the old non-parity tokens

### Checks (small + targeted)
- [ ] Run the smallest relevant check (typecheck/lint/test) and record result

Clear previous task (backup + reset previous Ralph state):
1) Create an archive directory (neat + predictable):
   - If `docs/` exists: `docs/ralph_archive/<YYYY-MM-DD_HHMMSS>/`
   - Else: `.ralph_archive/<YYYY-MM-DD_HHMMSS>/`
2) Copy the prior Ralph control files into the archive directory:
   - `PROMPT.md`
   - `@fix_plan.md`
   - `@AGENT.md` (if present)
3) Also archive these Ralph loop state files if present (repo root):
   - `.call_count`
   - `.circuit_breaker_state`
   - `.circuit_breaker_history`
   - `.exit_signals`
   - `.response_analysis`
   - `.ralph_session`
   - `.ralph_session_history`
   - `.last_reset`
   - `status.json`
   - `progress.json`
4) After backup, delete ONLY the files listed in (3) from repo root so the next loop starts clean.
   - Do NOT delete logs/ or any product files.

UPDATE RULES (use sandbox1/psmobile as the “good” reference shape)
The “good” shape you’re aiming for looks like this (examples are illustrative; preserve your repo’s exact formatting):

PROMPT.md (example style):
- Has a line like:
  - `Current project/spec (SSOT):`
- Has “Non-negotiables” and “Git safety” sections.
- Has the `---RALPH_STATUS---` block format EXACTLY.

@fix_plan.md (example style):
- Begins with:
  - `# Ralph Fix Plan — <topic> (<date>)`
  - `Spec (SSOT): - <DOC_PATH>`
- Has “one task per loop” phrasing.
- Has checkboxes for autonomous work.
- Manual QA appears as non-blocking notes/follow-ups, NOT gating completion.

@AGENT.md (example style):
- Has setup/run/check commands and key code locations.

Now do the updates:

A) UPDATE `@AGENT.md` (only if it already exists; do not create it)
- Update “Current spec (SSOT)” to DOC_PATH.
- Update “Checks / quality backpressure” to match repo norms (prefer Make targets).
- Update “Run the app” commands as appropriate.
- Update “Key code locations” from DOC_PATH anchors (call-site audit + architecture anchors).
- Keep the file’s existing structure; patch lines, don’t rewrite.

If `@AGENT.md` is missing:
- Do NOT create it.
- Mention it in console summary as “skipped (missing)”.

B) UPDATE `@fix_plan.md` (in-place; preserve style; replace task content)
1) Update the “Spec (SSOT)” line(s) to point to DOC_PATH.
2) Replace the task list so it is bite-sized + autonomous:
   - One loop-sized checkbox per task.
   - Each task should be small and local (a few files), and correspond to the plan’s phases/call-site audit.
   - Include call-site sweeps and delete-list cleanup as explicit tasks if required by the plan.
   - Avoid “monster tasks”; split them like the GOOD examples above.
   - Add an explicit quality check at sensible points (typecheck/lint/test/build), but keep it lightweight and incremental.
3) Create or update a dedicated non-blocking section for HITL/manual verification:
   - Title suggestion (keep your file style): `Manual QA (HITL, non-blocking)` or `HITL Follow-ups (non-blocking)`
   - Use bullets ONLY (no checkboxes).
   - Put manual QA checklists here.
   - DO NOT include screenshot harness requirements.

C) UPDATE `PROMPT.md` (in-place; preserve structure; do not rewrite from scratch)
Update ONLY the sections needed to retarget:
- Update the SSOT reference to DOC_PATH (the line under “Current project/spec (SSOT)” or equivalent).
- Update the non-negotiables/guardrails list to match DOC_PATH (copy/condense without losing meaning).
- Ensure the execution rule is clear:
  - “ONE task per loop”
  - “Pick the first unchecked autonomous checkbox in @fix_plan.md”
- Ensure EXIT_SIGNAL semantics do not get blocked by manual QA:
  - If PROMPT.md says “all items in @fix_plan.md must be checked”:
    - Ensure manual QA is not represented as checkboxes (it must be bullets).
    - Reinforce that HITL follow-ups do not block completion.
- Preserve the `---RALPH_STATUS---` block format exactly. Do not change its keys.

STOP conditions (setup prompt only):
- If DOC_PATH is ambiguous: ask user to choose.
- If PROMPT.md or @fix_plan.md is missing: bail with the error above.
- Otherwise, do not ask questions.

CONSOLE OUTPUT FORMAT (summary only):
Summary:
- DOC_PATH: <path>
- Archive: <path>
- Updated:
  - `PROMPT.md`
  - `@fix_plan.md`
  - `@AGENT.md` (<updated|skipped missing>)
- Ralph state reset: <yes/no> (list which files were cleared, if any)
Open questions:
- <ONLY doc-path ambiguity or missing required anchors>
