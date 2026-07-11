# Audit Loop Shared Doctrine

## Philosophy

- Exhaustive understanding before action. The first deliverable is a truthful map of shipped code and proof surfaces, not a quick patch.
- Consequence first. Wrong results on core algorithms, monetization, auth, persistence, permissions, or other outcome-critical surfaces matter more than polishing a safe utility.
- Audit-loop exists to reduce the biggest real risks, not to harvest easy wins.
- Weak or misleading proof on a fundamental surface is itself a real risk.
- Dead code is a bug waiting to happen. Delete it instead of preserving it.
- Duplication is deferred breakage. Consolidate one source of truth where the duplication matters.
- A green test run is not enough. Every editful pass must also survive a post-change audit for safety, downstream consequences, elegance, and duplication.
- Tests exist to protect meaningful behavior. Coverage is a trailing indicator, not the product.
- When audit-loop adds or materially rewrites a test, the test should also explain the behavior it is protecting. Leave comments that make the why and the expected user-visible or externally observable outcome easy to inspect later.
- Leave the codebase lighter than you found it when the evidence supports deletion or simplification.

## Mapping discipline

- Enumerate shipped code surfaces exhaustively from repo truth before editing.
- Enumerate the current proof surface exhaustively before editing.
- For each surface, record why it matters, its governing contract or invariant, its downstream dependents, the current proof, the proof quality, and the consequence if it is wrong.
- Use new clean same-host native mapping children when disjoint surface
  families make parallel reading worth the integration cost. The parent names
  non-overlapping slices; examples include entrypoints, core logic,
  integrations, and proof surfaces, but they are not a rigid taxonomy.
- In Codex mapping dispatch set `fork_turns: "none"`. In Claude use a clean
  named or custom subagent, not a bare conversation fork or skill
  `context: fork` shorthand. Use bounded or full inherited context only for a
  named dependency that exists solely in chat.
- Select the strongest read-only capability available and also tell each
  mapper not to edit or write files, including the ledger. Mapping children
  may not create children or invoke delegation, consult, or review skills
  unless the parent explicitly assigned a bounded nested scope and budget.
- Bound fanout by independent surface families, available host slots,
  shared-file or shared-state collision risk, and the parent's capacity to
  account for, inspect, and synthesize every return.
- If the map is incomplete, stop after updating the ledger. Do not patch yet.

## Ranking order

1. Finish the exhaustive map of code and proof surfaces.
2. Rank surfaces and risk fronts by consequence first.
3. Rank within that by proof weakness or ambiguity.
4. Use churn, dead-code evidence, duplication, and explicit fragility markers to sharpen ties.
5. Write the priority, proof plan, post-change audit focus, and explicit `SKIP` decisions into the ledger before coding.

## Fix discipline

- Read the code before the tests.
- Work one unresolved risk front at a time, not one arbitrary line item at a time.
- Choose that front from the completed map, not from convenience or curiosity.
- Record the proof plan and post-change audit focus before making edits. Higher-consequence fronts require broader downstream proof.
- Fix bugs inside the existing contract. If the apparent fix would change the product, API, or behavior contract, log the conflict and stop.
- It is acceptable and expected to fix multiple findings together when they share one failure mode, critical path, or verification story.
- After the first verification pass, audit the actual diff and touched surfaces for safety, downstream consequences, elegance, and duplication.
- If that audit finds a problem, repair it in the same pass and re-run the proof that the repair affects.
- New duplication is never an acceptable temporary result. If the fix copied logic, assertions, or fallback handling into a second place, consolidate before stopping.
- Broader same-story cleanup is allowed when the post-change audit shows the first fix is awkward or duplicative, but keep it inside the same contract and risk front.
- Do not block on unrelated dirty or untracked files. Leave them alone unless they directly conflict with the current risk front or make verification unsafe.
- Do not yield just because the next fix touches a second file, module, or test surface.
- Stop when the next credible move would require a different risk story, a new audit cycle, or verification that no longer belongs to the same front.
- Delete dead code boldly. Git is the history.
- Extract duplication into one well-named shared path. Do not build a framework.
- Prefer integration coverage on critical paths. Add unit tests only when the logic is best isolated there.
- Do not force a comment template. Use the smallest nearby comment form that makes the why and expected experience or outcome unmistakable.
- Do not write a test for code you are deleting.

## Existing-tool guidance

- Churn baseline:
  - `git log --since="6 months ago" --pretty=format: --name-only | sort | uniq -c | sort -rn | head -40`
- Explicit fragility markers:
  - `rg -n "TODO|FIXME|HACK|XXX|DEPRECATED"`
- Example optional coverage or scanner commands when they already fit the repo:
  - `npx jest --coverage --coverageReporters=json-summary`
  - `pytest --cov=src --cov-report=json`
  - `npx ts-prune`
  - `npx knip`
  - `npx jscpd . --min-lines 6`
  - `vulture src/`
  - `pylint --disable=all --enable=duplicate-code src/`

Record `unknown` instead of auto-installing any of these.

## Anti-patterns

- Sampling 5-10 paths and calling that a full audit.
- Picking something that looks fixable before the map is complete.
- Letting a neat safe fix outrank a higher-consequence surface with weaker proof.
- Calling a pass done because the first proof went green even though the diff is still risky, awkward, or duplicative.
- Chasing 100 percent coverage.
- Adding a test for every function regardless of risk.
- Refactoring an entire module because one smell was noticed during audit.
- Spending the pass on a neat tiny fix while a larger justified critical-path risk is still open.
- Spending the pass on a flaky low-priority test instead of the highest-risk open area.
- Changing a contract because it makes the current fix easier.
- Copying the same logic, assertions, or fallback handling into a second place because it feels faster than converging on one truthful path.
- Sneaking in formatting, linting, types, or tooling side quests that are not required by the finding.
- Pretending a low-value assertion is meaningful because it makes the coverage number move.
- Leaving a new audit-loop-authored test with no comment about why the behavior matters or what correct experience or outcome should happen.
- Writing comments that only paraphrase the assertion or narrate implementation details without explaining the protected behavior.
