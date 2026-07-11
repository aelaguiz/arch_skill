# Failure Patterns

Use this catalog to sharpen suspicion after the architecture map is clear.
Apply judgment, read real code, and cite evidence you actually inspected.

For every pattern:

- name the user experience, requirement, or invariant the structure claims to
  serve
- identify current owners, or say there is no clear owner yet
- search for old and alternate paths that still express the same concept
- count the live concepts a future maintainer must understand
- decide whether the current shape is essential or accidental
- flag only current-code or requested-scope architecture risks with concrete
  evidence

## Architecture That "Just Happened"

Flag when the current structure is explainable as a sequence of patches, but
not as a design that would be chosen from today's user experience and
constraints.

Common signs:

- each piece has a local reason, but the total system has no clear owner
- the structure matches historical iteration order more than domain shape
- scaffolding or first-draft names now carry production behavior
- reviewers defend the current shape because it exists, not because
  requirements force it

Block when future work is likely to copy the accidental pattern, when ownership
is unclear, or when the same behavior can be achieved through a smaller
obvious owner.

Do not block merely because the code has history if the current architecture
now has a clear owner, narrow interface, and real requirement.

## Scope-Cycled Architecture Presented As Required

Flag when a worker or reviewer introduced durable architecture after scope
freeze, later plan/docs/tests encoded it as current truth, and subsequent
reviews used that truth to demand more services, state, retries, schemas, or
operational machinery.

Read the initial human ask, frozen convergence closure, explicit human
approvals, plan revisions, Decision Log, review waves, and final complexity
ledger. Current reachability proves the architecture exists, not that it was
authorized.

This is a `REQUIRED REPAIR` and forces `not-approved`. Group the unauthorized
concepts as one subtraction target. Do not recommend a new generalized system
as the repair. A newly found relationship absent from the frozen contract needs
a human decision rather than automatic expansion.

## Invalid Split Ownership

Flag when two modules both partly own the same domain concept, state,
lifecycle, validation, persistence, routing, prompt behavior, generated truth,
or contract.

Common signs:

- callers must choose between owners
- two owners validate or persist the same concept differently
- one path owns creation while another owns mutation with no shared invariant
- UI, job, script, or API path bypasses the supposed owner
- direct writers/readers remain live after centralization is claimed

Block when correctness depends on developer memory, when future edits can
update one owner and miss another, or when no real product/runtime split
justifies the ownership split.

Do not block when the review can name a real contract difference and code
enforces the boundary.

## Duplicate Truth With Different Names

Flag when two fields, configs, schemas, helpers, prompts, commands, fixtures,
generated artifacts, or docs express the same truth with different wording and
both can still influence behavior or future work.

Common signs:

- one runtime reads from config while another reads from metadata
- tests instantiate a duplicated rule instead of the owner
- generated artifacts can drift from source
- examples teach a different contract than the API enforces

Block when the codebase now has two answers to one question.

Do not block when one truth is purely historical, unreachable, or explicitly
non-authoritative.

## Compatibility Shim That Became Architecture

Flag when a migration bridge, fallback reader, old API, alias, feature flag,
adapter, or "temporary" path is still active after the new path exists, and
new work has started depending on it.

Common signs:

- old command or route still registered
- fallback accepts the old shape silently
- a shim has no deletion condition
- a new caller imports the compatibility layer directly
- both systems remain selectable behind a flag

Block when the shim becomes a second architecture or blocks convergence.

Do not block a short explicit compatibility bridge that delegates immediately
to the new owner, has no new direct callers, and has a deletion point.

## Abstraction Laundering

Flag when a wrapper, service, manager, registry, provider, orchestrator,
factory, policy object, or adapter gives messy logic a respectable name without
reducing concept count.

Common signs:

- it mostly passes data through
- it exposes the same flags as the implementation below
- it has the same method names as the wrapped service
- it exists for one caller without naming a real domain concept
- tests now mock the wrapper instead of behavior

Block when the abstraction removes no meaningful complexity, hides confusion,
creates a second API, weakens behavior proof, or makes future reviewers afraid
to delete it.

Do not block when the abstraction hides a dangerous boundary, names a real
domain concept, reduces caller burden, or makes invalid use harder.

## Layer Added To Avoid A Decision

Flag when a new layer routes between old and new paths instead of choosing one
or expressing a clear migration state.

Common signs:

- multiple modes exist because nobody chose the correct model
- runtime config decides between two owners
- code supports both representations indefinitely
- the layer's main job is to preserve disagreement

Block when decision avoidance becomes runtime complexity.

Do not block when the layer is a clear adapter at a true external boundary or
an explicit short-lived migration bridge.

## Generic Machinery For One Concrete Case

Flag when plugins, registries, metadata schemas, event buses, policy engines,
strategy maps, model matrices, or dispatch frameworks exist for one current
variation.

Block when genericity is justified only by possible future needs.

Do not block when there are multiple active variations with different
requirements and the machinery makes those variations simpler to reason about.

## Feature Flag As Architecture Boundary

Flag when a flag changes which architecture owns behavior, not just which user
behavior is enabled.

Common signs:

- each flag path owns separate state or validation
- both flag paths have separate downstream handling
- turning the flag off revives an old owner path
- the experiment requires behavior selection but the implementation duplicates
  ownership

Block when the repo now has two systems behind one interface.

Do not block real experiments. Instead, require the flag to select behavior
inside one owner when possible, or name the sunset path for duplicated owners.

## State Spread

Flag when several places track related state and must stay synchronized.

Common signs:

- callers can observe impossible combinations
- one owner updates persistence while another updates in-memory state
- separate booleans encode one domain state machine
- cleanup or retry paths update a different state surface than success paths

Block when bugs become timing, lifecycle, or forgotten-update failures.

Do not block separate state for truly separate lifecycle concerns when the
boundary is explicit and enforced.

## Caller Memory Contract

Flag when correct use requires callers to remember ordering, magic flags,
cleanup calls, lifecycle transitions, matching IDs, hidden validation rules, or
which old/new owner to call.

Block when the architecture leaks internal rules to every caller.

Repair target should move the rule into API shape, type, constructor, command,
route, schema, validator, state transition, or owner.

## Process-Step Decomposition

Flag when modules mirror execution steps rather than hiding volatile design
decisions.

Common signs:

- changing storage or representation requires edits across many steps
- output code knows details of input or transformation internals
- a process pipeline hides no dangerous decisions
- everything must be understood as a whole

Block when the cut makes change harder than a decision-hiding owner would.

## Shallow Module Sprawl

Flag when many files or classes have small implementations but large
interfaces, configuration surfaces, or caller obligations.

Block when the boundary costs more than it hides.

Repair target should merge shallow modules or create a deeper owner that hides
more complexity behind a smaller interface.

## Pattern Laundering

Flag when a new structure is defended because similar code exists nearby, but
the nearby pattern was never proven intentional or healthy.

Block when accidents become precedents.

Read the origin and current role of the existing pattern when it materially
affects the review. Classify it as canonical, accidental-but-contained,
different, or wrong-road.

## Over-Documented Bad Boundary

Flag when docs or comments explain how not to misuse an API, but the API still
permits misuse.

Block when documentation is the only thing preventing wrong calls, wrong state,
or wrong ownership use.

Do not turn this into docs cleanup. The repair target is code shape.

## Test-Mocked Architecture

Flag when tests prove an internal abstraction, mocked flow, or fixture contract
but do not prove the real runtime owner path.

Block when green tests hide a wrong boundary, preserve an obsolete contract, or
make the architecture seem safer than it is.

Do not turn this into a coverage complaint. It matters only when the test
surface hides or preserves the wrong architecture boundary.

## Orchestrator Gravity

Flag when a central orchestrator keeps gaining conditional branches,
sequencing rules, retries, special cases, and knowledge of child internals.

Block when the orchestrator becomes the accidental domain model.

Repair target should push decisions down to the owner that has the invariant
and keep orchestration focused on ordering.

## Adapter Pile

Flag when several adapters translate between internal shapes that could have
shared one contract.

Block when translation layers hide an unsettled model.

Do not block adapters at true external boundaries.

## Configuration As Programming Language

Flag when YAML, JSON, env matrices, config files, prompt metadata, or install
metadata encode branching logic that belongs in code or a simpler static
choice.

Block when the system gains a second programming language without tooling,
types, or owner clarity.

Do not block genuine deploy-time or experiment configuration with one clear
owner and a small shape.

## Generated Artifact Drift

Flag when generated files, schemas, snapshots, docs, examples, prompt surfaces,
or package metadata can disagree with source code.

Block when stale artifacts preserve duplicate truth, old owner paths, or
future-copy traps.

Do not turn this into docs cleanup. The repair target is one source of truth or
clear non-authority.

## Architecture Theater

Flag when a change adds diagrams, categories, modes, scorecards, policy
language, review artifacts, or process proof without making actual code paths
simpler.

Block when ceremony creates the feeling of control while adding concepts.

Do not block small human-readable review notes. Block when ceremony becomes
live architecture or hides unchanged code complexity.

## Experiment Requirement Overreach

Flag when A/B testing, reversibility, measurement, or staged rollout is used to
justify duplicated architecture.

Block when real experiment constraints are represented as permanent
split-brain systems.

Preserve the experiment, but force the split to the smallest possible level:
data, config, behavior selection inside one owner, or an explicit temporary
bridge.

## User Experience Mismatch

Flag when the architecture is elegant for internal builders but does not map
cleanly to the actual user job.

Block when internal structure distorts the product, starting state, or user
workflow.

Do not simplify by removing requested behavior. Simplify the path underneath
the behavior.

## Cemented First Draft

Flag when initial scaffolding, exploratory files, prototype naming, or
temporary directory layout now carries production behavior.

Block when prototype assumptions now mislead ownership, call paths, or future
work.

Repair target should promote the real owner or delete/rename scaffolding that
would mislead future agents.
