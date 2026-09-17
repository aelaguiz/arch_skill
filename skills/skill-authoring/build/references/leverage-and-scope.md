# Leverage And Scope

Use this file when you need to decide whether the skill should exist, what it should own, and how broad it can safely be.

## Start with the user problem, not the folder

The first question is not "what files should this skill contain?" It is:
> What repeated user problem will be solved better because this skill exists?
Write 2-3 concrete user asks first. Good asks are specific enough that you can imagine the exact turn where the skill should trigger.
Examples of good starting points:

- "Build a shared skill for implementing Figma designs in our React app."
- "Audit this existing deployment skill; it feels too broad and brittle."
- "Turn this repeated simulator-debug workflow into a reusable skill."

Bad starting points:

- "We should probably have a skill for this area."
- "Let us collect all our best practices in one place."
- "This seems important, so it should be a skill."

## Choose the right mechanism

Use a skill when:

- the workflow is reusable across many turns or many people
- the agent needs a repeatable process, reference pack, or tooling guidance
- implicit or explicit invocation would be valuable
- the package should travel between repos or users

Most reusable skills should still be prompt-only. A skill usually starts as the prompt the user would have typed repeatedly, plus the minimum boundaries and references needed to make that prompt portable.
Use a prompt when:

- the user wants an explicit one-shot command
- the interface depends on prompt-style arguments
- the workflow does not need progressive disclosure or packaging

Use `AGENTS.md` when:

- the guidance is repo-specific and should apply broadly inside one codebase
- the behavior is a standing local convention rather than a reusable packaged capability

Use ordinary docs when:

- humans are the primary audience
- no runtime behavior or invocation surface is needed

## Generalize from intent

A skill should capture the durable move behind the user's examples, not freeze the first example into control flow.
Good generalization:

- "Take the named lesson through the normal authoring flow."
- "Review the prompt for heuristic drift and fix the owning section."
- "Use the visible peer group to pick the right skill and explain the boundary."

Bad specialization:

- a fixed branch for one lesson number, section name, or field label
- formal inputs for a target the user can name in normal language
- hard blockers for normal start states, such as missing artifacts in a skill that is supposed to create those artifacts
- a runner or script whose only job is to enforce a prompt sequence the agent can follow from plain instructions

## Shape scope aggressively

High-impact skills are focused. They usually own one workflow family, not every nearby concern.
Good scope shape:

- one coherent job family
- obvious trigger language
- one or two clear boundary lines
- references split by phase, domain, or mode

Bad scope shape:

- several unrelated workflows hidden under one title
- one giant "best practices" dump
- a skill that mixes reusable doctrine with repo accidents
- a skill that exists only because the topic area is broad

One useful forcing function:

- name one lookalike request that should not trigger the skill
- put that boundary in `When not to use`

## Shape scope against visible peers

Scope is not only about the abstract size of the job. It is also about how the skill sits next to other skills the model can see.
When sibling skills exist, ask:

- Which nearby skill would a model choose by mistake?
- Does the target skill own selection, the broad pass, a specialist field, a primitive operation, a review verdict, or runtime mechanics?
- What should happen when the broad owner and specialist both seem relevant?
- Is the boundary clear in compact metadata, or only after reading the body?

Good peer-aware scope:

- a coordinator chooses or sequences work, then hands off
- a broad workflow skill preserves the throughline and routes leaf work
- a specialist owns one surface and reports upstream defects
- a primitive wrapper owns exact operations and receipts, not broad intent

Bad peer-aware scope:

- every skill in a cluster claims the whole domain
- the distinction is "use this for advanced work" with no ownership boundary
- a specialist silently absorbs coordinator or broad workflow duties
- a guide skill becomes an umbrella executor

Use peer fit to clarify the skill, not to create bureaucracy. If one `When not to use` line or handoff rule fixes the confusion, stop there.

## Massive impact comes from leverage, not volume

Do not mistake longer instructions for stronger capability.
The highest-leverage skills usually do a small number of important things well:

- they preserve hard-won workflow judgment
- they encode durable distinctions the model will otherwise blur
- they make important context discoverable at the right time
- they fail loud on missing prerequisites
- they reduce repeated re-explanation across many turns

## Degrees of freedom

Set the skill's specificity to match the fragility of the task.
High freedom: Use when multiple valid approaches exist and judgment is the point. This is the default for most prompt-first skills.
Medium freedom: Use when there is a preferred pattern but some variation is healthy.
Low freedom: Use only when the sequence is fragile, safety-critical, explicitly orchestrated, or repeatedly mis-executed after prompt guidance.
If you find yourself writing many rigid rules for a high-variance task, the skill is probably compensating for poor framing rather than teaching the real lesson.

## Self-containment rule

Anything the runtime truly needs should live inside the skill package.
Bundle into the skill when:

- the detail materially affects how the workflow is executed
- the file is needed for examples, schemas, or doctrine
- another repo or machine would fail without it

Leave outside the skill when:

- the content is repo-specific standing policy
- the detail is only useful during the one-time design process
- the file is internal worklog or planning residue
