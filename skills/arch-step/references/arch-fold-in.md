# `fold-in` Command Contract

## What this command does

- resolve one plan doc plus the true reference set
- ingest every relevant reference material fully
- distill binding obligations from those materials
- fold them into the main plan and wire them into the relevant phases so implementation cannot miss them

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Section 7 and helper-block expectations

## Inputs

- infer `DOC_PATH` as the single plan doc to update
- `REFS` are every other doc path or URL in the ask, plus obvious reference materials already listed in `related:` or clearly linked from the plan

## Writes

- `arch_skill:block:reference_pack`
- `related:` frontmatter when needed
- phase-plan `Reference obligations (must satisfy)` bullets when the phase plan exists

## Hard rules

- docs-only; do not modify code
- apply the single-document rule
- do not create additional planning docs
- read every reference fully
- if a URL requires auth or cannot be fetched, stop and ask for pasted content or an export
- if a diagram or image is referenced, extract a textual UX contract from it instead of hand-waving it

## DOC_PATH resolution

Pick the one true plan doc by best-effort scoring:

- strong signals:
  - canonical headings
  - `arch_skill:block:` markers
  - frontmatter with `status` or `doc_type`
- anti-signals:
  - `*_WORKLOG.md`
  - generic guides or indexes unless the user explicitly names them as the plan

If no credible doc was provided:

- search `docs/` for the most plan-like recent doc
- if still not credible, ask for the path explicitly

## Reference ingestion rules

For each `R#`:

- keep a stable identifier
- preserve the source pointer
- produce two layers:
  - distilled binding obligations
  - folded source content

Local files:

- read the file fully
- for folders, recursively include likely text docs only

URLs:

- fetch the human-readable content as best as possible

Images or diagrams:

- preserve the asset reference
- extract:
  - states
  - transitions
  - copy constraints
  - acceptance criteria
  - "must not change" notes

## Phase alignment rules

- if the ask explicitly names a phase, honor it
- otherwise map obligations by ownership:
  - UX refs -> UI or behavior phases
  - API or contract refs -> foundation phases
  - migration or delete refs -> cleanup phases
- if uncertain, treat the obligation as global rather than asking a low-value question

## Update rules

Write or update:

- `arch_skill:block:reference_pack`

Also:

- ensure `related:` includes the folded refs, deduped
- if the phase plan exists, add or update the exact bullet:
  - `* Reference obligations (must satisfy):`

Use this block shape:

```text
<!-- arch_skill:block:reference_pack:start -->
# Reference Pack (folded materials; phase-aligned)
Updated: <YYYY-MM-DD>

## Inventory
- R1 — <title> — <source path/URL>
- R2 — <title> — <source path/URL>

## Binding obligations (distilled; must satisfy)
- <obligation> (From: R#)

## Phase alignment (must satisfy per phase)
### Global (applies across phases)
- <obligation> (From: R#)

### Phase 1 — <phase name>
- Reference obligations (must satisfy):
  - <obligation> (From: R#)
- References:
  - R#, R#

## Folded sources (verbatim; inlined so they cannot be missed)
### R1 — <title> — <source>
~~~~markdown
<verbatim content or extracted text>
~~~~
<!-- arch_skill:block:reference_pack:end -->
```

## Quality bar

- resolve the right plan doc deterministically
- distill obligations, not just summaries
- wire obligations into phases where they matter
- keep the phase plan skimmable; do not paste whole specs into phase bullets
- make it impossible to implement the phase without seeing the relevant constraints

## Stop condition

- if the plan doc remains ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if a required reference cannot be read because of access or missing content, stop and ask for that content
- otherwise stop after the reference pack and phase wiring are updated

## Console contract

- one-line North Star reminder
- one-line punchline
- chosen `DOC_PATH` and how many refs were folded
- what changed in the reference pack and phase wiring
- missing or inaccessible refs only if real
- next action
