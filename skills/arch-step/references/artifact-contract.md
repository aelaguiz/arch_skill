# Arch Step Artifact Contract

This artifact is not a loose outline. It is one coherent plan doc that later commands keep sharpening. A command is not successful if it writes its local block but leaves the artifact structurally drifted, internally contradictory, or too vague for the next stage to trust.

## Canonical state objects

- `DOC_PATH`:
  - the one canonical plan doc under `docs/`
  - naming rule for new docs:
    - `docs/<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`
  - derive `TITLE_SCREAMING_SNAKE` from the ask as a short 5-9 word title, uppercased, spaces to `_`, punctuation removed
- `WORKLOG_PATH`:
  - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`
  - progress evidence only, never a second plan

Planning commands update `DOC_PATH` only, except `auto-plan`, which also manages `.codex/auto-plan-state.<SESSION_ID>.json` as controller state. `implement` and `implement-loop` may update code, `DOC_PATH`, and `WORKLOG_PATH`. `audit-implementation` updates `DOC_PATH` only.

## Artifact convergence rule

- `DOC_PATH` is the primary state of the workflow.
- Every command begins by checking whether `DOC_PATH` is canonical enough to support ordinary work.
- Local block ownership never overrides global artifact preservation.
- Preserve exact canonical headings and stable markers when they already exist.
- If a command can safely repair the portion of scaffold it owns, repair it.
- If the doc is materially non-canonical outside that safe boundary, route to `reformat`.
- No command may silently delete, displace, or degrade unrelated canonical sections.
- No command may silently condense instruction-bearing source material in a way that drops operational structure while claiming meaning was preserved.

## Required frontmatter

Canonical docs use this frontmatter shape:

```yaml
---
title: "<PROJECT> - <CHANGE> - Architecture Plan"
date: <YYYY-MM-DD>
status: draft | active | complete
fallback_policy: forbidden | approved
owners: [<name>, ...]
reviewers: [<name>, ...]
doc_type: architectural_change | parity_plan | phased_refactor | new_system
related:
  - <links to docs, PRs, designs, refs>
---
```

Field meaning:

- `title`:
  - readable architecture-plan title, not a slug
- `date`:
  - doc creation date or canonicalized doc date
- `status`:
  - `draft` while TL;DR + Section 0 await confirmation
  - `active` after explicit confirmation
  - `complete` only when the plan and implementation are actually complete
- `fallback_policy`:
  - default `forbidden`
  - only `approved` when an explicit exception is accepted and logged with timebox plus removal plan
- `owners` / `reviewers`:
  - preserve or seed when available evidence supports it
- `doc_type`:
  - classify the plan honestly
- `related`:
  - only real supporting links or materials

## Canonical top-level scaffold

These headings are mandatory in a canonical full doc:

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 1) Key Design Considerations (what matters most)`
- `# 2) Problem Statement (existing architecture + why change)`
- `# 3) Research Grounding (external + internal “ground truth”)`
- `# 4) Current Architecture (as-is)`
- `# 5) Target Architecture (to-be)`
- `# 6) Call-Site Audit (exhaustive change inventory)`
- `# 7) Depth-First Phased Implementation Plan (authoritative)`
- `# 8) Verification Strategy (common-sense; non-blocking)`
- `# 9) Rollout / Ops / Telemetry`
- `# 10) Decision Log (append-only)`

Optional appendices for `reformat`:

- `# Appendix A) Imported Notes (unplaced; do not delete)`
- `# Appendix B) Conversion Notes`

Use Appendix A to retain exact imported instruction-bearing text when it cannot be safely re-homed without loss. Use Appendix B to record any intentional condensation of that content and why the operational meaning still survives.

## Exact section scaffold

### `# TL;DR`

Canonical content shape:

- `Outcome`
- `Problem`
- `Approach`
- `Plan`
- `Non-negotiables`

The TL;DR is the highest-signal truth of the artifact. Later stages should not have to reinterpret what the plan is trying to do.

### `planning_passes`

This warn-first bookkeeping block belongs near the top of the doc:

```text
<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: not started
external_research_grounding: not started
deep_dive_pass_2: not started
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This is a warn-first checklist only. It should not hard-block execution.
-->
<!-- arch_skill:block:planning_passes:end -->
```

Update rules:

- preserve timestamps already present
- never wipe completed fields
- `deep-dive` marks pass 1 or pass 2
- pass 2 may reflect either external-research follow-through or an explicit second architecture-hardening pass such as `auto-plan`
- `external-research` marks `external_research_grounding`

### `# 0) Holistic North Star`

Canonical subsection shape:

- `## 0.1 The claim (falsifiable)`
- `## 0.2 In scope`
- `## 0.3 Out of scope`
- `## 0.4 Definition of done (acceptance evidence)`
- `## 0.5 Key invariants (fix immediately if violated)`

Required content:

- claim that is falsifiable
- explicit requested behavior scope and UX in-scope and out-of-scope surfaces
- explicit technical scope, exclusions, and allowed architectural convergence scope
- when the change is agent-backed, explicit capability-first stance for prompt/native-capability work versus deterministic support tooling
- smallest credible acceptance evidence
- smallest credible behavior-preservation evidence when refactor or consolidation is likely
- invariant list
  - strong examples include `No fallbacks`, `Fail-loud boundaries`, `No dual sources of truth`, and `No undefined behavior`
- strict fallback stance:
  - default no fallbacks or runtime shims
  - only approved exceptions with `fallback_policy: approved` plus Decision Log entry, timebox, and removal plan

### `# 1) Key Design Considerations (what matters most)`

Canonical subsection shape:

- `## 1.1 Priorities (ranked)`
- `## 1.2 Constraints`
- `## 1.3 Architectural principles (rules we will enforce)`
- `## 1.4 Known tradeoffs (explicit)`

Required content:

- ranked priorities
- constraints across correctness, performance, latency, migration, and operations as relevant
- enforceable architectural principles
  - strong examples include fail-loud boundaries, DI rules, no business logic in UI, reuse the canonical path, and no new parallel paths
- high-leverage pattern-propagation comments when introducing a new SSOT, contract, or tricky invariant

### `# 2) Problem Statement (existing architecture + why change)`

Canonical subsection shape:

- `## 2.1 What exists today`
- `## 2.2 What’s broken / missing (concrete)`
- `## 2.3 Constraints implied by the problem`

### `# 3) Research Grounding (external + internal “ground truth”)`

Canonical subsection shape:

- `## 3.1 External anchors (papers, systems, prior art)`
- `## 3.2 Internal ground truth (code as spec)`
- `## 3.3 Open questions from research`

Required content:

- adopt or reject reasoning for external anchors
- authoritative internal behavior anchors with file paths
- canonical owner path or boundary for the requested behavior
- when agent-backed, current prompt surfaces, native model capabilities, and existing tool/file/context exposure relevant to the change
- existing reusable patterns
- duplicate or drifting paths relevant to the change
- existing preservation signals when refactor or consolidation is likely
- evidence-based open questions

### `# 4) Current Architecture (as-is)`

Canonical subsection shape:

- `## 4.1 On-disk structure`
- `## 4.2 Control paths (runtime)`
- `## 4.3 Object model + key abstractions`
- `## 4.4 Observability + failure behavior today`
- `## 4.5 UI surfaces (ASCII mockups, if UI work)`

### `# 5) Target Architecture (to-be)`

Canonical subsection shape:

- `## 5.1 On-disk structure (future)`
- `## 5.2 Control paths (future)`
- `## 5.3 Object model + abstractions (future)`
- `## 5.4 Invariants and boundaries`
- `## 5.5 UI surfaces (ASCII mockups, if UI work)`

Required content:

- future structure
- future control paths
- canonical owner path for the requested behavior
- when agent-backed, explicit split between behavior carried by prompting/native capability use and behavior carried by deterministic code or tooling
- new or changed contracts and APIs
- migration notes where APIs change
- explicit convergence plan for duplicate or drifting paths
- fail-loud boundaries
- single source of truth
- determinism and performance boundaries where relevant

### `# 6) Call-Site Audit (exhaustive change inventory)`

Canonical subsection shape:

- `## 6.1 Change map (table)`
- `## 6.2 Migration notes`

When deep-dive adds consolidation analysis, preserve:

- `## Pattern Consolidation Sweep (anti-blinders; scoped by plan)`

Change-map table columns:

- `Area`
- `File`
- `Symbol / Call site`
- `Current behavior`
- `Required change`
- `Why`
- `New API / contract`
- `Tests impacted`

Migration notes should capture:

- canonical owner path / shared code path
- deprecated APIs if any
- delete list
- live docs/comments/instructions to update or delete
- behavior-preservation signals for refactors
- cleanup and migration notes

### `# 7) Depth-First Phased Implementation Plan (authoritative)`

Canonical heading plus rule line:

```text
# Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; every phase has exit criteria + explicit verification plan (tests optional). Refactors, consolidations, and shared-path extractions must preserve existing behavior with the smallest credible signal. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests (deletion checks, visual constants, doc-driven gates). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).
```

Canonical per-phase fields:

- `Goal`
- `Work`
- `Verification (smallest signal)`
- `Docs/comments (propagation; only if needed)`
- `Exit criteria`
- `Rollback`

For refactor-heavy work, the verification line should say how preserved behavior will be proven.
Use `Docs/comments` for live docs, comments, and instructions that must be updated or deleted so touched truth surfaces match shipped reality. Do not use it to preserve legacy explanation.

The phase plan is the one authoritative execution checklist.

Execution-time progress annotations may be added under a phase heading once implementation begins:

- `Status: IN PROGRESS`
- `Status: COMPLETE`
- `Status: BLOCKED`
- `Status: REOPENED (audit found missing code work)`
- `Completed work:`
- `Deferred:`
- `Blocked on:`
- `Manual QA (non-blocking):`

Keep these additions short and truthful. They are execution truth, not a second checklist.

### `# 8) Verification Strategy (common-sense; non-blocking)`

Principle lines to preserve:

- avoid verification bureaucracy
- prefer the smallest existing signal
- default to 1-3 checks total
- for agent-backed systems, prefer prompt, grounding, and native-capability improvements before new scripts or harnesses
- do not invent new harnesses, frameworks, or scripts unless they already exist and are the cheapest guardrail
- do not invent OCR layers, parser stacks, fuzzy matchers, or wrappers that substitute for native model capability without explicit plan justification
- keep UI/manual verification as finalization by default
- for refactors, prefer behavior-preservation checks that survive restructuring
- do not create proof tests for deletions, visual constants, or doc inventories
- document tricky invariants and gotchas at the SSOT or contract boundary

Canonical subsection shape:

- `## 8.1 Unit tests (contracts)`
- `## 8.2 Integration tests (flows)`
- `## 8.3 E2E / device tests (realistic)`

### `# 9) Rollout / Ops / Telemetry`

Canonical subsection shape:

- `## 9.1 Rollout plan`
- `## 9.2 Telemetry changes`
- `## 9.3 Operational runbook`

### `# 10) Decision Log (append-only)`

Canonical entry shape:

- `## <YYYY-MM-DD> - <decision title>`
- `Context`
- `Options`
- `Decision`
- `Consequences`
- `Follow-ups`

This section is append-only. Do not silently rewrite history when real plan drift occurs.

## Stable block inventory

Keep these markers stable when present:

- `arch_skill:block:planning_passes`
- `arch_skill:block:research_grounding`
- `arch_skill:block:external_research`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `arch_skill:block:phase_plan`
- `arch_skill:block:reference_pack`
- `arch_skill:block:plan_enhancer`
- `arch_skill:block:overbuild_protector`
- `arch_skill:block:review_gate`
- `arch_skill:block:implementation_audit`

If a matching semantic section exists without the marker, update it in place rather than duplicating it.

## Section roles and primary writers

- `# TL;DR`, `# 0)`, `# 1)`, `# 2)`, `# 8)`, `# 9)`, `# 10)`:
  - shared plan spine
  - seeded by `new` and `reformat`
  - later commands may update them only when their contract requires it
- `# 3)`:
  - primary writer: `research`
- `# 4)`, `# 5)`, `# 6)`:
  - primary writer: `deep-dive`
- `# 7)`:
  - primary writer: `phase-plan`
- `External Research` block:
  - primary writer: `external-research`
- helper blocks:
  - primary writers: matching helper commands
- `WORKLOG_PATH`:
  - primary writer: `implement`
- `implementation_audit`:
  - primary writer: `audit-implementation`

Primary ownership does not override global artifact preservation.

## Numbering and placement rules

- If the doc already uses numbered canonical headings, preserve numbering and exact wording.
- Do not renumber the rest of the doc when inserting or replacing sections.
- Update in place when a matching semantic section already exists.
- Prefer stable markers over heading detection.
- Preserve the order of the canonical scaffold.

## Cross-section consistency rules

Treat these as hard checks:

- TL;DR, Section 0, and Section 7 may not disagree on goal, requested behavior scope, allowed convergence scope, or plan shape.
- Section 1 should justify Section 5, not contradict it.
- Section 2 should explain the current reality that Sections 4 and 6 make concrete.
- Section 3 and External Research should sharpen Section 5 and Section 8, not float independently.
- Section 3, Section 5, and Section 6 must agree on the canonical owner path, migrations, deletes, live docs/comments cleanup, and adoption scope.
- Section 7 must be executable from Sections 5 and 6.
- Section 7 phase status lines and `WORKLOG_PATH` should agree about actual progress.
- Section 8 must match the evidence philosophy in Section 0, including preservation checks for refactor-heavy work, and the verification load implied by Section 7.
- Section 9 should stay proportional to the actual rollout and telemetry needs.
- Section 10 records meaningful drift, approvals, and exceptions.

## Full-consistency repair rule

- When a command materially changes architecture, scope, sequencing, verification, rollout, or accepted constraints, it must repair any obvious contradiction it created in adjacent sections before exiting.
- Prefer small truthful repairs over broad rewrites.
- If a prior decision changed in a meaningful way, append a Decision Log entry.
- If the command cannot safely repair the inconsistency inside its scope, it must say so and point to the next required command.

## Minimum health checks before ordinary stage work

- required frontmatter keys exist
- `# TL;DR` exists and is substantive
- `planning_passes` exists near the top
- `# 0) Holistic North Star` exists
- sections `# 1)` through `# 10)` exist with canonical headings
- command-owned blocks exist or can be inserted safely
- dependent sections are strong enough for the command to trust

## North Star confirmation rule

- `new` and `reformat` leave the doc in `status: draft`
- TL;DR and Section 0 must be drafted without placeholders when available evidence allows
- stop for explicit confirmation after bootstrapping
- only after confirmation should `status` move from `draft` to `active`

## Single-document rule

- all planning and decision-making live in `DOC_PATH`
- `WORKLOG_PATH` is execution evidence, not a second plan
- do not create sidecar planning docs
- if instruction-bearing content was intentionally condensed during `reformat` or `fold-in`, the artifact must still retain the exact source text somewhere recoverable

## Write-boundary rule

- `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `auto-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `review-gate`, and `audit-implementation` are docs-only
- `implement` and `implement-loop` are the code-writing commands in this skill
