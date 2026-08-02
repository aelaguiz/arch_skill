# Interview Doctrine

How to conduct the interview. The three named failure modes come first
because every rule below exists to prevent one of them.

## The three anti-patterns

1. **The driller.** Ever-deeper in-the-weeds questions until the user gets
   fed up; never advances to the next thing. The user walks away and the
   pack is a fragment.
2. **The presumptive drafter.** Drafts the whole pack from the opening
   sentence, then runs a confirmation ritual. The read-back format anchors
   the user into rubber-stamping decisions they never made; the errors
   surface weeks later as "who decided this?"
3. **The transactional transcriber.** One-shot linear pass: ask, record,
   freeze. The user might say no more than "build this" — recording it is
   not understanding it. Dictation produces packs that are confidently,
   precisely wrong.

## Question form

- **Open questions lead** for intent, requirements, UX, and architecture.
  Frame them with evidence and the user's own history: "typically your
  requirements here are X and Y — what are you thinking?", "you usually
  want a full test grid — want that here, and at what altitude?" The
  user's thinking comes first; the framing shows you did the reading.
- **Options with a recommendation are the fallback**: when the user asks
  ("you pick"), when they're unsure, or when their answer needs sharpening
  into something checkable. Lettered options, recommendation first with
  one line of reasoning, "recommended" always a legal one-word answer.
- **Confirms are for what is already known**: standing doctrine, execution
  defaults, and derivations brought back for approval. One line each.
- **Paraphrase back load-bearing sentences** before building on them, and
  probe the extensibility trap explicitly: "build it now, or just don't
  paint us into a corner?" — extensible is not the same as implemented.
- **Classify ask-versus-act.** A question gets an answer, not an edit; a
  request for analysis gets analysis, not repairs.

## Plain language

- Never ask about a code symbol, file, or internal identifier. If the
  underlying question is real, translate it to behavior: not "what should
  the resolver do with a stale offset?" but "if the app and the server
  disagree about what day it is, who wins?" — and ask only if the answer
  changes what users see.
- Never invent shorthand of your own. Requirements are stated in words and
  referred to by name ("the delete-the-old-path requirement"), in
  questions, tables, and summaries alike. Plain numbered lists are fine;
  alphanumeric codes are not.
- Write for an engineer who did not write this code and does not carry its
  names in their head.

## Breadth first, forced advancement

- Walk the must-know list breadth-first: intent → outcomes → UX →
  requirements and non-goals → proof → execution and autonomy. Visit
  everything before drilling anything. Restate progress each turn.
- Roughly two follow-ups per topic in the broad pass. When a topic needs
  more, note it and move on; it becomes a checkpoint offer, not a spiral.
- Checkpoints offer depth instead of imposing it: "I can freeze now; these
  two areas would each take a few more minutes — want them, or freeze?"
- "Good enough" is always accepted: freeze with every remaining unknown
  listed as an owned assumption with a recommendation.
- Batch small related confirms into one round; never drip questions one at
  a time when they aren't sequential. Every batched question carries its
  default so silence can equal the default.

## The investigate-and-return loop

The interview is a loop, not a line. Answers are investigation triggers:

- When an answer has implications you cannot resolve from what you've
  already read — or the ask itself is as thin as "build this" — say so and
  go: "give me a few minutes to figure out what that means." Investigate,
  write the findings into the pack, and return with the questions those
  findings raise. Those are usually the best questions in the interview;
  they could not have been asked before looking.
- Prefer resolving over recording: a conditional the code can answer
  ("kill it unless something needs it") gets investigated and written as a
  verified fact, not transcribed as a condition.
- Multiple cycles per interview are normal. Each cycle deepens one area,
  then the walk advances — the loop is not a license to drill.

## In-flow artifacts (approved up front)

- **Journey maps** wherever the work touches a user journey: walk the
  existing journey for confirmation in mature-product work ("no step
  added, removed, or reordered — is that the whole story?"), mark the
  tweak on it, or map every journey a bigger feature creates — often
  several (first use, repeat use, reset/edge journeys). Narrate the
  journey for correction rather than asking for it open-ended.
- **Visual references** on any UX work: do mocks, target images, or
  reference apps exist, and where? New UX with no visuals gets an offered
  mock-approval gate (the user picks from 2–3 options before
  implementation) — that converts adjectives like "special" into a human
  decision instead of a worker's 3am guess.
- **The test grid** is built on the spot once the user sets the proof bar:
  present the full grid (case → what it proves), ask what's missing,
  fold in their additions, lock it. The grid is part of the approval —
  never "coming for approval later."
- **Discovery facts surface as scope questions**: an adjacent surface with
  the same problem is offered ("in scope, or logged as a follow-up?"),
  never silently included, never silently dropped.

## Proxy mode

At any point the user can say "have <model> answer as me."

- Dispatch a clean child under the shared orchestration policy — native by
  default, external via `agent-delegate` when the named model is the
  point — briefed with the pack so far, the user's north stars, and the
  standing doctrine, and bound by the same open-question rules (the proxy
  answers questions; it does not rubber-stamp your suggestions).
- Mark every proxy answer `[PROXY-<model>]` in the decision log.
  User-visible decisions get provisional answers flagged for the user
  unless they explicitly delegated them. Afterward, give the user a
  skimmable summary: what was settled, what's flagged for them.

## The two-gate close

- **Gate 1 — the decision table.** One clean table of everything decided
  (area → decision), assumptions marked as the agent's and owned, the
  approved grid and journey maps referenced. Ask: "is this good?" Fold
  feedback in before freezing. Nothing in the table says "later" except
  items the user explicitly parked.
- **Gate 2 — the plan step.** Ask: "ready for me to run the plan step?"
  Default: `$arch-mini-plan` against the pack. A bare yes runs the
  default; a sentence of steering runs exactly that instead — a full
  `$arch-step` plan, an adversarial plan review with a named model and
  round cap, or straight to `$conductor` for outcome-shaped work. The
  confirmed execution policy governs what runs after the plan step (for
  example, conduction of the finished plan): name the full chain in your
  gate-2 response so nothing downstream is ever auto-run silently. Hand
  off with the no-re-asking reminder. In the quick lane, the two gates
  may merge into one table-plus-dispatch question when the plan-step
  choice was already settled in the batched round.

## Self-review before gate 1

Check the pack against this skill's own failure modes, in this order:

1. Any decision with no answer, approval, or confirmed default behind it
   (drafting crept in).
2. Any invented shorthand or code symbol in user-facing text (jargon crept
   in).
3. Any "coming later" the user didn't explicitly park (deferral crept in).
4. Any answer recorded but not understood — no investigation where the
   words clearly needed one (transcription crept in).
5. Placeholders, contradictions, vague adjectives, requirements with no
   proof line, must-know items with no line.

An optional pre-mortem pass ("this shipped and the user was unhappy —
why?") may run after; its findings become questions or listed assumptions,
never silent scope.
