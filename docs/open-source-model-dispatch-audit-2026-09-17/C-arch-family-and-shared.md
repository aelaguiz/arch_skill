# Dispatch Model/Host Audit — Slice C: arch-* family, loop skills, shared doctrine

Read-only audit. No file in `/Users/aelaguiz/workspace/arch_skill` was modified.

## Scope read

Live surface read (files with model/host/effort/dispatch content in this slice):

- `skills/_shared/agent-orchestration-policy.md` (332 lines, read in full)
- `skills/_shared/native-child-capabilities.md` (82 lines, read in full)
- `skills/_shared/scope-and-convergence.md` (145 lines, read in full — no model/host references)
- `skills/_shared/model_resolution.py` (inspected: lines 1-60, 140-175, 592-700)
- `skills/_shared/depth-first-planning.md` (searched — no model/host references)
- `skills/arch-epic/SKILL.md` (462 lines, read in full), `references/model-and-effort.md` (243 lines, read in full), `references/workflow-contract.md` (lines 310-372), `references/examples.md` (lines 320-375), `references/epic-doc-contract.md` (lines 30-145, 370-380), `references/arch-step-integration.md` (lines 240-258), `references/critic-contract.md`, `references/critic-prompt.md`, `references/auto-harness-prompts.md`, `references/resume-semantics.md` (searched), `scripts/run_arch_epic.py` (searched)
- `skills/arch-step/SKILL.md` (309 lines, read in full), `references/arch-consistency-pass.md` (lines 25-78), `references/arch-review-gate.md` (lines 10-35), `references/section-quality.md` (lines 492-505), all other `references/*.md` searched for model/host tokens
- `skills/miniarch-step/SKILL.md` (searched + lines 70-92), `references/arch-auto-plan.md` (lines 65-115), `references/arch-implement-loop.md` (lines 105-150), all other references searched
- `skills/arch-mini-plan/SKILL.md` + `references/{artifact-contract,fit-and-escalation,one-pass-plan,quality-bar,shared-doctrine}.md` (searched — no model/host references)
- `skills/arch-docs/SKILL.md` (lines 80-145), `references/{arch-docs-controller,internal-evaluator,pass,scope-and-profile,cleanup-rules}.md`
- `skills/arch-flow/SKILL.md` (read in full) + `references/{detection,checklist-rules,recommendation-rules}.md` (searched — no model/host references)
- `skills/arch-skills-guide/SKILL.md` + `references/{skill-map,boundary-examples}.md` (searched — no model/host references)
- `skills/lilarch/SKILL.md` (lines 38-60), `references/{plan,finish,shared-doctrine}.md`
- `skills/bugs-flow/SKILL.md` (lines 36-90), `references/{analyze,fix,review,shared-doctrine,bug-doc-contract}.md`
- `skills/comment-loop/SKILL.md` (lines 70-90), `references/{run,review,shared-doctrine,comment-loop-controller}.md`
- `skills/audit-loop/SKILL.md` (lines 54-135), `references/{run,review,shared-doctrine,audit-loop-controller}.md`
- `skills/audit-loop-sim/SKILL.md` (lines 74-92), `references/{run,review,shared-doctrine,audit-loop-sim-controller}.md`
- `skills/north-star-investigation/SKILL.md` + all references (searched — no model/host references)
- `skills/startup-pragmatism/SKILL.md` (+ references searched — no model/host references)
- `skills/unblocker/SKILL.md` + `references/{charter-template,unblocker-evidence}.md`
- `skills/intent-police/SKILL.md` + `references/intent-police-brief.md`
- `skills/goal-loop/` (live dir exists; see F13)
- Context only (not my slice, cited for authority/ownership): `Makefile`, `README.md`

Build-surface check: `diff -rq` run for `arch-docs`, `arch-flow`, `arch-mini-plan`, `arch-skills-guide` (the four of my slice with a `build/` dir). Every compared file differs; `build/` also holds files with no live counterpart (`controller-lifecycle.md`, `model-and-runtime.md`, `arch-operating-doctrine.md`).

## Findings

### F1: The shared policy hard-defaults any Codex model choice to `gpt-6-astra` at `xhigh`

Quote:
```
## Codex model preference

Default a Codex model choice to `gpt-6-astra` at `xhigh`. Accept `astra` as
`gpt-6-astra`. When the user mentions GPT-5.6 Sol, recommend GPT-6 Astra at
`xhigh`; use Astra for a casual or accidental old-model reference. Preserve a
deliberate request to keep Sol or another exact model, and preserve explicitly
chosen effort. Do not silently change the model of an existing session.
```
Anchor: `skills/_shared/agent-orchestration-policy.md:76-82`

Why it matters: this is the only always-on model preference in the shared doctrine, and every arch/loop skill reads this file by name. It is scoped to "a Codex model choice", so it fires only when a Codex role is actually being resolved — not for native children of a non-Codex host.

Effect on a non-Astra/non-Fable/non-Codex/non-Claude parent: **harmless** — a DeepSeek/GLM parent that never chooses a Codex lane never touches this rule. The cost is that the rule offers no cheap Codex option: if such a parent does opt into one external Codex role and omits the model, it lands on the most expensive catalog model by doctrine.

### F2: `arch-epic` repeats the same Astra/`xhigh` Codex default in four live files

Quotes:
```
  load-bearing values. An omitted model on an external Codex role defaults to
  `gpt-6-astra`, and an omitted effort on that Astra role defaults to `xhigh`.
```
`skills/arch-epic/SKILL.md:189-190`
```
- accept `astra`, `luna`, and `terra` as exact Codex models and use
  `gpt-6-astra` when a Codex role omits its model; use `xhigh` when that Astra
  role also omits effort
```
`skills/arch-epic/references/model-and-effort.md:79-81` (repeated at `:125-128`, `:213-214`)
```
  `model-and-effort.md`, except an omitted Codex model defaults to
  `gpt-6-astra`, an omitted effort on that Astra role defaults to `xhigh`, and
```
`skills/arch-epic/references/epic-doc-contract.md:71-73`
```
- If an external Codex critic was selected and its model is missing, use
  `gpt-6-astra`; if that Astra critic also omits effort, use `xhigh`.
```
`skills/arch-epic/references/workflow-contract.md:321-322` (repeated at `:363-365`)

Why it matters: four independent statements of the same default make it the de-facto Codex policy for this skill family. All four sit inside the "explicit external-harness" lane, which is stated as opt-in at `skills/arch-epic/SKILL.md:41-44`.

Effect on a non-Astra/non-Fable/non-Codex/non-Claude parent: **harmless** — the external lane is only entered by deliberate selection, and the resolved mapping is printed with `model_source=default` (`model-and-effort.md:182-184`), so an open-source-model parent sees the upgrade before it runs.

### F3: `miniarch-step` is the only place in this slice that pins a model for a *native* child

Quotes:
```
- For miniarch planner and auditor roles, prefer `gpt-5.4-mini` with `xhigh`
  reasoning only when the active native tool schema can select and confirm
  both. Otherwise use the inherited native capability and do not claim the
  child used an unconfirmed model or effort.
```
`skills/miniarch-step/SKILL.md:84-88`
```
`gpt-5.4-mini` with `xhigh` reasoning is the preferred miniarch planning
profile only when the active native schema can select and confirm both. If it
cannot, use the inherited native capability and report only what the host can
confirm.
```
`skills/miniarch-step/references/arch-auto-plan.md:96-99`
```
Prefer `gpt-5.4-mini` at `xhigh` only when the active native schema can select
and confirm both model and effort. Otherwise use inherited native capability
and do not claim the preferred profile ran.
```
`skills/miniarch-step/references/arch-implement-loop.md:137-139`

Why it matters: this is a Codex-catalog model named as the preferred profile for a native child. The guard is real and repeated three times, so it cannot silently misreport.

Effect: **degrades**. On a Prime Agent parent running DeepSeek or GLM, `gpt-5.4-mini` is not in the authenticated catalog; per the shared matrix (`native-child-capabilities.md:24`, "it must be in the authenticated catalog or the spawn hard-fails") attempting it hard-fails, so the guard forces the inherited path. The child then runs the parent's model, and the doctrine offers no cheap alternative profile for that host.

### F4: The preferred miniarch pin names the model generation the shared resolver blocks, and the block is exact-id only

Quotes:
```
BLOCKED_CODEX_MODELS = frozenset({"gpt-5.4", "gpt-5.5"})
```
`skills/_shared/model_resolution.py:32`
```
- If the user says `gpt 5.4`, `gpt 5.5`, or a variant of either while choosing
  a model, do not execute it. Say that the old model is blocked and ask whether
  they meant `gpt-6-astra`.
```
`skills/arch-epic/references/model-and-effort.md:148-151`

Why it matters: `miniarch-step`'s preferred native profile (`gpt-5.4-mini`) is one generation down from a blocked model, and `_reject_blocked_codex_model` (`model_resolution.py:666-672`) compares exact ids only, so `gpt-5.4-mini` passes the block while `gpt-5.4` fails it. Two doctrine surfaces therefore disagree about whether the 5.4 generation is usable.

Effect: **degrades**. Nothing crashes on a DeepSeek/GLM parent (the pinned profile is unreachable anyway), but on a Codex-family host the resolver's block list and the miniarch preference point in opposite directions, which is a maintenance trap rather than a runtime break.

### F5: The host mapping names Codex and Claude only — 36 live `fork_turns` lines, one other-host fallback

Quotes (representative; pattern repeated verbatim in 14 live skill files):
```
- Native starting context is explicit. Codex dispatch always sets
  `fork_turns` to `"none"` for clean planner/worker/critic roles, to a positive
  count only for deliberately bounded chat context, or to `"all"` only when
  the full conversation is genuinely required. Claude uses a clean named
  subagent by default
```
`skills/arch-epic/SKILL.md:127-131`
```
- Mapping slices and each independent `review` critic default to new clean
  same-host native children. In Codex set `fork_turns: "none"`; in Claude use
  a clean named or custom subagent, not a bare conversation fork or skill
  `context: fork` shorthand.
```
`skills/audit-loop/SKILL.md:73-76`
```
- On another host, use its clean native child mechanism when available. If it
  has no such mechanism, the parent performs the same two lenses serially
  rather than inventing an external process solely for freshness.
```
`skills/arch-step/references/arch-consistency-pass.md:67-69` — the only other-host fallback in the slice

Why it matters: `rg -n 'fork_turns'` over the live slice returns 36 lines, all of them Codex/Claude mechanism statements. The dispatch blocks in `arch-step`, `miniarch-step`, `arch-docs`, `lilarch`, `bugs-flow`, `comment-loop`, `audit-loop`, `audit-loop-sim`, and `arch-epic` enumerate only those two hosts, and never say what to do on a third host. The generic resolution exists one hop away in `skills/_shared/agent-orchestration-policy.md:210-216` ("In Prime Agent, a native child is always clean — there is no fork primitive…").

Effect: **degrades**. A Prime Agent parent with a DeepSeek or GLM model reads a dispatch block that has no branch for its host and must import the Prime paragraph from the shared file. Only `arch-consistency-pass.md:67` states the fallback locally.

### F6: On Codex the child's provider is copied from the parent turn

Quote:
```
| **Cross-provider** child | **Yes** — provider is not a constraint in the spawn path. The gate is the authenticated catalog: a host logged in to two providers can spawn a child on either | **No** through `model` — the child's provider is copied from the parent turn. Reachable only through a human-installed role whose config file sets its own provider | ...
```
`skills/_shared/native-child-capabilities.md:27`
```
| Pin child **model** | `model="provider/id"` on the spawn call. Exact selector; it must be in the authenticated catalog or the spawn hard-fails | `spawn_agent(model=...)`. The slug must be catalog-tagged for v2; on a typical host that is only the `gpt-5.6-*` family | ...
```
`skills/_shared/native-child-capabilities.md:24`

Why it matters: this is the sharpest documented limit for the user's own case. On a Codex parent whose profile is Fugu, a native child's provider comes from the parent turn, so the child is a Fugu child; pinning it onto a `gpt-5.6-*` cheap model is not reachable through `model`.

Effect: **breaks** for the specific intent "pin a cheaper native child under a Fugu Codex parent". The doctrine's escape hatch is named in the same row — an external session, or a human-installed role whose own config sets the provider.

### F7: The native-child cost rationale assumes an expensive parent

Quotes:
```
A native child normally inherits the parent's model and thinking level. That
inheritance is the whole cost question. An unpinned native child runs the
parent's model on whatever you gave it, so bulk reading and long implementation
turns land on the most expensive model in the run. A child pinned to a cheaper
model bills that model instead.
```
`skills/_shared/agent-orchestration-policy.md:86-90`
```
When one fails, say which one and take the external lane for that reason. An
unpinned native child is not a cheap lane: it runs the parent's model on
whatever you gave it.
```
`skills/_shared/native-child-capabilities.md:79-81`

Why it matters: the argument for pinning a child is a cost argument built on "the parent is the most expensive model in the run".

Effect: **degrades** (the advice stays valid, the reason inverts). With DeepSeek or GLM as the parent, an unpinned child is the cheap lane, so the stated motivation for resolving a "cheap worker profile" (`agent-orchestration-policy.md:93-95`) no longer applies and the text does not say what replaces it.

### F8: `auto` modes depend on host-native goal mode, and the parity claim names only Codex and Claude

Quotes:
```
`auto` is the repeated audit loop. Native goal mode supplies the repeated turns;
this skill does not install or arm automation hooks.
```
`skills/audit-loop/SKILL.md:120-121` (same shape at `arch-docs/SKILL.md:131-132`, `comment-loop` and `audit-loop-sim` equivalents)
```
Everything above works identically on Claude Code and Codex because
`$arch-step`'s `auto-plan`, `implement-loop`, and `auto-implement` commands are native
goal-mode friendly in both runtimes.
```
`skills/arch-epic/references/arch-step-integration.md:250-252`
```
`arch-loop`, `delay-poll`, `wait`, `code-review`, ... Use native `/goal` for free-form completion,
```
`README.md:166`

Why it matters: every repeated `auto` mode in this slice has been reduced to a dependence on the host's goal mode, and the only two hosts the doctrine names are Codex and Claude. Every mode also carries an explicit bounded fallback ("Outside native goal mode, stop after one run/review cycle and print the next exact command", `skills/audit-loop/SKILL.md:131`).

Effect: **degrades**. On a Prime Agent parent with DeepSeek or GLM the loop cannot repeat; it runs one bounded pass and names the next command. Nothing fails loudly, but the mode name overstates what will happen. Whether Prime Agent's own thread-goal surface qualifies as "native goal mode" is not stated anywhere in this slice (see Open questions).

### F9: `auto` descriptions still describe the loop as a Codex/Claude capability

Quotes:
```
- The user wants to run one manual pass now or leave the audit running in Codex or Claude Code until the worthwhile work is exhausted.
```
`skills/audit-loop/SKILL.md:18` — identical wording at `skills/comment-loop/SKILL.md:18`, `skills/audit-loop-sim/SKILL.md:18`, `skills/arch-docs/SKILL.md:20`

Why it matters: these are the trigger sentences an agent matches against. They name two hosts as the condition for the loop.

Effect: **degrades**. A non-Codex, non-Claude parent reading its own skill's trigger text sees a mode it is told belongs to other hosts, even though the body would degrade gracefully.

### F10: A plan-quality rule is conditioned on the host

Quote:
```
- in Codex, it reflects two real cold-reader passes rather than one same-voice reread
```
`skills/arch-step/references/section-quality.md:500`

Why it matters: this sits in the "Strong when:" list for the consistency check — a quality bar, not a dispatch note. It defines the strong form only for Codex.

Effect: **degrades**. On a Prime/DeepSeek parent the strong bar for this section is undefined; the generic rule at `arch-consistency-pass.md:67-69` still requires two independent passes, so the requirement survives while its stated bar does not.

### F11: `arch-epic` claims cross-runtime parity for exactly two hosts

Quote:
```
Everything above works identically on Claude Code and Codex because
`$arch-step`'s `auto-plan`, `implement-loop`, and `auto-implement` commands are native
goal-mode friendly in both runtimes. The epic skill checks sub-plan doc
truth rather than external automation state.
```
`skills/arch-epic/references/arch-step-integration.md:250-253`

Why it matters: this is the skill's own statement of its portability boundary. It is true for a Fugu-profile Codex parent (still Codex) and false for any third host.

Effect: **breaks** as a written claim for a Prime/DeepSeek parent, and **degrades** in practice: the bounded-pass fallbacks keep the epic usable, but the "works identically" promise does not hold for the continuation behavior.

### F12: `build/` copies are stale, are never installed, and still contain hard Codex model pins

Quotes:
```
- `gpt-5.4`, `gpt-5.4-mini`, and any `gpt-*` or `codex-*` pattern resolve to the `codex` runtime.
```
`skills/arch-mini-plan/build/references/model-and-runtime.md:9` (live has no such file)
```
- Fresh audit children (arch-step implement-loop, miniarch-step implement-loop): Codex `gpt-5.4` `xhigh` (or `gpt-5.4-mini` `xhigh` for miniarch).
```
`skills/arch-mini-plan/build/references/model-and-runtime.md:31` — `gpt-5.4` is blocked at `skills/_shared/model_resolution.py:32`
```
`arch-loop` is the only controller whose terminal verdict comes from a fresh unsandboxed Codex `gpt-5.4` `xhigh` evaluator subprocess ... The evaluator is always Codex even when Claude hosts the Stop hook.
```
`skills/arch-mini-plan/build/references/controller-lifecycle.md:140` (duplicated in `audit-loop/build`, `audit-loop-sim/build`, `comment-loop/build`, `arch-docs/build`, `goal-loop/build`)

Why it matters for authority: `build/` is not part of the shipped surface. `Makefile:199` rejects any source path matching `*/build/*`; `Makefile:236`, `:272`, `:301`, `:339`, `:501` delete `build` directories from every install target; `Makefile:355` fails verification if a `build` directory is found installed. `README.md:181` names `arch-epic` "transport-neutral … with deliberate external modes", which matches the live files, not the build copies.

Effect: **harmless** at runtime — the stale pins never reach a host. It is a maintainer trap: the build copies are the last place where `gpt-5.4`, "always Codex", and per-skill `model-and-runtime.md` pin tables survive, and they contradict the live doctrine and the blocked-model list.

### F13: `goal-loop` has a live directory but is on the install removal list

Quotes:
```
REMOVED_SKILLS := arch-skill arch-plan codemagic-builds customerio arch-loop delay-poll wait code-review plan-swarm skill-flow codex-babysit eli10 plan-conductor goal-loop
```
`Makefile:4`
```
The source remains at `skills/goal-loop/`. It is not installed by default;
`make install` and `make remote_install` remove installed copies.
```
`README.md:358-359`

Why it matters: `skills/goal-loop/SKILL.md` and seven references are live in the tree but ship nowhere; every install target removes the installed copy first.

Effect: **harmless** for a non-Astra/non-Codex parent (the directory has no model, effort, host, or dispatch references at all). Reported because it is a live-looking surface that no host actually loads.

### F14: `unblocker` pins the required Pro consultation to GPT-6 Astra's `Pro` option

Quotes:
```
- A required Pro review means GPT-6 Astra's literal `Pro` option, never Extra
  High, xhigh, Ultra, Thinking, or another substitute. ... `$chatgpt-web`, with required
  `$browseros` usage, uses only the already-open numbered Pro profiles, such as
  Pro 1 through Pro 5 or whichever exist.
```
`skills/unblocker/SKILL.md:87-91` (mirrored at `skills/unblocker/references/charter-template.md:52-56`)
```
For a consultation with GPT-6 Astra Pro, or a Fable or Sol audit brief under
`$delegated-implementation`, ...
```
`skills/_shared/agent-orchestration-policy.md:160-161`

Why it matters: this is an external consultation lane whose target identity is a named model tier, not a transport. It is independent of the parent runtime and parent model — the consult runs in ChatGPT through BrowserOS.

Effect: **harmless** for a DeepSeek/GLM parent (the lane does not change with the parent model). It would break only if the user's Pro account were not GPT-6 Astra Pro, which is a fact about the account, not about the parent.

### F15: Fugu is already a first-class external Codex target in the shared resolver

Quotes:
```
    Fugu runs through Codex profiles so the selected provider and custom model
    catalog load from `$CODEX_HOME/<profile>.config.toml`. Ordinary Codex
    models still use `--model`.
```
`skills/_shared/model_resolution.py:149-151`
```
- "implementation worker on Codex Fugu Ultra xhigh"
```
`skills/arch-epic/references/model-and-effort.md:109`
```
- `fugu` and `fugu-ultra` are Codex profile names; preserve them as `fugu` and
  `fugu-ultra` and launch them with `codex exec -p`.
```
`skills/arch-epic/references/model-and-effort.md:132-133`
```
- resolve `fugu` and `fugu-xhigh` as Codex profiles, not model-list ids
```
`skills/arch-epic/references/model-and-effort.md:83`

Why it matters: it disproves the hypothesis that this slice cannot express a Fugu target. `codex_model_or_profile_args` (`model_resolution.py:141-161`) emits `-p <profile>`, and `arch-epic/scripts/run_arch_epic.py:1029` and `:1138` call it for the Codex worker and critic lanes.

Effect: **already generic / works**. A Fugu-profile Codex parent can be the external target of an arch-epic role table, and Fugu effort defaults (`fugu` → `high`, `fugu-ultra` → `xhigh`, `model_resolution.py:59-62`) are encoded rather than guessed.

### F16: The hypothesis's own example text is not in this slice

Quote:
```
Astra delegates to GPT-5.6 Sol high; Fable delegates to Opus 5.
```
`skills/delegated-implementation/SKILL.md:3`

Why it matters: `rg -n 'delegates to|Sol high'` over the whole live `skills/` tree returns only `skills/delegated-implementation/SKILL.md:3` and `skills/delegated-implementation/agents/openai.yaml:4`. No file in the arch-*, loop, or shared slice contains a coordinator-identity delegation rule or names a parent model as the reason for a child model.

Effect: **already generic** for this slice — the arch family's role dispatch is written as transport-first and host-relative, not as "Astra delegates to X".

## Model/host reference inventory

| path:line | quoted token (model, effort, host, profile) | category | verdict for an open-source-model parent |
|---|---|---|---|
| `skills/_shared/agent-orchestration-policy.md:78` | `Default a Codex model choice to `gpt-6-astra` at `xhigh`` | external lane | harmless (fires only when a Codex choice is made) |
| `skills/_shared/agent-orchestration-policy.md:79` | `GPT-5.6 Sol` → `recommend GPT-6 Astra at `xhigh`` | external lane | harmless |
| `skills/_shared/agent-orchestration-policy.md:160` | `GPT-6 Astra Pro, or a Fable or Sol audit brief` | external lane | harmless |
| `skills/_shared/agent-orchestration-policy.md:178` | `In Codex native multi-agent dispatch, set `fork_turns`` | parent-identity assumption | degrades (no branch for a third host) |
| `skills/_shared/agent-orchestration-policy.md:190` | `spawn_agent`, `followup_task`, `send_message` | parent-identity assumption | harmless (Codex-only primitives, labeled as such) |
| `skills/_shared/agent-orchestration-policy.md:198` | `In Claude Code, distinguish several native mechanisms` | parent-identity assumption | harmless (labeled) |
| `skills/_shared/agent-orchestration-policy.md:210` | `In Prime Agent, a native child is always clean` | doc example / host facts | already generic (the Prime paragraph) |
| `skills/_shared/agent-orchestration-policy.md:320-329` | `An independent Codex review normally uses a clean native child`; `A Claude cold review uses a clean named subagent` | doc example | already generic (illustrative; says so at `:331`) |
| `skills/_shared/native-child-capabilities.md:24` | `is only the `gpt-5.6-*` family` | child-model pin (facts) | breaks for a Fugu Codex parent pinning a native child |
| `skills/_shared/native-child-capabilities.md:25` | `thinking=` / `reasoning_effort=` / frontmatter `effort:` with `low, medium, high, xhigh, max` | child-model pin (facts) | degrades (effort pinning is host-dependent) |
| `skills/_shared/native-child-capabilities.md:27` | `the child's provider is copied from the parent turn` | child-model pin (facts) | breaks for cross-provider native pins on Codex |
| `skills/_shared/native-child-capabilities.md:28` | `fork_turns`: `none`, `all`, positive integer | parent-identity assumption | harmless (host fact, labeled) |
| `skills/_shared/native-child-capabilities.md:80` | `An unpinned native child is not a cheap lane` | doc example | degrades (reason inverts for a cheap parent) |
| `skills/_shared/model_resolution.py:24` | `PREFERRED_CODEX_MODEL = "gpt-6-astra"` | child-model pin (code) | harmless unless a Codex lane is selected |
| `skills/_shared/model_resolution.py:25` | `PREFERRED_CODEX_EFFORT = "xhigh"` | child-model pin (code) | harmless unless a Codex lane is selected |
| `skills/_shared/model_resolution.py:32` | `BLOCKED_CODEX_MODELS = frozenset({"gpt-5.4", "gpt-5.5"})` | child-model pin (code) | harmless; conflicts with F3/F4 |
| `skills/_shared/model_resolution.py:54-62` | `_FUGU_EFFORTS` / `"fugu-ultra": "xhigh"` | external lane (code) | already generic (Fugu is supported) |
| `skills/_shared/model_resolution.py:141-161` | `codex_model_or_profile_args` → `["-p", codex_profile]` | external lane (code) | already generic |
| `skills/_shared/model_resolution.py:284-300` | `"codex" -> codex / gpt-6-astra / xhigh`; `"Fugu Ultra xhigh" -> codex / profile fugu-ultra` | doc example (code docstring) | harmless |
| `skills/arch-epic/SKILL.md:189-192` | ``gpt-6-astra``, ``xhigh``, `kimi-code/k3`, `max`, `grok-4.6` | external lane | harmless (opt-in lane) |
| `skills/arch-epic/SKILL.md:105` | ``$codex-review-yolo`` / `the exact external `yolo` profile` | external lane | harmless (explicit selection) |
| `skills/arch-epic/SKILL.md:127-134` | `Codex dispatch always sets `fork_turns``; `Claude uses a clean named subagent` | parent-identity assumption | degrades |
| `skills/arch-epic/SKILL.md:253` | `broad `xhigh` or `max` planner/worker runs` | doc example (timing) | harmless |
| `skills/arch-epic/SKILL.md:401-404` | `--runtime claude|codex|grok|kimi`, `--effort`, `[--codex-profile <profile>]` | external lane (CLI) | already generic (Fugu reachable) |
| `skills/arch-epic/references/model-and-effort.md:9` | `An external Claude, Codex, Grok, or Kimi process` | external lane | already generic |
| `skills/arch-epic/references/model-and-effort.md:43-45` | `epic_planner: claude fable 5.1 high` / `implementation_worker: codex gpt-6-astra xhigh` / `critic: codex gpt-6-astra xhigh` | doc example | harmless (example table) |
| `skills/arch-epic/references/model-and-effort.md:79-81` | `use `gpt-6-astra` when a Codex role omits its model; use `xhigh`` | external lane | harmless |
| `skills/arch-epic/references/model-and-effort.md:83` | `resolve `fugu` and `fugu-xhigh` as Codex profiles` | external lane | already generic |
| `skills/arch-epic/references/model-and-effort.md:87-88` | `model=kimi-code/k3`; `default an omitted Kimi effort to `max`` | external lane | harmless |
| `skills/arch-epic/references/model-and-effort.md:106-113` | `"implementation worker on Codex gpt-6-astra xhigh"`, `"critic on Terra high"`, `"codex gpt-6-astra high everywhere"` | doc example (accepted phrasing) | harmless |
| `skills/arch-epic/references/model-and-effort.md:123-128` | `astra`, `luna`, `terra` normalize to `gpt-6-astra` … `xhigh` | external lane | harmless |
| `skills/arch-epic/references/model-and-effort.md:132-133` | `launch them with `codex exec -p`` | external lane | already generic |
| `skills/arch-epic/references/model-and-effort.md:148-151` | `gpt 5.4`, `gpt 5.5` … `blocked` | external lane | harmless |
| `skills/arch-epic/references/model-and-effort.md:157-160` | `fugu` defaults to `high`; `fugu-ultra` defaults to `xhigh` | external lane | already generic |
| `skills/arch-epic/references/model-and-effort.md:182-191` | resolved-mapping table incl. `model_source=default`, `effort_source=preference_default` | doc example | already generic (makes defaults visible) |
| `skills/arch-epic/references/model-and-effort.md:196` | `Do not ask for a model table merely to use capable native children` | doc example | already generic |
| `skills/arch-epic/references/model-and-effort.md:213-214` | `A Codex role with no model uses gpt-6-astra, and that Astra role uses xhigh` | external lane (ask-once text) | harmless |
| `skills/arch-epic/references/model-and-effort.md:242` | `Apply the Codex preference in `../../_shared/agent-orchestration-policy.md`` | external lane | harmless |
| `skills/arch-epic/references/workflow-contract.md:321-326` | `use `gpt-6-astra`; if that Astra critic also omits effort, use `xhigh``; `Do not ask for model values for an ordinary capable native critic` | external lane | harmless |
| `skills/arch-epic/references/workflow-contract.md:358-359` | `In Codex set `fork_turns: "none"`. In Claude use a clean named subagent` | parent-identity assumption | degrades |
| `skills/arch-epic/references/epic-doc-contract.md:37-40` | `critic_runtime: null \| claude \| codex \| grok \| kimi`; `critic_model`; `critic_effort`; `models_sha256` | external lane (schema) | harmless (null for native) |
| `skills/arch-epic/references/epic-doc-contract.md:71-75` | `an omitted Codex model defaults to `gpt-6-astra` … `kimi-code/k3` at `max`` | external lane | harmless |
| `skills/arch-epic/references/epic-doc-contract.md:101-118` | `claude fable 5.1 high` / `codex gpt-6-astra xhigh` ×2 | doc example | harmless |
| `skills/arch-epic/references/examples.md:13-21` | `Use claude fable-5.1 high for the critic.` / `critic_model: claude-fable-5-1` | doc example | harmless |
| `skills/arch-epic/references/examples.md:331-338` | `epic_planner -> native, clean, new child` … `For Codex native dispatch, each new role uses `fork_turns: "none"` ` | doc example | already generic (native path, no model) |
| `skills/arch-epic/references/examples.md:360-361` | `planner Claude Fable 5.1 high, implementation Codex gpt-6-astra xhigh` | doc example | harmless |
| `skills/arch-epic/references/arch-step-integration.md:250-252` | `works identically on Claude Code and Codex` | parent-identity assumption | breaks as a claim; degrades in practice |
| `skills/arch-epic/references/critic-contract.md:15` | `Prefer the active host's native child; use an external Claude, Codex, Grok, or Kimi` | external lane | already generic |
| `skills/arch-epic/references/resume-semantics.md:67-71` | `For a Kimi external role … `kimi -r <exact-session-id>`` | external lane | harmless |
| `skills/arch-epic/references/auto-harness-prompts.md:5` | `Same-host roles normally use native children.` | doc example | already generic |
| `skills/arch-step/SKILL.md:93-94` | `In Codex, set `fork_turns: "none"`; in Claude Code, use clean named or custom subagents` | parent-identity assumption | degrades |
| `skills/arch-step/references/arch-consistency-pass.md:64-69` | `In Codex, create each explorer with `fork_turns: "none"` … `On another host, use its clean native child mechanism when available.` | parent-identity assumption + fallback | already generic (only explicit third-host fallback) |
| `skills/arch-step/references/section-quality.md:500` | `in Codex, it reflects two real cold-reader passes` | parent-identity assumption (quality bar) | degrades |
| `skills/arch-step/references/arch-review-gate.md:21-24` | `another provider, exact model/profile, durable session …` | external lane | already generic |
| `skills/miniarch-step/SKILL.md:84-88` | ``gpt-5.4-mini`` with `xhigh` | **child-model pin (native)** | degrades |
| `skills/miniarch-step/SKILL.md:74-76` | `In Codex, set `fork_turns: "none"`; in Claude Code, use clean named or custom subagents` | parent-identity assumption | degrades |
| `skills/miniarch-step/references/arch-auto-plan.md:82-83` | `In Codex, set `fork_turns: "none"`. In Claude Code, …` | parent-identity assumption | degrades |
| `skills/miniarch-step/references/arch-auto-plan.md:96-99` | `preferred miniarch planning profile only when the active native schema can select and confirm both` | **child-model pin (native)** | degrades |
| `skills/miniarch-step/references/arch-implement-loop.md:116-117` | `In Codex, set `fork_turns: "none"`. In Claude Code, …` | parent-identity assumption | degrades |
| `skills/miniarch-step/references/arch-implement-loop.md:137-139` | `Prefer `gpt-5.4-mini` at `xhigh`` | **child-model pin (native)** | degrades |
| `skills/arch-docs/SKILL.md:92-94` | `In Codex set `fork_turns: "none"`; in Claude use a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/arch-docs/SKILL.md:20` | `The user explicitly wants `arch-docs auto` and expects native goal-mode` | parent-identity assumption | degrades |
| `skills/arch-docs/references/arch-docs-controller.md:6-9` | `Codex dispatch sets `fork_turns: "none"`, and Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/arch-docs/references/internal-evaluator.md:9-11` | `In Codex set `fork_turns: "none"`; in Claude use a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/arch-docs/references/pass.md:51-52` | `Codex uses `fork_turns: "none"`; Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/lilarch/SKILL.md:44-45` | `In Codex, start those clean children with `fork_turns: "none"`; in Claude Code, …` | parent-identity assumption | degrades |
| `skills/lilarch/references/plan.md:33-34` | `In Codex, set `fork_turns: "none"`; in Claude Code, use a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/lilarch/references/finish.md:35-36` | `In Codex use `fork_turns: "none"`; in Claude Code use a clean named or custom subagent.` | parent-identity assumption | degrades |
| `skills/bugs-flow/SKILL.md:74-75` | `In Codex set `fork_turns: "none"`; in Claude use a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/bugs-flow/references/fix.md:33-34` | `In Codex set `fork_turns: "none"`; in Claude use a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/bugs-flow/references/review.md:14-15` | `In Codex set `fork_turns: "none"`; in Claude use a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/comment-loop/SKILL.md:74-75` | `In Codex set `fork_turns: "none"`; in Claude use a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/comment-loop/SKILL.md:18` | `leave the explanatory hardening loop running in Codex or Claude Code` | parent-identity assumption | degrades |
| `skills/comment-loop/references/run.md:42-43` | `Codex uses `fork_turns: "none"`, and Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/comment-loop/references/review.md:19-20` | `Codex uses `fork_turns: "none"`; Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/comment-loop/references/shared-doctrine.md:25-26` | `In Codex mapping dispatch set `fork_turns: "none"`. In Claude use a clean … subagent` | parent-identity assumption | degrades |
| `skills/comment-loop/references/comment-loop-controller.md:8-9` | `Codex uses `fork_turns: "none"`; Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/audit-loop/SKILL.md:18` | `leave the audit running in Codex or Claude Code` | parent-identity assumption | degrades |
| `skills/audit-loop/SKILL.md:74-75` | `In Codex set `fork_turns: "none"`; in Claude use a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/audit-loop/SKILL.md:120-121` | `Native goal mode supplies the repeated turns; this skill does not install or arm automation hooks.` | parent-identity assumption | degrades |
| `skills/audit-loop/references/run.md:41-42` | `Codex uses `fork_turns: "none"`, and Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/audit-loop/references/review.md:19-20` | `Codex uses `fork_turns: "none"`; Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/audit-loop/references/shared-doctrine.md:25-26` | `In Codex mapping dispatch set `fork_turns: "none"`. In Claude use a clean … subagent` | parent-identity assumption | degrades |
| `skills/audit-loop/references/audit-loop-controller.md:8-9` | `Codex uses `fork_turns: "none"`; Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/audit-loop-sim/SKILL.md:80-81` | `In Codex set `fork_turns: "none"`; in Claude use a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/audit-loop-sim/references/run.md:40-41` | `Codex uses `fork_turns: "none"`, and Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/audit-loop-sim/references/review.md:19-20` | `Codex uses `fork_turns: "none"`; Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/audit-loop-sim/references/shared-doctrine.md:24-25` | `In Codex mapping dispatch set `fork_turns: "none"`. In Claude use a clean … subagent` | parent-identity assumption | degrades |
| `skills/audit-loop-sim/references/audit-loop-sim-controller.md:8-9` | `Codex uses `fork_turns: "none"`; Claude uses a clean named or custom subagent` | parent-identity assumption | degrades |
| `skills/unblocker/SKILL.md:87-91` | `GPT-6 Astra's literal `Pro` option`; `numbered Pro profiles` | external lane | harmless (account-dependent, not parent-model dependent) |
| `skills/unblocker/references/charter-template.md:52-56` | `Pro means GPT-6 Astra's literal `Pro` option` | external lane | harmless |
| `skills/intent-police/SKILL.md:62-65` | `Keep the same child alive for the whole run … If the host cannot keep it alive, stand up a fresh child re-anchored from the ledger` | doc example | already generic (host-agnostic fallback) |
| `skills/intent-police/SKILL.md:50-51` | `dispatch a read-only, clean-context, long-lived child` | doc example | already generic (no model or host named) |
| `skills/arch-flow/SKILL.md` (all 51 lines) | no model, effort, host, or profile token | — | already generic |
| `skills/arch-skills-guide/SKILL.md` + `references/` | no model, effort, host, or profile token | — | already generic |
| `skills/arch-mini-plan/SKILL.md` + `references/` | no model, effort, host, or profile token | — | already generic |
| `skills/north-star-investigation/**` | no model, effort, host, or profile token | — | already generic |
| `skills/startup-pragmatism/**` | no model, effort, host, or profile token | — | already generic |
| `skills/goal-loop/**` (live) | no model, effort, host, or profile token | — | already generic (but not installed, F13) |
| `skills/arch-mini-plan/build/references/model-and-runtime.md:30-31` | `Codex `gpt-5.4` `xhigh``; `(or `gpt-5.4-mini` `xhigh` for miniarch)` | child-model pin (stale build surface) | harmless at runtime (never installed) |
| `skills/*/build/references/controller-lifecycle.md:140` | `fresh unsandboxed Codex `gpt-5.4` `xhigh` evaluator subprocess … always Codex even when Claude hosts the Stop hook` | external lane (stale build surface) | harmless at runtime (never installed) |

Counts: 36 live lines reference `fork_turns` (all Codex/Claude mechanism statements; 1 file adds an other-host fallback). 3 live lines pin a native child model (`miniarch-step`). No live line in this slice pins a model to a *coordinator/parent* identity.

## What already works generically

- `skills/_shared/agent-orchestration-policy.md:36-40` states the transport preference without naming a host: "Prefer a native child of the active host for ordinary same-host work when that child can do the job."
- `skills/_shared/agent-orchestration-policy.md:42-48` defines the external lane by benefit, not by model: "a different provider, a load-bearing exact model or profile, lifecycle beyond the parent turn, a durable resumable session, worktree or process isolation, a required automation surface, or a particular structured receipt."
- `skills/_shared/agent-orchestration-policy.md:64-68` forbids claiming an unconfirmed capability: "Do not claim that a native child uses a requested model, permission set, background lifecycle, or worktree unless the current host exposes and confirms that capability."
- `skills/_shared/agent-orchestration-policy.md:218-221` generalizes across hosts: "Other hosts may expose different primitives. Preserve the clean, bounded, and full distinction even when the exact syntax differs."
- `skills/_shared/agent-orchestration-policy.md:210-216` is the Prime Agent paragraph: clean-only children, model and thinking level as ordinary spawn arguments, per-installation catalog reach, depth-1 default.
- `skills/_shared/agent-orchestration-policy.md:100-116` makes pinning a three-test decision (Reach, Grip, Durability) and says what to do when a pin fails: "When a pin cannot be made or cannot be trusted, that is a concrete benefit the external lane provides."
- `skills/_shared/native-child-capabilities.md:16-18` tells the reader to distrust the facts file: "Treat every row as a starting expectation, not a promise. Inspect the live tool schema before you rely on a capability, and believe the schema over this file when they disagree."
- `skills/arch-step/references/arch-consistency-pass.md:67-69` is the only local third-host fallback: "On another host, use its clean native child mechanism when available. If it has no such mechanism, the parent performs the same two lenses serially rather than inventing an external process solely for freshness."
- `skills/arch-epic/references/model-and-effort.md:3` puts transport before model: "Resolve transport before model settings."
- `skills/arch-epic/references/model-and-effort.md:196` and `skills/arch-epic/references/workflow-contract.md:326` both refuse to invent a model table for native children: "Do not ask for a model table merely to use capable native children." / "Do not ask for model values for an ordinary capable native critic."
- `skills/arch-epic/references/examples.md:331-334` shows the native lane resolving with no model at all: "`epic_planner -> native, clean, new child` … `critic -> native, clean, new child for every independent gate; read-only`".
- `skills/arch-step/references/arch-review-gate.md:19-24` keeps the gate parent-owned and treats another provider as a separate lane.
- `skills/arch-docs/SKILL.md:131-132` and `skills/audit-loop/SKILL.md:120-121` removed hook dependence entirely: "this skill does not install or arm automation hooks."
- Every repeated mode pairs its goal-mode path with a bounded fallback, e.g. `skills/audit-loop/SKILL.md:131`: "Outside native goal mode, stop after one run/review cycle and print the next exact command."
- `skills/intent-police/SKILL.md:62-65` writes its own host-agnostic continuity fallback: "If the host cannot keep it alive, stand up a fresh child re-anchored from the ledger."
- The shared resolver already supports the user's Fugu Codex profile lane: `skills/_shared/model_resolution.py:141-161`, `:59-62`, and `skills/arch-epic/references/model-and-effort.md:83`, `:132-133`, `:157-160`.
- `README.md:181-182` states the intended posture for this slice: "`stepwise` and `arch-epic` are transport-neutral orchestrators with deliberate external modes".

## Open questions

1. Which hosts actually have "native goal mode"? The slice names Codex and Claude (`skills/arch-epic/references/arch-step-integration.md:250-252`) and `README.md:135` says "Use Codex `/goal` or Claude Code `/goal`". Prime Agent exposes a persistent thread goal surface, but no file in this slice says whether that counts as the native goal mode these `auto` modes require. This decides whether a DeepSeek/GLM Prime parent gets a loop or a bounded pass.
2. Does the local Codex catalog contain a cheap `gpt-5.4-mini` or any non-frontier model a Fugu-profile parent could pin a native child to? `native-child-capabilities.md:24` says the v2 slug family on a typical host "is only the `gpt-5.6-*` family", and I did not run `codex debug models` (read-only audit, no installs, no command execution against the user's Codex state).
3. Is `gpt-5.4-mini` still a live Codex model at all? The resolver blocks `gpt-5.4` exactly (`model_resolution.py:32`) while `miniarch-step` prefers `gpt-5.4-mini`; nothing in the repo states whether the mini variant still exists.
4. Does a `build/` regeneration pipeline exist that would overwrite live files, or is `build/` purely abandoned output? The Makefile excludes it from every install and verify path, and no Makefile target regenerates it, but I did not search for an out-of-repo generator.
5. What is the intended cheap-native-child story for a non-Astra parent? No live file in this slice names a profile a Prime/DeepSeek/GLM parent should pin children to; `miniarch-step`'s `gpt-5.4-mini` is the only native pin and it is Codex-catalog-specific.
