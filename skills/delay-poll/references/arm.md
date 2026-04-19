# Default Arm Mode

## Goal

Arm a real wait controller in Codex or Claude Code that keeps checking a condition on a fixed interval until it becomes true or the wait window expires.

## Required runtime preflight

Before arming the controller, verify all of these:

- the active host runtime is Codex or Claude Code
- the active runtime has the arch_skill-managed `Stop` entry
- that `Stop` entry points at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex` in Codex or `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude` in Claude Code
- in Codex, `codex features list` shows `codex_hooks` enabled
- in Claude Code, hook-suppressed child checks via `claude -p --settings '{"disableAllHooks":true}'` work with the machine's normal Claude auth

If any check fails, name the missing prerequisite and stop instead of pretending prompt-only waiting is the same feature.
Do not look for a dedicated delay-specific runner such as `delay_poll_controller.py`; `delay-poll` is backed by the shared suite hook at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`, the same installed runner that owns the other arch_skill auto controllers.

## State file contract

Create the host-aware state path only after the immediate first check says the condition is still false:

- Codex: derive `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/delay-poll-state.<SESSION_ID>.json`
- Claude Code: prefer `.claude/arch_skill/delay-poll-state.<SESSION_ID>.json` when the session id is available before the first Stop-hook turn; otherwise create `.claude/arch_skill/delay-poll-state.json` only as a legacy single-slot fallback and let the first Stop-hook turn claim it into the session-scoped path

Minimum shape:

```json
{
  "version": 1,
  "command": "delay-poll",
  "session_id": "<SESSION_ID>",
  "interval_seconds": 1800,
  "armed_at": 1760000000,
  "deadline_at": 1760086400,
  "check_prompt": "Check whether branch blah has been fully pushed yet.",
  "resume_prompt": "Pull branch blah and integrate it in.",
  "attempt_count": 1,
  "last_check_at": 1760000000,
  "last_summary": "Remote still does not show the expected pushed commit."
}
```

## Arm rules

- Keep `check_prompt` literal and explicit.
- Keep `resume_prompt` literal and action-ready.
- Default maximum wait window is 24 hours unless the user says otherwise.
- After the controller is armed, tell the user plainly to end the turn and let the installed Stop hook own the wait.
- Do not claim the feature is real if the current runtime cannot actually arm the state and rely on the installed Stop hook.
- Real missing prerequisites here are:
- no usable arch_skill-managed `Stop` entry for the active host runtime
- no installed shared runner at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`
- `codex_hooks` disabled in Codex
- hook-suppressed child checks via `claude -p --settings '{"disableAllHooks":true}'` unavailable or unauthenticated in Claude Code
