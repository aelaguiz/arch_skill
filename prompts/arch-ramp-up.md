---
description: "00) Ramp-up: read plan doc + referenced code before acting."
argument-hint: DOC_PATH=<path>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Read $DOC_PATH fully. Extract: current phase, completed phases, in-progress items, open questions, and Decision Log context.
Read all relevant code referenced by the doc (Internal Ground Truth anchors, Call-Site Audit table, target/current architecture sections). If anchors are missing, locate likely modules by searching the repo for the key symbols named in the doc.
Do not modify code or the document. Prepare to take action with the full context of what is already done.

OUTPUT FORMAT (console only):
Summary:
- Doc: <path> -- status: <draft|active|complete> -- current phase: <phase>
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
