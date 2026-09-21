# Runtime Notes

Facts a watcher or master needs about each runtime's store, where Amir's
words live, what is and is not readable, and how each host dispatches and
wakes. Verified 2026-09-15 on Amir's Mac. Stores change; believe the file over
this note when they disagree.

## Codex CLI

- Store: `~/.codex/sessions/YYYY/MM/DD/rollout-*-<thread_id>.jsonl`;
  metadata in `~/.codex/state_5.sqlite` (`threads`, `thread_spawn_edges`);
  goals in `goals_1.sqlite` (current state only, `/goal clear` destroys
  history).
- Amir's typed prompts appear as `event_msg` `item_completed` with
  `item.type = UserMessage`, and again as `response_item` messages with
  `role = user`. The scripts dedup the pair. `response_item` user records
  that start with `# AGENTS.md instructions` or contain
  `<codex_internal_context` are injected instructions, not Amir; the ones
  with `source="goal"` are the armed goal text and are emitted as `GOAL`.
- `turn_context` carries `approval_policy` and `sandbox_policy`. In the
  corpus this was `never` and `danger-full-access` in 3,655 of 3,697
  threads. An approval request under that policy is self-generated.
- Sub-agent payloads (`spawn_agent`, `send_message`, `followup_task`,
  `NEW_TASK`, `FINAL_ANSWER`) are encrypted in the rollout. The brief text
  is unreadable. Read the parent's narration of what it delegated and any
  brief files it wrote to disk. Children inherit the parent's user messages
  verbatim, so a child rollout does show Amir's words.
- Compaction (`compacted` records) retains the opening user turns verbatim
  and re-injects a block telling the agent not to spawn sub-agents unless
  asked. Mid-session corrections drop out of the retained window. This is
  why delegation collapses after many compactions; it is not why scope
  drifts.
- Most rollout files on a busy day are spawned children.
  `discover_sessions.py` excludes them unless `--include-children`.
- Single files reach 1.8 GB. Never read them directly.

## Claude Code

- Stores: `~/.claude/projects/<key>/<session>.jsonl` and, for every AI
  Manager label, `~/.aimgr/claude-homes/<label>/.claude/projects/...`.
  Subagent transcripts sit under `<session>/subagents/agent-*.jsonl`.
- Amir's sharpest corrections are not ordinary user records. They are
  `queue-operation` records with `reason: "absorbed_mid_turn"` and synthetic
  user records reading `[Request interrupted by user for tool use]`. The
  scripts emit these as `USER_QUEUED` and `USER_INTERRUPT`. The tool call the
  interrupt killed is usually the drift artifact.
- `permission-mode` records show `bypassPermissions` when present. Headless
  workers (`claude -p`) record no mode at all; absence means unattended.
- `system` records with `subtype: away_summary` are Claude Code's own
  one-line recap and often state a self-declared block in plain words.
- `AskUserQuestion` and `ExitPlanMode` were never used in the corpus. Halts
  are plain turn-final text.
- Delegated workers whose first message starts "You are an externally
  delegated worker" are excluded by default. Amir never speaks in them;
  drift there is found by comparing the brief to the output, which is a
  different job.
- Amir's voice-to-text produces curly apostrophes (U+2019). Normalize before
  matching his words.
- Thinking blocks are frequently empty. Judge from text and tool inputs.

## Prime Agent

- Store: `~/.prime/agent/sessions/<uuid>.jsonl` for roots. Children live
  under `session-artifacts/<root>/sub-<child>/` with the brief in a per-child
  `rlm-subagent.json` (`prompt`, `spawnCode`, `model`, `status`). The
  root-level `rlm-subagents.jsonl` index is obsolete.
- Child transcripts contain no `role: user` messages. The brief arrives as a
  `custom_message` of type `agent_message` with `id: spawn:<childId>`.
- Three surfaces restate the ask and are readable: `heartbeat_prompt`
  events (self-authored standing orders that re-fire every few minutes),
  `compaction` summaries with a structured `## Goal` block, and child
  briefs. The scripts emit `HEARTBEAT`, `COMPACTION` (goal block only), and
  `AGENT_MSG`. A goal bullet with no user-message ancestor is drift.
- `agent_status.taskState` is always `needs_input` with an empty summary.
  Only run length and cadence carry signal. Idle roots emit it every ~25
  seconds; more than twenty in a row with no message between means parked.
- Automated routines ("AIM routine binding check. Do not use tools.") appear
  as roots. Recognize and skip them; they are not Amir's sessions.
- Session id prefixes collide (five sessions begin `01a0671b`). Use full
  ids and paths.
- Pi (`~/.pi/agent/`) has had no real activity since 2026-08-09.

## Herdr

- MCP tools `list_agents`, `get_agent`, `read_pane` report live pane status
  (idle, working, blocked, done) for panes Herdr detects as agents. On
  2026-09-15 it detected one pane while AI Manager listed five live Claude
  sessions, so it corroborates rather than replaces transcript discovery.
- `read_pane` is the cheapest way to confirm a session is truly idle at a
  prompt versus mid-tool-call when the transcript is ambiguous.

## Discovery sources, in order

1. `discover_sessions.py` over the three stores (default window 6 hours).
2. `aim claude list` for managed Claude sessions and their labels.
3. Herdr `list_agents` for pane status.

## Host dispatch matrix

| Host running the master | Watcher dispatch | Model pin | Wake for the tick |
| --- | --- | --- | --- |
| Claude Code | Agent tool, clean subagent | `model` alias per call (`opus`, `sonnet`); effort cannot be pinned per call and inherits the parent | Session cron on an off-minute (`3-59/10 * * * *`), session-only, expires after 7 days; or a scheduled wakeup |
| Codex | `spawn_agent` with `fork_turns: "none"` | `model` and `reasoning_effort` per spawn; pins can expire when a child is unloaded, so keep checks short | Goal loop or timed follow-up whose turns do bookkeeping only |
| Prime Agent | Native child | `model` and `thinking` per spawn | Heartbeat prompt |

See `../../_shared/native-child-capabilities.md` for the current facts and
sharp edges before promising a pin.

## Script usage

```bash
S=~/.claude/skills/agent-watcher/scripts   # or the installed path on this host
python3 $S/discover_sessions.py --since 6h
python3 $S/session_events.py anchor --path <transcript>
python3 $S/session_events.py work   --path <transcript> [--cursor <n>] [--until HH:MM]
python3 $S/discover_sessions.py --children-of <codex key>
python3 $S/discover_sessions.py --find <session id he named>
python3 $S/session_events.py since  --path <transcript> --cursor <n> --full-args
python3 $S/session_events.py tail   --path <transcript> --tail-events 40
python3 $S/notify.py --message "..." --detail <packet> --session <key> --dedup-key <key>
```

Each prints one header line and bounded rows and writes the full result to
disk. `--help` documents the caps. Slack delivery needs
`AGENT_WATCHER_SLACK_TARGET` in `~/.config/agent-watcher/env` and the
`ops_bot` token file the `slack-post-engineering` skill documents; without
them `notify.py` reports Slack as skipped and still sends the desktop
notification and sound.
