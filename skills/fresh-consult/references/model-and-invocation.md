# Model And Invocation

This reference separates native review dispatch from the exact external
invocation lane. Apply `../../_shared/agent-orchestration-policy.md` first.
For ordinary same-host review, use the native mechanisms below. Use the CLI
sections only when an external provider, exact model/profile, lifecycle,
isolation, automation, or receipt benefit justifies the added process.

For the external lane, use this reference to resolve what the user meant by
"Claude", "Codex", "Cursor Agent", "Grok", "fable 5 high", "opus high",
"gpt-5.6-sol xhigh", "luna xhigh", "terra high", "GPT56SOLXI", "fugu high",
"fugu-ultra xhigh", "composer-2.5-fast", "grok-build", or similar phrasing,
and to run the selected read-only consult subprocess.

Fresh consult is review/second-opinion work. Provider routing is fixed: Codex
runs GPT/GBT/OpenAI model ids and Fugu profiles, Claude Code runs supported
Claude models, Cursor Agent runs Composer 2.5 Fast, and Grok CLI runs Grok
models. The first turn in a consult line starts clean from disk and the prompt;
bounded same-line follow-ups resume the captured child session by exact session
id.

## Native Review Dispatch

For a new independent Codex consult, create a clean native child with explicit
`fork_turns: "none"`. Do not omit the field. A positive count carries bounded
recent turns and `"all"` carries full parent context; those modes are not fresh
review defaults. Resume a bounded same-line follow-up through that exact child
handle. A new independent gate gets another child with
`fork_turns: "none"`.

In Claude Code, use a clean named or custom subagent for a new consult and
resume that exact subagent for a bounded same-line follow-up. Do not confuse a
clean named subagent with an explicit full-conversation fork. A skill declared
with `context: fork` runs in an isolated clean subagent context and does not
inherit the full conversation. Use a background agent only when work must
outlive the foreground turn. Do not create an agent team for ordinary
parent-mediated review; teams are for genuinely requested direct peer
coordination.

For other hosts, choose the equivalent explicit clean-child and exact-resume
mechanisms. Do not claim a native model override, permission set, worktree, or
background lifetime unless the active tool surface confirms it.

Native children commonly share the parent's workspace. Pair the strongest
available read-only capability with an explicit no-edit/no-write prompt and a
parent-owned status or diff check. The parent owns fanout and synthesis; child
prompts prohibit nested fanout unless a bounded scope and concurrency budget
are explicit.

## Choosing The External Lane

An external session is valid when it provides a concrete benefit the native
child does not. The examples above are recognition aids, not an allowlist or
approval gate. Weigh the external-process and same-provider Codex cost described
in the owning skill and shared policy without turning it into a ban or fixed
process limit.

External fresh turns start clean from disk and the prompt. External resume
turns continue only the exact captured session. Neither context choice implies
read-only enforcement, filesystem isolation, or a separate worktree.

## Required External Values

Every external consult child needs three execution values:

- `runtime` - `claude`, `codex`, `agent`, or `grok`
- `model` - the runnable CLI model identifier, or the Codex profile name for
  Fugu. An omitted model on a Codex lane resolves to `gpt-5.6-sol`.
- `effort` - the reasoning effort level, or `encoded-in-model` for Cursor Agent

If external transport has been selected and a required value is missing or
ambiguous after applying the Codex model default, ask one consolidated
question before invoking. Do not ask for CLI values for an ordinary native
review. For Cursor Agent Composer, effort resolves to `encoded-in-model`; do
not ask for a separate effort level.

```text
I need the fresh consult runtime, effort, and non-Codex model/profile when
applicable before invoking an external model. The consult runs as a clean
subprocess and can spend real model budget. What should I use?
```

Add only the missing facts to the question when some values are already known.

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
- `grok`, `grok build`, `grok-build`, `grok composer`, or
  `grok-composer-2.5-fast` implies `runtime=grok`.
- Bare `composer`, `composer 2.5`, or bare `2.5` is ambiguous unless the user
  explicitly names Cursor Agent or Grok in the same execution choice.
- If a phrase mixes Cursor Agent with GPT/GBT model ids, Fugu profiles, or
  Claude, fail loud instead of choosing a side. Never run GPT/GBT model ids,
  Fugu profiles, or Claude models through Cursor Agent.
- If a phrase mixes Grok with GPT/GBT model ids, Fugu profiles, Claude, or
  Cursor Agent, fail loud instead of choosing a side.
- If the user names only an effort level, such as "xhigh", ask for runtime.
  If the answer is Codex and still omits a model, use `gpt-5.6-sol`.
- If the user says only "run a fresh consult" or "get a second opinion", use a
  clean native child of the active host when it can satisfy the role. Ask for
  runtime/effort and a non-Codex model/profile only after an external lane is
  selected and those values are load-bearing.

The Codex default is deliberately narrow: when the lane is Codex and no model
or profile is named, use `gpt-5.6-sol`. Do not default the runtime itself, and
do not invent defaults for Claude, Cursor Agent, Grok, or Fugu profiles.

## Model Phrase Resolution

Treat model text as intent, not a loose alias:

- Accept `sol`, `luna`, and `terra` as the Codex 5.6 choices. They resolve to
  `gpt-5.6-sol`, `gpt-5.6-luna`, and `gpt-5.6-terra`; compact forms such as
  `GPT56LUNAXI` and `GPT56TERRAXI` preserve the named variant and imply
  `xhigh`. If a Codex lane names no model or profile, resolve it to
  `gpt-5.6-sol` and report that the model came from the default.
- Preserve model family and numeric version exactly. `gpt-5.6-terra` may normalize to
  `gpt-5.6-terra`; it must not become `gpt-5.6-sol`, `gpt-5.4`, or `gpt-5.5`. `fable 5` may normalize to
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
- For Grok, use `grok-build` by default when the user says `grok`,
  `grok cli`, `grok build`, or `grok-build`. Use
  `grok-composer-2.5-fast` only when the user names Grok Composer, such as
  `grok composer`, `grok composer 2.5`, or `grok-composer-2.5-fast`. Inspect
  `grok models` when availability matters, and do not pass GPT/GBT model ids,
  Fugu profiles, Claude, or Cursor Agent model ids to Grok.
- Do not run paid trial prompts to discover whether a Claude model exists. Use
  the CLI help/config surface when available; otherwise ask.

Always announce the raw-to-resolved mapping before execution:

```text
Claude Fable 5 high -> runtime=claude, model=claude-fable-5, effort=high
Claude Opus 4.7 xhigh -> runtime=claude, model=claude-opus-4-7, effort=xhigh
Codex high -> runtime=codex, model=gpt-5.6-sol, effort=high, model_source=default
Luna xhigh -> runtime=codex, model=gpt-5.6-luna, effort=xhigh
Terra high -> runtime=codex, model=gpt-5.6-terra, effort=high
Fugu Ultra xhigh -> runtime=codex, model=fugu-ultra, codex_profile=fugu-ultra, effort=xhigh
Cursor Agent composer 2.5 -> runtime=agent, model=composer-2.5-fast, effort=encoded-in-model
Grok Build high -> runtime=grok, model=grok-build, effort=high
```

For deterministic script plumbing that needs the same rules, use
`../../_shared/model_resolution.py` instead of creating a local model alias
table. The helper exists to keep fresh-consult, agent-delegate,
model-consensus, Stepwise-style orchestrators, and arch-epic automatic
harnesses aligned on exact-version preservation and fail-loud behavior.

For Fable consult children, keep the prompt direct: state the goal, hard
constraints, evidence expectations, and done-ness clearly. Do not ask the child
to show private reasoning or turn the consult into a rigid step script; keep the
visible output contract to verdict, evidence, session metadata, and directories.

## Effort Resolution

- Claude accepts `low`, `medium`, `high`, `xhigh`, and `max` via `--effort`.
- For ordinary Codex model ids, pass effort as
  `-c model_reasoning_effort='"<level>"'`.
- For Fugu profiles, use `-p fugu` or `-p fugu-ultra`. Omit `-c` when using
  the profile default (`fugu` defaults to `high`; `fugu-ultra` defaults to
  `xhigh`). Add `-c model_reasoning_effort='"<level>"'` only when the user
  explicitly requests a supported non-default Fugu Ultra effort.
- Grok accepts `low`, `medium`, `high`, `xhigh`, and `max` via `--effort`.
- Cursor Agent does not expose a separate `--effort` flag in the local CLI.
  Store effort as `encoded-in-model` and pass only
  `--model "composer-2.5-fast"`.
- For ordinary Codex model ids, confirm the selected model supports the
  requested effort when `codex debug models` is needed for model resolution.
  `codex debug models` does not prove whether local Fugu profiles exist.
- If effort is missing for Claude, Codex, or Grok, or the selected model does
  not support the requested effort, ask.

## Transport-Neutral Consult Continuity

Apply the lifecycle before mapping it to native or external mechanics:

- `new-clean` - a new native child or fresh external session for the first
  request or any independent gate.
- `exact-resume` - the exact native child or external session continues a
  bounded same-line follow-up.
- `clean-rotation` - a new clean reviewer replaces a three-turn line unless
  the user explicitly asks to continue it.

The external receipt modes are:

- `fresh-resumable` - default first request in a consult line. It starts clean,
  captures a session id, and writes chain metadata.
- `resume` - default for the second and third same-line requests when a healthy
  unambiguous prior chain exists. Strict pass/fail review does not change this
  default.
- `fresh-forced` - a clean-start chain because the user asked for cold,
  independent, or fresh-eyes review, or because execution choices changed.
- `fresh-rotated` - a clean-start chain because the prior same-line chain
  reached the default turn cap.

Treat a request as the same consult line when the parent can defend all of
these:

- same work root
- same participant identity and transport; for an external participant, the
  same runtime, model, and effort
- same main artifact, claim, flow, or target question family
- the user asks a follow-up, clarification, rerun after local edits, or narrowed
  check that depends on the previous consult
- the prior native child handle remains valid, or the external chain has a
  valid exact session id, and the consult line is below `max_chain_turns`

Start fresh instead when:

- the user asks for cold, independent, fresh-eyes, or clean-room review
- participant identity, transport, required capability, or work root changed
- the new artifact or question is materially different
- multiple possible prior children or chains match and the user did not provide
  an exact handle or run path
- the prior native handle is unavailable, or external `session_id.txt` is
  missing, empty, or `UNRECOVERABLE`
- the prior output was malformed or lacks the verdict footer
- the same-line chain has already reached three turns

Do not start fresh solely because the consult is strict, adversarial, or acting
as a completion arbiter. Strictness controls the acceptance bar; continuity
controls whether the same child session should inspect the follow-up.

If the only problem is ambiguity between candidate reviewers, ask one concise
question naming their exact handles or external chain directories. Do not
silently choose the newest child or chain, use runtime "continue latest"
features, or call `agent ls` or similar latest-session discovery. Resume only
the exact participant already tied to the same fresh-consult line.

For explicit parallel consults, the parent resolves transport independently and
creates one clean participant per question. External participants each get
their own chain under the group directory. Resume a participant only when the
follow-up identifies its exact native handle, external chain/run directory, or
question. Otherwise start clean or ask.

## External Chain And Turn Directories

Use one chain directory per consult line:

```bash
CONSULT_SLUG="<short-slug>"
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
CHAIN_DIR="$(mktemp -d "/tmp/fresh-consult/${CONSULT_SLUG}-${RUN_TS}-XXXXXX")"
CHAIN_PATH="$CHAIN_DIR/chain.json"
TURN_DIR="$CHAIN_DIR/turn-01"
mkdir -p "$TURN_DIR"
PROMPT_PATH="$TURN_DIR/prompt.md"
FINAL_PATH="$TURN_DIR/final.txt"
EVENTS_PATH="$TURN_DIR/events.jsonl"
STDERR_PATH="$TURN_DIR/stderr.log"
EXECUTION_PATH="$TURN_DIR/execution.json"
SESSION_PATH="$TURN_DIR/session_id.txt"
RESUME_FROM_PATH="$TURN_DIR/resume_from.txt"
```

Resume turns still get a new turn directory:

```bash
TURN_DIR="$CHAIN_DIR/turn-02"
mkdir -p "$TURN_DIR"
PROMPT_PATH="$TURN_DIR/prompt.md"
FINAL_PATH="$TURN_DIR/final.txt"
EVENTS_PATH="$TURN_DIR/events.jsonl"
STDERR_PATH="$TURN_DIR/stderr.log"
EXECUTION_PATH="$TURN_DIR/execution.json"
SESSION_PATH="$TURN_DIR/session_id.txt"
RESUME_FROM_PATH="$TURN_DIR/resume_from.txt"
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
  "schema_version": 1,
  "mode": "fresh-resumable | resume | fresh-forced | fresh-rotated",
  "runtime": "claude | codex | agent | grok",
  "model": "<resolved model or reused-from-session>",
  "effort": "<resolved effort or reused-from-session>",
  "work_root": "<absolute path>",
  "chain_dir": "<absolute path>",
  "turn": 2,
  "resume_from": "<prior turn run dir, explicit session id, or none>",
  "restart_reason": "none | user_forced_cold | chain_turn_limit | changed_execution | missing_session | ambiguous_chain"
}
```

For fresh-resumable, fresh-forced, fresh-rotated, and resume turns, write the
captured, reused, or replacement session id to `session_id.txt`. For resume
turns, write the source run directory or explicit session id to
`resume_from.txt`.

Maintain `chain.json` with enough metadata to make the next same-line decision
defensible:

```json
{
  "schema_version": 1,
  "skill": "fresh-consult",
  "chain_id": "<stable id>",
  "consult_slug": "<short slug>",
  "created_at_utc": "2026-06-05T00:00:00Z",
  "updated_at_utc": "2026-06-05T00:00:00Z",
  "work_root": "<absolute path>",
  "runtime": "claude | codex | agent | grok",
  "model": "<resolved model>",
  "effort": "<resolved effort or encoded-in-model>",
  "max_chain_turns": 3,
  "user_named_artifacts": ["<path or artifact>"],
  "artifact_fingerprint": "<hash of normalized artifact list>",
  "consult_objective": "<one-line objective>",
  "turns": [
    {
      "turn": 1,
      "mode": "fresh-resumable",
      "run_dir": "<absolute path>",
      "session_id_path": "<absolute path>",
      "session_id": "<captured id or UNRECOVERABLE>",
      "verdict": "pass | fail | malformed",
      "created_at_utc": "2026-06-05T00:00:00Z"
    }
  ]
}
```

Do not put secrets, pasted credentials, or raw full prompts in `chain.json`.
The prompt body stays in `prompt.md`.

## External Parallel Consult Group

Use the external parallel group path only when the user asks for parallel
consults or gives multiple consult questions and the parent has selected
external transport for those participants. Parallel consults are still
ordinary reviewers; the group only gives the parent a place to organize
chains, prompts, streams, finals, and the combined report. The parent owns the
fanout and children do not create further children unless an explicit nested
scope and budget says otherwise.

Create one group directory:

```bash
GROUP_SLUG="<short-slug>"
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
GROUP_DIR="$(mktemp -d "/tmp/fresh-consult/parallel-${GROUP_SLUG}-${RUN_TS}-XXXXXX")"
```

For each child, create a child chain beneath the group:

```bash
CHILD_SLUG="<child-slug>"
CHAIN_DIR="$GROUP_DIR/$CHILD_SLUG"
TURN_DIR="$CHAIN_DIR/turn-01"
mkdir -p "$TURN_DIR"
CHAIN_PATH="$CHAIN_DIR/chain.json"
PROMPT_PATH="$TURN_DIR/prompt.md"
FINAL_PATH="$TURN_DIR/final.txt"
EVENTS_PATH="$TURN_DIR/events.jsonl"
STDERR_PATH="$TURN_DIR/stderr.log"
EXECUTION_PATH="$TURN_DIR/execution.json"
SESSION_PATH="$TURN_DIR/session_id.txt"
```

Launch each child with the same Codex, Claude, Cursor Agent, or Grok command
shape below, using that child's paths. Record the shell PID and exit status in
the child directory if the host shell makes that convenient, but do not
introduce a script, controller, detached monitor, or state machine.

Default to one shared runtime/model/effort for all children. If the user clearly
assigns different execution choices to different children, apply those choices
exactly and announce the mapping before launch. If any child lacks a consult
question, work root, runtime, model, or effort, ask one consolidated question
before launching the group.

Wait for all children before reporting. If one child fails or returns malformed
output, preserve its chain and run directory and include that failure in the
group report; do not discard the successful sibling consults.

## External Codex Fresh Resumable

Use this shape for `fresh-resumable`, `fresh-forced`, and `fresh-rotated`
Codex consult turns:

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

Read the first `thread.started` event from `events.jsonl` and write its
`thread_id` to `session_id.txt`. If no thread id is captured, write
`UNRECOVERABLE` to `session_id.txt`, mark the turn malformed, and preserve the
turn directory.

Flag meanings:

- `--disable codex_hooks` isolates the consult from any local Codex hooks
  outside this package.
- `-C <work_root>` pins the filesystem context for fresh-start turns.
- `--dangerously-bypass-approvals-and-sandbox` gives the child realistic local
  access. Use only in trusted local environments.
- `--skip-git-repo-check` allows doc or artifact consults outside a git root.
- `--json` streams Codex event JSONL to `events.jsonl` while the child works.
- `-o "$FINAL_PATH"` captures the final assistant message.

Set `<codex_model_or_profile_flags>` this way:

- Ordinary Codex model id: `--model "<resolved_model>" -c model_reasoning_effort='"<resolved_effort>"'`
- Fugu profile at its default effort: `-p "<resolved_codex_profile>"`
- Fugu Ultra explicit non-default effort: `-p "fugu-ultra" -c model_reasoning_effort='"<resolved_effort>"'`

## External Codex Resume

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
Do not pass `-C` or `--cd` on resume. Do not use `--last`.

Auto-resume requires the same runtime, model, and effort as the original chain,
so omit model and effort flags on resume unless the user explicitly requests a
different execution choice and accepts that the report will call it out.

## External Claude Fresh Resumable

Use this shape for `fresh-resumable`, `fresh-forced`, and `fresh-rotated`
Claude consult turns:

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

Run Claude from `work_root`. Do not pass `--no-session-persistence`; the
session id is needed for bounded follow-up reuse.

After Claude exits, read the final `type=result` event from `events.jsonl` and
write its `result` text to `final.txt` before applying the verdict-footer
checks. Write the final result event's `session_id` to `session_id.txt`. If no
result event exists after a zero exit, or no session id is captured, treat the
turn as malformed and preserve the turn directory.

`--verbose` is required by the Claude CLI when `stream-json` output is used. Do
not omit it from fresh or resumed Claude consult commands.

## External Claude Resume

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

## External Cursor Agent Fresh Resumable

Use this shape for `fresh-resumable`, `fresh-forced`, and `fresh-rotated`
Cursor Agent consult turns. Cursor Agent has no `--verbose` flag; that flag is
Claude-only. `<resolved_agent_model>` must be `composer-2.5-fast`.

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
`events.jsonl` and write its `result` text to `final.txt`. Write the final
result event's `session_id` to `session_id.txt`. If no result event exists
after a zero exit, or no session id is captured, treat the turn as malformed
and preserve the turn directory.

## External Cursor Agent Resume

Use this shape to resume an explicit Cursor Agent session. Cursor Agent has no
`--verbose` flag; that flag is Claude-only. `<resolved_agent_model>` must be
`composer-2.5-fast`.

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
shared-worktree consult skill unless a future user explicitly asks for a
worktree-based variant.

After Cursor Agent exits, write the final `result` text to `final.txt`. Write
the returned `session_id` to `session_id.txt` when present; otherwise preserve
the input session id in `session_id.txt`.

## External Grok Fresh Resumable

Use this shape for `fresh-resumable`, `fresh-forced`, and `fresh-rotated` Grok
consult turns:

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
`final.txt`. Write the final `type=end` event's `sessionId` to
`session_id.txt`. If no final text exists after a zero exit, or no `sessionId`
is captured, treat the turn as malformed and preserve the turn directory.

## External Grok Resume

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

## External Monitoring Posture

Consults are not instant. A normal repo-backed consult commonly takes 5+
minutes. Broad artifact reads, `xhigh`, or `max` can reasonably take 20-40
minutes.

Poll on a minutes-scale cadence. Check `events.jsonl`, `stderr.log`, and
process liveness every few minutes; do not poll every few seconds. A missing
`final.txt` before the process exits is not a failure when the event stream is
still alive. Investigate only after the process exits non-zero, the stream
shows an error, or there is no stream activity for a long quiet window.

Resume turns still need monitoring and evidence checks. A resumed consult can
use child-session history, but it must re-read files when current repo state is
load-bearing. The resumed child applies the same strict pass/fail bar as a
fresh child.

## Failure Behavior

For native review, fail loud when the host cannot create the requested clean
child, cannot resume the exact participant needed for a same-line follow-up, or
cannot provide a load-bearing requested model/capability. A missing native
capability may justify the external lane; do not pretend the native dispatch
honors it.

For external review, fail loud and preserve the chain and turn directory when:

- the selected CLI is missing
- runtime/model/effort cannot be resolved exactly
- resume mode has no explicit session id, prior run directory, or prior chain
- `session_id.txt` is missing, empty, or `UNRECOVERABLE` for a resume
- the caller asks for cross-runtime resume
- the caller asks for Claude `--continue`, Codex `--last`, Cursor Agent
  `--continue`, `agent resume`, `agent ls`, Grok latest-session selection, or
  any other latest-session resume selection
- the child exits non-zero
- `final.txt` is empty
- Claude exits without a final `type=result` event
- Cursor Agent exits without a final `type=result` event
- Grok exits without final text
- the child omits the required verdict footer

When the prior same-line chain is already at three turns, start a new
`fresh-rotated` chain instead of failing.

Do not silently fall back between Claude, Codex, Cursor Agent, and Grok, one
model to another model, one effort level to another, or one session to another.
