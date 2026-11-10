# The reader: what Amir opens a sheet for

Read this before building a new tab, tracker, model, summary or dashboard,
and when he says a sheet is confusing, overloaded, too wordy or not useful.
`SKILL.md` states the intuitions. This file gives, for each one, what a miss
costs him, cases that look different from each other, where it stops, and
the question to ask while you look at the rendered tab.

His words for a sheet that works are "at a glance" and "get a read". A
sheet that fails is one he has to study.

The formatting rules in `formatting-guide.md` make a grid readable. These
intuitions decide what the grid should be. When the two pull apart, the
reader wins: a tab that passes every format check and leaves him unable to
answer his question has failed.

## 1. One question, answered on the first screen

**What a miss costs.** He reads the whole tab to learn something one line
could have said. Or he cannot find the line, and asks in chat, which is the
thing the sheet was there to save him.

**Cases.**

- A model works a goal back through every step of a funnel, and no cell
  says whether the goal is hit. The first tab should open with the question
  in words, the answer, and the size of the gap.
- A tab of checks where every status looks open. Cutting each cell to one
  line changes nothing. One line at the top naming the work that is left,
  and saying that closed rows need nothing, does.
- An analysis with a row per segment and a column per step. He needs every
  segment on one screen first, with a mark on what stands out, then the
  detail behind it.
- One wide tab that mixes situations, analytics, status and technical rules,
  when he wants to know two things: what situations exist, and what should
  happen in each. Two columns, grouped.
- The rows he needs most sit at the bottom of a long tab, or the roll-up is
  the last tab. Position is priority: first tab, top rows.

**Where it stops.** When he asks for a dump by name, give the dump: raw
material in a tab that he will build on. Raw-data and source tabs feed
formulas and checks and need no answer block. A summary never replaces the
detail. The detail stays in the workbook, behind the summary, linked from
the row it supports.

**In the grid.** The answer and a frozen header both want row 1. A long
table keeps its header at row 1 and takes its roll-up to the tab in front
of it. A tab of short stacked blocks freezes nothing and opens with the
roll-up.

**Ask while looking.** What did he open this tab to find out, and can I
read it off the first screen without scrolling or reading a cell twice?

## 2. The things he compares are columns

**What a miss costs.** With the compared things stacked in rows, or named
as a pair in one cell, he holds two names in his head and works out the
direction himself. With a sentence in a cell he has to read where he meant
to scan.

**Cases.**

- An experiment: control is one column, the variant is the next, the
  measures are rows. Not tiles, not one row per arm.
- A model: current and proposed are columns, the steps run down the rows in
  the order the arithmetic runs, and the base figures are the first rows.
- Who owns what: one column per owner, so a gap or a duplicate shows as a
  cell. A list of rows with the owner written in each one hides it.
- A cell that reads "took 40 s before, 12 s after" is two columns. A cell
  that mixes one side's result with a comment is a result column and a
  notes column. His fix is always more columns, never longer cells.
- A grid of campaign results whose campaign names moved into hover notes
  and whose setup rows moved below the performance rows. He cannot tell
  what the numbers belong to. Identity first, in cells, in his names.

**Where it stops.** Comparing a few things across many measures puts the
things in columns. Scanning many things on a few fields (a tracker, an
inventory) keeps one row per thing, with the short sorting fields on the
left and the long detail on the right. Side by side works for numbers and
short cells; long text wants the full width. Newest first is his direction
for versions and past periods in a table: leftmost column, or top row in a
vertical list. Rows are things he would recognise from using the product
(the screens a player sees), not the stages of your analysis.

**Ask while looking.** If I put my finger on one row and read across, am I
comparing the things he wants compared? Do I know what each number belongs
to before I reach it?

## 3. A figure sits beside what he reads it against

**What a miss costs.** He reads each figure against his target, the last
figure he saw, or the size of the business. A figure with no base looks
wrong, and one wrong-looking figure makes him doubt the tab. A figure in a
new unit looks like new bad news. A hidden figure looks like concealment.

**Cases.**

- A count of users that is a narrow filtered group, with nothing saying so.
  It contradicts the number he knows. The population and the dates belong in
  the header or the title.
- Rates with their bases somewhere else. The denominators go in rows at the
  top of the block, so every rate under them can be read against them.
- A summary of segments that becomes useful the moment the target sits in
  the next column.
- A column whose header does not say which way is good, holding a negative
  number. He reads the result backwards. Put the direction in the header.
- A scenario column next to an actuals column on a different base. He reads
  a drop that is not there. Same base, or a visible seam and a header that
  says what differs.
- A blended priority score. A correct explanation does not rescue it. Show
  the raw figure he can reason about.
- The newest versions left blank because their data is partial, or a rate
  shown as `Unavailable` because one feed is incomplete. Show what was
  observed, mark the column `to date`, and put the count beside the rate.

**Where it stops.** His field's own measures need no gloss: a confidence
interval, a win rate, a cost per install are plain to him, and a range
beside the rate is welcome. A plain "what this means" column is for the
work's own inputs and assumptions, in a few words; it goes when the facts
are ones he reads directly. A limit that changes what every number under
it is (most rows had no input, only half the records matched) is not a
per-cell mark. It goes once, at the top of the block, where the bases are.
`—` stays the mark for a value that does not exist.

**Ask while looking.** For this figure, can I see on the tab what it
counts, out of what, over which days, and what it should be? Is anything
blank that I have a number for?

## 4. The tracking sheet is where he looks instead of asking

**What a miss costs.** If the sheet lags the work or cannot be read at a
glance, he asks for status, which is what the sheet exists to prevent. If a
status cell holds notes, he reads every cell to learn whether a row is
done, and the tab always looks unfinished.

**Cases.**

- A status cell holding a sentence of evidence. The state is one value from
  a short list he chose, set by dropdown; the evidence lives on a details
  tab.
- Two status columns that he must combine to get the real state. One status,
  plus a count where it helps (done of total), plus what is next.
- A "defects found" column holding audit history beside the open defects.
  The column holds open defects only, and is empty when there are none.
- A roll-up count that needs a footnote to explain what it counts. One
  scale, one definition, and the roll-up is a formula over the rows.
- A row added for every post or event, or a history of how things got this
  way. The board is the picture of how things are now; activity and history
  go in a ledger he opens when he wants it.
- A table whose rows and columns shift between updates. He compares each
  version with the last, so the shape stays fixed and only values change.

**Where it stops.** This is not "fewer columns". He asks for more columns
when each one tells him something he would otherwise open every issue to
learn: the root cause, how items relate, what needs him. Each is a few
words. A decision he has made once goes into the sheet as a standing fact
so it stops being raised. The status list is his: short status words he set
are welcome, and ones you coin are not.

**Ask while looking.** Reading only the status column and the top rows,
can I tell what is done, what is left, and what needs him?

## 5. The sheet is his workbench, and you are his analyst

**What a miss costs.** A verdict where the data should be asks for trust he
cannot check. A plan for his week is you doing his job. A column he has to
fill in is a question parked where he will not answer it. He strips all
three out before he can use what is left.

**Cases.**

- An inventory he asked for, with a next action and a priority dropdown
  added on every row. He asked for the list.
- A dashboard that grew dated checkpoints and a recovery policy. He asked
  for something to look at.
- A results view that ends in a badge. He wants current and proposed side
  by side, one row per situation, the unknowns still marked unknown, and
  the source beside the claim.
- A feedback column, a "your thinking" column, lettered options in a
  dropdown with a formula counting how many he has answered. He will not
  fill in a form you built for him. He talks, and you record what he said.
- Sections or columns beyond the one he asked for. He has to work out what
  they are and whether they change the answer.

**Where it stops.** Stripping the judgment out is the opposite failure, and
he rejects it too. Deciding among rows, he asks for exactly these columns
in words: priority, testable now or later, recommended and a short why. A
green or red mark on cells that sit well above or below the rest is
welcome, because the numbers it reads are right there. In a tracker, what is
next and what needs him are state. A list of calls to make works as rows
with what is wrong for whom, your pick, a short reason, and a decision
cell that you fill from what he says. The ask itself still goes to him in
chat, in words. Your reading of the data goes in the message beside the
link, as your reading.

**Ask while looking.** Did he ask for every column here? Is there a cell
waiting for him to type? Where I marked something, can he see what the mark
is reading?

## Two that sharpen rules already in the guide

**His tabs are the format.** He keeps a house layout and expects new work to
match it. In a workbook he works from, read the tabs he built or praised
before you add a tab or a column, and make what you add match the cells
around it. A block poured in at full completeness (long cells, many new
columns) breaks the whole sheet for him even when every fact is right. He
often settles the shape before the data. A mock is the real grid, in its
final layout and style, in the tab where the real thing will live, with
made-up values and a title that says so. A layout he sketched in the
working sheet is both the format and the place: fill that tab. Once real
data is in, the word "mock" comes off, because he reads the title
literally.

**A tight header is where a private label gets made.** The guide asks for
short labels, and a header is the smallest space in the workbook. An
abbreviation, a nickname for a column, a tool's status word or an issue
number standing in for a task name all read fluently to you and stop him
cold. A label says what was counted ("Users in first 72h", not "Early
users"), so it cannot hide a choice you made. A tab or block title says
what it is: today or proposed, real or mock, a plan or a brainstorm. When
the plain name does not fit, the column gets wider.
