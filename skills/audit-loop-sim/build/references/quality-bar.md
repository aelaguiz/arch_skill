# Quality Bar

Strong vs weak triage, findings, tests, and stop decisions for the audit-loop-sim workflow.

## Strong triage

- The app surface, journey surface, and automation surface are mapped exhaustively.
- Major user journeys, primary-path risk fronts, and automation owners are explicit.
- Major unresolved automation risk fronts are explicit and come from the completed map.
- Priorities reflect real user impact first, then missing or weak real-app signal, then platform truth and fragility.
- The proof plan and post-change audit focus are explicit before edits begin.
- `SKIP` entries are deliberate and explained.
- Unavailable signals are recorded as `unknown`, not silently ignored.

## Weak triage

- The map is sampled or obviously incomplete.
- Priority order follows file size, aesthetics, or guesswork.
- The ledger has no clear journey model or automation-surface inventory.
- The pass picked something that looked fixable before the map was complete.
- The pass keeps cashing out on low-amplitude test tweaks while a larger journey gap stays open.
- `SKIP` means "did not feel like it".
- The same low-value area keeps returning with no justification.

## Strong findings

- File anchors are concrete.
- The description names the real-app blind spot, breakage, or fragility clearly and ties it back to the mapped consequence.
- The proposed fix matches the actual finding.
- Multiple related findings may be resolved together when that is what the automation risk front demands.
- The pass adds or repairs durable automation instead of only explaining what should probably be tested someday.
- The final diff passes an explicit post-change audit for safety, downstream consequences, elegance, and duplication.
- Same-story product logic and harness behavior are converged instead of spread into a second copy.

## Weak findings

- Vague "needs better tests" notes.
- No file anchors.
- Broad design critiques not tied to a fixable risk.
- Automation that protects implementation details without improving real-app signal.
- A "fix" that works only because the same lane or fallback handling was copied into another place.
- A pass that never audited the resulting diff after the first lane went green.

## Strong stop decisions

- `CONTINUE` names a concrete next mapping tranche or automation risk front.
- `CLEAN` means the map is complete and there is no credible major unresolved automation pass worth the cost.
- `CLEAN` means the latest editful pass also passed the post-change audit.
- `BLOCKED` names the real blocker plainly.
- Repeated lane-independent provider failures with no meaningful app signal are classified plainly as provider blockers instead of being rerun as if they were app bugs.

## Weak stop decisions

- `CONTINUE` with no next area.
- `CLEAN` before the exhaustive map is complete.
- `CLEAN` while obvious `P0` or `P1` work still exists.
- `CLEAN` because one small lane landed even though the same larger journey gap still has open justified work.
- `CLEAN` because lanes passed even though the resulting diff is still awkward, unsafe, or duplicative.
- `BLOCKED` when the real issue is simply lack of triage discipline.
- `BLOCKED` when the only problem is that the current review context could not inspect the sanctioned runtime surface.
- `BLOCKED` or `CLEAN` because a child review deleted the state file or ledger and the controller trusted that deletion as truth.
