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
- When the runtime supports delegation, use parallel read-only agents during mapping. Otherwise build the same exhaustive map sequentially.
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
- `auto` is hook-backed in Codex and Claude Code and must fail loud when the active host runtime lacks the repo-managed `Stop` entry for the installed runner at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py` (Codex reads it from `~/.codex/hooks.json`; Claude Code reads it from `~/.claude/settings.json`). In Codex that also includes the `codex_hooks` feature gate.
- Missing or deleted auto-controller state is not verdict truth. Repair the state file or ledger from fresh repo context before honoring a stop decision.
- No auto commits. Keep the ledger truthful without relying on git history.

## First move

1. Read `references/ledger-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Resolve the mode:
   - `run`
   - `review`
   - `auto`
4. Resolve repo root, root `.gitignore`, `_audit_sim_ledger.md`, and the host-aware `auto` controller state path described in `references/audit-loop-sim-controller.md`.
5. Read the matching mode reference and `references/quality-bar.md`.

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
- Re-read the ledger and current repo state from fresh context.
- Confirm whether the map is complete, whether the current or next front comes from the ranked map, and whether verification depth matched the front's consequence.
- Confirm whether the latest editful pass completed and passed the post-change audit for safety, downstream consequences, elegance, and duplication.
- Set the controller verdict to `CONTINUE`, `CLEAN`, or `BLOCKED` and name the next mapping tranche, automation risk front, or blocker plainly.

### 3) `auto`

**Arm first, disarm never.** This skill is hook-owned for `auto`. The very first step of every invocation writes a session-scoped controller state file; the very last step of the parent turn is to end the turn. Parent turns do not run the Stop hook, do not delete state, and do not clean up early — the Stop hook is the only process that clears state, and it does so only on `CLEAN`, `BLOCKED`, or deadline. Core doctrine, arm-time ensure-install, session-id rules, conflict gate, staleness sweep, and manual recovery live in `skills/_shared/controller-contract.md`. The rules below describe only what is specific to `audit-loop-sim auto`. State lives at `.codex/audit-loop-sim-state.<SESSION_ID>.json` (Codex) or `.claude/arch_skill/audit-loop-sim-state.<SESSION_ID>.json` (Claude Code); see `references/audit-loop-sim-controller.md` for the state schema.

Workflow:

1. **Arm**: run `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` → resolve session id → write state file → end the turn. The parent pass may run one truthful `run` pass (mapping-only is correct on the first turns) before ending. On Claude Code, resolve the session id first via `arch_controller_stop_hook.py --current-session`; abort with the tool's error message if it fails.
2. **Body** (hook-owned): the Stop hook launches a fresh `review` pass in the active host runtime, reads the verdict from `_audit_sim_ledger.md`, and on `CONTINUE` starts the next `$audit-loop-sim` pass.
3. **Disarm** (hook-owned): on `CLEAN`, the hook clears state, deletes `_audit_sim_ledger.md`, and removes the `.gitignore` entry; on `BLOCKED`, the hook clears state and stops honestly.

`audit-loop-sim`-specific rules:

- User-facing invocation is just `audit-loop-sim auto`.
- Missing or deleted controller state is not verdict truth. Repair the state file or ledger from fresh repo context before honoring a stop decision.
- Dirty or untracked files are not a blocker. Do not refuse to arm only because the repo has unrelated dirty or untracked files.
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

- `references/ledger-contract.md` - root ledger shape, controller block, status vocabulary, and cleanup lifecycle
- `references/shared-doctrine.md` - prioritization, fix discipline, and anti-patterns
- `references/run.md` - mapping-aware automation audit or fix pass
- `references/review.md` - fresh docs-only automation verdict pass
- `references/audit-loop-sim-controller.md` - audit-loop-sim controller state schema and verdict source (core doctrine lives in `skills/_shared/controller-contract.md`)
- `references/quality-bar.md` - strong vs weak triage, findings, tests, and stop decisions
