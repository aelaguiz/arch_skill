---
name: stepwise
description: "Run a user-described multi-step process inside a target repo by spawning a fresh Claude or Codex subprocess per step, verifying each step with an independent critic subprocess, and resuming the same step's session to fix critic findings before advancing. Use when the user asks to \"ramp up and execute\" a named process in another repo, \"strictly follow a skill order\", or wants an orchestrator-plus-critic that enforces process adherence without redoing the work itself. Do NOT use for: requirement-satisfaction loops (use arch-loop), plan-doc-backed full-arch implementation (use arch-step), bet-and-learn optimization (use goal-loop), one-shot reviews (use code-review), or work that fits in a single turn."
metadata:
  short-description: "Thoughtful stepwise orchestrator with per-step critic and session resume"
---

# stepwise

Execute an ordered multi-step process in a target repo. Each step runs in a
fresh Claude or Codex sub-session using the execution settings resolved for
that specific step. After each step, an independent critic sub-session judges
whether the step honored its declared contract. On fail, the same step session
resumes with the critic's findings — the orchestrator never redoes the step's
work itself. The orchestrator's job is sequencing, routing, and judgment; the
sub-sessions do the work.

This skill is a thoughtful interpreter, not a script runner. It reads the
user's free-form prompt (often flippant), the target repo's doctrine, and
drafts a concrete Step Manifest. The user confirms the manifest. Then each
step is spawned, critiqued, resumed if needed, and advanced when passing.

## When to use

- "ramp up on <topic> and implement <lesson> strictly according to <skill> order"
- "run <named process> in ../<repo> and make sure no steps are skipped"
- "orchestrate <multi-step flow> with a critic checking each step"
- "just get it done but don't make stuff up" — flippant stop conditions
  embedded in prose; the skill interprets them thoughtfully

## When not to use

- Requirement-satisfaction loop against an auditor → `$arch-loop`.
- Plan-doc-backed implementation of a fixed architecture plan → `$arch-step`.
- Bet-and-learn optimization (one bet per iteration with worklog) →
  `$goal-loop`.
- One-shot review of a diff or branch → `$code-review` or
  `$codex-review-yolo`.
- Work that fits in a single orchestrator turn with no sub-sessions.

## Non-negotiables

- Pin `raw_instructions` verbatim with `sha256`. Any rewrite clears run
  state (pattern from `$arch-loop`).
- Produce a Step Manifest and confirm it with the user before any step
  executes. Strictness tunes the gate's behavior; it never removes it.
- Every step runs in a fresh subprocess — never in orchestrator context.
- Every critic is a fresh subprocess independent of the step subprocess;
  returns structured JSON conforming to `StepVerdict`.
- When a blocker has a known, safe, bounded repair inside the current
  role's authority, perform that repair before escalating. Strictness
  controls checks and retry budget; it is not permission to halt on
  repairable orchestration drift.
- On critic FAIL, resume the same step's session with ONLY the critic's
  `resume_hint` — no orchestrator-authored commentary.
- Both step and critic subprocesses run dangerous / skip-permissions /
  no-sandbox. The critic's read-only discipline comes from its prompt and
  its schema, not a sandbox flag.
- Base runtime/model/effort are supplied by the user or target doctrine for
  step and critic independently. Ask once if required defaults are missing;
  never silently default.
- Optional execution preferences are interpreted after the Step Manifest is
  drafted. A phrase like "copywriting steps use Claude Opus 4.7" is a routing
  preference to resolve against real steps, not a built-in category.
- Orchestrator does NOT edit target-repo files. Only sub-sessions do.
- Orchestrator does NOT persistently load the target repo's contents
  into its own context — it points sub-sessions at paths; sub-sessions
  read fresh.
- No heuristic keyword→profile or keyword→model mapping. Interpretation is
  prose reasoning, taught by `references/strictness-profiles.md` and
  `references/execution-routing.md`.
- No `--ephemeral` on step subprocesses (ephemeral sessions cannot be
  resumed). Critic subprocesses DO use `--ephemeral`.
- Silent retry past the computed cap, silent skipping, and silent advance
  on fail are all forbidden. Apply the user's `stop_discipline`.
- Fabricated step completion (claim without artifact) fails the step
  regardless of profile.
- Do NOT reach for `/loop`, `ScheduleWakeup`, `delay-poll`, or any other
  wait-helper to bridge step or critic subprocess runs. This skill's
  execution model is foreground `Bash` calls to `run_stepwise.py`'s
  `step-spawn` / `critic-spawn` / `step-resume`. `Bash` tolerates up to
  a 10-minute timeout, which covers almost every step on a reasonable
  model. If a subprocess genuinely outlasts that, use Bash's
  `run_in_background` and wait for the harness's automatic
  task-notification — do not wake yourself with `/loop` or
  `ScheduleWakeup` every minute; every wake-up re-injects unrelated
  skill bodies and burns tokens. The orchestrator's waiting mechanism
  is whatever `Bash` already provides.
- When the critic sets `route_to_step_n` on a fail and
  `stop_discipline = autonomous_repair`, the orchestrator reopens the
  named target. The orchestrator does not pick which step to reopen —
  that is the critic's authority.
- Downstream re-runs after an upstream repair are fresh `step-spawn`s,
  not resumes. Their prior context was built on the broken upstream
  artifact; resuming would compound the error.
- Containment on `autonomous_repair` is the target step's own
  `max_retries`. Every reopening is another try on the target; when
  the target's retries exhaust, halt with its last verdict.

## First move

1. Capture the user's prompt verbatim. Compute `sha256`.
2. Read `references/strictness-profiles.md`. Interpret the prompt:
   pick profile, forced checks, stop discipline (`halt_and_ask |
   skip_and_continue | escalate_to_user | autonomous_repair`), retry
   cap.
3. Read `references/model-and-effort.md` and
   `references/execution-routing.md`. Parse base execution defaults and any
   routing preferences from the prompt. Ask one consolidated question if
   required defaults are missing.
4. Resolve `target_repo_path` (absolute). Fail loud if unresolvable.
5. Read `references/workflow-contract.md` for phase-by-phase detail.
6. Read `references/unblocking.md` before executing any subprocess loop.
7. Announce the interpretation before Phase 2.

## Workflow

Five phases. Detail in `references/workflow-contract.md`.

1. **Intake & interpretation.** Parse the prompt; set profile, forced
   checks, stop discipline, retry cap, execution defaults, and unresolved
   routing preferences. Announce.
2. **Process grounding.** Read the target repo's CLAUDE.md and the
   named process's SKILL.md. Draft steps, resolve execution preferences
   against those steps, and write `manifest.json` per
   `references/manifest-schema.md`.
3. **Plan confirmation.** Print manifest + interpretation. Gate per
   profile: strict always pauses, balanced pauses once, lenient
   prints and proceeds. Always include the resolved execution table.
4. **Step execution loop.** For each step: spawn step sub-session
   (fresh, not ephemeral); spawn critic sub-session (ephemeral,
   structured verdict); on pass advance; on fail resume the same
   session with the critic's `resume_hint`; repair known orchestration
   blockers inside the run directory before escalating; on cap exhaustion
   apply `stop_discipline`.
5. **Report.** Per-step status table, run directory path, most
   instructive critic finding, pending work if halted. No
   certification language.

## Output expectations

- Run directory at `.arch_skill/stepwise/runs/<run-id>/` in the
  orchestrator repo root (see `references/run-directory-layout.md`).
- Per-step artifacts under `steps/<n>/try-<k>/` and
  `steps/<n>/try-<k>/critic/`.
- `report.md` summarizing the run in plain English.
- Console summary with the run path and the status table.

## Reference map

- `references/workflow-contract.md` — five phases with inputs,
  outputs, and failure modes. Where judgment lives vs where
  determinism lives.
- `references/strictness-profiles.md` — teach interpretation of
  flippant stop conditions. Prose reasoning, not a keyword table.
- `references/model-and-effort.md` — how to elicit base step/critic
  runtime, model, and effort from the user; ask once if missing.
- `references/execution-routing.md` — how to resolve optional
  user-specified routing preferences against drafted steps without
  hardcoded task taxonomies.
- `references/unblocking.md` — how each role handles known blockers before
  asking or halting.
- `references/manifest-schema.md` — StepDescriptor shape with a
  worked example manifest.
- `references/critic-contract.md` — StepVerdict JSON schema, the
  five checks, strictness scoping, forced-checks rule.
- `references/step-verdict.schema.json` — canonical StepVerdict schema for
  subprocess structured output.
- `references/critic-prompt.md` — verbatim critic prompt body with
  placeholders the orchestrator fills.
- `references/step-prompt-contract.md` — initial and resume prompt
  shapes for step sub-sessions.
- `references/session-resume.md` — exact Claude and Codex flags,
  session-id capture, resume invocation. Verified against
  installed CLI versions.
- `references/run-directory-layout.md` — on-disk artifact layout
  per run.
- `references/examples.md` — seven worked examples including per-step
  execution routing, autonomous repair, and a
  fabrication catch + resume round-trip.

## The orchestration script

`scripts/run_stepwise.py` is the deterministic plumbing layer. It
spawns subprocesses, captures session ids, writes run-directory
artifacts, and parses critic verdicts. It does NOT interpret the
user's prompt, draft the manifest, decide pass/fail, or decide
advance/resume/halt. Those judgments live in the orchestrator's
prose reasoning inside this session, or inside the critic
sub-sessions.

Subcommands:

- `init-run` — create the run directory and initial `state.json`,
  including the pinned execution policy.
- `step-spawn` — spawn a fresh step sub-session; capture session id.
- `step-resume` — resume an existing step session with a resume prompt.
  **Requires the same `--target-repo` as step-spawn** (Claude
  persists sessions per-cwd).
- `critic-spawn` — spawn an ephemeral critic with a structured schema;
  parse the verdict.

Run `python3 scripts/run_stepwise.py <subcommand> --help` for flags.
