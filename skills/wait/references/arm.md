# Default Arm Mode

## Goal

Arm a real one-shot wait controller in Codex or Claude Code that sleeps inside the installed Stop hook for a parsed duration and then injects a literal resume prompt back into the same visible thread exactly once. No polling. No re-checking. No fresh child run.

## Duration grammar

Parse the user-supplied duration with `parse_wait_duration` from the shared runner. Accept only the following grammar:

- One or more `<N><unit>` components concatenated with no separators and no whitespace.
- `N` is a positive integer (base 10, no leading `+` or `-`).
- `unit` is exactly one of `s`, `m`, `h`, `d` (seconds, minutes, hours, days).
- Components are summed. Ordering is not enforced; `1h30m` and `30m1h` both parse to 5400 seconds.
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
- leading, trailing, or embedded whitespace (the caller is responsible for stripping outer whitespace; the parser rejects `1 h`, ` 1h`, `1h ` verbatim)
- unknown units (`1w`, `1y`, `1ms`)
- zero or negative components (`0m`, `-1h`)
- natural-language forms (`half an hour`, `30 minutes`, `an hour`)
- duplicate units (`1h2h`, `15m30m`)

An unparseable duration means refuse to arm. Do not guess, round, or "interpret" natural-language input.

## Required runtime preflight

Before arming the controller, verify all of these:

- the active host runtime is Codex or Claude Code
- the active runtime has the arch_skill-managed `Stop` entry
- that `Stop` entry points at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex` in Codex or `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude` in Claude Code
- the installed shared runner actually exists at that path
- in Codex, `codex features list` shows `codex_hooks` enabled

`wait` explicitly does NOT require the Claude hook-suppressed child-run preflight that `delay-poll` requires (`claude -p --settings '{"disableAllHooks":true}'`). That preflight exists because `delay-poll` launches fresh child runs at each re-check; `wait` never launches a child run and never re-evaluates anything, so that leg is irrelevant and is deliberately omitted.

If any check fails, name the missing prerequisite and stop instead of pretending prompt-only waiting is the same feature.

Do not look for a dedicated wait-specific runner such as `wait_controller.py`; `wait` is backed by the shared suite hook at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`, the same installed runner that owns the other arch_skill auto controllers.

## State file contract

Create the host-aware state path only after the duration has parsed and the runtime preflight has passed:

- Codex: derive `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/wait-state.<SESSION_ID>.json`
- Claude Code: prefer `.claude/arch_skill/wait-state.<SESSION_ID>.json` when the session id is available before the first Stop-hook turn; otherwise create `.claude/arch_skill/wait-state.json` and let the first Stop-hook turn claim session ownership via the same legacy-claim branch `delay-poll` uses

Exact shape (this is the only schema the runner's `validate_wait_state` accepts):

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
- `session_id` must match the hook's current session (or the legacy-claim branch applies for unsuffixed Claude Code state only).
- `armed_at` must be a positive integer epoch-seconds value.
- `deadline_at` must be an integer strictly greater than `armed_at`.
- `resume_prompt` must be a non-empty trimmed string. The runner stores it with leading/trailing whitespace stripped.

No `delay-poll`-only fields may appear. Specifically, **none of** `interval_seconds`, `check_prompt`, `attempt_count`, `last_check_at`, or `last_summary` may be present. The runner rejects state files that carry any of them: it clears the state and exits with status 2 and a message naming the offending field. This explicit rejection keeps the `wait` schema from drifting into the `delay-poll` schema.

## Arm rules

- Keep `resume_prompt` literal and action-ready. The Stop hook injects it verbatim; do not include TODOs, placeholders, or conditional branches inside it.
- Default maximum wait window is 24 hours (86400 seconds). If the user explicitly names a longer cap at arm time, the arm path may set a larger `deadline_at`; otherwise reject durations exceeding 24 hours.
- After the controller is armed, tell the user plainly to end the turn and let the installed Stop hook own the wait. No progress pings, no "checking in," no partial fires.
- If a `wait` state file already exists for this session, the arm writes overwrite it. Only one resume ever fires per armed state; re-arming replaces, it does not stack.
- If any other `arch_skill` controller state is already armed for this session (for example, `delay-poll`, `auto-plan`, `implement-loop`), the shared runner's conflict gate (`block_when_multiple_controller_states_armed`) halts the next turn with a conflict message listing both state files. Do not arm `wait` alongside another kind; resolve the conflict first.

## Fail-loud conditions

Refuse to arm (and name the cause) when any of the following are true:

- `parse_wait_duration` raises `ValueError`.
- the computed duration is 0 or negative.
- the computed duration exceeds 24 hours without an explicit user override.
- the active host runtime is neither Codex nor Claude Code.
- the active runtime does not have the repo-managed `Stop` entry pointing at the shared runner with the correct `--runtime` argument.
- the installed shared runner does not exist at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`.
- in Codex, `codex_hooks` is disabled.
- another `arch_skill` controller state is already armed for this session.

Do not invent runtime shims, fallback sleep loops, or "graceful degradation" paths. `fallback_policy: forbidden` applies.
