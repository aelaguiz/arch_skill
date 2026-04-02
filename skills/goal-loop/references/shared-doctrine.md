# Goal Loop Shared Doctrine

## Core rules

- The controller doc names the durable truth.
- The worklog is append-only memory, not a second controller.
- Read the most recent entries before picking a new bet.
- One iteration means one bet, one decision rule, one worklog entry.
- Do not confuse movement with learning. A bet that does not reduce uncertainty should usually not be run.

## Bet discipline

- Strong bets:
  - have a clear lever
  - have a pre-committed decision rule
  - can meaningfully update the current best belief
- Weak bets:
  - are really implementation projects in disguise
  - rerun the previous experiment unchanged
  - gather broad logs with no decision threshold

## Anti-sidetrack examples

- Good:
  - "change ranking threshold from X to Y and measure effect on retention"
  - "instrument this one funnel step to settle whether abandonment is on entry or save"
- Bad:
  - "refactor the whole subsystem before the next bet"
  - "run a bunch of exploratory tweaks and see what happens"
