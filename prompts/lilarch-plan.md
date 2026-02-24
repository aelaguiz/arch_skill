---
description: "lilarch 02) Plan: deep dive → 1–3 phase plan → internal + external plan audits (write back to DOC_PATH)."
argument-hint: "<Required: docs/<...>.md. Optional: REVIEW=1 to force external review even if the plan seems obvious.>"
---
# /prompts:lilarch-plan — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output should be short and high-signal (no logs); see OUTPUT FORMAT for required content.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.

Resolve DOC_PATH from $ARGUMENTS + the current conversation. If DOC_PATH is ambiguous, ask the user to choose from the top 2–3 candidates.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2–3 candidates)
  - Missing access/permissions
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.

# COMMUNICATING WITH USERNAME (IMPORTANT)
- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH, not in console output.

## Scope guard: lilarch is for 1–3 phases
If the plan expands beyond 3 phases (or clearly needs multiple checkpoints/migrations), warn and recommend switching to:
- `/prompts:arch-flow DOC_PATH FLOW=regular` (or)
- `/prompts:arch-phase-plan DOC_PATH` + `/prompts:arch-implement DOC_PATH`

You may still write what you learned into DOC_PATH, but don’t pretend lilarch-finish is the right tool for a large plan.

Documentation-only (planning):
- This prompt updates DOC_PATH only. DO NOT modify code.
- You may read code and run read-only searches to ground the plan and validate call-site completeness.
- Do not commit/push unless explicitly requested in $ARGUMENTS.

## Goal
In one pass, produce a small-feature plan that is:
- Fully specified enough to implement (no vague “update X somewhere”),
- Idiomatic to the repo (reuse patterns; avoid new abstractions unless necessary),
- Call-site complete (no hidden parallel paths),
- Audited both internally (self-audit) and externally (cross-tool reviewer),
…and record it all in DOC_PATH.

## Procedure (do this in order)
1) Read DOC_PATH fully (North Star + Requirements are authoritative).
2) Deep dive + plan writeback (mini-plan):
   - Confirm internal ground truth anchors + patterns to reuse.
   - Map current architecture and the target architecture (contracts/APIs).
   - Exhaustively enumerate call sites and required deletes/cleanup.
   - Write a 1–3 phase plan with per-phase “smallest signal” verification.
3) Internal plan audit (strict; verify with `rg`):
   - Target architecture fully specified?
   - Idiomatic fit?
   - Call sites audited?
   - If any FAIL/PARTIAL: fix DOC_PATH immediately (within reason) and re-score.
4) External plan audit (required for lilarch; unless blocked by missing reviewer CLI):
   - Run a cross-tool review via the “other agent CLI” (Claude↔Codex).
   - Integrate the feedback you agree with (update DOC_PATH).
5) Stop with a clear “ready to implement” verdict + next command.

## Subagents (optional; read-only only)
Use subagents if the repo surface is large. Do NOT run multiple doc-writing agents against DOC_PATH concurrently.
Suggested subagent scopes (keep it small; lilarch shouldn’t spawn 10 agents):
1) Ground truth + patterns
   - Output bullets only: `<path> — <what it defines> — <evidence>`
2) Call-site sweep + deletes inventory
   - Output bullets only: `<path> — <call site> — <current> — <required>`
3) Tests/fixtures + “smallest signal”
   - Output bullets only: `<command> — <what it proves>`

## Doc blocks to update (compat with arch flow)
Update/insert these blocks in DOC_PATH (anti-fragile placement; do NOT assume section numbers match):
- `<!-- arch_skill:block:research_grounding:start --> … end -->`
- `<!-- arch_skill:block:current_architecture:start --> … end -->`
- `<!-- arch_skill:block:target_architecture:start --> … end -->`
- `<!-- arch_skill:block:call_site_audit:start --> … end -->`
- `<!-- arch_skill:block:phase_plan:start --> … end -->`

Use these exact block marker shapes (copy/paste safe):

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
<!-- arch_skill:block:current_architecture:end -->

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
<!-- arch_skill:block:target_architecture:end -->

<!-- arch_skill:block:call_site_audit:start -->
# Call-Site Audit (exhaustive change inventory)

## Change map (table)
| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| <module> | <path> | <fn/cls> | <today> | <diff> | <rationale> | <new usage> | <tests> |

## Migration notes
* Deprecated APIs (if any):
* Delete list (what must be removed; include legacy shims/parallel paths if any):
<!-- arch_skill:block:call_site_audit:end -->

<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; every phase has exit criteria + explicit verification plan (tests optional). No fallbacks/runtime shims — the system must work correctly or fail loudly (delete legacy paths). Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests (deletion checks, visual constants, doc-driven gates).

## Phase 1 — <main change>
* Goal:
* Work:
* Verification (smallest signal):
* Docs/comments (propagation; only if needed):
* Exit criteria:
* Rollback:

## Phase 2 — <cleanup / deletes / consolidation> (optional)
* Goal:
* Work:
* Verification (smallest signal):
* Docs/comments (propagation; only if needed):
* Exit criteria:
* Rollback:
<!-- arch_skill:block:phase_plan:end -->

## Internal plan audit writeback (lilarch block)
Write/update this block near the top (after TL;DR if present; otherwise after YAML front matter):

<!-- lilarch:block:plan_audit:start -->
# Lilarch Plan Audit (authoritative)
Date: <YYYY-MM-DD>
Verdict: <PASS|PARTIAL|FAIL>

## Big 3 (non-negotiable)
- Target architecture fully specified: <PASS|PARTIAL|FAIL> — <why>
- Idiomatic fit to repo: <PASS|PARTIAL|FAIL> — <why>
- Call sites audited (exhaustive): <PASS|PARTIAL|FAIL> — <why> (include the `rg` evidence you used)

## Fixes applied in this pass
- <what you tightened in the doc>

## Remaining blockers / questions (must answer before `lilarch-finish`)
- <blocker>
<!-- lilarch:block:plan_audit:end -->

## External plan audit (cross-tool; no PAL MCP)
Hard constraint: DO NOT USE PAL MCP (this is a command-line action).
Detect which agent you’re running in and use the OTHER tool for the review:
- If `CLAUDECODE=1` is set (you are Claude Code): use Codex CLI
  - `codex exec --dangerously-bypass-approvals-and-sandbox`
- Otherwise: use Claude Code CLI
  - `claude -p --dangerously-skip-permissions`

Run an external plan review prompt that:
- Reads DOC_PATH,
- Checks completeness/idiomatic fit/call-site completeness,
- Calls out anything too vague to safely implement,
- Avoids recommending negative-value tests (deleted-code proofs, visual-constant/golden noise, doc-driven inventory gates, mock-only interaction tests),
- Flags any runtime fallback/shim suggestions as unacceptable unless explicitly approved.

Suggested review command pattern (pipe prompt; do NOT pass positional args):
```bash
if [ "$$CLAUDECODE" = "1" ]; then
  REVIEWER="codex exec --dangerously-bypass-approvals-and-sandbox"
else
  REVIEWER="claude -p --dangerously-skip-permissions"
fi

cat <<'REVIEW_EOF' | $$REVIEWER
You are reviewing a small-feature plan doc at DOC_PATH="<DOC_PATH>".
Task: audit the plan for implementability and idiomatic fit.
Requirements:
- Be direct and actionable.
- Use evidence anchors: file paths / symbols you referenced.
- Focus on: (1) missing specs, (2) call-site misses, (3) parallel paths/SSOT risks, (4) plan phases too big or out-of-order, (5) minimal verification suggestions.
- Do NOT suggest negative-value tests (deleted-code proof, golden/visual-constant noise, doc-driven inventory gates, mock-only interaction tests).
Output:
1) Verdict: PASS / PARTIAL / FAIL (and why)
2) Top risks (ranked)
3) Specific doc edits to make (bullets; quote the headings to update)
4) Any repo patterns to reuse (with file anchors)
REVIEW_EOF
```

Integrate the feedback you agree with:
- Update DOC_PATH (tighten missing specifics; adjust phases; add call sites; add deletes).
- Record the review in the existing `arch_skill:block:review_gate` block (create it if missing) using this format:

<!-- arch_skill:block:review_gate:start -->
## Review Gate
- Reviewers: external (cross-tool)
- Question asked: “Is this plan implementable and idiomatic relative to the repo?”
- Feedback summary:
  - <item>
- Integrated changes:
  - <item>
- Decision: proceed to next phase? (yes/no)
<!-- arch_skill:block:review_gate:end -->

OUTPUT FORMAT (console only; USERNAME-style):
Communicate naturally in English, but include (briefly):
- North Star reminder (1 line)
- Punchline (1 line)
- What you updated in DOC_PATH (which blocks)
- Any “too big for lilarch” warning (if applicable)
- Plan audit verdict (PASS/PARTIAL/FAIL) + the 1–2 key remaining blockers (if any)
- Next action (usually: `/prompts:lilarch-finish DOC_PATH`)
