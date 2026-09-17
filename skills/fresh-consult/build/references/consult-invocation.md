# Consult Invocation

Fresh-consult specific invocation: run directories, Codex and Claude command shapes, parallel consult groups, monitoring posture, and failure behavior. Model/runtime/effort resolution rules are in references/model-and-invocation.md.

## Required values

Every consult child needs three execution values:

- `runtime` - `claude` or `codex`
- `model` - the runnable CLI model identifier
- `effort` - the reasoning effort level

If any value is missing or ambiguous, ask one consolidated question before invoking.

## Run directory

Create one run directory per consult child:

```bash
CONSULT_SLUG="<short-slug>"
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$(mktemp -d "/tmp/fresh-consult/${CONSULT_SLUG}-${RUN_TS}-XXXXXX")"
PROMPT_PATH="$RUN_DIR/prompt.md"
FINAL_PATH="$RUN_DIR/final.txt"
EVENTS_PATH="$RUN_DIR/events.jsonl"
STDERR_PATH="$RUN_DIR/stderr.log"
```

Write the prompt to `prompt.md`. Do not pass a long multiline prompt directly on the command line.
`events.jsonl` is the live child stream. `stderr.log` is the diagnostic error stream. `final.txt` is the final assistant text: Codex writes it directly with `-o`; for Claude, copy the `result` text from the final `type=result` event after the process exits.

## Parallel consult group

Use the parallel group path only when the user asks for parallel consults or gives multiple consult questions for this skill. Parallel consults are still ordinary fresh consult children; the group only gives the parent a place to organize prompts, streams, finals, and the combined report.
Create one group directory:

```bash
GROUP_SLUG="<short-slug>"
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
GROUP_DIR="$(mktemp -d "/tmp/fresh-consult/parallel-${GROUP_SLUG}-${RUN_TS}-XXXXXX")"
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
```

Launch each child with the same Codex or Claude command shape below, using that child's paths. Record the shell PID and exit status in the child directory if the host shell makes that convenient, but do not introduce a script, controller, detached monitor, or state machine.
Default to one shared runtime/model/effort for all children. If the user clearly assigns different execution choices to different children, apply those choices exactly and announce the mapping before launch. If any child lacks a consult question, work root, runtime, model, or effort, ask one consolidated question before launching the group.
Wait for all children before reporting. If one child fails or returns malformed output, preserve its run directory and include that failure in the group report; do not discard the successful sibling consults.

## Codex command

Use this shape for a Codex consult:

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

- `--ephemeral` keeps the child stateless and cold.
- `--disable codex_hooks` prevents hook recursion.
- `-C <work_root>` pins the filesystem context.
- `--dangerously-bypass-approvals-and-sandbox` gives the child realistic local access. Use only in trusted local environments.
- `--skip-git-repo-check` allows doc or artifact consults outside a git root.
- `--json` streams Codex event JSONL to `events.jsonl` while the child works.
- `-o "$FINAL_PATH"` captures the final assistant message.

## Claude command

Use this shape for a Claude consult:

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

- `-p` runs non-interactively and exits.
- `--output-format stream-json` emits live JSONL events to `events.jsonl`.
- `--include-partial-messages` and `--include-hook-events` preserve progress and tool/hook activity for long consults.
- `--dangerously-skip-permissions` gives the child realistic local access. Use only in trusted local environments.
- `--settings '{"disableAllHooks":true}'` prevents hook recursion.
- `--model` and `--effort` pin the execution choice.

After Claude exits, read the final `type=result` event from `events.jsonl` and write its `result` text to `final.txt` before applying the verdict-footer checks. If no result event exists after a zero exit, treat the run as malformed and preserve the run directory.

## Monitoring posture

Consults are not instant. A normal repo-backed consult commonly takes 5+ minutes. Broad artifact reads, `xhigh`, or `max` can reasonably take 20-40 minutes.
Poll on a minutes-scale cadence. Check `events.jsonl`, `stderr.log`, and process liveness every few minutes; do not poll every few seconds. A missing `final.txt` before the process exits is not a failure when the event stream is still alive. Investigate only after the process exits non-zero, the stream shows an error, or there is no stream activity for a long quiet window.
Do not use `-r`, `--resume`, `--continue`, or Codex `exec resume`; a consult is a cold read, not a resumed conversation.

## Failure behavior

Fail loud and preserve the run directory when:

- the selected CLI is missing
- runtime/model/effort cannot be resolved exactly
- the child exits non-zero
- `final.txt` is empty
- Claude exits without a final `type=result` event
- the child omits the required verdict footer

Do not silently fall back from Claude to Codex, Codex to Claude, one model to another model, or one effort level to another.
