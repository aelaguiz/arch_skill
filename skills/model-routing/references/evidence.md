# The evidence behind model-routing

Measured October 27, 2026, on Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 and GPT-6.1 Sol 6.1 (Codex Fast tier). When these models are replaced, the numbers below are history; the shape (a strong model at a lower level beats a smaller model) is the first guess to test again.

## What was measured

78 real helper tasks from two weeks of agent work, across 17 kinds, were rerun on the setting they first ran on (most often Opus 5.5 at xhigh or max) and on lower settings. Reruns were sandboxed: they read what the original read and could not send, post, push or deploy. Two judges, Sol 6.1 at high and Opus 5.5 at medium, scored every answer 1 to 5 without knowing which setting wrote it. "Misled" counts answers two or more points below the original setting's on the same task. Time is the median of each rerun's wall-clock time over the original setting's rerun of the same task, under the same load.

## Lowering the level on the same model

Both judges agree on these, because each compares a model with itself.

| Step down | Tasks | Score change, judge 1 / judge 2 |
|---|---:|---|
| Opus 5.5 at xhigh or max to Opus 5.5 at medium | 52 | −0.4 / −0.4 |
| Sol 6.1 at xhigh to Sol 6.1 at high | 9 | −0.2 / 0.0 |
| Sonnet 5.5 at max to Sonnet 5.5 at medium | 13 | −1.1 / −1.1 |

## Every setting against the original, all tasks

| Setting | Tasks | Score change | Misled | Time |
|---|---:|---:|---:|---:|
| The original setting, run a second time | 37 | 0.0 | 0 (0%) | 101% |
| Opus 5.5 at medium | 76 | −0.5 | 5 (7%) | 39% |
| Opus 5.5 at low | 78 | −1.2 | 23 (29%) | 13% |
| Sonnet 5.5 at medium | 78 | −1.1 | 25 (32%) | 28% |
| Sonnet 5.5 at low | 78 | −1.4 | 31 (40%) | 19% |
| Haiku 5.5 at low | 78 | −1.6 | 40 (51%) | 24% |

## Each kind of work, level by level

Each score is the average blind score, 1 to 5, from Sol 6.1's judge and then Opus 5.5's judge. "First ran on" gives the setting each task started on, because the mix differs by kind: on planning it was two Sonnet 5.5 at max, two Opus 5.5 and one Sol 6.1. So "Score there" is not one model's top level, and a lower setting compares with it fairly only on the tasks that first ran on that same model. `task-types.md` makes that comparison where it matters, and names how many tasks it covers. Otherwise read along a row within one family, for the reason in the next section: each judge favours its own family, but a judge's lean is the same for two levels of one model. The rows run from where levels mattered least to where they mattered most.

| Kind of work | Tasks | First ran on | Score there | Opus 5.5 medium | Opus 5.5 low | Sonnet 5.5 medium | Sonnet 5.5 low | Haiku 5.5 low | Sol 6.1 high | Sol 6.1 medium | Sol 6.1 low |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Research a question from sources | 5 | Opus 5.5 xhigh 3, Opus 5.5 high 1, Opus 5.5 max 1 | 2.6 / 4.4 | 2.6 / 4.2 | 2.2 / 3.2 | 2.0 / 3.4 | 2.2 / 3.6 | 1.8 / 2.2 | 3.8 / 4.0 | 3.6 / 4.0 | 3.8 / 4.2 |
| Judge images or frames against a standard | 5 | Sonnet 5.5 max 3, Opus 5.5 high 1, Sol 6.1 xhigh 1 | 4.0 / 4.2 | 3.2 / 4.0 | 2.2 / 3.2 | 2.6 / 3.8 | 2.4 / 3.2 | 2.2 / 2.6 | 4.0 / 4.0 | 3.8 / 4.0 | 4.0 / 4.0 |
| Work out a problem with one right answer | 4 | Opus 5.5 high 2, Sol 6.1 high 1, Sol 6.1 xhigh 1 | 3.5 / 3.2 | 2.5 / 3.5 | 2.8 / 3.0 | 2.8 / 3.0 | 2.8 / 3.0 | 2.8 / 2.5 | 4.3 / 3.0 | 4.5 / 3.5 | 4.2 / 3.2 |
| Check another agent's work against its brief | 4 | Opus 5.5 xhigh 3, Opus 5.5 max 1 | 3.8 / 4.8 | 3.2 / 4.5 | 2.8 / 4.0 | 2.5 / 3.2 | 2.2 / 3.2 | 2.5 / 2.8 | 4.8 / 4.0 | 4.5 / 4.0 | 4.8 / 4.0 |
| Write an internal document | 3 | Opus 5.5 xhigh 3 | 3.3 / 4.7 | 3.7 / 4.3 | 3.3 / 4.0 | 2.7 / 4.0 | 2.3 / 3.0 | 2.7 / 3.0 | 4.3 / 3.3 | 4.0 / 3.7 | 4.0 / 3.3 |
| Read a document cold | 4 | Opus 5.5 xhigh 2, Opus 5.5 max 1, Sonnet 5.5 max 1 | 3.0 / 4.2 | 2.5 / 3.2 | 2.8 / 4.0 | 2.2 / 2.8 | 2.2 / 2.5 | 2.0 / 3.8 | 3.2 / 3.5 | 3.5 / 3.5 | 3.2 / 3.5 |
| Analyze a dataset | 5 | Opus 5.5 xhigh 3, Opus 5.5 max 1, Sol 6.1 xhigh 1 | 2.8 / 4.2 | 2.2 / 3.8 | 2.2 / 2.4 | 2.2 / 3.2 | 2.2 / 2.8 | 2.6 / 2.4 | 4.2 / 3.4 | 4.0 / 3.6 | 3.4 / 3.0 |
| Check numbers and quotes against sources | 6 | Opus 5.5 xhigh 2, Sol 6.1 xhigh 1, Opus 5.5 max 1, Sonnet 5.5 max 1, Opus 5.5 high 1 | 4.2 / 4.7 | 3.2 / 4.0 | 2.0 / 3.0 | 2.5 / 3.5 | 2.0 / 2.7 | 1.8 / 2.5 | 4.5 / 3.8 | 3.8 / 3.8 | 3.8 / 3.8 |
| Label items by a codebook | 5 | Sonnet 5.5 max 3, Opus 5.5 max 1, Opus 5.5 xhigh 1 | 3.6 / 4.4 | 3.8 / 4.8 | 3.4 / 3.6 | 3.0 / 3.4 | 2.8 / 2.8 | 2.6 / 2.8 | 4.0 / 3.8 | 3.8 / 3.6 | 3.2 / 3.4 |
| Plan or design work | 5 | Sonnet 5.5 max 2, Opus 5.5 xhigh 1, Opus 5.5 max 1, Sol 6.1 xhigh 1 | 4.2 / 4.8 | 2.8 / 4.0 | 2.6 / 3.8 | 2.4 / 4.0 | 2.6 / 3.8 | 2.0 / 2.4 | 4.8 / 3.8 | 5.0 / 3.4 | 4.6 / 3.2 |
| Write short copy people read | 5 | Opus 5.5 max 2, Sonnet 5.5 max 1, Opus 5.5 medium 1, Opus 5.5 xhigh 1 | 4.0 / 4.6 | 3.0 / 3.5 | 2.2 / 2.6 | 2.8 / 3.4 | 2.4 / 3.2 | 2.0 / 2.4 | 4.5 / 4.0 | 4.5 / 3.8 | 3.0 / 2.8 |
| Explain how code behaves or why it broke | 4 | Opus 5.5 xhigh 3, Opus 5.5 high 1 | 4.0 / 4.8 | 3.8 / 5.0 | 2.0 / 2.2 | 2.2 / 2.5 | 2.2 / 2.8 | 2.2 / 2.0 | 4.0 / 4.0 | 3.8 / 2.8 | 3.8 / 3.2 |
| Judge writing against a standard | 5 | Opus 5.5 xhigh 2, Opus 5.5 high 2, Opus 5.5 max 1 | 3.4 / 4.6 | 3.2 / 4.2 | 2.8 / 3.0 | 2.4 / 3.6 | 1.8 / 2.6 | 2.0 / 2.8 | 4.6 / 3.6 | 3.2 / 2.6 | 2.8 / 2.4 |
| Review code or a plan | 5 | Sol 6.1 xhigh 4, Opus 5.5 high 1 | 4.0 / 4.5 | 2.4 / 3.8 | 2.0 / 3.0 | 2.0 / 3.8 | 2.6 / 3.5 | 2.2 / 2.8 | 4.2 / 4.5 | 3.6 / 3.5 | 3.8 / 4.0 |
| Build a content item through its steps | 6 | Opus 5.5 xhigh 3, Opus 5.5 high 1, Sol 6.1 xhigh 1, Opus 5.5 medium 1 | 3.2 / 4.3 | 2.6 / 4.2 | 2.3 / 4.0 | 2.2 / 3.7 | 1.8 / 3.3 | 2.2 / 3.2 | 3.0 / 3.3 | 2.8 / 3.0 | 2.7 / 2.8 |
| Translate text | 5 | Opus 5.5 max 3, Opus 5.5 xhigh 2 | 4.8 / 5.0 | 4.0 / 4.2 | 3.0 / 3.2 | 3.0 / 3.2 | 2.6 / 2.8 | 2.0 / 2.2 | 4.0 / 3.2 | 4.2 / 3.2 | 3.8 / 3.0 |

Each kind has 3 to 6 tasks, so a row is a direction, not a verdict. Across all kinds, Sol 6.1 at high scored 3.9, medium 3.7 and low 3.5, and misled on 4%, 12% and 10% of tasks. Terra 6.1 and Astra 6.0 weren't in this test, and neither were writing code, builds or device work, because the test was stopped before its code-writing tasks ran.

## Why the scores don't rank one family against the other

Each judge scored its own family's answers about 1.5 points higher than the other judge did, though neither knew which model wrote which answer. Sol 6.1's judge put Sol 6.1 at high 0.6 points above the original Opus 5.5 answers; Opus 5.5's judge put it 0.9 below. Averaging the two does not remove that, so the back-test cannot say whether Sol 6.1 can replace Opus 5.5 or the reverse. Settling it needs a judge from neither family, or tasks whose answers can be checked.

## What real use showed afterwards

An audit of every Codex and Claude session across five machines, October 29 to November 5, 2026.

- 1,565 of the 1,621 helpers at the two top levels had inherited that level or forked. Nobody had chosen it.
- Reviewers on a timer at the top Codex model took 59% of that week's Codex allowance. Of 2,086 check-ins read closely, 576 came after a session that had done nothing but handle the last review.
- One plan took 179 reviews across 22 drafts, each reasonable from inside its round.
- A build check at medium wrote 18k tokens in about 4 minutes, and at max 113k tokens in about 20.
- No Terra 6.1 xhigh build from a full spec was found that Sol 6.1 had to redo. 13 of 105 cheap device workers died on a request error, which says nothing about the model's work.

## Crossing families and small jobs

28 runs, November 5, 2026: four small jobs with known answers through seven routes from both parents. All 28 were right, so this measures speed and cost, not quality. Sonnet 5.5 at medium beat crossing to Sol 6.1 at high on speed on all four jobs (44 against 82 seconds in total) and tied on cost ($0.36 against $0.38 with the parent). The numbers are in `costs.md`. This is why "Mechanical work" and "Fix a well-defined bug" name Sonnet 5.5 at medium: those rows end in a check. It rests on two small code jobs, against a back-test where Sonnet 5.5 at medium misled on about 3 tasks in 10 with no check at the end.

A second round gave Sol 6.1 at high and Terra 6.1 at xhigh one identical brief from both parents, and most of a remaining gap closed: see the end of `costs.md`.

## A timed reviewer moved to a cheaper model

November 5, 2026: 20 saved check-ins from three long-running jobs reran on Sol 6.1 at high, from a frozen copy of what each session had done. The test counted only findings the session really acted on after Astra 6.0 at xhigh raised them: 52 of the 92 it raised. Two readers marked each one without knowing who wrote it, and agreed on 43.

| | Raised | Partly | Missed |
|---|---:|---:|---:|
| Sol 6.1 at high, all 52 | 33% to 40% | 17% to 31% | 37% to 42% |
| 25 that changed real work | 7 to 12 | 6 to 14 | 4 to 7 |
| 9 that corrected what a person had been told | 4 | 1 | 4 |
| 18 that corrected a record or note | 5 to 6 | 1 to 2 | 11 |

That step moved the model and the level together, so the same looks then ran on Sol 6.1 at xhigh, changing only the level. On the 16 that finished, Sol 6.1 at xhigh raised or partly raised 23 to 24 of 41 findings against 24 to 26 for Sol 6.1 at high, so the level didn't explain the gap. It raised 5 or 6 more further findings on real work, unchecked, at 1.2 times the cost.

Astra 6.0 at high then ran on all 20 looks. It raised or partly raised 32 of the 52 findings on both readers' marks, against 30 to 33 for Sol 6.1 at high, at $3.33 a look against $0.53. On the 5 looks where Astra 6.0 at xhigh also ran from a frozen copy, Astra 6.0 at high got 10 to 11 of 14 against 10 to 12, in about half the time and for 8% less. Astra 6.0 at high and Sol 6.1 at high missed 14 of the same findings, and the evidence was missing or only partly in the copy for 12 of those.

These figures are a floor on what either would catch live: it had no live records, no earlier thread and shortened tool output. Of the 19 findings both readers said it missed, the evidence was fully in its copy for 4. Astra 6.0 rerun from the same frozen copies also lost findings, missing 2 to 4 of 14 on five looks where Sol 6.1 missed 4 to 5, so that gap is too small to divide between the model and the setup.

Sol 6.1 lost most on the job where reviews most often change real work, though that job's reviews also lean most on files a transcript doesn't hold. It lost least on the job whose reviews mostly correct records. Readers counted 24 to 33 further findings from Sol 6.1 that would change real work, and nobody checked whether those were true. A cold look cost $0.53 on Sol 6.1 at high against $3.75 on Astra 6.0 at xhigh, about a seventh, and Astra 6.0's live look cost $7.43. Price per token alone says a fifth, but that ignores what the level does to the tokens.

## What each model adds

November 5, 2026: the catches above say nothing about what a model adds that nobody needed, so that was tested too. Terra 6.1 at xhigh and Opus 5.5 at high ran the same 20 looks. Every further finding from all six settings, 445 in all, went to two blind readers, Opus 5.5 at high and Astra 6.0 at high, to sort as a case a user or the business here really meets, a risk nobody meets, or a nit. They agreed on 354. Pairs below read one reader, then the other.

| 20 looks, 52 findings | Terra 6.1 xhigh | Sol 6.1 high | Astra 6.0 high | Opus 5.5 high |
|---|---:|---:|---:|---:|
| Raised or partly, of 52 | 30, 30 | 33, 30 | 32, 32 | 35, 31 |
| Missed, of 25 that changed real work | 10, 10 | 4, 7 | 5, 6 | 6, 9 |
| Further findings a look | 3.7 | 3.6 | 3.5 | 8.2 |
| Of those, really met | 63%, 52% | 45%, 36% | 57%, 44% | 64%, 51% |
| A risk nobody here meets | 6%, 4% | 4%, 2% | 7%, 2% | 6%, 1% |
| Nits | 30%, 43% | 50%, 61% | 35%, 52% | 30%, 46% |
| Cost a look | $0.15 | $0.53 | $3.33 | $1.12 |
| Minutes a look | 2.3 | 6.0 | 4.8 | 3.7 |

Four stored code-writing tasks then ran on one brief each. The same two readers said blind whether each did the job and what they'd cut.

| 4 builds | Terra 6.1 xhigh | Sol 6.1 xhigh | Astra 6.0 high | Opus 5.5 medium |
|---|---:|---:|---:|---:|
| Ended early, by its own report | 3 | 2 | 1 | 0 |
| Does the job: yes, partly, no, first reader | 2, 1, 1 | 2, 1, 1 | 3, 1, 0 | 4, 0, 0 |
| Does the job, second reader | 2, 1, 1 | 2, 1, 1 | 3, 1, 0 | 4, 0, 0 |
| Code lines | 241 | 470 | 380 | 754 |
| Guards, a rough text match | 7 | 9 | 5 | 15 |
| Share cut, first reader | 13% | 32% | 18% | 9% |
| Same, without two offline test files | 13% | 10% | 16% | 9% |
| Share cut, second reader | 1% | 2% | 2% | 1% |
| Cost of all four | $0.77 | $2.44 | $9.66 | $8.59 |
| Median minutes | 3.3 | 6.6 | 4.8 | 6.9 |

- **The field read isn't settled.** Every brief was tight and every run short. Open work and rounds of fixes, where people saw the adding, weren't tested.
- **The share cut rests on one reader, and that reader moves.** The second cut almost nothing from anyone, and the first cut its own maker least. Two settings kept an offline test file, because the copy had no keys for live checks. The first reader cut one file whole and kept most of the other.
- **A reader trims what it's given.** Two builds of one job, 86 and 388 code lines, both read "yes" and lost little. The share cut can't see what a smaller design would have saved.
- **The readers saw diffs, not closing reports.** One build scored "yes" by both readers came from a run that said it hadn't finished.
- **Two of the three causes of early endings came from the test copy:** a broken generator and missing content. The third was a contradiction in a real brief.
- **Further findings are unchecked,** and the sort read a one-sentence summary of each.

Since then, two live timers moved to Sol 6.1 at high. Over ten looks on young threads, one averaged $0.40 a look against $3.85 for the first six looks of the Astra 6.0 at xhigh thread before it, and the other $0.71 at one look an hour, all at list price. Sessions took nine of ten logged findings, two looks found nothing, and no finding asked for a new guard.

## How firm the rows are

`task-types.md` says what stands behind each row. Rows with a task count rest on the level-by-level scores above, compared within a family. Rows marked not measured are starting guesses from field use. Opus 5.5 at high was measured on 15 tasks, plus 4 blind-scored on November 5, where it pulled clearly ahead of Opus 5.5 at medium on none. Terra 6.1 at xhigh and Astra 6.0 at xhigh were run on a few real tasks each, November 5: neither pulled clearly ahead of or behind Sol 6.1 on blind scores, on three tasks a side. The four builds above add a direction for one kind of work, and no more.

## Measuring again

When a new model or level arrives, `$model-eval` runs the back-test again for it and updates this skill from the result. The first run's method, log, tasks, tooling and scores are in psbrain at `projects/agent-watcher/efficiency-profile/task-routing/`.

## Gemini 4 Carbon across helpers, research, builds, reviews and crossing

Measured November 10, 2026, through Antigravity (`agy`) against stored baselines with zero baseline reruns. Two neutral blind judges from the other two families, Opus 5.5 at medium and Sol 6.1 at high, graded every answer without model names. Standard list prices below are Google's December 1, 2026 rates ($4 input, $0.20 cached input, $20 output, $0 cache write); November introductory rates are half of standard.

### Five multi-file helper tasks

Five stored tasks covering planning, translation under length limits, external copy under policy rules, repository survey and multi-file fact checking:

| Setting | Finished | Minutes, all 5 | Cost, standard (Nov intro) | Sol 6.1 judge | Opus 5.5 judge |
|---|---:|---:|---:|---:|---:|
| Gemini 4 Carbon at medium | 5 of 5 | 70.9 | $15.07 ($7.53) | 3.6 | 3.8 |
| Gemini 4 Carbon at high | 2 of 5 | 98.4 | $21.75 ($10.88) | 1.8 | 1.8 |
| Opus 5.5 at xhigh (stored) | 5 of 5 | 52.8 | $26.16 | 3.8 | 3.6 |
| Fable 5.2 at high (stored) | 5 of 5 | 41.7 | $27.79 | 3.2 | 3.8 |
| Fable 5.2 at xhigh (stored) | 5 of 5 | 69.5 | $41.57 | 3.2 | 4.0 |

Carbon at `high` timed out past 21 minutes of file paging (136 to 201 tool steps) on three of the five tasks. Carbon at `medium` finished all five and matched Opus 5.5 at `xhigh` on combined blind score for 42% less at standard rates, taking 34% longer than Opus 5.5 at `xhigh` and 4.0 times as long as Opus 5.5 at `medium` (17.6 minutes, $9.86 on the same five tasks). On two of those tasks where Gemini 4 Argon at `high` also ran as a control, Argon finished in 15.0 minutes ($3.61 standard, $1.81 intro) and scored 2.5 on both judges against 3.0 and 3.5 for Carbon at `medium`.

### Hard analytical rewinds and open systems questions

Three research questions from a quantitative systems project, each rewound to the exact inputs before the team caught a wrong turn, plus two open memory and scaling questions on the same codebase:

| 3 rewound research questions | Finished | Minutes, all 3 | Cost, standard (Nov intro) | Sol 6.1 judge | Opus 5.5 judge |
|---|---:|---:|---:|---:|---:|
| Fable 5.2 at xhigh (stored) | 3 of 3 | ~65 | ~$25 | 3.7 | 4.3 |
| Opus 5.5 at xhigh (stored) | 3 of 3 | ~45 | ~$12 | 3.7 | 3.7 |
| Gemini 4 Carbon at medium | 3 of 3 | 64.4 | $9.26 ($4.63) | 2.7 | 3.0 |
| Gemini 4 Carbon at high | 2 of 3 | 84.4 | $15.66 ($7.83) | 2.0 | 2.7 |

On the first two rewinds, Carbon at both levels reproduced the team's settled arithmetic and traced the underlying code mechanism, losing points for co-headlining an unmeasured carry on the first and attributing an unsplit residual by subtraction on the second; on the third, Carbon at `high` wrote seven analysis scripts and timed out at 29 minutes without delivering its answer. On the two open questions (56.7 minutes in all, $8.63 standard, $4.31 intro), Carbon at `high` finished both and independently found verified code-level levers, an algebraic double-exponentiation bug in an existing projection, and an allocator size-class boundary tax that matched or extended what Opus 5.5 and Fable 5.2 found.

### Four code builds and five reviewer control looks

On the same four stored builds reported in "What each model adds" above, both blind readers scored Gemini 4 Carbon at `high` **1 yes, 1 partly, 2 no** (median 20.0 minutes, $14.12 standard, $7.06 intro): two builds timed out after 20 minutes of reading with zero diff, one timed out after writing 499 code lines and 27 guards (12% and 32% cut by the two readers), and one finished cleanly (22 code lines, 96 test lines, 0 guards).

On the five control looks (14 taken findings) where Astra 6.0 at `xhigh` also ran from frozen copies:

| 5 control looks, 14 findings | Terra 6.1 xhigh | Sol 6.1 high | Opus 5.5 high | Astra 6.0 high | Astra 6.0 xhigh | Carbon 4 high |
|---|---:|---:|---:|---:|---:|---:|
| Raised or partly, reader 1 / reader 2 | 10 / 10 | 10 / 9 | 10 / 10 | 11 / 10 | 10 / 12 | 12 / 12 |
| Missed, of 14 | 4 / 4 | 4 / 5 | 4 / 4 | 3 / 4 | 4 / 2 | 2 / 2 |
| Further findings a look | 2.8 to 3.2 | 3.0 to 3.2 | 8.2 to 8.6 | 2.8 | 2.4 to 2.8 | 10.2 to 13.8 |
| Cost a look, standard | $0.15 | $0.53 | $1.12 | $3.33 | $3.75 | $2.77 ($1.38 Nov) |
| Minutes a look | 2.3 | 6.0 | 3.7 | 4.8 | ~10 | 13.5 |

On four small cross-family jobs (two from a Claude parent, two from a Codex parent calling `agy` with Gemini 4 Carbon at `medium`), all four answers were right, setup and reading stayed small, and `agy` itself took 115 to 226 seconds ($0.31 to $0.56 standard) where Sonnet 5.5, Sol 6.1 and Terra 6.1 took 25 to 56 seconds ($0.03 to $0.10).

## GPT-6.2 Sol and Astra on stored work, real briefs and real plans

Measured November 17, 2026, on GPT-6.2 Sol and GPT-6.2 Astra, with only the new models run: 83 scored runs, about $235 at list price. One run per setting on everything below, so each table is a direction. Prices for 6.2 are as reported at launch.

### The 20 reviewer looks

Same frozen looks, prompt and two readers as November 5. Pairs read one reader, then the other.

| 20 looks, 52 findings | Sol 6.1 high | Sol 6.2 high | Astra 6.0 high | Astra 6.2 high |
|---|---:|---:|---:|---:|
| Raised or partly | 33, 30 | 42, 41 | 32, 32 | 39, 36 |
| Missed | 19, 22 | 10, 11 | 20, 20 | 13, 16 |
| Missed, of 25 that changed real work | 4, 7 | 4, 5 | 5, 6 | 6, 8 |
| Further findings a look | 3.6 | 6.0 | 3.5 | 5.6 |
| Of those, really met a look | 1.6, 1.6 | 3.2, 2.9 | 1.6, 1.6 | 2.8, 2.6 |
| A risk nobody here meets, a look | 0.1, 0.1 | 0.6, 0.3 | 0.3, 0.2 | 0.7, 0.5 |
| Cost a look | $0.53 | $0.58 | $3.33 | $1.56 |
| Minutes a look | 6.0 | 5.5 | 4.8 | 5.4 |

- **The readers did not drift.** The 6.2 answers were marked on November 17 and the older ones on November 5. The same two readers re-marked the stored Sol 6.1 and Astra 6.0 answers on November 17 and gave the same mark on 45 to 49 of the 52 findings; no count moved by more than 3.
- Sol 6.2 at high's gain is mostly misses turned into partial catches. Its clean catches rose by 3 and 2.
- Astra 6.2 at high's saving is two fifths fewer tokens and three fifths the lower price.
- On the 5 control looks, Astra 6.2 at xhigh raised or partly raised 10 and 10 of 14 against 12 and 12 for Astra 6.2 at high, at $2.26 a look and twice the minutes.
- The further findings of every setting, old and new, were sorted again in one pass. That pass agreed with November 5's sort on 86% of the old findings, so a share can move several points between passes.

### The four stored builds

| 4 builds | Sol 6.2 high | Sol 6.2 xhigh | Astra 6.2 high |
|---|---:|---:|---:|
| Finished, by its own report | 4 | 4 | 4 |
| Went around a written rule to finish | 2 | 2 | 2 |
| Closing report says so | 0 of 2 | 0 of 2 | 1 of 2 |
| Does the job, both readers | 4 yes | 3 yes, 1 partly on one reader | 4 yes |
| Cost of all four | $2.70 | $2.88 | $6.89 |

Code written came to 313 to 389 lines and 6 to 11 guards a setting, against 754 and 15 for Opus 5.5 at medium. On the build whose compiler fails, where the repository says to name the problem and stop, the three 6.1 and 6.0 settings had stopped and Opus 5.5 had gone around it and said so. All three 6.2 runs went around it: one installed a newer compiler than the repository pins, two generated the output in a scratch copy with the failing part left out. None of their reports mentions it. On the build whose brief asks for a change and forbids the folder it lives in, both Sol 6.2 runs made the change without mentioning the conflict, and Astra 6.2 made it in its own copy of the repository and said so.

### Three real engineer briefs

Briefs written by an engineer for a Codex helper, rerun from the commit each started from, with the inputs each brief reads pinned to the day it was sent. A blind reader on Opus 5.5 at high played the engineer: it wrote the fix list without seeing the builder's report, the builder got one fix round, and the same reader judged the result. One job was a small app change, one a large app change, one crossed app and server.

| Across the three | Terra 6.1 xhigh | Sol 6.2 high | Sol 6.2 xhigh |
|---|---:|---:|---:|
| Ready after one fix round | 0 | 1 | 2 |
| Fix items on the first pass | 18 | 12 | 13 |
| Wrong / missing / not asked for | 11 / 5 / 2 | 4 / 1 / 7 | 5 / 0 / 8 |
| New faults the fix round added | 5 | 2 | 0 |
| Of the items the real engineer had raised, repeated | 10 of 11 | 14 of 21 | 15 of 23 |
| Builder's cost, build and fix round | $4.78 | $16.36 | $16.40 |
| Builder's minutes | 44 | 81 | 78 |

- The reader called Sol 6.2 at xhigh ready on all three. On one, an existing test fails after its fix round and its report said done, so it counts as 2.
- Terra 6.1 stopped on the large job at a real gap in the brief and built nothing there, which is what the repository's rules ask.
- When the live copy of a design spec no longer matched the brief, all three settings stopped within 30 seconds and said so.
- Terra 6.1 wrote the least code. Both Sol 6.2 settings landed near the merged change on the small job and about half again above it on the job that crossed app and server.
- A cold read of a diff by the reader cost about $2, more than a Sol 6.2 build. That is the reader's cost in this test, and a second round for Terra 6.1 costs about one such read plus a dollar of build.

### Two real plans

Two plans a technical lead wrote for features that have since shipped, rewound to the ask, the design and the code as they stood. Each new plan was scored on the 21 things the real plans later got wrong or left open: 1 for already right, half for partly. Readers were Opus 5.5 at high and Astra 6.2 at high, blind; no third maker read them. Every planner's transcript was checked for reading anything dated after the real plan, and none did.

| Planner | Astra 6.2 reader | Opus 5.5 reader | Cost a plan | Minutes a plan |
|---|---:|---:|---|---|
| Astra 6.2 xhigh | 10.0 | 11.5 | $3.76, $4.09 | 18, 21 |
| Astra 6.2 max | 9.0 | 12.0 | $5.88, $6.63 | 36, 32 |
| Sol 6.2 high | 8.5 | 11.5 | $0.72, $0.95 | 6, 10 |
| Opus 5.5 high | 8.0 | 11.0 | $4.38, $6.56 | 10, 16 |

Both readers put Opus 5.5 last or tied for last. Only Astra 6.2 at xhigh foresaw the fault that later shipped on the plan that crossed a server, an app and a deploy. Only Opus 5.5 planned the measurement on the other. Every plan asked for 5 to 12 things the shipped feature never needed. The list scores only the real plans' own mistakes.

### Account room

Read from the weekly bars of the accounts that carried the runs, before and after. A point of a Codex account's week came to roughly $15 to $30 of list price, and a point of a Claude account's week to roughly $3 to $4.50. The bars are whole percents and the accounts were shared, so both are rough.
