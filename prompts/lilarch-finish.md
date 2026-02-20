---
description: "lilarch 03) Finish: implement 1–3 phases, then audit completeness + run external code review (write back to DOC_PATH)."
argument-hint: "<Required: docs/<...>.md. Optional: PAUSE=1 to pause between phases. Optional: SKIP_REVIEW=1 to skip external review (not recommended).>"
---
# /prompts:lilarch-finish — $ARGUMENTS
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
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

## Scope guard: lilarch is for 1–3 phases
If DOC_PATH’s phase plan is >3 phases or obviously large/cross-cutting, warn and recommend switching to:
- `/prompts:arch-implement DOC_PATH` (or `arch-implement-agent`)
…then stop unless the user explicitly insists on continuing in lilarch mode.

## Git discipline (important; avoid collateral damage)
- NEVER do implementation work directly on `main` (or the repo’s default branch).
- If you are currently on `main` / `master` (or otherwise not on a feature branch), cut a new branch and continue work there.
  - Branch name: `USERNAME/lilarch-<short-slug>` (derived from DOC_PATH title).

## Worklog (required; lightweight)
- Derive WORKLOG_PATH from DOC_PATH using the same directory and suffix: `<DOC_BASENAME>_WORKLOG.md`.
- If WORKLOG_PATH is missing, create it and add cross-links:
  - Plan doc should reference WORKLOG_PATH near the top (add if missing).
  - Worklog should link back to DOC_PATH at the top.
- Keep the worklog short: phase-boundary notes + commands run + results.

## Implementation rules (carry-over from arch, but condensed)
- Read DOC_PATH fully. Treat it as the authoritative spec.
- No-fallback policy (strict):
  - Do NOT add runtime fallbacks/compat shims/placeholder behavior to emulate correctness.
  - Only allowed if DOC_PATH explicitly sets `fallback_policy: approved` AND there’s a Decision Log entry with a timebox + removal plan.
- Implement systematically, phase-by-phase (depth-first). Keep changes minimal and idiomatic.
- After each meaningful chunk (at least once per phase), run the smallest relevant programmatic signal and record it (tests/typecheck/lint/build).
- Avoid negative-value tests by default (deleted-code proofs, golden/visual-constant noise, doc-driven inventory gates, mock-only interaction tests).
- Pattern propagation via comments (high leverage):
  - If you introduce a new SSOT/contract or discover a tricky gotcha, add a short doc comment at the canonical boundary explaining the invariant and how to extend safely.
  - Do NOT comment everything.

## Optional pausing
If `$ARGUMENTS` includes `PAUSE=1`, then after each phase:
- Write a short worklog entry,
- Summarize what changed + what check you ran,
- Ask the user if you should proceed to the next phase.

## Finish procedure (do this in order)
1) Implement the phase plan in DOC_PATH (1–3 phases), updating WORKLOG_PATH as you go.
2) Self-audit (internal completeness check; no code changes yet):
   - Verify call-site completeness via `rg` (search for old APIs/paths and expected new usage).
   - Verify deletes/cleanup expectations.
   - Verify SSOT (no parallel writers/readers).
3) Record an Implementation Audit block in DOC_PATH (create if missing):

<!-- arch_skill:block:implementation_audit:start -->
# Implementation Audit (authoritative)
Date: <YYYY-MM-DD>
Verdict (code): <COMPLETE|NOT COMPLETE>
Manual QA: <pending|complete|n/a> (non-blocking)

## Code blockers (why code isn’t done)
- <bullets only about missing/incorrect code>

## Missing items (code gaps; evidence-anchored; no tables)
- <area>
  - Evidence anchors:
    - <path:line>
  - Plan expects:
    - <expected>
  - Code reality:
    - <actual>
  - Fix:
    - <fix>

## Non-blocking follow-ups (manual QA / human verification)
- <follow-up item>
<!-- arch_skill:block:implementation_audit:end -->

4) External code review (recommended; skip only if `$ARGUMENTS` includes `SKIP_REVIEW=1`):
   - Hard constraint: DO NOT USE PAL MCP (this is a command-line action).
   - Use a cross-tool reviewer (Claude↔Codex) so this agent gets a second set of eyes.
   - CRITICAL: pipe the prompt (positional args can hang in nested sessions).
   - Detect reviewer CLI:
     - If `CLAUDECODE=1` is set (you are Claude Code): use Codex CLI
       - `codex exec --dangerously-bypass-approvals-and-sandbox`
     - Otherwise: use Claude Code CLI
     - `claude -p --dangerously-skip-permissions`
   - Suggested command pattern:
     ```bash
     if [ "$$CLAUDECODE" = "1" ]; then
       REVIEWER="codex exec --dangerously-bypass-approvals-and-sandbox"
     else
       REVIEWER="claude -p --dangerously-skip-permissions"
     fi
 
     cat <<'REVIEW_EOF' | $$REVIEWER
     You are code reviewing an implementation relative to DOC_PATH="<DOC_PATH>".
     Task:
     - Verify completeness vs the plan (especially call sites + deletes).
     - Verify idiomatic fit to the existing repo (avoid new patterns when existing ones suffice).
     - Flag SSOT violations / parallel paths / hidden fallbacks.
 
     Constraints:
     - Use evidence anchors: file paths / symbols / grep targets.
     - Do NOT suggest negative-value tests (deleted-code proofs, golden/visual-constant noise, doc-driven inventory gates, mock-only interaction tests).
     - Call out any runtime fallbacks/compat shims/placeholder behavior/silent error swallowing/defaulting.
 
     Output:
     1) Verdict: COMPLETE / NOT COMPLETE (and why)
     2) Top risks (ranked)
     3) Concrete fixes (file anchors)
     4) Tests/checks to run (smallest relevant set)
     REVIEW_EOF
     ```
   - Integrate high-confidence feedback you agree with; keep changes minimal and in-scope.
   - If the reviewer CLI is missing/not authenticated, report that as the blocker and proceed with a stricter self-audit (do not invent a new review mechanism).
5) Run the smallest relevant checks again after integrating review feedback.
6) If code is complete, update DOC_PATH frontmatter `status:` → `complete`.

OUTPUT FORMAT (console only; USERNAME-style):
Communicate naturally in English, but include (briefly):
- North Star reminder (1 line)
- Punchline (1 line; what state we’re in: implemented vs not complete)
- What you implemented + checks you ran (short)
- Any remaining gaps (if NOT COMPLETE) and where they live (file anchors)
- Whether external review ran (and the top 1–2 findings)
- Pointers (DOC_PATH / WORKLOG_PATH)
