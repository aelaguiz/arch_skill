---
name: wait
description: "Arm a one-shot delay-then-resume controller for Codex and Claude Code that sleeps inside the installed Stop hook for a parsed duration (e.g. `30m`, `1h30m`, `90s`, `2d`) and then injects a literal resume prompt back into the same visible thread exactly once. Use when the user wants Codex or Claude Code to wait a specific amount of time and then continue the same task. Not for condition re-checking (use `delay-poll`), recurring or scheduled work (use `/loop` or `schedule`), or work that must survive after the host session exits."
metadata:
  short-description: "One-shot delay-then-resume controller"
---

# Wait

Use this skill when the user wants the same visible Codex or Claude Code thread to sleep for a specific parsed duration and then continue with a literal follow-up prompt exactly once. No polling. No re-checking. One sleep, one fire.

## When to use

- The user names a duration such as `30m`, `1h30m`, `90s`, `2d`, or `45m15s` and wants the same thread to continue after that delay.
- The user wants real hook-backed waiting rather than a manual reminder, an external scheduler, or a spin-loop.
- The continuation prompt is literal and already known at arm time.

## When not to use

- The user wants to re-check a condition repeatedly until it becomes true. Use `delay-poll`.
- The user wants recurring, scheduled, or cron-style work. Use `/loop` or `schedule`.
- The runtime is neither Codex nor Claude Code, or the installed Stop-hook path is unavailable.
- The work must survive after the current session or host exits.
- The duration cannot be parsed by the grammar documented in `references/arm.md`; fail loud rather than guessing.

## Non-negotiables

- `wait` must be real hook-backed behavior in Codex and Claude Code. The installed runner is the shared suite hook at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`. If that runner or the active host runtime's repo-managed `Stop` entry is missing, fail loud. In Codex that means `~/.codex/hooks.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex` plus the `codex_hooks` feature gate. In Claude Code that means `~/.claude/settings.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude`.
- `wait` performs no fresh child run at any point. It is a pure sleep-then-inject primitive. There is no `check` mode, no re-evaluation, no external tool call. If the user wants any of those, route to a different skill.
- Parse the duration exactly as specified in `references/arm.md`. Accept only the documented grammar; reject natural-language forms, negative or zero components, unknown units, and embedded whitespace. An unparseable duration means refuse to arm.
- Keep the continuation as a literal `resume_prompt`. Do not rewrite, summarize, or interpret it.
- Default maximum wait window is 24 hours unless the user explicitly sets a larger cap at arm time. Reject negative or zero durations.
- One session holds at most one arch_skill controller state at a time. The shared runner's conflict gate halts the turn if two or more are armed for the same session, listing the offending state files. Arming `wait` alongside another already-armed controller kind for the same session is a user-visible conflict, not a priority race.
- `wait` is single-slot per session. Re-arming `wait` in a session that already has a `wait` state file overwrites the prior state; only one resume will fire.
- Do not look for or require a dedicated `wait_controller.py`. `wait` is owned by the shared suite hook, not a separate controller binary.
- Do not run the Stop hook yourself. After the controller is armed, just end the turn and let the installed Stop hook sleep and fire.

## First move

1. Read `references/wait-controller.md`.
2. Parse the user-supplied duration with the `parse_wait_duration` grammar. If the string does not parse, name the failure and stop.
3. Run `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` as described in `skills/_shared/controller-contract.md`. The installer fails loud if it cannot write the canonical Stop entry; do not proceed on failure.
4. Resolve the host-aware `wait` controller state path described in `references/wait-controller.md`.

## Workflow

**Arm first, disarm never.** This skill is hook-owned. The very first step of every invocation writes a session-scoped controller state file; the very last step of the parent turn is to end the turn. Parent turns do not run the Stop hook, do not delete state, and do not clean up early — the Stop hook is the only process that clears state, and it does so only when the deadline elapses. Core doctrine, arm-time ensure-install, session-id rules, conflict gate, staleness sweep, and manual recovery live in `skills/_shared/controller-contract.md`. `wait` is a one-shot resume controller (documented in the shared contract's Deviations section): it sleeps inside the Stop hook, fires `resume_prompt` back into the same thread exactly once when the deadline elapses, and never launches a child run. State lives at `.codex/wait-state.<SESSION_ID>.json` (Codex) or `.claude/arch_skill/wait-state.<SESSION_ID>.json` (Claude Code); see `references/wait-controller.md` for the state schema.

Workflow:

1. **Arm**: ensure-install the Stop hook (`arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>`; fails loud on drift) → resolve the session id (on Claude Code via `arch_controller_stop_hook.py --current-session`; abort with its error if it fails) → resolve the literal `resume_prompt` (if the user did not supply one explicitly, ask; never invent a prompt) → parse the duration into `duration_seconds` (refuse to arm if 0, negative, or exceeds 24 hours without an explicit cap override) → compute `armed_at = current_epoch_seconds()` and `deadline_at = armed_at + duration_seconds` → write state → end the turn.
2. **Body** (hook-owned): the installed Stop hook sleeps until `deadline_at` and then injects `resume_prompt` verbatim back into the same visible thread exactly once.
3. **Disarm** (hook-owned): the Stop hook clears state when the deadline fires.

There is no `check` mode. There is no other mode. `wait` never launches a child run, so no child-run health check is needed.

## Output expectations

- Keep console output short:
  - the parsed duration expressed in human units (e.g. "1h30m = 5400s")
  - the computed `deadline_at` (or the equivalent wall-clock time the Stop hook will resume at)
  - the literal `resume_prompt` as it will be injected
  - whether the controller armed successfully
  - the exact next move (end the turn)
- No progress updates. No status lines. No "checking in" while the wait is armed. The Stop hook owns the entire wait window.

## Reference map

- `references/wait-controller.md` - duration grammar, state file schema, and arm-mode behavior (core doctrine, arm-time ensure-install, and recovery live in `skills/_shared/controller-contract.md`)
