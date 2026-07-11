# Bugs Flow Review Mode

## Goal

Audit the implementation against the bug doc only when the user explicitly asked for review.

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
