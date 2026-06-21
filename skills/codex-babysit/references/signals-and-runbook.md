# Signals And Runbook

Everything here is operational detail for babysitting a running codex goal-mode
session. Pane strings are verified against **codex v0.137.0** — confirm them
against the running version (`codex --version`); the TUI wording can drift.

## Table of contents

- Pane signal strings
- aim rotation facts
- codex CLI facts that matter
- Runbook: rotate + restart + resume + verify
- No-tight-loop poll pattern
- Self-spawned delegate caveat
- Judging real completion

## Pane signal strings

Read everything from `tmux capture-pane -t <target> -p`. Grep the footer/body for:

- **WORKING**: footer contains `esc to interrupt` (e.g. `Planning a patch
  implementation (2m 20s • esc to interrupt)`). The leading verb is dynamic model
  text — do NOT match on the verb, match on `to interrupt`. Goal-mode also shows
  `Pursuing goal (Nm)` on the right.
- **IDLE / awaiting input**: footer shows `? for shortcuts` and NO `to interrupt`
  line. Idle ≠ done: it can mean finished-a-turn, stalled, paused, or goal-complete.
  Disambiguate with the goal-state strings below.
- **HARD USAGE LIMIT (act)**: `You've hit your usage limit`, `Usage limit reached`,
  `reached your usage limit`, `out of credits`. Goal-mode variant in the footer:
  `Goal hit usage limits (/goal resume)`. Also treat `Goal blocked (/goal resume)`
  as act-now.
- **GOAL PAUSED**: `Goal paused (/goal resume)` — needs a resume nudge, not a rotation.
- **GOAL DONE**: `Goal achieved (...)` in the footer — terminal success state.
- **TRANSIENT (do NOT rotate)**: `Reconnecting... N/M` — codex's own retry/backoff;
  it self-heals. Only act if it is *stuck* reconnecting across many polls.
- **CONTEXT**: footer `Context NN% left`. codex AUTO-COMPACTS near the limit and
  keeps going (you will see it drop to single digits then jump back up). Low
  context is NOT a failure and is not a reason to restart.
- **Empty-composer ghost text** rotates among placeholders such as
  `Implement {feature}` — it is not a state signal; ignore it.

## aim rotation facts

- `aim status` — pool summary; the `CODEX` block at the bottom shows the live
  `active_label` and `account_id`.
- `aim status --accounts` — per-account `5h_used`, `5h_in` (reset), `wk_used`,
  `wk_in`, status, and flags.
- `aim codex use [label]` — rewrites `~/.codex/auth.json`. No label = round-robin
  auto-pick (may land on a high-weekly account); pass an explicit `<label>` to
  control the choice.
- Prefer a `ready` account with low `5h_used` AND low `wk_used`. Auto-pick only
  weighs round-robin/5h, so it can choose a 90%+-weekly account — override it.
- Skip accounts with `st=reauth` / `missing_credentials`, and skip any flagged
  `5h_full`.
- `aim`'s `5h_full` / 100% is a *leading* flag, not a hard block. codex commonly
  keeps working 10+ minutes past it. Rotate on the PANE usage-limit string, not on
  the percentage.
- Do not use the aim "Tend" path (`aim codex run --tend`) for this — drive the
  rotation explicitly with `aim codex use` + a manual restart.

## codex CLI facts that matter

- **Auth is cached at startup.** codex reads `~/.codex/auth.json` once when the
  process starts and caches it in memory. Swapping the file mid-session does
  nothing until the process restarts. So: `aim codex use` ⇒ restart codex.
- **Resume appends to the same session.** `codex resume <SESSION_ID>` reopens the
  existing rollout file (same id) and appends — the goal and history are preserved.
  `codex resume --last` resumes the most recent; prefer the explicit id so a stray
  newer session can't be picked by mistake.
- **Profile flag is global-before-subcommand in practice**, e.g.
  `codex -p yolo resume <SESSION_ID>` works (this is how such sessions are usually
  launched). Match however the session was originally launched.
- Find the session id from the footer or the newest file under
  `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*-<SESSION_ID>.jsonl`.

## Runbook: rotate + restart + resume + verify

Trigger only on a real usage-limit pane string, process death, or a sustained
stuck-reconnect.

1. **Confirm it's real** — a hard usage-limit string / `Goal hit usage limits`, or
   the pane's `pane_current_command` is no longer `codex`. Ignore lone
   `Reconnecting...`.
2. **Pick a fresh account** — `aim status --accounts`; choose a `ready` account
   with low 5h and low weekly. `aim codex use <label>`. Verify: `aim status`
   `active_label` changed and `~/.codex/auth.json` `tokens.account_id` matches.
3. **Kill the pane's codex child** (cleaner than sending keys):
   ```bash
   CPID=$(pgrep -P "$(tmux list-panes -t <target> -F '#{pane_pid}' | head -1)" | head -1)
   kill "$CPID"   # wait until pane_current_command returns to the shell; kill -9 only if it won't exit
   ```
4. **Relaunch + resume the same session**:
   ```bash
   tmux send-keys -t <target> 'codex -p yolo resume <SESSION_ID>' Enter
   ```
   Wait ~15-25s for the TUI to load, then capture the pane.
5. **Re-enter the goal** — a usage-limit-paused goal does NOT auto-resume:
   - If a "Resume paused goal?" menu appears (option 1 "Resume goal" preselected):
     `tmux send-keys -t <target> Enter`.
   - If instead it sits idle showing `Goal paused` / `(/goal resume)` and no menu:
     `tmux send-keys -t <target> '/goal resume' Enter`.
6. **Verify it ACTUALLY resumed work** — footer shows `Pursuing goal` AND a working
   line (`esc to interrupt`) on the NEW account, not immediately re-limited, with
   `Context NN% left` advancing or new tool-call output. Log the account + evidence.

## No-tight-loop poll pattern

The point is to wait between checks without burning your own context and without a
tight loop. Use a backgrounded poller that exits early on trouble and otherwise
emits one healthy tick; re-arm it each wake. Background `sleep` is fine; foreground
`sleep`/busy-poll is not. Adapt the target, interval, and signal strings:

```bash
SESS=<target>; DUR=900; INT=30; el=0      # ~15 min, 30s polls
while [ $el -lt $DUR ]; do
  tmux has-session -t "$SESS" 2>/dev/null || { echo "SIGNAL=SESSIONGONE"; exit 21; }
  cap=$(tmux capture-pane -t "$SESS" -p 2>/dev/null)
  if printf '%s' "$cap" | grep -qE "Usage limit reached|hit your usage limit|out of credits|Goal hit usage limits|Goal blocked"; then
    echo "SIGNAL=RATELIMIT"; exit 10; fi
  [ "$(tmux list-panes -t "$SESS" -F '#{pane_current_command}' | head -1)" != "codex" ] && { echo "SIGNAL=PROCDEAD"; exit 11; }
  # optional: track consecutive 'Reconnecting' polls and exit RECONNECT_STUCK after ~5 in a row
  sleep $INT; el=$((el+INT))
done
ctx=$(printf '%s' "$cap" | grep -oE 'Context [0-9]+% left' | head -1)
printf '%s' "$cap" | grep -q 'to interrupt' && w=working || w=idle
echo "SIGNAL=TICK state=$w ctx=[$ctx]"
```

Run it with your harness's background-job support so it re-invokes you on exit
(trouble fast, or the healthy tick at the interval). On each wake: read the signal,
capture once more, judge, act via the runbook if needed, append one worklog line,
and re-arm. A SIGNAL=TICK with `state=idle` is your cue to look closer (done vs
stalled vs paused), not an automatic alarm.

## Self-spawned delegate caveat

A codex goal often spawns its own sub-agents (`codex exec ...`, e.g. via an
`agent-delegate`-style review). Those children also consume aim accounts and can
even rotate `active_label` themselves when *they* hit a limit. Consequences:

- Pool pressure and rate limits can originate from codex's children, not just the
  pane session.
- Do not assume the active account is the one you last set — re-read
  `aim status` `active_label` at restart time and resume on whatever is current
  and healthy.
- A long "Waiting for background terminal" / "Awaiting review feedback" footer is
  usually a delegate or build running, not a stall. Confirm via the child process
  list / CPU before treating it as stuck; an API-bound delegate sits near 0% CPU
  while still working.

## Judging real completion

Stand down only when the goal is genuinely done:

- Footer reads `Goal achieved`, the session is idle, and codex produced an
  evidenced final report (work done, reviews accepted, checks run, residual issues
  named).
- A multi-part goal is done only when the LAST part is — do not stop after part one.
- Distinguish from look-alikes: `Goal paused` ⇒ resume; idle with no `Goal
  achieved` and goal not met ⇒ stalled, nudge/restart; a single passing check or a
  commit mid-goal ⇒ keep going.
- When in doubt, keep watching. Premature stand-down is the main failure mode.
