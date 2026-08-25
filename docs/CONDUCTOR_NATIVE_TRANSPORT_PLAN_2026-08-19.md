# Conductor: Native-Capable Transport Plan

**Date:** 2026-08-19
**Repo:** `arch_skill`
**Job:** answer whether `$conductor` is external-only, and plan the edit that
makes it native-capable with an explicit worker thinking level.
**Method:** full read of `skills/conductor/**`, plus three read-only harness
investigations against source and installed binaries.

**Status: IMPLEMENTED 2026-08-19.** Sections 1-4 are the findings and the rule.
Section 5 is the edit plan as executed. Section 10's open questions were
decided by the user and are answered inline there.

---

## 1. Verdict

**Yes. `conductor` is external-by-doctrine today, and it argues against native
children on a cost premise that is factually wrong on all three hosts we run.**

The skill does not merely prefer external transport. It names external the
standing default for every heavy role, and tells the agent that native children
are never a cheap lane:

> "Native subagents bill the parent's expensive model — they are not a cheap
> lane, so bulk work never routes to them."
> — `skills/conductor/SKILL.md`, North Stars

> "Native children are not a budget lane and not free parallelism — they are
> the parent's wallet with a different face. Reserve them for genuinely tiny
> errands a fleet round-trip would dwarf (a one-file read-only check), a
> capability only the host exposes, an explicit user request, or an unavailable
> external runtime."
> — `skills/conductor/references/delegation-and-monitoring.md`, opening

> "Never run these reviews through the parent's own native subagents — bulk
> review reading on the parent's model is the exact spend this skill exists to
> avoid."
> — `skills/conductor/references/delegation-and-monitoring.md`

The same claim is repeated four more times in
`references/audit-and-send-back.md` (cold verifier, requested cynical reviews,
delegated artifact inspection) and once in `agents/openai.yaml`'s
`default_prompt`.

This is a known, deliberate deviation. `docs/external-dispatch-native-subagent-inventory.md`
already records it:

> "conductor is also the only skill that treats native sub-agents as an
> *economic* category ... Everywhere else in the repo, native children are the
> *preferred* lane and external transport is the thing that must justify
> itself. Conductor inverts the suite-wide default on purpose and says why.
> That is a documented deviation ... the single biggest divergence from
> `_shared/agent-orchestration-policy.md` in the repo."

**The premise it inverts on is false.** All three hosts let a parent pin a
child's model, and all three let a parent set some form of child-specific
reasoning effort. A native child bills the *child's* model, not the parent's —
but only if the parent actually pins it. The correct rule is not "avoid native
children"; it is **"pin the child's model and effort, or inherit the parent's
knowingly."**

---

## 2. Verified harness capabilities

Three independent read-only investigations, 2026-08-19. Full evidence with
file:line anchors and quoted code:

- `/tmp/conductor-native-research/prime-agent.md`
- `/tmp/conductor-native-research/codex.md`
- `/tmp/conductor-native-research/claude-code.md`

Builds under test: Prime Agent `packages/coding-agent` at
`/Users/aelaguiz/workspace/prime-agent-fast-label-ready-20260817`; Codex repo
`ceb2ffb793` with installed `codex-cli 0.148.0-alpha.20` and
`multi_agent_v2 = stable/true`; Claude Code `2.1.228` (build 2026-08-11), zod
schemas read from the binary plus current `code.claude.com` docs.

### 2.1 Matrix

| Capability | Prime Agent | Codex CLI (multi_agent_v2) | Claude Code 2.1.228 |
|---|---|---|---|
| Pin child **model** | Yes — `model="provider/id"` on `rlm(...)`, exact selector, must be in the authenticated catalog; unknown selector hard-throws | Yes — `spawn_agent(model=...)`; slug must be catalog-tagged `multi_agent_version == v2`. On this host that is only `gpt-5.6-sol` and `gpt-5.6-terra` | Yes — three levers, in order: `CLAUDE_CODE_SUBAGENT_MODEL` env, per-call `model` param, agent frontmatter `model:` |
| Pin child **thinking / effort** | Yes — `thinking=` with `off,minimal,low,medium,high,xhigh,max` | Yes — `reasoning_effort=` with `none,minimal,low,medium,high,xhigh,max,ultra`; validated against the *effective child* model (sol/terra accept `low..ultra`) | **Partial** — agent frontmatter `effort:` accepts `low,medium,high,xhigh,max`. There is **no per-call effort param** on the `Agent` tool, and docs state verbatim "There is no per-subagent thinking setting" |
| Pin **model + effort together** | Yes | Yes; with a model override the effort validates against the new model, and an omitted effort takes that model's default | Only through a pre-authored agent definition file carrying both `model:` and `effort:` |
| **Cross-provider** native child | **Yes** — provider is not a constraint anywhere in the spawn path; the only gate is "in the authenticated catalog + auth preflight ok" | **No** via `model`: the child's provider is copied from the parent turn and never overridden; `ModelPreset` has no provider field. Possible only through a human-installed `agent_type` role whose config file sets `model_provider` | **No** — "doesn't support routing Claude Code to non-Claude models through any gateway"; `ANTHROPIC_BASE_URL` is process-wide and changes where requests go, not which model answers |
| Starting context | Clean only; no fork option exists | `fork_turns`: `none` / `all` / positive-int string. **Default when omitted is `all`** | Clean by default; `subagent_type:"fork"` inherits everything and forces the parent model |
| Resume the exact child | By child name/id through `agent_message` | `followup_task` / `send_message` on the canonical `task_name` | `SendMessage({to: agentId \| name})`, full history retained |
| Concurrency | No cap (kernel boot throttle only delays) | **Default 3 children** (cap 4 including root); LRU unload before error | 20 (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) |
| Child fan-out (grandchildren) | **Default depth 1 — a child cannot spawn its own children.** Raise with `/rlm-max-depth N` or `RLM_MAX_DEPTH` | Uncapped in V2 (the depth check is V1-only) | Depth 3 (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) |
| Billing | Child bills at **its own model's rate**; cost is summed into parent totals tagged by origin. Caveat: this is Prime Agent's static price table; subscription-metered providers may meter against plan quota (unverified) | Same account/plan/rate-limit window — all children share the parent's single `AuthManager`, and there is no account/key/org param on `spawn_agent`. Child token usage is per-thread and is **never rolled up to the parent**, so parent-side totals under-report a native run | Same Anthropic account/plan either way |

### 2.2 Three sharp edges the plan must encode

**A. Codex raw overrides do not survive eviction.** A native Codex V2 child
keeps its pinned model and effort *while it is loaded*. When the residency LRU
unloads it and a `followup_task` rebuilds it from rollout, the reload config is
taken from the **current parent turn** — so the child silently resumes on the
**parent's model and effort**. Only an `agent_type` role survives, because the
role is persisted in `SessionSource`; a raw `spawn_agent(model=..., reasoning_effort=...)`
argument is not persisted anywhere. This is exactly the runaway-cost failure the
conductor's original doctrine feared, and it lands precisely on conductor's
send-back loop, which resumes the same worker up to three times. Evidence:
`multi_agents_v2/message_tool.rs:92`, `multi_agents_common.rs:185-200`,
`control/spawn.rs:255-259`, `control/residency.rs:81-115`.

**B. Claude Code has no per-call effort.** Pinning a Claude subagent's effort
requires a pre-authored agent definition file with `effort:`. A conductor that
wants "Claude workers at `high`" cannot express that in the dispatch call; it
needs an installed agent definition, or it uses the external lane. The per-call
`model` param is also a closed enum (`sonnet|opus|haiku|fable`) — full model IDs
only work through frontmatter or the env var.

**C. Prime Agent children cannot fan out at default depth.** Conductor's worker
prompt contract currently promises every worker: "You may use your own native
sub-agents on this host whenever they help; you do not need permission." On
Prime Agent at the default `RLM_MAX_DEPTH=1` that is false — the child's spawn
attempt fails. The prompt must state fan-out as an observed capability, not an
assumption.

---

## 3. What this does and does not change

**Changes.** The cost argument for external-by-default collapses. On every host
we run, a parent can put workers on a cheaper model than its own, and on two of
three it can also set their effort per call. "Cheap parallel fleet" is a
*worker profile*, not a transport.

**Does not change.** External transport keeps real, named benefits that no
native lane provides:

1. **Cross-provider from a Codex or Claude Code parent.** Verified impossible
   natively without human config-file work. Your instinct is right for those
   two hosts.
2. **Cross-provider from a Prime Agent parent is possible natively** —
   provider is not a constraint in the spawn path. The gate is the
   authenticated catalog: **if the install is logged in to both providers, a
   cross-provider child is an ordinary native spawn.** Reach is a
   per-installation fact, so check the catalog rather than assuming either
   answer. On this machine the catalog is Anthropic-only today.
3. **`aim` usage-limit rotation** across Codex accounts with exact-session
   resume. External only.
4. **Sessions that outlive the parent process**, and durable resumable handles
   across restarts.
5. **Structured receipts** (`events.jsonl`, `final.txt`, run directories) when
   the run needs post-mortem evidence.
6. **Concurrency beyond the native cap** — most sharply on Codex, where the
   native cap is 3 children.
7. **Process and worktree isolation** where the host lacks it. Note Claude Code
   has native `isolation: worktree` in agent frontmatter.
8. **`conductor terra`** — an explicit user preset naming an exact external
   profile, worktree, and receipt contract. Unchanged.

---

## 4. Proposed decision rule

Replace "external fleet by default" with **worker profile first, transport
second**. The conductor resolves the profile it wants, then picks the cheapest
lane that can actually deliver it.

### Step 1 — Resolve the worker profile

One consolidated question for load-bearing missing values, as today:

- **Provider and model** — default stays `gpt-5.6-sol`.
- **Thinking / effort level** — default stays `ultra` for Sol. This is the
  user-facing knob you asked for, and it uses the existing shared vocabulary in
  `skills/_shared/model_resolution.py`: `low, medium, high, xhigh, max, ultra`.
- **Durability need** — will slices outlive the parent turn or process?
- **Isolation need** — shared worktree, dedicated worktree, or process
  isolation?
- **Receipt need** — is a captured event/final artifact load-bearing evidence?

### Step 2 — Choose native when all four hold

- **N1 Reachable.** The wanted model is in the parent host's native child
  catalog. (Codex: catalog-tagged v2 only. Claude: Claude models only. Prime:
  the authenticated catalog, which may span providers.)
- **N2 Pinnable.** The host can set that model **and** that effort for the
  child. (Claude needs a pre-authored agent definition to satisfy this.)
- **N3 Durable enough.** The pin survives the run's resume pattern. On Codex
  this means either the slice completes inside residency, or the profile is
  expressed as an `agent_type` role.
- **N4 No external-only benefit is load-bearing** from the section 3 list.

### Step 3 — Otherwise use `$agent-delegate`

Always-external cases, stated plainly so the agent does not have to re-derive
them:

- Cross-provider work from a Codex or Claude Code parent.
- A Prime Agent parent whose authenticated catalog lacks the wanted provider.
- Codex-hosted runs needing more than 3 concurrent workers.
- Codex-hosted long slices where residency eviction would silently re-price a
  resumed worker on the parent's model, with no `agent_type` role installed.
- Claude-hosted runs needing a per-call exact model ID or per-call effort with
  no agent definition installed.
- `aim` rotation across Codex usage limits.
- `conductor terra`.

### Step 4 — Announce and log it

Announce the resolved profile and lane before the first launch, as the skill
already requires for external. Record lane, model, effort, starting context,
and the exact handle per slice in the conductor log — the log contract already
has fields for external run directories and needs the same for native handles.

---

## 5. Edit plan

Authored under `$skill-authoring`. Its binding constraints for this job:

- Shared orchestration semantics live in `skills/_shared/agent-orchestration-policy.md`;
  the owning skill keeps only its role, domain judgment, slicing, handoffs, and
  result contract.
- Do not copy an orchestration mini-policy into the skill, and do not add a
  dispatcher, controller, or script that owns cross-skill transport decisions.
- Keep `SKILL.md` lean; heavy detail goes to `references/`.
- Co-edit `agents/openai.yaml` whenever the visible contract changes.
- Teach judgment, not a routing table.

Per repo `AGENTS.md`: keep each change in its smallest owning surface, and run
`npx skills check` after skill package changes.

### 5.1 `skills/_shared/agent-orchestration-policy.md` — shared semantics

The policy today says "Do not claim that a native child uses a requested model
... unless the current host exposes and confirms that capability" but gives no
host facts, and it has **no Prime Agent entry at all**. Two edits:

1. In **"Map context to the active host"**, add a Prime Agent bullet group:
   clean-only context with no fork, `model=` and `thinking=` kwargs, resume by
   child name through `agent_message`, and the default depth-1 fan-out limit.
2. Add one short subsection, **"Pin model and thinking level, or inherit
   knowingly"** (~20 lines). Content: a native child inherits the parent's model
   and thinking level unless pinned; pinning is the difference between a cheap
   lane and an expensive one; state the pin at dispatch the same way
   `fork_turns` is stated; verify the pin against the live tool schema rather
   than memory; and check whether the pin survives the host's resume path
   before planning a multi-round repair loop on it.

Keep the per-host matrix **out** of this always-on file.

### 5.2 `skills/_shared/native-child-capabilities.md` — new shared reference

**Recommended.** One dated, on-demand reference holding the section 2 matrix
plus the three sharp edges, with a provenance header naming the exact builds and
an explicit instruction to verify a row against the live tool schema before
relying on it. Pointed to from the policy's new subsection and from
`conductor/references/delegation-and-monitoring.md`.

Why shared and not conductor-local: `conductor`, `fresh-consult`, `stepwise`,
`model-consensus`, `arch-epic`, and `agent-delegate` all make the same
native-vs-external call and all currently guess at these facts.

Alternative if you want a smaller blast radius: keep the matrix inside
`skills/conductor/references/delegation-and-monitoring.md` and revisit sharing
later. That trades duplication risk for a one-skill change.

### 5.3 `skills/conductor/SKILL.md` — the contract change

| Location | Change |
|---|---|
| frontmatter `description` | Drop "Default execution is the cheap parallel external fleet ... native children stay a narrow exception." Replace with the worker-profile framing: a cheap parallel worker fleet on a named model and thinking level, run natively when the host can pin that profile and externally when it cannot. Keep the Terra sentence. Stay under 1024 chars. |
| North Stars, bullet 2 | Delete "Native subagents bill the parent's expensive model — they are not a cheap lane, so bulk work never routes to them." Replace with: an unpinned native child inherits the parent's expensive model; a pinned one bills its own. Pin it, or use the external lane. |
| Non-Negotiables, the standing-fleet-policy bullet | Rewrite as the section 4 decision rule: resolve the worker profile first, then take the cheapest lane that can actually deliver it. Keep the existing "honor explicit user choices in both directions." |
| Non-Negotiables, external identity bullet | Rename to worker identity. Keep every default (`gpt-5.6-sol`/`ultra`, `kimi-code/k3`/`max`, sol/luna/terra aliases, provider routing). Add: the thinking/effort level is a first-class worker value on **both** lanes, from the same vocabulary. |
| Non-Negotiables, "Initial workers are new clean fleet sessions" | Make lane-neutral: initial workers are new clean children on the selected lane; repairs resume the exact captured handle through its original transport. |
| Non-Negotiables, native starting context | Keep as is; it is already correct and now matters more. Add that Codex `fork_turns` **defaults to `all`** when omitted, so a clean worker must say `"none"` explicitly. |
| Non-Negotiables, fan-out line | Change "may fan out to its own native sub-agents" to a capability the conductor states as observed for the chosen host, naming the Prime Agent depth-1 default as the case where it is false. |
| First Move, step 6 | Replace "The fleet default is external Codex `gpt-5.6-sol` at `ultra`" with: resolve the worker profile (provider/model, thinking level, durability, isolation, receipts), then the lane. Same defaults, same one consolidated question. |
| Workflow, step 4 | Lane-neutral dispatch wording. |
| Workflow, step 10 | Cold verifier and requested cynical reviews run as new clean children on the selected lane, not "external fleet session." |

### 5.4 `skills/conductor/references/delegation-and-monitoring.md` — biggest rewrite

- **Opening paragraph**: replace the "parent's wallet with a different face"
  argument with the pinning rule and the section 4 test. This is the load-bearing
  paragraph; everything else in the file echoes it.
- **Dispatch And Continuation Mapping**: make all five entries lane-neutral.
  Keep exact-handle resume, keep respawn-on-cold-restart, keep parent-owned
  parallel waves.
- **Native Starting Context**: keep; add the Codex `fork_turns` default-`all`
  warning and the Prime Agent clean-only fact.
- **External Worker Identity** → **Worker Identity And Profile**: model and
  effort resolution shared by both lanes; the external-specific process contract
  (Kimi env vars, session receipts, `aim` rotation) stays under an external
  subsection.
- **Patient Monitoring**: it already says "a liveness monitor suited to its
  transport." Add the concrete native signals per host, and add the Codex note
  that child token usage is per-thread and never rolled up to the parent, so
  parent-side cost totals under-report a native run.
- **Conductor Token Economy**: keep the two-sided ledger unchanged. Rewrite only
  the clause "on a cheap model, which a native subagent is not" — the accurate
  statement is that delegated bulk work belongs on the cheap *profile*, on
  whichever lane carries it.

### 5.5 `skills/conductor/references/audit-and-send-back.md` — four passages

All four say some version of "native subagents bill the parent's expensive
model." Rewrite each to the pinned-profile rule:

1. Delegated artifact inspection ("require the inspecting fleet worker...").
2. Cold verifier ("Run it as a clean external fleet one-shot by default ...
   Use a native clean child only on explicit user request or when no external
   runtime exists").
3. Requested cynical reviews ("Never run them through the parent's own native
   subagents").
4. Decisive-proof reproduction ("a different clean fleet session").

Keep the independence requirements intact — a *different clean* child is still
required. Only the transport claim changes.

### 5.6 `skills/conductor/references/worker-prompt-contract.md` — small

- "Write the exact child prompt to the native dispatch or external `prompt.md`"
  — already lane-neutral, keep.
- **Capabilities And Boundaries**: replace the unconditional native fan-out
  promise with a slot the conductor fills from the host's real capability, and
  keep "Do not spawn external agents" unchanged — that rule is transport policy,
  not a cost claim.
- Add `Worker profile: <model> at <thinking level>` to the Worker Context block
  so the worker knows and can report its own profile.

### 5.7 `skills/conductor/references/conductor-log-contract.md`

Add native handle fields alongside the existing external run-directory fields:
lane, model, thinking level, starting context, exact handle. One row shape for
both lanes.

### 5.8 `skills/conductor/references/terra-delivery-shortcut.md` — no change

It explicitly selects the external lane and names its benefit. Leave it.

### 5.9 `skills/conductor/agents/openai.yaml` — required co-edit

`short_description` and `default_prompt` both advertise "cheap external fleet"
and "Native subagents bill the parent's expensive model: never use them for
reviews." Rewrite both to match the new contract.

### 5.10 Docs that restate the old contract

- `README.md` line 66 and the `### conductor` section (~line 670).
- `docs/arch_skill_usage_guide.md` `### conductor` section (~line 789).
- Root `AGENTS.md` skill-routing bullet for `$conductor`.
- Add a resolution banner to `docs/external-dispatch-native-subagent-inventory.md`
  noting the economic-category finding is superseded, matching the banner style
  already at the top of that file.

---

## 6. Draft wording for the two load-bearing passages

These are drafts to react to, not final text. Everything else in section 5
follows from them.

### 6.1 `SKILL.md` North Star bullet 2 (replacement)

> Parent tokens go to plan understanding, slice design, cynical audit judgment,
> and first-hand verification of finished work products. Worker tokens go to
> investigation, implementation, repair, proof runs, and heavy review reading —
> on a cheap worker profile, whichever lane carries it. A native child inherits
> the parent's expensive model unless the parent pins its model and thinking
> level; a pinned child bills its own. Pin the profile, or take the external
> lane. Never route bulk work to an unpinned native child.

### 6.2 `delegation-and-monitoring.md` opening (replacement)

> The conductor chooses transport under
> `../../_shared/agent-orchestration-policy.md`; transport does not choose the
> workflow. Resolve the **worker profile** first — provider and model, thinking
> level, durability, isolation, receipts — then take the cheapest lane that can
> actually deliver that profile.
>
> The old rule of thumb, "native children are the parent's wallet with a
> different face," is only true of an *unpinned* native child. Every host we run
> lets the parent pin a child's model, and most let the parent set the child's
> thinking level too. A pinned native child on `haiku`/`sol`-class is a cheap
> lane. An unpinned one silently runs the conductor's own expensive model on
> bulk reading, which is the exact spend this skill exists to avoid.
>
> Take the native lane when all four hold:
> **reachable** (the model is in this host's native child catalog),
> **pinnable** (this host can set that model *and* that thinking level for the
> child), **durable enough** (the pin survives this run's resume pattern), and
> **no external-only benefit is load-bearing**.
>
> Take the external lane through `$agent-delegate` when any of those fails, and
> name which one. Cross-provider work from a Codex or Claude Code parent always
> fails "reachable." So do `aim` usage-limit rotation, sessions that must
> outlive the parent process, required run-directory receipts, concurrency past
> the host's native cap, and the `conductor terra` preset.
>
> Verify a capability against the live tool schema before promising it. See
> `../../_shared/native-child-capabilities.md` for the current per-host matrix
> and its known sharp edges.

---

## 7. Execution order and effort

Do it in one pass; the passages contradict each other if split.

| # | Step | Files | Effort |
|---|---|---|---|
| 1 | Write the shared capability reference | `skills/_shared/native-child-capabilities.md` | 45 min |
| 2 | Extend the shared policy | `skills/_shared/agent-orchestration-policy.md` | 30 min |
| 3 | Rewrite the conductor delegation reference | `references/delegation-and-monitoring.md` | 60 min |
| 4 | Update `SKILL.md` (description, North Star, 5 non-negotiables, First Move 6, Workflow 4 and 10) | `skills/conductor/SKILL.md` | 60 min |
| 5 | Fix the four audit passages | `references/audit-and-send-back.md` | 25 min |
| 6 | Worker prompt + log contract | `references/worker-prompt-contract.md`, `references/conductor-log-contract.md` | 25 min |
| 7 | Co-edit runtime metadata | `agents/openai.yaml` | 20 min |
| 8 | Docs sync | `README.md`, `docs/arch_skill_usage_guide.md`, `AGENTS.md`, inventory banner | 30 min |
| 9 | Verify | see section 8 | 20 min |

**Total: about 5 hours** of focused editing.

---

## 8. Verification

1. `npx skills check` — required by `AGENTS.md` after any change under `skills/`.
2. Frontmatter `description` stays under the 1024-character runtime cap.
3. Stale-phrase sweep — each of these must return zero hits in `skills/`:
   - `rg -n "wallet with a different face" skills/`
   - `rg -n "bill the parent.s expensive model" skills/`
   - `rg -n "never the cheap lane|not a cheap lane" skills/`
   - `rg -n "external fleet" skills/conductor/` (expect hits only in
     `terra-delivery-shortcut.md`)
4. Consistency sweep — `agents/openai.yaml` `default_prompt` must not contradict
   `SKILL.md`; grep both for "native" and read the hits side by side.
5. No new script, runner, or controller was added. The change is prompt-only.
6. `make verify_install` only if the install surface changed. It should not.
7. Cold read: hand the edited `SKILL.md` plus
   `references/delegation-and-monitoring.md` to a clean reviewer and ask one
   question — "on a Claude Code host, conducting a plan that needs Codex
   `gpt-5.6-sol` workers at `ultra`, which lane does this doctrine select and
   why?" The correct answer is external, because cross-provider fails
   "reachable." If the reviewer hesitates, the rule is not clear enough.

---

## 9. Risks

| Risk | Mitigation |
|---|---|
| The agent reads "native is now allowed" as "native is now preferred" and runs bulk review on an unpinned parent model | The pin requirement is stated in the same sentence as the permission, in all four surfaces. The N2 "pinnable" test is a hard gate, not advice. |
| The capability matrix goes stale as harnesses change | Dated provenance header, exact build IDs, and an explicit "verify against the live tool schema before relying on a row" instruction. Kept out of always-on context. |
| Codex residency eviction silently re-prices a resumed worker | Called out as sharp edge A, encoded as the N3 "durable enough" test, and named as an always-external case when no `agent_type` role is installed. |
| The doctrine turns into a routing table and kills judgment | The rule is four named tests plus a list of recognized always-external cases, phrased as recognition aids. `$skill-authoring` forbids canned menus; keep the tests as reasoning prompts. |
| Scope creep into `fresh-consult`, `stepwise`, `model-consensus`, `arch-epic` | Out of scope for this change. Those skills already prefer native and only gain the shared reference. Revisit separately if their wording proves wrong. |

---

## 10. Decisions taken

1. **Shared reference.** Implemented as `skills/_shared/native-child-capabilities.md`,
   installed with the rest of `_shared` and verified by `make verify_install`.
   Six skills make the same native-vs-external call and all of them can now read
   one dated source of facts.
2. **Default lane when both work.** Native. The pinned profile makes it the same
   money, and it avoids the separate-process contention the shared policy
   already flags. The external lane stays one word away and keeps every named
   benefit.
3. **Prime Agent cross-provider.** Treated as a per-installation catalog
   question, not a vendor limit: when the install is authenticated for both
   providers, a cross-provider child is an ordinary native spawn. The doctrine
   says check the catalog.
4. **Thinking-level default.** Unchanged — `ultra` for Sol on both lanes. The
   level is now a first-class worker value drawn from one vocabulary and
   recorded per slice in the conductor log, so a user can lower it per run
   without editing doctrine.

## Appendix — evidence files

| File | Contents |
|---|---|
| `/tmp/conductor-native-research/prime-agent.md` | Prime Agent spawn path, model/thinking resolution, cost accounting, depth limits, with `agent-session.ts` / `model-registry.ts` / `thinking-levels.ts` anchors |
| `/tmp/conductor-native-research/codex.md` | Codex `multi_agent_v2` tool schemas, `model` + `reasoning_effort` validation, `fork_turns`, the role-based provider path, eviction behavior, limits, billing |
| `/tmp/conductor-native-research/claude-code.md` | Claude Code 2.1.228 agent-definition zod schema, model resolution order, `effort:`, gateway limits, concurrency and depth env vars |

These are scratch research artifacts outside the repo. Copy anything durable
into `skills/_shared/native-child-capabilities.md` when step 1 runs.
