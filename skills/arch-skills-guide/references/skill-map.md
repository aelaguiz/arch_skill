# Arch Skills Guide Map

Use this file when the user wants help choosing between the arch subskills.

## Decision order

Start with the strongest discriminator first:

1. Is the ask mostly "what's next?" on an existing plan doc?
   - use `arch-flow`
2. Is the ask mainly docs cleanup, stale-doc consolidation, or working-doc retirement with code truth stable enough to trust?
   - use `arch-docs`
3. Is the ask for the full arch workflow, one explicit full-arch step, generic continuation on a full-arch doc, `advance`, or concise stage-quality status?
   - use `arch-step`
4. Is it a repo-wide map-first comment hardening pass focused on shared contracts, conventions, gotchas, or subtle behavior in code?
   - use `comment-loop`
5. Is it a repo-wide audit pass, systematic defect hunt, or leave-it-running cleanup loop?
   - use `audit-loop`
6. Is it a bug, regression, crash, incident, or Sentry/log investigation?
   - use `bugs-flow`
7. Is the path unknown and the work open-ended?
   - use `goal-loop`
8. Is it a quant-heavy optimization or root-cause hunt with ranked hypotheses and brutal tests?
   - use `north-star-investigation`
9. Is it a small feature or improvement that should fit in 1-3 phases?
   - use `lilarch`
10. Does the user want a one-pass mini plan with canonical arch blocks?
   - use `arch-mini-plan`
11. Otherwise, default to `arch-step`.

## Skill map

| Skill | Use when | Do not default to it when | Example asks |
| --- | --- | --- | --- |
| `arch-step` | the user wants the full arch workflow, a specific full-arch command, helpers, `advance`, or compact stage-quality status | they only need a read-only checklist or the task belongs to a different workflow family | "Do the full arch flow", "Run research on this plan", "do the review gate", "advance the flow one step", "audit implementation vs plan" |
| `arch-docs` | the code is already clean enough to trust and the main job is cleaning stale, overlapping, or misleading docs, including post-arch plan/worklog retirement | the feature still needs code work, or the ask is generic copy editing or net-new documentation authoring | "Clean up the docs in this repo", "retire this plan/worklog and fold the truth into evergreen docs", "run the docs cleanup loop" |
| `arch-mini-plan` | the user wants a compact one-pass plan but still wants canonical arch blocks | the work is tiny enough for `lilarch` or large enough for full arch | "Give me the mini plan version", "one-pass arch plan for this task" |
| `lilarch` | contained 1-3 phase feature work | the task is migration-heavy, investigation-heavy, or broad | "Small feature, use lilarch", "tight feature flow for this improvement" |
| `bugs-flow` | regressions, crashes, incidents, Sentry/log-driven fixes | planned feature work or open-ended optimization | "Analyze this Sentry issue", "fix this bug and verify it" |
| `comment-loop` | the user wants a repo-wide code comment pass, wants the agent to deeply understand the repo before explaining it, or wants shared contracts, conventions, gotchas, and subtle behavior documented in code | the job is docs cleanup, one local comment tweak, or bug fixing | "Map this repo and add the comments that actually matter", "deeply understand the codebase before commenting conventions", "keep hardening the high-value code comments until the real gaps are gone" |
| `audit-loop` | the user wants a repo-wide audit pass, the next worthwhile defect fixed, or a bounded cleanup loop that keeps going until review says stop | there is already one concrete known bug or the main job is docs cleanup | "Scan this repo for bugs and fix what matters", "do one audit pass", "keep cleaning this codebase until no worthwhile audit work remains" |
| `goal-loop` | the goal is clear but the path is unknown; repeated bets matter | the task already has a fixed implementation plan | "We need to improve this metric but don't know the path" |
| `north-star-investigation` | the user wants a quantified investigation with ranked hypotheses and brutal tests | the task is just a normal bug fix or plain goal loop | "Run a deep investigation on this performance issue" |
| `arch-flow` | the user already has a plan doc and wants a read-only checklist or next-step routing | they actually want the work performed | "What's next on this doc?", "give me the checklist before we run anything" |

## Near-lookalike boundaries

- `arch-flow` vs `arch-step`:
  - use `arch-flow` for read-only checklist and next-step routing
  - use `arch-step` when the user wants continuation, the concise stage-quality readout, or `advance` to inspect and optionally execute one next full-arch step
- `arch-step` vs `arch-docs`:
  - use `arch-step` while the feature still needs planning, implementation, or code-completeness audit
  - use `arch-docs` once the code is clean and the remaining job is docs cleanup, consolidation, or working-doc retirement
- `bugs-flow` vs `audit-loop`:
  - use `bugs-flow` for one concrete known bug or incident
  - use `audit-loop` when the job is to find the next worthwhile bug or fragility across the repo
- `arch-docs` vs `comment-loop`:
  - use `arch-docs` when the main job is repo documentation cleanup grounded in already-stable code truth
  - use `comment-loop` when the main job is high-value explanatory hardening inside code comments, docstrings, or doc comments
- `comment-loop` vs `audit-loop`:
  - use `comment-loop` when the repo mainly needs clearer explanation of existing contracts, conventions, or gotchas
  - use `audit-loop` when the repo mainly needs the next real bug, dead code, duplication, or proof gap fixed
- `arch-docs` vs `audit-loop`:
  - use `arch-docs` when the main job is documentation cleanup grounded in already-stable code truth
  - use `audit-loop` when the main job is code audit, defect finding, dead-code deletion, or duplication cleanup
- `arch-step` vs `arch-mini-plan`:
  - use `arch-mini-plan` only when the user wants a compressed one-pass plan
  - otherwise use `arch-step` for real full-arch work
- `arch-mini-plan` vs `lilarch`:
  - use `lilarch` for true small-feature delivery with start/plan/finish
  - use `arch-mini-plan` when the user still wants canonical arch blocks
- `goal-loop` vs `north-star-investigation`:
  - use `north-star-investigation` when the investigation itself is the main product and math/hypothesis ranking matters
  - use `goal-loop` for broader iterative work where the path is unknown
- `bugs-flow` vs `north-star-investigation`:
  - use `bugs-flow` for concrete incident or regression handling
  - use `north-star-investigation` when the problem is a harder optimization/root-cause hunt with explicit quantified bets

## Response shape

When the user wants a recommendation:

- Name the primary skill first.
- Then explain:
  - why it fits this ask
  - the closest alternative
  - the boundary between them

When the user wants a tour:

- Give the suite in decision order:
  - `arch-flow`
  - `arch-docs`
  - `arch-step`
  - `comment-loop`
  - `audit-loop`
  - `bugs-flow`
  - `goal-loop`
  - `north-star-investigation`
  - `lilarch`
  - `arch-mini-plan`
- Keep each skill explanation to one sentence unless the user asks for more depth.
