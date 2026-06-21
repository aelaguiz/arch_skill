---
name: codex-babysit
description: "Monitor and keep alive a long codex goal-mode session that is already running in a tmux pane, until codex's own goal genuinely completes. Watch the pane for usage limits, stalls, or process death; on a real usage limit rotate the aim account (`aim status` then `aim codex use <label>`), then kill, restart, and `codex resume <session-id>` the SAME session, clear the 'Resume paused goal?' menu, and verify it ACTUALLY resumed work on the new account; check on a ~15-min cadence via a background poll, never a tight loop. Use when the user says monitor/babysit/watch/keep-running my codex, keep it going across rate limits, or restart-and-resume it when limited. Not for spawning a worker to do a task (`agent-delegate`), running your own goal-seeking loop (`goal-loop`), a one-off codex review (`codex-review-yolo`), or purging ~/.codex state (`codex-cleanup`)."
metadata:
  short-description: "Babysit a running codex goal-mode tmux session across usage limits"
---

# codex-babysit

Use this skill when a `codex` session is **already running a long goal** (goal-mode,
footer shows `Pursuing goal`) inside a tmux pane, and the user wants it kept alive
across usage limits, stalls, and restarts until that goal genuinely finishes —
often unattended for hours.

This skill is a **watchdog, not a worker**. It does not do codex's task and does
not launch the session. It watches the pane, decides when codex is actually stuck
versus just slow, rotates the aim account when codex hits a real usage limit,
restarts and resumes the *same* session, and proves work resumed — on a cadence
that does not burn your own context. The hard parts are all judgment: telling a
real limit from a transient blip, an idle-because-done from an idle-because-stuck,
and "restarted" from "actually resumed work."

## When to use

- The user says "monitor / babysit / watch / keep running my codex", "keep it
  going when it gets rate limited", "restart and resume it if it hits a usage
  limit", or "make sure my long codex goal finishes overnight".
- A codex goal-mode session is live in a known tmux pane and the work will outlast
  one account's usage window, so account rotations will be needed.
- The user wants hands-off continuity: codex should keep making progress even as
  individual accounts hit their 5h/weekly caps.

## When not to use

- You need to *launch* a subprocess/worker to do a task → `agent-delegate`.
- You want to run *your own* goal-seeking loop where you make the bets →
  `goal-loop`.
- You want a one-off external review from codex on an artifact → `codex-review-yolo`.
- You need to clean bloated `~/.codex` state → `codex-cleanup`.
- There is no live codex session/pane to watch yet. Start it (or have the user
  start it) first; this skill keeps an existing session alive, it does not create one.

## Non-negotiables

- **Judge state from the PANE, not from aim percentages.** `aim`'s `5h_full` /
  100% is a *leading accounting flag*, not a hard block — codex keeps working past
  it until the API actually refuses a request. Rotate on real pane signals only.
- **Rotate only on a real usage limit or process death.** Never rotate on a
  transient `Reconnecting...` — it self-heals. Distinguish the two before acting.
- **A process restart is REQUIRED after `aim codex use`.** codex reads
  `~/.codex/auth.json` once at startup and caches it; swapping the file does
  nothing to the running process. Account change ⇒ restart.
- **Resume the SAME session id** (`codex resume <SESSION_ID>`), which appends to
  the same rollout and preserves the goal and history. Do not start a fresh session.
- **"Restarted" is not "resumed work."** After resume, the goal does not
  auto-resume: clear the "Resume paused goal?" menu (Enter on option 1) or send
  `/goal resume`, then verify the footer shows `Pursuing goal` AND a working line
  on the NEW account. Verify every time.
- **Never tight-loop your own context.** Wait between checks with a backgrounded
  poller that exits early on trouble; do not busy-poll in the foreground.
- **Keep going until codex's OWN goal is genuinely complete** (footer
  `Goal achieved` plus a real, evidenced final report) — not until the first green
  moment, a single passing check, or a commit.
- **Keep a short append-only worklog** of every check and every rotation, where
  the user wants it (a docs dir they name, or `/tmp` scratch). Learnings and
  rotations go in as they happen, not at the end.

## First move

1. Read `references/signals-and-runbook.md`.
2. Confirm prerequisites exist on the host: `codex`, `aim`, `tmux`.
3. Identify the target: the tmux session/pane (`tmux capture-pane -t <target> -p`)
   and the codex `<SESSION_ID>` (from the footer or `~/.codex/sessions/...`).
4. Capture the pane once and classify state: working / idle / rate-limited / done.
5. Note the active account and pool headroom: `aim status` (CODEX block) and
   `aim status --accounts`.
6. Start the worklog, then arm the first background poll cycle.

## Workflow

### 1. Establish baseline
Capture the pane, read the footer signals, record the active account and session
id, and confirm codex is actually working (not already idle/stuck). Start the
worklog with the target, session id, account, and the goal it is pursuing.

### 2. Watch on a cadence
Run a background poll (~15 min) that early-exits on a hard usage-limit, process
death, or stuck-reconnect, and otherwise emits one healthy tick. On each wake:
capture, judge, act if needed, append one worklog line, re-arm the next cycle.
Tighten the cadence only during an imminent-incident window. See the reference for
the exact signal strings and the no-tight-loop poll pattern.

### 3. Rotate + restart + resume (on a real limit or death)
Pick a healthy `ready` account with low 5h *and* weekly usage, `aim codex use
<label>`, verify `auth.json`. Kill the pane's codex child, relaunch
`codex resume <SESSION_ID>`, clear the resume-goal menu, and verify `Pursuing
goal` + a working line on the new account. Full step-by-step runbook is in the
reference.

### 4. Judge completion
Stand down only when codex declares the goal genuinely complete (`Goal achieved`
plus an evidenced final report). Carefully distinguish "done" from "idle/stalled"
(nudge/restart) and from "paused" (resume). When unsure, keep watching.

## Output expectations

- A short heartbeat to the user on each healthy tick, and a clear report on every
  rotation: what tripped, which account you moved to, and the evidence that work
  actually resumed.
- An append-only worklog capturing checks, learnings, and every rotation.
- A final stand-down message when the goal is genuinely complete — with the
  evidence (footer, commits, reviews) that it is real, not premature.

## Reference map

- `references/signals-and-runbook.md` — pane signal strings (working / idle / goal
  states / hard limit / transient / done), aim rotation facts, the exact
  kill→restart→resume→verify runbook, the no-tight-loop background poll pattern,
  the self-spawned-delegate caveat, and how to judge real completion.
