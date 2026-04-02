# Arch Skills Guide Map

Use this file when the user wants help choosing between the arch subskills.

## Decision order

Start with the strongest discriminator first:

1. Is the ask mostly "what's next?" on an existing plan doc?
   - use `arch-flow`
2. Is the ask for one explicit full-arch step, `advance`, or concise stage-quality status?
   - use `arch-step`
3. Is it a bug, regression, crash, incident, or Sentry/log investigation?
   - use `bugs-flow`
4. Is the path unknown and the work open-ended?
   - use `goal-loop`
5. Is it a quant-heavy optimization or root-cause hunt with ranked hypotheses and brutal tests?
   - use `north-star-investigation`
6. Is it a small feature or improvement that should fit in 1-3 phases?
   - use `lilarch`
7. Does the user want a one-pass mini plan with canonical arch blocks?
   - use `arch-mini-plan`
8. Otherwise, default to `arch-plan` for the full multi-step arch workflow.

## Skill map

| Skill | Use when | Do not default to it when | Example asks |
| --- | --- | --- | --- |
| `arch-plan` | medium/large multi-phase work, full arch planning, deep dive, external research, phase plans, implementation audits | the task is tiny, bug-shaped, open-ended with no fixed path, or the user wants literal one-step control | "Do the full arch flow", "give me the deep dive and phase plan", "audit implementation vs plan" |
| `arch-step` | the user wants explicit full-arch command control: one command at a time, helpers, `advance`, or compact stage-quality status | they want the broader intent-driven full-arch flow handled more holistically or only need a read-only checklist | "Run research on this plan", "do the review gate", "advance the flow one step", "status on this arch doc" |
| `arch-mini-plan` | the user wants a compact one-pass plan but still wants canonical arch blocks | the work is tiny enough for `lilarch` or large enough for full arch | "Give me the mini plan version", "one-pass arch plan for this task" |
| `lilarch` | contained 1-3 phase feature work | the task is migration-heavy, investigation-heavy, or broad | "Small feature, use lilarch", "tight feature flow for this improvement" |
| `bugs-flow` | regressions, crashes, incidents, Sentry/log-driven fixes | planned feature work or open-ended optimization | "Analyze this Sentry issue", "fix this bug and verify it" |
| `goal-loop` | the goal is clear but the path is unknown; repeated bets matter | the task already has a fixed implementation plan | "We need to improve this metric but don't know the path" |
| `north-star-investigation` | the user wants a quantified investigation with ranked hypotheses and brutal tests | the task is just a normal bug fix or plain goal loop | "Run a deep investigation on this performance issue" |
| `arch-flow` | the user already has a plan doc and wants status or next-step routing | they actually want the work performed | "What's next on this doc?", "continue the plan" |

## Near-lookalike boundaries

- `arch-plan` vs `arch-mini-plan`:
  - use `arch-mini-plan` only when the user wants a compressed one-pass plan
  - otherwise use `arch-plan`
- `arch-plan` vs `arch-step`:
  - use `arch-step` when the user wants literal command control, helpers, `advance`, or compact status
  - use `arch-plan` when they want the broader full-arch workflow handled by phase family or end-to-end
- `arch-flow` vs `arch-step`:
  - use `arch-flow` for read-only checklist and next-step routing
  - use `arch-step` when the user wants the concise stage-quality readout or wants `advance` to inspect and optionally execute one next full-arch step
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
  - `arch-step`
  - `bugs-flow`
  - `goal-loop`
  - `north-star-investigation`
  - `lilarch`
  - `arch-mini-plan`
  - `arch-plan`
- Keep each skill explanation to one sentence unless the user asks for more depth.
