# `plan-enhance` Command Contract

## What this command does

- take an existing plan and harden it toward the simplest, most idiomatic, most drift-resistant version of itself
- make SSOT, canonical path ownership, boundaries, deletes, migration obligations, and preservation checks explicit
- leave behind a concrete helper block that sharpens the main artifact without competing with it

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Sections 1, 5, 6, 7, and 8

## Reads for alignment

- the full plan doc
- especially `# 0)`, `# 1)`, `# 5)`, `# 6)`, `# 7)`, and `# 8)`

## Writes

- `arch_skill:block:plan_enhancer`
- the relevant main-plan sections when a better contract is obvious and low-risk to state directly

## Hard rules

- docs-only; do not modify code
- read `DOC_PATH` fully and enough code to make real architectural decisions
- code is ground truth
- do not design fallbacks or compatibility shims by default
- treat requested behavior scope as authoritative; architectural convergence may widen when needed to remove duplicate truth or prevent a new parallel path
- if consolidation would add product behavior or speculative infrastructure, default to follow-up or ignore rather than re-asking scope
- ask only for true product, UX, or access gaps

## Quality bar

- make SSOT explicit
- name the canonical path that should own the requested behavior
- remove or reject parallel implementations
- make boundaries and invariants enforceable
- name required deletes and cleanup
- identify must-change call sites and drift-prone adopters
- name the behavior-preservation checks that make refactors safe
- keep the evidence plan common-sense and non-blocking
- explicitly note where a short boundary comment should live when future drift is likely

## Update rules

Write or update:

- `arch_skill:block:plan_enhancer`

Insert near the end before the Decision Log when possible.

Use this block shape:

```text
<!-- arch_skill:block:plan_enhancer:start -->
# Plan Enhancer Notes (authoritative)

## What I changed (plan upgrades)
- <bullets>

## Architecture verdict
- Canonical owner path: <path or boundary>
- Is this now "best possible by our standards"? <yes/no>
- Biggest remaining risks:
  - <bullets>

## Enforceable rules (drift-proofing)
- <rules we will enforce architecturally, not socially>

## Call sites + migration
- Must-change call sites:
  - `<path>` — <symbol> — <why>
- Deletes / cleanup (no parallel paths):
  - `<path>` — <what gets deleted>

## Consolidation sweep (anti-blinders)
- Other places that should adopt the new central pattern:
  - <area> — Proposed: <include|follow-up|ignore> — <why>

## Evidence (non-blocking)
- Behavior-preservation checks after refactor:
  - <existing test/check OR smallest new behavior-level check> — <what it proves stayed the same>
- Evidence we'll rely on:
  - <existing test/check OR instrumentation/log signature OR manual checklist> — <what you'll look for>
- What we will not block on:
  - <item such as screen recordings or sim screenshot baselines>

## Questions (ONLY if truly needed)
- <requested-behavior scope decision> — default recommendation: <recommendation>
<!-- arch_skill:block:plan_enhancer:end -->
```

## Consistency duties

- if the helper block surfaces a better architecture, sharpen the main plan sections first and use the helper block to record the hardening
- do not let the helper block become a parallel plan or second checklist
- if the helper block finds a simpler way to converge onto an existing path, update the main plan rather than merely praising the idea
- if the verdict exposes a real earlier mistake, record meaningful drift in Section 10

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if the plan has a true product or UX gap that cannot be derived, stop with a default recommendation
- otherwise stop after the plan is hardened and the helper block reflects the upgrades

## Console contract

- one-line North Star reminder
- one-line punchline
- what upgrades were made to the plan
- biggest remaining risks
- next action
