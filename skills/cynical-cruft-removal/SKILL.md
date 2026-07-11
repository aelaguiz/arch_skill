---
name: cynical-cruft-removal
description: "Run a prompt-only cynical cruft removal review over a repo, branch, diff, subsystem, test suite, or artifact set by assuming references are not proof of value. Produce a deep deletion report for low-value items that should go away: dead code, self-referential islands, retired V1/V2 paths, stale feature flags, worthless tests, fake coverage, unused dependencies, obsolete configs/scripts, stale generated artifacts, and point-in-time docs/examples that no longer serve a live purpose. Use when the user wants skeptical cleanup judgment and deletion candidates, not normal code review, docs-only cleanup, architecture review, implementation, or automated deletion."
metadata:
  short-description: "Deep deletion report for low-value repo artifacts"
---

# Cynical Cruft Removal

Use this skill when the user wants a skeptical cleanup review that produces a
deep report of low-value repo items that should go away.

The job is to distrust reference-count proof, identify live roots, trace current
purpose, find dead or low-value clusters across code, tests, docs, configs,
dependencies, generated artifacts, assets, prompts, examples, scripts, and data
surfaces, save a deletion report, and return the verdict plus path.

This skill does not edit files, delete files, commit, push, open PRs, run
external review subprocesses, build a cleanup harness, or decide the user's
broader workflow.

## Use When

- The user asks for cynical, skeptical, adversarial, or deep cruft cleanup
  review.
- The user wants a report of low-value items that should go away from a repo,
  branch, diff, path set, subsystem, test suite, dependency set, generated
  artifact set, or docs/examples/prompt surface.
- The user says ordinary reference search is too shallow and wants the review
  to challenge whether references prove real value.
- The user wants to find dead code, self-referential islands, retired V1/V2
  paths, stale feature flags, compatibility ghosts, phantom public APIs,
  configuration cemeteries, unused or oversized dependencies, stale generated
  artifacts, point-in-time docs, stale examples, or prompt surfaces that keep
  retired behavior alive.
- The user wants tests reviewed as artifacts: worthless tests, tests that test
  mocks, fake coverage, brittle snapshots, tests for retired behavior, or tests
  that keep dead code alive.

## Do Not Use When

- The user wants a normal high-signal bug-focused code review. Use the host
  agent's normal review response.
- The user wants exhaustive line-by-line, file-by-file, or coverage-ledger
  review where coverage itself is the deliverable. Use
  `exhaustive-code-review`.
- The user wants skeptical implementation completion review: "did this plan
  really get implemented, or is the completion story lying?" Use
  `cynical-code-review`.
- The user wants accidental architecture and subtraction review while
  preserving the same UX or experiment requirements. Use
  `cynical-architecture-review`.
- The user wants stale-doc cleanup and canonical docs consolidation. Use
  `arch-docs`.
- The user wants only a harsh maintainability, spaghetti, file-size, or
  code-judo pass. Use `thermo-nuclear-code-quality-review`.
- The user wants QA signoff, test coverage improvement, release readiness,
  docs polish, formatting cleanup, implementation, deletion, PR shipping, or
  workflow orchestration.

## Non-Negotiables

- Review only. Do not edit or delete reviewed files unless the user explicitly
  asks for a follow-up implementation pass.
- Save the review artifact under
  `/tmp/cynical-cruft-removal/<slug>-<timestamp>/` unless the user explicitly
  asks for a repo doc path.
- This is prompt-only doctrine. Do not build a rule engine, runner, controller,
  scorer, harness, script, or formal parameter interface.
- Maximize native parallel agents for broad review targets when available.
  Account for every launched lane before finalizing.
- Do not manually spawn `codex`, `claude`, `agent`, `grok`, or any other
  coding-harness executable.
- Do not invoke external agent, delegation, consult, or review skills as the
  review mechanism.
- Start from distrust: references, exports, tests, docs, examples, generated
  files, prompts, comments, package metadata, compatibility wrappers, and old
  status text are claims, not proof of value.
- A reference proves a mention. It does not prove a live purpose.
- A test proves a test exists. It does not prove the code or behavior still
  matters.
- A doc proves someone wrote a doc. It does not prove the doc is current or the
  referenced artifact should stay.
- Current live purpose is the keep standard.
- For plan-, branch-, conductor-, PR-, or history-backed work, current
  reachability and product use do not prove the work was authorized. Apply
  `skills/_shared/scope-and-convergence.md`: reconstruct the initial human
  scope, frozen initial convergence closure, later human approvals, review
  waves, and final code. A live cluster created through unauthorized
  post-freeze expansion or scope cycling is cruft and forces `cruft-found`.
- Group scope-laundered code with the tests, schemas, configs, dependencies,
  docs, prompts, and operational surfaces that keep it alive. The normal action
  is subtraction of the cluster. If provenance should exist but cannot be
  recovered, return `scope-incomplete`; mark the lane not applicable only for a
  standalone target with no scope story.
- Findings must be deletion-relevant. Drop generic style nits, missing-test
  requests, docs polish, formatting complaints, and normal QA concerns unless
  they expose low-value artifacts that should go away.
- A clean review is allowed, but only after likely hidden cruft patterns were
  checked and recorded honestly.

## First Move

1. Resolve the requested review target from natural language: current repo,
   current worktree, branch diff, commit range, explicit paths, subsystem, test
   suite, dependency set, generated artifacts, docs/examples/prompt surface, or
   user-named suspicious area.
2. Read local instructions and nearby conventions that define supported
   surfaces.
3. Create the run directory under `/tmp/cynical-cruft-removal/`.
4. Save `target.md`: target, scope, user concern, current branch/diff context,
   supplied plan or cleanup claim if any, explicit exclusions, and local
   instructions read.
5. When scope history exists, reconstruct the human baseline, frozen closure,
   later human approvals, and review waves before accepting current liveness as
   keep evidence.
6. Read `references/cruft-lenses.md`.
7. Read `references/output-contract.md`.
8. Read `references/agent-slices.md` before launching native parallel agents.
9. Read `references/examples.md` when the target involves tests, docs,
   generated artifacts, self-referential islands, V1/V2 paths, stale flags,
   dependencies, or confusing peer review lanes.

## Workflow

1. Save the target summary as `target.md`.
2. Build `live-root-map.md`: product/user workflows, runtime entrypoints,
   public APIs and package exports, build/install/deploy/release paths,
   supported commands, plugin hooks, integration contracts, safety/security/
   migration/data obligations, and current tests/docs/examples/prompts that
   genuinely belong to live behavior.
3. Build `purpose-map.md`: artifacts that claim to matter, the current purpose
   each appears to serve, the live root or owner proving that purpose, and
   suspicious keep reasons.
4. Build `reference-graph-notes.md`: code, tests, docs, examples, generated
   files, package exports, configs, scripts, prompts, assets, styles, locale
   keys, data/schema/telemetry names, and self-referential islands.
5. Use native parallel agents for independent read-only slices when the target
   is broad enough: live roots, self-referential islands, test bloat,
   dependencies/build/config, docs/examples/generated surfaces, V1/V2 and stale
   flags, and low-value live abstractions.
6. Challenge every reference: is the referring artifact itself live, does the
   reference come from a live root, and would deleting the candidate break real
   current behavior or only stale support surfaces?
7. Hunt hidden cruft clusters: self-referential islands, test-hostage code,
   docs-laundered code, generated-artifact laundering, stale feature flags,
   compatibility ghosts, V1/V2 shadow systems, phantom public APIs,
   configuration cemeteries, oversized or unused dependencies, stale assets,
   stale locale keys, old telemetry names, and retired examples.
8. For scope-backed work, hunt scope-laundered live clusters. Do not keep them
   merely because current code, tests, docs, or users now reach them.
9. Review tests as artifacts. Report tests that should be deleted or rewritten
   with their cruft cluster. Do not ask for more tests unless the user
   explicitly requested test strategy.
10. Review docs, examples, and prompts as artifact supports. Treat them as
   secondary unless they are themselves stale or they keep code, tests, or
   workflows alive.
11. Review dependencies, build files, package metadata, config, and scripts as
    code surfaces that can preserve dead behavior.
12. Use git history when retirement timing, migration completion, old
    ownership matters.
13. Use `references/cruft-lenses.md` and `references/examples.md` to classify
    concrete candidates. Use examples as illustrations of reasoning, not a
    lookup table.
14. Save `low-value-catalog.md`, `test-bloat-report.md`,
    `deletion-candidates.md`, `keep-decisions.md`, `coverage.md`,
    `findings.md`, and `verdict.md`.
15. Return a short findings-first answer with the verdict and run directory.

## Output Expectations

The final chat reply includes:

- verdict: `cruft-found`, `no-material-cruft-found`, `scope-incomplete`, or
  `unsafe-to-judge`
- top deletion clusters, if any
- owner checks, if any
- notable keep decisions, if material
- run directory path
- one next action from the review, not a workflow prescription

The full saved artifact follows `references/output-contract.md`.

## Reference Map

- `references/cruft-lenses.md` - live-purpose model, root types, hidden cruft
  patterns, deletion classes, test-bloat lenses, dependency/build/config
  lenses, and docs/examples/generated-artifact lenses
- `references/agent-slices.md` - native parallel-agent slice guidance and
  accounting rules
- `references/output-contract.md` - required saved files, verdicts, finding
  shape, maps, and final chat summary shape
- `references/examples.md` - examples and anti-examples for self-referential
  islands, test-hostage code, V1/V2 shadows, stale flags, low-value wrappers,
  generated artifacts, and stale docs/examples
