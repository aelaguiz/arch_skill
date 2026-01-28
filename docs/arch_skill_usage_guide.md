# arch_skill — Usage Guide (Regular Flow vs Mini Flow)

This guide explains the **intended usage** of the prompts in `prompts/` as two operational workflows:

- **Regular arch flow**: more prompts, more checkpoints; best for medium/large changes and anything risky.
- **Mini flow**: fewer prompts, “one-pass planning”; best for small, contained changes.

It also captures the conventions that make the flows work (doc blocks, worklog naming, subagent rules).

Important: this repo is meant to be used via **installed Codex CLI prompts** (slash commands).
You don’t “import” this repo as a skill inside another repo; you install the prompts into `~/.codex/prompts/`.

---

## 0) Setup (so `/prompts:*` commands exist)

These prompt files are meant to be installed as Codex “custom prompts”:

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

Restart Codex after updating prompts.

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
- `<!-- arch_skill:block:current_architecture:start --> … end -->`
- `<!-- arch_skill:block:target_architecture:start --> … end -->`
- `<!-- arch_skill:block:call_site_audit:start --> … end -->`
- `<!-- arch_skill:block:phase_plan:start --> … end -->`
- `<!-- arch_skill:block:review_gate:start --> … end -->`
- `<!-- arch_skill:block:gaps_concerns:start --> … end -->`
- `<!-- arch_skill:block:implementation_audit:start --> … end -->`

Practical rule: **don’t delete or rename these markers** once they’re in your doc.

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

### “UI verification is slowing us down mid-flight”
Fix: defer UI verification to finalization and track it as a non-blocking checklist in `WORKLOG_PATH`.
