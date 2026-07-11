# Review Lenses

Use these lenses to split or structure the audit. They are not a checklist
executor. Parent synthesis owns the verdict.

For `implementation-audit` mode, use
`implementation-audit-mode.md#implementation-lenses`. The lenses below are for
plan-readiness audits before implementation.

## Required Lenses

### `scope-provenance-and-minimal-convergence`

Recover the initial human-authorized outcome, explicit later human approvals,
the initial architecture's pre-freeze convergence closure, and the freeze
anchor. Map every durable obligation to human scope or that closure. Reject
"the plan says so" when the cited plan text was agent-authored and has no
upstream authority. Distinguish directly competing same-contract paths from
similar neighboring code, and reject speculative proof or infrastructure.

This lens may identify the smallest plan gap but may not add scope. Before
freeze, route the gap back to the initial planning owner. After freeze, require
a human decision. Treat scope cycling—agent work becoming code and then being
used to justify more work—as blocking.

### `outcome-north-star`

Check whether the plan states the desired world before task detail. Verify that
done-state requirements describe what will be true when the plan is complete.
Block task-shaped requirements that can be checked off while the outcome
remains false.

### `ambiguity-and-miscommunication`

Find real ambiguity where two reasonable implementers could build different
outcomes. Focus on outcome, requirements, constraints, non-constraints,
compatibility, deletion, proof, and phase order. Ignore fake ambiguity and
questions already answered by repo truth.

### `requirements-constraints-simplicity`

Check requirements, non-requirements, hard constraints, non-constraints,
assumptions, and complexity sources. Challenge every complexity source with:
can this be simpler without breaking stated requirements?

### `tiny-team-maintainability`

Judge whether the plan fits a tiny team. Prefer self-documenting code, simple
control flow, proven libraries, existing patterns, and minimal custom
infrastructure. Block ongoing maintenance burden without clear payoff.

### `depth-first-risk`

Check whether the plan proves a narrow end-to-end path before it widens.
Identify the first integrated slice, highest-risk seam, and exact proof
required before adding callers, variants, platforms, or features. Block broad
scaffolding that defers integration proof to the end.

### `code-truth-map`

For repo-backed plans, verify that current architecture, target architecture,
and call-site inventory match repo reality. Find unnamed owner paths, callers,
adjacent same-contract or same-behavior paths, generated artifacts, tests,
docs, prompts, or config the plan must account for.

### `canonical-owner-and-ssot`

Ask whether the plan extends the correct central path. Find duplicate truth,
parallel implementations, shadow contracts, alternate writers/readers, and
wrong-layer logic. Check whether adjacent caller families or feature variants
that should share the same owner would still route around it.

### `existing-pattern-and-convergence`

Find comparable repo patterns and judge whether the plan chose the canonical
owner. Comparable or same-behavior code is evidence, not scope authority. Only
directly competing same-contract paths already inside the pre-freeze closure
may be required automatically; newly discovered paths route to planning before
freeze or a human decision after freeze. Block unjustified new patterns.

### `caller-invariant-state`

Review the proposed API or boundary from the caller side. Check misuse
resistance, invariant ownership, state-model simplicity, partial-update risk,
and whether callers must know internals.

### `drift-proof-coupling`

Inspect shared dependencies, schemas, generated artifacts, adapters, fixtures,
prompts, tests, docs, and contract families. Check whether dependent pieces
share one source of truth or can silently diverge. Include sibling surfaces
that expose the same contract through another route, command, feature, prompt,
fixture, or generated artifact.

### `elegance-and-code-judo`

Search for a simpler architecture that deletes concepts. Challenge wrappers,
conditionals, compatibility layers, overbroad scaffolding, fake abstractions,
and unnecessary tools. Track concepts added, deleted, merged, privatized, or
left exposed.

### `deletion-and-side-door`

Search for legacy paths, flags, direct mutation paths, old commands, bad
defaults, docs, examples, comments, prompts, tests, fixtures, and other
surfaces that keep old behavior discoverable or callable. Also check adjacent
live paths that are not obviously legacy but still implement or teach the same
behavior through a different owner.

### `proof-and-phase-exit`

Check whether phases, checklists, exit criteria, rollback, and verification
actually prove architecture and behavior-preservation claims. Prefer
behavior-level integration proof when risk crosses modules or runtime
boundaries. Reject proof that only proves compiler, framework, or mocks.

## Conditional Lenses

- `agent-capability`: Required when the plan changes prompts, agents, skills,
  LLM workflows, MCP, or model-facing behavior. Check prompt-first and native
  capability options before custom tooling.
- `docs-contract-drift`: Required when the plan changes public commands, APIs,
  docs, prompts, user-facing contracts, telemetry names, stable IDs, examples,
  or install behavior.
- `security-boundary`: Required when the plan touches auth, permissions,
  secrets, command execution, input validation, privacy, filesystem, process,
  or network boundaries.

## Parent Synthesis

Do not concatenate lens reports. The parent must:

- spot-check cited plan and code evidence
- dedupe findings across lenses
- classify each finding as a required repair, observation, wrong, or out of scope
- preserve genuine unresolved decisions
- add missed findings when evidence supports them
- keep the final verdict no softer than the worst unresolved required repair

Child reports are evidence. They are not the verdict.
