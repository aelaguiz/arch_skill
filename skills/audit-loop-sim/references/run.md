# `run` Mode

## Goal

Run one serious mapping, automation audit, or fix pass that leaves `_audit_sim_ledger.md` more truthful and materially advances either the exhaustive app map or the biggest unresolved real-app automation risk in the repo. Editful passes are not done until the resulting diff passes a post-change audit for safety, downstream consequences, elegance, and duplication.

## Writes

- `_audit_sim_ledger.md`
- root `.gitignore`
- product code when the pass reaches a justified same-story fix
- automation, harness, fixtures, or native glue only when they protect meaningful behavior

## Pass shape

One `run` pass owns either:

- one unfinished mapping tranche, or
- one automation risk front chosen from the completed map

A risk front is the highest-priority unresolved real-app problem cluster where the findings share either:

- one critical user-journey story
- one failure mode
- one verification surface

The pass may cross product files, modules, integration tests, harness helpers, fixtures, or native glue when that is what it takes to complete the same mapping tranche or reduce the same automation risk front honestly.

Unrelated dirty or untracked files are normal context, not a blocker. Leave them untouched unless they directly conflict with the current automation risk front or make verification unsafe.

Do not force the pass to stop after one finding or one patch when the same mapping tranche or risk front still has clearly justified work.

Do stop when the next move would require a genuinely different mapping tranche, journey story, audit cycle, or verification basis.

## Mapping child contract

The parent captures current git status and the relevant diff before mapping
fanout. Each child receives one non-overlapping journey, app, harness, or
platform family, exact repo and ledger paths, and a read-only brief. Start it
as a new clean same-host native child: Codex uses `fork_turns: "none"`, and
Claude uses a clean named or custom subagent rather than a bare conversation
fork or skill `context: fork` shorthand. Use inherited chat context only for a
named chat-only dependency.

Use the strongest read-only capability the host exposes and still say: do not
edit or write files, including `_audit_sim_ledger.md`; do not create children
or invoke delegation, consult, or review skills unless the parent explicitly
assigned a bounded nested scope and budget. Require the return to name files,
journeys, and harness paths read, mapped contracts and platform obligations,
current real-app proof and gaps, candidate risk fronts, coverage limits, and
collision risks. Dispatch the child only after confirming it inherits the
sanctioned simulator or device capabilities required by `audit-loop-sim`.
Otherwise keep the slice with the authorized parent or complete it
sequentially and return live state as `unknown`; external transport is not a
capability bypass. The parent waits for and accounts for every slice, compares
current status and diff with the pre-dispatch state, reconciles overlap, and
alone writes accepted evidence into the ledger.

## Procedure

1. Create or repair `_audit_sim_ledger.md` and the `.gitignore` entry.
2. Refresh `Started` and `Last updated` dates as needed.
3. Build or refresh Phase 1 exhaustively:
   - enumerate app surfaces, user journeys, and the current automation surface from repo truth
   - record each journey or surface's contract or expected outcome, consequence if it is wrong, and current real-app proof
   - record cross-platform obligations and platform ingress when they matter
   - assess proof quality, flake risk, harness drift, and missing signal
   - use churn and fragility signals when they sharpen judgment
   - write map status, priorities, and explicit `SKIP` decisions
4. When independent surface families make delegation worthwhile, gather them
   with the bounded mapping-child contract above. Otherwise complete the same
   map sequentially.
5. If the map is incomplete, update `Next Area` with the next unfinished mapping tranche, update the ledger, and stop without edits.
6. Rank automation risk fronts from the completed map by consequence first, then proof weakness, then fragility.
7. Choose the highest-priority unresolved automation risk front from that ranking.
8. Record the pre-edit proof plan and post-change audit focus for that front in Phase 1.
9. Read the product implementation and the current automation in that risk front before patching either.
10. Log precise findings in Phase 2 with file anchors and finding type.
11. Decide what durable automation signal and same-story product fix is missing.
12. Fix the strongest justified work across that risk front:
   - end-to-end automation addition
   - existing lane repair or de-flake
   - harness, fixture, QA-command, or native-ingress hardening
   - same-story product bug fix exposed by the new automation
13. Verify the initial fix:
   - run the smallest targeted real-app signal that proves the fix
   - when the repo provides `mobile-sim`, use `mobile-sim` for simulator or device control
   - if the sanctioned simulator or device surface fails before app signal, do one bounded recovery step before calling the front blocked
   - use one bounded host-health recovery when the sanctioned surface lacks the needed repair command, for example simulator toolchain selection, current live-target re-bootstrap, or emulator cache trimming
   - iterate on iOS first when iOS is available and the risk is not platform-specific
   - before calling a cross-platform front done, run one Android confirmation on the same journey
   - make the proof depth proportional to the consequence and blast radius of the touched journeys or surfaces
14. Audit the resulting diff and touched surfaces:
   - `SAFETY`: contracts, invariants, edge handling, and blast-radius containment still hold
   - `DOWNSTREAM`: callers, dependents, shared helpers, platform obligations, and proof surfaces do not have unaddressed fallout
   - `ELEGANCE`: the fix is coherent rather than patchy, brittle, or obviously awkward
   - `DUPLICATION`: no new duplicate product logic, lane behavior, harness steps, or fallback handling was introduced
15. If the post-change audit finds a problem, repair it in the same pass:
   - keep the repair inside the same automation risk front and existing contract
   - allow broader same-story cleanup only when that is the cleanest way to remove the new fragility or duplication
   - re-run the targeted and broader proof that the repair affects
16. Update:
   - finding status
   - automation additions
   - post-change audit status
   - `Last updated`
   - the map and ranking if the fix changed them materially
   - `Next Area` or `Stop Reason` if the next unfinished mapping tranche, unresolved automation risk front, or blocker is obvious
17. Stop only when further useful work would become a different mapping story, automation story, or verification basis, not merely because another file, module, or test surface is involved.

## Triage reminders

- A primary-path or monetization or onboarding journey with weak real-app signal is usually more important than a weird settings edge case.
- A tiny isolated test tweak does not win if the same user-journey failure mode still has obvious unresolved work.
- An incomplete map is not good enough to justify a quick lane tweak.
- Existing repo-native automation or harness surfaces are usually worth extending before building a new lane family.
- A quick fix that creates a second copy of the same journey logic or harness behavior loses, even if the first lane goes green.
- Low-risk, low-churn, already-protected behavior is a good `SKIP`.
- Unrelated dirty or untracked files do not justify stopping or downgrading the pass on their own.
- If a current live target died, re-bootstrap a current live target before treating the miss as app breakage.
- If repeated cloud runs fail with the same provider-side infrastructure error and no meaningful app signal, stop and record the provider blocker instead of queueing more identical reruns.

## Verification rules

- Prefer behavior-level verification over implementation-detail checks.
- Primary journeys deserve at least one realistic end-to-end signal where feasible.
- Higher-consequence journeys and surfaces deserve broader downstream real-app proof than narrow harness fixes.
- Do not substitute Flutter unit or widget tests when the current front requires simulator or device proof; spend real effort on the sanctioned simulator path first, then stop blocked if it still cannot produce the required signal.
- If the best evidence is a targeted real-app lane plus a broader existing suite, run both.
- Every editful pass also needs the post-change audit. Passing lanes do not waive that requirement.
- If the repo has no credible automated signal for the fix, say so plainly in the ledger.
- If the current review or run context cannot inspect the sanctioned simulator or device surface cleanly, record that state as `unknown` unless you have stronger evidence of a real blocker.
