# Model And Invocation

Use this reference to resolve what the user meant by "Claude", "Codex",
"opus high", "gpt 5.5 xhigh", or similar phrasing, and to run the selected
fresh subprocess.

## Required Values

Every consult needs three execution values:

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

- `codex`, `gpt`, `gpt-5.5`, `gpt 5.5 high`, or `gpt-5.3-codex` implies
  `runtime=codex`.
- `claude`, `opus`, `sonnet`, or `haiku` implies `runtime=claude`.
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
- For Claude, when the runtime is Claude and the user names family plus
  version, prefer `claude-<family>-<version-with-hyphens>`, for example
  `claude-opus-4-7` or `claude-sonnet-4-6`.
- Family-only Claude aliases such as `opus`, `sonnet`, or `haiku` are allowed
  only when the user did not pin a version.
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

Create one run directory per consult:

```bash
CONSULT_SLUG="<short-slug>"
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$(mktemp -d "/tmp/fresh-consult/${CONSULT_SLUG}-${RUN_TS}-XXXXXX")"
PROMPT_PATH="$RUN_DIR/prompt.md"
FINAL_PATH="$RUN_DIR/final.txt"
STREAM_PATH="$RUN_DIR/stream.log"
```

Write the prompt to `prompt.md`. Do not pass a long multiline prompt directly
on the command line.

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
  -o "$FINAL_PATH" \
  < "$PROMPT_PATH" \
  > "$STREAM_PATH" 2>&1
```

Flag meanings:

- `--ephemeral` keeps the child stateless and cold.
- `--disable codex_hooks` prevents hook recursion.
- `-C <work_root>` pins the filesystem context.
- `--dangerously-bypass-approvals-and-sandbox` gives the child realistic local
  access. Use only in trusted local environments.
- `--skip-git-repo-check` allows doc or artifact consults outside a git root.
- `-o "$FINAL_PATH"` captures the final assistant message.

## Claude Command

Use this shape for a Claude consult:

```bash
claude -p \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model "<resolved_model>" \
  --effort "<resolved_effort>" \
  < "$PROMPT_PATH" \
  > "$FINAL_PATH" 2> "$STREAM_PATH"
```

Flag meanings:

- `-p` runs non-interactively and exits.
- `--dangerously-skip-permissions` gives the child realistic local access. Use
  only in trusted local environments.
- `--settings '{"disableAllHooks":true}'` prevents hook recursion.
- `--model` and `--effort` pin the execution choice.

Do not use `-r`, `--resume`, `--continue`, or Codex `exec resume`; a consult is
a cold read, not a resumed conversation.

## Failure Behavior

Fail loud and preserve the run directory when:

- the selected CLI is missing
- runtime/model/effort cannot be resolved exactly
- the child exits non-zero
- `final.txt` is empty
- the child omits the required verdict footer

Do not silently fall back from Claude to Codex, Codex to Claude, one model to
another model, or one effort level to another.
