---
description: "10) Phase progress: update doc + decision log."
argument-hint: DOC_PATH=<path> (optional)
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
If DOC_PATH is not provided, locate the most relevant architecture doc by semantic match to $ARGUMENTS and the current conversation; prefer the doc that explicitly matches the topic and is most recently updated among relevant candidates. If you cannot determine a clear winner, ask the user to choose from the top 2–3 candidates.
Update the doc with progress for the current phase. If a phase is explicitly provided by the user, use it. Otherwise infer it from the doc (latest “Phase <n> Progress Update” or the most recent phase with incomplete exit criteria). If ambiguous, ask which phase to update.
Add decisions to Decision Log.
Do not create additional planning docs.
Write the progress update into $DOC_PATH and append the decision entry to the Decision Log. Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
## Phase <n> Progress Update
- Work completed:
  - <item>
- Tests run + results:
  - <command> — <result>
- Issues / deviations:
  - <issue>
- Next steps:
  - <step>

## Decision Log (append-only)
## <YYYY-MM-DD> — <decision title>
- Context:
- Options:
- Decision:
- Consequences:
- Follow-ups:

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- Proceed to next phase? (yes/no)
