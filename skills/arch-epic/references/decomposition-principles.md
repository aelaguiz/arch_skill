# Decomposition principles: when to split a goal into sub-plans

The skill's first hard problem is decomposition. A big goal lands on your
desk; you have to propose an ordered list of sub-plans the user can scan
and approve in one read-through.

There is no checklist here. A recipe breaks on the non-obvious cases.
What you need is judgment about three things: independence, describability,
and ordering. This file teaches each one with a concrete example and a
counterexample.

## Independence: when does a sub-plan deserve its own DOC_PATH?

A sub-plan is independent enough to split out when its North Star and
acceptance criteria can be written without referencing another sub-plan's
internals. The sub-plan's spec stands on its own. Someone reading it cold
could tell you whether the work is done without also reading a sibling
plan.

Example — good split:
> Goal: "Ship a new admin dashboard with SSO."
> Sub-plan 1: Add SSO support to the existing auth service.
> Sub-plan 2: Build the admin dashboard that uses SSO.
>
> Sub-plan 1's North Star is stated in terms of the auth service's API
> contract. Sub-plan 2's North Star references that contract as an input,
> not its internals. A reviewer of sub-plan 1 does not need the dashboard
> spec to judge it.

Counterexample — bad split:
> Goal: "Add a notifications feature."
> Sub-plan 1: Build the notification service.
> Sub-plan 2: Wire the notification service into every touchpoint.
>
> Sub-plan 2 cannot be described without cross-referencing sub-plan 1's
> internals (which queues, which delivery states, which retry semantics).
> These should be one sub-plan. The "wire everything up" phase is a
> Section 7 phase inside the notifications plan, not a sibling plan.

The rule of thumb: if the split forces a reader to flip between two plan
docs to understand either one, it is not really a split. Fold them.

## Describability: does the one-sentence test pass?

Every sub-plan should be statable in one plain-English sentence a
non-technical reader understands. This is not a formatting rule; it is a
diagnostic. If you cannot write the sentence, the sub-plan is not well
scoped yet.

Example — sentence passes the test:
> "Add magic-link login to the existing email-password auth service."

A reader can tell you the goal (new login mode), the surface (the auth
service), and the boundary (add, not replace). That is enough to approve
or reject without reading the full plan.

Counterexample — sentence fails the test:
> "Handle all the data stuff."

There is no goal. No surface. No boundary. A sub-plan like this is always
the seam where scope drift happens during implementation. Push back. Ask
what concrete output the sub-plan produces, then rewrite.

When a sentence is getting long ("Add magic-link login and TOTP and
WebAuthn with a shared second-factor registry and also refactor the
session store"), that is a signal to split again, not a signal to keep
writing.

## Ordering: dependency first, risk next

Sub-plans are ordered by dependency and then by risk.

Dependency means: sub-plan B cannot start until sub-plan A has shipped
a stable piece of output (an API, a schema, a migration). Order those
with A before B. Do not overlap.

Risk means: if two sub-plans have no dependency, run the scariest one
first. Scary means high uncertainty, novel territory, likely to surface
a new requirement during implementation. If it blows up, it blows up
early and you can adjust the decomposition before a lot of downstream
work depends on it.

Example — ordering by dependency:
> Sub-plan 1: Design and ship the v2 search API contract.
> Sub-plan 2: Migrate the web UI from v1 to v2 search.
> Sub-plan 3: Migrate the mobile clients from v1 to v2 search.

Sub-plans 2 and 3 are independent of each other but both depend on 1.
You could do 2 and 3 in either order after 1. Pick the one with higher
risk first (probably mobile — shipping cycle is slower, edge cases
harder to patch post-ship).

Counterexample — ordering by convenience:
> Sub-plan 1: Web UI migration.
> Sub-plan 2: Design the v2 API.
> Sub-plan 3: Mobile migration.

Sub-plan 1 cannot actually start until 2 is done; this ordering lies
about when each sub-plan is runnable. Reorder.

## Inter-plan gates: assertions, not tasks

Between consecutive sub-plans there is a gate: the condition that must
be true before the next sub-plan can start planning. A gate is an
assertion about shipped state, not a task description.

Example — good gate:
> "The v2 search API contract is locked in docs/SEARCH_V2_API_*.md and
> the endpoints return production data for at least one query type."

A reader can check the gate by reading the named doc and hitting the
endpoint. It is falsifiable.

Counterexample — bad gate:
> "Finish the API work."

This is a task. It tells you nothing about what "finish" means, and
there is no state to inspect. The gate needs to name what will exist
when sub-plan A is truly ready to hand off to sub-plan B.

Gates are stored verbatim in the epic doc's Decomposition section.
They also end up surfaced to the user at decomposition-approval time so
the user can reject fuzzy gates before any real work begins.

## How many sub-plans?

Typical: three to seven. That number fits on a screen, a reader can
hold the whole map in their head, and each sub-plan is weighty enough
to justify arch-step's canonical plan discipline.

Fewer than three: consider whether `arch-epic` is even the right skill.
A two-sub-plan epic is sometimes legitimate (shared system + its
consumer), but a one-sub-plan "epic" is just an `$arch-step` plan with
extra ceremony around it — send the user there directly.

More than seven: the decomposition is probably too fine. Each
`$arch-step` plan already has its own Section 7 phase discipline, which
breaks a sub-plan into smaller ordered phases inside its own canonical
doc. If you find yourself proposing ten sub-plans, look for sub-plans
that share a surface and fold them back together, letting arch-step's
phases carry the weight.

## Announcing the decomposition to the user

When the skill presents the decomposition for approval, present it
exactly the way the user will want to review it:

```
Decomposition (draft — needs your approval):

1. Ship SSO support in the auth service.
2. Build the admin dashboard backed by SSO.
3. Migrate existing admin users onto SSO without session loss.

Gates between:
1 → 2: SSO login endpoint is live in staging and returns a session
      token compatible with the existing dashboard middleware.
2 → 3: Admin dashboard is live behind SSO for new users in staging.

Order rationale: 2 and 3 both depend on 1. 3 runs after 2 because the
migration script needs to test against the real dashboard.
```

That is the format. Short, scannable, falsifiable gates, explicit
ordering rationale. If the user says "swap 2 and 3" or "combine 2 and
3 into one sub-plan," apply the change and re-render before moving on.

## When to ask vs. propose

Ask the user if:
- The goal references a system or concept you cannot locate in any repo
  you have access to. Decomposition needs ground truth; do not guess.
- The goal has two equally valid splits and neither dominates on
  dependency or risk. Present both briefly and let the user pick.
- The goal contains scope you suspect the user did not mean. Example:
  "overhaul the billing system" — ask whether that includes the
  dunning flow or is strictly the checkout path.

Propose confidently if:
- The goal is concrete and the repo's existing architecture makes the
  boundaries obvious. Draft the decomposition and hand it to the user
  to approve or adjust.
- The goal references patterns the repo already uses (e.g., "add
  another provider to the existing integration layer"). The
  decomposition mirrors the existing layering.

Announcing uncertainty is fine. Pretending to know when you do not is
not.
