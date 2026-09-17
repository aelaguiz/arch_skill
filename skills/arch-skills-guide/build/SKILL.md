---
name: "arch-skills-guide"
description: "Explain the arch skill suite, distinguish the live subskills, and recommend the right one for a user's task. Use when a request asks which arch skill to use, what the difference is between `arch-step`, `miniarch-step`, `arch-docs`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `arch-loop`, `goal-loop`, `north-star-investigation`, `arch-flow`, or wants a quick tour of the arch suite. Not for actually running the underlying workflow."
version: "1.0.0"
license: "MIT"
---

# Arch Skills Guide

Use this skill when the user needs help choosing or understanding the arch suite, not when they are ready to run the underlying workflow.

## When to use

The user asks which arch skill to use.
The user asks for the difference between the arch subskills.
The user wants a quick arch-suite tour before choosing a workflow.
The user describes a task and wants the best-fit subskill recommendation.

## When not to use

The user already knows the right subskill and wants the work done. Switch to that skill instead.
The ask is generic architecture advice unrelated to this repo's arch suite.
The user is asking for flow status inside an existing doc. Use `arch-flow`.

## Non-negotiables

Recommend one primary skill whenever possible.
If the task is ambiguous, name the top 2 candidates and explain the boundary between them.
Tie the recommendation to the user's actual ask, not to generic descriptions.
Do not keep the guide skill loaded once the user wants execution; hand off to the recommended skill.
Stay current with the installed suite only. Do not route to removed umbrellas or archived surfaces.

## First move

Read the Decision Order section below to classify the ask.
Classify the ask into one of these families: broad full arch, faster full arch, docs cleanup, mini-plan, lilarch, bug flow, audit loop, comment loop, audit loop sim, arch loop (generic hook-backed completion loop), goal loop, north-star investigation, flow-status / "what's next?"
Read the Boundary Examples section when a nearby lookalike needs sharper comparison.
Recommend the best-fit skill and explain why nearby skills are worse fits.

## Workflow

Decide what the user needs: quick tour, compare two or more subskills, or recommend the best-fit skill for a concrete task.
Map the task to the suite:
broad full arch planning, implementation, or implementation audit -> `arch-step`
faster full arch planning, implementation, or implementation audit for smaller well-defined features -> `miniarch-step`
docs cleanup, stale-doc consolidation, or post-arch plan/worklog retirement -> `arch-docs`
one-pass canonical mini plan -> `arch-mini-plan`
small 1-3 phase feature -> `lilarch`
bug, regression, crash, or Sentry issue -> `bugs-flow`
repo-wide explanation hardening, high-value code comments, or map-first convention/gotcha comments -> `comment-loop`
repo-wide audit pass, systematic defect hunt, or leave-it-running cleanup loop -> `audit-loop`
repo-wide real-app automation audit loop with a simulator ledger -> `audit-loop-sim`
generic hook-backed completion loop with free-form requirements, optional `$skill` audits, optional runtime/cadence/iteration caps, and an external Codex evaluator stop authority -> `arch-loop`
open-ended goal where the path is unknown -> `goal-loop`
quant-heavy investigation with ranked hypotheses -> `north-star-investigation`
read-only checklist or next-step routing on an arch doc -> `arch-flow`
Answer with: the primary recommendation, a short why, the nearest lookalike and why it is not the default.
If the user says to proceed, stop guiding and switch to the recommended skill.

## Output expectations

Keep the explanation short and decision-oriented.
Prefer: one recommended skill, one alternate when ambiguity is real, a one-line "use this when / not that" distinction.
If the user asked for a tour, summarize the suite without dumping the whole repo history.

## Decision order

Start with the strongest discriminator first:
1. Is the ask mostly "what's next?" on an existing plan doc? -> use `arch-flow`
2. Is the ask mainly docs cleanup, stale-doc consolidation, or working-doc retirement with code truth stable enough to trust? -> use `arch-docs`
3. Is the ask for broad, ambiguity-heavy, or helper-heavy full arch work? -> use `arch-step`
4. Is the ask for faster full-arch work on a smaller well-defined feature, still with phasing and real auto controllers? -> use `miniarch-step`
5. Is it a repo-wide map-first comment hardening pass focused on shared contracts, conventions, gotchas, or subtle behavior in code? -> use `comment-loop`
6. Is it a repo-wide audit pass, systematic defect hunt, or leave-it-running cleanup loop? -> use `audit-loop`
7. Is it a repo-wide real-app automation audit loop with a simulator ledger? -> use `audit-loop-sim`
8. Is the ask a generic hook-backed completion loop over free-form requirements, with no prescribed map-first flow, optional `$skill` audit obligations, and optional runtime/cadence/iteration caps? -> use `arch-loop`
9. Is it a bug, regression, crash, incident, or Sentry/log investigation? -> use `bugs-flow`
10. Is the path unknown and the work open-ended? -> use `goal-loop`
11. Is it a quant-heavy optimization or root-cause hunt with ranked hypotheses and brutal tests? -> use `north-star-investigation`
12. Is it a small feature or improvement that should fit in 1-3 phases? -> use `lilarch`
13. Does the user want a one-pass mini plan with canonical arch blocks? -> use `arch-mini-plan`
14. Otherwise, default to `arch-step`.

## Skill map

`arch-step`: the user wants the broad full arch workflow, a specific helper-heavy full-arch command, or a generic full-arch continuation where scope or architecture may still widen materially. Do not default to it when they only need a read-only checklist, a one-pass mini plan, or a smaller well-defined feature that fits the faster full-arch tier.
`miniarch-step`: the user wants the faster full-arch workflow for a smaller well-defined feature that still needs canonical arch blocks, phased execution, and real auto controllers. Do not default to it when the work is tiny enough for `lilarch`, planning-only, or broad enough to need the full `arch-step` helper surface.
`arch-docs`: the code is already clean enough to trust and the main job is cleaning stale, overlapping, or misleading docs, including post-arch plan/worklog retirement. Do not default to it when the feature still needs code work, or the ask is generic copy editing or net-new documentation authoring.
`arch-mini-plan`: the user wants a compact one-pass plan but still wants canonical arch blocks. Do not default to it when the work is tiny enough for `lilarch` or needs actual full-arch execution now.
`lilarch`: contained 1-3 phase feature work. Do not default to it when the task is migration-heavy, investigation-heavy, or broad.
`bugs-flow`: regressions, crashes, incidents, Sentry/log-driven fixes. Do not default to it when it is planned feature work or open-ended optimization.
`comment-loop`: the user wants a repo-wide code comment pass, wants the agent to deeply understand the repo before explaining it, or wants shared contracts, conventions, gotchas, and subtle behavior documented in code. Do not default to it when the job is docs cleanup, one local comment tweak, or bug fixing.
`audit-loop`: the user wants a repo-wide audit pass, the next worthwhile defect fixed, or a bounded cleanup loop that keeps going until review says stop. Do not default to it when there is already one concrete known bug or the main job is docs cleanup.
`audit-loop-sim`: the user wants a repo-wide real-app automation pass with a simulator ledger and a consequence-first ranking. Do not default to it when the real job is one concrete regression, docs cleanup, or non-automation audit.
`arch-loop`: the user wants a generic hook-backed completion loop over free-form requirements, optional named-skill audit obligations (e.g. `$agent-linter`, `$code-review`), and optional runtime/cadence/iteration caps, with a fresh Codex `gpt-5.4` `xhigh` external evaluator as the only stop authority. Do not default to it when the work fits a prescribed map-first loop (`audit-loop`, `comment-loop`, `audit-loop-sim`), is a pure condition-poll (`delay-poll`), or is a one-shot sleep (`wait`).
`goal-loop`: the goal is clear but the path is unknown; repeated bets matter. Do not default to it when the task already has a fixed implementation plan.
`north-star-investigation`: the user wants a quantified investigation with ranked hypotheses and brutal tests. Do not default to it when the task is just a normal bug fix or plain goal loop.
`arch-flow`: the user already has a plan doc and wants a read-only checklist or next-step routing. Do not default to it when they actually want the work performed.

## Near-lookalike boundaries

`arch-flow` vs `arch-step`: use `arch-flow` for read-only checklist and next-step routing; use `arch-step` or `miniarch-step` when the user wants continuation, the concise stage-quality readout, or `advance` to inspect and optionally execute one next full-arch step.
`arch-step` vs `miniarch-step`: use `miniarch-step` when the work is still full arch, but smaller, well-defined, and best served by one research pass plus one deep-dive pass; use `arch-step` when ambiguity, breadth, or helper needs justify the broader surface.
`arch-step` vs `arch-docs`: use `arch-step` while the feature still needs planning, implementation, or code-completeness audit; use `arch-docs` once the code is clean and the remaining job is docs cleanup, consolidation, or working-doc retirement.
`bugs-flow` vs `audit-loop`: use `bugs-flow` for one concrete known bug or incident; use `audit-loop` when the job is to find the next worthwhile bug or fragility across the repo.
`arch-docs` vs `comment-loop`: use `arch-docs` when the main job is repo documentation cleanup grounded in already-stable code truth; use `comment-loop` when the main job is high-value explanatory hardening inside code comments, docstrings, or doc comments.
`comment-loop` vs `audit-loop`: use `comment-loop` when the repo mainly needs clearer explanation of existing contracts, conventions, or gotchas; use `audit-loop` when the repo mainly needs the next real bug, dead code, duplication, or proof gap fixed.
`arch-loop` vs specialized loops (`audit-loop`, `comment-loop`, `audit-loop-sim`): use the specialized loop when the user actually wants that skill's prescribed map-first flow, artifact contract, and ranking; use `arch-loop` when the requirements are free-form, the "done" signal is an external Codex evaluator verdict, or the user wants named `$skill` audit obligations and optional runtime/cadence/iteration caps.
`arch-loop` vs `delay-poll`: use `delay-poll` when the job is purely "wait and re-check a condition" with no parent work happening between checks; use `arch-loop` when the loop has actual requirements to satisfy, or needs repeat parent work until a Codex evaluator says `clean` or `blocked`.
`arch-loop` vs `wait`: use `wait` when the user wants a one-shot sleep then a single literal resume prompt; use `arch-loop` when the loop must run until completion requirements are met, not on a fixed clock.
`arch-loop` vs `goal-loop`: use `goal-loop` when the user wants the controller-doc plus append-only iteration log shape; use `arch-loop` when the user wants native hook-backed repeat turns and an external Codex evaluator as the stop authority.
`arch-docs` vs `audit-loop`: use `arch-docs` when the main job is documentation cleanup grounded in already-stable code truth; use `audit-loop` when the main job is code audit, defect finding, dead-code deletion, or duplication cleanup.
`miniarch-step` vs `arch-mini-plan`: use `arch-mini-plan` only when the user wants a compressed one-pass plan; use `miniarch-step` when the user wants faster full-arch execution against the same canonical doc.
`miniarch-step` vs `lilarch`: use `lilarch` for true small-feature delivery with start/plan/finish; use `miniarch-step` when the change is still smallish but needs the canonical full-arch artifact and full-arch audit loop.
`arch-mini-plan` vs `lilarch`: use `lilarch` for true small-feature delivery with start/plan/finish; use `arch-mini-plan` when the user still wants canonical arch blocks.
`goal-loop` vs `north-star-investigation`: use `north-star-investigation` when the investigation itself is the main product and math/hypothesis ranking matters; use `goal-loop` for broader iterative work where the path is unknown.
`bugs-flow` vs `north-star-investigation`: use `bugs-flow` for concrete incident or regression handling; use `north-star-investigation` when the problem is a harder optimization/root-cause hunt with explicit quantified bets.

## Boundary examples

Broad full arch vs faster full arch:
"This is still full arch work, but the feature is small and well-defined. Go fast" -> `miniarch-step`
"This migration is broad, ambiguous, or needs the helper passes" -> `arch-step`
Faster full arch vs mini plan:
"I want the faster full arch workflow, not just a one-pass plan" -> `miniarch-step`
"Give me the mini plan version in one pass" -> `arch-mini-plan`
Full arch vs mini plan:
"Do the full arch flow for this migration" -> `arch-step`
"Give me the mini plan version in one pass" -> `arch-mini-plan`
Full arch vs read-only flow:
"What is the next move on this doc?" -> `arch-flow`
"Advance this doc and run the next step" -> `arch-step`
Full arch vs docs cleanup:
"Implement the plan and audit the code against it" -> `arch-step`
"The code is clean; now clean up the feature docs and retire the plan doc" -> `arch-docs`
Single bug vs audit loop:
"Analyze this Sentry crash and fix it" -> `bugs-flow`
"Scan the repo for the next real bugs and keep cleaning until it is not worth continuing" -> `audit-loop`
Docs cleanup vs comment loop:
"The code is stable; explain the conventions and gotchas in code comments" -> `comment-loop`
"The code is stable; clean up the docs and retire stale working notes" -> `arch-docs`
Comment loop vs audit loop:
"Deeply map this repo, then add the comments that actually matter" -> `comment-loop`
"Deeply map this repo, then fix the biggest real bugs and proof gaps" -> `audit-loop`
Faster full arch vs lilarch:
"This is too serious for lilarch, but still a small well-defined feature" -> `miniarch-step`
"This should fit in 1-3 phases, use little arch" -> `lilarch`
Mini plan vs lilarch:
"Small feature, but I still want the canonical architecture blocks" -> `arch-mini-plan`
"This should fit in 1-3 phases, use little arch" -> `lilarch`
Bugs vs investigation loops:
"We need to explain a metric drop and test ranked hypotheses" -> `north-star-investigation`
"We know the goal but not the path, keep iterating bets" -> `goal-loop`
Specialized loops vs generic completion loop:
"Keep tightening the onboarding copy across the marketing site until it reads well on mobile" -> `arch-loop`
"Rewrite this AGENTS.md file with `$agent-linter` as a required clean audit" -> `arch-loop`
"Every 30 minutes check whether staging is reachable and keep fixing infra until it is, max 8 hours" -> `arch-loop`
"Scan this repo for bugs and fix what matters, consequence-first" -> `audit-loop`
"Deeply map this repo, then add the comments that actually matter" -> `comment-loop`
"Find the biggest automation blind spots in the real app and keep closing them" -> `audit-loop-sim`
Generic completion loop vs pure wait/poll:
"Wait 1h30m then continue investigating the flaky test" -> `wait`
"Every 30 minutes check whether branch X has been pushed; when it is, integrate it" -> `delay-poll`
"Every 30 minutes check whether staging is reachable and keep fixing infra until it is, max 8 hours" -> `arch-loop` (parent work between checks, external evaluator decides when to stop)

## Response shape

When the user wants a recommendation: name the primary skill first, then explain why it fits this ask, the closest alternative, and the boundary between them.
When the user wants a tour: give the suite in decision order (`arch-flow`, `arch-docs`, `arch-step`, `miniarch-step`, `comment-loop`, `audit-loop`, `audit-loop-sim`, `arch-loop`, `bugs-flow`, `goal-loop`, `north-star-investigation`, `lilarch`, `arch-mini-plan`), keeping each skill explanation to one sentence unless the user asks for more depth.
