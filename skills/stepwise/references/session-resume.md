# Session resume mechanics

Verified against Claude Code CLI 2.1.119 and Codex CLI 0.124.0-alpha.3. When
either CLI version drifts, re-run the verification block at the bottom of this
file before trusting any invocation here.

## Why sessions matter for this skill

A step runs in a fresh subprocess. The critic inspects the output and either
passes or fails it. On fail, we need to resume **the same step session** with
the critic's findings — never spawn a new session, never redo the work in the
orchestrator. Claude and Codex expose different session handles; this reference
is the single place the exact mechanics live.

## Runtime behavior contract

- Step sub-sessions are resumable. Do not pass `--ephemeral` (Codex) or
  `--no-session-persistence` (Claude) to them.
- Critic sub-sessions are stateless. Pass `--ephemeral` (Codex) or rely on
  fresh process (Claude) — we never resume a critic.
- Both runtimes run with dangerous/skip-permissions/no-sandbox. This is a
  user-set constraint on this skill. Read-only discipline for the critic is
  enforced in the critic prompt, not with a sandbox flag.

## Claude — step session (resumable)

```
claude \
  -p \
  --output-format json \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model <resolved_step_model> \
  --effort <resolved_step_effort> \
  <step_prompt>
```

Claude's stdout has two observed top-level shapes depending on whether the
turn used tools:

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
  --output-format json \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model <resolved_step_model> \
  --effort <resolved_step_effort> \
  -r <session_id> \
  <resume_prompt>
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
  --output-format json \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model <resolved_critic_model> \
  --effort <resolved_critic_effort> \
  --json-schema '<StepVerdict schema>' \
  <critic_prompt>
```

The critic's structured output is returned at `.structured_output` on the
result event. When the critic uses tools to verify artifacts (the common
case), Claude's top-level shape is the event-stream array rather than a
single dict — walk the array for `type=result` and read `.structured_output`
from it. `scripts/run_stepwise.py` handles both shapes via
`_extract_verdict_from_final(final)`; do not reimplement the walk at
new callsites. The schema is passed as a JSON string argument (no file
reference). `.result` carries a short text summary; `.structured_output`
on the result event is the authoritative verdict.

## Codex — step session (resumable)

```
codex exec \
  --cd <target_repo> \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --model <resolved_step_model> \
  -c model_reasoning_effort='"<resolved_step_effort>"' \
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
  <resume_prompt>
```

`codex exec resume` does not accept `--cd` — the session carries the cwd from
its original invocation. It keeps `--model` optional; omit it to reuse the
session's model, or pass it if you want to force a specific model on resume.

## Codex — critic (stateless, structured)

```
codex exec \
  --cd <target_repo> \
  --ephemeral \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --model <resolved_critic_model> \
  -c model_reasoning_effort='"<resolved_critic_effort>"' \
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
StepVerdict semantically so `resume_hint`, `route_to_step_n`, and
`abstain_reason` still behave as optional concepts.

## Notes on flag drift

- Claude's `--effort` accepts: `low`, `medium`, `high`, `xhigh`, `max`.
- Claude's `--permission-mode` is separate from `--dangerously-skip-permissions`;
  do not set both.
- Codex uses `-c model_reasoning_effort='"<level>"'` — note the TOML-quoted
  string inside a shell-quoted argument. The inner double quotes are required.
- Codex 0.124 rejects old schema files where properties such as `resume_hint`
  exist in `properties` but not in `required`. This is recoverable
  orchestration drift: normalize the schema and retry, do not halt the whole
  run if the schema semantics are clear.
- `--output-format json` on Claude and `--json` on Codex are unrelated flags
  with similar purpose: Claude returns one JSON object at end, Codex streams
  JSONL events. Treat them differently in the parser.

## Verification block

Run these six invocations against a fresh temp directory to confirm behavior
before shipping changes to this skill. Substitute any cheap available models;
behavior does not depend on model choice.

```
# 1 Claude step
claude -p --output-format json --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' --model haiku \
  "Say PING." | jq '.session_id,.result'

# 2 Claude resume (reuse id from step 1; must run from same cwd as step 1)
claude -p --output-format json --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' --model haiku -r <ID> \
  "Say PONG." | jq '.session_id,.result'

# 3 Claude critic
claude -p --output-format json --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' --model haiku \
  --json-schema '{"type":"object","additionalProperties":false,"required":["verdict"],"properties":{"verdict":{"enum":["pass","fail"]}}}' \
  "Return verdict pass." | jq '.structured_output'

# 4 Codex step
codex exec --cd /tmp/smoke --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check --model gpt-5.4 -c model_reasoning_effort='"low"' \
  --json -o /tmp/smoke/step.txt "Say PING." < /dev/null

# 5 Codex resume (reuse thread_id from step 4)
codex exec resume <THREAD_ID> --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check --json -o /tmp/smoke/resume.txt "Say PONG." < /dev/null

# 6 Codex critic (schema file needs additionalProperties:false and every
# property in required)
codex exec --cd /tmp/smoke --ephemeral \
  --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  --model gpt-5.4 -c model_reasoning_effort='"low"' \
  --output-schema /tmp/smoke/schema.json --json -o /tmp/smoke/verdict.json \
  "Return verdict pass." < /dev/null
```

If any of the six fails or emits a different shape than described above,
update this file before editing anything else — other files in the skill
refer back here as the source of truth.
