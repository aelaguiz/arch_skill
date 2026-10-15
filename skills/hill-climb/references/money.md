# Money: pace, lanes, the main budget, and the money request

Read this on every tick that sets spend, and whenever money is short or the owner has answered a request.

## Pace

Spend steadily enough to learn and earn while the money lasts. Too fast, and the money runs out before the first tests
have read, so the first request for more comes with nothing to show. Too slow, and tests take weeks to read and the
climb barely moves. At setup, write down in `pace` how fast this climb means to spend and why, from the money, the
platform's traffic and how long a test needs to read. Pace weighs how soon the climb needs answers, how much the
platform sells before each extra dollar costs more, and how long a test needs to read. When the owner has said more
money will come on request, there is no need to stretch what is in hand, and a pace that starves tests to make it last
makes the climb learn slowly and earn little; but more money on request does not make fast spending free. On most
auction platforms a result costs more as the daily budget rises, and money not spent stays with the owner. When what the
climb spends is a scarce count rather than money (posts, sends, slots), weigh how many the audience will welcome against
what `must_not_waste` says.

Committed daily spend is the summed `daily_budget` of the tests that will spend soon: live ones, and checked ones about
to launch. Keep it near the pace unless there is a reason not to, and say what the reason is.

## The three lanes

Each lane's next dollar buys something different:

- **Confirm** buys belief: a rerun on fresh days turns a lean into a lesson that can steer the search. A strong lean
  left unconfirmed can tilt test money and the next explore pick, but cannot narrow the search or carry the main budget,
  which is why confirming one is often worth more than one more new test.
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
nothing at all. Plan the last stretch at setup, and when exploring stops paying for this climb, have the strategist say
so in the charter with its reason rather than letting it lapse tick after tick.

The charter's `lanes` record this climb's current leaning between the three, in words, with its reasons; each tick still
puts the next dollar where it buys most right now. When money is short the lanes compete: exploit protects this week's
results, explore protects next month's options, and confirm decides whether last week's leans were real. Weigh what each
would cost to cut now, keep exploring going, and give your reasons in the Log.

## The main budget, and replacing the best

Exploit keeps earning from what is known to work. At the start that is usually what the business already runs best; a
new option earns the main budget when its lesson is proven and its edge would survive the shrinkage winners show once
moved (references/evidence.md, and the charter's `replacing`). When several proven options are close, spread the money
by how likely each is to be the best, worked out from their results after discounting; one sensible way among others. A
proven challenger with a small edge stays a lesson on the map and a reason to explore near it.

## The money request

Ask for more money early enough that the owner can answer before it runs out, through `money_request_channel`. The
request is a case the owner can decide from in one read. They read it cold, without the workbook, so name each test and
lesson by what it tries (the tired-parent opening, say), not by its key. Write it after the tick's plans and checks have
settled, so what it says the climb will do next is what the climb is doing; when nothing is planned yet, it says what
the climb would test next, and it never waits for a plan to pass:

- **standing**: where the hill climb stands against the bar, with the number and what it compares to;
- **learned**: what it has learned and how sure each part is (proven or unconfirmed);
- **next**: what it would test next and why;
- **amount**: how much, and what that buys at the current pace.

Write it as a Money row (`kind` request, with `standing`, `learned`, `next` and `amount`), then send the same case
through the channel. Do not nag: one request per shortfall is the norm, and a follow-up is for when silence would cost
more than a repeat, saying what changed.

While it waits, spend what is left where it teaches or earns most, and keep reading open tests. When the owner answers:

- a grant: a Money `grant` row, then raise the Charter's `money_total` by the amount, citing the grant row in `reason`;
- a refusal: a Money `refusal` row; what is left is all there is, so spend it where it teaches or earns most, finish the
  tests that are open, and plan how the climb winds down.

A hill climb that spends no money has nothing to ask for.
