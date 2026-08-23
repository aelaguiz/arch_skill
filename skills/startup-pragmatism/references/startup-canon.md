# Startup Canon: Best Practices and Sources

Distilled from primary sources - Paul Graham, Garry Tan, Michael Seibel, Sam
Altman, Jessica Livingston, Dalton Caldwell, Paul Buchheit, Reid Hoffman,
Dave Girouard, Eric Ries, Steve Blank, Jeff Bezos (shareholder letters),
Annie Duke, Marty Cagan, Richard Gabriel, Donald Knuth, Martin Fowler, Dan
McKinley, John Boyd/John Carmack, Startup Genome, and 37signals. Every quote
below was verified against the fetched source text.

## The ten load-bearing principles

**P1. Usefulness is defined by the user, not by the quality of the work.**
An artifact nobody uses is worthless regardless of its rigor. "Products are
not paint. They're not art" (Seibel). There is "just one mistake that kills
startups: not making something users want" (Graham, The 18 Mistakes That
Kill Startups). Before polishing anything, name the user and the decision it
unblocks; if you can't, stop.

**P2. Ship at the point of embarrassment, then iterate.** "If you're not
embarrassed by your first product release, you've released too late"
(Hoffman). Launching a mediocre product as soon as possible beats waiting
(Seibel/Ralston, YC Essential Advice). Slowness in launching is a canonical
startup killer (Graham). Embarrassment is calibration, not failure.

**P3. Take the 90/10 solution, always.** "A 90% solution to a real customer
problem which is available right away, is much better than a 100% solution
that takes ages to build" (Buchheit). "Pick three key attributes or
features, get those things very, very right, and then forget about
everything else" (Buchheit, Great vs Good). Search for the 10%-effort
version before starting the 100% version; the forced cut reveals the
essence.

**P4. Decide fast; match deliberation to reversibility.** "Fast decisions
are far better than slow ones and radically better than no decisions"; "the
vast majority aren't worth more than 10 minutes"; "very few can't be undone"
(Girouard, Speed as a Habit). "Is this going to destroy the company? If not,
let them test it" (Hoffman). Reversible decisions get minutes and a
default-yes to action at 50-70% information.

**P5. Learning rate is the only compounding asset.** "The faster you learn,
the more likely you are to build something that people love before anyone
else" (Seibel). Measure progress in iterations-per-week and
lessons-per-iteration, never in the thoroughness of any single iteration.

**P6. Contact with reality beats analysis.** "There are no facts inside your
building" (Blank). "You only really start learning about your user when you
put a product in front of them" (Seibel). Internal validation - more
analysis, more review, more simulated proof - is procrastination once a
real-world test is available. Positive feedback without shipped usage counts
as zero (Caldwell on tarpit ideas).

**P7. Do things that don't scale.** Recruit users by hand; do the work
manually; narrow the market until you can win it this week (Graham).
Building scalable infrastructure early is deferred-usefulness disguised as
diligence.

**P8. Momentum is existential.** "The prime directive of great execution is
'never lose momentum'" (Altman, Startup Playbook). "I have never, not once,
seen a slow-moving founder be really successful" (Altman). Know if you are
default alive or default dead (Graham). Low burn buys iterations, and
iterations are life.

**P9. Be relentlessly resourceful.** "Relentlessly resourceful" is the
founder job description in two words (Graham). "Blocked" must always be
translated into "here are the two workarounds I tried and the third I am
trying." "Startups rarely die in mid keystroke. So keep typing!" (Graham,
How Not to Die).

**P10. Optimize the loop, not the artifact.** The real product is the
learning loop: team, cadence, decision speed. When tempted to perfect a
single output, instead change the loop - shorter deadline, tighter scope
cut, earlier user contact - so every future output improves. Build, don't
perform building.

## The four-question rigor framework

Asked in order, these decide the rigor budget for any decision or piece of
work.

**Q1. One-way or two-way door? (Bezos, 2015/2016 shareholder letters.)**
Two-way doors (revertible commit, renameable name, redoable draft,
re-runnable analysis) "can and should be made quickly by high judgment
individuals or small groups." One-way doors (irreversible delete, external
send, prod mutation, public commitment, money spent) get "great
deliberation" - the only class deserving heavy proof. Guard both ways:
habitually using the light process on true one-way doors is fatal too.
The skill is classification, not a blanket bias.

**Q2. What does being wrong cost, versus being slow? (Bezos, Fowler, Knuth,
Cagan.)** "If you're good at course correcting, being wrong may be less
costly than you think, whereas being slow is going to be expensive for
sure" (Bezos). For speculative capability, "your odds are at least 2/3"
that it is unnecessary (Fowler, YAGNI). Rigor invested in the noncritical
97% has "a strong negative impact" on everything after it, and intuition
about what is critical "fails" - find the critical 3% by measurement, not
anxiety (Knuth).

**Q3. How much information is actually available, and at what price?
(Bezos, Duke, Blank.)** Act at "somewhere around 70% of the information you
wish you had"; waiting for 90% means "you're probably being slow" (Bezos).
Some information is permanently hidden; past ~70%, further proof buys
feeling, not knowledge (Duke). If the missing 30% lives outside the
building, ship something and ask (Blank).

**Q4. Which option maximizes learning per unit time? (Ries, Boyd, Graham,
Carmack.)** The unit of progress is validated learning (Ries). "Speed of
iteration beats quality of iteration" (Boyd's law). Outcomes come from "the
500 smart decisions" - protect the ability to make many decisions rather
than perfecting any single one (Carmack).

## Calibration table

| Situation | Door | Rigor deserved |
| --- | --- | --- |
| Naming, structure, drafts, internal docs | Two-way | None beyond taste; decide instantly |
| Code with tests, behind review, revertible | Two-way | Light: make it work, verify the changed seam, ship |
| Tool/tech/abstraction choice | Two-way with carry cost | Default boring; novelty only on mission-critical need (McKinley) |
| Speculative "we'll need it later" capability | Don't walk through | Zero. 2/3 odds it is pure waste (Fowler) |
| Scaling/hardening before real load | Premature | Zero until evidence of load. Premature scaling appears in ~70% of startup failures (Startup Genome) |
| Perf/robustness in the measured critical 3% | Varies | Real rigor - after measurement identifies it (Knuth) |
| Irreversible delete, external send, prod data, money | One-way | Full deliberation, consultation, proof (Bezos) |
| Direction choice with zero user contact yet | Compounds | Don't add rigor - add reality contact; smallest testable version out (Blank, Ries) |

## Failure modes this canon exists to catch

1. **Proof-maximizing on two-way doors** - receipts and exhaustive
   verification for decisions that cost less to redo than to prove.
2. **"We followed the process"** - process compliance treated as the
   outcome. "The process is not the thing" (Bezos, 2016).
3. **Resulting-driven ratchets** - one bad outcome after a fast decision
   leading to permanently heavier process. Judge the decision by the
   information available at the time; react to failure patterns, not single
   failures (Duke).
4. **Efficiently executing the irrelevant** - flawless implementation of an
   unvalidated direction. Iridium burned $5.2B executing a stale assumption
   perfectly (Blank). Failed startups write 3.4x more code in discovery
   than successful ones (Startup Genome).
5. **Indigestion** - "more startups die of indigestion than starvation"
   (Packard, via Bryce Roberts). Adding machinery as the default answer is
   what kills.
6. **Perfection before contact** - the 50-80% version that ships wins
   (Gabriel, Worse is Better).
7. **Scope-hold instead of scope-cut** - when over budget, cut scope: "half
   a product, not a half-assed product"; fix time and flex scope
   (37signals, Getting Real).

## Quote bank

- "Make something people want." - Y Combinator motto
- "If you're not embarrassed by your first product release, you've released
  too late." - Reid Hoffman
- "Fast decisions are far better than slow ones and radically better than
  no decisions." - Dave Girouard
- "I have never, not once, seen a slow-moving founder be really
  successful." - Sam Altman
- "The prime directive of great execution is 'never lose momentum'." - Sam
  Altman
- "There are no facts inside your building." - Steve Blank
- "Most decisions should probably be made with somewhere around 70% of the
  information you wish you had. If you wait for 90%, in most cases, you're
  probably being slow." - Jeff Bezos, 2016 shareholder letter
- "If you're good at course correcting, being wrong may be less costly than
  you think, whereas being slow is going to be expensive for sure." - Jeff
  Bezos
- "Premature optimization is the root of all evil (or at least most of it)
  in programming." - Donald Knuth (whose full point: effort in the
  noncritical 97% actively harms; find the critical 3% by measurement)
- "You aren't gonna need it." - Extreme Programming / Martin Fowler
- "Speed of iteration beats quality of iteration." - Boyd's law
- "Pick three key attributes or features, get those things very, very
  right, and then forget about everything else." - Paul Buchheit
- "It's far better to have a hundred people love your product than a
  hundred thousand who kind of like it." - Michael Seibel
- "Write code and talk to users." - Michael Seibel & Geoff Ralston
- "Build stuff and talk to users. And nothing else." - Jessica Livingston
- "Sell shit, make money. One of my mantras is just don't die." - Dalton
  Caldwell
- "Startups rarely die in mid keystroke. So keep typing!" - Paul Graham
- "Do things that don't scale." - Paul Graham

For the full research with per-source principles and URLs, see the repo's
`docs/startup-pragmatism/research/` (build-time input, not required at
runtime).
