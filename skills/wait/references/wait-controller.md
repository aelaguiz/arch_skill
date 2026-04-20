# wait Controller

Core doctrine and lifecycle live in `skills/_shared/controller-contract.md`.
This file documents only the `wait`-specific duration grammar, state schema,
and one-shot resume semantics.

## Deviation

`wait` is a one-shot resume controller. It sleeps inside the installed Stop
hook for a parsed duration and injects `resume_prompt` back into the same
thread exactly once when the deadline elapses. There is no polling, no
re-check, no fresh child run. This is documented in the shared contract's
Deviations section.

`wait` never launches a child run, so it does not need the Claude
hook-suppressed child-run health check that `delay-poll` performs.

## Duration grammar

Parse the user-supplied duration with `parse_wait_duration` from the shared
runner. Accept only the following grammar:

- One or more `<N><unit>` components concatenated with no separators and no
  whitespace.
- `N` is a positive integer (base 10, no leading `+` or `-`).
- `unit` is exactly one of `s`, `m`, `h`, `d` (seconds, minutes, hours, days).
- Components are summed. Ordering is not enforced; `1h30m` and `30m1h` both
  parse to 5400 seconds.
- Each unit may appear at most once per string. `1h2h` is rejected.

Examples that must parse:

| Input        | Seconds |
|--------------|---------|
| `90s`        | 90      |
| `30m`        | 1800    |
| `1h`         | 3600    |
| `2d`         | 172800  |
| `1h30m`      | 5400    |
| `2h15m30s`   | 8130    |

Strings that must fail-loud with a `ValueError`:

- empty string
- leading, trailing, or embedded whitespace (the caller is responsible for
  stripping outer whitespace; the parser rejects `1 h`, ` 1h`, `1h ` verbatim)
- unknown units (`1w`, `1y`, `1ms`)
- zero or negative components (`0m`, `-1h`)
- natural-language forms (`half an hour`, `30 minutes`, `an hour`)
- duplicate units (`1h2h`, `15m30m`)

An unparseable duration means refuse to arm. Do not guess, round, or
"interpret" natural-language input.

## State file schema

Paths (session-scoped, per the shared contract):

- Codex: `.codex/wait-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/wait-state.<SESSION_ID>.json`

Exact shape (this is the only schema the runner's `validate_wait_state`
accepts):

```json
{
  "version": 1,
  "command": "wait",
  "session_id": "<SESSION_ID>",
  "armed_at": 1760000000,
  "deadline_at": 1760005400,
  "resume_prompt": "Continue investigating the regression report now that we have waited for the upstream build."
}
```

Field rules enforced by `validate_wait_state`:

- `version` must equal `1`.
- `command` must equal `"wait"`.
- `session_id` must match the hook's current session.
- `armed_at` must be a positive integer epoch-seconds value.
- `deadline_at` must be an integer strictly greater than `armed_at`.
- `resume_prompt` must be a non-empty trimmed string. The runner stores it
  with leading/trailing whitespace stripped.

No `delay-poll`-only fields may appear. Specifically, **none of**
`interval_seconds`, `check_prompt`, `attempt_count`, `last_check_at`, or
`last_summary` may be present. The runner rejects state files that carry any
of them: it clears the state and exits with status 2 and a message naming
the offending field. This explicit rejection keeps the `wait` schema from
drifting into the `delay-poll` schema.

## Continuation rule

The loop fires exactly once when `deadline_at` elapses. The Stop hook injects
`resume_prompt` verbatim and clears state. There is no re-check.

- Default maximum wait window is 24 hours (86400 seconds). If the user
  explicitly names a longer cap at arm time, the arm path may set a larger
  `deadline_at`; otherwise reject durations exceeding 24 hours.
- Re-arming `wait` in a session that already has a `wait` state file
  overwrites the prior state; only one resume fires per armed state.
- Keep `resume_prompt` literal and action-ready. The Stop hook injects it
  verbatim; do not include TODOs, placeholders, or conditional branches.
