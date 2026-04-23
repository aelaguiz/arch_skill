# Scope-change discipline: materially different path vs noise

The epic critic runs after each sub-plan finishes and arch-step's
audit confirms code completion. Its one unique job is to detect
scope drift — places where the shipped sub-plan diverges from what
the user approved, or where implementation surfaced a must-have
requirement nobody anticipated.

This file teaches what to flag and what to ignore. The critic reads
it. The orchestrator reads it too, because the orchestrator decides
whether to auto-apply the critic's recommendation or halt for user
input.

## What counts as "materially different"

A discovery is materially different when it affects the
decomposition or the approved spec of a sub-plan. Three specific
patterns:

1. The sub-plan's implementation revealed a new must-have surface
   that is not in the sub-plan's approved acceptance criteria.
   Example: sub-plan 1 shipped auth; worklog mentions that session
   tokens need a background rotation job that nobody listed. The
   rotation job is a whole new system — it deserves its own
   decision.
2. The sub-plan's implementation cut or downgraded something that
   was approved. Example: the phase plan listed "dashboard shows
   the last 30 days of audit events" in the acceptance criteria,
   but the shipped code only shows 7 days and there's no Decision
   Log entry explaining the change. That is silent scope reduction.
3. The sub-plan's implementation added behavior that nobody
   approved. Example: the sub-plan said "use existing auth" but
   the shipped code added a new guest-mode bypass. That is silent
   scope expansion.

All three are the critic's job to catch. All three cause
`verdict: scope_change_detected`.

## What counts as noise

A discovery is noise when it does not affect the decomposition or
the spec. The critic ignores:

- File renames during implementation.
- Internal helper refactors the plan did not prescribe.
- Utility functions added to deduplicate code.
- Linter warnings suppressed or configuration tweaks.
- Dirty git working tree at audit time.
- Style choices inside the sub-plan's declared scope (naming
  conventions, code layout, comment density).
- Minor test additions beyond what the phase plan required.
- A different third-party library choice if both serve the same
  contract and the North Star did not name a specific one.

These are implementation details the sub-plan's author is
authorized to make. The critic flagging them would be noise in the
other direction — it would halt epics for things the user does not
need to decide.

## Classifying a discovered item

When the critic finds a candidate for flagging, it fills a
`discovered_items[]` entry:

```json
{
  "what": "one-sentence description of the discovered need",
  "must_have_or_nice": "must_have" | "nice_to_have",
  "recommendation": "extend_current" | "new_sub_plan" | "defer" | "drop"
}
```

### `must_have_or_nice`

A discovery is `must_have` when omitting it means the sub-plan's
North Star is not actually met, or the gate to the next sub-plan
cannot be satisfied. If shipping the sub-plan without this item
leaves the user with a broken or unsafe path, it is must-have.

A discovery is `nice_to_have` when the sub-plan's North Star is
met without it and the gate still holds. The item is a legitimate
observation ("we noticed we could also do X") but the sub-plan
stands on its own.

### `recommendation`

- `extend_current`: the item fits inside the current sub-plan's
  scope without distortion. Typically a small additional task that
  reuses the sub-plan's surface and could have been in the
  original phase plan. The sub-plan goes back to implementing
  after the checklist and exit criteria are updated.
- `new_sub_plan`: the item is a separate piece of work with its
  own North Star. It belongs in a new arch-step plan inserted
  into the epic's Decomposition. Typically large enough to warrant
  its own planning pass.
- `defer`: the item is real but not needed for this epic. Park it
  in the Decision Log for the user's future consideration. The
  sub-plan is marked complete.
- `drop`: the item was a mirage — on closer look, it is not
  actually needed. Drop it entirely. Decision Log records the
  rationale so nobody re-discovers it later.

The critic makes its best recommendation. The orchestrator and the
user decide whether to accept it.

## Auto-act rule

When the critic returns `verdict: scope_change_detected`, the
orchestrator looks at every `discovered_items[]` entry:

- If every item has `must_have_or_nice: nice_to_have` AND
  `recommendation` in `{defer, drop}`: the orchestrator applies
  the recommendation automatically. Append a Decision Log entry
  naming each item and the action taken. Update the sub-plan
  Status to `complete`. Continue to the next sub-plan.
- If any item has `must_have_or_nice: must_have`: halt. Set epic
  `status: halted`, sub-plan Status to `scope-changed`, ask the
  user.
- If any item has `recommendation` in `{extend_current,
  new_sub_plan}`: halt regardless of must-have-or-nice. These
  recommendations change the decomposition. The user must decide.

The auto-act rule is narrow on purpose. The skill's value is that
it does not hide decisions that affect your decomposition. Items
the skill can confidently park or drop (nice-to-have observations,
not must-haves) are pure noise reduction; everything else is
yours to decide.

## What the orchestrator tells the user

When the orchestrator halts on a scope change, it renders the
critic's verdict in plain English. The user sees:

```
Sub-plan 2 (Build admin dashboard backed by SSO) is code-complete
per arch-step. The epic critic found one must-have discovery and
one nice-to-have:

1. [must_have] During implementation, the session store grew a
   new "locked" state to handle SSO revocation races. This is not
   in the original North Star (which said "uses existing auth") —
   it's new auth behavior.
   Recommended: new_sub_plan.

2. [nice_to_have] The dashboard currently polls for new audit
   events every 10s; a WebSocket upgrade would be cleaner.
   Recommended: defer.

Your options on item 1:
  a. extend current sub-plan — add the locked-state behavior into
     this sub-plan's scope (and re-run implement-loop).
  b. new sub-plan — insert a new sub-plan between this one and
     sub-plan 3. You approve a new North Star for it.
  c. defer — park for future, treat item 1 as non-blocking, mark
     this sub-plan complete.
  d. drop — decide the locked-state addition was unneeded, roll
     it back, mark this sub-plan complete.

Item 2 will be auto-deferred unless you say otherwise.

What do you want to do with item 1?
```

That format is the shape. Concrete, scannable, one decision at a
time. The user replies with a single letter or their own rewording;
the orchestrator applies and resumes.

## What the orchestrator does NOT do

- Pretend a must-have is a nice-to-have to avoid halting. The
  critic's classification is authoritative. If the orchestrator
  disagrees with the critic's classification, it surfaces that
  disagreement to the user, not silently reinterprets.
- Propose its own scope-change recommendation beyond the critic's.
  The orchestrator renders what the critic said; it does not add
  a fifth option.
- Skip the Decision Log entry when auto-applying. Every decision,
  even a purely-automatic one, leaves a paper trail so the user
  can review it later.
- Preemptively flag during implementation. The critic runs once,
  at sub-plan completion, after arch-step says the code is done.
  Mid-implementation discoveries are handled inside arch-step's
  own flow (its consistency-pass and audit-implementation stages).
  The epic critic is the cross-sub-plan guard.
