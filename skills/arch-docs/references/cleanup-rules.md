# Cleanup Rules

The bias is delete stale truth and promote durable truth, not preserve every document.

## Non-authoritative signals

- Do not trust what a doc calls itself until current code and shipped behavior support it.
- Folder names such as `docs/living` and labels such as `Status: LIVING`, `Last verified`, `Classification`, or similar freshness markers are claims to verify, not evidence that the doc should survive.
- Do not keep or refresh a doc just because it sits in the repo's "live" area or because a status header says it is current.

## Promote or author durable truth

- Rewrite or expand the best existing canonical doc first when it can honestly carry the topic.
- In `public OSS` repos, create the standard community-doc homes when they are missing.
- Prefer folding durable truth into an existing evergreen home over preserving a stale wrapper.
- Create a focused new evergreen doc only when the canonical-home judgment says the topic should stand alone, current readers would seek it directly, and the existing README, docs index, or module docs cannot carry it cleanly.
- Good additions are grounded, current, canonical, and clearly useful to current readers.
- Bad additions are speculative, aspirational, duplicate, or taxonomy-first.
- Do not hide `LICENSE*`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, or `SUPPORT.md` inside another doc when the repo is `public OSS` and those homes are missing.
- If equivalent truth already exists in a weaker home, normalize it into the conventional canonical doc before deleting the old wrapper.
- Do not delete the old wrapper until the durable truth actually lives in the surviving canonical home.

## Commit, then delete

- TEMP, DRAFT, WIP, OLD, or DEPRECATED files whose subject is already shipped, removed, or superseded
- duplicate docs when another doc covers the same topic better
- docs for features or systems that no longer exist
- empty or near-empty stubs
- obsolete working docs after their durable truth is promoted elsewhere

Before deleting a bounded batch of these docs:

- stage the docs in that delete batch
- create a backup git commit first
- do not stage unrelated dirty files elsewhere in the repo
- if the commit cannot be created, stop instead of deleting

## Consolidate then delete

- Merge the good parts into the canonical surviving doc.
- Delete the weaker duplicate in the same run.
- Do not leave a live redirect stub that only says "see other file." Those rot quickly.

## Plan and worklog retirement

- Treat plan docs, worklogs, investigation notes, and similar working artifacts as temporary unless they are transformed into the one canonical evergreen doc.
- Mine durable truth into evergreen docs first.
- If the plan doc can be transformed in place into the one clean evergreen doc, do that and remove the arch scaffolding.
- Otherwise fold the durable truth into better homes and delete the obsolete working docs.

## Dated doc retirement

- Treat launch notes, rollout docs, migration one-offs, completed audits, temporary investigations, incident-era notes, and similar point-in-time artifacts as disposable unless current readers still need them.
- In this repo family, point-in-time docs older than 30 days are presumed stale.
- Survival after 30 days requires an explicit code-grounded current-reader need, not a doc label, folder location, or freshness header.
- Use `git log` when a doc looks time-bound or suspiciously untouched and the keep/delete call is unclear.
- Look for the last meaningful content change, not moves, renames, formatting churn, or mechanical edits.
- Keep the durable truth, not the moment-in-time wrapper. Fold forward what still matters, then delete the rest.
- Most aged implementation-pass docs should fold into an existing evergreen home and disappear in the same run rather than being promoted into standalone evergreen docs.
- Do not keep a doc just because it once mattered or because it feels safer to preserve it. Git is the archive.

## Freshness laundering ban

- Do not make a dead doc look current by editing metadata alone.
- `Status`, `Last verified`, `Last updated`, `Classification`, and similar freshness fields may change only when the body was materially re-grounded against current code in the same pass.
- Metadata-only freshness edits are a docs-cleanup failure.

## Reference repair

- After every delete or move, grep the repo for references to the deleted path.
- After every substantive rewrite or new canonical doc, repair or add the references readers will actually use.
- Fix or remove broken references in the same pass.
- Broken internal links are a docs-cleanup failure, not optional polish.

## Concision rules

- Remove history that is no longer needed to understand the current state.
- Remove hedging and filler.
- Remove examples that no longer run against the current codebase.
- Do not let age alone override clear current-reader value, but do use the 30-day presumption aggressively.
- If a sentence cannot be grounded confidently, delete it instead of keeping an aspirational guess.

## Ledger rule

- Use `.doc-audit-ledger.md` as temporary scaffolding only.
- It should include:
  - repo doc profile
  - inventory
  - missing canonical homes
  - canonical home decisions
  - topic map
  - deletions
  - fixes applied
  - final doc map while the pass is active
- Delete the ledger before the cleanup is declared complete.
