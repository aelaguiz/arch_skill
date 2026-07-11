# `run` Mode

## Goal

Run one serious mapping, audit, or fix pass that leaves `_audit_ledger.md` more truthful and materially advances either the exhaustive repo map or the biggest unresolved risk in the repo. Editful passes are not done until the resulting diff passes a post-change audit for safety, downstream consequences, elegance, and duplication.

## Writes

- `_audit_ledger.md`
- root `.gitignore`
- product code when the pass reaches a justified fix
- tests only when they protect meaningful behavior
- comments in audit-loop-added or materially rewritten tests when needed to explain the why and expected experience or outcome

## Pass shape

One `run` pass owns either:

- one unfinished mapping tranche, or
- one risk front chosen from the completed map

A risk front is the highest-priority unresolved problem cluster where the findings share either:

- one critical-path story
- one failure mode
- one verification surface

The pass may cross multiple files, modules, or tests when that is what it takes to complete the same mapping tranche or reduce the same risk front honestly.

Unrelated dirty or untracked files are normal context, not a blocker. Leave them untouched unless they directly conflict with the current risk front or make verification unsafe.

Do not force the pass to stop after one finding or one patch when the same mapping tranche or risk front still has clearly justified work.

Do stop when the next move would require a genuinely different mapping tranche, risk story, audit cycle, or verification basis.

## Mapping child contract

The parent captures current git status and the relevant diff before mapping
fanout. Each child receives one non-overlapping surface family, exact repo and
ledger paths, and a read-only brief. Start it as a new clean same-host native
child: Codex uses `fork_turns: "none"`, and Claude uses a clean named or custom
subagent rather than a bare conversation fork or skill `context: fork`
shorthand. Use inherited chat context only for a named chat-only dependency.

Use the strongest read-only capability the host exposes and still say: do not
edit or write files, including `_audit_ledger.md`; do not create children or
invoke delegation, consult, or review skills unless the parent explicitly
assigned a bounded nested scope and budget. Require the return to name files
and symbols read, mapped contracts and dependents, current proof and gaps,
candidate risk fronts, coverage limits, and collision risks. The parent waits
for and accounts for every slice, compares current status and diff with the
pre-dispatch state, reconciles overlap, and alone writes accepted evidence into
the ledger.

## Procedure

1. Create or repair `_audit_ledger.md` and the `.gitignore` entry.
2. Refresh `Started` and `Last updated` dates as needed.
3. Build or refresh Phase 1 exhaustively:
   - enumerate shipped code surfaces from repo truth
   - enumerate the current proof surface from repo truth
   - record each surface's contract or invariant, downstream dependents, and consequence if it is wrong
   - assess current proof quality and missing signal
   - use churn, dead-code signals, duplication signals, and explicit fragility markers when they sharpen judgment
   - write map status, priorities, and explicit `SKIP` decisions
4. When independent surface families make delegation worthwhile, gather them
   with the bounded mapping-child contract above. Otherwise complete the same
   map sequentially.
5. If the map is incomplete, update `Next Area` with the next unfinished mapping tranche, update the ledger, and stop without edits.
6. Rank risk fronts from the completed map by consequence first, then proof weakness, then fragility.
7. Choose the highest-priority unresolved risk front from that ranking.
8. Record the pre-edit proof plan and post-change audit focus for that front in Phase 1.
9. Read the implementation in that risk front before reading its tests.
10. Log precise findings in Phase 2 with file anchors and finding type.
11. Read the existing tests and decide what verification is missing. If the pass adds or materially rewrites a test, leave comments in the test code that explain why the behavior matters and what correct user-visible or externally observable outcome should happen.
12. Fix the strongest justified work across that risk front:
   - bug fix
   - dead-code deletion
   - duplication extraction
   - high-value test addition
13. Verify the initial fix:
   - run the smallest targeted signal that proves the fix
   - run the broader relevant suite when that signal exists and is credible
   - make the proof depth proportional to the consequence and blast radius of the touched surfaces
14. Audit the resulting diff and touched surfaces:
   - `SAFETY`: contracts, invariants, edge handling, and blast-radius containment still hold
   - `DOWNSTREAM`: callers, dependents, shared helpers, and proof surfaces do not have unaddressed fallout
   - `ELEGANCE`: the fix is coherent rather than patchy, brittle, or obviously awkward
   - `DUPLICATION`: no new duplicate logic, assertions, or fallback handling was introduced
15. If the post-change audit finds a problem, repair it in the same pass:
   - keep the repair inside the same risk front and existing contract
   - allow broader same-story cleanup only when that is the cleanest way to remove the new fragility or duplication
   - re-run the targeted and broader proof that the repair affects
16. Update:
   - finding status
   - test additions
   - post-change audit status
   - `Last updated`
   - the map and ranking if the fix changed them materially
   - `Next Area` or `Stop Reason` if the next unfinished mapping tranche, unresolved risk front, or blocker is obvious
17. Stop only when further useful work would become a different mapping story, audit story, or verification basis, not merely because another file or module is involved.

## Triage reminders

- A consequence-heavy surface with weak proof is usually more important than a noisier utility.
- Dead code on a critical path is immediately worth deleting.
- Duplication on a critical path is immediately worth consolidating.
- A tiny isolated fix does not win if the same critical-path failure mode still has obvious unresolved work.
- An incomplete map is not good enough to justify a quick patch.
- A quick fix that creates a second copy of the logic loses, even if the first test pass is green.
- Low-risk, low-churn, already-tested code is a good `SKIP`.
- Unrelated dirty or untracked files do not justify stopping or downgrading the pass on their own.

## Verification rules

- Prefer behavior-level verification over implementation-detail checks.
- Critical paths deserve at least one realistic integration signal where feasible.
- Higher-consequence surfaces deserve broader downstream proof than narrow utility fixes.
- If the best evidence is a targeted test plus a broader existing suite, run both.
- Every editful pass also needs the post-change audit. Passing tests do not waive that requirement.
- When you add or materially rewrite a test, make the intent locally clear in the test code itself. Do not rely on the ledger alone to carry the why or the expected experience or outcome.
- If the repo has no credible automated signal for the fix, say so plainly in the ledger.
