# Audit Loop Sim Quality Bar

## Strong triage

- major user journeys and primary-path risk fronts are explicit
- major unresolved automation risk fronts are explicit
- priorities reflect real user impact, missing real-app signal, platform truth, and churn when useful
- `SKIP` entries are deliberate and explained
- unavailable signals are recorded as `unknown`, not silently ignored

## Weak triage

- priority order follows file size, aesthetics, or guesswork
- the ledger has no clear primary journeys
- the pass keeps cashing out on low-amplitude test tweaks while a larger journey gap stays open
- `SKIP` means "did not feel like it"
- the same low-value area keeps returning with no justification

## Strong findings

- file anchors are concrete
- the description names the real-app blind spot, breakage, or fragility clearly
- the proposed fix matches the actual finding
- multiple related findings may be resolved together when that is what the automation risk front demands
- the pass adds or repairs durable automation instead of only explaining what should probably be tested someday

## Weak findings

- vague "needs better tests" notes
- no file anchors
- broad design critiques not tied to a fixable risk
- automation that protects implementation details without improving real-app signal

## Strong stop decisions

- `CONTINUE` names a concrete next automation risk front
- `CLEAN` means there is no credible major unresolved automation pass worth the cost
- `BLOCKED` names the real blocker plainly
- repeated lane-independent provider failures with no meaningful app signal are classified plainly as provider blockers instead of being rerun as if they were app bugs

## Weak stop decisions

- `CONTINUE` with no next area
- `CLEAN` while obvious `P0` or `P1` work still exists
- `CLEAN` because one small lane landed even though the same larger journey gap still has open justified work
- `BLOCKED` when the real issue is simply lack of triage discipline
- `BLOCKED` when the only problem is that the current review context could not inspect the sanctioned runtime surface
- `BLOCKED` or `CLEAN` because a child review deleted the state file or ledger and the controller trusted that deletion as truth
