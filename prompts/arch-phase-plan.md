---
description: "06) Phase plan: depth-first implementation plan."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-phase-plan — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):
- Do NOT ask the user technical questions you can answer by reading code or the plan doc; go look and decide.
- Ask the user only for true product decisions / external constraints not present in the repo/doc, or to disambiguate between multiple equally plausible docs.
- If multiple viable technical approaches exist, pick the most idiomatic default and note alternatives in the doc (do not ask “what do you want to do?”).
You are designing an execution plan. Good implementation planning looks like:
- Depth-first: build foundations first, then migrate callers, then cleanup.
- Small phases: many small phases > a few huge ones.
- Each phase is executable and drift-proof: Goal, Work, Test plan, Exit criteria, Rollback.
- Verification should be common-sense and non-blocking (avoid “proof ladders”):
  - Prefer the smallest existing test/harness; avoid building new harnesses/frameworks unless they will be reused repeatedly.
  - If sim/video/screenshot proof is flaky or slow, use targeted instrumentation + a short manual QA checklist and keep moving; record any pending manual verification explicitly.
- When introducing/upgrading a central primitive (SSOT, lifecycle/motion primitive, layout contract, policy resolver, etc.), include an explicit adoption/migration step for all call sites discovered (or explicitly defer with rationale). Do not create parallel solutions.

Stop-the-line: North Star Gate (must pass before writing the phase plan)
- Falsifiable + verifiable: the North Star states a concrete claim AND how we will prove it (acceptance evidence: tests/harness/instrumentation/manual QA + stop-the-line invariants).
- Bounded + coherent: the North Star clearly states in-scope + out-of-scope and does not contradict the TL;DR/plan.
If the North Star Gate does not pass, STOP and ask the user to fix/confirm the North Star in the doc before proceeding.

Stop-the-line: UX Scope Gate (must pass before writing the phase plan)
- The doc explicitly states UX in-scope and UX out-of-scope: what screens/states/behaviors change vs do NOT change.
- UX scope is coherent with the North Star and does not silently expand.
If the UX Scope Gate does not pass, STOP and ask the user to fix/confirm scope in the doc before proceeding.

Write/update the phased plan block into DOC_PATH (anti-fragile: do NOT assume section numbers match the template).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:phase_plan:start -->` … `<!-- arch_skill:block:phase_plan:end -->`
2) Else, if the doc already contains a section whose heading includes "Phase Plan" or "Phased Implementation" (case-insensitive), update it in place.
3) Else insert a new top-level phased plan section:
   - Prefer inserting after the Call-Site Audit / Change Inventory section if present,
   - otherwise after Target Architecture,
   - otherwise after Research/Problem sections.
Numbering rule:
- If the doc uses numbered headings ("# 7) ..."), preserve existing numbering; do not renumber the rest of the document.
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)

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
<!-- arch_skill:block:phase_plan:end -->

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>
