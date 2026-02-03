---
description: "05) Mini plan (agent-assisted): research + deep dive + phase plan in one pass (small tasks)."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-mini-plan-agent — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output should be short and high-signal (no logs); see OUTPUT FORMAT for required content.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2-3 candidates.
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

What this prompt is for (mini workflow):
- This is the "mini" planning pass for smaller tasks where you want to combine:
  - Research grounding (internal anchors/patterns + optional external anchors),
  - Deep dive (current + target architecture + call-site audit),
  - Phase plan (depth-first plan with minimal verification bureaucracy),
  into ONE prompt.
- It should still produce the same canonical arch_skill blocks as the full flow. It just does more per prompt.

Documentation-only (planning):
- This prompt is for documentation and planning only. DO NOT modify code.
- You may read code and run read-only searches to ground the plan.
- If you discover code changes we likely need, capture them in DOC_PATH (call-site audit + phase plan), with file anchors (do not implement them here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Alignment checks (keep it light, but real)
- North Star: concrete + scoped claim, with a smallest-credible acceptance signal (prefer existing checks).
- UX scope: explicit in-scope / out-of-scope (what users see changes vs does not change).
If either is missing or contradictory, pause and ask for a quick doc edit before proceeding.

Subagents (agent-assisted; use aggressively; read-only only)
- Goal: keep repo-wide scanning and long outputs out of the main agent context.
- Do NOT run multiple doc-writing agents against the same DOC_PATH concurrently. Parallelism should happen inside this prompt via read-only subagents.
- Subagent ground rules:
  - Read-only: subagents MUST NOT modify files or create artifacts.
  - Shared environment: avoid commands that generate/overwrite outputs; prefer pure read/search.
  - No questions: subagents must answer from repo/doc evidence only.
  - No recursion: subagents must NOT spawn other subagents.
  - Output must match the exact format requested (no extra narrative).
  - Do not spam/poll subagents; wait for completion, then integrate.
  - Close subagents once their results are captured.

Spawn subagents as needed (disjoint scopes; read-only; run in parallel):
1) Subagent: Internal Ground Truth + Reusable Patterns
   - Task: find authoritative behavior anchors + existing reusable patterns relevant to this change.
   - Output format (bullets only):
     - Authoritative anchor: <path> — <what it defines/guarantees> — <evidence: symbol/test/comment>
     - Reusable pattern: <path> — <pattern name> — <how it maps to this change>
2) Subagent: Fixtures / Examples / Tests Scan
   - Task: find fixtures/examples/tests that encode behavior relevant to the change. Prefer authoritative tests that prove expectations; avoid adding new harnesses unless necessary.
   - Output format (bullets only):
     - <path> — <what scenario it encodes> — <why it is authoritative>
3) Subagent: Current Architecture Mapper
   - Task: summarize as-is architecture from repo code (tree, control paths, ownership, failure behavior).
   - Output format (sections only):
     On-disk structure:
     <tree>
     Control paths:
     - <flow>
     Object model + key abstractions:
     - <item>
     Observability + failure behavior:
     - <item>
4) Subagent: Call-Site Sweeper
   - Task: enumerate ALL call sites for symbols/APIs implicated by DOC_PATH + any obvious near-neighbors discovered in code. Include both "must change" call sites and "danger: parallel path" call sites.
   - Output format (bullets only):
     - <path> — <symbol/call site> — <why it is a call site> — <current behavior>
5) Subagent: Deletes / Cleanup Inventory (anti-parallel-paths)
   - Task: identify what must be deleted/removed/disabled to avoid parallel paths (old APIs, dead files, old writers/readers, fallback behavior).
   - Output format (bullets only):
     - <path> — <what should be deleted/removed/blocked> — <why>
6) Subagent: Smallest Signal Checks
   - Task: identify the smallest existing checks (tests/typecheck/lint/build) relevant to the change, and propose a minimal per-phase signal.
   - Output format (bullets only):
     - <phase candidate> — <command> — <signal>

Mini-plan philosophy (keep it sharp, not bureaucratic):
- Keep "research" tight: internal anchors + patterns first; external anchors optional (only if this change touches a domain where best practices materially affect correctness).
- Keep architecture "complete enough to ship": explicit contracts/APIs, SSOT clarity, migration + delete list to prevent parallel truth.
- Keep phase plan short: default 1-2 phases plus optional cleanup phase. No sprawling proof ladders. 1-3 checks total unless the repo already makes more checks cheap.

Planning passes block (warn-first; do NOT hard-block)
- If DOC_PATH contains `<!-- arch_skill:block:planning_passes:start -->` … `<!-- arch_skill:block:planning_passes:end -->`, keep it updated.
- If missing, insert a new planning passes block near the top of the doc:
  - Prefer inserting after the TL;DR section if present,
  - otherwise after YAML front matter,
  - otherwise at the top of the document.
- Update rules:
  - This prompt counts as a deep dive planning pass. If external research grounding exists in DOC_PATH, set `deep_dive_pass_2: done <YYYY-MM-DD>`.
  - Otherwise set `deep_dive_pass_1: done <YYYY-MM-DD>`.
  - Do NOT clear other fields (especially `external_research_grounding`).
  - Preserve any existing timestamps if present; update only the field(s) you are completing now.

What you must produce/update in DOC_PATH (same canonical blocks as full flow):
1) Research Grounding block:
   - `<!-- arch_skill:block:research_grounding:start -->` … `<!-- arch_skill:block:research_grounding:end -->`
2) Current Architecture block:
   - `<!-- arch_skill:block:current_architecture:start -->` … `<!-- arch_skill:block:current_architecture:end -->`
3) Target Architecture block:
   - `<!-- arch_skill:block:target_architecture:start -->` … `<!-- arch_skill:block:target_architecture:end -->`
4) Call-Site Audit block:
   - `<!-- arch_skill:block:call_site_audit:start -->` … `<!-- arch_skill:block:call_site_audit:end -->`
5) Phase Plan block:
   - `<!-- arch_skill:block:phase_plan:start -->` … `<!-- arch_skill:block:phase_plan:end -->`

Hard rules (drift-proof, even in mini mode):
- Code is ground truth: every claim is anchored in file paths (include symbols when helpful).
- No competing sources of truth: prefer centralized contracts/primitives; delete/avoid parallel implementations.
- Do not ask the user technical questions you can answer by reading code; go look and decide.
- If multiple viable technical approaches exist, pick the most idiomatic default and note alternatives in the doc (do not ask "what do you want to do?").

Doc update rules (anti-fragile; do NOT assume section numbers match the template)
- Always prefer block markers if present; otherwise update in place by semantically matching headings; otherwise insert new top-level sections.
- Numbering rule:
  - If the doc uses numbered headings ("# 4) ..."), preserve existing numbering; do not renumber the rest of the document.
- Do not paste the full inserted blocks to the console.

DOCUMENT INSERT FORMATS (use these exact block marker shapes; adapt headings to existing numbering)

Planning passes (insert only if missing):
<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: not started
external_research_grounding: not started
deep_dive_pass_2: not started
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
-->
<!-- arch_skill:block:planning_passes:end -->

Research grounding:
<!-- arch_skill:block:research_grounding:start -->
# Research Grounding (external + internal "ground truth")
## External anchors (papers, systems, prior art)
- <source> — <adopt/reject + what exactly> — <why it applies>

## Internal ground truth (code as spec)
- Authoritative behavior anchors (do not reinvent):
  - `<path>` — <what it defines / guarantees>
- Existing patterns to reuse:
  - `<path>` — <pattern name> — <how we reuse it>

## Open questions (evidence-based)
- <question> — <what evidence would settle it>
<!-- arch_skill:block:research_grounding:end -->

Current architecture:
<!-- arch_skill:block:current_architecture:start -->
# Current Architecture (as-is)

## On-disk structure
```text
<tree of relevant dirs/files>
```

## Control paths (runtime)
* Flow A:
  * Step 1 -> Step 2 -> Step 3
* Flow B:
  * ...

## Object model + key abstractions
* Key types:
* Ownership boundaries:
* Public APIs:
  * `Foo.doThing(args) -> Result`

## Observability + failure behavior today
* Logs:
* Metrics:
* Failure surfaces:
* Common failure modes:

## UI surfaces (ASCII mockups, if UI work)
```ascii
<ASCII mockups for current UI states, if relevant>
```
<!-- arch_skill:block:current_architecture:end -->

Target architecture:
<!-- arch_skill:block:target_architecture:start -->
# Target Architecture (to-be)

## On-disk structure (future)
```text
<new/changed tree>
```

## Control paths (future)
* Flow A (new):
* Flow B (new):

## Object model + abstractions (future)
* New types/modules:
* Explicit contracts:
* Public APIs (new/changed):
  * `Foo.doThingV2(args) -> Result`
  * Migration notes:

## Invariants and boundaries
* Fail-loud boundaries:
* Single source of truth:
* Determinism contracts (time/randomness):
* Performance / allocation boundaries:

## UI surfaces (ASCII mockups, if UI work)
```ascii
<ASCII mockups for target UI states, if relevant>
```
<!-- arch_skill:block:target_architecture:end -->

Call-site audit (inventory + anti-drift):
<!-- arch_skill:block:call_site_audit:start -->
# Call-Site Audit (exhaustive change inventory)

## Change map (table)
| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| <module> | <path> | <fn/cls> | <today> | <diff> | <rationale> | <new usage> | <tests> |

## Migration notes
* Deprecated APIs:
* Compatibility shims (if any):
* Delete list (what must be removed):

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)
| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude) |
| ---- | ------------- | ---------------- | ---------------------- | ------------------------------------- |
| <area> | <path> | <pattern> | <reason> | <include/defer/exclude> |
<!-- arch_skill:block:call_site_audit:end -->

Phase plan (mini: keep phases small; include per-phase smallest signal):
<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; every phase has exit criteria + explicit verification plan (tests optional). Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests (deletion checks, visual constants, doc-driven gates). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

## Phase 1 — <main change>

* Goal:
* Work:
* Verification (smallest signal):
* Docs/comments (propagation; only if needed):
* Exit criteria:
* Rollback:

## Phase 2 — <cleanup / deletes / consolidation>

* Goal:
* Work:
* Verification (smallest signal):
* Docs/comments (propagation; only if needed):
* Exit criteria:
* Rollback:
<!-- arch_skill:block:phase_plan:end -->

OUTPUT FORMAT (console only; USERNAME-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line)
- What you did / what changed (doc sections updated)
- Issues/Risks (if any)
- Next action (usually: run /prompts:arch-implement-agent with DOC_PATH)
- Need from USERNAME (only if required)
- Pointers (DOC_PATH / WORKLOG_PATH / other artifacts)
