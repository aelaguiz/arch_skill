---
name: audit-loop-sim
description: "Run the standalone real-app automation audit workflow with a root simulator audit ledger: exhaustively map the app, journeys, and current automation surface before any edits, rank automation risk fronts by consequence and proof weakness, then fix the biggest end-to-end automation gaps and same-story bugs without changing contracts. Every editful pass must then audit its own diff for safety, unintended downstream consequences, elegance, and duplication before it can count as done. Use when the user wants repo-wide simulator or emulator automation work, wants the agent to build a full mental model before acting, or wants to leave the automation audit running in Codex or Claude Code until no credible work remains. Not for a single known bug, generic repo audit, or manual QA-only work."
metadata:
  short-description: "Exhaustive map-first real-app automation loop"
---

# Audit Loop Sim

Use this skill when the job is to exhaustively map a mobile app, its journeys, and its current automation surface, rank the strongest automation risk fronts by consequence, reduce the biggest unresolved real-app automation risks without changing contracts, and audit each resulting change before it counts as done.

## When to use

- The user wants a repo-wide simulator or emulator automation pass rather than help with one already-known bug.
- The user wants the agent to build a full mental model of the app and automation surface before acting.
- The user wants to find and close real-app blind spots, weak critical-path automation, or missing end-to-end coverage in priority order.
- The user wants to run one manual pass now or leave the automation audit running in Codex or Claude Code until the worthwhile work is exhausted.

## When not to use

- The task is a concrete known bug, crash, regression, or Sentry issue. Use `bugs-flow`.
- The work is a general repo bug hunt, dead-code sweep, or duplication cleanup rather than a real-app automation audit. Use `audit-loop`.
- The work is fixed-scope feature delivery or architecture planning. Use `arch-step`, `arch-mini-plan`, or `lilarch`.
- The task is manual QA only, a release checklist, or an open-ended optimization loop where the main job is not closing real-app automation risk. Use `goal-loop` or `north-star-investigation`.

## Non-negotiables

- `_audit_sim_ledger.md` at repo root is the source of truth. Add it to the root `.gitignore` immediately.
- Triage before code changes. Do not skip straight to editing because one suspicious line looks fixable.
- Exhaustively map app surfaces, user journeys, and the current automation surface before any product-code or automation edits. If the map is incomplete, update the ledger and stop.
- When independent surface families make delegation worthwhile, use bounded
  clean native read-only mapping slices. Otherwise build the same exhaustive
  map sequentially.
- Rank consequence and impact first, then proof weakness, then fragility. Do not let a tiny safe automation tweak outrank a higher-consequence journey or surface.
- Select a risk front from the completed map, not from a hunch.
- Fix bugs inside the existing product, journey, and automation contracts. If the only apparent fix would change a contract, log the conflict and stop.
- Verification depth must be proportional to downstream consequence and blast radius.
- Every editful pass must run a post-change audit on the actual diff and touched surfaces for safety, downstream consequences, elegance, and duplication before it can stop.
- If that audit fails, repair the issue in the same pass and re-verify before stopping.
- New duplication is illegal. Do not solve a journey or automation front by copying product logic, lane behavior, harness steps, or fallback handling into a second place.
- Use the repo's canonical simulator or device surface and existing automation stack. If the repo ships `mobile-sim`, use `mobile-sim` for simulator or device control instead of inventing a parallel command story.
- Reduce the top unresolved real-app automation risk materially. Do not cash out a pass on a tiny safe test tweak while a bigger justified journey gap still dominates the app.
- It is acceptable and often necessary to touch product code, integration tests, harness helpers, fixtures, native glue, or QA surfaces when they belong to the same automation risk story.
- Broader same-story cleanup is allowed when the post-change audit shows the current fix is awkward or duplicative, but keep it inside the same contract and risk front. Do not build a framework or a parallel harness family.
- If the new automation exposes a same-story app bug, fix it in the same pass instead of leaving a knowingly broken lane behind.
- Prefer behavior-level end-to-end proof on meaningful journeys. Do not write negative-value automation.
- Do not decide that simulator or device work is annoying and quietly downgrade a real-app risk front into Flutter unit or widget tests. Work the sanctioned simulator path for a while, and if it still cannot produce the required real-app signal, stop blocked and name that blocker plainly.
- When iOS simulator is available and the risk is not platform-specific, use iOS for faster iteration and close with one Android confirmation for the same journey before calling a cross-platform risk front done.
- If the current context cannot inspect the sanctioned simulator or device surface for review-only reasons such as sandbox access, host permission errors, or wrapper failures, record the live state as `unknown`. Do not call that alone `BLOCKED`.
- Before declaring a simulator or device front blocked, do one bounded recovery on the sanctioned surface or one bounded host-health recovery when the sanctioned surface lacks the required repair command.
- If repeated cloud runs fail with the same lane-independent provider or infrastructure error and no meaningful app signal, stop honestly and record the provider blocker instead of rerunning the same lane.
- Unrelated dirty or untracked files are not a blocker. Leave them alone unless they directly conflict with the current automation risk front or make verification unsafe.
- Default invocation with no mode is `run`.
- `review` is docs-only.
- `auto` is goal-mode friendly. In native goal mode, keep running `run` then `review` until no credible automation audit work remains or a real blocker stops it. Outside goal mode, run one bounded pass and name the exact next command.
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
5. Resolve repo root, root `.gitignore`, and `_audit_sim_ledger.md`.
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
- Select a mapping or review child only when the host confirms that it inherits
  the sanctioned simulator or device capabilities required by
  `audit-loop-sim`. If the host cannot confirm that inheritance, keep the work
  with the authorized parent or run it sequentially; lack of child access keeps
  live state `unknown` and does not authorize an external transport as a
  capability bypass.
- Split only across independent journey, app, harness, platform, or review
  families. Bound fanout by available host slots, shared-file or shared-state
  collision risk, sanctioned device contention, and the parent's capacity to
  inspect and integrate every return.
- If a controller needs a background or external process after the parent turn
  ends, that transport supplies lifecycle continuity, not critic freshness and
  not new simulator authority. Choose it only for an authorized concrete
  benefit under the shared policy.

## Workflow

### 1) `run`

- Create or repair `_audit_sim_ledger.md` and the `.gitignore` entry.
- Build or refresh the exhaustive map of app surfaces, user journeys, and the current automation surface.
- If the map is incomplete, record the next unfinished mapping tranche in `Next Area`, update the ledger, and stop without edits.
- Once the map is complete, rank automation risk fronts by consequence first, then proof weakness, then fragility.
- Pick the highest-priority unresolved automation risk front from that ranking and record the pre-edit proof plan plus the post-change audit focus.
- Read the implementation and current automation before patching, log findings, and fix the strongest justified work across that risk front.
- When the repo provides `mobile-sim`, use it for simulator or device management. If the current front needs simulator or device proof, do not replace that with Flutter unit or widget tests just because the simulator path is hard; either recover it or stop blocked.
- Verify the changes with proof proportional to the front's consequence.
- Audit the resulting diff and touched surfaces for safety, unintended downstream consequences, elegance, and duplication. If any lens fails, repair it in the same pass and re-verify.
- Update the ledger and stop only when further useful work would require a genuinely different automation story, a new reconnaissance pass, or a real blocker.

### 2) `review`

- Stay docs-only.
- Repair the ledger if it is missing or malformed.
- Have a new clean independent critic re-read the ledger and current repo
  state without writing files; the parent spot-checks and integrates its
  return.
- Confirm whether the map is complete, whether the current or next front comes from the ranked map, and whether verification depth matched the front's consequence.
- Confirm whether the latest editful pass completed and passed the post-change audit for safety, downstream consequences, elegance, and duplication.
- Set the controller verdict to `CONTINUE`, `CLEAN`, or `BLOCKED` and name the next mapping tranche, automation risk front, or blocker plainly.

### 3) `auto`

`auto` is the repeated real-app automation audit loop. Native goal mode supplies
the repeated turns; this skill does not install or arm automation hooks.

Workflow:

1. Run one truthful `run` pass. Mapping-only is correct on the first turns.
2. Run a new clean independent `review` critic against
   `_audit_sim_ledger.md` and current repo state, using a same-host native child
   by default while the parent session is active.
3. If review says `CONTINUE`, run the next `$audit-loop-sim run` pass.
4. In native goal mode, keep repeating until review says `CLEAN` or `BLOCKED`.
5. Outside native goal mode, stop after one run/review cycle and print the next exact command.

`audit-loop-sim`-specific rules:

- User-facing invocation is just `audit-loop-sim auto`.
- Dirty or untracked files are not a blocker. Do not refuse to run only because the repo has unrelated dirty or untracked files.
- `auto` must not downgrade real-app simulator risk into Flutter unit or widget tests. If the sanctioned simulator path cannot produce the required signal, stop blocked and name the blocker plainly.
- Do not auto-commit findings.

## Output expectations

- Update `_audit_sim_ledger.md` in every mode.
- Keep console output short:
  - automation North Star reminder
  - punchline
  - current mapping tranche, automation risk front, or verdict
  - evidence or tests run
  - next action

## Reference map

- `references/ledger-contract.md` - root ledger shape, status vocabulary, and cleanup lifecycle
- `references/shared-doctrine.md` - prioritization, fix discipline, and anti-patterns
- `references/run.md` - mapping-aware automation audit or fix pass
- `references/review.md` - new clean docs-only automation verdict pass
- `references/audit-loop-sim-controller.md` - audit-loop-sim auto status and verdict source
- `references/quality-bar.md` - strong vs weak triage, findings, tests, and stop decisions
