# The map: what to explore next

Read this when choosing explore tests, when new ideas come in, and when judging whether an idea is new.

## What the map is

Items are built from many attributes (an ad's headline, image, presenter and offer; a search term's intent; a page's
layout and promise), and every item is coded on all of them (references/making.md). The map is the grid of the few in
the charter's `map_attributes`, the ones with the most leverage; each cell is a **type**, written as `attr=value` pairs
in the Charter's attribute order joined by `|`.

Within a test, the sides differ only where its question is (below), so the result can be pinned on that; what the plan
holds, it names in `held_constant`, usually at a value chosen with care (the best known one is usual, unless it rests on
thin data or costs too much, like a deep discount). Across tests, results stay comparable because every item is coded in
full, so a later reader can see what else differed; production need not freeze for the whole climb. A new execution that
differs from what ran before in many ways is a fair explore test, and its lesson is about the items, not about any one
attribute.

Choose the map's attributes for the biggest expected swing in the bar, from history and research when there is some and
from the platform's own options when there is none, and keep the map small enough for the traffic to visit every cell
within a lesson's life: a map the money can never cover is a list of guesses.

The Map tab has one row per cell: `best` (the current best), `tested`, `untested`, or `stale` (tested so long ago that
the result may no longer hold). A cell whose test is live but unread is still `untested`. Update a cell after each read.

## Choosing what to explore

Weigh what each candidate could teach against what it would cost. A few things to keep in view:

- Attributes interact. A value that looks bad on average can be the best in combination, so a cell is not written off
  from its row and column, and an untested cell's promise is unknown rather than low.
- An option that stopped getting money after a bad start never gets the data that would correct it, so a thin history
  after a bad start can look worse than the option is; a thin history that looks good can be luck in the other
  direction. Stale results may no longer hold either.
- Research-backed ideas from outside the current search are how the climb finds what it would never have thought of.
- When recent tests keep circling one attribute or one corner of the map, ask whether that is because it keeps paying or
  because it is familiar.

## What a test may change

A test can only answer the question its plan asks, so what it changes must match that question. A plan asking whether
one attribute helps ("does a price-first headline beat a benefit-first one?") changes only that attribute and holds
everything else; change two things in one comparison and that comparison cannot say which one did it, though across many
coded items that vary both, the patterns can. A plan asking whether one cell beats another ("is a before-and-after photo
with a price-first headline better than our best?") may differ in several attributes, and its lesson is then about the
two cells, not about any one attribute. When no live option is the right comparison for the question, an explore test
may launch its own comparison arm beside it, on the same days.

The fastest teacher is often not any one test but the pattern across many. With many items running, each coded in
full, the attributes the promising items share and the weak ones lack show up across the coding long before
one-attribute tests could isolate them. Let those patterns suggest hypotheses, and use variations that change one
attribute of a promising item to check the ones worth money.

## Is the idea new?

Ask whether the test would teach something the record does not already know. A repeat of a tried test's cell and
approach wastes money when the earlier test answered the question; it is worth running when that answer was thin, broken
or old, and then it is a rerun with `rerun_of` set. An idea that only repeats an answered question gets `near_copy_of`
(the test it repeats) and is parked or rejected with the reason. A variation of a contender is not a repeat: it asks
what about the contender carries its promise. Nor are several different items in one cell repeats of each other: run
together, they show whether the cell or one item carries a result. A repeat is the same item, or one so close it could
teach nothing new.
