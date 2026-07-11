# `review` Mode

## Goal

Run a new clean, docs-only comment-loop verdict pass that decides whether the exhaustive map is complete, whether the current ranking is still truthful, and whether a major unresolved explanation front still justifies more work.

## Writes

- `_comment_ledger.md`
- root `.gitignore` when the ledger is missing and must be repaired

These are parent-owned writes. The critic does not write them. No code comments
or product code changes are allowed in `review`.

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
  coverage limits, and the next mapping tranche or comment front when
  relevant. The parent accounts for the return, compares current status and
  diff with the pre-dispatch state, spot-checks evidence, resolves conflicts,
  writes the ledger, chooses any accepted repair direction, and owns the final
  verdict.

## Procedure

1. The parent creates or repairs `_comment_ledger.md` and the `.gitignore`
   entry if they are missing, then captures current git status and the relevant
   diff.
2. Start the critic under the boundary above. The critic re-reads:
   - controller block
   - Phase 1 triage
   - open findings
   - comment additions
   - decisions log
3. The critic inspects current repo state from its clean context:
   - changed files
   - relevant tests, build checks, or scanner output when needed
   - whether the exhaustive map is complete
   - whether the current or next front comes from the ranked map
   - whether the latest pass actually reduced the top explanation risk
   - whether the same front still has justified unresolved work
   - whether the latest pass used proof proportional to the front's consequence and blast radius
   - whether the latest comments are accurate, concise, and placed at the strongest owner boundary
   - whether touched stale comments were actually removed or repaired
   - treat unrelated dirty or untracked files as ordinary context, not as an automatic blocker
4. The critic returns one recommendation plus evidence and coverage limits:
   - `CONTINUE` when a concrete worthwhile next mapping tranche or comment front remains
   - `CLEAN` when the map is complete, only fixed items or explicit `SKIP`s remain, and no credible major explanation pass is justified
   - `BLOCKED` when the next move would be speculative, repeated, or stopped by a real blocker
5. The parent accounts for the critic, compares repository state with the
   pre-dispatch snapshot, and spot-checks the returned evidence before setting
   the controller block.
6. The parent updates `Last Review` and keeps the ledger truthful about why the
   decision was made.

## Verdict rules

### `CONTINUE`

Use only when:

- the exhaustive map is not complete and a concrete next mapping tranche exists, or a concrete next comment front exists
- the current or next front is still justified by the priority matrix
- the current front still has unresolved work or the next front clearly dominates the repo
- the latest pass did not leave key explanation ambiguous or underproved
- the next pass would not merely repeat the last failed idea

`Next Area` is required. It may name an unfinished mapping tranche, comment front, or problem cluster, not just a tiny local file.

### `CLEAN`

Use only when:

- the highest-priority unresolved explanation fronts have been fixed or explicitly skipped
- the exhaustive map is complete
- no credible `P0`, `P1`, or justified `P2` comment pass remains
- rescanning would likely just relitigate prior `SKIP` decisions
- the loop is not merely stopping because the next useful work touches a broader surface

`Stop Reason` should be blank.

### `BLOCKED`

Use when:

- the next move depends on missing access, tooling, or evidence
- the next move would rerun the same idea without a changed lever
- the ledger is too weak to continue honestly without first repairing the investigation
- the only honest next move would fix buggy behavior, clarify an unsettled contract, or do a broader docs rewrite instead of writing comments
- the highest-priority comment front belongs to generated or otherwise non-authoritative surfaces that cannot be safely edited
- the claimed explanation improvement depends on comments that are still too speculative or stale to trust

`Stop Reason` is required.

A dirty worktree by itself is not enough for `BLOCKED`. An incomplete map is also not enough for `BLOCKED`; use `CONTINUE` for unfinished mapping work. Use `BLOCKED` only when the current repo state directly conflicts with the next justified pass or makes truthful explanation unsafe.
