# Open-Source Model Dispatch Support

**Date:** 2026-09-17
**Repo:** `arch_skill`
**Question answered:** how do we give the skills that dispatch to model agents full support for open-source parent models (DeepSeek, GLM, Fugu), so those skills dispatch correctly by default?
**Method:** read-only audit of the live skill surface, plus live probes of the two installed hosts. No skill file was changed.
**Raw evidence:** `docs/open-source-model-dispatch-audit-2026-09-17/` holds the five evidence files behind this report: the container-skill inventory, the review and consult inventory, the arch-* family inventory, the runtime-reality probe, and my own verified host facts.

> **Resolution (2026-09-17):** the fix plan below was superseded the same day by
> `UNNAMED_PARENT_MODEL_NATIVE_DEFAULT_PLAN_2026-09-17.md`, which was reviewed by
> Fable 5.1 (high) and then implemented across twelve files. Two things differ
> from what this document proposed. The resolver change is dropped: adding a
> `native` value to `VALID_RUNTIMES` would fail inside `run_arch_epic.py` after
> run state already exists, and the host's own child is expressed by absence
> instead. The Codex and `fork_turns` sections are deferred, because the shipped
> default needs neither. Read the plan and the skills for current behavior; read
> the rest of this document as the pre-change record.

---

## The answer in one screen

Your instinct is right about the intent and wrong about the current state.

**Right:** unless you name a model, these skills should dispatch to the active host's native children, and those children should inherit your model. That is also what the runtime does today. I proved it in this session: the parent model is `openrouter/deepseek/deepseek-v4.1-flash`, and every unpinned child I started came up on that same model.

**Wrong:** the skills do not currently say that. Nothing in the container skills tells a non-Astra, non-Fable parent what worker to use, and one skill's only rule for you is a dead end:

```text
For another parent model, use the worker choice supplied by the user or calling workflow.
```
`skills/delegated-implementation/SKILL.md:48-49`

Four things are actually broken or missing, in priority order:

1. **The executive/worker contract is gated on your model's name.** `issue-to-pr` and `epic-to-prs` give the "workers code, parent reviews every line, parent authors skills" contract only to an "Astra or Fable coordinator" (`skills/issue-to-pr/SKILL.md:18`, `skills/epic-to-prs/SKILL.md:20`). Every other parent, including every open-source parent, gets a pointer to a transport policy that assigns no review duty and no authorship duty.
2. **There is a second, executable model truth that excludes open-source models entirely.** `skills/_shared/model_resolution.py` is called as code by skills and scripts. Its runtime enum is `{"agent", "claude", "codex", "grok", "kimi"}` (`:22`). `deepseek`, `glm`, and `native` all raise `ModelResolutionError`. This is not just prose that needs a reword — it is a router that cannot name your models.
3. **The cost doctrine assumes your parent model is the most expensive thing in the run.** `conductor` says "never route bulk work to an unpinned native child" (`skills/conductor/SKILL.md:36-39`). With DeepSeek, GLM, or Fugu as the parent, the unpinned native child is the *cheapest* lane, and the rule forbids it. No file defines the inverted default.
4. **Codex cannot do what the skills assume it can.** On Codex, a child's provider is copied from the parent turn (`skills/_shared/native-child-capabilities.md:27`), so "Astra to Sol" is physically unavailable under `-p fugu` or `-p glm53`. Worse, native children only work for models whose catalog entry carries `multi_agent_version: "v2"`: your DeepSeek catalog has it, your Fugu and GLM catalogs do not.

The fix is small and lands in four places: the two `_shared` files, the shared resolver, and the container skills' execution contract. Section "The fix plan" has the ordered list.

### The direct question: will these skills call Sol or Opus on their own?

Mostly no, and that is worth stating precisely, because it changes what needs fixing.

- **No audited skill pins a native child to a named model as a default.** Every one of the 37 findings confirms this. The review and consult skills say "prefer a clean native child of the active host", which for you inherits DeepSeek, GLM, or Fugu. There is no hidden native pin to a vendor model.
- **The Astra-to-Sol and Fable-to-Opus rules do not fire for you today.** They are conditional on your model's name, so under a DeepSeek or GLM parent neither branch matches. The defect is the missing rule, not a wrong model.
- **Two real paths still land on a vendor model unnamed.** Selecting an external Codex lane and omitting the model silently resolves to `gpt-6-astra` at `xhigh` with `effort_source=preference_default` (`skills/fresh-consult/references/model-and-invocation.md:123-126`, mirrored in `agent-delegate`, `model-consensus`, and `stepwise`). And copying a goal-prompt template that already names models, such as `Use $model-consensus with opus 4.7 max and gpt-6-astra xhigh` (`skills/prompt-authoring/references/codex-goal-prompts.md:306`).
- **One skill can reach an external lane without being named.** `allow_implicit_invocation: true` appears on `skills/agent-delegate/agents/openai.yaml:7` and on no other skill in the review and consult slice. Its own text scopes it to editful workers and routes read-only review to `$fresh-consult`, so it is not a reviewer risk, but it is the one automatic hook.

So the practical exposure is narrow: keep the external-lane defaults honest, stop copying model names in goal prompts when you do not want them, and the default lane for every open-source parent is already the one you wanted.


---

## What I verified live, and what I only read

Verified by direct probe on this machine:

| Fact | Proof |
|---|---|
| Unpinned native children inherit the parent model | Four audit children admitted with `model = openrouter/deepseek/deepseek-v4.1-flash`, the same as the parent |
| An unsupported thinking level hard-fails the spawn | `thinking="medium"` on `openrouter/deepseek/deepseek-v4.1-flash` raised `RuntimeError: Requested thinking level "medium" is not supported by model ...; supported levels: low, high, xhigh` |
| Cross-provider native children work from an open-source parent | `openai-codex/gpt-5.6-luna` and `sakana/fugu-max` both admitted as native Prime children from the DeepSeek parent |
| `gpt-6-astra` does not exist in the Prime catalog | `rlm.find_models("astra")` and `rlm.find_models("gpt-6")` both return zero results. The Prime `openai-codex` catalog is `gpt-5.5`, `gpt-5.6-luna`, `gpt-5.6-sol`, `gpt-5.6-sol-1m`, `gpt-5.6-terra` |
| Partial thinking-level maps on open-source models | `~/.prime/agent/models.json`: DeepSeek `deepseek/deepseek-v4.1-flash` supports low/high/xhigh only; GLM `z-ai/glm-5.3` supports low/high/max; both Fugu entries support high/xhigh/max |
| Codex tags children per model in the catalog | `codex debug models` marks `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` as `multi_agent_version: v2`; `gpt-5.5` carries no tag. Your `~/.codex/deepseek-flash.json` tags all four DeepSeek models `v2`; `~/.codex/fugu.json`, `~/.codex/glm.json`, and `~/.codex/union-alpha.json` carry no tag |
| Codex has a per-host child-profile lever that no skill uses | The installed Codex binary reads `[agents] default_subagent_model` and `[agents] default_subagent_reasoning_effort`; your `~/.codex/config.toml` sets only `max_concurrent_threads_per_session = 7` in `[agents]`, with `multi_agent = true` and `multi_agent_v2 = true` under `[features]` |
| Your Codex open-source profiles are real and numerous | 15 profile files under `~/.codex/*.config.toml`: `fugu`, `fugu-ultra`, `fugu-max`, `fugu-ultra-v2`, `fugu-xhigh`, `glm`, `glm-xhigh`, `glm53`, `dsflash`, `dsflash-or`, `dsflash-unquantized`, `union`, `union-alpha`, plus `yolo`/`ylo` on `gpt-6-astra` |
| Prime inheritance is explicit in the runtime source | `agent-session.js`: `_resolveRlmSubagentModel` returns the parent model when no model is referenced; child thinking is `options.thinkingLevel ?? clampThinkingLevel(options.model, this.thinkingLevel)` |
| Prime can pin any authenticated selector, cross-provider | 221 reachable selectors across six providers (`openrouter`, `prime-inference`, `anthropic`, `openai-codex`, `deepseek`, `xai`), including `anthropic/claude-opus-5` and `anthropic/claude-fable-5`. Only `name`, `model`, and `thinking` are legal spawn kwargs |
| Codex inheritance is already your practice, not just the default | Of 4,561 `spawn_agent` calls in September sessions, 0 carried a `model` argument. The offered override list is the active profile catalog: a DeepSeek parent was offered only the DeepSeek models |
| Claude Code named subagents carry their own model | Real files under `~/.claude/agents/*.md` set `model:` in frontmatter; an unset or `inherit` value follows the parent; the binary refuses a model outside the allowlist, then inherits the parent model |
| Installed surface matches the repo | `~/.agents/skills/{issue-to-pr,epic-to-prs,delegated-implementation,conductor}` and their `_shared` files are byte-identical to the tracked repo files. Codex reads this same `~/.agents/skills` surface by design (`README.md:164`), so a repo fix reaches both hosts |

Read but not executed: the skill prose inventory (three slices, 37 findings, roughly 205 inventory rows), the runtime-reality probe, the Makefile install surface, and the `build/` copies.

Not verified: whether an untagged Codex catalog model is refused as a subagent or merely unselectable, and whether Prime's thread-goal surface counts as the "native goal mode" the `auto` modes require. Both are listed under open questions.

---

## The four root problems

### P1. Two model truths, and the executable one has no open-source lane

The prose vocabulary in `skills/*.md` is one truth. `skills/_shared/model_resolution.py` is a second, load-bearing truth: scripts and skills call it as code, and `arch-epic` and `stepwise` route their role tables through it.

```python
VALID_RUNTIMES = {"agent", "claude", "codex", "grok", "kimi"}
PREFERRED_CODEX_MODEL = "gpt-6-astra"
PREFERRED_CODEX_EFFORT = "xhigh"
BLOCKED_CODEX_MODELS = frozenset({"gpt-5.4", "gpt-5.5"})
```
`skills/_shared/model_resolution.py:22-32`

Probed behavior with a loaded copy of that module:

```text
'deepseek r1 high' -> ModelResolutionError: could not infer runtime from 'deepseek r1 high';
                      name claude, codex, agent, grok, or kimi
'glm 4.6 high'     -> same
'native'           -> same
'codex' against a catalog without gpt-6-astra
                   -> ModelResolutionError: 'codex' did not match an available Codex model
                      with the same family and exact version; candidate was 'gpt-6-astra'
```

Repo-wide, `git grep -i -e deepseek -e qwen -e llama -- 'skills/*'` returns nothing. The only open-source mentions in the repo live in `docs/`. So an open-source model can be neither a resolved child target nor a resolved parent profile anywhere in the live surface.

The resolver also knows only 2 of your 15 Codex profiles: `_FUGU_EFFORTS` covers `fugu` and `fugu-ultra`, and `codex_model_or_profile_args` emits `-p <profile>`. `fugu-max`, `fugu-ultra-v2`, `fugu-xhigh`, `glm`, `glm-xhigh`, `glm53`, `dsflash*`, and `union*` are invisible.

### P2. The container skills gate the execution contract on parent identity

Both delivery skills branch on the same phrase:

```text
For an Astra or Fable coordinator, apply `$delegated-implementation` throughout the work:
delegate code, reproduction, tests, and repairs; personally review every deliverable and
changed code line.
```
`skills/issue-to-pr/SKILL.md:18-20`, word-matched at `skills/epic-to-prs/SKILL.md:20-23`

The other branch is a pointer, not a contract:

```text
For other dispatches, read the installed `../_shared/agent-orchestration-policy.md` and
apply `$prompt-authoring` to the populated brief.
```
`skills/issue-to-pr/SKILL.md:205-209`, mirrored at `skills/epic-to-prs/SKILL.md:200-205`

That policy file owns transport, context, continuation, isolation, topology, and return evidence. It never says who reviews each deliverable, who owns skill authorship, or which worker profile to use. So a DeepSeek, GLM, or Fugu parent keeps the delivery output obligations and loses the execution contract that makes delegated delivery safe.

`delegated-implementation` completes the pattern. Its worker rule is a two-branch identity switch with no third default, and its frontmatter ships that switch into router metadata:

```text
An Astra parent assigns implementation and verification to GPT-5.6 Sol (`gpt-5.6-sol`) at `high`.
A Fable parent assigns them to Opus 5 ... For another parent model, use the worker choice supplied
by the user or calling workflow.
```
`skills/delegated-implementation/SKILL.md:44-49`; the same claim is in `skills/delegated-implementation/agents/openai.yaml:4`

Note the honest correction from the audit: no file says a coordinator *must* be a specific model. These are conditional gates. The defect is that a parent which matches neither branch falls through to no rule at all. That also excludes a Codex parent running `gpt-5.6-terra`, `gpt-5.6-luna`, or a Fugu profile, which is a live gap for you today.

### P3. The cost doctrine is written for an expensive parent, and open-source parents invert it

```text
A native child inherits the parent's model and thinking level unless the dispatch pins them...
Pin the profile or take the external lane; never route bulk work to an unpinned native child.
```
`skills/conductor/SKILL.md:36-39`, again at `skills/conductor/references/delegation-and-monitoring.md:10-13`

```text
An unpinned native child is not a cheap lane: it runs the parent's model on whatever you gave it.
```
`skills/_shared/native-child-capabilities.md:80-81`

The reasoning is sound for an Astra or Fable parent: inheritance would put bulk reading on the most expensive model in the run, so pinning a cheap worker is the cost control. With DeepSeek, GLM, or Fugu as the parent, inheritance is already the cheap lane, and this rule forbids the cheapest option for all bulk work.

The doctrine sees the inversion once and does not act on it:

```text
The default fleet is Astra at xhigh; do not assume it is cheaper than the parent.
```
`skills/conductor/references/delegation-and-monitoring.md:108`

That sentence is a caveat without a fallback. A cheap parent is left following a pinning rule designed for an expensive one, with no documented cheap-fleet default.

### P4. Host assumptions are baked as a Codex-plus-Claude pair, and Prime has no local branch

`rg -n 'fork_turns'` over the live surface returns 36 lines. Every dispatch block enumerates Codex and Claude only, for example:

```text
In Codex set `fork_turns: "none"`; in Claude use a clean named or custom subagent
```
`skills/audit-loop/SKILL.md:74-75`, repeated in `arch-step`, `miniarch-step`, `arch-docs`, `lilarch`, `bugs-flow`, `comment-loop`, `audit-loop-sim`, and `arch-epic`

Exactly one file states a third-host fallback:

```text
On another host, use its clean native child mechanism when available.
```
`skills/arch-step/references/arch-consistency-pass.md:67-69`

The generic answer already exists one hop away, so this is duplication that lost a branch rather than missing knowledge:

```text
In Prime Agent, a native child is always clean — there is no fork primitive... Model and
thinking level are ordinary spawn arguments, and the child's reach is whatever that
installation is authenticated for rather than the parent's own provider.
```
`skills/_shared/agent-orchestration-policy.md:210-216`

The same pattern weakens the `auto` modes. `audit-loop`, `comment-loop`, `audit-loop-sim`, and `arch-docs` describe their loop as a Codex or Claude Code capability (`skills/audit-loop/SKILL.md:18`) and depend on that host's goal mode (`:120-121`). `arch-epic` claims parity for exactly two hosts (`skills/arch-epic/references/arch-step-integration.md:250-252`). A Prime parent still gets a bounded single pass, because every mode carries a fallback, but the mode name overstates what will happen.

### P5. Codex-specific limits the skills do not encode

Three facts decide what is possible under `-p fugu`, `-p glm53`, or `-p dsflash`:

1. **Provider follows the parent.** "No through `model` — the child's provider is copied from the parent turn" (`skills/_shared/native-child-capabilities.md:27`). A Fugu parent cannot spawn a Sol child. A native child under a Fugu parent is a Fugu child.
2. **Native children require a per-model catalog tag.** `codex debug models` marks exactly four models `multi_agent_version: v2`. Your DeepSeek catalog tags all four entries `v2`; `~/.codex/fugu.json` and `~/.codex/glm.json` tag none. So on this machine, native-child dispatch works under `-p dsflash` / `-p dsflash-or` and is unavailable under `-p fugu*` and `-p glm*`.
3. **The skills never use Codex's own child-profile lever.** `[agents] default_subagent_model` and `default_subagent_reasoning_effort` are read by the installed binary. Your config sets only `max_concurrent_threads_per_session = 7`. A skill could name that lever instead of relying on per-spawn arguments that expire when a child is unloaded — the sharp edge the policy already documents (`skills/_shared/native-child-capabilities.md:44-51`).

The practical picture is better than the prose suggests. `spawn_agent` does take an optional model, but its override list is the active profile's catalog, and your own practice is already pure inheritance: 0 of 4,561 September `spawn_agent` calls passed a model. So on Codex your intent is not merely the right policy; it is the only policy that has ever run.

Reproducing the model-resolution phrase table would also not help here, because the table answers "which external harness runs this model", not "what does the active host's child catalog hold".

### P6. Smaller contradictions that will confuse an open-source parent

These are not open-source-specific, but they are the ones a careful parent will trip over:

- `fresh-consult` and `model-consensus` say `sonnet` and `haiku` "are not supported by this repo's subprocess doctrine" and to "fail loud" (`skills/fresh-consult/references/model-and-invocation.md:99-100`, `:155`), while `stepwise` ships commands and a test fixture that run `--model haiku` (`skills/stepwise/references/session-resume.md:402`, `skills/stepwise/scripts/test_run_stepwise.py:364`).
- `stepwise` accepts four runtimes (`claude, codex, grok, kimi`) in both prose and argparse (`skills/stepwise/references/model-and-effort.md:15`, `skills/stepwise/scripts/run_stepwise.py:1710`), while its three sibling skills accept five including `agent`.
- `miniarch-step` prefers `gpt-5.4-mini` at `xhigh` for native planners and auditors (`skills/miniarch-step/SKILL.md:84-88`) while the resolver blocks `gpt-5.4` exactly (`skills/_shared/model_resolution.py:32`).
- `miniarch-step` is also the only skill in the suite that already handles your case correctly. Its guard is the pattern to copy everywhere:

```text
For miniarch planner and auditor roles, prefer `gpt-5.4-mini` with `xhigh` reasoning only when
the active native tool schema can select and confirm both. Otherwise use the inherited native
capability and do not claim the child used an unconfirmed model or effort.
```
`skills/miniarch-step/SKILL.md:84-88`

- The untracked `skills/<slug>/build/` copies still contain `Codex gpt-5.4 xhigh` and "always Codex" pins. They are rejected as install sources (`Makefile:199`), pruned (`Makefile:236`), and fail verification if present (`Makefile:355`), so they are harmless at runtime and a maintenance trap in review.


---

## Findings ranked by consequence

Status vocabulary: **breaks** = the action cannot be completed as written; **degrades** = it runs but produces the wrong or an undefined result; **harmless** = no effect on an open-source parent; **already generic** = works correctly as written.

| # | Finding | Anchor | Status |
|---|---|---|---|
| 1 | Worker model is chosen by parent identity, with no third default | `skills/delegated-implementation/SKILL.md:44-49` | breaks |
| 2 | Executive/worker contract and skill authorship are granted only to Astra/Fable parents | `skills/issue-to-pr/SKILL.md:18,205-209`; `skills/epic-to-prs/SKILL.md:20,200-205` | breaks |
| 3 | Executable resolver has no open-source runtime, no `native`, and no Prime host | `skills/_shared/model_resolution.py:22-32` | breaks |
| 4 | Codex cannot pin a cross-provider child; Fugu and GLM catalogs are not v2-tagged, so native children are unavailable there | `skills/_shared/native-child-capabilities.md:24,27`; `~/.codex/fugu.json`, `~/.codex/glm.json` | breaks |
| 5 | Codex role table assumes cross-model resolution and a `gpt-6-astra` default | `skills/_shared/agent-orchestration-policy.md:78-82` | breaks |
| 6 | Unsupported thinking level hard-fails the spawn; skills pin levels without checking the model map | `skills/_shared/native-child-capabilities.md:26`; proved live | breaks |
| 7 | Bulk work is forbidden on the only cheap lane an open-source parent has | `skills/conductor/SKILL.md:36-39`; `skills/conductor/references/delegation-and-monitoring.md:10-13` | degrades |
| 8 | Conductor fleet default is a named model from another provider | `skills/conductor/SKILL.md:294-296`; `skills/conductor/references/delegation-and-monitoring.md:103-108` | degrades |
| 9 | 36 host-mechanism lines name Codex and Claude only; one file has a third-host branch | `skills/audit-loop/SKILL.md:74-75` and 13 other files; `skills/arch-step/references/arch-consistency-pass.md:67-69` | degrades |
| 10 | `gpt-6-astra` is a Codex model absent from Prime, so a host-blind default is unresolvable there | `skills/_shared/agent-orchestration-policy.md:78`; `rlm.find_models("astra")` = 0 | degrades |
| 11 | Review skills say "prefer a clean native child" but never repeat the inheritance rule, so a review becomes self-review by the parent model | `skills/fresh-consult/SKILL.md:15`; `skills/plan-audit/SKILL.md:75-79`; policy inheritance rule is only at `skills/_shared/agent-orchestration-policy.md:86` | degrades |
| 12 | Required Pro review has no substitute or fallback lane | `skills/issue-to-pr/SKILL.md:143-144`; `skills/epic-to-prs/SKILL.md:151-152` | degrades |
| 13 | `conductor terra` forbids substitution when the Codex lane is unavailable | `skills/conductor/references/terra-delivery-shortcut.md:34-35` and `:104-107` | degrades |
| 14 | `auto` modes and the epic parity claim describe Codex/Claude goal mode only | `skills/audit-loop/SKILL.md:18,120-121`; `skills/arch-epic/references/arch-step-integration.md:250-252` | degrades |
| 15 | `agent-watcher`'s worked examples are Claude aliases | `skills/agent-watcher/SKILL.md:51-53,62` | degrades |
| 16 | Sonnet/Haiku prohibition contradicts Stepwise's own commands and test | `skills/fresh-consult/references/model-and-invocation.md:99-100` vs `skills/stepwise/references/session-resume.md:402` | degrades |
| 17 | Stepwise accepts four runtimes where sibling skills accept five | `skills/stepwise/references/model-and-effort.md:15`; `skills/stepwise/scripts/run_stepwise.py:1710` | degrades |
| 18 | `gpt-5.4-mini` preference sits next to a `gpt-5.4` block | `skills/miniarch-step/SKILL.md:84-88`; `skills/_shared/model_resolution.py:32` | degrades |
| 19 | Codex openai.yaml prompts assert an Astra/Fable coordinator identity | `skills/issue-to-pr/agents/openai.yaml:4`; `skills/delegated-implementation/agents/openai.yaml:4` | degrades on Codex |
| 20 | Only 2 of 15 local Codex profiles are expressible | `skills/_shared/model_resolution.py:54-62` | degrades |
| 21 | Stale `build/` copies keep retired pins and "always Codex" text | `skills/*/build/references/*` | harmless at runtime |
| 22 | `skills/goal-loop/` looks live but is on the install removal list | `Makefile:4` | harmless |
| 23 | Remaining opt-in external pins (yolo, terra, Pro, Fugu-as-child) are deliberate contracts | `skills/codex-review-yolo/SKILL.md:46,81`; `skills/conductor/references/terra-delivery-shortcut.md:31-35` | harmless |

---

## What already works, so we fix less

These are correct today and should be kept:

1. **Native inheritance is the documented default.** "A native child normally inherits the parent's model and thinking level. That inheritance is the whole cost question." (`skills/_shared/agent-orchestration-policy.md:86-91`). Your expectation is already the written doctrine; it just is not repeated in the container skills.
2. **Transport choice is benefit-based and host-relative.** "Prefer a native child of the active host for ordinary same-host work when that child can do the job." (`skills/_shared/agent-orchestration-policy.md:36-40`). No transport default needs inventing.
3. **The unknowable host is handled explicitly.** "For other hosts, choose the equivalent explicit clean-child and exact-resume mechanisms. Do not claim a native model override... unless the active tool surface confirms it." (`skills/fresh-consult/references/model-and-invocation.md:40-42`).
4. **Prime is described accurately once.** Clean-only children, model and thinking level as ordinary spawn arguments, per-installation catalog reach (`skills/_shared/agent-orchestration-policy.md:210-216`), and reach as a per-installation fact (`skills/_shared/native-child-capabilities.md:56-60`). My probes confirm all of it.
5. **Pin-or-inherit is a three-test decision.** Reach, grip, durability, with named failure handling (`skills/_shared/agent-orchestration-policy.md:100-116`).
6. **The miniarch guard is the pattern to copy.** "Only when the active native tool schema can select and confirm both. Otherwise use the inherited native capability." (`skills/miniarch-step/SKILL.md:84-88`).
7. **The resolver fails loud instead of substituting.** Two runtime families, two effort levels, blocked models, and exact family/version all raise rather than silently downgrade.
8. **The review skills are model-free where it matters.** `cynical-code-review`, `cynical-architecture-review`, `cynical-cruft-removal`, and `exhaustive-code-review` contain no model token and ban external reviewer lanes by design, so they cannot mis-dispatch. Their limitation is the inverse of the concern: they also cannot give provider diversity.
9. **`agent-delegate` is the only skill that can reach an external lane without being named** (`skills/agent-delegate/agents/openai.yaml:7`); the other 11 in the review slice are opt-in. Automatic pins reach a parent through copied goal-prompt text, for example `Use $model-consensus with opus 4.7 max and gpt-6-astra xhigh` (`skills/prompt-authoring/references/codex-goal-prompts.md:306`).
10. **Install is not a blocker.** The installed Agents/Codex surface is byte-identical to the repo, and Codex reads that same surface (`README.md:164`). One repo fix reaches Prime, Codex, Claude Code, and the other install roots.


---

## The fix plan

Design rules the fix follows:

1. **One owner per rule.** The shared policy owns the default dispatch profile. Container skills own roles and duties. Per-skill files stop restating host mechanics.
2. **Resolve from the live catalog, never from a baked list.** A child profile is a per-installation fact, so the skill states the test and the default, not the catalog.
3. **Inherit by default; pin as an optimization.** Pinning stays valuable when the parent is the expensive model or the work needs a stronger or cheaper profile than the parent's.
4. **Judge against the parent, not against a vendor.** The cost and quality reasoning must work for DeepSeek, GLM, and Fugu as well as Astra and Fable.

### Change 1 — Give the shared policy a default child profile

`skills/_shared/agent-orchestration-policy.md`. Add one section, and scope the existing Codex preference.

```markdown
## Default child profile

Resolve every child from the active host's live catalog, not from a baked list. When the user has
not named a model, the default child profile is the parent's own model and thinking level,
inherited by omitting both. That is correct for every parent, and it is the cheapest lane when the
parent is a cheap model. Pin a different profile only when the work needs one, when the user named
one, or when the calling workflow names one, and say which applies.
```

Scope the existing preference so it cannot be read as a host-blind default:

```markdown
## Codex model preference

Applies when a Codex lane or a Codex host is actually selected. Resolve the id against that host's
live catalog before use. `gpt-6-astra` is a Codex model; Prime Agent's catalog does not contain it,
so a Prime parent must never resolve a child to it.
```

Add one paragraph naming the partial-capability trap: a model's supported thinking levels are a per-model fact, an unsupported level hard-fails an explicit pin, and an inherited level is clamped instead of failing. Cite `skills/_shared/native-child-capabilities.md`.

### Change 2 — Refresh the host facts file with what is now verified

`skills/_shared/native-child-capabilities.md`. Update the provenance line and three rows, and add one short section.

- **Prime Agent row:** model pin is an exact `provider/id` selector; unsupported thinking level hard-fails; add that open-source parents are ordinary parents here, and that inheritance, not pinning, is the cheap lane. Record the cross-provider result I proved from a DeepSeek parent.
- **Codex row:** add the per-model gate — a native child exists only for a catalog entry tagged `multi_agent_version: "v2"`. The base catalog tags the `gpt-6-astra` and `gpt-5.6-*` family; a profile's own `model_catalog_json` decides for custom providers. Add `[agents] default_subagent_model` and `[agents] default_subagent_reasoning_effort` as the durable child-profile lever, which is stronger than a per-spawn argument that expires on unload.
- **New section "Open-source parents":** state the three verified behaviors in one place — inheritance by default, per-model thinking-level maps with hard failure on an unsupported explicit level, and per-installation catalog reach. Record that this installation reaches 221 selectors across six providers, including Opus 5 and Fable 5, so "a Prime parent cannot pin a vendor child" is false and no skill should say it.

### Change 3 — Extend the executable resolver instead of working around it

`skills/_shared/model_resolution.py`. This is the only change that makes an open-source model expressible in code.

1. Add `"native"` to `VALID_RUNTIMES`, meaning "the active host's own child, inheriting the parent's profile". `resolve_execution_phrase("native")` returns a native resolution with no pinned model or effort.
2. Add a catalog-driven capability check so effort validation can use the host's real map when the caller supplies one, keeping the built-in sets only as a fallback.
3. Discover local Codex profiles from `$CODEX_HOME/*.config.toml` the way `discover_codex_models` discovers model ids, so `fugu-max`, `fugu-ultra-v2`, `fugu-xhigh`, `glm`, `glm-xhigh`, `glm53`, `dsflash*`, and `union*` stop being invisible. Keep `fugu` and `fugu-ultra` working.
4. Keep failing loud on ambiguity, but make the message name the native option. Today it says "name claude, codex, agent, grok, or kimi"; it should also say "or name `native` to use this host's own child".
5. Refresh the docstring examples, and add cases to the existing test surface for `native`, an open-source phrase, and a local profile.

### Change 4 — Make the executive/worker contract unconditional

This is the highest-value user-visible fix, and it is what you asked about.

In `skills/issue-to-pr/SKILL.md` and `skills/epic-to-prs/SKILL.md`, the review duty, the worker duty, and parent-owned skill authorship become unconditional. The model table becomes an example, not a gate:

```text
Apply `$delegated-implementation` to every coordinator: workers implement, test, and repair;
the coordinator personally reviews every deliverable and changed code line and authors all skill
content. Where the coordinator's own model is one of the named families, its documented worker
default applies; otherwise the worker is the inherited native child, or the model the user named.
```

In `skills/delegated-implementation/SKILL.md`, replace the identity switch with an ordered rule:

```text
Use the worker the user named. If the user named none and the calling workflow names none, the
worker is a native child of the active host that inherits the parent's model and thinking level.
Astra to GPT-5.6 Sol at high and Fable to Opus 5 are the two documented named defaults, not the
only supported parents.
```

Update the frontmatter `description` and `skills/delegated-implementation/agents/openai.yaml` default prompt to match, because those surfaces are what a router and a Codex session read first. The current description ships "Astra delegates to GPT-5.6 Sol high; Fable delegates to Opus 5" to every reader, including parents it excludes.

### Change 5 — Fix the cost inversion in `conductor`

In `skills/conductor/SKILL.md` and `skills/conductor/references/delegation-and-monitoring.md`:

- Scope the anti-unpinned rule to its real reason: "never route bulk work to an unpinned native child **when the parent's own profile is more expensive than the intended fleet profile**."
- Add the inverted default: "when no provider is named and the parent is the cheaper model, the inherited native child is the fleet; pin only to raise quality or to match a user-named model."
- Replace the flat "fleet profile defaults to Codex `gpt-6-astra` at `xhigh`" (`skills/conductor/SKILL.md:294-296`) with: default to the inherited native child; use a named model when the user named one; keep the Astra default only inside an explicitly selected Codex fleet.
- Keep the pinned-fleet path intact for expensive parents. It is correct there, and the Terra preset should stay as it is.

### Change 6 — Replace host-pair enumeration with one pointer

The 36 `fork_turns` lines restate Codex and Claude mechanics and lose the third host. Keep one authoritative host-mapping section in `skills/_shared/agent-orchestration-policy.md` and reduce the per-skill lines to a single sentence:

```text
Set the clean-context mechanism your host requires, and read the host mapping in
`../_shared/agent-orchestration-policy.md`. On a host that is not Codex or Claude, use its clean
native child mechanism; if it has none, do the work serially in the parent.
```

`skills/arch-step/references/arch-consistency-pass.md:67-69` already has this shape. Apply it to `arch-step`, `miniarch-step`, `arch-docs`, `lilarch`, `bugs-flow`, `comment-loop`, `audit-loop`, `audit-loop-sim`, and `arch-epic`, and to the four `auto` trigger lines that name Codex or Claude Code.

### Change 7 — Make Codex able to do it (machine config, not the repo)

Only if you want it, with backups first:

1. Add `"multi_agent_version": "v2"` to the entries in `~/.codex/fugu.json` and `~/.codex/glm.json`, and to `~/.codex/union-alpha.json` if that model is meant to spawn children. Verify with one live spawn in a `-p fugu` session before trusting it.
2. Optionally set `[agents] default_subagent_model` and `default_subagent_reasoning_effort` in `~/.codex/config.toml` so children inherit a chosen profile durably. This is the lever the skills should name instead of relying on a per-spawn pin that expires.

### Change 8 — Record the routing rule where you read it

- `AGENTS.md` → Skill Routing: scope the Codex default to a selected Codex lane, and add one sentence: open-source parents (DeepSeek, GLM, Fugu) dispatch to native children that inherit the parent's model unless you name a worker.
- `README.md`: add the open-source parents to the host and model paragraph, and say that native inheritance is the default lane.
- Remove the stale `skills/<slug>/build/` copies, or state in the repo docs that they are abandoned output and not a surface.

### Recommended order

| Wave | Changes | What it buys |
|---|---|---|
| 1 | 1, 2, 4 | Your stated intent becomes the written default, and the container skills stop gating the execution contract on your model's name |
| 2 | 3, 5 | The executable resolver can name `native` and your profiles, and the cost rule stops forbidding your cheapest lane |
| 3 | 6, 7, 8 | Third-host dispatch works everywhere, Codex can actually spawn Fugu and GLM children, and the routing rule is recorded |

---

## How to verify each change

| Change | Proof |
|---|---|
| 1, 2 | Read the changed sections back. Confirm no file states a host-blind `gpt-6-astra` default and that the Prime paragraph covers inheritance, partial thinking maps, and catalog reach |
| 3 | Load the module from disk and resolve `native`, `fugu-max high`, `glm53 xhigh`, `deepseek high`, and `codex` with a catalog that lacks `gpt-6-astra`. Confirm `native` resolves, the local profiles resolve as profiles, and the failure message names `native` |
| 4 | Spawn one child per parent shape with the model omitted, and confirm the child's model equals the parent's. Confirm the skill text assigns the review and authorship duties in the non-Astra branch |
| 5 | Read the conductor's fleet default back, and confirm an open-source parent is told to inherit rather than to pin |
| 6 | `rg -n 'fork_turns' skills/` and confirm each remaining line names the host mapping rather than a two-host pair |
| 7 | One live spawn inside a `-p fugu` session; confirm a child starts and reports a Fugu model. Re-check `~/.codex/config.toml` parses |
| 8 | `npx skills check` after the skill changes; `rg` the new `AGENTS.md` and `README.md` lines |

Run `npx skills check` for any change under `skills/`, per `AGENTS.md`. Run `make verify_install` only for change 8.

Do not add tests that assert doctrine wording. Test the resolver's deterministic behavior instead: `native` resolves, local profiles resolve, and an unsupported effort raises.

---

## Open questions I could not settle

1. **Does an untagged Codex catalog model refuse a child, or merely make it unselectable?** The base catalog tags `gpt-6-astra` and the `gpt-5.6-*` family `v2` and leaves older `gpt-5.5` untagged, and the repo's own facts file says the slug "must be catalog-tagged for v2". One live spawn inside a `-p fugu` session settles it.
2. **Does `multi_agent_version` on a profile catalog entry need anything else?** Your DeepSeek catalog carries the tag; the Fugu and GLM catalogs do not. Whether the tag alone is sufficient is unverified.
3. **Is Prime's thread-goal surface the "native goal mode" the `auto` modes require?** If it is, the loop modes work on Prime and the four trigger lines should say so. If it is not, the bounded single pass is the honest behavior.
4. **How is a native Prime child on `openai-codex/gpt-5.6-*` billed?** It may consume the Codex subscription window instead of Prime inference. No skill says, and the cost logic depends on the answer.
5. **Are "Astra" and "Fable" model identities or host identities?** The skills never define them, and `_CLAUDE_FAMILIES = {"fable", "opus"}` reads Fable as a Claude family. A maintainer statement would settle how the two named defaults should be reworded.
6. **Was excluding Terra, Luna, and Sol from the Astra/Fable gate deliberate?** Today a Codex parent on `gpt-5.6-terra` matches neither branch.
7. **Does any other machine install a stale `build/` copy?** On this machine they are untracked and never installed.

---

## The first step I would take

Change 4, on top of the two sentences from changes 1 and 2 that it depends on. It is about 30 lines of prose across three skills, it removes the dead-end rule that started this question, and it makes `issue-to-pr` and `epic-to-prs` behave the same way for DeepSeek, GLM, and Fugu as they do for Astra and Fable. Change 3 is the largest single piece of work and should follow as its own change, because it moves executable behavior and needs resolver tests.

