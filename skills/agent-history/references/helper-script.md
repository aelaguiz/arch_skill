# Agent History Helper Script

`scripts/agent_history.py` is a read-only helper for parsing local Codex, Claude
Code, Pi, and Prime Agent history stores. It exists because JSONL and SQLite
extraction is deterministic enough that agents should not reimplement it every
time.

The script is not a user-facing query language. The agent decides what the user
means, runs the helper with the current runtime and scope, inspects the
evidence, and writes the answer.

## Dependency Model

The helper is self-contained Python and uses only the standard library. It has
no runtime package dependencies.

Run it with:

```bash
python3 skills/agent-history/scripts/agent_history.py <command> --runtime <codex|claude|pi|prime>
```

If a future version needs non-stdlib dependencies, it must carry them in a PEP
723 script header and bootstrap through `uv --quiet run --script` so the host
agent does not have to figure out dependencies.

## Commands

- `sessions`: list candidate sessions for a runtime, cwd, and time window.
- `prompts`: extract submitted/user prompts.
- `commands`: extract slash/TUI command evidence.
- `goals`: extract goal evidence.
- `search`: search transcript, prompt, command, and tool text using
  agent-chosen terms or regex.
- `show`: show bounded detail for one result id from a prior run artifact.

## Shared Options

- `--runtime codex|claude|pi|prime`: required for all search commands. Use the
  current runtime by default.
- `--cwd <path>`: default is the process cwd.
- `--scope current-project|all-projects`: default is `current-project`.
- `--since <time>`: default is `24h`; accepts relative durations, ISO dates,
  ISO datetimes, and `today`.
- `--until <time>`: optional end time.
- `--include-sidechains`: include Claude subagent JSONL and Prime `sub-*` child
  transcripts.
- `--limit <n>`: default 20.
- `--max-results <n>`: default 2000. Bounds how many results are retained and
  written to disk; the newest are kept.
- `--page <n>`: default 1.
- `--format summary|jsonl`: default `summary`.
- `--max-preview-chars <n>`: default bounded preview.
- `--output-root <path>`: default `/tmp/agent-history`.
- `--codex-home`, `--claude-home`, `--pi-home`, `--prime-home`: test or
  alternate homes.

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
