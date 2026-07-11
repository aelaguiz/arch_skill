# Native continuation and external session adapter

Verified against Claude Code CLI 2.1.119, Codex CLI 0.124.0-alpha.3, and Grok
CLI 0.2.22. When a CLI version drifts, re-run the relevant verification block
at the bottom of this file before trusting that invocation.

## Transport ownership

The orchestrator chooses transport under
`../../_shared/agent-orchestration-policy.md`; this file does not. Same-host
workers and critics normally use native children. `run_stepwise.py` and the CLI
forms below are the deterministic external adapter when a concrete provider,
exact model/profile, lifecycle, isolation, automation, structured receipt, or
another deliberate benefit warrants an external process.

## Native context and continuation

- Initial workers and every independent critic start clean. In Codex native
  dispatch always set `fork_turns: "none"`; use a positive count only for
  bounded chat-only context and `"all"` only for a genuinely full-conversation
  dependency. In Claude, use a clean named subagent. An explicit conversation
  fork carries full conversation; a skill with `context: fork` instead runs in
  an isolated clean subagent context.
- Diagnostic and repair turns resume the exact worker child through its native
  handle. Never resume a convenient old child for another role. Every critic
  rejudgement is another new clean child.
- Context inheritance is separate from permissions, capabilities, filesystem
  sharing, background lifetime, and worktree isolation. Record those choices
  independently in the dispatch receipt.
- The parent owns fanout and integration. Children may not create more agents
  or invoke delegation/consult skills unless the parent assigned a bounded
  nested scope and budget.

## Why external sessions matter

On failure, Stepwise may resume an external worker in two ways: read-only
diagnostic conversation, then operational repair after root cause is located.
Claude, Codex, and Grok expose different external session handles; this
reference is the single place those exact mechanics live.

## External runtime behavior contract

- External worker sessions are resumable. Do not pass `--ephemeral` (Codex) or
  `--no-session-persistence` (Claude) to them.
- External critic sessions are stateless. Pass `--ephemeral` for Codex, rely on
  a new clean process for Claude and Grok, and never resume a critic.
- Diagnostic and repair turns both resume exact external worker sessions.
  Diagnostic turns are read-only by prompt contract and do not consume repair
  bounces. Repair turns are operational and do consume repair bounces.
- External runtimes use the existing dangerous/skip-permissions/no-sandbox
  convention. This does not define native child permissions. Read-only
  discipline for every critic remains in the prompt, is enforced by capability
  when available, and is checked by the parent against repository state.

## Claude — step session (resumable)

```
claude \
  -p \
  --output-format stream-json \
  --verbose \
  --include-partial-messages \
  --include-hook-events \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model <resolved_step_model> \
  --effort <resolved_step_effort> \
  <step_prompt>
```

Claude's stdout is JSONL when `stream-json` is active. The final answer is the
last parseable `type=result` event in the combined stream. Older
`--output-format json` runs had two observed top-level shapes depending on
whether the turn used tools, and the parser still accepts both:

- **Single result object** (no tool use). Session id at `.session_id`:

  ```json
  {"type":"result","subtype":"success","result":"PING",
   "session_id":"5f303873-ac01-44a6-903a-3a62e3a699f0", ...}
  ```

- **Event-stream array** (tool use occurred, or `--json-schema` is set).
  The result event is one entry with `type=result`. Session id lives on
  that event, not at the top level:

  ```json
  [{"type":"system",...},
   {"type":"assistant",...},
   {"type":"user","message":{"content":[{"type":"tool_result",...}]}},
   {"type":"result","session_id":"5f303873-...","structured_output":{...}, ...}]
  ```

`scripts/run_stepwise.py`'s `_extract_claude_result_event(payload)` is the
canonical shape-normalizer: pass either a dict or a list, get back the
result event dict (or None if absent). Use it at every parse boundary —
never `payload.get(...)` directly on stdout JSON.

## Claude — step resume

```
claude \
  -p \
  --output-format stream-json \
  --verbose \
  --include-partial-messages \
  --include-hook-events \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model <resolved_step_model> \
  --effort <resolved_step_effort> \
  -r <session_id> \
  <diagnostic_or_repair_prompt>
```

The returned `.session_id` equals the resumed id (verified). Use `-r`, never
`--continue`: `--continue` picks the most-recent-in-cwd, which can collide with
other work in the same directory.

**Important:** Claude persists sessions per-cwd. Resume must run in the same
working directory as the original step. If the step spawned with cwd
`<target_repo>`, the resume also runs with cwd `<target_repo>`. Running
`claude -r <id>` from a different directory errors with "No conversation
found with session ID". The script sets subprocess cwd accordingly; any
hand-crafted invocation must do the same.

## Claude — critic (stateless, structured)

```
claude \
  -p \
  --output-format stream-json \
  --verbose \
  --include-partial-messages \
  --include-hook-events \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model <resolved_critic_model> \
  --effort <resolved_critic_effort> \
  --json-schema '<StepVerdict schema>' \
  <critic_prompt>
```

The critic's structured output is returned at `.structured_output` on the
final `type=result` event. With `stream-json`, that result event is read as
the last parseable result event in `stream.log`; older `--output-format json`
runs may have emitted a dict or event-stream array. `scripts/run_stepwise.py`
handles all accepted shapes via `_extract_verdict_from_final(final)`; do not
reimplement the walk at new callsites. The schema is passed as a JSON string
argument (no file reference). `.result` carries a short text summary;
`.structured_output` on the result event is the authoritative verdict.

## Codex — step session (resumable)

```
codex exec \
  --cd <target_repo> \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  <codex_model_or_profile_flags> \
  --json \
  -o <final_message_file> \
  <step_prompt>
```

Session id arrives as `thread_id` in the first JSONL event on stdout:

```json
{"type":"thread.started","thread_id":"019db801-7807-7f82-a2a1-1740a9fa4b6b"}
```

Capture `thread_id` from that event. The final assistant message is written to
the file named by `-o`. Full event stream is on stdout (one JSONL event per
line) — keep it as the transcript.

Codex prints `Reading additional input from stdin...` to stderr on start.
That is cosmetic; the process completes on stdin EOF. Close stdin explicitly
(`< /dev/null`) in orchestration to make behavior deterministic.

Do not pass `--ephemeral`. Ephemeral sessions are not resumable.

## Codex — step resume

```
codex exec resume <thread_id> \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --json \
  -o <final_message_file> \
  <diagnostic_or_repair_prompt>
```

`codex exec resume` does not accept `--cd` — the session carries the cwd from
its original invocation. Omit model/profile and effort flags on ordinary
resumes so Codex reuses the session's original execution choice.

## Codex — critic (stateless, structured)

```
codex exec \
  --cd <target_repo> \
  --ephemeral \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  <codex_model_or_profile_flags> \
  --output-schema <schema_file> \
  --json \
  -o <verdict_json_file> \
  <critic_prompt>
```

The structured verdict is written verbatim to the file named by `-o`. No
wrapper. Codex's `--output-schema` requires `"additionalProperties": false` at
every object level and requires every object property to be listed in
`required`. Semantically optional fields must therefore be
required-but-nullable. `scripts/run_stepwise.py` writes a normalized
`critic/schema.codex.json` before invoking Codex, then validates the returned
observational StepVerdict semantically.

Set `<codex_model_or_profile_flags>` this way:

- Ordinary Codex model id: `--model <resolved_model> -c model_reasoning_effort='"<resolved_effort>"'`
- Fugu profile at its default effort: `-p <resolved_codex_profile>`
- Fugu Ultra explicit non-default effort: `-p fugu-ultra -c model_reasoning_effort='"<resolved_effort>"'`

## Grok — step session (resumable)

```
RUST_LOG=off grok \
  --cwd <target_repo> \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model <resolved_step_model> \
  --effort <resolved_step_effort> \
  --output-format streaming-json \
  --prompt-file <step_prompt_file>
```

Grok stdout is JSONL when `streaming-json` is active. Concatenate `type=text`
event `data` chunks for the final answer. Capture the final `type=end`
event's `sessionId` for resume.

## Grok — step resume

```
RUST_LOG=off grok \
  --cwd <target_repo> \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model <resolved_step_model> \
  --effort <resolved_step_effort> \
  --output-format streaming-json \
  --resume <session_id> \
  --prompt-file <diagnostic_or_repair_prompt_file>
```

Use `--resume <session_id>` only. Do not use latest-session selection.

## Grok — critic (fresh, post-validated)

```
RUST_LOG=off grok \
  --cwd <target_repo> \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model <resolved_critic_model> \
  --effort <resolved_critic_effort> \
  --output-format streaming-json \
  --prompt-file <critic_prompt_with_schema_file>
```

Grok has no schema-enforcement flag in the local CLI. The script writes a
Grok-specific prompt file that appends the StepVerdict JSON Schema, parses the
final text as JSON, and then runs the same semantic verdict validation.

## Notes on flag drift

- Claude's `--effort` accepts: `low`, `medium`, `high`, `xhigh`, `max`.
- Claude's `--permission-mode` is separate from `--dangerously-skip-permissions`;
  do not set both.
- For ordinary Codex model ids, Codex uses
  `-c model_reasoning_effort='"<level>"'` — note the TOML-quoted string inside
  a shell-quoted argument. The inner double quotes are required.
- For Fugu profiles, use `-p fugu` or `-p fugu-ultra`. Omit `-c` at the
  profile default (`fugu=high`, `fugu-ultra=xhigh`); add `-c` only for an
  explicit supported non-default Fugu Ultra effort.
- Codex 0.124 rejects schema files where properties exist in `properties` but
  not in `required`. This is recoverable orchestration drift: normalize the
  schema and retry, do not halt the whole run if the schema semantics are
  clear.
- `--output-format stream-json` on Claude and `--json` on Codex are unrelated
  flags with similar purpose: both preserve live JSONL events, but their event
  shapes differ. Treat them differently in the parser.
- `--verbose` is required by the Claude CLI when `--output-format stream-json`
  is used. Add it to every Claude stream-json step, resume, diagnostic, critic,
  and smoke-test command.
- Grok does not accept `--sandbox disabled`; do not add it. Its default local
  mode is unsandboxed. Use `RUST_LOG=off` to suppress noisy success stderr
  while preserving useful failure errors.
- Grok has no documented hook-suppression flag. Do not invent one.

## Verification block

Run the relevant invocations against a fresh temp directory to confirm behavior
before shipping changes to this skill. Substitute any cheap available models;
behavior does not depend on model choice.

```
# 1 Claude step
claude -p --output-format stream-json --verbose --include-partial-messages \
  --include-hook-events --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' --model haiku \
  "Say PING." | tee /tmp/smoke/claude-step.events.jsonl | tail -n 1 | jq '.session_id,.result'

# 2 Claude resume (reuse id from step 1; must run from same cwd as step 1)
claude -p --output-format stream-json --verbose --include-partial-messages \
  --include-hook-events --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' --model haiku -r <ID> \
  "Say PONG." | tee /tmp/smoke/claude-resume.events.jsonl | tail -n 1 | jq '.session_id,.result'

# 3 Claude critic
claude -p --output-format stream-json --verbose --include-partial-messages \
  --include-hook-events --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' --model haiku \
  --json-schema '{"type":"object","additionalProperties":false,"required":["verdict"],"properties":{"verdict":{"enum":["pass","fail"]}}}' \
  "Return verdict pass." | tee /tmp/smoke/claude-critic.events.jsonl | tail -n 1 | jq '.structured_output'

# 4 Codex step
codex exec --cd /tmp/smoke --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check --model gpt-5.6-sol -c model_reasoning_effort='"low"' \
  --json -o /tmp/smoke/step.txt "Say PING." < /dev/null

# 5 Codex resume (reuse thread_id from step 4)
codex exec resume <THREAD_ID> --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check --json -o /tmp/smoke/resume.txt "Say PONG." < /dev/null

# 6 Codex critic (schema file needs additionalProperties:false and every
# property in required)
codex exec --cd /tmp/smoke --ephemeral \
  --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  --model gpt-5.6-sol -c model_reasoning_effort='"low"' \
  --output-schema /tmp/smoke/schema.json --json -o /tmp/smoke/verdict.json \
  "Return verdict pass." < /dev/null

# 7 Grok step
printf 'Say PING.' > /tmp/smoke/grok-step.prompt
RUST_LOG=off grok --cwd /tmp/smoke --no-auto-update --no-memory \
  --no-subagents --disable-web-search --permission-mode bypassPermissions \
  --always-approve --model grok-build --effort low \
  --output-format streaming-json --prompt-file /tmp/smoke/grok-step.prompt \
  | tee /tmp/smoke/grok-step.events.jsonl

# 8 Grok resume (reuse sessionId from step 7)
printf 'Say PONG.' > /tmp/smoke/grok-resume.prompt
RUST_LOG=off grok --cwd /tmp/smoke --no-auto-update --no-memory \
  --no-subagents --disable-web-search --permission-mode bypassPermissions \
  --always-approve --model grok-build --effort low \
  --output-format streaming-json --resume <SESSION_ID> \
  --prompt-file /tmp/smoke/grok-resume.prompt \
  | tee /tmp/smoke/grok-resume.events.jsonl

# 9 Grok critic (schema is appended to the prompt, then output is parsed)
printf 'Return JSON only: {"verdict":"pass"}' > /tmp/smoke/grok-critic.prompt
RUST_LOG=off grok --cwd /tmp/smoke --no-auto-update --no-memory \
  --no-subagents --disable-web-search --permission-mode bypassPermissions \
  --always-approve --model grok-build --effort low \
  --output-format streaming-json --prompt-file /tmp/smoke/grok-critic.prompt \
  | tee /tmp/smoke/grok-critic.events.jsonl
```

If any of the six fails or emits a different shape than described above,
update this file before editing anything else — other files in the skill
refer back here as the source of truth.
