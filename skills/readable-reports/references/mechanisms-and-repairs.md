# Mechanisms And Repairs

Each mechanism below raises the cost of reading without adding a fact. The
"before" examples are verbatim from real reports written for the same reader;
the "after" versions are repairs built from facts the same report or its
sources contained. Use the mechanisms as recognition tests, not as a checklist
to recite. A sentence usually carries two or three at once; repair the one
that hides the most and the others often fall away.

The common cause: the writer has chunked the work into private labels and
forgotten the reader has not. The reader must rebuild the writer's model
before the sentence means anything. Every repair below either supplies the
model in the sentence or names the thing in words the reader already owns.

## 1. Undefined referent or internal-model word

The single most frequent failure. The sentence uses a noun that only the
writer's context can resolve: root, children, the reset, the stack, parity,
lane, band, face, canon, the verifier, GP, "three links".

Why it costs: the reader searches for an antecedent, finds none, and either
guesses or stops. In the lab a missing antecedent adds about 180 ms per
sentence; in a report it adds a re-read or a wrong guess.

Before: "Checkout root now clean, children blocked."

After: "The base pull request of the checkout repair stack
([psmobile #5001](https://github.com/funcountry/psmobile/pull/5001), Android
checkout cancellation evidence) passed review and CI. The four fixes stacked
on top of it ([#5056](https://github.com/funcountry/psmobile/pull/5056) to
[#5059](https://github.com/funcountry/psmobile/pull/5059)) cannot merge until
it merges."

Before: "Your language choice is confusing. Three links. What's a link? A link
in a chain? A URL link?" (the reader, on a deck that coined "three links" for
a three-stage funnel)

Repair rule: say the idea in plain words and drop the coined term, or name the
term after the idea. "The three stages from ad tap to install to first
purchase" needs no legend.

## 2. Telegraphic compression

Dropped subjects, verbs, and articles; facts joined by semicolons.

Why it costs: the words removed are the ones that fix who did what. Reading
time does not fall when articles and conjunctions are cut (Martin 1974:
25% fewer words, reading time flat); ambiguity rises. The reader supplies the
grammar the writer deleted, once per fragment.

Before: "Reset running September 2/4; audience rebuilt; SDK finding and 8 ASO
assets September 5."

After: "Tim restarted the Meta campaigns on the March settings on September 2
and 4, rebuilt the audience, and delivered eight App Store listing assets on
September 5. (The SDK finding is not described in the source.)"

Before: "Mtime alone not progress."

After: "A file being edited recently does not mean the work moved forward."

Repair rule: put the subject and verb back. If the cell is now too long, cut a
fact and keep the grammar. A cell that still needs semicolons is a list; make
it rows or bullets.

## 3. Bare code, id, or number with no plain name

"#4792/#4807", "MW-064", "S25", "W3", "A3", "2.1.41", a commit hash, a flag
name, a Sentry group.

Why it costs: a number is a pointer, not a fact. Even the writer's own reader
has to go look it up. "stop saying W3. I don't know what fucking W3 is. Talk in
English."

Before: "#4792/#4807 open at 15:40, same code since September 2; Natasha still
needs working events."

After: "The two pull requests that send mission events to Customer.io
([psmobile #4792](https://github.com/funcountry/psmobile/pull/4792) and
[#4807](https://github.com/funcountry/psmobile/pull/4807)) are still open and
have not changed since September 2. Natasha cannot rebuild her lifecycle
campaigns until they ship."

Repair rule: plain name first, code in parentheses, and a link on every PR,
issue, document, or message. A code defined forty lines earlier is still a
bare code here.

## 4. Tool state or system word used as English

CLEAN, BLOCKED, HOLDING, "ok", RECOVERED 2 of 3, FIXED IN MAIN, a flag name
and its value, "route_disposed".

Why it costs: these are enum values from a tool's state machine. "Clean" in
English means something else. The reader cannot tell whether the state is good
news, bad news, or nothing, or what would change it.

Before: "Settled Purchase parity AppsFlyer 5 / Meta 0; spend gate HOLDING."

After: "AppsFlyer recorded 5 purchases and Meta recorded 0 for the same
period, so the two do not agree yet. Ad spend stays where it is until they
do."

Before: "the pre-action reveal flip (playVsAiPreActionRecommendationRevealEnabled = false → true, one line)"

After: "The Play vs AI coach now shows its recommendation before the player
acts, instead of after. (Flag: playVsAiPreActionRecommendationRevealEnabled.)"

Repair rule: say what is true about the work and what the reader would see.
Keep the exact token in parentheses if someone will need to search for it.

## 5. Status label with no mechanism

"Aligned; finish delivery." "Aligned; event delivery blocked." "P1 WORSE."
A color with no sentence.

Why it costs: a verdict with no relation to attach it to. Readers process and
remember causal relations ("because", "until") faster than bare verdicts, at
every education level. These labels sit exactly where the reader decides, so
each one costs more than its length.

Before: "Aligned; event delivery blocked."

After: "Natasha's lifecycle work matches the LTV priority. It is blocked
because the mission events her journeys depend on have not shipped; the
backend agent and Natasha own that handoff."

Repair rule: every status names the subject, the state, the cause or blocker,
and the next step or owner. If the cause is unknown, write "cause not
checked". That sentence is more useful than the label.

## 6. Noun stack

Three to five nouns welded into a term the writer coined during the work:
"trigger-to-journey handoff", "campaign and signal recovery", "no-terminal
watchdog", "adjacent normalized-frame repeat rate", "purchase-terminal repair".

Why it costs: each adjacent noun pair forces the reader to pick a relation;
an ad hoc compound has no stored relation, so the reader computes one per
pair and guesses the grouping. Past three nouns the string stops parsing.

Before: "the inspected path has no bounded in-place recovery action if
neither native nor canonical evidence arrives."

After: "If the store does not answer within 10 seconds, the paywall shows
'Checking purchase...' and disables the buy button. If the answer never
comes, the player has no way out except the back arrow."

Repair rule: unpack the compound into a clause with a verb. Move the head
noun forward and add the missing relation.

## 7. Symbol standing in for a sentence

Arrows, "=", and slashes carrying "of", "versus", "and", "then", "becomes".

Why it costs: the relation is unstated, so the reader supplies it. One page
used 25 arrows in 2,300 words and slashes with three different meanings.

Before: "Profitable acquisition → campaign and signal recovery"

After: "Goal: paid ads that make money. Work: restore the March campaign
settings and fix the purchase events we send to Meta and AppsFlyer."

Before: "0 / 11 / 0 and 0 / 3 / 0"

After: "Friday: 0 bought, 11 cancelled, 0 errors. Saturday: 0 bought, 3
cancelled, 0 errors."

Repair rule: write the verb.

## 8. Number with no comparison or meaning

Why it costs: the reader does the division and then decides whether the
result matters. Both steps belong to the writer.

Before: "Paid D30 payer formation: 96/6,500 April →15/2,694 July; mature
cohorts, partial attribution."

After: "Of paid installs, 1.5 percent paid within 30 days in April (96 of
6,500). In July it was 0.6 percent (15 of 2,694). Attribution is incomplete,
so some paid payers may be missing from both counts."

A model sentence from a report that reads well: "iOS converts 56.4% of
started checkouts this week (79/140), a whisker under the spring's 58 to
66%."

Repair rule: rate, raw counts, baseline, and what it means for the decision,
in one sentence.

## 9. The report narrating itself

Run ids, model names, the rules the agent applied, what it suppressed, how
many sources it read, and sentences that describe how a section behaves.

Why it costs: the reader wades through the writer's day to reach the world.
"that is just putting all sorts of unecessary cognitive load in the report."

Before, at the top of a page: "Business outcomes first. Tasks last. Preserve
continuity. GP is non-authoritative. Plans and decisions are not goals; no
invented metric targets."

After: cut from the body. If a reader needs the method, it lives in an
appendix or a separate working file.

Before: "A watch, not a standing slot: it appears while open and retires when
closed."

After: delete.

Repair rule: the body is the judgment; the method is an appendix. No
"earlier reconstructions", "the previous turn", "above", "below". The page
stands alone.

## 10. Overlong sentence, stacked parentheticals, stacked hedges

Why it costs: working memory holds about four new chunks. A 174-word
"one line" with four URLs and three parentheticals exceeds that several
times over. Hedges stacked on hedges hide the magnitude and the certainty
the reader needs.

Before: "What happened, in one line: at 18:02:30Z Sep 4 (1:02pm Central) Fly
release v126 put Go backend decfcaee into production (release/2.1.41 plus the
EV-free advice backport ... plus the restored legacy entitlement bridge = the
mechanism the watch named for MW-052 on Sep 2, confirmed by the team's own
root-cause doc), the RustAI engine moved 947f5dcf to 0e91d464 ..."

After: "On Friday at 1:02pm Chicago we deployed a new backend and a new
poker engine. The backend deploy restored the old entitlement path, which is
what fixed the League standings errors. The engine deploy fixed the
three-player action bug and removed the CPU-heavy EV calculation."

Repair rule: one idea per sentence. State magnitude and certainty once, in
words: "median latency fell from 420 ms to 310 ms in one run; not repeated
yet" instead of "seems somewhat improved, possibly".

## 11. Mixed clocks and drifting names

Two time zones on one page, or the same thing under different names
("purchase blackout", "purchase-terminal repair", "Success measurement is
broken", "every store purchase grants Plus but the app never recognizes it"
for one bug across three reports).

Why it costs: the reader converts clocks, and cannot tell that two mentions
are one thing.

Repair rule: one clock, the reader's, stated once at the top. One plain name
per thing, reused exactly, on this page and the next report.

## 12. Heading that is a label, not a message

"Status", "Reproduction", "Lane", "Where everyone's work stands".

Why it costs: scanners read the first two words of a heading and decide
whether to read on. A topic label gives them nothing to act on; a message
does.

Before: "Status: Reproduced by direct production observation." (a method
template opening an audit, with the answer four sections down)

After: open with the executive answer as the heading: "Android converts
worse because many more checkout starts end in cancellation, not because
paywalls fail to load."

A heading that reads well: "This looks bad: on Android the app dies while
the person is using it and comes back on the 'Checking for Updates' boot
screen, somewhere else."

Repair rule: the heading states what the section says. A reader who reads
only headings should still have the story.

## 13. Explaining what the reader already knows

Defining a pull request, CI, a cohort, or a rate for an engineer; an analogy
in place of a mechanism; stating the obvious as insight; "simply",
"basically".

Why it costs: redundancy is load too, and it signals the text is not for
this reader. "You're stating the obvious shit in a way like it's insightful
before you give the actual feedback." Instructional support that helps
novices measurably hurts experts.

Repair rule: never explain the field and never define a word the reader
uses himself (paygate, offering, cohort, canonical). Name only the writer's
private labels. Keep real component names and real numbers; simplify the
sentence, not the vocabulary.

## 14. Editorializing and scolding

Asserting the business's intent, framing in-progress work as a problem,
dramatizing an expected cost, or telling the reader what he keeps failing
to do.

Before: "We keep shipping experiments whose answers we never collect."

After: "Three experiments are running with no dashboard that can score them:
the January home-tab split (about 7,800 users a week), the missions A/B
(0 of 6,206 assignments recorded), and the onboarding restart arms. Each
needs a decision: read it, or stop it."

Repair rule: report what was observed and how often. Leave judgment of
intent and priority to the reader.

## 15. AI tells and formula

Em dashes; the measured AI vocabulary (delve, crucial, pivotal, landscape,
underscore, testament, and the rest); negative parallelism ("not just X,
it's Y"); triads; mirrored contrasts; reveal bridges ("Here is the real
issue"); recap loops; ceremonial closers; the same sentence shape in every
row.

Why it costs: the reader stops trusting the page. "sounds like AI" is a hard
fail from this reader, on sight.

Repair rule: remove the word by repairing the sentence, not by swapping a
synonym. The canonical list lives in one file:
`/Users/aelaguiz/workspace/psagentspace/skills/fc-authored-copy/references/editorial-judgment.md`.

## The worked row

The original table cell, describing the reader's own work, to the reader:

"Comparison worksheets delivered; repair stacks moving. Checkout root now
clean, children blocked. Aligned; finish delivery."

Mechanisms present: 1, 2, 3, 4, 5, 9 (the verdict label is the writer's
process word).

Repaired, at the length a status cell can hold:

"You delivered the March-versus-now campaign comparison worksheets. The
checkout repair stack is close: the base pull request
([psmobile #5001](https://github.com/funcountry/psmobile/pull/5001)) can merge
now; the four fixes stacked on it
([#5056](https://github.com/funcountry/psmobile/pull/5056) to
[#5059](https://github.com/funcountry/psmobile/pull/5059)) cannot merge until
it does. None of the five is in a store build yet. Next: merge the stack and
cut a release candidate."

Seventy words against fifteen, and it can be read once. That is the trade.
