---
description: "02) Phase 1 kickoff: research setup + checkpoints."
argument-hint: DOC_PATH=<path> (optional)
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
If DOC_PATH is not provided, locate the most relevant architecture doc by semantic match to $ARGUMENTS and the current conversation; prefer the doc that explicitly matches the topic and is most recently updated among relevant candidates. If you cannot determine a clear winner, ask the user to choose from the top 2–3 candidates.
We will work out of a single canonical doc at $DOC_PATH.
Start Phase 1 (Research). Ask clarifying questions only if there are multiple viable options or ambiguity.
Summarize research anchors and pause for a lightweight check before Phase 2.
Write the kickoff + summary block into $DOC_PATH (insert after TL;DR, before #0). Do not paste the full block to the console.

DOCUMENT INSERT FORMAT (insert after TL;DR, before #0):
## Phase 1 Kickoff (Research)
- Repo: <current>
- Target doc: <path>
- Assumptions:
  - <list>
- Questions (only if ambiguous):
  - <Q1>
- Plan:
  1) <step>
  2) <step>

## Phase 1 Summary (fill after research)
- Internal anchors:
  - <path> — <behavior>
- External anchors:
  - <source> — <adopt/reject>
- Open questions:
  - <Q> — <evidence needed>

Decision: proceed to Phase 2? (yes/no)

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- Proceed to Phase 2? (yes/no)
- <other open questions, if any>
