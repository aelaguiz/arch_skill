# Plan Interview Skill — Intent And Raw Notes

Date: 2026-08-02. Source: Amir, dictated. This file is the doc pack's anchor:
what the future skill is for, in his words, cleaned up but not reinterpreted.

## The problem

Plan quality today is spotty and proportional to how much effort Amir puts into
the planning conversation. He usually skips the conversations that matter most:
desired user journeys, intended user experience, what testing is needed
(simulator automations vs unit tests vs widget tests — a big deal for psmobile,
but the gap is general). The result: plans that read fine but are underspecified
in exactly the places that later blow up.

Recurring failure classes he named:

1. **Unintended user experience.** The finished plan (and then the built code)
   contains new UX he never meant to introduce. He finds out later.
2. **Scope creep via review waves.** The three cynical reviews propose far more
   work than is in scope; if the plan doesn't say precisely what is in scope,
   the conductor can't push back and the scope grows.
3. **Away-from-keyboard stalls and dumb questions.** Agents stop to ask him
   questions mid-run that a well-written plan would have answered, or ask in
   code-level jargon ("what do you want for C8?", "what should
   `<function he forgot exists>` do?"). He wrote much of this code and is a
   high-end engineer, but he does not carry every identifier in his head.
   Jargon interrogation is obnoxious and useless.
4. **Fuzzy definition of done.** Plans don't say exactly what must be
   accomplished to count as complete, or exactly what testing is required.

## The idea

A skill that **conducts an interview** and produces a doc pack so strong that
any downstream implementation-planning skill produces an A+ plan from it.

Rough shape he described:

1. **Orient.** First just figure out what he's talking about.
2. **Immerse.** Then go read all the code, the GitHub history, the docs — get
   fully up to speed on its own.
3. **Doc pack.** While immersing, write out a doc pack (or one growing doc) of
   reference material it is pulling together.
4. **Interview.** Then interview him — ideally until the work is genuinely
   well defined; realistically until he gets fed up. "Well defined" means more
   context than he gives today: user journeys, UX intent, testing intent,
   model assignments, the works.
5. **Handoff.** The output is incredibly high-quality input for
   `$arch-mini-plan` / `$arch-step` and `$conductor` — designed to compose with
   them but not required to be used with them.

## Interview conduct requirements

- All communication with Amir uses the globally installed `i-have-adhd` skill
  (when installed): action-first, numbered, bounded, no preamble.
- **Never interrogate in jargon.** Do not ask what a specific function, class,
  file, or subsystem identifier should do. Translate every question into
  product/behavior English. If a code-level decision is needed, present it as
  plain-English options with a recommendation.
- The skill should burn its own tokens getting up to speed rather than asking
  him things the repo, git history, or docs can answer.
- **At any point he can sub in another model as him** — a proxy interviewee
  (e.g. a strong model answering on his behalf) so the interview can continue
  without him.

## Question territory the interview must cover (his list, not exhaustive)

- What are we doing?
- Why are we doing it?
- North stars.
- Outcomes we expect.
- Intended user experience interview (journeys; and explicitly: what UX must
  NOT change / no new UX unless named).
- Requirements interview.
- Architecture interview.
- Testing: what proof is required — simulator automations vs unit tests vs
  widget tests, per surface.
- Execution logistics that should be pinned in the plan doc:
  - which model/effort executes (e.g. Codex `gpt-5.6-sol` at `ultra`),
  - which models run the three cynical skill audits (e.g. Terra/"care" xhigh),
  - which model runs the final adversarial review (e.g. Fable xhigh),
  - who does PR authoring + follow-through (e.g. sol ultra),
  - pin a worktree; for psmobile pin a simulator — recorded in the plan doc.

## His current manual recipe (what the skill should capture up front)

Today he builds a plan, then tells `$conductor` roughly:

1. Run it with sol ultra.
2. Pin a worktree now; (psmobile) pin a simulator now; write both into the plan
   document.
3. When you think you're done, run the three cynical reviews (e.g. Terra
   xhigh). "Don't take them at their word — they will produce way more scope
   creep. You have to go back to the plan and ask what is actually in scope.
   You can't let them scope creep."
4. Then have a Fable xhigh agent do an adversarial review.
5. Then have sol ultra run `$pr-authoring` and `$pr-review-followthrough`.

Every one of those is a manual reminder he types each run. A better plan should
carry them so the conductor never has to ask and he never has to remember.

## Calibration addendum (2026-08-02, after reviewing rev 1)

Three corrections from Amir, now binding on the design:

1. **Educate, don't draft.** After the opening ask (plus a couple of
   orienting questions), the skill goes and educates itself — code, history,
   docs, his past asks in similar situations — and builds reference material
   plus at most a blank template. It does NOT build a plan from that first
   sentence: "if it builds the plan based off that first sentence, it's
   going to build in a bunch of shit that I have to unwind."
2. **Real elicitation, not confirmation rituals.** Open questions with
   informed framing ("typically your requirements here are X — what are you
   thinking?", "you usually want a full test grid — want that here?"). His
   thinking first; options/recommendations as fallback. Not "no questions",
   not "two questions", not forever: the discovery process scales with
   complexity, but the must-always-know list always gets a line: what/why,
   success signals, project type, UX delta, requirements, non-goals + scope
   boundary, architecture requirements, test grid + proof, definition of
   done, execution policy, autonomy contract, open decisions/assumptions.
3. **Always ask about visuals for UX work.** Do mocks, target images, or
   reference apps exist? Where? If new UX has no visuals, offer a
   mock-approval gate before implementation.
4. **Two-gate close.** A clean decision table ("is this good?"), then
   "ready for me to run the plan step?" — bare yes runs `$arch-mini-plan`;
   a sentence of steering (full arch-step, adversarial with a named model)
   runs exactly that.
5. **No codified language, including the skill's own.** Requirements are
   said in words and referred to by name — never R1/Q3-style shorthand.
6. **The test grid is approved in the interview, up front.** Built on the
   spot, approved or edited right there; it is part of the approval, never
   "coming later." Nothing in the decision table says "later" except items
   Amir explicitly parked.
7. **User journey map required wherever the work touches a journey.** In a
   mature product (psmobile) mostly confirming the existing journey
   unchanged or marking the tweak; bigger features map every journey they
   create, sometimes several.
8. **The interview is a loop, not a line.** Not transactional: Amir's
   answers are investigation triggers, not entries to transcribe. He might
   say no more than "build this." The skill goes and figures out what the
   words mean in this codebase, writes what it learned into the documents,
   and comes back with questions it couldn't have known to ask before.
   Education recurs mid-interview, multiple cycles as needed; the
   must-always-know list still bounds what ends up written, and each cycle
   deepens an area then advances.

## Success bar for the skill

- When he is away from the keyboard, the plan carries enough high-level
  context — north stars, first-principles intent — that executing agents can
  make solid decisions alone instead of stopping to ask.
- The plan states exactly what must be accomplished to be considered complete,
  and exactly what testing is required.
- Nothing user-visible changes unless the plan names it.
- Scope boundary explicit enough that cynical-review findings can be triaged
  against it mechanically ("in scope / out of scope") by the conductor.
