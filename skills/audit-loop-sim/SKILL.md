---
name: audit-loop-sim
description: "Run the standalone real-app automation audit workflow with a root simulator audit ledger: find and fix the biggest end-to-end automation gaps, missing high-value mobile coverage, and same-story bugs exposed by simulator or emulator runs. Use when the user wants repo-wide simulator or emulator automation work, wants the agent to push on the highest-value real-app coverage gaps instead of tiny safe test tweaks, or wants to leave the automation audit running in Codex until no credible work remains. Not for a single known bug, generic repo audit, or manual QA-only work."
metadata:
  short-description: "Repo-wide real-app automation risk loop"
---

# Audit Loop Sim

Use this skill when the job is to inspect a mobile app codebase for its biggest unresolved real-app automation risks, push on the strongest current automation risk front until it is materially reduced, and leave a truthful simulator audit ledger behind.

## When to use

- The user wants a repo-wide simulator or emulator automation pass rather than help with one already-known bug.
- The user wants to find and close real-app blind spots, weak critical-path automation, or missing end-to-end coverage in priority order.
- The user wants to run one manual pass now or leave the automation audit running in Codex until the worthwhile work is exhausted.

## When not to use

- The task is a concrete known bug, crash, regression, or Sentry issue. Use `bugs-flow`.
- The work is a general repo bug hunt, dead-code sweep, or duplication cleanup rather than a real-app automation audit. Use `audit-loop`.
- The work is fixed-scope feature delivery or architecture planning. Use `arch-step`, `arch-mini-plan`, or `lilarch`.
- The task is manual QA only, a release checklist, or an open-ended optimization loop where the main job is not closing real-app automation risk. Use `goal-loop` or `north-star-investigation`.

## Non-negotiables

- `_audit_sim_ledger.md` at repo root is the source of truth. Add it to the root `.gitignore` immediately.
- Triage before code changes. Do not skip straight to editing because one suspicious line looks fixable.
- Start with primary journeys and existing repo-native automation evidence. Record unavailable signals as `unknown` instead of auto-installing new tooling.
- Use the repo's canonical simulator or device surface and existing automation stack. If the repo ships `mobile-sim`, use `mobile-sim` for simulator or device control instead of inventing a parallel command story.
- Reduce the top unresolved real-app automation risk materially. Do not cash out a pass on a tiny safe test tweak while a bigger justified journey gap still dominates the app.
- It is acceptable and often necessary to touch product code, integration tests, harness helpers, fixtures, native glue, or QA surfaces when they belong to the same automation risk story.
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
- `auto` is Codex-only and must fail loud when hook support or `codex_hooks` is missing.
- Missing or deleted auto-controller state is not verdict truth. Repair the state file or ledger from fresh repo context before honoring a stop decision.
- No auto commits. Keep the ledger truthful without relying on git history.

## First move

1. Read `references/ledger-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Resolve the mode:
   - `run`
   - `review`
   - `auto`
4. Resolve repo root, root `.gitignore`, `_audit_sim_ledger.md`, and `.codex/audit-loop-sim-state.<SESSION_ID>.json` when in `auto`, with `SESSION_ID` taken from `CODEX_THREAD_ID`.
5. Read the matching mode reference and `references/quality-bar.md`.

## Workflow

### 1) `run`

- Create or repair `_audit_sim_ledger.md` and the `.gitignore` entry.
- Refresh triage from primary journeys, real-app signal, automation gaps, platform truth, churn when useful, and explicit `SKIP` decisions.
- Pick the highest-priority unresolved automation risk front.
- Read the implementation and current automation before patching, log findings, and fix the strongest justified work across that risk front.
- When the repo provides `mobile-sim`, use it for simulator or device management. If the current front needs simulator or device proof, do not replace that with Flutter unit or widget tests just because the simulator path is hard; either recover it or stop blocked.
- Verify the changes, update the ledger, and stop only when further useful work would require a genuinely different automation story, a new reconnaissance pass, or a real blocker.

### 2) `review`

- Stay docs-only.
- Repair the ledger if it is missing or malformed.
- Re-read the ledger and current repo state from fresh context.
- Set the controller verdict to `CONTINUE`, `CLEAN`, or `BLOCKED` and name the next automation risk front or blocker plainly.

### 3) `auto`

- Run Codex-only preflight for hooks and feature flags.
- Derive `SESSION_ID` from `CODEX_THREAD_ID`, then create or refresh `.codex/audit-loop-sim-state.<SESSION_ID>.json`.
- Do not run the Stop hook yourself. After `auto` is armed, just end the turn and let Codex run the installed Stop hook.
- Run one truthful `run` pass.
- Let the installed Stop hook launch a fresh `review` pass and continue only while the verdict stays `CONTINUE` because real unresolved automation risk still remains.

## Output expectations

- Update `_audit_sim_ledger.md` in every mode.
- Keep console output short:
  - automation North Star reminder
  - punchline
  - current automation risk front or verdict
  - evidence or tests run
  - next action

## Reference map

- `references/ledger-contract.md` - root ledger shape, controller block, status vocabulary, and cleanup lifecycle
- `references/shared-doctrine.md` - prioritization, fix discipline, and anti-patterns
- `references/run.md` - risk-front automation audit or fix pass
- `references/review.md` - fresh docs-only automation verdict pass
- `references/auto.md` - Codex-only controller contract and state file
- `references/quality-bar.md` - strong vs weak triage, findings, tests, and stop decisions
