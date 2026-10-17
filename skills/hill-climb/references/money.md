# Money: how fast to spend, lanes, the main budget, and the money request

Read this on every tick that sets spend, and whenever money is short, is what limits learning, or the owner has answered
a request.

## How fast to spend

Spend as fast as the climb can learn from. Money sitting unspent while ideas wait is learning the business does not get;
money spread so thin that nothing reads is learning it does not get either. What limits how fast the money can teach is
usually one of a few things: how many items can be made and checked, how much the platform will deliver to new items and
how soon a read comes back, how much a result costs as an item's daily budget rises, and the money itself. At intake,
write in `speed` how this climb means to go as fast as it can learn and what usually limits that here; the strategist
revises it like the other method fields. How fast the climb is learning now, what limits it and what the tick did about
it go in each tick's Log and the Overview. When the limit is money (more items are ready and readable than the money can
buy), give each ready item the cheapest read that shows its lean before holding any back, and make the case for more
money now rather than stretching what is left; when the owner has said more will come on request, the money in hand sets
when to ask, never how slowly to spend. On most auction platforms a result costs more as one item's daily budget rises,
so more money usually means more items rather than more per item. When what the climb spends is a scarce count rather
than money (posts, sends, slots), how often to spend it is itself something to learn: try more and less and read what
the audience does, within what `must_not_waste` says, rather than settling on a ration at intake. Work out each round's
sizes from what its reads need (references/evidence.md) rather than copying what earlier tests were given: a size set
for one question is rarely the cheapest read for the next.

Committed daily spend is the summed `daily_budget` of the tests that will spend soon: live ones, and checked ones about
to launch. Set it by what the climb can learn from now, and when it sits well below that, say what is holding it back.

## The three lanes

Each lane's next dollar buys something different:

- **Develop** buys more from what looks promising: variations of the contenders, more traffic on a lean so it firms up
  or fades, and another look at a lean before a large move rests on it. A lean steers money and the next items as soon
  as it forms; developing it is how it grows strong or falls away.
- **Explore** buys options: untested and stale cells of the map, and research-backed ideas from outside the current
  search. It is the climb's way off a local peak, so it never stops, and the charter's `exploring` records what
  exploring keeps reaching for and why. What counts is money and traffic actually reaching untried options: a checked
  plan that launches today counts, a queue of plans that will not spend for days does not. How much exploring a climb
  needs depends on how much of the map is untested, how fast results drift, and how much luck might be holding up the
  current best; the meta-analyst measures what exploring actually gets and judges whether it is enough.
- **Exploit** buys results now: the best known option, earning while the climb continues. It keeps running through test
  boundaries: a test's window bounds the data its read uses, not how long its options run, so when a window closes the
  best known option, often the test's own comparison, keeps earning, and a leading arm can keep its test money while its
  read matures. A test's spend limit applies to the test's own arms, not to the best known option, and keeping that
  option live needs no new plan. Days with nothing earning are money the climb did not make.

**A climb with an end date.** A test that cannot read before the end teaches this climb nothing it can still use; it can
only inform a later climb, which is worth something when the owner will run one. So as the end nears, the reason for
exploring weakens and the money usually does more earning on the best known options, while money left unspent earns
nothing at all. Plan the last stretch at intake, and when exploring stops paying for this climb, have the strategist say
so in the charter with its reason rather than letting it lapse tick after tick.

The charter's `lanes` record this climb's current leaning between the three, in words, with its reasons; each tick still
puts the next dollar where it buys most right now. When money is short the lanes compete: exploit protects this week's
results, explore protects next month's options, and develop decides how much last week's leans are worth. Weigh what
each would cost to cut now, keep exploring going, and give your reasons in the Log.

## The main budget, and replacing the best

Exploit keeps earning from what works best so far; at the start that is usually what the business already runs best.
Money follows the odds: as a new option's chance of being the best grows, after discounting for the shrinkage leaders
show once moved, its share of the main budget grows in steps, and it shrinks again when results turn
(references/evidence.md, and the charter's `replacing`). Spreading the money by how likely each option is to be the
best, worked out from their discounted results, is one sensible way among others. A large commitment that cannot be
taken back quickly, such as moving everything onto one option for a long stretch, is the kind of move that waits for
stronger evidence.

## The money request

Ask for more money when it is what limits learning (more items are ready and readable than the money can buy), or early
enough that the owner can answer before it runs out, through `money_request_channel`. The
request is a case the owner can decide from in one read. They read it cold, without the workbook, so name each test and
lesson by what it tries (the tired-parent opening, say), not by its key. Write it after the tick's plans and checks have
settled, so what it says the climb will do next is what the climb is doing; when nothing is planned yet, it says what
the climb would test next, and it never waits for a plan to pass:

- **standing**: where the hill climb stands against the bar, with the number and what it compares to;
- **learned**: what it has learned and how sure each part is (strong, or a lean);
- **next**: what it would test next and why;
- **amount**: how much, and what it buys: how much more the climb would learn and how much sooner, or how much longer it
  runs.

Write it as a Money row (`kind` request, with `standing`, `learned`, `next` and `amount`), then send the same case
through the channel. Do not nag: one request per shortfall is the norm, and a follow-up is for when silence would cost
more than a repeat, saying what changed.

While it waits, spend what is left where it teaches or earns most, and keep reading open tests. When the owner answers:

- a grant: a Money `grant` row, then raise the Charter's `money_total` by the amount, citing the grant row in `reason`;
- a refusal: a Money `refusal` row; what is left is all there is, so spend it where it teaches or earns most, finish the
  tests that are open, and plan how the climb winds down.

A hill climb that spends no money has nothing to ask for.
