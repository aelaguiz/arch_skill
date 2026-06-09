---
name: stepwise
description: "Run an ordered multi-step process inside a target repo with one fresh Claude, Codex, or Grok worker session per step, an independent observational critic, and a Stepwise-owned diagnose-and-repair loop that talks to struggling sessions, walks upstream when inputs are suspect, and repairs at root cause. Use for named process execution with strict step ordering and evidence. Do NOT use for plan-doc implementation (arch-step), bet-and-learn optimization (goal-loop), one-shot reviews, or single-turn work."
metadata:
  short-description: "Diagnostic multi-step orchestrator with critics"
---

# stepwise

Execute an ordered multi-step process in a target repo. Each step runs in a
fresh Claude, Codex, or Grok sub-session using the execution settings resolved
for that step. An independent critic sub-session judges whether the attempt
honored its declared contract. When a critic fails or abstains with inspectable
evidence, Stepwise diagnoses the failure before repair: it reads the evidence,
talks directly to the relevant session, walks upstream when inputs are suspect,
and authors the repair prompt itself.

Stepwise maintains a truthful chain from user intent to manifest, from manifest
to owner skill, from owner skill to worker action, from worker action to
evidence, and from evidence to critic judgment. When the chain breaks,
Stepwise locates the break and restores truth. It does not paper over the
break.

## When to use

- "ramp up on <topic> and implement <lesson> strictly according to <skill> order"
- "run <named process> in ../<repo> and make sure no steps are skipped"
- "orchestrate <multi-step flow> with a critic checking each step"
- "just get it done but don't make stuff up" where the request still needs
  ordered sub-sessions and auditable evidence

## When not to use

- Free-form requirement loops with no step manifest -> native `/goal`.
- Plan-doc-backed implementation of a fixed architecture plan -> `$arch-step`.
- Bet-and-learn optimization, one bet per iteration with worklog ->
  `$goal-loop`.
- One-shot review of a diff or branch -> the host agent's normal review
  response or
  `$codex-review-yolo`.
- Work that fits in a single orchestrator turn with no sub-sessions.

## Non-negotiables

- Truthful propagation is the single invariant. Every pass corresponds to
  honest evidence. Every fail is diagnosed to root cause before repair. No step
  passes with fabricated evidence; no repair prompt contains invented
  constraints.
- Pin `raw_instructions` verbatim with `sha256`. Any rewrite clears run state.
- Produce a Step Manifest and confirm it with the user before any step
  executes. Strictness tunes the gate's behavior; it never removes it.
- Every worker step runs in a fresh subprocess. Retry and repair messages
  resume that same session so the worker has its own history.
- Every critic is a fresh, independent subprocess. The critic observes and
  returns structured JSON conforming to `StepVerdict`; it never prescribes
  future worker actions.
- The critic observes; the orchestrator reasons; the worker executes. The
  critic never writes agent commands. The orchestrator never edits target-repo
  files or invents constraints. The worker never sees orchestrator-internal
  vocabulary.
- Every critic fail and every inspectable abstain enters the same diagnostic
  protocol. Stepwise holds read-only diagnostic conversation with the agents
  involved, walking upstream when evidence points there, until root cause is
  located or the diagnostic turn cap is exhausted.
- If diagnosis shows a step received bad input from an earlier step, repair the
  upstream session that owns the bad input. Downstream steps respawn fresh
  after upstream repair; resuming downstream sessions would compound broken
  context.
- Every hard boundary and operational instruction in a repair prompt carries a
  source tag: user, manifest, owner runbook, critic evidence, or confirmed
  diagnosis. Unsourced boundaries or instructions are invented and must be
  removed.
- Learnings are consulted with applicability tests and surfaced in Stepwise's
  reasoning. They never appear as worker-facing doctrine. Workers act on owner
  doctrine, not on Stepwise process memory.
- Both worker and critic subprocesses run dangerous / skip-permissions /
  no-sandbox. The critic's read-only discipline comes from its prompt and
  schema, not a sandbox flag.
- Base runtime/model/effort are supplied by the user or target doctrine for
  worker and critic independently. Ask once if required defaults are missing;
  never silently default.
- Optional execution preferences are interpreted after the Step Manifest is
  drafted. A phrase like "copywriting steps use Claude Fable 5" is a routing
  preference to resolve against real steps, not a built-in category.
- Orchestrator does not persistently load the target repo's contents into its
  own context. It points sub-sessions at paths; sub-sessions read fresh.
- Resolve profile, execution routing, and repair limits from the complete user
  prompt, then quote the source phrase in the announcement when a specific
  phrase drives the decision.
- Default broken-step repair limit is 5 operational repair bounces. A clear
  user bound such as "up to three times" can override it; otherwise keep 5.
  Strict/balanced/lenient never changes this number.
- Diagnostic read-only turns do not consume repair bounces. Operational repair
  prompts do.
- Do not use stateless-only worker subprocess flags because workers must be
  resumable. Critics use the runtime's fresh/stateless command shape where
  supported.
- Silent worker repair past the resolved repair limit, silent skipping, and
  silent advance on fail are forbidden. Apply `stop_discipline` when repair
  capacity is exhausted.
- Fabricated step completion, claim without artifact or transcript evidence,
  fails the step regardless of profile.
- Do not use `/loop`, `ScheduleWakeup`, or any wait-helper to
  bridge step or critic subprocess runs. This skill's execution model is
  foreground `Bash` calls to `run_stepwise.py`. If a subprocess genuinely
  outlasts the shell timeout, use the shell's background support and wait for
  the harness notification.
- Child subprocesses commonly take 5+ minutes, and broad `xhigh` or `max`
  worker/critic turns can reasonably take 20-40 minutes. `stream.log` is live;
  inspect it and process liveness every few minutes rather than polling every
  few seconds or treating a missing final file as a hang before exit.

## First move

1. Capture the user's prompt verbatim. Compute `sha256`.
2. Read `references/strictness-profiles.md`. Interpret profile, forced
   checks, stop discipline, and broken-step repair limit.
3. Read `references/model-and-effort.md` and
   `references/execution-routing.md`. Parse base execution defaults and any
   routing preferences. Ask one consolidated question if required defaults are
   missing.
4. Resolve `target_repo_path` as an absolute path. Fail loud if unresolvable.
5. Read `references/workflow-contract.md` for the five-phase workflow.
6. Read `references/diagnose-and-repair.md` before executing any subprocess
   loop.
7. Read `references/unblocking.md` before deciding a subprocess failure is a
   user-facing blocker.
8. Announce the interpretation before Phase 2.

## Workflow

Five phases. Detail lives in `references/workflow-contract.md`.

1. **Intake & interpretation.** Parse the prompt; set profile, forced checks,
   stop discipline, repair limit, execution defaults, and unresolved execution
   preferences. Announce.
2. **Process grounding.** Read the target repo's `CLAUDE.md` / `AGENTS.md`
   and the named process's `SKILL.md`. Draft steps, resolve execution
   preferences against those steps, and write `manifest.json` per
   `references/manifest-schema.md`.
3. **Plan confirmation.** Print manifest + interpretation. Gate per profile:
   strict always pauses, balanced pauses once, lenient prints and proceeds.
   Always include the resolved execution table.
4. **Step execution loop.** For each step: spawn the worker, spawn the
   observational critic, advance on pass, and on fail or inspectable abstain
   run the single diagnose-and-repair protocol. Repair at the root-cause
   session, respawn downstream fresh after upstream repair, and halt when
   repair capacity or diagnostic clarity is exhausted.
5. **Report.** Per-step status table, run directory path, instructive critic
   observations, diagnostic records, learnings considered/written, and pending
   work if halted. No certification language.

## Output expectations

- Run directory at `.arch_skill/stepwise/runs/<run-id>/` in the orchestrator
  repo root.
- Per-step artifacts under `steps/<n>/try-<k>/`.
- Attempt origin metadata at `steps/<n>/try-<k>/origin.json`.
- Diagnostic records under `steps/<n>/try-<k>/diagnostic/`.
- Learnings under `.arch_skill/stepwise/learnings/`.
- `report.md` summarizing the run in plain English.
- Console summary with run path, status table, and any halted root cause.

## Reference map

- `references/workflow-contract.md` - five phases with inputs, outputs,
  failure modes, and where judgment lives.
- `references/diagnose-and-repair.md` - single failure-handling protocol,
  diagnostic conversation, upstream traversal, repair authorship, budgets, and
  halt conditions.
- `references/strictness-profiles.md` - profile, forced checks, stop
  discipline, and repair-bounce policy.
- `references/model-and-effort.md` - how to elicit base worker/critic runtime,
  model, and effort from the user.
- `references/execution-routing.md` - how to resolve optional execution
  preferences against drafted steps without hardcoded task taxonomies.
- `references/unblocking.md` - how roles handle known blockers before asking or
  halting.
- `references/manifest-schema.md` - Step Manifest and StepDescriptor shape.
- `references/critic-contract.md` - observational StepVerdict schema and check
  definitions.
- `references/step-verdict.schema.json` - canonical StepVerdict JSON schema.
- `references/critic-prompt.md` - verbatim observation-only critic prompt.
- `references/session-prompt-contracts.md` - initial, diagnostic, and repair
  prompt contracts for worker sessions.
- `references/session-resume.md` - Claude and Codex invocation flags, session-id
  capture, and resume behavior.
- `references/run-directory-layout.md` - on-disk artifact layout.
- `references/learnings.md` - persistent process-learning ledger.
- `references/examples.md` - worked examples of local diagnosis and upstream
  traversal.

## The orchestration script

`scripts/run_stepwise.py` is deterministic plumbing. It spawns subprocesses,
captures session ids, writes run-directory artifacts, and validates critic
verdicts. It does not interpret the user's prompt, draft the manifest, decide
root cause, or author repairs.

Subcommands:

- `init-run` - create the run directory and initial `state.json`.
- `step-spawn` - spawn a fresh worker sub-session; capture session id.
- `step-resume` - resume an existing worker session with an operational repair
  prompt.
- `step-diagnose` - resume an existing worker session read-only and write the
  diagnostic turn into `diagnostic/` without consuming a repair bounce.
- `critic-spawn` - spawn a fresh critic with a structured schema; parse and
  validate the observational verdict.
- `latest-session` - print latest try/session metadata for a step.
- `upstream-for` - print manifest-declared upstream artifacts and latest
  sessions for a step.
- `report-scaffold` - print or write a deterministic `report.md` scaffold.

Run `python3 scripts/run_stepwise.py <subcommand> --help` for flags.
