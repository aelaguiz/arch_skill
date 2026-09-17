# Controller Lifecycle Contract

Shared controller lifecycle doctrine for arch_skill. This document owns cross-skill runtime rules for every hook-backed loop skill. Local skill references describe only what is unique to that controller (state schema, verdict source, continuation rule).

## Arm first, disarm never

Hook-backed skills are owned by the installed Stop hook, not by the parent turn. The very first step of every invocation writes a session-scoped controller state file; the very last step of the parent turn is to end the turn. Parent turns do not run the Stop hook, do not delete state, and do not clean up early — the Stop hook is the only process that clears state, and it does so only on `CLEAN`, `BLOCKED`, or deadline.

- If you believe the loop is done, end your turn and let the Stop hook verify and clean up.
- If the loop needs to stop for a reason only you know, say so plainly in the turn text and still end the turn — do not delete state yourself.
- This rule is universal. Individual controllers document their own verdict source (internal, external evaluator, deadline, condition check) in their Deviations section, but none of them override arm first, disarm never.

## Workflow shape for every loop skill

Every hook-backed loop skill follows the same three-step shape.

- Arm: ensure-install → resolve session id → write session-scoped state → end turn.
- Body: (hook-owned) Stop hook runs the controller body.
- Disarm: (hook-owned) Stop hook clears state on terminal verdict.

Three lines. Every loop skill in the suite. The skill-specific reference file fills in what body means (a fresh audit child, a sleep, a condition check, an external evaluator) and what the terminal verdict is (`CLEAN`, `BLOCKED`, deadline, condition-true, max iterations).

## Runtime arm-install (inescapable)

Every arm's first action is the installer. Not check the installer ran — run it, unconditionally, every time:

```bash
python3 ~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py \
  --ensure-installed --runtime <codex|claude>
```

`<runtime>` is `codex` when the active host is Codex, `claude` when it is Claude Code. The installer is idempotent and flock-guarded: parallel sessions converge on the same canonical bytes without races. Do not read settings.json or hooks.json first and decide looks fine, skip. Trusting on-disk state is the failure mode that produced unsuffixed state files and deaf controllers.

- If the installer itself fails loud (missing sibling upsert script, unparseable settings JSON), stop and report the exact error. Do not fall back to a prompt-only loop. Do not write any controller state file until the installer has succeeded.

> **IMPORTANT — Dispatch-time loud verify**
> _callout_
> Every Stop-hook turn runs the same verify at the top of `main()` before touching any state. Any drift (missing Stop entry, stale runner path, missing SessionStart hook on Claude) fails loud with the exact repair command and exits 2 without dispatching. There is no silent migration, no legacy fallback, no transitional shim.

> **WARNING — Forbidden: unsuffixed state paths**
> _callout_
> Writing `<controller>-state.json` without `.<SESSION_ID>` is forbidden on both runtimes. If session-id resolution fails after ensure-install, stop and tell the user to restart the session; do not fall back to a single-slot path. Any unsuffixed file the runner finds on disk is moved to `_stale/` on sight with a loud log line — it is never honored.

## Session identity

Controller state is keyed by session id so concurrent runs in the same working directory do not collide.

- **Codex**: `SESSION_ID` is derived from `CODEX_THREAD_ID` and is always available at arm time.
- **Claude Code**: `SESSION_ID` is cached to disk by the installed `SessionStart` hook at `~/.claude/state/arch_skill/sessions/<CLAUDE_CLI_PID>.json`. At arm time the parent turn resolves it by running `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --current-session`, which walks up the PPID chain to the Claude CLI process and reads the cached record. If the cache is missing, the helper exits 2 with the loud-failure message. There is no single-slot fallback. The first session after `make install` must be restarted so the SessionStart hook fires against the installed runner.

Two sessions in the same repo are isolated because their state files are named with different session ids.

## State file paths

- Codex: `.codex/<controller>-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/<controller>-state.<SESSION_ID>.json`

`<controller>` is the registered controller command (e.g. `auto-plan`, `audit-loop`, `wait`, `delay-poll`, `arch-loop`). The full list is canonical in the runner's `CONTROLLERS` registry; run `arch_controller_stop_hook.py --list-controllers` to see it.

## State file envelope fields

Every state file carries at minimum:

- `version` — integer schema version (currently `1` for all controllers)
- `command` — the controller command (must match the registry entry)
- `session_id` — session id the state was armed under
- `armed_at` — epoch seconds when the state was written

Additional fields are controller-specific; see each skill's per-skill reference.

## Lifecycle

- The parent pass writes the state file after `--ensure-installed` returns 0 and the session id resolves. The write is the last meaningful action of the parent turn. The parent then ends the turn.

- The installed Stop hook runs on turn-end and dispatches to the controller whose state file is present for the current session. The body is controller-specific: a bounded work pass, a fresh audit child, a sleep, a condition check, an external evaluator call.

- The Stop hook clears state only on: `CLEAN` (terminal success), `BLOCKED` (terminal failure), deadline (`deadline_at` has passed), max iterations (controller-specific cap reached), or invalid state (the state file fails validation; the hook moves it to `_stale/` and reports the specific broken field). Parent turns never clear state.

## Parent-pass discipline

The parent pass is the turn the model runs between hook firings. It must advance real state or yield honestly. Five rules govern it universally across every hook-backed skill in this suite.

### Choosing the yield kind

`sleep_for` when the next step is an automated check the parent itself can run later — poll a marker file, re-check a CI status, re-test a background process, wait on a detached job. The parent wakes itself and re-evaluates with no human in the loop. If the work outlasts a single hook-timeout window, arm repeated `sleep_for` pauses: wake, poll, and if not ready arm another `sleep_for`. Detached jobs of any wall-clock length (hours, days) stay on the `sleep_for` track as long as the check is automatable. A long estimated duration is not by itself a reason to escalate to `await_user`.
`await_user` when the next step genuinely requires human input — a clarification, a scope decision, missing context only the user has, or a desire to widen or rescope the run. If the only useful thing the user could do is say wake me up later, that is `sleep_for`, not `await_user`.

### No-progress rule

If two consecutive parent passes produce no real change, the next parent pass must end with `requested_yield: {kind: "await_user", reason: "no progress after 2 passes: ..."}` and end the turn. The Stop hook honors `await_user` by stopping with `continue=False` and leaving the controller armed, so the next user turn naturally resumes dispatch. Do not fire a third identical pass expecting a different verdict.
Real change means at least one of: a repo file edit that did not already exist, a plan or doc edit that changed decision content not just wording, or a new evidence entry the fresh evaluator or audit child has not already seen. Re-reading the plan, re-running a command with the same output, or re-typing the same summary is not real change.

### No invented budgets

Timing belongs to the hook. `deadline_at`, the controller's iteration cap, and the parsed cadence are the real termination conditions on top of the controller's terminal verdicts (`clean`, `blocked`, condition-true). The parent pass does not have a separate in-session budget, wall-time budget, or token budget on top of those.
Do not self-declare `blocked` because remaining work feels expensive, the wall-time estimate looks large, or the external auditor is costly. If a next step is reachable, take it, or arm a paced pause via `requested_yield: {kind: "sleep_for", seconds: <int>, reason: "..."}`. If the armed window is genuinely too small for the work, say so plainly in the turn text and yield with `await_user` so the user can widen the window or rescope.

### Exhaust the frontier before handing to audit

Ending the parent turn is not a cheap checkpoint. Each turn end pays for a full fresh audit or evaluator child run. End the turn when you genuinely believe you are done with everything you can reach right now — the entire current plan frontier, every named audit, every reachable phase — not after one small local fix, one convenient subset, or one phase while later approved phases are still reachable.
If a genuine blocker stops you short of the frontier (missing information, parallel-agent edit, external dependency not ready), yield explicitly via `await_user` or `sleep_for`. Do not end the turn silently mid-frontier.

### Respect the tree state the user gave you

Work on the branch and working tree the user set. Do not stash changes, create new branches, split the work across multiple PRs, or rewrite history. Do not clean up untracked files. Commit hygiene, branch strategy, and PR shape are the user's decisions.

### Parallel-agent edits are a pause signal, not a revert signal

If the working tree contains edits the current pass did not make — an unfamiliar commit, a foreign file, a new compiler error that came from outside this pass — treat it as a likely parallel-agent artifact. Do not revert, overwrite, or rewrite it. Pause briefly via `requested_yield: {kind: "sleep_for", seconds: 300, reason: "unfamiliar tree state; letting parallel agent land its fix"}`. Five minutes is the default. After the pause, re-read tree truth and continue. Escalate to `await_user` only after two consecutive pause-retry cycles fail.

## Conflict gate

One session may arm only one controller kind at a time. If two or more controller state files are armed for the same session when the Stop hook fires, the gate halts the turn with a message listing the offending state files. Different sessions in the same working directory are isolated because their session-scoped paths differ.

## Staleness sweep

On every Stop-hook startup the runner scans both state roots (`.codex/` and `.claude/arch_skill/`) for stale state: `deadline_at` has elapsed by more than a small slack window, or the session id does not match any live session. Stale state is moved to `<root>/_stale/<ISO-timestamp>-<original-name>` and the user is told where it went. The runner does not auto-resume stale state.

## Manual recovery

If a loop left stale state on disk (terminal died, user force-stopped, conflict gate fired), clear it manually.

- One controller, current session: `rm .codex/<controller>-state.<SESSION_ID>.json` or `rm .claude/arch_skill/<controller>-state.<SESSION_ID>.json`
- Every arch_skill state file: `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --disarm-all --yes`
- One controller by name: `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --disarm <controller> --yes`
- Inspect: `arch_controller_stop_hook.py --list-controllers` or `--doctor`

The `--disarm` and `--disarm-all` flags only remove controller state files. They never touch source code, plans, ledgers, or anything outside the two state roots.

## Deviations from the default pattern

Four skills depart from the default arm-first pattern in one specific way each. None of them override arm first, disarm never; each documents a single well-scoped exception.

### delay-poll conditional arm

`delay-poll` runs one immediate grounded check against `check_prompt` before arming. If the condition is already true, it continues from the same turn without arming state. If the condition is still false, it arms and the Stop hook owns interval-polled re-checks.

### arch-loop external evaluator verdict

`arch-loop` is the only controller whose terminal verdict comes from a fresh unsandboxed Codex `gpt-5.4` `xhigh` evaluator subprocess rather than from internal controller logic. The Stop hook launches the evaluator, parses its structured JSON verdict, and transitions state per the skill-specific reference. The parent agent never self-certifies completion. The evaluator is always Codex even when Claude hosts the Stop hook.

### wait one-shot resume

`wait` sleeps inside the Stop hook for a parsed duration (`30m`, `1h30m`, `90s`, `2d`) and fires `resume_prompt` back into the same thread exactly once when the deadline elapses. There is no polling, no re-check, no fresh child run during the wait.

### code-review optional hook-backed invocation

`code-review` has two invocation paths: direct (runs the review subprocess synchronously) and hook-backed (arms state, lets the Stop hook drive the run). Direct invocation does not use this contract at all. Only hook-backed invocation is governed by the rules here. The review subprocess always shells out to a fresh unsandboxed Codex process, even when Claude hosts the Stop hook.

## Gemini note

Loop skills are Codex and Claude Code only. Gemini has no Stop-hook surface, so the Gemini install target omits every loop skill (`arch-loop`, `delay-poll`, `wait`, and every `auto` mode). If the user wants a loop on Gemini, the honest answer is: this suite does not support that yet.

## Adding a new controller

Four steps:

1. Add an entry to `CONTROLLERS` in `skills/arch-step/scripts/arch_controller_stop_hook.py` with the command name, state file name, display name, and dispatch function.
2. Write the controller's `dispatch_<name>(resolved_state, hook_context)` function alongside the registry.
3. Add a per-skill reference file under `skills/<skill>/references/` documenting the state schema, verdict source, and continuation rule. Open with: Core doctrine and lifecycle live in references/controller-lifecycle.md. This file documents only the <name>-specific state schema and verdict source.
4. Import and emit `ControllerLifecycle` in the skill's `SKILL.prompt` via `emit:` and add only the skill-local arm/disarm details to the SKILL body.

No other files should need changes. If a fifth step shows up, that is a sign the pattern has drifted; file a doctrine bug rather than sidestepping it.
