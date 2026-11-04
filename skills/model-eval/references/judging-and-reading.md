# Judging the reruns and reading the scores

## How a task is judged

A judge sees one task at a time: the brief as the reruns got it, the original result as context, and every answer to that task, the new model's beside the stored ones (the reference among them), labelled with letters in random order. It is not told which model or level made which. It grades each rerun 1 to 5 against what the brief asked and what the person asking needed. The first run's brief to its judges is `SCORE_PROMPT` in `judge.py`; its core:

> Grade each run on its own merits against what the brief asked for and what the person who asked needed from it: is it correct, did it find or produce what matters, did it follow the brief's rules (for example read-only, or the output format it asked for), and would someone relying on it be well served. Two good runs can differ: a review can find different real problems, a translation can choose different good words. Do not mark a run down for differing from another run; mark it down for being wrong, missing something important the brief asked for, breaking the brief's rules, or not finishing. Where you can check a claim against the files or facts the runs cite, the run that got it right should score higher.
>
> 5 = excellent: correct and complete on everything that matters. 4 = good: correct on what matters, small gaps or imprecision. 3 = usable with care: one real error or omission a careful reader would need to catch. 2 = poor: several real errors or a major omission; relying on it would mislead. 1 = failed: did not do the task, or wrong on its central point.

Each judge answers with a score and one sentence of reason per run. Keep those reasons: they are how you read a case without rereading every answer.

What a judge sees of a rerun is its final answer, the files it wrote (or its diff), and whether it ended in an error. A rerun that ended in an error but still gave a full answer is graded on the answer.

The first run's judges were GPT-6.1 Sol at high on the Codex pool and Claude Opus 5.5 at medium on a pooled Claude account. Both judged every task, all of a task's reruns in one pass, after every setting for that task had finished. They were not set up alike. Sol's judge ran as a Codex agent with its shell, so it could open the files the answers cited. Opus's ran with no tools, so it could only read what it was given. The brief asks judges to check claims against the files, and only one of them could. Give every judge the same material, the same tools and a comparable thinking level. Otherwise a gap between judges may come from their setup rather than their family.

## What to compute

For each setting, overall and kind by kind, against the reference on the same task:

- **Score change**: the setting's score minus the reference's, averaged over tasks.
- **Misled**: how many tasks the setting scored two or more points below the reference. That is an answer a parent would have been misled by. Give its share an interval, because small counts swing.
- **Time**: the median, over tasks, of the setting's wall-clock time divided by the reference's.
- **The noise floor**: the same numbers for the reference's own repeat. On October 27 the repeat changed by 0.0 and misled on 0 of 37 tasks.
- **By judge**: every comparison above, once per judge. Where the two judges disagree on the direction of a change, the change is not settled, however the average falls.

Leave out a task whose reference rerun itself failed (the two judges' average at 1.5 or below), since there is no drop to measure. Also leave out a setting's rerun of a task its harness cannot run as written, and say so beside the table.

`analyze_scores.py` makes most of these tables, but it averages the two judges in every row and prints only one overall line per judge. Its averaged table had Sol at high 0.1 below the reference, with 4% misled. Those numbers carried the interim picks of Sol, which were withdrawn once the split by judge was made by hand. Add the split by judge to every table before you read it. The script also prints a "pick" per kind from a fixed cut, which is not how the router was decided: read the tables and the cases, and decide.

## Testing a judge you haven't used for this

A new judge, especially one brought in from a third family to settle a comparison across families, has to show it can tell answers apart before you lean on it. Score with it a handful of tasks where you already know how the answers should come out. Repeat runs of the reference should come out level. On a task whose answer can be checked (a test that passes, a number already verified, a solver's answer), the right answer should score above the wrong one. Run the same tasks past the existing judges too, and see where they part. A judge that ranks those cases wrongly isn't settling anything.

## Reading the result

Kinds have four to six tasks each, so a kind's row shows a direction, not a verdict. Agreement between the judges, a large time saving, and few misleading answers on a kind together make a strong case. A single row, however good, makes a weak one.

Before the router moves any kind of work, read that kind's misleading cases: the answers, both judges' reasons, and the brief. `backtest/cases.md` in the last run shows the form. The cases show what the lower setting skipped. If what it skipped is something the parent would catch on reading, the step down may still hold. If it is the one thing the task existed to find, it doesn't.

The last run's numbers are in `model-routing`'s `references/evidence.md`, which you will rewrite. For a new version of a model, the closest comparison is that file's row for the setting it would replace.
