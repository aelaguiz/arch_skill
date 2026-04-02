---
title: "arch_skill — Goal-Seeking Loop Prompts (Idempotent + Iterative) — Proposal"
date: 2026-02-07
status: draft
owners: ["Amir Elaguizy", "Codex"]
reviewers: ["Amir Elaguizy"]
doc_type: new_system
related:
  # Existing arch_skill patterns we want to reuse (and generalize)
  - prompts/north-star-investigation-bootstrap.md
  - prompts/north-star-investigation-loop.md
  - prompts/arch-flow.md
  - prompts/arch-context-load.md
  - prompts/arch-implement.md
  - docs/arch_skill_usage_guide.md
  - docs/growth/RIGOROUS_FEATURE_PLAN_ITERATION_WITH_PARALLEL_SUBAGENTS_2026-01-24.md
  # Concrete “goal-seeking loops in the wild” (PS Mobile 4 examples)
  - /Users/aelaguiz/workspace/psmobile4/docs/PLAYABLES_LESSONS_QUALITY_REFINEMENT_PROCESS.md
  - /Users/aelaguiz/workspace/psmobile4/docs/PLAYABLES_LESSONS_QUALITY_REFINEMENT_RUNNING_LOG.md
  - /Users/aelaguiz/workspace/psmobile4/docs/content/SKILL.md
---

# TL;DR

- **Outcome:** A small, reusable prompt family that can (1) generate/repair a “Goal-Seeking Loop” SSOT doc and (2) run **one tight iteration** at a time — without falling into the “check spiral / context poisoning” failure mode — so repeated runs compound learning and converge toward the North Star.
- **Problem:** Our current “process plan” docs are expensive to author and fragile to execute: if we include too many checks, the agent gets stuck verifying forever; if we don’t include them, execution drifts, scope creeps, or the agent “forgets what it’s doing.”
- **Approach:** Treat a loop doc as the controller (single source of truth) and make the prompts *thin wrappers* around it: **read contract → validate gate → pick ONE bet → do minimal work → record evidence → update the loop doc/worklog**. Put heavy details in worklogs and use explicit anti-sidetrack rules (parking lot + no-reruns + one-lever-per-iteration) to preserve iteration velocity.
- **Plan:** (1) Define the “Goal Loop Doc” template + required blocks, (2) add `goal-loop-new` + `goal-loop-iterate` prompts (plus optional `goal-loop-flow` + `goal-loop-context-load`), (3) dogfood on 2–3 real efforts and refine the gates/anti-sidetrack rules until it’s reliably autonomous and idempotent.
- **Non-negotiables:**
  - **Operating mode:** iteration velocity + compounding learning (tight loop > exhaustive correctness theater).
  - **Idempotent prompts:** re-running a prompt must converge (no duplicated sections, no prompt-instruction drift, no “rewrite the whole doc every time”).
  - **Anti-sidetrack is first-class:** explicit out-of-scope + “parking lot” + “no reruns” + “one bet per iteration.”
  - **No mandatory human gates baked in:** human judgment steps only happen if explicitly encoded in the loop doc (default is fully autonomous execution).
  - **Required-elements gate exists:** we do not begin iterations until the loop doc has the required contract elements (or the bootstrap prompt fills them).

---

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-02-07 (read arch_skill prompts/docs + psmobile4 loop docs)
external_research_grounding: not started
deep_dive_pass_2: not started
recommended_flow: define loop doc contract -> write prompts -> dogfood -> iterate
note: This is a warn-first checklist only. It should not hard-block execution.
-->
<!-- arch_skill:block:planning_passes:end -->

---

# 0) Holistic North Star

## 0.1 The claim (falsifiable)
> If we introduce a dedicated “Goal-Seeking Loop” prompt family that is (a) **doc-first**, (b) **idempotent**, and (c) explicitly optimized for **iteration velocity + compounding learning**, then we can run the same goal-seeking process repeatedly without getting trapped in checks, losing context, or scope creeping — and every iteration will reliably end with:
> - exactly one concrete forward output (code/doc/data artifact),
> - an updated worklog entry with evidence, and
> - a tightened next iteration bet,
> until the North Star acceptance signal is met.

## 0.2 In scope
- **Deliverables (this proposal):**
  - A “Goal Loop Doc” template (SSOT) with required contract blocks.
  - A minimal prompt set to operate that doc:
    - `goal-loop-new` (doc-only, contract repair + North Star confirmation)
    - `goal-loop-iterate` (execute one iteration + update worklog)
    - optional: `goal-loop-flow` (status + next-step router)
    - optional: `goal-loop-context-load` (context digest / compression)
  - A small set of explicit anti-sidetrack rules, expressed as doc sections and enforced by prompts.
- **Behavioral goals:**
  - Autonomous by default (no “ask for confirmation” loops unless the doc explicitly requires it).
  - Repeatable execution (stable blocks; append-only worklog; de-dupe/no-rerun).

## 0.3 Out of scope (anti-sidetrack by definition)
- **We are not** building or changing the actual codebase behavior in this doc.
- **We are not** designing a “perfect” universal framework for every team/workflow.
- **We are not** baking in mandatory human approvals (“Amir picks option”) as a hard-coded phase.
- **We are not** requiring comprehensive repo audits or full test suites per iteration.
- **We are not** adding new harnesses/tooling as a prerequisite for the loop (unless explicitly requested in a specific loop doc later).

## 0.4 Definition of done (acceptance evidence)
- A new prompt family exists and is installable alongside the existing arch_skill prompts.
- The prompts can be re-run on the same loop doc without:
  - duplicating sections,
  - rewriting stable blocks unnecessarily,
  - or drifting away from the loop doc’s contract.
- Dogfood evidence (minimum acceptance):
  - Run `goal-loop-new` → produces a valid loop doc (gate passes).
  - Run `goal-loop-iterate` for 3 consecutive iterations on the same effort:
    - each iteration changes at least one “lever” and produces a concrete output,
    - each iteration updates the worklog with evidence + next bet,
    - no iteration re-runs an identical check without changing a lever (“no reruns”).
- The prompt family consistently prioritizes **the best lever for the North Star** over the closest/easiest local fix (avoid local maxima).

## 0.5 Key invariants (fix immediately if violated)
- **One-bet rule:** one iteration = one bet/hypothesis = one main lever change.
- **No check spiral:** checks exist only to unblock a decision, validate a lever, or prevent a likely regression; otherwise proceed.
- **Parking lot:** any discovered tangent goes into a parking lot with concrete anchors (paths, commands) and is explicitly deferred.
- **Doc is the controller:** prompts do not “freestyle” a new process; they execute the loop doc.

---

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)
1) **Iteration velocity + compounding learning** (tight learning loop is the product).
2) **Idempotence and convergence** (re-run prompts safely; no doc drift).
3) **Anti-sidetrack robustness** (explicit out-of-scope + no reruns + parking lot).
4) **Autonomy-first** (human steps must be explicit opt-ins in the doc).
5) **Minimal, credible verification** (enough to not fool ourselves; never a proof-burden trap).

## 1.2 Constraints (real-world)
- Context is finite; long scans and exhaustive checklists poison the agent’s ability to execute.
- “More checks” is not monotonic with “more shipping”: overly rigid gates can stall progress indefinitely.
- A prompt that tries to re-teach itself the entire process every run becomes unstable (instruction bloat).
- Different domains have different definitions of “evidence” (tests vs queries vs screenshots vs manual QA) — the system must allow local definition without losing structure.

## 1.3 Architectural principles (rules we enforce in prompt design)
- **Prompts are thin; docs carry process.**
  - The prompt should not contain a 200-line checklist; it should execute the doc contract.
- **Stable blocks + append-only logs.**
  - Stable doc sections are replaced in-place via markers.
  - Worklog is chronological and append-only.
- **Subagent isolation for heavy scanning (optional).**
  - When grep-heavy/code-audit work is required, delegate to read-only subagents to keep main context lean (pattern used in `arch-*-agent` prompts).
- **Fail loud on missing contract pieces, but self-heal when possible.**
  - If required elements are missing, bootstrap fills them; only ask the human when it’s truly a product/UX decision.

## 1.4 Known tradeoffs (explicit)
- We will sometimes accept “good enough evidence” (e.g., a targeted test or a small repro) instead of exhaustive proof, because the objective is compounding iteration.
- “No mandatory human gates” means the system must be opinionated about defaults; users can override by encoding explicit gates in the doc.

---

# 2) Problem Statement (why “goal-seeking loops” fail today)

## 2.1 Observed failure modes
These match the pain described in the prompt request (and show up repeatedly across docs and executions):

1) **Check spiral**
   - The agent front-loads verification, keeps discovering more to verify, and never returns to the actual iteration/execution loop.

2) **Context poisoning**
   - Massive audits, logs, or exhaustive inventories consume the context window; by the time execution starts, the agent forgets the North Star and starts thrashing.

3) **Local maxima**
   - The agent optimizes “nearest fix” rather than “best lever” (because the nearest fix is easiest to prove/verify).

4) **Scope creep by ‘good ideas’**
   - Tangents get treated as mandatory, especially when the agent finds “something else wrong.”

5) **Hidden human gates**
   - A loop silently relies on human judgment (e.g., “Amir picks option”) even when we wanted an autonomous run, creating dead-ends.

## 2.2 Root cause (architectural)
The current loop specs tend to be:
- either **too vague** (so execution drifts),
- or **too exhaustive** (so execution never starts),
- and they often lack explicit *controller contracts*:
  - required elements,
  - explicit out-of-scope,
  - stop conditions,
  - and the “one iteration = one bet” rule.

---

# 3) Research Grounding (what we already have that works)

## 3.1 Internal anchors (arch_skill)
These already encode many of the needed primitives — we want to generalize and repackage them for “goal-seeking loops”:

- **Bootstrapping a controller doc (doc-first):**
  - `prompts/north-star-investigation-bootstrap.md`
- **One-iteration-at-a-time execution discipline:**
  - `prompts/north-star-investigation-loop.md`
- **Flow routing based on doc markers (read-only status + next step):**
  - `prompts/arch-flow.md`
- **Context compression to avoid poisoning:**
  - `prompts/arch-context-load.md`
- **Anti-negative-value verification policy:**
  - `prompts/arch-implement.md`

## 3.2 Concrete examples (PS Mobile 4)
These are “loop docs in production” that demonstrate the split between a stable process doc and an append-only running log:

- **Stable process SSOT + explicit invariants + de-dupe gate:**
  - `/Users/aelaguiz/workspace/psmobile4/docs/PLAYABLES_LESSONS_QUALITY_REFINEMENT_PROCESS.md`
- **Chronological running log with an entry template (append-only):**
  - `/Users/aelaguiz/workspace/psmobile4/docs/PLAYABLES_LESSONS_QUALITY_REFINEMENT_RUNNING_LOG.md`
- **A skill-style operating manual encoding the loop, inputs, and non-negotiables:**
  - `/Users/aelaguiz/workspace/psmobile4/docs/content/SKILL.md`

## 3.3 “Too-rigorous” patterns to keep optional
This doc contains powerful rigor tools (Way 1 / Way 2, confidence tags, parallel specialists), but it’s also the type of structure that can become a check spiral if enforced everywhere:

- `docs/growth/RIGOROUS_FEATURE_PLAN_ITERATION_WITH_PARALLEL_SUBAGENTS_2026-01-24.md`

Proposal: keep these as **optional overlays** invoked only when the loop doc marks a claim as “load-bearing” (see §5.6).

---

# 4) Current Architecture (what we have today)

## 4.1 We have “arch flows”
`arch_skill` excels at planning/executing code changes with a single SSOT plan doc + worklog.

But a “goal-seeking loop” is often *not* a single implementation plan:
- it’s a repeated controller loop (measure → decide → act → learn),
- it needs explicit anti-sidetrack rules,
- and it needs idempotent iteration semantics.

## 4.2 We have “North Star Investigation”
The existing `north-star-investigation-*` prompts are close to the desired behavior:
- bootstrap a controller doc,
- iterate with one bet + brutal test,
- update worklog and refine hypotheses.

But it is framed as “investigation,” and doesn’t yet package:
- a generic “goal loop doc” template,
- a generic “anti-sidetrack” section as part of the North Star contract,
- or a general-purpose router that makes the next step obvious without bloating context.

---

# 5) Target Architecture (proposal): Goal-Seeking Loop System

This is the proposal for a small, composable system that makes goal-seeking loops:
- repeatable,
- autonomous by default,
- idempotent to rerun,
- and hard to derail.

## 5.1 Canonical artifacts

**A) Goal Loop Doc (SSOT; stable controller)**
- Path: `docs/<TITLE>_<DATE>.md`
- Purpose: defines the North Star, anti-sidetrack contract, scoreboard, levers, and the loop protocol.
- Update pattern: stable blocks updated in-place (markers).

**B) Worklog (append-only)**
- Path: `docs/<TITLE>_<DATE>_WORKLOG.md`
- Purpose: chronological evidence and decisions; every iteration appends one entry.

**C) Parking Lot (optional; can live inside Worklog)**
- Purpose: explicitly defer tangents with anchors so they don’t hijack the iteration.

## 5.2 “Goal Loop Doc” template (required blocks)

This doc should be *short and controller-like*. It should not become a second worklog.

### YAML frontmatter (minimal)
```yaml
---
title: "<PROJECT> — <NORTH STAR> — Goal Loop"
date: <YYYY-MM-DD>
status: draft | active | complete
owners: [<name>]
reviewers: [<name>]
doc_type: goal_loop
---
```

### Required controller sections
1) **North Star (falsifiable claim)**
2) **Operating mode**
   - Must explicitly state: “iteration velocity + compounding learning”
3) **Anti-sidetrack contract**
   - Out of scope
   - Anti-goals (“we will not do X”)
   - Parking lot rules
4) **Scoreboard**
   - Primary acceptance signal(s)
   - Guardrails (what would cause stop/rollback)
   - Evidence sources (tests/queries/screenshots/etc)
5) **Non-negotiables / invariants**
6) **Lever inventory (small)**
   - 5–15 candidate levers max; do not list every possible thing in the universe.
7) **Iteration protocol**
   - one-bet rule
   - no-reruns rule
   - stop conditions
8) **De-dupe**
   - “If this was already tried, link to it and do not restart.”

### Block markers (idempotence API)
We should use explicit markers so prompts can replace stable blocks without relying on brittle headings:

- `<!-- goal_loop:block:contract:start --> … end -->`
- `<!-- goal_loop:block:scoreboard:start --> … end -->`
- `<!-- goal_loop:block:levers:start --> … end -->`
- `<!-- goal_loop:block:iteration_protocol:start --> … end -->`
- `<!-- goal_loop:block:anti_sidetrack:start --> … end -->`
- `<!-- goal_loop:block:de_dupe:start --> … end -->`

## 5.3 Required-elements gate (how we avoid “jumping into execution wrong”)

**Gate rule:**
- `goal-loop-iterate` must not run an iteration unless:
  - `status: active`, AND
  - all required blocks exist and are non-placeholder.

**Autonomous default behavior:**
- If the gate fails, `goal-loop-iterate` automatically runs the bootstrap behavior in-place:
  - fills missing blocks,
  - tightens scope,
  - writes a minimal scoreboard,
  - and only asks a question if it is truly a product/UX decision or an external unknown.

**Human gates (optional; explicit)**
- If a loop requires a human decision, it must be encoded explicitly:
  - e.g., a `Human Gates` section listing what must be decided and what options are acceptable.
- Otherwise, the loop is assumed autonomous.

## 5.4 Anti-sidetrack contract (the thing we’re missing today)

The “anti-sidetrack” section should be first-class and treated as law.

Recommended contents:
- **Out of scope** (explicit exclusions)
- **Anti-goals** (things that look tempting but are forbidden)
- **Parking lot rule**
  - If you discover a tangent: write it to Parking Lot with anchors, then resume the iteration.
- **No premature refactors**
  - Refactors are allowed only when they directly unblock the current lever.
- **No exhaustive audits by default**
  - Audits happen only when the loop doc declares them as the next bet.

## 5.5 The iteration protocol (tight loop)

The loop should be defined so it can be repeated indefinitely without instruction bloat:

1) Re-read the controller blocks (North Star + anti-sidetrack + scoreboard + invariants).
2) Pick **ONE bet** (highest info gain / best lever).
3) Pre-commit the decision rule (what outcome means “keep going” vs “change direction”).
4) Do the minimum work to test/ship that bet (one concrete output).
5) Run the smallest credible evidence signal.
6) Append one worklog entry with evidence + conclusion + next bet.
7) Update controller blocks only if the evidence forces a contract change.

## 5.6 Optional rigor overlays (only when marked load-bearing)

To avoid the check spiral, “rigor” tools should be opt-in and localized:

- **Way 1 / Way 2** cross-check (from the growth doc) only for claims explicitly marked load-bearing in the loop doc.
- **Confidence tagging** (G/Y/R) only on claims that affect lever choice.
- **Parallel subagents** only when the bet requires broad scanning or independent cross-checks.

Default stance: if a check won’t change the next action, don’t do it.

---

# 6) Prompt Suite (proposal)

## 6.1 `/prompts:goal-loop-new`
Purpose:
- Create or repair a Goal Loop Doc so the required-elements gate passes.

Rules:
- Doc-only. No production code changes in this prompt.
- Strict question policy (only ask what cannot be inferred from repo/docs).
- Output is the loop doc path + the drafted controller blocks.

## 6.2 `/prompts:goal-loop-iterate`
Purpose:
- Execute exactly one iteration and update the worklog (and controller blocks if needed).

Rules:
- If gate fails, self-heal by running bootstrap behaviors (no human gate unless explicitly required).
- One-bet rule, no reruns, parking lot enforcement.
- Keep chat output short; details go to the worklog.

## 6.3 `/prompts:goal-loop-flow` (optional)
Purpose:
- Read-only status and next-step router (like `arch-flow`).

Output:
- Gate status (pass/fail) + evidence.
- Recommended next command.

## 6.4 `/prompts:goal-loop-context-load` (optional)
Purpose:
- Compress context into a short “Context Digest” block so long-running loops stay stable.

---

# 7) Phase Plan (if/when we implement in this repo)

## Phase 1 — Spec hardening (docs only)
- Write the final Goal Loop Doc template (markers + required blocks).
- Write a small “anti-sidetrack” contract checklist (doc section, not prompt bloat).

## Phase 2 — Minimal prompt implementation
- Add `prompts/goal-loop-new.md`
- Add `prompts/goal-loop-iterate.md`
- Ensure idempotent update rules via block markers.

## Phase 3 — Router + context compression (optional upgrades)
- Add `prompts/goal-loop-flow.md`
- Add `prompts/goal-loop-context-load.md`

## Phase 4 — Dogfood + refine
- Run on 2–3 real efforts.
- Tighten gates and anti-sidetrack rules based on observed failures.

---

# Appendix A — Why this should work

This proposal is explicitly a synthesis of:
- the **controller doc + loop discipline** of `north-star-investigation-*`,
- the **routing + idempotent markers** strategy of `arch-flow`,
- and the **stable process SSOT + append-only running log** pattern in PS Mobile 4 quality docs.

The missing piece is packaging those primitives into a prompt family whose *default behavior* is:
velocity + convergence, not exhaustive verification theater.
