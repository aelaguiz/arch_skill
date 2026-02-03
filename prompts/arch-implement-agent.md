---
description: "11a) Implement (agent-assisted): ship the plan end-to-end using subagents for code + tests to keep main context lean."
argument-hint: "<Optional: paste symptoms/constraints. Optional: include a docs/<...>.md path anywhere to pin the plan doc.>"
---
# /prompts:arch-implement-agent — $ARGUMENTS
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

Git discipline (important; avoid collateral damage):
- NEVER do implementation work directly on `main` (or the repo’s default branch).
- If you are currently on `main` / `master` (or otherwise not on a feature branch), immediately cut a new branch from `origin/main` and continue work there.
  - If local state prevents a clean branch-off, create the branch first, then reconcile with `origin/main` once safe (merge/rebase as appropriate).

# COMMUNICATING WITH USERNAME (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Subagents (agent-assisted implementation; keep main context lean)
- Use subagents to keep implementation detail + test logs out of the main agent context.
- Shared environment rule: only ONE code-writing subagent at a time.
- Parallel subagents are allowed ONLY for read-only work (e.g., call-site scanning), and must not write files.
- Subagent ground rules:
  - No questions: subagents must answer from repo/doc evidence only.
  - No recursion: subagents must NOT spawn other subagents.
  - No commits: subagents must NOT commit/push; main agent handles final git operations.
  - No log spam: subagents must NOT paste long logs/diffs to the console; write details into WORKLOG_PATH and return a short summary.
  - Do not spam/poll subagents with “are you done?”; wait for completion, then integrate.
  - Close subagents once their results are captured. If a subagent is mis-scoped, interrupt/redirect sparingly.

Agent-assisted execution loop (main agent):
- Read DOC_PATH and identify the next phase in order.
- For each phase: spawn a Phase Implementer subagent with a tight scope, wait, review summary, merge/adjust docs, then close.
- Continue phase-by-phase until the plan is complete (unless blocked by a key invariant or missing external decision).

Spawn subagents as needed (disjoint scopes):
1) Subagent: Phase Implementer (write-capable; ONE phase only)
   - Task: implement exactly one phase from DOC_PATH (Phase <n> (<descriptor>)). Do not start the next phase.
   - Constraints:
     - Touch only the code required for that phase + any required compilation fallout.
     - Keep SSOT real (no parallel paths). Perform required deletes/cleanup for the phase.
     - Run the smallest relevant check for this phase (per DOC_PATH) and record results.
     - Update DOC_PATH + WORKLOG_PATH to reflect what was done and what was checked.
     - Do NOT ask the user technical questions; search the repo and decide.
     - Do NOT paste logs/diffs; write details to WORKLOG_PATH and return summary only.
   - Output format (summary only):
     Summary:
     - Phase: Phase <n> (<descriptor>)
     - Touched files:
       - <path>
     - Key changes:
       - <bullet>
     - Checks run:
       - <command> — <result>
     - Docs/worklog updated: <yes/no>
     - Status: <done|blocked>
     - Blockers (if any):
       - <evidence anchor>

2) Subagent: Test Runner (optional; log-heavy; no code edits)
   - Task: run the final test sweep specified in DOC_PATH (and only that), summarize results, and write them into WORKLOG_PATH.
   - Constraints:
     - Do NOT modify code.
     - Do NOT paste full logs; only summary + failing command + 3-5 key lines if needed.
   - Output format (summary only):
     Summary:
     - Commands run:
       - <command> — <result>
     - Failures (if any):
       - <short> — <evidence anchor>
     - WORKLOG_PATH updated: <yes/no>


Quick alignment checks (keep it lightweight)
- North Star: concrete + scoped, with a smallest-credible acceptance signal (prefer existing checks).
- UX scope: explicit in-scope / out-of-scope (what users see changes vs does not change).
If either is missing or contradictory, pause and ask for a quick doc edit before making code changes.

Read DOC_PATH fully. Treat the doc as the authoritative spec and checklist.

Warn-first preflight (recommended planning pass sequence; do NOT hard-block)
- Recommended flow before phase plan and implementation:
  1) Deep dive (pass 1): current/target architecture + call-site audit
  2) External research grounding (best practices where applicable)
  3) Deep dive (pass 2): integrate external research into target architecture + call-site audit
- Before executing any code changes, check DOC_PATH for the planning passes marker:
  - `<!-- arch_skill:block:planning_passes:start -->` … `<!-- arch_skill:block:planning_passes:end -->`
  - If present: use it to determine which passes are done.
  - If missing: infer from doc contents (deep dive blocks / external research block), but treat deep dive pass 2 as unknown.
- If the recommended sequence is incomplete or unknown, DO NOT stop. Proceed, but:
  - Print a clear warning in the Summary (missing items + recommended next prompts).
  - Continue to respect North Star + UX scope; do not “wing it.”

Implementation discipline (optimize for steady execution, not ceremony):
- Stay aligned (simple):
  - At phase boundaries, re-check the North Star + UX scope + invariants in DOC_PATH.
  - If the plan needs sequencing tweaks, update DOC_PATH (Decision Log entry) and keep going unless it changes user-facing scope or requires a product decision.
- Implement SYSTEMATICALLY: follow the phased plan (or the plan’s checklist) in order.
- Check as you go: after each meaningful chunk (at least once per phase), run the smallest relevant *programmatic* signal (tests/typecheck/lint/build, or targeted instrumentation/log signature) and record the result.
- Verification policy (autonomy-first):
  - Prefer existing checks over building bespoke harnesses/DSLs; add only minimal tests/instrumentation that directly prevent a likely regression.
  - Defer manual verification and UI automation (sim/maestro flows) to **Finalization** by default. Keep a short checklist of what needs UI confirmation and keep moving.
  - Testing discipline (value-driven; avoid negative-value tests):
    - Default: do NOT add new tests if compile/typecheck/lint + existing targeted checks already give enough confidence.
    - Write tests only when they buy real confidence (e.g., bug regression, new logic/state transitions, or user-facing interaction behavior).
    - Do NOT write “proof” tests that:
      - assert deleted code isn’t referenced (use compiler/typecheck + repo search instead),
      - assert visual constants (colors/margins/pixels) or add golden sets unless the repo already has a stable golden discipline,
      - enforce doc inventories via tests (doc-driven gates),
      - only verify mocks/interactions with no behavior assertions,
      - require `Future.delayed()` or timing hacks.
    - If an existing negative-value test is blocking the PR, prefer deleting it or rewriting it to a behavior-level assertion (record the rationale + what replaced it).
  - Pattern documentation via comments (propagation; high leverage):
    - When you introduce a new SSOT/contract, or you discover a non-obvious gotcha, add a short doc comment at the canonical boundary module explaining:
      - what it owns (SSOT),
      - the invariant(s) that must not be broken,
      - the sharp edge / “looks equivalent but isn’t” trap,
      - how to extend safely.
    - Do NOT comment everything; prefer a few crisp comments in the places future engineers will grep first.
- Keep the doc current: update DOC_PATH as you go to reflect real progress, phase completion, and any plan drift you discover.
  - If the plan drifts, update the plan doc and add a Decision Log entry (append-only).
  - If a phase is complete, mark it complete in the doc (do not leave the doc ambiguous).
- Avoid blinders: if you introduce/upgrade a centralized pattern (SSOT/primitives/contracts), scan for other call sites that should adopt it to prevent drift.
  - If it's clearly in-scope, do it (no question).
  - If it expands UX scope or meaningfully expands work, do NOT expand scope:
    - Record it as a follow-up candidate (with file paths/symbols + why) and continue.
    - Only stop+ask if the plan’s scope/North Star is internally contradictory (i.e., required work is declared out-of-scope).

Worklog (lightweight; keep it short):
- Derive WORKLOG_PATH from DOC_PATH using the same directory and suffix: `<DOC_BASENAME>_WORKLOG.md`.
- If WORKLOG_PATH is missing, create it and add cross-links:
  - Plan doc should reference WORKLOG_PATH near the top (add if missing).
  - Worklog should link back to DOC_PATH at the top.
- When creating WORKLOG_PATH, initialize it with a minimal header + first entry (keep it short; avoid writing a second plan doc).
- Append short progress updates there at phase boundaries (or when something changes).

Preferred worklog insert format:
## Phase <n> (<phase name>) Progress Update
- Work completed:
  - <item>
- Tests run + results:
  - <command> — <result>
- Issues / deviations:
  - <issue>
- Next steps:
  - <step>

Stop conditions (do not plow ahead):
- If a key invariant fails: stop, fix immediately, and re-run the smallest check that catches the issue.
- If a real blocker prevents progress: stop and report with evidence anchors (file paths, logs, failing test).

Finish criteria:
- All phases / checklist items are complete and the North Star is satisfied.
- The doc reflects reality: no “done” claims without evidence.

Finalization (after implementation is complete):
1) Run a final test sweep appropriate to the plan (tests listed in the doc + any standard repo checks).
2) Run UI verification at the end (do not gate mid-implementation):
   - If UI automation exists (e.g., Maestro), run it now and record results.
   - Otherwise, provide a short manual checklist (screens/states to confirm) and mark it as pending if you can’t run it yourself.
3) Get a code review from opus/gemini (via read-only reviewer subagents; keep main context lean):
   - Explicit question: “Is this complete and idiomatic relative to the plan?”
   - Reviewer subagent rules:
     - Read-only: MUST NOT modify files.
     - No questions: MUST answer from DOC_PATH + repo evidence only.
     - No recursion: MUST NOT spawn other subagents.
     - Output must be short, actionable bullets with evidence anchors (file paths/symbols).
   - Provide ALL context they need (plan doc + key code paths + diffs).
   - Integrate feedback you agree with; do not scope creep.
4) Commit and push AFTER review (unless the user explicitly requested a different sequence).
   - Stage only files you touched; ignore other dirty files.

OUTPUT FORMAT (console only; USERNAME-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line)
- What you did / what changed
- Issues/Risks (if any)
- Next action
- Need from USERNAME (only if required)
- Pointers (DOC_PATH / WORKLOG_PATH / other artifacts)
