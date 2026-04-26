# Model And Invocation

`model-consensus` invokes child models directly from the parent agent. It does
not create a new runner script, model alias table, harness, or deterministic
controller.

## Required Participant Values

Each participant needs:

- `runtime`: `claude` or `codex`
- `model`: runnable model id or exact model phrase
- `effort`: `low`, `medium`, `high`, `xhigh`, or `max` when supported by the
  selected runtime/model
- `role`: `collaborator` or `adversary`

If any execution choice is missing or ambiguous, ask one consolidated question:

```text
Before I run model-consensus, I need the two participant choices. These are
real external model sessions and can spend model budget. Please give
runtime/model/effort for Model A and Model B, and say whether either should be
adversarial.
```

## Model Phrase Resolution

Follow the shared model-resolution doctrine:

- Preserve family and numeric version exactly. `gpt 5.5` may normalize to
  `gpt-5.5`; it must not become `gpt-5.4`. `opus 4.7` may normalize to
  `claude-opus-4-7`; it must not become another Opus version.
- Infer runtime only from unambiguous family evidence: `gpt`/`codex` implies
  Codex; `claude`/`opus`/`sonnet`/`haiku` implies Claude.
- For Codex, inspect `codex debug models` when model availability matters and
  choose an available id with the same family and exact version.
- For Claude family plus version, prefer
  `claude-<family>-<version-with-hyphens>`, such as `claude-opus-4-7`.
- Family-only Claude aliases are allowed only when the user did not pin a
  version.
- Do not run paid trial prompts to discover Claude model availability.
- If discovery is unavailable, ambiguous, or no exact match exists, ask for the
  runnable model id.

For deterministic plumbing that already needs the same resolver, use
`skills/_shared/model_resolution.py`. Do not add another model shorthand file
to this skill.

Always announce the mapping before execution:

```text
Model A: "Claude Opus 4.7 xhigh" -> runtime=claude, model=claude-opus-4-7, effort=xhigh
Model B: "gpt 5.5 xhigh" -> runtime=codex, model=gpt-5.5, effort=xhigh
```

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
active monitoring path.

```bash
claude -p \
  --output-format stream-json \
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

## Claude: Resume Turn

```bash
claude -p \
  --output-format stream-json \
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

## Monitoring Posture

Choose foreground or background intentionally:

- Foreground is better for short prompts because the parent does not need a
  polling loop.
- Background is better for long repo-reading rounds, but only with full event
  streams preserved.
- Default to a minutes-scale check cadence for long children. A 60 second floor
  is acceptable for active monitoring; several minutes is better when the
  stream is clearly alive.
- Do not treat an empty final file after four or nine minutes as "hung" when
  the process still exists and event streams may not have reached a final
  message. Large planning rounds can take 20 to 60 minutes.
- Investigate before terminating. Check process state, event stream growth,
  tool calls, partial messages, stderr, and whether the model is blocked on a
  permission or input prompt.

Failure is explicit: missing CLI, unresolved exact model, child non-zero exit,
empty final result after process exit, or a child refusing the prompt contract.
Do not silently switch runtimes, downgrade models, reduce effort, or replace a
long-running child with the parent agent's own answer.
