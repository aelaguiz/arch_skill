# Arch Skills Guide Boundary Examples

## Broad full arch vs faster full arch

- "This is still full arch work, but the feature is small and well-defined. Go fast":
  - `miniarch-step`
- "This migration is broad, ambiguous, or needs the helper passes":
  - `arch-step`

## Faster full arch vs mini plan

- "I want the faster full arch workflow, not just a one-pass plan":
  - `miniarch-step`
- "Give me the mini plan version in one pass":
  - `arch-mini-plan`

## Full arch vs mini plan

- "Do the full arch flow for this migration":
  - `arch-step`
- "Give me the mini plan version in one pass":
  - `arch-mini-plan`

## Full arch vs read-only flow

- "What is the next move on this doc?":
  - `arch-flow`
- "Advance this doc and run the next step":
  - `arch-step`

## Full arch vs docs cleanup

- "Implement the plan and audit the code against it":
  - `arch-step`
- "The code is clean; now clean up the feature docs and retire the plan doc":
  - `arch-docs`

## Single bug vs audit loop

- "Analyze this Sentry crash and fix it":
  - `bugs-flow`
- "Scan the repo for the next real bugs and keep cleaning until it is not worth continuing":
  - `audit-loop`

## Docs cleanup vs comment loop

- "The code is stable; explain the conventions and gotchas in code comments":
  - `comment-loop`
- "The code is stable; clean up the docs and retire stale working notes":
  - `arch-docs`

## Comment loop vs audit loop

- "Deeply map this repo, then add the comments that actually matter":
  - `comment-loop`
- "Deeply map this repo, then fix the biggest real bugs and proof gaps":
  - `audit-loop`

## Faster full arch vs lilarch

- "This is too serious for lilarch, but still a small well-defined feature":
  - `miniarch-step`
- "This should fit in 1-3 phases, use little arch":
  - `lilarch`

## Mini plan vs lilarch

- "Small feature, but I still want the canonical architecture blocks":
  - `arch-mini-plan`
- "This should fit in 1-3 phases, use little arch":
  - `lilarch`

## Bugs vs investigation loops

- "We need to explain a metric drop and test ranked hypotheses":
  - `north-star-investigation`
- "We know the goal but not the path, keep iterating bets":
  - `goal-loop`

## Specialized loops vs generic completion loop

- "Keep tightening the onboarding copy across the marketing site until it reads well on mobile":
  - `arch-loop`
- "Rewrite this AGENTS.md file with `$agent-linter` as a required clean audit":
  - `arch-loop`
- "Every 30 minutes check whether staging is reachable and keep fixing infra until it is, max 8 hours":
  - `arch-loop`
- "Scan this repo for bugs and fix what matters, consequence-first":
  - `audit-loop`
- "Deeply map this repo, then add the comments that actually matter":
  - `comment-loop`
- "Find the biggest automation blind spots in the real app and keep closing them":
  - `audit-loop-sim`

## Generic completion loop vs pure wait/poll

- "Wait 1h30m then continue investigating the flaky test":
  - `wait`
- "Every 30 minutes check whether branch X has been pushed; when it is, integrate it":
  - `delay-poll`
- "Every 30 minutes check whether staging is reachable and keep fixing infra until it is, max 8 hours":
  - `arch-loop` (parent work between checks, external evaluator decides when to stop)
