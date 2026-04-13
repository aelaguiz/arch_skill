# Comment Loop Quality Bar

## Strong triage

- the shipped code surface, proof surface, and explanatory surface are mapped exhaustively
- critical paths and outcome-critical shared contracts are explicit
- major unresolved comment fronts are explicit and come from the completed map
- priorities reflect consequence first, then sharedness, then explanation weakness, then confusion or staleness signals
- the proof plan is explicit before edits begin
- `SKIP` entries are deliberate and explained
- unavailable signals are recorded as `unknown`, not silently ignored

## Weak triage

- the map is sampled or obviously incomplete
- priority order follows aesthetics or local readability guesses
- the ledger has no clear consequence model or explanatory-surface inventory
- the pass picked something that looked commentable before the map was complete
- the pass keeps cashing out on low-amplitude comment wins while a bigger shared misunderstanding risk stays open
- `SKIP` means "did not feel like it"
- the same low-value area keeps returning with no justification

## Strong findings

- file anchors are concrete
- the description names the misunderstanding risk clearly and ties it back to the mapped consequence
- the proposed comment plan matches the actual finding
- stale or misleading comments are treated as real cleanup work, not optional polish
- multiple related findings may be resolved together when that is what the comment front demands
- comment-loop-added or materially rewritten comments explain the contract, convention, or gotcha without narrating obvious mechanics

## Weak findings

- vague "needs comments" notes
- no file anchors
- broad documentation critiques not tied to a fixable explanation front
- comments that only restate names, signatures, or local mechanics
- comments that repeat the same convention at every call site instead of at the owner boundary

## Strong stop decisions

- `CONTINUE` names a concrete next mapping tranche or comment front
- `CLEAN` means the map is complete and there is no credible major unresolved explanation pass worth the cost
- `BLOCKED` names the real blocker plainly

## Weak stop decisions

- `CONTINUE` with no next area
- `CLEAN` before the exhaustive map is complete
- `CLEAN` while obvious `P0` or `P1` comment work still exists
- `CLEAN` because one local comment landed even though the same larger shared misunderstanding front still has open justified work
- `BLOCKED` when the real issue is simply lack of triage discipline
