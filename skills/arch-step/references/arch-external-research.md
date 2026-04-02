# `external-research` Command Contract

## What this command does

- use web research for plan-adjacent, broadly generalizable topics
- synthesize best practice into plan-specific adopt or reject guidance
- update the external research block and planning-pass state
- update the main plan if the research materially changes architecture, sequencing, or verification

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for external research, Section 5, and Section 8

## Reads for alignment

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 3) Research Grounding`
- `# 5) Target Architecture`
- `# 7) Depth-First Phased Implementation Plan` when present

## Writes

- `planning_passes.external_research_grounding`
- `arch_skill:block:external_research`
- affected plan sections and Decision Log when research changes the plan

## Hard rules

- docs-only; do not modify code
- use web research only for topics with general external guidance
- keep the topic set narrow
- prefer primary or clearly authoritative sources
- if sources disagree, summarize the disagreement and choose a default recommendation
- if North Star or UX scope is contradictory, stop for a quick doc correction before continuing
- do the research directly inside this command; do not rely on external model orchestration

## Relevance filter

Research a topic only when both are true:

- the plan touches the area or will be blocked by it
- the topic has broadly reusable external guidance

Good topic examples:

- animation or motion patterns, including reduce-motion behavior
- state-machine patterns
- CI or build determinism practices
- reliable concurrency or cancellation patterns
- framework-idiomatic testing strategy

Skip project-trivia topics that do not generalize.

Boundary examples:

- `event semantics` usually does not generalize enough
- `analytics schema design` might generalize enough when the plan is about analytics contracts

## Research budget

- aim for 2-5 topics total
- use 3-7 high-quality sources per topic at most
- prefer official docs, framework authors, language authors, or broadly trusted library maintainers

## Planning-passes update rule

- ensure the `planning_passes` block exists
- set:
  - `external_research_grounding: done <YYYY-MM-DD>`
- preserve all other fields

## Placement and update rules

Update in this order:

1. replace inside `arch_skill:block:external_research` when it exists
2. otherwise update an existing external research or best-practices section
3. otherwise insert a new top-level section after Research Grounding, after Target Architecture, or after TL;DR/Section 0

Preserve numbering if the doc already uses numbered sections.

Use this block shape:

```text
<!-- arch_skill:block:external_research:start -->
# External Research (best-in-class references; plan-adjacent)

> Goal: anchor the plan in idiomatic, broadly accepted practices where applicable. This section intentionally avoids project-specific internals.

## Topics researched (and why)
- <topic> — <why it applies>

## Findings + how we apply them

### <Topic A>
- Best practices (synthesized):
  - <bullet>
- Recommended default for this plan:
  - <bullet>
- Pitfalls / footguns:
  - <bullet>
- Sources:
  - <title> — <url> — <why it is authoritative>

## Adopt / Reject summary
- Adopt:
  - <what we will do + where it impacts the plan>
- Reject:
  - <what we will not do + why>

## Open questions (ONLY if truly not answerable)
- <question> — evidence needed: <what would settle it>
<!-- arch_skill:block:external_research:end -->
```

## Consistency duties beyond local ownership

- if external guidance changes architecture, sequencing, or verification stance, repair the smallest clearly stale claims elsewhere in the doc
- append or update a Decision Log entry when the research changes an earlier conclusion in a meaningful way
- do not leave external research saying one thing while TL;DR, Section 0, or Section 8 still say another

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if North Star or UX scope is contradictory, stop for a quick doc correction
- otherwise stop after the external research block, planning-pass update, and any required plan repairs are complete

## Console contract

- one-line North Star reminder
- one-line punchline
- what topics were researched and how they affected the plan
- real issues or risks only
- next action
