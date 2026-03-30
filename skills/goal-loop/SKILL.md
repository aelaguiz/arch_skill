---
name: goal-loop
description: "Autonomous goal-seeking loop with a controller doc and append-only worklog. Use for open-ended optimization, investigation, or metric-improvement work where the goal is clear but the path is not. Not for fixed-scope architecture plans, small feature delivery, or ordinary bug fixes."
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

- The work already has a fixed-scope plan. Use `arch-plan`, `arch-mini-plan`, or `lilarch`.
- The task is a concrete bug investigation or fix. Use `bugs-flow`.
- The user needs a math-first Commander’s Intent investigation specifically. Use `north-star-investigation`.

## Non-negotiables

- The controller doc and append-only worklog are first-class. Read the worklog before every iteration.
- New or draft goal-loop docs require North Star confirmation before the loop becomes active.
- One iteration means one bet with a pre-committed decision rule.
- No reruns of the same bet without changing a lever or evidence surface.
- Setup mode is docs-only. Code changes only happen during iteration mode.

## First move

1. Read `references/controller-contract.md`.
2. Resolve the mode:
   - new or repair controller
   - readiness / flow-status
   - iterate
3. Resolve `DOC_PATH` and `WORKLOG_PATH`.
4. Read the most recent worklog entries before choosing a new bet.

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

- `references/controller-contract.md` - required blocks, worklog rules, and iteration protocol
