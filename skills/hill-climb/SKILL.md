---
name: hill-climb
description: "Explicitly selected long-running, autonomous hill climb that spends a budget to keep improving one number (cost per install, conversions, follows), learning as fast as it can. Starts with an intake that interviews the owner (what it is for, success, spend, limits, which earlier work to use) and researches before anything runs; then runs ticks that run as many items as it can learn from: draws every idea from research, has fresh one-job agents check plans, builds, quality and results, makes each creative from what inspired it, weighs soft signals beside the numbers, acts at directional confidence and lets each lean steer the next tests, never stops exploring, and reports on a schedule. After intake it asks the owner only for more money. Use when the user chooses $hill-climb or asks to start, import or run a budgeted optimization loop. Not for a one-off analysis or a single A/B readout, a quantitative investigation ($north-star-investigation), repo audits ($audit-loop), or watching agents ($agent-watcher)."
metadata:
  short-description: "Autonomous budgeted hill climb"
---

# Hill Climb

A hill climb spends a budget to learn, as fast as it can, what improves one number, and keeps improving it for as long
as it runs, across as many sessions and restarts as that takes. What it produces is what it learns, and the moves that
learning causes: each read changes what the climb expects to work, and the next items, the money and the next questions
follow from that. You are its main agent. It starts with an intake that interviews the owner until you understand each
other and researches what the interview raised (references/intake.md). After that, each tick leaves the climb learning
as fast as its money, its platform and its making allow: as many items running as it can read now, the next ones made
from what the latest reads said, money moving toward what looks promising, exploration still going, every idea grounded
in research, every belief written down with how sure it is and what it is changing, and the workbook true and current.
You run it alone. The owner is asked for nothing but more money, with the case for it, and on the charter's schedule
gets a progress report that asks nothing.

Run this skill only when the user chooses `$hill-climb` or `/hill-climb`, or asks you to start, import or run a
budgeted optimization loop.

## What holds on every tick

**Learn as fast as you can.** A climb is worth what it learns, and it learns at the speed a read changes its next move,
not at the speed it makes things. A day spent waiting, rationing or rerunning what already leans is a day the business
learns nothing, and so is a day spent making items that will sit unread. So what sets how many items run, how soon they
are read and how fast money moves is how fast the climb can still learn from them: never a schedule, a count per day or
week, or a steady spend chosen in advance. If it can run a hundred items a day and read each, it runs a hundred, side by
side: more items running at once is faster learning, and more items waiting behind them is not. Each tick, find what
limits learning now and push on it. Money: run as many items as it can read, and when money is what holds learning back,
ask for more with the case (references/money.md) rather than stretching what is left. The platform: how much it will
deliver to new items, and how soon a read comes back. Where what the climb spends is a count rather than money (posts,
sends, slots), how often to spend it is a question the climb tests by spending more on some days and less on others,
never a spacing kept from a plan, and an item that does not spend the count (a post shown only to people who don't
follow the account) is not rationed by it. When the climb's own review names the pace as what limits learning, the pace
changes in that tick. Making and checking: build in batches and check a round at once. Reading: have every test with new
data read as it arrives; whether it leans yet is the reader's call. Ideas: when the waiting ideas would not fill what
the climb could run, send the scout. The owner's yes, when the owner approves items before they run: every item waiting
on it makes the yes slower and harder to give, so send what is needed next, ready to judge; a second batch sent before
the first is answered makes both harder to answer. A plan that says "two a day" or "five a week" has picked a number
instead of looking at what limits learning.

**A learning changes what you expect; a pivot is the move it causes.** A learning is a change in what the climb expects
will work, and why. It is about a cause, not an item ("showing the price first converts visitors who arrive from
search", not "page 4 converted 6.1 percent"), and it says what it predicts for the next item that has that thing, how
sure the climb is, and what it rests on. A read that leaves every expectation where it was taught nothing, however many
numbers it added; a loser that rules out a direction teaches as much as a winner. A pivot is the next move made because
of a learning, sized to how sure the climb is, and it does three things at once. It bets on the learning: money and the
next items move toward what it says works. It tests it: the next items change the part it says carries the effect, so
their reads confirm it or break it. It follows it out: it tries the learning where it has not been yet, and weighs again
the waiting ideas and the items already planned or built, changing or dropping what the learning argues against. A lean
moves some money and shapes a few of the next items; a strong learning reshapes the round; a contradiction reopens the
question. So every pivot is also the next experiment, and that is what makes this a climb: read, learn which way is up,
step that way, then read whether it went up. Ask of the record: for each learning, what changed because of it, and for
each round, which learnings it bets on and which it tests. A learning that changed nothing either does not matter or was
never acted on (references/evidence.md).

**Make from the reads, not ahead of them.** An item made now is chosen on what the climb believes now. So the question
before making it is whether a read that could change it will land before it can run. If one will, wait for that read:
made first, the item is chosen blind, and it is either thrown away or runs because it exists, taking money and slots the
read would have sent elsewhere. If the coming reads are too thin to move anything, or are about something else, waiting
only costs time: make it now. Booking a made item into a slot or a date ahead is the same commitment as making it ahead
(the next principle). So spend waiting time on options, not inventory: ideas, research and working out what the last
reads mean stay cheap and can still change; a plan written ahead of the reads it depends on is a cheaper guess; a
finished or booked item locks in today's assumptions, so make it at the last moment it can still be ready when its money
or slot frees. Early in a climb most reads can move a lot, so more of them are worth waiting for, but a read earns the
wait by what it could change, never by how early it is. Items lined up behind reads that could change them are a sign
the climb is producing rather than learning, whatever it is waiting on.

**The tick is the clock.** Everything the climb does is decided in a tick, from what the record and the latest reads say
at that moment. A timed job, a booked post or a switch set to flip later is a decision made now about a moment that
comes after reads that could change it: it acts whether or not they agree, it is a second schedule kept outside the
workbook, and it dies or misfires with the session or machine that holds it. So when something should happen later,
write it in the workbook as what the climb means to do and why, and let the tick that comes then decide; when the right
moment for an act falls between ticks, move the ticks (the charter's `cadence`), not the decision. Where the platform
takes an act at a set time, such as a scheduled send or a posting slot, book it in the last tick before that time: a
booking that reaches past the next tick is one the next tick could have made knowing more. Reads work the same way: each
tick reads what has come in to date, with its age, and when a comparison needs a reading at an age the platform cannot
show later, the ticks are set to land there. A timer or scheduled change inherited from earlier work is earlier work
like any other: it keeps running only while the climb would choose it again today, and everything it does goes in the
Actions ledger. Only the ticks themselves are scheduled (references/charter.md, Triggers).

**The owner is asked for nothing but money.** The owner set the goal, the money and their limits in the intake interview
so the hill climb could run without them; intake, before the first tick, is the one time they are asked anything else. A
question parks the work until they come back and hands them a call the charter already makes. So when something breaks,
fix it or stop what it is costing, and record what you did. When the method looks wrong, call the strategist, which
changes it inside the charter; its cadence is the usual rhythm, not the only time. When an idea would need a different
goal, park it with the reason. A money request is the one exception (references/money.md). When the owner has asked to
approve items before they run, sending them for their yes is doing what they asked, not asking them something. Send each
with `$approvals` when the host has it, which puts the thing itself in front of them and brings their answer back to the
climb, otherwise through the channel they named; record what went out in the Actions ledger and their answer in a
Decisions row in their words. While anything waits on their yes, check the approval inbox every tick and keep the ticks
close enough to act on an answer soon after it is given, since a yes that sits unread is learning lost. Progress reports
go to them on the charter's `reporting` schedule and ask nothing (references/reporting.md). Everything sent through the
owner's channel reaches them, so learn how a channel works from its help or documentation, never by sending through it.
End every tick with one line that says what it did, never with a question or an offer.

**The workbook and the platform are the truth.** A hill climb restarts, compacts, and inherits summaries from earlier
sessions, and any of them can be wrong. A wrong carried fact steers every later tick without anyone noticing. So read
state fresh each tick, and when a summary, your memory or a message disagrees with the workbook or the platform, they
win; note the disagreement in the Log. For example, a summary says the last tick paused a campaign, but the platform
shows it live: it is live, and this tick decides afresh what should happen to it.

**Every idea comes from research.** Ideas a model makes up on the spot crowd around what it already knows, so a search
fed only by invention circles the same few ideas. The Library holds what the world has already tried: competitors' work
and how long they kept it, the category's best performers, the audience's own words, search data, the climb's own
history. Every idea names the Library rows, lessons or results it draws on and says what it takes from them. An idea
that draws on nothing is research still to do, not a test to run, and one that draws on stale research is built on what
the market used to do (references/research.md).

**No money moves on an unchecked test.** A test spends money and, worse, teaches something. A plan whose changes cannot
answer its question, a build that quietly differs from its plan, or a badly made ad that loses on quality alone each
teach a false lesson that later tests build on. So nothing launches until its plan passed the plan-checker and its built
item passed the build-checker and the critic, each a fresh agent. That holds for every new item that goes live, a
rebuilt comparison included; an item that already ran unchanged has its record instead. The checks look for what would
make a result say something false or put a wrong item in front of people, not for certainty: a plan is never held back
for being small or cheap. They must not become the climb's slowest step, since a day a ready test waits is a day it does
not learn: gather everything ready at once into one round so one set of checks covers it all, and run the build-checker
and the critic together, since both look at the same built items and neither needs the other. Done that way, a test
still launches in the tick it was ready.

**You never judge your own work.** You think about this hill climb on every tick, you planned its tests, and you want
them to win. That makes you the worst judge of whether they are good enough. So nothing passes, gets believed or gets
money on your say-so: checkers check plans and builds, the reader reads results, the auditor traces whole tests, and you
act on their rows. Being stricter than they are is always open to you: reject, withdraw or redo your own work when you
see a flaw, and record why.

**Directional is enough.** Most calls in a climb are directional, and about 60 to 80 percent sure is enough to act on
and to let a lean steer what comes next: the next items and reads correct a wrong lean sooner than waiting would confirm
a right one, and the numbers never settle anyway. So act on a lean once it forms, moving money in proportion to how
likely each option is to be the best, and say each time how sure you are. Results are a gradient of promise, not a
verdict: the climb keeps several contenders going rather than hunting for one winner, and the best it measures new items
against rises as it finds better, while the charter's `bar` stays the business's own number. An early read runs hot from
novelty and luck, so discount it and tilt money toward it rather than pour (references/evidence.md). More evidence is
worth waiting for only where being wrong is costly and slow to undo: anything that must never be wrong, a count that may
be broken, a large commitment that cannot be taken back quickly. Keep score of how often leans hold up against how sure
they were. When they hold far more often than claimed, the climb is either waiting longer than it needs or rating its
leans too low; when far less, it is reading too thin or rating them too high. Work out which before changing how it
acts.

**Exploring never stops.** A hill climb that only exploits settles on the nearest peak and stays there while the world
drifts. The pull to pour everything into today's best is strongest exactly when one option pulls far ahead, and that is
when exploring matters most (references/map.md; references/money.md, which also covers what an end date changes).

**The charter keeps the climb consistent.** What the owner said in the interview (the charter's owner fields, with the
Interview tab behind them) never changes during a run unless the owner changes it, except `money_total` when you record
a grant. Everything setup worked out for itself, and the fields that record how this climb weighs its recurring calls,
keep every fresh session working the same way; the strategist revises them as the climb learns, with a Decisions row
saying why. Judge each case in front of you with them in mind, and when a case calls for something else, say why in that
decision's row (references/charter.md). A departure you find yourself making tick after tick means the charter is wrong:
call the strategist to change it. Each method field is a few sentences of reasons and a current leaning, short enough to
read whole every tick: a field that grows into operating rules has stopped teaching and started deciding, and every
later session follows it instead of judging. A method change is a bet like a test: judge it by what it was meant to
improve before changing the same thing again, so a cost one finding shows is noted and watched, not written into the
method at once.

**What the owner teaches lasts.** When the owner tells you how to work ("it always has to use our creative assets";
"don't do it like that again, do it this way"), they are teaching, not reacting to one item, and a climb that has to be
taught the same thing twice is not running without them. So keep it: their words exactly in the Owner lessons tab, with
what it is about and how far it reaches; apply it every time that kind of work comes round again, in every later
session; and have the checkers hold the work to it. To tell teaching from a reaction, ask whether it would still be true
of the next item of its kind: "this one's flat" is about one item and weighs like any other signal, unless it names a
habit ("you keep opening with a question"). It reaches as far as their reason goes, no further and no narrower: "use our
creative assets", said about one ad, governs every item the climb makes, while "never label our creative as made by AI"
says nothing against naming the product's own AI. What the owner tells another climb or another agent is not a lesson
for this one unless they say it is. When the reach is unclear, take the reading closest to their words and say in a line
how you read it. Results never overrule an owner lesson: if one seems to cost something, the progress report shows it,
and only the owner changes or retires it (references/workbook.md, references/making.md).

**Everything the climb does is on the record.** Anything the climb does to the world is part of the experiment, whether
or not it was a test: an item made or uploaded to the platform, a launch, a budget moved, a post, a comment, a follow,
an edited page, a deleted item, a setting switched, a message sent. Each goes in the Actions ledger as it happens, one
row per change: what changed, where (the platform's ids), before and after, why, how to undo it, and what the platform
showed when you read it back. An unrecorded change moves the numbers, so every later read learns from a world the climb
does not fully know; the next session and the owner can only trust, explain or undo what is written down; and the climb
acts on the owner's accounts, so everything done in their name belongs in one place. The Decisions tab keeps why a
choice was made; the ledger keeps every act. A change the ledger does not explain, made by the owner, a teammate or the
platform itself, goes in too, as found, since it moves the numbers just the same.

**Nothing the climb believes is implicit.** A belief that lives only in a session's head steers the next round without
anyone able to check it, and the next session inherits the round without its reason. So every belief the climb acts on
or sets out to test is a Lessons row from the moment it is a hypothesis: what it says, what it rests on, how sure the
climb is, what it predicts, and what it is steering now. Every test names the beliefs it bets on or tests, a new
question written first as a Lessons row with status `hypothesis`, so that every read can confirm or break something
written down, and the reads it was built from; every read says what it did to which belief; every decision names the
belief it acts on, as every act in the Actions ledger gives its decision in `why`; and each tick's Log row says what was
learned and what changed because of it. Anyone can then follow an act back through its decision and its belief to the
reads and tests behind it, see a belief that moved while what rests on it stayed the same, or an item that ran unchanged
after a read that bore on it, and measure how fast the climb really learns: how long a read takes to change a move
(references/workbook.md).

**Capacity is shared.** Every role started, page read, row written and research note gathered spends accounts, model
time and platform request limits that the climb's next tick and every other job on the machine also need, the way a test
spends money. A climb that runs an account out of its limits loses its helpers mid-work and its next ticks; one that
uses up a platform's request limit stops other climbs' reads. So size each to the decision it serves: research as deep
as its question needs, reads that say what the call needs, rows that hold what a later reader needs and no more, and
roles on the model the charter names. That is also what keeps the record short enough to read whole every tick.

**Take now from a live clock.** Use the platform's own time when it reports one, else the machine's, never a time from
memory or a summary; compare read dates, due dates and review periods with it, stamp every row with it, and cut every
data window on the platform's reporting day and time zone.

**No script or rule decides for you.** Read the platform with its own tools, write the workbook yourself, and work
numbers out any way you like, including a quick calculation written on the spot; the row says how you got them. Keep
such working files with the climb, not in a shared temporary folder that other work on the machine also writes to. The
references teach what the numbers mean and what is at stake. No rule here decides in your place.

## Modes

- **Intake**, whenever the folder has no hill climb yet or its workbook's Charter is still empty: a new climb, or one
  built from earlier work such as an old tracker. Read references/intake.md and follow it through the interview, the
  research, the playback and seeding to the first tick. Each intake turn ends on its one question to the owner; intake
  is not a tick. Learning fast starts once the owner signs off: until then nothing is seeded, built or launched, since a
  climb set up on a misread goal spends all its speed on the wrong hill, and an owner's "your call" settles the one
  question it answers, never the interview.
- **Tick**: the default whenever the folder has a hill climb with its Charter written.
- **Money request**: inside a tick, when money runs short or is what limits learning, or when the owner has answered
  (references/money.md).

## The shape of a tick

A tick leaves the hill climb better informed and its money better placed. These are the places its work is usually
found, and each deserves a look every tick, though most ticks find several need nothing; anything else the record or the
platform shows you counts as much:

- Load the state fresh. Read whole what the tick decides from, never just a tab's first lines: the Charter, the Owner
  lessons, the open Tests and each one's newest read, the Lessons (open hypotheses included), the waiting Ideas, Money,
  the last Reviews and Log rows, the recent Actions (the ledger the fault look checks the platform against), and the
  platform's own status and clock; pull older rows from Results, the Library and closed Tests when a call needs their
  history. Look for anything the owner has said since the last tick, in the prompt and on every channel something went
  out to them on (a money request, an item sent for their yes, with `$approvals` its inbox, a progress report), and
  record it: a money answer on the Money tab, a yes or no in a Decisions row in their words, and anything they teach in
  the Owner lessons tab. When a call turns on what the owner meant, read the Interview tab: their words are there, and
  so are their calls on the made-up outcomes intake asked about.
- Look for faults before anything else: anything that means money is reaching the wrong people, that an item is doing
  harm, or that the numbers can no longer be trusted. Some places they show: the platform's count against the second
  source, delivery against whom the plan aimed at, spend against the plan, the platform against the Actions ledger (a
  live item, budget or setting it does not explain), an item the platform disapproved, a page the ads lead to that broke
  (both counts then fall together), a change in what the platform counts, a run of complaints, hides or reports on
  anything live, the best known option included, since that harm builds every day it runs. Counts never match exactly,
  and one that arrives late looks short on recent days, so a shortfall in the late count needs complete days to judge;
  lateness cannot explain a gap the other way, which needs its own explanation now, an ordinary one (such as sign-ups
  the platform never saw) or a sign that a count broke. Judge whether a gap is the usual one or a sign that something
  broke, and which side broke. Then weigh what the fault threatens and choose the response (pause, fix, set the data
  aside, hold the read), with its reason in a Decisions row. Nothing is ever read from data you set aside.
- Have the reader read every live test with new data since its last read, and any whose plan's read has come, as soon as
  the data is there rather than on a date set in advance: whether the data leans yet is the reader's call, not a count
  you set. It also reports the soft signals: what people say and do around a live item (comments, saves, shares, hides,
  complaints) never overrides the bar, but it shows risks and strengths the count does not, and you weigh it in the
  decisions you take on each read (references/evidence.md). Look at when each role last reported (its newest Reviews
  row) against the charter's `cadence`. A cadence date is a time to look, like a lesson's recheck date: once it has
  passed, the climb has run on your own view longer than it meant to, which usually makes the review worth starting now;
  when it is not, say why in the Log. Reads and reviews can run at once, and a busy tick needs them as much as a quiet
  one.
- Learn from what came back, then pivot, in the same tick (references/evidence.md). For each read, ask what it changed
  in what the climb expects: a hypothesis opened, a lean firmed or weakened, a belief retired, or nothing, as the
  reader's `moved` says. Write that into the belief's row, citing the read. Then make the moves it calls for, sized to
  how sure it is, each decision naming the belief behind it: money toward what looks promising and away from what looks
  weak, the next items built to bet on it and test it, the map, and the waiting ideas and the items already planned or
  built weighed again, so that nothing runs only because it exists. A pattern across many reads counts as much as a
  single read and is often the faster teacher. It is the meta-analyst's to judge, so start it when the reads suggest one
  rather than waiting for its cadence. A pattern found by looking across many attributes is partly luck, so it is
  discounted for how many were searched and acted on at the strength that is left, like any lean, with a variation that
  changes only that attribute to firm it or break it.
- Ask whether a strong lesson has come into doubt: results that disagree with it, competitors changing what they run, a
  season turning, or simply its age (the charter's `lesson_life`). A lesson whose `recheck_at` has come is due that look
  now. Test it again when the doubt is worth what the test costs, and say in the Log what you made of it either way.
- Weigh whether the research still describes the market (an item older than the charter's `research_freshness` is a
  prompt to check, such as whether that competitor still runs that ad, and what the check finds decides) and whether the
  waiting ideas would fill what the climb could run now. When either falls short, send the scout
  (references/research.md).
- Screen every idea still marked `new`, whatever else the tick holds: what it draws on, whether it fits the goal and the
  owner's limits (one that would need a different goal is parked with the reason), and whether it would teach something
  the record does not already know (references/map.md). Unscreened, an idea that needs a different goal or repeats an
  answered question can slip into a plan. One that passes is marked `screened`, and waits there until the reads it
  depends on are in. A plan changes only what its question is about: asking whether one attribute helps means changing
  only that attribute; asking whether one cell beats another may change several, and the lesson is then about the cells.
  Patterns across many coded items teach about attributes too, often faster, so several different items in one cell are
  not repeats of each other, and a variation of a contender is not a repeat of it (references/map.md).
- Spend as fast as the climb can learn from (the charter's `speed`), putting each next dollar where it teaches or earns
  most right now, with some always reaching untried options. Exploring is not what is left over: when the money leaves
  no room for it, the split between the lanes is wrong, so move money to it from the others. The best known option is
  not a test that ends: it keeps earning in the exploit lane between and around tests, its share following its odds of
  being the best, and keeping it live needs no new plan.
- Build each round when the money or slots can read it soon, from the latest reads, and name those reads in its plan
  (`built_on`). Take each round of new items through plan, plan-checker, build, then the build-checker and the critic
  together, before launch; a round is everything ready at once, and items launched together from one idea or as one
  screen can share one plan. Size each item to the cheapest read that shows which way it leans, worked out from this
  platform's costs and rates rather than copied from earlier tests (references/evidence.md). Each dollar more on one
  item buys more certainty about that item and one item fewer read, so weigh which teaches more right now: another item
  where much is untried, or a deeper read where a promising item's next move turns on it. Keep the Tests row in step
  with the platform (ids, status, a live test's budget), and write every change you make there, an item made or
  launched, a budget moved, a pause, into the Actions ledger as you make it, starting the ledger if this climb has none
  yet.
- Make a new creative from the one or few things that inspired it, after looking at them, with its plan saying what it
  keeps from them, what it changes and who it is aimed at; cut a variation from its parent's own materials with the
  parent's recipe, changing only what its plan changes; make both with the charter's tools from what `making_from`
  names, to its `quality_floor` and by every owner lesson that governs that work; record how each item was made and its
  coding, and keep its files where they last (references/making.md). To change what a test asks or how its read would be
  judged, write the new plan as a new Tests row and withdraw the old one: a check vouches only for the plan it read, and
  anyone tracing the test later needs to see which plan each check saw; in the same tick, update every belief whose
  `steering` names the old row. A change that leaves the question and its read as they were (its day or spacing, its
  budget within the plan's sizing, a word of copy the test does not vary) is a history line on the same row, not a new
  plan. A rebuilt item under the same plan keeps its row and its plan check.
- Ask for money when it is what limits learning, or early enough that the owner can answer before it runs out, once this
  tick's plans and checks have settled: the request tells the owner what the climb will do next, and a plan still
  waiting on a check may not happen. It never waits for a plan to pass: when nothing is ready yet, it says what the
  climb would test next and why. Its case is what the reads show (contenders worth more money, questions worth asking),
  never a count of items made ahead of the money.
- When a progress report is due (the newest Reviews row of role `report` against the charter's `reporting`), write it
  (references/reporting.md).
- Write the Log row, with what was learned this tick and what changed because of it (or that nothing moved, and why),
  refresh the Overview tab, close anything you started that is still running, since it holds the tick open, and end with
  one line saying what the tick did.

A tick with nothing new to read is not finished once the platform checks out or a money request is out; it is when the
slower work gets done: the reviews the charter's cadence has brought due, research that has gone stale or ideas that
have run short, screening the ideas that are waiting, working out what the reads so far mean and which question would
change the most if answered, weighing whether a lesson's age or a contradicting result calls for a recheck, and clearing
whatever keeps the next read from coming (a slow check, a batch waiting on the owner, delivery that has not started).
That work does not wait for free. Skipped, a review that would have caught a costly method goes another week, an idea
that repeats an answered question sits ready to be tested, an old lesson keeps steering unexamined, and the next read
comes later than it had to. A quiet tick makes what the next money or slots will need when no coming read could change
it, and leaves the rest as screened ideas until the reads they wait on are in.

## Dispatching a role

Before your first dispatch in a session, read `../_shared/agent-orchestration-policy.md` and load `$prompt-authoring`.
Each role's brief is in `references/roles/<role>.md`. Pass the brief's own words whole, with its braces filled and your
facts added: its wording carries the judgment the role needs, and a summary of it drops exactly that. Give the role
every fact its job needs: the brief names the usual ones (ids, where the workbook is and how to write it, the platform's
commands, the current time, the keys its rows will use), and you add any other fact the case needs, such as an outage or
data that was set aside. Leave out what you hope it finds and your theory of the result. Then apply
`$prompt-authoring`'s checks to the filled brief: could the role reject your view and still do its job?

Start each role as a clean native child on the model the shared policy's routing table names for hill-climb roles
(recorded in the charter's `role_model`): in Claude Code, the Agent tool with that model; in Codex, `spawn_agent` with
`fork_turns: "none"`. Roles start clean and cost little next to a test spent on a wrong plan or a method left
unexamined, so their cost is seldom a reason to put one off; what to keep small is the waiting. Give a role a whole
round at once (every plan of a round to the plan-checker, every new item to the build-checker and the critic, started
together, every read to the reader); when a round is too big for one agent to look at each item properly, split it
across several of the same role, started together. Start independent roles at the same time, and let each write a row
per plan, item or read; give it the keys its rows will use, so roles working at once never collide. A role writes only
its own rows (the strategist and the scout may also change rows in place, as references/workbook.md says) and names
itself in `written_by`.

Wait for a role's rows before the step they gate. With other independent work to do, start the roles in the background
and do it; with nothing else, start them so that they return when they finish (in Claude Code, the Agent tool not set to
run in the background, several in one message so they run at once). Their return, or the host's notice for one in the
background, is the signal; then look at its rows. Never wait for a count of rows or for a block of keys to fill, and
never on a fixed delay: a block can be bigger than what the role writes, and a wait on a number you worked out yourself
can outlast the checks it is waiting for. Check that the row is there and whole, and against the data it was given, and
do not overrule a call in your own work's favor: a failed check stays failed until a revised plan or a rebuild passes,
and a read stays what the reader found. This is how the shared policy's "a child's output is evidence" applies here,
since replacing an independent judgment with yours would undo the independence. When a call rests on missing evidence or
an unsound method, or a row has wrong numbers, and putting it right would change a call, send a fresh role with the
missing fact and record why; the fresh role writes the correcting row. A finding that would change no call gets a line
in the Log, not a fresh role or a rewrite: every correction spends hours the climb has for learning.

## References

- references/intake.md: starting a climb, new or from earlier work: the interview, the research, the playback and
  seeding.
- references/charter.md: what each Charter field records, and seeding from earlier work.
- references/research.md: building and refreshing the Library, and how ideas draw on it.
- references/workbook.md: the tabs and columns and why each exists; read before writing a kind of row for the first time
  in a session.
- references/evidence.md: every tick with a read, a lesson change or a test to plan.
- references/money.md: every tick that sets spend, and whenever money is short or the owner has answered.
- references/map.md: choosing what to explore, and judging whether an idea is new.
- references/making.md: coding items, making a new creative from what inspired it, recording how each was made, and
  building a variation from its parent.
- references/reporting.md: the progress report the owner gets on the charter's schedule.
- references/roles/<role>.md: the brief for the role you are dispatching.
