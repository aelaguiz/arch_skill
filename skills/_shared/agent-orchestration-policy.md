# Agent Orchestration Policy

Use this policy whenever a skill or repository instruction asks an agent to
create, resume, replace, or coordinate another model agent. The calling skill
owns the workflow and role; this file owns the shared meaning of transport,
starting context and brief authority, continuation, isolation, topology, and
return evidence.

Do not copy this policy into every skill. Read it, keep the skill-specific role
contract local, and make the dispatch choices below explicit where the work is
actually launched.

## Define the dispatch before launching

Every child should have seven clear properties:

1. **Role** — the bounded job and the decision or files it owns.
2. **Transport** — active-host native child, host-native background child, or
   external runtime process/session.
3. **Starting context and brief authority** — clean, bounded recent context, or
   full parent context, plus which inputs are binding authority versus
   challengeable evidence or caller hypotheses.
4. **Continuation** — new child, exact-child resume, or fresh replacement.
5. **Isolation and capabilities** — read/write scope, tools, permissions,
   filesystem/worktree behavior, and any device or browser access.
6. **Topology** — who may create children, how independent scopes divide, and
   who integrates the results.
7. **Return contract** — the evidence the parent needs to accept, repair, or
   reject the work.

These are reasoning prompts, not a form to serialize. State them in the
smallest useful place: the workflow contract, child prompt, or dispatch note.

## Choose transport for the benefit it provides

Prefer a native child of the active host for ordinary same-host work when that
child can do the job. Native children let the host coordinate its own threads,
permissions, session lifecycle, and concurrency without multiplying unrelated
top-level runtimes. This preference applies to both implementation and review;
it is not a rule that every task needs a child.

An external process or session remains a valid lane when it provides a concrete
benefit the native child does not: a different provider, a load-bearing exact
model or profile, lifecycle beyond the parent turn, a durable resumable session,
worktree or process isolation, a required automation surface, or a particular
structured receipt. Those examples are recognition aids, not a closed
allowlist. Explain the benefit and weigh it against the extra process,
integration, and shared-state cost.

Independent same-provider Codex processes can be materially more expensive
than native Codex children. They create separate operating-system processes and
may contend on Codex's shared SQLite/WAL state; on some hosts this has caused
system-wide stalls. Treat that as a real cost when choosing transport and
fanout, especially when several external Codex sessions already exist. It is
not a prohibition, approval gate, or fixed process-count limit: one external
Codex session can still be the right choice when its concrete benefit is worth
the cost.

Honor an explicit user request for a provider, model, profile, durable session,
or external consultation. When the request names a desired outcome such as
"another reviewer" rather than a transport, choose transport under this
policy.

Do not claim that a native child uses a requested model, permission set,
background lifecycle, or worktree unless the current host exposes and confirms
that capability. Inspect the active tool surface. If a load-bearing capability
is unavailable natively, use the appropriate external or background lane and
say what it buys.

## Choose starting context deliberately

**Clean context** is the default for independent work. Give the child the goal,
artifact paths, constraints, and acceptance evidence it needs, then let it read
source truth. Clean context reduces inherited framing and is especially useful
for critics, repository mapping, and workers whose durable plan or log already
contains their inputs.

**Bounded context** is appropriate when a child needs a few recent chat-only
decisions but not the whole conversation. Include only the relevant recent
turns or restate those decisions in the child brief. Do not use a full fork as
a substitute for writing down a small load-bearing fact.

**Full parent context** is appropriate only when the task genuinely depends on
the conversation as a whole. A full fork carries the parent's framing,
assumptions, and persuasive completion story as well as useful facts; it is
usually the wrong default for an independent critic.

### Preserve independent judgment in the brief

A clean child has no inherited conversation, but a leading brief can still
carry the caller's framing. Before the first model-agent dispatch, and before a
follow-up materially changes the goal, authority, scope, theory, or success
bar, apply `$prompt-authoring` to the actual populated child brief. Applying it
only to a reusable template is insufficient. For an exact same-role resume,
audit the new delta instead of rebuilding the whole prompt. Preserve an exact
verbatim relay when the user explicitly requests one.

Build the brief from the user's goal, source artifacts, verified facts,
binding decisions and constraints, assigned scope, and return contract. Do not
silently turn the parent's diagnosis, preferred solution, or chosen evidence
path into task truth. When a parent belief is materially useful, expose it as a
non-binding hypothesis with its evidence or provenance and let the child reject
it. Omit it when an unanchored cold read is the point.

An authoritative checklist may define completion without defining the only
investigation, reasoning, or implementation path. If finite checks are the
whole role, report the result as scoped verification rather than broad
independent review. Keep parent-only transport rationale, session bookkeeping,
and receipt metadata out of the child brief unless they change the child's
capabilities, continuity, or work.

Recognition test: could the child reject the parent's theory and still satisfy
the authoritative task? If not, either the theory is genuinely binding or the
brief is overconstrained.

Use these terms consistently. "Fresh" means a new clean child unless the
workflow explicitly says otherwise. "Fork" must say whether it is bounded or
full. Context inheritance does not imply filesystem, permission, or process
isolation.

## Map context to the active host

In Codex native multi-agent dispatch, set `fork_turns` explicitly:

- `"none"` starts a clean child;
- a positive count such as `"2"` carries bounded recent turns;
- `"all"` carries the full available conversation.

Do not omit `fork_turns` and assume the child is clean; hosts and tool versions
may default omitted context differently. A full Codex fork is a host-prepared
child context, not a promise of a byte-for-byte transcript clone. It may also
constrain child model overrides, so inspect the current tool schema before
promising a different native child model.

When Codex exposes its native collaboration tools, `spawn_agent` creates the
role and returns its durable target handle. Preserve that handle. Use
`followup_task` to give the same role another turn (including when it is idle),
and `send_message` for information that should reach a currently running role
without independently starting a turn. A new `spawn_agent` is a replacement,
not a resume. Tool names can evolve, so use the active schema rather than
shelling out merely to imitate these semantics.

In Claude Code, distinguish several native mechanisms:

- a named or custom subagent normally starts clean and receives its task brief;
- an explicit conversation fork carries the parent conversation;
- a skill declared with `context: fork` runs in an isolated clean subagent
  context and is not shorthand for full conversation inheritance;
- an existing subagent can receive follow-up work through its exact handle;
- a background agent is the native durable lane when work must outlive the
  immediate foreground turn;
- an agent team is for work that benefits from direct peer coordination, not
  ordinary parent-mediated fanout.

Other hosts may expose different primitives. Preserve the clean, bounded, and
full distinction even when the exact syntax differs.

## Continue the role, not merely the process

Resume the exact child when the same role is continuing its own work: an
implementer repairing accepted findings, a planner revising its plan, or a
participant answering a bounded follow-up in an ongoing dialogue. Give the
resume a compact delta and preserve its durable handle.

Start a fresh clean replacement when independence is the point: a cold critic,
a second verification gate, or a downstream worker whose inputs changed enough
to invalidate its earlier view. Never resume a convenient old session for an
unrelated role merely because its handle exists.

If an upstream artifact changes after a downstream child read it, decide
whether the downstream work can be repaired by the same role or must be
restarted clean. Make that dependency decision explicit.

## Separate context from isolation and capability

Native children commonly share the parent's workspace even when their chat
context is clean. A no-edit sentence is useful doctrine but is not an enforced
filesystem boundary. For review-only work, combine the strongest controls the
host actually provides:

- a read-only capability or sandbox when available;
- an explicit no-edit/no-write child contract;
- a parent-owned `git status` or diff check before accepting the result.

For editful work, give each child a non-overlapping owner path or sequence
colliding work under one owner. Use a separate worktree only when isolation or
lifecycle truly requires it, and plan the merge rather than treating the
worktree as automatic integration.

Permissions, browser/device access, network access, and background lifetime are
separate choices. Do not use an external process merely to smuggle in a
capability the workflow has not authorized.

## Keep topology parent-owned

The parent owns decomposition, the concurrency budget, and final integration.
Parallelize work that is genuinely independent; do not "maximize agents" as an
end in itself. Account for available host slots, shared files, external process
cost, and the parent's ability to review every result.

Children must not create their own children or invoke delegation/consult skills
unless the parent explicitly assigns a nested scope and budget. Ordinary
worker and critic prompts should say that plainly. If peers need to communicate
directly rather than through the parent, choose a host-native team deliberately
and name why that topology helps.

## Require an integration-ready return

A useful child return tells the parent:

- whether the bounded task completed;
- what it learned or changed, with file and symbol anchors;
- which commands or checks ran and their results;
- unresolved findings, assumptions, blockers, or collision risks;
- the exact session/child handle and receipt path when continuation matters.

The parent verifies claims against current workspace truth, reconciles overlap,
decides what to accept, and owns the final user-facing answer. Claimed work
products are part of that truth: the parent loads the artifact itself and
verifies its substance — or assigns an inspector that returns extracted
evidence rather than a verdict — and adopts analytical conclusions only at
anchors it has verified. Child output is evidence, not automatic acceptance.

## Representative decisions

An independent Codex review normally uses a clean native child with explicit
no-edit guidance and a parent diff check. A Codex child that needs only the last
two chat decisions uses bounded native context. A requested `-p yolo` receipt
uses the external profile lane because that exact profile and artifact shape
are the point. A Claude cold review uses a clean named subagent; a Claude side
task that truly needs the whole conversation uses an explicit conversation
fork. A Claude implementer receiving accepted findings resumes its exact
subagent, while the next independent critic starts clean. A Claude parent
asking for a Codex opinion necessarily crosses providers and therefore uses an
external Codex session.

These examples illustrate the reasoning. They do not replace it.
