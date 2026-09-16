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
    intent.md          watcher: his words and your decoding, nothing else
    ledger.md          watcher, append-only
    cursor.json        watcher
    events/            pages from session_events.py; keep the last few
    escalations/       watcher, one file per finding
```

## roster.json

```json
{
  "started": "...", "watcher_model": "sonnet", "watcher_effort": "inherits parent",
  "rest_minutes": 10, "max_concurrent": 4,
  "wake": "claude session cron 3-59/10, expires <date>",
  "excluded": ["claude-<this master's session id>"],
  "sessions": {
    "codex-01a0...": {
      "runtime": "codex", "path": "...", "cwd": "...",
      "status": "new | watching | dormant | retired | stopped | automated",
      "last_seen_size": 0, "last_seen_mtime": "...",
      "last_check_started": "...", "last_check_finished": "...",
      "watcher_running": false, "last_verdict": "ALIGNED",
      "misses": [{"at": "...", "shape": "rebuilt instead of reused"}],
      "idle_raised_at": null,
      "rejected": ["<dedup key>: <one-line reason>"]
    }
  }
}
```

`misses` is the master's fleet metric. Dormant: no new bytes for six hours
and the last event is his turn or a normal completion. Retired: absent from
discovery for 48 hours.

## cursor.json

```json
{"runtime": "codex", "path": "...", "cursor": 3871289,
 "last_event_ts": "...", "last_check": "...", "checks": 7}
```

`cursor` is the byte offset returned by `session_events.py`. Never guess it.

## intent.md

His words and your decoding of them. Nothing the agent, its children, or a
reviewer said belongs here. Keep it short enough to re-read every check. It
changes only when he speaks, and most of his messages do not change it.

```
# Intent: <key>
Anchored: <ts>   Last revised: <ts>   Runtime: <runtime>   cwd: <cwd>

## His words (verbatim, with timestamps)
- 11:47:52 "okay see this screenshot? ... make a Poker Skill version ... use our existing components"
- (inherited from <session or doc>: "...")

## What he wants
<plain words: the outcome, how he will judge it>

## Boundaries he stated
- ...

## Authorizations on record
- 11:47:52 build the mock in Figma beside the reference

## Inferred non-goals (inference, confidence)
- no new component library, no redesign of the paygate (high)

## Open ambiguities
- ...

## Corrections he has had to make (each one is a miss)
- 11:57:29 "use our canonical styles and components": rebuilt instead of reused
```

## ledger.md

Append-only. One line per requirement, decision, constraint, or claim as it
enters the work, then one line per check.

```
2026-09-15 11:47:52 USER      "make a Poker Skill version ... use our existing components"
2026-09-15 11:48:24 CLAIM     "I'll build a Poker Skill styled version ... using the existing paygate components"
2026-09-15 11:50:04 WORK      mcp__figma__use_figma: createFrame x2, createRectangle x2, createText (helper); no createInstance  [contradicts CLAIM 11:48:24]
2026-09-15 11:51:03 CLAIM     "uses our existing visual system and components"  [contradicted by WORK 11:50:04]
2026-09-15 11:57:29 MISS      he corrected "rebuilt instead of reused"; WORK 11:50:04 was in my window at 11:52 and I did not escalate
CHECK 2026-09-15 11:52  cursor 9576590  new events 17  verdict ESCALATE  packet escalations/20260915-1152-rebuilt-not-reused.md
```

Tags: `USER` (his words), `WORK` (what a tool call did, from arguments or
inventory), `CLAIM` (the agent's or a child's or a reviewer's statement about
the work), `AGENT` (a decision or artifact the agent introduced: plan item,
goal text, brief clause, heartbeat, workaround), `EXTERNAL` (a reviewer or
panel finding and when the agent adopted it), `SELF-FILE` (the agent citing
a file it wrote as authority), `MISS` (a correction from him you did not
pre-empt, with what you should have seen).

## Escalation packet

`escalations/<YYYYMMDD-HHMM>-<slug>.md`. First line is the dedup key.

```
dedup: codex-01a0a504-...:rebuilt-not-reused
session: codex-01a0a504-... (codex)  cwd: ~/workspace/psagentspace
class: drift-lateral | drift-additive | drift-subtractive | two-of-anything | false-authorization | machine-footprint | self-block

## His words
- 11:47:52 "... use our existing components"

## The work
- 11:50:04 mcp__figma__use_figma: createFrame x2, createRectangle x2, createText x1 (helper for every label); createInstance x0; importComponentByKeyAsync x0

## The claim
- 11:51:03 "The Poker Skill version uses our existing visual system and components."

Running since 11:50:04, 1 turn, 2 minutes.

## Why he would be surprised
He asked for reuse of components he already built. The work is a rebuild from primitives, and the agent's message says the opposite.
```

Nothing else. No recommendation, no fix, no code opinion, no question.

## Return contract

One line from the watcher to the master, then at most two sentences:

- `NO_CHANGE cursor=<n>`
- `ALIGNED cursor=<n>` then the one thing you checked hardest and why it passed
- `MISS cursor=<n> <what he caught that you did not>`
- `ESCALATE <n> <path> [<path>...] cursor=<n>` then one sentence per packet

## alerts.jsonl

Written by `notify.py`. One JSON object per line with `ts`, `title`,
`message`, `session`, `dedup_key`, `detail` (packet path), `suppressed`, and
per-channel `results`.

## Alert message shape

Under 200 characters, a statement, never a question. Session first, then
what happened, then the one-line reply he could send to that session.

- `codex 01a0a504 (paygate mocks): asked to reuse components; the mock was drawn from rectangles and the agent says it reused. Reply there: "use the real components".`
- `4 sessions in 12 min each got your "one priority definition" correction. Fleet-wide: every parent invented its own scale.`
- `codex 01a09d33: asking approval to publish after you said "retarget them to main". Reply "go".`
