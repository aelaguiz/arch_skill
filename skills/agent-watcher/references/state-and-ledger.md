# State And Ledger

Everything the watcher fleet writes lives under `~/.agent-watcher/` (override
with `AGENT_WATCHER_HOME`). The master owns the top level; each watcher owns
one session directory. The files are the continuity: a watcher is a fresh
child at every check and re-anchors from them, and a master that restarts
re-attaches to the roster.

## Layout

```
~/.agent-watcher/
  roster.json          master
  alerts.jsonl         master, appended by notify.py
  discovery.json       master, rewritten by discover_sessions.py each tick
  sessions/<key>/      one per watched session; key is <runtime>-<session id>
    intent.md          watcher
    ledger.md          watcher, append-only
    cursor.json        watcher
    events/            pages written by session_events.py; keep the last few
    escalations/       watcher, one file per finding
```

## roster.json

```json
{
  "started": "2026-09-15T08:00:00-05:00",
  "watcher_model": "opus",
  "watcher_effort": "inherits parent (Claude Code cannot pin per call)",
  "rest_minutes": 10,
  "max_concurrent": 4,
  "wake": "claude session cron */10 on minute 3, expires 2026-09-22",
  "excluded": ["claude-<this master's session id>"],
  "sessions": {
    "codex-01a0...": {
      "runtime": "codex", "path": "...", "cwd": "...",
      "status": "new | watching | dormant | retired | stopped",
      "last_seen_size": 123456, "last_seen_mtime": "...",
      "last_check_started": "...", "last_check_finished": "...",
      "watcher_running": false, "last_verdict": "ALIGNED",
      "idle_raised_at": null,
      "rejected": ["<dedup key>: <one-line reason>"]
    }
  }
}
```

Dormant: no new bytes for six hours and the last event is Amir's turn or a
normal completion. Retired: absent from discovery for 48 hours. Both are
skipped until they move.

## cursor.json

```json
{"runtime": "codex", "path": "...", "cursor": 3871289,
 "last_event_ts": "...", "last_check": "...", "checks": 7}
```

`cursor` is the byte offset returned by `session_events.py`. Never guess it.

## intent.md

Short enough to re-read every check. Suggested shape:

```
# Intent: <key>
Anchored: <ts>   Last revised: <ts>   Runtime: <runtime>   cwd: <cwd>

## His words (verbatim, with timestamps)
- 10:08:45 "We have a feature flag that we flip once an app store version goes live..."
- 10:28:27 "Okay turn the production paywall on for 2.1.42."
- (inherited from <session>: "...")

## What he wants
<plain words: the problem, the outcome he will judge by>

## Boundaries he stated
- ...

## Authorizations on record
- 10:28:27 flip the production paywall flag for 2.1.42
- ...

## Inferred non-goals (inference, confidence)
- no new git worktree, no telemetry polling, no activation record (high)

## Open ambiguities
- ...
```

Revise only when Amir speaks. Date each revision. Keep superseded lines,
struck through or under a "revised" heading, so a later reader can see the
shift.

## ledger.md

Append-only. One line per requirement, decision, or constraint as it enters
the work, then one line per check.

```
2026-09-13 10:08:45 USER      "confirm that I did forget that?"
2026-09-13 10:28:27 USER      "turn the production paywall on for 2.1.42"
2026-09-13 10:28:33 AGENT     plan grew to 4 steps: recheck, worktree, activation record, BigQuery polling  [source: assistant turn]
2026-09-13 10:29:04 AGENT     new git worktree/branch for a flag flip  [tool: git worktree add]
2026-09-13 10:31:10 EXTERNAL  none yet
CHECK 2026-09-15 08:12  cursor 3871289  new events 59  verdict ESCALATE  packet escalations/20260915-0812-receipts-pipeline.md
```

Provenance classes: `USER`, `AGENT` (the coding agent or its own children,
including plans, goals, briefs, heartbeats, workarounds), `EXTERNAL`
(reviewer, panel, audit, Pro consult), and `SELF-FILE` when the agent cites a
file it wrote as authority.

## Escalation packet

`escalations/<YYYYMMDD-HHMM>-<slug>.md`. First line is the dedup key.

```
dedup: codex-01a09b4f-...:receipts-pipeline
session: codex-01a09b4f-... (codex)  cwd: ~/workspace/psagentspace
class: drift-additive | drift-lateral | drift-subtractive | false-authorization | self-block

## His words
- 10:28:27 "Okay turn the production paywall on for 2.1.42."

## What happened
- 10:28:33 assistant: "Step 1 of 4: Recheck the approved build..." (plan grew from 3 to 4 steps)
- 10:29:04 tool: git worktree add ... (new worktree for a flag flip)
- 10:31:40 assistant: "...local activation record... observer expectations... BigQuery telemetry polling"
Provenance: AGENT (skill ceremony read as requirement)
Running since 10:28:33, 4 turns, 6 minutes.

## Why he would be surprised
He asked for one setting to be flipped. The agent built a four-step receipts
pipeline with its own worktree and telemetry polling around it.

## For a self-block only
Authorization on record: 06:23:27 "retarget them to main dispatch to sol agents"
Doctrine cited: psagentspace/AGENTS.md:44
```

Nothing else. No recommendation, no fix, no code opinion.

## Return contract

One line from the watcher to the master:

- `NO_CHANGE cursor=<n>`
- `ALIGNED cursor=<n> <one sentence>`
- `ESCALATE <n> <path> [<path>...] cursor=<n>` then one sentence per packet.

## alerts.jsonl

Written by `notify.py`. One JSON object per line with `ts`, `title`,
`message`, `session`, `dedup_key`, `detail` (packet path), `suppressed`, and
per-channel `results`. The master checks `dedup_key` before notifying and
logs rejected packets with `--suppressed`.

## Alert message shape

Under 200 characters. Session first, then what happened, then what he can
reply with. Examples:

- `codex 01a09b4f (psagentspace): flag flip grew a 4-step receipts pipeline + worktree. Reply "just flip it" to that session.`
- `codex 01a09d33: asking approval to publish after you said "retarget them to main". Reply "go".`
- `3 sessions blocked on Xcode build since 16:20. Host problem: disk/xcode-select. One fix, not three.`
