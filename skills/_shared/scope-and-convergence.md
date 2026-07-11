# Scope And Convergence Doctrine

Use this reference for fixed-scope planning, plan-backed implementation, and
plan-backed review. It defines when adjacent work belongs in a clean solution
and when it is unauthorized scope growth.

## Governing Law

Build exactly the human-authorized outcome with the smallest sufficient
solution. During initial plan architecture, include only the adjacent
same-contract work required to leave one authoritative owner. Freeze that scope
before implementation. After the freeze, scope increases only when a human
asks for or explicitly approves the increase.

```text
Allowed implementation scope
  = human-authorized outcome and constraints
  + initial minimal convergence closure frozen before implementation
  + later expansion explicitly approved by a human decision owner
```

A worker, reviewer, audit, verifier, plan edit, worklog, test, PR comment, or
already-built code path cannot authorize scope.

## Terms

- **Human-authorized outcome:** behavior, constraints, supported surfaces, and
  acceptance results directly requested or explicitly approved by the relevant
  human decision owner.
- **Smallest sufficient solution:** the least new behavior, code, concepts,
  owners, proof, and operational surface that genuinely satisfies that outcome
  through the correct owner path.
- **Competing authority:** two live paths can independently define, write,
  validate, route, render, serialize, configure, or teach the same contract so
  a future change could update one and leave the other stale. Similar-looking
  code or nearby debt is not enough.
- **Initial minimal convergence closure:** the smallest adjacent set of caller
  migrations, owner moves, cutovers, or deletes that initial plan architecture
  must include because the narrow change would otherwise create or preserve a
  competing authority for the exact changed contract.
- **Scope freeze:** the implementation-ready boundary after initial
  architecture, call-site mapping, cutover/delete decisions, and phase planning
  are complete, but before the first implementation edit or worker dispatch.
- **Scope cycling:** agent- or reviewer-created work becomes code, then later
  plans, tests, logs, or reviews treat that code as authority and demand still
  more work from it.

## Initial Architecture Window

Initial plan architecture may include adjacent work without a separate human
ask only when every condition below is true:

1. The exact changed contract and intended canonical owner are named.
2. Current repo evidence identifies the competing live paths.
3. Leaving those paths untouched would make this change split-brained,
   partially migrated, or dependent on a side door.
4. The added work only routes, migrates, consolidates, or deletes. It adds no
   new product behavior, guarantee, platform, mode, generic extension point,
   or speculative infrastructure.
5. The chosen boundary is the smallest set that restores one authority.
6. The plan records the closure and delete/cutover before it freezes.

If any condition fails, keep the item out of scope or ask a human. Pattern
parity, general correctness, architectural taste, a real edge case, or a
reviewer's concern can shape work already in scope; none can broaden scope.

The plan's Scope and Simplicity Contract should record:

- human-authorized outcome and authorization anchors;
- smallest sufficient solution;
- initial minimal convergence closure, including explicit `none`;
- scope-freeze boundary;
- enough proof;
- do-not-build boundary;
- accepted residual risk.

The canonical plan owns those facts. Logs and review artifacts point to plan
anchors; they do not copy or replace the contract.

## After Scope Freeze

Implementation and review may:

- complete or repair work already named by the human outcome or frozen initial
  convergence closure;
- subtract unauthorized machinery or redesign inside the frozen boundary;
- report a newly discovered adjacent path and ask a human to expand and
  re-freeze the plan;
- record a real out-of-scope observation when it materially matters.

Implementation and review may not:

- add a newly discovered adjacent path to the closure;
- turn a finding into an automatic implementation obligation;
- update the plan after building something and cite that update as authority;
- use repeated reviewer agreement as approval;
- preserve unauthorized work because tests, docs, callers, or later code now
  depend on it.

If a review is the first agent to find a competing same-contract path, the
review may reject the result but cannot expand the repair scope. The next move
is either human-approved expansion and re-freeze, or subtraction/redesign
inside the existing boundary.

## Finding Dispositions

For plan-backed implementation or review, classify each material finding as:

- **authorized:** directly required by frozen human scope;
- **frozen-convergence-required:** already named in the initial convergence
  closure;
- **new-scope-needs-human:** absent from the frozen contract, including a newly
  discovered same-contract path;
- **out-of-scope:** real but not required for this change;
- **unauthorized-built-scope:** implemented without authority and requiring
  subtraction or explicit human ratification.

Only the first two become automatic repair work. A repeated finding keeps the
same disposition; repetition does not create authority.

## Scope-Cycling Hard Fail

For plan-backed or history-backed cynical review, reconstruct the initial human
scope, frozen convergence closure, later human approvals, plan revisions,
worker/review waves, and final code. Unauthorized post-freeze growth is
blocking even when it works and tests pass.

The accepted resolutions are:

1. subtract or consolidate the unauthorized work back to the frozen contract;
2. obtain explicit approval from the human decision owner, update the canonical
   plan, and re-freeze before implementation resumes.

Reviewer findings never satisfy option 2. When a plan-backed review should
have scope provenance but cannot recover it, return the review's non-approving
coverage verdict instead of guessing. Standalone reviews with no plan,
completion claim, or human-scope history may mark this lane not applicable.

## Legacy Plans

Do not bulk-rewrite historical plans. Before implementing a legacy or
non-canonical plan, recover and record the equivalent frozen contract at
intake. If the boundary cannot be established without inventing intent, stop
for one human scope decision before editing.
