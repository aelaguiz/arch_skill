---
name: cynical-architecture-review
description: "Run a prompt-only cynical architecture review over a branch, diff, subsystem, plan-backed implementation, or code area by assuming the architecture was not intentionally designed but emerged through iteration and got cemented. Hunt for sprawl, invalid split ownership, duplicate truth, accidental abstractions, compatibility shims, flags-as-architecture, registries, adapters, state spread, wrong decomposition, and complexity not forced by the intended user experience or hard experiment requirements. Push subtraction-first architecture: delete, consolidate, move ownership, simplify boundaries, and preserve the same UX with fewer concepts and less code. Not for normal bug review, QA/test/doc review, exhaustive coverage review, completion-truth review, implementation, or proof harnesses."
metadata:
  short-description: "Subtraction-first accidental architecture review"
---

# Cynical Architecture Review

Use this skill when the user wants a skeptical architecture review that assumes
the current structure may have emerged accidentally through iteration and then
been mistaken for intentional design.

The job is to read current code, preserve the intended user experience and hard
experiment requirements, find architecture that "just happened", identify
sprawl, invalid ownership splits, duplicate truth, and unjustified complexity,
save a findings-first review artifact, and report the verdict plus path.

This skill does not implement, repair, commit, push, open PRs, route repair
waves, run external review subprocesses, redesign the product, or decide the
user's broader workflow.

## Use When

- The user asks for a cynical, skeptical, adversarial, or subtraction-first
  architecture review.
- The user says the architecture feels ugly, sprawling, accidental,
  overgrown, split-brained, cemented by iteration, or not intentionally
  designed.
- The user wants to preserve the same UX or experiment while achieving it with
  fewer concepts, fewer owners, fewer paths, fewer states, less code, or a
  cleaner architecture boundary.
- The user wants to find invalid split ownership, duplicate truth, accidental
  abstractions, compatibility shims, feature flags as architecture, registries,
  adapter piles, state spread, wrong decomposition, or patterns likely to
  spread if left in place.
- The user says not to focus on pedantic QA, tests, docs, or proof rituals and
  instead wants architecture issues in code surfaced deeply.

## Do Not Use When

- The user wants a normal high-signal bug-focused code review. Use the host
  agent's normal review response.
- The user wants exhaustive line-by-line, file-by-file, or coverage-ledger
  review where coverage itself is the deliverable. Use
  `exhaustive-code-review`.
- The user wants skeptical implementation completion review: "did this plan
  really get implemented, or is the completion story lying?" Use
  `cynical-code-review`.
- The user wants a plan audited before work starts or implemented code reviewed
  mainly against a plan artifact's architecture bar. Use `plan-audit`.
- The user wants only a harsh maintainability, spaghetti, file-size, or
  code-judo pass. Use `thermo-nuclear-code-quality-review`.
- The user wants QA review, test coverage review, test cleanup, docs cleanup,
  README drift review, proof validation, CI hygiene, or release-readiness
  checking unless they explicitly ask this skill to include that lane.
- The user wants fixes, implementation, PR shipping, or workflow orchestration.

## Non-Negotiables

- Review only. Do not edit reviewed files.
- Save the review artifact under
  `/tmp/cynical-architecture-review/<slug>-<timestamp>/` unless the user
  explicitly asks for a repo doc path.
- This is prompt-only doctrine. Do not build a rule engine, runner,
  controller, scorer, harness, script, or formal parameter interface.
- Maximize native parallel agents for broad review targets when available.
  Account for every launched lane before finalizing.
- Do not manually spawn `codex`, `claude`, `agent`, `grok`, or any other
  coding-harness executable.
- Do not invoke external agent, delegation, consult, or review skills as the
  review mechanism.
- Start from distrust: existing architecture, names, wrappers, owners,
  folders, tests, docs, examples, generated artifacts, comments, and status
  text are claims, not proof of intentional design.
- Current code behavior and current code structure are the final authority for
  what exists. Intended UX, hard constraints, and experiment requirements are
  the authority for what must continue to exist.
- Human-authorized UX and constraints, plus the initial pre-freeze minimal
  convergence closure and explicit later human approvals, are the authority for
  what this change may add. Apply `skills/_shared/scope-and-convergence.md`.
- For plan-, branch-, conductor-, PR-, or history-backed work, reconstruct
  scope provenance and review waves. Every durable concept in the complexity
  ledger must trace to human scope or the frozen closure. Architecture that
  became "required" only through agent iteration or review cycling is a
  `REQUIRED REPAIR` and forces `not-approved`; default to subtraction. If
  provenance should exist but cannot be recovered, return `scope-incomplete`.
  Mark this lane not applicable only for standalone targets with no scope story.
- Do not change the intended user experience or weaken experiment requirements
  in the review. Find a simpler architecture underneath those constraints.
- Do not focus on QA, test coverage, test hygiene, docs hygiene, README drift,
  proof validation, CI hygiene, or release-readiness checks unless the user
  explicitly asks. Tests, docs, fixtures, examples, generated artifacts, and
  status text matter only when they reveal an architecture problem: stale
  generated truth, mocked boundary, duplicate contract, side door, old owner
  path, or future-copy trap.
- Findings must be concrete current-code or requested-scope architecture risks.
  Drop style preferences, generic maintainability advice, missing-test nits,
  doc hygiene, and vague "could be cleaner" comments unless they expose
  accidental architecture.
- A clean review is allowed, but only after the likely ways the architecture
  could be accidental have been checked and recorded honestly.

## First Move

1. Resolve the requested review target from natural language: current worktree,
   branch diff, commit range, explicit paths, subsystem, plan scope, or
   architecture claim.
2. Read local instructions and nearby architecture/review-relevant conventions.
3. Create the run directory under `/tmp/cynical-architecture-review/`.
4. Write the architecture story in plain English: what the current structure
   appears to be, what user experience and hard constraints it claims to serve,
   and what would have to be true for that structure to be justified.
5. When scope history exists, reconstruct the initial human baseline, frozen
   convergence closure, later human approvals, and review/plan waves before
   accepting the latest architecture story.
6. Read `references/review-lenses.md`.
7. Read `references/output-contract.md`.
8. Read `references/agent-slices.md` before launching native parallel agents.
9. Read `references/failure-patterns.md` when the target involves sprawl,
   split ownership, duplicate truth, flags, adapters, generated artifacts,
   config, or a plan-backed implementation.
10. Read `references/examples.md` when the architecture appears to have emerged
   historically, when tests/docs may be misdirection, or when peer review lanes
   are easy to confuse.

## Workflow

1. Save the review target summary as `target.md`.
2. Build `architecture-map.md`: intended UX, experiment requirements, hard
   constraints, current owners, current call paths, state, storage, APIs,
   config, generated artifacts, old paths, and adjacent same-contract surfaces.
3. Build `complexity-ledger.md`: live concepts, files, owner boundaries,
   states, flags, modes, adapters, registries, wrappers, shims, sync points,
   and caller obligations a maintainer must understand.
   For scope-backed work, attach a human or pre-freeze closure anchor to every
   durable concept; missing anchors are not cured by current reachability.
4. Use native parallel agents for independent read-only slices when the target
   is broad enough: UX/requirement mapping, owner/invariant mapping, old-path
   and duplicate-truth search, abstraction/complexity review, state/config
   review, and future-copy surface review.
5. Trace actual control flow, data flow, callers, readers, writers, lifecycle,
   persistence, public entrypoints, and authoritative internal boundaries
   until the real owner path is visible.
6. Treat existing splits as suspect. Ask what product, runtime, experiment,
   compatibility, safety, or domain requirement forces each split. If none
   exists, classify the split as accidental architecture.
7. Challenge every abstraction, layer, flag, wrapper, registry, adapter,
   compatibility path, state surface, generated truth, and owner boundary with:
   what requirement forces this to exist, and what breaks if it disappears?
8. Prefer deletion, consolidation, ownership repair, single state models,
   deeper modules, and clearer boundaries before proposing new abstractions.
9. Review QA/tests/docs/proof surfaces only when they are architecture evidence:
   mocked boundaries, stale generated truth, obsolete contracts, old owner
   paths, side doors, or misleading future-copy surfaces.
10. Run the scope-provenance and no-cycling lens. A newly discovered
    architectural relationship is not permission to expand the required repair
    beyond the frozen contract.
11. Use `references/review-lenses.md` and `references/failure-patterns.md` to
    classify concrete risks. Use `references/examples.md` as illustrations of
    reasoning, not a lookup table.
12. Save `coverage.md`, `subtraction-map.md`, `findings.md`, and
    `verdict.md`.
13. Return a short findings-first answer with the verdict and run directory.

## Output Expectations

The final chat reply includes:

- verdict: `approve`, `not-approved`, or `scope-incomplete`
- required repairs, if any
- observations, if material
- run directory path
- one next action from the review, not a workflow prescription

The full saved artifact follows `references/output-contract.md`.

## Reference Map

- `references/review-lenses.md` - source-informed subtraction doctrine,
  ground-truth order, complexity tests, and valid versus invalid complexity
- `references/failure-patterns.md` - concrete accidental architecture patterns,
  evidence to read, required-repair conditions, and safe-difference guards
- `references/agent-slices.md` - native parallel-agent slice guidance and
  accounting rules
- `references/output-contract.md` - required saved files, verdicts, finding
  shape, architecture maps, and final chat summary shape
- `references/examples.md` - examples and anti-examples for accidental
  architecture review, including QA/test/docs boundaries
