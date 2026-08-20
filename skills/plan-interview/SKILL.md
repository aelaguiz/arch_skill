---
name: plan-interview
description: "Conduct an evidence-grounded intent interview that turns a described outcome — even three words like 'build this' — into an approved Intent Pack: north star, user journey maps, UX delta with visual references, plain-language numbered requirements, non-goals, architecture constraints, an in-interview-approved test grid, definition of done, execution policy, and autonomy contract, closed by a decision table and a steerable plan-step gate defaulting to `arch-mini-plan`. Educates itself on code, docs, git history, and the user's past asks first — facts and a blank template, never a pre-drafted plan — then interviews breadth-first in plain non-jargon English with investigate-and-return cycles, with a proxy model able to answer as the user. Use when the user wants a planning interview, an intent pack, or intent captured before planning. Not for writing the implementation plan (arch-mini-plan/arch-step), auditing a plan (plan-audit), executing one (conductor), or read-only opinions (fresh-consult)."
metadata:
  short-description: "Interview-driven intent capture producing an approved Intent Pack"
---

# Plan Interview

Use this skill when the user wants the front of the pipeline done right: an
interview that converts a described outcome into an Intent Pack so precise
that downstream planning and execution never stop to ask a question the pack
already answers, and nothing user-visible changes unless the pack names it.

The interview is a loop, not a line. The user's answers are investigation
triggers, not entries to transcribe: the skill goes and figures out what the
words mean in this codebase, writes what it learned into the pack, and comes
back with questions it could not have known to ask before looking.

## When to use

- The user describes an outcome and wants it properly captured before
  planning: "interview me about this", "build the intent pack", "let's spec
  this out", or just "build this" plus a pointer.
- Plan quality has been spotty and the user wants intent, requirements,
  user experience, testing, and execution logistics extracted up front.
- A conductor-sized effort needs an approved scope boundary, journey maps, an
  approved test grid, and a definition of done before any plan is written.

## When not to use

- The diff could be described in one sentence — just do the work.
- The user wants the implementation plan written: `arch-mini-plan` or
  `arch-step` (the pack is their input, not their replacement).
- The user wants an existing plan audited (`plan-audit`), a plan executed
  (`conductor`), or a read-only second opinion (`fresh-consult`).
- The artifact would duplicate a plan that already exists — this skill
  captures intent before planning, it does not re-plan.

## Non-negotiables

- **The interview runs in the foreground conversation.** The user answers
  in this thread, so the interviewer must be this thread: never delegate
  the interview itself to a background agent, subagent, or external
  worker. If this skill finds itself running in a background or child
  context where the user cannot reply directly, stop and return control so
  the main conversation runs it. Children are for education research and
  the explicitly requested proxy interviewee only; they report to the
  parent, and the parent asks the questions.
- **Educate, don't draft.** After the opening ask and at most 1–3 orienting
  questions, education produces facts, reference material, and a blank
  template — zero decisions. Never pre-fill the pack from the opening
  sentence: a drafted pack is a pile of decisions the user never made,
  formatted to be rubber-stamped.
- **Elicit, don't confirm.** Open questions first, framed with evidence and
  the user's own past asks ("typically your requirements here are X — what
  are you thinking?"). Options with a recommendation are the fallback —
  when the user asks, is unsure, or an answer needs sharpening — never the
  lead for intent, requirements, UX, or architecture. Standing doctrine and
  execution policy are one-line confirms.
- **Plain English only.** Never ask about code symbols, file names, or
  internal identifiers, and never invent shorthand of your own: requirements
  are stated in words and referred to by name afterward, never as
  R1/Q3-style codes. Recognition test: could someone who never read this
  code answer the question? If an always-on communication-style skill is
  installed (for example `i-have-adhd`), its rules govern every
  user-facing message.
- **The loop is structural.** "Give me a few minutes to figure out what
  that means" is a first-class move at any point, multiple times per
  interview. Each trip writes findings into the pack and returns with the
  questions those findings raise. Cycles deepen one area, then the walk
  advances.
- **Breadth before depth, always advancing.** Walk the must-always-know
  list breadth-first; roughly two follow-ups per topic in the broad pass;
  checkpoints offer depth ("sign off now, or take a few more minutes on
  these areas?") instead of imposing it. "Good enough" is always accepted
  and produces the pack with assumptions listed and owned. Restate
  progress each turn.
- **Everything approved up front.** Journey maps wherever a journey is
  touched, visual references asked for on any UX work, and the full test
  grid built and approved inside the interview. Nothing in the close says
  "coming later" except items the user explicitly parked.
- **Discovery raises questions, never scope.** An adjacent surface with the
  same problem is a scope question for the user, not included work.
- **The pack is not a plan.** It records intent, requirements, boundaries,
  and proof obligations. Target architecture belongs to the planning skill
  downstream; architecture *requirements* (constraints) belong here.
- Apply `../_shared/agent-orchestration-policy.md` whenever education
  researchers or a proxy interviewee are dispatched, and apply
  `$prompt-authoring` to each populated child brief.
- Read `references/standing-doctrine.md` and bake its core requirements and
  execution defaults into every pack; ask only about deviations.

## First move

1. Read `references/must-know-list.md` — the interview's backbone.
2. Read `references/intent-pack-contract.md` and
   `references/education-contract.md`.
3. Read `references/interview-doctrine.md` before the first question.
4. Read `references/standing-doctrine.md` for what is never re-asked.
5. Judge the size: one-sentence diff → say so and skip the skill;
   small-but-real → quick lane (brief education, one batched round of
   evidence-backed questions, quarter-page pack; the close may merge the
   two gates into one table-plus-dispatch question when the plan-step
   choice was already settled in the batched round); otherwise full lane.
6. Ask the 1–3 orienting questions needed to aim education. No decisions.

## Workflow

1. **Orient.** Restate the ask in plain English; classify nothing yet.
2. **Educate.** Dispatch clean read-only researchers per the shared policy
   and `references/education-contract.md`. Output: research files, a facts
   briefing, and the blank Intent Pack template.
3. **Interview.** Walk the must-always-know list breadth-first under
   `references/interview-doctrine.md`: open questions with informed
   framing, investigate-and-return cycles as answers demand, journey maps
   and the test grid produced and approved in-flow, standing items as
   one-line confirms, answers written into the pack immediately. Open
   every questioning round after the first with the compact running
   decisions table — what's settled so far — so the user follows along by
   table while answering; the gate-1 table is the final version of the
   same table, never a reveal.
4. **Proxy on request.** "Have <model> answer as me" swaps in a clean
   proxy child under the same open-question rules; answers are marked,
   user-visible decisions stay provisional unless delegated, and the user
   gets a skimmable decision summary afterward.
5. **Harden.** Self-review against this skill's own failure modes: any
   pack decision with no answer, approval, or confirmed default behind it;
   any invented shorthand; any un-parked "later"; any answer recorded but
   not understood — plus placeholders, contradictions, vague adjectives,
   requirements with no proof line, must-know items with no line.
6. **Close with two gates.** Gate 1: the decision table — everything
   decided, one clean table, assumptions marked and owned — "is this
   good?" Gate 2: "ready for me to run the plan step?" A bare yes runs
   `$arch-mini-plan` against the pack; a sentence of steering (full
   `$arch-step`, an adversarial plan review with a named model and round
   cap, straight to `$conductor`) runs exactly that. Hand off with the
   reminder that downstream skills must not re-ask what the pack answers.

## Output expectations

- The Intent Pack per `references/intent-pack-contract.md`, signed off after
  gate 1 feedback is folded in.
- A decision log in the pack: every question and answer, proxy answers
  marked, rejected alternatives, flagged derivations.
- The gate-2 handoff executed as steered, with the chosen next command
  named plainly.
- Chat output stays compact: progress lines during the interview, the
  decision table at the close, detail in the pack.

## Reference map

- `references/must-know-list.md` — the 13 items every pack must have a
  line for, with tags and strong/weak bars
- `references/intent-pack-contract.md` — artifact layout, blank template,
  decision log, sign-off rules, acceptance bar
- `references/interview-doctrine.md` — elicitation, framing, the
  investigate-and-return loop, budgets, jargon ban, grid-up-front, journey
  maps, visuals, two-gate close, proxy mode
- `references/education-contract.md` — researcher lenses,
  facts-not-decisions rule, recurring mid-interview education
- `references/standing-doctrine.md` — core requirements and execution
  defaults baked into every pack
- `references/examples.md` — six worked interviews plus counter-examples;
  illustrations of the moves, not a lookup table
- `../_shared/agent-orchestration-policy.md` — dispatch semantics for
  researchers and the proxy interviewee
