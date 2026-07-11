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
- When independent surface families make delegation worthwhile, use bounded
  clean native read-only mapping slices. Otherwise build the same exhaustive
  map sequentially.
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
- `auto` is goal-mode friendly. In native goal mode, keep running `run` then `review` until no credible audit work remains or a real blocker stops it. Outside goal mode, run one bounded pass and name the exact next command.
- No auto commits. Keep the ledger truthful without relying on git history.

## First move

1. Read `references/ledger-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Read `../_shared/agent-orchestration-policy.md` before dispatching any
   mapping or review child.
4. Resolve the mode:
   - `run`
   - `review`
   - `auto`
5. Resolve repo root, root `.gitignore`, and `_audit_ledger.md`.
6. Read the matching mode reference and `references/quality-bar.md`.

## Parent And Child Roles

- The active parent owns audit scope, ledger writes, decomposition, every
  child-result account, synthesis, accepted repair direction, and the final
  controller verdict. Capture current git status and the relevant diff before
  read-only children run, then compare current state before accepting their
  evidence.
- Mapping slices and each independent `review` critic default to new clean
  same-host native children. In Codex set `fork_turns: "none"`; in Claude use
  a clean named or custom subagent, not a bare conversation fork or skill
  `context: fork` shorthand. Use bounded or full inherited context only for a
  named dependency that exists solely in chat; ordinary context travels via
  the ledger, exact paths, and the child brief.
- Give mappers and critics the strongest read-only capability the host exposes
  and explicitly tell them not to edit or write files, including the ledger.
  They may not create children or invoke delegation, consult, or review skills
  unless the parent explicitly assigns a bounded nested scope and budget.
- Split only across independent surface families or review lenses. Bound
  fanout by available host slots, shared-file or shared-state collision risk,
  and the parent's capacity to inspect and integrate every return.
- If a controller needs a background or external process after the parent turn
  ends, that transport supplies lifecycle continuity, not critic freshness.
  Choose it only when that concrete lifecycle or another benefit is worth its
  process and integration cost under the shared policy.

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
- Have a new clean independent critic re-read the ledger and current repo
  state without writing files; the parent spot-checks and integrates its
  return.
- Confirm whether the map is complete, whether the current or next front comes from the ranked map, and whether verification depth matched the front's consequence.
- Confirm whether the latest editful pass completed and passed the post-change audit for safety, downstream consequences, elegance, and duplication.
- Check whether audit-loop-added or materially rewritten tests explain their purpose clearly enough for a later reviewer to spot a misunderstanding in the protected behavior or expected experience.
- Set the controller verdict to `CONTINUE`, `CLEAN`, or `BLOCKED` and name the next mapping tranche, risk front, or blocker plainly.

### 3) `auto`

`auto` is the repeated audit loop. Native goal mode supplies the repeated turns;
this skill does not install or arm automation hooks.

Workflow:

1. Run one truthful `run` pass. Mapping-only is correct on the first turns.
2. Run a new clean independent `review` critic against `_audit_ledger.md` and
   current repo state, using a same-host native child by default while the
   parent session is active.
3. If review says `CONTINUE`, run the next `$audit-loop run` pass.
4. In native goal mode, keep repeating until review says `CLEAN` or `BLOCKED`.
5. Outside native goal mode, stop after one run/review cycle and print the next exact command.

`audit-loop`-specific rules:

- User-facing invocation is just `audit-loop auto`.
- Dirty or untracked files are not a blocker. Do not refuse to run only because the repo has unrelated dirty or untracked files.
- `auto` must not degrade into a tiny-safe-fix treadmill or skip exhaustive mapping just to land a quick patch.
- Do not auto-commit findings.

## Output expectations

- Update `_audit_ledger.md` in every mode.
- Keep console output short:
  - audit North Star reminder
  - punchline
  - current mapping tranche, risk front, or verdict
  - evidence or tests run
  - next action

## Reference map

- `references/ledger-contract.md` - root ledger shape, status vocabulary, and cleanup lifecycle
- `references/shared-doctrine.md` - prioritization, fix discipline, and anti-patterns
- `references/run.md` - mapping-aware audit or fix pass
- `references/review.md` - new clean docs-only verdict pass
- `references/audit-loop-controller.md` - audit-loop auto status and verdict source
- `references/quality-bar.md` - strong vs weak triage, findings, tests, and stop decisions
