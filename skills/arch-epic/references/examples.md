# Worked examples

Five scenarios. Each walks through the user's interaction and the
skill's state transitions at key moments. These are teaching examples,
not a script to copy.

## Example 1 — Happy path, three sub-plans

### User invokes

> "Work on this repo. I want to ship a new admin dashboard with SSO
> support. Three plans roughly: SSO in the auth service, the
> dashboard itself, then migrate existing admins. Use claude
> fable-5 high for the critic."

### `start` mode

Skill proposes `docs/EPIC_ADMIN_DASHBOARD_SSO_2026-04-22.md`. User
is silent on path, so proceed. Skill writes frontmatter with
`critic_runtime: claude`, `critic_model: claude-fable-5`,
`critic_effort: high`, hashes set.

Drafts the Decomposition:

```
1. **Ship SSO in the auth service**: Add SAML/OIDC support to the
   existing email-password auth service.
   - DOC_PATH: (not yet set)
   - Gate to next: SSO login endpoint live in staging, returns a
     session token compatible with existing dashboard middleware.
   - Status: pending

2. **Build admin dashboard backed by SSO**: New internal dashboard
   that authenticates via the SSO flow from sub-plan 1.
   - DOC_PATH: (not yet set)
   - Gate to next: Admin dashboard live behind SSO for new users
     in staging.
   - Status: pending

3. **Migrate existing admins to SSO**: Cut over in-flight admins
   from email-password to SSO without session loss.
   - DOC_PATH: (not yet set)
   - Gate to next: (last sub-plan)
   - Status: pending
```

Orchestration Log:
- `2026-04-22 Goal captured. Decomposition drafted (3 sub-plans). Awaiting user approval.`

Skill ends turn, surfaces Decomposition, asks for approval.

### User replies
> "Looks good, go."

### `approve-decomposition` mode

Skill flips `sub_plans_approved: true`, `status: active`. Appends
log entry. Ends turn.

### Next turn — `run` mode, sub-plan 1 `pending`

Skill proposes
`docs/epic/ADMIN_DASHBOARD_SSO_2026-04-22/PHASE_01_AUTH_SSO_2026-04-22.md`
for sub-plan 1's DOC_PATH. Invokes
`$arch-step new docs/epic/ADMIN_DASHBOARD_SSO_2026-04-22/PHASE_01_AUTH_SSO_2026-04-22.md`
with the sub-plan's description as seed. Ends turn.

User confirms the North Star in the arch-step flow on the next
turn.

### Subsequent turns

- Skill sees `status: active` in sub-plan 1's DOC_PATH frontmatter.
  Updates epic Status to `north-star-approved`. Invokes
  `$arch-step auto-plan docs/epic/ADMIN_DASHBOARD_SSO_2026-04-22/PHASE_01_AUTH_SSO_2026-04-22.md`. Status becomes
  `planning`. Ends turn.
- Native goal-mode continuation drives auto-plan across turns (research,
  deep-dive pass 1, deep-dive pass 2, phase-plan, consistency-pass).
- Once `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc
  <DOC_PATH>` exits 0, skill invokes `$arch-step implement-loop`. Status becomes
  `implementing`.
- Native goal-mode continuation drives implement-loop and audit-implementation.
- Once audit COMPLETE, skill spawns the epic
  critic subprocess via `run_arch_epic.py critic-spawn`.
- Critic returns `verdict: pass`. Skill marks sub-plan 1 Status
  `complete`. Writes verdict path. Loops.

### Sub-plans 2 and 3 follow the same path

Each runs through `new` → `auto-plan` → `implement-loop` → critic.
All pass. After sub-plan 3 completes, skill sets
`status: complete`, appends final Orchestration Log entry, and
prints the summary.

## Example 2 — Scope-change detected, new sub-plan inserted

### During sub-plan 1 (Ship SSO in the auth service)

arch-step's implement-loop completes cleanly. Audit block says
`Verdict (code): COMPLETE`. Skill runs the epic critic.

### Critic's observations

The worklog contains this entry:

> "Phase 3: Added session token rotation hooks because the SSO
> provider's refresh-token lifecycle requires background rotation.
> Implemented the rotation call inline in the request middleware
> for now, but this really wants a dedicated background job — the
> middleware approach doesn't work for long-lived sessions that
> idle past refresh windows. Not blocking shipping today."

### Critic returns

```json
{
  "sub_plan_name": "Ship SSO in the auth service",
  "verdict": "scope_change_detected",
  "checks": [
    {"name": "epic_requirement_coverage", "status": "pass",
     "evidence": "sub-plan coverage owns SSO auth service requirements and assigns dashboard/migration requirements to named later sub-plans"},
    {"name": "north_star_preserved", "status": "pass",
     "evidence": "SSO login endpoint is live; session tokens issued"},
    {"name": "scope_not_cut", "status": "pass",
     "evidence": "all phase checklist items are complete"},
    {"name": "no_orphaned_discoveries", "status": "fail",
     "evidence": "worklog Phase 3 names token rotation background job as required for long-lived sessions but implementation is inline middleware"},
    {"name": "audit_clean", "status": "pass",
     "evidence": "arch-step audit COMPLETE, no reopened phases"}
  ],
  "discovered_items": [
    {
      "what": "background token rotation job for long-lived sessions; current middleware fails when session idles past refresh window",
      "scope_relationship": "required_for_approved_scope",
      "recommendation": "new_sub_plan"
    }
  ],
  "summary": "Sub-plan 1 shipped cleanly for short sessions but worklog names a required background rotation job that is not in any sub-plan's scope. Recommending new_sub_plan before sub-plan 2 (dashboard) starts."
}
```

### Skill applies scope lock

One `discovered_item`; `scope_relationship:
required_for_approved_scope`; `recommendation: new_sub_plan`. Per
`scope-change-discipline.md`, material scope items never auto-apply.
Skill halts.

Sets `status: halted`, sub-plan 1 Status to `scope-changed`.
Appends critic verdict path. Appends Decision Log entry:

> 2026-04-22 During sub-plan 1 (Ship SSO in the auth service)
> implementation, worklog surfaced that background token rotation
> is required for long-lived sessions. Current implementation
> is inline middleware and fails when sessions idle past refresh
> windows. Options:
>   a. extend_current — roll the rotation job into sub-plan 1's
>      scope, re-run implement-loop.
>   b. new_sub_plan — insert a new sub-plan between 1 and 2.
> What do you want?

Skill ends turn with the question.

### User replies
> "b, new sub-plan. Call it 'Token rotation background job.'"

### `resume-scope-change` mode

Skill inserts a new Decomposition entry as sub-plan 1.5:

```
1.5. **Token rotation background job**: Background job that
     rotates SSO session tokens ahead of refresh expiry for
     long-lived sessions.
   - DOC_PATH: (not yet set)
   - Gate to next: Rotation job running in staging, rotating
     tokens ahead of expiry with observable metrics.
   - Status: pending
```

Sub-plan 1 Status becomes `complete`. Original gate 1 → 2 is
moved to gate 1.5 → 2. Skill updates Orchestration Log and
Decision Log, flips `status: active`.

### Next turn

`run` mode sees sub-plan 1.5 `pending`. Skill proposes
`docs/epic/ADMIN_DASHBOARD_SSO_2026-04-22/PHASE_01_5_TOKEN_ROTATION_BACKGROUND_JOB_2026-04-22.md`
and invokes `$arch-step new` on that DOC_PATH. Flow continues as in
Example 1 from that point.

## Example 3 — Harmless improvement ignored, no scope action

### During sub-plan 2 (Build admin dashboard)

arch-step audit passes. Skill runs critic.

### Critic returns

```json
{
  "sub_plan_name": "Build admin dashboard backed by SSO",
  "verdict": "scope_change_detected",
  "checks": [
    {"name": "epic_requirement_coverage", "status": "pass",
     "evidence": "dashboard requirements are owned here; auth service SSO is satisfied by sub-plan 1; migration remains assigned to sub-plan 3"},
    {"name": "north_star_preserved", "status": "pass", "evidence": "..."},
    {"name": "scope_not_cut", "status": "pass", "evidence": "..."},
    {"name": "no_orphaned_discoveries", "status": "pass",
     "evidence": "worklog notes dashboard polls every 10s and mentions WebSockets would be cleaner, but the approved North Star and gate only require timely audit event visibility"},
    {"name": "audit_clean", "status": "pass", "evidence": "..."}
  ],
  "discovered_items": [],
  "summary": "Sub-plan 2 shipped cleanly. The WebSocket note is a harmless implementation observation, not approved scope drift."
}
```

### Skill applies scope lock

No `discovered_items` exist. Per `scope-change-discipline.md`, harmless
improvement ideas are ignored rather than recorded as scope decisions.

Skill:
- Marks sub-plan 2 Status `complete` with verdict path.
- Proceeds to sub-plan 3 on the next turn without stopping.

No scope choice was made. The WebSocket observation can become future work
only if the user asks for it outside the locked epic scope.

## Example 4 — Same-session `auto-plan`, then `auto-implement`

### User invokes

> "Use `$arch-epic auto-plan` on this approved payments migration epic.
> I want every sub-plan planned before implementation starts."

### `auto-plan` mode

The epic doc already has `sub_plans_approved: true`.

For sub-plan 1, the skill assigns:

```text
docs/epic/PAYMENTS_MIGRATION_2026-06-07/PHASE_01_PAYMENT_CONTRACT_2026-06-07.md
```

It creates only the sub-plan scaffold by applying the `arch-step new` artifact
contract directly from the approved Decomposition, raw epic goal, prior gates,
and Epic Requirement Coverage. Because the sub-plan North Star is a direct
expansion of approved scope, no separate user approval is needed. If there were
two valid North Stars, the skill would stop and ask. Scaffold creation is setup
only; it is not readiness proof.

Then it invokes:

```text
$arch-step auto-plan docs/epic/PAYMENTS_MIGRATION_2026-06-07/PHASE_01_PAYMENT_CONTRACT_2026-06-07.md
```

When `skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>` exits
0, the skill marks sub-plan 1:

```text
Status: planned
```

Native goal-mode continuation repeats the same process for sub-plans 2 and 3.
No implementation starts during `auto-plan`.

If the sub-plan doc has marker-looking planning blocks but missing or incomplete
generated receipts, `ready --doc <DOC_PATH>` fails. The skill keeps the sub-plan
at `planning` and continues `$arch-step auto-plan <DOC_PATH>` instead of moving
to the next sub-plan.

### User invokes

> "Now use `$arch-epic auto-implement`."

### `auto-implement` mode

The skill first confirms every non-complete sub-plan is `planned`. Then it
selects sub-plan 1, re-checks the ArcStep readiness gate for that exact
DOC_PATH, and invokes:

```text
$arch-step auto-implement docs/epic/PAYMENTS_MIGRATION_2026-06-07/PHASE_01_PAYMENT_CONTRACT_2026-06-07.md
```

One invocation is not completion. In native goal mode, the skill keeps that
same sub-plan at `implementing` and continues the real ArcStep
implement/prove/audit loop until the sub-plan's
`arch_skill:block:implementation_audit` says `Verdict (code): COMPLETE` or a
true blocker stops progress. If the audit is missing, NOT COMPLETE, or reopens
phases, the skill does not run the epic critic yet; it continues or reports the
exact `$arch-step auto-implement <DOC_PATH>` command.

When ArcStep audit is COMPLETE, the skill runs the normal epic critic. Only
after the critic passes does it mark sub-plan 1 `complete` and move to sub-plan
2. If the critic returns `incomplete`, the sub-plan stays `implementing` and
routes back through ArcStep instead of advancing.

### Takeaway

Same-session `auto-plan` and `auto-implement` are drivers over existing
`arch-step` proof. `auto-implement` needs ArcStep audit COMPLETE plus epic
critic pass for each sub-plan. They do not use the role table, spawned workers,
polling policy, or spawned-harness run directory.

## Example 5 — Spawned-harness automatic mode with role-based workers

### User invokes

> "Use `$arch-epic` to implement this approved payments migration
> epic automatically. Ask me which agents to use."

### Role-table gate

The epic doc already has `sub_plans_approved: true` and no
`auto_execution` block. The skill asks one consolidated question for
the spawned-harness role table:

```text
Before I run the epic automatically, I need the role execution table.

- epic_planner: drafts/repairs sub-plan North Stars and requirement coverage
- implementation_worker: edits code/docs and runs verification
- critic: checks North Star, plan readiness, completion, and scope drift
```

### User replies

> "Planner Claude Fable 5 high, implementation Codex gpt 5.5
> xhigh, critic Codex gpt 5.5 xhigh."

### `auto-run` mode

The skill resolves and announces:

```text
epic_planner -> runtime=claude, model=claude-fable-5, effort=high
implementation_worker -> runtime=codex, model=gpt-5.5, effort=xhigh
critic -> runtime=codex, model=gpt-5.5, effort=xhigh
poll_seconds -> 180
quiet_floor_seconds -> 900
stuck_floor_seconds -> 1800
max_runtime_seconds -> 7200
```

It writes `auto_execution` to the epic doc and initializes:

```text
.arch_skill/arch-epic/auto/payments-migration/run-<ts>/
```

For sub-plan 1, the parent orchestrator stays compact and launches
one child at a time:

1. Planner harness creates the numbered per-epic sub-plan DOC_PATH
   and Epic Requirement Coverage.
2. Critic harness checks the North Star / coverage gate.
3. Implementation worker edits the repo and updates the worklog.
4. Critic harness checks completion and scope drift.
5. If a critic finds ordinary in-scope unfinished work, the parent
   resumes the same planner or implementation worker session with the
   critic verdict as evidence. The critic does not prescribe repair
   steps.

The skill starts long planner and implementation children in detached mode,
then watches `child-status` and `child-tail` at the pinned `poll_seconds`
cadence while their `events.jsonl`, `stderr.log`, and `stream.log` grow. It
does not poll every few seconds, it does not call a child failed just because
there is no final artifact after a short window, and it does not plan sub-plan
2 until sub-plan 1 passes its critic gates.

## Takeaways

- In spawned-harness automatic mode, the user makes a bounded set of decisions:
  goal, decomposition, role execution policy, and scope changes. Everything
  else runs without their attention.
- Automatic repair is same-role session resume. The implementer keeps its
  context; the critic stays fresh and observation-only.
- `pass-after-retry` in stepwise has no analogue here. Spawned-harness mode may
  resume the same role session after a critic failure, but the sub-plan only
  advances after a fresh critic pass.
- The epic critic catches cross-plan issues; arch-step catches
  within-plan issues.
- Halting is normal when the critic flags approved-scope work. That is
  the skill doing its job, not a failure.
