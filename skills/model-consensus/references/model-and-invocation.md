# Model And Invocation

`model-consensus` dispatches each Claude, Codex, Cursor Agent, Grok, Kimi, or
agy participant directly from the parent agent. It resolves transport
independently: same-host participants use separate clean native children when
the active host can satisfy the requested model capability; cross-provider or
unavailable exact-model/profile participants use external sessions. It does not create a
new runner script, model alias table, harness, or deterministic controller.
Provider routing is fixed: Codex runs GPT/GBT/OpenAI model ids and Fugu
profiles, Claude Code runs supported Claude models, Cursor Agent runs Composer
2.5 Fast, Grok CLI runs Grok models, Kimi Code runs Kimi K3, and the
Antigravity CLI (`agy`) runs Gemini models. An agy participant is the way to
put a Google model in the dialogue.

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
prompt, and a parent-owned status or diff check. The parent owns external
topology and integration. Participant prompts allow each participant's own
native sub-agents and forbid starting external agents.

## Required Participant Values

Each participant needs a requested identity and role:

- `runtime`: `claude`, `codex`, `agent`, `grok`, `kimi`, or `agy`
- `model`: runnable model id, Codex profile name, or exact model phrase. An
  omitted model on a Codex lane resolves to `gpt-6.1-sol`; an omitted model on
  a Kimi lane resolves to `kimi-code/k3`; an omitted model on an agy lane
  resolves to `gemini-4-argon`.
- `effort`: `low`, `medium`, `high`, `xhigh`, `max`, or `ultra` when supported
  by the selected runtime/model; omitted Sol effort resolves to the `xhigh`
  preference default, omitted Kimi effort resolves to the K3 model default,
  `max`, and omitted agy effort resolves to the `high` preference default
- `role`: `collaborator` or `adversary`
- `transport`: active-host native child or external runtime session, chosen
  after inspecting whether native model capability suffices
- `starting context`: clean for the independent first pass
- `continuation`: the exact child/session handle after launch

If any load-bearing participant choice is missing or ambiguous after applying
the Codex, Kimi, and agy defaults, ask one consolidated question. Explain that
only participants resolved to the external lane create external model sessions:

```text
Before I run model-consensus, I need the two participant choices. Please give
provider and any non-default effort for Model A and Model B, plus a
model/profile for participants outside the Codex, Kimi, and agy defaults, and
say whether either should be adversarial. Codex defaults to gpt-6.1-sol at
xhigh when its model and effort are omitted; Kimi defaults to kimi-code/k3 at
max; agy defaults to gemini-4-argon at high. I will use native children where
the active host can honor the requested capability and external sessions for
the remaining participants; external sessions spend separate model budget.
Cursor Agent is Composer-only; natural Grok wording resolves to grok-4.6.
```

## Model Phrase Resolution

Follow the shared model-resolution doctrine:

- Accept `sol`, `astra`, `luna`, and `terra` as Codex choices. They resolve to
  `gpt-6.1-sol`, `gpt-6-astra`, `gpt-6-luna`, and `gpt-5.6-terra`; compact forms such as
  `GPT6LUNAXI` and `GPT56TERRAXI` preserve the named variant and imply
  `xhigh`. If a Codex lane names no model or profile, resolve it to
  `gpt-6.1-sol` and report that the model came from the default. If the
  resulting Sol lane names no effort, resolve it to `xhigh` and report
  `effort_source=preference_default`.
- Preserve family and numeric version exactly. `gpt-6-luna` may normalize to
  `gpt-6-luna`; it must not become `gpt-6.1-sol`, `gpt-5.4`, or `gpt-5.5`. `fable 5.1` may normalize to
  `claude-fable-5-1`, and `opus 4.7` may normalize to `claude-opus-4-7`, and `opus 5.5` to `claude-opus-5-5`;
  neither may become another Claude family or version.
- If the user says `gpt 5.4`, `gpt 5.5`, or a variant of either while choosing
  a model, do not execute it. Say that the old model is blocked and ask whether
  they meant `gpt-6.1-sol`. This is an intent check, not an alias rule: do not
  rewrite the version yourself.
- Infer runtime only from unambiguous family evidence: `gpt`/`gbt`/`fugu`/
  `fugu-ultra`/`codex`/`sol`/`luna`/`terra` implies Codex; `claude fable`, `fable`,
  `claude opus`, or `opus` implies Claude; `agent`, `cursor`, `cursor agent`,
  or `cursor-agent` implies Cursor Agent only for Composer.
  natural `grok`, `grok build`, `grok cli`, `grok-4.6`, or an explicit legacy
  `grok-*` slug implies Grok; `kimi`, `kimi code`, `kimi k3`, `k3`, or
  `moonshot` implies Kimi; `agy`, `antigravity`, `gemini`, `argon`, or an exact
  `gemini-*` id implies agy. "Antigravity agent" names agy, not Cursor Agent;
  only the word `cursor` selects Cursor Agent beside an agy word, and that
  phrase then fails as mixed.
  If a phrase mixes Cursor Agent with GPT/GBT model ids, Fugu profiles, or
  Claude, fail loud instead of choosing a side. If a phrase mixes Grok, Kimi,
  or agy with GPT/GBT model ids, Fugu profiles, Claude, Cursor Agent, or each
  other, fail loud instead of choosing a side. `agy opus` fails this way even
  though agy's own catalog lists Claude Opus.
- For ordinary Codex model ids, inspect `codex debug models` when model
  availability matters and choose an available id with the same family and
  exact version. For Fugu, resolve `fugu` and `fugu-ultra` as Codex profiles,
  not model-list ids; preserve the profile names exactly and launch them with
  `-p`.
- For Claude, preserve the named supported Claude family and version. Fable 5.1
  resolves to `claude-fable-5-1`; Opus 4.7 resolves to `claude-opus-4-7`; Opus 5.5 resolves to `claude-opus-5-5`. If the
  user names Sonnet or Haiku, fail loud and ask for a supported Claude choice.
- For Cursor Agent, always use `composer-2.5-fast`. Accept `composer`,
  `composer 2.5`, `composer-2.5`, `composer-2.5-fast`, or bare `2.5` in a
  Cursor Agent context as that runnable id. Do not use Cursor model discovery
  for non-Composer routing, and do not pass GPT/GBT model ids, Fugu profiles,
  or Claude model ids to Cursor Agent.
- For Grok, natural `grok`, `grok cli`, and `grok build` wording resolves to
  `grok-4.6`; “Grok Build” is the harness, not a model id. If that wording
  names a numeric version other than `4.6`, fail loud rather than discarding
  it. Preserve explicit
  legacy slugs such as `grok-build` and `grok-composer-2.5-fast` exactly and
  require discovery to confirm them. Never rewrite an explicit slug.
- For Kimi, `kimi`, `kimi code`, `kimi k3`, `k3`, and `moonshot` resolve to
  `kimi-code/k3`. Preserve that callable alias exactly; do not auto-resolve
  older Kimi-for-coding/K2.7 aliases or cross provider model ids. When
  availability matters, inspect the top-level `.models` keys from
  `kimi provider list --json`.
- For agy, bare `agy`, `antigravity`, `gemini`, and `argon`, natural
  `gemini 4 argon`, and the exact id `gemini-4-argon` resolve to
  `gemini-4-argon`. `gemini flash`, `gemini 3.8 flash`, or `gemini-3.8-flash`
  resolves to `gemini-3.8-flash`, and only when Flash is named. A baked effort
  suffix such as `gemini-4-argon-medium` reads as model plus effort. A natural
  version the catalog does not have, such as `gemini 4.5 argon`, `argon 4.5`, or `gemini 3 flash`, or a Gemini version with neither Argon nor Flash, such as
  `gemini 2.5 pro`, fails; never rewrite it. Only Gemini models run through
  agy: its catalog also lists Claude Opus 5.5, Claude Sonnet 5.5, and GPT-OSS,
  but Opus stays on Claude Code and this doctrine routes neither Sonnet nor
  GPT-OSS. Before the first agy launch, run `agy models`. If it says to sign in, stop and
  report that agy is signed out: a signed-out headless agy run opens the
  Google sign-in page in the user's browser. Each model line is
  `<id-with-effort-suffix>\t<display name>`, and the base id is the id without
  its `-low`, `-medium`, or `-high` suffix. Argon needs a Google AI Ultra
  sign-in, so a machine without one will not list it. If the catalog lists
  models but not the requested one, fail and name the sign-in as the likely
  cause; never substitute Flash or another provider.
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
Model A: "Claude Fable 5.1 high" -> runtime=claude, model=claude-fable-5-1, effort=high
Model B: "Claude Opus 4.7 xhigh" -> runtime=claude, model=claude-opus-4-7, effort=xhigh
Model C: "codex" -> runtime=codex, model=gpt-6.1-sol, effort=xhigh, model_source=default, effort_source=preference_default
Model D: "codex high" -> runtime=codex, model=gpt-6.1-sol, effort=high, model_source=default
Model E: "luna xhigh" -> runtime=codex, model=gpt-6-luna, effort=xhigh
Model F: "terra high" -> runtime=codex, model=gpt-5.6-terra, effort=high
Model G: "Fugu Ultra xhigh" -> runtime=codex, model=fugu-ultra, codex_profile=fugu-ultra, effort=xhigh
Model H: "Grok Build high" -> runtime=grok, model=grok-4.6, effort=high
Model I: "Kimi K3 high" -> runtime=kimi, model=kimi-code/k3, effort=high
Model J: "Kimi" -> runtime=kimi, model=kimi-code/k3, effort=max, effort_source=model_default
Model K: "Argon high" -> runtime=agy, model=gemini-4-argon, effort=high
Model L: "Gemini" -> runtime=agy, model=gemini-4-argon, effort=high, model_source=default, effort_source=preference_default
Model M: "Gemini Flash medium" -> runtime=agy, model=gemini-3.8-flash, effort=medium
"agy opus high" -> fail: names Claude and agy; Opus runs through Claude Code
```

Effort follows the selected model's real contract. `grok-4.6` supports
`low`, `medium`, and `high`; do not infer support for `xhigh` or `max` from the
generic CLI parser. Kimi K3 advertises `low`, `high`, and `max`, with omitted
effort defaulting to `max`. Pass Kimi effort through
`KIMI_MODEL_THINKING_EFFORT`; there is no `--effort` flag. Preserve an explicit
`medium` or `xhigh` as a forced override, but never choose either by default or
inference and never remap one effort to another. agy's Gemini models accept
`low`, `medium`, and `high` via `--effort`, with omitted effort defaulting to
`high` as a preference default; `xhigh`, `max`, and `ultra` fail before launch.
Pass the base id with `--model` and the effort with `--effort`, even when the
user named a baked id such as `gemini-4-argon-high`.

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
prompt file where the runtime supports it. Kimi and agy have no verified
prompt-file or stdin form, so each takes the saved prompt as one argv value
without a shell (`-p` for Kimi, attached `--print=` for agy); recognize the
operating-system argv-size limit. For agy, also record `agy --version` in the
run index for each participant turn, because agy updates itself between runs
and has no switch to stop that. Keep event streams and final messages
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
rounds. Participant prompts are read-only, allow each participant's own native
sub-agents, and prohibit starting external agents.

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

## External Kimi: First Turn

Use a resumable Kimi session for each Kimi participant. A fresh turn starts
without prior conversation but still persists a session:

```bash
KIMI_CODE_NO_AUTO_UPDATE=1 \
KIMI_MODEL_THINKING_EFFORT="<resolved_effort>" \
kimi \
  -m "<resolved_kimi_model>" \
  -p "$(cat "$RUN_DIR/round-01/model-a-prompt.md")" \
  --output-format stream-json \
  > "$RUN_DIR/round-01/model-a-events.jsonl" \
  2> "$RUN_DIR/round-01/model-a-stderr.log"
```

Run from `work_root`; Kimi has no cwd flag and its sessions are cwd-scoped.
Build argv directly rather than evaluating untrusted prompt text through a
shell. Kimi always persists a session, so it cannot satisfy a load-bearing
stateless/no-persist participant requirement. Set `KIMI_CODE_NO_AUTO_UPDATE=1`
on every run. Print mode performs
automatic approval, but it is not a full permission, hook, or static-denial
bypass. Do not add `--yolo`, `--auto`, or `--plan`, which conflict with `-p`.
Kimi has no documented hook-suppression flag and inherits configured hooks and
MCP servers.

Concatenate string `content` from every `role=assistant` event into the
participant final. Capture the durable `session_id` from the `role=meta`,
`type=session.resume_hint` event. Missing final text or a missing hint makes a
resumable turn malformed; preserve its receipts and do not replace the
participant silently.

## External Kimi: Resume Turn

Resume from the same `work_root` with the exact captured id:

```bash
KIMI_CODE_NO_AUTO_UPDATE=1 \
KIMI_MODEL_THINKING_EFFORT="<resolved_effort>" \
kimi \
  -r "<session_id>" \
  -m "<resolved_kimi_model>" \
  -p "$(cat "$RUN_DIR/round-02/model-a-prompt.md")" \
  --output-format stream-json \
  > "$RUN_DIR/round-02/model-a-events.jsonl" \
  2> "$RUN_DIR/round-02/model-a-stderr.log"
```

Use `-r <session_id>`, never `-c`/`--continue` or another latest-session
selector. Parse final text and require a fresh `session.resume_hint` exactly as
on the first turn. A missing hint is unrecoverable for continuation; do not
reuse the input id as a fallback.

## External agy: First Turn

Use a resumable agy conversation for each agy participant. A fresh turn starts
without prior conversation but still persists one:

```bash
agy \
  --print="$(cat "$RUN_DIR/round-01/model-a-prompt.md")" \
  --model "<resolved_agy_model>" \
  --effort "<resolved_effort>" \
  --output-format stream-json \
  --print-timeout 0 \
  --dangerously-skip-permissions \
  > "$RUN_DIR/round-01/model-a-events.jsonl" \
  2> "$RUN_DIR/round-01/model-a-stderr.log"
```

Run from `work_root`; agy has no cwd flag. Keep the prompt attached to
`--print=`, so a prompt that starts with `-` is not read as a flag.
`--print-timeout 0` waits for the whole turn; older builds defaulted to five
minutes, which would cut off a long repo-reading round. agy always persists a
conversation, so it cannot satisfy a load-bearing stateless/no-persist
participant requirement.

Pass `--dangerously-skip-permissions` for participants too: a headless run
cannot answer a permission prompt, and a machine on agy's shipped
`request-review` setting would otherwise refuse the tools the participant
needs to read evidence. The participant stays read-only through the no-edit
contract and the parent's status or diff check, as on the Grok lane. Do not
add `--mode plan` as a read-only mode; it writes an `implementation_plan.md`
artifact and waits for approval instead of answering. Do not add `--sandbox`
or feed the prompt through `--input-format stream-json`, whose message shape is
undocumented. agy runs the user's global hooks from
`~/.gemini/config/hooks.json` and its configured MCP servers in every
subprocess, and no flag disables them.

The first event line is `event=init`; keep its `conversation_id` for resume.
After exit, read the last line, `event=result`. When `result.status` is
`SUCCESS`, write `result.response` to the participant final file and check
that `result.conversation_id` matches the init id. A missing result line, a
`status` of `ERROR` (its `error` string says why), an empty `response`, or a
missing or mismatched conversation id makes the turn malformed; preserve its
receipts and do not replace the participant silently. If a caller adds
`--json-schema <schema path>`, read only the parsed object in
`result.structured_output`, because `result.response` can then hold prose or
extra keys around the JSON.

## External agy: Resume Turn

Resume from the same `work_root` with the exact captured id:

```bash
agy \
  --conversation "<session_id>" \
  --print="$(cat "$RUN_DIR/round-02/model-a-prompt.md")" \
  --model "<resolved_agy_model>" \
  --effort "<resolved_effort>" \
  --output-format stream-json \
  --print-timeout 0 \
  --dangerously-skip-permissions \
  > "$RUN_DIR/round-02/model-a-events.jsonl" \
  2> "$RUN_DIR/round-02/model-a-stderr.log"
```

Use `--conversation <session_id>`, never `-c`/`--continue` or another
latest-session selector. Parse the result as on the first turn, then check the
id. agy does not fail on an id it cannot find: it writes
`warning: conversation "<id>" not found` to stderr, answers in a new
conversation under a new id, and exits 0 with `SUCCESS`. Both the init and
result `conversation_id` must therefore equal the requested id. If either is
missing or different, the participant answered without its own earlier
reasoning. That is a failed resume, never a usable round: preserve its
receipts, report the failure, and do not adopt the new id, reuse the input id,
or start a fresh participant in its place.

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
participant, missing external CLI, unresolved exact model/effort, child non-zero
exit, empty final result after process exit, missing terminal result event,
Kimi output without `role=assistant` text or a fresh resumable-turn
`session.resume_hint`, agy output whose `result.status` is not `SUCCESS` or
whose init or result `conversation_id` is missing or, on resume, differs from
the requested id, latest-session selection such as Kimi or agy `-c`, or a
participant refusing the prompt contract. If native capability is unavailable,
select the external lane deliberately rather than pretending the native child
honors it. Do not silently switch among Claude, Codex, Cursor Agent, Grok,
Kimi, and agy, downgrade models (Argon to Flash included), reduce effort,
or replace a long-running participant with the parent agent's own answer.

Apply the Codex preference in `../../_shared/agent-orchestration-policy.md`: default omitted Codex models and bare `sol` to `gpt-6.1-sol` at `xhigh`. Preserve explicit model versions and effort choices; do not redirect Sol requests to Astra.
