# Arch Step Artifact Contract

This artifact is not a loose outline. It is one coherent plan doc that later commands keep sharpening. A command is not successful if it writes its local block but leaves the artifact structurally drifted, internally contradictory, too vague for the next stage to trust, or not decision-complete enough for readiness claims.

Decision-complete means the main artifact has no unresolved plan-shaping decisions left about requested behavior, adjacent surfaces that must stay in sync, compatibility posture, canonical owner path, target architecture, required deletes or migrations, fallback policy, acceptance evidence, required implementation scope, or what must be true to end each planned phase.

## Canonical state objects

- `DOC_PATH`:
  - the one canonical plan doc under `docs/`
  - naming rule for new docs:
    - `docs/<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`
  - derive `TITLE_SCREAMING_SNAKE` from the ask as a short 5-9 word title, uppercased, spaces to `_`, punctuation removed
- `WORKLOG_PATH`:
  - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`
  - progress evidence only, never a second plan

Planning commands update `DOC_PATH` only, except `auto-plan`, which also arms the host-aware controller state for hook-owned later stages: `.codex/miniarch-step-auto-plan-state.<SESSION_ID>.json` in Codex or `.claude/arch_skill/miniarch-step-auto-plan-state(.<SESSION_ID>).json` in Claude Code. For `auto-plan`, `DOC_PATH` remains the planning-progress ledger; the state file is only armed controller state for that doc/session. `implement` and `implement-loop` may update code, `DOC_PATH`, and `WORKLOG_PATH`. `audit-implementation` updates `DOC_PATH` only.

## Artifact convergence rule

- `DOC_PATH` is the primary state of the workflow.
- Every command begins by checking whether `DOC_PATH` is canonical enough to support ordinary work.
- Local block ownership never overrides global artifact preservation.
- Preserve exact canonical headings and stable markers when they already exist.
- If a command can safely repair the portion of scaffold it owns, repair it.
- If the doc is materially non-canonical outside that safe boundary, route to `reformat`.
- No command may silently delete, displace, or degrade unrelated canonical sections.
- No command may silently condense instruction-bearing source material in a way that drops operational structure while claiming meaning was preserved.
- No command may declare the plan ready, complete, or implementation-ready while decision gaps remain in the main artifact.

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
recommended_flow: research -> deep dive -> phase plan -> implement
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions.
-->
<!-- arch_skill:block:planning_passes:end -->
```

Update rules:

- preserve timestamps already present
- never wipe completed fields
- `deep-dive` marks `deep_dive_pass_1`

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
- explicit adjacent-surface scope when the change touches a contract family, source of truth, or migration boundary
- explicit compatibility posture for changed contracts or migration boundaries:
  - preserve the existing contract
  - clean cutover or breaking change allowed
  - approved timeboxed bridge with removal plan
- when the change is agent-backed, explicit capability-first stance for prompt/native-capability work versus deterministic support tooling
- credible acceptance evidence proportional to the work and risk
- credible behavior-preservation evidence when refactor or consolidation is likely
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
  - these must be realizable in shipped code, runtime ownership, types, APIs, or behavior-level checks, not by keyword greps, doc scans, absence checks, or repo-shape policing
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
- `## 3.3 Decision gaps that must be resolved before implementation`

Required content:

- adopt or reject reasoning for external anchors
- authoritative internal behavior anchors with file paths
- canonical owner path or boundary for the requested behavior
- adjacent surfaces tied to the same contract family, source of truth, or migration boundary
- compatibility posture and why it is the right cutover or preservation story
- when agent-backed, current prompt surfaces, native model capabilities, and existing tool/file/context exposure relevant to the change
- existing reusable patterns
- duplicate or drifting paths relevant to the change
- existing preservation signals when refactor or consolidation is likely
- any remaining decision gaps written as explicit blockers or exact user questions

Implementation readiness rule:

- a plan is not ready for `implement` or `implement-loop` while Section `3.3` or any equivalent blocker surface is non-empty
- authoritative sections must not hide unresolved plan-shaping decisions behind conditional wording, alternate branches, or "default recommendation" language

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
- compatibility posture for changed contracts or migration boundaries, separate from `fallback_policy`
- approved bridge shape and removal plan when a bridge is explicitly allowed
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

Rows may include non-code surfaces when they participate in the same contract family, migration boundary, or parity story.

Migration notes should capture:

- canonical owner path / shared code path
- deprecated APIs if any
- delete list
- adjacent surfaces that must move with the same contract or may be explicitly deferred
- compatibility posture / cutover notes
- live docs/comments/instructions to update or delete
- behavior-preservation signals for refactors
- cleanup and migration notes

### `# 7) Depth-First Phased Implementation Plan (authoritative)`

Canonical heading plus rule line:

```text
# Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit and is explanatory only for modern docs. `Checklist (must all be done)` is the authoritative must-do list inside the phase. `Exit criteria (all required)` names the exhaustive concrete done conditions the audit must validate. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Before a phase is valid, run an obligation sweep and move every required promise from architecture, call-site audit, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridges, and required helper follow-through into `Checklist` or `Exit criteria`. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). If a bridge is explicitly approved, timebox it and include removal work; otherwise plan either clean cutover or preservation work directly. Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests and heuristic gates (deletion checks, visual constants, doc-driven gates, keyword or absence gates, repo-shape policing). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).
```

Canonical per-phase fields:

- `Goal`
- `Work`
- `Checklist (must all be done)`
- `Verification (required proof)`
- `Docs/comments (propagation; only if needed)`
- `Exit criteria (all required)`
- `Rollback`

Each phase should own one coherent self-contained unit of work that later phases can build upon directly. Earlier phases should establish the most fundamental primitives, owner paths, contracts, prompt surfaces, or migration prerequisites. If two decompositions are both valid, prefer more phases than fewer.
`Work` describes the unit. For modern docs it must not carry standalone required obligations. `Checklist` is the authoritative must-do list within that phase. `Exit criteria` are exhaustive concrete done conditions, and all of them are required. `Verification` names the proof that must run for the phase claims. If deleting or rewriting live docs/comments/instructions is required for phase completeness, that required work must appear in `Checklist` or `Exit criteria`, not only in `Docs/comments`.
If a required obligation remains visible only in `Work`, `Verification`, `Docs/comments`, migration notes, delete lists, or helper narration, Section 7 is underspecified and not ready for execution.
If the change spans a contract family or migration boundary, the phase plan should encode the chosen adjacent-surface follow-through and the chosen cutover, preservation, or approved-bridge work directly instead of leaving that choice implicit.
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

Keep these additions short and truthful. They are execution truth, not a second checklist. A phase is only complete when every checklist item and every exit criterion is satisfied.

### `# 8) Verification Strategy (common-sense; non-blocking)`

Principle lines to preserve:

- avoid verification bureaucracy
- prefer existing credible signals that genuinely prove the claim
- keep the proof set lean but sufficient
- for agent-backed systems, prefer prompt, grounding, and native-capability improvements before new scripts or harnesses
- do not invent new harnesses, frameworks, or scripts unless they already exist and are the cheapest guardrail
- do not answer "drift resistance" or "enforcement" with docs-audit scripts, stale-term greps, absence checks, repo-structure tests, or CI gates whose main job is policing the tree rather than protecting shipped behavior
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

Additional canonical entry shape for intent-derived resolutions (required whenever the agent resolves a would-be blocker question from approved intent rather than asking the user):

- `## <YYYY-MM-DD> - Intent-derived: <title>`
- `Blocker:` what was unclear or looked like it needed a user question
- `Consulted:` the specific sections read (Section 0 / TL;DR / Section 7.X / other)
- `Intent says:` the relevant constraint, quoted or tightly paraphrased
- `Decision:` what was chosen and why it aligns with approved intent
- `Consequences:` effect on plan or code; any follow-ups

Additional canonical entry shape for user-approved scope cuts (required whenever the user approves narrowing approved scope, acceptance criteria, or a phase obligation):

- `## <YYYY-MM-DD> - Scope cut (user-approved): <title>`
- `Cut:` what was removed, downgraded, or deferred
- `Why it looked necessary:` the real reason
- `Intent evidence checked:` the Section 0 / TL;DR / Section 7 references consulted
- `User approval:` when asked, how the user responded
- `Consequences:` plan updates, follow-ups, any phases reopened

This section is append-only. Do not silently rewrite history when real plan drift occurs. Silent narrowing of approved scope is forbidden; every intent-derived resolution and every approved scope cut must appear here.

## Stable block inventory

Keep these markers stable when present:

- `arch_skill:block:planning_passes`
- `arch_skill:block:research_grounding`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `arch_skill:block:phase_plan`
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
- if instruction-bearing content was intentionally condensed during `reformat`, the artifact must still retain the exact source text somewhere recoverable

## Write-boundary rule

- `new`, `reformat`, `research`, `deep-dive`, `phase-plan`, `auto-plan`, and `audit-implementation` are docs-only
- `implement` and `implement-loop` are the code-writing commands in this skill
