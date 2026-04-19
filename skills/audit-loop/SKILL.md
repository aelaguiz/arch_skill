---
name: audit-loop
description: "Run the standalone repo-audit workflow with a root audit ledger: exhaustively map the codebase and current proof surface before any edits, rank risk fronts by consequence and proof weakness, then fix the biggest real bugs, dead code, duplication, and high-value regression gaps without changing contracts. Every editful pass must then audit its own diff for safety, unintended downstream consequences, elegance, and duplication before it can count as done. Use when the user wants a repo-wide audit pass, wants the agent to build a full mental model before acting, or wants to leave the audit running in Codex or Claude Code until no credible audit work remains. Not for a single known bug, feature planning, or generic optimization loops."
metadata:
  short-description: "Exhaustive map-first repo audit loop"
---

# Audit Loop

Use this skill when the job is to exhaustively map a codebase and its current proof surface, rank the strongest risk fronts by consequence, reduce the biggest real unresolved risks without changing contracts, and audit each resulting change before it counts as done.

## When to use

- The user wants a repo-wide audit pass rather than help with one already-known bug.
- The user wants the agent to build a full mental model of the repo before acting.
- The user wants to find and fix real bugs, dead code, duplication, or missing high-value tests in priority order.
- The user wants to run one manual pass now or leave the audit running in Codex or Claude Code until the worthwhile work is exhausted.

## When not to use

- The task is a concrete known bug, crash, regression, or Sentry issue. Use `bugs-flow`.
- The work is fixed-scope feature delivery or architecture planning. Use `arch-step`, `arch-mini-plan`, or `lilarch`.
- The task is an open-ended optimization or investigation loop where the path is unknown and the job is not primarily bug finding. Use `goal-loop` or `north-star-investigation`.

## Non-negotiables

- `_audit_ledger.md` at repo root is the source of truth. Add it to the root `.gitignore` immediately.
- Triage before code changes. Do not skip straight to editing because one suspicious line looks fixable.
- Exhaustively map shipped code surfaces and the current proof surface before any product-code or test edits. If the map is incomplete, update the ledger and stop.
- When the runtime supports delegation, use parallel read-only agents during mapping. Otherwise build the same exhaustive map sequentially.
- Rank consequence and impact first, then proof weakness, then fragility. Do not let a tiny safe fix outrank a higher-consequence surface.
- Select a risk front from the completed map, not from a hunch.
- Fix bugs inside the existing product, API, and behavior contracts. If the only apparent fix would change a contract, log the conflict and stop.
- Verification depth must be proportional to downstream consequence and blast radius.
- Every editful pass must run a post-change audit on the actual diff and touched surfaces for safety, downstream consequences, elegance, and duplication before it can stop.
- If that audit fails, repair the issue in the same pass and re-verify before stopping.
- New duplication is illegal. Do not solve a risk front by copying logic, tests, or fallback handling into a second place.
- Reduce the top unresolved risk materially. Do not cash out a pass on a tiny safe fix while a bigger justified problem still dominates the repo.
- Dead code deletion counts as a fix. Duplication on critical paths counts as real bug prevention work.
- It is acceptable and often necessary to touch multiple files, modules, and tests when they belong to the same risk story.
- Broader same-story cleanup is allowed when the post-change audit shows the current fix is awkward or duplicative, but keep it inside the same contract and risk front. Do not build a framework.
- Prefer behavior-level verification and integration coverage on critical paths. Do not write negative-value tests.
- When you add or materially rewrite a test, leave comments in the test that explain why the behavior matters and what correct user-visible or externally observable outcome should happen. The goal is to make misunderstandings easy to spot later, not to narrate the assertion line by line.
- Unrelated dirty or untracked files are not a blocker. Leave them alone unless they directly conflict with the current risk front or make verification unsafe.
- Default invocation with no mode is `run`.
- `review` is docs-only.
- `auto` is hook-backed in Codex and Claude Code and must fail loud when the active host runtime lacks the repo-managed `Stop` entry for the installed runner at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py` (Codex reads it from `~/.codex/hooks.json`; Claude Code reads it from `~/.claude/settings.json`). In Codex that also includes the `codex_hooks` feature gate.
- No auto commits. Keep the ledger truthful without relying on git history.

## First move

1. Read `references/ledger-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Resolve the mode:
   - `run`
   - `review`
   - `auto`
4. Resolve repo root, root `.gitignore`, `_audit_ledger.md`, and the host-aware `auto` controller state path described in `references/auto.md`.
5. Read the matching mode reference and `references/quality-bar.md`.

## Workflow

### 1) `run`

- Create or repair `_audit_ledger.md` and the `.gitignore` entry.
- Build or refresh the exhaustive map of shipped code surfaces and the current proof surface.
- If the map is incomplete, record the next unfinished mapping tranche in `Next Area`, update the ledger, and stop without edits.
- Once the map is complete, rank risk fronts by consequence first, then proof weakness, then fragility.
- Pick the highest-priority unresolved risk front from that ranking and record the pre-edit proof plan plus the post-change audit focus.
- Read the implementation before the tests, log findings, and fix the strongest justified work across that risk front.
- When the pass adds or materially rewrites tests, make the intent clear in the test code itself so a later reader can see the why and the expected experience or outcome without reconstructing it from the assertion body.
- Verify the changes with proof proportional to the front's consequence.
- Audit the resulting diff and touched surfaces for safety, unintended downstream consequences, elegance, and duplication. If any lens fails, repair it in the same pass and re-verify.
- Update the ledger and stop only when further useful work would require a genuinely different audit story, a new reconnaissance pass, or a real blocker.

### 2) `review`

- Stay docs-only.
- Repair the ledger if it is missing or malformed.
- Re-read the ledger and current repo state from fresh context.
- Confirm whether the map is complete, whether the current or next front comes from the ranked map, and whether verification depth matched the front's consequence.
- Confirm whether the latest editful pass completed and passed the post-change audit for safety, downstream consequences, elegance, and duplication.
- Check whether audit-loop-added or materially rewritten tests explain their purpose clearly enough for a later reviewer to spot a misunderstanding in the protected behavior or expected experience.
- Set the controller verdict to `CONTINUE`, `CLEAN`, or `BLOCKED` and name the next mapping tranche, risk front, or blocker plainly.

### 3) `auto`

- Run host-aware preflight for hooks and feature flags.
- Arm the host-aware `auto` controller state described in `references/auto.md`.
- Do not run the Stop hook yourself. After `auto` is armed, just end the turn and let the installed Stop hook run.
- Run one truthful `run` pass. The first turns may be mapping-only.
- Let the installed Stop hook launch a fresh `review` pass and continue only while the verdict stays `CONTINUE` because mapping work or real unresolved risk still remains.

## Output expectations

- Update `_audit_ledger.md` in every mode.
- Keep console output short:
  - audit North Star reminder
  - punchline
  - current mapping tranche, risk front, or verdict
  - evidence or tests run
  - next action

## Reference map

- `references/ledger-contract.md` - root ledger shape, controller block, status vocabulary, and cleanup lifecycle
- `references/shared-doctrine.md` - prioritization, fix discipline, and anti-patterns
- `references/run.md` - mapping-aware audit or fix pass
- `references/review.md` - fresh docs-only verdict pass
- `references/auto.md` - Codex and Claude Code controller contract and state file
- `references/quality-bar.md` - strong vs weak triage, findings, tests, and stop decisions
