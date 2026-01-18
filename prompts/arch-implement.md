---
description: "11) Implement: ship the plan end-to-end (systematic, test-as-you-go, review gate, commit/push after review)."
argument-hint: "<Optional: paste symptoms/constraints. Optional: include a docs/<...>.md path anywhere to pin the plan doc.>"
---
# /prompts:arch-implement — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):
- Do NOT ask the user technical questions you can answer by reading code, tests, or the plan doc; go look and decide.
- Ask the user only for true product decisions / external constraints not present in the repo/doc, or to disambiguate between multiple plausible plan docs.
- If multiple viable technical approaches exist, pick the most idiomatic default and align to the plan (do not ask “what do you want to do?”).

Stop-the-line gates (must pass before executing the plan)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the plan doc before proceeding.

Read DOC_PATH fully. Treat the doc as the authoritative spec and checklist.

Implementation discipline (optimize for steady execution, not ceremony):
- Refresh discipline (prevent drift):
  - At the start of each phase (and at least every ~30–60 minutes of work), re-read the North Star, UX scope, and stop-the-line invariants in the plan doc.
  - Before starting any new phase, explicitly confirm you are executing the phases in order (no skipping), and that the next work item supports the North Star.
  - If you discover you are out of order or the plan is missing a prerequisite step, STOP and update the plan doc sequencing (Decision Log entry) before continuing.
- Implement SYSTEMATICALLY: follow the phased plan (or the plan’s checklist) in order.
- Test as you go: after each meaningful chunk (at least once per phase), gather the smallest relevant evidence (existing test/harness, targeted instrumentation/log signature, or a quick manual check) and record what it proved.
- Common-sense verification (avoid “proof ladders”):
  - Prefer existing signal over building new harnesses; add only minimal tests/instrumentation that pay off.
  - Do not block the entire plan on flaky sim/video/screenshot steps; if human visual verification is required, add a short manual checklist + clear log/trace signatures and keep moving (record pending QA explicitly in the doc/worklog).
- Keep the doc current: update DOC_PATH as you go to reflect real progress, phase completion, and any plan drift you discover.
  - If the plan drifts, update the plan doc and add a Decision Log entry (append-only).
  - If a phase is complete, mark it complete in the doc (do not leave the doc ambiguous).
- Avoid blinders: if you introduce/upgrade a centralized pattern (SSOT/primitives/contracts), scan for other call sites that should adopt it to prevent drift.
  - If it's clearly in-scope, do it (no question).
  - If it expands UX scope or meaningfully expands work, stop and ask the user to confirm Now vs Next vs Never (scope decision, not a technical question).

Optional worklog (lightweight, not required):
- If `<DOC_BASENAME>_WORKLOG.md` exists, append short progress updates there as you go.
- Do NOT create a new worklog unless the plan doc already references one or the user explicitly asked for it.

Stop conditions (do not plow ahead):
- If a stop-the-line invariant fails: stop, fix immediately, and prove it with a test or evidence.
- If a real blocker prevents progress: stop and report with evidence anchors (file paths, logs, failing test).

Finish criteria:
- All phases / checklist items are complete and the North Star is satisfied.
- The doc reflects reality: no “done” claims without evidence.

Finalization (after implementation is complete):
1) Run a final test sweep appropriate to the plan (tests listed in the doc + any standard repo checks).
2) Get a code review from opus/gemini:
   - Explicit question: “Is this complete and idiomatic relative to the plan?”
   - Provide ALL context they need (plan doc + key code paths + diffs).
   - Integrate feedback you agree with; do not scope creep.
3) Commit and push AFTER review (unless the user explicitly requested a different sequence).
   - Stage only files you touched; ignore other dirty files.

OUTPUT FORMAT (console only):
Summary:
- Doc: <path>
- Worklog: <found|missing|skipped>
- North Star refresh: <done|skipped> — <1 short line: how current work supports North Star>
- Phase order: <in order|out of order fixed> — working on <phase name/number>
- Progress:
  - <what changed>
- Tests run:
  - <command> — <result>
- Status: <complete|in progress|blocked>
- Review: <not started|requested|integrated>
- Commit/push: <not done|done>
Blockers (if any):
- <blocker + evidence anchor>
Next:
- <next action>
