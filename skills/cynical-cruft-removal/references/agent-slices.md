# Native Agent Slices

Use native parallel agents only when the host already provides them and the
target is broad enough that independent read-only slices will improve coverage.
Do not use external subprocess review, delegation, consult, or coding-harness
skills as the review mechanism.

The parent reviewer owns the final verdict. Child agents provide evidence, not
approval.

## When To Slice

Use slices when the requested target crosses several independent surfaces, such
as a whole repo, large branch, broad subsystem, large test suite, dependency
cleanup, or generated artifact cleanup.

Do not slice when:

- the scope is small enough for one reviewer to trace directly
- the user asked for a quick local answer
- the host does not provide native parallel agents
- the parent cannot inspect and account for every child result before
  finalizing

## Slice Options

Choose only slices that match the target.

### Live Roots

Map product/user workflows, runtime entrypoints, public APIs, build/install/
deploy/release paths, supported commands, integration contracts, and safety/
security/migration/data obligations. Report which roots can prove value.

### Self-Referential Islands

Find clusters of files that reference each other but have no inbound live root.
Include code, tests, docs, examples, generated files, package exports, configs,
and prompts that keep the cluster alive.

### Test Bloat

Find tests that protect no current behavior, test mocks or fixtures, duplicate
implementation logic, pin private details, preserve retired behavior, pad
coverage, or keep dead code alive. Do not request more tests.

### Dependencies, Build, And Config

Find unused or oversized dependencies, dev dependencies for retired tests or
generators, stale package exports, dead commands, obsolete CI jobs, old env
vars, config keys for deleted modes, and stale lockfile residue.

### Docs, Examples, Prompts, And Generated Surfaces

Find point-in-time docs that read like current truth, examples for retired APIs,
prompt surfaces that teach old behavior, generated files with stale source
truth, and docs/generated references that launder dead artifacts.

### V1/V2 And Stale Flags

Find retired V1 paths left beside current V2 paths, stale feature flags,
compatibility ghosts, fallback branches, old aliases, phantom public APIs, and
deployment/config branches that preserve impossible states.

### Low-Value Live Abstractions

Find reachable but low-value wrappers, registries, adapters, factories,
single-use generic abstractions, duplicate implementations, glue files, and
compatibility layers that do not serve a current requirement.

### Scope-Laundered Live Clusters

For scope-backed work, compare the initial human scope and frozen convergence
closure with review waves and current artifacts. Group unauthorized code,
tests, schemas, configs, docs, dependencies, and ops surfaces even when live.
Current reachability is not approval. Recommend subtraction, not replacement
machinery.

## Child Prompt Shape

Use a compact prompt like:

```text
You are one read-only reviewer in a cynical cruft removal review.

Slice: <slice name>
Target: <target>

Assume references are not proof of value. Identify current roots, suspicious
artifacts, weak references, self-preserving clusters, deletion candidates, keep
decisions, and coverage gaps for this slice only.

When scope history is supplied, treat human scope and the frozen closure as
authority. Report scope-laundered live clusters; do not keep them because later
agents made them reachable.

Return concise evidence with repo paths. Do not edit files. Do not ask for more
tests or docs. Do not use external review/delegation tools.
```

## Parent Accounting

Before finalizing, the parent must record in `coverage.md`:

- slice name
- agent status
- files or surfaces covered
- candidate clusters found
- keep decisions worth preserving
- gaps or conflicts
- how the parent used or rejected the child evidence

If a child does not return, is interrupted, or gives unusable evidence, record
that honestly. Do not count launched-but-unreturned work as review coverage.
