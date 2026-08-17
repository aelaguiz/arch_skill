---
name: intent-police
description: "Stand up and consult a long-lived, read-only intent-police agent that independently derives the user's intent from their verbatim words, keeps an on-disk intent ledger, and gives blunt advisory feedback on whether current work still serves that intent. Use when the user asks for an intent police or a standing check that long, delegated, or overnight work stays what they asked for. Consult it at plan changes and decisions, after feedback from other agents before adopting findings, before calling work done, when the user's direction changes, and periodically during long unattended stretches. It classifies direction changes as micro-adjustment versus fundamental shift, filters review findings for scope creep, infers the business problem behind capability asks, and recommends subtraction only. Not for code-quality review, one-shot cold reads, plan-artifact audits, convened decision panels, implementation, or any gating or escalation machinery."
metadata:
  short-description: "Long-lived advocate for the user's intent"
---

# Intent Police

Use this skill to stand up and consult a long-lived agent whose only job is to
hold the user's intent and say, plainly, whether the work still serves it.

The failure this skill exists to stop: an agent converts the user's outcome
into an implementation framing, reviewers generate findings scoped to that
framing, the agent treats those findings as new authority and expands scope,
each expansion gets re-reviewed, and the user wakes up to an overbuilt
monstrosity that does not accomplish the goal. Nobody in that loop still holds
the user's original words. The intent police is the one who does.

It is the user's advocate in the loop, with a deliberately different
perspective from whatever implementation detail is currently up for debate.
Its feedback is advice. You own your decisions; it owns the reminder of what
the user actually asked for.

## When to use

- The user asks for an intent police, an intent check, or a standing watch
  that work stays what they asked for.
- A long run of work — a goal, epic, plan implementation, or overnight
  autonomous stretch — will involve decisions, reviews by other agents, or
  done-claims while the user is away.
- You are coordinating workers and reviewers and want a clean-context
  advocate filtering review output for scope creep before it becomes work.

## When not to use

- One-shot clean opinion on an artifact: `$fresh-consult`.
- Plan-artifact readiness or code-against-plan audit: `$plan-audit`.
- Skeptical code-reality review: `$cynical-code-review`.
- A convened cross-disciplinary decision: `$revenue-product-tech-panel`.
- Code quality, correctness, or test review of any kind — the intent police
  never opines on those.
- Short interactive work where the user is present and steering; they are
  their own intent police.

Do not stand one up automatically inside other workflows. The user asks for
it, or you ask the user whether they want one for a long unattended run.

## Standing it up

Stand up one intent police per run of work, before or at the first
consequential decision — not one per task.

Read `../_shared/agent-orchestration-policy.md` and dispatch a read-only,
clean-context, long-lived child. Give it the role brief at
`references/intent-police-brief.md` plus:

- The user's **verbatim messages** for this run — the actual words, unedited.
  Never substitute your summary of them.
- Any artifact the user personally wrote or explicitly approved (issue text,
  an approved plan, a `$plan-interview` Intent Pack).
- Read access pointers: repo root, plan docs, relevant PRs.
- A ledger path you choose, e.g. `docs/INTENT_LEDGER_<topic>_<date>.md` in
  the working repo.

Keep the same child alive for the whole run and resume it for every consult.
If the host cannot keep it alive, stand up a fresh child re-anchored from the
ledger plus any new user messages; the ledger, not the process, is the
continuity.

## The consult moments

Consult at judgment moments, not constantly. These are the moments that
matter; execute them with your own judgment rather than a schedule:

- **Changes and planning.** Adopting a plan, rewriting a plan, choosing
  between approaches, or any moment the work-item list is about to grow.
- **After receiving feedback from other agents.** Panels, fresh consults,
  cynical reviews, PR comments — consult before adopting the findings as
  work. This is the anti-spiral valve: review output passes through the
  user's advocate before it becomes scope.
- **Getting ready to call something done.** Done-ness is judged against the
  outcome in the ledger, not against your task list.
- **The user's direction changes.** Forward the new words verbatim for the
  micro-adjustment versus fundamental-shift ruling.
- **Periodically during long unattended stretches.** Send a short status so
  drift is caught before it compounds. Choose the cadence yourself.

Between consults, leave it alone. Do not ask it to co-design, brainstorm,
pre-approve routine steps, or referee implementation debates.

## What to send at a consult

A consult is a status share, not a question. You are not commissioning an
audit; you are showing the user's advocate what happened and letting it react
under its own mandate. The default consult message is: here is what the user
said (verbatim), here is what we did and decided since last time, here are
the artifacts — per your mandate, what are your thoughts?

Do not ask it narrow or leading questions — "is this done-claim honest?",
"check only whether the plan lists each requirement", "verify section 3."
Narrow questions get narrow answers and quietly turn the advocate into an
auditor scoped by your framing, which is exactly the framing it exists to be
independent of. If you have a specific worry, name it as context after the
open ask; never make it the question.

Keep its context clean. Send:

- New user messages since the last consult, verbatim.
- A short factual status: what is built or decided, the current work-item
  list, and what is about to happen next.
- Review findings as a summarized list of proposed changes with their claimed
  justification, labeled as reviewer proposals — never raw reviewer or panel
  transcripts.
- Pointers (paths, PR numbers) it may read directly.

Never send a fork of your own context, and never present your theory of what
the user "really wants" as fact. It derives intent itself.

## How to treat the feedback

Each reply comes back short: an intent restatement, a verdict (`aligned`,
`drifting`, `spiraling`, or `ambiguous — ask the user`), and named items that
do not serve intent with cut/defer/ask suggestions.

- Treat it as advice from the user's advocate and apply your own judgment.
  There is no gate, veto, or escalation machinery here.
- When it rules a review finding out of scope, the default is to drop the
  finding. Adopting it anyway deserves real evidence — ideally the user's own
  words — not another review round.
- When it says `drifting` or `spiraling`, the honest responses are to cut the
  named items or to ask the user; declaring victory over its objection and
  moving on is how monstrosities get built.
- When it says the intent is ambiguous, the answer is one plain question to
  the user, not more analysis.
- Even an `aligned` reply restates the user's actual goal. Let that
  restatement anchor your next stretch of work; that reminder is half the
  value of the skill.
- You may push back once with evidence it missed. If it holds its ruling, the
  tie-breaker is the user, not another reviewer.

## Non-negotiables

- The intent police is read-only and advisory. Do not give it write access,
  gate authority, or escalation duties, and do not build compliance
  machinery around it.
- The user's verbatim words are its only intent authority. Reviewer findings,
  agent discoveries, and technical blockers never shift intent.
- It recommends subtraction only. If a consult reply proposes new scope, that
  reply is out of role — say so and disregard the addition.
- Do not recruit it into implementation debate or code-quality review; that
  is how the advocate becomes another spiral participant.
- One intent police per run, resumed across consults, with its ledger on
  disk in the working repo.
