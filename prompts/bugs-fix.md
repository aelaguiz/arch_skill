---
description: "Plan + implement the bug fix, challenge the plan, and update the bug doc with verification."
argument-hint: "<Optional: constraints or priorities. Optional: include a docs/bugs/<...>.md bug doc path.>"
---
# /prompts:bugs-fix — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.
Inputs: $ARGUMENTS is freeform steering. Process it intelligently.

Resolve DOC_PATH:
- If $ARGUMENTS includes a docs/bugs/<...>.md path, use it.
- Otherwise infer the most relevant bug doc; if ambiguous, ask me to pick from the top 2–3 candidates.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2–3 candidates)
  - Missing access/permissions
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.

# COMMUNICATING WITH DEV (IMPORTANT)
- Start console output with a 1 line reminder of our Bug North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH, not in console output.

Read DOC_PATH fully. Treat it as the authoritative spec.

Quick alignment checks (keep it light):
- Bug North Star is concrete and falsifiable.
- Most likely root cause is identified OR a fix-ready hypothesis is explicitly chosen.
If the doc is not fix-ready, stop and recommend running /prompts:bugs-analyze (do not wing it).

Implementation discipline (speed + safety):
- Keep the fix minimal and localized; do not add new abstractions unless clearly needed.
- No-fallback policy (strict; do not propose):
  - Do NOT add “make it feel unbroken” fallbacks (compatibility shims, placeholder values, silent error swallowing, or alternate codepaths) to mask the bug.
  - If an exception is truly required (rare), stop and ask Dev for explicit approval and record it in DOC_PATH (Decision Log / Fix Plan) with a timebox + removal plan.
- Challenge the plan: list 1–3 plausible alternatives and why we are not choosing them.
- Avoid external research unless required to resolve ambiguous framework/library behavior; if needed, confirm the current date first.
- Testing policy: run the smallest relevant check(s) after meaningful changes; avoid “negative-value” tests.
- If DB migrations are required, create them but do NOT apply them; tell Dev to apply.
- Do not commit/push unless explicitly requested.

DOC UPDATE RULES (anti-fragile; do NOT assume section numbers):
1) If block markers exist, replace the content inside them:
   - <!-- bugs:block:fix_plan:start --> … <!-- bugs:block:fix_plan:end -->
   - <!-- bugs:block:implementation:start --> … <!-- bugs:block:implementation:end -->
2) Else update in place if headings include (case-insensitive):
   - “Fix Plan”, “Implementation”, “Verification”
3) Else insert missing top-level sections after “Investigation”.
Update TL;DR/status if it changed.
Do not paste full doc content to the console.
Keep status consistent:
- When status changes, update both YAML front matter `status` and the TL;DR `Status` line.

Fix plan content requirements (concise but complete):
- Proposed fix (minimal)
- Alternatives considered (and why rejected)
- Step-by-step work plan with exit criteria
- Risks / mitigations
- Verification (tests/logs/metrics)
- Rollback / mitigation

Implementation notes requirements:
- What changed (paths + short description)
- Tests run + results
- Manual QA checklist or “n/a”
- Outcome/status (verifying/resolved/blocked)
- Perceived risk level: `very low` | `low` | `medium` | `high` | `very high`
  - `very low`: Changes are small and highly localized in a single, well-understood area; behavior is straightforward and side effects are unlikely.
  - `low`: Changes are still fairly contained, but touch a slightly broader surface area or introduce modest state/timing sensitivity; limited side effects are possible.
  - `medium`: Changes span multiple files/flows or introduce non-trivial state/timing/ordering behavior; regressions are plausible; targeted verification is recommended.
  - `high`: Changes touch core/shared components, widely-used flows, or cross-cutting behavior relied on by other systems; interaction risk is significant; broader verification and evidence are recommended.
  - `very high`: Changes touch critical components across multiple systems and/or involve complex concurrency/migration/state behavior with unknowns; unexpected side effects are likely; intensive testing and evidence gathering are strongly recommended.
  - Include 2–5 bullets explaining why this risk level applies and what mitigations/verifications were (or should be) used.

OUTPUT FORMAT (console only; Dev-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- Bug North Star reminder (1 line)
- Punchline (1 line)
- What you did / what changed
- Tests run + results
- Perceived risk level (and why, briefly)
- Issues/Risks (if any)
- Next action
- Need from Dev (only if required)
- Pointers (DOC_PATH / other artifacts)
