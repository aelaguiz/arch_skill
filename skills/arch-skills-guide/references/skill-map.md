# Arch Skills Guide Map

Use this file when the user wants help choosing between the arch subskills.

## Decision order

Start with the strongest discriminator first:

1. Is the ask mostly "what's next?" on an existing plan doc?
   - use `arch-flow`
2. Is the ask mainly docs cleanup, stale-doc consolidation, or working-doc retirement with code truth stable enough to trust?
   - use `arch-docs`
3. Is the ask for broad, ambiguity-heavy, or helper-heavy full arch work?
   - use `arch-step`
4. Is the ask for faster full-arch work on a smaller well-defined feature, still with phasing and real auto controllers?
   - use `miniarch-step`
5. Is it a repo-wide map-first comment hardening pass focused on shared contracts, conventions, gotchas, or subtle behavior in code?
   - use `comment-loop`
6. Is it a repo-wide audit pass, systematic defect hunt, or leave-it-running cleanup loop?
   - use `audit-loop`
7. Is it a repo-wide real-app automation audit loop with a simulator ledger?
   - use `audit-loop-sim`
8. Is the ask a generic hook-backed completion loop over free-form requirements, with no prescribed map-first flow, optional `$skill` audit obligations, and optional runtime/cadence/iteration caps?
   - use `arch-loop`
9. Is it a bug, regression, crash, incident, or Sentry/log investigation?
   - use `bugs-flow`
10. Is the path unknown and the work open-ended?
   - use `goal-loop`
11. Is it a quant-heavy optimization or root-cause hunt with ranked hypotheses and brutal tests?
   - use `north-star-investigation`
12. Is it a small feature or improvement that should fit in 1-3 phases?
   - use `lilarch`
13. Does the user want a one-pass mini plan with canonical arch blocks?
   - use `arch-mini-plan`
14. Otherwise, default to `arch-step`.

## Skill map

| Skill | Use when | Do not default to it when | Example asks |
| --- | --- | --- | --- |
| `arch-step` | the user wants the broad full arch workflow, a specific helper-heavy full-arch command, or a generic full-arch continuation where scope or architecture may still widen materially | they only need a read-only checklist, a one-pass mini plan, or a smaller well-defined feature that fits the faster full-arch tier | "Do the full arch flow", "Run research on this plan", "do the review gate", "advance the flow one step", "audit implementation vs plan" |
| `miniarch-step` | the user wants the faster full-arch workflow for a smaller well-defined feature that still needs canonical arch blocks, phased execution, and real auto controllers | the work is tiny enough for `lilarch`, planning-only, or broad enough to need the full `arch-step` helper surface | "Use the faster full arch flow for this feature", "run miniarch-step on this plan", "do the quick full-arch pass with auto-plan and implement-loop" |
| `arch-docs` | the code is already clean enough to trust and the main job is cleaning stale, overlapping, or misleading docs, including post-arch plan/worklog retirement | the feature still needs code work, or the ask is generic copy editing or net-new documentation authoring | "Clean up the docs in this repo", "retire this plan/worklog and fold the truth into evergreen docs", "run the docs cleanup loop" |
| `arch-mini-plan` | the user wants a compact one-pass plan but still wants canonical arch blocks | the work is tiny enough for `lilarch` or needs actual full-arch execution now | "Give me the mini plan version", "one-pass arch plan for this task" |
| `lilarch` | contained 1-3 phase feature work | the task is migration-heavy, investigation-heavy, or broad | "Small feature, use lilarch", "tight feature flow for this improvement" |
| `bugs-flow` | regressions, crashes, incidents, Sentry/log-driven fixes | planned feature work or open-ended optimization | "Analyze this Sentry issue", "fix this bug and verify it" |
| `comment-loop` | the user wants a repo-wide code comment pass, wants the agent to deeply understand the repo before explaining it, or wants shared contracts, conventions, gotchas, and subtle behavior documented in code | the job is docs cleanup, one local comment tweak, or bug fixing | "Map this repo and add the comments that actually matter", "deeply understand the codebase before commenting conventions", "keep hardening the high-value code comments until the real gaps are gone" |
| `audit-loop` | the user wants a repo-wide audit pass, the next worthwhile defect fixed, or a bounded cleanup loop that keeps going until review says stop | there is already one concrete known bug or the main job is docs cleanup | "Scan this repo for bugs and fix what matters", "do one audit pass", "keep cleaning this codebase until no worthwhile audit work remains" |
| `audit-loop-sim` | the user wants a repo-wide real-app automation pass with a simulator ledger and a consequence-first ranking | the real job is one concrete regression, docs cleanup, or non-automation audit | "Find the biggest automation blind spots in the real app", "keep running the simulator audit loop" |
| `arch-loop` | the user wants a generic hook-backed completion loop over free-form requirements, optional named-skill audit obligations (e.g. `$agent-linter`, `$code-review`), and optional runtime/cadence/iteration caps, with a fresh Codex `gpt-5.4` `xhigh` external evaluator as the only stop authority | the work fits a prescribed map-first loop (`audit-loop`, `comment-loop`, `audit-loop-sim`), is a pure condition-poll (`delay-poll`), or is a one-shot sleep (`wait`) | "Tighten this onboarding copy until it reads cleanly on mobile", "rewrite this AGENTS.md with `$agent-linter` as a required clean audit", "every 30 minutes check whether staging is reachable and keep fixing infra until it is, max 8 hours" |
| `goal-loop` | the goal is clear but the path is unknown; repeated bets matter | the task already has a fixed implementation plan | "We need to improve this metric but don't know the path" |
| `north-star-investigation` | the user wants a quantified investigation with ranked hypotheses and brutal tests | the task is just a normal bug fix or plain goal loop | "Run a deep investigation on this performance issue" |
| `arch-flow` | the user already has a plan doc and wants a read-only checklist or next-step routing | they actually want the work performed | "What's next on this doc?", "give me the checklist before we run anything" |

## Near-lookalike boundaries

- `arch-flow` vs `arch-step`:
  - use `arch-flow` for read-only checklist and next-step routing
  - use `arch-step` or `miniarch-step` when the user wants continuation, the concise stage-quality readout, or `advance` to inspect and optionally execute one next full-arch step
- `arch-step` vs `miniarch-step`:
  - use `miniarch-step` when the work is still full arch, but smaller, well-defined, and best served by one research pass plus one deep-dive pass
  - use `arch-step` when ambiguity, breadth, or helper needs justify the broader surface
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
- `arch-loop` vs specialized loops (`audit-loop`, `comment-loop`, `audit-loop-sim`):
  - use the specialized loop when the user actually wants that skill's prescribed map-first flow, artifact contract, and ranking
  - use `arch-loop` when the requirements are free-form, the "done" signal is an external Codex evaluator verdict, or the user wants named `$skill` audit obligations and optional runtime/cadence/iteration caps
- `arch-loop` vs `delay-poll`:
  - use `delay-poll` when the job is purely "wait and re-check a condition" with no parent work happening between checks
  - use `arch-loop` when the loop has actual requirements to satisfy, or needs repeat parent work until a Codex evaluator says `clean` or `blocked`
- `arch-loop` vs `wait`:
  - use `wait` when the user wants a one-shot sleep then a single literal resume prompt
  - use `arch-loop` when the loop must run until completion requirements are met, not on a fixed clock
- `arch-loop` vs `goal-loop`:
  - use `goal-loop` when the user wants the controller-doc plus append-only iteration log shape
  - use `arch-loop` when the user wants native hook-backed repeat turns and an external Codex evaluator as the stop authority
- `arch-docs` vs `audit-loop`:
  - use `arch-docs` when the main job is documentation cleanup grounded in already-stable code truth
  - use `audit-loop` when the main job is code audit, defect finding, dead-code deletion, or duplication cleanup
- `miniarch-step` vs `arch-mini-plan`:
  - use `arch-mini-plan` only when the user wants a compressed one-pass plan
  - use `miniarch-step` when the user wants faster full-arch execution against the same canonical doc
- `miniarch-step` vs `lilarch`:
  - use `lilarch` for true small-feature delivery with start/plan/finish
  - use `miniarch-step` when the change is still smallish but needs the canonical full-arch artifact and full-arch audit loop
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
  - `miniarch-step`
  - `comment-loop`
  - `audit-loop`
  - `audit-loop-sim`
  - `arch-loop`
  - `bugs-flow`
  - `goal-loop`
  - `north-star-investigation`
  - `lilarch`
  - `arch-mini-plan`
- Keep each skill explanation to one sentence unless the user asks for more depth.
