# Review Mode

Fresh docs-only audit verdict pass that decides whether the exhaustive map is complete, whether the current ranking is still truthful, whether a major unresolved risk front still justifies more work, and whether the latest editful pass actually survived the required post-change audit.

## Goal

Run a fresh, docs-only audit verdict pass that decides whether the exhaustive map is complete, whether the current ranking is still truthful, whether a major unresolved risk front still justifies more work, and whether the latest editful pass actually survived the required post-change audit.

## Writes

- `_audit_ledger.md`
- Root `.gitignore` when the ledger is missing and must be repaired

No product code changes are allowed in `review`.

## Procedure

1. Create or repair `_audit_ledger.md` and the `.gitignore` entry if they are missing.
2. Re-read: controller block, Phase 1 triage, open findings, test additions, post-change audit, decisions log.
3. Inspect current repo state from fresh context: changed files, relevant tests/build checks/scanner output when needed, whether the exhaustive map is complete, whether the current or next front comes from the ranked map, whether the latest pass actually reduced the top open risk, whether the same risk front still has justified unresolved work, whether the latest pass used proof proportional to the front's consequence and blast radius, whether the latest editful pass completed and passed the post-change audit for safety/downstream consequences/elegance/duplication, whether the fix introduced new duplicate logic/assertions/fallback handling instead of converging on one truthful path, whether audit-loop-added or materially rewritten tests make the protected behavior and expected outcome clear enough to catch misunderstanding later. Treat unrelated dirty or untracked files as ordinary context, not as an automatic blocker.
4. Set the controller block: `CONTINUE` when a concrete worthwhile next mapping tranche or risk front remains; `CLEAN` when the map is complete, only fixed items or explicit `SKIP`s remain, and no credible major audit pass is justified; `BLOCKED` when the next move would be speculative, repeated, or stopped by a real blocker.
5. Update `Last Review`.
6. Keep the ledger truthful about why the decision was made.

## Verdict `CONTINUE`

Use only when:

- The exhaustive map is not complete and a concrete next mapping tranche exists, or a concrete next risk front exists.
- The current or next front is still justified by the priority matrix.
- The current front still has unresolved work or the next front clearly dominates the repo.
- The latest editful pass still has unresolved post-change audit issues that should be repaired in the same risk story.
- The latest pass did not leave key new verification ambiguous or underexplained.
- The next pass would not merely repeat the last failed idea.

`Next Area` is required. It may name an unfinished mapping tranche, risk front, or problem cluster, not just a tiny local file.

## Verdict `CLEAN`

Use only when:

- The highest-priority unresolved risk fronts have been fixed or explicitly skipped.
- The exhaustive map is complete.
- No credible `P0`, `P1`, or justified `P2` audit pass remains.
- Rescanning would likely just relitigate prior `SKIP` decisions.
- The loop is not merely stopping because the next useful work touches a broader surface.
- The latest editful pass passed the post-change audit for safety, downstream consequences, elegance, and duplication.

`Stop Reason` should be blank.

## Verdict `BLOCKED`

Use when:

- The next move depends on missing access, tooling, or evidence.
- The failing baseline or current repo state makes the next pass unsafe.
- The next pass would rerun the same idea without a changed lever.
- The ledger is too weak to continue honestly without first repairing the investigation.
- The only honest next move would change an existing product, API, or behavior contract instead of fixing a bug inside it.
- The remaining repair required by the post-change audit depends on missing access, tooling, or evidence rather than ordinary same-story cleanup.
- The claimed risk reduction depends on new or materially rewritten tests whose intent is too unclear to trust.

`Stop Reason` is required.
A dirty worktree by itself is not enough for `BLOCKED`. An incomplete map is also not enough for `BLOCKED`; use `CONTINUE` for unfinished mapping work. Use `BLOCKED` only when the current repo state directly conflicts with the next justified pass or makes verification unsafe.
