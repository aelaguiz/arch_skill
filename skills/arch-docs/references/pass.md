# Default DGTFO Pass

The default `arch-docs` invocation runs one grounded DGTFO cleanup pass:

- Discover
- Ground-truth
- Trim
- Fix
- Organize

## Goal

Leave the resolved docs scope materially healthier than before: cleaner, more current, clearer, and easier for readers to rely on, without drifting into speculative or purely aesthetic reorganization.

## Ledger contract

Create or refresh `.doc-audit-ledger.md` while the pass is active.

Recommended sections:

- `# Doc Audit Ledger`
- `## Repo Doc Profile`
- `## Inventory`
- `## History Signals`
- `## Survival Justifications`
- `## Missing Canonical Homes`
- `## Canonical Home Decisions`
- `## Topic Map`
- `## Deletions`
- `## Fixes Applied`
- `## Final Doc Map`
- `## Status`

This file is scaffolding, not a shipped artifact.

## Discover

- Inventory every doc-shaped surface in the resolved scope.
- If the run started with no narrower context, inventory the repo docs surface first, then choose the strongest grounded docs-health slice for the current pass.
- In repo-scope `auto`, the next pass may widen or shift across the repo docs surface when discovery shows more grounded docs debt elsewhere.
- Record file, location, topic, likely freshness, and overlap notes.
- Flag point-in-time docs older than 30 days as presumptively stale unless later grounding proves a current-reader need.
- Resolve repo posture and record whether the standard public-repo baseline applies.
- Record clear grounded doc gaps where current readers would expect canonical evergreen guidance but do not have it.
- In `public OSS` repos, record each missing standard community doc as a real canonical-home gap, not an optional note.
- When staleness, datedness, or one-off status matters, inspect `git log` and identify the last meaningful content change.
- Record history evidence only where it changed the keep/delete judgment.

## Ground-truth

- For each topic, read the current code and current shipped behavior.
- Record contradictions across docs, code, and surviving behavior.
- Treat doc self-descriptions, folder placement, and freshness headers as untrusted claims until the code supports them.
- Identify the one best canonical home for the topic, or determine that the repo currently lacks a viable home.
- Record why the topic stays in an existing home or why it now deserves its own doc.
- Ask whether an old doc still serves a current reader need or is only preserving a point-in-time snapshot that git already remembers.
- For any point-in-time doc older than 30 days that survives, record the explicit code-grounded current-reader need in `## Survival Justifications`.
- Ask what a current reader still would not understand, trust, or be able to do if the surviving docs stayed as they are.

## Trim

- Before deleting a bounded batch of stale, duplicate, or obviously dated docs, stage those docs and create a backup git commit first.
- Stage only the docs in that delete batch, not unrelated dirty files elsewhere in the repo.
- If the backup commit cannot be created, stop instead of deleting.
- Delete stale or duplicate docs aggressively inside scope once the backup commit exists.
- Delete obviously time-bound docs once their durable truth has been folded forward and no clear lasting reader value remains.
- When a stale wrapper still contains durable truth, fold that truth into the best existing evergreen home and delete the wrapper in the same run.
- Retire obsolete working docs and completed plan/worklog residue once durable truth has been promoted.
- Repair references after every delete.

## Fix

- Correct stale surviving docs against code truth.
- Clarify confusing explanations, missing prerequisites, and misleading ordering when readers would otherwise fail or misunderstand the system.
- Expand the existing canonical home when it is the right place for grounded missing truth.
- Author a focused new canonical evergreen doc only when one of these is true:
  - the repo is `public OSS` and a standard community-doc home is missing
  - the canonical-home judgment says a differentiated evergreen topic should stand alone
- Do not promote a stale implementation-pass wrapper into a standalone evergreen doc just because it contains some useful details. If the topic fits an existing home, fold it there and delete the wrapper.
- Do not update freshness metadata unless the doc body was materially re-grounded against current code in the same pass.
- Front-load what readers actually need.
- Remove history and context that no longer helps.

## Organize

- Update the root README, docs index, or local README when surviving or newly created canonical docs need a discoverable entry.
- Keep naming and placement aligned with existing repo conventions.

## Completion bar

A pass is strong when:

- the repo doc profile is grounded
- the touched topics have one canonical home each
- stale duplicates are gone
- obviously dated docs without lasting reader value are gone or transformed in place
- point-in-time docs older than 30 days are gone unless `## Survival Justifications` records an explicit code-grounded current-reader need
- stale surviving docs are updated
- confusing docs that still matter are clarified
- grounded missing truth has been promoted into a canonical evergreen home
- no doc was made to look current through metadata-only freshness edits
- required public-repo baseline docs exist when the repo is `public OSS`
- broken references in touched scope are repaired
- durable truth was promoted before deletions
- `.doc-audit-ledger.md` is deleted before the run finishes clean, or kept only while an explicitly continuing multi-pass cleanup is still active

If those are not true yet, the pass should stop honestly with the next grounded move.
