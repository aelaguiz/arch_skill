---
description: "Optional) Phase plan granularize (agent-assisted): rewrite the existing phase plan into micro-phases + microtasks using parallel read-only subagents."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin DOC_PATH (optional). Optional: LEVEL=1..5 FOCUS=\"...\">"
---
# /prompts:arch-phase-plan-granularize-agent — $ARGUMENTS
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


Subagents (agent-assisted; parallel read-only sweeps when beneficial)
- Use subagents to keep repo-wide scanning and long outputs out of the main agent context.
- Spawn these subagents in parallel only when they are read-only and disjoint.
- Subagent ground rules:
  - Read-only: subagents MUST NOT modify files or create artifacts.
  - Shared environment: avoid commands that generate/overwrite outputs; prefer pure read/search.
  - No questions: subagents must answer from repo/doc evidence only.
  - No recursion: subagents must NOT spawn other subagents.
  - Output must match the exact format requested (no extra narrative).
  - Do not spam/poll subagents; wait for completion, then integrate.
  - Close subagents once their results are captured.


Documentation-only (planning):
- This prompt edits markdown documentation only. DO NOT modify product code.
- Single SSOT rule: do NOT add a second checklist block. Rewrite the existing Phase Plan in-place.
- You may read code and run read-only searches to ground file anchors, call-site groupings, and checks.
- Do not commit/push unless explicitly requested in $ARGUMENTS.


## North Star (authoritative)
Turn an existing Phase Plan into an execution-grade microtask checklist so smaller/dumber coding agents can execute it safely:
- micro-phases,
- loop-sized tasks,
- file/symbol anchored,
- smallest credible checks,
- explicit deletes/cleanup,
- and still a single SSOT (Phase Plan only).


## Inputs / knobs (parse from $ARGUMENTS; no friction)
Same knobs as the non-agent prompt:
- `LEVEL=1..5` and `FOCUS="..."`
- Default LEVEL:
  - If Phase Plan metadata exists, default to `min(current_level + 1, 5)`.
  - Else default to `LEVEL=2`.


## Procedure (agent-assisted; deterministic)

### 1) Resolve DOC_PATH
DOC_PATH:
- If $ARGUMENTS includes a `docs/<...>.md` path, use it.
- Otherwise infer from the conversation.
- If ambiguous, ask me to pick from the top 2–3 candidates.

### 2) Read DOC_PATH fully; locate Phase Plan
Locate the phase plan section:
1) Prefer the block markers:
   - `<!-- arch_skill:block:phase_plan:start -->` … `<!-- arch_skill:block:phase_plan:end -->`
2) Else find a heading containing “Phase Plan” / “Phased Implementation”.

If you cannot find a Phase Plan:
- STOP and print the exact next command:
  - `/prompts:arch-phase-plan DOC_PATH`
- Do not invent a new plan format.

### 3) Determine target LEVEL
- Parse `LEVEL=` from $ARGUMENTS if present.
- Else read Phase Plan granularize metadata if present; otherwise default to `LEVEL=2`.

### 4) Spawn subagents (only when needed; disjoint scopes)
Use subagents if the repo surface is large or the plan implies a large migration/deletes list. Otherwise do it inline.

Spawn in parallel (read-only), as needed:

1) Subagent: Call-Site Grouper (read-only)
   - Task: enumerate call sites that must change and group them into logical migration batches.
   - Inputs:
     - The `Call-Site Audit` section in DOC_PATH
     - Any symbols/APIs referenced in the Phase Plan
   - Output format (bullets only):
     - Group: <name>
       - <path> — <symbol> — <why>

2) Subagent: Deletes / Cleanup Inventory (read-only)
   - Task: identify what must be deleted/removed/disabled to avoid parallel paths (old APIs, dead files, unused codepaths).
   - Output format (bullets only):
     - <path> — <what should be deleted/removed/blocked> — <why>

3) Subagent: Smallest Signal Commands Scout (read-only)
   - Task: find the smallest existing checks relevant to the plan (tests/typecheck/lint/build) and propose a minimal per-phase signal.
   - Output format (bullets only):
     - <phase candidate> — <command> — <signal>

4) Subagent: Risk Hotspots Finder (optional; read-only; best at LEVEL>=4)
   - Task: find boundaries likely to require extra task splitting (concurrency, caching, global state, data migrations, risky refactors).
   - Output format (bullets only):
     - <area> — <anchor> — <why risky> — <suggested splits>

Integrate subagent results into Phase Plan microtasks. If subagents disagree, resolve by reading code (do not ask the user).

### 5) Rewrite the Phase Plan in-place (single SSOT)
Same rewrite rules as the non-agent prompt, with two emphasis points:
- Make call-site batches explicit (especially at LEVEL>=3) using the Call-Site Grouper output.
- Make deletes/cleanup explicit (no parallel paths) using the Deletes Inventory output.

Monotonic / re-entrant rule:
- Preserve any completed tasks (`[x]` / `[X]`) verbatim.
- Prefer refining/splitting only pending tasks, and append new microtasks after existing done tasks.

### 6) Add/update granularize metadata (inside Phase Plan)
Add/update this multi-line HTML comment near the top of the Phase Plan block:

`<!--
arch_skill:phase_plan_granularize
level: <LEVEL>
pass_count: <increment>
last_updated: <YYYY-MM-DD>
-->`


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
- Whether subagents were used and what they contributed (1 sentence)
- What changed (e.g., “phase plan microtasked with explicit call-site batches + deletes + checks”)
- Issues/Risks (if any)
- Next action (usually: proceed to `/prompts:arch-implement-agent DOC_PATH`)
- Need from USERNAME (only if required)
- Pointers (DOC_PATH)

