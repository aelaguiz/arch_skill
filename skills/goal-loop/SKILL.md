---
name: goal-loop
description: "Run the standalone goal-seeking loop with a controller doc and append-only worklog. Use for open-ended optimization, investigation, or metric-improvement work where the goal is clear but the path is not. Not for fixed-scope architecture plans, small feature delivery, or ordinary bug fixes."
metadata:
  short-description: "Open-ended goal-seeking loop"
---

# Goal Loop

Use this skill when the user has a North Star but does not yet know the best path.

## When to use

- The user wants to iterate toward a goal through repeated bets rather than follow a fixed implementation plan.
- The work is open-ended optimization, investigation, or metric improvement.
- Restart safety and compounding learning matter more than a one-shot plan.

## When not to use

- The work already has a fixed-scope plan. Use `arch-step`, `arch-mini-plan`, or `lilarch`.
- The task is a concrete bug investigation or fix. Use `bugs-flow`.
- The user needs a math-first Commander’s Intent investigation specifically. Use `north-star-investigation`.

## Non-negotiables

- The controller doc and append-only worklog are first-class. Read the worklog before every iteration.
- New or draft goal-loop docs require North Star confirmation before the loop becomes active.
- One iteration means one bet with a pre-committed decision rule.
- No reruns of the same bet without changing a lever or evidence surface.
- Setup mode is docs-only. Code changes only happen during iteration mode.
- Keep the loop honest about the best current belief and biggest uncertainty.

## First move

1. Read `references/controller-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Resolve the mode:
   - new or repair controller
   - readiness / flow-status
   - iterate
4. Resolve `DOC_PATH` and `WORKLOG_PATH`.
5. Read the most recent worklog entries before choosing a new bet.
6. Read the matching mode reference and `references/quality-bar.md`.

## Workflow

### 1) Setup or repair

- Create or repair the controller doc and the append-only worklog.
- Draft the North Star, scoreboard, lever inventory, and anti-sidetrack contract.
- Pause for North Star confirmation when the doc is new or still draft.

### 2) Flow-status

- If the user asks what is next, inspect the controller and worklog for readiness.
- Recommend the single best next move rather than reciting the whole doctrine.

### 3) Iterate

- Re-read the controller contract and the latest worklog entries.
- Choose one bet and pre-commit the decision rule.
- Do the minimum work needed for that bet.
- Run the smallest credible signal.
- Append exactly one worklog entry with evidence, learnings, and the next bet.

## Output expectations

- Update `DOC_PATH` and `WORKLOG_PATH` when the loop state changes.
- Keep the console output short:
  - North Star reminder
  - punchline
  - current best belief
  - biggest uncertainty
  - next bet
  - pointers to the controller/worklog

## Reference map

- `references/controller-contract.md` - required blocks, worklog rules, status rules, and loop contract
- `references/shared-doctrine.md` - loop discipline, bet quality, and anti-sidetrack rules
- `references/setup.md` - create or repair the controller and make the loop ready
- `references/iterate.md` - choose one bet, pre-commit the rule, and append one honest worklog entry
- `references/flow-status.md` - read-only readiness and next-bet recommendation rules
- `references/context-digest.md` - write or refresh the restart-safe digest only when requested
- `references/quality-bar.md` - strong vs weak controller state, bets, and worklog entries
