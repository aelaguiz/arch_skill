# North Star Investigation Iterate

## Goal

Run the single highest-information bet, update the worklog, and rerank the hypotheses honestly.

## Iteration order

1. Re-read the North Star, scoreboard, and latest worklog.
2. Choose one bet with the highest information gain.
3. Pre-commit the decision rule.
4. Run the fastest brutal test that can settle the question.
5. Append the worklog entry.
6. Update the ranked hypotheses if the evidence changed the picture.

## Brutal-test examples

- trap the suspected path and prove the symptom disappears
- toggle one suspected bottleneck off and compare the metric
- use an oracle or minimal repro instead of broad instrumentation

## Bad iteration behavior

- rerun the last test unchanged
- collect more logs because the current story feels incomplete
- keep the same ranking after contradictory evidence
