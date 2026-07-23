# Model And Invocation

Use this reference after the caller has deliberately selected the external
worker lane under `../../_shared/agent-orchestration-policy.md`. It owns model
resolution, command syntax, exact external-session continuation, and receipt
capture; it does not decide the worker's role, decompose the task, or integrate
the result.

Use it to resolve what the user meant by "Claude", "Codex",
"Cursor Agent", "Grok", "Kimi", "fable 5 high", "opus high", "gpt-5.6-sol ultra",
"luna xhigh", "terra high", "fugu high", "fugu-ultra xhigh",
"composer-2.5-fast", "grok-4.5", "kimi k3", or
similar phrasing, and to run the
selected worker subprocess or explicit parallel group of worker subprocesses.
Fresh-resumable is the default: new children start cold but capture a session
handle for later exact resume. Provider routing is fixed: Codex runs
GPT/GBT/OpenAI model ids and Fugu profiles, Claude Code runs supported Claude
models, Cursor Agent runs Composer 2.5 Fast, Grok CLI runs Grok models, and
Kimi Code runs Kimi K3.

## External Context

External context is explicit: `fresh-one-shot` and `fresh-resumable` start
clean from the prompt and disk; `resume` continues the exact captured worker.
None inherits bounded or full parent chat automatically. Context remains
separate from the shared worktree, unsandboxed permissions, and process
isolation used below.

## Required Values

Every delegation child needs:

- `mode` - `fresh-one-shot`, `fresh-resumable`, or `resume`
- `runtime` - `claude`, `codex`, `agent`, `grok`, or `kimi`
- `model` - the runnable CLI model identifier or Codex profile name, or the
  previous session model/profile when a resume intentionally reuses it.
  An omitted model on a Codex lane resolves to `gpt-5.6-sol`; an omitted model
  on a Kimi lane resolves to `kimi-code/k3`.
- `effort` - the reasoning effort level, or the previous session effort when a
  resume intentionally reuses it. GPT-5.6 Sol defaults an omitted effort to
  `ultra`; Kimi K3 defaults one to `max`.

Resume mode also needs either:

- `session_id` - Claude `session_id`, Codex `thread_id`, Cursor Agent
  `session_id`, Grok `sessionId`, or Kimi `session_id` from the
  `session.resume_hint` meta event
- `run_dir` - a previous `agent-delegate` run directory containing
  `session_id.txt` and `execution.json`

If any required value is missing or ambiguous after applying the Codex
model/Sol-effort defaults and the Kimi defaults, ask one consolidated question
before invoking:

```text
I need the delegate runtime, any non-default effort, a model/profile outside
the Codex and Kimi defaults when applicable, and the resume handle before
invoking an external agent. The delegate runs as a foreground subprocess, can
edit the shared worktree, and can spend real model budget. What should I use?
```

Add only the missing facts to the question when some values are already known.

Parallel groups use the same required values for each child. Default to one
shared runtime/model/effort for all children. If the user clearly assigns
different execution choices to different children, apply those choices exactly
and announce the mapping before launch.

## Delegation Mode

- `fresh-resumable` is the default. It creates a cold child that captures a
  session handle and can be resumed later by exact handle.
- `fresh-one-shot` creates a cold child and may use stateless CLI flags. Use it
  only when the caller explicitly asks for a stateless, ephemeral, no-resume, or
  throwaway worker.
- `resume` continues an explicit same-runtime session id or prior run
  directory. Do not resume "latest" sessions, do not use Claude `--continue`,
  and do not use Codex `--last`.

Same-runtime is mandatory. Claude sessions resume through Claude with
`-r <session_id>`. Codex threads resume through `codex exec resume
<thread_id>`. Cursor Agent sessions resume through `agent -p --resume
<session_id>`. Grok sessions resume through `grok --resume <session_id>`.
Kimi sessions resume through `kimi -r <session_id>` from the original working
directory. Never use Kimi `-c`/`--continue`, which selects the latest session.

Parallel delegation defaults to `fresh-resumable` and also supports explicit
`fresh-one-shot`. Keep
`resume` on the single-worker path; launching several resumed sessions at once
is a different orchestration problem and is not part of this prompt-first
skill.

## Runtime Inference

Infer runtime only when the user's wording makes it unambiguous:

- `codex`, `openai`, `gpt`, `gbt`, `sol`, `luna`, `terra`,
  `gpt-5.6-sol`, `gpt-5.6-luna`, `gpt-5.6-terra`, `GPT56SOLXI`,
  `GPT56LUNAXI`, `GPT56TERRAXI`, `gpt-5.3-codex`, `fugu high`, or
  `fugu-ultra xhigh` implies `runtime=codex`.
- `claude fable`, `fable`, `claude opus`, or `opus` implies
  `runtime=claude`.
- `sonnet` and `haiku` are not supported by this repo's subprocess doctrine;
  ask for a supported Claude choice instead of silently running them.
- `agent`, `cursor`, `cursor agent`, or `cursor-agent` implies
  `runtime=agent` only for Composer. Cursor Agent always resolves to
  `composer-2.5-fast`.
- `grok`, natural `grok build`, natural `grok cli`, `grok-4.5`, or an explicit
  legacy `grok-*` slug implies `runtime=grok`.
- `kimi`, `kimi code`, `kimi k3`, `k3`, or `moonshot` implies `runtime=kimi`.
  An omitted Kimi model resolves to `kimi-code/k3`; an omitted Kimi effort
  resolves to `max` and is reported as a model default.
- Bare `composer`, `composer 2.5`, or bare `2.5` is ambiguous unless the user
  explicitly names Cursor Agent or Grok in the same execution choice.
- If a phrase mixes Cursor Agent with GPT/GBT model ids, Fugu profiles, or
  Claude, fail loud instead of choosing a side. Never run GPT/GBT model ids,
  Fugu profiles, or Claude models through Cursor Agent.
- If a phrase mixes Grok or Kimi with GPT/GBT model ids, Fugu profiles, Claude, or
  Cursor Agent, fail loud instead of choosing a side.
- If the user names only an effort level, such as "xhigh", ask for runtime.
  If the answer is Codex and still omits a model, use `gpt-5.6-sol`.
- If the user says only "delegate this" or "have another agent do this", ask
  for runtime; ask for effort or a model/profile only when the selected lane
  falls outside the Sol and Kimi defaults. Omitted Sol effort is the deliberate
  `ultra` preference default; omitted Kimi effort is the deliberate `max`
  model default.

The defaults are deliberately narrow: when the lane is Codex and no model or
profile is named, use `gpt-5.6-sol`; when a Sol lane omits effort, use `ultra`
with `effort_source=preference_default`; when the lane is Kimi, use
`kimi-code/k3` and default an omitted effort to `max`. Do not default the
runtime itself, and do not invent defaults for Claude, Cursor Agent, Grok,
other Codex models, or Fugu profiles.

## Model Phrase Resolution

Treat model text as intent, not a loose alias:

- Accept `sol`, `luna`, and `terra` as the Codex 5.6 choices. They resolve to
  `gpt-5.6-sol`, `gpt-5.6-luna`, and `gpt-5.6-terra`; compact forms such as
  `GPT56LUNAXI` and `GPT56TERRAXI` preserve the named variant and imply
  `xhigh`. If a Codex lane names no model or profile, resolve it to
  `gpt-5.6-sol` and report that the model came from the default. If the
  resulting Sol lane names no effort, resolve it to `ultra` and report
  `effort_source=preference_default`.
- Preserve model family and numeric version exactly. `gpt-5.6-luna` may normalize to
  `gpt-5.6-luna`; it must not become `gpt-5.6-sol`, `gpt-5.4`, or `gpt-5.5`. `fable 5` may normalize to
  `claude-fable-5`, and `opus 4.7` may normalize to `claude-opus-4-7`;
  neither may become another Claude family or version.
- If the user says `gpt 5.4`, `gpt 5.5`, or a variant of either while choosing
  a model, do not execute it. Say that the old model is blocked and ask whether
  they meant `gpt-5.6-sol`. This is an intent check, not an alias rule: do not
  rewrite the version yourself.
- For ordinary Codex model ids, inspect `codex debug models` when needed and
  choose an available identifier with the same family and exact version. For
  Fugu, resolve `fugu` and `fugu-ultra` as Codex profiles, not model-list ids;
  preserve the profile names exactly and launch them with `-p`.
- For Claude, preserve the named supported Claude family and version. Fable 5
  resolves to `claude-fable-5`; Opus 4.7 resolves to `claude-opus-4-7`. If the
  user names Sonnet or Haiku, fail loud and ask for a supported Claude choice.
- For Cursor Agent, always use `composer-2.5-fast`. Accept `agent`, `cursor`,
  `cursor agent`, `cursor-agent`, `composer`, `composer 2.5`,
  `composer-2.5`, `composer-2.5-fast`, or bare `2.5` only in Cursor Agent
  context as that runnable id. Do not use Cursor model discovery for
  non-Composer routing, and do not pass GPT/GBT model ids, Fugu profiles,
  Claude, or Grok model ids to Cursor Agent.
- For Grok, natural `grok`, `grok cli`, and `grok build` wording resolves to
  the current `grok-4.5` model. Treat the product phrase “Grok Build” as the
  Grok harness, not as a model id. If that wording names a numeric version
  other than `4.5`, fail loud rather than discarding it. Preserve an explicitly named legacy slug
  such as `grok-build` or `grok-composer-2.5-fast` exactly and require it to be
  discoverable; never rewrite it to `grok-4.5`. Inspect `grok models` when
  availability matters, and do not pass another provider's model ids to Grok.
- For Kimi, `kimi`, `kimi code`, `kimi k3`, `k3`, and `moonshot` resolve to
  `kimi-code/k3` in the Kimi lane. Preserve the callable alias exactly. Do not
  auto-resolve older Kimi-for-coding/K2.7 aliases in this K3 contract, and do
  not pass another provider's model id to Kimi. When availability matters,
  inspect the top-level `.models` keys from `kimi provider list --json`.
- Do not run paid trial prompts to discover whether a Claude model exists. Use
  the CLI help/config surface when available; otherwise ask.

Always announce the raw-to-resolved mapping before execution:

```text
Claude Fable 5 high -> runtime=claude, model=claude-fable-5, effort=high
Claude Opus 4.7 xhigh -> runtime=claude, model=claude-opus-4-7, effort=xhigh
Codex -> runtime=codex, model=gpt-5.6-sol, effort=ultra, model_source=default, effort_source=preference_default
Codex high -> runtime=codex, model=gpt-5.6-sol, effort=high, model_source=default
Luna xhigh -> runtime=codex, model=gpt-5.6-luna, effort=xhigh
Terra high -> runtime=codex, model=gpt-5.6-terra, effort=high
Fugu Ultra xhigh -> runtime=codex, model=fugu-ultra, codex_profile=fugu-ultra, effort=xhigh
Grok Build high -> runtime=grok, model=grok-4.5, effort=high
Kimi K3 high -> runtime=kimi, model=kimi-code/k3, effort=high
Kimi -> runtime=kimi, model=kimi-code/k3, effort=max, effort_source=model_default
```

For deterministic script plumbing that needs the same rules, use
`../../_shared/model_resolution.py` instead of creating a local model alias
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
- For ordinary Codex model ids, pass effort as
  `-c model_reasoning_effort='"<level>"'`. GPT-5.6 Sol uses `ultra` when the
  effort is omitted; preserve any explicit supported effort instead.
- For Fugu profiles, use `-p fugu` or `-p fugu-ultra`. Omit `-c` when using
  the profile default (`fugu` defaults to `high`; `fugu-ultra` defaults to
  `xhigh`). Add `-c model_reasoning_effort='"<level>"'` only when the user
  explicitly requests a supported non-default Fugu Ultra effort.
- `grok-4.5` accepts its catalog-advertised `low`, `medium`, and `high` efforts
  via `--effort`. Do not widen that set because the generic CLI parser accepts
  other effort words. Explicit legacy Grok ids remain exact and discovery-gated
  without invented model-specific effort metadata.
- Kimi K3 advertises `low`, `high`, and `max`, with `max` as its model default.
  Pass effort through the process environment as
  `KIMI_MODEL_THINKING_EFFORT=<level>`; Kimi has no `--effort` flag. Preserve an
  explicit `medium` or `xhigh` verbatim as a forced override, but never select
  either by default or inference and never remap one effort to another.
- Cursor Agent does not expose a separate `--effort` flag in the local CLI.
  Store effort as `encoded-in-model` and pass only
  `--model "composer-2.5-fast"`.
- For ordinary Codex model ids, confirm the selected model supports the
  requested effort when `codex debug models` is needed for model resolution.
  `codex debug models` does not prove whether local Fugu profiles exist.
- Outside the Sol and Kimi defaults, if a required effort is missing or the
  selected model does not support it, ask. Sol defaults an omitted effort to
  `ultra`; Kimi defaults one to `max`.
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

Write the prompt to `prompt.md`. Codex and Claude consume it through stdin and
Grok uses its prompt-file flag. Kimi has no verified prompt-file or stdin form,
so pass the file contents as one `-p` argv value without a shell; recognize that
the operating-system argv-size limit can reject an unusually large prompt.

`events.jsonl` is the live child stream. `stderr.log` is the diagnostic error
stream. `final.txt` is the final assistant text: Codex writes it directly with
`-o`; for Claude and Cursor Agent, copy the `result` text from the final
`type=result` event after the process exits. For Grok, concatenate streamed
`type=text` `data` chunks after the process exits. For Kimi, concatenate the
`content` values of `role=assistant` events after exit.

Write `execution.json` before invocation with at least:

```json
{
  "transport": "external",
  "external_benefit": "<concrete provider/model/lifecycle/isolation/automation/receipt benefit>",
  "starting_context": "clean-prompt-and-disk | existing-exact-session-context",
  "continuation": "new-one-shot | new-resumable-session | exact-session-resume",
  "mode": "fresh-one-shot | fresh-resumable | resume",
  "runtime": "claude | codex | agent | grok | kimi",
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
multiple delegated tasks for this skill and the parent can review every result.
Parallel workers are still ordinary external delegates; the group only gives
the parent a place to organize prompts, streams, finals, execution metadata,
and the combined report. The parent owns the concurrency budget and assigns
non-overlapping owner paths when edits would otherwise collide; children do
not create their own children unless an explicit nested scope and budget says
otherwise.

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

Launch each child with the same Codex, Claude, Cursor Agent, Grok, or Kimi command
shape below, using that child's paths. Record the shell PID and exit status in
the child directory if the host shell makes that convenient, but do not
introduce a script, controller, detached monitor, separate worktree, or merge
layer.

Nearby files alone do not prove a collision, but sequence work that shares one
owner or assign non-overlapping write scopes where practical. Brief every child
that other workers may be editing the same repo, that unfamiliar changes must
not be reverted, and that actual conflicts should be reported with file
evidence. After all children finish, inspect repo state and child reports before
presenting the combined result.

Wait for all children before reporting. If one child fails or returns malformed
output, preserve its run directory and include that failure in the group report;
do not discard successful sibling work.

## Codex Fresh Resumable

Use this shape for the default fresh-resumable Codex delegation:

```bash
codex exec \
  --disable codex_hooks \
  -C "<work_root>" \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  <codex_model_or_profile_flags> \
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

## Codex Fresh One-Shot

Use this shape only for explicit stateless Codex delegation:

```bash
codex exec \
  --ephemeral \
  --disable codex_hooks \
  -C "<work_root>" \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  <codex_model_or_profile_flags> \
  --json \
  -o "$FINAL_PATH" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

`--ephemeral` keeps the child stateless and cold. Use this only for
`fresh-one-shot`; ephemeral sessions are not resumable.

Set `<codex_model_or_profile_flags>` this way:

- Ordinary Codex model id: `--model "<resolved_model>" -c model_reasoning_effort='"<resolved_effort>"'`
- Fugu profile at its default effort: `-p "<resolved_codex_profile>"`
- Fugu Ultra explicit non-default effort: `-p "fugu-ultra" -c model_reasoning_effort='"<resolved_effort>"'`

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

Omit model/profile and effort config to reuse the session's execution choice.
If the caller explicitly requires a model/profile or effort change on resume,
announce that mapping and add the matching flags:

```bash
  <codex_model_or_profile_flags> \
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

## Kimi Fresh

Use this shape for both `fresh-one-shot` and `fresh-resumable` Kimi runs. Fresh
means no prior conversation is resumed; Kimi still persists a session:

```bash
KIMI_CODE_NO_AUTO_UPDATE=1 \
KIMI_MODEL_THINKING_EFFORT="<resolved_effort>" \
kimi \
  -m "<resolved_kimi_model>" \
  -p "$(cat "$PROMPT_PATH")" \
  --output-format stream-json \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Run the process from `work_root`; Kimi has no working-directory flag and its
sessions are cwd-scoped. Build argv directly in a real implementation rather
than evaluating this illustrative shell with untrusted prompt text.

Kimi always persists a session. `fresh-one-shot` may ignore its receipt, but it
is not ephemeral; this lane cannot satisfy a load-bearing stateless/no-persist
requirement.

Print mode performs automatic approval, but it is not a full permission, hook,
or static-denial bypass. Do not add `--yolo`, `--auto`, or `--plan`; those flags
conflict with `-p`. Kimi has no documented hook-suppression flag and inherits
the user's configured hooks and MCP servers. Do not invent sandbox, memory, or
hook flags.

After exit, concatenate every `role=assistant` event's string `content` into
`final.txt`. Capture the durable `session_id` from the
`role=meta`, `type=session.resume_hint` event and write it to `session_id.txt`
for a fresh-resumable run. Missing assistant text or a missing resume hint when
continuation was promised is malformed output; preserve the run directory.

## Kimi Resume

Resume only the exact captured Kimi session, from the same `work_root`:

```bash
KIMI_CODE_NO_AUTO_UPDATE=1 \
KIMI_MODEL_THINKING_EFFORT="<resolved_effort>" \
kimi \
  -r "<session_id>" \
  -m "<resolved_kimi_model>" \
  -p "$(cat "$PROMPT_PATH")" \
  --output-format stream-json \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Use `-r <session_id>`, never `-c`/`--continue` or another latest-session
selector. Parse final text and require a fresh returned resume hint exactly as
in a fresh run. A missing hint is unrecoverable for promised continuation; do
not reuse the input id as a fallback.

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

This section governs in-flight liveness only, never result acceptance: a
clean exit with `STATUS: done` still gets the post-completion checks in
`delegate-prompt-and-output.md` — repo truth, loaded work products, and
conclusion anchors. When a calling skill imposes its own monitoring doctrine
(for example the conductor's heartbeat rules, which forbid streaming
`events.jsonl` into its context), the caller's doctrine governs the parent
side; prefer cheap signals — process liveness, `stderr.log` growth,
changed-file mtimes — over consuming the event stream.

## Codex Usage-Limit Continuity

A Codex worker that dies on a hard usage limit is recoverable without losing
its session. Recognize it from the run artifacts: `stderr.log` or
`events.jsonl` showing a usage-limit / out-of-credits error on exit. A
transient reconnect or backoff message is not a limit; leave those to codex's
own retry.

When the limit is real and an `aim` account pool is available:

1. Rotate per `../../_shared/aim-rotation.md`: pick a healthy account,
   `aim codex use <label>`, verify the switch took.
2. Continue the **same worker** through the normal `resume` mode with the
   captured `session_id.txt` — a new process on the new account, appending to
   the same session. Match the original launch shape (profile, model,
   effort).
3. Verify the resumed worker actually makes progress on the new account
   before reporting it recovered.

This is exact-session continuation on the same runtime and model, not a
fallback, so it does not violate the no-silent-fallback rule below — but say
in the parent report that a rotation happened and on which account the work
finished. Without an `aim` pool, a usage-limit death is an ordinary loud
failure: preserve the run directory and report it.

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
  Kimi `-c`/`--continue`, or any other "latest" resume selection
- the child exits non-zero
- `final.txt` is empty
- Claude exits without a final `type=result` event
- Cursor Agent exits without a final `type=result` event
- Grok exits without final text
- Kimi exits without any `role=assistant` text
- a caller requires truly stateless/no-persist Kimi execution
- fresh-resumable Codex does not emit `thread.started`
- fresh-resumable Grok does not emit a final `sessionId`
- fresh-resumable Kimi does not emit a `session.resume_hint` `session_id`
- the child omits the required status footer

Do not silently fall back between Claude, Codex, Cursor Agent, Grok, and Kimi, one
model to another model, one effort level to another, foreground to detached
execution, or shared-worktree execution to a separate worktree.
