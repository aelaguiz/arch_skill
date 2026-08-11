# External Dispatch And Native Sub-Agent Use: Evidence Inventory

> **Resolution (2026-08-11):** The policy described below was changed after this
> inventory was written. `skills/_shared/agent-orchestration-policy.md` and every
> skill that restated it now say: a child may always create its own native
> sub-agents on its own host, with no parent permission, nested scope, or budget;
> and a child may never spawn external agents — a worker started through
> `$agent-delegate` cannot itself use `$agent-delegate` or any other external
> transport. External topology stays parent-owned. Read everything below as the
> pre-change record, not current doctrine.

**Date:** 2026-08-11
**Repo:** `arch_skill`
**Scope:** every live skill under `skills/` that dispatches, delegates, or
coordinates another model agent, plus `skills/_shared/agent-orchestration-policy.md`.
**Method:** read-only. Full-text reads of each `SKILL.md` and its `references/`,
plus repo-wide `rg` sweeps for `native`, `subagent`, `sub-agent`, `nested`,
`spawn`, `delegate`, `worker`, `fleet`, `create children`, `other model agents`.
No skill file was modified.

---

## The finding in one paragraph

Yes — there is a real and remarkably consistent ban, and it lives in one place:
`skills/_shared/agent-orchestration-policy.md` says *"Children must not create
their own children or invoke delegation/consult skills unless the parent
explicitly assigns a nested scope and budget."* Every dispatching skill in the
repo restates that same rule in its own words, and every one of them writes it
into the actual child prompt text. But the rule is **transport-agnostic**: it
bans the spawned agent from creating *any* child — native sub-agent, external
process, or delegation/consult skill — and almost no skill distinguishes those
cases. So "does the spawned external Codex worker get to use its own native
sub-agents?" is answered only implicitly: **no, unless the parent explicitly
budgeted a nested scope.** The rule is a default-off with an explicit
override, not an absolute prohibition, and it is framed as topology control
(the parent owns decomposition and integration), never as a per-transport
capability rule.

**The one loud exception is `conductor`, and it points the opposite way.**
Conductor's cost model *depends on* the spawned external fleet reviewer running
its own sub-agents inside itself, because those nested slices bill the cheap
fleet host instead of the parent's expensive model:
*"invokes the installed review skill itself against the repo, so any slices it
fans out bill the fleet host's cheap model, not the parent's"*
(`skills/conductor/references/delegation-and-monitoring.md:33-36`). That
sentence sits in the same skill whose Non-Negotiables say *"Every child prompt
forbids creating more model agents ... unless the parent deliberately assigns a
bounded nested scope and budget"* (`skills/conductor/SKILL.md:176-178`). Both
can be true — invoking the review instrument *is* the nested-scope assignment —
but conductor never says so out loud, so the two passages read as a
contradiction to anyone who did not already know the intent.

**Second finding worth knowing:** conductor is also the only skill that treats
native sub-agents as an *economic* category ("Native subagents bill the
parent's expensive model — they are not a cheap lane, so bulk work never routes
to them", `skills/conductor/SKILL.md:35-37`). Everywhere else in the repo,
native children are the *preferred* lane and external transport is the thing
that must justify itself. Conductor inverts the suite-wide default on purpose
and says why. That is a documented deviation, not an accident, but it is the
single biggest divergence from `_shared/agent-orchestration-policy.md` in the
repo.

---

## The shared policy: what it actually says

`skills/_shared/agent-orchestration-policy.md` is the file every dispatching
skill defers to. Three passages matter here.

**1. The nested-child rule (lines 194-205, "Keep topology parent-owned"):**

> The parent owns decomposition, the concurrency budget, and final integration.
> Parallelize work that is genuinely independent; do not "maximize agents" as an
> end in itself. Account for available host slots, shared files, external process
> cost, and the parent's ability to review every result.
>
> Children must not create their own children or invoke delegation/consult skills
> unless the parent explicitly assigns a nested scope and budget. Ordinary
> worker and critic prompts should say that plainly. If peers need to communicate
> directly rather than through the parent, choose a host-native team deliberately
> and name why that topology helps.

Note what this does and does not say. It does **not** distinguish "the child is
a native sub-agent of my host" from "the child is an external Codex process."
It bans *children of children*, full stop, whichever transport either uses.
It also does not phrase the ban as a safety or capability boundary — the stated
reason is that the parent owns decomposition and must be able to review every
result.

**2. The transport preference (lines 36-44):**

> Prefer a native child of the active host for ordinary same-host work when that
> child can do the job. ... An external process or session remains a valid lane
> when it provides a concrete benefit the native child does not.

This is the suite-wide default that `conductor` deliberately inverts.

**3. Native children are not isolation (lines 176-178):**

> Native children commonly share the parent's workspace even when their chat
> context is clean. A no-edit sentence is useful doctrine but is not an enforced
> filesystem boundary.

Relevant because several skills lean on the no-nested-children prompt line as if
it were enforced; it is not, and the policy says so.

---

## Per-skill inventory

Legend for column 2 (**child's own sub-agents**):
`BAN+override` = child is told not to create children, unless the parent
explicitly assigns a bounded nested scope and budget.
`BAN(hard)` = stated with no override clause in that specific prompt.
`ALLOW` = the skill affirmatively expects/relies on the child fanning out.
`SILENT` = the skill does not address it.

| Skill | Dispatch kind | Child's own sub-agents | Parent's own sub-agents | Defers to shared policy |
|---|---|---|---|---|
| `agent-delegate` | External editful worker/session (Claude, Codex, Cursor, Grok, Kimi) | BAN+override | Parent owns fanout; ordinary same-host work should be a native child *instead of* this skill | Yes, explicitly |
| `conductor` | External "fleet" workers by default; native child is a narrow exception | BAN+override in worker prompt — but **ALLOW (implied)** for fleet review instruments | **Discouraged on cost grounds**; native sub-agents are "never the cheap lane" | Yes, but overrides its transport preference |
| `stepwise` | Native children preferred; external adapter for deliberate benefit | BAN+override (worker), BAN(hard) (critic + diagnostic turn) | Orchestrator owns fanout and integration | Yes, explicitly |
| `arch-epic` | Native planner/worker/critic preferred; external harness lane | BAN+override, plus a separate ban on nested `auto-plan`/`implement-loop` | Parent owns sequencing, fanout, integration | Yes, explicitly |
| `fresh-consult` | Clean native child preferred; external session for concrete benefit | BAN+override | Parent owns fanout, concurrency budget, synthesis | Yes, explicitly |
| `model-consensus` | Per-participant native or external; parent relays | BAN+override | Parent owns fanout, round sequencing, relay | Yes, explicitly |
| `codex-review-yolo` | External Codex `-p yolo` process only | BAN(hard) in the shipped prompt template | Cost-aware: don't spin parallel yolo reviewers as a speed reflex | Yes, explicitly |
| `codex-babysit` | Monitors an already-running external Codex pane; dispatches nothing | **SILENT — and treats self-spawned sub-agents as normal** | N/A (not a dispatcher) | Mentions the policy file only in a "when not to use" pointer |
| `plan-implement` | Native children; explicit external handoff to `agent-delegate`/`conductor` | BAN+override (repeated in all three shipped child prompts) | Native sub-agents encouraged, with a Good Uses / Bad Uses list | Yes, explicitly |
| `plan-audit` | Native read-only audit children | BAN+override | Parent owns fanout and verdict | Yes, explicitly |
| `cynical-code-review` / `-architecture-review` / `-cruft-removal` | Native read-only slices only; external review skills explicitly forbidden as mechanism | BAN+override | Native slices encouraged for broad targets | Yes, explicitly |
| `exhaustive-code-review` | Native read-only coverage slices | BAN+override | Coverage-led native fanout | Yes, explicitly |
| `bugs-flow`, `audit-loop`, `audit-loop-sim`, `comment-loop`, `arch-docs`, `lilarch`, `miniarch-step`, `arch-step` | Native children; external is an available transport choice | BAN+override | Parent owns fanout | Yes, explicitly |
| `arch-step-goal-prompt` | Authors goal prompts that describe dispatch | BAN+override (as required goal-prompt content) | Describes both lanes | Yes, explicitly |
| `plan-interview` | Native read-only research children | "no nested fanout" (BAN, no override stated) | Native research children encouraged | Yes, explicitly |

---

### `agent-delegate` — the external worker adapter

**Dispatch kind.** External editful worker or resumable session, run as a
separate OS process with a captured receipt. Explicitly *not* the lane for
ordinary same-host work: *"For ordinary same-host work, use the active host's
native child directly when that child can satisfy the role"*
(`skills/agent-delegate/SKILL.md:16-17`).

**What it says about the spawned worker's own sub-agents.** A clear default-off
with an explicit override, stated in the Non-Negotiables:

> - Tell every worker not to create children or invoke delegation/consult skills.
>   Nested fanout is allowed only when the parent explicitly assigns a bounded
>   nested scope and concurrency budget in that worker's prompt.
>
> — `skills/agent-delegate/SKILL.md:144-146`

The shipped worker prompt puts the same rule in the child's own "You must not"
list:

> 4. Create child agents or invoke delegation/consult skills unless the parent
>    explicitly assigned a bounded nested scope and concurrency budget above.
>
> — `skills/agent-delegate/references/delegate-prompt-and-output.md:90-91`

Important nuance: the worker **is** allowed to use ordinary installed skills —
*"Use installed skills when their trigger and contract fit the delegated task"*
(`references/delegate-prompt-and-output.md:77`) — bounded by
*"Use installed skills only when they directly improve the delegated work and
do not violate the parent-owned fanout boundary"* (`:106-107`). So a delegated
worker may use, say, `$skill-authoring`, but may not use a skill whose
mechanism is fanning out children.

And the anti-pattern list frames the whole thing as topology, not capability:

> - Tell workers to maximize their own fanout. The parent owns decomposition and
>   concurrency unless it explicitly assigns a bounded nested scope and budget.
>
> — `skills/agent-delegate/references/delegate-prompt-and-output.md:219-220`

**What it says about the parent's sub-agents.** The parent should use native
children for ordinary same-host work rather than routing through this skill at
all (`SKILL.md:16-17`, `SKILL.md:63-67`, First Move step 4 at `SKILL.md:170-181`).

**Defers to shared policy.** Yes: *"Apply `../_shared/agent-orchestration-policy.md`
before selecting this lane"* (`SKILL.md:75`), and it is First Move step 1.

---

### `conductor` — the exception that matters

**Dispatch kind.** Mixed, with an inverted default: the standing lane is a
**cheap parallel external fleet** through `$agent-delegate` (Codex
`gpt-5.6-sol` at `ultra`), with native children as a narrow exception.

**What it says about the spawned worker's own sub-agents — two contradictory
readings in the same skill.**

*Reading A — the general contract (ban):*

> - The parent owns decomposition, fanout, and integration. Every child prompt
>   forbids creating more model agents or invoking delegation/consult skills
>   unless the parent deliberately assigns a bounded nested scope and budget.
>
> — `skills/conductor/SKILL.md:176-178`

The shipped worker prompt says the same to the worker's face:

> The parent owns fanout and integration. Do not create or coordinate other model
> agents, manually spawn coding-harness executables, or invoke delegation or
> consult skills unless this prompt explicitly assigns a bounded nested scope and
> budget.
>
> — `skills/conductor/references/worker-prompt-contract.md:61-64`

Repeated for parallel waves (`references/delegation-and-monitoring.md:50-53`),
for chunking (`references/chunking-and-parallelism.md:63-64`), and for shaping
research workers, where it is stated without an override: *"Clean context,
read-only role, no implementation, no nested delegation"*
(`references/shaping-and-outcome-map.md:32-34`).

*Reading B — the review instruments (relies on nested fanout):*

> - **Final-gate review instruments → new clean fleet sessions.** Each
>   selected cynical review runs as its own clean external fleet session that
>   invokes the installed review skill itself against the repo, so any slices
>   it fans out bill the fleet host's cheap model, not the parent's. ...
>   Never run these reviews through native subagents — bulk
>   review reading on the parent's model is the exact spend this skill exists
>   to avoid.
>
> — `skills/conductor/references/delegation-and-monitoring.md:33-40`

And again in the audit reference:

> Never run these reviews through
> native subagents: they bill the parent's expensive model, and bulk review
> reading is exactly the spend the fleet exists to absorb — a fleet
> reviewer's own slices run on the fleet host's cheap model.
>
> — `skills/conductor/references/audit-and-send-back.md:249-252`

This is the only place in the repo where a skill affirmatively expects a
spawned external agent to run its own sub-agents, and it treats that nesting as
the *benefit*. The instruments it dispatches (`$cynical-code-review` and
friends) do in fact fan out native children by their own doctrine — see
`skills/cynical-code-review/SKILL.md:63-67`. So the conductor's economics are
built on nested native sub-agents inside the external worker, while the same
skill's default prompt contract forbids exactly that unless assigned.

**What it says about the parent's sub-agents — an inverted preference.**
This is a second, distinct deviation:

> Fleet
> tokens go to investigation, implementation, repair, proof runs, and heavy
> review reading. Native subagents bill the parent's expensive model — they
> are not a cheap lane, so bulk work never routes to them.
>
> — `skills/conductor/SKILL.md:35-37`

> The reason is money, said plainly: native children on the
> parent's host run the parent's expensive model, so a "native review" or
> "native worker" spends premium tokens on exactly the bulk reading the fleet
> exists to absorb. Native children are not a budget lane and not free
> parallelism — they are the parent's wallet with a different face. Reserve
> them for genuinely tiny errands a fleet round-trip would dwarf (a one-file
> read-only check), a capability only the host exposes, an explicit user
> request, or an unavailable external runtime.
>
> — `skills/conductor/references/delegation-and-monitoring.md:8-15`

> That work
> routes to fleet workers, who read the files so the conductor does not — on
> a cheap model, which a native subagent is not.
>
> — `skills/conductor/references/delegation-and-monitoring.md:155-158`

**Defers to shared policy.** Yes, and it names its override explicitly:
*"Apply `../_shared/agent-orchestration-policy.md` at every worker and reviewer
dispatch ... The conductor's default execution lane is the cheap parallel
external fleet ... as a deliberate standing policy choice ... that exact
cheaper/faster model is the concrete benefit the shared policy asks external
transport to name"* (`skills/conductor/SKILL.md:101-115`). So the inversion is
argued inside the policy's own terms rather than silently taken.

---

### `stepwise` — ordered process, native-preferred, external adapter available

**Dispatch kind.** One clean worker per step plus a new clean critic per step.
Native children preferred; the external adapter is a deliberate-benefit lane
(`skills/stepwise/SKILL.md:55-60`, `references/execution-routing.md:63-70`).

**Child's own sub-agents.** BAN+override at the doctrine level:

> - The orchestrator owns fanout and integration. Worker and critic prompts
>   forbid creating other model agents or invoking delegation/consult skills
>   unless the orchestrator explicitly assigns a bounded nested scope and budget.
>
> — `skills/stepwise/SKILL.md:77-79`

Written into the actual prompts. The repair prompt carries the override:

> Do not create or coordinate other model agents or invoke delegation/consult
> skills unless this prompt explicitly assigns a bounded nested scope and budget.
>
> — `skills/stepwise/references/session-prompt-contracts.md:137-138`

The read-only **diagnostic** prompt states it flat, with no override:

> Do not create or coordinate other model agents or invoke delegation/consult
> skills.
>
> — `skills/stepwise/references/session-prompt-contracts.md:80-81`

The critic contract lists it under things the critic must not do, also with no
override: *"Create or coordinate other model agents or invoke delegation/consult
skills."* (`skills/stepwise/references/critic-contract.md:162`).

**Parent's sub-agents.** Orchestrator-owned fanout; native children preferred
(`references/session-resume.md:30-32`, `references/execution-routing.md:63-70`).

**Defers to shared policy.** Yes (`skills/stepwise/SKILL.md:54`,
`references/session-resume.md`).

---

### `arch-epic` — multi-plan epic decomposition

**Dispatch kind.** Clean native planner/worker/critic children preferred; an
explicit external-harness lane exists for provider/model/lifecycle/receipt
benefit (`skills/arch-epic/SKILL.md:118-125`,
`references/model-and-effort.md:3-14`).

**Child's own sub-agents.** BAN+override:

> - The parent owns sequencing, any fanout, and final integration. Planner,
>   worker, and critic prompts forbid creating other model agents or invoking
>   delegation/consult skills unless the parent explicitly assigns a bounded
>   nested scope and budget.
>
> — `skills/arch-epic/SKILL.md:134-137`

The shipped harness prompt repeats it and adds a second, arch-specific
restriction that no other skill has — a ban on the child re-entering *automatic
continuation commands*:

> - avoid nested automatic continuation commands such as `auto-plan` or
>   `implement-loop`
> - do not create or coordinate other model agents, manually start model-harness
>   processes, or invoke delegation/consult skills unless the parent explicitly
>   assigned a bounded nested scope and budget
>
> — `skills/arch-epic/references/auto-harness-prompts.md:54-58`

**Parent's sub-agents.** Preferred and encouraged; explicit `fork_turns`
discipline at `SKILL.md:126-133`.

**Defers to shared policy.** Yes (`skills/arch-epic/SKILL.md:118`).

---

### `fresh-consult` — read-only second opinions

**Dispatch kind.** "Fresh" is a *context* claim, not a CLI: clean native child
preferred for same-host review, external session when the provider/exact
model/receipt is the point.

**Child's own sub-agents.** BAN+override:

> - The parent owns fanout, the concurrency budget, evidence spot-checking, and
>   synthesis. Every reviewer prompt prohibits child-created fanout and
>   delegation/consult skills unless the parent explicitly assigns a bounded
>   nested scope and budget.
>
> — `skills/fresh-consult/SKILL.md:111-114`

The shipped reviewer prompt is the most explicit "no-child rule" wording in the
repo:

> Do not edit or write files, run formatters, coordinate directly with sibling
> consults, create child agents, invoke delegation/consult skills, or start
> another controller. Only a nested scope and budget explicitly assigned above
> can relax the no-child rule.
>
> — `skills/fresh-consult/references/consult-prompt-and-output.md:65-68`

Anti-pattern list: *"Tell reviewers to maximize their own fanout. The parent
owns decomposition, concurrency, evidence checking, and synthesis unless it
explicitly budgets a nested scope."*
(`references/consult-prompt-and-output.md:148-150`).

**Parent's sub-agents.** Preferred: First Move step 4 is *"Inspect the active
host's native child surface. Choose a new clean native child for ordinary
same-host review when it can satisfy the role."* (`SKILL.md:134-137`).

**Defers to shared policy.** Yes — First Move step 1 (`SKILL.md:128`).

---

### `model-consensus` — two participants iterating to convergence

**Dispatch kind.** Transport resolved **per participant**: clean native children
for same-host participants, external sessions for cross-provider or exact-model
needs. Parent relays between them.

**Child's own sub-agents.** BAN+override:

> - The parent owns fanout, the concurrency budget, round sequencing, evidence
>   relay, and final integration. Participant prompts prohibit child-created
>   fanout and delegation/consult skills unless the parent explicitly assigns a
>   bounded nested scope and budget.
>
> — `skills/model-consensus/SKILL.md:85-88`

In every one of the four shipped participant prompt shapes:

> Do not edit or write workspace files. Do not create child agents or invoke
> delegation/consult skills. The parent owns fanout, evidence relay, and
> integration unless it explicitly assigns a bounded nested scope and budget.
>
> — `skills/model-consensus/references/prompt-contracts.md:89-91`
>   (repeated at `:135-137`, `:175-177`, `:204-206`)

It also bans a related topology — participants messaging each other:
*"Parent relay is the default topology. Participants do not message each other
directly and do not create children unless the parent explicitly budgets a
bounded nested scope."* (`references/workflow-contract.md:22-25`).

**Parent's sub-agents.** Encouraged for same-host participants, with explicit
`fork_turns: "none"` / clean named subagent discipline (`SKILL.md:70-80`).

**Defers to shared policy.** Yes.

---

### `codex-review-yolo` — the pinned external Codex profile

**Dispatch kind.** External only, by design: `codex exec -p yolo` in a new clean
process with captured receipts. It says so: *"An ordinary same-host Codex review
should use a clean native child instead."* (`skills/codex-review-yolo/SKILL.md:14-15`).

**Child's own sub-agents.** BAN, and unusually it is stated with no override
clause anywhere in the skill:

> - **Keep topology parent-owned.** The review prompt tells Codex not to spawn
>   nested agents or invoke delegation/consult skills. The parent verifies and
>   integrates the verdict.
>
> — `skills/codex-review-yolo/SKILL.md:68-70`

> 6. Note that this dispatch is a new clean external review with no continuation
>    handle. Tell the reviewer not to edit or spawn children.
>
> — `skills/codex-review-yolo/SKILL.md:100-101`

The shipped prompt template puts it in Hard Constraints:

> - Do not spawn child agents or invoke delegation/consult workflows.
>
> — `skills/codex-review-yolo/references/prompt-template.md:30`

**Parent's sub-agents.** Not a native-child skill, but it warns the parent
against reflexive external fanout: *"Do not create parallel `yolo` reviewers
merely as a speed reflex ... This is a cost judgment, not a ban or fixed process
limit."* (`SKILL.md:63-67`).

**Defers to shared policy.** Yes: *"Read `../_shared/agent-orchestration-policy.md`
before dispatch. This skill's transport is intentionally external and its
starting context is intentionally clean; it does not redefine the suite-wide
transport or context policy."* (`SKILL.md:17-20`).

---

### `codex-babysit` — the gap

**Dispatch kind.** None. It monitors an already-running external Codex goal-mode
tmux pane and keeps it alive across usage limits. It explicitly is not a
dispatcher: *"this skill keeps an existing session alive, it does not create
one"* (`skills/codex-babysit/SKILL.md:47-48`).

**Child's own sub-agents — SILENT, and it treats them as normal operating
reality.** The only mention is descriptive, not restrictive:

> ## Self-spawned delegate caveat
>
> A codex goal often spawns its own sub-agents (`codex exec ...`, e.g. via an
> `agent-delegate`-style review). Those children also consume aim accounts and can
> even rotate `active_label` themselves when *they* hit a limit.
>
> — `skills/codex-babysit/references/signals-and-runbook.md:109-113`

The same observation is in shared doctrine:
*"Codex work often spawns its own children (`codex exec ...`, delegated
reviews). Children consume the same account pool and can rotate `active_label`
themselves."* (`skills/_shared/aim-rotation.md:56-62`).

This is not a contradiction — the babysat session was launched by a *human*, not
by a skill under this policy, so no one assigned it a nested-scope budget in the
first place. But it is worth recording that the repo's own operational doctrine
assumes long-running Codex goals routinely fan out sub-agents, which is what the
dispatch skills forbid by default.

**Parent's sub-agents.** N/A. It does point elsewhere for spawning:
*"You need to launch a new task worker. Prefer the active host's native child
when it can do the job; use `agent-delegate` only for a deliberate external
worker/session benefit."* (`SKILL.md:40-42`).

**Defers to shared policy.** Not directly — it never reads the policy file; it
only routes away to other skills.

**Install status note:** `codex-babysit` is in `REMOVED_SKILLS` in the
`Makefile` (line 4) and is not in `SKILLS`. `README.md:56` confirms it is
"optional source-retained ... not installed by default", even though
`AGENTS.md` still routes to `$codex-babysit`.

---

### `plan-implement` — native acceleration, external by explicit handoff

**Dispatch kind.** Primarily native children; an explicitly requested external
worker is handed to `agent-delegate` or `conductor`.

**Child's own sub-agents.** BAN+override, stated once in doctrine and repeated
in all three shipped child prompts:

> - Children do not create children or invoke delegation, consult, or review
>   skills unless the parent explicitly assigns a nested scope and budget.
>
> — `skills/plan-implement/SKILL.md:81-82`

> - prohibit children from creating children or invoking delegation, consult, or
>   review skills unless the brief assigns a nested scope and budget
>
> — `skills/plan-implement/references/native-subagent-contract.md:59-60`

Same sentence appears verbatim inside the Code Map Subagent prompt (`:97-99`),
the Continuous Review Subagent prompt (`:121-123`), and the Proof Freshness
Subagent prompt (`:151-153`).

**Parent's sub-agents.** This is the repo's most detailed *pro*-native-subagent
doctrine, with an explicit Good Uses / Bad Uses list
(`references/native-subagent-contract.md:8-35`). The restriction on the parent
is about *external* harnesses, not native ones:

> - Do not manually spawn separate coding-harness executables such as `codex`,
>   `claude`, `agent`, `grok`, or `kimi` for ordinary acceleration. This lightweight lane may
>   still hand an explicitly requested external worker or conductor to
>   `agent-delegate` or `conductor` under the shared policy; external
>   execution is a deliberate route, not a blanket ban.
>
> — `skills/plan-implement/SKILL.md:89-93`

**Defers to shared policy.** Yes (`SKILL.md:66-67`,
`references/native-subagent-contract.md:3-4`).

---

### The native-only review family — `cynical-*`, `exhaustive-code-review`, `plan-audit`

These are not external dispatchers; they are included because `conductor`
dispatches them *into* external fleet sessions, which is where the tension in
the conductor section comes from.

They forbid external transport as their own mechanism:

> - Do not manually spawn `codex`, `claude`, `agent`, `grok`, `kimi`, or any other
>   coding-harness executable.
> - Do not invoke external agent, delegation, consult, or review skills as the
>   review mechanism.
>
> — `skills/cynical-code-review/SKILL.md:75-78`

They fan out **native** children by design:

> - For broad targets, fan out only across genuinely independent review lenses
>   or path families. Start each independent slice as a new clean same-host
>   native child when the active host supports it...
>
> — `skills/cynical-code-review/SKILL.md:63-67`

And they apply the same nested ban to their own slices:

> - Children do not create children or invoke delegation, consult, or review
>   skills unless the parent explicitly assigns a nested scope and budget.
>
> — `skills/cynical-code-review/SKILL.md:71-72`
>   (identical at `skills/cynical-architecture-review/SKILL.md:77-78`,
>   `skills/cynical-cruft-removal/SKILL.md:80-81`,
>   `skills/exhaustive-code-review/SKILL.md:56-57`,
>   and `skills/plan-audit/SKILL.md:86-87`)

**Why this matters for conductor:** when conductor launches
`$cynical-code-review` inside an external fleet session, that session's *own*
native slices are exactly the "children of children" the conductor's worker
prompt contract forbids by default. Conductor is counting on them; nobody wrote
down that the instrument dispatch is the nested-scope assignment.

---

### The remaining workflow skills (consistent, no surprises)

`bugs-flow`, `audit-loop`, `audit-loop-sim`, `comment-loop`, `arch-docs`,
`lilarch`, `miniarch-step`, `arch-step`, `arch-step-goal-prompt`, and
`plan-interview` all restate the same BAN+override, all defer to the shared
policy, and all treat external transport as an available lane that must name its
benefit. Representative quotes:

- `skills/bugs-flow/SKILL.md:85-89`: *"Implementers and critics may not create
  children or invoke delegation, consult, or review skills unless the parent
  explicitly assigns a bounded nested scope and budget."*
- `skills/audit-loop/SKILL.md:80-81`, `skills/audit-loop-sim/SKILL.md:86-87`,
  `skills/comment-loop/SKILL.md:80-81`: *"They may not create children or invoke
  delegation, consult, or review skills unless the parent explicitly assigns a
  bounded nested scope and budget."*
- `skills/arch-docs/SKILL.md:97-99`: same rule for the docs ledger children.
- `skills/lilarch/SKILL.md:47-52`: *"Children do not fan out unless the parent
  explicitly assigns a bounded nested scope and budget, and total fanout stays
  proportional to independent work, host slots, collision risk, and parent
  integration capacity."*
- `skills/miniarch-step/SKILL.md:79-81`: *"Children do not fan out without a
  bounded nested scope and budget assigned by the parent."*
- `skills/arch-step/references/arch-consistency-pass.md:41-42`: *"children may
  not create children or invoke delegation or consultation workflows. This
  command assigns no nested scope or budget"* — a rare case of a skill
  explicitly closing the override for one command.
- `skills/arch-step/references/arch-review-gate.md:20`: the gate may not
  *"create a child or external reviewer merely to perform its own gate"*.
- `skills/arch-step-goal-prompt/references/arcstep-goal-prompt-contract.md:198-200`:
  the authored goal prompt must state *"the parent owns fanout and integration;
  children do not create children unless the parent explicitly assigns a bounded
  nested scope and budget"*.
- `skills/plan-interview/references/education-contract.md:19-23`: *"Clean
  read-only native children, non-overlapping lenses, no nested fanout"* — states
  the ban with no override clause.

---

## Inconsistencies and gaps

**1. Conductor's fleet-reviewer fanout is never reconciled with its own child
prompt contract.** `skills/conductor/SKILL.md:176-178` says every child prompt
forbids creating more model agents unless the parent deliberately assigns a
nested scope; `skills/conductor/references/delegation-and-monitoring.md:33-36`
and `references/audit-and-send-back.md:249-252` build the cost model on the
fleet reviewer fanning out its own slices. Nothing in conductor says the review
instrument dispatch *is* the nested-scope assignment, and the worker prompt
skeleton in `references/worker-prompt-contract.md:61-64` carries the flat
prohibition. A reader following the letter would strip the fanout the skill
depends on. **This is the single highest-value fix: one sentence in
`delegation-and-monitoring.md` saying the instrument dispatch grants the
instrument a bounded nested scope on the fleet host.**

**2. The whole suite bans nested children without ever distinguishing native
from external.** The shared policy's rule
(`skills/_shared/agent-orchestration-policy.md:201-202`) is transport-agnostic,
and every skill inherits that ambiguity. The working hypothesis this inventory
was written to test — "these skills ban native sub-agent usage inside the
spawned agent" — is **true only by inclusion**: they ban all children, so native
ones are covered. No skill says "the external Codex worker may not use its own
native sub-agents" in those words. Conductor is the only file in the repo that
reasons about the spawned agent's native sub-agents at all, and it reasons in
favor of them.

**3. Override clause present in some prompts, absent in others, with no stated
reason.** `codex-review-yolo` (`SKILL.md:68-70`,
`references/prompt-template.md:30`), the stepwise critic
(`references/critic-contract.md:162`), the stepwise diagnostic prompt
(`references/session-prompt-contracts.md:80-81`), conductor's shaping research
workers (`references/shaping-and-outcome-map.md:34`), and plan-interview's
researchers (`references/education-contract.md:21`) state a flat ban with no
"unless the parent assigns a nested scope" escape. Everywhere else the override
is explicit. This is probably deliberate for read-only single-shot roles, but
it is never said, so it reads as drift.

**4. `codex-babysit` is silent and out of the policy loop.** It never reads
`_shared/agent-orchestration-policy.md`, and its runbook
(`references/signals-and-runbook.md:109-113`) plus `_shared/aim-rotation.md:56-62`
document self-spawned Codex sub-agents as normal expected behavior to plan
around. Defensible — the babysat session was human-launched — but the repo has
no sentence connecting the two views. It is also not installed
(`Makefile:4` `REMOVED_SKILLS`) while `AGENTS.md` still routes to it.

**5. Conductor inverts the suite-wide native-first preference.** The shared
policy says *"Prefer a native child of the active host for ordinary same-host
work"* (lines 36-37). Conductor says *"Native subagents bill the parent's
expensive model — they are not a cheap lane, so bulk work never routes to
them"* (`SKILL.md:35-37`) and *"they are the parent's wallet with a different
face"* (`references/delegation-and-monitoring.md:11-12`). Conductor argues the
inversion in the policy's own terms (`SKILL.md:101-115`), so this is a
documented deviation rather than a violation — but it is the only skill whose
default lane is external, and anyone generalizing from conductor to the rest of
the suite will be wrong.

**6. Nobody addresses grandchild depth.** Every skill covers "child must not
create a child." Once a parent *does* assign a nested scope and budget, no file
says whether the grandchild inherits the same prohibition or whether the budget
is depth-1. In practice conductor's fleet reviewers already operate at depth 2
(parent → fleet session → review slice), so this is a live question, not a
hypothetical.

**7. The ban is prompt-level only, and the policy admits prompts are not
enforcement.** `skills/_shared/agent-orchestration-policy.md:165-168` says a
no-edit sentence "is not an enforced filesystem boundary" and prescribes a
parent-side `git status`/diff check as compensation. There is no analogous
compensating check for the no-nested-children rule — no skill tells the parent
to verify that its child did not spawn anything. `codex-review-yolo` comes
closest by requiring a pre/post repo-state comparison
(`SKILL.md:70-77`), but that catches edits, not fanout.

---

## Appendix: search commands used

```bash
rg -l "agent-orchestration-policy" skills/
rg -c -i "native subagent|native sub-agent|native child|subagent|sub-agent" skills/ -g '!__pycache__'
rg -n -i "own children|its own child|nested scope|must not create|do not create their own|no nested|nested delegation|nested agent|sub-delegat|subdelegat" skills/ -g '!__pycache__'
rg -n -i "native subagent|native sub-agent" skills/ -g '!__pycache__' -g '!*/build/*'
rg -l -i '\$agent-delegate|codex exec|claude -p|external session|external worker|external harness|external adapter|external fleet' skills/
```

`skills/*/build/` directories were excluded: the `Makefile` prunes `build`,
`prompts`, and `__pycache__` from every install target (lines 209, 245, 274,
312) and `verify_install` fails if they appear (lines 328, 359, 388, 435), so
they are not live runtime surface.
