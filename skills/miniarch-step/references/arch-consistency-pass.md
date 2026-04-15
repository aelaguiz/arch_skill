# `consistency-pass` Command Contract

## What this command does

- run an end-to-end cold-read consistency audit over one canonical full-arch doc
- repair obvious cross-section contradictions in place before implementation starts
- use two parallel cold-reader passes in Codex so the parent integrator gets fresh eyes across the whole artifact
- record the outcome in one helper block
- decide whether the doc is decision-complete and ready to proceed to `implement`

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for `# TL;DR`, `# 0)` through `# 10)`, `planning_passes`, and helper blocks

## Writes

- `arch_skill:block:consistency_pass`
- any real plan sections that need repair after accepted findings

## Hard rules

- docs-only; do not modify code
- this helper stays optional in ordinary manual `miniarch-step` usage, but `auto-plan` must run it after `phase-plan`
- treat the artifact as a set of truth claims that must agree end to end; this is not copy editing or prose cleanup
- use the cross-section consistency rules in `artifact-contract.md` as the primary rubric
- integrate accepted repairs into the main artifact first, then write or update the helper block
- keep Section 7 as the one authoritative execution checklist; do not create a shadow checklist here
- do not use external reviewer CLIs or other-model consultations
- in Codex, use exactly two parallel `explorer` agents for the cold read
- outside Codex, keep the same review question and block shape; do not invent a second workflow just because explorer agents are not a runtime primitive
- if the North Star, deep-dive, or phase plan is too weak to audit honestly, stop and point to the earlier command that must repair it
- `Decision: proceed to implement? yes` is forbidden while unresolved decisions, unauthorized scope cuts, orphan phase obligations, or non-auditable exit criteria remain

## Codex cold-read split

In Codex, use exactly two parallel `explorer` agents with this fixed ownership split:

- Explorer 1:
  - frontmatter
  - `# TL;DR`
  - `# 0)`, `# 1)`, `# 2)`, `# 7)`, `# 8)`, `# 9)`, `# 10)`
  - helper-block drift
- Explorer 2:
  - `# 3)`, `# 4)`, `# 5)`, `# 6)`, and `# 7)`
  - whether architecture, call-site audit, verification, rollout, and cleanup still agree

The parent pass owns integration:

- read the full artifact yourself before delegating
- send the two explorers in parallel
- reconcile overlaps or disagreements in the parent pass
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
- Reviewers: explorer 1, explorer 2, self-integrator
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
