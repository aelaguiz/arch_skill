---
name: arch-skills-guide
description: "Explain the arch skill suite, distinguish the live subskills, and recommend the right one for a user's task. Use when a request asks which arch skill to use, what the difference is between `arch-step`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `goal-loop`, `north-star-investigation`, `arch-flow`, or wants a quick tour of the arch suite. Not for actually running the underlying workflow."
metadata:
  short-description: "Guide and selector for the arch skill suite"
---

# Arch Skills Guide

Use this skill when the user needs help choosing or understanding the arch suite, not when they are ready to run the underlying workflow.

## When to use

- The user asks which arch skill to use.
- The user asks for the difference between the arch subskills.
- The user wants a quick arch-suite tour before choosing a workflow.
- The user describes a task and wants the best-fit subskill recommendation.

## When not to use

- The user already knows the right subskill and wants the work done. Switch to that skill instead.
- The ask is generic architecture advice unrelated to this repo's arch suite.
- The user is asking for flow status inside an existing doc. Use `arch-flow`.

## Non-negotiables

- Recommend one primary skill whenever possible.
- If the task is ambiguous, name the top 2 candidates and explain the boundary between them.
- Tie the recommendation to the user’s actual ask, not to generic descriptions.
- Do not keep the guide skill loaded once the user wants execution; hand off to the recommended skill.
- Stay current with the installed suite only. Do not route to removed umbrellas or archived surfaces.

## First move

1. Read `references/skill-map.md`.
2. Classify the ask into one of these families:
   - full arch
   - mini-plan
   - lilarch
   - bug flow
   - goal loop
   - north-star investigation
   - flow-status / "what's next?"
3. Read `references/boundary-examples.md` when a nearby lookalike needs sharper comparison.
4. Recommend the best-fit skill and explain why nearby skills are worse fits.

## Workflow

1. Decide what the user needs:
   - quick tour
   - compare two or more subskills
   - recommend the best-fit skill for a concrete task
2. Map the task to the suite:
   - full arch planning, implementation, or implementation audit -> `arch-step`
   - one-pass canonical mini plan -> `arch-mini-plan`
   - small 1-3 phase feature -> `lilarch`
   - bug, regression, crash, or Sentry issue -> `bugs-flow`
   - open-ended goal where the path is unknown -> `goal-loop`
   - quant-heavy investigation with ranked hypotheses -> `north-star-investigation`
   - read-only checklist or next-step routing on an arch doc -> `arch-flow`
3. Answer with:
   - the primary recommendation
   - a short why
   - the nearest lookalike and why it is not the default
4. If the user says to proceed, stop guiding and switch to the recommended skill.

## Output expectations

- Keep the explanation short and decision-oriented.
- Prefer:
  - one recommended skill
  - one alternate when ambiguity is real
  - a one-line "use this when / not that" distinction
- If the user asked for a tour, summarize the suite without dumping the whole repo history.

## Reference map

- `references/skill-map.md` - the arch suite decision map, comparison table, and example asks
- `references/boundary-examples.md` - near-lookalike examples and the exact line between them
