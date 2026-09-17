# Peer Groups And Boundaries

Use this file when a skill lives near sibling skills, when the user says the roles are blurry, or when a package already has a suite, lane, or guide skill.

## Why peer fit matters

A skill can be well written in isolation and still fail at runtime if nearby skills look the same from the model's point of view.
The model usually chooses from compact metadata first: name, description, runtime eligibility, and maybe a short prompt. If three eligible skills share the same domain words, artifact words, and quality claims, the body text cannot save routing reliably. Peer fit is the discipline of making the first choice honest before the skill loads.
This is not a demand for a routing table. The goal is to teach the author to recognize the target skill's lane and the closest wrong lane.

## Find the visible peer group

Look only at peers the runtime or repo actually exposes:

- sibling `skills/*/SKILL.md` packages in the target repo or install surface
- local skill inventories in `README.md`, `AGENTS.md`, or runtime metadata
- existing guide, router, or coordinator skills
- tool, command, or primitive wrappers that cover the same user-language ask

Do not infer a large hidden suite from naming alone. If the peer package or binding brief cannot be inspected, say that peer fit cannot be judged.

## Name the lane

Use these lane names as diagnostic language, not as mandatory taxonomy.

- **Coordinator or router** — Owns selection, order, next step, or handoff. Does not perform every underlying specialist job itself.
- **Broad workflow owner** — Owns the throughline across several steps or fields. Routes leaf work to specialists instead of absorbing them.
- **Narrow specialist** — Owns one artifact, field, stage, risk surface, or proof burden. Reports upstream defects instead of compensating for them locally.
- **Primitive or tool wrapper** — Owns deterministic command, API, schema, receipt, or data mutation rules. Should not make broad product or workflow choices unless that is explicit.
- **Audit or review utility** — Owns findings, verdicts, scoring, or review coverage. Should not silently become the implementation lane.
- **Runtime utility** — Owns host behavior such as hooks, waits, gating, installation, or dispatch. Should not become generic workflow advice because it has privileged mechanics.

The lane should explain why this skill exists next to its neighbors. If the lane only restates the folder name, it is not doing enough work.

## Nearest-lookalike test

Before rewriting trigger prose, ask:

- 1. Which existing or proposed skill is easiest to confuse with this one?
- 2. Would a model choose correctly if it saw only the names and descriptions?
- 3. What is the real discriminator: artifact, stage, owner, proof type, entry condition, exit condition, risk, or handoff?
- 4. What should happen when both skills appear relevant?
- 5. What user ask should choose the other skill instead?

Strong boundaries sound like ownership:

- "This skill chooses the route; the specialist performs the route."
- "This skill owns lesson-wide coherence; field skills own individual lines."
- "This skill reviews the artifact; it does not edit the artifact."
- "This skill wraps the primitive; it does not invent upstream intent."

Weak boundaries sound like vibe:

- "Use this for better quality."
- "Use this when the task is important."
- "Use this for advanced cases."
- "Use the other skill for simpler work."

If the discriminator only works as a keyword list, the scope is probably still muddy.

## Boundary repair options

Pick the smallest repair that makes the peer choice clear.

- Sharpen the target skill's `description` when the skill is right but the runtime trigger is blurry.
- Add a `When not to use` or handoff line when the body is clear but the nearest lookalike is not rejected loudly enough.
- Re-home detail into `references/` when the entrypoint is trying to explain a whole suite.
- Split a skill when two independent jobs have different entry conditions, outputs, and validation loops.
- Merge or demote a skill when it exists only as a renamed slice of a sibling.
- Move repo-wide standing policy to `AGENTS.md` when every skill in the peer group is repeating the same local rule.
- Create or update a guide skill when the user problem is choosing among a stable suite, not executing one lane.

Do not make every specialist list every other specialist. A skill needs the closest boundary and the handoff rule, not a directory index.

## When to add or update a guide skill

A guide skill is useful when users or models repeatedly need to choose among a stable group of adjacent skills.
Use a guide skill when:

- the user asks which skill to use or how a suite is divided
- several real skills are valid candidates until their boundaries are compared
- the right answer is selection, ordering, or next-step routing

Do not use a guide skill when:

- there are only one or two lookalikes and a stronger `description` would fix it
- the suite is still volatile and a map would fossilize unfinished decisions
- the user already selected the underlying skill and wants execution

Guide skills should recommend one primary lane when possible, explain the nearest alternative, and then hand off. They should not become umbrella execution skills.

## Final self-check

- Is the target skill's lane clear next to visible peers?
- Is the nearest lookalike named or at least recognizable?
- Would compact metadata give the model enough signal to choose correctly?
- Does `When not to use` reject the closest wrong lane, not just generic unrelated work?
- Is handoff behavior clear when a coordinator, broad owner, specialist, or primitive all touch the same user goal?
- Did examples illustrate the boundary without becoming a routing table?
