# Bugs Flow Review Mode

## Goal

Audit the implementation against the bug doc only when the user explicitly asked for review.

## Review scope

- Does the code fix the documented bug?
- Does the verification evidence match the bug?
- Did the implementation introduce forbidden fallback or shim behavior?
- Did the doc truth stay current?

## Rules

- Review is explicit-review-only.
- Findings should be bug-specific, not a generic cleanup wishlist.
- If the fix is incomplete, reopen the doc status and name the missing work.
- If the user did not ask for review, stop after local verification.
