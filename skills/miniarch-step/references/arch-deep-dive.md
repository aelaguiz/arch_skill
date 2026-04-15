# `deep-dive` Command Contract

## What this command does

- produce or sharpen the current architecture
- fully specify the target architecture
- make the call-site audit exhaustive enough within requested behavior plus required convergence work to drive implementation and later audit
- update the warn-first planning-pass state

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Sections 4, 5, 6, and `planning_passes`

## Reads for alignment

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 1) Key Design Considerations`
- `# 2) Problem Statement`
- `# 3) Research Grounding`
- any existing research grounding

## Writes

- `planning_passes`
- `# 4) Current Architecture (as-is)`
- `# 5) Target Architecture (to-be)`
- `# 6) Call-Site Audit (exhaustive change inventory)`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`

## Hard rules

- docs-only; do not modify code
- code is ground truth
- read code and run read-only searches as needed
- if the North Star, requested behavior scope, allowed architectural convergence scope, or any other plan-shaping decision is contradictory, stop and ask the exact blocker question
- no fallback or shim design unless the plan explicitly approves it
- search for the canonical existing path before proposing a new abstraction or code path
- inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story before treating the obvious path as exhaustive
- compatibility posture is separate from `fallback_policy`; do not leave preservation versus clean cutover implicit in the authoritative plan
- when the change is agent-backed, decide what behavior belongs in prompt or native-capability usage versus deterministic code before designing new tooling
- if the target design does not reuse the canonical path, justify why the existing path cannot own the change
- if the change retires or reroutes a live truth surface, name the code paths, docs, comments, or instructions that must be deleted or rewritten
- if multiple viable technical approaches exist, resolve them from repo truth plus approved intent or ask the user the exact choice; do not leave multiple viable architectures open in the authoritative plan

## Quality bar

- Section 4 must describe current structure, flows, ownership, and failure behavior concretely enough to plan against
- Section 5 must fully specify the future architecture, canonical owner path, contracts, boundaries, SSOT, no-parallel-path stance, and capability-first versus deterministic responsibilities when the system is agent-backed
- Section 6 must be exhaustive enough within approved scope to drive implementation and later audit
- Section 6 must explicitly capture adjacent surfaces that move with the same contract family or are intentionally deferred or excluded
- Section 6 must make compatibility posture explicit enough that later planning does not have to guess whether the plan preserves the contract, cuts over cleanly, or carries an approved bridge
- Section 6 must explicitly capture touched live docs, comments, or instructions that need deletion or rewrite because the change would otherwise leave stale truth behind
- Section 6 must call out capability-replacing harnesses, wrappers, or side paths that should be deleted or explicitly justified when the system is agent-backed
- if the design introduces or sharpens a central pattern, the consolidation sweep must capture only decisions that are already resolved from repo truth or explicit scope text; otherwise it must surface a blocker question
- any required convergence or consolidation work must name the preservation signal that will prove behavior was not broken

## Planning-passes update rule

- ensure the `planning_passes` block exists near the top
- mark:
  - `deep_dive_pass_1: done <YYYY-MM-DD>`
- preserve existing timestamps and never wipe completed fields

## Pattern consolidation sweep

If the design introduces or updates a central pattern, contract family, format surface, lifecycle primitive, or policy boundary:

- look for other places that should adopt it
- capture file paths or symbols
- default dispositions:
  - required to converge onto the same canonical path, keep the same contract family honest, or avoid contradictory sibling surfaces -> include
  - explicitly non-blocking by approved scope text -> defer
  - explicitly out of scope or clearly new product behavior -> exclude
  - if requiredness is still unclear -> ask the user instead of guessing

## Placement and update rules

Update in this order:

1. replace inside markers when they exist:
   - `arch_skill:block:current_architecture`
   - `arch_skill:block:target_architecture`
   - `arch_skill:block:call_site_audit`
2. otherwise update semantically matching sections in place
3. otherwise insert the missing top-level sections after research/problem sections and before phase plan or verification sections

If the doc is canonical, preserve exact headings and numbering for Sections 4, 5, and 6.

Use this call-site section shape:

```text
<!-- arch_skill:block:call_site_audit:start -->
# Call-Site Audit (exhaustive change inventory)

## Change map (table)
| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| <module> | <path> | <fn/cls> | <today> | <diff> | <rationale> | <new usage> | <tests> |

Rows may name non-code surfaces when they participate in the same contract family or migration boundary.

## Migration notes
* Canonical owner path / shared code path:
* Deprecated APIs (if any):
* Delete list (what must be removed; include superseded shims/parallel paths if any):
* Adjacent surfaces tied to the same contract family:
* Compatibility posture / cutover plan:
* Capability-replacing harnesses to delete or justify:
* Live docs/comments/instructions to update or delete:
* Behavior-preservation signals for refactors:

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)
| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude/blocker question) |
| ---- | ------------- | ---------------- | ---------------------- | ------------------------------------- |
| <area> | <path> | <pattern> | <reason> | <include/defer/exclude/blocker question> |
<!-- arch_skill:block:call_site_audit:end -->
```

## Consistency duties beyond local ownership

- if Sections 4 through 6 materially sharpen the design, repair clearly stale TL;DR, Section 0, Section 1, or Section 8 claims that are now wrong
- if the architecture changed in a meaningful way, append or update a Decision Log entry
- if the new target architecture invalidates the current phase plan, say so plainly and point the next move to `phase-plan`

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if the North Star, requested behavior scope, allowed architectural convergence scope, or any other architecture-shaping decision is contradictory or unresolved, stop and ask the exact blocker question
- otherwise stop after Sections 4 through 6 and `planning_passes` are updated for this run

## Console contract

- one-line North Star reminder
- one-line punchline
- what changed in current architecture, target architecture, and call-site audit
- real issues or risks only
- next action
