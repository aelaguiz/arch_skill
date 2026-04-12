# `run` Mode

## Goal

Run one serious automation audit or fix pass that leaves `_audit_sim_ledger.md` more truthful and materially reduces the biggest unresolved real-app automation risk in the repo.

## Writes

- `_audit_sim_ledger.md`
- root `.gitignore`
- product code when the pass reaches a justified same-story fix
- automation, harness, fixtures, or native glue only when they protect meaningful behavior

## Pass shape

One `run` pass owns one automation risk front. A risk front is the highest-priority unresolved real-app problem cluster where the findings share either:

- one critical user-journey story
- one failure mode
- one verification surface

The pass may cross product files, modules, integration tests, harness helpers, fixtures, or native glue when that is what it takes to reduce the same automation risk front honestly.

Unrelated dirty or untracked files are normal context, not a blocker. Leave them untouched unless they directly conflict with the current automation risk front or make verification unsafe.

Do not force the pass to stop after one finding or one patch when the same risk front still has clearly justified work.

Do stop when the next move would require a genuinely different journey story, a fresh audit cycle, or a different verification basis.

## Procedure

1. Create or repair `_audit_sim_ledger.md` and the `.gitignore` entry.
2. Refresh `Started` and `Last updated` dates as needed.
3. Build or refresh Phase 1:
   - identify primary journeys and the app surfaces they depend on
   - gather current real-app automation signal
   - gather platform truth and cross-platform obligations
   - measure churn when it sharpens judgment
   - note obvious flow, harness, fixture, or native ingress gaps when available
   - write priorities and explicit `SKIP` decisions
4. Choose the highest-priority unresolved automation risk front from Phase 1.
5. Read the product implementation and the current automation in that risk front before patching either.
6. Log precise findings in Phase 2 with file anchors and finding type.
7. Decide what durable automation signal and same-story product fix is missing.
8. Fix the strongest justified work across that risk front:
   - end-to-end automation addition
   - existing lane repair or de-flake
   - harness, fixture, QA-command, or native-ingress hardening
   - same-story product bug fix exposed by the new automation
9. Verify:
   - run the smallest targeted real-app signal that proves the fix
   - when the repo provides `mobile-sim`, use `mobile-sim` for simulator or device control
   - if the sanctioned simulator or device surface fails before app signal, do one bounded recovery step before calling the front blocked
   - use one bounded host-health recovery when the sanctioned surface lacks the needed repair command, for example simulator toolchain selection, current live-target re-bootstrap, or emulator cache trimming
   - iterate on iOS first when iOS is available and the risk is not platform-specific
   - before calling a cross-platform front done, run one Android confirmation on the same journey
10. Update:
   - finding status
   - automation additions
   - `Last updated`
   - `Next Area` or `Stop Reason` if the next unresolved automation risk front or blocker is obvious
11. Stop only when further useful work would become a different automation story, not merely because another file, module, or test surface is involved.

## Triage reminders

- A primary-path or monetization or onboarding journey with weak real-app signal is usually more important than a weird settings edge case.
- A tiny isolated test tweak does not win if the same user-journey failure mode still has obvious unresolved work.
- Existing repo-native automation or harness surfaces are usually worth extending before building a new lane family.
- Low-risk, low-churn, already-protected behavior is a good `SKIP`.
- Unrelated dirty or untracked files do not justify stopping or downgrading the pass on their own.
- If a current live target died, re-bootstrap a current live target before treating the miss as app breakage.
- If repeated cloud runs fail with the same provider-side infrastructure error and no meaningful app signal, stop and record the provider blocker instead of queueing more identical reruns.

## Verification rules

- Prefer behavior-level verification over implementation-detail checks.
- Primary journeys deserve at least one realistic end-to-end signal where feasible.
- Do not substitute Flutter unit or widget tests when the current front requires simulator or device proof; spend real effort on the sanctioned simulator path first, then stop blocked if it still cannot produce the required signal.
- If the best evidence is a targeted real-app lane plus a broader existing suite, run both.
- If the repo has no credible automated signal for the fix, say so plainly in the ledger.
- If the current review or run context cannot inspect the sanctioned simulator or device surface cleanly, record that state as `unknown` unless you have stronger evidence of a real blocker.
