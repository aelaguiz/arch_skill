---
description: "00) Ramp-up: read plan doc + referenced code before acting."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-ramp-up — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):
- Do NOT ask the user technical questions you can answer by reading code or the plan doc; go look and decide.
- Ask the user only to disambiguate which doc to use (top 2–3 candidates) or for true external constraints not present anywhere in the repo/doc.
Derive WORKLOG_PATH from DOC_PATH using the same directory and suffix: `<DOC_BASENAME>_WORKLOG.md`. If missing, report that it does not exist.
Read DOC_PATH fully. Extract: current phase, completed phases, in-progress items, open questions, and Decision Log context.
If WORKLOG_PATH exists, read it and include key execution notes + latest phase progress summary.
Read all relevant code referenced by the doc (Internal Ground Truth anchors, Call-Site Audit table, target/current architecture sections). If anchors are missing, locate likely modules by searching the repo for the key symbols named in the doc.
Do not modify code or the document. Prepare to take action with the full context of what is already done.

OUTPUT FORMAT (console only):
Summary:
- Doc: <path> -- status: <draft|active|complete> -- current phase: <phase>
- Worklog: <path> -- status: <found|missing>
- What's done:
  - <item>
- In progress:
  - <item>
- Relevant code reviewed:
  - <path>
Readiness:
- Ready to proceed? (yes/no)
- Blockers / missing context:
  - <item>
Open questions:
- <question>
