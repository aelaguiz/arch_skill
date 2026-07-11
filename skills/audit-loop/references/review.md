# `review` Mode

## Goal

Run a new clean, docs-only audit verdict pass that decides whether the exhaustive map is complete, whether the current ranking is still truthful, whether a major unresolved risk front still justifies more work, and whether the latest editful pass actually survived the required post-change audit.

## Writes

- `_audit_ledger.md`
- root `.gitignore` when the ledger is missing and must be repaired

These are parent-owned writes. The critic does not write them. No product code
changes are allowed in `review`.

## Parent And Critic Boundary

- The parent creates or repairs the ledger, captures current git status and the
  relevant diff, and then starts a new clean same-host native critic by
  default. Codex uses `fork_turns: "none"`; Claude uses a clean named or custom
  subagent rather than a bare conversation fork or skill `context: fork`
  shorthand.
- Give the critic the ledger and exact repo paths. Use bounded or full
  inherited context only for a named dependency that exists solely in chat.
- Select the strongest read-only capability available and explicitly tell the
  critic not to edit or write any file, including the ledger. It may not create
  children or invoke delegation, consult, or review skills unless the parent
  assigned a bounded nested scope and budget.
- The critic returns a verdict recommendation, path-anchored evidence,
  coverage limits, and the next mapping tranche or risk front when relevant.
  The parent accounts for the return, compares current status and diff with the
  pre-dispatch state, spot-checks evidence, resolves conflicts, writes the
  ledger, chooses any accepted repair direction, and owns the final verdict.

## Procedure

1. The parent creates or repairs `_audit_ledger.md` and the `.gitignore` entry
   if they are missing, then captures current git status and the relevant diff.
2. Start the critic under the boundary above. The critic re-reads:
   - controller block
   - Phase 1 triage
   - open findings
   - test additions
   - post-change audit
   - decisions log
3. The critic inspects current repo state from its clean context:
   - changed files
   - relevant tests, build checks, or scanner output when needed
   - whether the exhaustive map is complete
   - whether the current or next front comes from the ranked map
   - whether the latest pass actually reduced the top open risk
   - whether the same risk front still has justified unresolved work
   - whether the latest pass used proof proportional to the front's consequence and blast radius
   - whether the latest editful pass completed and passed the post-change audit for safety, downstream consequences, elegance, and duplication
   - whether the fix introduced new duplicate logic, assertions, or fallback handling instead of converging on one truthful path
   - whether audit-loop-added or materially rewritten tests make the protected behavior, why it matters, and the expected user-visible or externally observable outcome clear enough to catch misunderstanding later
   - treat unrelated dirty or untracked files as ordinary context, not as an automatic blocker
4. The critic returns one recommendation plus evidence and coverage limits:
   - `CONTINUE` when a concrete worthwhile next mapping tranche or risk front remains
   - `CLEAN` when the map is complete, only fixed items or explicit `SKIP`s remain, and no credible major audit pass is justified
   - `BLOCKED` when the next move would be speculative, repeated, or stopped by a real blocker
5. The parent accounts for the critic, compares repository state with the
   pre-dispatch snapshot, and spot-checks the returned evidence before setting
   the controller block.
6. The parent updates `Last Review` and keeps the ledger truthful about why the
   decision was made.

## Verdict rules

### `CONTINUE`

Use only when:

- the exhaustive map is not complete and a concrete next mapping tranche exists, or a concrete next risk front exists
- the current or next front is still justified by the priority matrix
- the current front still has unresolved work or the next front clearly dominates the repo
- the latest editful pass still has unresolved post-change audit issues that should be repaired in the same risk story
- the latest pass did not leave key new verification ambiguous or underexplained
- the next pass would not merely repeat the last failed idea

`Next Area` is required. It may name an unfinished mapping tranche, risk front, or problem cluster, not just a tiny local file.

### `CLEAN`

Use only when:

- the highest-priority unresolved risk fronts have been fixed or explicitly skipped
- the exhaustive map is complete
- no credible `P0`, `P1`, or justified `P2` audit pass remains
- rescanning would likely just relitigate prior `SKIP` decisions
- the loop is not merely stopping because the next useful work touches a broader surface
- the latest editful pass passed the post-change audit for safety, downstream consequences, elegance, and duplication

`Stop Reason` should be blank.

### `BLOCKED`

Use when:

- the next move depends on missing access, tooling, or evidence
- the failing baseline or current repo state makes the next pass unsafe
- the next pass would rerun the same idea without a changed lever
- the ledger is too weak to continue honestly without first repairing the investigation
- the only honest next move would change an existing product, API, or behavior contract instead of fixing a bug inside it
- the remaining repair required by the post-change audit depends on missing access, tooling, or evidence rather than ordinary same-story cleanup
- the claimed risk reduction depends on new or materially rewritten tests whose intent is too unclear to trust

`Stop Reason` is required.

A dirty worktree by itself is not enough for `BLOCKED`. An incomplete map is also not enough for `BLOCKED`; use `CONTINUE` for unfinished mapping work. Use `BLOCKED` only when the current repo state directly conflicts with the next justified pass or makes verification unsafe.
