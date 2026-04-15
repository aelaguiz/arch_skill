# Miniarch Step Status

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
5. Phase plan
6. Implementation
7. Audit
8. Docs cleanup
9. Best next move

## Allowed grades

Use exactly:

- `strong`
- `decent`
- `weak`
- `missing`

## Artifact evidence rules

### Plan artifact

Inspect:

- required frontmatter
- `# TL;DR`
- `planning_passes`
- exact canonical headings for `# 0)` through `# 10)`
- whether the major sections agree with each other

Grade:

- `strong` when the doc is structurally canonical, the major sections have credible content, the core sections agree, adjacent-surface and compatibility-posture decisions are explicit, the artifact is decision-complete, and any instruction-bearing imported content is either preserved structurally or explicitly condensed with recoverable source text
- `decent` when the structure is mostly canonical but one important section is thin
- `weak` when the doc is usable but structurally drifted, partially canonical, missing multiple required sections, internally inconsistent, still contains unresolved plan-shaping decisions, silently omits adjacent surfaces or compatibility posture, or silently compresses instruction-bearing imported content
- `missing` when there is no credible canonical full-arch artifact

Also apply the "big 3" readiness bar:

- target architecture fully specified
- architecture sufficiently idiomatic and convergent
- call sites audited exhaustively enough within approved scope to trust the plan

A doc cannot be artifact-strong if TL;DR, Section 0, Section 5, Section 6, or Section 7 are still weak, or if unresolved decisions remain anywhere in the authoritative artifact.

### North Star

Inspect:

- frontmatter `status`
- `# TL;DR`
- `# 0) Holistic North Star`

Grade:

- `strong` when TL;DR and Section 0 are concrete, scoped, falsifiable, evidence-aware, clearly distinguish requested behavior scope from allowed convergence scope, make adjacent-surface scope and compatibility posture explicit, contain no unresolved plan-shaping decisions, and `status` is `active` or `complete`
- `decent` when the content is mostly real but thin in one important place
- `weak` when the draft is vague, contradictory, placeholder-heavy, or still leaves plan-shaping decisions unresolved
- `missing` when the doc is not credibly bootstrapped

### Research

Inspect:

- `arch_skill:block:research_grounding`
- or a semantically equivalent research section with the canonical structure

Grade:

- `strong` when the block has authoritative internal anchors, names the canonical owner path, names adjacent surfaces and compatibility posture, names reusable patterns, grounds prompt and capability surfaces when the system is agent-backed, names preservation signals when needed, and turns any remaining decision gaps into explicit blockers instead of hiding them
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

- `strong` when current architecture is grounded, target architecture is fully specified, the canonical owner path is explicit, adjacent surfaces and compatibility posture are explicit, agent-backed behavior is split cleanly between prompt/capability use and deterministic code when relevant, the call-site audit is exhaustive enough within approved scope to drive implementation and audit, and no architecture-shaping decisions remain unresolved
- `decent` when all exist but one is still thin
- `weak` when one or more exist but do not meet the depth bar
- `missing` when one or more are absent

Also report whether the single deep-dive pass has been completed.

### Phase plan

Inspect:

- `arch_skill:block:phase_plan`

Grade:

- `strong` when the authoritative phased plan exists, remains the single execution checklist, each phase owns one coherent self-contained unit, the decomposition is foundational-first and biases toward more phases than fewer when both are valid, each phase has concrete work, an explicit exhaustive checklist, verification, exhaustive exit criteria, and rollback, refactor-heavy phases name preservation checks, adjacent-surface and cutover or preservation work are explicit, touched live docs/comments that would otherwise go stale are either deleted or rewritten in the plan, and the checklist contains no unresolved branches or "decide later" language
- `decent` when present but one or more phases are thin
- `weak` when generic, incomplete, blends coherent units into oversized phases, omits or underspecifies phase checklists, strands required obligations outside the authoritative phase-exit surface, uses vague or non-auditable exit criteria, mixes product creep into ship-blocking work, leaves touched live docs/comments cleanup implicit, or still contains unresolved execution choices
- `missing` when absent

### Implementation

Inspect:

- `WORKLOG_PATH`
- phase status updates in `DOC_PATH`
- implementation progress notes that match the implementation contract

Grade:

- `strong` when worklog and doc both reflect real phased progress or completion against the Section 7 checklist and exit criteria, required proof and required docs/comments propagation are visible where phase completeness depends on them, Section 7 phase status lines match the worklog, ledger-like completeness is visible, refactor-heavy phases ran preservation checks, touched live docs/comments that would otherwise go stale were cleaned up when needed, and the doc matches reality
- `decent` when implementation is real but progress truth is thin
- `weak` when there are claims of progress or completion without credible worklog or doc evidence for checklist completion, required proof, or exit-criteria satisfaction
- `missing` when no implementation evidence exists

### Audit

Inspect:

- `arch_skill:block:implementation_audit`
- reopened phase notes

Grade:

- `strong` when the audit block is evidence-anchored, reopened phases are updated in place, missing code is clearly separated from non-blocking manual QA, the audit validates both checklist items and exit criteria for modern phases, touched live docs/comments that would otherwise go stale are treated as implementation gaps when warranted, and unjustified scaffolding around agent-backed behavior is treated as an implementation gap
- `decent` when present but thin
- `weak` when nominal but not convincingly reconciled, or when exit-criteria validation is missing, vague, or clearly incomplete
- `missing` when absent

### Docs cleanup

Inspect:

- whether `Verdict (code): COMPLETE` is already present
- whether `DOC_PATH` and `WORKLOG_PATH` still exist as live feature residue
- whether the next required move is now the `arch-docs` handoff

Grade:

- `strong` when the code audit is clean and the artifact is ready to hand off to `arch-docs`
- `decent` when the code audit is close but still thin
- `weak` when the code audit is incomplete or the docs-cleanup handoff is still unclear
- `missing` when there is no credible audit state yet

## Output shape

Keep the output compact and human:

- one short line for the artifact
- one short line per core stage
- one short `Best next move:` line

Do not emit the longer `advance` checklist here.

## Best-next-move rule

Choose the command that most improves artifact completeness or core-flow progress:

1. no plan doc yet -> `new`
2. existing doc is not canonical enough to trust -> `reformat`
3. North Star is still draft or too weak -> stop for confirmation or repair via `reformat`
4. after North Star confirmation, stop and wait for the user's explicit next command; do not auto-advance into `research` or any later stage
5. unresolved decision gap remains that repo truth cannot settle -> ask the user the exact blocker question
6. earliest required structure or owned block is missing -> run the command that repairs it
7. required structure exists but the next critical sections are still weak, including canonical-path analysis, preservation verification, or decision-completeness -> run the command that strengthens them
8. otherwise follow the core arc:
   - `research`
   - `deep-dive`
   - `phase-plan`
   - `consistency-pass` when the artifact clearly needs an end-to-end cold-read repair or the user explicitly wants it
   - `implement` by default
   - `implement-loop` when the user explicitly wants the full-frontier delivery loop to a clean audit
   - `audit-implementation`
9. if the code audit is clean and the feature still needs docs cleanup, hand off to `Use $arch-docs`
10. if all required stages are complete and the live feature residue is already retired, say there is no required next move
