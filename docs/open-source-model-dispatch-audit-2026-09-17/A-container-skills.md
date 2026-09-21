# Container / delivery dispatch-model audit

Read-only audit. No file in `/Users/aelaguiz/workspace/arch_skill` was modified.
Multi-line quotes are wrapped onto one line; words are unchanged. Line numbers are 1-based.

## Scope read

Container/delivery skills (all of `SKILL.md`, `references/`, and `agents/`):

- `skills/issue-to-pr/SKILL.md` (217 lines), `skills/issue-to-pr/references/dispatch-evidence.md` (135), `skills/issue-to-pr/agents/openai.yaml` (6)
- `skills/epic-to-prs/SKILL.md` (215 lines), `skills/epic-to-prs/references/epic-dispatch-evidence.md` (125), `skills/epic-to-prs/agents/openai.yaml` (6)
- `skills/delegated-implementation/SKILL.md` (107 lines), `skills/delegated-implementation/agents/openai.yaml` (5)
- `skills/conductor/SKILL.md` (449 lines), `skills/conductor/agents/openai.yaml` (7)
- `skills/conductor/references/`: `audit-and-send-back.md` (279), `chunking-and-parallelism.md` (86), `conductor-log-contract.md` (121), `delegation-and-monitoring.md` (224), `plan-intake-and-readiness.md` (103), `shaping-and-outcome-map.md` (83), `terra-delivery-shortcut.md` (112), `worker-prompt-contract.md` (156), `workflow-contract.md` (101)
- `skills/pr-authoring/SKILL.md` (117 lines) and its only reference `skills/pr-authoring/references/pr-body-scaffold.md` (grep for model/host tokens: no matches)
- `skills/pr-review-followthrough/SKILL.md` (182 lines)
- `skills/_shared/agent-orchestration-policy.md` (331 lines)
- `skills/_shared/native-child-capabilities.md` (81 lines)
- Supporting cross-reference (outside the assigned slice, used only to confirm provider ownership): `skills/_shared/model_resolution.py`

`skills/gh-issue-filing/` does not exist in this repo. No other files exist under any of the container skill directories.

## Assumed roles and parent identities

Role map these skills assign:

| Role | Assigned model/effort | Where |
|---|---|---|
| Planning + final review (external) | GPT-6 Astra, literal `Pro` option, Extended thinking, via `$chatgpt-web`/`$browseros` | `skills/issue-to-pr/SKILL.md:15`, `:109`; `skills/epic-to-prs/SKILL.md:115` |
| Implementation / verification worker | GPT-5.6 Sol `gpt-5.6-sol` at `high` when the parent is Astra; Opus 5 when the parent is Fable | `skills/delegated-implementation/SKILL.md:44-46` |
| Conductor worker fleet (default) | Codex `gpt-6-astra` at `xhigh` | `skills/conductor/SKILL.md:294-295`; `skills/conductor/references/delegation-and-monitoring.md:103-108` |
| `conductor terra` fleet | external `runtime=codex, model=gpt-5.6-terra, effort=xhigh` | `skills/conductor/references/terra-delivery-shortcut.md:31-35` |
| Cold verifier / cynical review readers | "new clean child on the fleet profile", never an unpinned native child | `skills/conductor/SKILL.md:165-170`; `skills/conductor/references/audit-and-send-back.md:247-251` |
| PR authoring / PR follow-through | no model named; host-neutral | `skills/pr-authoring/SKILL.md:12`, `:98`; `skills/pr-review-followthrough/SKILL.md` (no model token at all) |

Parent identities the container skills assume or name: **Astra** (`gpt-6-astra`, a Codex/Prime model) and **Fable** (a Claude model; `skills/_shared/model_resolution.py:34` defines `_CLAUDE_FAMILIES = {"fable", "opus"}`). Those two model identities gate the executive/worker split. **Codex** and **Claude** appear as host-capability names for dispatch mechanics, not as the gate. Fugu appears only as a Codex *worker* profile. **DeepSeek and GLM appear nowhere in this slice** (`rg -i -e deepseek -e '\bglm\b'` over every file listed above returns zero matches).

No file in this slice says a coordinator MUST be a specific model. The two closest statements are conditional gates: `skills/issue-to-pr/SKILL.md:18` and `skills/epic-to-prs/SKILL.md:20`. A Codex parent running `gpt-5.6-terra`, and any DeepSeek/GLM/Fugu parent, satisfies neither branch and falls into the "other dispatches" branch.

## Findings

### F1: `delegated-implementation` keys the worker model to the parent model identity

Quote (`skills/delegated-implementation/SKILL.md:44-49`):

> An Astra parent assigns implementation and verification to GPT-5.6 Sol (`gpt-5.6-sol`) at `high`. A Fable parent assigns them to Opus 5, using the user's effort choice or the harness's applicable default. These are deliberate worker selections; the general Astra preference does not replace Sol here. Honor explicit user model and effort overrides. For another parent model, use the worker choice supplied by the user or calling workflow.

Quote (`skills/delegated-implementation/SKILL.md:3`, frontmatter `description`):

> description: "Keep the parent responsible for requirements, architecture, integration, and direct review while its subagents implement, test, and repair. Used by issue-to-pr and epic-to-prs for Astra or Fable coordinators, or when the user asks for this executive/worker split on accepted work. Astra delegates to GPT-5.6 Sol high; Fable delegates to Opus 5. All skill authorship stays with the parent. Owns execution responsibilities, not a delivery lifecycle, agent launcher, read-only review, or conductor's full workflow."

Why it matters: this is the only container rule that names a concrete child model for implementation work. It is a two-branch identity switch, and the third branch has no default: line 48-49 hands the choice back to the user or the calling workflow.

Effect on a DeepSeek/GLM/Fugu parent: **degrades**. The Astra and Fable branches never fire, so the skill supplies no worker model, no effort, and no cheaper-worker default. The frontmatter line still ships "Astra delegates to GPT-5.6 Sol high; Fable delegates to Opus 5" into any router that reads skill descriptions, so a parent can read a routing rule that does not apply to it. Note the counter-evidence to the hypothesis: nothing here says "use an unpinned native child"; the unpinned native child is only what happens by omission.

### F2: `issue-to-pr` and `epic-to-prs` gate the executive/worker split on "Astra or Fable"

Quotes:

- `skills/issue-to-pr/SKILL.md:18-20`: For an Astra or Fable coordinator, apply `$delegated-implementation` throughout the work: delegate code, reproduction, tests, and repairs; personally review every deliverable and changed code line. All skill authorship stays with the
- `skills/issue-to-pr/SKILL.md:205-209`: For Astra and Fable coordinators, `$delegated-implementation` owns the worker selection, brief, direct review, and repair contract, including parent-owned skill authorship. For other dispatches, read the installed `../_shared/agent-orchestration-policy.md` and apply `$prompt-authoring` to the populated brief. Leave spawning mechanics to the active harness. Carry the
- `skills/epic-to-prs/SKILL.md:20-23`: For an Astra or Fable coordinator, apply `$delegated-implementation` across the epic. Workers implement, test, and repair; the parent owns decisions, integration, and direct review of every deliverable and changed code line. All skill authorship stays with the parent, including skill work inside a child issue.
- `skills/epic-to-prs/SKILL.md:200-205`: For Astra and Fable coordinators, `$delegated-implementation` owns worker selection, requirements briefs, direct review, and code repair. The originating coordinator retains every deliverable's acceptance and all skill authorship when assigning issues to workers; an issue handoff does not replace it with another executive. For other dispatches, read the installed `../_shared/agent-orchestration-policy.md` and apply `$prompt-authoring` to the

Why it matters: the executive/worker contract (workers code, test, and repair; the parent personally reviews every deliverable and every changed line; all skill authorship stays with the parent) is assigned **only** inside the Astra/Fable branch. Both skills route every other parent to `../_shared/agent-orchestration-policy.md` plus `$prompt-authoring`, and that policy file never says who reviews deliverables or who owns skill authorship.

Effect on a DeepSeek/GLM/Fugu parent: **degrades**. The parent keeps the delivery obligations (plan from Pro, merge-ready stop line) but loses the explicit review-and-authorship assignment, and the fallback pointer is a transport policy, not a replacement execution contract. `delegated-implementation` remains invocable by any parent when "the user asks for this division of work" (`skills/delegated-implementation/SKILL.md:15-17`), so the gap is a missing default, not a hard block.

### F3: the Pro planning/review lane is mandatory and explicitly non-substitutable

Quotes:

- `skills/issue-to-pr/SKILL.md:15-16`: its accepted scope. Use Pro for initial planning and final review; use the working agent's judgment to carry the work between them.
- `skills/issue-to-pr/SKILL.md:143-144`: user to say Pro is available again. Do not substitute another model for a required Pro review or claim a pending review passed.
- `skills/epic-to-prs/SKILL.md:151-152`: independent work remains, and wait for the user to say Pro is back. Never substitute another model for a required Pro review or count it as passed.
- `skills/issue-to-pr/SKILL.md:109-113`: Use GPT-6 Astra with the literal `Pro` option and Extended thinking through `$chatgpt-web`. Read and apply `$browseros` before BrowserOS calls. Verify `Pro` in ChatGPT's `Chat` surface: Extra High, xhigh, Ultra, Thinking, and the highest remaining setting are not Pro. Follow `$chatgpt-web` for input delivery and account switching when Pro is missing, disabled, or explicitly capped.

Why it matters: the highest-value review lane in issue-to-pr/epic-to-prs is an **external** lane chosen by route, not by parent identity. It is pinned to a concrete model and UI surface and the skills forbid substituting another model for it.

Effect on a DeepSeek/GLM/Fugu parent: **already generic** about the parent, **degrades** in practice. The lane works from any parent that can drive BrowserOS and holds a numbered Pro profile; the parent's own model is irrelevant. If Pro or BrowserOS is unavailable, the documented behavior is to pause the blocked decision and not to substitute, so a DeepSeek parent with no Pro access has no in-native review path: `skills/issue-to-pr/SKILL.md:134-144`, `skills/epic-to-prs/SKILL.md:139-152`.

### F4: the conductor's default worker fleet is Codex `gpt-6-astra` at `xhigh`

Quote (`skills/conductor/SKILL.md:294-296`, "First Move" step 6):

> parallelism, wave cap, and cold-verifier toggle. The fleet profile defaults to Codex `gpt-6-astra` at `xhigh`; a user-named provider swaps the whole fleet — Kimi to `kimi-code/k3` at `max`, Grok to `grok-4.6`, Cursor to

Quote (`skills/conductor/references/delegation-and-monitoring.md:103-108`): model/profile outside the defaults. When the fleet is Codex and the model is omitted, use `gpt-6-astra`; when that Astra lane also omits the level, use `xhigh`. When it is Kimi, use `kimi-code/k3` and default an omitted level to `max`. For Codex, accept explicit `astra`, `luna`, and `terra` as `gpt-6-astra`, `gpt-5.6-luna`, and `gpt-5.6-terra`. Ask one consolidated question for other missing execution values. The default fleet is Astra at xhigh; do not assume it is cheaper than the

Quote (`skills/conductor/SKILL.md:119-122`): from one vocabulary, and the user normally supplies them. A Codex worker with no named model defaults to `gpt-6-astra`, and an omitted level on that Astra worker defaults to `xhigh`; a Kimi worker with omitted model and level defaults to `kimi-code/k3` at `max`. Accept `astra`, `luna`, and `terra` as

Quote (`skills/conductor/references/workflow-contract.md:28-29`): cap, and cold-verifier toggle. An external Codex worker with no named model uses `gpt-6-astra`; that Astra worker uses `xhigh` when effort is omitted.

Why it matters: three files restate one default. When the user names no provider, the fleet is resolved to a specific OpenAI-family model at a specific effort, on any host.

Effect on a Fugu-profile Codex parent: **degrades**. The default names a model from a different provider than the parent profile. `skills/_shared/native-child-capabilities.md:27` states that on Codex a child's provider is copied from the parent turn and cross-provider reach is not available through `model`, and `:24` says the v2 slug must be catalog-tagged, "on a typical host that is only the `gpt-5.6-*` family". The conductor does supply the escape: verify reach and pinnability first, otherwise take `$agent-delegate` (`skills/conductor/SKILL.md:109-117`; `skills/conductor/references/delegation-and-monitoring.md:15-30`). Effect on a DeepSeek/GLM parent in Prime Agent: same shape, and better supported, because `skills/_shared/agent-orchestration-policy.md:210-216` says a Prime child's reach is "whatever that installation is authenticated for rather than the parent's own provider".

### F5: the conductor forbids bulk work on an unpinned native child, which is the only cheap lane for a cheap parent

Quotes:

- `skills/conductor/SKILL.md:36-39`: native child inherits the parent's model unless the dispatch pins its model and thinking level; a pinned child bills its own. Pin the profile or take the external lane, and never route bulk work to an unpinned native child.
- `skills/conductor/SKILL.md:116-117`: host cannot enforce. An unpinned native child runs the conductor's own profile, so pin the selected model and effort before assigning bulk reading. Honor explicit user choices in both directions.
- `skills/conductor/references/delegation-and-monitoring.md:10-13`: The cost rule is about pinning, not about transport. A native child inherits the parent's model and thinking level unless the dispatch pins them, so an unpinned native worker may not use the selected fleet profile. A pinned one bills its own model. Pin the profile or take the external lane; never route bulk work to an unpinned native child.
- `skills/conductor/references/audit-and-send-back.md:247-251`: Give it the same scope anchors. Run it on the cheap fleet profile — a whole-plan cold read is bulk reading, and an unpinned native child would put it on the conductor's own model. A one-shot with no resume is the easiest role to pin natively, because no eviction can quietly re-price it; take the external lane when this host cannot pin the profile. It may reject

Why it matters: the rule is written for a parent that is the most expensive model in the run. Its stated cost model is "an unpinned native child runs the parent's model".

Effect on a DeepSeek/GLM parent: **degrades**, and this is the strongest disproof of the hypothesis that these skills already default to native subagents. For a cheap parent, the unpinned native child is the *cheapest* lane, and the rule forbids it for all bulk work. The doctrine acknowledges the inversion once but does not act on it: `skills/conductor/references/delegation-and-monitoring.md:108` says "The default fleet is Astra at xhigh; do not assume it is cheaper than the parent." A cheap parent is left following a pinning rule designed for an expensive one, with no documented cheaper-fleet default.

### F6: Fugu is recognized only as a Codex worker profile, never as a parent identity

Quote (`skills/conductor/SKILL.md:124-128`): question only for load-bearing missing values. Provider routing remains: Codex runs GPT/GBT/OpenAI ids and Fugu profiles, Claude Code runs supported Claude models, Cursor Agent runs `composer-2.5-fast`, natural Grok wording resolves to `grok-4.6`, and Kimi runs `kimi-code/k3` with an omitted-level default of `max`. Explicit legacy Grok ids remain exact and discovery-gated.

Supporting fact (`skills/_shared/model_resolution.py:149-151`): Fugu runs through Codex profiles so the selected provider and custom model catalog load from `$CODEX_HOME/<profile>.config.toml`. Ordinary Codex models still use `--model`. — Fugu is selected by `codex -p fugu` profile, i.e. `codex_model_or_profile_args` (`skills/_shared/model_resolution.py:141-159`).

Why it matters: this is the most Fugu-aware text in the container set. It establishes that a Codex host can run a Fugu-model worker.

Effect on a Fugu-profile Codex parent: **degrades**. Nothing in the container skills asks what happens when the *parent* is the Fugu process. The provider-routing sentence lists Fugu as a worker option under Codex; the parent-side defaults (F4) still resolve to `gpt-6-astra`, and the Astra default is not on the Fugu provider (`skills/_shared/native-child-capabilities.md:27`).

### F7: `conductor terra` locks an external Codex pin and removes runtime/model/effort judgment

Quotes:

- `skills/conductor/references/terra-delivery-shortcut.md:20-23`: - This preset deliberately selects the external `$agent-delegate` lane. The exact Terra xhigh profile, dedicated-worktree continuity, durable session receipts, and downstream delivery handoffs are the benefit; do not silently replace it with a generic native child.
- `skills/conductor/references/terra-delivery-shortcut.md:31-35`: - Resolve `terra xhigh` exactly as `runtime=codex, model=gpt-5.6-terra, effort=xhigh`. Use that policy for implementation, repair, delegated verification, the cold verifier, and the three cynical review sessions. Do not ask for runtime, model, or effort and do not silently substitute another choice.
- `skills/conductor/references/terra-delivery-shortcut.md:104-107`: `SKILL.md`. A missing CLI, unsafe worktree state, unavailable review skill, GitHub authorization failure, irreducible CI failure, or real human product decision is a blocker to report, not a reason to skip a stage.

Why it matters: the preset is the strongest model pin in the container set, and it is deliberately transport-pinned, so it does not depend on the parent's identity. It also removes the agent's ability to substitute when the Codex lane is unavailable.

Effect on a DeepSeek/GLM/Fugu parent: **harmless** to the parent model (a separate `codex -p`/`--model` process carries the pin); **breaks** only when the Codex CLI or `gpt-5.6-terra` profile is missing, which the shortcut defines as a reportable blocker rather than a reason to substitute (line 104-107). It also means the preset gives a DeepSeek parent no guidance at all about which model *it* should use for its own judgment work.

### F8: the Codex default prompts assert the Astra/Fable coordinator identity

Quotes (`agents/openai.yaml:4`, single-line `default_prompt`):

- `skills/issue-to-pr/agents/openai.yaml:4` contains: "GPT-6 Astra Pro planning and final review" and "Astra and Fable coordinators apply $delegated-implementation, personally review every deliverable and changed code line, and retain all skill authorship; workers implement, test, and repair code."
- `skills/epic-to-prs/agents/openai.yaml:4` contains: "shared GPT-6 Astra Pro planning and reviews" and "Astra and Fable coordinators apply $delegated-implementation: workers code, test, and repair; the originating parent personally reviews every deliverable and changed code line and authors all skill content."
- `skills/delegated-implementation/agents/openai.yaml:4` contains: "Use Astra to GPT-5.6 Sol high or Fable to Opus 5, honoring explicit user choices and the active harness's agent mechanics."

Why it matters: `agents/openai.yaml` is a Codex-facing routing surface. It restates the adult-model identity assumption as the skill's default prompt.

Effect on a non-Astra/non-Fable parent: **harmless** on hosts that never read `agents/openai.yaml` (Prime Agent, Claude Code). Inside a Codex host — including a Fugu-profile Codex — the default prompt asserts an Astra/Fable coordinator identity the process may not have.

### F9: quote check — the Astra/Fable gate also excludes Terra, Sol, Luna, and every non-listed model

Quotes: `skills/issue-to-pr/SKILL.md:18` and `skills/epic-to-prs/SKILL.md:20` both read "For an Astra or Fable coordinator, apply `$delegated-implementation` throughout ..." / "For an Astra or Fable coordinator, apply `$delegated-implementation` across the ...". The conductor's own alias list is wider: defaults to `kimi-code/k3` at `max`. Accept `astra`, `luna`, and `terra` as `gpt-6-astra`, `gpt-5.6-luna`, and `gpt-5.6-terra`. Ask one consolidated

Why it matters: the container skills do not define what "Astra" and "Fable" are. `skills/delegated-implementation/SKILL.md:44-45` maps them to `gpt-5.6-sol` workers and Opus 5 workers, which reads as model families, not hosts. `skills/_shared/model_resolution.py:34` (`_CLAUDE_FAMILIES = {"fable", "opus"}`) supports reading Fable as a Claude family.

Effect: **degrades**. A Codex parent running `gpt-5.6-terra`, `gpt-5.6-luna`, or a Fugu profile matches neither gate branch, so it silently inherits F2's weaker fallback even though its host is Codex and it is an OpenAI-family coordinator.

## Model/host reference inventory

Category key: PID = parent-identity assumption; PIN = child-model/effort pin; EXT = external lane or external pin; DOC = doc example / historical evidence; HOST = host-capability fact. Verdict is for an open-source-model parent (DeepSeek, GLM, or a Fugu-profile Codex) that is not Astra/Fable/Codex-default/Claude.

| path:line | quoted token | category | verdict |
|---|---|---|---|
| skills/delegated-implementation/SKILL.md:3 | `Astra delegates to GPT-5.6 Sol high; Fable delegates to Opus 5` | PID + PIN | degrades - gate never fires; frontmatter still ships the routing text |
| skills/delegated-implementation/SKILL.md:44 | `An Astra parent assigns implementation and verification to GPT-5.6 Sol` (`gpt-5.6-sol`) `at` `high` | PIN | degrades - no equivalent default for another parent |
| skills/delegated-implementation/SKILL.md:45 | `A Fable parent assigns them to Opus 5` | PIN | degrades - Claude-only branch |
| skills/delegated-implementation/SKILL.md:46 | `the harness's applicable default` | PIN | already generic |
| skills/delegated-implementation/SKILL.md:47 | `These are deliberate worker selections; the general Astra preference does not replace Sol here.` | PIN | harmless - resolves an internal conflict, no host effect |
| skills/delegated-implementation/SKILL.md:48-49 | `For another parent model, use the worker choice supplied by the user or calling workflow.` | PID fallback | degrades - fallback has no default when neither supplies one |
| skills/delegated-implementation/SKILL.md:51-55 | `The active harness provides the available agents, model identifiers, capabilities, and instructions for spawning and continuing them.` | HOST | already generic |
| skills/delegated-implementation/SKILL.md:86 | `A native reader has no` `@GitHub`; `give it the worktree path and the PR link instead.` | HOST | already generic - capability, not model |
| skills/issue-to-pr/SKILL.md:3 | `GPT-6 Astra Pro planning/final review`; `Astra and Fable coordinators use delegated-implementation` | PID (description) | harmless at runtime, but asserts a coordinator identity in router metadata |
| skills/issue-to-pr/SKILL.md:15 | `Use Pro for initial planning and final review` | EXT | works from any parent; degrades only if Pro/BrowserOS is absent |
| skills/issue-to-pr/SKILL.md:18 | `For an Astra or Fable coordinator, apply` `$delegated-implementation` `throughout` | PID gate | degrades - excluded parents lose the executive/worker contract |
| skills/issue-to-pr/SKILL.md:109 | `Use GPT-6 Astra with the literal` `Pro` `option and Extended thinking through` `$chatgpt-web` | EXT | already generic w.r.t. parent model |
| skills/issue-to-pr/SKILL.md:112 | `Extra High, xhigh, Ultra, Thinking, and the highest remaining setting are not Pro` | EXT | already generic |
| skills/issue-to-pr/SKILL.md:143-144 | `Do not substitute another model for a required Pro review or claim a pending review passed.` | EXT lock | degrades - no in-native substitute documented |
| skills/issue-to-pr/SKILL.md:205-209 | `For Astra and Fable coordinators,` `$delegated-implementation` `owns the worker selection, brief, direct review, and repair contract`; `For other dispatches, read the installed` `../_shared/agent-orchestration-policy.md` | PID + fallback | degrades - policy pointer assigns no review or authorship role |
| skills/issue-to-pr/agents/openai.yaml:4 | `GPT-6 Astra Pro`; `Astra and Fable coordinators apply $delegated-implementation` | PID (Codex prompt) | harmless off Codex; asserts Astra identity inside Codex |
| skills/issue-to-pr/references/dispatch-evidence.md:25 | `verbatim quotations remain historical evidence, not current model selection.` | DOC | harmless - explicitly superseded |
| skills/issue-to-pr/references/dispatch-evidence.md:53 | `"yeah you fucking idiot 5.6 sol pro / it should always use the absolute latest and absolute most powerful model."` | DOC | harmless - historical owner correction, marked superseded |
| skills/epic-to-prs/SKILL.md:20 | `For an Astra or Fable coordinator, apply` `$delegated-implementation` `across the` | PID gate | degrades - same as issue-to-pr |
| skills/epic-to-prs/SKILL.md:115 | `Use one GPT-6 Astra Pro thread for the epic` | EXT | already generic w.r.t. parent model |
| skills/epic-to-prs/SKILL.md:152 | `Never substitute another model for a required Pro review or count it as passed.` | EXT lock | degrades - no substitute path |
| skills/epic-to-prs/SKILL.md:200-205 | `For Astra and Fable coordinators,` `$delegated-implementation` `owns worker selection... For other dispatches, read the installed` `../_shared/agent-orchestration-policy.md` | PID + fallback | degrades |
| skills/epic-to-prs/agents/openai.yaml:4 | `shared GPT-6 Astra Pro planning and reviews` | PID (Codex prompt) | harmless off Codex |
| skills/epic-to-prs/references/epic-dispatch-evidence.md:25 | `verbatim quotations remain historical evidence, not current model selection.` | DOC | harmless |
| skills/delegated-implementation/agents/openai.yaml:4 | `Use Astra to GPT-5.6 Sol high or Fable to Opus 5` | PIN (Codex prompt) | harmless off Codex; degrades inside a Fugu-profile Codex |
| skills/conductor/SKILL.md:36-39 | `A native child inherits the parent's model unless the dispatch pins its model and thinking level; a pinned child bills its own. Pin the profile or take the external lane, and never route bulk work to an unpinned native child.` | cost rule | degrades - forbids the only cheap lane for a cheap parent |
| skills/conductor/SKILL.md:103-117 | `Apply` `../_shared/agent-orchestration-policy.md` `at every worker and reviewer dispatch... Resolve the worker profile before the lane` | HOST/transport | already generic |
| skills/conductor/SKILL.md:109-112 | `Take the native lane when the profile is reachable in this host's child catalog, pinnable in both model and thinking level, durable... Otherwise take` `$agent-delegate` | HOST/transport | already generic - parent-model agnostic |
| skills/conductor/SKILL.md:120-122 | `A Codex worker with no named model defaults to` `gpt-6-astra`, `and an omitted level on that Astra worker defaults to` `xhigh`; `a Kimi worker... defaults to` `kimi-code/k3` `at` `max` | PIN default | degrades on a Fugu-profile Codex (other provider catalog) |
| skills/conductor/SKILL.md:122-123 | `Accept` `astra`, `luna`, `and` `terra` `as` `gpt-6-astra`, `gpt-5.6-luna`, `and` `gpt-5.6-terra` | PIN alias map | harmless |
| skills/conductor/SKILL.md:125 | `Codex runs GPT/GBT/OpenAI ids and Fugu profiles` | HOST/provider | already generic - the only Fugu-aware line; Fugu is a worker option only |
| skills/conductor/SKILL.md:126-128 | `Cursor Agent runs` `composer-2.5-fast`, `natural Grok wording resolves to` `grok-4.6`, `and Kimi runs` `kimi-code/k3` | PIN/provider | already generic |
| skills/conductor/SKILL.md:171-180 | `Native model, thinking level, and starting context are all explicit at dispatch. Codex states` `fork_turns`... `Prime Agent children are always clean` | HOST mechanics | already generic - keyed on host, not parent model |
| skills/conductor/SKILL.md:294-296 | `The fleet profile defaults to Codex` `gpt-6-astra` `at` `xhigh`; `a user-named provider swaps the whole fleet` | PIN default | degrades - no cheap-parent or Fugu-parent default |
| skills/conductor/references/delegation-and-monitoring.md:10-13 | `Pin the profile or take the external lane; never route bulk work to an unpinned native child.` | cost rule | degrades |
| skills/conductor/references/delegation-and-monitoring.md:15-30 | `Take the native lane when all four hold` ... `Take the external lane through` `$agent-delegate` `when any of those fails, and say which one` | HOST/transport | already generic |
| skills/conductor/references/delegation-and-monitoring.md:103-107 | `When the fleet is Codex and the model is omitted, use` `gpt-6-astra`; `when that Astra lane also omits the level, use` `xhigh`; `When it is Kimi, use` `kimi-code/k3` | PIN default | degrades on a Fugu-profile Codex |
| skills/conductor/references/delegation-and-monitoring.md:108 | `The default fleet is Astra at xhigh; do not assume it is cheaper than the` `parent.` | cost caveat | degrades - caveat recorded, default unchanged |
| skills/conductor/references/delegation-and-monitoring.md:121-128 | `A Kimi worker inherits` `$agent-delegate`'`s process contract: ` `KIMI_CODE_NO_AUTO_UPDATE=1`... `never... fall back to another provider, model, or effort.` | EXT mechanics | already generic |
| skills/conductor/references/delegation-and-monitoring.md:130-131 | `Natural` `grok`, `grok cli`, `or` `grok build` `wording resolves to` `grok-4.6` | PIN/provider | already generic |
| skills/conductor/references/workflow-contract.md:28-29 | `An external Codex worker with no named model uses` `gpt-6-astra`; `that Astra worker uses` `xhigh` `when effort is omitted.` | EXT default | harmless when the Codex lane is chosen; degrades as a default on a host without Codex |
| skills/conductor/references/terra-delivery-shortcut.md:20-23 | `This preset deliberately selects the external` `$agent-delegate` `lane... do not silently replace it with a generic native child.` | EXT lock | already generic w.r.t. parent model |
| skills/conductor/references/terra-delivery-shortcut.md:31-35 | `Resolve` `terra xhigh` `exactly as` `runtime=codex, model=gpt-5.6-terra, effort=xhigh`... `do not silently substitute another choice.` | EXT pin | works from any parent; breaks if codex/`gpt-5.6-terra` is unavailable, with no substitute allowed |
| skills/conductor/references/terra-delivery-shortcut.md:53 | `external Codex` `gpt-5.6-terra` `at` `xhigh` | EXT pin | same as above |
| skills/conductor/references/terra-delivery-shortcut.md:58 | `three` `fresh-one-shot` `Terra xhigh external sessions` | EXT pin | same as above |
| skills/conductor/references/terra-delivery-shortcut.md:70 | `a new clean external Terra xhigh repair worker` | EXT pin | same as above |
| skills/conductor/references/terra-delivery-shortcut.md:104-107 | `A missing CLI, unsafe worktree state, unavailable review skill... is a blocker to report, not a reason to skip a stage.` | EXT blocker rule | degrades - no fallback model or lane is permitted |
| skills/conductor/references/worker-prompt-contract.md:20 | `Worker profile: <model> at <thinking level>` | template | already generic |
| skills/conductor/references/worker-prompt-contract.md:62-66 | `State the authorized native delegation scope and this host's child-depth limits` ... `Do not spawn external agents: no` `$agent-delegate`, `no other external Claude, Codex, Cursor Agent, Grok, or Kimi session` | HOST/topology | already generic |
| skills/conductor/references/conductor-log-contract.md:66-70 | `Worker/handle names the lane, the pinned model and thinking level` ... `Record the profile even when it matches the fleet default` | receipt rule | already generic |
| skills/conductor/references/audit-and-send-back.md:114 | `a verification worker in a different clean session on the fleet profile` | fleet profile | degrades - fleet profile undefined for a cheap or Fugu parent |
| skills/conductor/references/audit-and-send-back.md:247-251 | `Run it on the cheap fleet profile` ... `an unpinned native child would put it on the conductor's own model` | cost rule | degrades |
| skills/conductor/references/audit-and-send-back.md:189 | `never silently switch runtime, model, or effort.` | process rule | already generic |
| skills/pr-authoring/SKILL.md:12 | `Use the host runtime's available GitHub-capable tool or connector to publish the PR.` | HOST-neutral | already generic |
| skills/pr-authoring/SKILL.md:23-24 | `Use the host agent's normal review response.` | HOST-neutral | already generic |
| skills/pr-review-followthrough/SKILL.md:86 | `Prefer repo-root` `AGENTS.md`, `CLAUDE.md`, `PR templates, review-policy files, and workflow files over memory.` | DOC | harmless - doc names, not a model pin |
| skills/_shared/agent-orchestration-policy.md:36-40 | `Prefer a native child of the active host for ordinary same-host work when that child can do the job.` | transport preference | already generic - supports the hypothesis |
| skills/_shared/agent-orchestration-policy.md:59-62 | `Honor an explicit user request for a provider, model, profile, durable session, or external consultation.` | user override | already generic |
| skills/_shared/agent-orchestration-policy.md:78-82 | `Default a Codex model choice to` `gpt-6-astra` `at` `xhigh`... `When the user mentions GPT-5.6 Sol, recommend GPT-6 Astra at` `xhigh` | PIN default | degrades on a Codex host whose provider is Fugu |
| skills/_shared/agent-orchestration-policy.md:86-91 | `A native child normally inherits the parent's model and thinking level. That inheritance is the whole cost question.` | inheritance doctrine | already generic - supports the hypothesis |
| skills/_shared/agent-orchestration-policy.md:100-116 | `Reach` ... `Grip` ... `Durability`; `Cross-provider reach is a per-installation fact, not a vendor fact` | HOST test | already generic |
| skills/_shared/agent-orchestration-policy.md:210-216 | `In Prime Agent, a native child is always clean` ... `Model and thinking level are ordinary spawn arguments, and the child's reach is whatever that installation is authenticated for rather than the parent's own provider.` | HOST fact | already generic - the strongest evidence a DeepSeek/GLM Prime parent can still pin a GPT/Claude child |
| skills/_shared/native-child-capabilities.md:24 | `The slug must be catalog-tagged for v2; on a typical host that is only the` `gpt-5.6-*` `family` | HOST fact | breaks the `gpt-6-astra` default on such a Codex host |
| skills/_shared/native-child-capabilities.md:26 | `Hard spawn failure when set explicitly; an inherited level is silently clamped` | HOST fact | breaks explicit unsupported pins (Prime) |
| skills/_shared/native-child-capabilities.md:27 | `No` `through` `model` `- the child's provider is copied from the parent turn.` (Codex) | HOST fact | breaks cross-provider native children on Codex and Claude |
| skills/_shared/native-child-capabilities.md:31 | `Depth 1 by default - a child cannot spawn its own children.` (Prime) | HOST fact | already generic - affects fanout, not model choice |
| skills/_shared/native-child-capabilities.md:56-60 | `Reach is per-installation, not per-vendor.` ... `Check the catalog before deciding; do not assume either answer.` | HOST fact | already generic |
| skills/_shared/native-child-capabilities.md:80 | `An unpinned native child is not a cheap lane: it runs the parent's model on whatever you gave it.` | cost rule | degrades - asserts the inverse of a cheap parent's economics |

## Where a DeepSeek/GLM/Fugu parent is left without guidance

1. No worker model, effort, or cheaper-worker default. `skills/delegated-implementation/SKILL.md:44-49` covers Astra and Fable only; the third branch defers to the user or the calling workflow.
2. No executive/worker role assignment. The review-every-line and parent-owns-skill-authorship duties live only in the Astra/Fable branch (`skills/issue-to-pr/SKILL.md:18-22`; `skills/epic-to-prs/SKILL.md:20-23`). The fallback pointer (`issue-to-pr:205-209`) is a transport policy.
3. The conductor's cheap-lane rule points the wrong way. `skills/conductor/SKILL.md:36-39` and `skills/conductor/references/delegation-and-monitoring.md:10-13` forbid bulk work on an unpinned native child, which for a cheap parent is the cheapest lane. No container file defines a cheap-fleet default.
4. The conductor fleet default is another provider's model. `skills/conductor/SKILL.md:294-295` and `delegation-and-monitoring.md:103-108` default to Codex `gpt-6-astra` at `xhigh`. On a Fugu-profile Codex, `skills/_shared/native-child-capabilities.md:27` says the child provider is copied from the parent turn, and `:24` limits catalog-tagged slugs on a typical host to the `gpt-5.6-*` family.
5. No substitute is permitted when the Pro or Terra lane is unavailable. `skills/issue-to-pr/SKILL.md:143-144`, `skills/epic-to-prs/SKILL.md:151-152`, and `skills/conductor/references/terra-delivery-shortcut.md:34-35` all forbid substitution; no container skill names a native lane that can replace the required external review.
6. Model aliases are defined for Codex, Claude, Cursor, Grok, and Kimi only (`skills/conductor/SKILL.md:125-128`). No container file maps a DeepSeek or GLM model into worker vocabulary.

## What already works generically

- **Transport policy is parent-model agnostic.** `skills/_shared/agent-orchestration-policy.md:36-40` prefers a native child of the active host for ordinary same-host work; `:59-62` honors an explicit user provider/model request; `:100-116` tests reach, grip, and durability before relying on a pin.
- **Prime Agent host facts are already stated generically.** `skills/_shared/agent-orchestration-policy.md:210-216`: children are always clean, model and thinking level are ordinary spawn arguments, and reach is the installation's authenticated catalog, not the parent's provider. `skills/_shared/native-child-capabilities.md:56-60` says the same: reach is per-installation, not per-vendor. A DeepSeek or GLM Prime parent can therefore pin a GPT or Claude child when that installation is authenticated for it.
- **Conductor lane selection is parent-model agnostic.** `skills/conductor/SKILL.md:109-117` and `skills/conductor/references/delegation-and-monitoring.md:15-30` choose native versus external on reach, pinnability, durability, and external-only benefit, and require naming the failed test.
- **Per-host context mechanics are keyed on host, not parent model.** `skills/conductor/SKILL.md:171-180`, `skills/conductor/references/delegation-and-monitoring.md:74-87`, `skills/_shared/agent-orchestration-policy.md:176-221`.
- **Fugu is recognized, once.** `skills/conductor/SKILL.md:125` lists Fugu profiles as a Codex provider lane, and `skills/_shared/model_resolution.py:141-159` implements profile-based Fugu selection. This is the only Fugu awareness in the container set.
- **The executive/worker contract is invocable by any parent on request.** `skills/delegated-implementation/SKILL.md:15-17`: "Use this execution contract when a calling workflow requires it or the user asks for this division of work". The user can therefore pull a DeepSeek/GLM parent into the same split; only the automatic default is missing.
- **The PR skills carry no model, host, effort, or parent-identity assumption.** `skills/pr-authoring/SKILL.md:12` ("the host runtime's available GitHub-capable tool or connector"), `:98`; `skills/pr-review-followthrough/SKILL.md` has no model token anywhere.
- **Worker briefs are parameterized, not pre-pinned.** `skills/conductor/references/worker-prompt-contract.md:20` ("Worker profile: <model> at <thinking level>"), `:62-66` (state this host's child-depth limits; no external agents).
- **Historical evidence files are marked as superseded.** `skills/issue-to-pr/references/dispatch-evidence.md:25,29-30`; `skills/epic-to-prs/references/epic-dispatch-evidence.md:22-25`. Their model quotes are evidence, not runtime rules.

## Open questions

1. **Can a Fugu-profile Codex parent reach an OpenAI-family native child?** Not established from these files. `skills/_shared/native-child-capabilities.md:24` and `:27` say the slug must be catalog-tagged for v2 and the provider is copied from the parent turn, but the file also says to verify the live tool schema over the file (`:16-18`).
2. **Are Amir's Prime Agent DeepSeek/GLM installations authenticated for the GPT and Claude catalogs?** The skills depend on this (`agent-orchestration-policy.md:212-214`), and no file records the answer; it is a per-installation fact.
3. **Does `$chatgpt-web`/`$browseros` work from a DeepSeek/GLM Prime parent?** Nothing in this slice conditions it on the parent model, but `chatgpt-web` is outside this slice, so I did not verify its preconditions.
4. **Is "Astra" a model identity or a host?** The container skills never define it. `skills/delegated-implementation/SKILL.md:44-45` pairs "Astra parent" with `gpt-5.6-sol` workers, and `skills/_shared/model_resolution.py:34` treats `fable`/`opus` as Claude families. My reading is model identity, which is why F9 matters. A maintainer statement would settle it.
5. **Was excluding Terra-from-the-gate deliberate?** `gpt-5.6-terra` is a Codex/OpenAI model this repo uses as a worker default in `conductor terra`, yet a Terra-model Codex parent matches neither the Astra nor the Fable branch of `issue-to-pr`/`epic-to-prs`.

## Finding count

9 findings (F1-F9). 68 inventory rows. Read-only: no repo file changed.
