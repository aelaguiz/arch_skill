# Bugs Flow Fix Mode

Fix mode: implement the smallest credible fix that resolves the bug described by the doc and keeps verification honest.

## Goal

Implement the smallest credible fix that resolves the bug described by the doc and keeps verification honest.

## Required work

- Re-read the bug doc and confirm it is fix-ready.
- Tighten the fix plan in the doc if needed.
- Implement the smallest credible fix locally.
- Run the smallest credible verification.
- Update the implementation and verification sections.

## Minimal-fix examples

### Good:

- correct the nil/empty guard that caused the crash
- move the parse or validation to the one correct boundary
- update the one call-site family that still sends the bad payload

### Bad:

- return empty or null to silence the failure
- stale-cache or default-value fallback that masks bad state
- 'try the old API if the new one fails'
- dev-only shim left in production

## Verification rule

Verify the specific failure mode first.
Add broader regression checks only when the blast radius justifies them.
If a negative-value test blocks the fix because it encodes the wrong behavior, rewrite or delete that test. Do not preserve a false contract.
