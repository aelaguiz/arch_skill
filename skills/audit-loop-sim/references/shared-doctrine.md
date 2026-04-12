# Audit Loop Sim Shared Doctrine

## Philosophy

- Real app first. The job is to close the biggest gaps in the automation that catches bugs unit and widget tests miss.
- Audit-loop-sim exists to reduce the biggest real-app automation risks, not to harvest easy wins.
- Primary-path, onboarding, auth or session restore, monetization, core content progression, offline state, and platform ingress matter more than polishing a safe corner of settings when the evidence supports that.
- Prefer durable automation over manual QA recipes.
- Existing repo-native automation and simulator or device surfaces come first. In repos that provide `mobile-sim`, use `mobile-sim` for simulator or device control instead of inventing a parallel runner, lane family, or harness story.
- Tests exist to protect meaningful behavior. Coverage is a trailing indicator, not the product.
- Leave the app and automation surface stronger than you found them when the evidence supports a fix.

## Triage order

1. Identify 5-10 primary user journeys first.
2. Read the existing automation SSOT, flow registry, and sanctioned simulator or device surface.
3. Measure current real-app signal on those journeys.
4. Measure recent churn when it sharpens judgment.
5. Scan for flaky, archived, missing, or obviously weak automation on those journeys.
6. Write the priority and explicit `SKIP` decisions into the ledger before coding.

## Fix discipline

- Read the journey implementation and the current automation before patching either.
- Work one unresolved automation risk front at a time, not one arbitrary line item at a time.
- It is acceptable and expected to fix multiple findings together when they share one failure mode, journey, or verification story.
- Do not block on unrelated dirty or untracked files. Leave them alone unless they directly conflict with the current automation risk front or make verification unsafe.
- Do not yield just because the next fix touches a second file, module, harness helper, or test surface.
- Stop when the next credible move would require a different journey story, a new audit cycle, or verification that no longer belongs to the same front.
- If a new lane exposes a same-story product bug, fix it. Do not treat "the test found it" as enough.
- Prefer extending existing flow families and harness helpers over creating a brand-new automation island.
- Use iOS for faster iteration when available and not contradicted by the evidence; close cross-platform fronts with one Android confirmation.
- When the sanctioned simulator or device surface fails before app signal, do one bounded recovery step before calling the front blocked.
- If the sanctioned wrapper lacks the host-health command you need, one bounded native-tool recovery is acceptable when it is restorative rather than exploratory.
- If current review context cannot inspect the sanctioned runtime surface cleanly, record live state as `unknown` rather than promoting review-only access failure into a product blocker.
- Repeated cloud failures with the same lane-independent provider error and no app signal are provider blockers, not invitations to rerun the same lane forever.
- Do not build a second automation taxonomy just because the current one is imperfect.
- Do not quietly swap a simulator-required risk front to Flutter unit or widget tests because simulator work is failing. Recover the sanctioned simulator path or stop blocked.

## Existing-tool guidance

- Churn baseline:
  - `git log --since="6 months ago" --pretty=format: --name-only | sort | uniq -c | sort -rn | head -40`
- Explicit fragility markers:
  - `rg -n "TODO|FIXME|HACK|XXX|DEPRECATED"`
- Existing-tool examples when they already fit the repo:
  - repo-native integration or device test runners
  - repo-native simulator or device wrappers such as `mobile-sim`
  - existing QA commands or log-snapshot tooling
  - existing release-gate or device-farm lanes
  - `git log` churn baselines when they sharpen judgment

Record `unknown` instead of auto-installing any of these.

## Anti-patterns

- Chasing automation counts instead of meaningful journey protection.
- Adding a lane for every screen regardless of risk.
- Spending the pass on a neat tiny test fix while a larger justified primary-journey gap is still open.
- Spending the pass on a flaky low-priority screen instead of the highest-risk open journey.
- Inventing a second simulator, runner, or harness story because the current one is annoying.
- Deciding that simulator work is broken and calling Flutter unit or widget tests "good enough" for the same real-app risk front.
- Marking a front `BLOCKED` only because the current review context cannot inspect the sanctioned runtime surface.
- Treating missing auto state or a deleted ledger as if that alone proved the loop should stop.
- Rerunning the same cloud lane after repeated lane-independent provider failures with no app signal.
- Sneaking in formatting, linting, types, or tooling side quests that are not required by the finding.
- Pretending a low-value assertion is meaningful because it makes the suite look busier.
