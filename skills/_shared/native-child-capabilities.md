# Native Child Capabilities

Companion to `agent-orchestration-policy.md`. That file owns the *reasoning*
about transport; this file holds the *facts* a host-specific choice depends on:
whether the active host can pin a child's model and thinking level, whether it
can reach another provider, and where each pin quietly stops holding.

Read it when a dispatch decision turns on one of those facts. Do not copy it
into a skill.

**Provenance.** Verified 2026-08-19 by direct source and binary inspection:
Prime Agent `packages/coding-agent`; Codex repo `ceb2ffb793` with installed
`codex-cli 0.148.0-alpha.20` and `multi_agent_v2` stable; Claude Code `2.1.228`
(build 2026-08-11) zod schemas plus current `code.claude.com` docs.

**Harnesses move.** Treat every row as a starting expectation, not a promise.
Inspect the live tool schema before you rely on a capability, and believe the
schema over this file when they disagree.

## Matrix

| Capability | Prime Agent | Codex CLI (multi_agent_v2) | Claude Code |
|---|---|---|---|
| Pin child **model** | `model="provider/id"` on the spawn call. Exact selector; it must be in the authenticated catalog or the spawn hard-fails | `spawn_agent(model=...)`. The slug must be catalog-tagged for v2; on a typical host that is only the `gpt-5.6-*` family | Three levers, in order: `CLAUDE_CODE_SUBAGENT_MODEL` env, per-call `model`, agent frontmatter `model:`. The per-call form is a closed alias enum, not full IDs |
| Pin child **thinking / effort** | `thinking=` with `off, minimal, low, medium, high, xhigh, max` | `reasoning_effort=` with `none, minimal, low, medium, high, xhigh, max, ultra` | Agent frontmatter `effort:` with `low, medium, high, xhigh, max`. **No per-call effort parameter**, and no per-subagent extended-thinking toggle |
| Unsupported level | Hard spawn failure when set explicitly; an inherited level is silently clamped | Rejected with the model's supported list | Frontmatter value applies to that agent definition |
| **Cross-provider** child | **Yes** — provider is not a constraint in the spawn path. The gate is the authenticated catalog: a host logged in to two providers can spawn a child on either | **No** through `model` — the child's provider is copied from the parent turn. Reachable only through a human-installed role whose config file sets its own provider | **No** — the vendor does not route Claude Code to non-Claude models through any gateway; the base-URL override is process-wide and changes where requests go, not which model answers |
| Starting context | Clean only; no fork option exists | `fork_turns`: `none`, `all`, or a positive-integer string. **Omitting it means `all`** | Clean by default; the explicit fork form inherits everything and forces the parent model |
| Resume the exact child | Message the child by name or id | Follow-up or message tool against the canonical task name | Message tool against the agent id or name; full history retained |
| Concurrency | No cap; a kernel boot throttle delays rather than rejects | **3 children** by default; over-cap triggers an unload, not an error | 20 by default |
| Child fan-out | **Depth 1 by default — a child cannot spawn its own children.** Raise it deliberately at the host | Uncapped under v2 | Depth 3 by default |
| Billing | The child bills at **its own model's rate**, summed into parent totals and tagged by origin | One account and rate-limit window for the whole tree. Child token usage is per-thread and **is not rolled up**, so parent-side totals under-report | One account for the whole tree |

## Sharp edges

**A pin can expire mid-run.** Codex keeps a child's pinned model and effort only
while that child stays resident. When the residency cache unloads it and a
follow-up rebuilds it from its rollout, the rebuilt config comes from the
*current parent turn* — so the child silently resumes on the parent's model and
effort. A role-supplied profile survives because the role is persisted with the
session; a raw spawn argument is not persisted at all. Any workflow that resumes
the same child several times over a long run should either keep slices short
enough to stay resident, express the profile as a role, or use an external
session whose model is fixed by its own process.

**A model pin is not always an effort pin.** Claude Code can pin a subagent's
model at the call site but not its effort. Pinning effort there means authoring
an agent definition that carries both fields. A workflow that treats "pinned
model" as "pinned profile" will get the parent's session effort on Claude.

**Fan-out is a host fact, not a universal one.** A child that is told it may
create its own native sub-agents will simply fail on a host whose depth limit is
1. State fan-out as something you checked on this host, and size the child's job
for what it can actually do.

**Reach is per-installation, not per-vendor.** Prime Agent's cross-provider
ability depends on which providers that installation is authenticated for. When
the catalog holds two providers, a cross-provider child is an ordinary native
spawn. When it holds one, the same request needs an external session. Check the
catalog before deciding; do not assume either answer.

**Context inheritance is separate from everything else.** None of these rows say
anything about permissions, filesystem scope, worktree isolation, or network
access. Choose those independently.

## Using the matrix

A native child is the right lane when four things are true:

1. **Reachable** — the model you want is in this host's native child catalog.
2. **Pinnable** — this host can set that model *and* that thinking level.
3. **Durable enough** — the pin survives the continuation pattern this work
   needs.
4. **No external-only benefit is load-bearing** — no usage-limit rotation across
   accounts, no session that must outlive the parent process, no required run
   receipts, no concurrency past the native cap, no process isolation the host
   cannot give.

When one fails, say which one and take the external lane for that reason. An
unpinned native child is not a cheap lane: it runs the parent's model on
whatever you gave it.
