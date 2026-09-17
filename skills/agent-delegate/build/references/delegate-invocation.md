# Delegate Invocation

Agent-delegate specific invocation: delegation modes, run directories, Codex and Claude command shapes for all modes, parallel delegation groups, monitoring posture, and failure behavior. Model/runtime/effort resolution rules are in references/model-and-invocation.md.

## Required values

Every delegation child needs:

- `mode` - `fresh-one-shot`, `fresh-resumable`, or `resume`
- `runtime` - `claude` or `codex`
- `model` - the runnable CLI model identifier, or the previous session model when a resume intentionally reuses it
- `effort` - the reasoning effort level, or the previous session effort when a resume intentionally reuses it

Resume mode also needs either:

- `session_id` - Claude `session_id` or Codex `thread_id`
- `run_dir` - a previous `agent-delegate` run directory containing `session_id.txt` and `execution.json`

If any value is missing or ambiguous, ask one consolidated question before invoking.

## Delegation mode

- `fresh-one-shot` is the default. It creates a cold child and may use stateless CLI flags.
- `fresh-resumable` creates a cold child that can be resumed later. Use it only when the caller says this worker may need same-session continuation.
- `resume` continues an explicit same-runtime session id or prior run directory. Do not resume `latest` sessions, do not use Claude `--continue`, and do not use Codex `--last`.

Same-runtime is mandatory. Claude sessions resume through Claude with `-r <session_id>`. Codex threads resume through `codex exec resume <thread_id>`.
Parallel delegation supports `fresh-one-shot` and `fresh-resumable`. Keep `resume` on the single-worker path; launching several resumed sessions at once is a different orchestration problem and is not part of this prompt-first skill.

## Run directory

Create one run directory per delegation child:

```bash
DELEGATE_SLUG="<short-slug>"
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$(mktemp -d "/tmp/agent-delegate/${DELEGATE_SLUG}-${RUN_TS}-XXXXXX")"
PROMPT_PATH="$RUN_DIR/prompt.md"
FINAL_PATH="$RUN_DIR/final.txt"
EVENTS_PATH="$RUN_DIR/events.jsonl"
STDERR_PATH="$RUN_DIR/stderr.log"
EXECUTION_PATH="$RUN_DIR/execution.json"
SESSION_PATH="$RUN_DIR/session_id.txt"
RESUME_FROM_PATH="$RUN_DIR/resume_from.txt"
```

Write the prompt to `prompt.md`. Do not pass a long multiline prompt directly on the command line.
`events.jsonl` is the live child stream. `stderr.log` is the diagnostic error stream. `final.txt` is the final assistant text: Codex writes it directly with `-o`; for Claude, copy the `result` text from the final `type=result` event after the process exits.
Write `execution.json` before invocation with at least:

```json
{
  "mode": "fresh-one-shot | fresh-resumable | resume",
  "runtime": "claude | codex",
  "model": "<resolved model or reused-from-session>",
  "effort": "<resolved effort or reused-from-session>",
  "work_root": "<absolute path>",
  "forced_execution_on_resume": false
}
```

For fresh-resumable and resume runs, write the captured or reused session id to `session_id.txt`. For resume runs, write the source run directory or explicit session id to `resume_from.txt`.

## Parallel delegation group

Use the parallel group path only when the user asks for parallel agents or gives multiple delegated tasks for this skill. Parallel workers are still ordinary delegate children; the group only gives the parent a place to organize prompts, streams, finals, execution metadata, and the combined report.
Create one group directory:

```bash
GROUP_SLUG="<short-slug>"
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
GROUP_DIR="$(mktemp -d "/tmp/agent-delegate/parallel-${GROUP_SLUG}-${RUN_TS}-XXXXXX")"
```

For each child, create an ordinary child run directory beneath the group:

```bash
CHILD_SLUG="<child-slug>"
RUN_DIR="$GROUP_DIR/$CHILD_SLUG"
mkdir -p "$RUN_DIR"
PROMPT_PATH="$RUN_DIR/prompt.md"
FINAL_PATH="$RUN_DIR/final.txt"
EVENTS_PATH="$RUN_DIR/events.jsonl"
STDERR_PATH="$RUN_DIR/stderr.log"
EXECUTION_PATH="$RUN_DIR/execution.json"
SESSION_PATH="$RUN_DIR/session_id.txt"
```

Write `execution.json` before each child invocation with the normal fields plus:

```json
{
  "parallel_group_dir": "<absolute group dir>",
  "child_id": "<stable child id>",
  "child_task": "<one-line task>",
  "allowed_write_scope": "<scope from the prompt>"
}
```

Launch each child with the same Codex or Claude command shape below, using that child's paths. Record the shell PID and exit status in the child directory if the host shell makes that convenient, but do not introduce a script, controller, detached monitor, separate worktree, or merge layer.
Do not block launch because siblings might touch nearby files. Brief every child that other workers may be editing the same repo, that unfamiliar changes must not be reverted, and that actual conflicts should be reported with file evidence. After all children finish, inspect repo state and child reports before presenting the combined result.
Wait for all children before reporting. If one child fails or returns malformed output, preserve its run directory and include that failure in the group report; do not discard successful sibling work.

## Codex fresh one-shot

Use this shape for a default stateless Codex delegation:

```bash
codex exec \
  --ephemeral \
  --disable codex_hooks \
  -C "<work_root>" \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --model "<resolved_model>" \
  -c model_reasoning_effort='"<resolved_effort>"' \
  --json \
  -o "$FINAL_PATH" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

`--ephemeral` keeps the child stateless and cold. Use this only for `fresh-one-shot`; ephemeral sessions are not resumable.

## Codex fresh resumable

Use this shape when a Codex worker may need later same-session resume:

```bash
codex exec \
  --disable codex_hooks \
  -C "<work_root>" \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --model "<resolved_model>" \
  -c model_reasoning_effort='"<resolved_effort>"' \
  --json \
  -o "$FINAL_PATH" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Capture the `thread_id` from the first `thread.started` event in `events.jsonl` and write it to `session_id.txt`. If no thread id is captured, write `UNRECOVERABLE` to `session_id.txt`, treat the run as malformed, and preserve the run directory.

## Codex resume

Use this shape to resume an explicit Codex thread:

```bash
codex exec resume "<thread_id>" \
  --disable codex_hooks \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --json \
  -o "$FINAL_PATH" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

`codex exec resume` carries the working directory from the original session. Do not pass `-C` / `--cd` on resume.
Omit `--model` and effort config to reuse the session's execution choice. If the caller explicitly requires a model or effort change on resume, announce that mapping and add both flags.

## Claude fresh

Use this shape for both `fresh-one-shot` and `fresh-resumable` Claude delegations:

```bash
claude -p \
  --output-format stream-json \
  --include-partial-messages \
  --include-hook-events \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model "<resolved_model>" \
  --effort "<resolved_effort>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Run Claude from `work_root`. Do not pass `--no-session-persistence` for fresh-resumable runs.
After Claude exits, read the final `type=result` event from `events.jsonl` and write its `result` text to `final.txt` before applying the status-footer checks. For fresh-resumable runs, also write the final result event's `session_id` to `session_id.txt`. If no result event exists after a zero exit, or a fresh-resumable run has no session id, treat the run as malformed and preserve the run directory.

## Claude resume

Use this shape to resume an explicit Claude session:

```bash
claude -p \
  --output-format stream-json \
  --include-partial-messages \
  --include-hook-events \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model "<resolved_model>" \
  --effort "<resolved_effort>" \
  -r "<session_id>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Run the resume from the same `work_root` used by the original Claude session. Use `-r <session_id>`, never `--continue`, because `--continue` chooses the most recent conversation in the current directory and can collide with other work.
After Claude exits, write the final `result` text to `final.txt`. Write the returned `session_id` to `session_id.txt` when present; otherwise preserve the input session id in `session_id.txt`.

## Monitoring posture

Delegated work is not instant. A normal repo-backed task commonly takes 5+ minutes. Broad edits, verification, `xhigh`, or `max` can reasonably take 20-40 minutes.
Poll on a minutes-scale cadence. Check `events.jsonl`, `stderr.log`, repo state if writes are expected, and process liveness every few minutes; do not poll every few seconds. A missing `final.txt` before the process exits is not a failure when the event stream is still alive. Investigate only after the process exits non-zero, the stream shows an error, or there is no stream activity for a long quiet window.

## Failure behavior

Fail loud and preserve the run directory when:

- the selected CLI is missing
- runtime/model/effort cannot be resolved exactly
- the allowed write scope is missing or unsafe
- resume mode has no explicit session id or prior run directory
- `session_id.txt` is missing, empty, or `UNRECOVERABLE` for a resume
- the caller asks for cross-runtime resume
- the caller asks for Claude `--continue`, Codex `--last`, or `latest` resume selection
- the child exits non-zero
- `final.txt` is empty
- Claude exits without a final `type=result` event
- fresh-resumable Codex does not emit `thread.started`
- the child omits the required status footer

Do not silently fall back from Claude to Codex, Codex to Claude, one model to another model, one effort level to another, foreground to detached execution, or shared-worktree execution to a separate worktree.
