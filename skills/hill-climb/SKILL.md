---
name: hill-climb
description: "Explicitly selected long-running, autonomous hill climb that spends a budget to keep improving one number (cost per install, conversions, follows) by the scientific method. Starts with an intake that interviews the owner (what it is for, success, spend, limits, which earlier work to use) and researches before anything runs; then runs scheduled ticks: draws every idea from research, plans every test before money moves, has fresh one-job agents check plans, builds, quality and results, makes each creative from what inspired it, weighs soft signals beside the numbers, acts on reversible moves quickly but believes a lesson only after a rerun, never stops exploring, and reports on a schedule. After intake it asks the owner only for more money. Use when the user chooses $hill-climb or asks to start, import or run a budgeted optimization loop. Not for a one-off analysis or a single A/B readout, a quantitative investigation ($north-star-investigation), repo audits ($audit-loop), or watching agents ($agent-watcher)."
metadata:
  short-description: "Autonomous budgeted hill climb"
---

# Hill Climb

A hill climb spends a budget, one honest test at a time, to keep improving one number for as long as it runs, across as
many sessions and restarts as that takes. You are its main agent. It starts with an intake that interviews the owner
until you understand each other and researches what the interview raised (references/intake.md). After that, each tick
leaves the workbook true and current, money moving toward what earns, exploration still going, every idea grounded in
research, and every belief labeled with how sure it is. You run it alone. The owner is asked for nothing but more money,
with the case for it, and on the charter's schedule gets a progress report that asks nothing.

Run this skill only when the user chooses `$hill-climb` or `/hill-climb`, or asks you to start, import or run a
budgeted optimization loop.

## What holds on every tick

**The owner is asked for nothing but money.** The owner set the goal, the money and their limits in the intake interview
so the hill climb could run without them; intake, before the first tick, is the one time they are asked anything else. A
question parks the work until they come back and hands them a call the charter already makes. So when something breaks,
fix it or stop what it is costing, and record what you did. When the method looks wrong, call the strategist, which
changes it inside the charter; its cadence is the usual rhythm, not the only time. When an idea would need a different
goal, park it with the reason. A money request is the one exception (references/money.md). Progress reports go to them
on the charter's `reporting` schedule and ask nothing (references/reporting.md). Everything sent through the owner's
channel reaches them, so learn how a channel works from its help or documentation, never by sending through it. End
every tick with one line that says what it did, never with a question or an offer.

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
rebuilt comparison included; an item that already ran unchanged has its record instead. The checks must not become the
climb's slowest step, since a day a ready test waits is a day it does not learn: gather the tests ready at once into one
round so one set of checks covers them all, and run the build-checker and the critic together, since both look at the
same built items and neither needs the other. Done that way, a test still launches in the tick it was ready.

**You never judge your own work.** You think about this hill climb on every tick, you planned its tests, and you want
them to win. That makes you the worst judge of whether they are good enough. So nothing passes, gets believed or gets
money on your say-so: checkers check plans and builds, the reader reads results, the auditor traces whole tests, and you
act on their rows. Being stricter than they are is always open to you: reject, withdraw or redo your own work when you
see a flaw, and record why.

**Act quickly; believe slowly.** Most moves can be undone the next day: shifting some test money, starting the next
test, pausing a loser. Waiting for certainty on those costs more than an occasional wrong move. The lean worth acting on
comes from a read at its planned date. A lead partway through a test is its noisiest slice, mostly luck and novelty, and
money moved toward it also changes which days and people that side buys, so the planned read no longer compares like
with like, all for a few days of slightly better spending (references/evidence.md). A lesson is different: once
believed, it narrows what you try and where the money goes, and first results run hot from novelty, luck and the day of
the week. So a lesson is believed only after a rerun on fresh days shows the same thing on its own data, and the main
budget usually waits for that (references/evidence.md).

**Exploring never stops.** A hill climb that only exploits settles on the nearest peak and stays there while the world
drifts. The pull to pour everything into today's winner is strongest exactly when one option wins big, and that is when
exploring matters most (references/map.md; references/money.md, which also covers what an end date changes).

**The charter keeps the climb consistent.** What the owner said in the interview (the charter's owner fields, with the
Interview tab behind them) never changes during a run unless the owner changes it, except `money_total` when you record
a grant. Everything setup worked out for itself, and the fields that record how this climb weighs its recurring calls,
keep every fresh session working the same way; the strategist revises them as the climb learns, with a Decisions row
saying why. Judge each case in front of you with them in mind, and when a case calls for something else, say why in that
decision's row (references/charter.md). A departure you find yourself making tick after tick means the charter is wrong:
call the strategist to change it.

**Take now from a live clock.** Use the platform's own time when it reports one, else the machine's, never a time from
memory or a summary; compare read dates, due dates and review periods with it, stamp every row with it, and cut every
data window on the platform's reporting day and time zone.

**You judge; nothing judges for you.** Read the platform with its own tools, write the workbook yourself, and work
numbers out any way you like, including a quick calculation written on the spot; the row says how you got them. Keep
such working files with the climb, not in a shared temporary folder that other work on the machine also writes to. The
references teach what the numbers mean and what is at stake. No rule here decides in your place.

## Modes

- **Intake**, whenever the folder has no hill climb yet or its workbook's Charter is still empty: a new climb, or one
  built from earlier work such as an old tracker. Read references/intake.md and follow it through the interview, the
  research, the playback and seeding to the first tick. Each intake turn ends on its one question to the owner; intake
  is not a tick.
- **Tick**: the default whenever the folder has a hill climb with its Charter written.
- **Money request**: inside a tick, when money runs short or the owner has answered (references/money.md).

## The shape of a tick

A tick leaves the hill climb better informed and its money better placed. These are the places its work is usually
found, and each deserves a look every tick, though most ticks find several need nothing; anything else the record or the
platform shows you counts as much:

- Load the state fresh, reading each tab whole rather than its first lines: the Charter, open Tests, Lessons, Ideas, the
  Library, the last Reviews and Log rows, Money, and the platform's own status and clock. If the owner has answered a
  money request, record it: the answer usually comes back on the channel the request went out on, so look there while a
  request is open, as well as in the prompt. When a call turns on what the owner meant, read the Interview tab: their
  words are there, and so are their calls on the made-up outcomes intake asked about.
- Look for faults before anything else: anything that means money is reaching the wrong people, that an item is doing
  harm, or that the numbers can no longer be trusted. Some places they show: the platform's count against the second
  source, delivery against whom the plan aimed at, spend against the plan, an item the platform disapproved, a page the
  ads lead to that broke (both counts then fall together), a change in what the platform counts, a run of complaints,
  hides or reports on anything live, the best known option included, since that harm builds every day it runs. Counts
  never match exactly, and one that arrives late looks short on recent days, so a shortfall in the late count needs
  complete days to judge; lateness cannot explain a gap the other way, which needs its own explanation now, an ordinary
  one (such as sign-ups the platform never saw) or a sign that a count broke. Judge whether a gap is the usual one or a
  sign that something broke, and which side broke. Then weigh what the fault threatens and choose the response (pause,
  fix, set the data aside, hold the read), with its reason in a Decisions row. Nothing is ever read from data you set
  aside.
- Have the tick's due reads made by one reader, which also reports the soft signals: what people say and do around a
  live item (comments, saves, shares, hides, complaints) never overrides the bar, but it shows risks and strengths the
  count does not, and you weigh it in the decisions you take on each read (references/evidence.md). Look at when each
  role last reported (its newest Reviews row) against the charter's `cadence`. A cadence date is a time to look, like a
  lesson's recheck date: once it has passed, the climb has run on your own view longer than it meant to, which usually
  makes the review worth starting now; when it is not, say why in the Log. Reads and reviews can run at once, and a busy
  tick needs them as much as a quiet one.
- Act on what came back (references/evidence.md): moves that can be undone, reruns, lessons, the map.
- Ask whether any proven lesson has come into doubt: results that disagree with it, competitors changing what they run,
  a season turning, or simply its age (the charter's `lesson_life`). A lesson whose `recheck_at` has come is due that
  look now. Recheck it when the doubt is worth a rerun's cost, and say in the Log what you made of it either way.
- Weigh whether the research still describes the market (an item older than the charter's `research_freshness` is a
  prompt to check, such as whether that competitor still runs that ad, and what the check finds decides) and whether the
  waiting ideas would fill the next days of exploring. When either falls short, send the scout (references/research.md).
- Screen every idea still marked `new`, whatever else the tick holds: what it draws on, whether it fits the goal and the
  owner's limits (one that would need a different goal is parked with the reason), and whether it would teach something
  the record does not already know (references/map.md). An idea left `new` stays one step from being planned, a goal
  change or an answered question included. A plan changes what its question is about: asking whether one attribute helps
  means changing only that attribute; asking whether one cell beats another may change several, and the lesson is then
  about the cells.
- Keep spending near the charter's pace, putting each lane's next dollar where it buys most right now, with some of it
  always reaching untried options. Exploring is not what is left over: when the pace leaves no room for it, the split
  between the lanes is wrong, so move money to it from the others. The best known option is not a test that ends: it
  keeps earning in the exploit lane between and around tests until something better is proven or it stops earning, and
  keeping it live needs no new plan.
- Take each round of new tests through plan, plan-checker, build, then the build-checker and the critic together, before
  launch; a round is the tests ready at once, and planning the next days' tests together keeps the checks few. Size each
  plan before it goes: work out, as the plan-checker will, what it can see by its read date with the money in hand,
  since a plan sent back costs another round. Keep the Tests row in step with the platform (ids, status, a live test's
  budget). Make a new creative from the one or few things that inspired it, after looking at them, with its plan saying
  what it keeps from them, what it changes and who it is aimed at; cut a variation from its parent's own materials with
  the parent's recipe, changing only what its plan changes; make both with the charter's tools from what `making_from`
  names, to its `quality_floor`; record how each item was made and its coding, and keep its files where they last
  (references/making.md). To change a plan, before its check or after one, write the new plan as a new Tests row and
  withdraw the old one: a check vouches only for the plan it read, and anyone tracing the test later needs to see which
  plan each check saw.
- Ask for money early enough that the owner can answer before it runs out, once this tick's plans and checks have
  settled: the request tells the owner what the climb will do next, and a plan still waiting on a check may not happen.
  It never waits for a plan to pass: when nothing is ready yet, it says what the climb would test next and why.
- When a progress report is due (the newest Reviews row of role `report` against the charter's `reporting`), write it
  (references/reporting.md).
- Write the Log row, refresh the Overview tab, close anything you started that is still running, since it holds the tick
  open, and end with one line saying what the tick did.

A tick with no read due is not finished once the platform checks out or a money request is out; it is when the slower
work gets done: the reviews the charter's cadence has brought due, research that has gone stale or ideas that have run
short, screening the ideas that are waiting, weighing whether a lesson's age or a contradicting result calls for a
recheck, readying the next checked plans so money can move when it should. That work does not wait for free. Skipped, a
review that would have caught a costly method goes another week, an idea that repeats an answered question sits ready to
be tested, an old lesson keeps steering unexamined, and money idles while the next test is still unplanned.

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
round at once (every plan of a round to one plan-checker, every new item to one build-checker and one critic, started
together, every due read to one reader), start independent roles at the same time, and let each write a row per plan,
item or read; give it the keys its rows will use, so roles working at once never collide. A role writes only its own
rows (the strategist and the scout may also change rows in place, as references/workbook.md says) and names itself in
`written_by`.

Wait for a role's row before the step it gates; your host tells you when a child finishes, so do other independent work
meanwhile. When there is nothing else to do, wait on the signal that the work is done (the host's notice, or the role's
rows under the keys you gave it), not on a fixed delay or a guess, which spends the minutes the checks were meant to
save or never ends. Check that the row is there and whole, and against the data it was given, and do not overrule a call
in your own work's favor: a failed check stays failed until a revised plan or a rebuild passes, and a read stays what
the reader found. This is how the shared policy's "a child's output is evidence" applies here, since replacing an
independent judgment with yours would undo the independence. When a call rests on missing evidence or an unsound method,
or a row has wrong numbers, send a fresh role with the missing fact and record why; the fresh role writes the correcting
row.

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
