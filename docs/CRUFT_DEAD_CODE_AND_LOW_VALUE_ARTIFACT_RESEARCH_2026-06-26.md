# Cruft, Dead Code, And Low-Value Artifact Research

Date: 2026-06-26

Companion proposal:
[Cynical cruft removal skill proposal](CYNICAL_CRUFT_REMOVAL_SKILL_PROPOSAL_2026-06-26.md)

Implemented runtime skill:
[`skills/cynical-cruft-removal/`](../skills/cynical-cruft-removal/)

Related local context:

- [Cynical architecture review intention](CYNICAL_ARCHITECTURE_REVIEW_INTENTION_2026-06-25.md)
- [Cynical code review skill proposal](CYNICAL_CODE_REVIEW_SKILL_PROPOSAL_2026-06-25.md)
- [Agent history recurring failure patterns](AGENT_HISTORY_RECURRING_FAILURE_PATTERNS_2026-06-25.md)
- [Agent history failure examples pack](agent_history_failure_examples_2026-06-25/README.md)

Status: research and doctrine source for a proposed prompt-only skill. This is
not an implemented runtime skill.

## Bottom Line

Cruft is not only code with zero references.

Cruft is any code, test, doc, dependency, config, asset, generated file, prompt,
example, or workflow surface that consumes maintenance attention while no
longer serving a current purpose.

The hard part is that low-value artifacts often have references. A bad artifact
can be kept alive by tests, docs, examples, generated metadata, compatibility
wrappers, exports, old scripts, or another dead artifact. A string match proves
that something points at it. It does not prove that the thing still matters.

The proposed skill should therefore ask:

```text
What live purpose does this artifact serve today?
```

Not:

```text
Can I find any reference to it?
```

## Research Claim

The best cleanup work is not a mechanical unused-code pass. It is a purpose
audit.

A reviewer should identify live roots, trace what actually reaches them, then
challenge every remaining "keep" story:

- Is this reached by a current product, runtime, build, deploy, install, safety,
  migration, or owner workflow?
- Is this only referenced by tests, docs, examples, generated files, prompts,
  or old compatibility surfaces?
- If we removed it, what real current behavior would break?
- If it only teaches, preserves, or documents retired behavior, why is git
  history not the archive?

That posture is especially important for AI-written code. Agent history shows
the repeated failure pattern: the agent treats names, comments, docs, tests,
status blocks, wrappers, and reviewer receipts as proof. The cleanup skill must
do the opposite. It must treat those surfaces as claims to verify.

## Source Synthesis

### Martin Fowler: technical debt is a maintenance drag, and YAGNI prevents speculative waste

Sources:

- [Technical Debt](https://martinfowler.com/bliki/TechnicalDebt.html)
- [Yagni](https://martinfowler.com/bliki/Yagni.html)

Useful idea:
Fowler's technical debt framing is about the future cost of internal quality
problems. YAGNI says not to build capability just because it might be useful
later.

Cruft-removal translation:

- Code can be reachable and still be debt if it makes future change harder
  without serving a current purpose.
- Speculative hooks, general frameworks, adapters, options, flags, and API
  surfaces should not survive merely because someone imagined a future use.
- A retired implementation does not become valuable because it was once
  carefully designed.

Review question:

```text
Is this artifact serving today's system, or only preserving yesterday's idea or
tomorrow's guess?
```

### John Ousterhout: complexity appears as change amplification, cognitive load, and unknown unknowns

Sources:

- [Stanford CS190 complexity notes](https://web.stanford.edu/~ouster/cgi-bin/cs190-spring16/lecture.php?topic=complexity)
- [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php)

Useful idea:
Ousterhout frames complexity as anything that makes software hard to understand
or change. His common symptoms include needing to touch many places for a small
change, needing to hold too much in mind, and being surprised by hidden
dependencies.

Cruft-removal translation:

- A low-value artifact is not harmless if maintainers must remember it, route
  around it, keep it compatible, configure it, or avoid breaking stale tests.
- Dead islands matter even when they do not execute, because they add cognitive
  load and create false choices for future work.
- A wrapper, alias, compatibility branch, or duplicate config key can be cruft
  even if it is technically reachable.

Review question:

```text
What extra thing must a future maintainer understand because this still exists?
```

### Parnas and Lehman: software ages unless change actively fights decay

Sources:

- [Parnas, Software Aging](https://www.cs.toronto.edu/~chechik/courses18/csc2125/paper3.pdf)
- [Lehman's laws of software evolution](https://dl.acm.org/doi/10.1145/101146.101150)

Useful idea:
Software systems change under pressure. Unless the structure is actively
maintained, adaptation accumulates complexity and the system ages.

Cruft-removal translation:

- Retired versions, compatibility ghosts, old toggles, and "temporary" shims
  are normal aging products.
- The fact that something grew historically is not proof that it is still part
  of the intended design.
- Cleanup is not cosmetic. It is how a system resists age.

Review question:

```text
Which artifacts exist because change happened, not because current design needs
them?
```

### Brooks: separate essential complexity from accidental complexity

Source:
[No Silver Bullet](https://www.cs.unc.edu/techreports/86-020.pdf)

Useful idea:
Brooks distinguishes problem complexity that is inherent from accidental
complexity created by representation, tools, or implementation choices.

Cruft-removal translation:

- Do not delete requirements. Delete accidental residue around requirements.
- A cleanup review must preserve the intended user experience, public contract,
  safety invariant, and hard experiment requirement.
- A deletion candidate is strongest when the same real behavior survives with
  fewer concepts, fewer files, fewer owners, and fewer future decisions.

Review question:

```text
What part of this artifact is forced by the problem, and what part is just how
we happened to build it?
```

### Refactoring literature: code smells include bloaters, speculative generality, lazy classes, duplicate code, and dead code

Sources:

- [Refactoring catalog](https://refactoring.com/catalog/)
- [Refactoring Guru code smells catalog](https://refactoring.guru/refactoring/smells)

Useful idea:
Classic code-smell catalogs recognize that harmful code is not only broken
code. Long methods, duplicate code, speculative generality, lazy classes, data
classes, and dead code are all signs that structure no longer pays for itself.

Cruft-removal translation:

- "It works" is too low a bar.
- A class, module, helper, abstraction, or config layer should earn its
  existence.
- A tiny object that only forwards calls, an abstraction with one real
  implementation, or a generic layer used by one local case can be negative
  value.

Review question:

```text
Does this artifact pay rent, or does it only make the system look more
architected?
```

### Google testing guidance and xUnit patterns: tests can become cruft too

Sources:

- [Software Engineering at Google, Testing Overview](https://abseil.io/resources/swe-book/html/ch11.html)
- [Software Engineering at Google, Unit Testing](https://abseil.io/resources/swe-book/html/ch12.html)
- [Software Engineering at Google, Test Doubles](https://abseil.io/resources/swe-book/html/ch13.html)
- [Google Testing Blog, Change Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html)
- [xUnit Patterns, Test Smells](http://xunitpatterns.com/Test%20Smells.html)

Useful idea:
Tests are code. They need maintenance. A bad test can reduce confidence,
increase friction, lock implementation details, or preserve obsolete behavior.

Cruft-removal translation:

- A test reference can be evidence that code is still valuable, but it can also
  be evidence that the test is keeping dead behavior alive.
- Tests that only import modules, snapshot huge unstable output, assert
  implementation details, test mocks instead of behavior, or duplicate the
  implementation logic may be low value.
- Coverage is not value. A test should protect a current behavior or invariant
  that matters.

Review question:

```text
If this test disappeared, what real current bug would become more likely?
```

### Piranha and stale feature flags: flags and compatibility paths create dead-code roots

Sources:

- [Uber Engineering, Piranha](https://www.uber.com/blog/piranha/)
- [Piranha paper](https://arxiv.org/abs/2004.13654)

Useful idea:
Feature flags often leave stale branches behind. Piranha exists because stale
flag cleanup is a recurring, automatable source of dead code and complexity.

Cruft-removal translation:

- A stale flag can create the illusion of two supported behaviors when only one
  is real.
- A compatibility branch can be reachable by syntax while unreachable by
  current rollout state.
- Flags deserve current-state proof, not "there is an if statement" proof.

Review question:

```text
Is this branch reachable in the real product state, or only in a retired flag
state?
```

### OWASP: dependency size is a supply-chain and maintainability risk

Source:
[OWASP Top 10 Risks for Open Source Software](https://owasp.org/www-project-open-source-software-top-10/)

Useful idea:
Dependencies can be too small, too large, too indirect, or too poorly matched
to the actual need. Over-sized dependency use increases the inherited surface
area.

Cruft-removal translation:

- An unused dependency is obvious cruft.
- A dependency used once for a trivial operation can also be cruft if the
  project inherits more API, security, update, build, and transitive-dependency
  surface than the problem deserves.
- Dev dependencies that only support retired tests or obsolete generators are
  also cleanup candidates.

Review question:

```text
Does this dependency solve a current problem at the right size, or does it drag
around a larger world than the repo needs?
```

### Large-scale dead code work: dead code includes data, generated artifacts, and ecosystem references

Sources:

- [Meta Engineering, Automating dead code cleanup](https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/)
- [Dead code removal at Meta, ESEC/FSE 2023 industry paper listing](https://2023.esec-fse.org/details/fse-2023-industry/12/Dead-Code-Removal-at-Meta-Automatically-Deleting-Millions-of-Lines-of-Code-and-Petab)

Useful idea:
At large scale, dead code is not only unreachable functions. It includes
deprecated data, generated artifacts, and ecosystem references that make
deletion hard.

Cruft-removal translation:

- Generated files and data surfaces can keep retired concepts visible after the
  source owner is gone.
- Deletion judgment needs graph thinking, not isolated file thinking.
- A current-looking reference may be the residue of an obsolete generator,
  schema, fixture, or data pipeline.

Review question:

```text
Is this artifact live from a real root, or is it being repeated by a stale
generator, schema, fixture, or data copy?
```

## Working Definition Of "Live Purpose"

An artifact has a live purpose only if it serves at least one current root.

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

## Cruft Taxonomy

### 1. Dead Code

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

### 2. Low-Value Live Code

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

This is the class a string search misses most often. The artifact is "used,"
but the use is not valuable.

### 3. Test Bloat And Test Cruft

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

Cleanup posture:

```text
Do not ask "does this test reference the code?"
Ask "what current behavior or invariant does this test protect?"
```

### 4. Documentation, Prompt, And Example Cruft

Docs are not the main focus of the proposed skill, but they can keep dead
systems alive.

Common forms:

- point-in-time plan docs that are no longer current operating truth
- old worklogs that read like instructions
- examples for retired APIs
- README sections that describe removed or unsupported commands
- prompt files that teach old behavior
- generated docs copied from obsolete metadata
- diagrams that preserve old ownership
- docs that only cite other stale docs
- "migration complete" notes that keep both old and new systems conceptually
  alive

Cleanup posture:

```text
If a doc is the only reason an old thing looks live, the doc is suspect too.
```

### 5. Dependency, Build, And Config Cruft

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

Cleanup posture:

```text
Build metadata is code. It can preserve dead behavior just as effectively as a
source file.
```

### 6. Data, Telemetry, And Ops Cruft

Common forms:

- dead database columns and tables
- retired event names
- old analytics dimensions
- dashboards for removed workflows
- alerts tied to obsolete systems
- migration states that cannot occur anymore
- old queue topics, cron jobs, and worker names
- data copies retained because no one proved the current root

Cleanup posture:

```text
Data and ops cleanup needs more caution than local code cleanup, but references
still do not prove current purpose.
```

## Hidden Cruft Patterns

### Self-Referential Island

Several files reference each other, and a string search makes them look alive.
No live root reaches the island.

Signal:

- all inbound references come from the island itself, tests for the island, old
  docs, examples, generated metadata, or package exports no current consumer
  uses

Reviewer move:

- identify root reachability, not only local references
- classify as deletion candidate or quarantine candidate

### Reference Laundering

A weak reference gets treated as strong evidence because it appears in an
official-looking file.

Examples:

- generated metadata references old command
- docs cite retired helper
- test imports old API
- package export exposes old symbol
- compatibility shim calls old path to preserve a name

Reviewer move:

- ask whether the referring artifact itself has a live purpose

### Test Hostage

Dead code stays because tests still expect it.

Signal:

- code is only used by tests
- tests describe retired behavior
- deleting the code would only break tests with no current product impact

Reviewer move:

- treat the test as part of the cruft cluster
- recommend deleting or rewriting the test with the code

### Docs Laundering

Docs keep old behavior plausible after code moved on.

Signal:

- docs are the only current reference to a command, workflow, option, class, or
  old owner
- docs contain status language that sounds current but no live root agrees

Reviewer move:

- mark the doc as stale-supporting cruft, not keep evidence

### Generated Artifact Laundering

Generated files keep repeating old names after the source owner changed or
disappeared.

Signal:

- generated file references old API
- generator source is gone, retired, or points to stale metadata
- no current build path regenerates the artifact

Reviewer move:

- trace source-of-truth generation path before accepting the reference

### Compatibility Ghost

A compatibility wrapper, old export, alias, flag branch, or fallback path stays
after the compatibility need is gone.

Signal:

- no current consumer requires the old name or behavior
- comments say "temporary," "legacy," "for now," "backcompat," or "TODO"
- git history shows the migration completed long ago

Reviewer move:

- identify current consumers; if none, recommend deletion or a short
  deprecation task with owner check

### V1/V2 Shadow System

V2 is current, but V1 remains partially wired through tests, docs, examples,
config, scripts, or exports.

Signal:

- both systems can be found by search
- only V2 is used by the product path
- V1 survives because removing it breaks old tests or documentation examples

Reviewer move:

- report the whole shadow system as one deletion cluster, not as isolated files

### Phantom Public API

Something is exported or documented like a public contract, but no current user
depends on it.

Signal:

- export map includes symbols with no external consumer
- docs imply support, but no integration path uses it
- code exists to preserve a name rather than a behavior

Reviewer move:

- distinguish "public in syntax" from "public in obligation"

### Configuration Cemetery

Config options accumulate after the code paths they select are retired.

Signal:

- env var, YAML key, feature flag, package script, CI matrix entry, or runtime
  option is read but no current deployment sets a meaningful alternative
- default branch is the only real branch

Reviewer move:

- trace actual environment/deploy/install use, not only parser reads

## Deletion Judgment Model

Use a confidence tier, not a binary keep/delete answer.

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

- artifact looks dead, but external consumers, deployed config, data retention,
  migration, or security requirements could exist outside the repo
- owner check is small and specific

Expected report action:

```text
Ask <specific owner/system question>, then delete if no current obligation is
found.
```

### Quarantine Or Mark Retired

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
- deletion should happen by moving the live responsibility to the canonical
  owner first

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

## Evidence The Skill Should Read

A deep cleanup report should inspect the smallest set of evidence that can
answer purpose, not just reference count.

Useful evidence:

- runtime entrypoints and route maps
- package exports and public APIs
- build, install, deploy, and release commands
- CLI commands and scripts
- import/call/reference graph
- tests that reference the artifact
- docs, examples, prompts, and generated surfaces that reference it
- feature flags, config keys, env vars, and rollout state
- package manifests and lockfiles
- telemetry names, data migrations, and storage schemas when relevant
- git history for retirement timing, migration completion, and old owner
  boundaries
- local instructions that define supported surfaces

The skill should use broad `rg` search, but it must not stop there. Search is
only a map of mentions. It is not a map of value.

## Relationship To Existing Skills

### Versus `arch-docs`

`arch-docs` cleans stale documentation and consolidates docs onto canonical
homes.

The proposed cruft skill is repo-wide low-value artifact review. Docs are only
one surface, and they matter mostly when they preserve stale code, retired APIs,
old workflows, or misleading future instructions.

### Versus `cynical-code-review`

`cynical-code-review` asks whether an implementation story is truthful.

The proposed cruft skill asks whether artifacts should still exist. It can use
a completion claim as context, but its center is deletion value, not whether a
plan was implemented.

### Versus `cynical-architecture-review`

`cynical-architecture-review` asks whether the architecture emerged
accidentally and should be simplified while preserving the same UX.

The proposed cruft skill is lower and broader: code, tests, docs, dependencies,
configs, assets, data names, generated files, prompts, and examples can all be
deletion candidates. Architecture may explain why a cluster should be
consolidated, but the cruft skill's output is a report of low-value things that
should go away.

### Versus `exhaustive-code-review`

`exhaustive-code-review` treats coverage as the deliverable.

The proposed cruft skill treats deletion judgment as the deliverable. It should
be deep, but not because it must account for every touched hunk. It is deep
because it traces purpose, roots, and low-value clusters.

### Versus `thermo-nuclear-code-quality-review`

`thermo-nuclear-code-quality-review` is a harsh maintainability review.

The proposed cruft skill is not generic harshness. It should name what can
disappear, why references do not rescue it, what risk deletion carries, and
what cluster should be removed together.

## What A Strong Report Must Contain

The output of the future skill should be a deep report, not a quick list.

Required substance:

- target and scope
- live roots inspected
- purpose map
- reference graph notes
- deletion candidate clusters
- low-value live-code candidates
- worthless or negative-value tests
- docs/examples/prompts/generated surfaces that preserve stale behavior
- dependency/build/config cruft
- confidence tier for each candidate
- expected deletion risk
- exact reason references do not prove value
- recommended action
- explicit keep decisions for suspicious artifacts that survived review
- coverage gaps where deletion judgment would be dishonest

The strongest findings should read like this:

```text
Item: src/v1/importer.ts and tests/v1-importer.test.ts
Current references: one package export, three tests, one old docs page
Why references do not prove value: no runtime route, CLI command, package
consumer, or current docs path enters V1; tests assert retired behavior; docs
page is a point-in-time migration note
Live purpose test: failed
Deletion class: delete now as a cluster
Risk: low; package export removal should be noted if this repo has external
consumers
Recommended action: delete V1 importer, its tests, and the stale docs section
together
```

Weak output:

```text
No references found, delete it.
```

Also weak:

```text
It is referenced in tests, keep it.
```

## Core Doctrine For The Proposed Skill

1. References are clues, not proof.
2. A current root plus a current purpose is the keep standard.
3. Tests, docs, examples, generated files, and exports can launder dead code.
4. A self-referential island is still dead if no live root enters it.
5. Low-value live code can be worse than dead code because it actively shapes
   future work.
6. Test cleanup is about deleting worthless tests and tests that preserve dead
   behavior, not asking for more coverage.
7. Docs cleanup is not the center, but docs can be deletion evidence or stale
   support structures.
8. Git history is the archive for retired ideas.
9. Deletion should be cluster-aware. Delete the dead code, tests, docs,
   examples, generated artifacts, exports, and configs that keep each other
   alive.
10. When deletion risk depends on external contracts, name the exact owner
    check instead of using vague caution as a keep reason.
