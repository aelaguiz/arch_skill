# Cynical Cruft Removal Skill Proposal

Date: 2026-06-26

Research base:
[Cruft, dead code, and low-value artifact research](CRUFT_DEAD_CODE_AND_LOW_VALUE_ARTIFACT_RESEARCH_2026-06-26.md)

Related local context:

- [Cynical code review skill proposal](CYNICAL_CODE_REVIEW_SKILL_PROPOSAL_2026-06-25.md)
- [Cynical architecture review intention](CYNICAL_ARCHITECTURE_REVIEW_INTENTION_2026-06-25.md)
- [Agent history recurring failure patterns](AGENT_HISTORY_RECURRING_FAILURE_PATTERNS_2026-06-25.md)
- [Agent history failure examples pack](agent_history_failure_examples_2026-06-25/README.md)

Status: implemented as
[`skills/cynical-cruft-removal/`](../skills/cynical-cruft-removal/) on
2026-06-26. Runtime doctrine lives in
[`skills/cynical-cruft-removal/SKILL.md`](../skills/cynical-cruft-removal/SKILL.md).

## Proposed Skill

```text
cynical-cruft-removal
```

Subtitle:

```text
Deep deletion report for low-value repo artifacts.
```

## Repeated User Problem

The user has a repo, branch, diff, subsystem, test suite, or artifact set that
has accumulated junk. Some junk is obvious dead code. The dangerous junk is
harder: tests that test nothing, tests that keep dead code alive, files that
only call each other, retired V1 systems left beside V2, stale feature flags,
old generated files, obsolete config, unused dependencies, stale examples, and
point-in-time docs that still look official.

The ordinary AI failure is to run a string search, find any reference, and keep
the artifact. That is not enough. References can be self-referential or stale.
They can launder the artifact through tests, docs, examples, generated files,
exports, and old wrappers.

The skill should force a deeper question:

```text
Does this artifact serve a current live purpose, or is it low-value residue
that should go away?
```

## Leverage Claim

This should be a reusable skill because the failure is repeated and specific:

- agents over-respect references
- agents keep low-value artifacts because deleting feels risky
- agents treat tests as proof instead of asking whether the test protects real
  behavior
- agents treat docs and examples as current truth when they may be stale
- agents miss clusters where code, tests, docs, generated files, and config keep
  each other alive
- agents report only "unused" items instead of judging purpose

A prompt-only skill can fix the posture without adding a runner. The work is
reasoning-heavy: identify live roots, trace purpose, challenge weak keep
stories, group deletion clusters, and produce a clear report.

## Canonical User Asks

```text
Use $cynical-cruft-removal on this repo and give me a deep report of low-value
items that should go away.
```

```text
Audit this test suite for worthless tests, tests that test mocks, tests that
only preserve dead code, and tests that should be deleted with the code they
keep alive.
```

```text
Find retired V1/V2 cruft, self-referential islands, stale feature flags, dead
configs, unused dependencies, generated junk, stale examples, and point-in-time
docs that no longer serve a live purpose.
```

## Anti-Case

Do not use this skill for ordinary code review, ordinary architecture review,
test coverage improvement, QA signoff, docs-only cleanup, formatting cleanup,
or implementation.

This skill can review tests and docs, but not as pedantic QA or docs hygiene.
It reviews them as possible low-value artifacts or as surfaces that keep stale
code alive.

## Proposed Trigger Description

Draft frontmatter description:

```yaml
description: "Run a prompt-only cynical cruft removal review over a repo, branch, diff, subsystem, test suite, or artifact set by assuming references are not proof of value. Produce a deep deletion report for low-value items that should go away: dead code, self-referential islands, retired V1/V2 paths, stale feature flags, worthless tests, fake coverage, unused dependencies, obsolete configs/scripts, stale generated artifacts, and point-in-time docs/examples that no longer serve a live purpose. Use when the user wants skeptical cleanup judgment and deletion candidates, not normal code review, docs-only cleanup, architecture review, implementation, or automated deletion."
```

Expected length: under the usual 1024-character runtime cap.

## Skill Lane And Peer Boundaries

### Lane

This is a prompt-only review utility.

It produces a saved, findings-first cleanup report. It does not edit, delete,
commit, push, open PRs, run external subprocess review, build a proof harness,
or own the user's broader workflow.

### Versus `arch-docs`

`arch-docs` owns stale-doc cleanup and canonical docs consolidation.

`cynical-cruft-removal` owns repo-wide low-value artifact review. Docs are only
one artifact type. They matter when they are stale themselves or when they
preserve stale code, old workflows, or retired APIs.

### Versus `cynical-code-review`

`cynical-code-review` asks whether an implementation story is truthful.

`cynical-cruft-removal` asks what should go away. It can use a plan, diff, or
completion claim as context, but the output is deletion judgment, not
implementation-integrity verdict.

### Versus `cynical-architecture-review`

`cynical-architecture-review` hunts accidental architecture and simplification
opportunities while preserving the intended UX.

`cynical-cruft-removal` is more artifact-centered. It hunts code, tests, docs,
examples, dependencies, configs, generated files, prompts, assets, data names,
and scripts whose current value does not justify keeping them.

### Versus `exhaustive-code-review`

`exhaustive-code-review` makes coverage part of the deliverable.

`cynical-cruft-removal` makes deletion value part of the deliverable. It should
be deep, but it is not a file-by-file coverage ledger unless that is required
to make deletion judgment honest.

### Versus `thermo-nuclear-code-quality-review`

`thermo-nuclear-code-quality-review` is a harsh maintainability review.

`cynical-cruft-removal` is not general harshness. It must name low-value items,
explain why they should go away, and separate real keep reasons from fake
reference proof.

## Proposed Runtime Mission

Review the requested target from a skeptical cleanup posture.

The reviewer should:

1. Identify current live roots.
2. Identify artifacts that claim to be live because they are referenced.
3. Trace whether those references come from real current roots or from stale,
   self-referential, generated, test-only, docs-only, or compatibility surfaces.
4. Separate artifacts with current purpose from artifacts with only historical,
   speculative, cosmetic, or self-preserving purpose.
5. Group deletion candidates into clusters so code, tests, docs, examples,
   generated files, exports, configs, and dependencies that keep each other
   alive can be removed together.
6. Save a deep report of low-value items that should go away.

## Non-Negotiables

- Review only. Do not edit or delete reviewed files unless the user explicitly
  asks for a follow-up implementation pass.
- Save the review artifact under
  `/tmp/cynical-cruft-removal/<slug>-<timestamp>/` unless the user explicitly
  asks for a repo doc path.
- This is prompt-only doctrine. Do not build a rule engine, runner, controller,
  scorer, harness, script, or formal parameter interface.
- Do not manually spawn `codex`, `claude`, `agent`, `grok`, or any other
  coding-harness executable.
- Do not invoke external agent, delegation, consult, or review skills as the
  review mechanism.
- Use native parallel agents only when the host already provides them, the
  target is broad enough, and the parent can account for every lane before
  finalizing.
- Start from distrust: references, exports, tests, docs, examples, generated
  files, prompts, comments, package metadata, compatibility wrappers, and old
  status text are claims, not proof of value.
- A reference proves a mention. It does not prove a live purpose.
- A test proves a test exists. It does not prove the code or behavior still
  matters.
- A doc proves someone wrote a doc. It does not prove the doc is current or the
  referenced artifact should stay.
- Current live purpose is the keep standard.
- Findings must be deletion-relevant. Drop generic style nits, missing-test
  requests, docs polish, formatting complaints, and normal QA concerns unless
  they expose low-value artifacts that should go away.
- A clean review is allowed, but only after likely hidden cruft patterns were
  checked and recorded honestly.

## Proposed First Move

1. Resolve the review target from natural language: current repo, current
   branch, diff, path set, subsystem, test suite, dependency set, generated
   artifacts, docs/examples surface, plan-backed cleanup scope, or user-named
   suspicious area.
2. Read local instructions and nearby conventions that define supported
   surfaces.
3. Create the run directory under `/tmp/cynical-cruft-removal/`.
4. Save `target.md`: target, scope, user concern, current branch/diff context,
   and any explicit exclusions.
5. Read the proposed skill references when implemented:
   `references/cruft-lenses.md`, `references/output-contract.md`, and
   `references/examples.md`.
6. Build an initial `live-root-map.md` before writing findings.

## Proposed Workflow

1. Save the target summary.
2. Identify live roots:
   - product/user workflows
   - runtime entrypoints
   - public APIs and package exports
   - build/install/deploy/release paths
   - plugin hooks and integration contracts
   - supported CLI commands and scripts
   - security, safety, migration, compliance, or data-retention obligations
   - tests that protect current live behavior
   - docs/examples/prompts that a current user or maintainer actually needs
3. Build a purpose map:
   - what artifacts claim to matter
   - what current purpose each artifact appears to serve
   - what owner or root proves that purpose
   - where the purpose is missing or suspect
4. Build a reference graph:
   - direct code references
   - tests
   - docs
   - examples
   - generated files
   - package exports
   - configs
   - scripts
   - prompts
   - data/schema/telemetry names when relevant
5. Challenge each reference:
   - Is the referring artifact itself live?
   - Does the reference come from a live root or a stale island?
   - Is this a current contract or a fossilized old contract?
   - Would removing the artifact break real current behavior, or only stale
     support surfaces?
6. Hunt hidden cruft clusters:
   - self-referential islands
   - test-hostage code
   - docs-laundered code
   - generated-artifact laundering
   - stale feature flags
   - compatibility ghosts
   - V1/V2 shadow systems
   - phantom public APIs
   - configuration cemeteries
   - oversized or unused dependencies
   - stale assets, locale keys, telemetry names, and examples
7. Review tests as artifacts:
   - identify tests that protect current behavior
   - identify tests that only import, snapshot, mock, duplicate implementation,
     pin internals, preserve retired behavior, or pad coverage
   - report tests that should be deleted or rewritten with their cruft cluster
   - do not ask for more tests unless the user explicitly requested test
     strategy
8. Review docs/examples/prompts as artifact supports:
   - identify stale point-in-time docs that look current
   - identify examples for retired APIs
   - identify prompt or instruction surfaces that teach old behavior
   - treat docs as secondary unless they keep code, tests, or workflows alive
9. Review dependencies/build/config:
   - unused dependencies
   - dependencies only used by retired tests or scripts
   - oversized dependencies for trivial use
   - stale package exports
   - dead Makefile/npm/CI commands
   - config keys and env vars for deleted modes
10. Use git history when retirement timing, migration completion, or old
    ownership matters.
11. Classify every candidate by deletion confidence.
12. Save `low-value-catalog.md`, `deletion-candidates.md`, `keep-decisions.md`,
    `coverage.md`, `findings.md`, and `verdict.md`.
13. Return a short findings-first reply with the verdict and run directory.

## Proposed Saved Artifact

The skill should save a Markdown review ledger:

```text
/tmp/cynical-cruft-removal/<scope-slug>-<timestamp>/
  target.md
  live-root-map.md
  purpose-map.md
  reference-graph-notes.md
  low-value-catalog.md
  test-bloat-report.md
  deletion-candidates.md
  keep-decisions.md
  coverage.md
  findings.md
  verdict.md
```

### `target.md`

Records:

- target
- user concern
- branch/diff/path scope
- plan or completion-claim context, if any
- explicit exclusions
- local instructions read

### `live-root-map.md`

Records:

- runtime roots
- build/install/deploy/release roots
- package exports and public APIs
- supported commands
- supported user workflows
- current safety/security/migration/data obligations
- current docs/tests/examples that actually belong to live behavior

### `purpose-map.md`

Records:

- artifact
- claimed purpose
- actual current purpose
- live root proving purpose, if any
- suspicious keep reason
- current owner, if found

### `reference-graph-notes.md`

Records:

- code references
- test references
- docs/examples/prompt references
- generated references
- config/build/package references
- data/schema/telemetry references
- self-referential islands
- references that were rejected as weak proof

### `low-value-catalog.md`

Groups all suspicious artifacts by type:

- dead code
- low-value live code
- tests
- docs/examples/prompts
- generated artifacts
- dependencies
- build/config/package metadata
- assets/locale/style artifacts
- data/telemetry/ops surfaces

### `test-bloat-report.md`

This is not a coverage report.

It records tests that should go away, tests that should be rewritten only if
the underlying current behavior still matters, and tests that keep dead code
alive.

### `deletion-candidates.md`

Records every delete/consolidate/quarantine candidate with deletion confidence
and cluster membership.

### `keep-decisions.md`

Records suspicious artifacts that survived review and why.

This file prevents a bad report shape where only delete candidates are visible
and the user cannot tell whether the reviewer checked obvious near misses.

### `coverage.md`

Records inspected files, commands, searches, graphs, history reads, native
parallel-agent lanes if used, and honest gaps.

This is evidence accounting, not proof theater.

### `findings.md`

Findings-first review. Each finding should be concrete, deletion-relevant, and
grounded in current repo evidence.

### `verdict.md`

Summarizes the result:

- verdict
- top deletion clusters
- highest-risk keep decisions
- unresolved owner checks
- next action

## Proposed Verdicts

```text
cruft-found
```

At least one material low-value artifact or cluster should be deleted,
consolidated, quarantined, or owner-checked for removal.

```text
no-material-cruft-found
```

The requested scope was reviewed and no material low-value removal candidate
was found. This verdict should be rare in messy scopes and must name the hidden
cruft patterns that were checked.

```text
scope-incomplete
```

The reviewer could not inspect enough roots, references, or owner surfaces to
make deletion judgment honestly.

```text
unsafe-to-judge
```

The repo contains external contract, data, migration, compliance, or production
state risk that blocks deletion judgment until a specific owner question is
answered. This verdict should name the exact missing fact.

## Proposed Finding Shape

Use this structure:

```text
Finding: <short deletion-relevant title>
Item: <path/symbol/artifact/cluster>
Current references: <where it is mentioned>
Why references do not prove value: <stale/self-referential/test/docs/generated/etc.>
Live purpose test: <passed/failed/unclear, with reason>
Deletion class: <delete now/delete after owner check/quarantine/consolidate/keep>
Evidence read: <files/commands/history/surfaces>
Expected risk if removed: <real breakage risk, not vague fear>
Recommended action: <delete/rewrite/consolidate/owner-check>
```

## Deletion Classes

### Delete Now

Use when there is no current live root and references are self-referential,
stale, generated, tests-only, docs-only, or example-only.

### Delete After One Owner Check

Use when the repo evidence points to deletion, but a narrow external fact could
change the answer.

Good owner check:

```text
Does any supported external integration still import `legacyExport` from the
published package?
```

Bad owner check:

```text
Maybe someone uses this somewhere.
```

### Quarantine

Use when deletion is probably right but order matters, such as data migrations,
production flags, public contracts, or safety paths.

### Consolidate

Use when the artifact has a live behavior but the owner is wrong or duplicated.
The recommendation should move live behavior to the canonical owner, then
delete the duplicate.

### Keep

Use when a current root and current purpose are both clear. The keep decision
must say what current behavior, contract, or invariant would be harmed by
removal.

## Example Findings

### Example 1: Self-Referential Island

```text
Finding: Retired importer island is not live
Item: src/import/v1/**, tests/import-v1/**, docs/import-v1-migration.md
Current references: V1 files import each other; V1 tests import the V1 entry;
one old migration doc links the old CLI command.
Why references do not prove value: no current CLI command, route, package
export, or runtime importer enters V1. Tests and docs only preserve retired V1
behavior.
Live purpose test: failed.
Deletion class: delete now.
Evidence read: package exports, CLI command registry, import graph, V2 route,
V1 tests, migration doc, git history after V2 landed.
Expected risk if removed: low inside repo; external package export was already
removed in the V2 migration.
Recommended action: delete V1 code, V1 tests, and V1 migration doc together.
```

### Example 2: Test Hostage

```text
Finding: Mock-only tests keep a dead adapter alive
Item: src/payments/legacyGatewayAdapter.ts and
tests/payments/legacyGatewayAdapter.test.ts
Current references: one unit test file and one docs example.
Why references do not prove value: tests mock the gateway and assert adapter
method names; no payment path calls the adapter; docs example references a
retired provider.
Live purpose test: failed.
Deletion class: delete now.
Evidence read: payment route, provider registry, package exports, tests, docs
example, git history for provider removal.
Expected risk if removed: low; only dead tests break.
Recommended action: delete adapter, test, and docs example.
```

### Example 3: Low-Value Live Wrapper

```text
Finding: Pass-through registry adds a second owner for one implementation
Item: src/render/rendererRegistry.ts
Current references: current renderer path calls registry, but registry has one
entry and one caller.
Why references do not prove value: the registry is reachable, but it adds a
concept without supporting multiple current renderers, runtime selection, or a
plugin contract.
Live purpose test: failed for the registry abstraction; passed for rendering
behavior.
Deletion class: consolidate.
Evidence read: renderer call path, config, package exports, docs, tests.
Expected risk if removed: medium; callers should move directly to canonical
renderer before deleting registry.
Recommended action: inline current renderer ownership and delete the registry.
```

### Example 4: Stale Feature Flag

```text
Finding: Old onboarding flag preserves impossible branch
Item: onboarding_v1_enabled flag branch
Current references: code branch, env default, one old test, and one config doc.
Why references do not prove value: production config always disables V1; rollout
history shows V2 has been permanent; test asserts the retired V1 branch.
Live purpose test: failed.
Deletion class: delete after one owner check.
Evidence read: config defaults, deploy env docs, feature flag call sites, tests,
git history.
Expected risk if removed: medium if an untracked environment still sets the
flag.
Recommended action: ask whether any deployed environment still sets
`onboarding_v1_enabled`; if not, delete branch, flag config, test, and doc.
```

### Example 5: Worthless Snapshot Test

```text
Finding: Snapshot test detects churn but protects no behavior
Item: tests/snapshots/full-dashboard-render.test.ts
Current references: live dashboard component, giant snapshot fixture.
Why references do not prove value: the dashboard is live, but the test asserts
the whole rendered structure and fails on harmless copy/layout changes without
checking a user-visible invariant.
Live purpose test: failed for the test, passed for the component.
Deletion class: delete or rewrite only around current invariants.
Evidence read: test body, component behavior, related targeted tests.
Expected risk if removed: low if targeted behavior tests remain.
Recommended action: delete the snapshot; add no replacement unless a current
dashboard invariant is missing and the user asks for test strategy.
```

## Report Quality Bar

Great output feels like a ruthless maintainer walked the repo with a map of
what actually matters.

It should:

- name deletion clusters, not isolated trivia
- explain why each candidate lacks current purpose
- show why references do not rescue the candidate
- distinguish dead code from low-value live code
- identify tests that should disappear, not ask for more tests by reflex
- treat docs as secondary unless they preserve stale truth
- name external-risk owner checks precisely
- include suspicious keep decisions
- give the user a report they can hand to an implementer

Weak output:

- lists only files with zero references
- says "referenced, keep" without purpose analysis
- focuses on style nits
- asks for more tests or docs by habit
- reports one file at a time when a cluster should be deleted together
- avoids deletion recommendations because deletion feels risky
- builds a harness instead of doing the review

## Proposed Reference Files If Implemented

Start lean. A viable first package could be:

```text
skills/cynical-cruft-removal/
  SKILL.md
  references/
    cruft-lenses.md
    output-contract.md
    examples.md
```

Do not add scripts unless repeated real runs show a deterministic helper is
needed for bounded graph extraction or report templating. Even then, the script
must be a helper, not the workflow owner.

### `SKILL.md`

Owns:

- trigger contract
- use and do-not-use boundaries
- non-negotiables
- first move
- workflow
- output expectations
- reference map

### `references/cruft-lenses.md`

Owns:

- live purpose model
- root types
- hidden cruft patterns
- deletion classes
- test-bloat lenses
- dependency/build/config lenses
- docs/examples/generated-artifact lenses

### `references/output-contract.md`

Owns:

- saved artifact layout
- verdict definitions
- finding shape
- coverage accounting
- final chat response shape

### `references/examples.md`

Owns:

- self-referential island example
- test hostage example
- V1/V2 shadow example
- stale feature flag example
- low-value live wrapper example
- stale docs/generated artifact example

Examples must teach reasoning. They must not become a finite checklist.

## Draft `SKILL.md` Shape

The eventual runtime skill should be concise. Suggested shape:

```markdown
# Cynical Cruft Removal

Use this skill when the user wants a skeptical cleanup review that produces a
deep report of low-value repo items that should go away.

The job is to distrust reference-count proof, identify live roots, trace
current purpose, find dead or low-value clusters across code/tests/docs/configs/
dependencies/generated artifacts, save a deletion report, and return the
verdict plus path.

This skill does not edit files, delete files, commit, push, open PRs, run a
cleanup harness, or become normal QA/test/docs review.
```

Then include:

- `Use When`
- `Do Not Use When`
- `Non-Negotiables`
- `First Move`
- `Workflow`
- `Output Expectations`
- `Reference Map`

Keep the detailed taxonomy in references, not in `SKILL.md`.

## Proposed Final Chat Reply Shape

When the skill runs, the chat reply should be short:

```text
Verdict: cruft-found

Top deletion clusters:
- src/import/v1/** with V1 tests and migration doc: no live root reaches V1.
- legacy renderer registry: reachable but low-value; one caller, one entry,
  no plugin contract.
- dashboard full snapshot: protects no current behavior and creates churn.

Run directory: /tmp/cynical-cruft-removal/<scope-slug>-<timestamp>/

Next action: delete cluster 1 first; owner-check the stale feature flag before
deleting cluster 2.
```

The full report carries the detail. The chat reply should not paste the whole
artifact unless the user asks.

## Implementation Plan

Implemented on 2026-06-26:

1. Add `skills/cynical-cruft-removal/SKILL.md`.
2. Add references:
   - `references/cruft-lenses.md`
   - `references/output-contract.md`
   - `references/agent-slices.md`
   - `references/examples.md`
3. Add the skill to install inventory in `Makefile` and `README.md` if this
   repo's install surface requires explicit listing.
4. Add routing guidance to `AGENTS.md`, `README.md`, and
   `docs/arch_skill_usage_guide.md` if the skill becomes shipped surface.
5. Run `npx skills check` after touching `skills/`.
6. Run install-surface verification only if install behavior changes.

## Open Design Decisions

### Name

Recommended: `cynical-cruft-removal`.

Reason:
The user wants removal energy and a report of things that should go away. The
skill is review-only by default, but the name keeps the deletion bias clear.

Alternative: `cynical-cruft-audit`.

Reason to reject for now:
`audit` sounds safer and weaker. It may invite generic findings instead of the
deep deletion report the user wants.

### Agent Slices

The eventual skill can support native parallel agents for broad scopes, using
slices such as:

- live-root mapping
- self-referential island search
- test-bloat review
- dependency/build/config review
- docs/examples/generated-surface review
- V1/V2 and stale-flag review

But this must stay native-agent prompt work. Do not create an external worker
swarm, subprocess launcher, or deterministic controller.

### Deletion Versus Report

Default behavior should be report-only.

Reason:
The skill's main value is judgment. Deletion can be a follow-up implementation
task after the user approves the report or selects clusters.

If the user explicitly asks for cleanup execution later, that should be a
separate implementation turn or a future execution mode, not hidden inside the
review skill.

## Final Proposal

Build `cynical-cruft-removal` as a prompt-only, review-only skill whose output
is a deep saved report of low-value artifacts that should go away.

Its core doctrine:

```text
References are not value. Current purpose is value.
```

Its report must go deeper than unused-file detection. It should find
self-referential islands, test-hostage code, stale feature flags, retired V1/V2
systems, worthless tests, dependency/build/config bloat, stale generated
artifacts, and docs/examples/prompts that keep dead behavior alive.

The skill should not focus on QA, missing tests, docs polish, or proof
harnesses. It should focus on the repo surfaces that no longer earn their
place, explain why they should be removed, and give the user a deletion-ready
report.
