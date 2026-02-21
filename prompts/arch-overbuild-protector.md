---
description: "Optional) Overbuild protector: scope triage + de-scope guard (classify Phase Plan items; move scope creep to follow-ups)."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin DOC_PATH (optional). Optional: MODE=report|apply STRICT=0|1 FOCUS=\"...\">"
---
# /prompts:arch-overbuild-protector — $ARGUMENTS
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
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.


Documentation-only (planning):
- This prompt edits markdown documentation only. DO NOT modify product code.
- Single SSOT rule: do NOT add a second execution checklist. The Phase Plan remains the authoritative execution list.
- You may read code and run read-only searches to validate "parity" claims and avoid inventing obligations.
- Do not commit/push unless explicitly requested in $ARGUMENTS.


## North Star (authoritative)
Prevent overbuilding and scope creep (especially from smaller coding agents) by making scope decisions explicit and mechanically enforceable in the plan doc:
- Every Phase Plan work item gets a justification bucket.
- Anything out-of-scope becomes intentionally deferred (Follow-ups), not silently dropped.
- Anything that is a known bug vector is explicitly rejected by default (unless explicitly requested/approved in-scope).


## Inputs / knobs (parse from $ARGUMENTS; no friction)
Optional knobs (best-effort parsing; do not hard-block if missing):
- `MODE=report|apply`:
  - `report` (default): write the scope triage block; do not rewrite the Phase Plan.
  - `apply`: write the scope triage block AND rewrite the Phase Plan in-place so only ship-blocking tasks remain as blocking checkboxes.
- `STRICT=0|1`:
  - `1` (default): ambiguity defaults to Follow-up (out of scope), not Include.
  - `0`: ambiguity defaults to Optional (timeboxed) instead of Follow-up.
- `FOCUS="..."` (optional): bias classification to a subset (e.g., "verification", "tooling", "Phase 2").


## Procedure (deterministic; avoid thrash)

### 1) Resolve DOC_PATH
DOC_PATH:
- If $ARGUMENTS includes a `docs/<...>.md` path, use it.
- Otherwise infer from the conversation.
- If ambiguous, ask me to pick from the top 2–3 candidates.

### 2) Read DOC_PATH and locate required anchors
Read DOC_PATH fully.

Treat these sections as scope authority (if present):
- `# TL;DR`
- `# 0) Holistic North Star`:
  - `0.2 In scope`
  - `0.3 Out of scope`
  - `0.4 Definition of done`
- YAML frontmatter `fallback_policy:` (default forbidden)

If any of those are missing or vague, WARN in the overbuild protector block (but do not hard-block).

### 3) Locate the Phase Plan (authoritative execution checklist)
Locate the phase plan section using best-effort:
1) Prefer the block markers:
   - `<!-- arch_skill:block:phase_plan:start -->` ... `<!-- arch_skill:block:phase_plan:end -->`
2) Else find a heading containing "Phase Plan" / "Phased Implementation" (case-insensitive).

If you cannot find a Phase Plan:
- STOP and print a short warning + the exact next command to run:
  - `/prompts:arch-phase-plan DOC_PATH`
- Do not invent a new plan format here.

### 4) Extract candidate work items from the Phase Plan
Best-effort extraction rules (do not overthink; keep it stable):
- Prefer explicit checkbox work items (`- [ ] ...`, `* [ ] ...`, `- [x] ...`).
- Preserve stable task IDs if they exist (e.g., `P2.T3`).
- If no checkboxes exist, treat each top-level "Work" bullet as a work item.
- If the Phase Plan is too unstructured to extract items reliably, warn and classify at the phase level instead.

### 5) Classify each work item into a scope bucket + disposition
For each extracted work item, assign:
- A justification bucket (A-G below)
- A disposition (Include ship-blocking / Optional timeboxed / Follow-up out of scope / Reject bug vector)
- Evidence anchors (brief, cite the relevant doc section and any file paths if used)

Bucket A - Explicit Ask (Include ship-blocking by default)
- Directly requested by the user blurb / TL;DR / in-scope UX surfaces / technical scope.

Bucket B - North-Star Necessary (Include ship-blocking by default)
- Required to satisfy the falsifiable claim and/or the Definition of Done evidence.
- Common examples: call-site migrations, deletes/cleanup to avoid parallel sources of truth, correctness fixes, minimal verification.

Bucket C - Parity Necessary (Include ship-blocking by default, but requires proof)
- Required to match an existing codebase convention or integration contract.
- Hard requirement: cite an internal anchor (file path/symbol/harness) proving the parity constraint exists.
- No anchor -> do not classify as parity.

Bucket D - Risk Mitigation Necessary (Include ship-blocking by default, but minimal)
- Required to avoid a concrete regression vector (data corruption, security exposure, correctness regression, perf cliff, migration safety).
- Guardrail: keep risk mitigation minimal; do not expand product scope.

Bucket E - Optional Quality (Optional timeboxed or Follow-up by default)
- Nice-to-have, "best practice", or maintainability improvement that is not required to ship the North Star.
- Default:
  - If it's tiny/low-risk: Optional (timeboxed).
  - Otherwise: Follow-up (out of scope), especially when STRICT=1.

Bucket F - Scope Creep (Follow-up out of scope by default)
- Expands UX scope beyond `0.2 In scope` or violates `0.3 Out of scope`.
- Or introduces new systems/harnesses not justified by A-D.

Bucket G - Bug Vector (Reject by default)
- Adds long-lived complexity / new failure modes / brittle gates without being necessary.
- Default reject list (unless explicitly requested/approved in-scope):
  - Runtime fallbacks/shims when `fallback_policy: forbidden` (or missing).
  - New "deleted code not referenced" tests.
  - Visual-constant / golden tests for churny UI (pixels/margins/colors).
  - Coverage gates / bespoke coverage reporting infrastructure.
  - New "remote runner" / distributed execution wiring for local dev tasks.
  - New generators/frameworks introduced just to save a little time.

Tie-breakers (deterministic defaults):
- If STRICT=1:
  - Ambiguity defaults to Follow-up (not Include).
- If STRICT=0:
  - Ambiguity defaults to Optional (timeboxed).
- Parity is never assumed: no anchor -> not parity.
- New tooling is Follow-up unless A-D clearly applies.

### 6) Write the Overbuild Protector block into DOC_PATH
Write/update this block (do not assume section numbers):
1) If `<!-- arch_skill:block:overbuild_protector:start -->` exists, replace inside markers.
2) Else append near the end before Decision Log if present, otherwise append.

Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:overbuild_protector:start -->
## Overbuild Protector (scope triage)

Summary:
- Mode: <report|apply>, Strict: <0|1>, Focus: <... or n/a>
- Items reviewed: <n>
- Include (ship-blocking): <n> (A: <n>, B: <n>, C: <n>, D: <n>)
- Optional (timeboxed): <n>
- Follow-ups (out of scope): <n>
- Rejected (bug vectors): <n>

Include (ship-blocking):
- <item> - Bucket <A|B|C|D> - Evidence: <doc section(s)> - Anchors: <paths/symbols if used>

Optional (timeboxed):
- <item> - Bucket <E> - Why optional: <...> - Evidence: <...>

Follow-ups (out of scope / intentionally deferred):
- <item> - Bucket <E|F> - Why deferred: <...> - Evidence: <...>

Rejected (bug vectors):
- <item> - Bucket <G> - Why reject: <...> - What to do instead: <smaller alternative>

Parity anchors used (if any):
- `<path>` - <pattern / contract>

Notes:
- Any scope-contract gaps that made classification lower-confidence:
  - <gap>
<!-- arch_skill:block:overbuild_protector:end -->

### 7) If MODE=apply, rewrite the Phase Plan in-place (no second checklist)
If MODE is `apply`:
- Rewrite the existing Phase Plan in-place so execution agents cannot accidentally treat out-of-scope items as required.
- Keep the Phase Plan as the single authoritative execution checklist; do not add a second checklist elsewhere.

Rules (anti-thrash):
- Do not delete or rewrite already-completed checkbox lines (`[x]` / `[X]`). Treat them as sunk cost and record the classification in the overbuild protector block.
- Preserve stable task IDs (e.g., `P2.T3`) if present.
- For Follow-ups (out of scope): remove them from the Phase Plan and list them under the overbuild protector block's Follow-ups section (intentionally deferred).
- For Optional (timeboxed): keep them in the Phase Plan but label clearly as optional (e.g., prefix "OPTIONAL:" or suffix "(optional)"), so they are non-blocking.
- For Reject (bug vectors): remove them from the Phase Plan and list them under Rejected with a recommended smaller alternative.

OUTPUT FORMAT (console only; USERNAME-style):
Communicate naturally in English, but include (briefly):
- North Star reminder (1 line)
- Punchline (1 line)
- DOC_PATH + MODE/STRICT
- What changed (e.g., "classified Phase Plan items; moved scope creep to intentional follow-ups")
- Issues/Risks (if any)
- Next action (usually: proceed to `/prompts:arch-review-gate DOC_PATH` or `/prompts:arch-implement(-agent) DOC_PATH`)
- Need from USERNAME (only if required)
- Pointers (DOC_PATH)

