# North Star Investigation Iterate

Iterate mode for north-star-investigation: run the single highest-information bet, update the worklog, and rerank the hypotheses honestly.

## Goal

Run the single highest-information bet, update the worklog, and rerank the hypotheses honestly.

## Iteration order

- Re-read the North Star, scoreboard, and latest worklog.
- Choose one bet with the highest information gain.
- Pre-commit the decision rule.
- Run the fastest brutal test that can settle the question.
- Append the worklog entry.
- Update the ranked hypotheses if the evidence changed the picture.

## Brutal-test examples

- trap the suspected path and prove the symptom disappears
- toggle one suspected bottleneck off and compare the metric
- use an oracle or minimal repro instead of broad instrumentation

## Bad iteration behavior

- rerun the last test unchanged
- collect more logs because the current story feels incomplete
- keep the same ranking after contradictory evidence
