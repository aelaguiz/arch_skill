# Granular Plan Decomposition (Optional) — Prompt Proposal

Date: 2026-02-08  
Scope: `arch_skill` planning docs (`docs/<...>.md`) produced by the **arch flow** prompts (not goal-seeking loops).

## TL;DR

We add an **optional, re-entrant planning prompt** that takes an existing `DOC_PATH` (with a North Star + deep dive + phase plan) and rewrites the existing **Phase Plan** into an **extremely granular, agent-ready execution checklist** (single SSOT; no second plan section):

- More phases than we “need” (micro-phases) so small agents can execute one slice at a time.
- Each task is **specific**: file/symbol anchors, explicit edits, smallest verification signal, and “done” criteria.
- It is **re-entrant and monotonic**: run it multiple times to get more granular each time without duplicating content or thrashing the doc.
- It uses **parallel read-only subagents** to make the checklist grounded in reality (call sites, deletes, commands, existing tests).

Proposed commands:
- `/prompts:arch-phase-plan-granularize DOC_PATH [LEVEL=1..5] [FOCUS=…]`
- `/prompts:arch-phase-plan-granularize-agent DOC_PATH [LEVEL=1..5] [FOCUS=…]` (same output; uses subagents)

---

## Why This Exists

The current `arch_skill` planning flow produces:
- a good North Star,
- grounded architecture + call-site audit,
- a depth-first phase plan.

That is usually “human-executable” and “strong-agent executable”, but it’s not reliably “small-agent executable” because:
- phases are still chunky,
- “migrate all call sites” hides the real work,
- the plan omits the intermediate scaffolding tasks that prevent agents from getting stuck (inventory, grouping, deletes, checks).

This prompt is a **specialized refinement pass**: it turns a plan into **a decomposition tree** whose leaves are loop-sized tasks.

---

## Non-Goals (Explicit)

- This is **not** a goal-seeking loop controller. Do not use on `goal-loop-*` docs.
- This is **not** an architecture redesign prompt (that’s `arch-plan-enhance`).
- This is **not** a replacement for deep dive / call-site audit. It assumes those exist (or warns if missing).
- This prompt does **not** implement code. Planning-only.
- It should not introduce “verification bureaucracy” (no doc-driven gates, no brittle test mandates).

---

## Where It Fits In The arch_skill Flow

Recommended placement (regular flow):
1) `/prompts:arch-research` (or agent)  
2) `/prompts:arch-deep-dive` (or agent)  
3) `/prompts:arch-plan-enhance` (optional, recommended)  
4) `/prompts:arch-phase-plan` (or agent)  
5) `/prompts:arch-fold-in` (optional; if references/specs must be obeyed)  
6) **`/prompts:arch-phase-plan-granularize`** (optional; makes Phase Plan micro-phased + micro-tasked)  
7) `/prompts:arch-implement-agent` (now can drive off microtasks)

Mini flow:
- After `/prompts:arch-mini-plan-agent`, you can run granularize if you want tiny tasks.

Rule: if run “too early” (missing deep dive / phase plan), the prompt should **warn** and proceed with best-effort decomposition, but it must explicitly label low-confidence areas and suggest the missing prompts.

---

## Key Requirements (What “Good” Looks Like)

### 1) Monotonic re-entrancy (run N times; get more granular)

The output must be safe to regenerate and refine:
- Re-running with the same `LEVEL` is idempotent (no diff, or minimal timestamp change).
- Re-running with a higher `LEVEL` refines tasks further.
- Re-running after plan updates reconciles tasks without wiping progress or duplicating sections.

Concrete behavior:
- The Phase Plan remains the single authoritative execution checklist.
- The granularize prompt updates **only** the existing `<!-- arch_skill:block:phase_plan:start --> … end -->` content.
- Optional: store tiny metadata in an HTML comment inside the Phase Plan block for re-entrancy (not a second plan), e.g.:
  - `level: <1..5>`
  - `pass_count: <n>`
  - `last_updated: <YYYY-MM-DD>`

### 2) Specificity is *grounded in repo reality*

The prompt must not just “split bullets”. It must:
- read call-site audit and/or derive call sites from code searches,
- list deletes/cleanup needed to avoid parallel paths,
- name the commands that will act as verification,
- cite file paths/symbols in tasks.

### 3) “Small-agent sized” tasks

Each checkbox should be finishable in one tight loop:
- touches a small set of files (rule of thumb: 1–3),
- has one responsibility,
- has explicit “done” criteria and a smallest verification signal.

If a task can’t be scoped that small, it must be split (by call-site group, by layer, or by a create→migrate→delete pattern).

### 4) Dependency-ordered

Tasks must be ordered so execution is mostly linear:
- foundational SSOT/contracts first,
- then migrate one bounded slice,
- then migrate remaining call sites in batches,
- then delete old paths,
- then final verification + cleanup.

### 5) No scope creep

Decomposition can add *missing tasks required to achieve the stated North Star*, but it must not expand UX/product scope.
- If it discovers out-of-scope “good ideas”, it records them as `Follow-ups (out of scope)` with anchors.

---

## Single-Source-of-Truth Rule (No Second Checklist)

We should not add a second “execution checklist” section.

Instead, granularization should:
- treat `arch_skill:block:phase_plan` as the **only** execution checklist, and
- rewrite it in-place until it is small-agent executable.

This keeps the cognitive load low: implementers do not cross-reference “phases vs checklist”; they follow the Phase Plan.

The other canonical blocks keep their current roles:
- `arch_skill:block:call_site_audit` is an inventory/evidence anchor (helps completeness, not an alternate plan).
- `arch_skill:block:reference_pack` is binding obligations (if present) that Phase Plan tasks should explicitly mention under “Reference obligations (must satisfy)”.

Stop condition:
- If `DOC_PATH` does not contain a Phase Plan block/section yet, granularize should not invent a new plan format. It should warn and recommend running `/prompts:arch-phase-plan` first (or proceed by creating the Phase Plan block using the existing template, then immediately granularize it).

### Proposed Phase Plan shape (post-granularize)

```md
<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)

<!--
arch_skill:phase_plan_granularize
level: <1..5>
pass_count: <n>
last_updated: <YYYY-MM-DD>
-->

> Rule: one checkbox = one loop-sized, finishable change. Every checkbox includes file anchors + smallest verification signal. Manual QA is non-blocking bullets only.

## Phase 0 — Setup + inventory (always)
* Goal:
* Work (microtasks):
  - [ ] P0.T1 — Refresh call-site groups (cite anchors; do not hand-wave).
  - [ ] P0.T2 — Refresh deletes/cleanup list (no parallel paths).
  - [ ] P0.T3 — Confirm smallest “fast check” commands.
* Verification (smallest signal):
* Exit criteria:
* Rollback:

## Phase 1 — <foundation>
* Goal:
* Work (microtasks):
  - [ ] P1.T1 — <task title>
    - File anchors:
    - Steps:
    - Verification (smallest signal):
    - Exit criteria:
    - Rollback:
* Reference obligations (must satisfy): (if reference pack exists)
* Docs/comments (propagation; only if needed):
* Exit criteria:
* Rollback:

## Phase N — Finalization
* Goal:
* Work (microtasks):
  - [ ] PN.T1 — Final check sweep (as specified)
* Manual QA (non-blocking):
  - <bullet checklist>
* Exit criteria:
* Rollback:
<!-- arch_skill:block:phase_plan:end -->
```

Notes:
- Use consistent task IDs (`P1.T3`) so reruns can preserve identity while refining content.
- Keep “Manual QA” as bullets, never as blocking checkboxes.

---

## Granularity Levels (Dialing Specificity)

This is the key “run it N times” behavior. The prompt takes an optional `LEVEL=` argument; otherwise it defaults to “one level deeper than current”.

### Level 1: Phase hardening (light)
- Ensure each phase (in the Phase Plan) has:
  - call-site list (or reference to call-site audit section),
  - deletes list,
  - smallest verification signal,
  - explicit “done”.
- Split only the obviously-too-big items.

### Level 2: SSOT/migrate/delete decomposition (recommended default)
Apply the canonical split (borrowed from Ralph decomposition):
1) introduce SSOT/contract
2) migrate one bounded slice
3) migrate remaining call sites (in batches)
4) delete old path + cleanup
5) run a relevant check

### Level 3: Call-site batching + per-file anchors
- Expand migrations into explicit batches:
  - Group call sites by directory/module/feature.
  - Convert “migrate remaining” into multiple tasks (“migrate group A”, “migrate group B”…).
- Each task includes the concrete list of paths/symbols it changes.

### Level 4: Sub-tasking for tricky work (per-symbol / per-flow)
- Split tasks that hide complexity:
  - concurrency boundaries, caching, cross-thread work, data migrations, risky refactors.
- Add explicit “trap checks” where regressions are likely.

### Level 5: Execution-grade microtasks (maximum granularity)
- Break any remaining multi-file changes into:
  - “introduce scaffolding” task,
  - “wire one call site” task,
  - “wire remaining” tasks,
  - “delete legacy path” task,
  - “final check + cleanup” task.
- Add explicit “no parallel truth” delete/disable steps wherever applicable.

Guardrail: higher `LEVEL` must not produce nonsense. If a task is already atomic, it stays as-is.

---

## How The Prompt Produces Real Tasks (Algorithm)

### Inputs it should trust (in priority order)
1) `DOC_PATH` North Star + scope boundaries (authoritative)
2) `Call-Site Audit` block (authoritative inventory when present)
3) `Phase Plan` block (authoritative sequencing)
4) `Reference Pack` block (binding obligations, if present)
5) Repo reality (code searches for call sites / existing patterns / test commands)

### Decomposition heuristics (practical)

Split tasks along these seams (in this order):
1) **Introduce vs adopt**
   - Creating a new primitive/SSOT is separate from migrating call sites.
2) **One bounded slice first**
   - Always include a “migrate one small slice” task to validate the approach before sweeping.
3) **Call-site groups**
   - Prefer grouping by feature/dir/module rather than “all at once”.
4) **Deletes are first-class**
   - Any migration task must have a corresponding delete/cleanup task to eliminate parallel paths.
5) **Verification is attached to tasks**
   - Every group has a smallest check; not all checks are full-suite.

### Output normalization (avoid churn on reruns)
To keep re-runs stable:
- Deterministic ordering:
  - phases in dependency order,
  - within a phase: tasks ordered by (foundation → migrate small slice → migrate groups → delete → check).
- Stable IDs:
  - task IDs remain stable unless the underlying phase plan changed materially.
- Change detection:
  - if phase plan changes, reconcile by matching tasks by file anchors and phase names before generating new IDs.

---

## Agent-Assisted Variant (Parallel Read-Only Subagents)

The “agent” version should be identical in output, just more grounded and more complete on large repos.

Subagent ground rules (copy the existing pattern from `arch-*-agent` prompts):
- Read-only; no file writes; no recursion; no questions; concise outputs.

Recommended subagents (disjoint scopes):

1) **Call-Site Grouper**
   - Input: the symbols/APIs in `Call-Site Audit` + phase plan.
   - Output:
     - Group: <name>
       - <path> — <symbol> — <why>

2) **Deletes / Cleanup Inventory**
   - Output:
     - <path> — <what should be deleted/disabled> — <why>

3) **Smallest Signal Commands Scout**
   - Output:
     - <check name> — <command> — <what it proves>

4) **Risk Hotspots / Tricky Boundaries Finder (optional at higher levels)**
   - Finds tasks likely to require extra splitting:
     - concurrency, caching, global state, migrations, API boundaries.
   - Output:
     - <area> — <anchor> — <why risky> — <suggested extra task splits>

Main agent synthesis:
- Merge subagent results into the Phase Plan microtasks (file anchors + grouping + deletes + checks).
- Resolve conflicts by reading code (do not ask the user).

---

## Integration Points (How It Becomes Usable)

### A) Update prompt catalogs (later, when implementing)
- Add the new commands to:
  - `skills/arch-skill/SKILL.md` prompt catalog
  - `skills/arch-skill/resources/PROMPT_INDEX.md`
  - `docs/suggested_custom_prompts.md`

### B) Optional arch-flow step (later, when implementing)
Add a new optional step between “Phase plan” and “Implement”:
- “Phase plan granularize (optional): `/prompts:arch-phase-plan-granularize DOC_PATH LEVEL=2`”

### C) Execution integration (optional)
No special execution integration is required if we keep SSOT: implementers already follow `arch_skill:block:phase_plan`.

---

## Known Risks + Mitigations

### Risk: output bloat / context poisoning
If microtasks are huge, it can make the Phase Plan unreadable.

Mitigations:
- Keep the checklist skimmable:
  - 1–2 lines per checkbox max
  - heavy detail stays in call-site audit table / reference pack
- Add a “compact mode”:
  - include file anchors + verification, but avoid long step-by-step prose unless Level >= 4.

### Risk: false precision
Overly prescriptive tasks can be wrong if the plan is wrong.

Mitigation:
- Treat deep dive + phase plan as prerequisites.
- Include explicit “inventory refresh” tasks in Phase 0.

### Risk: scope creep
As you scan the repo, you’ll find adjacent improvements.

Mitigation:
- Put them in Follow-ups with anchors and keep the main checklist aligned to the North Star.

---

## What I Would Implement Next (If You Want This As Real Prompts)

1) Implement `arch-phase-plan-granularize` (planning-only; rewrites the Phase Plan in-place).
2) Implement `arch-phase-plan-granularize-agent` (same logic, but calls the read-only subagents listed above).
3) Add the optional step to `arch-flow` and the prompt indexes.
4) Optional: add a one-liner to `arch-implement-agent` docs that Phase Plan may contain microtask checkboxes (no behavior change needed).
