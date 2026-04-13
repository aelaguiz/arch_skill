# Comment Loop Shared Doctrine

## Philosophy

- Understanding before explanation. The first deliverable is a truthful map of repo, proof, and explanatory surfaces, not a quick comment pass.
- Comments are for high-cost misunderstanding, not for line-by-line narration.
- Shared contracts, conventions, and gotchas on critical paths matter more than isolated code-style nits.
- A stale or misleading comment on an outcome-critical surface is itself a real maintenance risk.
- A missing canonical owner comment is usually worse than many missing local comments.
- The point of the pass is to make the next careful reader less likely to misread behavior, not to decorate the repo.
- Delete or repair stale explanation. Git is the history.

## Mapping discipline

- Enumerate shipped code surfaces exhaustively from repo truth before editing.
- Enumerate the current proof surface exhaustively before editing.
- Enumerate the current explanatory surface exhaustively before editing.
- For each surface, record why it matters, its governing contract or invariant, its downstream dependents, the current proof, the proof quality, the current explanation, and the consequence if it is misunderstood.
- Record shared contracts, conventions, gotchas, and preferred comment sites explicitly in the ledger.
- Use parallel read-only agents when the runtime supports delegation. Split by disjoint surface families such as entrypoints, core logic, integrations, proof surfaces, and current explanatory coverage. Treat those splits as examples, not a rigid taxonomy.
- If the map is incomplete, stop after updating the ledger. Do not comment yet.

## Ranking order

1. Finish the exhaustive map of code, proof, and explanatory surfaces.
2. Rank surfaces and comment fronts by consequence of misunderstanding first.
3. Rank within that by sharedness and downstream blast radius.
4. Rank within that by explanation weakness, misleadingness, or staleness.
5. Use churn, explicit fragility markers, and repeated confusion points to sharpen ties.
6. Write the priority, proof plan, and explicit `SKIP` decisions into the ledger before editing.

## Comment discipline

- Read the code before you explain it.
- Work one unresolved comment front at a time, not one arbitrary file at a time.
- Choose that front from the completed map, not from convenience.
- Record the proof plan before making edits. Higher-consequence fronts require broader downstream proof.
- Comments explain existing behavior, not desired future behavior.
- Declaration or doc comments should explain use, contract, side effects, dependencies, defaults, ownership, lifetimes, allowed ranges, errors, panics, or safety requirements when those matter to a caller.
- Inline comments should explain non-obvious implementation choices, ordering, concurrency, invalidation, cache behavior, cross-boundary assumptions, or rationale. They should not narrate mechanics the code already states clearly.
- Data member or constant comments are only worth writing when the type and name do not already make the invariant or relationship obvious.
- Test comments should explain the protected behavior and why it matters, not paraphrase assertions.
- Prefer one authoritative comment at the canonical owner boundary over copied explanations at call sites.
- Examples belong only when they are the clearest way to show intended use or a counterintuitive trap.
- If a surface is still behaviorally ambiguous, buggy, or contract-conflicted, do not freeze that uncertainty into comments. Log it and route to the owning skill.
- Do not block on unrelated dirty or untracked files. Leave them alone unless they directly conflict with the current comment front or make verification unsafe.

## Existing-tool guidance

- Churn baseline:
  - `git log --since="6 months ago" --pretty=format: --name-only | sort | uniq -c | sort -rn | head -40`
- Explicit fragility markers:
  - `rg -n "TODO|FIXME|HACK|XXX|NOTE|WARNING|DEPRECATED"`
- Explanation hotspots:
  - public entrypoints and exported APIs
  - persistence and integration boundaries
  - lifecycle, ownership, or concurrency code
  - code with counterintuitive defaults, ordering, or side effects
  - tests that protect subtle behavior but do not say why

Record `unknown` instead of auto-installing new tools.

## Anti-patterns

- Sampling a handful of files and calling that a full explanation pass.
- Adding comments before the map is complete.
- Letting a neat local note outrank a shared critical-path gotcha.
- Commenting a bug instead of fixing or routing it.
- Duplicating the same convention explanation across many call sites.
- Explaining signatures, obvious operations, or naming that is already clear in code.
- Preserving stale migration history or implementation archaeology in live comments.
- Writing comments that are more speculative than the proof.
- Treating any new comment as a win even when it adds noise.
- Leaving touched stale comments in place because the new comment seems good enough nearby.
