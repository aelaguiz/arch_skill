# `deep-dive` Command Contract

## What this command does

- produce or sharpen the current architecture
- fully specify the target architecture
- make the call-site audit exhaustive enough to drive implementation and later audit
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
- any existing external research

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
- if North Star or UX scope is contradictory, stop for a quick doc correction
- no fallback or shim design unless the plan explicitly approves it
- if multiple viable technical approaches exist, choose the most idiomatic default and note alternatives instead of punting the decision

## Quality bar

- Section 4 must describe current structure, flows, ownership, and failure behavior concretely enough to plan against
- Section 5 must fully specify the future architecture, contracts, boundaries, SSOT, and no-parallel-path stance
- Section 6 must be exhaustive enough to drive implementation and later audit
- if the design introduces or sharpens a central pattern, the consolidation sweep must capture include, defer, or exclude candidates rather than ignoring drift risk

## Planning-passes update rule

- ensure the `planning_passes` block exists near the top
- if external research already exists, mark:
  - `deep_dive_pass_2: done <YYYY-MM-DD>`
- otherwise mark:
  - `deep_dive_pass_1: done <YYYY-MM-DD>`
- preserve existing timestamps and never wipe completed fields

## Pattern consolidation sweep

If the design introduces or updates a central pattern, contract, lifecycle primitive, or policy boundary:

- look for other places that should adopt it
- capture file paths or symbols
- default dispositions:
  - clearly in scope -> include
  - scope expansion -> defer or exclude
  - stop only if the plan is internally contradictory

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

## Migration notes
* Deprecated APIs (if any):
* Delete list (what must be removed; include superseded shims/parallel paths if any):

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)
| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude) |
| ---- | ------------- | ---------------- | ---------------------- | ------------------------------------- |
| <area> | <path> | <pattern> | <reason> | <include/defer/exclude> |
<!-- arch_skill:block:call_site_audit:end -->
```

## Consistency duties beyond local ownership

- if Sections 4 through 6 materially sharpen the design, repair clearly stale TL;DR, Section 0, or Section 1 claims that are now wrong
- if the architecture changed in a meaningful way, append or update a Decision Log entry
- if the new target architecture invalidates the current phase plan, say so plainly and point the next move to `phase-plan`

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if North Star or UX scope is contradictory, stop for a quick doc correction
- otherwise stop after Sections 4 through 6 and `planning_passes` are updated for this run

## Console contract

- one-line North Star reminder
- one-line punchline
- what changed in current architecture, target architecture, and call-site audit
- real issues or risks only
- next action
