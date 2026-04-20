# delay-poll Controller

Core doctrine and lifecycle live in `skills/_shared/controller-contract.md`.
This file documents only the `delay-poll`-specific state schema and
conditional-arm deviation.

## Deviation

`delay-poll` runs one immediate grounded check against `check_prompt` before
arming. If the condition is already true, the parent continues from the same
turn without arming state. If the condition is still false, the parent arms
the controller and the Stop hook owns interval-polled re-checks until the
condition becomes true or the deadline elapses. This is documented in the
shared contract's Deviations section.

The conditional-arm exists to avoid a useless sleep when the user's condition
is already satisfied. It is not a license for the parent turn to disarm
later.

## Verdict source

The Stop hook launches a fresh read-only `check` child on the configured
interval:

- Codex: `codex exec --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox`
  with `$delay-poll check`
- Claude Code: `claude -p --settings '{"disableAllHooks":true}'` with
  `/delay-poll check`

The child returns JSON with `ready`, `summary`, and `evidence`. The Stop hook
parses:

- `ready: true` — the condition is satisfied. The hook clears state and
  resumes the parent thread with `resume_prompt` plus the latest `summary`.
- `ready: false` — the hook keeps state armed, updates `attempt_count`,
  `last_check_at`, and `last_summary`, sleeps `interval_seconds`, and
  re-checks.
- deadline elapsed — the hook clears state.

## State file schema

Paths (session-scoped, per the shared contract):

- Codex: `.codex/delay-poll-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/delay-poll-state.<SESSION_ID>.json`

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

## Continuation rule

- Keep `check_prompt` literal and explicit.
- Keep `resume_prompt` literal and action-ready.
- Default maximum wait window is 24 hours unless the user says otherwise.
- Later polling checks stay read-only. Mutation belongs only to the resumed
  main thread after the condition becomes true.
