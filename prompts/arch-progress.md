---
description: Update canonical architecture doc with execution progress.
argument-hint: DOC_PATH=<path> PHASE=<n>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Update $DOC_PATH with progress for Phase $PHASE.
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
