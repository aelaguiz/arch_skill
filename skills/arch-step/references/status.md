# Arch Step Status

`status` is the compact read-only surface.

Use `advance` when the user wants the full checklist, the exact next command, or optional one-step execution.

## What status inspects first

Before grading stages, inspect the artifact itself:

- required frontmatter
- `# TL;DR`
- `planning_passes`
- `# 0) Holistic North Star`
- exact canonical top-level sections `# 1)` through `# 10)`
- required command-owned blocks
- `WORKLOG_PATH` and `implementation_audit` when implementation has started
- the relevant quality bars from `section-quality.md`

## What status reports

Report in this order:

1. Plan artifact
2. North Star
3. Research
4. Deep dive
5. External research
6. Phase plan
7. Implementation
8. Audit
9. Helper summary
10. Best next move

## Allowed grades

Use exactly:

- `strong`
- `decent`
- `weak`
- `missing`
- `not needed`

`not needed` is only for external research and helper commands.

## Artifact evidence rules

### Plan artifact

Inspect:

- required frontmatter
- `# TL;DR`
- `planning_passes`
- exact canonical headings for `# 0)` through `# 10)`
- whether the major sections agree with each other

Grade:

- `strong` when the doc is structurally canonical, the major sections have credible content, the core sections agree, and any instruction-bearing imported content is either preserved structurally or explicitly condensed with recoverable source text
- `decent` when the structure is mostly canonical but one important section is thin
- `weak` when the doc is usable but structurally drifted, partially canonical, missing multiple required sections, internally inconsistent, or silently compresses instruction-bearing imported content
- `missing` when there is no credible canonical full-arch artifact

Also apply the "big 3" readiness bar:

- target architecture fully specified
- architecture sufficiently idiomatic and convergent
- call sites audited exhaustively enough within approved scope to trust the plan

A doc cannot be artifact-strong if TL;DR, Section 0, Section 5, Section 6, or Section 7 are still weak.

### North Star

Inspect:

- frontmatter `status`
- `# TL;DR`
- `# 0) Holistic North Star`

Grade:

- `strong` when TL;DR and Section 0 are concrete, scoped, falsifiable, evidence-aware, clearly distinguish requested behavior scope from allowed convergence scope, and `status` is `active` or `complete`
- `decent` when the content is mostly real but thin in one important place
- `weak` when the draft is vague, contradictory, or placeholder-heavy
- `missing` when the doc is not credibly bootstrapped

### Research

Inspect:

- `arch_skill:block:research_grounding`
- or a semantically equivalent research section with the canonical structure

Grade:

- `strong` when the block has authoritative internal anchors, names the canonical owner path, names reusable patterns, grounds prompt and capability surfaces when the system is agent-backed, names preservation signals when needed, and uses evidence-based open questions
- `decent` when present but thinner than required
- `weak` when present but generic or under-anchored
- `missing` when absent

### Deep dive

Inspect:

- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `planning_passes`

Grade:

- `strong` when current architecture is grounded, target architecture is fully specified, the canonical owner path is explicit, agent-backed behavior is split cleanly between prompt/capability use and deterministic code when relevant, and the call-site audit is exhaustive enough within approved scope to drive implementation and audit
- `decent` when all exist but one is still thin
- `weak` when one or more exist but do not meet the depth bar
- `missing` when one or more are absent

Also report whether pass 1 or pass 2 has been completed.

### External research

Inspect:

- `arch_skill:block:external_research`
- `planning_passes.external_research_grounding`

Grade:

- `strong` when the block uses narrow relevant topics, authoritative sources, and clear adopt or reject guidance for this plan
- `decent` when useful but thin
- `weak` when present but not truly synthesized
- `missing` when warranted but absent
- `not needed` when the plan is repo-local and external best practice does not materially affect correctness or idiomatic design

### Phase plan

Inspect:

- `arch_skill:block:phase_plan`

Grade:

- `strong` when the authoritative phased plan exists, remains the single execution checklist, each phase has concrete work, verification, exit criteria, and rollback, refactor-heavy phases name preservation checks, touched live docs/comments that would otherwise go stale are either deleted or rewritten in the plan, and agent-backed tooling is explicitly justified against prompt-first options
- `decent` when present but one or more phases are thin
- `weak` when generic, incomplete, mixes product creep into ship-blocking work, leaves touched live docs/comments cleanup implicit, or competes with helper checklists
- `missing` when absent

### Implementation

Inspect:

- `WORKLOG_PATH`
- phase status updates in `DOC_PATH`
- implementation progress notes that match the implementation contract

Grade:

- `strong` when worklog and doc both reflect real phased progress or completion, Section 7 phase status lines match the worklog, ledger-like completeness is visible, refactor-heavy phases ran preservation checks, touched live docs/comments that would otherwise go stale were cleaned up when needed, agent-backed changes leaned on the planned prompt or capability path before new tooling, and the doc matches reality
- `decent` when implementation is real but progress truth is thin
- `weak` when there are claims of progress without credible worklog or doc evidence
- `missing` when no implementation evidence exists

### Audit

Inspect:

- `arch_skill:block:implementation_audit`
- reopened phase notes

Grade:

- `strong` when the audit block is evidence-anchored, reopened phases are updated in place, missing code is clearly separated from non-blocking manual QA, touched live docs/comments that would otherwise go stale are treated as implementation gaps when warranted, and unjustified scaffolding around agent-backed behavior is treated as an implementation gap
- `decent` when present but thin
- `weak` when nominal but not convincingly reconciled
- `missing` when absent

## Helper summary rules

- `plan-enhance` is present when `arch_skill:block:plan_enhancer` exists
- `fold-in` is present when `arch_skill:block:reference_pack` exists
- `overbuild-protector` is present when `arch_skill:block:overbuild_protector` exists
- `review-gate` is present when `arch_skill:block:review_gate` exists

Summarize helpers in one compact line. Example:

- `Helpers are mixed: plan enhancer is strong, fold-in is decent, overbuild protector is missing, review gate is not needed.`

## Output shape

Keep the output compact and human:

- one short line for the artifact
- one short line per core stage
- one short helper line
- one short `Best next move:` line

Do not emit the longer `advance` checklist here.

## Best-next-move rule

Choose the command that most improves artifact completeness or core-flow progress:

- no canonical doc yet -> `new`
- non-canonical existing doc -> `reformat`
- draft or weak North Star -> confirm or repair via `reformat`
- missing research -> `research`
- weak or incomplete current architecture, target architecture, canonical-path analysis, or call-site audit -> `deep-dive`
- warranted but missing external research -> `external-research`
- weak, creep-heavy, missing capability-first analysis, preservation-light, or stale-live-doc-light execution checklist -> `phase-plan`
- code progress without worklog truth -> `implement`
- missing implementation audit -> `audit-implementation`
