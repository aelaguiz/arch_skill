# Bugs Flow Review Mode

## Goal

Audit the implementation against the bug doc only when the user explicitly
asked for review. Each independent gate uses a new clean critic; accepted
repairs return to the exact implementer that owns the fix.

## Dispatch And Ownership

- The parent owns the bug scope, frozen convergence closure, bug-doc writes,
  finding disposition, accepted repairs, synthesis, and final verdict.
- Capture current git status and the relevant diff before dispatch, then start
  a new clean same-host native critic by default. In Codex set
  `fork_turns: "none"`; in Claude use a clean named or custom subagent, not a
  bare conversation fork or skill `context: fork` shorthand.
- Pass `DOC_PATH`, exact implementation paths, verification evidence, and the
  frozen closure directly. Use bounded or full inherited context only for a
  named dependency that exists solely in chat.
- Select the strongest read-only capability available and explicitly tell the
  critic not to edit or write code, the bug doc, or any other file. The critic
  may not create children or invoke delegation, consult, or review skills
  unless the parent explicitly assigned a bounded nested scope and budget.
- If independent lenses genuinely warrant fanout, keep them non-overlapping
  and bound the wave by host slots, shared-file or shared-state collision risk,
  and the parent's capacity to inspect and integrate every return.
- External review remains available when a concrete provider, model,
  lifecycle, isolation, automation, receipt, or other benefit is worth the
  added process and integration cost. It is neither banned nor required for a
  clean review, and it follows the same no-write and parent-integration
  contract.

## Review scope

- Does the code fix the documented bug?
- Does the verification evidence match the bug?
- Did the implementation introduce forbidden fallback or shim behavior?
- Did the doc truth stay current?
- Did the implementation stay inside the frozen bug scope and avoid scope
  cycling?

## Rules

- Review is explicit-review-only.
- Findings should be bug-specific, not a generic cleanup wishlist.
- Classify material findings using the shared scope dispositions. Review may
  require repair of authorized/frozen-closure work or subtraction of
  unauthorized work; it may not add an adjacent area to the fix.
- If the fix is incomplete, reopen the doc status and name the missing work.
- If the user did not ask for review, stop after local verification.

## Return And Repair Loop

The critic returns completion status, files and paths inspected, bug-specific
findings with evidence, scope disposition, coverage limits, and blockers or
collision risks. The parent accounts for every critic return, compares current
git status and diff with the pre-dispatch state, spot-checks the evidence, and
decides which findings to accept.

Send accepted repair findings to the exact implementer handle that produced or
owns the fix. Keep the repair inside the frozen closure. After repair and
verification, start a different new clean critic for the next independent
gate; do not resume or recycle the prior critic. The parent alone updates the
bug doc and declares the final verdict.
