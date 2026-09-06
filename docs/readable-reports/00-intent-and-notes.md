# Readable Reports Skill: Intent And Raw Notes

Date: 2026-09-06. Source: Amir, spoken. This file is the doc pack's anchor: what
the skill is for, in his words, cleaned up but not reinterpreted.

## The problem, in his words

"I need you to deeply research how to write understandable text in reports.
... I'm the CEO of the company. I'm also an engineer. I built almost
everything we're looking at but the cognitive burden of trying to parse it is
so fucking high and I can't even put my finger on it. It's not just 'make
things shorter,' right? ... There are skills in PS Agent space for how I do
writing, which I find very understandable."

"I'm looking at this and it says, 'checkout route now, clean, children
blocked.' I don't know what the fuck that means. I could parse it if I had to.
I could be like, 'Okay we're talking about something about the checkout.' I
don't know what we're talking about, but I know there are checkout issues.
What's the root? Does it mean the root PR, like children issues, right? It's
just fucking confusing, dude, and it's sort of the standard of the writing I
get back from these agents."

"I need it to not create so much cognitive burden to try to parse these
things. I need it to be simple and easy to understand, and when I try to do
this half the time I get something that goes into this: 'Oh he's an idiot.'
I'll say, 'Computers are like brains.' It either treats me like a child or it
writes it in a way that requires full concentration to even figure out what
the fuck they're saying, right?"

## The bar, in his words

"A really smart engineering-focused executive could read this at a glance and
understand it without having to drop everything and fully focus on every
single fucking word."

And, clarifying the loop: "you're to judge the output from the astra agent
using your skill until you think its highly understandable, context is clear,
fits my preferred communication styles, etc."

## The trigger example

The report: https://share.fun.country/20260906-763f8a326c72/index.html
(saved copy: `samples/20260906-morning-priorities.html` and `.txt` beside this
file). Source markdown:
`/Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06.md`.

The line: "Checkout root now clean, children blocked." What it means: the base
pull request of the stacked checkout repair PRs (psmobile #5001) passed review
and CI; the four PRs stacked on top of it (#5056 to #5059) cannot merge until
it does. Six words, two undefined nouns ("root", "children"), no subject, no
verb, no consequence. A reader who wrote the code still had to guess.

## Added rule (Amir, 2026-09-06, same session)

"And any time we mention a PR or an issue or anything, it should just be a
link."

Every PR, issue, commit, document, dashboard, or message the report mentions
is a clickable link, labeled with its plain-English name (the repo and number
or title for PRs and issues). Never a bare number the reader has to go find.
This matches the standing rule in `/Users/aelaguiz/workspace/psagentspace/AGENTS.md`
("PR And Issue Mentions Are Hyperlinks", 2026-08-21) and widens it to
"anything".

## Corrections during the build (Amir, 2026-09-06)

On the round-2 skill draft, which added a "define any house term used more
than twice" rule after the round-1 rewrite left "offering" and "paygate"
undefined:

"Hold on, paygate and offering are words I would use. You can't make it
define every single fucking normal business term, right? I especially know
terms that I myself use. I think you're fucking missing the point with that:
house terms are never defined. By the way, making it wordier is not
helpful."

"Yeah you need to make it non-fucking heuristic. If you're making stupid
rules about things used more than twice, you're treating me like a fucking
child, right? How about this: you set up a cold reader agent who is me,
right? Have it read everything about me, everything I've written, and have
it give my fucking perspective and use that as the external validator for
this because you clearly suck at it."

What changed: the definition rule was deleted; the naming rule now turns on
ownership (the writer's private label versus the reader's own vocabulary),
not frequency; every numeric threshold (words per cell, words per sentence,
percent longer) was removed in favor of judgment tests; "do not make it
wordier" is a non-negotiable. A cold-reader agent immersed in his writing
and corrections now judges every round instead of the parent.

## What he asked for

1. Look at the reports.
2. Look at the writing materials agents have built in psagentspace.
3. Deeply research what great looks like, and his own preferences.
4. Save all findings to this doc pack.
5. Use `$skill-authoring` to build a skill.
6. Spawn a Codex Astra (low) agent, have it use the skill to rewrite a couple
   of his reports. Up to three rounds. Between rounds, the parent judges the
   rewrite against the bar and tweaks the skill.

## Two failure modes to hold at once

- Too dense: telegraphic fragments, internal codes, labels without mechanism,
  every sentence a puzzle. This is the default failure of agent reports.
- Too simple: "computers are like brains." Explaining the field instead of
  naming the fact. Padding. Talking down. This is the default failure when an
  agent is told "make it simpler."

The skill must remove the first without producing the second. The reader is
an expert. Give him the fact, the cause, and the consequence in plain words,
and never explain what he already knows.

## Doc pack layout

- `00-intent-and-notes.md`: this file.
- `10-amir-writing-rules-and-voice-corpus.md`: his existing rules and approved prose.
- `20-amir-corrections-on-readability.md`: his verbatim corrections from session history.
- `30-external-research-what-great-looks-like.md`: outside research and exemplars.
- `40-report-corpus-diagnosis.md`: sentence-level diagnosis of real reports.
- `50-synthesis.md`: the principles the skill is built on, with evidence pointers.
- `60-rewrite-rounds.md`: the Astra rounds, verdicts, and skill changes.
- `samples/`: saved reports and rewrites.
