---
description: "10) Phase progress: update worklog (plan only for decisions)."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-progress — $ARGUMENTS
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
- This prompt only updates docs (WORKLOG_PATH, and Decision Log in DOC_PATH if needed). DO NOT modify code.
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Alignment checks (keep it light before updating progress)
- North Star: concrete + scoped, with a smallest-credible acceptance signal.
- UX scope: explicit in-scope / out-of-scope (what users see changes vs does not change).
If either is missing or contradictory, pause and ask for a quick doc edit before proceeding.
Derive WORKLOG_PATH from DOC_PATH using the same directory and suffix: `<DOC_BASENAME>_WORKLOG.md`. If missing, create it. Add cross-links: plan doc should reference the worklog near the top; worklog should link back to the plan doc.
Update the worklog with progress for the current phase. If a phase is explicitly provided by the user, use it. Otherwise infer it from the doc (latest “Phase <n> (<phase name>) Progress Update” or the most recent phase with incomplete exit criteria). If ambiguous, ask which phase to update.
Add decisions to the plan doc Decision Log only if a real decision was made.
Do not create additional planning docs.
Write the progress update into WORKLOG_PATH. Do not paste the full block to the console.

WORKLOG INSERT FORMAT:
## Phase <n> (<phase name>) Progress Update
- Work completed:
  - <item>
- Tests run + results:
  - <command> — <result>
- Issues / deviations:
  - <issue>
- Next steps:
  - <step>

PLAN DOC DECISION LOG (only if needed):
## Decision Log (append-only)
## <YYYY-MM-DD> — <decision title>
- Context:
- Options:
- Decision:
- Consequences:
- Follow-ups:

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
