# The charter: setting up and adopting a hill climb

Read this when setting up a hill climb, adopting an existing tracker, or when a Charter field's meaning is in doubt.

Contents: setting up · the owner's fields · the method fields · the workbook's form · triggers · adoption

## Setting up

The person starting the hill climb says what they want in plain words ("get the cost of a sign-up as low as possible;
you have $2,000 for the quarter"). Turn that, the platform and any history into a complete Charter without asking
anything: where something is not stated, choose what a careful operator would and write why in the field's `reason`. A
question at setup is the first of many; an assumption written down can be revisited by the strategist.

1. Read what the platform offers (its options, costs and limits) and any history the folder holds.
2. Research before choosing anything else (references/research.md): who the competitors are, what has worked for them
   and for the category, how the audience talks. Fill the Library.
3. Code the medium (references/making.md) and write the Charter, every field below with its reason.
4. Create the workbook (below) and fill the Map: one row per cell of `map_attributes`, `untested` unless history or
   research says otherwise. Decide what exploit runs at first, with your reason: usually what the business already runs
   best, since stopping it would cost money to learn nothing; with no history there may be nothing known yet worth
   exploiting.
5. Import useful history as closed tests and their results with `legacy_ref`, so discounting has past results to learn
   from and the map starts with what is known; for any item the climb may vary, gather its files and how it was made
   (references/making.md).
6. Write the first Ideas, each drawing on the Library, then run the first tick.

## The owner's fields

These hold what the owner actually said, and they never change during a run, except `money_total`, which rises when a
grant is recorded.

| Field | What to write |
|---|---|
| `goal` | the number being improved and which way ("cost per sign-up, lower is better") |
| `money_total` | the money given so far |
| `off_limits` | what the owner said must not change |
| `money_request_channel` | how a money request reaches the owner: the channel the request came through, or the one the owner named |

## What setup works out

These are setup's own judgments about the climb's world. Write each with its reason; the strategist revises them as the
climb learns, with a Decisions row. Some revisions need care: changing how the bar is counted, or the second source,
costs comparison with every earlier result, so make the change when what it gains is worth that (the old count broke or
drifted from the goal, or a truer one became available) and mark the break; new attribute values grow the map, and their
cells start untested.

| Field | What to write |
|---|---|
| `bar` | the number decisions use, its formula and its source of truth |
| `budget_unit` | what the climb spends: a currency, or a count of something scarce (posts, sends, slots) |
| `must_not_waste` | what must not be wasted (money on unreadable tests, the audience's patience) |
| `levers` | what the hill climb may change |
| `attributes` | the full coding of the medium: every attribute a viewer could notice or a maker could choose, each with its values, in the order types are written (references/making.md) |
| `audience` | who the items are for and where they meet them; the critic judges as one of them |
| `reporting` | how often the owner gets a progress report, in what form and where it goes (references/reporting.md): what the owner asked for, which then stays as they said it, else what fits how they read |
| `platform` | the commands or tools that read data and act, including where people's comments, saves, shares and hides on the items can be read |
| `second_source` | the independent count that checks the platform, and how late it can be |

## The method fields

These record how this climb has chosen to weigh its recurring calls, so that every fresh session weighs them the same
way. They are reasons and a current leaning, not cutoffs: a number written here gets followed by every later session, so
write the reasoning, and a number only where the field asks for one. You choose them at setup from the situation;
afterwards the strategist changes them, each time with a Decisions `method-change` row, and you update only `trigger`.
When the record shows the method costing something, call the strategist then; its cadence is the usual rhythm, not the
only time. None of them decides a case by itself: each decision still judges the case in front of it, and says why when
it departs from them.

| Field | What it records, and what to weigh |
|---|---|
| `early_read` | the cheapest signal that tracks the goal, and how often it is checked against the goal: a cheap signal that drifts from the goal steers the whole climb wrong |
| `map_attributes` | which attributes form the map (references/map.md) |
| `lanes` | the current leaning between confirm, explore and exploit, in words, with the reasons (references/money.md) |
| `exploring` | what exploring keeps reaching for however well the best is doing, and why: which untried cells and outside ideas matter most, how much of the map is untried, how fast results drift, how much luck may be holding up the best; never nothing while a test could still read before the climb ends |
| `acting` | how this climb weighs evidence before a move that can be undone (references/evidence.md) |
| `believing` | what a rerun has to show before a lesson is proven |
| `replacing` | what a proven challenger has to show before it takes the main budget |
| `lesson_life` | roughly how long a proven lesson goes before its age alone puts it in doubt: shorter where results drift fast |
| `research_freshness` | how fast this market's research material goes stale, and why (references/research.md) |
| `test_sizing` | how a test's size and read date are chosen from what it can show at the traffic |
| `pace` | the committed daily spend to aim at (references/money.md) |
| `cadence` | how often to watch for faults, step back (meta-analyst), revisit the method (strategist), audit, and replay past calls (the auditor re-scoring calls made since the last replay against what came after, and checking the early read still tracks the goal): often enough to catch a narrowing search before it wastes a week, rarely enough that each method change can be judged before the next |
| `trigger` | what starts the ticks (below) |
| `role_model` | the model the role agents run on: the one the shared policy's routing table names for hill-climb roles |
| `outside_sources` | where research looks, and the tools that reach it |
| `competitors` | who the competitors are, from research |

## The workbook's form

Use the workbook the request names, or the one the hill climb already has. Otherwise create a Google Sheet when the host
can reach Google Sheets, since that is where its owner can read it; if the host cannot, or the owner asked for files,
keep a folder of CSV files, one per tab, in the hill climb's folder. Record the choice in the Log.
references/workbook.md has the tabs and columns.

## Triggers

Ticks need something to start them. If something outside this session already starts the ticks, schedule nothing and
record that. Otherwise use the host's scheduler: on Claude Code, a recurring session job whose prompt runs this skill's
tick (a prompt that names this skill and asks for the next tick) at the charter's cadence. Those jobs expire after seven
days, so each tick checks the job and creates it again before it lapses, and records that in `trigger`. Never ask the
owner to schedule ticks.

## Adoption

Adopting an existing tracker means the climb continues with everything it already learned, under this skill's ways. What
matters: what the old tracker learned carries forward, every imported row can be traced back to where it came from (a
`legacy_ref` such as `<tab or file name>:<row number>`), and the old record is not rewritten, because its owner may
still read it and it is the evidence for what was imported. Choose the form with that in mind: a new workbook beside the
old one, or new tabs in the same sheet when its owner already reads it daily.

Some things to carry over with care:

- A test still running stays live; it has not been read yet, so it gets a read date now and no result.
- Closed results come over as results (`call` `legacy`), so discounting has a history to learn from.
- An old learning is a lean until a rerun has held, whatever the old tracker called it, so it comes over no stronger
  than `unconfirmed` unless the old tracker shows that rerun; one the record already contradicts is weighed like a
  lesson a rerun failed to show (retired, narrowed or kept as a light lean), with that evidence.
- Old hypotheses become Ideas that cite their legacy rows; old research or angle lists become Library rows.

Then research to fill what the old tracker lacked, fill the Map, and run the first tick.
