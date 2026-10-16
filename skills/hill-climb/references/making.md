# Making items: coding, new creatives, recipes and variations

Read this at intake, where the coding is built, before making any item, and whenever a plan varies an item that
already ran.

## Code every item richly

An item is more than the few attributes a test varies. A viewer notices, and a maker chooses, many things at once: a
video ad has dozens; a landing page has its headline, hero image, proof, how the price shows, the form and the button's
words; an email has its sender, subject line, preview text, opening, offer and call to action. Code every item, and
every Library row you can, on all of them, with values: the scheme goes in the Charter's `attributes`, each built item's
values in its Tests row's `coding`, a Library row's in its own `coding`. Build the scheme at intake, as research
(references/intake.md): from the medium's anatomy (what the platform's own guidance and the people who make these items
say they are made of), from what competitors vary, from the platform's options, and from the owner's own items that they
let in. Give each value an example, a real item or a line from one, so that two people coding the same item agree and an
idea can say exactly what it would change; trying the scheme on a handful of real items shows where two attributes
overlap or a value is missing. Code what is actually there, and say when an attribute cannot be seen or does not apply
rather than guess.

A rich coding does three jobs a thin one cannot. Once results come in, it shows which attributes go with the winners and
losers, which is how the map comes to hold the attributes that matter. It lets the build check see an item change
something its plan never named. And it lets an idea say exactly what it would change. The map (`map_attributes`,
references/map.md) still uses only the few attributes with the most leverage: the coding is the record, the map is the
search.

## Make a new creative from what inspired it

A new creative starts from its idea and the one or few things that inspired it: Library items, the owner's own items,
earlier tests. Look at them before making anything, since this is the research for this creative: how they open, what
they say, how they are made, what people said about them. When they do not show how to make it well (the craft of the
format, how others make this kind of item, a reference for a part the idea needs), look that up too before building, and
add what you find to the Library. Then write in its plan what it keeps from them, what it changes and who it is aimed
at; with what that should do to the number, that is the test's hypothesis, and the Tests row's `inspired_by` holds their
keys. Saying what it keeps and what it changes is what lets a result teach something: "we kept the competitor's question
opening and changed the subject to our app" can be built on, while "something like their ad" cannot. Who it is aimed at
belongs to the idea, not to the climb: the climb exists partly to find out who responds, so each creative says whom it
is for, and the critic reads it as that person.

Make it from what the charter's `making_from` names, with its `tools`, never with a tool `tool_rules` rules out. Left
to its defaults, an agent reaches for whatever model it remembers, often an old one; the tools intake found make good
items now are the ones to use, and using one outside them is a choice whose reason goes in the recipe.

How well it is made is judged against the charter's `quality_floor`: at least as good as the items it names, and never
wrong on what it says can never be wrong. Polish is not the bar. A plain, rough or AI-looking item often performs; it
falls short only when it would lose for being worse made, or gets wrong something that can never be wrong.

## Record how each item was made

Write each built item's recipe in its Tests row: the tool and the command, the prompts or templates, the models and
their settings, the voices, the source files and where they are kept, the exact copy; and, for a variation, the item it
was made from (`made_from`). A later session that never saw this one makes the item again, or varies it, from that
recipe. Without it, a fresh session rebuilds from the coded values or the copy, and a rebuild changes things nobody
chose.

Keep every item's files in the climb's own lasting storage, not where the tool left them: a generated take or a download
link can expire, and generators rarely make the same thing twice, so the original files are what a clean variation is
cut from. At intake, do the same for every item the climb may vary but did not make, such as the business's current
best among what the owner let in: gather its files and whatever is known of how it was made, and record them in its
row.

## Build a variation from its parent

A variation exists to answer one question about an item that did well, so it should differ from its parent only where
its plan says. Cut it from the parent's own materials with the parent's recipe, change only the planned attribute, and
keep every other choice the parent made: the same takes, voice, settings and copy. Make the new part the same way the
parent's parts were made, so the change is the one the plan names and not a change of production. A variation rebuilt
from scratch can differ in most of its attributes at once: a version meant to ask whether an ad sells without its
presenter, rebuilt rather than cut from the ad, also changes the voice, the pacing, the music and the words, and its
result can no longer say whether the presenter mattered.

When a clean variation cannot be made from the parent's materials, say so. A new execution of the idea is a different
kind of test: it gives the idea another fair shot, is planned and screened like any new idea, and is never read as
evidence about one change.

## What the build check compares

For a variation, the build-checker compares the built item with its parent on every coded attribute and the copy, not
only the attributes the plan names, since an unplanned difference anywhere can move the result. For a new item, it
compares the item with its plan. For both, it reads the recipe while the files still exist and judges whether a session
that never saw the build could make the item again from it.
