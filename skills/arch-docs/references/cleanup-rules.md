# Cleanup Rules

The bias is delete-and-consolidate, not add-and-preserve.

## Delete immediately

- TEMP, DRAFT, WIP, OLD, or DEPRECATED files whose subject is already shipped, removed, or superseded
- duplicate docs when another doc covers the same topic better
- docs for features or systems that no longer exist
- empty or near-empty stubs
- obsolete working docs after their durable truth is promoted elsewhere

## Consolidate then delete

- Merge the good parts into the canonical surviving doc.
- Delete the weaker duplicate in the same run.
- Do not leave a live redirect stub that only says "see other file." Those rot quickly.

## Plan and worklog retirement

- Treat plan docs, worklogs, investigation notes, and similar working artifacts as temporary unless they are transformed into the one canonical evergreen doc.
- Mine durable truth into evergreen docs first.
- If the plan doc can be transformed in place into the one clean evergreen doc, do that and remove the arch scaffolding.
- Otherwise fold the durable truth into better homes and delete the obsolete working docs.

## Reference repair

- After every delete or move, grep the repo for references to the deleted path.
- Fix or remove broken references in the same pass.
- Broken internal links are a docs-cleanup failure, not optional polish.

## Concision rules

- Remove history that is no longer needed to understand the current state.
- Remove hedging and filler.
- Remove examples that no longer run against the current codebase.
- If a sentence cannot be grounded confidently, delete it instead of keeping an aspirational guess.

## Ledger rule

- Use `.doc-audit-ledger.md` as temporary scaffolding only.
- It should include:
  - repo doc profile
  - inventory
  - topic map
  - deletions
  - fixes applied
  - final doc map while the pass is active
- Delete the ledger before the cleanup is declared complete.
