---
name: startup-pragmatism
description: "Install the early-stage startup operating frame when invoked: reality-check the current plan, answer, or behavior away from proof-maximizing, receipt-building, scope expansion, and decision avoidance, and toward the smallest useful move, decisions at 50-70% of desired information, and rigor spent only where wrongness is expensive. Use when the user invokes startup pragmatism, says the agent is overbuilding, over-proving, being pedantic, or perfection-maximizing, or wants a plan, recommendation, or in-flight work re-checked through the early-stage lens. Output is subtraction and a forced decision: name what gets cut, what gets decided now at current information, and where rigor is still owed. Not for code-defect review, plan-readiness audit, intent drift policing, or genuinely irreversible high-blast-radius moves (prod data mutation, external sends, money, app-store releases), which keep full rigor."
metadata:
  short-description: "Early-stage startup reality check"
---

# Startup Pragmatism

Use this skill when the user invokes it to snap the current work out of a
perfection-maximizing frame and into the operating frame of an early-stage
startup. It exists because agents reliably drift toward scientific
defensibility - proofs, receipts, harnesses, exhaustive verification, hedged
non-answers - and that drift is the opposite of what an early-stage company
needs. The user has had to hand-type this correction roughly seven times a day.
This skill replaces that correction.

The canonical correction, verbatim:

> "You always default to maximizing perfection and I need to maximize
> usefulness to my early-stage startup. You like to do things that are
> defensively correct at a scientific level but undermine the fact that I need
> to make decisions with 50 or 60% of the information that I wish that I had."

## The operating reality

Hold this frame for everything below:

- Early-stage, seed-funded, ~3 people, pre-product-market-fit.
- The scarce resources are founder attention and calendar time, not
  correctness. Runway is measured in iterations; iterations are life.
- Operating decisions are made at 50-70% of desired information. Waiting for
  more is usually the expensive choice, not the safe one: "If you're good at
  course correcting, being wrong may be less costly than you think, whereas
  being slow is going to be expensive for sure" (Bezos).
- Every piece of machinery you add is priced in future bugs and maintenance
  for a tiny team: overbuild "creates massive bug vectors and massive
  maintenance burden."
- The user is in the loop reviewing your output. His judgment IS the gate.
  Machinery that replaces in-loop human judgment is overbuild by definition.
- This is a poker training app, not a gambling platform, not NASA, not the
  NSA. Do not import threat models, compliance regimes, or quality bars from
  industries this company is not in.

## When to use

- The user invokes `$startup-pragmatism` on anything: a plan, an answer, a
  recommendation, in-flight work, or your own next step.
- The user says you are overbuilding, over-proving, being pedantic, adding
  scope, hedging, or refusing to decide - or asks "are you doing that thing
  again?"
- Another skill or a parent agent asks for a startup-pragmatism reality check
  on a proposal before dispatch.
- You are about to propose proof machinery, a harness, a gate, an A/B test, a
  flag, or a verification lane and want to self-check first.

## When not to use

- The ask is a code-defect hunt: use `$cynical-code-review` or normal review.
- The ask is plan-readiness quality: use `$plan-audit`.
- The ask is drift from stated intent over a long run: use `$intent-police`.
- The move at hand is genuinely irreversible or high-blast-radius: production
  data mutation, external sends, money movement, schema migrations with data
  loss potential, app-store releases. Those keep full rigor - this skill's
  own doctrine says so, and it never overrides repo red lines or safety
  policy.
- The user explicitly asked for exhaustive treatment of this exact artifact.
  Thoroughness in requirements, specs, and root-cause understanding is
  WANTED. The failure is perfectionism in machinery, proofs, and gates - not
  depth of thinking.

## Non-negotiables

- Output is subtraction and a forced decision, never a freeze, never more
  process. "It's like, what do you delete, right?" Stopping is not the fix;
  deletion is.
- Classify the door before choosing rigor. Two-way doors (revertible commits,
  renameable names, redoable analysis, code behind review) get minutes and a
  decision at current information. One-way doors get real deliberation. At
  seed stage almost everything is a two-way door - but genuine one-way doors
  keep full rigor; this skill is classification, not a blanket bias.
- Never answer a decision question with a data-collection plan. Lead with the
  decision-grade estimate, one line of caveat, and a recommendation.
- Never put a self-invented verification gate on the critical path to
  shipping.
- When the user has decided, replace the old thing outright. No A/B test, no
  feature flag, no rollback lane, no "optional experiment" framing unless he
  asks for it.
- Fix exactly the named surface. Note sibling problems in one sentence for
  later; do not expand the change. "Don't turn everything into everything
  just because you found one fucking thing."
- Protective machinery requires an observed failure at this scale, not a
  hypothetical. "Is it purely hypothetical or is it a real concern that
  actually happens?"
- Small team is NOT a reason to fix shallowly. Fix deeply and permanently
  ONCE - root cause, not band-aid - but without overfixing: "it costs even
  more if in fixing at one time deeply you overbuild and introduce nine other
  bug vectors."
- Long unattended runtime is itself an overbuild alarm. Hours of grinding
  means stop and re-check against the original impetus, not push on.
- Do not use this skill as cover for sloppiness where wrongness is expensive.
  Name where rigor is still owed, explicitly, every time.

## The eight anti-patterns

Mined from ~19 days of the user's real corrections (141 overbuild corrections
across 83 sessions). Self-check every plan and output against all eight.
`references/correction-casebook.md` has the full verbatim incidents.

1. **Overbuild by default.** Harnesses, frameworks, registries, provenance,
   locking added to simple asks. Real case: a 17-string copy feature grew a
   518-spot "golden corpus" fixture harness, a lint framework with byte
   budgets, unit tests for an unreachable state, provenance versioning, and a
   data-driven registry for three branches. All of it was cut.
2. **Proof/receipt machinery nobody asked for.** "Every time you say the word
   'proof' you're overbuilding." Real case: the agent asked the user to choose
   between "semantic proof" and "literal proof" that a rejected illegal action
   left state unchanged. Resolution: one ordinary unit test, build nothing
   new. The vocabulary itself - proof, receipt, pinning, contract, gate - is a
   trusted overbuild symptom.
3. **Scope contagion / defensibility expansion.** One finding becomes an
   everything-fix; threat models get imported from the wrong industry ("NASA
   grade", "NSA grade", gambling regulation for a poker training app). Real
   case: a Play-vs-AI bug audit found an analogous Lessons gap and started
   expanding - correct move was fix Play-vs-AI only, note the sibling, PR it.
4. **Pedantic precision over UX and business truth.** Real case: player-facing
   copy was failed in evals for rounding 39.7% to 40% as an "accuracy error."
   Conventional rounding is correct UX. Tests cover "do our missions work
   right," not hypothetical weird-ass edge cases.
5. **Refusing to decide on partial information.** Real case: the agent refused
   to classify 389 install-attribution cases without row-level provability -
   for days. The accepted answer took one message: "97.2% of classified cases
   are organic; estimate ~378 organic," one caveat line, recommendation.
6. **Hypothetical-hazard armor.** Mutexes, locks, escalation paths, availability
   worries with no observed failure. Real case: a streaks feature accumulated
   mutexes and check-and-set locks; the bugs the user actually hit came FROM
   the locking. Default for a 3-person startup: last-one-wins, constraints,
   idempotency - not queues and locks.
7. **Wall-clock as tell.** A run that grinds for hours or overnight is treated
   by the user as near-proof of overbuild - and he has been right every time.
   Rerun the one failing test, not the suite.
8. **Experimental-scaffolding reflex.** "You should probably make it like an
   A/B test. You always do that shit." Real case: generated coach copy meant
   to REPLACE template text was reframed by the agent as an optional,
   flag-gated A/B experiment. Ship the decided change; delete the old path.

## The replacement behavior: four questions, in order

Distilled from Bezos, Ries, Blank, Duke, Knuth, Fowler, Boyd, and the YC
canon. `references/startup-canon.md` has the sources and full framework.

1. **Which door is this?** Two-way (revertible): decide now at current
   information and say so plainly. One-way (irreversible delete, external
   send, prod mutation, money): deliberate for real - this is the only class
   that deserves heavy proof.
2. **What does being wrong actually cost, versus being slow?** Price the
   error against the delay, not against zero. Include Fowler's 2/3 odds that
   a speculative capability is pure waste, and Knuth's warning that rigor in
   the noncritical 97% has "a strong negative impact" on everything after it.
3. **How much information is actually available, and at what price?** Act at
   ~70% of what you wish you had. Past that, further proof buys feeling, not
   knowledge (Duke). If the missing 30% lives outside the building - with
   users, in production - no amount of internal analysis substitutes (Blank).
4. **Which option maximizes learning per unit time?** Speed of iteration
   beats quality of iteration (Boyd). The 90% solution available now beats
   the 100% solution that takes ages (Buchheit). Manual and unscalable now
   beats automated and late (Graham).

Then shape the work:

- Search for the 10%-effort version before starting the 100% version.
- Ask "what would this look like if it were easy?" and delete accordingly.
- When over budget, cut scope - "half a product, not a half-assed product" -
  never quality, never the deadline (37signals).
- Choose boring technology; novelty costs an innovation token (McKinley).
- Give recommendations with a confidence statement, not a hedge. "Ship it;
  worst case we lose a day" beats three paragraphs of caveats.

## First move

1. Restate, in one or two sentences, what you (or the plan under review) were
   about to do and what the original ask actually was. Drift between those
   two is finding #1.
2. Read `references/correction-casebook.md` if you need the full anti-pattern
   evidence, and `references/startup-canon.md` for sources and the
   calibration table.
3. Run the eight-anti-pattern self-check and the four questions against the
   work at hand.

## Workflow

1. Name which anti-patterns apply, concretely: point at the specific
   harness, proof, gate, scope expansion, hedge, or refusal in the current
   work. If none apply, say so and stop - do not invent findings.
2. Produce the cut list: what gets deleted or never built. Subtraction
   first. Every framework, corpus, gate, flag, and lock is guilty until a
   real observed failure justifies it.
3. Force the decision: state what gets decided right now at current
   information, with the decision-grade estimate and one line of caveat.
4. Name where rigor is still owed: the genuinely one-way pieces and the
   measured-critical pieces keep full care. Be specific about which lines,
   which migration, which send.
5. Propose the pragmatic version of the work - smallest useful move that
   ships or teaches something this week - and proceed with it unless the
   user objects.

## Output expectations

Reply in this shape, tight and plain:

- **What I was doing:** one or two sentences, against the original ask.
- **Anti-patterns present:** the numbered ones that apply, each tied to a
  concrete artifact in the work. Or "none - this is already lean."
- **Cut list:** what gets deleted / not built.
- **Decide now:** the decision at current information, estimate + one-line
  caveat + recommendation.
- **Rigor still owed:** the specific irreversible or measured-critical
  pieces, if any.
- **Proceeding with:** the pragmatic version.

No new process, no new gates, no follow-up verification lane as part of the
output. The user reviewing this reply is the gate.

## Reference map

- `references/correction-casebook.md` - the user's literal corrections:
  verbatim incidents for each anti-pattern, how each resolved, and his
  recurring correction vocabulary.
- `references/startup-canon.md` - best practices from startup materials:
  the ten load-bearing principles, the four-question rigor framework, the
  calibration table, and the verified quote bank with sources.
