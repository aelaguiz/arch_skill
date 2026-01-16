---
description: "12) Maestro autopilot: run tests, fix flow issues, re-run."
argument-hint: <optional guidance>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Goal: autonomously run Maestro testing and make it stable. Prefer centralized, reusable subflows and avoid one-off fixes.

1) Pick target:
   - If $ARGUMENTS mentions a make target or flow path, use it.
   - Otherwise run `make test-smoke` on iOS first.
2) Run the target. If it fails:
   - Classify: automation instability vs product bug.
   - If product bug: stop and report.
   - If automation instability: fix it **systemically** by refactoring into common subflows, deduping patterns, and preventing drift.
3) Re-run until stable on iOS, then run on Android (unless guidance says iOS‑only or Android‑only).
4) Keep a short work log and note fixes in the relevant doc if one exists.
5) Commit only files you changed; ignore other dirty files. Push if requested.

OUTPUT FORMAT (console only):
Summary:
- Target: <make target or flow>
- iOS result: <pass/fail>
- Android result: <pass/fail or skipped>
- Fixes made: <high-level>
- Product bug found: <yes/no>
Next:
- <what to do next>
