# Default Arm Mode

## Goal

Arm a real Codex wait controller that keeps checking a condition on a fixed interval until it becomes true or the wait window expires.

## Required runtime preflight

Before arming the controller, verify all of these:

- Codex is the active host runtime
- installed Stop-hook support exists in `~/.codex/hooks.json`
- the installed suite controller runner exists under `~/.agents/skills/arch-step/scripts/`
- `codex features list` shows `codex_hooks` enabled

If any check fails, name the missing prerequisite and stop instead of pretending prompt-only waiting is the same feature.

## State file contract

Resolve `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/delay-poll-state.<SESSION_ID>.json` only after the immediate first check says the condition is still false.

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
