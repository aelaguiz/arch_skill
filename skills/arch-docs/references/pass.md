# Default DGTFO Pass

The default `arch-docs` invocation runs one bounded DGTFO cleanup pass:

- Discover
- Ground-truth
- Trim
- Fix
- Organize

## Goal

Leave the resolved docs scope materially cleaner than before without drifting into speculative or purely aesthetic reorganization.

## Ledger contract

Create or refresh `.doc-audit-ledger.md` while the pass is active.

Recommended sections:

- `# Doc Audit Ledger`
- `## Repo Doc Profile`
- `## Inventory`
- `## Topic Map`
- `## Deletions`
- `## Fixes Applied`
- `## Final Doc Map`
- `## Status`

This file is scaffolding, not a shipped artifact.

## Discover

- Inventory every doc-shaped surface in the resolved scope.
- If the run started with no narrower context, inventory the repo docs surface first, then choose the highest-confidence bounded topic cluster for the current pass.
- Record file, location, topic, likely freshness, and overlap notes.
- Check the last meaningful commit when staleness matters.

## Ground-truth

- For each topic, read the current code and current shipped behavior.
- Record contradictions across docs, code, and surviving behavior.
- Identify the one best canonical home for the topic.

## Trim

- Before deleting a bounded batch of stale or duplicate docs, stage those docs and create a backup git commit first.
- Stage only the docs in that delete batch, not unrelated dirty files elsewhere in the repo.
- If the backup commit cannot be created, stop instead of deleting.
- Delete stale or duplicate docs aggressively inside scope once the backup commit exists.
- Retire obsolete working docs and completed plan/worklog residue once durable truth has been promoted.
- Repair references after every delete.

## Fix

- Correct the surviving canonical docs against code truth.
- Front-load what readers actually need.
- Remove history and context that no longer helps.

## Organize

- Update the root README, docs index, or local README when the surviving canonical docs need a discoverable entry.
- Keep naming and placement aligned with existing repo conventions.

## Completion bar

A pass is strong when:

- the repo doc profile is grounded
- the touched topics have one canonical home each
- stale duplicates are gone
- broken references in touched scope are repaired
- durable truth was promoted before deletions
- `.doc-audit-ledger.md` is deleted before the run finishes clean, or kept only while an explicitly continuing multi-pass cleanup is still active

If those are not true yet, the pass should stop honestly with the next bounded move.
