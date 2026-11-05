---
name: model-routing
description: "Required whenever you start a helper, from a Claude or a Codex parent: a subagent, a `claude -p` or `codex exec` run, a worker a skill or script launches, or a reviewer on a timer. Teaches how to choose its model and thinking level, which is part of the job and never left to inheritance: why the helper exists (a cheap, fast answer or another maker's eye), what a setting really costs once level, Fast and repeat runs are counted, which kinds of work each setting does well, which reviews need deep thinking, stepping up after a miss, native against external helpers, and whose pick wins. Use before you set a helper's model or effort, when you write a skill, script, grid or brief that starts helpers, or when asked which model or thinking level fits a kind of work. Not for whether or how to delegate (agent-delegate and the shared orchestration policy), the model of a session someone else started, or which model an application's code should call."
metadata:
  short-description: "Choose every helper's model and thinking level"
---

# Model Routing

Every helper you start runs on a model and a thinking level you chose. That choice is part of your job, like choosing what to ask it. There is no default to fall back on. A helper given no level takes yours, which was set for your work and not for its work: in one audit, about 19 in 20 helpers at the two top levels got there by inheriting or forking, and nobody had decided they should.

You are after the answer you can act on, as soon as possible, without spending what the work doesn't need. Speed is wall-clock time until you have that answer. A fast wrong answer is slower than a slow right one, because you act on it or redo it. Cost is how long the accounts last for every other agent drawing on them. When the two pull apart and the accounts have room, speed wins. Most of the time they don't pull apart: the setting that wastes money is usually wasting minutes too.

Your own model and level were set by whoever started you, and you can't change them. Nothing here is about them. What is yours is which work you hand off and how each helper runs.

Always refer to a model as "it" or "its", never as "he" or "she".

## Why this helper exists

Most helpers exist to get something done cheaply and fast: find something out, make a change, run a check. Any setting that gets you a usable answer soonest is right, whichever maker built it.

Some exist to put another maker's biases in the mix: a second opinion on a plan, a review before a change lands. Models from one maker share blind spots and favor their own work, so here the other family is the point, and a cheaper setting in your own family doesn't do the job at any price.

One helper can want both. A reviewer that checks in on long-running work wants the other maker's eye, and it runs dozens of times, so it has to earn each run.

## What things cost

Per-token prices alone mislead, because three things multiply them. [references/costs.md](references/costs.md) has today's prices and what a typical run costs at each setting.

- **The level multiplies tokens.** The same model on the same job cost about three times as much at its top level as at medium, and one build check wrote six times the tokens.
- **Fast multiplies the price.** It costs 2 to 2.5 times standard. Sol at xhigh on Fast comes to about what Opus at medium costs for the same job.
- **Runs multiply everything.** Cost is price times how many times it runs. A deep review run once is cheap for what it can catch. The same review on a timer, or after every small revision, was the largest use of an allowance we have measured, well past half of a week's Codex.

So the money is in what repeats. Before you start anything that does (a reviewer on a timer, a loop, a fan-out, rounds of review), multiply it out. A cheap setting on a timer can cost more than a dear one that runs once. A one-off isn't worth agonizing over: pick what fits and go.

## What a thinking level buys

A higher thinking level does not make a model write faster. It makes it do more before it answers: check everything the brief asks for, find a way around an obstacle, keep many rules in mind at once. That costs minutes, and whether the minutes buy anything depends on where the answer's value comes from.

When the material you hand the helper carries the answer (the sources, the data, the codebook, the code, the standard to judge against) and you will read and check what comes back, the extra work adds time and not quality, and the same model at a lower level reaches as good an answer in well under the time. Coding a batch of short videos by a codebook, medium took 3 minutes against 18 and scored higher. Asked who set up an account and what state it was in, the top level came back confidently wrong after 25 minutes; medium found the meeting notes that answered it.

When the value is in what the helper notices that nobody pointed it at, the thinking is the job. Rewriting a batch of quiz questions, the top level fixed the one question whose correct answer was marked wrong; medium answered "nothing to fix" in under a minute. A short task can be like this too: translating twelve strings under a glossary, a width limit and a check script, medium translated as well but skipped measuring the width and running the check. A fast answer that looks finished and isn't costs more than the minutes it saved.

## When a smaller model holds up

Moving to a smaller model is a different bet from lowering the level. A strong model at a lower level keeps its grip on the brief and does less extra work. A smaller model can lose the grip: in a back-test, Sonnet and Haiku, and Opus at its lowest level, dropped rules of the brief and missed the point about a third of the time or more, against 7% for Opus at medium. A read-only review on Sonnet found the real defects and then wrote files anyway. Sonnet has no room to step down either: at medium it does markedly worse than at max.

That is a finding about work where the brief in the helper's head is all that keeps it honest. Where the spec is complete and a test or a build shows whether the work is right, a smaller model does well: we found no Terra xhigh build from a full spec that Sol had to redo. So ask what keeps this helper honest, and how much of the work a check really proves. A hidden test proves the code does what the test checks. A green build says nothing about whether a PR's description is true, or whether every rule in the brief was kept. If the check covers what could go wrong, the smaller model is likely as good and cheaper. If only the brief does, keep the strong model at a lower level.

## Which setting does which kind of work

Each row is where to start: the cheapest setting we have seen do that kind of work well, for each family. [references/evidence.md](references/evidence.md) says how firm each is, and some rest on very little. Names are families, so use the newest version of each. A task that is plainly one of these under another name starts in the same place, and one that is harder than its row starts higher. "Native or external" below says which column to take.

| Kind of work | For example | Claude | Codex | Why that is enough |
|---|---|---|---|---|
| Mechanical work | Rebase, run the tests and report what failed | Sonnet medium | Terra xhigh | The steps are known and the result shows whether they worked |
| Bring text in line with the facts | PR text, docs after a change | Opus medium | Terra xhigh | The facts are in hand, but no test reads the meaning, so you do |
| Look something up | Research a question, analyze a dataset, explain how code behaves | Opus medium | Sol high | The sources hold the answer, and you read what comes back with them |
| Work out a problem with one right answer | "Which of these three options is correct, and why?" | Opus medium | Sol high | The answer can be checked; more thinking re-derives what medium finds |
| Check work against a stated standard | Did the build stay inside its spec, label by a codebook, judge copy or images by a style guide | Opus medium | Sol high | The standard is handed over; the helper compares rather than invents |
| Check in on running work | "Is this session still doing what it was asked?" | Opus medium | Sol high | The same kind of check, run many times |
| Fix a well-defined bug | Cause known, one or two files, one part of a full spec | Sonnet medium | Terra xhigh | The thinking is done, and the tests prove the fix |
| Walk a test plan on a device | Capture each screen and compare it with what was decided | Opus high | Terra xhigh | A long brief, held for many steps |
| Find a bug's cause | Reproduce it and name the cause, a red CI job nobody has read | Opus medium | Sol xhigh | The cause is unknown, so the search has to stay honest |
| Build across several parts from a spec | App and backend, several screens | Opus medium | Sol xhigh | The spec makes the calls; the helper has to keep all of them in view |
| New feature with algorithmic changes | A new game rule, a ratings change, a spec with open design calls | Opus high | Sol xhigh | The design is still being made, so a cheap first try costs more |
| Write words people read | Scripts, ad copy, the product's own lines | Opus high | Sol xhigh | The value is in what it notices |
| Plan or design | An implementation plan and its test plan | Opus high | Sol xhigh | The value is in what it notices |
| Second opinion, once | A plan or PR, looking for what you missed | Opus high | Astra xhigh | One deep pass, from a maker other than the one that made the work |

A task that fits no row still gets chosen, never left to a default. Ask what carries the answer, what will catch a mistake, and which row it is closest to.

The table gives the cheapest setting that does each kind well, and the goal is still the soonest usable answer. Where a dearer setting finishes sooner, someone is waiting and the accounts have room, take it.

## Which reviews need deep thinking

"Review" covers two jobs that look alike and route differently, and reviews are where most of an allowance goes.

A check compares work with a standard someone handed over: did this session stay on its brief, does the build do what the spec says, do the numbers tie. The standard carries the judgment, so a lower level does it as well.

A second opinion looks for what nobody pointed it at: what is wrong with this plan, what did we miss, what will this change break. There the thinking is the job. It earns the deep setting because it runs once, when what it finds can still change the work. Its first pass finds what matters, each pass after that returns a smaller list, and a strict reader always finds one more.

What it is asked to find decides which one you have. How often it runs decides what it costs. A reviewer on a timer that only compares a session with its brief is a check. One asked what the session has stopped seeing (a goal nobody set, an assumption nobody settled, whether the work deserves its time) is doing the deep job over and over, which is why it can be the largest use of an allowance. So run it less before you run it cheaper: a review with nothing new to read has nothing to say, and its pace can fit how fast the work can go wrong.

Running it cheaper is a real trade, so look at what its catches are. When a timed reviewer on Astra at xhigh was rerun on Sol at high from a frozen copy, it raised at least in part about three quarters of the findings that had changed real work, at about a seventh of the cost, and about half of what it lost outright was corrections to records and notes. It still lost a few findings that had changed real work, and it fell furthest on the job where reviews change real work most often. That step moved the model and the level together, so it can't say which one cost the catches. So far it suggests the step suits a review that mostly keeps records honest, and costs more where the review is what's steering the work. `references/evidence.md` has the numbers.

## Step up on a miss, once

Work that plainly needs deep thinking starts deep, because climbing through three settings takes longer than starting in the right place. Everything else starts at its row. When a helper misses, go up one step and try once: on Claude one level, on Codex from Terra to Sol to Astra. Running the same setting again mostly buys the same answer. If the step up misses the same way, stop spending and look at the brief, because two settings failing alike usually means the task was unclear or too big.

A miss is about the work: wrong, unfinished, or a rule of the brief dropped. A helper that died on a launch error, an account limit or a broken tool didn't miss. Fix that and run the same setting again. No amount of model would have saved the one worker in eight that died on a request error in one batch of cheap device runs.

## Native or external

A native helper comes from your host's own subagent tool: Opus, Sonnet or Haiku from a Claude parent, Sol, Terra or Astra from a Codex parent. An external helper is another command line's run, `codex exec` from Claude or `claude -p` from Codex. Either parent can cross, and nothing here assumes which parent you are.

Crossing itself costs little, so let it decide little. In a small test, crossing from a Claude parent added about 2 seconds and a cent, and from a Codex parent 13 to 33 seconds and about 3 cents, mostly extra turns to write the brief down and wait. No launch failed. Those are floors, because the parents were handed the command: finding an account or recovering from a refused launch would add to them. [references/costs.md](references/costs.md) has the stages.

What decided speed and cost was the helper. On small jobs with checkable answers, every route got every answer right, and the helper's own work differed far more than the crossing did. Sonnet at medium was quickest, Terra at xhigh cost about a third as much, and Opus at medium cost the most and wasn't faster than either. So from a Claude parent, when someone is waiting on a small checked job, native Sonnet gets there first, and when nobody is waiting, Terra is worth the two seconds. Those jobs took a minute or two and nobody judged anything but the answer, so they say nothing about holding a long brief, where "When a smaller model holds up" still applies.

A second opinion goes to a maker other than the one that made the work, which may not be your own family: a Codex parent checking a plan Opus wrote wants Codex.

The brief moves a helper's speed more than crossing does. Sol at high and Terra at xhigh first looked about twice as slow when a Claude parent briefed them, but given the same brief they slowed about as much under their own parent. So keep any brief to what the job needs, on either side.

## When speed is worth paying for

Fast and more helpers at once spend more to get the same work sooner. That pays when someone is waiting: a person in the conversation, work that can't start until this finishes. It buys nothing for work nobody is waiting on. A reviewer on a timer that finishes in two minutes instead of four changes nothing about the run it watches, and neither does a faster overnight batch.

A higher thinking level is not a speed setting. It is slower, so when someone is waiting, drop whatever level isn't buying quality before you pay for Fast.

## Whose pick wins

A model or level the user names for a run wins. A pin in a skill, grid, script or brief stands when its reason is written beside it and the reason still holds: "Astra xhigh, because this review is for what Claude can't see." A setting with no reason beside it is a copy of what someone once used, so choose afresh. A pin to an old version of a family means that family: use the newest.

When you write something that starts helpers, it inherits this job: point it at this skill, or give the setting with its reason. A bare model name in a launch line becomes everyone's default within weeks.

## What you hand off

Whether to delegate belongs to `agent-delegate`, but your choice of setting starts there. You run at the level someone set for your whole job, and every step you take yourself pays that rate. Long mechanical stretches (hundreds of shell commands, log reading, retries) are the costly part: one long-running session spent nearly all of its responses on single shell commands. Hand those to a cheap helper. The other edge is a lookup with a known target, which takes less to do than to brief, so do it yourself.

## When one family has no room

Codex and Claude run on separate pools of accounts. When one pool has no room, the other family's model at the matching level takes the work the same day, so nothing stalls waiting for a reset. Astra at xhigh is about Opus at high. Sol at xhigh is about Opus at medium or low; where the job turns on following a long brief, take medium. Terra at xhigh sits lower on coding, about where Sonnet at medium to high or Opus at low would be, but its work still stands in on Opus at medium, because Terra's jobs are builds and checks that hold a brief. The match runs the other way when the Claude accounts are short.

Look again before switching, because accounts come back. Keep the family you would have used while it has room: the match settles which level to ask for, not that the two families think alike. Say which model stood in wherever the work records its models.

## Setting it

Pass both a model and a level, every time. Otherwise use each family's newest version: Claude's `opus` and `sonnet` aliases resolve to it, and Codex's catalog lists it in `~/.codex/models_cache.json`.

- Claude Code's Agent tool: `model: "opus"` and `effort: "medium"`.
- A one-shot Claude run: `claude -p --model opus --effort medium`.
- A Codex native helper: `spawn_agent` with `model` and `reasoning_effort`.
- A Codex run: `codex exec -m gpt-6.1-sol -c model_reasoning_effort="high"`. Add `-c service_tier="fast"` for Fast, and only when "When speed is worth paying for" says so.
- Other hosts, and where a pin stops holding: `../_shared/native-child-capabilities.md`. Check the live tool schema when it and this list disagree.

A fork takes its parent's model and level and can't be lowered, so forking means paying your own rate for the helper. Fork when it truly needs your whole context, and otherwise start it fresh with the setting you chose.

The measurements behind this skill are in [references/evidence.md](references/evidence.md). When a model arrives or a price moves, `$model-eval` tests it and updates this skill.
