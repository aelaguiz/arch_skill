---
description: "13) Maestro rerun last: re-run most recent failed flow."
argument-hint: <optional guidance>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Find the most recent Maestro run under logs/maestro/**. If it failed, re-run the same target with the same platform/device settings. If no failure is found, run the most recent target once.

OUTPUT FORMAT (console only):
Summary:
- Target: <make target or flow>
- Result: <pass/fail>
Next:
- <what to do next>
