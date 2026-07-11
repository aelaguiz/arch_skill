# `review` Mode

## Goal

Run a new clean, docs-only automation verdict pass that decides whether the exhaustive map is complete, whether the current ranking is still truthful, whether a major unresolved real-app automation risk front still justifies more work, and whether the latest editful pass actually survived the required post-change audit.

## Writes

- `_audit_sim_ledger.md`
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
- Select the critic only after confirming that it inherits the sanctioned
  simulator or device capabilities required by `audit-loop-sim`. If the host
  cannot confirm that inheritance, keep the review with the authorized parent
  and return live state as `unknown`; do not use an external transport as an
  unauthorized capability bypass.
- The critic returns a verdict recommendation, path-anchored evidence,
  coverage limits, and the next mapping tranche or risk front when relevant.
  The parent accounts for the return, compares current status and diff with the
  pre-dispatch state, spot-checks evidence, resolves conflicts, writes the
  ledger, chooses any accepted repair direction, and owns the final verdict.

## Procedure

1. The parent creates or repairs `_audit_sim_ledger.md` and the `.gitignore`
   entry if they are missing, then captures current git status and the relevant
   diff.
2. Start the critic under the boundary above. The critic re-reads:
   - controller block
   - Phase 1 triage
   - open findings
   - automation additions
   - post-change audit
   - decisions log
3. The critic inspects current repo state from its clean context:
   - changed files
   - relevant automation files, runner output, build checks, or logs when needed
   - whether the exhaustive map is complete
   - whether the current or next front comes from the ranked map
   - whether the latest pass actually reduced the top open automation risk
   - whether the same automation risk front still has justified unresolved work
   - whether the latest pass used proof proportional to the front's consequence and blast radius
   - whether the latest editful pass completed and passed the post-change audit for safety, downstream consequences, elegance, and duplication
   - whether the latest pass produced the required simulator or device signal through the sanctioned surface, using `mobile-sim` when the repo provides it
   - whether the fix introduced new duplicate product logic, lane behavior, harness steps, or fallback handling instead of converging on one truthful path
   - whether the sanctioned simulator or device surface is unavailable only because the current review context cannot inspect it cleanly, for example sandbox `EPERM`, host permission issues, or wrapper failures that are not yet evidence of app or harness breakage
   - whether a cross-platform front still needs Android confirmation before it can honestly be called done
   - treat unrelated dirty or untracked files as ordinary context, not as an automatic blocker
4. The critic returns one recommendation plus evidence and coverage limits:
   - `CONTINUE` when a concrete worthwhile next mapping tranche or automation risk front remains
   - `CLEAN` when the map is complete, only fixed items or explicit `SKIP`s remain, and no credible major automation pass is justified
   - `BLOCKED` when the next move would be speculative, repeated, or stopped by a real blocker
5. The parent accounts for the critic, compares repository state with the
   pre-dispatch snapshot, and spot-checks the returned evidence before setting
   the controller block.
6. The parent updates `Last Review` and keeps the ledger truthful about why the
   decision was made.

## Verdict rules

### `CONTINUE`

Use only when:

- the exhaustive map is not complete and a concrete next mapping tranche exists, or a concrete next automation risk front exists
- the current or next front is still justified by the priority matrix
- the current front still has unresolved work or the next front clearly dominates the app
- the latest editful pass still has unresolved post-change audit issues that should be repaired in the same automation story
- the next pass would not merely repeat the last failed idea

`Next Area` is required. It may name an unfinished mapping tranche, real-app automation risk front, or problem cluster, not just a tiny local file.

### `CLEAN`

Use only when:

- the highest-priority unresolved automation risk fronts have been fixed or explicitly skipped
- the exhaustive map is complete
- no credible `P0`, `P1`, or justified `P2` automation pass remains
- rescanning would likely just relitigate prior `SKIP` decisions
- the loop is not merely stopping because the next useful work touches a broader automation surface
- the latest front did not quietly degrade into Flutter unit or widget tests where simulator or device proof was required
- any cross-platform front that was iterated on iOS has a credible Android closeout when Android still matters for that story
- the latest editful pass passed the post-change audit for safety, downstream consequences, elegance, and duplication

`Stop Reason` should be blank.

### `BLOCKED`

Use when:

- the next move depends on missing access, tooling, or evidence
- the failing baseline or current repo state makes the next pass unsafe
- the next pass would rerun the same idea without a changed lever
- the ledger is too weak to continue honestly without first repairing the investigation
- the only honest next move would change an existing product, journey, or automation contract instead of fixing a bug inside it
- the remaining repair required by the post-change audit depends on missing access, tooling, or evidence rather than ordinary same-story cleanup
- the current front still requires simulator or device proof, but the sanctioned path could not be made to work after bounded recovery work, using `mobile-sim` when the repo provides it
- the remaining work would require inventing a parallel automation system instead of using the repo's existing surfaces

If the latest pass only has Flutter unit or widget evidence where the current front required simulator or device proof, do not mark `CLEAN`. Mark `BLOCKED` and name the simulator blocker plainly.
If the current review context cannot inspect the sanctioned simulator or device surface for review-only reasons, do not mark `BLOCKED` from that alone. Record live runtime state as `unknown` and base the verdict on the repo-local evidence you do have.

`Stop Reason` is required.

A dirty worktree by itself is not enough for `BLOCKED`. An incomplete map is also not enough for `BLOCKED`; use `CONTINUE` for unfinished mapping work. Use `BLOCKED` only when the current repo state directly conflicts with the next justified pass or makes verification unsafe.
