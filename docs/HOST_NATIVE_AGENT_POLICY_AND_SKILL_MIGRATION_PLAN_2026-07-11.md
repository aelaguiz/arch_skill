# Host-Native Agent Policy and Skill Migration Plan

Status: implemented and independently verified; publication ready
Date: 2026-07-11
Repository: `/Users/aelaguiz/workspace/arch_skill`
Companion substrate: `docs/HOST_NATIVE_AGENT_POLICY_AND_SKILL_MIGRATION_PLAN_2026-07-11_DAG.md`

## Executive decision

The skill suite should become **host-native first, not external-process first**.

When a skill is running inside Codex and the required worker can be a Codex/OpenAI worker with the current host's tools, permissions, lifecycle, model controls, and isolation, it should generally use Codex's native agent system. The equivalent rule applies inside Claude Code. A separate CLI session is a higher-cost lane, not a forbidden one: use it when a concrete benefit justifies the added process, coordination, and shared-state cost. Common reasons include a different provider, an exact model/profile or structured interface the native tool does not expose, durable background work beyond the parent lifecycle, a separate worktree or permission boundary, or an explicit user request for that external lane.

One practical reason for the Codex preference is operational: the user has observed independent Codex CLI instances contending on Codex's shared SQLite write-ahead-log state and, under enough concurrent activity, locking up the wider system. That observation should inform judgment rather than become a categorical rule. One external Codex session may be the right trade when it buys a real capability; several unnecessary parallel Codex processes are more expensive and deserve more scrutiny. The policy should explain that mechanism and let the agent weigh the expected benefit, concurrency, and host state instead of enforcing a ban, approval gate, or fixed process threshold.

Every use of an agent must separately choose:

1. the worker's role;
2. its starting context;
3. whether later work resumes that worker or starts a new one;
4. its permissions and filesystem isolation;
5. its coordination topology;
6. its transport;
7. the evidence and state it must return for integration.

The current suite often collapses all seven decisions into one instruction such as “use a fresh external agent,” “maximize native parallel agents,” or “delegate through `$agent-delegate`.” That is the root design error. Freshness is a context choice, parallelism is a topology choice, and Claude/Codex CLI invocation is a transport choice. They are not synonyms.

The owning source of truth should be a new shared runtime contract:

`skills/_shared/agent-orchestration-policy.md`

Agent-using skills should read that policy and retain only their local role, task-slicing, handoff, and result rules. The suite should not gain a universal runner, dispatcher script, controller, or manifest. Agent judgment stays in the skill; the shared policy standardizes the decisions that are currently duplicated and contradictory.

## Scope and evidence basis

This review covers all 46 locally authored live packages under `skills/<slug>/SKILL.md`, their live `references/` files, and the 35 `agents/openai.yaml` metadata files present in the analyzed baseline. The implementation adds runtime metadata for `stepwise`, bringing the final live metadata count to 36. It also reads the one additional installed vendored package, `thermo-nuclear-code-quality-review`, as an observe-only surface. Generated or untracked `build/` copies are excluded from runtime conclusions. The vendored review package discusses parallel code structure but does not dispatch agents or own this repository's agent policy.

The Codex analysis is grounded in `/Users/aelaguiz/workspace/codex` at commit:

`1f0566d3f59298d1bb88820a0d35294f1eeb07ea` — 2026-07-09, `exec-server: expose process helper to outer sandbox (#31937)`

The Claude analysis is grounded in the installed `claude` CLI version `2.1.207` and Anthropic's current official documentation as read on 2026-07-11.

The `arch_skill` working tree changed concurrently during this audit. The analysis therefore describes the live files observed on 2026-07-11, not a clean-commit snapshot. No concurrently modified skill file is changed by this document.

## The target mental model

### Agent use is a seven-field dispatch decision

The shared policy should require the invoking agent to settle these fields before dispatch. They do not need to be serialized into YAML; a concise prompt or parent worklog may carry them.

| Field | Required question | Canonical choices |
|---|---|---|
| Role | What independent result is this worker accountable for? | explorer, implementer, critic, verifier, specialist, coordinator |
| Transport | Who owns the child lifecycle? | local/no child, native child, host-native background session, external same-provider session, external cross-provider session |
| Starting context | What conversation state should the child receive? | clean, bounded recent turns, full fork |
| Continuation | What happens after its first result? | one-shot, same-agent follow-up, same-session resume, fresh replacement |
| Isolation | What may it read or write, and where? | read-only, shared worktree with disjoint scope, isolated worktree, separate environment/account |
| Topology | Who coordinates whom? | parent-child, peer team, sequential handoff |
| Result contract | What must come back? | findings/evidence, changed paths, proof, blockers, session/agent handle when continuation is intended |

Transport must be chosen last. The role and context requirements determine whether the native host is sufficient; a preferred executable must not determine the workflow in advance.

### Canonical context vocabulary

The shared policy should use these terms consistently:

- **Clean**: the child receives its task brief, repository instructions available to that child type, and named artifacts, but none of the parent's conversation history. Use this for independent reviews, cold reads, self-contained disk-grounded exploration, and most parallel mapping.
- **Bounded fork**: the child receives only a named number of recent parent turns. Use this when recent user decisions matter but the full conversation would add anchoring and token cost. Codex MultiAgentV2 exposes this directly; Claude Code currently does not expose an equivalent native partial-history fork.
- **Full fork**: the child receives the parent's available conversation history. Use this only when important truth exists in chat and would be materially lossy to restate. It is not the default for a reviewer.
- **Resume**: the same child/session continues with its existing history. Use this for incremental feedback, repair, or the next step of the same role and objective.
- **Fresh replacement**: a new clean child takes over. Use this for independent verification, a role change, a poisoned or over-anchored history, material upstream truth changes, or a deliberately cold second opinion.

Files and durable logs should carry workflow truth whenever practical. A full conversation fork is not a substitute for keeping the plan, evidence, or decision record current on disk.

### Canonical transport vocabulary

- **Local/no child**: the parent does the work. This is correct for small, tightly coupled, sequential, or coordination-heavy tasks.
- **Native child**: use the active host's built-in child-agent facility. This is the default for same-host work.
- **Host-native background session**: use a first-party durable/background facility when the work must outlive the current interactive turn or needs the host's own worktree/session management.
- **External same-provider session**: start a separate Claude or Codex CLI session from inside that same provider's host. This is a higher-cost lane to choose when its concrete model, lifecycle, isolation, or automation benefit is worth the added process and shared-state overhead; it is not the normal way to get a clean context.
- **External cross-provider session**: start a provider different from the active host. This is the normal external-consult case.

“Native” describes lifecycle ownership, not whether the implementation happens to use another operating-system process internally. Claude's background-agent supervisor is still a host-native product surface; a skill manually shelling out to `claude -p` and parsing files in `/tmp` is an external harness surface.

### Operational cost of independent Codex processes

Native Codex children keep same-host delegation under Codex's own agent lifecycle and concurrency manager. A separately launched `codex exec` is another top-level process with its own startup, session, and shared-state activity. In this environment, concurrent independent Codex processes have been observed contending on global SQLite/WAL state strongly enough to degrade or lock up the system.

This is a decision factor, not a prohibition:

- If native agents provide the required model capability, context, continuation, tools, and lifecycle, they usually avoid unnecessary process and shared-state pressure.
- An external Codex session can still be worthwhile for an exact profile, durable independent lifecycle, structured automation receipt, isolation boundary, or another concrete advantage.
- The cost rises with unnecessary parallel external Codex fanout. Prefer the smallest useful fanout and serialize when current host behavior makes contention likely, but do not invent a universal numeric limit.
- The agent should be able to explain what the external process buys. It does not need a formal exception record or new user approval unless the surrounding workflow already requires one.

The durable principle is to compare the operational cost with the expected benefit. “Never launch external Codex” and “always launch external workers” are equally blunt substitutes for judgment.

## What Codex actually provides

### Native children are real child threads

Codex MultiAgentV2 creates a new thread through the same `AgentControl`, assigns it a canonical task path, gives it the active turn's runtime configuration, and exposes parent/child messaging. It is not merely a prompt macro around `codex exec`.

Relevant source:

- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs:40-129`
- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/agent/control/spawn.rs:230-425`
- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/tools/handlers/multi_agents_common.rs:154-231`

The child config refreshes the current model/provider/reasoning settings and copies the active approval policy, permission profile, working directory, developer instructions, and base instructions. A Codex child therefore shares the active host's runtime capabilities unless an exposed child override says otherwise.

### MultiAgentV2 has three explicit starting-context modes

| `fork_turns` | Meaning | Policy use |
|---|---|---|
| `"none"` | No surrounding parent conversation is forked | Clean reviewer, independent explorer, self-contained implementation slice |
| positive integer string, for example `"3"` | Keep the last N fork-turn boundaries | Recent-decision context without full-history anchoring |
| `"all"` | Full-history fork | Only when the task materially depends on the parent conversation |
| omitted | Defaults to `"all"` | Unsafe as an implicit suite default; agent-using skills should choose explicitly |

The default is implemented at `multi_agents_v2/spawn.rs:199-224`, and the tool schema documents the same behavior at `tools/handlers/multi_agents_spec.rs:595-634`. This means a skill that says only “spawn a fresh native reviewer” can accidentally do the opposite in Codex: an omitted argument produces a full parent-history fork.

The bounded mode counts real user-message or trigger-turn inter-agent boundaries, not arbitrary model messages. See `thread_rollout_truncation.rs:62-126,208-230`.

### A Codex fork is sanitized, not a byte-for-byte transcript copy

Codex keeps system, developer, and user messages and assistant final answers. It drops reasoning items, tool calls and outputs, web/image operations, and inter-agent communication records from the child rollout. A full fork preserves reference-context items; a bounded fork drops pre-turn startup context and rebuilds context on the child turn.

Relevant source:

- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/agent/control/spawn.rs:45-78,493-582`
- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/thread_rollout_truncation.rs:208-230`

Policy implication: “full fork” means inherited conversational conclusions and instructions, not inherited hidden reasoning or the parent's complete tool trace. A child that needs exact command output or evidence must receive a file path or explicit task material.

### Full forks constrain model overrides

MultiAgentV2 rejects agent-type, model, and reasoning-effort overrides on full-history forks. Clean and bounded children may accept those overrides when the active tool schema exposes them. The default configuration currently sets `hide_spawn_agent_metadata: true`, so this session's native `spawn_agent` surface exposes task, message, and `fork_turns`, but not model/role/effort selection.

Relevant source:

- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs:67-85`
- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/tools/handlers/multi_agents_common.rs:193-203`
- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/tools/handlers/multi_agents_spec.rs:595-640`
- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/config/mod.rs:1144-1179`

Policy implication: an exact Codex profile such as `yolo`, a pinned model, or a particular effort tier can be a legitimate reason to use an external same-provider session when the native surface does not expose it. “Same provider” alone is not proof that native can satisfy every execution requirement.

### Continuation is native too

MultiAgentV2 supports continued work without a new CLI process:

- `followup_task` delivers a message and triggers another turn on the same child.
- `send_message` queues a message without necessarily triggering a turn.
- `wait_agent` waits for mailbox or status activity; it should be used sparingly rather than as a polling loop.
- resident V2 child threads can be reloaded from stored rollouts.

Relevant source:

- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/tools/handlers/multi_agents_v2/followup_task.rs:24-38`
- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/tools/handlers/multi_agents_v2/send_message.rs:24-38`
- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/agent/control/spawn.rs:584-766`

Policy implication: “resume the same worker after review feedback” does not inherently require `$agent-delegate` or `codex exec resume`. If the native child is still in the active session, use the native follow-up path.

### Native children share filesystem and parent runtime policy

Codex's own usage guidance states that all agents use the same current directory and filesystem. The child also inherits the active approval and permission settings. Native children are therefore context-isolated threads, not automatically read-only sandboxes or isolated worktrees.

The default V2 limit is four concurrent threads per session including the root, leaving at most three active child slots under the default configuration.

Relevant source:

- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/config/mod.rs:207-261,1431-1444`
- `/Users/aelaguiz/workspace/codex/codex-rs/core/src/tools/handlers/multi_agents_common.rs:206-231`

Policy implications:

- Do not dispatch overlapping write scopes into the shared checkout.
- Do not call a child “read-only” as though the prompt changed its runtime permissions. When Codex cannot enforce a child-specific read-only profile, state the behavioral restriction and have the parent compare repository state before and after the review.
- Do not let children recursively fan out just because the tool permits it. The parent owns the concurrency budget and assigns nested spawning explicitly.

### Legacy V1 differs

The older MultiAgentV1 handler uses `fork_context: bool` with a default of `false`; V2 replaces it with `fork_turns` and defaults omitted values to full history. See `tools/handlers/multi_agents/spawn.rs:45-140,231-241`.

The shared policy must describe behavior by detected capability, not assume every Codex installation has the V2 schema. If `fork_turns` is unavailable, use the host's supported clean/fork control or give a clean child a complete task brief.

## What Claude Code actually provides

### Named and built-in subagents start clean

Claude Code's ordinary named, built-in, and custom subagents run in separate context windows. By default they do not see the parent conversation, previously invoked skills, or files already read by the parent. They receive their own system prompt, a delegation message, repository context appropriate to that agent type, and any explicitly preloaded skills.

Explore and Plan are special: they are read-only and skip `CLAUDE.md` and the parent git snapshot. General-purpose and custom subagents normally load them. Claude subagents can also define tool restrictions, permission mode, model, effort, MCP scope, and `isolation: worktree`.

Source: [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents).

Policy implication: inside Claude, a cold reviewer or independent explorer normally needs an ordinary native subagent, not a new `claude -p` subprocess.

### Claude has an explicit full-conversation fork

An explicit forked subagent inherits the entire parent conversation, including the same system prompt, tools, model, and message history. Its tool calls remain outside the main conversation and only its result returns. Anthropic describes model-driven fork spawning as experimental, while the explicit fork feature is available in current Claude Code.

Source: [Claude Code forked subagents](https://code.claude.com/docs/en/sub-agents#fork-the-current-conversation).

Use this only for work that genuinely needs the parent's chat history or for parallel approaches from the same conversational state. A named subagent is the cleaner default for a cold review.

### Claude's `context: fork` skill field is a terminology trap

In Claude skill frontmatter, `context: fork` currently runs the skill in a new isolated subagent and explicitly does **not** give that subagent the parent conversation history. The skill body becomes the task prompt, and `agent:` selects the subagent environment. That is the opposite of what an explicit forked subagent means in the subagent documentation.

Source: [Claude Code skills: run skills in a subagent](https://code.claude.com/docs/en/slash-commands#run-skills-in-a-subagent).

The shared policy must not use the bare word “fork” without naming the host surface:

- **Claude explicit conversation fork** means full parent history.
- **Claude skill `context: fork`** means isolated skill execution without parent conversation history.

### Claude supports native resume

Each ordinary subagent invocation is fresh unless Claude resumes an existing child by its agent ID/name. A resumed subagent retains its full history, tool calls, results, and reasoning. Explore and Plan are one-shot and cannot be resumed; use general-purpose or a custom subagent when continuation matters. Subagent transcripts persist within the parent session and can survive a Claude restart when the main session is resumed.

Source: [Claude Code subagent resume behavior](https://code.claude.com/docs/en/sub-agents#resume-subagents).

Policy implication: repair feedback for the same role should go back to the same resumable subagent. A fresh critic should be a new child, not a resumed implementer.

Claude also permits nested subagents, but the current depth limit is five levels below the main conversation. A depth-five child does not receive the Agent tool. A fork cannot spawn another fork, although it can spawn ordinary child types. These are runtime capabilities, not permission for recursive fanout; the shared policy should still leave nested spawning off unless the parent assigns it.

### Agent teams are for peer coordination, not ordinary fanout

Claude agent teams create fully independent sessions with their own contexts, a shared task list, and direct teammate-to-teammate messages. A teammate receives normal project context and the lead's spawn prompt, but not the lead conversation history. Teammates start with the lead's permission settings. Their model does not necessarily inherit the lead's active model unless the default or spawn instruction selects that behavior, while their effort setting currently follows the lead. They cost more and add coordination overhead. Anthropic recommends them for work where peers must communicate or challenge one another, not for focused children that only need to report to a parent.

Source: [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams).

Policy implication: ordinary skill parallelism should remain parent-child subagents. Use a team only when direct peer exchange is necessary to the result, such as competing hypotheses that must cross-examine one another or independently owned modules that need active cross-layer coordination.

Current team limitations also matter to policy: in-process teammates are not restored by ordinary session resume, teammates cannot create nested teams, and per-teammate permission mode cannot be selected at spawn. A skill that needs durable exact-child resume or stronger isolation should not choose a team merely because it wants several workers.

### Background agents are the durable native lane

Claude's agent view and `claude --bg` manage independent full Claude Code conversations that keep running without an attached terminal. Before editing, a background session normally moves itself into an isolated git worktree. It can be attached, replied to, and resumed through the host's supervisor.

Source: [Claude Code agent view and background agents](https://code.claude.com/docs/en/agent-view).

Policy implication: when the requirement is durability or background work rather than cross-provider consultation, prefer the host-native background surface over a skill-owned `/tmp` harness where available.

### CLI and SDK sessions still have valid roles

Claude CLI `--resume` continues a session, while `--fork-session` copies its history into a new session ID. The Agent SDK similarly supports resuming full session history or forking it into a new session. Session history and filesystem state are distinct; moving a transcript does not move repository changes.

Sources: [Claude Code CLI reference](https://code.claude.com/docs/en/cli-usage), [Claude Agent SDK sessions](https://code.claude.com/docs/en/agent-sdk/sessions).

These are useful automation interfaces, but a skill should not choose them merely to get fresh context or another Claude worker. Native subagents already provide that.

## The proposed shared policy

The new `skills/_shared/agent-orchestration-policy.md` should be concise enough to load in every agent-using skill but complete enough that those skills do not restate host behavior. Its normative content should be the following.

### 1. Decide whether a child helps

Keep the work in the parent when it is small, tightly coupled, sequential, likely to require repeated parent judgment, or would cost more to brief and integrate than to do directly. Spawn only a concrete, bounded slice that can make useful progress independently.

Parallelism is an optimization, not a completion requirement. Do not “maximize agents.” Use the smallest fanout that matches genuinely independent work and the host's available slots.

### 2. Prefer the active host's native child and choose external transport deliberately

Prefer a native child when the provider, model capability, tool access, lifecycle, permissions, and isolation fit the job. This normally keeps same-host explorers, implementers, critics, and verifiers under the host's own lifecycle manager. Inside Codex it also avoids creating independent top-level Codex processes that may add SQLite/WAL contention under concurrent use.

External sessions remain a valid tool. Choose one when its concrete benefit is worth the added process, coordination, and shared-state cost. Common reasons include:

- the requested participant is a different provider;
- the user explicitly requests a particular external runtime or CLI lane;
- an exact model, profile, effort, service tier, or role is required and the native tool cannot select it;
- the work must survive beyond the parent session and no adequate host-native background surface is available;
- the work needs an isolated worktree, account, machine, environment, or permission boundary the native child cannot provide;
- automation requires a stable structured-output/event/transcript interface unavailable from the native child;
- native agents are unavailable or disabled.

These reasons are illustrative, not an exhaustive permission list. A new situation should be decided from the same underlying question: what does the separate process buy, and is that benefit worth its operational cost here?

The desire for more concurrency does not automatically make an external process the better choice. Weigh the likely speedup against process startup, integration cost, filesystem ownership, and—in Codex—observed shared SQLite/WAL contention. Reduce or serialize external fanout when that is the more reliable trade, without imposing a fixed global threshold.

The parent should be able to explain a material same-provider external choice in ordinary prose. Do not create a mandatory approval gate, formal exception record, or canned decision form unless the surrounding workflow already needs one.

### 3. Choose starting context explicitly

- Use **clean** for independent audits, cold reads, broad mapping slices, and disk-grounded work with a complete brief.
- Use **bounded:N** for recent user decisions in Codex when full history is unnecessary.
- Use **full fork** only when chat-only context is material and restating it would be lossy.
- Choose Codex `fork_turns` explicitly in a skill-directed spawn because the current V2 omission default is `all` and may silently defeat the intended context isolation.
- Name the exact Claude surface—explicit conversation fork or skill `context: fork`—because they have opposite history semantics.

### 4. Choose continuation explicitly

Resume the same child when the role, objective, artifact, and underlying truth are unchanged and the new message is incremental feedback or repair. Start a clean replacement when the role changes, an independent opinion is required, upstream inputs invalidate the prior reasoning, the child is anchored or contaminated, or the parent intentionally wants a cold gate.

Do not use “latest session.” Preserve and use the exact native agent ID or external session handle when continuation is intended.

### 5. Separate context from permissions and filesystem isolation

A clean context is not a read-only sandbox. A full fork is not a shared-worktree guarantee. State all three independently.

- Prefer enforced read-only tools/permissions for reviewers when the host exposes them.
- On Codex surfaces that inherit parent permissions, pair the no-edit prompt with a parent repository-state check.
- Give parallel writers disjoint path ownership or separate worktrees. Never dispatch two writers to overlapping files in one checkout.
- The parent owns integration, conflict resolution, and final verification.
- Do not let a child commit, push, publish, message people, or mutate external state unless the task explicitly assigns that authority.

### 6. Parent owns fanout and nesting

Nested spawning is off by default even when the runtime permits it. A child may spawn another child only when the parent explicitly grants a concurrency budget and non-overlapping task scope. Remove generic child prompts that say “maximize parallelism” or encourage children to launch agents on their own.

### 7. Require an integration-ready result

Every child returns:

- its conclusion or completed slice;
- exact evidence or changed paths;
- verification performed and not performed;
- blockers or uncertainty;
- the agent/session handle only when continuation is intended.

The parent spot-checks evidence, audits changes, accounts for every child, and decides whether to accept, resume, replace, or discard the result.

## Authoring standard for the migration

All policy and skill-prose work in this migration should explicitly apply `$skill-authoring` and `$prompt-authoring`.

`$skill-authoring` governs ownership and package shape:

- The shared policy owns only the reusable cross-skill decisions: whether a child helps, starting context, continuation, transport tradeoffs, permissions/isolation, topology, and parent integration.
- Each workflow skill retains its distinct job, domain judgment, task slicing, handoff, and result contract. It should reference the shared policy instead of copying a local mini-policy.
- `agent-delegate` and other runtime adapters own deterministic invocation mechanics and receipts, not the parent workflow's reasoning.
- The policy stays prompt-first and self-contained. Do not add a dispatcher, controller, parameter schema, decision form, or script merely to enforce prose the agent can follow with judgment.
- Detailed source research remains in this plan; the shared runtime file carries only the durable explanation and operating principles needed during execution.

`$prompt-authoring` governs how the policy teaches:

- Explain the mechanism behind a preference. For external Codex, name the extra top-level process and observed shared SQLite/WAL contention so the agent understands why concurrency can be costly.
- State the desired outcome and tie-breakers, then let the agent inspect the active host, requested model/provider, lifecycle, isolation, and likely concurrency before choosing.
- Use the external-process reasons as examples and recognition tests, not a finite permission list.
- Preserve useful freedom. Do not turn one operational incident into “never,” a magic process count, mandatory user approval, or a required rationale template.
- Make strong and weak decisions recognizable: strong decisions connect transport to a concrete benefit and account for operational cost; weak decisions shell out reflexively merely to obtain clean context, parallelism, or continuation that the host already provides.
- Patch the owning section when behavior is wrong. Do not repeat the SQLite warning or native-first preference throughout every skill.

The quality bar is an agent that can explain and make a good new decision in an unanticipated situation, not an agent that memorizes an allowed-actions table.

## Findings

### F1 — High: the suite has no shared owner for agent semantics

Finding: Agent dispatch semantics have split ownership and no shared policy.
Severity: High

External orchestration skills define subprocess-first behavior, while review and implementation skills independently ban external harnesses and say to use native agents. Neither side defines a common context, continuation, permission, or isolation vocabulary.

Evidence:

- `skills/agent-delegate/SKILL.md:10-16,65-98,141-162`
- `skills/fresh-consult/SKILL.md:11-14,62-87,128-137`
- `skills/plan-conductor/SKILL.md:16-18,91-112,204-214`
- `skills/plan-implement/SKILL.md:63-69`
- `skills/plan-audit/SKILL.md:73`
- `skills/cynical-code-review/SKILL.md:61-65`
- `skills/exhaustive-code-review/SKILL.md:46-49`

Why it matters: the same conceptual task gets a different transport solely because of which skill routed it, not because of provider, context, lifecycle, or isolation needs.
Smallest fix: add `skills/_shared/agent-orchestration-policy.md`; require agent-using skills to read it and delete their duplicated generic transport rules.
Owner: `skills/skill-authoring/SKILL.md`, `skills/agent-delegate/SKILL.md`, `skills/plan-implement/SKILL.md`

### F2 — High: core orchestrators make external same-provider sessions the default

Finding: Same-provider work is routed through external CLI sessions by default.
Severity: High

`agent-delegate`, `fresh-consult`, `model-consensus`, `plan-conductor`, `stepwise`, and the spawned-harness lane of `arch-epic` hard-code or strongly prefer separately launched Claude/Codex/Grok/Cursor sessions. This is appropriate for cross-provider participation and some exact-profile workflows, but not as the general same-host route.

Evidence:

- `skills/agent-delegate/SKILL.md:3,10-16,141-153`
- `skills/fresh-consult/SKILL.md:3,11-14,128-137`
- `skills/model-consensus/references/workflow-contract.md:103-130`
- `skills/plan-conductor/SKILL.md:3,16-18,105-112,204-214`
- `skills/stepwise/SKILL.md:3,49-68`
- `skills/arch-epic/SKILL.md:3,143-185`
- User-reported operational evidence, 2026-07-11: concurrent independent Codex CLI instances can contend on shared SQLite/WAL state and lock up the wider system.

Why it matters: clean context, parallelism, or resumability incorrectly implies a shell-out even though both Codex and Claude have native clean children and same-child continuation. Inside Codex, reflexive shell-outs also multiply top-level processes and can amplify the observed shared-state contention.
Smallest fix: make child transport a deliberate decision at every dispatch point and use the external adapter when its concrete benefit justifies the added operational cost.
Owner: `skills/agent-delegate/SKILL.md`, `skills/fresh-consult/SKILL.md`, `skills/model-consensus/SKILL.md`, `skills/plan-conductor/SKILL.md`, `skills/stepwise/SKILL.md`, `skills/arch-epic/SKILL.md`

### F3 — High: native context mode is usually unspecified

Finding: Native-agent instructions do not choose clean, bounded, full-fork, or resume context.
Severity: High

The native-first skills say “native parallel agents,” “fresh reviewer,” or “parallel read-only agents” without selecting clean, bounded, full-fork, or resume semantics. This is especially risky in Codex V2 because omitted `fork_turns` defaults to full history.

Evidence:

- `skills/plan-audit/SKILL.md:73`
- `skills/plan-implement/references/native-subagent-contract.md:7-59`
- `skills/cynical-architecture-review/SKILL.md:67-71,106,123`
- `skills/cynical-code-review/SKILL.md:61-65,90,105`
- `skills/cynical-cruft-removal/SKILL.md:70-74,105,124`
- `skills/exhaustive-code-review/SKILL.md:46-49,76`
- `skills/skill-flow/references/parallel-walk-protocol.md:3-6,31-43,141-153`
- `skills/audit-loop/SKILL.md:30,76-95`
- `skills/audit-loop-sim/SKILL.md:31,82-100`
- `skills/comment-loop/SKILL.md:31,74-91`

Why it matters: independent critics may inherit the exact completion narrative they are supposed to challenge, broad mapping agents may receive unnecessary tokens, and “fresh” behavior differs by host and invocation surface.
Smallest fix: default independent native slices to clean context and require every deviation to state bounded/full-fork or exact-child resume explicitly.
Owner: `skills/plan-audit/SKILL.md`, `skills/plan-implement/references/native-subagent-contract.md`, `skills/skill-flow/references/parallel-walk-protocol.md`, `skills/exhaustive-code-review/SKILL.md`

### F4 — High: “fresh,” “fork,” and “resume” are overloaded

Finding: Context and continuity terms have incompatible meanings across skills and hosts.
Severity: High

`fresh` sometimes means a new CLI session, sometimes a fresh review phase in the same goal session, and sometimes merely “re-read the repository.” Codex V2 full-forks by default; Claude named subagents start clean; Claude explicit forks inherit full history; Claude skill `context: fork` starts isolated without history.

Evidence:

- `skills/fresh-consult/SKILL.md:3,74-85`
- `skills/arch-docs/SKILL.md:18,53,106-109`
- `skills/audit-loop/SKILL.md:76-97`
- `skills/stepwise/SKILL.md:49-68`

Why it matters: skill authors cannot safely infer behavior from one adjective.
Smallest fix: define canonical clean/bounded/full-fork/resume/fresh-replacement terms and map each one to exact Codex and Claude surfaces.
Owner: `skills/prompt-authoring/SKILL.md`, `skills/skill-authoring/SKILL.md`, `skills/fresh-consult/SKILL.md`

### F5 — High: context isolation is confused with permission and worktree isolation

Finding: A clean conversation is treated as though it also enforced no-write or filesystem isolation.
Severity: High

Several external children run unsandboxed in the shared checkout and rely on a prompt to remain read-only. Native Codex children also share filesystem and inherited permissions. The current suite does not consistently distinguish a clean prompt context from enforced no-write capability or from a separate worktree.

Evidence:

- `skills/agent-delegate/SKILL.md:3,93-98,153`
- `skills/fresh-consult/SKILL.md:3,82-87,137`
- `skills/plan-conductor/references/delegation-and-monitoring.md:11-21`
- Codex `config/mod.rs:254-257` and `multi_agents_common.rs:206-231`

Why it matters: “read-only” reviewers can still alter files; parallel writers can collide; a clean session can produce dirty shared state.
Smallest fix: make context, runtime permissions, and checkout/worktree placement separate mandatory dispatch fields; require parent state checks where no enforced read-only child exists.
Owner: `skills/agent-delegate/SKILL.md`, `skills/fresh-consult/SKILL.md`, `skills/plan-conductor/references/delegation-and-monitoring.md`

### F6 — High: recursive fanout is encouraged without ownership or slot budgets

Finding: Child prompts encourage nested parallelism without parent-owned scope or concurrency limits.
Severity: High

Some worker and reviewer prompts instruct children to maximize parallel-agent use while merely telling them not to invoke subagent-spawning skills. Both current Codex and Claude permit nested subagents. That restriction does not prevent native recursive fanout.

Evidence:

- `skills/model-consensus/SKILL.md:128`
- `skills/fresh-consult/references/consult-prompt-and-output.md:59`
- `skills/plan-conductor/references/worker-prompt-contract.md:14-51`
- `skills/exhaustive-code-review/SKILL.md:46,76`

Why it matters: the parent loses control of concurrency, write ownership, cost, and result accounting. On default Codex V2 there are only four concurrent threads including root.
Smallest fix: make nested spawning off by default and replace “maximize parallelism” with parent-assigned, non-overlapping slices under an explicit slot budget.
Owner: `skills/model-consensus/SKILL.md`, `skills/fresh-consult/references/consult-prompt-and-output.md`, `skills/plan-conductor/references/worker-prompt-contract.md`, `skills/exhaustive-code-review/SKILL.md`

### F7 — Medium: good continuation semantics are trapped inside external adapters

Finding: Fresh/resume/replace workflow semantics are encoded as external session mechanics.
Severity: Medium

`stepwise`, `fresh-consult`, `agent-delegate`, `model-consensus`, and `plan-conductor` contain useful distinctions between a fresh worker, same-session repair, fresh critic, and downstream respawn after poisoned upstream work. Those are workflow semantics and should survive transport changes. They should not be encoded only as CLI session-ID behavior.

Evidence:

- `skills/stepwise/SKILL.md:49-68,76-98`
- `skills/stepwise/references/session-resume.md:7-26`
- `skills/fresh-consult/SKILL.md:74-85,131-137`
- `skills/agent-delegate/SKILL.md:72-98,148-162`
- `skills/plan-conductor/SKILL.md:105-106,146,204-214`

Why it matters: native agents cannot benefit from the suite's strongest continuity design even though both hosts support exact-child follow-up.
Smallest fix: lift continuation rules into the shared policy and let each orchestrator preserve exact-role resume independently of native or external transport.
Owner: `skills/stepwise/SKILL.md`, `skills/fresh-consult/SKILL.md`, `skills/agent-delegate/SKILL.md`, `skills/plan-conductor/SKILL.md`

### F8 — Medium: an “external never” correction would also be wrong

Finding: A native-only rule would erase legitimate capability and lifecycle exceptions.
Severity: Medium

Codex's current native surface may hide model/profile/effort selection, and a full fork explicitly rejects those overrides. Detached durability, structured automation output, separate accounts/environments, and cross-provider participants are also real requirements.

Evidence:

- `skills/codex-review-yolo/SKILL.md:33,65,97`
- `skills/model-consensus/SKILL.md:71-74`
- `skills/agent-delegate/SKILL.md:65-86`
- `skills/codex-babysit/SKILL.md:53-57,93-109`

Why it matters: replacing every CLI path with native children would break exact-profile review, exact-model consensus, cross-provider consults, work beyond a parent lifecycle, and some automation receipts.
Smallest fix: adopt a native-first tradeoff principle with explanatory examples, not a native-only rule or exhaustive exception list.
Owner: `skills/agent-delegate/SKILL.md`, `skills/codex-review-yolo/SKILL.md`, `skills/model-consensus/SKILL.md`, `skills/codex-babysit/SKILL.md`

### F9 — High: the skill-flow DAG extractor is blind to this repository's real links

Finding: The DAG extraction rule suppresses the repository's normal backticked skill references.
Severity: High

The required extraction whitelist ignores inline-code spans. The repository's
normal writing style renders live routes in both dollar-prefixed
`` `$skill-slug` `` spans and exact unprefixed `` `skill-slug` `` spans. The
protocol-correct 46-node baseline DAG therefore contains one extracted edge:
`prompt-authoring -> skill-authoring` from an unbackticked frontmatter mention.
The controlled implementation walk confirmed that repairing only the dollar
form would still hide roughly one hundred unique exact-peer relationships.

Evidence:

- `skills/skill-flow/references/parallel-walk-protocol.md` extraction rules
- `skills/plan-conductor/SKILL.md:16,58-67,157-158,204,222-235`
- `skills/arch-epic/SKILL.md:3,10,94-102`
- `skills/arch-step-goal-prompt/SKILL.md:36-52`
- `skills/stepwise/SKILL.md:35-40`
- companion DAG for the exact extracted substrate

Why it matters: degree-based “dead skill,” isolation, over-promotion, and missing-route findings can be confidently wrong.
Smallest fix: count semantically valid backticked `$skill-name` tokens and
exact resolving backticked peer slugs while continuing to exclude fenced code,
shell variables, commands, modes, filenames, and incidental code words, then
regenerate the substrate.
Owner: `skills/skill-flow/references/parallel-walk-protocol.md`, `skills/skill-flow/references/dag-substrate-format.md`

### F10 — Medium: runtime metadata and install verification can drift from doctrine

Finding: Package metadata and installed shared-file proof can diverge from live skill doctrine.
Severity: Medium

Thirty-five baseline packages have `agents/openai.yaml`; several repeat external/native behavior from their `SKILL.md`. The migration adds a 36th metadata file for `stepwise`. The `_shared` directory is already installed for Agents/Codex, Claude, and Gemini, but `make verify_install` initially checks only the existing shared planning and model-resolution files.

Evidence:

- `Makefile:6-8,190-194,226-230,255-259`
- `Makefile:280-281,315-316,345-346`
- `README.md:52,236,462-516`

Why it matters: changing only `SKILL.md` leaves routing text stale, while adding the shared policy without a verify assertion makes an incomplete install easier to miss.
Smallest fix: make skill-authoring require metadata co-edits and add explicit shared-policy checks to the existing install verification targets.
Owner: `skills/skill-authoring/SKILL.md`, `skills/skill-authoring/references/skill-pattern-contract.md`

## Complete 46-skill disposition matrix

Priority legend:

- **P0 redesign**: the skill owns transport and currently makes the wrong default or hard-codes one runtime mechanism.
- **P1 policy consumer**: keep the skill's job, but make native context, continuation, permissions, or fanout explicit through the shared policy.
- **Intentional external/durable lane**: the external or long-lived session has a real capability or lifecycle job; explain that job and prevent generic routing from selecting it reflexively.
- **Governance**: the skill does not dispatch workers but should enforce the shared contract when it authors or audits agent guidance.
- **No runtime change**: no agent-dispatch behavior was found; do not add irrelevant policy context.

| # | Skill | Current stance | Disposition | Required change |
|---:|---|---|---|---|
| 1 | `agent-definition-auditor` | Audits agent-definition markdown; does not dispatch | Governance | Add an audit lens: agent instructions must separate transport, context, continuation, isolation, and topology and must not duplicate or contradict the shared policy. |
| 2 | `agent-delegate` | External Claude/Codex/Cursor/Grok workers, normally resumable, unsandboxed shared worktree | **P0 redesign** | Recast as the explicit external-session adapter. Prefer native use when it supplies the needed capability without the extra process cost. Preserve cross-provider, exact-model, durable-session, and structured-receipt lanes. Require deliberate transport and context/continuation choices, not an approval gate or finite exception test. |
| 3 | `agent-history` | Searches local agent session history; no dispatch | No runtime change | Keep focused on history search. Its routes to consult/delegation skills can remain, but those peers will make the transport decision under the shared policy. |
| 4 | `agents-md-authoring` | Authors repository agent instructions; no dispatch | Governance | When authored `AGENTS.md` text discusses agents, require host-native-first behavior and explicit clean/fork/resume semantics; point to a repo-local policy rather than pasting this entire contract. |
| 5 | `amir-publish` | Publishes this skill repository; no dispatch | No runtime change | None. Do not make publishing load agent policy. |
| 6 | `arch-docs` | Native goal-loop continuation plus a “fresh” evaluator with unspecified child semantics | P1 policy consumer | Define the evaluator as a new clean native critic while the host session is active. If an auto controller must continue after the parent turn ends, explain that the same-provider external/background launch is buying lifecycle continuity rather than review freshness. Mapping children, if any, are clean and read-only. |
| 7 | `arch-epic` | Mixes same-session commands with explicit external planner/worker/critic harnesses | **P0 redesign** | Prefer same-host native children. Start planner/worker roles clean from durable epic/sub-plan artifacts, resume the exact role for repair, and start every independent critic clean. Retain external participants when their model, lifecycle, isolation, or automation benefit justifies the added process cost. Do not make a runner own agent judgment. |
| 8 | `arch-flow` | Read-only status/router; no dispatch | No runtime change | None. It may report which workflow is next without choosing worker transport. |
| 9 | `arch-mini-plan` | One-pass plan authoring; references agent-backed systems but does not orchestrate children | No runtime change | None unless a future edit adds actual child dispatch. Do not preload the policy merely because the subject matter mentions agents. |
| 10 | `arch-skills-guide` | Explains suite routing; no dispatch | No runtime change | Add at most a short route explanation after the migrated skills change meaning; do not duplicate the policy. |
| 11 | `arch-step` | Mostly parent-owned flow; consistency pass can use two Codex explorer agents without a context choice | P1 policy consumer | Make consistency explorers native-clean (`fork_turns: "none"` in Codex), read-only by capability where available, with disjoint lenses and parent synthesis. Use a fork only for explicitly chat-bound decisions. |
| 12 | `arch-step-goal-prompt` | Writes durable goal prompts and reviewer gates; reviewer transport/context is ambiguous | P1 policy consumer | Make generated prompts state whether each reviewer is clean, bounded, forked, or resumed and what concrete benefit motivates external execution when selected. Do not bake one provider's CLI syntax into generic goal semantics. |
| 13 | `audit-loop` | Native goal loop; parallel read-only mapping; “fresh” review context | P1 policy consumer | Use native-clean mapping children and a new clean critic. Cap fanout by independent surface families and host slots. Pair Codex prompt-only no-edit rules with a parent diff/status check. Explain controller-spawned new processes as a lifecycle mechanism, not the meaning of a fresh review. |
| 14 | `audit-loop-sim` | Same shape as `audit-loop`, with simulator access constraints | P1 policy consumer | Same context rules as `audit-loop`; additionally select a child only if it inherits the sanctioned simulator/device capabilities. Do not use external transport merely to bypass a review-context access failure without evidence. |
| 15 | `bugs-flow` | May use an external model for review; no native-first or context rule | P1 policy consumer | Prefer a native-clean critic. Resume the same implementer for accepted repair findings; use a new clean critic for the next independent gate. External review remains available when its provider, model, lifecycle, isolation, or automation benefit is worth the additional process cost. |
| 16 | `chatgpt-web` | Serial query through a logged-in ChatGPT browser surface | Intentional external/durable lane | Keep as an explicit capability/provider route, not a generic local agent. Define whether a request opens a new clean ChatGPT conversation or continues an exact prior conversation; never silently reuse an unrelated tab history. |
| 17 | `codex-babysit` | Monitors and resumes an already-running detached Codex session; does not launch task workers | Intentional external/durable lane | Keep. State that it observes an existing durable session and is not an agent-transport selector. Its “resume same session” semantics are correct for the monitoring job. |
| 18 | `codex-cleanup` | Cleans stale local Codex state; no dispatch | No runtime change | None. |
| 19 | `codex-review-yolo` | Intentionally launches `codex exec -p yolo` with captured structured artifacts | Intentional external/durable lane | Keep as the exact-profile/structured-receipt lane. Route ordinary same-host reviews to a clean native critic; use this skill when the `yolo` profile or its receipt shape provides the needed value. |
| 20 | `comment-loop` | Parallel read-only mapping plus a “fresh” review pass | P1 policy consumer | Use native-clean mapping children and a new clean critic, with bounded fanout and parent state checks. Explain post-turn controller continuation as a lifecycle mechanism, not the default meaning of “fresh.” |
| 21 | `commit-history-authoring` | Rewrites commit messages; no dispatch | No runtime change | None. |
| 22 | `contact-sheet-builder` | Deterministic presentation helper; no dispatch | No runtime change | None. |
| 23 | `cynical-architecture-review` | Explicit native parallel review; external harnesses banned; context unspecified | P1 policy consumer | Start independent review slices clean, keep them read-only, prevent nested fanout, assign non-overlapping lenses, and have the parent integrate and deduplicate. Do not full-fork the completion narrative by default. |
| 24 | `cynical-code-review` | Explicit native parallel review; external harnesses banned; context unspecified | P1 policy consumer | Same as cynical architecture review. A plan-backed slice may receive named plan paths, not the parent's entire persuasive conversation. |
| 25 | `cynical-cruft-removal` | Explicit native read-only slices; external harnesses banned; context unspecified | P1 policy consumer | Same clean native review contract; ensure reference-count findings are returned with evidence and no child edits. |
| 26 | `eli10` | Response style only; no dispatch | No runtime change | None. |
| 27 | `exhaustive-code-review` | Tells the parent to maximize native parallel agents | P1 policy consumer | Replace “maximize” with a coverage-led slice plan bounded by host slots. Use clean native reviewers, prohibit nested fanout unless assigned, maintain a child accounting ledger, and synthesize in the parent. |
| 28 | `fal-ai-tools` | Selects MCP/SDK/HTTP tool transport, not agents | No runtime change | None. Tool fallback is outside the child-agent policy unless a future workflow starts model agents. |
| 29 | `fc-branded-pdf` | Deterministic rendering/presentation helper; no dispatch | No runtime change | None. |
| 30 | `figma-best-practices` | Figma domain guidance; no dispatch | No runtime change | None. Do not confuse Figma MCP tool sessions with child-agent context. |
| 31 | `flutter-reference` | Flutter doctrine; no dispatch | No runtime change | None. |
| 32 | `fresh-consult` | Always launches external model sessions; clean first turn, exact resume for follow-ups | **P0 redesign** | Make “fresh consult” describe a clean independent reviewer, not a CLI. Inside the same host use a native-clean child by default; cross-provider or exact-model consults use the external adapter. Preserve exact-child resume for bounded follow-ups and fresh replacement for an independent later turn. |
| 33 | `goal-loop` | Parent-owned bet-and-learn loop; no child guidance | No runtime change | Keep the loop single-owner by default. If a future bet is independently delegated, it must use the shared policy, but the skill need not load it now. |
| 34 | `lilarch` | Says implementation stays local and external review needs an explicit ask; native children undefined | P1 policy consumer | Clarify that “local” means active-host execution, not necessarily one thread. Permit native children for truly independent mapping/review/low-collision slices with explicit context; keep external review available when its concrete benefit is worth the added cost. |
| 35 | `miniarch-step` | Native goal mode, optional pinned-model parallel planners, “fresh” auditor | P1 policy consumer | Use native-clean planners/auditors when the host can meet the required capability. If the exact model pin is load-bearing and native model selection is unavailable, explain the exact-model benefit of an external lane rather than pretending the native spawn can honor it. |
| 36 | `model-consensus` | Always creates two external model sessions and resumes each exact history | **P0 redesign** | Resolve each participant independently. Same-host participants use separate native-clean children; cross-provider or unavailable exact-model participants use external sessions. Resume each exact participant between rounds. Parent relay remains the default; do not use a peer team unless direct participant messaging is part of the requested method. |
| 37 | `north-star-investigation` | Parent-owned math-first loop; no dispatch | No runtime change | None. |
| 38 | `plan-audit` | Native-first and explicitly bans ordinary external acceleration; context unspecified | P1 policy consumer | Keep native-first. Start independent audit slices clean, pass plan/code paths explicitly, use enforced read-only capability when available, and require parent evidence/accounting. Fork only when the plan decision exists solely in chat. |
| 39 | `plan-conductor` | Hard-routes all implementation through external `$agent-delegate`; exact-session repairs and fresh critics | **P0 redesign** | Make worker transport selectable under the shared policy. Same-host phase workers start as native-clean children from plan/log artifacts; accepted findings return to the same worker; cold critics are new clean children. Use external workers for exact cheaper models, durability, worktree isolation, cross-provider roles, or the explicit Terra lane. Preserve the parent-as-architect boundary. |
| 40 | `plan-implement` | Good native-first design with bounded subagent work; clean/fork/resume unspecified | P1 policy consumer | Use as the positive exemplar after adding explicit context choices. Default independent children to clean; use bounded/full forks only for real chat dependency; resume the same implementer for its repair; keep parent synthesis and proof ownership. |
| 41 | `pr-authoring` | PR publication specialist; no dispatch | No runtime change | None. |
| 42 | `pr-review-followthrough` | One long-lived parent loop for polling, fixes, replies, and merge readiness; no dispatch | No runtime change | Keep single-owner continuity. If future review/fix slices use children, apply the policy, but do not add fanout merely because the loop is long-lived. |
| 43 | `prompt-authoring` | Authors reviewer/agent prompts but does not distinguish native/external or context modes | Governance | Add the seven-field dispatch decision to prompt review. A prompt that says “fresh agent,” “fork,” “resume,” or “parallel agents” must define the intended host semantics or defer to the shared policy. |
| 44 | `skill-authoring` | Authors and audits skill packages; no runtime dispatch policy | Governance | Require every agent-using skill to read the shared policy, keep only local role doctrine, update runtime metadata, and avoid scripts that own orchestration judgment. Add the policy to peer-boundary and audit checklists without wording-lock tests. |
| 45 | `skill-flow` | Mandates parallel native walkers; context unspecified; extractor hides nearly all real edges | P1 policy consumer | Use clean native walkers with no nested fanout and parent aggregation. Repair the extraction contract so code-spanned `$skill` references count while fenced shell/code false positives remain excluded. Regenerate this DAG and then rerun degree/waste analysis. |
| 46 | `stepwise` | External fresh worker per step, fresh critic, exact worker resume on failure | **P0 redesign** | Preserve its excellent context lifecycle but make transport host-aware: native-clean worker per same-host step, new native-clean critic, same-child repair, fresh downstream respawn after invalid upstream truth. Keep external sessions available when their provider, model, lifecycle, isolation, or structured-output benefit justifies the added cost. Keep deterministic helpers narrow. |

### Installed vendored package

`thermo-nuclear-code-quality-review` is the 47th package on the Agents/Codex and Claude install lists, sourced unchanged from `vendor/cursor/plugins/cursor-team-kit/skills/`. Its 192-line review contract discusses parallelizing independent program work as a code-architecture consideration, but it contains no child-agent dispatch, native/external selection, or clean/fork/resume guidance. No agent-policy change is needed, and the repository's red line prohibits editing it for this migration. If a future vendor update adds agent orchestration, enforce routing at this repository's Makefile/docs boundary or intentionally update the vendor source in a separately authorized task.

## Migration architecture by skill family

### Family A — External-session adapters

`agent-delegate` should become the single explicit adapter for editful external sessions. `fresh-consult` and `model-consensus` may call the same narrow invocation reference for participants that actually require an external process, but their primary doctrine should remain transport-neutral.

Do not route native work through `$agent-delegate` merely to preserve one public skill name. Native children are already available to the invoking agent and should be called directly under the shared policy.

The adapter should own only deterministic mechanics:

- runtime/model/profile resolution;
- safe command syntax;
- exact session-handle capture and resume;
- event/final-output capture;
- namespaced temporary paths;
- status receipt parsing.

It must not own task decomposition, role choice, context choice, review policy, or parent integration.

### Family B — Transport-neutral orchestrators

`arch-epic`, `plan-conductor`, `stepwise`, and `model-consensus` should preserve their workflow-specific roles while selecting a transport per child.

Each dispatch point should read like:

> Start a clean implementation worker from `<plan path>` and `<log path>`. Prefer a native child in the active host because it keeps same-host work under the host's own lifecycle manager. Use an external session when its provider, model, lifecycle, isolation, or automation benefit is worth the additional process and shared-state cost. Preserve its exact handle because accepted repair findings return to the same worker.

That is materially different from:

> Run `$agent-delegate` fresh-resumable.

The first statement preserves workflow intent across Codex and Claude; the second prematurely chooses a harness.

### Family C — Independent review and audit skills

`plan-audit`, the three cynical reviews, `exhaustive-code-review`, `skill-flow`, and the review phases of the loop skills should converge on one shared native-review contract:

- start independent slices clean;
- name exact paths and lenses;
- prefer enforced read-only tools;
- prohibit nested fanout unless the parent assigned it;
- return path-and-line evidence;
- do not edit;
- have the parent account for every slice and check repository state;
- use a full fork only when the review target depends on a chat-only decision.

The individual skills still own what to review and how to judge it. The shared policy owns how the reviewer is launched.

### Family D — Goal loops and fresh gates

`arch-docs`, `audit-loop`, `audit-loop-sim`, and `comment-loop` need two distinct concepts:

1. a **clean critic** that independently judges current disk truth; and
2. a **continuation mechanism** that causes the next parent pass.

The clean critic should be native when the parent session is active. If a Stop hook or goal controller necessarily starts another process after the parent turn has ended, that process is justified by lifecycle, not by review freshness. The doctrine should say so explicitly.

### Family E — Intentional external or durable boundaries

`codex-review-yolo`, `codex-babysit`, and `chatgpt-web` should remain narrow intentional lanes whose external or durable mechanism directly serves their job:

- `codex-review-yolo` owns one exact Codex profile and receipt shape;
- `codex-babysit` owns an already-running durable session and exact-session resume;
- `chatgpt-web` owns a logged-in browser capability and must define new-versus-existing conversation state.

Their descriptions should make it difficult for generic “use an agent” routing to land there.

## Implementation plan

### Phase 0 — Freeze the implementation snapshot

Before editing, wait for or coordinate with the current concurrent skill changes. Record:

- `git rev-parse HEAD`;
- `git status --short`;
- the 46 live package names;
- the current `agents/openai.yaml` inventory;
- the installed Codex/Claude capability surfaces.

Do not normalize, restore, or regenerate unrelated changed files. If the planned files remain concurrently owned, create a separate worktree or stop and ask for coordination rather than merging blindly.

Exit criteria:

- the implementation has a stable base snapshot;
- all pre-existing changes are identified as user-owned;
- no generated `build/` copy is treated as the live source.

### Phase 1 — Add the shared policy and install proof

Create `skills/_shared/agent-orchestration-policy.md` with the normative content in “The proposed shared policy.” Use `$skill-authoring` to keep its ownership narrow, prompt-first, self-contained, and distinct from workflow skills and runtime adapters. Use `$prompt-authoring` to explain the transport mechanism, operating principles, recognition tests, and quality bar without turning examples into an allowed-actions table. Keep it command-first and concise. Use this analysis as authoring provenance, but do not make the installed runtime policy depend on this repo-local plan or copy the entire research section into always-on skill context.

Update:

- `Makefile` verify assertions for Agents/Codex, Claude, and Gemini shared installs;
- `README.md` shared-policy/install notes and the native-versus-external summary;
- `docs/arch_skill_usage_guide.md` with a short transport/context selection section;
- repo `AGENTS.md` routing so agent-using skill work is expected to apply the shared policy.

Do not add a new controller or dispatcher script. `_shared` is already copied by all install targets, so install behavior should need only explicit verification/documentation unless the current Makefile snapshot proves otherwise.

Exit criteria:

- the policy is self-contained and host-aware;
- the native preference explains the lifecycle and SQLite/WAL tradeoff without becoming a ban, approval gate, or fixed process threshold;
- external-process reasons are illustrative recognition tests rather than an exhaustive list;
- installed paths are documented;
- `make verify_install` asserts the new shared file at all supported install surfaces;
- no skill has yet been half-migrated to a policy that is not installable.

### Phase 2 — Update the governance skills

Update, in order:

1. `prompt-authoring` — agent prompt/context vocabulary;
2. `skill-authoring` — shared-policy dependency and package audit rules;
3. `agents-md-authoring` — repository-level agent policy authoring;
4. `agent-definition-auditor` — conformance findings.

Update their relevant `agents/openai.yaml` files in the same change. Do not add exact-word tests for doctrine. The governance skills should inspect whether the required decisions are present and coherent, not require one sentence template.

Apply `$skill-authoring` to package ownership, peer boundaries, progressive disclosure, metadata, and validation. Apply `$prompt-authoring` to every edited `SKILL.md`, reference, bundled prompt, and `agents/openai.yaml` default prompt so the migration preserves explanation, agent judgment, and the original workflow's useful behavior.

Exit criteria:

- future skill edits naturally preserve the policy;
- prompts no longer use bare “fresh/fork/resume” agent language;
- audit output identifies transport/context/isolation conflation.

### Phase 3 — Migrate the six transport owners

Migrate one coherent group at a time:

1. `agent-delegate` as the external editful adapter;
2. `fresh-consult` as transport-neutral clean review;
3. `model-consensus` as per-participant transport selection;
4. `plan-conductor` as transport-neutral phase orchestration;
5. `stepwise` as transport-neutral worker/critic lifecycle;
6. `arch-epic` as native-first planner/worker/critic orchestration.

For each skill:

- preserve the conceptual fresh/resume/replace behavior;
- replace hard-coded transport ownership with shared-policy selection;
- remove generic nested-parallelism instructions;
- retain exact external model/profile resolution only in the external lane;
- keep helper scripts limited to deterministic invocation and parsing;
- update `SKILL.md`, live references, scripts that expose command syntax, and `agents/openai.yaml` together;
- update README routing when public behavior changes.

Do not rename these skills in the first migration. Changing semantics and routing is enough; renames would add install cleanup and user migration risk without improving the policy.

Exit criteria:

- same-host default examples use native children;
- cross-provider and capability-gap examples still work through external adapters;
- same-role repair resumes the exact child regardless of transport;
- fresh critics never accidentally resume implementer history;
- no parent tells a child to maximize its own fanout.

### Phase 4 — Migrate native policy consumers

Apply the shared policy to:

- `arch-docs`;
- `arch-step`;
- `arch-step-goal-prompt`;
- `audit-loop`;
- `audit-loop-sim`;
- `bugs-flow`;
- `comment-loop`;
- `cynical-architecture-review`;
- `cynical-code-review`;
- `cynical-cruft-removal`;
- `exhaustive-code-review`;
- `lilarch`;
- `miniarch-step`;
- `plan-audit`;
- `plan-implement`;
- `skill-flow`.

Use one mechanical audit checklist per package:

1. Every dispatch has a role and bounded task.
2. Every native spawn chooses clean, bounded, or full context.
3. Every follow-up chooses resume or fresh replacement.
4. Read/write and worktree behavior is explicit.
5. Parallel scopes do not overlap.
6. Parent integration and result accounting are explicit.
7. External same-provider use has a concrete benefit that the skill weighs against added process, integration, and shared-state cost.
8. `agents/openai.yaml` agrees with the live skill.

Exit criteria:

- no bare “fresh agent/reviewer” remains where a child is intended;
- no bare “maximize parallel agents” remains;
- Codex-directed spawns never rely on omitted `fork_turns`;
- Claude guidance distinguishes named subagent, explicit conversation fork, skill `context: fork`, team, and background session where relevant.

### Phase 5 — Clarify intentional external and durable lanes

Update `codex-review-yolo`, `codex-babysit`, and `chatgpt-web` descriptions and routing boundaries. Their implementation mechanisms should remain intact unless a separate task finds a real bug.

For `miniarch-step` and any other exact-model instruction, verify whether current native model selection is actually exposed in each supported host. If it is not, either:

- make the model a preference and use inherited native capability; or
- keep it load-bearing and explain why the exact-model external lane is worth its added cost.

Do not claim a native child ran a requested model when the active tool schema cannot select or report it.

Exit criteria:

- intentional external lanes remain reachable by exact request;
- generic same-host work no longer routes into them;
- new versus resumed browser/session state is unambiguous.

### Phase 6 — Repair and regenerate the skill DAG

Change the `skill-flow` extraction contract so normal backticked `$skill-name`
references and exact resolving backticked peer slugs count as prose edges when
the surrounding sentence names a real relationship. Continue excluding fenced
command examples, shell variables, command names, modes, filenames, and
incidental code words. The correct distinction is semantic location, exact
target resolution, and surrounding relationship—not “all inline code is
invisible.”

Then:

1. rerun the 46-package parallel walk with clean native children;
2. regenerate `docs/HOST_NATIVE_AGENT_POLICY_AND_SKILL_MIGRATION_PLAN_2026-07-11_DAG.md` or a dated successor;
3. include all extracted labeled edges with `path:line` evidence;
4. recompute dead-skill, over-promotion, duplicate-owner, and broken-reference findings;
5. revise any migration conclusion that depended on the false edge-free graph.

If a deterministic parser exists or is introduced, test its syntax behavior with small artificial fixtures rather than asserting wording from live skill doctrine. If the extraction remains prompt-only, validate it through a controlled sample and review, not a phrase-lock unit test.

Exit criteria:

- dollar-prefixed and exact unprefixed backticked live peer references appear;
- fenced shell examples do not become false graph edges;
- the graph no longer reports widespread false isolation;
- every edge has an allowed label and exact evidence.

### Phase 7 — Verify the whole install surface

Run after all skill-package changes:

```sh
npx skills check
make verify_install
```

Also run targeted repository checks:

```sh
rg -n "Maximize (native )?parallel agents|maximize.*agents" skills README.md docs
rg -n "fresh (agent|reviewer|critic|auditor)|fork|resume" skills --glob 'SKILL.md' --glob 'references/*.md' --glob 'agents/openai.yaml'
rg -n "codex exec|claude -p|agent-delegate|fresh-consult" skills README.md docs
rg -n "agent-orchestration-policy.md" skills README.md Makefile docs AGENTS.md
```

Review every match by meaning; do not mechanically delete valid external-lane explanations. Re-read the edited files and verify every new command and path. If helper scripts changed, run their narrow deterministic checks. Do not add unit tests that lock skill doctrine to exact phrases.

Exit criteria:

- all skill packages pass `npx skills check`;
- all supported installed surfaces contain the shared policy;
- README, Makefile, runtime metadata, and live skill doctrine agree;
- external same-provider execution is chosen for an explained concrete benefit rather than reflexive fanout, without introducing a prohibition or approval gate;
- the working tree contains no accidental generated-copy or vendor edits.

## Acceptance tests for the policy itself

The migration is complete only if these representative scenarios route correctly. They are recognition tests for the underlying principles, not a closed decision table.

| Scenario | Expected decision |
|---|---|
| Codex parent wants an independent Codex code reviewer | Native child, `fork_turns: "none"`, no-edit instruction, parent state check |
| Codex child needs the last two user decisions but not the whole chat | Native child, `fork_turns: "2"` |
| Codex child needs chat-only architecture decisions and no model override | Native full fork, `fork_turns: "all"` |
| Codex parent requires exact `-p yolo` output | External same-provider lane through `codex-review-yolo`; the exact-profile benefit justifies the added process cost |
| Codex parent wants several ordinary Codex workers in parallel | Prefer native children so Codex manages the fanout without multiplying independent top-level processes and SQLite/WAL pressure |
| A concrete Codex task benefits materially from one external session | Allow it; explain the capability or lifecycle benefit and keep fanout proportionate to current contention risk |
| Claude parent wants a cold Claude review | Named/custom native subagent, clean context |
| Claude parent wants a side task with the entire conversation | Explicit conversation fork, not skill `context: fork` shorthand |
| Claude skill should run isolated from the parent chat | Skill `context: fork`; document that it is clean/isolated |
| Claude implementer receives accepted review findings | Resume the exact native subagent with `SendMessage` |
| Claude task must keep running detached and isolate edits | Host-native background agent/worktree |
| Claude parent wants a Codex opinion | External cross-provider session |
| Two same-host models debate through a parent relay | Two clean native children if model selection is exposed; otherwise external only for the unavailable participant(s) |
| Two workers must edit the same file | Do not parallelize; sequence under one owner or isolate and deliberately merge |
| Three independent read-only repository slices | Native clean children up to the host slot budget; parent integrates |
| A child wants to spawn more children | Deny by default; allow only with explicit parent-owned scope and concurrency budget |
| A fresh critic must assess a repaired implementation | New clean critic, not the resumed implementer and not a full parent-history fork |
| A Stop hook must continue after the parent turn has ended | A same-provider process/background launch is reasonable because it provides lifecycle continuity; use an existing controller log if one already belongs to the workflow, but add no new exception ceremony |

## Non-goals

This plan does not:

- eliminate external model consultation;
- prohibit external same-provider Codex sessions;
- turn illustrative transport reasons into a finite allowlist, mandatory approval flow, rationale form, or fixed process-count threshold;
- force agents into every workflow;
- create one universal multi-provider runner;
- make scripts own decomposition, judgment, or review;
- require a serialized dispatch manifest for ordinary tasks;
- change vendored plugin source;
- treat generated `build/` directories as live skill packages;
- rename public skills in the first pass;
- make exact-word doctrine tests;
- assume context isolation enforces filesystem isolation;
- assume all Codex or Claude versions expose the same controls.

## Recommended end state

After migration, the suite should read as one coherent system:

- Skills say **what role is needed, what it owns, what context it should start with, and what must return**.
- The shared policy says **how to choose native versus background versus external transport, how to map context and resume semantics to the active host, and how to constrain permissions and fanout**.
- Narrow adapters say **how to invoke an external runtime and capture its deterministic receipts**.
- The parent agent remains the architect, integration owner, and final verifier.

The key behavior is simple: **same-host work generally prefers native agents; context is always explicit; resume is a workflow decision, not a CLI assumption; and an external process is chosen when the concrete benefit is worth its additional lifecycle, integration, and shared-state cost—not reflexively because “another agent” was requested.**
