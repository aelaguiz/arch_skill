# `review` Mode

## Goal

Run a fresh, docs-only audit verdict pass that decides whether the loop should continue, stop clean, or stop blocked.

## Writes

- `_audit_ledger.md`
- root `.gitignore` when the ledger is missing and must be repaired

No product code changes are allowed in `review`.

## Procedure

1. Create or repair `_audit_ledger.md` and the `.gitignore` entry if they are missing.
2. Re-read:
   - controller block
   - Phase 1 triage
   - open findings
   - test additions
   - decisions log
3. Inspect current repo state from fresh context:
   - changed files
   - relevant tests, build checks, or scanner output when needed
   - whether the latest pass actually reduced the top open risk
4. Set the controller block:
   - `CONTINUE` when a concrete worthwhile next area remains
   - `CLEAN` when only fixed items or explicit `SKIP`s remain and no credible next audit pass is justified
   - `BLOCKED` when the next move would be speculative, repeated, or stopped by a real blocker
5. Update `Last Review`.
6. Keep the ledger truthful about why the decision was made.

## Verdict rules

### `CONTINUE`

Use only when:

- a concrete next area exists
- the area is still justified by the priority matrix
- the next pass would not merely repeat the last failed idea

`Next Area` is required.

### `CLEAN`

Use only when:

- the highest-priority unresolved work has been fixed or explicitly skipped
- no credible `P0`, `P1`, or justified `P2` audit pass remains
- rescanning would likely just relitigate prior `SKIP` decisions

`Stop Reason` should be blank.

### `BLOCKED`

Use when:

- the next move depends on missing access, tooling, or evidence
- the failing baseline or current repo state makes the next pass unsafe
- the next pass would rerun the same idea without a changed lever
- the ledger is too weak to continue honestly without first repairing the investigation

`Stop Reason` is required.
