---
description: "14) Maestro kill: stop stuck maestro runs."
argument-hint: <optional guidance>
---
# /prompts:maestro-kill — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Find running Maestro processes and stop them cleanly. If multiple are running, stop all. Confirm no Maestro processes remain.

OUTPUT FORMAT (console only):
Summary:
- Killed: <process list or count>
- Remaining: <none or list>
Next:
- <what to do next>
