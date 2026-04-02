# `reformat` Command Contract

## What this command does

- take an existing architecture or plan doc that is not in canonical shape
- convert it into the canonical `arch-step` artifact
- preserve meaning-bearing content instead of rewriting from scratch
- draft TL;DR plus Section 0 from the source evidence and stop for confirmation

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for TL;DR, Section 0, and the sections the source content maps into

## Inputs

- `DOC_PATH`:
  - if the ask includes `OUT=...`, treat that as the output path and the first markdown path as the input doc
  - otherwise use the markdown path from the ask
  - if no path is clear, ask for the top 2-3 best candidates
- treat the input doc as the source of truth for meaning-bearing content

## Exact artifact responsibility

This command must restore:

- canonical frontmatter
- `# TL;DR`
- `planning_passes`
- `# 0)` through `# 10)`
- Appendix A and Appendix B when needed

## Hard rules

- docs-only; do not modify code
- do not rewrite from scratch
- preserve links, code fences, tables, decisions, TODOs, open questions, and call-site notes
- infer only from explicit source evidence
- label uncertain synthesis as draft inference
- if something is truly missing, leave a TODO or placeholder instead of inventing it
- if content cannot be confidently placed, keep it in Appendix A instead of dropping it
- do not introduce new scope
- preserve the single-document rule

## Quality bar

- preserve all meaning-bearing content
- map content into the canonical structure once where possible
- keep original wording when it carries nuance
- normalize heading drift back to the canonical shape
- draft TL;DR and Section 0 concretely when the source supports it

## Why this command exists

The goal is not prettier markdown. The goal is to recover one plan artifact that later commands can trust:

- same structure every time
- same meaning preserved
- same alignment lock up front
- no content loss hiding in "cleanup"

## Conversion procedure

1. Read the input doc fully.
2. Create the canonical skeleton from `artifact-contract.md`.
3. Map source content into the best-fitting canonical sections.
4. Preserve code fences, tables, and links exactly.
5. Prefer placing content once unless duplication is the only safe way to avoid losing meaning.
6. Draft TL;DR and Section 0 from source evidence.
7. Preserve or insert the canonical `planning_passes` block.
8. Add:
   - `Appendix A) Imported Notes` for unplaced source content
   - `Appendix B) Conversion Notes` for major moves and remaining gaps
9. Make one final consistency pass across TL;DR, Section 0, and Section 7.
10. Write in place unless `OUT=...` is provided.

## Consistency duties before stopping

- TL;DR, Section 0, and the phase plan should not contradict each other after conversion
- preserve the strongest explicit source claims about scope, evidence, fallbacks, and sequencing
- if the source remains ambiguous, keep that ambiguity visible instead of smoothing it away

## Stop condition

After converting the doc:

- print the drafted TL;DR
- print the drafted North Star
- ask for confirmation or edits
- stop

## Console contract

- one-line North Star reminder
- one-line punchline
- output doc path
- drafted TL;DR
- drafted North Star
- ask for `yes` or edits
