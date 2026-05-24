# Model And Invocation

Use this reference to resolve what the user meant by "Claude", "Codex",
"opus high", "gpt 5.5 xhigh", "GBT55XI", or similar phrasing, and to run the
selected fresh subprocess or explicit parallel group of fresh subprocesses.
Fresh consult is review/second-opinion work, so it uses Codex for GPT/GBT and
Claude Code for Opus. It does not run Cursor Agent consults.

## Required Values

Every consult child needs three execution values:

- `runtime` - `claude` or `codex`
- `model` - the runnable CLI model identifier
- `effort` - the reasoning effort level

If any value is missing or ambiguous, ask one consolidated question before
invoking:

```text
I need the fresh consult runtime, model, and effort before invoking an external
model. The consult runs as a clean subprocess and can spend real model budget.
What should I use?
```

Add only the missing facts to the question when some values are already known.

## Runtime Inference

Infer runtime only when the user's wording makes it unambiguous:

- `codex`, `openai`, `gpt`, `gbt`, `gpt-5.5`, `GBT55XI`,
  `gpt 5.5 high`, or `gpt-5.3-codex` implies
  `runtime=codex`.
- `claude opus` or `opus` implies `runtime=claude`.
- `sonnet` and `haiku` are not supported by this repo's subprocess doctrine;
  ask for Opus instead of silently running them.
- `agent`, `cursor`, `cursor agent`, or `cursor-agent` is not a fresh-consult
  runtime. If a phrase mixes Cursor Agent with GPT/GBT or Claude, fail loud:
  Codex runs GPT/GBT, Claude Code runs Opus, and Cursor Agent runs only
  Composer implementation workers.
- If the user names only an effort level, such as "xhigh", ask for runtime and
  model.
- If the user says only "run a fresh consult" or "get a second opinion", ask
  for runtime, model, and effort.

Do not choose a favorite default. The selected model changes both cost and
quality, so the user supplies it.

## Model Phrase Resolution

Treat model text as intent, not a loose alias:

- Preserve model family and numeric version exactly. `gpt 5.5` may normalize to
  `gpt-5.5`; it must not become `gpt-5.4`. `opus 4.7` may normalize to
  `claude-opus-4-7`; it must not become another Opus version.
- If the user says `gpt 5.4` or a `gpt-5.4` variant while choosing a model,
  pause before execution and ask whether they meant `gpt-5.5` or explicitly
  want `gpt-5.4`. This is an intent check, not an alias rule: do not rewrite
  the version yourself.
- For Codex, inspect `codex debug models` when needed and choose an available
  identifier with the same family and exact version. If no exact match exists
  or multiple matches are plausible, ask for the runnable model id.
- For Claude, only Opus is supported. When the runtime is Claude and the user
  names family plus version, prefer `claude-opus-<version-with-hyphens>`, for
  example `claude-opus-4-7`. If the user names Sonnet or Haiku, fail loud and
  ask for an Opus choice.
- Cursor Agent is not a fresh-consult model host. Do not use Cursor model
  discovery for consult routing, and do not pass GPT/GBT or Claude model ids
  to Cursor Agent.
- Do not run paid trial prompts to discover whether a Claude model exists. Use
  the CLI help/config surface when available; otherwise ask.

Always announce the raw-to-resolved mapping before execution:

```text
Claude Opus 4.7 xhigh -> runtime=claude, model=claude-opus-4-7, effort=xhigh
```

For deterministic script plumbing that needs the same rules, use
`skills/_shared/model_resolution.py` instead of creating a local model alias
table. The helper exists to keep fresh-consult, Stepwise-style orchestrators,
and arch-epic automatic harnesses aligned on exact-version preservation and
fail-loud behavior.

## Effort Resolution

- Claude accepts `low`, `medium`, `high`, `xhigh`, and `max` via `--effort`.
- Codex effort is passed as `-c model_reasoning_effort='"<level>"'`.
- For Codex, confirm the selected model supports the requested effort when
  `codex debug models` is needed for model resolution.
- If the effort is missing or the selected model does not support it, ask.

## Run Directory

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

Write the prompt to `prompt.md`. Do not pass a long multiline prompt directly
on the command line.

`events.jsonl` is the live child stream. `stderr.log` is the diagnostic error
stream. `final.txt` is the final assistant text: Codex writes it directly with
`-o`; for Claude, copy the `result` text from the final `type=result` event
after the process exits.

## Parallel Consult Group

Use the parallel group path only when the user asks for parallel consults or
gives multiple consult questions for this skill. Parallel consults are still
ordinary fresh consult children; the group only gives the parent a place to
organize prompts, streams, finals, and the combined report.

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

Launch each child with the same Codex or Claude command shape below, using
that child's paths. Record the shell PID and exit status in the child directory
if the host shell makes that convenient, but do not introduce a script,
controller, detached monitor, or state machine.

Default to one shared runtime/model/effort for all children. If the user clearly
assigns different execution choices to different children, apply those choices
exactly and announce the mapping before launch. If any child lacks a consult
question, work root, runtime, model, or effort, ask one consolidated question
before launching the group.

Wait for all children before reporting. If one child fails or returns malformed
output, preserve its run directory and include that failure in the group report;
do not discard the successful sibling consults.

## Codex Command

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

Flag meanings:

- `--ephemeral` keeps the child stateless and cold.
- `--disable codex_hooks` prevents hook recursion.
- `-C <work_root>` pins the filesystem context.
- `--dangerously-bypass-approvals-and-sandbox` gives the child realistic local
  access. Use only in trusted local environments.
- `--skip-git-repo-check` allows doc or artifact consults outside a git root.
- `--json` streams Codex event JSONL to `events.jsonl` while the child works.
- `-o "$FINAL_PATH"` captures the final assistant message.

## Claude Command

Use this shape for a Claude consult:

```bash
claude -p \
  --output-format stream-json \
  --verbose \
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

Flag meanings:

- `-p` runs non-interactively and exits.
- `--output-format stream-json` emits live JSONL events to `events.jsonl`.
- `--verbose` is required by the Claude CLI when `stream-json` output is used.
- `--include-partial-messages` and `--include-hook-events` preserve progress
  and tool/hook activity for long consults.
- `--dangerously-skip-permissions` gives the child realistic local access. Use
  only in trusted local environments.
- `--settings '{"disableAllHooks":true}'` prevents hook recursion.
- `--model` and `--effort` pin the execution choice.

After Claude exits, read the final `type=result` event from `events.jsonl` and
write its `result` text to `final.txt` before applying the verdict-footer
checks. If no result event exists after a zero exit, treat the run as malformed
and preserve the run directory.

## Monitoring Posture

Consults are not instant. A normal repo-backed consult commonly takes 5+
minutes. Broad artifact reads, `xhigh`, or `max` can reasonably take 20-40
minutes.

Poll on a minutes-scale cadence. Check `events.jsonl`, `stderr.log`, and
process liveness every few minutes; do not poll every few seconds. A missing
`final.txt` before the process exits is not a failure when the event stream is
still alive. Investigate only after the process exits non-zero, the stream
shows an error, or there is no stream activity for a long quiet window.

Do not use Claude `-r` or Codex `exec resume`; a consult is a cold read, not a
resumed conversation. Do not use Cursor Agent for fresh consults.

## Failure Behavior

Fail loud and preserve the run directory when:

- the selected CLI is missing
- runtime/model/effort cannot be resolved exactly
- the child exits non-zero
- `final.txt` is empty
- Claude exits without a final `type=result` event
- the child omits the required verdict footer

Do not silently fall back between Claude and Codex, one model to another model,
or one effort level to another.
