# arch_skill — Usage Guide

This guide explains the **intended usage** of the prompts in `prompts/` across four operational workflows:

- **Regular arch flow**: more prompts, more checkpoints; best for medium/large changes and anything risky.
- **Mini flow**: fewer prompts, "one-pass planning"; best for small, contained changes.
- **Goal-seeking loops**: autonomous iteration for open-ended goals (optimization, investigation, metric improvement).
- **North Star investigation**: deep hypothesis-driven investigation for root-cause analysis or optimization.

It also captures the conventions that make the flows work (doc blocks, worklog naming, subagent rules).

Important: this repo is meant to be used via **installed prompts** (slash commands) in **Codex CLI** or **Claude Code**.
It also ships an optional **router skill** (`arch-skill`) as a parallel mechanism — prompts remain the SSOT procedures.

---

## 0) Setup (so `/prompts:*` commands exist)

These prompt files are meant to be installed as custom prompts (slash commands) for Codex CLI and/or Claude Code:

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

Restart Codex/Claude Code after updating prompts/skills.

What `make install` installs:

**Codex CLI:**
- Prompts → `~/.codex/prompts/`
- Templates → `~/.codex/templates/arch_skill/`
- Skills → `~/.codex/skills/arch-skill/`, `~/.codex/skills/arch-flow/`, `~/.codex/skills/codemagic-builds/`

**Claude Code:**
- Prompts → `~/.claude/commands/prompts/`
- Skills → `~/.claude/skills/arch-skill/`, `~/.claude/skills/arch-flow/`

---

## 1) Key invariants (applies to both flows)

These are the rules the prompt family is designed around. If you violate them, the workflow degrades fast.

### Single-document rule (SSOT for planning)
- There is **one canonical plan doc** in `docs/` for the effort.
- Planning, decisions, architecture, and phase tracking live in that single doc.
- The worklog is separate, but it’s **not a second plan doc** (it’s a progress journal).

### Code is ground truth
- Plans must be anchored in file paths / symbols / tests.
- Avoid speculative architecture not backed by repo reality.

### Minimal, credible verification
- Prefer existing checks: targeted unit/integration tests, `make test`, `pnpm test`, `cargo test`, etc.
- If no tests exist for the behavior, use minimal instrumentation/log signature or a short manual checklist.
- Avoid inventing new harnesses by default.

### No fallbacks (strict)
- Default: do not add runtime fallbacks/shims/placeholder behavior to emulate correctness.
- If an exception is truly required, it must be explicitly approved in the plan doc by setting `fallback_policy: approved` and recording a Decision Log entry with a timebox + removal plan.

### Question policy (strict)
Only ask questions that cannot be answered by searching the repo / reading code / reading docs:
- Product/UX decisions not encoded anywhere
- External constraints (policies, dates, KPIs) not in repo/docs
- Doc-path ambiguity (choose from top 2–3 candidates)
- Missing access/permissions

---

## 2) Canonical artifacts and conventions

### `DOC_PATH` (the plan doc)
Most prompts accept freeform text, but will try to resolve `DOC_PATH` from:
- A `docs/<...>.md` path you include anywhere in your arguments, otherwise
- The current conversation, otherwise
- They’ll ask you to choose from the top 2–3 candidates.

Practical rule: **always include the plan doc path explicitly** once it exists.

### `arch-flow` (status + next-step helper)
At any time, run:
- `/prompts:arch-flow DOC_PATH`

It prints a checklist of where you are in the regular/mini flow and recommends the next prompt (with an optional `RUN=1` mode to execute the next step immediately).

### `WORKLOG_PATH` (the progress journal)
Implementation- and progress-oriented prompts derive the worklog from the plan doc:

`WORKLOG_PATH = <same directory>/<DOC_BASENAME>_WORKLOG.md`

Examples:
- `docs/FOO_2026-01-28.md` → `docs/FOO_2026-01-28_WORKLOG.md`
- `docs/growth/BAR_2026-01-28.md` → `docs/growth/BAR_2026-01-28_WORKLOG.md`

### “Block markers” are the stable API between prompts
Many prompts update the plan by replacing the content inside these markers (instead of relying on section numbers):

- `<!-- arch_skill:block:planning_passes:start --> … end -->`
- `<!-- arch_skill:block:research_grounding:start --> … end -->`
- `<!-- arch_skill:block:reference_pack:start --> … end -->`
- `<!-- arch_skill:block:current_architecture:start --> … end -->`
- `<!-- arch_skill:block:target_architecture:start --> … end -->`
- `<!-- arch_skill:block:call_site_audit:start --> … end -->`
- `<!-- arch_skill:block:phase_plan:start --> … end -->`
- `<!-- arch_skill:block:overbuild_protector:start --> … end -->`
- `<!-- arch_skill:block:review_gate:start --> … end -->`
- `<!-- arch_skill:block:gaps_concerns:start --> … end -->`
- `<!-- arch_skill:block:implementation_audit:start --> … end -->`

Practical rule: **don’t delete or rename these markers** once they’re in your doc.

### Reference folding (optional, but high leverage)
If your plan depends on “out of band” materials (UX diagrams, specs, best-practice docs, etc.), implementation can miss them if they’re only linked.

Use:
- `/prompts:arch-fold-in docs/<...>.md <any number of ref doc paths/URLs> <short blurb>`

What it does:
- Folds reference material *into* `DOC_PATH` under the `reference_pack` block.
- Wires binding “must satisfy” obligations into the relevant phases (so implementation can’t skip them).

Practical placement: run it after the phase plan is written and before implementation (Phase 3 → Phase 4).

---

## 3) Choosing a flow

### Use the **mini flow** when…
- The change is **small and bounded** (1–2 modules, few call sites).
- There’s a clear intended outcome and you mostly need to confirm call sites + plan sequencing.
- You can plausibly plan + start shipping within one session.

### Use the **regular arch flow** when…
- The change is **medium/large**, cross-cutting, or high-risk (SSOT changes, migrations, infra, concurrency).
- You expect **multiple phases** or meaningful cleanup/deletes.
- You need explicit checkpoints (North Star confirmation, research sufficiency, review gate).
- External best practices meaningfully affect correctness (security, crypto, concurrency, offline, payments, etc.).

If you’re on the fence: default to the regular flow. The overhead is mostly “structured writeback” you’ll want anyway.

### Lilarch flow (tiny tasks, 3 prompts)
`lilarch` is a **compressed mini-arch** flow intended for **small features or improvements** that can ship in **1–3 phases**.

Use `lilarch` when:
- You mostly need to (1) lock North Star + requirements, (2) confirm call sites + idiomatic plan, (3) ship + review.
- You want to avoid the larger prompt surface area of the full arch flow.

Avoid `lilarch` when:
- The plan is likely **4+ phases**, a broad migration, or a new system.
- Investigation dominates (unknown root cause) → use `bugs-*` or North Star investigation.

Flow:
1) `/prompts:lilarch-start <freeform request>`
2) `/prompts:lilarch-plan docs/<...>.md`
3) `/prompts:lilarch-finish docs/<...>.md`

If lilarch feels too small midway, the doc is still compatible with the full arch prompts (same block marker conventions), so you can switch to `/prompts:arch-flow docs/<...>.md FLOW=regular`.

---

## 4) Regular arch flow (recommended for serious work)

This is the “multi-prompt, phase-gated” workflow.

### 4.1 Start / normalize the plan doc

**If you don’t have a plan doc yet**
1) `/prompts:arch-new <freeform blurb>`
   - Creates `docs/<TITLE>_<DATE>.md`
   - Drafts TL;DR + North Star and asks you to confirm (this is intentional; don’t skip it)

**If you already have a doc, but it’s not in canonical format**
1) `/prompts:arch-reformat <path-to-existing-doc.md> [OUT=docs/<...>.md]`
   - Preserves content, maps it into the canonical template, then asks you to confirm the North Star

Optional but common:
2) `/prompts:arch-ramp-up docs/<...>.md`
   - Read-only orientation on the plan doc + key repo anchors before doing anything heavy

### 4.2 Phase 1 — Research grounding

3) `/prompts:arch-kickoff docs/<...>.md`
   - Writes a Phase 1 kickoff block and explicitly asks if you want to proceed to Phase 2

4) `/prompts:arch-research docs/<...>.md`
   - Populates research grounding (internal anchors + optional external anchors + evidence-based questions)

If web best-practice research is truly required:
5) `/prompts:arch-external-research-agent docs/<...>.md`
   - Adds a structured external research block with sources (this is the one that’s meant to browse)

### 4.3 Phase 2 — Architecture deep dive

6) `/prompts:arch-deep-dive docs/<...>.md`
   - Produces:
     - Current architecture (as-is)
     - Target architecture (to-be)
     - Call-site audit (exhaustive change inventory)
   - Updates the `planning_passes` “warn-first” bookkeeping

If the change touches UI/UX:
7) `/prompts:arch-ui-ascii docs/<...>.md`
   - Adds ASCII mockups for current + target states (contract-level, not vibes)

### 4.4 Phase 3 — Implementation planning

8) `/prompts:arch-plan-enhance docs/<...>.md` (optional but recommended)
   - Hardens the plan for SSOT, deletes, enforceable boundaries, and consolidation sweep

9) `/prompts:arch-phase-plan docs/<...>.md`
   - Inserts the authoritative depth-first phased implementation plan (with exit criteria + rollback)
   - Warns (doesn’t block) if planning passes were skipped/unknown

Optional (recommended when you have specs/design docs you don’t want missed during implementation):
- `/prompts:arch-fold-in docs/<...>.md <any number of ref doc paths/URLs> <short blurb>`
  - Folds references *into* the plan doc and wires binding obligations into the relevant phases.

Optional (when you want to aggressively prevent scope creep / overbuild before implementation):
- `/prompts:arch-overbuild-protector docs/<...>.md MODE=report` (default) or `MODE=apply`
  - Classifies Phase Plan items as ship-blocking vs optional vs follow-ups (intentionally deferred) vs rejected bug vectors.
  - MODE=apply rewrites the Phase Plan in-place so out-of-scope items cannot be mistaken as required work.

Optional (when you want extremely granular, small-agent-executable tasks):
- `/prompts:arch-phase-plan-granularize docs/<...>.md LEVEL=2`
  - Rewrites the existing Phase Plan in-place into micro-phases + microtasks (single SSOT; no second checklist).
  - Safe to re-run to get more granular (e.g., run again with `LEVEL=3`, `LEVEL=4`, etc).
  - If the repo is large, prefer `/prompts:arch-phase-plan-granularize-agent`.

10) `/prompts:arch-review-gate docs/<...>.md` (recommended for high-risk changes)
   - Runs an “idiomatic + completeness” review pass and writes the review gate block into the doc

### 4.5 Phase 4 — Execution

11) `/prompts:arch-implement docs/<...>.md`
   - Implements phase-by-phase
   - Creates/updates `WORKLOG_PATH`
   - Runs the smallest checks per phase and records results
   - Defers UI verification until finalization by default

Optional “did we actually ship it?” automation QA (sims/emulators):
- `/prompts:arch-qa-autotest docs/<...>.md` (runs the existing automation harness on an already-running sim/emulator and reopens plan phases if failures prove missing work)

Optional during long executions:
- `/prompts:arch-progress docs/<...>.md` (worklog updates without re-planning)

Recommended when you think you’re “done”:
- `/prompts:arch-audit docs/<...>.md` (gaps & concerns list)
- `/prompts:arch-audit-implementation docs/<...>.md` (strict “is code actually complete vs plan?” audit)

---

## 5) Mini flow (small tasks, fewer prompts)

This flow compresses the planning passes into one prompt while still producing the canonical blocks.

### 5.1 Start / normalize the plan doc

If you need a plan doc:
1) `/prompts:arch-new <freeform blurb>`

If you already have a doc but it’s the wrong format:
1) `/prompts:arch-reformat <path-to-existing-doc.md>`

### 5.2 One-pass planning

2) `/prompts:arch-mini-plan-agent docs/<...>.md <optional guidance>`

This single prompt is intended to fill/update:
- Research grounding
- Current architecture
- Target architecture
- Call-site audit
- Phase plan

Key constraint: **don’t run multiple doc-writing prompts concurrently against the same `DOC_PATH`.**
The mini prompt uses parallel *read-only* subagents internally; that’s where parallelism should happen.

### 5.3 Execution

Optional (when you want microtasks before implementation):
- `/prompts:arch-phase-plan-granularize docs/<...>.md LEVEL=2`

3) `/prompts:arch-implement-agent docs/<...>.md`

Optional post-checks:
- `/prompts:arch-qa-autotest docs/<...>.md` (automation QA on existing sims/emulators; reopens plan issues with evidence)
- `/prompts:arch-audit-agent docs/<...>.md`
- `/prompts:arch-audit-implementation-agent docs/<...>.md`

---

## 6) Agent-assisted variants (when to use `*-agent` prompts)

Many “regular flow” prompts have a `*-agent` sibling that does the same work but uses parallel read-only subagents
for repo-wide scanning (call sites, patterns, tests) to keep the main context lean.

Use agent-assisted variants when:
- Call-site completeness matters (migrations, refactors, SSOT rewrites)
- The repo is large and manual scanning is error-prone
- You want parallel “specialist scans” without polluting the main agent’s context

Examples:
- `/prompts:arch-research-agent` instead of `/prompts:arch-research`
- `/prompts:arch-deep-dive-agent` instead of `/prompts:arch-deep-dive`
- `/prompts:arch-phase-plan-agent` instead of `/prompts:arch-phase-plan`
- `/prompts:arch-phase-plan-granularize-agent` instead of `/prompts:arch-phase-plan-granularize`
- `/prompts:arch-implement-agent` for implementation where you want phase-by-phase subagents

---

## 7) Common failure modes (and the intended fix)

### “The agent is asking me stuff it could look up”
Fix: enforce the strict question policy. The prompt family already expects “go read code and decide”.

### “We have 3 docs and nobody knows what’s authoritative”
Fix: return to the single-document rule. Use one `DOC_PATH`; everything else becomes a link/reference or appendix.

### “We shipped code but the doc is stale / phases are lies”
Fix: run `/prompts:arch-audit-implementation` (or `*-agent`) and reopen false-complete phases.

### “We missed a call site / left a parallel path”
Fix: deep dive audit + consolidation sweep + explicit delete list; then rerun audit.

### "UI verification is slowing us down mid-flight"
Fix: defer UI verification to finalization and track it as a non-blocking checklist in `WORKLOG_PATH`.

---

## 8) Goal-seeking loops (open-ended goals)

Use goal loops when the goal is clear but the path isn't — optimization, metric improvement, investigation, or any situation where you need to iterate toward a target rather than execute a fixed plan.

### When to use goal loops vs arch flow
- **Arch flow:** You know _what_ to build. You need structured planning, phased execution, and completion audits.
- **Goal loops:** You know _where_ you want to get, but not exactly _how_. You need to explore, experiment, and compound learning.

### How it works
Goal loops maintain two artifacts:
1. **SSOT doc** — the authoritative goal definition (North Star, scope, non-negotiables, scoreboard, hypotheses)
2. **Running log** — append-only journal of bets, results, and learnings (never edited, only appended)

### Goal loop flow

1) `/prompts:goal-loop-new <freeform goal>`
   - Creates/repairs the Goal Loop SSOT doc + running log
   - Confirms the North Star with the user
   - Idempotent — safe to re-run on an existing doc

2) `/prompts:goal-loop-flow <DOC_PATH>`
   - Read-only readiness check: is the doc bootstrapped? Is the running log present?
   - Recommends the single best next step (bootstrap vs iterate)

3) `/prompts:goal-loop-iterate <DOC_PATH>`
   - Executes exactly ONE bet (highest info-gain)
   - Reads the running log first to avoid reruns
   - Appends a worklog entry with evidence + learnings
   - Anti-sidetrack: stays focused on the North Star

4) `/prompts:goal-loop-context-load <DOC_PATH>`
   - Writes a short Context Digest from the doc + running log
   - Use this before handing off to a new agent or restarting a session
   - Details remain in the running log; the digest is just a high-signal brief

### Typical loop session
```
/prompts:goal-loop-new "Double conversion rate on signup flow"
# → creates docs/GOAL_LOOP_SIGNUP_CONVERSION_2026-02-07.md + _RUNNING_LOG.md
# → confirms North Star

/prompts:goal-loop-iterate docs/GOAL_LOOP_SIGNUP_CONVERSION_2026-02-07.md
# → runs one bet, appends to log
# → repeat as many times as needed

/prompts:goal-loop-context-load docs/GOAL_LOOP_SIGNUP_CONVERSION_2026-02-07.md
# → write digest for handoff/restart
```

---

## 9) North Star investigation (deep root-cause analysis)

Use North Star investigation when you need to deeply investigate an optimization problem or root-cause issue. It's more structured than goal loops — hypothesis-driven with pre-committed decision rules and brutal tests.

### When to use
- Root-cause debugging of complex, multi-factor issues
- Performance optimization where you need to identify the biggest lever
- Any investigation where "the truth" requires measurement and math, not speculation

### Investigation flow

1) `/prompts:north-star-investigation-bootstrap <freeform description>`
   - Creates the investigation doc with: North Star, scope, non-negotiables, scoreboard, ground truth anchors, quant model, ranked hypotheses, first iteration plan, and initial worklog
   - Phase 1 is **doc-only** — no production code edits

2) `/prompts:north-star-investigation-loop <DOC_PATH>`
   - Executes one iteration of the investigation loop:
     - Re-reads North Star + scope + non-negotiables (treats as law)
     - Chooses ONE hypothesis (highest info gain)
     - Designs the fastest brutal test (traps, negative proofs, toggles, oracles)
     - Executes minimum work, updates the doc with results
   - Phase 2 **may edit code** (temporary instrumentation allowed)
   - No reruns: if a test already exists in the worklog with the same config, must change a lever or move on

### Key differences from goal loops
- **North Star investigation** is math-first and hypothesis-driven — each bet has a pre-committed pass/fail rule
- **Goal loops** are more flexible — each bet has expected learning outcomes but doesn't require quantitative decision rules
- Use investigation when the problem is quantitative; use goal loops when the problem is exploratory
