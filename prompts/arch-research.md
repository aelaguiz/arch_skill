---
description: "03) Research grounding: external + internal anchors."
argument-hint: DOC_PATH=<path> (optional)
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
If DOC_PATH is not provided, locate the most relevant architecture doc by semantic match to $ARGUMENTS and the current conversation; prefer the doc that explicitly matches the topic and is most recently updated among relevant candidates. If you cannot determine a clear winner, ask the user to choose from the top 2–3 candidates.
Fill the Research Grounding section in $DOC_PATH.
- External anchors: what to adopt vs reject.
- Internal ground truth: file paths + behaviors.
- Open questions + evidence needed.
Write the Research Grounding block into $DOC_PATH (replace section 3 in-place). Do not paste the full block to the console.

DOCUMENT INSERT FORMAT (replace section 3 in-place):
# 3) Research Grounding (external + internal “ground truth”)
## 3.1 External anchors (papers, systems, prior art)
- <source> — <what we borrow / what we reject> — <why it applies>

## 3.2 Internal ground truth (code as spec)
- **Authoritative behavior anchors (do not reinvent):**
  - `<path>` — <what it defines>
- **Existing patterns we will reuse:**
  - `<path>` — <pattern>

## 3.3 Open questions from research
- Q1:
- Q2:
- What evidence would settle them:

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>
