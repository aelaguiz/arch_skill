# Evidence: what a test can show, and how far to trust it

Read this on every tick that has a result to act on, a lesson to change, or a test to plan.

Contents: what a test can show · letting the running result decide nothing · why first results run hot · discounting ·
how sure to be · the record's words for a read · when the counts disagree · what people say and do around an item ·
lessons · worked cases · when a plan fails its check

## What a test can show

A rate measured on a sample is the true rate plus luck, and the luck shrinks only with the square root of the sample. A
few dozen conversions a side can separate a big difference, such as one option converting about twice as well as the
other, and nothing subtler; telling apart options a tenth apart takes many times the traffic. So before a test is
planned, work out what it can see: from the comparison's rate, the planned spend and the platform's cost, how many
conversions will each side have by the read date, and how big a gap stands out from luck at that size? If the gap the
plan hopes for is smaller, the test cannot answer its own question: plan a bigger swing, a longer read, or another test.
Traffic bought faster reads sooner: a test that buys its traffic in three days reads before one that spreads it over a
week. Whether that costs anything depends on the platform: where a click costs the same at any daily budget, the faster
test learns sooner for the same money; where results cost more as the daily budget rises, as on most auction platforms,
speed has a price. A shorter window also covers fewer days of the week and may reach a different slice of the audience,
so it must still cover what the comparison needs.

This is why a hill climb with little traffic tests big, different ideas rather than polishing one: small refinements are
invisible at its size, while a different approach can be told apart in days.

Work numbers out any way you like, including a quick calculation you write on the spot. The judgment stays yours, and
the row you write says how you got the number.

## Reading at the planned date

A test is read at the date its plan set before launch, or by a reading rule its plan set before launch. What goes wrong
otherwise is choosing when to look after seeing the data: a test watched every day and stopped on the day it looks good
roughly quadruples its false wins (in one simulation, from 5% to 23%), because luck always has a good day somewhere, and
a lead partway through is mostly luck and novelty. So no test is called a winner except at its planned read, and nothing
is believed on a lead partway through. Moving money toward a test that is ahead acts on that lead as surely as stopping
it on a good day would, and it also changes which days and people that side buys, so the planned read stops comparing
like with like; what it gains is a few days of slightly better spending. That trade rarely favors moving, the test's own
budget included. A plan that means to act on repeated looks says so before launch, with a method built for them (a
sequential test, say), and the plan-checker judges whether it is honest.

Stopping a test early for other reasons is a different trade. Cutting one that is losing badly saves money and costs a
little chance of seeing a winner that was having a bad start; whether that is worth it depends on how much it is burning
and how bad the start is, and a plan can name before launch what harm would justify stopping. A fault, spend running
away from the plan, or a market change that makes the question moot can also stop a test; traffic that came in short can
stretch one to a later read date. Say why in a Decisions row. A test stopped early tells you little about its idea.

## Why first results run hot

New items get a burst of attention that fades; some days of the week convert better than others; and a winner is chosen
partly because luck favored it, so part of its measured edge will not repeat. Compare the two sides on the same days, so
the calendar affects both alike, and expect any first result to shrink.

## Discounting toward past results

Past tests show how big real differences usually are. When most past tests moved results a little, a new result that
looks huge on a small sample is probably mostly luck. So pull each new result toward what past results typically were:
hard when the sample is small, gently when it is large. Some ways to do it: mix the new counts with the past results'
typical rate weighted like a modest test of its own; or compare the new gap with the spread of past gaps. Use a method
you can explain in a sentence, apply it the same way to both sides, and leave out the test's own earlier data so a
result is not discounted toward itself.

## How sure to be

How strong the evidence must be depends on what a wrong call costs, so set out the stakes before deciding: what the move
could gain, what it could lose, what waiting a few more days would cost, and how cheaply the move could be undone.

- **A move you can undo cheaply** (shifting some test money, starting the next test, pausing a test that is losing)
  needs only a lean, because waiting costs money every day and the move can be reversed when more is known.
- **A lesson** steers later tests and where the money goes, so it is not believed until a rerun on fresh days, read on
  its own data, shows the same thing clearly. Pooling the rerun with the first test would carry the first test's novelty
  and luck along.
- **Moving the main budget** onto a new option bets what the business earns on it. When most ideas fail, a good share of
  apparent wins are luck (when about 1 idea in 10 works, about 1 in 5 "significant" wins is false), and winners keep
  only part of their first edge once moved (one team's moved winners kept about 0.62 to 0.73 of their first level). That
  is why the main budget usually waits for a confirmed lesson and an edge big enough to survive that shrinkage. If a
  case looks different (a huge, clear effect on a large sample, or a move that costs little to reverse), say why in the
  Decisions row; the strategist and the auditor will look at it.

The charter's `acting`, `believing` and `replacing` fields say how this hill climb has been weighing these, in its own
words. Use them to stay consistent from tick to tick, judge the case in front of you, and when the case calls for
something else, say why.

## The record's words for a read

A read is recorded with one of three words: `act` (the evidence favors the tested option), `stop` (it does not) or
`hold` (the numbers cannot answer the question). If none fits, write the word you would use and why. The word says which
way the evidence leans now, not whether it is believed: a first read that leans is `act` or `stop` though no lesson
rests on it yet. The word is a summary; the row also sets out what was weighed. What to do next is a separate judgment,
recorded with its reason:

- A favored first read is a lean. It can earn some test money now and tilt which explore test comes next. Rerun it on
  fresh days when believing it would change something (narrowing the search, carrying the main budget, shaping later
  tests) and the money in hand can buy a rerun that reads, since a lesson does none of those until it shows itself
  twice. A lean that nothing will build on can stay a lean. Either way, a Decisions row says what you decided and why.
- A flat read means the test could not tell the two apart at its size. Record that, not a winner and a loser.
- A rerun that does not clearly show the same thing leaves the lesson unproven. It may mean the first read was luck, the
  effect is smaller than it looked, or it held only in some conditions; you might retire the lesson, narrow its claim to
  where it held, keep it as a light lean for exploring, or test it again bigger, depending on what knowing would be
  worth against what the test would cost.
- A hold means these numbers cannot answer the question. Plan it again if the question still matters once the cause is
  fixed.

## When the counts disagree

The platform's count and the second source's never match exactly: attribution windows, time zones and late arrivals see
to that, and some platforms spend past a daily budget on some days by design. So the question is not whether they differ
but whether this gap is the usual one or a sign that the counting or the delivery broke, which count is wrong, and
whether the call would change either way. If one count is plainly broken and the other is complete, read from the sound
one and say so. Set aside, with an `exclude-data` decision, only what cannot be trusted, and never read a result from
data you set aside.

## What people say and do around an item

The bar counts one thing. People also comment, reply, save, share, hide, report and complain, and those signals carry
what the count misses: an ad that converts while its comments call it misleading may be buying sign-ups that cancel,
wearing out the audience or the brand; one that people save and share may be earning beyond its window; the questions
people ask name what they want to know. Read them beside the count, with counts and a few quotes, and weigh them. They
never override the bar. A read's call says what the count shows, since lessons are built from it, and the signals sit
beside it in the read's `signals`; what they justify is a decision, with its reason (pausing a converting ad that draws
complaints, holding off on scaling one people resent, an idea taken from what people keep asking), and a pattern across
tests can be a lesson of its own. They build between reads too, so the tick's look for faults covers a run of complaints
on anything live. Put the audience's own words in the Library.

## Lessons

A lesson is one row per subject: what it says, what it compares (a `winner` and a `loser`, when it is a comparison), the
tests that are its evidence, and a status that says how far to trust it. Update the row in place as its status moves,
and keep every row: lists rewritten wholesale lose detail and do worse than none.

- A read that shows a difference records or updates an `unconfirmed` lesson. A confirm rerun is a new Tests row in the
  confirm lane with `rerun_of` and `lesson_id`, on fresh days.
- When a rerun shows the same thing clearly on its own data, the lesson becomes `proven`, with a `recheck_at` the
  charter's `lesson_life` away as a reminder. When it does not, the lesson stays unproven (above); say what you did with
  it and why. A retired lesson stays in the tab.
- A proven lesson's `recheck_at` is the date to look at it again, not a switch. When results disagree with it, the
  market changes, or that date arrives, weigh how much the lesson is steering, how fast this market drifts, and whether
  recent results still agree; mark it `recheck` and rerun it when that weighing raises a real doubt worth a rerun's
  cost, and say why either way.

Proven lessons may narrow the search and carry the main budget. An unconfirmed one may steer which explore test comes
next, lightly.

## Worked cases

These come from real hill climbs, told as general cases.

- **A day-of-week finding that faded.** Over ten days, clicks late in the week converted about twice as often as early
  in the week. It was tempting to move the whole budget. As a first result it was a lean: worth a rerun over the next
  weeks, read by day, and not worth betting the budget on.
- **A creative whose first days looked twice as good.** A new ad converted 11 of its first 32 clicks, then 5 of its next
  44; its first three days were its best everywhere it launched. That is novelty at work, and the reason the main budget
  waits for a rerun on fresh days.
- **A keyword group never bought because nothing was ever tried.** A group with no history looked worse than groups with
  thin, noisy histories, so it never got money. An untried option is not a bad one; what it could teach is a reason to
  try it.

## When a plan fails its check

A failed check is the check working. Read its reasons and decide what the idea deserves. A plan that can be put right
gets a revised plan, written as a new Tests row with the same `idea_id` while the old row becomes `withdrawn`, and goes
to a fresh plan-checker once it puts right everything the reasons name, sized again with the money in hand: a revision
that fixes one reason and meets the next costs another round. When the money in hand cannot buy a readable answer to the
question, the question is the wrong size for now; ask one a smaller test can read (a bolder change, or a gap the record
says is likely to be large), or let it wait for money. An idea that cites nothing goes back to research, and one that
repeats an answered question is parked. A built item that fails the build-checker or the critic usually gets a rebuild,
checked again, unless the reasons say the idea cannot be made well with what the platform offers. Whatever you decide,
the Ideas or Tests row says why.
