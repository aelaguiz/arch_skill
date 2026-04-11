---
name: arch-docs
description: "Audit and repair repo documentation with the DGTFO loop: orient to the repo's doc system, inventory doc-shaped surfaces, ground each topic against current code, trim stale, duplicate, or obviously dated docs, update stale surviving docs, clarify confusing docs, promote or author canonical evergreen docs when the repo clearly needs them, and organize navigation. Use when the user wants stale docs cleaned up, overlapping docs consolidated, outdated docs deleted, confusing docs clarified, missing grounded docs promoted into evergreen homes, plan/worklog truth folded into evergreen docs, or explicit Codex hook-backed `auto` docs cleanup. It works as a standalone docs-audit skill in any repo and can also use active arch artifacts as narrowing context when they exist. By default, `$arch-docs` should just run one normal pass with no extra arguments. Not for generic copy editing, open-ended net-new doc authoring, or speculative taxonomy redesign."
metadata:
  short-description: "Topic-first docs audit and cleanup"
---

# Arch Docs

Use this skill when the code is stable enough to ground documentation against current reality and the main job is leaving the docs surface more accurate, clearer, and more useful.

## When to use

- The user wants a docs audit pass that finds stale docs, duplicate docs, outdated READMEs, dead migration notes, misleading setup/architecture docs, or grounded doc gaps that should exist in evergreen docs.
- A repo needs topic-first cleanup where one topic may be spread across several files and several files may overlap on the same topic.
- A full-arch plan and worklog should be treated as context, mined for durable truth, and then retired or transformed into evergreen docs.
- The user wants to run the DGTFO loop directly in a repo with no requirement that an arch plan already exists.
- The user explicitly wants `arch-docs auto` in Codex and expects real hook-backed continuation with a fresh external evaluation after each pass.

## When not to use

- The task is generic copy editing, README polish, or human-facing doc writing with no cleanup, clarification, canonicalization, or truth-audit workflow.
- The user wants net-new aspirational docs or a broad taxonomy redesign untethered from repo truth.
- The code is still changing too fast to ground docs honestly. Finish or audit the implementation first.
- The real task is choosing or editing a skill package. Use `skill-authoring`.

## Non-negotiables

- The unit of work is the topic, not the file.
- Adapt to the repo's current doc gravity instead of imposing a new framework.
- Code is ground truth. Existing docs are evidence to inspect, not authority to trust.
- Every in-scope topic should end with one canonical evergreen home.
- Bias toward deleting stale truth and promoting durable truth. Stale docs are worse than no docs, but missing or confusing canonical docs are also a failure.
- Standalone runs must still work with no `DOC_PATH` and no explicit path arguments.
- If explicit user context or active arch context exists, use it to narrow the audit intelligently. If not, audit the repo's docs surface directly.
- Use a temporary repo-root `.doc-audit-ledger.md` while the cleanup is active. Delete it before the cleanup finishes.
- Promote durable truth into evergreen docs, then delete obsolete working docs, plan/worklog residue, and stale duplicates in scope. Git is the archive.
- If a grounded topic clearly lacks a viable canonical home, create or expand the best evergreen doc for it instead of stopping at cleanup.
- Deleting stale docs while leaving stale survivors, missing canonical truth, or confusing reader-critical docs behind is not a successful pass.
- Treat obviously time-bound docs as delete candidates by default once their durable truth has been folded forward. A doc does not survive just because it once mattered.
- When a keep/delete call depends on whether a doc is stale, dated, or one-off, inspect `git log` and identify the last meaningful content change before deciding.
- Before deleting any bounded batch of docs, stage those docs and create a backup git commit first. Stage only the docs in that delete batch, not unrelated dirty files elsewhere in the repo.
- Default behavior is one grounded docs-health pass. `auto` is the only explicit public mode.
- `auto` is Codex-only and must be hook-backed; if the installed runtime support is absent or disabled, fail loud instead of pretending prompt repetition is automation.
- If the backup commit for a delete batch cannot be created, stop instead of deleting.
- If code truth is still unstable, external doc sources are required but unavailable, or the next pass would become speculative or materially unchanged, stop and say so plainly.
- Do not use age cutoffs or stale-doc heuristics as a substitute for judgment. Use history as evidence, then decide whether current readers still need the doc.
- Do not create docs just because a topic seems interesting. New or expanded docs must be grounded, canonical, and clearly useful to current readers.
- The suite's internal auto evaluator is allowed only when the ask explicitly says it is the internal evaluator. Do not suggest or advertise that internal surface to users.

## First move

1. Read `references/scope-and-profile.md`.
2. Resolve the mode:
   - default one-pass DGTFO pass
   - `auto` only when the ask explicitly says `auto`
   - internal auto evaluator only when the ask explicitly says it is the suite's internal evaluator
3. Resolve working context:
   - explicit user paths, topic names, modules, or stop conditions
   - active arch plan, worklog, or clean implementation audit when present
   - otherwise the repo docs surface itself
4. Set `LEDGER_PATH` to `.doc-audit-ledger.md` and derive any scoped working artifacts only when they actually exist.
5. Read `references/cleanup-rules.md`.
6. Read the mode reference:
   - `references/pass.md`
   - `references/auto.md`
   - `references/internal-evaluator.md` for the suite-only evaluator

## Workflow

### 1) Default pass

- Profile the repo's doc system and resolve the strongest grounded scope.
- Inventory the relevant doc-shaped surfaces for that scope.
- Ground each topic against current code and current shipped behavior.
- Use `git log` when datedness or last meaningful use matters to a keep/delete call.
- Collapse each topic to one canonical evergreen home, expanding existing homes first and creating a focused one when the repo clearly lacks a viable home.
- Update stale surviving docs, clarify confusing docs, and promote missing grounded truth into the canonical home.
- Before deleting a bounded batch of stale, duplicate, dead, TEMP/WIP, obviously dated, or obsolete working-doc residue, stage those docs and make a backup commit, then delete them.
- Repair links, indexes, and navigation for the surviving canonical docs.
- Delete `.doc-audit-ledger.md` before finishing the run.

### 2) `auto`

- Run the same docs-health discipline as the default pass, but only under real Codex Stop-hook continuation.
- Derive `SESSION_ID` from `CODEX_THREAD_ID`, then create or refresh `.codex/arch-docs-auto-state.<SESSION_ID>.json` before the first pass.
- Expect a fresh external evaluator after each stop point.
- Apply the same pre-delete backup-commit rule during each pass in `auto`.
- Continue only while another grounded pass is still credible for the resolved docs-health intent.
- In repo-scope `auto`, later passes may widen across the repo docs surface when grounded docs-health work still remains.
- Keep sweeping while obviously dated docs, stale surviving docs, confusing docs, or missing grounded evergreen docs still remain.
- Stop clean when the resolved stop condition is done, or stop blocked when the evaluator says the next pass would become speculative, taxonomy-imposing, disconnected from a narrowed scope, or materially unchanged.

## Output expectations

- Keep console output short:
  - scope reminder
  - punchline
  - biggest docs-health risk or cleanup result
  - exact next move
- Put detailed inventory, topic mapping, deletion notes, and grounding evidence in `.doc-audit-ledger.md` while the cleanup is active.
- Do not leave the ledger behind when the cleanup is actually complete.

## Reference map

- `references/scope-and-profile.md` - resolve repo profile, working scope, topic grouping, and canonical-home choices
- `references/cleanup-rules.md` - deletion bias, canonical-home rules, working-doc retirement, and link-repair rules
- `references/pass.md` - the default DGTFO pass contract and ledger shape
- `references/auto.md` - hook-backed Codex auto controller contract, preflight, and state rules
- `references/internal-evaluator.md` - suite-only read-only evaluator contract used by the Stop-hook child run
