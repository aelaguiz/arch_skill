---
name: arch-docs
description: "Aggressively retire stale repo documentation with the DGTFO loop: ground every topic against current code, treat old point-in-time docs as delete candidates by default, fold durable truth into real evergreen homes, and only keep or author standalone docs when current readers genuinely need them. Use when stale worklogs, implementation docs, misleading `living` docs, outdated READMEs, dead migration notes, or explicit hook-backed `auto` docs cleanup in Codex or Claude Code need a code-grounded delete-first pass. Not for generic copy editing, open-ended aspirational doc authoring, or speculative taxonomy redesign."
metadata:
  short-description: "Delete-first docs audit and retirement"
---

# Arch Docs

Use this skill when the code is stable enough to ground documentation against current reality and the main job is retiring stale point-in-time docs aggressively while preserving only the durable truth current readers still need.

## When to use

- The user wants a docs audit pass that finds stale docs, duplicate docs, outdated READMEs, dead migration notes, misleading setup/architecture docs, fake `living` docs, or grounded doc gaps that should exist in real evergreen docs.
- A repo needs topic-first cleanup where one topic may be spread across several files and several files may overlap on the same topic.
- A full-arch plan and worklog should be treated as context, mined for durable truth, and then retired or transformed into evergreen docs.
- The user wants to run the DGTFO loop directly in a repo with no requirement that an arch plan already exists.
- The user explicitly wants `arch-docs auto` in Codex or Claude Code and expects real hook-backed continuation with a fresh external evaluation after each pass.

## When not to use

- The task is generic copy editing, README polish, or human-facing doc writing with no cleanup, clarification, canonicalization, or truth-audit workflow.
- The user wants net-new aspirational docs or a broad taxonomy redesign untethered from repo truth.
- The code is still changing too fast to ground docs honestly. Finish or audit the implementation first.
- The real task is choosing or editing a skill package. Use `skill-authoring`.

## Non-negotiables

- The unit of work is the topic, not the file.
- Adapt to the repo's current doc gravity instead of imposing a new framework.
- Code is ground truth. Existing docs are evidence to inspect, not authority to trust.
- Resolve repo posture from repo evidence: `public OSS` versus `private/internal`.
- If repo posture is unclear, default to `private/internal` instead of guessing `public OSS`.
- Every in-scope topic should end with one canonical evergreen home.
- In `public OSS` repos, treat the standard community-doc surface as expected standalone canonical homes: `README`, `LICENSE*`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `SUPPORT.md`.
- Bias toward deleting stale truth and promoting durable truth. Stale docs are worse than no docs, but missing or confusing canonical docs are also a failure.
- Standalone runs must still work with no `DOC_PATH` and no explicit path arguments.
- If explicit user context or active arch context exists, use it to narrow the audit intelligently. If not, audit the repo's docs surface directly.
- Use a temporary repo-root `.doc-audit-ledger.md` while the cleanup is active. Delete it before the cleanup finishes.
- Promote durable truth into evergreen docs, then delete obsolete working docs, plan/worklog residue, and stale duplicates in scope. Git is the archive.
- Do not trust what a doc calls itself. Folder names like `docs/living` and headers like `Status: LIVING`, `Last verified`, or similar freshness labels are claims to verify against code, not evidence that the doc should survive.
- Create a net-new doc only when it is the canonical result of the cleanup, not because the topic feels interesting.
- New docs are allowed in exactly two grounded cases:
  - a `public OSS` repo is missing a standard community-doc home
  - a differentiated evergreen topic fails the split-versus-expand test in `references/canonical-home-judgment.md`
- Deleting stale docs while leaving stale survivors, missing canonical truth, or confusing reader-critical docs behind is not a successful pass.
- Treat obviously time-bound docs as delete candidates by default once their durable truth has been folded forward. A doc does not survive just because it once mattered.
- In this repo family, point-in-time docs older than 30 days are presumed stale. Survival must be justified with explicit code-grounded current-reader value, not with doc labels, location, or freshness metadata.
- When a keep/delete call depends on whether a doc is stale, dated, or one-off, inspect `git log` and identify the last meaningful content change before deciding.
- Do not make a dead doc look current by editing freshness metadata alone. If the body was not materially re-grounded against current code in the same pass, the doc is still stale and should usually be deleted or folded forward.
- Before deleting any bounded batch of docs, stage those docs and create a backup git commit first. Stage only the docs in that delete batch, not unrelated dirty files elsewhere in the repo.
- Default behavior is one grounded docs-health pass. `auto` is the only explicit public mode.
- `auto` is hook-backed in Codex and Claude Code; if the installed runtime support is absent or disabled, fail loud instead of pretending prompt repetition is automation.
- If the backup commit for a delete batch cannot be created, stop instead of deleting.
- If code truth is still unstable, external doc sources are required but unavailable, or the next pass would become speculative or materially unchanged, stop and say so plainly.
- Do not use age alone as the whole verdict. Use history and current code as evidence, but keep the 30-day presumption strong: old point-in-time docs should earn survival, not the other way around.
- Do not bury standard public-repo docs as README subsections when they should exist as their own conventional docs.
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
5. Read `references/canonical-home-judgment.md`.
6. Read `references/cleanup-rules.md`.
7. Read the mode reference:
   - `references/pass.md`
   - `references/arch-docs-controller.md`
   - `references/internal-evaluator.md` for the suite-only evaluator

## Workflow

### 1) Default pass

- Profile the repo's doc system and resolve the strongest grounded scope.
- Inventory the relevant doc-shaped surfaces for that scope.
- Ground each topic against current code and current shipped behavior.
- Treat every doc label, status line, and freshness header as untrusted until the code and current shipped behavior support it.
- Resolve repo posture from evidence and decide whether the public-repo baseline applies.
- Use `git log` when datedness or last meaningful use matters to a keep/delete call.
- For point-in-time docs older than 30 days, require an explicit code-grounded survival reason before they remain in scope as live docs.
- Collapse each topic to one canonical evergreen home, expanding existing homes first and creating a focused new one only when the canonical-home judgment says the topic should stand alone.
- Update stale surviving docs, clarify confusing docs, and promote missing grounded truth into the canonical home.
- Fold durable truth into an existing evergreen home whenever it fits cleanly. Most aged implementation-pass docs should disappear after that fold-forward instead of becoming standalone evergreen docs.
- Before deleting a bounded batch of stale, duplicate, dead, TEMP/WIP, obviously dated, or obsolete working-doc residue, stage those docs and make a backup commit, then delete them.
- Repair links, indexes, and navigation for the surviving canonical docs.
- Delete `.doc-audit-ledger.md` before finishing the run.

### 2) `auto`

**Arm first, disarm never.** This skill is hook-owned for `auto`. The very first step of every invocation writes a session-scoped controller state file; the very last step of the parent turn is to end the turn. Parent turns do not run the Stop hook, do not delete state, and do not clean up early — the Stop hook is the only process that clears state, and it does so only on `CLEAN`, `BLOCKED`, or deadline. Core doctrine, arm-time ensure-install, session-id rules, conflict gate, staleness sweep, and manual recovery live in `skills/_shared/controller-contract.md`. The rules below describe only what is specific to `arch-docs auto`. State lives at `.codex/arch-docs-auto-state.<SESSION_ID>.json` (Codex) or `.claude/arch_skill/arch-docs-auto-state.<SESSION_ID>.json` (Claude Code); see `references/arch-docs-controller.md` for the state schema.

Workflow:

1. **Arm**: run `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` → resolve session id → write state file → end the turn. The parent pass may run one grounded default DGTFO pass before ending. On Claude Code, resolve the session id first via `arch_controller_stop_hook.py --current-session`; abort with the tool's error message if it fails.
2. **Body** (hook-owned): the Stop hook launches a fresh external evaluator (see `references/internal-evaluator.md`) against the ledger and current code. On `CONTINUE`, the hook starts the next `$arch-docs` pass.
3. **Disarm** (hook-owned): on `CLEAN` or `BLOCKED`, the hook clears state; on `CLEAN` the ledger lifecycle in `references/pass.md` applies.

`arch-docs`-specific rules:

- User-facing invocation is `arch-docs auto` only when the ask explicitly says `auto`.
- Apply the same pre-delete backup-commit rule during each pass in `auto`.
- Keep sweeping while obviously dated docs, stale surviving docs, confusing docs, missing required public-repo docs, or missing grounded evergreen docs still remain.
- In this repo family, keep treating point-in-time docs older than 30 days as presumptively stale until the pass records explicit code-grounded current-reader value for each survivor.
- A pass that mainly refreshed labels like `Status: LIVING` or `Last verified` without materially re-grounding the body is still a stale-doc pass that needs more delete-first cleanup.
- Stop blocked when the evaluator says the next pass would become speculative, taxonomy-imposing, disconnected from a narrowed scope, or materially unchanged.

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
- `references/canonical-home-judgment.md` - resolve repo posture, public-repo baseline docs, and split-versus-expand decisions for new docs
- `references/cleanup-rules.md` - deletion bias, canonical-home rules, working-doc retirement, and link-repair rules
- `references/pass.md` - the default DGTFO pass contract and ledger shape
- `references/arch-docs-controller.md` - arch-docs auto-controller state schema and verdict source (core doctrine lives in `skills/_shared/controller-contract.md`)
- `references/internal-evaluator.md` - suite-only read-only evaluator contract used by the Stop-hook child run
