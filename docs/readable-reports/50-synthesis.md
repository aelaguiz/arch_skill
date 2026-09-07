# Synthesis: What The Skill Is Built On

Date: 2026-09-06. This file turns the four evidence files into the principles
the `readable-reports` skill teaches. Each principle names its evidence so a
later editor can check it instead of trusting it. Evidence keys:

- `10`: `10-amir-writing-rules-and-voice-corpus.md` (his standing rules, approved prose)
- `20`: `20-amir-corrections-on-readability.md` (67 verbatim corrections, 12 approvals)
- `30`: `30-external-research-what-great-looks-like.md` (outside research)
- `40`: `40-report-corpus-diagnosis.md` (63 flagged passages across 6 real reports)

## The one-sentence version

Write every sentence so a smart engineer who has been away from this work for
two days can say back who did what, what is true now, why, and what happens
next, after one read, without looking anywhere else on the page.

## What the problem is, and is not

The problem is reconstruction cost. The reader has to rebuild the writer's
model before the sentence means anything. It is not length. It is not
vocabulary level. It is not the reader.

- The trigger line, "Checkout root now clean, children blocked", was written
  about Amir's own work, to Amir, and he could not read it (`40`, case study).
  So "the reader lacks context" is not the explanation.
- Every one of the 63 flagged passages fails on the dense side. Zero fail by
  talking down (`40`, findings). The corpus does not show the "computers are
  like brains" failure, but Amir names it as the usual result when he asks
  for simpler text (`00`), and the ledger has it: "one tick too dumbed down
  ... I dont' want to be spoken to like a child" (`20`, 2026-08-31).
- He rejects padding and compression with the same force: "don't write a
  fucking book" and "I can't even understand what the fuck you're saying"
  on a 54-word post (`10`, finding 3). Shortness is not the target. One-pass
  parse is.
- "You're over explaining and under explaining simultaneously" (`20`,
  2026-06-21): method and history pile up while the one load-bearing fact is
  missing. That is the precise shape of most agent reports.

## The reader

A senior engineer and the CEO. He built much of the system. He does not hold
it in working memory today: "pretend I'm not familiar with the fucking plan"
(`20`, 2026-07-04), "I've been working on this for 2 days. I don't know what
an earlier reconstruction is" (`20`, 2026-09-04). He wants the plain sentence
first and the exact term second: "what does that mean in plain english" then
"are you saying its a reverse incompatible build?" (`10`, 2026-08-05). He will
not be told what he already knows: "you're literally defining a fucking
wheel" (`10`, 2026-08-15). And he reads to decide, not to admire coverage:
"I don't care about receipts. I care about good headlines and good copy."
(`10`, 2026-08-23).

Calibration that follows: never define what any engineer knows (pull request,
CI, staging, cohort). Always name what is house-specific (a workbook, a
verifier, an internal code, a tool's status word). Keep real component names
and real numbers. Simplify the pacing and the sentence, not the vocabulary of
the field.

## The mechanisms, ranked by cost

From `40` (counts are flagged passages out of 63; most passages carry more
than one mechanism):

| Mechanism | Count | What it costs the reader |
|---|---|---|
| Undefined referent or internal-model word (root, children, reset, parity, lane, canon, GP) | 45 | Must rebuild the writer's model before the sentence means anything |
| Telegraphic compression (dropped subject, verb, article; semicolon chains) | 18 | Must supply the grammar the writer removed |
| Bare code or ID with no plain name (#4792, MW-064, S25, 2.1.41) | 18 | Must go look it up, or guess |
| Noun stack ("trigger-to-journey handoff", "campaign and signal recovery") | 17 | Must unpack a hidden sentence |
| Agent narrating its own process (run ids, models, rules applied, what it suppressed) | 15 | Must wade through method to reach the fact |
| Symbol standing in for a sentence (arrows, "=", slashes with three meanings) | 10 | Must guess the relation |
| Status label with no mechanism ("Aligned; finish delivery", CLEAN/BLOCKED, HOLDING) | 8 | Sits at the decision point; says neither cause nor consequence |
| Number with no comparison or so-what ("96/6,500 April → 15/2,694 July") | 6 | Must do the division and decide if it matters |
| Overlong sentence, stacked parentheticals, stacked hedges | 13 | Must hold too much at once |
| Mixed or unlabeled time zones | 4 | Must reconcile two clocks |
| Heading that is a label, not a message | 4 | Must read the body to learn what the section says |
| Same thing under different names across the page or across reports | 3 | Cannot tell that two mentions are one thing |

Amir's corrections map onto the same list (`20`, findings 1 to 10): bare codes
("stop saying W3 ... Talk in English"), density ("get to simple punchlines
quickly"), buried answers ("Just tell me the fucking caveat"), artifacts that
lean on the chat ("Nobody knows what you're talking about"), system words
instead of user-facing words ("written for robots not humans"), over- and
under-explaining at once, tone (both edges), editorializing ("You're framing
it with this authority on the business"), shape (outcome first, tables,
one unhedged sentence on top), and unclear questions ("What the fuck are you
asking me in plain English?").

## The principles the skill teaches

Each principle is a consequence of "the reader must not have to reconstruct".
When a case is not covered, reason from the consequence.

### 1. Name the thing, every time

A word only the writer's context can resolve is a bare code, whatever it looks
like: "W3", "MW-064", "#5001", "root", "children", "the reset", "the stack",
"parity", "canon", "GP", "the verifier", CLEAN, BLOCKED, HOLDING. Name it in
the reader's words on every mention; put the exact code, number, or term in
parentheses after the name when it is needed as a lookup key. Never lead with a
term the reader has not met. If a label needs a legend, rename the label.

Evidence: `10` (Plain English, Never Bare Codes, 2026-08-21: "a code defined
40 lines earlier is still a bare code"); `20` finding 1 (nine rows, three
runtimes); `40` finding 1 (45 of 63).

### 2. Tool states and system words become sentences about the work

GitHub says CLEAN and BLOCKED; a flag is named `playVsAiPreActionRecommendationRevealEnabled`;
a Sentry group is "1Y"; a scheduler says "ok". None of these is English. Say
what is true about the work and what the reader would see: "can merge now",
"cannot merge until the base merges", "the reveal now shows before the
player acts", "the error has not fired since Friday's deploy". The reader's
model of the work chooses the nouns, not the writer's data model.

Evidence: `40` case study (CLEAN/BLOCKED pasted from `mergeStateStatus`;
"root"/"children" from the PR body); `20` finding 5 ("you're not speaking in
user facing terms"; "A flag name is not an explanation"; "written for robots
not humans").

### 3. Every status carries its mechanism and its consequence

A status is four things: the named subject, what is true now, why (the cause
or the blocker), and what happens next or who acts. "Aligned; blocked" gives
one of the four. "Checkout root now clean, children blocked" gives none. A
sentence that has the state but not the cause is a label; a sentence with the
cause but no consequence leaves the reader to decide whether it matters.

Evidence: `40` finding 6 (status labels sit at every decision point); `20`
finding 3 ("You're telling me it's complete but not complete. It's
nonsensical."; "what's between us and the plan being done?"); `10` finding 4
(state and next action open the status).

### 4. Full sentences: a subject and a verb in every one, tables included

Telegraphic fragments save the writer ten words and charge the reader for
each. Write "Tim restarted the Meta campaigns on the March settings on
September 2 and 4", not "Reset running September 2/4". A table cell is one
fact in one sentence, or a short list of such sentences; a cell that needs
semicolons is a list and gets rows or bullets. Never use an arrow, "=", or a
slash where a verb belongs. When the sentence is too long, cut a fact; never
cut the grammar.

Evidence: `40` findings 2, 7 (25 arrows in 2,300 words; slashes with three
meanings); `10` gap 3 ("the fix is cutting a claim, never fusing"); `20`
finding 2 ("five or seven words" for notes, but always words).

### 5. Answer first, then mechanism, then evidence

The first sentence of the document, of each section, and of each table row
is the message. One unhedged sentence on top ("put a single top level
commander's directive at the top. that should be one unmistakable sentence,
not hedged"). Evidence links follow the point, never lead it. If there is
one caveat, the caveat is the answer. Headings are messages, not labels: the
reader should know what a section says from its heading.

Evidence: `20` findings 3, 9; `10` findings 4, 6 ("receipts follow the OP and
draft, never lead them"); `40` "what reads well" 1, 4, 5 (the executive
answer; "This looks bad: ..." as a heading); `30` (BLUF, Pyramid, inverted
pyramid, Rogers and Lasky-Fink).

### 6. Numbers arrive with their comparison and their meaning

A number alone is a puzzle. Put the rate next to its raw counts and next to
the baseline that gives it meaning, in one sentence: "iOS converts 56.4% of
started checkouts this week (79/140), a whisker under the spring's 58 to
66%." Do the division for the reader ("1.5 percent in April, 0.6 percent in
July"). Say what the number means for the decision in the same breath.

Evidence: `40` finding 8 and "what reads well" 2; `20` (reactivations row:
"Are these returning users? ... Help me understand").

### 7. The report is about the business, not about itself

Run ids, model names, the rules the agent applied, what it suppressed, how
many sources it read, and how it verified go in an appendix or a separate
working file. The body is the judgment. No sentence describes the report's
own behavior ("A watch, not a standing slot: it appears while open and
retires when closed"). No "earlier reconstructions", "the previous turn",
"above" or "below". The artifact stands alone.

Evidence: `40` finding 5 (15 passages); `20` finding 4 and the 2026-07-18
row ("that is just putting all sorts of unecessary cognitive load in the
report"); `10` finding 10 ("no report-about-itself exposition anywhere").

### 8. Do not talk down; do not editorialize

The reader is an expert. Do not define common engineering or business terms,
do not use analogies in place of mechanisms, do not state the obvious as
insight, do not pad with "simply" or "basically". Keep real names and real
numbers. And report what was observed and how often; do not assert the
business's intent, scold the reader, or dramatize an expected cost: "I'm
seeing a lot of instances where this feels like a very aggressive user
experience" is the register, not "the energy wall is built as an
interruption."

Evidence: `20` findings 7, 8 ("Don't talk to me like I'm an idiot but don't
use jargon either"; "one tick too dumbed down"; "remvoe this: We keep
shipping experiments whose answers we never collect"); `10` (Amir 2026-08-03:
"stating the obvious shit in a way like it's insightful").

### 9. One name per thing, one clock per page

The same bug carried four names across three reports (`40` finding 10). Pick
the plain name once and reuse it exactly. Give every time in one time zone,
the reader's, and say which. Newest first in vertical lists; time left to
right in charts.

Evidence: `40` findings 9, 10; `10` (Charts Flow Left To Right; Tables Stay
Newest First, 2026-07-20).

### 10. Every reference is a link with a plain name

Any PR, issue, commit, document, dashboard, message, or file the text
mentions is a clickable link labeled with what it is: "[the Android checkout
cancellation PR (psmobile #5001)](https://github.com/funcountry/psmobile/pull/5001)".
Never a bare number the reader has to go find. Never a raw URL as the label.
Paths are absolute.

Evidence: `00` (Amir, 2026-09-06: "any time we mention a PR or an issue or
anything, it should just be a link"); `10` (PR And Issue Mentions Are
Hyperlinks, 2026-08-21; File Paths Are Always Absolute, 2026-08-24).

### 11. Questions to the reader are one plain question with the choices in words

If the report needs a decision, write the question a person could answer
from that one paragraph: what is being decided, the two or three choices in
plain words, and what each one changes. Not an item code, not "reply go on
the four rulings".

Evidence: `20` finding 10 (five rows: "What the fuck are you asking me in
plain English?").

### 12. No AI tells, no formula

Em dashes, the measured AI vocabulary, negative parallelism ("not just X,
it's Y"), triads, mirrored contrasts, reveal bridges ("Here is the real
issue"), recap loops, and ceremonial closers are hard fails. So is the same
shape repeated across every row or every report. The canonical banned list
lives in one file; point at it, do not copy it.

Evidence: `10` finding 9 and "What he rejects"; `20` finding 7 ("sounds like
AI" is a hard fail); canonical list:
`/Users/aelaguiz/workspace/psagentspace/skills/fc-authored-copy/references/editorial-judgment.md`.

## The test

Read the sentence once, cold. Can you say who did what to what, what is true
now, why, and what happens next, without looking anywhere else on the page?
If not, the sentence has one of the twelve mechanisms in it. Find which and
repair that, rather than shortening.

Evidence: `10` gap 10 (the community ledger's cold-read test, ported); `20`
2026-07-18 ("have an agent cold read this and put theirselves in the seat of
andrew or one of our investors ... could they read this and make sense of
it?").

## Shape he has accepted

- One unhedged sentence on top that carries the message. Then tables.
- Business outcome first, initiative second, tasks last.
- Tables for status of many things; a few words per cell, in sentences.
- Numbered steps for plans. Numbered answers to numbered questions.
- Process or method at the bottom, or in a separate file.
- A short "words I use" block at the top when the page needs house terms
  (the September 3 Meta ads report did this and every later sentence reads
  at a glance).

Evidence: `20` finding 9 and "what he praised"; `40` "what reads well" 10.

## What the skill must not become

- A length cap. Length is not the target.
- A synonym swap. A banned word is removed by repairing the sentence.
- A template. "A correction to a template is not a new template."
- A harness. "Don't build some fucking harness ... Just update the skill."
- A vocabulary cap. Keep the real terms; supply the plain sentence first.
