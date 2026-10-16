# Agent History Helper Script

`scripts/agent_history.py` is a read-only helper for parsing local Codex, Claude
Code, Pi, Prime Agent, and Antigravity CLI (agy) history stores. It exists because JSONL and SQLite
extraction is deterministic enough that agents should not reimplement it every
time.

The script is not a user-facing query language. The agent decides what the user
means, runs the helper with the current runtime and scope, inspects the
evidence, and writes the answer.

## Dependency Model

The helper is self-contained Python and uses only the standard library. It has
no runtime package dependencies.

Run it from the skill's own folder:

```bash
python3 <this skill>/scripts/agent_history.py read <session id>
python3 <this skill>/scripts/agent_history.py <command> --runtime <codex|claude|pi|prime|agy>
```

If a future version needs non-stdlib dependencies, it must carry them in a PEP
723 script header and bootstrap through `uv --quiet run --script` so the host
agent does not have to figure out dependencies.

## Commands

- `read <session id>`: open one session by its id, or the first 8 or more
  characters of it, and show what happened in it in order. See below.
- `sessions`: list candidate sessions for a runtime, cwd, and time window.
- `prompts`: extract submitted/user prompts.
- `commands`: extract slash/TUI command evidence.
- `goals`: extract goal evidence.
- `search`: search transcript, prompt, command, and tool text using
  agent-chosen terms or regex.
- `show`: show bounded detail for one result id from a prior run artifact.

## `read`

```text
OK agent-history read: <N> entries[ after <time>]; showing the last <M>; run=<run_dir>
session: <runtime> <full id>
title: <title or ->
project: <cwd>
activity: <first time> to <last time>
transcript: <path of the copy that was read>
older copies: <other paths>            (only when copies exist)
continues: <earlier id> <path>          (when the session continues another)
  which continues: <id> <path>          (back to the first session)
memory: <memory folders>                (Claude: those with anything in them)
instructions: <AGENTS.md / CLAUDE.md files for this project and user>
everything the user wrote, from the first session: python3 <script> read <id> --yours
readable copy: <run_dir>/transcript.md

<time> | <user|assistant|tool call|tool result|compaction|context> | <preview>
...

earlier entries: <run_dir>/transcript.md
next time: python3 <script> read <full id> --after <last time>
```

- The id is matched against transcript file and folder names, so the lookup
  does not read any transcript but the one it opens. With no `--runtime` it
  looks in every runtime; a prefix that matches several sessions prints them
  and exits 2; no match prints `NO_MATCH` with what was searched and exits 1.
- When AI Manager left copies of one session in several account folders, the
  most recently written copy is read and the others are listed.
- `context` entries are text the runtime injected rather than anyone typing
  it: Codex environment and instruction blocks, Claude meta messages. Claude
  `<system-reminder>` blocks are removed from user turns. Reasoning and
  thinking blocks are left out.
- `continues:` comes from the summary a continued Claude session opens with,
  which names the transcript it came from ("read the full transcript at:").
  Each earlier session is opened the same way, nearest first. One that is no
  longer on this machine prints `(not on this machine: <path>)`.
- `--yours` prints only what the user typed, in this session and every
  earlier one it continues, oldest first, each line tagged with its session.
  Tool output, compaction summaries, notifications and injected context are
  left out, and a slash command prints as `/name args`. It prints every
  message (`--last` still limits it), with up to 2,000 characters each, and
  writes them in full to `yours.md`. Its `next time:` line keeps `--yours`.
- `memory:` lists Claude memory folders with anything in them, for the
  project folder and each folder above it, since Claude keys memory by the
  repo root. `instructions:` lists `AGENTS.md` and `CLAUDE.md` in those
  folders, plus the user's Claude or Codex instructions file.
- `--after <time>` keeps entries after that time, compared to the second.
  `--last <n>` sets how many entries print (default 40; `0` prints all).
  `--max-preview-chars` sets each printed line's length (default 300).
- The run folder holds `transcript.md` (every entry, or every entry after
  `--after`, with long entries cut: tool calls and results at 1,500
  characters, replies at 4,000, prompts at 6,000, compaction summaries at
  8,000), `entries.jsonl`, and `errors.jsonl`.
- `--claude-home`, `--codex-home`, `--agy-home`, `--prime-home`, `--pi-home`,
  and `--output-root` work as they do for the search commands.

## Homes

Claude and Codex searches, and `read`, use every home they can find unless one
is passed explicitly:

- Claude: `$CLAUDE_CONFIG_DIR`, `~/.claude`, and every
  `~/.aimgr/claude-homes/<account>/.claude` (AI Manager keeps one per
  account).
- Codex: `$CODEX_HOME`, `~/.codex`, and `~/.aimgr/codex-cli`. Two homes whose
  `sessions` folder is the same place count once.

`--claude-home <path>` or `--codex-home <path>` narrows the search to that one
home. Exact duplicate results from copied transcripts are shown once. A
transcript last written before `--since` is skipped without being read.

## Shared Options

- `--runtime codex|claude|pi|prime|agy`: required for all search commands. Use the
  current runtime by default. Optional for `read`.
- `--cwd <path>`: default is the process cwd.
- `--scope current-project|all-projects`: default is `current-project`.
- `--since <time>`: default is `24h`; accepts relative durations, ISO dates,
  ISO datetimes, and `today`.
- `--until <time>`: optional end time.
- `--include-sidechains`: include Claude subagent JSONL, Prime `sub-*` child
  transcripts, and agy subagent conversations.
- `--limit <n>`: default 20.
- `--max-results <n>`: default 2000. Bounds how many results are retained and
  written to disk; the newest are kept.
- `--page <n>`: default 1.
- `--format summary|jsonl`: default `summary`.
- `--max-preview-chars <n>`: default bounded preview.
- `--output-root <path>`: default `/tmp/agent-history`.
- `--codex-home`, `--claude-home`: read only that one home instead of every
  home (see Homes).
- `--pi-home`, `--prime-home`, `--agy-home` (default
  `~/.gemini/antigravity-cli`): alternate homes.

`search` also accepts positional query terms and `--regex`.

## Runtime Notes

- `goals` has no store to read in `pi` and `prime`. The helper returns `/goal`
  command text when it exists and records the missing store in `sources.jsonl`.
- `sessions` for `pi` and `prime` reports session name, message count, model,
  AI Manager account label, compaction count, and the parent id for a child.
- Prime child transcripts are labelled from `rlm-subagents.jsonl`, so a child
  appears under its dispatch name rather than its directory id.
- Result kinds for these runtimes are `session`, `prompt`, `command`, `goal`,
  `message`, `agent_message`, `custom`, `status`, and `compaction`.
- `child_usage_attributed` records are never returned; they are accounting.
- `agy` reads each conversation's transcript and takes its title, project
  folder, and parent conversation from `conversation_summaries.db`. Prompts
  have agy's `<USER_REQUEST>` wrapper removed. `search` also matches Argon's
  replies (`message`), its reasoning (`thinking`), tool calls including
  subagent briefs (`tool_call`), tool output (`tool_output`), and system
  messages (`system`). A subagent result names its parent conversation in
  `thread_id` and `context`.
- When the result cap bites, the summary line says `capped at <n>` and
  `sources.jsonl` records how many older sessions went unscanned.

## Output Contract

Default stdout is intentionally small:

```text
OK agent-history <command>: <N> matches; showing <M>; run=<run_dir>
<compact rows>
show: python3 <script> show --run <run_dir> --id <id> --context 3
next page: python3 <script> <command> ... --page <n>
```

No-match output:

```text
NO_MATCH agent-history <command>: searched <sources>; run=<run_dir>
```

Failure output:

```text
ERROR agent-history <command>: <reason>
```

Large data goes to disk, not stdout.

## Artifact Layout

Each run writes:

- `manifest.json`: runtime, command, cwd, scope, time range, source counts, and
  errors count.
- `results.jsonl`: one result per line.
- `sources.jsonl`: stores inspected.
- `errors.jsonl`: recoverable parse/read errors.

Result records include:

- `id`
- `runtime`
- `kind`
- `source`
- `confidence`
- `timestamp`
- `session_id` or `thread_id`
- `cwd`
- `path`
- `line` when available
- `role` when available
- `preview`
- `text_capped`
- `context`

## Script Discipline

- Default output must be bounded.
- Raw transcript text is drill-down, not default output.
- Bad JSONL lines should become recoverable errors, not aborts.
- Missing optional stores should be reported as absent sources, not fatal
  errors.
- The helper should expose evidence; the agent owns interpretation.
