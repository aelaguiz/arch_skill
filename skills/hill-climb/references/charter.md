# The charter: its fields, and seeding from earlier work

Read this when intake writes the Charter (references/intake.md), when seeding a climb from earlier work, or when a
Charter field's meaning is in doubt.

Contents: where the charter comes from · the owner's fields · what setup works out · the method fields · the
workbook's form · triggers · seeding from earlier work

## Where the charter comes from

Intake writes it, once the owner has signed off on the playback (references/intake.md). The owner's fields come from
the interview, in the owner's words; setup's fields and the method fields come from intake's research and your
judgment, each with its reason. Every field is a row with its `value`, `reason` and `history`.

## The owner's fields

These hold what the owner said in the interview, in their words, with the Interview key behind each in its `reason`.
The climb never changes them; only the owner does, and then intake reopens that one question (references/intake.md,
Seeding). `money_total` also rises when a grant is recorded. Where the owner said "your call", the field holds your
choice and says so, and the strategist may revise it like setup's own.

| Field | What to write |
|---|---|
| `purpose` | what the climb is for: the outcome behind the number, and why now |
| `earlier_work` | each piece of earlier work and the owner's ruling on it: use it, use it as history only, or leave it out |
| `goal` | the number being improved and which way ("cost per sign-up, lower is better") |
| `success` | what the owner counts as success or break-even, in their words; `bar` holds the number worked out from it |
| `money_total` | the money given so far |
| `levers` | what the owner allowed the climb to change |
| `off_limits` | what the owner said must never happen or change |
| `making_from` | what creatives are made from: the material, the people, the sources |
| `quality_floor` | the items new ones must be at least as good as, and what can never be wrong in them; as the climb makes better items, the best of them raise the floor |
| `tool_rules` | tools the owner said to use or never to use |
| `research_direction` | where the owner said research should look, and anything they asked to have researched |
| `reporting` | how often the owner gets a progress report, in what form and where it goes (references/reporting.md) |
| `money_request_channel` | how a money request reaches the owner: the channel the request came through, or the one the owner named |

## What setup works out

These are setup's own judgments about the climb's world, made from intake's research. Write each with its reason and
sources; the strategist revises them as the climb learns, with a Decisions row. Some revisions need care: changing how
the bar is counted, or the second source, costs comparison with every earlier result, so make the change when what it
gains is worth that (the old count broke or drifted from the goal, or a truer one became available) and mark the break;
new attribute values grow the map, and their cells start untested. When a field can only be finished once data comes in,
such as a bar built on a baseline the climb has yet to measure, write in it what it waits for; the strategist fills it
in when the data is there, as it would any other revision, so the number every later call is held to has an independent
hand and a Decisions row behind it.

| Field | What to write |
|---|---|
| `bar` | the number decisions use, its formula and its source of truth, worked out from `success` with each assumption |
| `budget_unit` | what the climb spends: a currency, or a count of something scarce (posts, sends, slots) |
| `must_not_waste` | what must not be wasted (money on reads that cannot show even a direction, the audience's patience) |
| `attributes` | the full coding of the medium: every attribute a viewer could notice or a maker could choose, each with its values and an example of each, in the order types are written (references/making.md) |
| `tools` | what the climb makes items with now, inside `tool_rules`, and why each is the one to use |
| `platform` | the commands or tools that read data and act, including where people's comments, saves, shares and hides on the items can be read |
| `second_source` | the independent count that checks the platform, and how late it can be |

## The method fields

These record how this climb has chosen to weigh its recurring calls, so that every fresh session weighs them the same
way. They are reasons and a current leaning, not cutoffs: a number written here gets followed by every later session, so
write the reasoning, and a number only where the field asks for one. Keep each to a few sentences: the main agent reads
them whole every tick, and a field that grows into operating rules decides the cases its reasons were meant to inform.
You choose them at intake from the research and the situation; they are this skill's to set, never a question for the
owner. Afterwards the strategist changes them, each time with a Decisions `method-change` row, and you update only
`trigger`. When the record shows the method costing something, call the strategist then; its cadence is the usual
rhythm, not the only time. None of them decides a case by itself: each decision still judges the case in front of it,
and says why when it departs from them.

| Field | What it records, and what to weigh |
|---|---|
| `early_read` | the cheapest signal that tracks the goal, and how often it is checked against the goal: a cheap signal that drifts from the goal steers the whole climb wrong |
| `map_attributes` | which attributes form the map (references/map.md) |
| `lanes` | the current leaning between develop, explore and exploit, in words, with the reasons (references/money.md) |
| `exploring` | what exploring keeps reaching for however well the best is doing, and why: which untried cells and outside ideas matter most, how much of the map is untried, how fast results drift, how much luck may be holding up the best; never nothing while a test could still read before the climb ends |
| `acting` | how sure the climb wants to be before a move, by what a wrong move would cost: directional, about 60 to 80 percent, for anything that can be undone (references/evidence.md) |
| `believing` | how a lean grows strong (later items, variations and reads that keep agreeing), and what a large, hard-to-undo move needs on top |
| `replacing` | how money follows the odds onto a new option, and what a large commitment that cannot be taken back quickly needs |
| `lesson_life` | roughly how long a strong lesson goes before its age alone puts it in doubt: shorter where results drift fast |
| `research_freshness` | how fast this market's research material goes stale, and why (references/research.md) |
| `test_sizing` | how to work out the cheapest read that shows which way an item leans on this platform, from its costs and rates, and how a fair comparison runs here; worked out again for each round from what its reads need, never a size or count that later rounds copy |
| `speed` | how this climb means to go as fast as it can learn, what usually limits that on this platform, what decides how far ahead of its reads it makes items here (how much the coming reads could change them, how long making, checking and any owner's yes take), and, where it spends a count such as posts, how it means to try spending more and less and read what each does, and why; how fast it is going now goes in the Log and the Overview (references/money.md) |
| `cadence` | how often ticks run and watch for faults (often enough that new results are acted on soon after they arrive), step back (meta-analyst), revisit the method (strategist), audit, and replay past calls (the auditor re-scoring calls made since the last replay against what came after, and checking the early read still tracks the goal): often enough to catch a narrowing search before it wastes a week, rarely enough that each method change can be judged before the next |
| `trigger` | what starts the ticks (below) |
| `role_model` | the model the role agents run on: the one the shared policy's routing table names for hill-climb roles |
| `outside_sources` | where research looks, and the tools that reach it: the owner's `research_direction` first |
| `competitors` | who the competitors are, from research |

## The workbook's form

Use the workbook the request names, or the one the hill climb already has. Otherwise create a Google Sheet when the host
can reach Google Sheets, since that is where its owner can read it; if the host cannot, or the owner asked for files,
keep a folder of CSV files, one per tab, in the hill climb's folder. Record the choice in the Log.
references/workbook.md has the tabs and columns.

## Triggers

Ticks need something to start them, and only the ticks are scheduled: everything else the climb does is decided inside
one (SKILL.md, The tick is the clock). If something outside this session already starts the ticks, schedule nothing and
record that. Otherwise prefer a trigger that lives outside any one session, such as the host's durable scheduler or a
job on the machine that starts a fresh session for each tick, since every tick reads its state from the workbook anyway.
A job kept inside one session stops when that session ends, moves to another account or reaches its expiry. When that is
all the host offers (on Claude Code, a recurring session job whose prompt names this skill and asks for the next tick,
at the charter's cadence; such jobs expire after seven days), each tick checks the job and creates it again before it
lapses, and the climb's notes say how a fresh session restarts it. Record which in `trigger`. Never ask the owner to
schedule ticks. Whatever starts them, a tick must pick up cleanly from the workbook and the platform after any restart,
since sessions end, move and compact.

## Seeding from earlier work

Earlier work (an old tracker, past tests, idea lists, dimensions, rulings, research) comes into the climb only as the
owner ruled in `earlier_work`; what they left out is used nowhere. What they let in keeps its trail, and the old record
is not rewritten, because its owner may still read it and it is the evidence for what came over. Every imported row
names where it came from in `legacy_ref` (such as `<tab or file name>:<row number>`). Choose the form with that in
mind: a new workbook beside the old one, or new tabs in the same sheet when its owner already reads it daily.

Some things to carry over with care:

- History the owner let in comes over as closed tests and their results (`call` `legacy`), so discounting has past
  results to learn from and the map starts with what is known. Gather the files and recipes of any item the climb may
  vary (references/making.md).
- A test still running is read like any live test, by the climb's reader as soon as it has enough data to lean; until
  then it has no result, even when the owner let its file in as history, since its numbers so far are a window still
  open, not a read.
- An old learning the owner let in comes over at the strength its evidence carries (a `lean`, or `strong` where many
  results agree), whatever the old tracker called it, and only when it is about the new `goal`; one the record already contradicts is weighed like a lean
  that later results went against (retired, narrowed or kept as a light lean), with that evidence.
- Old hypotheses the owner let in become Ideas that cite their legacy rows; old research or angle lists become Library
  rows.
- Old choices (the measure, the dimensions, the test sizes, the rules for reading results) do not come over as choices.
  Intake works each one out again from the goal and the research; where it lands on an old choice, it gives its own
  reason.
