# `run` Mode

## Goal

Run one serious mapping or comment-hardening pass that leaves `_comment_ledger.md` more truthful and materially advances either the exhaustive repo map or the highest-impact unresolved explanation gap in the repo.

## Writes

- `_comment_ledger.md`
- root `.gitignore`
- code comments, docstrings, or doc comments when the pass reaches a justified explanation front
- deletion or repair of touched stale comments

No product behavior changes are allowed in `run`. If the truth would require a code fix or contract change, log that and stop or route to the owning skill.

## Pass shape

One `run` pass owns either:

- one unfinished mapping tranche, or
- one comment front chosen from the completed map

A comment front is the highest-priority unresolved explanation cluster where the work shares either:

- one critical-path story
- one shared contract or convention
- one canonical owner boundary

The pass may cross multiple files, modules, and tests when that is what it takes to complete the same mapping tranche or reduce the same misunderstanding risk honestly.

Unrelated dirty or untracked files are normal context, not a blocker. Leave them untouched unless they directly conflict with the current comment front or make verification unsafe.

Do not force the pass to stop after one edited comment when the same mapping tranche or comment front still has clearly justified work.

Do stop when the next move would require a genuinely different mapping tranche, explanation story, or verification basis.

## Procedure

1. Create or repair `_comment_ledger.md` and the `.gitignore` entry.
2. Refresh `Started` and `Last updated` dates as needed.
3. Build or refresh Phase 1 exhaustively:
   - enumerate shipped code surfaces from repo truth
   - enumerate the current proof surface from repo truth
   - enumerate the current explanatory surface from repo truth
   - record each surface's contract or invariant, downstream dependents, current proof, proof quality, current explanation, explanation quality, and consequence if it is misunderstood
   - record shared contracts, conventions, and gotchas plus the preferred comment owner site
   - assess current explanation accuracy, staleness risk, and missing signal
   - use churn, fragility markers, and repeated confusion points when they sharpen judgment
   - write map status, priorities, and explicit `SKIP` decisions
4. When the runtime supports delegation, use parallel read-only agents to gather disjoint mapping slices. Otherwise complete the same map sequentially.
5. If the map is incomplete, update `Next Area` with the next unfinished mapping tranche, update the ledger, and stop without edits.
6. Rank comment fronts from the completed map by consequence first, then sharedness, then explanation weakness or misleadingness, then confusion and staleness signals.
7. Choose the highest-priority unresolved comment front from that ranking.
8. Record the pre-edit proof plan for that front in Phase 1.
9. Read the implementation in that front before writing explanation. Read tests, callers, and nearby boundaries as needed to prove the comments will be truthful.
10. Log precise findings in Phase 2 with file anchors and finding type.
11. Add or repair the strongest justified explanation across that front:
   - canonical contract comment
   - convention comment
   - gotcha comment
   - stale comment rewrite or deletion
   - clarifying test comment
12. Verify:
   - run the smallest targeted signal that proves the explanation is truthful
   - run the broader relevant suite when that signal exists and is credible
   - make the proof depth proportional to the consequence and blast radius of the touched surfaces
   - reread the edited code to ensure the comments are concise, accurate, and not line-by-line narration
13. Update:
   - finding status
   - comment additions
   - `Last updated`
   - the map and ranking if the edits changed them materially
   - `Next Area` or `Stop Reason` if the next unfinished mapping tranche, unresolved comment front, or blocker is obvious
14. Stop only when further useful work would become a different mapping story, explanation story, or verification basis, not merely because another file or module is involved.

## Triage reminders

- An outcome-critical shared contract with weak explanation is usually more important than a noisier local helper.
- A misleading old docstring on a critical path is immediately worth fixing.
- A single canonical comment at the owner boundary is usually worth more than several local hints.
- An incomplete map is not good enough to justify a quick explanation pass.
- Low-risk, low-churn, already-well-explained code is a good `SKIP`.
- Unrelated dirty or untracked files do not justify stopping or downgrading the pass on their own.

## Verification rules

- Prefer behavior-level proof over assumption.
- Critical paths deserve at least one realistic signal that the comment is truthful.
- Higher-consequence surfaces deserve broader downstream proof than narrow utility comments.
- If the best evidence is a targeted test plus a broader existing suite, run both.
- If the repo has no credible automated signal for the truth being documented, say so plainly in the ledger.
