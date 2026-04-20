---
name: delay-poll
description: "Arm a delay-and-check controller for Codex and Claude Code that waits inside the installed Stop hook, re-runs a read-only condition check on a fixed interval, and resumes the same thread when the condition becomes true. Use when the user wants Codex or Claude Code to keep checking something every 30 minutes, every hour, or similar and continue later when it becomes true. Not for background daemons, non-hook runtimes, or one-shot checks."
metadata:
  short-description: "Wait and recheck controller"
---

# Delay Poll

Use this skill when the user wants the same visible Codex or Claude Code thread to wait, re-check some external condition on a fixed interval, and continue only after that condition becomes true.

## When to use

- The user wants Codex or Claude Code to keep checking whether something external has changed before continuing the same task.
- The user names an interval such as every 30 minutes, every hour, or similar.
- The user wants real hook-backed waiting rather than a manual reminder or a one-shot check.

## When not to use

- The task only needs one immediate check right now.
- The user wants a background scheduler, notification daemon, or work that must survive after the current session or host goes away.
- The runtime is neither Codex nor Claude Code, or the installed Stop-hook path is unavailable.
- The user wants open-ended repeated work rather than "wait until this condition is true, then continue." Use the owning workflow instead.

## Non-negotiables

- `delay-poll` must be real hook-backed behavior in Codex and Claude Code. The installed runner is the shared suite hook at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`. If that runner or the active host runtime's repo-managed `Stop` entry is missing, fail loud. In Codex that means `~/.codex/hooks.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex` plus the `codex_hooks` feature gate. In Claude Code that means `~/.claude/settings.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude`.
- Keep the waited-on condition as a literal `check_prompt` and the continuation as a literal `resume_prompt`. Do not invent git-specific, CI-specific, or service-specific heuristics.
- Do one immediate grounded check before arming the wait state. If the condition is already true, do not arm the controller.
- Default maximum wait window is 24 hours unless the user explicitly sets a different cap.
- Later polling checks stay read-only. Mutation belongs only to the resumed main thread after the condition becomes true.
- One session may arm only one arch_skill controller kind at a time. If another controller state is already armed for the same session, the installed Stop hook stops with a conflict message naming the files.
- Do not look for or require a dedicated delay-specific runner file such as `delay_poll_controller.py`. `delay-poll` is owned by the shared suite hook, not a separate controller binary.
- Do not run the Stop hook yourself. After the controller is armed, just end the turn and let the installed Stop hook run.
- Internal `check` mode is suite-only. Do not advertise it as a public user workflow.

## First move

1. Resolve the mode:
   - default arm mode
   - `check` only when the invocation explicitly says `check`
2. Read the matching reference:
   - `references/delay-poll-controller.md`
   - `references/check.md`
3. Resolve repo root and the host-aware `delay-poll` controller state path described in `references/delay-poll-controller.md`.
4. In default arm mode, run `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` as described in `skills/_shared/controller-contract.md` before creating controller state. The installer fails loud if it cannot write the canonical Stop entry; do not proceed on failure.

## Workflow

**Arm first, disarm never.** This skill is hook-owned. The very first step of every invocation writes a session-scoped controller state file; the very last step of the parent turn is to end the turn. Parent turns do not run the Stop hook, do not delete state, and do not clean up early — the Stop hook is the only process that clears state, and it does so only when the condition becomes true, the deadline elapses, or the evaluator blocks. Core doctrine, arm-time ensure-install, session-id rules, conflict gate, staleness sweep, and manual recovery live in `skills/_shared/controller-contract.md`. `delay-poll` uses a documented conditional-arm deviation (shared contract, Deviations section): the parent runs one immediate grounded check before arming so a condition that is already true does not cost a useless sleep. If the pre-check passes, the parent continues from the same turn without arming state. State lives at `.codex/delay-poll-state.<SESSION_ID>.json` (Codex) or `.claude/arch_skill/delay-poll-state.<SESSION_ID>.json` (Claude Code); see `references/delay-poll-controller.md` for the state schema.

### 1) Default arm mode

1. **Arm**: ensure-install the Stop hook (`arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>`; fails loud on drift) → resolve the session id (on Claude Code via `arch_controller_stop_hook.py --current-session`; abort with its error if it fails) → resolve literal `check_prompt`, polling interval, maximum wait window, and `resume_prompt` (default resume prompt when the user did not supply one: `The waited-on condition is now satisfied. Continue the same task using this new truth and the latest check summary below.`) → run one immediate grounded read-only check against the literal `check_prompt`. If the condition is already true, continue from the same turn with the `resume_prompt` plus the latest summary and do not arm state. If the condition is not yet true, write the session-scoped state file and end the turn.
2. **Body** (hook-owned): the installed Stop hook sleeps, launches a fresh read-only `check` child on the configured interval (Codex: `codex exec --ephemeral`; Claude Code: `claude -p --settings '{"disableAllHooks":true}'`), parses `ready`/`summary`/`evidence`, and resumes the parent thread with `resume_prompt` and the latest summary when `ready` is true.
3. **Disarm** (hook-owned): the Stop hook clears state when the condition becomes true, the deadline elapses, or a fresh evaluator blocks.

### 2) `check` mode

- Stay read-only.
- Evaluate only the literal `check_prompt` passed in the current invocation.
- Ground the answer in current repo truth, current external truth, or both, depending on what the prompt actually asks for.
- Return structured JSON only with:
  - `ready`
  - `summary`
  - `evidence`

## Output expectations

- Default arm mode: keep console output short:
  - waited-on condition reminder
  - punchline
  - interval and deadline
  - whether the controller armed or the condition was already ready
  - exact next move
- `check` mode: return structured JSON only. `summary` must be non-blank. `evidence` should be a short list of concrete facts, not a prose paragraph.

## Reference map

- `references/delay-poll-controller.md` - state schema, conditional-arm deviation, and arm-mode behavior (core doctrine and recovery live in `skills/_shared/controller-contract.md`)
- `references/check.md` - suite-only read-only checker contract and JSON output rules
