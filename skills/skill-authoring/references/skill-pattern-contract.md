# Skill Pattern Contract

This file is the contract for what a strong skill must contain, what it must not do, and where each kind of guidance belongs.

## Table of contents

- Ordered design flow
- What makes a skill high impact
- Prompt-first default
- Peer fit in crowded skill groups
- Packaging ownership by file type
- Fatal anti-patterns
- Symptom-to-fix map
- Final self-check

## Ordered design flow

1. **Job to be done and leverage claim**
   - Name the repeated user problem and the improved world state the skill should create.
2. **Canonical use cases and one anti-case**
   - Capture 2-3 exact user asks the skill should handle and one similar ask it should reject.
3. **Mechanism choice**
   - Decide whether this belongs in a skill, prompt, `AGENTS.md`, plan doc, or ordinary documentation.
4. **Prompt-first shape**
   - Treat the skill as a reusable prompt contract first. Apply `$prompt-authoring` discipline before adding references, scripts, parameters, or orchestration.
5. **Peer-group fit**
   - When visible sibling skills exist, name the target lane and the nearest lookalike before rewriting trigger text.
6. **Trigger description**
   - Write the `description` so it explains what the skill does, when it should fire, and what nearby work is out of scope while staying within the runtime length cap.
7. **Runtime-specific machine behavior**
   - Encode host-specific invocation, gating, or command behavior in frontmatter or supported machine-readable fields rather than hiding it in prose.
8. **Agent-orchestration ownership when applicable**
   - Require agent-using skills to load the installed shared orchestration policy, keep role-local workflow in the owning skill, and avoid duplicating shared transport, context, continuation, isolation, topology, or integration doctrine.
9. **Core runtime contract**
   - Put the durable workflow, boundaries, and output expectations in `SKILL.md`.
10. **Progressive disclosure**
   - Move detailed doctrine, schemas, examples, and audits into `references/`.
11. **Determinism only when earned**
   - Add `scripts/` only when natural-language execution keeps failing, the same code is being re-authored repeatedly, or exact validation is the real job. Record why prompt-only guidance is not enough.
12. **Validation**
   - Test trigger quality, package integrity, and real execution separately.

## What makes a skill high impact

A skill earns its existence when it changes how the agent performs a repeated class of work, not merely how a document is worded.

Strong leverage usually comes from one or more of these:

- the workflow has multiple steps or non-obvious ordering
- good results depend on context the model will not reliably reconstruct unaided
- the task needs bundled references, schemas, or tooling instructions
- the same reasoning or packaging mistakes recur across requests
- a durable skill reduces repeated prompt-writing and makes a shared quality bar portable

A skill is usually low leverage when:

- it restates generic advice the model already knows
- it is only a thin wrapper around one one-off command
- the workflow is mostly repo-local policy that belongs in `AGENTS.md`
- the package exists only because the folder structure feels tidy

## Prompt-first default

Most skills should feel like a reusable prompt the user no longer wants to type
by hand. They should preserve the user's intent, load the right context, and
leave the agent enough freedom to reason.

The default package ladder is:

1. use a one-shot prompt or repo note when reuse is not real,
2. ship a lean prompt-only `SKILL.md`,
3. add small references when they reduce repeated prompting or keep the entrypoint short,
4. add a script only for deterministic validation, transforms, or repeated code that natural language handles poorly,
5. add a runner, launcher, controller, or harness only when the user explicitly wants orchestration or the workflow genuinely cannot be expressed as prompt guidance.

Do not turn ordinary natural-language intent into flags, menus, formal inputs,
or fake blockers. If the user can say the target in normal language, the skill
should teach the agent how to interpret it with judgment.

## Peer fit in crowded skill groups

Many skill failures are not isolated writing failures. They are peer-group
failures: several eligible skills share the same domain words and the model
cannot tell which lane owns the current ask.

When a skill has visible peers, define the skill relative to the closest wrong
choice. The strongest discriminator is usually ownership, not intensity:

- coordinator or router versus underlying execution skill
- broad workflow owner versus narrow specialist
- primitive or tool wrapper versus authoring workflow
- audit or review utility versus implementation lane
- runtime utility versus generic task advice

Do not solve peer overlap with a giant directory map inside every `SKILL.md`.
Most skills need one nearest lookalike, one rejection line, and one handoff
rule. Stable suites that repeatedly need selection logic may deserve a guide
skill, but the guide should choose and hand off rather than execute every lane.

## Packaging ownership by file type

- `SKILL.md`
  - Owns the trigger contract, required frontmatter, use boundaries, non-negotiables, workflow, and reference map.
- `references/`
  - Own detailed doctrine, examples, schemas, evaluation criteria, and deeper guidance that should load only when needed.
- `scripts/`
  - Own deterministic transforms, validators, or repeated logic that natural language handles poorly.
  - Also own their own stdout contract: scripts the skill ships are called by the agent, so their default output shape is part of the skill's prompt-budget surface. See `references/script-output-economy.md`.
  - Need an explicit reason. "Code feels safer" is not a reason.
- `assets/`
  - Own files used in outputs, not background reading.
- `agents/openai.yaml`
  - Own UI metadata, default prompt text, and invocation policy when that metadata adds real value.

If a file does not clearly own something the runtime needs, it probably should not exist.

## Fatal anti-patterns

Never ship a skill that relies on:

- folder-first design with no real use cases
- vague or marketing-style descriptions that overtrigger or undertrigger
- over-1024-character descriptions that are invalid for runtimes with the
  standard skill metadata cap
- peer-overlapping descriptions that make sibling skills indistinguishable
- giant umbrella scope that hides multiple unrelated workflows in one package
- heuristic rulebooks, slogans, or finite lists standing in for reasoning
- over-specialized skills that encode one repair incident instead of the general user intent
- formal parameter schemas, flags, menus, or launchers for normal language asks
- fake blockers that stop the agent before it has used the obvious owning prompt or skill
- runners, controllers, or harnesses added when a prompt-only runbook would do the job
- agent-using packages that duplicate the shared orchestration policy or hide transport, context, continuation, isolation, topology, or integration choices in a skill-local dispatcher script
- runtime dependence on external repo docs, hidden notes, or local prompt packs
- bloated `SKILL.md` files that should have been split into references
- decorative scripts added before proving the need for determinism
- auxiliary packaging clutter like in-skill `README.md`, changelogs, or process diaries

The test is simple:

- Would the skill still make sense if you removed the folder name and looked only at the use cases?
- Could the description accidentally match generic writing or planning work?
- Could the description also match a sibling skill with no clear discriminator?
- Is the description within the target runtime length cap?
- Does the skill teach why and when, or only recite what?
- Does the skill preserve the agent's ability to reason, or does it try to predict every branch?
- Could another repo install this skill and still use it without missing context?

If the answer is bad, the package is probably teaching cargo cult, not capability.

## Symptom-to-fix map

If the problem is:

- the skill loads at the wrong times: fix the `description`, scope boundaries, and maybe `allow_implicit_invocation`
- the skill never loads for obvious asks: strengthen the `description` with clearer user-language triggers
- the skill fails package validation for description length: keep the trigger
  discriminator but move explanation into `SKILL.md` or `references/`
- the wrong sibling skill loads: name the nearest lookalike and repair the ownership boundary, handoff rule, or guide skill
- the skill loads correctly but executes poorly: fix `SKILL.md`, the workflow, or add a script if the failure is deterministic
- the skill blocks on normal first-run inputs: remove the fake blocker and teach the expected start state
- the skill overfits one example: extract the durable principle, generalize the trigger, and demote the incident to an example if it still helps
- the skill works in one turn but degrades the agent across follow-up turns: a shipped script is dumping unbounded output into the prompt; fix the script's output shape via `references/script-output-economy.md`
- the skill feels huge or muddy: narrow the use cases, split reference material, or split the skill entirely
- the skill depends on repo trivia: move that material to `AGENTS.md` or bundle only the reusable part
- the package contains many files with little runtime value: delete them and keep the ownership model strict
- examples feel like the real rulebook: extract the principle upward and demote the examples back to illustrations

## Final self-check

- Is the repeated user problem concrete and worth a reusable skill?
- Are 2-3 canonical use cases and one anti-case obvious?
- If visible peer skills exist, is the nearest lookalike boundary clear?
- Is the `description` precise enough to control triggering?
- Is the `description` at or under 1024 characters unless the target runtime has a stricter cap?
- Are runtime-specific invocation and gating rules encoded in machine-readable form where the host supports them?
- If the skill dispatches agents, does it load the installed shared orchestration policy while keeping only role-local workflow doctrine in the package?
- Is agent dispatch still a judgment-led prompt contract rather than a skill-local controller or orchestration-owned script?
- Does `SKILL.md` contain only the durable contract and workflow?
- Are detailed examples and doctrine in `references/` instead of bloating the entrypoint?
- Are scripts present only because they add real deterministic value?
- Is there a written reason if the package adds scripts, runners, launchers, controllers, or formal inputs?
- Could this be a simple reusable prompt instead?
- Did the author generalize from the user's real intent instead of encoding one incident?
- Is the runtime package self-contained?
- Could a reviewer explain why this is a skill rather than a prompt or repo note?
- Does the skill teach underlying lessons instead of short-circuiting judgment with heuristics?
