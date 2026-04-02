---
name: north-star-investigation
description: "Run the standalone math-first investigation loop using a Commander's Intent doc, ranked hypotheses, and brutal tests. Use when a request needs quantitative sanity checks, fastest-learning bets, and an investigation worklog rather than a fixed implementation plan. Not for ordinary bug fixes, feature delivery, or generic goal loops that do not need this level of quantified hypothesis work."
metadata:
  short-description: "Quantitative investigation loop"
---

# North Star Investigation

Use this skill for the investigation workflow where quantitative reasoning and fastest-learning bets are the main job.

## When to use

- The task is an optimization or root-cause hunt where the best move is not yet obvious.
- The user wants a Commander's Intent style investigation doc with ranked hypotheses and brutal tests.
- Math, budgets, effect sizes, or measured-vs-assumed distinctions materially affect the investigation quality.

## When not to use

- The task is a straightforward bug fix with a normal bug doc. Use `bugs-flow`.
- The task is planned feature or architecture delivery. Use `arch-step`, `arch-mini-plan`, or `lilarch`.
- The user wants a generic open-ended goal loop without the quant-heavy investigation frame. Use `goal-loop`.

## Non-negotiables

- Start from the investigation doc and its worklog, not from memory.
- Math-first when the question is quantitative: call out what is measured vs assumed.
- Prefer brutal tests, traps, toggles, oracles, and minimal repros over wide logging.
- One highest-info bet at a time.
- Bootstrap mode is docs-first. Keep detailed evidence in the worklog.
- Keep ranked hypotheses current. Do not let stale theories linger as if they were equally likely.

## First move

1. Read `references/investigation-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Resolve the mode:
   - bootstrap or refresh the investigation doc
   - iterate on the next hypothesis
4. Resolve `DOC_PATH` and its worklog.
5. Re-read the North Star, scoreboard, and latest worklog before choosing the next bet.
6. Read the matching mode reference and `references/quality-bar.md`.

## Workflow

### 1) Bootstrap mode

- Create or refresh the investigation doc.
- Capture:
  - North Star
  - scope and non-negotiables
  - scoreboard
  - ground-truth anchors
  - quant model / sanity checks
  - ranked hypotheses
  - first 1-3 bets
- Seed the worklog with what you inspected and what you currently believe.

### 2) Iterate mode

- Print a short state of the union.
- Choose one bet with the highest information gain.
- Pre-commit the decision rule.
- Run the fastest brutal test that can settle the question.
- Append the worklog entry and update the hypotheses or next bet if the evidence changed the picture.

## Output expectations

- Keep the full detail in the worklog, not in console chatter.
- Console output should stay short:
  - North Star reminder
  - punchline
  - current best belief
  - biggest uncertainty
  - next bet and time budget
  - pointers to the doc/worklog

## Reference map

- `references/investigation-contract.md` - required doc components, worklog expectations, and loop rules
- `references/shared-doctrine.md` - math-first doctrine, hypothesis discipline, and boundary rules
- `references/bootstrap.md` - create or refresh the investigation doc and seed the first bets
- `references/iterate.md` - choose one highest-information bet and update the ranked hypotheses
- `references/quality-bar.md` - strong vs weak bars for quant models, hypotheses, and brutal tests
