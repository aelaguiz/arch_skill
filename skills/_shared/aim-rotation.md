# Aim Account Rotation For Codex

Shared mechanics for continuing Codex work across hard usage limits by
rotating the active `aim` account and resuming the exact same session. Any
skill that runs or supervises a Codex process may point here; the owning skill
keeps its own trigger signals (pane strings, `stderr.log` shapes) and its own
process mechanics (tmux keys, subprocess relaunch).

## aim facts

- `aim status` — pool summary; the `CODEX` block shows the live
  `active_label` and `account_id`.
- `aim status --accounts` — per-account `5h_used`, `5h_in` (reset), `wk_used`,
  `wk_in`, status, and flags.
- `aim codex use [label]` — rewrites `~/.codex/auth.json`. No label =
  round-robin auto-pick, which only weighs round-robin/5h and can land on a
  90%+-weekly account — pass an explicit `<label>` to control the choice.
- Before every external Codex launch, use `aim status --accounts`, choose a
  ready label with low five-hour and weekly usage (skip `5h_full` or roughly
  over 60% weekly), run `aim codex use <label>`, and confirm
  `aim status --compact`. Launch through AIMgr, never a bare coding CLI.
- `aim`'s `5h_full` / 100% is a *leading* flag, not a hard block; codex
  commonly keeps working past it. Rotate on the runtime's real usage-limit
  signal, not on the percentage.
- Do not use the aim "Tend" path (`aim codex run --tend`) for rotation; drive
  it explicitly with `aim codex use` plus a manual restart.

## codex facts that make rotation work

- **Auth is cached at startup.** codex reads `~/.codex/auth.json` once at
  process start. Swapping the file mid-session does nothing until the process
  restarts. `aim codex use` ⇒ restart the codex process.
- **Resume appends to the same session.** An AIMgr-managed Codex resume reopens
  the existing rollout file and appends; goal and history are preserved.
  Prefer the explicit id over `--last` so a stray newer session cannot be
  picked by mistake.
- Match the original launch shape on resume; the profile flag is
  global-before-subcommand in practice (`codex -p <profile> resume
  <SESSION_ID>`).
- The session id is in the newest file under
  `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*-<SESSION_ID>.jsonl` when it
  was not captured elsewhere.

## Core rotation sequence

1. **Confirm the limit is real.** A hard usage-limit signal or a dead
   process — never a lone transient reconnect, which self-heals.
2. **Pick and switch.** Select a different explicit ready label as above and
   confirm `aim status --compact`; do not print or copy credentials.
3. **Stop the old owned job and restart through AIMgr.** Verify remaining
   descendants exited before relaunch; a live process never picks up new auth.
4. **Resume the exact session** with the captured session id and the original
   launch shape.
5. **Verify progress.** A 429, `usage_limit_reached`, or empty completion gets
   one rotation and same-session retry. Do not wait out limits or substitute a
   different model.

## Pool-pressure caveat

Concurrent external launches share account-selection state; confirm the chosen
label immediately before launching. Native children follow their actual host,
not the executable that launched the parent. In Prime only, children inherit
one root AIMgr binding and cannot rotate independently; move that root with
`aim prime resume <session> --rotate`. Codex and Claude Code keep their native
delegation lane. Claude external execution uses `aim claude run (opus|fable)`.
