---
description: "Transform a folder/set of requirements + implementation + feedback docs into a single canonical feature plan doc (example-template format)."
argument-hint: "<Provide one or more paths (files and/or folders). Example: docs/reqs.md docs/impl/ or docs/specs/>"
---
# /prompts:new-arch-from-docs — $ARGUMENTS

Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.

Inputs:
- `$ARGUMENTS` contains either:
  - a list of document paths, and/or
  - a folder path that contains documents (requirements, design notes, implementation notes, review feedback, etc.).
- Treat the input documents as the source of truth. Your job is *reformatting + consolidation*, not inventing new requirements.

Question policy (strict):
- You MUST answer anything discoverable from the provided docs by reading them; do not ask.
- Allowed questions only:
  - Input-path ambiguity (e.g., multiple candidate folders, or no paths provided)
  - A required product/UX decision that is truly missing AND blocks writing a falsifiable North Star
  - Missing access/permissions (can’t read the docs)
- If you think you need to ask, first state what you read/looked at; ask only after exhausting evidence.

Documentation-only:
- This prompt creates/edits docs only. DO NOT modify code.
- You may run read-only searches to understand relationships/references (e.g., `rg` across the provided documents).
- Do not commit/push unless explicitly requested in `$ARGUMENTS`.

## Goal
Given a set of documents describing a feature or set of work (requirements, planning, implementation notes, review/feedback docs, etc.):
1) Analyze and understand them (dedupe, reconcile, and extract the authoritative intent).
2) Transform them into a single new “feature” document that matches the **canonical format** (same structure as `example-template.md` in this prompts folder).
3) Preserve all relevant information (no losing decisions/constraints/edge cases).
4) Replace placeholders with concrete content from the source docs.
5) Produce a single consolidated doc that reorganizes everything into the template sections.
6) Anything that does not map cleanly into an existing section must still be preserved:
   - either placed into an obvious existing section with a clearly labeled subheading, OR
   - placed into a new section titled `Appendix: Unmapped Inputs (labeled)` at the end.

## Procedure (do this in order)
1) Resolve `INPUT_PATHS` from `$ARGUMENTS`.
   - If a folder is provided, recursively include likely doc files (prefer: `.md`, `.txt`, `.mdx`).
   - If both files + folders are provided, include both.
   - If there are zero valid paths, stop and ask the user for the intended paths.
2) Read every input document fully.
   - Build a quick inventory: path → doc “type” guess (requirements / plan / implementation notes / feedback / misc).
   - Extract the “authoritative” statements: goals, scope, constraints, decisions, tradeoffs, acceptance criteria, rollout constraints, telemetry, etc.
3) Derive the new doc’s title and filename:
   - Create the output document in `docs` 
   - Use naming rule:
     - `docs/<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`
     - TITLE_SCREAMING_SNAKE: 5–9 words derived from the feature, uppercased, spaces → `_`, punctuation removed.
   - Date: use today’s date in `YYYY-MM-DD` (no user input required).
4) Write the new consolidated doc using the exact section structure below.
   - Fill every section that has relevant information from the inputs.
   - If a section is truly not applicable, write `n/a` with a short justification (1–2 lines) so the doc is explicit.
   - Never leave `<PLACEHOLDER: ...>` tokens in the final output doc.
   - When information is ambiguous or contradictory across source docs:
     - pick the most recently updated doc *if the docs indicate recency*, otherwise pick the most explicit,
     - record the conflict + your resolution in the Decision Log with citations to source docs.
5) Preserve traceability:
   - Wherever feasible, include “Evidence anchors” using source doc paths (e.g., `From: docs/reqs.md`).
   - Add a final appendix section listing all source docs ingested (and a 1-line summary of each).

## Output (console)
Keep console output short and high-signal:
- One-line purpose summary.
- `OUTPUT_DOC_PATH`.
- Any critical conflicts you resolved (1–3 bullets max).
- Next action (if any).

## DOCUMENT CONTENT FORMAT (write to OUTPUT_DOC_PATH)

---
title: "<Project/Area> — <Feature/Change> — Feature Plan"
date: <YYYY-MM-DD>
status: draft | active | complete
owners: ["<owner or TBD (not provided in source docs)>"]
reviewers: ["<reviewer or TBD (not provided in source docs)>"]
doc_type: architectural_change | parity_plan | phased_refactor | new_system
related:
  - "<links from source docs (PRs/designs/threads)>"
---

Worklog: `<DOC_BASENAME>_WORKLOG.md` (created/maintained during implementation)

# TL;DR
- **Outcome:** <falsifiable outcome>
- **Problem:** <concise problem statement>
- **Approach:** <high-level approach>
- **Plan:** <phases summary>
- **Non-negotiables:** <3–7 bullets>

---

<!-- arch_skill:block:implementation_audit:start -->
# Implementation Audit (authoritative)
Date: <YYYY-MM-DD>
Verdict (code): <COMPLETE|NOT COMPLETE|n/a (pre-implementation)>
Manual QA: <pending|complete|n/a> (non-blocking)

## Code blockers (why code isn’t done)
- <code-only blockers, or “n/a (not implemented yet)”>

## Reopened phases (false-complete fixes)
- <n/a (not implemented yet) OR populated when auditing a shipped change>

## Missing items (code gaps; evidence-anchored; no tables)
- <n/a (not implemented yet) OR gaps with evidence anchors>

## Non-blocking follow-ups (manual QA / screenshots / human verification)
- <manual QA follow-ups (optional)>

## External second opinions
- Opus: <received|pending|n/a>
- Gemini: <received|pending|n/a>
<!-- arch_skill:block:implementation_audit:end -->

---

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: <not started|done YYYY-MM-DD|n/a (converted from existing docs)>
external_research_grounding: <not started|done YYYY-MM-DD|n/a (converted from existing docs)>
deep_dive_pass_2: <not started|done YYYY-MM-DD|n/a (converted from existing docs)>
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This is a warn-first checklist only. It should not hard-block execution.
-->
<!-- arch_skill:block:planning_passes:end -->

---

# 0) Holistic North Star
## 0.1 The claim (falsifiable)
> <If we do X, then Y is true, measured by Z, by date/condition W>

## 0.2 In scope
- UX surfaces (what users will see change):
  - <...>
- Technical scope (what code will change):
  - <...>

## 0.3 Out of scope
- UX surfaces (what users must NOT see change):
  - <...>
- Technical scope (explicit exclusions):
  - <...>

## 0.4 Definition of done (acceptance evidence)
- <acceptance criteria>
- Evidence plan:
  - Primary signal: <existing tests/checks OR log signature OR minimal manual checklist>
  - Optional second signal: <...>
- Metrics / thresholds (if relevant):
  - <metric>: <threshold> — measured via <dash/test/log>

## 0.5 Key invariants (fix immediately if violated)
- <invariants>

---

# 1) Key Design Considerations (what matters most)
## 1.1 Priorities (ranked)
1) <...>
2) <...>
3) <...>

## 1.2 Constraints
- Correctness:
- Performance:
- Offline / latency:
- Compatibility / migration:
- Operational / observability:

## 1.3 Architectural principles (rules we will enforce)
- <...>

## 1.4 Known tradeoffs (explicit)
- <tradeoff> → chosen direction + why
- Alternatives rejected + why

---

# 2) Problem Statement (existing architecture + why change)
## 2.1 What exists today
- <overview>
- Primary flows / control paths:
  - <flow A>
  - <flow B>

## 2.2 What’s broken / missing (concrete)
- Symptoms:
- Root causes (hypotheses):
- Why now:

## 2.3 Constraints implied by the problem
- <...>

---

<!-- arch_skill:block:research_grounding:start -->
# 3) Research Grounding (external + internal “ground truth”)
## 3.1 External anchors (papers, systems, prior art)
- <source> — <adopt/reject + what exactly> — <why it applies>

## 3.2 Internal ground truth (code as spec)
- Authoritative behavior anchors (do not reinvent):
  - `<path>` — <what it defines / guarantees>
- Existing patterns to reuse:
  - `<path>` — <pattern name> — <how we reuse it>

## 3.3 Open questions (evidence-based)
- <question> — <what evidence would settle it>
<!-- arch_skill:block:research_grounding:end -->

---

<!-- arch_skill:block:external_research:start -->
# External Research (best-in-class references; plan-adjacent)
> Goal: anchor the plan in idiomatic, broadly-accepted practices where applicable. This section intentionally avoids project-specific internals.

## Topics researched (and why)
- <topic> — <why it applies>

## Findings + how we apply them
### <Topic A>
- Best practices (synthesized):
  - <...>
- Recommended default for this plan:
  - <...>
- Pitfalls / footguns:
  - <...>
- Sources:
  - <title> — <url> — <why it’s authoritative>

## Adopt / Reject summary
- Adopt:
  - <...>
- Reject:
  - <...>

## Open questions (ONLY if truly not answerable)
- <question> — evidence needed: <...>
<!-- arch_skill:block:external_research:end -->

---

<!-- arch_skill:block:current_architecture:start -->
# 4) Current Architecture (as-is)
## 4.1 On-disk structure
```text
<tree of relevant dirs/files>
```

## 4.2 Control paths (runtime)
- Flow A:
  - Step 1 → Step 2 → Step 3
- Flow B:
  - ...

## 4.3 Object model + key abstractions
- Key types:
- Ownership boundaries:
- Public APIs:
  - `Foo.doThing(args) -> Result`

## 4.4 Observability + failure behavior today
- Logs:
- Metrics:
- Failure surfaces:
- Common failure modes:

## 4.5 UI surfaces (ASCII mockups, if UI work)
```ascii
<ASCII mockups for current UI states, if relevant>
```
<!-- arch_skill:block:current_architecture:end -->

---

<!-- arch_skill:block:target_architecture:start -->
# 5) Target Architecture (to-be)
## 5.1 On-disk structure (future)
```text
<new/changed tree>
```

## 5.2 Control paths (future)
- Flow A (new):
- Flow B (new):

## 5.3 Object model + abstractions (future)
- New types/modules:
- Explicit contracts:
- Public APIs (new/changed):
  - `Foo.doThingV2(args) -> Result`
  - Migration notes:

## 5.4 Invariants and boundaries
- Fail-loud boundaries:
- Single source of truth:
- Determinism contracts (time/randomness):
- Performance / allocation boundaries:

## 5.5 UI surfaces (ASCII mockups, if UI work)
```ascii
<ASCII mockups for target UI states, if relevant>
```
<!-- arch_skill:block:target_architecture:end -->

---

<!-- arch_skill:block:call_site_audit:start -->
# 6) Call-Site Audit (exhaustive change inventory)
## 6.1 Change map (table)
| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| ... | ... | ... | ... | ... | ... | ... | ... |

## 6.2 Migration notes
- Deprecated APIs:
- Compatibility shims (if any):
- Delete list (what must be removed):

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)
| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude) |
| ---- | ------------- | ---------------- | ---------------------- | ------------------------------------- |
| ... | ... | ... | ... | ... |
<!-- arch_skill:block:call_site_audit:end -->

---

<!-- arch_skill:block:phase_plan:start -->
# 7) Depth-First Phased Implementation Plan (authoritative)
> Rule: systematic build, foundational first; every phase has exit criteria + explicit verification plan (tests optional).

## Phase 1 — <foundation>
Status: planned
- Goal:
- Work:
- Verification (smallest signal):
- Exit criteria:
- Rollback:

## Phase N — <end state + cleanup>
Status: planned
- Goal:
- Work:
- Verification (smallest signal):
- Exit criteria:
- Rollback:
<!-- arch_skill:block:phase_plan:end -->

---

# 8) Verification Strategy (common-sense; non-blocking)
## 8.1 Unit tests (contracts)
## 8.2 Integration tests (flows)
## 8.3 E2E / device tests (realistic)

---

# 9) Rollout / Ops / Telemetry
## 9.1 Rollout plan
## 9.2 Telemetry changes
## 9.3 Operational runbook

---

# DevX Targets (optional)
<n/a OR extracted from docs>

---

# Review Gate (optional)
<n/a OR extracted from docs>

---

<!-- arch_skill:block:plan_enhancer:start -->
# Plan Enhancer Notes (authoritative)
<n/a (not run) OR extracted if plan-enhancement docs exist>
<!-- arch_skill:block:plan_enhancer:end -->

---

# Appendix: Source Material (ingested)
- `<path>` — <1-line summary of what this doc contributed>

# Appendix: Unmapped Inputs (labeled)
> Anything that didn’t cleanly map into the template goes here, labeled so it can be re-homed later.
- <label>: <content>

---

# 10) Decision Log (append-only)
## <YYYY-MM-DD> — <decision title>
- Context:
- Options:
- Decision:
- Consequences:
- Follow-ups:

