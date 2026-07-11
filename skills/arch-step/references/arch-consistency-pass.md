# `consistency-pass` Command Contract

## What this command does

- run an end-to-end cold-read consistency audit over one canonical full-arch doc
- repair obvious cross-section contradictions in place before implementation starts
- use two new clean same-host native cold-reader roles so the parent integrator gets independent eyes across the whole artifact
- record the outcome in one helper block
- decide whether the doc is decision-complete and ready to proceed to `implement`

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `../../_shared/agent-orchestration-policy.md`
- `../../_shared/scope-and-convergence.md`
- `section-quality.md` for `# TL;DR`, `# 0)` through `# 10)`, `planning_passes`, and helper blocks

## Writes

- `arch_skill:block:consistency_pass`
- any real plan sections that need repair after accepted findings
- `arch_skill:block:auto_plan_receipts` only through the stage gate when running as the current `auto-plan` stage

## Hard rules

- docs-only; do not modify code
- this helper stays optional in ordinary manual `arch-step` usage, but `auto-plan` must run it after `phase-plan`
- treat the artifact as a set of truth claims that must agree end to end; this is not copy editing or prose cleanup
- use the cross-section consistency rules in `artifact-contract.md` as the primary rubric
- integrate accepted repairs into the main artifact first, then write or update the helper block
- keep Section 7 as the one authoritative execution checklist; do not create a shadow checklist here
- the independence needed here comes from clean native child context. Do not
  add an external same-provider process merely to simulate freshness. A
  separately requested provider, exact-model/profile, durable session, or
  structured-receipt review is a different review lane and must name the
  concrete benefit that justifies its added process and integration cost
- use the two explorer roles below and no additional fanout. Run them in
  parallel only when the active host has the child slots and the parent can
  integrate both returns; otherwise run the same two clean roles sequentially
- children may not create children or invoke delegation or consultation
  workflows. This command assigns no nested scope or budget
- if the North Star, deep-dive, or phase plan is too weak to audit honestly, stop and point to the earlier command that must repair it
- `Decision: proceed to implement? yes` is forbidden while unresolved decisions,
  unauthorized scope cuts or additions, scope provenance gaps, an unfrozen or
  unbounded convergence closure, scope laundering/cycling, orphan phase
  obligations, or non-auditable exit criteria remain
- compare TL;DR, Section 0, target architecture, Section 7, proof, and Section
  10 against the original human anchors. A plan item or Decision Log entry
  cannot cite itself as authority. Remove unauthorized additions or stop for a
  human decision; cold readers do not create new scope
- when running as the current `auto-plan` stage, run `python3 skills/arch-step/scripts/arch_stage_gate.py begin --doc <DOC_PATH> --stage consistency-pass` before the cold read and `python3 skills/arch-step/scripts/arch_stage_gate.py complete --doc <DOC_PATH> --stage consistency-pass` after the helper block is current
- if the stage gate says a different stage is next, stop and report that required command instead of hand-editing receipts or treating an existing consistency marker as proof that this command ran

## Native clean cold-read split

Create two new same-host native children. Give each child `DOC_PATH`, the
shared references above, one lens below, and the return contract in this
section. `New` means do not resume an earlier planner, implementer, or reviewer.
The children share the workspace but not the parent's completion narrative.

Map clean context deliberately:

- In Codex, create each explorer with `fork_turns: "none"`.
- In Claude Code, use a clean named or custom subagent for each explorer; do
  not use an explicit conversation fork for these independent cold reads.
- On another host, use its clean native child mechanism when available. If it
  has no such mechanism, the parent performs the same two lenses serially
  rather than inventing an external process solely for freshness.

Use the strongest read-only capability or sandbox the active host actually
exposes, and say in both briefs: inspect only; do not edit, write, apply
patches, commit, or change repo state. Do not claim the capability is enforced
unless the active tool schema confirms it. The parent captures the relevant
`git status` or diff immediately before dispatch and compares current repo
state after both returns, before making any integration edits.

The lenses are intentionally non-overlapping. Both explorers may read the full
artifact to understand cross-references, but each reports only findings owned
by its lens:

- Scope and execution-authority explorer:
  - owns human authorization, North Star, scope provenance, convergence
    closure, scope freeze, compatibility decisions, phase-frontier
    completeness, exhaustive checklist/exit obligations, Decision Log
    authority, helper-block drift, unresolved decisions, and unauthorized
    cuts or additions
  - uses frontmatter, `# TL;DR`, `# 0)`, `# 1)`, `# 2)`, `# 7)`, `# 10)`, and
    helper blocks as its primary evidence
- Architecture and proof-chain explorer:
  - owns research grounding, current-to-target architecture coherence,
    canonical owner path, call-site/migration/delete coverage, preservation
    evidence, verification sufficiency, rollout, and cleanup coherence
  - uses `# 3)` through `# 6)`, `# 8)`, and `# 9)` as its primary evidence;
    it may cite Section 7 as the downstream claim to compare against, but does
    not duplicate the first explorer's scope-authority or obligation audit

Each explorer returns:

- whether its bounded review completed
- findings with section or path anchors, the controlling rule or evidence, and
  the smallest main-doc repair or blocker question
- checks or searches it performed and any unresolved assumptions
- an explicit confirmation that it made no writes and created no children

The parent pass owns integration:

- read the full artifact before dispatch
- verify the no-write claim against current repo state
- reconcile the two lenses and resolve any cross-lens contradiction itself
- re-read the current artifact before editing so concurrent changes are not
  overwritten
- repair the main artifact first
- only then write `arch_skill:block:consistency_pass`

## Core review question

Ask the same question every time:

- `Does this artifact still say the same thing end to end about outcome, requested behavior scope, allowed convergence scope, adjacent surfaces that must stay in sync, compatibility posture, canonical owner path, required deletes or migrations, authoritative execution order, exhaustive phase-exit conditions, verification expectations, rollout obligations, and approved exceptions? Are any plan-shaping decisions still unresolved? Did the artifact silently cut any approved behavior or required work, silently strand required obligations outside Checklist or Exit criteria, or silently assume backward compatibility? If anything is off, what must change in the main doc before implementation should begin?`

Anchor that question using `artifact-contract.md` and `section-quality.md`:

- TL;DR, Section 0, and Section 7 must agree on goal, scope, and plan shape
- Section 3, Section 5, Section 6, and Section 7 must agree on the canonical owner path, adjacent surfaces, compatibility posture, migrations, deletes, and adoption scope
- Section 7 must be executable from Sections 5 and 6 without hidden work
- no required phase obligation may exist only in `Work`, `Verification`, `Docs/comments`, migration notes, delete lists, or helper narration
- Section 7 exit criteria must be concrete enough that `audit-implementation` can validate them without guessing
- Section 8 and Section 9 must still match the execution burden implied by Section 7
- helper blocks must not drift into competing execution surfaces
- Decision Log entries must still match any meaningful drift or approved exception the artifact now depends on

## Update rules

Write or update:

- `arch_skill:block:consistency_pass`

Use this block shape:

```text
<!-- arch_skill:block:consistency_pass:start -->
## Consistency Pass
- Reviewers: scope/execution-authority explorer, architecture/proof-chain explorer, parent integrator
- Scope checked:
  - <item>
- Findings summary:
  - <item>
- Integrated repairs:
  - <item>
- Remaining inconsistencies:
  - <item or `none`>
- Unresolved decisions:
  - <item or `none`>
- Unauthorized scope cuts:
  - <item or `none`>
- Decision-complete:
  - <yes|no>
- Decision: proceed to implement? <yes|no>
<!-- arch_skill:block:consistency_pass:end -->
```

Insert near the end before the Decision Log when possible.

## Quality bar

- catches real cross-section contradictions, not just awkward wording
- repairs the main artifact instead of parking issues in the helper block
- makes it obvious whether implementation should proceed now
- catches silent parity omissions and hidden compatibility assumptions before implementation starts
- catches orphan obligations outside the authoritative phase-exit surface and vague exit criteria before implementation starts
- keeps remaining inconsistencies explicit when the answer is `no`
- makes unresolved decisions and unauthorized scope cuts explicit
- stays short and decision-oriented once the repairs are integrated

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if the artifact still needs earlier planning repair, stop and point to the owning command
- otherwise stop after repairs are integrated and the helper block is current

## Console contract

- one-line North Star reminder
- one-line punchline
- what changed in the main artifact
- remaining inconsistencies
- whether the doc should proceed to `implement`
