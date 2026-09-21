# Audit B — Review, Consultation, and Multi-Agent-Review Skills

Read-only audit. No repo file was edited. Every claim carries a `path:line` anchor into the tracked
working tree at `/Users/aelaguiz/workspace/arch_skill` (branch state as found, 2026-09-17).

Headline: the hypothesis is **partly true and partly disproved** for this slice.

- True: every concrete model/profile pin in this slice is a **vendor** pin (GPT/Claude/Grok/Kimi). None
  of these skills can express "the parent's own provider" or an unlisted open-source model as a
  delegated reviewer. The runtime enum is closed at five harnesses and contains no DeepSeek/GLM lane.
- Disproved: no skill in this slice pins a **native** child to a named model as a default, and none
  self-selects during ordinary work except `agent-delegate`. Ten of the twelve skills tell the parent
  to prefer a clean native child of the active host and to refuse a native model claim the host cannot
  confirm. Under a DeepSeek/GLM/Fugu parent that instruction still executes; it just inherits the
  parent's own model.
- The real defects are narrower than "hard-coded models": (a) a vendor default fires only inside an
  already-selected external Codex/Kimi lane, (b) one skill (`stepwise`) contradicts the other three
  about Sonnet/Haiku, (c) `agent-watcher`'s only worked model examples are Claude aliases, and
  (d) none of the twelve has any text for a parent whose own provider is not one of the five.

## Scope read

Files read (all under `/Users/aelaguiz/workspace/arch_skill`):

- `skills/fresh-consult/SKILL.md`
- `skills/fresh-consult/references/model-and-invocation.md`
- `skills/fresh-consult/references/consult-prompt-and-output.md`
- `skills/fresh-consult/agents/openai.yaml`
- `skills/model-consensus/SKILL.md`
- `skills/model-consensus/references/model-and-invocation.md`
- `skills/model-consensus/references/workflow-contract.md`
- `skills/model-consensus/references/examples.md`
- `skills/model-consensus/agents/openai.yaml`
- `skills/stepwise/SKILL.md`
- `skills/stepwise/references/model-and-effort.md`
- `skills/stepwise/references/session-resume.md`
- `skills/stepwise/references/execution-routing.md`
- `skills/stepwise/references/manifest-schema.md` (model-bearing lines)
- `skills/stepwise/scripts/run_stepwise.py` (argparse surface only)
- `skills/stepwise/scripts/test_run_stepwise.py` (model-bearing lines)
- `skills/stepwise/agents/openai.yaml`
- `skills/codex-review-yolo/SKILL.md`
- `skills/codex-review-yolo/references/troubleshooting.md` (model-bearing lines)
- `skills/plan-audit/SKILL.md`
- `skills/plan-audit/references/child-prompt-contract.md`
- `skills/plan-audit/references/proper-audit-checklist.md` (model-bearing lines)
- `skills/plan-implement/SKILL.md`
- `skills/plan-implement/references/native-subagent-contract.md`
- `skills/plan-implement/references/continuous-review.md` (model-bearing line)
- `skills/cynical-code-review/SKILL.md` + `references/agent-slices.md`
- `skills/cynical-architecture-review/SKILL.md`
- `skills/cynical-cruft-removal/SKILL.md`
- `skills/exhaustive-code-review/SKILL.md`
- `skills/agent-watcher/SKILL.md`
- `skills/agent-watcher/references/runtime-notes.md`
- `skills/agent-watcher/references/state-and-ledger.md`
- `skills/agent-watcher/references/watcher-brief.md` (model-bearing lines)
- `skills/agent-delegate/SKILL.md`
- `skills/agent-delegate/references/model-and-invocation.md`
- Cross-cutting, read because every skill in the slice delegates to it: `skills/_shared/agent-orchestration-policy.md`,
  `skills/_shared/native-child-capabilities.md`, `skills/_shared/model_resolution.py`
- Supporting, read only at the cited lines: `README.md`, `Makefile`, `skills/prompt-authoring/references/codex-goal-prompts.md`

Method: `rg -n` over the twelve skill directories with an explicit token list (model families, effort
levels, host names, profile names, CLI binaries), then full reads of every file above, then a direct
probe of `skills/_shared/model_resolution.py` loaded from disk with explicit empty catalogs so no
network, install, or repo write occurred.

One scope fact that changes how the repo should be read: `skills/<slug>/build/` directories exist on
disk but are **untracked build internals** — `git ls-files | grep -c '/build/'` returns `0`,
`git status` shows `?? skills/fresh-consult/build/` and `?? skills/agent-delegate/build/`, `Makefile:199`
rejects `*/build/*` as an install source, `Makefile:236` prunes it, and the installed copy of
`~/.agents/skills/fresh-consult/SKILL.md` is byte-identical to the tracked top-level file. The copies
under `build/` still carry stale pins (`gpt-5.4`, `$code-review`) that no longer exist on the live
surface. Verdict for a reader: harmless if left alone, misleading if grepped.

## Findings

### F1: An external Codex lane silently resolves to OpenAI `gpt-6-astra` + `xhigh` with no user choice

Exact quote:

> The defaults are deliberately narrow: when the lane is Codex and no model or
> profile is named, use `gpt-6-astra`; when an Astra lane omits effort, use `xhigh`
> with `effort_source=preference_default`; when the lane is Kimi, use
> `kimi-code/k3` and default an omitted effort to `max`.

`skills/fresh-consult/references/model-and-invocation.md:123`-`126`

Restated identically in three sibling skills:

- `skills/fresh-consult/references/model-and-invocation.md:68` — "An omitted model on a Codex lane resolves to `gpt-6-astra`"
- `skills/fresh-consult/SKILL.md:101` — "external Codex model defaults to `gpt-6-astra`, and an omitted effort on"
- `skills/agent-delegate/SKILL.md:93` — "defaults to `gpt-6-astra` and a Kimi lane defaults to `kimi-code/k3`"
- `skills/agent-delegate/references/model-and-invocation.md:37` — "An omitted model on a Codex lane resolves to `gpt-6-astra`"
- `skills/model-consensus/references/model-and-invocation.md:55` — "omitted model on a Codex lane resolves to `gpt-6-astra`"
- `skills/stepwise/references/model-and-effort.md:23`-`24` — "an external Codex worker or critic with no named / model uses `gpt-6-astra`; that Astra lane uses `xhigh` when effort is omitted"

Why it matters: this is the only default model in the slice, and it is a hard-coded vendor choice. It is
scoped correctly — it fires only *after* an external Codex lane has been selected — but once the parent
is on that lane, the parent never chose the model.

Effect on a non-Astra/non-Fable/non-Codex/non-Claude parent (DeepSeek, GLM, Fugu-profile Codex): **degrades**.
The lane still works and the reviewer is on a *different* provider than the parent, which is the point of
an external consult. But when the parent is itself running a provider unlisted in the repo, the repo has
no vocabulary for "review on my own provider", so the only reachable exact-model paths are the five
vendor lanes, and an unbriefed Codex lane quietly lands on `gpt-6-astra xhigh`.

### F2: The resolver's runtime enum is closed at five harnesses; no open-source provider exists anywhere

Exact quote:

> VALID_RUNTIMES = {"agent", "claude", "codex", "grok", "kimi"}

`skills/_shared/model_resolution.py:22`

> - `runtime` - `claude`, `codex`, `agent`, `grok`, or `kimi`

`skills/fresh-consult/references/model-and-invocation.md:66` (same list at `skills/agent-delegate/references/model-and-invocation.md:34`,
`skills/model-consensus/references/model-and-invocation.md:53`)

Direct probe of that tracked module from disk with explicit empty catalogs:

```text
FAIL 'deepseek r1 high'  -> ModelResolutionError: could not infer runtime from 'deepseek r1 high'; name claude, codex, agent, grok, or kimi
FAIL 'glm 4.6 high'      -> ModelResolutionError: could not infer runtime from 'glm 4.6 high'; name claude, codex, agent, grok, or kimi
FAIL 'qwen3 max'         -> ModelResolutionError: could not infer runtime from 'qwen3 max'; name claude, codex, agent, grok, or kimi
FAIL 'llama high'        -> ModelResolutionError: could not infer runtime from 'llama high'; name claude, codex, agent, grok, or kimi
```

Repo-wide, `git grep -i -e deepseek -e qwen -e llama -- 'skills/*'` returns nothing (exit 1); the only
DeepSeek/GLM mentions in the repository are in `docs/` research archives.

Why it matters: the user's stated reason for asking is that he now runs DeepSeek and GLM as parents. No
skill in this slice can name a DeepSeek/GLM model as a reviewer, and no skill says what a parent in that
position should do.

Effect: **breaks** for the request "get a second opinion from another open-source model". The failure is
loud and safe (the resolver raises instead of substituting), but the parent has to invent the lane
itself. Harmless for the five vendor lanes.

### F3: `stepwise` contradicts the other three skills about Sonnet and Haiku

Exact quotes, same repo, same week:

> - `sonnet` and `haiku` are not supported by this repo's subprocess doctrine;
>   ask for a supported Claude choice instead of silently running them.

`skills/fresh-consult/references/model-and-invocation.md:99`-`100`

> user names Sonnet or Haiku, fail loud and ask for a supported Claude choice.

`skills/fresh-consult/references/model-and-invocation.md:155`; identical at `skills/model-consensus/references/model-and-invocation.md:120`

versus:

> --settings '{"disableAllHooks":true}' --model haiku \

`skills/stepwise/references/session-resume.md:402` (also `:408`, `:414`)

The code agrees with the smoke test, not the doctrine: `skills/stepwise/scripts/test_run_stepwise.py:364`
passes `"--model", "haiku"`, and `skills/_shared/model_resolution.py:584`-`585` raises
`unsupported Claude family: sonnet` / `haiku` for the resolver on those same names.

Why it matters: a parent that reads only `fresh-consult` will refuse a request the repo's own Stepwise
verification block and tests execute. The audit reader cannot tell which file is authoritative.

Effect on an open-source parent: **degrades**. A DeepSeek/GLM parent is the most likely actor to follow
the written doctrine literally and refuse a `haiku`/`sonnet` reviewer, then be unable to explain why
`stepwise` still ships commands that use it.

### F4: `codex-review-yolo` is a hard-pinned external profile that refuses any other profile

Exact quote:

> - **Run codex with `-p yolo` explicitly.** The profile carries gpt-6-astra + xhigh reasoning + fast service tier + `danger-full-access` sandbox. Any other profile changes the contract.

`skills/codex-review-yolo/SKILL.md:46`

> Require `gpt-6-astra`, `xhigh`, `fast`, and `danger-full-access`.

`skills/codex-review-yolo/SKILL.md:81` (gate; `skills/codex-review-yolo/SKILL.md:151` re-states
"`-p yolo` — the profile. Non-negotiable.")

Why it matters: this is the one place in the slice where a concrete model *is* the deliverable, and the
skill says so. It runs a separate `codex` process with its own profile file
(`skills/codex-review-yolo/SKILL.md:80`), so the parent's own model is irrelevant to the invocation.

Effect: **harmless** for every parent, including DeepSeek/GLM/Fugu, because the pin is deliberate,
opt-in, and cross-process. The only parent-dependent failure is the precondition: `skills/codex-review-yolo/SKILL.md:42`
— "`codex` is not installed on the host — `which codex` returns nothing. Stop and tell the user."

### F5: `agent-watcher`'s only worked model examples are Claude aliases

Exact quote:

> - **Pin the watcher model he named.** "Use Sonnet subagents" means every
>   watcher runs on Sonnet, for the whole run. Never switch models for cost.
>   Say plainly when effort inherits.

`skills/agent-watcher/SKILL.md:51`-`53`

> - "Run the watcher skill, use Opus subagents." "Watch all my sessions."

`skills/agent-watcher/SKILL.md:62`

> "started": "...", "watcher_model": "sonnet", "watcher_effort": "inherits parent",

`skills/agent-watcher/references/state-and-ledger.md:28`

The host matrix gives Claude the alias lever and Codex the model-id lever, but only the Claude row names
concrete models:

> | Claude Code | Agent tool, clean subagent | `model` alias per call (`opus`, `sonnet`); effort cannot be pinned per call and inherits the parent | ...

`skills/agent-watcher/references/runtime-notes.md:102`

> | Codex | `spawn_agent` with `fork_turns: "none"` | `model` and `reasoning_effort` per spawn; pins can expire when a child is unloaded, so keep checks short | ...

`skills/agent-watcher/references/runtime-notes.md:103`

Why it matters: the instruction "pin the model he named" is host-blind in the skill prose and host-aware
only in a table row. The slice's own facts file says a Codex child's provider is copied from the parent
turn and the slug must be catalog-tagged, typically only `gpt-5.6-*`:

> | **Cross-provider** child | ... | **No** through `model` — the child's provider is copied from the parent turn. ...

`skills/_shared/native-child-capabilities.md:27`

Effect on a Fugu-profile Codex parent: **degrades**. "Use Sonnet subagents" (the skill's own example) is
not reachable as a Codex native spawn under those facts. On a Prime/DeepSeek parent the same example
degrades to "pick something in this installation's catalog", which the skill does correctly ask for at
`skills/agent-watcher/SKILL.md:79` — "Resolve the watcher model from his words and the host's pin facts".

### F6: A native child inherits the parent's model unless the pin is explicit — and no skill in this slice says so

Exact quote:

> A native child normally inherits the parent's model and thinking level. That
> inheritance is the whole cost question. An unpinned native child runs the
> parent's model on whatever you gave it, so bulk reading and long implementation
> turns land on the most expensive model in the run.

`skills/_shared/agent-orchestration-policy.md:86`-`91`

The same warning ends the capabilities file: `skills/_shared/native-child-capabilities.md:80`-`81` —
"An unpinned native child is not a cheap lane: it runs the parent's model on whatever you gave it."

Why it matters: this is the actual behavior a DeepSeek/GLM/Fugu parent will hit, and it lives only in
`_shared`. Ten skills in the slice say "prefer a clean native child of the active host" without repeating
the inheritance rule or requiring a pin.

Effect: **degrades** in a specific way. Every review skill in this slice still runs, and the review is
real, but the reviewer is the parent's own model. For a DeepSeek/GLM/Fugu parent that means a
review-of-myself-by-myself unless the parent knows to open an external vendor lane. Concrete anchors:
`skills/fresh-consult/SKILL.md:15`, `skills/model-consensus/SKILL.md:64`-`69`, `skills/plan-audit/SKILL.md:75`-`79`,
`skills/exhaustive-code-review/SKILL.md:48`-`52`.

### F7: `stepwise`'s external lane supports four runtimes; the other three skills support five

Exact quote:

> - `execution_defaults.step.runtime` - `claude`, `codex`, `grok`, or `kimi`

`skills/stepwise/references/model-and-effort.md:15`

The same four-value list is enforced in code — `skills/stepwise/scripts/run_stepwise.py:1710` and `:1732`
and `:1754` and `:1770` all use `choices=["claude", "codex", "grok", "kimi"]` — while the shared resolver
accepts `agent` too (`skills/_shared/model_resolution.py:22`) and the other three skills list five
(`skills/fresh-consult/references/model-and-invocation.md:66`, `skills/agent-delegate/references/model-and-invocation.md:34`,
`skills/model-consensus/references/model-and-invocation.md:53`).

Why it matters: a parent that learned its lane list from any sibling skill will hand an invalid `--runtime`
to the only script in the slice, or will silently drop Cursor Agent as a critic option.

Effect: **degrades**. Provider choice for a Stepwise critic is narrower than the slice claims and the
documentation does not say the narrowing is intentional. `skills/stepwise/scripts/run_stepwise.py` also
requires `--model` and `--effort` (`required=True` for both on `step-spawn`), so the script never invents
a model; only the prose default in F1 does.

### F8: The four cynical/exhaustive review skills ban external reviewer lanes outright — by design

Exact quotes:

> - Do not invoke external agent, delegation, consult, or review skills as the
>   review mechanism.

`skills/cynical-code-review/SKILL.md:77`-`78`; word-identical at `skills/cynical-architecture-review/SKILL.md:82`-`83`
and `skills/cynical-cruft-removal/SKILL.md:86`-`87`

> - Do not manually spawn `codex`, `claude`, `agent`, or other coding-harness
>   executables.

`skills/exhaustive-code-review/SKILL.md:60`-`61`

Why it matters: these skills contain **zero** model, effort, or profile tokens (`rg` over their four
directories returns no model-family hit). Their only reviewer mechanism is a clean native child, which
per F6 runs the parent's model.

Effect: **already generic** and **harmless** — nothing here breaks for a DeepSeek/GLM/Fugu parent. The
truthful caveat is the inverse of the user's hypothesis: these skills work fine and cannot give him
provider diversity, because diversity is explicitly out of scope for them.

### F9: What actually fires without a user command in this slice is one skill plus a goal-prompt template

Exact evidence, `allow_implicit_invocation` per skill metadata:

- `skills/fresh-consult/agents/openai.yaml:7` — `false`
- `skills/model-consensus/agents/openai.yaml:7` — `false`
- `skills/stepwise/agents/openai.yaml:7` — `false`
- `skills/plan-audit/agents/openai.yaml:7` — `false`
- `skills/plan-implement/agents/openai.yaml:7` — `false`
- `skills/cynical-code-review/agents/openai.yaml:7`, `skills/cynical-architecture-review/agents/openai.yaml:7`, `skills/cynical-cruft-removal/agents/openai.yaml:7`, `skills/exhaustive-code-review/agents/openai.yaml:7` — `false`
- `skills/codex-review-yolo/` has no `agents/openai.yaml`; its own description scopes it to "the user explicitly asks for `codex -p yolo`" (`skills/codex-review-yolo/SKILL.md:25`)
- `skills/agent-watcher/agents/openai.yaml:7` — `false`
- `skills/agent-delegate/agents/openai.yaml:7` — `true` (the one exception)

The pinned lanes are reached without a model choice only through prompt text a parent copies into a goal:

> Use `$codex-review-yolo` as a blind review of the final diff and receipts. Do not provide the expected verdict.

`skills/prompt-authoring/references/codex-goal-prompts.md:181`

> Use `$model-consensus` with `opus 4.7 max` and `gpt-6-astra xhigh` to decide the plan shape.

`skills/prompt-authoring/references/codex-goal-prompts.md:306`

Why it matters: it answers the "explicitly selected versus self-selecting" question with file evidence.
In this slice, selection is opt-in; the automatic pins live in goal-prompt templates, which are outside
the slice but are the realistic path by which a DeepSeek/GLM/Fugu parent would land on `opus 4.7 max`.

Effect: **degrades** only through the copied template. `agent-delegate` at `true` is the one place the
harness may reach an external lane on its own; it is an editful-worker adapter, not a reviewer.

### F10: The Codex default hard-fails, rather than degrading, when the local catalog lacks that exact id

Exact quote:

> For ordinary Codex model ids, inspect `codex debug models` when needed and
> choose an available identifier with the same family and exact version.

`skills/fresh-consult/references/model-and-invocation.md:149`-`150` (parallel at `skills/stepwise/references/model-and-effort.md:91`-`94`)

Probe of the tracked resolver with a non-empty catalog that does not carry `gpt-6-astra`:

```text
FAIL 'codex'  -> ModelResolutionError: 'codex' did not match an available Codex model with the same family and exact version; candidate was 'gpt-6-astra'
FAIL 'astra'  -> ModelResolutionError: 'astra' did not match an available Codex model with the same family and exact version; candidate was 'gpt-6-astra'
```

Why it matters: on a Codex installation whose catalog is built around profiles rather than OpenAI slugs,
the documented default is unreachable and the flow stops instead of falling back to the parent's
provider or to the only model the host actually has.

Effect: **degrades**. Failing loud is the correct behavior, but it puts the whole model choice back on a
parent that may be a DeepSeek/GLM model with no repo guidance for that case. Same-family substitution is
deliberately refused (`skills/_shared/model_resolution.py:675`-`676` compares exact equality only).

### F11: Fugu is treated as a child lane only; a Fugu *parent* is nowhere in the slice

Exact quote:

> - `fugu high`, or
>   `fugu-ultra xhigh` implies `runtime=codex`.

`skills/fresh-consult/references/model-and-invocation.md:95`-`96`

> When an external Codex lane uses Fugu, its execution block also stores
> `codex_profile` as `fugu` or `fugu-ultra`.

`skills/stepwise/references/model-and-effort.md:26`-`27`

Every Fugu mention in this slice is a destination for a delegated child
(`skills/fresh-consult/references/model-and-invocation.md:151`-`152`, `skills/agent-delegate/SKILL.md:42`,
`skills/model-consensus/references/model-and-invocation.md:241`-`242`, `skills/stepwise/references/session-resume.md:367`-`369`).
No file states what changes when the *parent* is itself a Fugu-profile Codex: that its provider differs
from OpenAI, that a native child will inherit that provider
(`skills/_shared/native-child-capabilities.md:27`), or that the `gpt-6-astra` default is a different
provider from the parent.

Effect on a Fugu-profile Codex parent: **degrades**. The mechanics all still work — Fugu is a Codex CLI
host and every Codex-native instruction in the slice applies — but the parent must derive the provider
consequence from `_shared` rather than from the skill it selected.

### F12: Not every pinned token in the slice is a default; two are deliberate doc examples

Exact quotes, both inert example text rather than instructions to the parent:

> Model G: "Fugu Ultra xhigh" -> runtime=codex, model=fugu-ultra, codex_profile=fugu-ultra, effort=xhigh

`skills/model-consensus/references/model-and-invocation.md:156` (mirrored at `skills/fresh-consult/references/model-and-invocation.md:185`,
`skills/agent-delegate/references/model-and-invocation.md:196`)

> - "use Claude Fable 5.1 high for steps and Codex gpt-6-astra xhigh for critic"

`skills/stepwise/references/model-and-effort.md:53` (a list of "Acceptable shapes in the user's prompt")

And the smoke-test block pins a cheaper model on purpose:

> behavior does not depend on model choice.

`skills/stepwise/references/session-resume.md:395`-`396`

Why it matters: a token inventory alone would count these as model pins. They are examples, and the
smoke test explicitly says the model is substitutable. Reporting them as hard-codes would overstate the
hypothesis.

Effect: **harmless** for every parent. Listed here to keep the inventory honest and to show that the
slice's concrete pins split into three different categories: fire-by-default (F1), deliberate opt-in
contract (F4), and inert example (F12).

## Model/host reference inventory

Category key: **default** = fires without a user model choice inside a selected lane; **opt-in** = part of
a deliberately selected lane's contract; **example** = illustrative text; **parent-identity** = assumes
something about the running parent or its host.

| path:line | quoted token | category | verdict for an open-source-model parent |
|---|---|---|---|
| `skills/fresh-consult/references/model-and-invocation.md:123` | `use gpt-6-astra` (Codex lane, no model named) | default (child-model pin, external) | degrades — silent vendor default; unreachable if the id is absent locally |
| `skills/fresh-consult/references/model-and-invocation.md:125` | `effort_source=preference_default` for `xhigh` | default | degrades — same |
| `skills/fresh-consult/references/model-and-invocation.md:68` | `gpt-6-astra` | default | degrades |
| `skills/fresh-consult/SKILL.md:101` | `gpt-6-astra` | default | degrades |
| `skills/agent-delegate/SKILL.md:93` | `gpt-6-astra` / `kimi-code/k3` | default | degrades |
| `skills/agent-delegate/references/model-and-invocation.md:37` | `gpt-6-astra` | default | degrades |
| `skills/model-consensus/references/model-and-invocation.md:55` | `gpt-6-astra` | default | degrades |
| `skills/stepwise/references/model-and-effort.md:23`-`24` | `gpt-6-astra` / `xhigh` | default | degrades |
| `skills/fresh-consult/references/model-and-invocation.md:70`-`71` | `encoded-in-model` / Astra `xhigh` / Kimi `max` | default (effort) | degrades — Kimi `max` is a real default on that lane |
| `skills/_shared/model_resolution.py:24`-`28` | `PREFERRED_CODEX_MODEL`/`PREFERRED_CODEX_EFFORT`/`PREFERRED_GROK_MODEL`/`PREFERRED_KIMI_MODEL`/`KIMI_DEFAULT_EFFORT` | default (code constants) | degrades — the defaults are executable, not just prose |
| `skills/codex-review-yolo/SKILL.md:46` | `-p yolo` = `gpt-6-astra` + `xhigh` + fast tier + `danger-full-access` | opt-in (external profile pin) | harmless — opt-in, cross-process, parent-model independent |
| `skills/codex-review-yolo/SKILL.md:81` | `Require gpt-6-astra, xhigh, fast, and danger-full-access` | opt-in | harmless |
| `skills/agent-watcher/SKILL.md:51`-`52` | `"Use Sonnet subagents"` | parent-identity (host alias assumption) | degrades — Claude alias only; not reachable on a Fugu/Codex or unauthenticated Prime host |
| `skills/agent-watcher/SKILL.md:62` | `use Opus subagents` | parent-identity | degrades — same |
| `skills/agent-watcher/references/runtime-notes.md:102` | `model` alias per call (`opus`, `sonnet`) | example (host matrix) | harmless — correctly labeled per-host |
| `skills/agent-watcher/references/runtime-notes.md:103` | `model` and `reasoning_effort` per spawn | example (host matrix) | harmless — no model named |
| `skills/agent-watcher/references/state-and-ledger.md:28` | `"watcher_model": "sonnet"` | example (ledger shape) | harmless — schema example |
| `skills/stepwise/references/session-resume.md:402` | `--model haiku` | example (smoke test) | degrades — contradicts F3 doctrine; model is substitutable per `:395` |
| `skills/stepwise/references/session-resume.md:420` | `--model gpt-6-astra -c model_reasoning_effort='"low"'` | example (smoke test) | harmless |
| `skills/stepwise/references/session-resume.md:439` | `--model grok-4.6 --effort low` | example (smoke test) | harmless |
| `skills/stepwise/references/session-resume.md:463` | `-m kimi-code/k3` | example (smoke test) | harmless |
| `skills/stepwise/scripts/test_run_stepwise.py:364` | `"--model", "haiku"` | example (test fixture) | degrades — locks the contradiction in F3 |
| `skills/model-consensus/references/model-and-invocation.md:156` | `fugu-ultra` / `codex_profile=fugu-ultra` | example (mapping table) | harmless |
| `skills/stepwise/references/model-and-effort.md:53`-`61` | Fable 5.1 / gpt-6-astra / Luna / Terra / Fugu | example (accepted prompt shapes) | harmless |
| `skills/model-consensus/references/examples.md:8` | `Claude Opus 4.7 xhigh and Codex gpt-6-astra xhigh` | example (user prompt) | harmless |
| `skills/model-consensus/references/examples.md:33`-`34` | `Codex gpt-6-astra xhigh` / `Claude Fable 5.1 high` | example | harmless |
| `skills/model-consensus/references/examples.md:56` | `gpt-6-astra xhigh and Opus 4.7 max` | example | harmless |
| `skills/fresh-consult/SKILL.md:33`-`43` | `Ask Claude`, `clean Codex reviewer`, `Cursor Agent Composer 2.5 Fast`, `Grok Build`, `Kimi K3` | example ("When to use" triggers) | harmless — recognition examples, explicitly framed as such at `:18`-`19` |
| `skills/exhaustive-code-review/SKILL.md:38` | `external Codex/Claude/Cursor second opinion` | example (routing boundary) | harmless — routes away from this skill |
| `skills/cynical-code-review/SKILL.md:49` | `external Codex, Claude, Cursor, Grok, or Kimi second opinion` | example (routing boundary) | harmless |
| `skills/plan-audit/references/child-prompt-contract.md:10` | `` `codex`, `claude`, `agent`, `grok`, or `kimi` `` | example (prohibition list) | harmless |
| `skills/plan-implement/SKILL.md:89` | `` `codex`, `claude`, `agent`, `grok`, or `kimi` `` | example (prohibition list) | harmless |
| `skills/plan-implement/references/native-subagent-contract.md:52` | `Claude using a clean named or custom subagent` | parent-identity (host mechanism) | already generic — codes the mechanism, not a model |
| `skills/fresh-consult/references/model-and-invocation.md:40`-`42` | `For other hosts, choose the equivalent explicit clean-child and exact-resume mechanisms` | parent-identity (generic fallback) | already generic — the one place the slice handles an unnamed host |
| `skills/_shared/native-child-capabilities.md:27` | Codex cross-provider child: `No` | parent-identity (host fact) | degrades — a Fugu/Codex parent cannot pin a child to another provider via `model` |
| `skills/_shared/native-child-capabilities.md:24` | Prime child model `must be in the authenticated catalog or the spawn hard-fails` | parent-identity (host fact) | degrades — a DeepSeek/GLM parent can only spawn what the install is authenticated for |
| `skills/_shared/agent-orchestration-policy.md:86` | `A native child normally inherits the parent's model and thinking level` | parent-identity (inheritance fact) | degrades — self-review by the parent's own model unless a lane is opened |

## What already works generically

These are places that correctly inherit the parent or correctly delegate the transport decision. They
disprove the strong form of the hypothesis.

1. **Transport choice is delegated, with a stated benefit test and no transport default.**
   `skills/fresh-consult/SKILL.md:15`-`19`: "Prefer a clean native child of the active host for ordinary
   same-host review. Use the external lane when it buys a concrete provider, exact model/profile,
   lifecycle, isolation, automation, or structured-receipt benefit ... These are recognition examples,
   not a closed allowlist or an approval gate." Same shape at `skills/model-consensus/SKILL.md:64`-`69`,
   `skills/stepwise/SKILL.md:54`-`61`, `skills/agent-delegate/SKILL.md:16`-`20`.

2. **The unknown-host fallback is explicit.** `skills/fresh-consult/references/model-and-invocation.md:40`-`42`:
   "For other hosts, choose the equivalent explicit clean-child and exact-resume mechanisms. Do not claim
   a native model override, permission set, worktree, or background lifetime unless the active tool
   surface confirms it." This is exactly the instruction a DeepSeek/GLM/Fugu parent needs, and it is
   transport-neutral.

3. **No skill in this slice pins a native child to a named model as a default.** Every model override in
   the slice is either external-lane resolution or an example, and the one native-child pin
   (`agent-watcher`, F5) fires only for a model the user names. The negative instruction appears here:
   `skills/model-consensus/SKILL.md:73`-`74`, `skills/model-consensus/references/model-and-invocation.md:31`-`32`,
   `skills/stepwise/references/manifest-schema.md:84` ("`null` when native model selection is ..."),
   `skills/fresh-consult/references/model-and-invocation.md:41`.

4. **The external resolver fails loud instead of substituting.** `skills/_shared/model_resolution.py:553`-`557`
   rejects a phrase that names two runtime families; `:509`-`513` rejects two effort levels; `:666`-`672`
   rejects blocked models; `:675`-`676` requires exact family and version. Probed behaviors:
   `deepseek`/`glm` → runtime error, `sonnet`/`haiku` → unsupported family, `codex` against a
   `gpt-5.6-*`-only catalog → no-match error. Nothing is silently downgraded.

5. **The four cynical/exhaustive skills are entirely model-free.** `rg` for model families, effort
   levels, and CLI binaries over `skills/cynical-code-review`, `skills/cynical-architecture-review`,
   `skills/cynical-cruft-removal`, and `skills/exhaustive-code-review` returns no model hit. Their
   reviewer mechanism is a clean native child plus a no-edit contract and a parent diff check
   (`skills/exhaustive-code-review/SKILL.md:48`-`55`).

6. **The reviewer prompt is transport-neutral.** `skills/fresh-consult/references/consult-prompt-and-output.md:17`-`18`
   — "Send it as the native child task brief, or write it to `prompt.md` when using the external lane" —
   and `:37`-`40` put transport rationale in the parent's dispatch record, not in a child prompt that
   would have to name its own host.

7. **The repo's own plan already names this risk.** `docs/CONDUCTOR_NATIVE_TRANSPORT_PLAN_2026-08-19.md:451`
   lists "The agent reads 'native is now allowed' as 'native is now preferred' and runs bulk review on an
   unpinned parent model" as a known failure mode, with the mitigations "the pin requirement is stated in
   the same sentence as the permission" and "The N2 'pinnable' test is a hard gate, not advice." The
   skill surfaces have not fully carried that mitigation into the review slice — see F6.

## Open questions

1. **What is the actual catalog of a Fugu-profile Codex installation?** `skills/_shared/native-child-capabilities.md:24`
   says a `spawn_agent` slug "must be catalog-tagged for v2; on a typical host that is only the
   `gpt-5.6-*` family". Whether a Fugu-profile parent can spawn a `gpt-5.6-*` child, or any child at all
   outside its own provider, is not stated anywhere I read. This audit did not run `codex debug models`
   or spawn anything, so the fact is unestablished.

2. **Is the Sonnet/Haiku prohibition (F3) intentional for Stepwise's own smoke tests?** The doctrine files
   forbid it and the test fixtures use it. I could not find a tracked note that reconciles them, and I
   did not run the tests.

3. **Does `allow_implicit_invocation: true` on `agent-delegate` ever reach a reviewer?** The skill's own
   text scopes it to editful workers and routes read-only review to `$fresh-consult`
   (`skills/agent-delegate/SKILL.md:56`-`58`). I did not observe the host's routing behavior, only the
   metadata flag at `skills/agent-delegate/agents/openai.yaml:7`.

4. **Which model does a Prime child inherit when the parent is DeepSeek or GLM?** The policy states
   inheritance (`skills/_shared/agent-orchestration-policy.md:86`-`91`) and states that reach is
   per-installation (`:210`-`216`), but no file states the parent-model-to-child-model mapping for an
   open-source parent, and this audit was told not to spawn subagents, so it was not observed.

5. **Is `xhigh` reachable on a non-OpenAI child in Prime?** `skills/_shared/native-child-capabilities.md:25`
   lists `xhigh` as a valid Prime `thinking=` value and `:26` says an inherited level is silently clamped.
   Whether a DeepSeek/GLM child accepts `xhigh` is unverified here.

6. **Are the untracked `build/` copies a live surface on any machine?** They are untracked here, rejected
   as install sources by `Makefile:199`, pruned by `Makefile:236`, and absent from
   `~/.agents/skills/fresh-consult/`. They still contain `gpt-5.4` and `$code-review` text. I did not
   inspect any other machine, so I cannot state whether a stale copy is installed elsewhere.
