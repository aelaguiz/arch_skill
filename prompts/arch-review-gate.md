---
description: "09) Review gate: external idiomatic+completeness check."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-review-gate — $ARGUMENTS
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
- This prompt is for documentation and planning only. DO NOT modify code.
- You may read code to answer reviewer questions and ground dispositions.
- Integrate reviewer feedback by updating DOC_PATH (not by changing implementation here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Alignment checks (keep it light before requesting external review)
- North Star: concrete + scoped, with a smallest-credible acceptance signal.
- UX scope: explicit in-scope / out-of-scope (what users see changes vs does not change).
If either is missing or contradictory, pause and ask for a quick doc edit before proceeding.

Reviewer subagents (explicit; keep main context lean)
- Run opus/gemini review via TWO read-only reviewer subagents (one per model) so the main agent stays focused on the plan and dispositions.
- Reviewer subagent rules:
  - Read-only: MUST NOT modify files.
  - No questions: MUST answer from DOC_PATH + repo evidence only.
  - No recursion: MUST NOT spawn other subagents.
  - Output must be short, actionable bullets with evidence anchors (file paths/symbols).
- Provide reviewers enough context to answer (DOC_PATH + the key file anchors/diffs relevant to the plan).
- Ask each reviewer (same question):
  - “Is this idiomatic and complete relative to DOC_PATH? What’s missing? Where does code drift from the plan? Any SSOT/contract violations?”
  - If you suggest tests: suggest only high-signal, refactor-resistant checks. Do NOT suggest negative-value tests (deleted-code proofs, visual-constant/golden noise, doc-driven inventory gates, mock-only interaction tests). If an existing test suite is clearly negative value, call it out and recommend deletion or rewrite.
  - Pattern propagation: are any new SSOTs/contracts or tricky gotchas documented via short, high-leverage code comments at the canonical boundary (without comment spam)?

Request reviews from opus/gemini (via subagents), then integrate feedback you agree with.
Update DOC_PATH before moving to the next phase.
Write/update the Review Gate block into DOC_PATH (anti-fragile placement).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:review_gate:start -->` … `<!-- arch_skill:block:review_gate:end -->`
2) Else, if a "Review Gate" section exists (heading match), update it in place.
3) Else append near the end of the plan doc (before Decision Log if present, otherwise append).
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:review_gate:start -->
## Review Gate
- Reviewers: <opus|gemini>
- Question asked: “Is this idiomatic and complete relative to the plan?”
- Feedback summary:
  - <item>
- Integrated changes:
  - <item>
- Decision: proceed to next phase? (yes/no)
<!-- arch_skill:block:review_gate:end -->

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
