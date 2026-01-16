---
description: "06) Phase plan: depth-first implementation plan."
argument-hint: DOC_PATH=<path> (optional)
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
If DOC_PATH is not provided, locate the most relevant architecture doc by semantic match to $ARGUMENTS and the current conversation; prefer the doc that explicitly matches the topic and is most recently updated among relevant candidates. If you cannot determine a clear winner, ask the user to choose from the top 2–3 candidates.
Insert a depth-first phased plan at the top of $DOC_PATH.
Each phase must include: Goal, Work, Test plan, Exit criteria, Rollback.
More phases are better than fewer. Keep them concrete.
Write the phased plan block into $DOC_PATH (insert at top). Do not paste the full block to the console.

DOCUMENT INSERT FORMAT (insert at top):
# 7) Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; every phase has exit criteria + explicit test plan.

## Phase 0 — Baseline gates

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

## Phase 1 — <foundation>

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

## Phase N — <end state + cleanup>

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>
