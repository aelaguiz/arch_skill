# `research` Command Contract

## What this command does

- ground the plan in internal code truth and relevant external anchors
- write or update the Research Grounding section
- surface evidence-based open questions
- write likely code implications into the plan without implementing them

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for TL;DR, Section 0, Section 2, and Section 3

## Reads for alignment

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 2) Problem Statement`
- any existing research or external research content

## Writes

- `# 3) Research Grounding (external + internal “ground truth”)`
- `arch_skill:block:research_grounding`

## Hard rules

- docs-only; do not modify code
- use repo evidence first
- read code and run read-only searches as needed
- search for the canonical existing path before blessing a new abstraction or code path
- if research reveals likely code changes, write them into the plan with file anchors instead of implementing them
- if the North Star, requested behavior scope, or allowed architectural convergence scope is unclear or contradictory, stop for a quick doc correction before continuing

## Quality bar

Good research looks like:

- authoritative internal anchors with concrete file paths and what they define
- the canonical owner path or boundary is named explicitly
- reusable patterns named explicitly so later stages do not reinvent them
- duplicate or drifting paths relevant to the change are called out early
- existing preservation signals are named when refactor or consolidation is likely
- external anchors only when they add real value, each with adopt or reject reasoning
- open questions framed as evidence needed rather than vague TODOs

Research is weak when it is generic, unanchored, cargo-culted, or disconnected from the plan.

## Placement and update rules

Update the doc in this order:

1. if `arch_skill:block:research_grounding` exists, replace inside it
2. otherwise update an existing research-like section in place
3. otherwise insert a new top-level Section 3 after the problem statement or after TL;DR/frontmatter if needed

If the doc is canonical, preserve the exact Section 3 heading and numbering.

Use this block shape:

```text
<!-- arch_skill:block:research_grounding:start -->
# Research Grounding (external + internal “ground truth”)
## External anchors (papers, systems, prior art)
- <source> — <adopt/reject + what exactly> — <why it applies>

## Internal ground truth (code as spec)
- Authoritative behavior anchors (do not reinvent):
  - `<path>` — <what it defines / guarantees>
- Canonical path / owner to reuse:
  - `<path>` — <behavior or contract this path should own>
- Existing patterns to reuse:
  - `<path>` — <pattern name> — <how we reuse it>
- Duplicate or drifting paths relevant to this change:
  - `<path>` — <why it may need convergence or deletion>
- Behavior-preservation signals already available:
  - `<test/check>` — <what current behavior it protects>

## Open questions (evidence-based)
- <question> — <what evidence would settle it>
<!-- arch_skill:block:research_grounding:end -->
```

## Consistency duties beyond local ownership

- if research disproves an assumption already stated in TL;DR or Section 0, repair the smallest stale claim so the doc stays honest
- if research materially changes likely architecture, convergence scope, or verification choices, point the next move to `deep-dive` or `phase-plan` as appropriate
- do not rewrite later sections here, but do not leave obvious contradictions unmarked

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if the North Star, requested behavior scope, or allowed architectural convergence scope is contradictory, stop for a quick doc correction
- otherwise stop after the research block is updated and the next move is clear

## Console contract

- one-line North Star reminder
- one-line punchline
- what changed in research grounding
- real issues or risks only
- next action
- need from the user only if required
