# Architecture Quality Canon

Use this reference for the strict quality bar. It is doctrine for reviewer
judgment, not a deterministic rubric.

The same quality bar applies before and after implementation. Before
implementation, use it to judge whether the plan will create the right code.
After implementation, use `implementation-audit` mode to judge the code shape
against the plan. That mode is code review only: it does not run tests, ask for
logs, prove CI, or investigate whether a completion claim is truthful.

## Code Truth First

A plan is not strong because it sounds complete. It is strong when its claims
survive contact with the files, symbols, tests, generated artifacts, runtime
config, prompts, docs, and local instructions that govern the system.

For repo-backed plans, read all relevant code before approval. "All relevant"
means every surface needed to validate the plan's claims:

- files and symbols named by the plan
- current and likely target owner modules
- public callers and representative internal call sites
- alternate entrypoints, commands, routes, jobs, UI paths, prompts, scripts, or
  generated artifacts that can exercise the same behavior
- persistence, schema, config, fixture, adapter, and test surfaces that define
  or preserve the contract
- comparable existing patterns
- stale or legacy paths the plan claims to delete, migrate, or supersede

If more relevant code may exist, search and read before approving.

## Outcome Contract

A plan should start with the world it is trying to make true, not with tasks.
The North Star is the plain outcome. Done-state requirements are the concrete
truths that must hold when the plan is complete.

Strong done-state requirements say what will work, what will be impossible,
what will be deleted, what will be centralized, what will be simpler, and what
will be proven. Weak requirements are task-shaped: "update the service",
"refactor the flow", or "add support".

Block the plan when its checklist can complete while the intended outcome
remains false.

## Requirements And Constraints

Before judging architecture, identify:

- requirements
- non-requirements
- hard constraints
- non-constraints
- assumptions or beliefs
- complexity sources

Challenge every complexity source with: can this be simpler without breaking
the stated requirements? Complexity that cannot point back to a real
requirement, hard constraint, or drift-proofing need should be removed.

## Scope Provenance And Freeze

Apply `skills/_shared/scope-and-convergence.md`. The implementation boundary is
the human-authorized outcome plus the smallest directly competing
same-contract closure found by initial architecture before implementation, plus
later explicit human approvals. Similarity, architectural taste, generic risk,
review findings, agent-authored plan edits, and already-built code are not
authority.

Audit may reject missing provenance, an unbounded closure, or scope cycling. It
must not repair those defects by adding adjacent work itself. Before freeze,
return the gap to the planning owner. After freeze, require a human decision or
subtraction/redesign inside the frozen boundary.

## Real Ambiguity

Real ambiguity exists when two reasonable implementers could read the plan and
build meaningfully different outcomes. Surface only ambiguity that changes
outcome, scope, architecture, constraints, compatibility, deletes, proof, or
phase order. Ignore fake ambiguity and questions the repo can answer.

For each real ambiguity, name the plausible interpretations, the architecture
impact, the required decision, and whether repo truth resolves it.

Resolution is not a chat answer. A human decision owner must resolve outcome,
scope, compatibility, or constraint changes. An explicitly authorized agent
may resolve only implementation choices already inside the frozen contract.
The plan must carry the decision through all affected sections before the item
is resolved.

## Tiny-Team Maintainability

Architect for a tiny team, not a large platform staff. Prefer:

- self-documenting names and boundaries
- direct control flow
- fewer moving parts when ownership stays clear
- well-debugged existing libraries for solved problems
- boring local patterns over bespoke infrastructure
- one obvious debugging path

Block custom frameworks, runners, parsers, plugin layers, or broad config
systems when a simpler direct implementation or existing pattern would do.

## Depth-First Implementation Risk

Good plans prove a narrow integrated path early, then widen. Bad plans build
layers, helpers, variants, and parallel workstreams that only meet at the end.

Require:

- a first narrow slice that crosses the highest-risk seam
- proof in the real runtime, simulator, command path, integration test, or
  closest honest environment
- later phases that widen from a proven base
- bells, optional modes, and polish deferred until the core path works

Block plans that can reach the end before discovering the architecture was
broken from the start.

## Canonical Ownership And Existing Patterns

Prefer the existing canonical owner path when it can cleanly own the behavior.
Block parallel implementations, duplicate writers/readers, duplicate truth,
shadow contracts, and wrappers that hide unresolved contracts.

Before accepting a new pattern, audit comparable patterns. Classify related
code as:

- `already authorized`
- `frozen convergence closure`
- `leave different`
- `new scope needs human`

A locally good new pattern can still make the repo worse if related old
patterns remain live and unclassified.

## Caller Shape, State, And Invariants

Review the design from the caller's side. Correct usage should be obvious;
incorrect usage should be hard.

Block plans where callers must know internal lifecycle rules, pass magic flags,
repeat validation, choose between old and new APIs, or bypass the owner path.

Name key invariants and where they live. Prefer types, state models, runtime
routing, deletion, or API shape over developer memory. Avoid booleans, nullable
fields, and partial states that allow impossible combinations.

## Drift-Proof Coupling

When components depend on each other, the plan must make drift hard. Shared
dependencies should be represented once or fail loudly when they diverge.

Check schemas, generated artifacts, fixtures, prompts, examples, adapters,
tests, docs, and contract families. Drift-proofing should come from shared
code, typed contracts, one writer, one validator, one schema, one adapter
boundary, generated artifacts, or fail-loud checks.

## Abstractions And Concept Count

Every abstraction must earn its keep by removing repeated logic, naming a real
domain concept, hiding a dangerous boundary, simplifying callers, or making
invalid usage harder.

Bad abstractions wrap one function, pass parameters through unchanged, hide
messy contracts, introduce frameworks too early, or add new concepts while old
concepts remain live.

Elegance usually means fewer live concepts needed to explain the same behavior.

## Delete Legacy Paths And Close Side Doors

Git is the archive. Plans should delete retired live truth surfaces:

- old code paths
- stale feature flags
- compatibility shims
- duplicate APIs
- obsolete docs, examples, comments, prompts, and instructions
- generated artifacts no longer consumed
- bad defaults

Inspect side doors: alternate entrypoints, scripts, commands, direct mutation
paths, fallback readers/writers, fixtures, examples, tests, prompts, and docs
that still teach or route old behavior.

If the plan only changes the happy path, it is not architecture-complete.

## Real Boundaries And Meaningful Proof

Boundaries belong in code, routing, types, APIs, behavior, and shipped
contracts. Do not rely on stale-term greps, absence tests, docs-audit scripts,
repo layout policing, or comments saying "do not use" while the path remains
callable.

Proof should target the highest-risk seam. Prefer integration proof when risk
crosses modules, persistence, commands, generated artifacts, UI state, runtime
boundaries, or agent/tool contracts.

Unit tests are useful for tricky isolated rules. They are weak when they only
prove the compiler, framework, mocks, or implementation details.
