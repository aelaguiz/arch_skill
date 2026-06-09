# Model And Invocation

`model-consensus` invokes Claude, Codex, Cursor Agent, or Grok child models
directly from the parent agent. It does not create a new runner script, model
alias table, harness, or deterministic controller.
Provider routing is fixed: Codex runs GPT/GBT/OpenAI models, Claude Code runs
supported Claude models, Cursor Agent runs Composer 2.5 Fast, and Grok CLI runs
Grok models.

## Required Participant Values

Each participant needs:

- `runtime`: `claude`, `codex`, `agent`, or `grok`
- `model`: runnable model id or exact model phrase
- `effort`: `low`, `medium`, `high`, `xhigh`, or `max` when supported by the
  selected runtime/model
- `role`: `collaborator` or `adversary`

If any execution choice is missing or ambiguous, ask one consolidated question:

```text
Before I run model-consensus, I need the two participant choices. These are
real external model sessions and can spend model budget. Please give
runtime/model/effort for Model A and Model B, and say whether either should be
adversarial. Cursor Agent is Composer-only; Grok defaults to grok-build unless
you name Grok Composer.
```

## Model Phrase Resolution

Follow the shared model-resolution doctrine:

- Preserve family and numeric version exactly. `gpt 5.5` may normalize to
  `gpt-5.5`; it must not become `gpt-5.4`. `fable 5` may normalize to
  `claude-fable-5`, and `opus 4.7` may normalize to `claude-opus-4-7`;
  neither may become another Claude family or version.
- If the user says `gpt 5.4` or a `gpt-5.4` variant while choosing a model,
  pause before execution and ask whether they meant `gpt-5.5` or explicitly
  want `gpt-5.4`. This is an intent check, not an alias rule: do not rewrite
  the version yourself.
- Infer runtime only from unambiguous family evidence: `gpt`/`gbt`/`codex`
  implies Codex; `claude fable`, `fable`, `claude opus`, or `opus` implies
  Claude; `agent`, `cursor`, `cursor agent`, or `cursor-agent` implies Cursor
  Agent only for Composer.
  `grok`, `grok-build`, `grok build`, or `grok composer` implies Grok.
  If a phrase mixes Cursor Agent with GPT/GBT or Claude, fail loud instead of
  choosing a side. If a phrase mixes Grok with GPT/GBT, Claude, or Cursor
  Agent, fail loud instead of choosing a side.
- For Codex, inspect `codex debug models` when model availability matters and
  choose an available id with the same family and exact version.
- For Claude, preserve the named supported Claude family and version. Fable 5
  resolves to `claude-fable-5`; Opus 4.7 resolves to `claude-opus-4-7`. If the
  user names Sonnet or Haiku, fail loud and ask for a supported Claude choice.
- For Cursor Agent, always use `composer-2.5-fast`. Accept `composer`,
  `composer 2.5`, `composer-2.5`, `composer-2.5-fast`, or bare `2.5` in a
  Cursor Agent context as that runnable id. Do not use Cursor model discovery
  for non-Composer routing, and do not pass GPT/GBT or Claude model ids to
  Cursor Agent.
- For Grok, use `grok-build` by default when the user says `grok`,
  `grok cli`, `grok build`, or `grok-build`. Use
  `grok-composer-2.5-fast` only when the user names Grok Composer, such as
  `grok composer`, `grok composer 2.5`, or `grok-composer-2.5-fast`. Inspect
  `grok models` when availability matters.
- Bare `composer`, `composer 2.5`, or bare `2.5` is ambiguous unless the user
  explicitly names Cursor Agent or Grok in the same execution choice.
- Do not run paid trial prompts to discover Claude model availability.
- If discovery is unavailable, ambiguous, or no exact match exists, ask for the
  runnable model id.

For deterministic plumbing that already needs the same resolver, use
`skills/_shared/model_resolution.py`. Do not add another model shorthand file
to this skill.

Always announce the mapping before execution:

```text
Model A: "Claude Fable 5 high" -> runtime=claude, model=claude-fable-5, effort=high
Model B: "Claude Opus 4.7 xhigh" -> runtime=claude, model=claude-opus-4-7, effort=xhigh
Model C: "gpt 5.5 xhigh" -> runtime=codex, model=gpt-5.5, effort=xhigh
Model D: "Grok Build high" -> runtime=grok, model=grok-build, effort=high
```

For Fable participant prompts, keep the brief direct: state the goal,
constraints, evidence obligations, and done-ness clearly. Do not ask the child
to show private reasoning or turn the dialogue into a rigid step script; keep
the visible output contract to proposals, critiques, agreement status, evidence,
session metadata, and run directories.

## Run Directory

Create the artifact directory by hand:

```bash
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR=".arch_skill/model-consensus/<goal-slug>-${RUN_TS}"
mkdir -p "$RUN_DIR"
```

Write prompts to files. Long multiline prompts should go through stdin or a
prompt file, not a huge shell argument. Keep event streams and final messages
separate enough that the parent can inspect progress without reading long
transcripts into context.

## Codex: First Turn

Use a resumable Codex session for each participant. Do not pass `--ephemeral`
for participants because the dialogue needs `codex exec resume`.

```bash
codex exec \
  --cd "<work_root>" \
  --disable codex_hooks \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --model "<resolved_model>" \
  -c model_reasoning_effort='"<resolved_effort>"' \
  --json \
  -o "$RUN_DIR/round-01/model-a-final.md" \
  < "$RUN_DIR/round-01/model-a-prompt.md" \
  > "$RUN_DIR/round-01/model-a-events.jsonl" \
  2> "$RUN_DIR/round-01/model-a-stderr.log"
```

Read the `thread.started` event from `events.jsonl` and keep its `thread_id`.
Codex streams JSONL events on stdout and writes the final assistant message to
the path passed with `-o`.

## Codex: Resume Turn

```bash
codex exec resume <thread_id> \
  --disable codex_hooks \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --json \
  -o "$RUN_DIR/round-02/model-a-final.md" \
  < "$RUN_DIR/round-02/model-a-prompt.md" \
  > "$RUN_DIR/round-02/model-a-events.jsonl" \
  2> "$RUN_DIR/round-02/model-a-stderr.log"
```

`codex exec resume` carries the original working directory. It does not need
`--cd` on resume.

## Claude: First Turn

Use `stream-json` for participant sessions so long repo-reading work has an
active monitoring path. Cursor Agent has no `--verbose` flag; that flag is
Claude-only.

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
  < "$RUN_DIR/round-01/model-b-prompt.md" \
  > "$RUN_DIR/round-01/model-b-events.jsonl" \
  2> "$RUN_DIR/round-01/model-b-stderr.log"
```

The final `type=result` event contains the result text and `session_id`. Keep
that `session_id` for resume. Run Claude resumes from the same working
directory as the first turn.
`--verbose` is required by the Claude CLI when `stream-json` output is used.

## Claude: Resume Turn

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
  -r <session_id> \
  < "$RUN_DIR/round-02/model-b-prompt.md" \
  > "$RUN_DIR/round-02/model-b-events.jsonl" \
  2> "$RUN_DIR/round-02/model-b-stderr.log"
```

Use `-r <session_id>`, not "continue latest", because multiple child sessions
may exist in the same repo.

## Cursor Agent: First Turn

Use `stream-json` for participant sessions so long repo-reading work has an
active monitoring path. Cursor Agent has no `--verbose` flag; that flag is
Claude-only.
`<resolved_agent_model>` must be `composer-2.5-fast`.

```bash
agent -p \
  --output-format stream-json \
  --trust \
  --workspace "<work_root>" \
  --model "<resolved_agent_model>" \
  < "$RUN_DIR/round-01/model-a-prompt.md" \
  > "$RUN_DIR/round-01/model-a-events.jsonl" \
  2> "$RUN_DIR/round-01/model-a-stderr.log"
```

The final `type=result` event contains the result text and `session_id`. Keep
that `session_id` for resume. Always pass `--output-format` explicitly.
Cursor Agent has no documented hook-suppression flag and no `--verbose` flag;
do not invent either one.

## Cursor Agent: Resume Turn

```bash
agent -p \
  --output-format stream-json \
  --trust \
  --workspace "<work_root>" \
  --model "<resolved_agent_model>" \
  --resume "<session_id>" \
  < "$RUN_DIR/round-02/model-a-prompt.md" \
  > "$RUN_DIR/round-02/model-a-events.jsonl" \
  2> "$RUN_DIR/round-02/model-a-stderr.log"
```

Use `--resume <session_id>`, not `--continue`, `agent resume`, or `agent ls`,
because multiple child sessions may exist in the same repo. Do not add
`--verbose`; that flag is Claude-only. `<resolved_agent_model>` must be
`composer-2.5-fast`.

## Grok: First Turn

Use a resumable Grok session for each Grok participant:

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
  --prompt-file "$RUN_DIR/round-01/model-a-prompt.md" \
  > "$RUN_DIR/round-01/model-a-events.jsonl" \
  2> "$RUN_DIR/round-01/model-a-stderr.log"
```

Concatenate streamed `type=text` `data` chunks into the participant final file.
Keep the final `type=end` event's `sessionId` for resume. Do not pass
`--sandbox disabled`; Grok does not accept that flag/value pair, and its
default local mode is unsandboxed. Grok has no documented hook-suppression
flag.

## Grok: Resume Turn

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
  --prompt-file "$RUN_DIR/round-02/model-a-prompt.md" \
  > "$RUN_DIR/round-02/model-a-events.jsonl" \
  2> "$RUN_DIR/round-02/model-a-stderr.log"
```

Use `--resume <session_id>`, not latest-session selection, because multiple
child sessions may exist in the same repo.

## Monitoring Posture

Choose foreground or background intentionally:

- Foreground is better for short prompts because the parent does not need a
  polling loop.
- Background is better for long repo-reading rounds, but only with full event
  streams preserved.
- Normal child rounds commonly take 5+ minutes. Broad repo-reading rounds,
  `xhigh`, or `max` can reasonably take 20-40 minutes.
- Default to a minutes-scale check cadence for long children. A 60 second floor
  is acceptable for active monitoring; several minutes is better when the
  stream is clearly alive.
- Do not treat an empty final file after four or nine minutes as "hung" when
  the process still exists and event streams may not have reached a final
  message. Large planning rounds can exceed the 20-40 minute norm.
- Investigate before terminating. Check process state, event stream growth,
  tool calls, partial messages, stderr, and whether the model is blocked on a
  permission or input prompt.

Failure is explicit: missing CLI, unresolved exact model, child non-zero exit,
empty final result after process exit, missing terminal result event, or a
child refusing the prompt contract. Do not silently switch runtimes, downgrade
models, reduce effort, or replace a long-running child with the parent agent's
own answer.
