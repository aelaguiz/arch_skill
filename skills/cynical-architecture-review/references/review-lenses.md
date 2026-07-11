# Review Lenses

Use this reference after the target is resolved. It is architecture-review
doctrine, not a deterministic rubric.

The central question is:

```text
If we started from the required user experience and constraints today, would we
choose this architecture again?
```

## Ground Truth Order

Resolve truth in this order:

1. Human-authorized user experience and outcome: what the user explicitly asked
   to see, do, or rely on.
2. Explicit later human scope approvals, if any.
3. Initial architecture's pre-freeze minimal convergence closure.
4. Experiment requirements: what must stay measurable, switchable, reversible,
   comparable, or stable for the experiment to remain valid.
5. Hard constraints: platform, runtime, data, security, performance, model,
   framework, migration, or compatibility facts that cannot be wished away.
6. Current code behavior and current ownership paths.
7. Existing repo patterns that are actually canonical after reading them.
8. The smallest robust architecture that preserves the authorized items above.
9. The implementation's explanation for itself.

The implementation explanation comes last because it is often the lie.

## Scope Provenance And No-Cycling Lens

For work with a recoverable scope story, map every durable concept, owner,
state, service, dependency, compatibility path, mode, operational surface,
harness, and proof category to human scope or the frozen initial convergence
closure. A Decision Log entry, reviewer finding, later plan revision, or
current reachability is not authority.

Fail architecture that became "necessary" only because agents iterated it into
the system and later reviews treated it as a premise. This is scope cycling. A
newly discovered architectural relationship may justify a human decision, but
the review may not expand the repair scope itself. Prefer subtracting the
unauthorized cluster back to the smallest authorized architecture.

## Subtraction-First Lens

Challenge requirements before architecture. Delete or consolidate before
optimizing. Simplify before speeding up or automating.

Ask:

- Which requirement forces this structure to exist?
- Who owns that requirement by name, code path, or domain responsibility?
- What breaks for the user or experiment if this layer disappears?
- What can be removed and added back only if reality proves it is needed?
- Are we optimizing, documenting, testing, or automating a structure that
  should not exist?

Block when a layer, wrapper, flag, registry, adapter, owner split, or
compatibility path cannot point back to a real requirement, hard constraint, or
invariant.

## Complexity Accumulation Lens

Complexity is anything that makes the system harder to understand, change,
debug, or safely extend. It often accumulates through many small dependencies,
not one dramatic mistake.

Account for the tax:

- files added
- concepts added
- APIs added
- flags or modes added
- states added
- owner boundaries added
- generated artifacts added
- config branches added
- call paths added
- sync points added
- places future edits must remember to touch
- ways a future agent can choose the wrong path

Then compare that tax to the requirement it claims to serve.

## Information-Hiding Lens

Good decomposition hides design decisions likely to change. Bad decomposition
mirrors process steps, historical folders, or local implementation episodes.

Ask:

- What volatile design decision does this module hide?
- Does the interface reveal more representation, sequencing, lifecycle, or
  storage detail than callers should know?
- If a representation changes, is the change contained to one owner or spread
  across process-step modules?
- Does the caller have to remember an internal lifecycle rule that the owner
  should enforce?

Block invalid split ownership when several modules must know the same private
representation, lifecycle rule, state transition, validation rule, or hidden
contract.

## Conceptual-Integrity Lens

One coherent design idea is better than many locally reasonable ideas.

Ask:

- Does the system now express one design idea, or several independent ideas
  that happen to coexist?
- Is this structure user-friendly because it is coherent, or impressive because
  it has many mechanisms?
- Did a useful local idea violate the larger architecture?
- Would omitting one anomalous feature or path make the system easier to use,
  maintain, and extend?

Block when a locally good pattern makes the whole system less coherent or gives
future work two incompatible examples to copy.

## Simplicity Versus Easiness Lens

Easy is nearby and familiar. Simple is not interwoven. An easy patch can
increase complexity by tangling responsibilities.

Ask:

- Did this choose the nearby path because it was easy, or the separated path
  because it is simple?
- Did a wrapper or helper reduce intertwinement, or just make the next edit
  more convenient?
- Are state, time, config, and ownership braided together?
- Can the same behavior be represented with fewer interdependent moving parts?

## YAGNI And Future-Bet Lens

Do not accept architecture for imagined future use.

Ask:

- What current variation forces this genericity?
- What future requirement is this betting on?
- Is that future requirement real enough to charge today's complexity tax?
- Would a direct solution be easier to replace if the future need arrives?

Block registries, plugin layers, metadata schemas, event buses, policy engines,
strategy maps, model matrices, and broad adapters when there is only one
current concrete case.

## User Experience And Experiment Preservation

The review must not simplify by damaging the product.

Do not recommend removing:

- user-visible behavior that is part of the requested experience
- experiment branches needed for measurement
- compatibility code with a real active consumer and no approved cutover
- safety checks that enforce an invariant
- domain concepts that are irreducible
- necessary adapters around true external systems

Instead, ask whether those realities can be represented with clearer ownership
and fewer live concepts.

## Valid Reasons For Complexity

Complexity can be justified when it directly preserves:

- required user experience
- real experiment requirement
- hard runtime or platform constraint
- security boundary
- reliability or recovery requirement
- measured performance requirement in the actual system
- explicit compatibility constraint with a sunset path
- domain concept that would otherwise leak everywhere
- invariant that becomes safer because the abstraction exists

Even justified complexity should still be the smallest robust shape available.

## Invalid Reasons For Complexity

Treat these as suspect:

- "We might need it later."
- "This is how the previous iteration did it."
- "It was easier to add a wrapper."
- "The docs explain the contract."
- "The test covers it."
- "The plan said to add a layer."
- "This gives us flexibility" without a concrete current variation.
- "This keeps old behavior working" without an active consumer and removal
  path.
- "This pattern already exists elsewhere" when the pattern may itself be
  accidental.
- "This is cleaner" when the concept count increased.

## QA, Tests, Docs, And Proof Boundary

This review should not drift into pedantic QA, test, docs, or proof review.

Do not focus on test coverage gaps, missing tests, fixture polish, README
drift, doc wording cleanup, proof freshness, release-readiness checklists, CI
hygiene, or QA process unless the user explicitly asks.

Tests and docs are only relevant when they are architecture evidence:

- a test mocks the boundary that should be the real owner
- a fixture preserves an obsolete contract
- generated docs or schemas still teach the old authority path
- examples route future work through the wrong owner
- status text says a path is deleted while code still routes through it
- a doc is the only thing preventing misuse that the API should make impossible

If tests or docs do not expose architecture ownership, complexity, or
future-copy risk, ignore them.

## Strong Finding Standard

A strong finding says:

```text
This structure is accidental because <evidence from current code>. It claims to
serve <requirement>, but the real requirement is <smaller truth>. The current
shape adds <complexity tax> and creates <future spread or bug risk>. A smaller
architecture would <delete/consolidate/move/make impossible> while preserving
<user behavior and experiment constraint>.
```

A weak finding is:

- cosmetic
- style-only
- test-only
- doc-only
- QA-focused unless the user requested QA
- proof-focused unless the user requested proof validation
- a vague "too complex" complaint
- a preference for a different pattern without showing a smaller architecture
- an attempt to change the product or experiment rather than simplify the
  architecture that serves it
