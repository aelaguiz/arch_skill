# Worked examples

Three scenarios. Each walks through the user's interaction and the
skill's state transitions at key moments. These are teaching examples,
not a script to copy.

## Example 1 — Happy path, three sub-plans

### User invokes

> "Work on this repo. I want to ship a new admin dashboard with SSO
> support. Three plans roughly: SSO in the auth service, the
> dashboard itself, then migrate existing admins. Use claude
> opus-4-7 xhigh for the critic."

### `start` mode

Skill proposes `docs/EPIC_ADMIN_DASHBOARD_SSO_2026-04-22.md`. User
is silent on path, so proceed. Skill writes frontmatter with
`critic_runtime: claude`, `critic_model: opus-4-7`,
`critic_effort: xhigh`, hashes set.

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

Skill proposes `docs/AUTH_SSO_2026-04-22.md` for sub-plan 1's
DOC_PATH. Invokes `$arch-step new docs/AUTH_SSO_2026-04-22.md`
with the sub-plan's description as seed. Ends turn.

User confirms the North Star in the arch-step flow on the next
turn.

### Subsequent turns

- Skill sees `status: active` in sub-plan 1's DOC_PATH frontmatter.
  Updates epic Status to `north-star-approved`. Invokes
  `$arch-step auto-plan docs/AUTH_SSO_2026-04-22.md`. Status becomes
  `planning`. Ends turn.
- Hook drives auto-plan across several turns (research,
  deep-dive, phase-plan, consistency-pass).
- Once state file is absent and consistency-pass is clean, skill
  invokes `$arch-step implement-loop`. Status becomes `implementing`.
- Hook drives implement-loop and audit-implementation.
- Once audit COMPLETE and no state file, skill spawns the epic
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
      "must_have_or_nice": "must_have",
      "recommendation": "new_sub_plan"
    }
  ],
  "summary": "Sub-plan 1 shipped cleanly for short sessions but worklog names a must-have background rotation job that is not in any sub-plan's scope. Recommending new_sub_plan before sub-plan 2 (dashboard) starts."
}
```

### Skill applies auto-act rule

One `discovered_item`; `must_have_or_nice: must_have`;
`recommendation: new_sub_plan`. Per `scope-change-discipline.md`,
must-have items never auto-apply. Skill halts.

Sets `status: halted`, sub-plan 1 Status to `scope-changed`.
Appends critic verdict path. Appends Decision Log entry:

> 2026-04-22 During sub-plan 1 (Ship SSO in the auth service)
> implementation, worklog surfaced that background token rotation
> is a must-have for long-lived sessions. Current implementation
> is inline middleware and fails when sessions idle past refresh
> windows. Options:
>   a. extend_current — roll the rotation job into sub-plan 1's
>      scope, re-run implement-loop.
>   b. new_sub_plan — insert a new sub-plan between 1 and 2.
>   c. defer — mark sub-plan 1 complete and park the rotation
>      issue for future.
>   d. drop — decide the rotation job is unneeded (reverse course
>      on the middleware change).
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

`run` mode sees sub-plan 1.5 `pending`. Invokes `$arch-step new`
on a proposed DOC_PATH. Flow continues as in Example 1 from that
point.

## Example 3 — Scope-change auto-acted on nice-to-have

### During sub-plan 2 (Build admin dashboard)

arch-step audit passes. Skill runs critic.

### Critic returns

```json
{
  "sub_plan_name": "Build admin dashboard backed by SSO",
  "verdict": "scope_change_detected",
  "checks": [
    {"name": "north_star_preserved", "status": "pass", "evidence": "..."},
    {"name": "scope_not_cut", "status": "pass", "evidence": "..."},
    {"name": "no_orphaned_discoveries", "status": "fail",
     "evidence": "worklog notes dashboard polls every 10s for audit events; implementer notes a WebSocket upgrade would be cleaner but is not required for staging"},
    {"name": "audit_clean", "status": "pass", "evidence": "..."}
  ],
  "discovered_items": [
    {
      "what": "WebSocket upgrade for audit event streaming instead of 10s polling",
      "must_have_or_nice": "nice_to_have",
      "recommendation": "defer"
    }
  ],
  "summary": "Sub-plan 2 shipped cleanly. One nice-to-have deferral identified: WebSocket upgrade for audit event streaming."
}
```

### Skill applies auto-act rule

One `discovered_item`; `must_have_or_nice: nice_to_have`;
`recommendation: defer`. Per `scope-change-discipline.md`, this
case auto-applies (all items nice_to_have, all recommendations in
`{defer, drop}`).

Skill:
- Appends Decision Log entry:
  > 2026-04-22 Sub-plan 2 completion: auto-deferred nice-to-have
  > item: WebSocket upgrade for audit event streaming. Current
  > 10s polling is sufficient for the approved North Star.
- Marks sub-plan 2 Status `complete` with verdict path.
- Announces the auto-action to the user (one line).
- Proceeds to sub-plan 3 on the next turn without stopping.

User sees the auto-deferral in the Decision Log and the brief
console notice but is not blocked.

## Takeaways

- The user makes three kinds of decisions: goal, decomposition,
  scope changes. Everything else runs without their attention.
- `pass-after-retry` in stepwise has no analogue here — sub-plans
  don't retry at the epic level. arch-step's implement-loop
  retries internally until audit passes or blocks.
- The epic critic catches cross-plan issues; arch-step catches
  within-plan issues.
- Halting is normal when the critic flags a must-have. That is
  the skill doing its job, not a failure.
