# `plan-enhance` Command Contract

## What this command does

- take an existing plan and harden it toward the most fully specified, idiomatic, drift-resistant, faithful-to-intent version of itself
- make SSOT, canonical path ownership, boundaries, deletes, migration obligations, and preservation checks explicit
- leave behind a concrete helper block that sharpens the main artifact without competing with it

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `skills/_shared/scope-and-convergence.md`
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
- treat the frozen Scope and Simplicity Contract as authoritative. Before
  freeze, enhancement may sharpen the smallest evidenced same-contract closure;
  after freeze, imported suggestions and reviewer ideas cannot widen it
- give every proposed addition a finding disposition. Only `authorized` and
  `frozen-convergence-required` may become required plan work automatically
- if consolidation would add product behavior or speculative infrastructure, exclude it only when the approved plan already makes that exclusion explicit; otherwise ask the user instead of downgrading it by taste
- ask only for true product, UX, access, or other plan-shaping gaps that repo evidence cannot settle

## Quality bar

- make SSOT explicit
- name the canonical path that should own the requested behavior
- remove or reject parallel implementations
- make boundaries and invariants explicit in real code, runtime, or API terms
- name required deletes and cleanup
- identify must-change call sites and drift-prone adopters
- identify touched live docs, comments, or instructions that must be deleted or rewritten to current reality
- when agent-backed, identify prompt-first or native-capability-first options before blessing new tooling
- reject repo-policing heuristics such as docs-audit scripts, stale-term greps, absence checks, or CI cleanliness gates unless the user explicitly asked for that tooling class
- name the behavior-preservation checks that make refactors safe
- keep the evidence plan common-sense and separate from the execution checklist
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
- Capability-first path: <prompt/grounding/native capability first; tooling only if justified>
- Is this now decision-complete and faithful to approved intent? <yes/no>
- Biggest remaining risks:
  - <bullets>

## Hard architecture rules (real surfaces only)
- <rules that land in code paths, runtime routing, types, APIs, or real behavior checks; never keyword greps, absence checks, or docs-audit gates>

## Call sites + migration
- Must-change call sites:
  - `<path>` — <symbol> — <why>
- Deletes / cleanup (no parallel paths):
  - `<path>` — <what gets deleted>
- Live docs/comments to delete or rewrite:
  - `<path>` — <delete or rewrite> — <why it would otherwise be stale>

## Consolidation sweep (anti-blinders)
- Other places that should adopt the new central pattern:
  - <area> — Proposed: <include|explicitly out of scope|blocker question> — <why>

## Evidence Planning
- Behavior-preservation checks after refactor:
  - <existing test/check OR new targeted behavior-level check> — <what it proves stayed the same>
- Evidence we'll rely on:
  - <existing test/check OR instrumentation/log signature OR manual checklist> — <what you'll look for>
- What we will not block on:
  - <item such as screen recordings or sim screenshot baselines>

## Blocker questions (ONLY if repo evidence cannot settle them)
- <exact blocker question> — repo evidence checked: <what was checked>
<!-- arch_skill:block:plan_enhancer:end -->
```

## Consistency duties

- if the helper block surfaces a better architecture, sharpen the main plan sections first and use the helper block to record the hardening
- do not let the helper block become a parallel plan or second checklist
- if the helper block finds a simpler way to converge onto an existing path, update the main plan rather than merely praising the idea
- if the verdict exposes a real earlier mistake, record meaningful drift in Section 10
- do not let the helper block invent "optional" or "follow-up" status for required work that has not actually been scoped out by the user or the main artifact

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if the plan has a true product, UX, or other plan-shaping gap that cannot be derived, stop and ask the exact blocker question
- otherwise stop after the plan is hardened and the helper block reflects the upgrades

## Console contract

- one-line North Star reminder
- one-line punchline
- what upgrades were made to the plan
- biggest remaining risks
- next action
