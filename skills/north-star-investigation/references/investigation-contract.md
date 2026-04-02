# North Star Investigation Contract

## Required doc components

The investigation doc should contain:

- North Star
- scope
- non-negotiables
- scoreboard
- ground-truth anchors
- quant model / sanity checks
- ranked hypotheses
- first iteration plan
- authoritative worklog

Optional when they materially improve the investigation:

- traps or toggles
- oracles
- measurement caveats
- explicit dead hypotheses

## Worklog expectations

Every loop should append the evidence trail:

- what changed
- commands run
- artifacts produced
- raw result
- conclusion
- next-step recommendation

Keep detailed evidence in the worklog. Keep the stable controller sections concise.

## Loop rules

- re-read the North Star, scope, non-negotiables, and scoreboard every iteration
- choose one bet
- pre-commit the decision rule
- avoid rerunning the same test unchanged
- prefer negative proofs, traps, toggles, oracles, or minimal repros

## Question rule

Only ask the user when:

- a true product decision is required
- an external constraint cannot be inferred
- access or permissions block the work
