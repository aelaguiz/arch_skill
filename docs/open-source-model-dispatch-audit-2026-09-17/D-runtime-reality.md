# D - Native subagent model dispatch: runtime reality on this machine

Read-only audit. Every claim below carries the exact command or file path used as proof.
Repo files, configs, and installs were not modified. No subagents were spawned by this audit.

Environment: macOS, user Amir.
- Prime Agent CLI: `/opt/homebrew/bin/prime-agent` -> `/Users/aelaguiz/.prime/installs/main-c8bc030/lib/node_modules/prime-agent/dist/bundle/cli.js`. `which prime` returns nothing (`prime --help` -> exit 1, empty output).
- Codex CLI: `codex --version` -> `codex-cli 0.154.0-alpha.3`.
- Claude Code: `claude --version` -> `2.1.274 (Claude Code)`.

---

## Prime Agent

### What catalog this install exposes for native children

Proof command (Python REPL, this session):

```python
await rlm.find_models('', limit=20)      # limit must be 1..20
```

The host enforces the bound: `RuntimeError: rlm.find_models limit must be an integer from 1 to 20`.
Repeating `find_models` over 20 queries (`'', claude, gpt, deepseek, glm, sol, fable, opus, terra, luna, ...`) returned **221 unique selectors** across six providers:

| provider | example selectors that exist today |
| --- | --- |
| `openrouter` | `openrouter/deepseek/deepseek-v4.1-flash`, `openrouter/z-ai/glm-5.3`, `openrouter/anthropic/claude-opus-5`, `openrouter/openai/gpt-5.6-sol`, `openrouter/stealth/union-alpha`-family, `openrouter/qwen/...`, `openrouter/moonshotai/kimi-k3`, `openrouter/meta-llama/...` |
| `prime-inference` | `prime-inference/z-ai/glm-5.3`, `prime-inference/openai/gpt-5.6-sol`, `prime-inference/anthropic/claude-opus-5`, `prime-inference/moonshotai/kimi-k3` |
| `anthropic` | `anthropic/claude-opus-5`, `anthropic/claude-fable-5`, `anthropic/claude-fable-5-1`, `anthropic/claude-sonnet-5`, `anthropic/claude-haiku-4-5` |
| `openai-codex` | `openai-codex/gpt-5.6-sol`, `openai-codex/gpt-5.6-sol-1m`, `openai-codex/gpt-5.6-luna`, `openai-codex/gpt-5.6-terra`, `openai-codex/gpt-5.5` |
| `deepseek` | `deepseek/deepseek-flash`, `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro` |
| `xai` | `xai/grok-4.6`, `xai/grok-4.3`, `xai/grok-4.5`, `xai/grok-4.20-0309-reasoning`, `xai/grok-build-0.1` |

Reachability rule (source: `/Users/aelaguiz/.prime/installs/main-c8bc030/lib/node_modules/prime-agent/dist/core/agent-session.js`, `_authenticatedRlmModels`):

```js
return (await this._modelRegistry.getExecutableModels()).filter((model) => {
    const status = this._modelRegistry.getProviderAuthStatus(model.provider);
    return status.source !== "stale" && status.label !== "expired";
});
```

So a child can use any model whose provider credential is live. Declared catalogs and credentials:
- `/Users/aelaguiz/.prime/agent/models.json` adds `anthropic/claude-fable-5-1` (with `"headers": {"user-agent": "claude-cli/2.1.251"}`), OpenRouter `stealth/union-alpha`, `z-ai/glm-5.3`, `deepseek/deepseek-v4.1-flash`, and Sakana `fugu-max`, `fugu-ultra-v2.0`; provider keys resolve live, e.g. `"apiKey": "!sed -n 's/^OPENROUTER_API_KEY=//p' /Users/aelaguiz/.codex/.env | head -1"`.
- `/Users/aelaguiz/.prime/agent/auth.json` holds credential bindings for `openai-codex`, `anthropic`, `xai` (aimgr external), plus `deepseek`, `sakana`, `serper` API keys.
- `/Users/aelaguiz/.prime/agent/settings.json`: `"defaultProvider": "openrouter"`, `"defaultModel": "deepseek/deepseek-v4.1-flash"`, `"defaultThinkingLevel": "xhigh"`, `"defaultServiceTier": "priority"`.

**`gpt-6-astra` is NOT reachable in Prime.** `await rlm.find_models('astra')` -> `0`; `await rlm.find_models('gpt-6')` -> `0`.

### What this session reports for itself (the parent is an open-source model)

Proof file: `/Users/aelaguiz/.prime/agent/sessions/01a0af5e-ebce-775a-b901-a535ae5479a6.jsonl` (the parent session), lines 1-3:

```
{"type": "session", "version": 3, "id": "01a0af5e-ebce-775a-b901-a535ae5479a6", ..., "rlmDepth": 0, "git": {...}}
{"type": "model_change", "provider": "openrouter", "modelId": "deepseek/deepseek-v4.1-flash", "thinkingLevel": null}
{"type": "thinking_level_change", "provider": null, "modelId": null, "thinkingLevel": "xhigh"}
```

Parent = `openrouter/deepseek-v4.1-flash` at thinking `xhigh`. That is an open-source model (DeepSeek V4.1 Flash) routed through OpenRouter.

### Inheritance default: yes, children inherit both model and thinking level

Source proof, `agent-session.js` -> `_resolveRlmSubagentModel`:

```js
async _resolveRlmSubagentModel(reference) {
    const parentModel = this.model;
    if (!parentModel) throw new Error(formatNoModelSelectedMessage());
    if (!reference) { return { model: parentModel }; }        // <-- inherit by default
    ...
```

and `_createRlmSubagentRuntimeOptions`:

```js
model: options.model,
thinkingLevel: options.thinkingLevel ?? clampThinkingLevel(options.model, this.thinkingLevel),
```

Live proof from this same parent session. Four children spawned without a model argument
(`/Users/aelaguiz/.prime/agent/session-artifacts/01a0af5e-ebce-775a-b901-a535ae5479a6/sub-*/rlm-subagent.json`
and the matching child session jsonl headers) recorded identical values to the parent:

```
dispatch-a-container   model {"provider":"openrouter","modelId":"deepseek/deepseek-v4.1-flash"}  thinking xhigh
dispatch-b-review      model {"provider":"openrouter","modelId":"deepseek/deepseek-v4.1-flash"}  thinking xhigh
dispatch-c-arch        model {"provider":"openrouter","modelId":"deepseek/deepseek-v4.1-flash"}  thinking xhigh
dispatch-d-runtime     model {"provider":"openrouter","modelId":"deepseek/deepseek-v4.1-flash"}  thinking xhigh
```

Child session jsonl confirmation (e.g. `.../sub-82aa1a00/01a0af5f-8e48-7651-b97c-ed6e33444ca5.jsonl`):

```
{"type": "model_change", ..., "provider": "openrouter", "modelId": "deepseek/deepseek-v4.1-flash"}
{"type": "thinking_level_change", ..., "thinkingLevel": "xhigh"}
```

### Can a child be pinned to a different model AND a different thinking level? Yes - proven live

API contract (`rlm/__init__.py`, spawn handle docstring):

```python
async def run(prompt: str, **kwargs) -> RLMSpawnHandle:
    """``model`` selects a child with an exact ``provider/model`` selector.
    ``thinking`` sets the child reasoning level ...; defaults to the parent level;
    levels invalid for the resolved model fail the spawn."""
```

Only three kwargs are legal; anything else throws (`agent-session.js`):

```js
const { name: rawName, model: rawModel, thinking: rawThinking, ...unsupported } = kwargs;
if (unsupportedKwargs.length > 0) throw new Error(`Unsupported rlm.run kwargs: ${unsupportedKwargs.sort().join(", ")}`);
```

Pinned model must be an exact authenticated `provider/id`, else the spawn throws:

```
Requested subagent model "<X>" is unavailable, unauthenticated, or expired
```

An explicitly requested thinking level outside the child model's levels also throws:

```
Requested thinking level "<X>" is not supported by model "<provider>/<id>"; supported levels: <list>
```

Live proof, from this parent session (`spawnCode` recorded in
`/Users/aelaguiz/.prime/agent/session-artifacts/01a0af5e-ebce-775a-b901-a535ae5479a6/sub-6823f16a/rlm-subagent.json`
and `sub-aa1bdfd3/rlm-subagent.json`):

```python
# Probe 2: cross-provider pin from an OSS parent -> is it reachable? (admission only, trivial prompt)
for nm, mdl, th in [('probe-cross-luna','openai-codex/gpt-5.6-luna','low'),
                    ('probe-cross-fugu','sakana/fugu-max','high')]:
    try:
        h = await rlm('Reply with the single word OK.', name=nm, model=mdl, thinking=th)
```

Recorded results:

| child | sessionName | recorded model | recorded thinking | status |
| --- | --- | --- | --- | --- |
| `sub-6823f16a` | `probe-cross-luna` | `openai-codex/gpt-5.6-luna` | `low` | deleted (admitted, ran, cleaned up) |
| `sub-aa1bdfd3` | `probe-cross-fugu` | `sakana/fugu-max` | `high` | deleted (admitted, ran, cleaned up) |

Both differ from the parent on provider, model, and thinking level. `sakana/fugu-max` is the
same "Fugu" family Amir runs in Codex; `openai-codex/gpt-5.6-luna` is a Codex-family model.

### Installed Prime skills name no model

`/Users/aelaguiz/.prime/agent/skills/` contains exactly two skills (`mcp-bridge`, `browseros`).
The only match for `model` in either `SKILL.md` is prose: `mcp-bridge/SKILL.md:9` - "adding direct model tools."
Neither names a parent or child model.

---

## Codex

### Model ids that are real in this install

Proof command: `codex debug models` (writes the raw catalog as JSON; no generation).

```
gpt-6-astra        vis=list  api=True  default_eff=medium  tiers=['priority'] speeds=['fast']
gpt-reserve        vis=hide  api=True  default_eff=medium  tiers=['priority'] speeds=['fast']
gpt-5.6-sol        vis=list  api=True  default_eff=low     tiers=['priority'] speeds=['fast']
gpt-5.6-terra      vis=list  api=True  default_eff=medium  tiers=['priority'] speeds=['fast']
gpt-5.6-luna       vis=list  api=True  default_eff=medium  tiers=['priority'] speeds=['fast']
gpt-5.5            vis=list  api=True  default_eff=medium  tiers=['priority'] speeds=['fast']
codex-auto-review  vis=hide  api=True  default_eff=medium  tiers=['priority'] speeds=['fast']
```

Seven slugs. `gpt-5.3-codex-spark` (used by `[profiles.spark]`) is **not** in this catalog today.

### Default profile / base model

`/Users/aelaguiz/.codex/config.toml`:

```
5: model = "gpt-6-astra"
8: model_reasoning_effort = "high"
19: [agents]
21: max_concurrent_threads_per_session = 7
38: multi_agent = true
39: multi_agent_v2 = true
252: [notice.model_migrations]
256: "gpt-5.3-codex" = "gpt-6-astra"
294: [profiles.spark]
296: model = "gpt-5.3-codex-spark"
297: model_reasoning_effort = "xhigh"
```

`-p yolo` profile (`/Users/aelaguiz/.codex/yolo.config.toml`, loaded per `config.toml:4` comment
"Yolo overrides live in ~/.codex/yolo.config.toml (loaded with `codex -p yolo`)."):

```
2: model = "gpt-6-astra"
4: model_reasoning_effort = "xhigh"
```

### Open-source-model profiles exist as separate config files

Their own first-line comments give the invocation, e.g.:

- `/Users/aelaguiz/.codex/fugu-max.config.toml` - "# Sakana Fugu Max ... Use: codex -p fugu-max", `model = "fugu-max"`, `model_provider = "sakana"`, `model_catalog_json = "/Users/aelaguiz/.codex/fugu.json"`, `model_reasoning_effort = "xhigh"`.
- `fugu-ultra-v2.config.toml` (`fugu-ultra-v2.0`), `fugu.config.toml` (`fugu`), `fugu-xhigh.config.toml`.
- `glm53.config.toml` - `model = "@preset/glm53-unquantized"`, `model_provider = "openrouter"`, catalog `glm.json`.
- `glm-xhigh.config.toml` - `model = "z-ai/glm-5.2"`, openrouter.
- `dsflash.config.toml` - "# DeepSeek V4.1 Flash, direct DeepSeek API ... Use: codex -p dsflash", `model = "deepseek-flash"`, `model_provider = "deepseek"`, catalog `deepseek-flash.json`.
- `dsflash-or.config.toml` (openrouter variant), `union-alpha.config.toml` (`stealth/union-alpha`).

Provider blocks exist in `config.toml`:

```
121: [model_providers.sakana]     base_url = "https://api.sakana.ai/v1"   env_key = "SAKANA_API_KEY"
130: [model_providers.openrouter] base_url = "https://openrouter.ai/api/v1" env_key = "OPENROUTER_API_KEY"
139: [model_providers.deepseek]   base_url = "https://api.deepseek.com"   env_key = "DEEPSEEK_API_KEY"
```

The per-profile catalogs list the models those profiles can use:

- `~/.codex/deepseek-flash.json`: `deepseek-flash`, `deepseek-v4-pro`, `deepseek/deepseek-v4.1-flash`, `@preset/deepseek41-unquantized`
- `~/.codex/glm.json`: `z-ai/glm-5.2`, `@preset/glm53-unquantized`
- `~/.codex/fugu.json`: `fugu`, `fugu-ultra`, `fugu-max`, `fugu-ultra-v2.0`
- `~/.codex/union-alpha.json`: `stealth/union-alpha`

### Does spawn_agent accept a per-child model override?

**It has an optional model field, but the default is inheritance and the tool text discourages setting it.**

Real session proof (namespace `multi_agent_v1`, tool text as the model actually received it),
`/Users/aelaguiz/.codex/sessions/2026/06/07/rollout-2026-06-07T14-05-58-019ea37a-40b9-7ec1-b636-051e40c4dc5d.jsonl`
(search for `tool_search_output` + `spawn_agent`):

```
function spawn_agent Available model overrides (optional; inherited parent model is preferred):
- `gpt-5.5`: Frontier model for complex coding, research, and real-world work. Reasoning efforts: low, medium (default), high, xhigh. Service tiers: priority.
- `gpt-5.4`: ... Reasoning efforts: low, medium (default), high, xhigh. Service tiers: priority.
- `gpt-5.4-mini`: ... - `gpt-5.3-codex-spark`: ...
Spawn a sub-agent for a well-scoped task. Returns the spawned agent id plus the user-facing nickname when available.
Spawned agents inherit your current model by default. If provided, `model` specifies the model to use for the spawned agent.
This spawn_agent tool provides you access to sub-agents that inherit your current model by default. Do not set the `model` field unless the user explicitly asks for a different model or there is a clear task-specific reason.
```

Handler-side validation exists in the binary
(`/opt/homebrew/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex`):

```
Unknown model `<X>` for spawn_agent. Available models: <list>
Reasoning effort `<X>` is not supported for model `<Y>`. Supported reasoning efforts: <list>
```

The override list is gated by an internal config key. `strings`-level inspection shows the key
`expose_spawn_agent_model_overrides` belongs to `struct MultiAgentV2ConfigToml with 16 elements`
(together with `max_concurrent_threads_per_session`, `hide_spawn_agent_metadata`, `wait_agent_enabled`,
`subagent_developer_instructions`, ...). It is **not** listed by `codex features list` (137 lines; `multi_agent` and
`multi_agent_v2` are `stable true`). A `-c agents.expose_spawn_agent_model_overrides=true` probe is rejected
because `agents` is `AgentRoleToml`:

```
Error: invalid type: boolean `true`, expected struct AgentRoleToml in `agents`
```

### What actually happens today on this machine: children always inherit

All September sessions, real tool calls:

- `rg -c '"name":"spawn_agent"' sessions/2026/09/*/*.jsonl` -> 145 files match.
- `rg -o '"name":"spawn_agent","namespace":"collaboration","arguments":"\{\\"[a-z_]+'` -> key histogram: `4561 "{\"task_name`, `3 "{\"fork_turns`, `1 "{\"target`.
- spawn_agent calls containing a `model` argument: **0**.

DeepSeek-parent session, real spawn call
(`/Users/aelaguiz/.codex/sessions/2026/09/15/rollout-2026-09-15T06-48-32-01a0a4e5-b61a-7201-8c8d-8375ff4e4191.jsonl`,
`session_meta.payload.model_provider = "deepseek"`):

```
"name":"spawn_agent","namespace":"collaboration","arguments":"{\"task_name\": \"evidence_3537\", \"fork_turns\": \"none\", \"message\": \"...\"}"
```

No `model` field. And that same parent reasoned, verbatim, in its own transcript:

```
The spawn_agent tool offers deepseek models only... The available model overrides are `deepseek-flash`, `deepseek/deepseek-v4.1-flash`, `deepseek-v4-pro`. So I cannot pin gpt-5.6-sol. Hmm - the tool list says "Available model overrides (optional; inherited parent model is preferred)". So the host constrains child models to the parent's provider...
```

Those three ids are exactly the DeepSeek ids in `~/.codex/deepseek-flash.json`.
The `-p yolo` / default route (`gpt-6-astra`) would list the OpenAI catalog instead.

---

## Claude Code

### Named subagents can carry their own model

There is no `~/.claude/agents/` directory on this machine (`ls ~/.claude/agents` -> "No such file or directory"),
but real agent definitions with a `model:` frontmatter field exist under the plugin marketplace and in projects:

`/Users/aelaguiz/.claude/plugins/marketplaces/claude-plugins-official/plugins/feature-dev/agents/code-reviewer.md`:

```
---
name: code-reviewer
description: Reviews code for bugs, logic errors, security vulnerabilities, ...
tools: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput
model: sonnet
color: red
---
```

`/Users/aelaguiz/workspace/psagentspace/.claude/agents/audit-budget.md`:

```
---
name: audit-budget
description: > Budget and bidding specialist. ...
model: sonnet
maxTurns: 20
tools: Read, Bash, Write, Glob, Grep
---
```

### Resolution semantics (from the Claude Code binary)

`/Users/aelaguiz/.local/share/claude/versions/2.1.274` (Mach-O arm64) contains the resolver and its labels:

```
CLAUDE_CODE_SUBAGENT_MODEL
CLAUDE_CODE_SUBAGENT_MODEL_FORCE
[M,"frontmatter"] : M!=="inherit"&&F!=="inherit" ? [F,"env"] : [s,"inherit"]
subagent_model_resolve  parent_inherit | family_step_down | family_mismatch | inherit_family_mismatch | override_dropped
requested_family / resolved_family / requested_model / resolved_model
Subagent model "<X>" is not in the availableModels allowlist; using the newest allowed model in its family
Subagent model "<X>" is not in the availableModels allowlist; inheriting the parent model
Agent model "<X>" is not in the availableModels allowlist; keeping the session model
Workflow agent model "<X>" ignored: CLAUDE_CODE_SUBAGENT_MODEL_FORCE is set
```

So: a named subagent's `model:` frontmatter is applied when allowed, and when it is not on the
allowlist the runtime either steps down inside the same family or inherits the parent model.

### Main model choice

`/Users/aelaguiz/.claude/settings.json`:

```
2:   "model": "opus[1m]",
     "effortLevel": "xhigh",
```

`claude --help`:

```
--model <model>     Model for the current session. Provide an alias for the latest model
                    (e.g. 'fable', 'opus', or 'sonnet') or a model's full name (e.g. 'claude-fable-5').
--agent <agent>     Agent for the current session. Overrides the 'agent' setting.
--agents <json>     JSON object defining custom agents (e.g. '{"reviewer": {"description": "Reviews code", "prompt": "You are a code reviewer"}}')
--fallback-model <model>   Enable automatic fallback to specified model(s) ...
```

### Repo note (skills do not ship Claude agent definitions)

`skills/<slug>/agents/` in `/Users/aelaguiz/workspace/arch_skill` contains only `openai.yaml`
(Codex agent manifests). `find skills -path '*/agents/*' -name '*.md'` -> 0 files. The Makefile mirrors
skill directories into `~/.claude/skills/` and copies `agents/openai.yaml` when present
(`Makefile:226: if [ -f skills/$$skill/agents/openai.yaml ]; then`), so no Claude-side `model:` field is installed.

---

## Cross-provider reach

| Host | Different provider for a native child? | Evidence |
| --- | --- | --- |
| Prime Agent | **Yes, proven live.** `openrouter/deepseek-v4.1-flash` parent spawned `openai-codex/gpt-5.6-luna` and `sakana/fugu-max` children. | `sub-6823f16a/rlm-subagent.json` + `sub-aa1bdfd3/rlm-subagent.json`; code path `_resolveRlmSubagentModel` searches `_authenticatedRlmModels()` across all providers with live auth. |
| Codex | **Not shown as available from a single-provider profile.** The override list is the active profile's catalog: OpenAI profile -> `gpt-5.5, gpt-5.4, gpt-5.4-mini, gpt-5.3-codex-spark`; DeepSeek profile -> `deepseek-flash, deepseek/deepseek-v4.1-flash, deepseek-v4-pro`. | 2026-06-07 rollout tool text; 2026-09-15 deepseek session reasoning + `~/.codex/deepseek-flash.json`. |
| Claude Code | **No evidence of a non-Anthropic child.** Overrides are Anthropic family aliases and are allowlist-checked, with `family_step_down` / `inherit_family_mismatch` outcomes. | Binary strings `Subagent model "<X>" is not in the availableModels allowlist; ...` and the `family_*` labels. |

---

## Live model-name inventory

Model names the skills rely on, where they appear in live agent config on this machine, and current validity.

| Path:line | Quoted token | Surface | Valid today? |
| --- | --- | --- | --- |
| `~/.codex/config.toml:5` | `model = "gpt-6-astra"` | Codex default base model | Yes - in `codex debug models` |
| `~/.codex/config.toml:256` | `"gpt-5.3-codex" = "gpt-6-astra"` | migration map | Yes (maps into a live model) |
| `~/.codex/config.toml:296` | `model = "gpt-5.3-codex-spark"` | `[profiles.spark]` | **No** - not in the current catalog |
| `~/.codex/yolo.config.toml:2` | `model = "gpt-6-astra"` | `-p yolo` profile | Yes |
| `~/.codex/yolo.config.toml:26-27` | `"gpt-5.6-sol"`, `gpt-6-astra` | TUI nux counters | Yes |
| `~/.codex/AGENTS.md:28` | "Default Codex to `gpt-6-astra` at `xhigh` ... recommend GPT-6 Astra ... Honor a deliberate request to keep Sol" | Codex agent instructions | Yes |
| `~/.codex/reject-gpt54.py:6-8` | `BLOCKED_MODELS = frozenset({"gpt-5.4", "gpt-5.5"})`, `PREFERRED_MODEL = "gpt-5.6-sol"`, `PREFERRED_EFFORT = "xhigh"` | SessionStart / UserPromptSubmit hook | Yes (gpt-5.6-sol and gpt-5.5 both exist; the block is policy, not availability) |
| `~/.claude/settings.json:2` | `"model": "opus[1m]"` | Claude Code main model | Yes (Opus 5 exists; `[1m]` is the 1M-context alias) |
| `~/.claude/CLAUDE.md:6-8` | "delegate security-sensitive actions ... to a Claude Opus 5 agent" | Claude Code instructions | Yes |
| `~/.prime/agent/settings.json:12,14,15,16` | `anthropic/claude-opus-5`, `anthropic/claude-fable-5-1`, `anthropic/claude-fable-5`, `openai-codex/gpt-5.6-sol` | `recentModels` | Yes - all four resolve via `rlm.find_models` |
| `~/.prime/agent/models.json:6-7` | `"id": "claude-fable-5-1"` | declared Prime model | Yes |
| `~/.prime/agent/harness/harness_state.json` (`entries/prompt/amir-native-gpt56-xhigh-openai-codex-routing`) | "use Prime Agent native children with the exact model selector `openai-codex/gpt-5.6-sol` and `thinking='xhigh'` ... Never use a `prime-inference/...` selector" | Prime global routing prompt | Yes - selector exists and pinning works |
| `~/.prime/agent/skills/mcp-bridge/SKILL.md:9`, `browseros/SKILL.md` | no model names | Installed Prime skills | n/a |
| `skills/issue-to-pr/agents/openai.yaml` (`default_prompt`) | "GPT-6 Astra Pro planning and final review written from $chatgpt-web's consultation templates" | Codex agent manifest in the skills repo | Naming the ChatGPT Pro consult model, not a child model |

Installed skills that name these models (regression risk, not config):
`rg -c 'gpt-6-astra|gpt-5\.6-sol|claude-opus-5|claude-fable-5' ~/.agents/skills` -> hits in 30 files, largest:
`stepwise/references/model-and-effort.md` (19), `arch-epic/references/model-and-effort.md` (16),
`agent-delegate/references/model-and-invocation.md` (14), `fresh-consult/references/model-and-invocation.md` (14),
`_shared/model_resolution.py` (11 matching lines; `:24: PREFERRED_CODEX_MODEL = "gpt-6-astra"`), `model-consensus/references/model-and-invocation.md` (11).

Stale-surface note: `PREFERRED_CODEX_MODEL = "gpt-6-astra"` is a Codex-only id. It resolves in the Codex CLI and
**not** in Prime Agent (`find_models('astra') -> 0`).

---

## What is proven vs assumed

**Proven (observed on this machine today):**
1. Prime native children inherit the parent's model **and** thinking level by default; verified for four children whose records match the `openrouter/deepseek-v4.1-flash` @ `xhigh` parent exactly.
2. Prime can pin a child to a different provider, model, and thinking level at spawn: `openai-codex/gpt-5.6-luna` @ `low` and `sakana/fugu-max` @ `high` were both admitted from that same DeepSeek parent.
3. Prime's usable child catalog is 221 selectors over 6 providers and includes `claude-opus-5`, `claude-fable-5`, `gpt-5.6-sol`, GLM 5.3, DeepSeek V4, Kimi K3, Fugu. It excludes `gpt-6-astra`.
4. Codex `spawn_agent` declares "Spawned agents inherit your current model by default" and exposes an optional `model` field plus per-model reasoning efforts and service tiers; the handler rejects unknown models and unsupported efforts.
5. In this install's real Codex usage, children always inherit: 4,561 `spawn_agent` calls in September sessions carry `task_name`/`fork_turns`/`message` and **zero** carry `model`.
6. Claude Code named subagents can carry `model:` in frontmatter (real files on disk), inherit the parent model when unset or `inherit`, and are corrected to `family_step_down` or parent inherit when the model is not allowlisted.
7. The parent model of this very session is an open-source model: `openrouter/deepseek-v4.1-flash` @ `xhigh`.

**Assumed (not fully established):**
1. The default value of `expose_spawn_agent_model_overrides` in this Codex build. The key is internal (`MultiAgentV2ConfigToml`); `-c` overrides for it are not type-checked, and `codex features list` does not show it.
2. Whether a Codex profile whose `model_catalog_json` contains several providers would offer a cross-provider child. Only single-provider catalogs were observed.
3. Whether Claude Code's `availableModels` allowlist ever permits a non-Anthropic child. No such case was found.
4. Whether the ChatGPT desktop app's subagent path (`/Applications/ChatGPT.app/Contents/Resources/codex`) exposes the model override the same way the CLI does.

---

## Open questions

1. Which config table owns `expose_spawn_agent_model_overrides` in this build, and what is its default? `[agents]` is `AgentRoleToml` here, so the flag must live in the `MultiAgentV2ConfigToml` table.
2. Is `[profiles.spark]` (`gpt-5.3-codex-spark`) still launchable, or is it a stale profile whose model left the catalog?
3. Does the ChatGPT desktop app expose a per-child model picker, or only the CLI's `spawn_agent` schema?
4. When the Prime parent runs on a very small free model (e.g. `openrouter/stealth/union-alpha`, `reasoning: false`), do children start with `thinking = "off"` only, since `getSupportedThinkingLevels` returns `["off"]` for non-reasoning models? (Predicted from source; not run, to avoid spend.)
5. Do the skills that name `gpt-6-astra` behave correctly when the parent host is Prime Agent, where that id does not exist?
