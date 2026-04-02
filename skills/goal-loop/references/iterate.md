# Goal Loop Iterate Mode

## Goal

Run exactly one high-information bet and append one honest worklog entry.

## Iteration order

1. Re-read the controller and latest worklog entries.
2. Choose the single best next bet.
3. Pre-commit the decision rule.
4. Do the minimum work needed to run the bet.
5. Run the smallest credible signal.
6. Append exactly one worklog entry.

## Decision-rule examples

- Good:
  - "If completion rises by at least 5 percent in this slice, keep the change and test expansion next."
  - "If the instrumentation shows abandonment before screen B, stop blaming the save path."
- Weak:
  - "We'll look at the results and decide later."
  - "If it seems better, keep going."

## De-dupe rule

- Do not rerun the same bet unchanged.
- Change a lever, audience, environment, or evidence surface before retrying.
