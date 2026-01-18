---
description: "05a) ASCII chart: visualize current topic or pipeline."
argument-hint: <guidance>
---
# /prompts:arch-ascii — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Use the freeform guidance in $ARGUMENTS to decide what to visualize. If a docs/<...>.md path appears in $ARGUMENTS, read it and use its current/target architecture or phase plan as the source of truth. If no doc is provided, infer from the current conversation and $ARGUMENTS; if multiple docs are plausible, ask the user to choose.
Do not modify any files. Output a simple, readable ASCII chart (60-100 cols). Prefer a single diagram. Keep labels short. Avoid ornate boxes.

OUTPUT FORMAT (console only):
Title: <short title>
```ascii
<diagram>
```
