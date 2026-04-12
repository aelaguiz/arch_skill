# `review` Mode

## Goal

Run a fresh, docs-only automation verdict pass that decides whether a major unresolved real-app automation risk front still justifies more work, or whether the loop should stop clean or blocked.

## Writes

- `_audit_sim_ledger.md`
- root `.gitignore` when the ledger is missing and must be repaired

No product code changes are allowed in `review`.

## Procedure

1. Create or repair `_audit_sim_ledger.md` and the `.gitignore` entry if they are missing.
2. Re-read:
   - controller block
   - Phase 1 triage
   - open findings
   - automation additions
   - decisions log
3. Inspect current repo state from fresh context:
   - changed files
   - relevant automation files, runner output, build checks, or logs when needed
   - whether the latest pass actually reduced the top open automation risk
   - whether the same automation risk front still has justified unresolved work
   - whether the latest pass produced the required simulator or device signal through the sanctioned surface, using `mobile-sim` when the repo provides it
   - whether the sanctioned simulator or device surface is unavailable only because the current review context cannot inspect it cleanly, for example sandbox `EPERM`, host permission issues, or wrapper failures that are not yet evidence of app or harness breakage
   - whether a cross-platform front still needs Android confirmation before it can honestly be called done
   - treat unrelated dirty or untracked files as ordinary context, not as an automatic blocker
4. Set the controller block:
   - `CONTINUE` when a concrete worthwhile next automation risk front remains
   - `CLEAN` when only fixed items or explicit `SKIP`s remain and no credible major automation pass is justified
   - `BLOCKED` when the next move would be speculative, repeated, or stopped by a real blocker
5. Update `Last Review`.
6. Keep the ledger truthful about why the decision was made.

## Verdict rules

### `CONTINUE`

Use only when:

- a concrete next automation risk front exists
- that risk front is still justified by the priority matrix
- the current front still has unresolved work or the next front clearly dominates the app
- the next pass would not merely repeat the last failed idea

`Next Area` is required. It may name a real-app automation risk front or problem cluster, not just a tiny local file.

### `CLEAN`

Use only when:

- the highest-priority unresolved automation risk fronts have been fixed or explicitly skipped
- no credible `P0`, `P1`, or justified `P2` automation pass remains
- rescanning would likely just relitigate prior `SKIP` decisions
- the loop is not merely stopping because the next useful work touches a broader automation surface
- the latest front did not quietly degrade into Flutter unit or widget tests where simulator or device proof was required
- any cross-platform front that was iterated on iOS has a credible Android closeout when Android still matters for that story

`Stop Reason` should be blank.

### `BLOCKED`

Use when:

- the next move depends on missing access, tooling, or evidence
- the failing baseline or current repo state makes the next pass unsafe
- the next pass would rerun the same idea without a changed lever
- the ledger is too weak to continue honestly without first repairing the investigation
- the current front still requires simulator or device proof, but the sanctioned path could not be made to work after bounded recovery work, using `mobile-sim` when the repo provides it
- the remaining work would require inventing a parallel automation system instead of using the repo's existing surfaces

If the latest pass only has Flutter unit or widget evidence where the current front required simulator or device proof, do not mark `CLEAN`. Mark `BLOCKED` and name the simulator blocker plainly.
If the current review context cannot inspect the sanctioned simulator or device surface for review-only reasons, do not mark `BLOCKED` from that alone. Record live runtime state as `unknown` and base the verdict on the repo-local evidence you do have.

`Stop Reason` is required.

A dirty worktree by itself is not enough for `BLOCKED`. Use `BLOCKED` only when the current repo state directly conflicts with the next justified pass or makes verification unsafe.
