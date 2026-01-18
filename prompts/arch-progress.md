---
description: "10) Phase progress: update worklog (plan only for decisions)."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-progress — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):
- Do NOT ask the user technical questions you can answer by reading code or the plan doc; go look and decide.
- Ask the user only for true product decisions / external constraints not present in the repo/doc.
- The only routine question allowed here is phase disambiguation if the doc/worklog is ambiguous.

Stop-the-line gates (must pass before updating progress)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the plan doc before proceeding.
Derive WORKLOG_PATH from DOC_PATH using the same directory and suffix: `<DOC_BASENAME>_WORKLOG.md`. If missing, create it. Add cross-links: plan doc should reference the worklog near the top; worklog should link back to the plan doc.
Update the worklog with progress for the current phase. If a phase is explicitly provided by the user, use it. Otherwise infer it from the doc (latest “Phase <n> Progress Update” or the most recent phase with incomplete exit criteria). If ambiguous, ask which phase to update.
Add decisions to the plan doc Decision Log only if a real decision was made.
Do not create additional planning docs.
Write the progress update into WORKLOG_PATH. Do not paste the full block to the console.

WORKLOG INSERT FORMAT:
## Phase <n> Progress Update
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

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- Worklog updated: <path>
- Plan updated (decisions only): <yes/no>
Open questions:
- Proceed to next phase? (yes/no)
