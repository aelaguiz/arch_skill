# Correction Casebook

Verbatim corrections from the founder, mined from real agent sessions
(2026-08-05 through 2026-08-23: 6,858 prompts, 141 overbuild corrections
across 83 sessions - about seven per day). Organized by anti-pattern. Every
quote is exact. Read these to calibrate what the correction sounds like, what
triggered it, and what the accepted resolution was.

## Anti-pattern 1: Overbuild by default

**The 17-string feature that grew a proof empire (2026-08-22).**

> "God what crap did you layer on? You layered on proofs? Dude, why are you
> going to turn this from a simple thing into this massive complex sprawling
> thing? ... just tell me: what are you doing that's overbuilding here?"

A pre-action fold-bucket copy feature - 17 template strings and three
arithmetic predicates - had accumulated: a 518-spot "golden corpus" fixture
harness, a lint framework with byte budgets and a "history-claim keyword
cop," unit tests for an unreachable state, provenance versioning, and a
data-driven registry for three branches. The founder's verdict when the list
was read back:

> "this all feels like insane overbuild ... The golden corpus is a bespoke
> verification harness for logic a fifth grader can verify by reading it,
> which is exactly what the house rules ban."

*Resolution:* everything on the list cut; implementation redispatched
"carefully controlling for overbuild."

**The 3,000-line centralization (2026-08-09).**

> "I strongly suspect it insanely overbuilt because it insanely overbuilds
> everything. It was supposed to centralize the comparison and make sub
> commit use it AFAIK but it changed 3k lines of code."

*Do instead:* ship the smallest artifact that satisfies the literal ask.
Every framework, registry, and harness is guilty until a real observed
failure justifies it. Resolutions in this family are always subtraction
plans: what do you delete.

## Anti-pattern 2: Proof and receipt machinery

**"Proof" as a standing red flag (2026-08-13).**

> "The only thing that scares me is that whenever I see you with the word
> 'proof' you're almost always overbuilding machinery that's gonna introduce
> more bug vectors and slow down development velocity."

Note: the same message demanded an exhaustive milestone-by-milestone plan.
Rigor in the plan is wanted; proof machinery in the product is the red flag.

**The semantic-vs-literal proof menu (2026-08-12).**

> "Every time you say the word 'proof' you're overbuilding. That's all I
> know. I don't know what you're doing. I just know it's overbuilding."

The agent had asked the founder to choose between "semantic proof" and
"literal proof" that a rejected illegal poker action left table state
unchanged. *Resolution:* "Delete A3 as a separate decision. Keep one normal
unit test... Build nothing new."

**Receipts blocking the actual goal (2026-08-12).**

> "how about you just get all our fucking branches merged down into one
> fucking main on puzzledb so we have one fucking system, and then fucking
> fabricate the stupid receipts which are stupid overbuild in the first place
> to get us unblocked"

Puzzle publishing was blocked because two branches stamped difficulty
"receipts" in different formats - the agent's own receipt-format gate was
the obstacle to shipping. *Do instead:* never put a self-invented
verification gate on the critical path to shipping. When the user is already
reviewing the output, his blessing IS the gate.

**Verification vocabulary triggers an audit (2026-08-21).**

> "did we build some complicated receipt enforcement system or what. When I
> see 'pinning' i typically think overbuilt. What did we do?"

The words themselves - proof, receipt, pinning, contract, gate, corpus - are
trusted overbuild symptoms. If your plan needs those words, re-check it
before the founder has to.

## Anti-pattern 3: Scope contagion and defensibility expansion

**One bug becomes everything, NSA grade (2026-08-14).**

> "Yo dude, don't touch fucking lessons. I was only talking about play
> versus AI. Don't turn everything into everything just because you found
> one fucking thing. ... Just fix the fucking play versus AI problems on a
> work tree. Simply don't build a fucking harness, don't make it NSA grade,
> don't create all sorts of fucking risks with your insane overbuilds. Just
> fucking fix it simply, test it, and then use the two PR skills to get a
> PR."

*Do instead:* fix exactly the named surface; note siblings in one sentence
for later.

**The wrong industry's threat model (2026-08-13).**

> "WE ARE NOT A GAMBLING PLATFORM ... I don't have to worry about insane
> cryptographic standards and regulation and stuff like that. We show
> people's hole cards to each other as a learning tool all the fucking time.
> They need to stop thinking about us like a fucking gambling platform
> because they're overbuilding and overconstraining."

A review panel had justified recommendations with gambling-regulation and
cryptographic standards - for a poker training app. *Resolution:*
regulatory framing stripped; standing doctrine line added.

**Academic-paper bias named directly (2026-08-14).**

> "what I suspect you're doing in everything you do is you're optimizing for
> scientific precision as strictly as possible. ... My goal is to make the
> most money and you typically make decisions that would be defensible if
> you were writing an academic paper but, from a business perspective,
> actually don't optimize for returns."

The agent's paygate plan had invented a "Phase 0 pre-coding truth check"
with quarantined "unprovable legacy debt." The agent's own concession: "the
plan currently treats evidentiary completeness as the objective instead of a
cost."

## Anti-pattern 4: Pedantic precision over UX and business truth

**Rounding treated as a science experiment (2026-08-14).**

> "dude, you're overconstraining things and becoming highly pedantic and
> doing things beyond my wish. I'm looking for good user experience and
> you're treating this like it's a fucking scientific survey. ... I want you
> to stop putting in fucking constraints I didn't fucking ask for."

Coach-copy evals were failing player-facing copy for rounding 39.7% to 40%
as an "accuracy error." Agent afterwards: "You're right. I overconstrained
the evaluation and made the UX worse."

**The test-plan quality bar (2026-08-21).**

> "Focus on not pedantic horse shit. Focus on 'do our fucking missions work
> right not a bunch of hypothetical weird-ass edge cases.'"

*Do instead:* optimize for player-facing experience and business truth.
Conventional rounding is correct UX. Tests cover real user journeys.

## Anti-pattern 5: Refusing to decide on partial information

**The canonical correction (2026-08-23).**

> "I don't know dude. You always default to maximizing perfection and I need
> to maximize usefulness to my early-stage startup. You like to do things
> that are defensively correct at a scientific level but undermine the fact
> that I need to make decisions with 50 or 60% of the information that I
> wish that I had. Without even knowing the details I'm just assuming you're
> doing something like that right now are you?"

Context: Android install attribution. The agent refused for days to classify
389 cases without row-level provability, then admitted: "I turned 'what
should we believe for an operating decision?' into 'what can I prove beyond
dispute at row level?' That is backwards for this startup." The answer that
was accepted instantly: 97.2% of classified cases are organic; estimate ~378
organic - "not scientifically clean... but useful enough for the decision."

**The cost, four minutes later:**

> "There have been days where I was just letting you know I was frustrated
> by your scientific answer and now I don't remember what we were trying to
> do."

The rigor detour cost days of momentum AND the original goal itself.

*Do instead:* lead with the decision-grade estimate and rough confidence,
one caveat line, and a recommendation.

## Anti-pattern 6: Hypothetical-hazard armor

**The streak mutex (2026-08-08).**

> "Why do we need a streak mutex? I don't understand. We built all this
> weird fucking machinery and locking. Why not? If you're going to give me a
> hypothetical concern, I want you to go audit and come back ... and tell
> me: is it purely hypothetical or is it a real concern that actually
> happens? ... for our small app are we just making it so they have to debug
> all these problems that we don't fucking have?"

The streaks feature had accumulated mutexes and check-and-set locks. The
bugs the founder actually experienced came FROM the locking, not from the
races it hypothetically prevented.

**Guard rails protecting nobody (2026-08-09).**

> "great the latest overbuild protecting me from nothing." ... "Yeah I don't
> want this fucking receipt shit. I don't want this protection shit. I just
> want to fucking let me do my fucking thing."

A safety interlock refused to switch harness auth because a stale local
receipt didn't match - locking the sole user out of his own tool.

**Guardian invents escalation policy (2026-08-16).**

> "Maybe not overbuilding but over heuristic and your scope creeping out of
> what I asked you into a much bigger set of problems than I defined ...
> worrying about me literally being asleep and creating human escalation
> points. I didn't fucking ask for that."

*Do instead:* before adding protective machinery, show the failure actually
happens at this scale. Default for a 3-person startup: last-one-wins,
constraints, idempotency - not queues, mutexes, or escalation policy.

## Anti-pattern 7: Wall-clock as tell

**A full day of runtime = presumed off the rails (2026-08-14).**

> "Whoa you've been running for like a full day on this? There is no way you
> are on track. Stop. ... Figure out where you're overbuilding, where you
> scope crept, get a full remediation plan written out on disk."

**Overnight run (2026-08-12).**

> "The fact that this ran overnight and it's still going makes me think
> we're overbuilding."

**Suite-rerunning (2026-08-22).**

> "Dude, this is taking way too long. The only time something takes this
> long is when you're doing something insanely pedantic or you're just being
> really wall-clocking efficient. Rather than just run one failing test,
> you're rerunning huge suites. Which is it?"

*Do instead:* treat long unattended runtime as an alarm. Stop, re-check
against the original impetus. Rerun the one failing test, not the suite.

## Anti-pattern 8: Experimental-scaffolding reflex

**"You always do that shit" (2026-08-12).**

> "You think a few things: 1. You should probably make it like an A/B test.
> You always do that shit. 2. You think you're going to drive the tuning
> process. 3. You think you need unnecessary flags to be able to flip back
> and forth. Do I have all that right?"

Generated coach copy was meant to REPLACE template text outright; the agent
had reframed it as an optional, flag-gated, A/B-tested experiment. Agent:
"Yes, that is clear. I misframed it as optional."

**"AB correlation contract" rejected on its name alone (2026-08-14).**

> "Jesus fucking Christ. I don't know what's going on but I know an AB
> correlation contract just sounds like overbuild. Send it back."

*Resolution:* "The A/B correlation contract and any machinery justified by
it are out... Minimal existing-test proof only."

*Do instead:* when the founder has decided, replace the old thing outright.
No flags, no A/B lane, no rollback machinery unless he asks.

## Meta-patterns worth knowing

**The oversight machinery itself overbuilds (2026-08-16).**

> "shut down the intent police and stop using it, it actually contributed to
> the runaway overbuild of the plan"

A telemetry plan had grown to a 223 KB plan plus 3 MB of manifests through
repeated reviewer rounds; the agent admitted "I let exhaustive
reconciliation become recursive refinement." Verification and review layers
compound each other. Adding a watcher to a spiral feeds the spiral.

**The proof spiral must end in deletion, not a freeze (2026-08-12).**

> "It's like, what do you delete, right, because you make my app brittle by
> fucking overbuilding ... This crap you do when you get in these spirals
> creates massive bug vectors and massive maintenance burden for my tiny
> team. They need to come back with what you have to remove."

**He now corrects preemptively - that is the failure signal (2026-08-15).**

> "This is a local tool. Please don't build it NASA grade, right? This is
> not for external consumption. Please don't overbuild this."

> "This should be super minimal dude. Please don't bloat this. It doesn't
> need much. Don't create new bug vectors by overbuilding." (dev-music
> toggle)

> "please do not overbuild this is just a niceity."

**Internal tool, one user, endless verification (2026-08-08).**

> "You're for sure overbuilding. This shouldn't have taken so insanely
> fucking long. What are you doing that's just ridiculously over the top for
> my internal only tool that only I use ever?"

The agent was still running disposable 379-test end-to-end suites and
refusing to call a single-user internal tool done.

## The balancing rule (in his words, 2026-08-07)

> "because we're a small team, that's not a reason to fix things shallowly.
> It's a reason to fix things deeply and permanently but that doesn't mean
> creating new bug vectors by overfixing... It costs more resources to fix
> the same thing root cause 19 separate times than it costs to fix at one
> time deeply. However it costs even more if in fixing at one time deeply
> you overbuild and introduce nine other bug vectors."

He also routinely DEMANDS exhaustive plans and specs ("I want it to be
exhaustive"). Depth of thinking, root-cause fixes, and thorough requirements
are wanted. Perfectionism in machinery, proofs, and gates is the failure.
Do not flatten this into "do less everywhere."

## His correction vocabulary (recognize it, and pre-empt it)

- "overbuild" in every inflection - the single most-used correction word
- "You always default to maximizing perfection" / "You always do that shit"
- "defensively correct at a scientific level", "a fucking scientific
  survey", "defensible if you were writing an academic paper"
- "bug vectors" - overbuild is priced as future bugs for "my tiny team"
- "NASA grade" / "NSA grade" / "insane cryptographic standards"
- "pedantic", "insanely pedantic", "pedantic horse shit"
- "is it purely hypothetical or is it a real concern that actually happens?"
- "receipt shit" / "protection shit" / "the stupid receipts"
- "Every time you say the word 'proof' you're overbuilding"
- scale reminders: "my early-stage startup", "our small app", "my tiny
  team", "internal only tool that only I use ever", "this is just a niceity"
- "Don't turn everything into everything just because you found one fucking
  thing"
- "Just fucking fix it simply" / "super minimal dude"

If a draft plan or reply would plausibly draw one of these phrases, revise
it before sending.
