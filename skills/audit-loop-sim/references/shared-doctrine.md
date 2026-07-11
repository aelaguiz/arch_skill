# Audit Loop Sim Shared Doctrine

## Philosophy

- Exhaustive understanding before action. The first deliverable is a truthful map of the app, the journeys, and the automation surface, not a quick lane tweak.
- Real app first. The job is to close the biggest gaps in the automation that catches bugs unit and widget tests miss.
- Audit-loop-sim exists to reduce the biggest real-app automation risks, not to harvest easy wins.
- Primary-path, onboarding, auth or session restore, monetization, core content progression, offline state, and platform ingress matter more than polishing a safe corner of settings when the evidence supports that.
- Prefer durable automation over manual QA recipes.
- Existing repo-native automation and simulator or device surfaces come first. In repos that provide `mobile-sim`, use `mobile-sim` for simulator or device control instead of inventing a parallel runner, lane family, or harness story.
- A green lane is not enough. Every editful pass must also survive a post-change audit for safety, downstream consequences, elegance, and duplication.
- Tests exist to protect meaningful behavior. Coverage is a trailing indicator, not the product.
- Leave the app and automation surface stronger than you found them when the evidence supports a fix.

## Mapping discipline

- Enumerate app surfaces, user journeys, and the current automation surface exhaustively from repo truth before editing.
- For each journey or surface, record why it matters, its governing contract or expected outcome, the current real-app proof, the proof quality, cross-platform obligations, and the consequence if it is wrong.
- Map both the app and the proof surface. A missing or misleading lane on a fundamental journey is itself a real risk.
- Use new clean same-host native mapping children when disjoint surface
  families make parallel reading worth the integration cost. The parent names
  non-overlapping slices; examples include journeys, app surfaces, harness
  surfaces, and platform ingress, but they are not a rigid taxonomy.
- In Codex mapping dispatch set `fork_turns: "none"`. In Claude use a clean
  named or custom subagent, not a bare conversation fork or skill
  `context: fork` shorthand. Use bounded or full inherited context only for a
  named dependency that exists solely in chat.
- Select the strongest read-only capability available and also tell each
  mapper not to edit or write files, including the ledger. Mapping children
  may not create children or invoke delegation, consult, or review skills
  unless the parent explicitly assigned a bounded nested scope and budget.
- Select a mapping child only after confirming that it inherits the sanctioned
  simulator or device capabilities required by `audit-loop-sim`. If the host
  cannot confirm that inheritance, keep the slice with the authorized parent
  or complete it sequentially; do not launch an external process merely to
  bypass that capability boundary.
- Bound fanout by independent surface families, available host slots,
  shared-file or shared-state collision risk, sanctioned device contention,
  and the parent's capacity to account for, inspect, and synthesize every
  return.
- If the map is incomplete, stop after updating the ledger. Do not patch yet.

## Ranking order

1. Finish the exhaustive map of the app and automation surfaces.
2. Rank journeys, surfaces, and risk fronts by consequence first.
3. Rank within that by proof weakness or ambiguity.
4. Use churn, fragility, missing real-app signal, flake evidence, and harness drift to sharpen ties.
5. Write the priority, proof plan, post-change audit focus, and explicit `SKIP` decisions into the ledger before coding.

## Fix discipline

- Read the journey implementation and the current automation before patching either.
- Work one unresolved automation risk front at a time, not one arbitrary line item at a time.
- Choose that front from the completed map, not from convenience or curiosity.
- Record the proof plan and post-change audit focus before making edits. Higher-consequence fronts require broader downstream real-app proof.
- Fix bugs inside the existing product, journey, and automation contracts. If the apparent fix would change that contract, log the conflict and stop.
- It is acceptable and expected to fix multiple findings together when they share one failure mode, journey, or verification story.
- After the first verification pass, audit the actual diff and touched surfaces for safety, downstream consequences, elegance, and duplication.
- If that audit finds a problem, repair it in the same pass and re-run the proof that the repair affects.
- New duplication is never an acceptable temporary result. If the fix copied product logic, lane behavior, harness steps, or fallback handling into a second place, consolidate before stopping.
- Broader same-story cleanup is allowed when the post-change audit shows the first fix is awkward or duplicative, but keep it inside the same contract and automation risk front.
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

- Sampling 5-10 journeys and calling that a full audit.
- Picking something that looks fixable before the map is complete.
- Letting a neat safe lane tweak outrank a higher-consequence journey with weaker proof.
- Calling a pass done because the first lane went green even though the diff is still risky, awkward, or duplicative.
- Chasing automation counts instead of meaningful journey protection.
- Adding a lane for every screen regardless of risk.
- Spending the pass on a neat tiny test fix while a larger justified primary-journey gap is still open.
- Spending the pass on a flaky low-priority screen instead of the highest-risk open journey.
- Changing a product, journey, or automation contract because it makes the current fix easier.
- Copying the same lane logic, harness steps, or fallback handling into a second place because it feels faster than converging on one truthful path.
- Inventing a second simulator, runner, or harness story because the current one is annoying.
- Deciding that simulator work is broken and calling Flutter unit or widget tests "good enough" for the same real-app risk front.
- Marking a front `BLOCKED` only because the current review context cannot inspect the sanctioned runtime surface.
- Treating missing auto state or a deleted ledger as if that alone proved the loop should stop.
- Rerunning the same cloud lane after repeated lane-independent provider failures with no app signal.
- Sneaking in formatting, linting, types, or tooling side quests that are not required by the finding.
- Pretending a low-value assertion is meaningful because it makes the suite look busier.
