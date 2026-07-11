# Examples And Anti-Examples

These examples teach the review posture. They are not a lookup table. A real
review still has to read the target code and cite current evidence.

## Scope-Cycled Reminder Architecture

Original human scope is one local reminder. Review wave 3 adds cross-device
monotonicity, wave 5 adds a database owner, and wave 8 adds retry identifiers.
The latest plan and current code treat all three as foundational, but no human
approved expansion and none appeared in the frozen initial convergence closure.

Strong finding: group the database, sync state, retry schema, config, tests,
docs, and dependencies as one scope-cycled architecture cluster. Return
`not-approved` and target subtraction to the local reminder. Do not recommend a
new synchronization framework. If cross-device behavior is now desired, it is
a separate human scope decision.

## The Core Move

Weak review:

```text
This architecture is complicated, but the tests pass and the plan says it is
intentional. No issues found.
```

Strong cynical architecture review:

```text
The plan says the registry gives us flexibility, but I found only one current
implementation and no runtime variation. The registry adds a new metadata
shape, a dispatcher, and a sync point with generated docs. The same UX can be
served by a direct owner method until a real second implementation exists.
```

The strong review does four things:

- starts from requirements and user experience
- counts the complexity tax
- refuses future-bet architecture
- proposes deletion or consolidation without changing behavior

## "Just Happened" Architecture

Failure shape:

- Each iteration added a local helper, flag, wrapper, or state surface.
- Later work treated those pieces as a deliberate architecture.

Review move:

- Reconstruct the smallest architecture from current UX and constraints.
- Mark which concepts exist only because of historical iteration.
- Flag patterns future work will copy if left in place.

Example finding:

```markdown
### [REQUIRED REPAIR] Scene mode split appears historical, not required

- File: src/scene/SceneRouter.ts
- Symbol / line: `routeTableScene` / `routeAmbientScene`
- Architecture claim being tested: Table and ambient scenes need separate route owners.
- Risk: Both paths build the same `SceneRenderRequest`, but each keeps its own
  lane key, retry handling, and cleanup callback. The split doubles the owner
  surface for one render contract.
- Evidence: `routeTableScene` and `routeAmbientScene` both call
  `SceneRenderer.render` with equivalent requirements but different local lane
  builders.
- Requirement / UX preserved: Users still enter the correct scene from table
  and ambient starts.
- Simpler architecture target: Collapse both routes through one scene-entry
  owner with the start context as data, not as two ownership paths.
- Cynical architecture pattern: historical split rationalized as architecture
```

## Invalid Split Ownership

Anti-example:

```text
The account form and API both validate names, but that is probably fine because
they are different layers.
```

Better:

```text
The form and API both own account-name validation. If the rule changes, there
are two places to update and either layer can accept a value the other rejects.
The UI can still give immediate feedback by calling the shared schema owner.
```

The question is not whether two layers exist. The question is where the
invariant lives.

## Abstraction Laundering

Failure shape:

- A new `Manager`, `Facade`, `Registry`, `Provider`, or `Adapter` makes a messy
  path sound intentional.
- The abstraction adds vocabulary without removing caller burden.

Review move:

- Ask what dangerous decision the abstraction hides.
- Count the new concepts it adds.
- Delete or inline it if it mostly forwards arguments.

Example finding:

```markdown
### [REQUIRED REPAIR] `ExportProviderRegistry` is generic machinery for one exporter

- File: src/export/ExportProviderRegistry.ts
- Symbol / line: `registerProvider`
- Architecture claim being tested: Export needs a provider registry for extensibility.
- Risk: The app has one active exporter, but the registry adds provider IDs,
  registration order, lookup failure, and generated docs sync. Future work now
  has to understand a plugin system that no requirement uses.
- Evidence: Only `CsvExporter` registers; all callers request the default
  export path.
- Requirement / UX preserved: Users can export CSV.
- Simpler architecture target: Call `CsvExporter` through the existing export
  service and add a registry only when a second real exporter exists.
- Cynical architecture pattern: generic machinery for one concrete case
```

## Flags As Architecture

Weak review:

```text
The feature flag is useful for the experiment.
```

Strong review:

```text
The experiment needs behavior selection, but this flag selects between two
owners with different state and validation. The split should move inside one
checkout owner so the experiment changes behavior, not architecture.
```

Preserve the experiment. Do not accept duplicated ownership as the default way
to preserve it.

## QA, Tests, And Docs Boundary

Weak review:

```text
Needs more unit tests and README updates.
```

Strong review:

```text
The tests matter here only because they mock `PaymentRouter`, which is the
boundary that should enforce the new owner. The test suite can stay small, but
the architecture cannot rely on a mocked boundary as proof that ownership is
real.
```

Use tests/docs only when they expose architecture truth or misdirection.
Do not emit QA/test/doc nits by default.

## Generated Artifact Drift

Failure shape:

- Source code moved to a new owner.
- Generated schema, prompt metadata, docs, examples, or snapshots still expose
  the old owner.

Review move:

- Identify the generator or source of truth.
- Ask whether the artifact is authoritative, consumed, or copied by future
  agents.
- Block stale generated truth when it preserves old architecture.

Anti-example:

```text
Update docs to match the new owner.
```

Better:

```text
`commands.generated.json` still exposes `legacyImport` as a command target.
This is not docs drift; it keeps the old architecture callable.
```

## Process-Step Decomposition

Failure shape:

- Files mirror steps in a flow: parse, normalize, enrich, write, render.
- Each step knows the same private representation.

Review move:

- Ask which design decision each module hides.
- If the answer is "a step in the process", test whether a representation
  change would touch every module.
- Recut toward the owner of the volatile decision.

## Compact Anti-Patterns

Drop findings that sound like this:

- "Needs more tests" without showing a mocked or stale architecture boundary.
- "Docs should be updated" without showing a future-copy trap or stale owner.
- "This could be cleaner" without naming the requirement and complexity tax.
- "Maybe centralize this" without naming the invariant and live split owner.
- "This is overengineered" without showing the smaller architecture that
  preserves UX and constraints.

Prefer findings that sound like this:

- "The experiment flag selects between two checkout owners; move behavior
  selection inside one owner."
- "The registry has one implementation and adds provider IDs, registration
  order, and generated-doc sync."
- "The test mocks the boundary that should enforce ownership, so green tests
  hide the split owner."
- "The adapter pile translates between internal shapes that could share one
  contract."
- "The first-draft scaffolding name now appears in public command metadata and
  will be copied as a pattern."
