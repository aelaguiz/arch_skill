---
name: model-eval
description: "Evaluate a new model or thinking level for our agents' helper work and update `model-routing` from the result: run only the new model on the last back-test's real helper tasks, have blind judges score its answers against each brief beside the stored answers of today's routing picks, and change the router's examples, commands and evidence where the result holds up. Use when a new model or version comes out (a new Opus, Sol, Sonnet, Gemini) and the user asks to evaluate it, back-test it, rerun the model eval, or get the model router updated with the latest models. Not for choosing one helper's model right now (model-routing), or which model an application's code should call."
metadata:
  short-description: "Back-test a new model and update model-routing"
---

# Model Eval

`model-routing` tells every agent which model and thinking level to give a helper. Its examples come from a back-test of real helper tasks, and they go stale when a new model arrives. This skill runs that back-test again for the new model and updates the router from what holds up.

You are done when the router says what the new evidence supports, its evidence file carries the new numbers with their date, and the user has seen what changed, why, and what the run cost. Nothing is published before that. A run that finds nothing worth changing is also a finished run: record its numbers and say so.

Speed here means what it means in the router: wall-clock time until the parent has an answer it can act on. A faster setting that misleads costs more than the minutes it saved, because the parent acts on the wrong answer or redoes the work.

## Start from the question the new model asks

The first back-test, on October 27, 2026, asked the widest question there is: which model and level for every kind of helper work. It reran 102 tasks on nine settings, 874 reruns over about ten hours, filled one account's five-hour window after another, and the user stopped it as more intense than expected. A new model almost never asks that again, and every answer that run measured is still on disk. Work out what the new model's arrival asks, and run only the new model on what answers that.

- **A new version of a model the router already uses**, such as a new Opus or Sol, asks whether it can take that model's place, and where its step-down now sits. Thinking levels don't carry across versions: the new model's medium may do what the old one did at high, or at low. Run it at two or three levels on the tasks of the kinds where it would be used.
- **A smaller or faster model** asks whether any kind of helper work can move to it. On October 27 Sonnet and Haiku fell a point or more behind and dropped rules of the brief; a newer one may not. Here the kinds matter more than the average, because one kind where it holds is worth finding.
- **A model from a family the router doesn't use** raises the judging problem below before anything else, so plan the judges first.
- **What crossing families costs** asks what a parent pays to reach a helper in the other family, on top of that model's price. A helper timed alone can't show this, so the parent has to be a real session that starts the helper, waits, reads the answer and acts on it. Split each run's time and tokens into briefing, launch and setup, the helper's work and reading the answer, and count launch failures, so the crossing can be told apart from the model.

Then size it. Four or five tasks of a kind show a direction, not a verdict. Where a call would move a lot of agent time, or the result is close, add tasks to that kind instead of adding them everywhere.

Write a cap before anything starts, in runs and in hours, covering parents, helpers, judges and retries. At the cap the run ends everything it started, not only its driver, and reports what it has. A wide question grows quietly: the first back-test was sized at three to four hours, and the user stopped it after ten. The router needs a direction it can act on, and a lean from a small round costs far less than a day of reruns. If a round leaves the question open, the next round is a new decision, sized from what this one showed.

Price it before you promise it. Rerun one task on the new model first: that proves the model id and the containment work, and shows what a rerun takes on it in minutes and in account window. The first run's reruns were estimated at three to four hours, and nine hours in they still weren't done: the code tasks that copy a repository made a long tail, disk pressure cut how many could run at once, and accounts hit their limits one after another. Estimate from that slow tail, not from the median rerun. Before the reruns start, write the run's plan in its folder and tell the user what it will take: how many reruns, which accounts, about how many hours, and how much of those accounts' week. Then start. When the run is going to pass its estimate, tell them then, before they have to ask.

## Start from the last run

Every run lives in its own dated folder beside the last one, in psbrain's `projects/agent-watcher/efficiency-profile/task-routing/`. The last run left a catalog of the kinds of helper work, a set of tasks already screened as safe to rerun, the tooling that ran reruns, judges and tables, every setting's answer to every task, and every score. Reuse all of it, the answers included. A new model needs only its own reruns: run it on those tasks, then have the judges score its answers in one pass beside the stored answers of the reference and the router's current pick. Rerunning the old settings would buy again answers you already have, and that is most of what made the first run so heavy. The tooling already carries fixes that took hours to find; fix what has broken since rather than rebuilding it. [references/rerun-setup.md](references/rerun-setup.md) says what each piece is, which stored answers to carry over, and how the reruns are contained.

A stored answer stands as long as what its task read still stands. Code tasks rerun at a fixed commit, and most tasks read files that haven't changed. A task that read something that has moved since, such as live data, a file edited since or the web, would hand the new model a different task. Rerun the reference beside the new model on that task, or leave it out. When so many have dropped that a kind is thin, or the work agents do has clearly moved on, pull fresh tasks from recent agent history the way the last run did. Only fresh tasks need every row run new.

## What makes the comparison fair

Compare every setting with a reference: the work as it comes out when nobody saves time on it, which is the strong model at its top level. On the last run's tasks the reference is already stored. On a fresh task, run it at the strong model's top level, not at whatever the task first ran on: once the router is in use, many tasks first ran on its stepped-down setting, and measuring against that lowers the bar a little with every run. The original result goes to the judges as context only.

Time is the weak spot of a stored answer, because it ran under that day's load. When a call turns on a close time saving, rerun the reference on a few of those tasks under today's load and see whether the ratio holds.

Give the new model's reruns the same setup the stored answers had. The last run mirrored each task's project instruction files and project skills into the rerun's folder, because a rerun in a bare scratch folder misses them, and that hurts a faster model more than a slower one, so it reads as a difference between models. A few early tasks ran without that context; run the new model on them the same way, or leave them out.

The stored answers include a second run of the reference on about half the tasks. Two identical runs already differ, a lot on open work like reviews, and the repeat shows how much, so a difference smaller than that isn't read as the model's. A fresh task needs that repeat too.

A brief written for one harness may not run on another. A brief that forbids shell commands, or relies on Claude's Skill tool, Agent tool or an MCP server, leaves Codex, whose only tool is the shell, with nothing it can do. Leave such a task out of that harness's rows rather than scoring the failure as the model's.

## Judging

Judges grade each answer blind, on whether it gave the person who asked what they needed: correct, found what matters, kept the brief's rules, finished. They don't grade by resemblance to another answer. Two good reviews of the same code find different real problems; judging by resemblance marked that honest variation as worse, and the first run had to change method an hour in.

A judge favours its own model family even when it doesn't know which model wrote what. On October 27 each judge scored its own family about 1.5 points higher than the other judge did: Sol's judge found Sol better than Opus, Opus's judge found it worse, and averaging them settled nothing. (The two judges weren't set up alike, either: Sol's could open the files the answers cited and Opus's had no tools, so some of that gap may be access. Give every judge the same material, the same tools and a comparable level, or you can't tell bias from setup.) The step-downs that went into the router held because each compared a model with itself, and both judges agreed on them. Agreement between judges from different families is what you can rest a change on.

So choose judges for the comparison you're making. When a model is compared with itself or a sibling in its own family, two judges from different families see the same pair, and what they agree on can be trusted. Across families, use a judge from neither family, or tasks whose answers can be checked: tests that pass, numbers already known, a solver's answer. Before leaning on a judge new to this work, see how it scores cases where you know the answer: repeat runs of one setting should come out level, and on a checkable task the right answer should score higher.

Read the misleading answers yourself before moving any kind of work: those two or more points below the reference on the same task. They are what a parent would have acted on, and they show what the lower setting skipped: a check the brief required, an obstacle it stopped at, the one wrong answer it missed. [references/judging-and-reading.md](references/judging-and-reading.md) has the scoring brief and how to read the tables.

## Reruns are real agents

Each rerun is a full agent with tools, working on real files. On October 27 they made 24 GB of repository copies in an hour, searched the whole disk for one file, kept running after their driver was stopped (48 processes, because none had its folder on its command line), and filled one account's five-hour window after another. Nothing reached the outside world, because each rerun could read anywhere but write only inside its own folder, had no MCP servers, and could not send, post, push or deploy. Keep it that way, and leave out a task whose rerun would need a real action rather than adapting it.

While the run goes, watch the disk, the machine's load and the accounts, and track reruns by their working directory, not their name. Run Claude reruns through AI Manager on pooled accounts with room, never on this session's own account, and rest an account before its window fills so the sessions that live on it keep room. When one hits a limit, move its work to another account rather than waiting. The settings, commands and watching are in [references/rerun-setup.md](references/rerun-setup.md).

## Updating the router

`model-routing` teaches how to choose, and its table says which setting does which kind of work. Keep that shape, and build anything new in it with `$intuition-building` and `$skill-authoring`. Change what the evidence supports: the settings in the table, the commands under "Setting it", and the reasoning when a new model changes it. For example, if a smaller model now holds on some kinds, "When a smaller model holds up" has to change too. Prices and run costs go in `references/costs.md`, dated, so a price change never touches the teaching. Rewrite `references/evidence.md` with the new numbers, dated and naming the models measured; the old numbers become history. Search arch_skill for the old pick's model id, because other skills that pin a helper follow the router and change with it.

Then check that the updated router teaches what you meant. Give a few fresh agents only a task each: one the change should move, one it should leave alone, and one nearby ask that isn't about helpers at all. See whether each loads the router, what it picks, and whether its reason is the router's idea in its own words or a copied row.

arch_skill is public, so the router's examples stay generic and its numbers aggregate; case detail stays in the run's folder.

Then tell the user, in plain words (`$readable-reports` for the write-up): what changed in routing and why, the numbers behind each change against the reference, the cases that misled, what is still open, and what the run cost. The change alters how every agent picks its helpers, so it is published when the user says so.

## References

- [references/rerun-setup.md](references/rerun-setup.md): where the last run's tasks, tooling and data live, the sandbox and the Claude and Codex command lines, project context, code tasks, accounts, and watching a run. Read when setting up or restarting reruns.
- [references/judging-and-reading.md](references/judging-and-reading.md): the blind scoring brief, what to compute, how to test a judge, and how to read small samples. Read when judging and when deciding what the scores support.
