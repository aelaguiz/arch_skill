# `new` Command Contract

## What this command does

- create a brand-new canonical full-arch plan doc in `docs/`
- draft TL;DR plus Section 0 directly from the ask
- seed the rest of the canonical scaffold so later commands work on one shared artifact
- stop for explicit North Star confirmation before deeper planning

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for TL;DR, Section 0, Sections 1, 2, 8, 9, 10, and `planning_passes`

## Inputs

- treat the freeform user ask as working intent, not polished requirements
- if the user already has an existing doc that should be converted, route to `reformat` instead of creating a second plan doc

## Exact artifact responsibility

This command owns the initial creation of:

- required frontmatter
- `# TL;DR`
- `planning_passes`
- `# 0) Holistic North Star`
- exact canonical headings for `# 1)` through `# 10)`

It is not enough to create a file with headings. This command bootstraps the whole artifact shape.

## Why TL;DR and Section 0 matter

Treat TL;DR plus Section 0 as the planning lock:

- TL;DR says outcome, problem, approach, and plan shape in the fewest lines possible
- Section 0 says scope, exclusions, evidence, invariants, and fallback stance
- later commands should be able to resolve ordinary tradeoffs from these sections without guessing

If they are weak, every later stage becomes soft.

## Hard rules

- docs-only; do not modify code
- create exactly one plan doc; do not create sidecar planning docs
- name the file `docs/<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`
- derive a short 5-9 word screaming-snake title from the ask
- start the doc as `status: draft`
- do not leave placeholders in TL;DR or Section 0 when the ask supports drafting them concretely
- if the user later confirms the North Star, update `status:` from `draft` to `active` without silently changing scope

## Quality bar

- TL;DR must be concrete enough to falsify
- Section 0 must be real enough to confirm or correct
- If the ask implies architectural convergence, Section 0 must make that internal scope explicit instead of leaving later stages to infer it.
- If the ask implies refactor pressure, the initial evidence stance should name how preserved behavior will be trusted.
- if the ask clearly implies priorities, problem framing, verification bias, rollout implications, or an immediate tradeoff, lightly seed the relevant later sections instead of leaving pure ceremony
- lightly seeded sections must stay truthful and minimal

## Consistency duties before stopping

- `title`, TL;DR, Section 0, and `fallback_policy` must tell the same story
- if the ask makes scope boundaries obvious, reflect them consistently in TL;DR and Section 0
- if rollout or telemetry are obviously irrelevant, Section 9 can say so briefly
- if the ask reveals a real constraint or tradeoff, seed Section 1 or Section 10 with it

## Procedure

1. Derive the file name from the ask.
2. Create the canonical frontmatter from `artifact-contract.md`.
3. Write the exact canonical scaffold for TL;DR, `planning_passes`, and Sections `0` through `10`.
4. Draft TL;DR:
   - falsifiable outcome
   - concrete problem
   - real architectural approach
   - believable phase shape
   - non-negotiables that constrain later decisions
5. Draft Section 0:
   - falsifiable claim
   - requested behavior in scope
   - allowed architectural convergence scope
   - UX and technical out-of-scope
   - smallest credible acceptance evidence
   - smallest credible behavior-preservation evidence when refactor or consolidation is likely
   - key invariants
     - no new parallel paths
     - no silent behavior drift during refactors
   - strict fallback stance
6. Lightly seed Sections `1`, `2`, `8`, `9`, and `10` when the ask clearly supports it.
7. Insert the canonical `planning_passes` block near the top.
8. Make one consistency pass across frontmatter, TL;DR, Section 0, and any lightly seeded later sections.
9. Stop for North Star confirmation.

## Stop condition

After writing the doc:

- print the drafted TL;DR
- print the drafted North Star
- ask for confirmation or edits
- if edits arrive, update the doc and ask again
- do not continue into research or deeper planning from the same `new` run

## Console contract

- one-line North Star reminder
- one-line punchline stating that the doc exists and what confirmation is needed
- doc path
- drafted TL;DR
- drafted North Star
- ask for `yes` or edits
