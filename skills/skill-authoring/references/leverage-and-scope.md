# Leverage And Scope

Use this file when you need to decide whether the skill should exist, what it should own, and how broad it can safely be.

## Table of contents

- Start with the user problem, not the folder
- Choose the right mechanism
- Shape scope aggressively
- Massive impact comes from leverage, not volume
- Degrees of freedom
- Self-containment rule

## Start with the user problem, not the folder

The first question is not "what files should this skill contain?" It is:

> What repeated user problem will be solved better because this skill exists?

Write 2-3 concrete user asks first. Good asks are specific enough that you can imagine the exact turn where the skill should trigger.

Examples:

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

- High freedom:
  - Use when multiple valid approaches exist and judgment is the point.
- Medium freedom:
  - Use when there is a preferred pattern but some variation is healthy.
- Low freedom:
  - Use when the sequence is fragile, safety-critical, or repeatedly mis-executed.

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
