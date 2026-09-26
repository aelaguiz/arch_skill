# Runtime Notes

Where each runtime keeps its transcripts, how to go from a Herdr pane to the session and its chain, and what the records look like, so you can read them with your own judgment and ordinary tools. Checked on Amir's machines in September 2026. Stores change; believe the files over this note when they disagree.

## From a Herdr pane to its session

1. `herdr session list --json` lists the Herdr sessions; for each running one, `herdr --session <s> workspace list` and `herdr --session <s> pane list --workspace <w>` give each pane's id, cwd and title. Herdr rarely detects the agent in a pane itself, so the pane is the place and the transcript is the truth. Amir names work by its Herdr space; use those names when you talk to him.
2. **Claude Code:** `aim claude list --json` lists managed sessions with account, thread name, thread id and cwd. The transcript is `~/.aimgr/claude-homes/<account>/.claude/projects/<cwd with / replaced by ->/<thread id>.jsonl`. Match a pane by cwd and thread name (the pane title usually carries it) and by the transcript being written while the pane is busy.
3. **Codex:** `~/.codex/state_5.sqlite`, table `threads` (id, cwd, title, updated_at, rollout_path; `agent_role` or `agent_nickname` set on children), opened read-only; rollouts under `~/.codex/sessions/YYYY/MM/DD/`. Match by cwd and recency; the pane's footer shows the thread name.
4. **A pane whose prompt shows `amir-server`** runs over ssh: its transcripts are on that host (`ssh home`), under `/home/aelaguiz/...` with the same layouts. Read them there and bring back only what you need.
5. When the mapping is ambiguous, read the pane's scrollback: an exit prints `claude --resume <id>`, and an account switch prints "Switching session from <account> to <account>".

## Following the chain

A piece of work outlives its sessions. Before building a model, walk back to the first session:

- **Restarts and account switches** create a new session id, often in another account's home. The pane scrollback shows the old and new ids; `aim claude list` shows the new one; the new transcript may begin by replaying the old one's lines or with a continuation summary.
- **Forks** carry the same thread name across several ids and accounts. Take all of them, oldest first, and skip exact replays.
- **A continuation summary** ("This session is being continued from a previous conversation…") is the agent's summary, not Amir's words; his words are in the earlier transcript.
- **"Ramp up on session X" or "read this session"** in his words pulls session X into the chain.

## Reading transcripts

Transcripts are JSONL, one record per line, and reach hundreds of megabytes (Codex rollouts, gigabytes). Never load or print a whole file, and never search across `~`, `~/.aimgr/claude-homes`, `~/.codex/sessions` or `/`: that has pinned Amir's machine before. Pick the file, then stream it line by line with a few lines of Python, keeping only the records you need. Amir's own words are small (about 3,000 tokens in a 78 MB transcript), so reading all of them is cheap once you filter. For current activity, read the last few megabytes (`tail -c`) and parse the complete lines. Every record has a `timestamp` (UTC); remember the time of the last record you read, and start there next time. For a replay or dry run "as of" a past moment, stop at the first record after it.

**Claude Code records:**

- Amir's typed message: `type` `user` with `origin.kind` `human`; the text is `message.content` (a string, or blocks of `type` `text`).
- A message he typed while the agent was busy: `type` `queue-operation` with `operation` `enqueue` (text in `content`), and `type` `attachment` whose `attachment.type` is `queued_command` (text in `attachment.prompt`). The same text can appear in both and again later as a user record; count it once. About one in six of his corrections arrives this way.
- Not his, though shaped like his: records with `isMeta` true (scheduled and injected prompts), and text that begins `<task-notification>`, `<agent-message`, `<system-reminder>`, `<command-name>`, "Base directory for this skill:", or "This session is being continued from a previous conversation".
- The agent: `type` `assistant`, content blocks of `text` and `tool_use` (the tool's name and full input: the file it wrote, the command it ran, the brief it gave a sub-agent). A blocking question is a `tool_use` named `AskUserQuestion`. Plain turn-final text is the more common way a Claude agent stops to ask.
- Compaction: `type` `system` with `subtype` `compact_boundary`. Sub-agent transcripts sit under `<session>/subagents/`; Amir never speaks there.
- His voice-to-text uses curly apostrophes; normalize before comparing text.

**Codex records** (each line has `type` and a `payload`):

- Amir's prompt: `event_msg` whose item is a `UserMessage`, and again as `response_item` `message` with `role` `user`; count it once. User-role text that starts `# AGENTS.md instructions` or contains `<codex_internal_context` is injected, not his.
- The agent: `response_item` `message` with `role` `assistant`, and `function_call` or `custom_tool_call` records with the tool name and arguments. `request_user_input_async` shows "? 1 question" in the pane and the agent usually keeps working; `request_user_input` waits.
- Sub-agent payloads are encrypted; read the parent's narration and any brief files it wrote. Children inherit his messages verbatim.
- `compacted` records keep his opening turns verbatim; mid-session corrections can drop out of the agent's view, which is when Codex agents ask him things he already answered.

**Prime Agent:** roots at `~/.prime/agent/sessions/<uuid>.jsonl`, children under `session-artifacts/<root>/sub-<child>/`. Heartbeat prompts and compaction goal blocks restate the ask and are worth reading; a goal line with no ancestor in his words is drift. Automated routines appear as roots; skip them.

## What the session produced

The transcript tells you where to look; the work itself is the evidence. In the session's working directory or worktree: `git log`, `git diff`, and the files it wrote (named in its tool calls). On GitHub: `gh pr view` and `gh pr diff` for its PRs, `gh issue view` for issues it wrote. For sheets and docs it edited, read the cells or sections it touched.

## Waking up and notifying

In Claude Code, pace your own wake-ups with the session's loop or scheduled wake-up. In Codex, use a goal loop or a timed follow-up. Readers are native children: in Claude Code they inherit your effort, which is the profile Amir chose for the watcher. For a desktop notification when something is badly wrong, use the host's own notification tool, or `osascript -e 'display notification "<text>" with title "Watcher" sound name "Glass"'` on the Mac.
