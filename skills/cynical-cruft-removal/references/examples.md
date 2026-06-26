# Examples

Use these examples to learn the reasoning pattern. Do not treat them as a
finite checklist. The current repo evidence decides each review.

## Strong Finding: Self-Referential Island

```markdown
### [DELETE] Retired importer island is not live

- Item: `src/import/v1/**`, `tests/import-v1/**`, `docs/import-v1-migration.md`
- Current references: V1 files import each other; V1 tests import the V1 entry;
  one old migration doc links the old CLI command.
- Why references do not prove value: no current CLI command, route, package
  export, or runtime importer enters V1. Tests and docs only preserve retired
  V1 behavior.
- Live purpose test: failed.
- Deletion class: delete now.
- Evidence read: package exports, CLI command registry, import graph, V2 route,
  V1 tests, migration doc, git history after V2 landed.
- Expected risk if removed: low inside repo; external package export was
  already removed in the V2 migration.
- Recommended action: delete V1 code, V1 tests, and V1 migration doc together.
```

Why it is strong:

- It treats the whole cluster as one deletion candidate.
- It rejects tests and docs as weak proof because neither is attached to a live
  root.
- It names the real risk instead of using vague caution.

## Strong Finding: Test Hostage

```markdown
### [DELETE] Mock-only tests keep a dead adapter alive

- Item: `src/payments/legacyGatewayAdapter.ts` and
  `tests/payments/legacyGatewayAdapter.test.ts`
- Current references: one unit test file and one docs example.
- Why references do not prove value: tests mock the gateway and assert adapter
  method names; no payment path calls the adapter; docs example references a
  retired provider.
- Live purpose test: failed.
- Deletion class: delete now.
- Evidence read: payment route, provider registry, package exports, tests, docs
  example, git history for provider removal.
- Expected risk if removed: low; only dead tests break.
- Recommended action: delete adapter, test, and docs example.
```

Why it is strong:

- It reviews the test as an artifact, not as automatic keep proof.
- It does not ask for more tests.
- It explains that breaking the test is acceptable because the test protects
  retired behavior.

## Strong Finding: Low-Value Live Wrapper

```markdown
### [CONSOLIDATE] Pass-through registry adds a second owner for one implementation

- Item: `src/render/rendererRegistry.ts`
- Current references: current renderer path calls registry, but registry has
  one entry and one caller.
- Why references do not prove value: the registry is reachable, but it adds a
  concept without supporting multiple current renderers, runtime selection, or
  a plugin contract.
- Live purpose test: failed for the registry abstraction; passed for rendering
  behavior.
- Deletion class: consolidate.
- Evidence read: renderer call path, config, package exports, docs, tests.
- Expected risk if removed: medium; callers should move directly to the
  canonical renderer before deleting registry.
- Recommended action: inline current renderer ownership and delete the
  registry.
```

Why it is strong:

- It does not confuse reachability with value.
- It preserves the live behavior while deleting the low-value structure.
- It classifies the candidate as consolidation, not blind deletion.

## Strong Finding: Stale Feature Flag

```markdown
### [OWNER CHECK] Old onboarding flag preserves impossible branch

- Item: `onboarding_v1_enabled` flag branch
- Current references: code branch, env default, one old test, and one config
  doc.
- Why references do not prove value: production config always disables V1;
  rollout history shows V2 has been permanent; test asserts the retired V1
  branch.
- Live purpose test: failed.
- Deletion class: delete after one owner check.
- Evidence read: config defaults, deploy env docs, feature flag call sites,
  tests, git history.
- Expected risk if removed: medium if an untracked environment still sets the
  flag.
- Recommended action: ask whether any deployed environment still sets
  `onboarding_v1_enabled`; if not, delete branch, flag config, test, and doc.
```

Why it is strong:

- It names the exact missing fact.
- It does not use vague external-risk fear as a keep reason.
- It groups code, config, test, and doc together.

## Strong Finding: Worthless Snapshot Test

```markdown
### [DELETE] Snapshot test detects churn but protects no behavior

- Item: `tests/snapshots/full-dashboard-render.test.ts`
- Current references: live dashboard component and giant snapshot fixture.
- Why references do not prove value: the dashboard is live, but the test asserts
  the whole rendered structure and fails on harmless copy/layout changes
  without checking a user-visible invariant.
- Live purpose test: failed for the test, passed for the component.
- Deletion class: delete or rewrite only around current invariants.
- Evidence read: test body, component behavior, related targeted tests.
- Expected risk if removed: low if targeted behavior tests remain.
- Recommended action: delete the snapshot; add no replacement unless a current
  dashboard invariant is missing and the user asks for test strategy.
```

Why it is strong:

- It separates the live component from the low-value test.
- It avoids reflexive test expansion.
- It says what risk remains.

## Weak Findings

Weak:

```text
No references found, delete it.
```

Why weak:

- It stops at search instead of proving root reachability and deletion risk.

Weak:

```text
It is referenced in tests, keep it.
```

Why weak:

- It treats tests as proof instead of asking whether the tests protect current
  behavior.

Weak:

```text
This file looks messy and should be cleaned up.
```

Why weak:

- It is generic maintainability review, not deletion judgment.

Weak:

```text
Add tests before deleting this.
```

Why weak:

- It drifts into test strategy. The cruft review should name deletion value,
  current purpose, and deletion risk. It should ask for more tests only when
  the user explicitly requests test strategy.
