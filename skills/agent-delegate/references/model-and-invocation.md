# Model And Invocation

Use this reference to resolve what the user meant by "Claude", "Codex",
"Cursor Agent", "Grok", "fable 5 high", "opus high", "gpt 5.5 xhigh",
"composer-2.5-fast", "grok-build", or similar phrasing, and to run the
selected worker subprocess or explicit parallel group of worker subprocesses.
Fresh one-shot is the default. Same-session resume is allowed only when the
caller explicitly requires continuity for one worker. Provider routing is
fixed: Codex runs GPT/GBT/OpenAI models, Claude Code runs supported Claude
models, Cursor Agent runs Composer 2.5 Fast, and Grok CLI runs Grok models.

## Required Values

Every delegation child needs:

- `mode` - `fresh-one-shot`, `fresh-resumable`, or `resume`
- `runtime` - `claude`, `codex`, `agent`, or `grok`
- `model` - the runnable CLI model identifier, or the previous session model
  when a resume intentionally reuses it
- `effort` - the reasoning effort level, or the previous session effort when a
  resume intentionally reuses it

Resume mode also needs either:

- `session_id` - Claude `session_id`, Codex `thread_id`, Cursor Agent
  `session_id`, or Grok `sessionId`
- `run_dir` - a previous `agent-delegate` run directory containing
  `session_id.txt` and `execution.json`

If any value is missing or ambiguous, ask one consolidated question before
invoking:

```text
I need the delegate runtime, model, effort, and resume handle before invoking
an external agent. The delegate runs as a foreground subprocess, can edit the
shared worktree, and can spend real model budget. What should I use?
```

Add only the missing facts to the question when some values are already known.

Parallel groups use the same required values for each child. Default to one
shared runtime/model/effort for all children. If the user clearly assigns
different execution choices to different children, apply those choices exactly
and announce the mapping before launch.

## Delegation Mode

- `fresh-one-shot` is the default. It creates a cold child and may use stateless
  CLI flags.
- `fresh-resumable` creates a cold child that can be resumed later. Use it only
  when the caller says this worker may need same-session continuation.
- `resume` continues an explicit same-runtime session id or prior run
  directory. Do not resume "latest" sessions, do not use Claude `--continue`,
  and do not use Codex `--last`.

Same-runtime is mandatory. Claude sessions resume through Claude with
`-r <session_id>`. Codex threads resume through `codex exec resume
<thread_id>`. Cursor Agent sessions resume through `agent -p --resume
<session_id>`. Grok sessions resume through `grok --resume <session_id>`.

Parallel delegation supports `fresh-one-shot` and `fresh-resumable`. Keep
`resume` on the single-worker path; launching several resumed sessions at once
is a different orchestration problem and is not part of this prompt-first
skill.

## Runtime Inference

Infer runtime only when the user's wording makes it unambiguous:

- `codex`, `openai`, `gpt`, `gbt`, `gpt-5.5`, `GBT55XI`,
  `gpt 5.5 high`, or `gpt-5.3-codex` implies
  `runtime=codex`.
- `claude fable`, `fable`, `claude opus`, or `opus` implies
  `runtime=claude`.
- `sonnet` and `haiku` are not supported by this repo's subprocess doctrine;
  ask for a supported Claude choice instead of silently running them.
- `agent`, `cursor`, `cursor agent`, or `cursor-agent` implies
  `runtime=agent` only for Composer. Cursor Agent always resolves to
  `composer-2.5-fast`.
- `grok`, `grok build`, `grok-build`, `grok composer`, or
  `grok-composer-2.5-fast` implies `runtime=grok`.
- Bare `composer`, `composer 2.5`, or bare `2.5` is ambiguous unless the user
  explicitly names Cursor Agent or Grok in the same execution choice.
- If a phrase mixes Cursor Agent with GPT/GBT or Claude, fail loud instead of
  choosing a side. Never run GPT/GBT or Claude models through Cursor Agent.
- If a phrase mixes Grok with GPT/GBT, Claude, or Cursor Agent, fail loud
  instead of choosing a side.
- If the user names only an effort level, such as "xhigh", ask for runtime and
  model.
- If the user says only "delegate this" or "have another agent do this", ask
  for runtime, model, and effort.

Do not choose a favorite default. The selected model changes both cost and
quality, so the user supplies it.

## Model Phrase Resolution

Treat model text as intent, not a loose alias:

- Preserve model family and numeric version exactly. `gpt 5.5` may normalize to
  `gpt-5.5`; it must not become `gpt-5.4`. `fable 5` may normalize to
  `claude-fable-5`, and `opus 4.7` may normalize to `claude-opus-4-7`;
  neither may become another Claude family or version.
- If the user says `gpt 5.4` or a `gpt-5.4` variant while choosing a model,
  pause before execution and ask whether they meant `gpt-5.5` or explicitly
  want `gpt-5.4`. This is an intent check, not an alias rule: do not rewrite
  the version yourself.
- For Codex, inspect `codex debug models` when needed and choose an available
  identifier with the same family and exact version. If no exact match exists
  or multiple matches are plausible, ask for the runnable model id.
- For Claude, preserve the named supported Claude family and version. Fable 5
  resolves to `claude-fable-5`; Opus 4.7 resolves to `claude-opus-4-7`. If the
  user names Sonnet or Haiku, fail loud and ask for a supported Claude choice.
- For Cursor Agent, always use `composer-2.5-fast`. Accept `agent`, `cursor`,
  `cursor agent`, `cursor-agent`, `composer`, `composer 2.5`,
  `composer-2.5`, `composer-2.5-fast`, or bare `2.5` only in Cursor Agent
  context as that runnable id. Do not use Cursor model discovery for
  non-Composer routing, and do not pass GPT/GBT, Claude, or Grok model ids to
  Cursor Agent.
- For Grok, use `grok-build` by default when the user says `grok`,
  `grok cli`, `grok build`, or `grok-build`. Use
  `grok-composer-2.5-fast` only when the user names Grok Composer, such as
  `grok composer`, `grok composer 2.5`, or `grok-composer-2.5-fast`. Inspect
  `grok models` when availability matters, and do not pass GPT/GBT, Claude, or
  Cursor Agent model ids to Grok.
- Do not run paid trial prompts to discover whether a Claude model exists. Use
  the CLI help/config surface when available; otherwise ask.

Always announce the raw-to-resolved mapping before execution:

```text
Claude Fable 5 high -> runtime=claude, model=claude-fable-5, effort=high
Claude Opus 4.7 xhigh -> runtime=claude, model=claude-opus-4-7, effort=xhigh
Grok Build high -> runtime=grok, model=grok-build, effort=high
```

For deterministic script plumbing that needs the same rules, use
`skills/_shared/model_resolution.py` instead of creating a local model alias
table. The helper exists to keep fresh-consult, agent-delegate,
model-consensus, Stepwise-style orchestrators, and arch-epic automatic
harnesses aligned on
exact-version preservation and fail-loud behavior.

For Fable delegate children, keep the prompt direct: state the task, write
scope, constraints, evidence expectations, and done-ness clearly. Do not ask
the child to show private reasoning or turn the delegation into a rigid step
script; keep the visible output contract to status, changed files,
verification, blockers, session metadata, and run directories.

## Effort Resolution

- Claude accepts `low`, `medium`, `high`, `xhigh`, and `max` via `--effort`.
- Codex effort is passed as `-c model_reasoning_effort='"<level>"'`.
- Grok accepts `low`, `medium`, `high`, `xhigh`, and `max` via `--effort`.
- Cursor Agent does not expose a separate `--effort` flag in the local CLI.
  Store effort as `encoded-in-model` and pass only
  `--model "composer-2.5-fast"`.
- For Codex, confirm the selected model supports the requested effort when
  `codex debug models` is needed for model resolution.
- If the effort is missing for Claude, Codex, or Grok, or the selected model
  does not support it, ask.
- A caller rule like "copywriting always xhigh" is execution intent from the
  caller. Apply it only to the delegated turn it clearly controls; do not add a
  built-in task taxonomy inside this skill.

## Run Directory

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

Write the prompt to `prompt.md`. Do not pass a long multiline prompt directly
on the command line.

`events.jsonl` is the live child stream. `stderr.log` is the diagnostic error
stream. `final.txt` is the final assistant text: Codex writes it directly with
`-o`; for Claude and Cursor Agent, copy the `result` text from the final
`type=result` event after the process exits. For Grok, concatenate streamed
`type=text` `data` chunks after the process exits.

Write `execution.json` before invocation with at least:

```json
{
  "mode": "fresh-one-shot | fresh-resumable | resume",
  "runtime": "claude | codex | agent | grok",
  "model": "<resolved model or reused-from-session>",
  "effort": "<resolved effort or reused-from-session>",
  "work_root": "<absolute path>",
  "forced_execution_on_resume": false
}
```

For fresh-resumable and resume runs, write the captured or reused session id to
`session_id.txt`. For resume runs, write the source run directory or explicit
session id to `resume_from.txt`.

## Parallel Delegation Group

Use the parallel group path only when the user asks for parallel agents or gives
multiple delegated tasks for this skill. Parallel workers are still ordinary
delegate children; the group only gives the parent a place to organize prompts,
streams, finals, execution metadata, and the combined report.

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

Launch each child with the same Codex, Claude, Cursor Agent, or Grok command
shape below, using that child's paths. Record the shell PID and exit status in
the child directory if the host shell makes that convenient, but do not
introduce a script, controller, detached monitor, separate worktree, or merge
layer.

Do not block launch because siblings might touch nearby files. Brief every
child that other workers may be editing the same repo, that unfamiliar changes
must not be reverted, and that actual conflicts should be reported with file
evidence. After all children finish, inspect repo state and child reports before
presenting the combined result.

Wait for all children before reporting. If one child fails or returns malformed
output, preserve its run directory and include that failure in the group report;
do not discard successful sibling work.

## Codex Fresh One-Shot

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

`--ephemeral` keeps the child stateless and cold. Use this only for
`fresh-one-shot`; ephemeral sessions are not resumable.

## Codex Fresh Resumable

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

Capture the `thread_id` from the first `thread.started` event in
`events.jsonl` and write it to `session_id.txt`. If no thread id is captured,
write `UNRECOVERABLE` to `session_id.txt`, treat the run as malformed, and
preserve the run directory.

## Codex Resume

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

`codex exec resume` carries the working directory from the original session.
Do not pass `-C` / `--cd` on resume.

Omit `--model` and effort config to reuse the session's execution choice. If
the caller explicitly requires a model or effort change on resume, announce
that mapping and add both flags:

```bash
  --model "<resolved_model>" \
  -c model_reasoning_effort='"<resolved_effort>"' \
```

Do not use `--last`; resume must name the exact `thread_id`.

## Claude Fresh

Use this shape for both `fresh-one-shot` and `fresh-resumable` Claude
delegations:

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

Run Claude from `work_root`. Do not pass `--no-session-persistence` for
fresh-resumable runs.

After Claude exits, read the final `type=result` event from `events.jsonl` and
write its `result` text to `final.txt` before applying the status-footer
checks. For fresh-resumable runs, also write the final result event's
`session_id` to `session_id.txt`. If no result event exists after a zero exit,
or a fresh-resumable run has no session id, treat the run as malformed and
preserve the run directory.

`--verbose` is required by the Claude CLI when `--output-format stream-json` is
used. Do not omit it from fresh or resumed Claude delegation commands.

## Claude Resume

Use this shape to resume an explicit Claude session:

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
  -r "<session_id>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Run the resume from the same `work_root` used by the original Claude session.
Use `-r <session_id>`, never `--continue`, because `--continue` chooses the
most recent conversation in the current directory and can collide with other
work.

After Claude exits, write the final `result` text to `final.txt`. Write the
returned `session_id` to `session_id.txt` when present; otherwise preserve the
input session id in `session_id.txt`.

## Cursor Agent Fresh

Use this shape for both `fresh-one-shot` and `fresh-resumable` Cursor Agent
delegations. Cursor Agent has no `--verbose` flag; that flag is Claude-only.
`<resolved_agent_model>` must be `composer-2.5-fast`.

```bash
agent -p \
  --force \
  --sandbox disabled \
  --output-format stream-json \
  --trust \
  --workspace "<work_root>" \
  --model "<resolved_agent_model>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Cursor Agent does not have a documented hook-suppression flag. Do not invent
one. Always pass `--output-format stream-json` explicitly because local help
and official docs have disagreed on the print-mode default. Do not add
`--verbose`; that flag is Claude-only.

After Cursor Agent exits, read the final `type=result` event from
`events.jsonl` and write its `result` text to `final.txt`. For
fresh-resumable runs, also write the final result event's `session_id` to
`session_id.txt`. If no result event exists after a zero exit, or a
fresh-resumable run has no session id, treat the run as malformed and preserve
the run directory.

## Cursor Agent Resume

Use this shape to resume an explicit Cursor Agent session. Cursor Agent has no
`--verbose` flag; that flag is Claude-only.
`<resolved_agent_model>` must be `composer-2.5-fast`.

```bash
agent -p \
  --force \
  --sandbox disabled \
  --output-format stream-json \
  --trust \
  --workspace "<work_root>" \
  --model "<resolved_agent_model>" \
  --resume "<session_id>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Use `--resume <session_id>` only. Do not use `--continue`, `agent resume`,
`agent ls`, or any latest-session selection. Do not use `--worktree` in this
shared-worktree skill unless a future user explicitly asks for a worktree-based
variant.

After Cursor Agent exits, write the final `result` text to `final.txt`. Write
the returned `session_id` to `session_id.txt` when present; otherwise preserve
the input session id in `session_id.txt`.

## Grok Fresh

Use this shape for both `fresh-one-shot` and `fresh-resumable` Grok
delegations:

```bash
RUST_LOG=off grok \
  --cwd "<work_root>" \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model "<resolved_grok_model>" \
  --effort "<resolved_effort>" \
  --output-format streaming-json \
  --prompt-file "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Do not pass `--sandbox disabled`; Grok does not accept that flag/value pair,
and its default local mode is unsandboxed. Grok has no documented
hook-suppression flag. Use `--no-auto-update`, `--no-memory`,
`--no-subagents`, and `--disable-web-search` for isolation.

After Grok exits, concatenate streamed `type=text` `data` chunks into
`final.txt`. For fresh-resumable runs, write the final `type=end` event's
`sessionId` to `session_id.txt`. If no final text exists after a zero exit, or
a fresh-resumable run has no `sessionId`, treat the run as malformed and
preserve the run directory.

## Grok Resume

Use this shape to resume an explicit Grok session:

```bash
RUST_LOG=off grok \
  --cwd "<work_root>" \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model "<resolved_grok_model>" \
  --effort "<resolved_effort>" \
  --output-format streaming-json \
  --resume "<session_id>" \
  --prompt-file "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Use `--resume <session_id>` only. Do not use any latest-session selection.
After Grok exits, write the final text to `final.txt` and preserve the returned
`sessionId` in `session_id.txt` when present.

## Monitoring Posture

Delegated work is not instant. A normal repo-backed task commonly takes 5+
minutes. Broad edits, verification, `xhigh`, or `max` can reasonably take
20-40 minutes.

Poll on a minutes-scale cadence. Check `events.jsonl`, `stderr.log`, repo
state if writes are expected, and process liveness every few minutes; do not
poll every few seconds. A missing `final.txt` before the process exits is not a
failure when the event stream is still alive. Investigate only after the
process exits non-zero, the stream shows an error, or there is no stream
activity for a long quiet window.

## Failure Behavior

Fail loud and preserve the run directory when:

- the selected CLI is missing
- runtime/model/effort cannot be resolved exactly
- the allowed write scope is missing or unsafe
- resume mode has no explicit session id or prior run directory
- `session_id.txt` is missing, empty, or `UNRECOVERABLE` for a resume
- the caller asks for cross-runtime resume
- the caller asks for Claude `--continue`, Codex `--last`, Cursor Agent
  `--continue`, `agent resume`, `agent ls`, Grok latest-session selection, or
  any other "latest" resume selection
- the child exits non-zero
- `final.txt` is empty
- Claude exits without a final `type=result` event
- Cursor Agent exits without a final `type=result` event
- Grok exits without final text
- fresh-resumable Codex does not emit `thread.started`
- fresh-resumable Grok does not emit a final `sessionId`
- the child omits the required status footer

Do not silently fall back between Claude, Codex, Cursor Agent, and Grok, one
model to another model, one effort level to another, foreground to detached
execution, or shared-worktree execution to a separate worktree.
