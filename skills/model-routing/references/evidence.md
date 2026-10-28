# The evidence behind model-routing

Measured October 27, 2026, on Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 and GPT-6.1 Sol (Codex Fast tier). When these models are replaced, the numbers below are history; the shape (a strong model at a lower level beats a smaller model) is the first guess to test again.

## What was measured

78 real helper tasks from two weeks of agent work, across 17 kinds, were rerun on the setting they first ran on (most often Opus at xhigh or max) and on lower settings. Reruns were sandboxed: they read what the original read and could not send, post, push or deploy. Two judges, Sol at high and Opus at medium, scored every answer 1 to 5 without knowing which setting wrote it. "Misled" counts answers two or more points below the original setting's on the same task. Time is the median of each rerun's wall-clock time over the original setting's rerun of the same task, under the same load.

## Lowering the level on the same model

Both judges agree on these, because each compares a model with itself.

| Step down | Tasks | Score change, judge 1 / judge 2 |
|---|---:|---|
| Opus at xhigh or max to Opus at medium | 52 | −0.4 / −0.4 |
| Sol at xhigh to Sol at high | 9 | −0.2 / 0.0 |
| Sonnet at max to Sonnet at medium | 13 | −1.1 / −1.1 |

## Every setting against the original, all tasks

| Setting | Tasks | Score change | Misled | Time |
|---|---:|---:|---:|---:|
| The original setting, run a second time | 37 | 0.0 | 0 (0%) | 101% |
| Opus at medium | 76 | −0.5 | 5 (7%) | 39% |
| Opus at low | 78 | −1.2 | 23 (29%) | 13% |
| Sonnet at medium | 78 | −1.1 | 25 (32%) | 28% |
| Sonnet at low | 78 | −1.4 | 31 (40%) | 19% |
| Haiku at low | 78 | −1.6 | 40 (51%) | 24% |

## The examples, kind by kind (Opus at medium against the original)

| Kind of task | Tasks | Score change | Misled | Time |
|---|---:|---:|---:|---:|
| Research a question from sources | 5 | −0.1 | 0 | 51% |
| Analyze a dataset | 5 | −0.5 | 0 | 40% |
| Label items by a codebook | 5 | +0.3 | 0 | 26% |
| Explain how code behaves or why it broke | 4 | 0.0 | 0 | 58% |
| Work out a problem with one right answer | 4 | −0.4 | 0 | 73% |
| Check another agent's work against its brief | 4 | −0.4 | 0 | 43% |
| Judge images or frames against a standard | 5 | −0.5 | 0 | 26% |
| Judge writing against a standard | 5 | −0.3 | 0 | 42% |

Each kind has 4 or 5 tasks, so a row is a direction, not a verdict.

## Why the skill does not move work between Claude and Sol

Each judge scored its own family's answers about 1.5 points higher than the other judge did, though neither knew which model wrote which answer. Sol's judge put Sol at high 0.6 points above the original Opus answers; Opus's judge put it 0.9 below. Averaging the two does not remove that, so the back-test cannot say whether Sol can replace Opus or the reverse. Settling it needs a judge from neither family, or tasks whose answers can be checked.

## Measuring again

The back-test's scripts, tasks, runs and scores are in psbrain at `projects/agent-watcher/efficiency-profile/task-routing/` (method and log in `PLAN.md`; `backtest.py` reruns, `judge.py` scores, `analyze_scores.py` tabulates). To check a new model or level, rerun a few tasks of each kind on it beside the current setting, and score them with judges who compare a model with itself, or from neither family.
