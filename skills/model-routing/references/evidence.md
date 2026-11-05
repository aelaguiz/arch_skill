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

## Each kind of work, level by level

Each score is the average blind score, 1 to 5, from Sol's judge and then Opus's judge. "First ran on" gives the setting each task started on, because the mix differs by kind: on planning it was two Sonnet at max, two Opus and one Sol. So "Score there" is not one model's top level, and a lower setting compares with it fairly only on the tasks that first ran on that same model. `task-types.md` makes that comparison where it matters, and names how many tasks it covers. Otherwise read along a row within one family, for the reason in the next section: each judge favours its own family, but a judge's lean is the same for two levels of one model. The rows run from where levels mattered least to where they mattered most.

| Kind of work | Tasks | First ran on | Score there | Opus medium | Opus low | Sonnet medium | Sonnet low | Haiku low | Sol high | Sol medium | Sol low |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Research a question from sources | 5 | Opus xhigh 3, Opus high 1, Opus max 1 | 2.6 / 4.4 | 2.6 / 4.2 | 2.2 / 3.2 | 2.0 / 3.4 | 2.2 / 3.6 | 1.8 / 2.2 | 3.8 / 4.0 | 3.6 / 4.0 | 3.8 / 4.2 |
| Judge images or frames against a standard | 5 | Sonnet max 3, Opus high 1, Sol xhigh 1 | 4.0 / 4.2 | 3.2 / 4.0 | 2.2 / 3.2 | 2.6 / 3.8 | 2.4 / 3.2 | 2.2 / 2.6 | 4.0 / 4.0 | 3.8 / 4.0 | 4.0 / 4.0 |
| Work out a problem with one right answer | 4 | Opus high 2, Sol high 1, Sol xhigh 1 | 3.5 / 3.2 | 2.5 / 3.5 | 2.8 / 3.0 | 2.8 / 3.0 | 2.8 / 3.0 | 2.8 / 2.5 | 4.3 / 3.0 | 4.5 / 3.5 | 4.2 / 3.2 |
| Check another agent's work against its brief | 4 | Opus xhigh 3, Opus max 1 | 3.8 / 4.8 | 3.2 / 4.5 | 2.8 / 4.0 | 2.5 / 3.2 | 2.2 / 3.2 | 2.5 / 2.8 | 4.8 / 4.0 | 4.5 / 4.0 | 4.8 / 4.0 |
| Write an internal document | 3 | Opus xhigh 3 | 3.3 / 4.7 | 3.7 / 4.3 | 3.3 / 4.0 | 2.7 / 4.0 | 2.3 / 3.0 | 2.7 / 3.0 | 4.3 / 3.3 | 4.0 / 3.7 | 4.0 / 3.3 |
| Read a document cold | 4 | Opus xhigh 2, Opus max 1, Sonnet max 1 | 3.0 / 4.2 | 2.5 / 3.2 | 2.8 / 4.0 | 2.2 / 2.8 | 2.2 / 2.5 | 2.0 / 3.8 | 3.2 / 3.5 | 3.5 / 3.5 | 3.2 / 3.5 |
| Analyze a dataset | 5 | Opus xhigh 3, Opus max 1, Sol xhigh 1 | 2.8 / 4.2 | 2.2 / 3.8 | 2.2 / 2.4 | 2.2 / 3.2 | 2.2 / 2.8 | 2.6 / 2.4 | 4.2 / 3.4 | 4.0 / 3.6 | 3.4 / 3.0 |
| Check numbers and quotes against sources | 6 | Opus xhigh 2, Sol xhigh 1, Opus max 1, Sonnet max 1, Opus high 1 | 4.2 / 4.7 | 3.2 / 4.0 | 2.0 / 3.0 | 2.5 / 3.5 | 2.0 / 2.7 | 1.8 / 2.5 | 4.5 / 3.8 | 3.8 / 3.8 | 3.8 / 3.8 |
| Label items by a codebook | 5 | Sonnet max 3, Opus max 1, Opus xhigh 1 | 3.6 / 4.4 | 3.8 / 4.8 | 3.4 / 3.6 | 3.0 / 3.4 | 2.8 / 2.8 | 2.6 / 2.8 | 4.0 / 3.8 | 3.8 / 3.6 | 3.2 / 3.4 |
| Plan or design work | 5 | Sonnet max 2, Opus xhigh 1, Opus max 1, Sol xhigh 1 | 4.2 / 4.8 | 2.8 / 4.0 | 2.6 / 3.8 | 2.4 / 4.0 | 2.6 / 3.8 | 2.0 / 2.4 | 4.8 / 3.8 | 5.0 / 3.4 | 4.6 / 3.2 |
| Write short copy people read | 5 | Opus max 2, Sonnet max 1, Opus medium 1, Opus xhigh 1 | 4.0 / 4.6 | 3.0 / 3.5 | 2.2 / 2.6 | 2.8 / 3.4 | 2.4 / 3.2 | 2.0 / 2.4 | 4.5 / 4.0 | 4.5 / 3.8 | 3.0 / 2.8 |
| Explain how code behaves or why it broke | 4 | Opus xhigh 3, Opus high 1 | 4.0 / 4.8 | 3.8 / 5.0 | 2.0 / 2.2 | 2.2 / 2.5 | 2.2 / 2.8 | 2.2 / 2.0 | 4.0 / 4.0 | 3.8 / 2.8 | 3.8 / 3.2 |
| Judge writing against a standard | 5 | Opus xhigh 2, Opus high 2, Opus max 1 | 3.4 / 4.6 | 3.2 / 4.2 | 2.8 / 3.0 | 2.4 / 3.6 | 1.8 / 2.6 | 2.0 / 2.8 | 4.6 / 3.6 | 3.2 / 2.6 | 2.8 / 2.4 |
| Review code or a plan | 5 | Sol xhigh 4, Opus high 1 | 4.0 / 4.5 | 2.4 / 3.8 | 2.0 / 3.0 | 2.0 / 3.8 | 2.6 / 3.5 | 2.2 / 2.8 | 4.2 / 4.5 | 3.6 / 3.5 | 3.8 / 4.0 |
| Build a content item through its steps | 6 | Opus xhigh 3, Opus high 1, Sol xhigh 1, Opus medium 1 | 3.2 / 4.3 | 2.6 / 4.2 | 2.3 / 4.0 | 2.2 / 3.7 | 1.8 / 3.3 | 2.2 / 3.2 | 3.0 / 3.3 | 2.8 / 3.0 | 2.7 / 2.8 |
| Translate text | 5 | Opus max 3, Opus xhigh 2 | 4.8 / 5.0 | 4.0 / 4.2 | 3.0 / 3.2 | 3.0 / 3.2 | 2.6 / 2.8 | 2.0 / 2.2 | 4.0 / 3.2 | 4.2 / 3.2 | 3.8 / 3.0 |

Each kind has 3 to 6 tasks, so a row is a direction, not a verdict. Across all kinds, Sol at high scored 3.9, medium 3.7 and low 3.5, and misled on 4%, 12% and 10% of tasks. Terra and Astra weren't in this test, and neither were writing code, builds or device work, because the test was stopped before its code-writing tasks ran.

## Why the scores don't rank one family against the other

Each judge scored its own family's answers about 1.5 points higher than the other judge did, though neither knew which model wrote which answer. Sol's judge put Sol at high 0.6 points above the original Opus answers; Opus's judge put it 0.9 below. Averaging the two does not remove that, so the back-test cannot say whether Sol can replace Opus or the reverse. Settling it needs a judge from neither family, or tasks whose answers can be checked.

## What real use showed afterwards

An audit of every Codex and Claude session across five machines, October 29 to November 5, 2026.

- 1,565 of the 1,621 helpers at the two top levels had inherited that level or forked. Nobody had chosen it.
- Reviewers on a timer at the top Codex model took 59% of that week's Codex allowance. Of 2,086 check-ins read closely, 576 came after a session that had done nothing but handle the last review.
- One plan took 179 reviews across 22 drafts, each reasonable from inside its round.
- A build check at medium wrote 18k tokens in about 4 minutes, and at max 113k tokens in about 20.
- No Terra xhigh build from a full spec was found that Sol had to redo. 13 of 105 cheap device workers died on a request error, which says nothing about the model's work.

## Crossing families and small jobs

28 runs, November 5, 2026: four small jobs with known answers through seven routes from both parents. All 28 were right, so this measures speed and cost, not quality. Sonnet at medium beat crossing to Sol at high on speed on all four jobs (44 against 82 seconds in total) and tied on cost ($0.36 against $0.38 with the parent). The numbers are in `costs.md`. This is why "Mechanical work" and "Fix a well-defined bug" name Sonnet at medium: those rows end in a check. It rests on two small code jobs, against a back-test where Sonnet at medium misled on about 3 tasks in 10 with no check at the end.

A second round gave Sol at high and Terra at xhigh one identical brief from both parents, and most of a remaining gap closed: see the end of `costs.md`.

## A timed reviewer moved to a cheaper model

November 5, 2026: 20 saved check-ins from three long-running jobs reran on Sol 6.1 at high, from a frozen copy of what each session had done. The test counted only findings the session really acted on after Astra 6.0 at xhigh raised them: 52 of the 92 it raised. Two readers marked each one without knowing who wrote it, and agreed on 43.

| | Raised | Partly | Missed |
|---|---:|---:|---:|
| Sol at high, all 52 | 33% to 40% | 17% to 31% | 37% to 42% |
| 25 that changed real work | 7 to 12 | 6 to 14 | 4 to 7 |
| 9 that corrected what a person had been told | 4 | 1 | 4 |
| 18 that corrected a record or note | 5 to 6 | 1 to 2 | 11 |

The step moved the model and the level together, so these figures describe Sol at high and say nothing about Sol at xhigh, which wasn't tested on this job. They are also a floor on what Sol at high would catch live: it had no live records, no earlier thread and shortened tool output. Of the 19 findings both readers said it missed, the evidence was fully in its copy for 4. Astra rerun from the same frozen copies also lost findings, missing 2 to 4 of 14 on five looks where Sol missed 4 to 5, so that gap is too small to divide between the model and the setup.

Sol lost most on the job where reviews most often change real work, though that job's reviews also lean most on files a transcript doesn't hold. It lost least on the job whose reviews mostly correct records. Readers counted 24 to 33 further findings from Sol that would change real work, and nobody checked whether those were true. A cold look cost $0.53 on Sol at high against $3.75 on Astra at xhigh, about a seventh, and Astra's live look cost $7.43. Price per token alone says a fifth, but that ignores what the level does to the tokens.

## How firm the rows are

`task-types.md` says what stands behind each row. Rows with a task count rest on the level-by-level scores above, compared within a family. Rows marked not measured are starting guesses from field use. Opus at high was measured on 15 tasks, plus 4 blind-scored on November 5, where it pulled clearly ahead of Opus at medium on none. Terra at xhigh and Astra at xhigh were run on a few real tasks each, November 5: neither pulled clearly ahead of or behind Sol on blind scores, on three tasks a side.

## Measuring again

When a new model or level arrives, `$model-eval` runs the back-test again for it and updates this skill from the result. The first run's method, log, tasks, tooling and scores are in psbrain at `projects/agent-watcher/efficiency-profile/task-routing/`.
