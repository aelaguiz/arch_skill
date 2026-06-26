# Cruft Lenses

Use these lenses to decide whether an artifact has current value or should go
away. References are clues, not proof. A current live root plus a current
purpose is the keep standard.

## Live Purpose

An artifact has a live purpose only when it serves at least one current root.

Ground-truth order:

1. Current user workflow or product behavior.
2. Runtime entrypoint, public API, package export, plugin hook, or integration
   contract that is actually supported.
3. Build, deploy, install, packaging, migration, or release path that still
   runs.
4. Current security, safety, compliance, data-retention, migration, or
   compatibility requirement with an owner.
5. Current test that protects live behavior or a real invariant.
6. Current docs, examples, or prompts that a reader genuinely needs to operate
   current behavior.
7. Source-of-truth generated artifact consumed by a live root.
8. Git history for retired ideas. If the only reason to keep a file is "we may
   want to remember it," the repo probably already has the archive.

A reference outside those roots is weak evidence. A reference from another
suspect artifact is not keep proof.

## Artifact Types

### Dead Code

Dead code includes:

- unreachable functions, methods, classes, modules, and branches
- uncalled scripts and commands
- unused exports and package entrypoints
- old CLI flags, env vars, settings, and config keys
- retired feature-flag branches
- old migrations, aliases, and compatibility shims with no current caller
- unreachable error handling for states the system can no longer enter
- old generated files that no current generator or runtime consumes
- dead CSS classes, assets, locale keys, routes, templates, and components

The hidden form is the dead island: files call each other, tests import them,
docs mention them, and examples still compile, but no live root enters the
island.

### Low-Value Live Code

Some cruft executes but still does not justify itself:

- pass-through wrappers that hide the real owner
- single-use generic abstractions
- factories, registries, adapters, or plugin systems with one current case
- duplicate implementations of the same contract
- compatibility layers for clients that no longer exist
- optional modes that product no longer supports
- speculative hooks for future requirements
- config branches that only encode old decisions
- glue files that exist only because previous structure was awkward
- code used only by tests, docs, examples, storybooks, or retired demo paths

For this class, "used" is not enough. Ask whether the use is valuable.

### Test Bloat And Test Cruft

Tests become cruft when they cost more maintenance than the confidence they
provide.

Common forms:

- assertion-free tests
- import-only tests
- smoke tests that verify the interpreter can load a module but no behavior
- tests that test mocks, fakes, fixtures, or local setup instead of product
  behavior
- tests that duplicate implementation logic
- snapshot tests that act as change detectors instead of behavior checks
- tests pinned to private implementation details
- tests for retired V1 behavior after V2 is the only supported path
- tests that preserve dead APIs so the code cannot be deleted
- massive fixtures used by one tiny assertion
- tests that require slow, flaky, or expensive setup but catch no meaningful
  defect
- coverage padding that exists to satisfy a number, not protect a behavior

Do not ask "does this test reference the code?" Ask "what current behavior or
invariant does this test protect?"

### Documentation, Prompt, And Example Cruft

Docs are not the main focus, but they can keep dead systems alive.

Common forms:

- point-in-time plan docs that are no longer current operating truth
- old worklogs that read like instructions
- examples for retired APIs
- README sections that describe removed or unsupported commands
- prompt files that teach old behavior
- generated docs copied from obsolete metadata
- diagrams that preserve old ownership
- docs that only cite other stale docs
- migration-complete notes that keep both old and new systems conceptually
  alive

If a doc is the only reason an old thing looks live, the doc is suspect too.

### Dependency, Build, And Config Cruft

Common forms:

- unused runtime dependencies
- dev dependencies needed only by dead tests, retired generators, or obsolete
  scripts
- oversized dependencies used for a trivial operation
- old build targets, Makefile commands, package scripts, CI jobs, and release
  steps
- package exports for retired entrypoints
- config files for old tools
- env vars nobody reads
- default values for deleted modes
- stale lockfile entries that remain because dependency cleanup stopped short

Build metadata is code. It can preserve dead behavior just as effectively as a
source file.

### Data, Telemetry, And Ops Cruft

Common forms:

- dead database columns and tables
- retired event names
- old analytics dimensions
- dashboards for removed workflows
- alerts tied to obsolete systems
- migration states that cannot occur anymore
- old queue topics, cron jobs, and worker names
- data copies retained because no one proved the current root

Data and ops cleanup needs more caution than local code cleanup, but references
still do not prove current purpose.

## Hidden Cruft Patterns

### Self-Referential Island

Several files reference each other, and search makes them look alive. No live
root reaches the island.

Review move:

- identify root reachability, not only local references
- classify the whole island as a deletion or quarantine candidate

### Reference Laundering

A weak reference gets treated as strong evidence because it appears in an
official-looking file.

Examples:

- generated metadata references an old command
- docs cite a retired helper
- a test imports an old API
- a package export exposes an old symbol
- a compatibility shim calls an old path to preserve a name

Review move:

- ask whether the referring artifact itself has a live purpose

### Test Hostage

Dead code stays because tests still expect it.

Signals:

- code is only used by tests
- tests describe retired behavior
- deleting the code would only break tests with no current product impact

Review move:

- treat the test as part of the cruft cluster
- recommend deleting or rewriting the test with the code

### Docs Laundering

Docs keep old behavior plausible after code moved on.

Signals:

- docs are the only current reference to a command, workflow, option, class, or
  old owner
- docs contain status language that sounds current but no live root agrees

Review move:

- mark the doc as stale-supporting cruft, not keep evidence

### Generated Artifact Laundering

Generated files keep repeating old names after the source owner changed or
disappeared.

Signals:

- generated file references an old API
- generator source is gone, retired, or points to stale metadata
- no current build path regenerates the artifact

Review move:

- trace the source-of-truth generation path before accepting the reference

### Compatibility Ghost

A compatibility wrapper, old export, alias, flag branch, or fallback path stays
after the compatibility need is gone.

Signals:

- no current consumer requires the old name or behavior
- comments say "temporary", "legacy", "for now", "backcompat", or "TODO"
- git history shows the migration completed long ago

Review move:

- identify current consumers; if none, recommend deletion or a narrow owner
  check

### V1/V2 Shadow System

V2 is current, but V1 remains partially wired through tests, docs, examples,
config, scripts, or exports.

Signals:

- both systems can be found by search
- only V2 is used by the product path
- V1 survives because removing it breaks old tests or documentation examples

Review move:

- report the whole shadow system as one deletion cluster, not as isolated files

### Phantom Public API

Something is exported or documented like a public contract, but no current user
depends on it.

Signals:

- export map includes symbols with no external consumer
- docs imply support, but no integration path uses it
- code exists to preserve a name rather than a behavior

Review move:

- distinguish "public in syntax" from "public in obligation"

### Configuration Cemetery

Config options accumulate after the code paths they select are retired.

Signals:

- env var, YAML key, feature flag, package script, CI matrix entry, or runtime
  option is read but no current deployment sets a meaningful alternative
- default branch is the only real branch

Review move:

- trace actual environment, deploy, and install use, not only parser reads

## Deletion Classes

### Delete Now

Use when:

- no live root reaches the artifact
- all references are self-referential, docs-only, tests-only, generated-stale,
  or retired examples
- deletion risk is local and clear

Expected report action:

```text
Delete this cluster together.
```

### Delete After One Owner Check

Use when:

- repo evidence points to deletion
- a narrow external consumer, deployed config, data-retention, migration,
  security, or public-contract fact could change the answer
- the owner check is small and specific

Expected report action:

```text
Ask <specific owner/system question>, then delete if no current obligation is
found.
```

Avoid vague owner checks such as "maybe someone uses this somewhere." Name the
exact missing fact.

### Quarantine

Use when:

- artifact is probably dead but deletion risk is high
- migration order matters
- runtime observability is needed before delete

Expected report action:

```text
Move behind an explicit retirement path or mark unsupported, then delete after
the stated condition.
```

### Consolidate

Use when:

- artifact is not individually dead, but duplicates another owner or preserves
  split truth
- deletion should happen by moving live responsibility to the canonical owner
  first

Expected report action:

```text
Move callers to the owner, then delete this duplicate path.
```

### Keep

Use when:

- a current root and current purpose are both clear
- the artifact's value is not only historical, speculative, docs-only,
  tests-only, or compatibility-by-habit

Expected report action:

```text
Keep, with the live purpose named.
```
