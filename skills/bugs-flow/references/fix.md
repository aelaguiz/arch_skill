# Bugs Flow Fix Mode

## Goal

Implement the smallest credible fix that resolves the bug described by the doc and keeps verification honest.

## Required work

1. Re-read the bug doc and confirm it is fix-ready.
2. Confirm the scope closure is frozen. Implement only the corrected behavior
   and directly competing paths already in that closure.
3. Tighten the fix plan in the doc without expanding scope.
4. Implement the smallest credible fix locally.
5. Run the smallest credible verification.
6. Update the implementation and verification sections.

If fix mode discovers another same-contract path or broader improvement, stop
with `new-scope-needs-human`; do not relabel it a systemic fix. If unauthorized
work was already built, subtract it before completion unless a human approves
and re-freezes the bug contract.

## Delegated implementer contract

The parent may keep a small fix local. When delegation saves real work, start
one new clean same-host native implementer and give it the bug doc, frozen
closure, exact owned paths, verification obligation, and explicit edit scope.
In Codex set `fork_turns: "none"`; in Claude use a clean named or custom
subagent rather than a bare conversation fork or skill `context: fork`
shorthand. Use bounded or full inherited context only for a named dependency
that exists solely in chat.

Preserve the implementer's exact handle. The child may not create children or
invoke delegation, consult, or review skills unless the parent explicitly
assigned a bounded nested scope and budget. Sequence any colliding edit scope
under this one owner rather than launching overlapping implementers. The parent
checks the current diff and bug doc, integrates the result, and sends accepted
review repairs back through the exact handle. A later independent critic is a
new clean child, not a continuation of the implementer.

## Minimal-fix examples

- Good:
  - correct the nil/empty guard that caused the crash
  - move the parse or validation to the one correct boundary
  - update the one call-site family that still sends the bad payload
- Bad:
  - return empty or null to silence the failure
  - stale-cache or default-value fallback that masks bad state
  - "try the old API if the new one fails"
  - dev-only shim left in production

## Verification rule

- Verify the specific failure mode first.
- Add broader regression checks only when the blast radius justifies them.
- If a negative-value test blocks the fix because it encodes the wrong behavior, rewrite or delete that test. Do not preserve a false contract.
