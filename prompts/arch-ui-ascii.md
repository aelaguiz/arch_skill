---
description: "05) UI ASCII: current-target mockups (if UI)."
argument-hint: DOC_PATH=<path> (optional)
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
If DOC_PATH is not provided, locate the most relevant architecture doc by semantic match to $ARGUMENTS and the current conversation; prefer the doc that explicitly matches the topic and is most recently updated among relevant candidates. If you cannot determine a clear winner, ask the user to choose from the top 2–3 candidates.
If the change touches UI/UX, add ASCII mockups for current and target states in $DOC_PATH.
Keep them contract-level, not illustrative.
Write the ASCII blocks into $DOC_PATH (sections 4.5 and 5.5). Do not paste the full blocks to the console.

DOCUMENT INSERT FORMAT (insert into sections 4.5 and 5.5):
Current UI ASCII:
```ascii
<ASCII mockups for current UI states>
```

Target UI ASCII:
```ascii
<ASCII mockups for target UI states>
```

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>
