# Comment Loop Quality Bar

Strong vs weak triage, findings, comments, and stop decisions. The quality bar for judging whether the comment-loop output is strong or weak.

## Strong triage

- The shipped code surface, proof surface, and explanatory surface are mapped exhaustively.
- Critical paths and outcome-critical shared contracts are explicit.
- Major unresolved comment fronts are explicit and come from the completed map.
- Priorities reflect consequence first, then sharedness, then explanation weakness, then confusion or staleness signals.
- The proof plan is explicit before edits begin.
- `SKIP` entries are deliberate and explained.
- Unavailable signals are recorded as `unknown`, not silently ignored.

## Weak triage

- The map is sampled or obviously incomplete.
- Priority order follows aesthetics or local readability guesses.
- The ledger has no clear consequence model or explanatory-surface inventory.
- The pass picked something that looked commentable before the map was complete.
- The pass keeps cashing out on low-amplitude comment wins while a bigger shared misunderstanding risk stays open.
- `SKIP` means "did not feel like it".
- The same low-value area keeps returning with no justification.

## Strong findings

- File anchors are concrete.
- The description names the misunderstanding risk clearly and ties it back to the mapped consequence.
- The proposed comment plan matches the actual finding.
- Stale or misleading comments are treated as real cleanup work, not optional polish.
- Multiple related findings may be resolved together when that is what the comment front demands.
- Comment-loop-added or materially rewritten comments explain the contract, convention, or gotcha without narrating obvious mechanics.

## Weak findings

- Vague "needs comments" notes.
- No file anchors.
- Broad documentation critiques not tied to a fixable explanation front.
- Comments that only restate names, signatures, or local mechanics.
- Comments that repeat the same convention at every call site instead of at the owner boundary.

## Strong stop decisions

- `CONTINUE` names a concrete next mapping tranche or comment front.
- `CLEAN` means the map is complete and there is no credible major unresolved explanation pass worth the cost.
- `BLOCKED` names the real blocker plainly.

## Weak stop decisions

- `CONTINUE` with no next area.
- `CLEAN` before the exhaustive map is complete.
- `CLEAN` while obvious `P0` or `P1` comment work still exists.
- `CLEAN` because one local comment landed even though the same larger shared misunderstanding front still has open justified work.
- `BLOCKED` when the real issue is simply lack of triage discipline.
