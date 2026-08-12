# Agent History Retrieval Playbook

Use this reference to turn casual user asks into grounded local history
searches. The goal is not to classify the user into a fixed query type. The
goal is to understand what evidence would answer the question.

## Defaults

- Runtime: current agent runtime.
- Project: current working directory unless the user names another project.
- Time: last 24 hours unless the user names a range.
- "Today": local calendar day.
- Output: concise evidence summary with handles and confidence notes.

Do not ask the user to restate these defaults. Apply them and mention them in
the answer.

## Intent Reading

Read the user's language for the evidence they want:

- "What prompt did I run here?" usually needs submitted prompt history plus
  transcript confirmation in the current project.
- "What goal commands did I run today?" needs current-runtime goal or command
  evidence, with storage-limit warnings where literal command text is not
  durable.
- "Where did I correct the agent?" needs user-authored turns plus surrounding
  assistant context.
- "Where was I struggling?" needs broader evidence: repeated corrections,
  clarifications, restarts, undo/redo language, frustration, failed tool loops,
  or mismatched assistant behavior.
- "What happened in this repo?" needs a cwd-scoped session timeline.

These are examples, not a routing table. Pick search terms and sources from the
actual wording, inspect context, and revise if the first pass is too narrow.

## Evidence Order

1. Start with cheap metadata:
   - Codex `state_5.sqlite.threads`
   - Claude project JSONL `cwd`, `sessionId`, title, and timestamp records
   - Pi/Prime session header lines (`type: session`) for id, cwd, and start time
   - global prompt recall files for prompt/command questions
2. Move to transcript records:
   - Codex rollout `event_msg.UserMessage` and `response_item.message`
   - Claude `user` and `assistant` records and content blocks
   - Pi/Prime `message` events, then `custom_message` for slash commands and
     agent-to-agent relay
3. Use adjacent stores only when they answer the question:
   - paste cache for pasted prompt bodies
   - file history for file snapshots
   - shell snapshots for environment context
   - tasks/plans/memories for derived state
4. Use logs last unless the user is asking about TUI behavior, errors, or
   command evidence that is not durably stored elsewhere.

## Helper Use

Use `scripts/agent_history.py` before writing one-off parsing commands.

Typical flow:

```bash
python3 skills/agent-history/scripts/agent_history.py prompts --runtime codex
python3 skills/agent-history/scripts/agent_history.py goals --runtime codex --since today
python3 skills/agent-history/scripts/agent_history.py commands --runtime claude --since today
python3 skills/agent-history/scripts/agent_history.py search --runtime claude struggling correction wrong instead
python3 skills/agent-history/scripts/agent_history.py sessions --runtime prime --since today
python3 skills/agent-history/scripts/agent_history.py search --runtime prime --include-sidechains worktree
python3 skills/agent-history/scripts/agent_history.py prompts --runtime pi --scope all-projects --since 30d
python3 skills/agent-history/scripts/agent_history.py show --run /tmp/agent-history/<run> --id <id> --context 3
```

Replace `--runtime` with the current runtime. Add `--scope all-projects` only
when the user asks beyond the current project.

## Common Searches

### Prompt Recall

- Codex: search `history.jsonl`, `threads.first_user_message`, and rollout user
  messages.
- Claude: search `history.jsonl.display`, project JSONL user messages, and
  paste-cache references.
- Confirm cwd/project before answering "here".

### Goal And Slash Commands

- Codex `/goal`: use `thread_goals` for current durable goal state and rollout
  tool calls named `create_goal` or `update_goal` for agent-set goals.
- Codex literal TUI slash text is often not durable; logs are best-effort.
- Claude slash commands: use `history.jsonl.display` and
  `queue-operation.content`.
- Claude custom command definitions under `commands/prompts` explain command
  meaning but are not history.
- Pi/Prime: `custom_message.session_slash_command` holds the literal command in
  `details.command.text`. There is no goal store, so a `/goal` line is command
  evidence and nothing durable survives after it.

### Prime Child Agents

- `rlm-subagents.jsonl` names each child, its dispatch prompt, and its
  transcript file. Read it before opening child transcripts.
- Pass `--include-sidechains` to search child work. Children usually run in
  their own worktrees, so their cwd differs from the parent's.
- `custom_message.agent_message` is what the child actually reported back to the
  parent; `rlm_child_terminal_notice` records a child that ended without
  replying.

### Corrections And Struggle

Start with user-authored text. Search the user's own words first, then expand
with nearby concepts only if needed. Useful families include:

- direct negation: "no", "wrong", "not that", "actually"
- instruction repair: "I meant", "instead", "read the instructions",
  "follow the"
- process correction: "stop", "undo", "revert", "try again", "you missed"
- frustration: user-provided wording, profanity, or repeated re-explanation

Do not treat this list as complete. The right search terms come from the user's
ask and the local transcript language. Always inspect surrounding turns before
calling something a correction.

## Answer Shape

Good answer:

- starts with the finding or no-match result
- states assumed runtime/project/time scope
- groups related hits instead of listing every row
- includes source path, session/thread id, timestamp, and confidence
- names storage limits plainly

Weak answer:

- dumps raw JSON or long transcript text
- hides that a result is inferred from state rather than exact command text
- searches all runtimes when the user asked from one runtime
- turns "struggling" into one brittle keyword list
- says "not found" without saying what was searched

## Stop Rule

Stop once the answer is supported enough for the user's question and the main
uncertainty is explicit. Keep searching only when a likely source remains
unsearched and could materially change the answer.
