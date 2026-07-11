# Model And Invocation

`model-consensus` dispatches each Claude, Codex, Cursor Agent, or Grok
participant directly from the parent agent. It resolves transport independently:
same-host participants use separate clean native children when the active host
can satisfy the requested model capability; cross-provider or unavailable
exact-model/profile participants use external sessions. It does not create a
new runner script, model alias table, harness, or deterministic controller.
Provider routing is fixed: Codex runs GPT/GBT/OpenAI model ids and Fugu
profiles, Claude Code runs supported Claude models, Cursor Agent runs Composer
2.5 Fast, and Grok CLI runs Grok models.

## Resolve Transport Per Participant

Apply `../../_shared/agent-orchestration-policy.md` before dispatch. Inspect the
active host's native child surface and resolve each participant separately.
Prefer native transport for ordinary same-host participation when the host can
honor the requested capability. Use an external session when a different
provider, load-bearing exact model/profile, lifecycle, isolation, automation,
or structured receipt provides a concrete benefit. These are recognition
examples, not a closed allowlist or approval gate.

Account for the external-process and same-provider Codex cost described in the
owning skill and shared policy when choosing transport and concurrency. It is a
tradeoff, not a prohibition or fixed process limit.

For a new Codex-native participant, use a separate child with explicit
`fork_turns: "none"`. A positive count carries bounded recent context and
`"all"` carries full parent context; neither is the independent-first-pass
default. Resume every later round through the participant's exact child handle.
Do not claim a native model override unless the current tool schema confirms
it.

In Claude Code, start each native participant as a separate clean named or
custom subagent and resume its exact handle on later rounds. An explicit
conversation fork carries full parent context and is not an independent first
pass. A skill declared with `context: fork` runs in an isolated clean subagent
context and is not shorthand for full conversation inheritance. A background
agent is appropriate only for a real lifecycle need. A team is not the default:
the parent relays participant outputs unless direct peer communication was
genuinely requested.

Context is separate from permission and workspace isolation. Participants are
read-only; use enforced read-only capability when available, a no-edit/no-write
prompt, and a parent-owned status or diff check. The parent owns fanout and
integration. Participant prompts prohibit nested fanout unless a bounded scope
and concurrency budget are explicit.

## Required Participant Values

Each participant needs a requested identity and role:

- `runtime`: `claude`, `codex`, `agent`, or `grok`
- `model`: runnable model id, Codex profile name, or exact model phrase. An
  omitted model on a Codex lane resolves to `gpt-5.6-sol`.
- `effort`: `low`, `medium`, `high`, `xhigh`, or `max` when supported by the
  selected runtime/model
- `role`: `collaborator` or `adversary`
- `transport`: active-host native child or external runtime session, chosen
  after inspecting whether native model capability suffices
- `starting context`: clean for the independent first pass
- `continuation`: the exact child/session handle after launch

If any load-bearing participant choice is missing or ambiguous after applying
the Codex model default, ask one consolidated question. Explain that only
participants resolved to the external lane create external model sessions:

```text
Before I run model-consensus, I need the two participant choices. Please give
provider/effort for Model A and Model B, plus a model/profile for non-Codex
participants, and say whether either should be adversarial. Codex defaults to
gpt-5.6-sol when its model is omitted. I will use native children where the
active host can honor the requested capability and external sessions for the
remaining participants; external sessions spend separate model budget. Cursor
Agent is Composer-only; Grok defaults to grok-build unless you name Grok
Composer.
```

## Model Phrase Resolution

Follow the shared model-resolution doctrine:

- Accept `sol`, `luna`, and `terra` as the Codex 5.6 choices. They resolve to
  `gpt-5.6-sol`, `gpt-5.6-luna`, and `gpt-5.6-terra`; compact forms such as
  `GPT56LUNAXI` and `GPT56TERRAXI` preserve the named variant and imply
  `xhigh`. If a Codex lane names no model or profile, resolve it to
  `gpt-5.6-sol` and report that the model came from the default.
- Preserve family and numeric version exactly. `gpt-5.6-luna` may normalize to
  `gpt-5.6-luna`; it must not become `gpt-5.6-sol`, `gpt-5.4`, or `gpt-5.5`. `fable 5` may normalize to
  `claude-fable-5`, and `opus 4.7` may normalize to `claude-opus-4-7`;
  neither may become another Claude family or version.
- If the user says `gpt 5.4`, `gpt 5.5`, or a variant of either while choosing
  a model, do not execute it. Say that the old model is blocked and ask whether
  they meant `gpt-5.6-sol`. This is an intent check, not an alias rule: do not
  rewrite the version yourself.
- Infer runtime only from unambiguous family evidence: `gpt`/`gbt`/`fugu`/
  `fugu-ultra`/`codex`/`sol`/`luna`/`terra` implies Codex; `claude fable`, `fable`,
  `claude opus`, or `opus` implies Claude; `agent`, `cursor`, `cursor agent`,
  or `cursor-agent` implies Cursor Agent only for Composer.
  `grok`, `grok-build`, `grok build`, or `grok composer` implies Grok.
  If a phrase mixes Cursor Agent with GPT/GBT model ids, Fugu profiles, or
  Claude, fail loud instead of choosing a side. If a phrase mixes Grok with
  GPT/GBT model ids, Fugu profiles, Claude, or Cursor Agent, fail loud instead
  of choosing a side.
- For ordinary Codex model ids, inspect `codex debug models` when model
  availability matters and choose an available id with the same family and
  exact version. For Fugu, resolve `fugu` and `fugu-ultra` as Codex profiles,
  not model-list ids; preserve the profile names exactly and launch them with
  `-p`.
- For Claude, preserve the named supported Claude family and version. Fable 5
  resolves to `claude-fable-5`; Opus 4.7 resolves to `claude-opus-4-7`. If the
  user names Sonnet or Haiku, fail loud and ask for a supported Claude choice.
- For Cursor Agent, always use `composer-2.5-fast`. Accept `composer`,
  `composer 2.5`, `composer-2.5`, `composer-2.5-fast`, or bare `2.5` in a
  Cursor Agent context as that runnable id. Do not use Cursor model discovery
  for non-Composer routing, and do not pass GPT/GBT model ids, Fugu profiles,
  or Claude model ids to Cursor Agent.
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
`../../_shared/model_resolution.py`. Do not add another model shorthand file
to this skill.

Always announce the mapping before execution:

```text
Model A: "Claude Fable 5 high" -> runtime=claude, model=claude-fable-5, effort=high
Model B: "Claude Opus 4.7 xhigh" -> runtime=claude, model=claude-opus-4-7, effort=xhigh
Model C: "codex high" -> runtime=codex, model=gpt-5.6-sol, effort=high, model_source=default
Model D: "luna xhigh" -> runtime=codex, model=gpt-5.6-luna, effort=xhigh
Model E: "terra high" -> runtime=codex, model=gpt-5.6-terra, effort=high
Model F: "Fugu Ultra xhigh" -> runtime=codex, model=fugu-ultra, codex_profile=fugu-ultra, effort=xhigh
Model G: "Grok Build high" -> runtime=grok, model=grok-build, effort=high
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

Record each participant's requested identity, resolved transport, explicit
starting-context mechanism, and exact native child or external session handle
in the run index. Native tool returns may be copied into the same round-final
artifacts; external event streams and stderr remain separate receipts.

## Native Participant Turns

Start both first-pass participants clean and independently. On Codex, dispatch
each native participant with `fork_turns: "none"`; on Claude Code, use separate
clean named/custom subagents. Other hosts should use their equivalent explicit
clean-child mechanism. Do not use bounded or full parent context merely because
it is convenient.

After both first passes finish, send critique, revision, and signoff prompts to
the exact participant handle that owns that position. Never select a latest
child, route a follow-up to the other participant, or replace a participant
silently. Store each returned final in the corresponding round artifact.

Parent relay remains the default. Do not create a team for ordinary consensus
rounds. Participant prompts are read-only and prohibit child-created fanout
unless an explicit bounded scope and budget says otherwise.

## External Codex: First Turn

Use a resumable Codex session for each participant. Do not pass `--ephemeral`
for participants because the dialogue needs `codex exec resume`.

```bash
codex exec \
  --cd "<work_root>" \
  --disable codex_hooks \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  <codex_model_or_profile_flags> \
  --json \
  -o "$RUN_DIR/round-01/model-a-final.md" \
  < "$RUN_DIR/round-01/model-a-prompt.md" \
  > "$RUN_DIR/round-01/model-a-events.jsonl" \
  2> "$RUN_DIR/round-01/model-a-stderr.log"
```

Read the `thread.started` event from `events.jsonl` and keep its `thread_id`.
Codex streams JSONL events on stdout and writes the final assistant message to
the path passed with `-o`.

Set `<codex_model_or_profile_flags>` this way:

- Ordinary Codex model id: `--model "<resolved_model>" -c model_reasoning_effort='"<resolved_effort>"'`
- Fugu profile at its default effort: `-p "<resolved_codex_profile>"`
- Fugu Ultra explicit non-default effort: `-p "fugu-ultra" -c model_reasoning_effort='"<resolved_effort>"'`

## External Codex: Resume Turn

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

## External Claude: First Turn

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

## External Claude: Resume Turn

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

## External Cursor Agent: First Turn

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

## External Cursor Agent: Resume Turn

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

## External Grok: First Turn

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

## External Grok: Resume Turn

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

Choose foreground or background intentionally for each participant:

- Foreground native or external execution is better for short prompts because
  the parent does not need a polling loop.
- For same-host work that must outlive the foreground turn, use a native
  background child only when the host supports it and the lifecycle benefit is
  real. For long external rounds, background shell execution may be useful,
  but only with full event streams and exact session receipts preserved.
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

Failure is explicit: unavailable native capability needed by the requested
participant, missing external CLI, unresolved exact model, child non-zero exit,
empty final result after process exit, missing terminal result event, or a
participant refusing the prompt contract. If native capability is unavailable,
select the external lane deliberately rather than pretending the native child
honors it. Do not silently switch providers, downgrade models, reduce effort,
or replace a long-running participant with the parent agent's own answer.
