---
name: skill-authoring
description: "Assemble, edit, refactor, or audit agent skill packages: the trigger description, the entry file, references, scripts and runtime metadata, and checking that the skill loads when it should and reaches the agent whole. Use when a skill needs creating, restructuring, re-scoping against sibling skills, slimming or validating, when a skill has grown into a pile of rules, or when an OpenClaw skill needs loader, gating or slash-command metadata. Write what the skill teaches with $prompt-authoring, and build any judgment it carries with $intuition-building. Not for one-off prompts ($prompt-authoring), AGENTS.md files ($agents-md-authoring), or turning a correction or lesson into guidance ($intuition-building)."
---

# Skill Authoring

A skill is a reusable prompt that a runtime loads when its description matches the work in front of an agent. This skill is about the package: how it gets picked, what goes in it, and whether it reaches the agent intact.

What the skill says is a separate job. Write its prose with `$prompt-authoring`. Most skills exist to give an agent judgment, so build that judgment with `$intuition-building`: explain what matters and why, with examples, instead of listing musts. A skill written as a list of rules teaches every agent that later edits it to add one more.

## How a skill works

Before a skill loads, the model sees only its name and description, next to every other installed skill's. So the description decides whether the skill gets used at all. It says what the skill does and when, in the words a user would actually say, and how it differs from the sibling most likely to be confused with it. Ownership ("writes the PR body," "reads past sessions") separates siblings better than intensity ("detailed," "deep"). Most runtimes cap descriptions at 1,024 characters; a description that loses its distinguishing line to fit is worse than one that keeps it and moves the explanation into the body.

Once loaded, the whole entry file is read on every use. Each line costs context every time and pushes what matters further down, so the opening carries what the agent most needs: the job, what it must not get wrong, and how it will know it is done. Material only some uses need goes in a reference, linked from the entry file with when to read it. A reference the agent doesn't know to open does nothing; one it opens every time belongs in the entry file. Anthropic and OpenAI both suggest keeping the entry file under about 500 lines and 5,000 tokens. That is the cost of reading it on every use, not a size to fill.

What reaches the agent is not always what is on disk. Tool output can drop the middle of a long file without saying so, and a short entry file that sends the agent straight to a long manual costs as much as a long entry file. When you check a skill, look at what actually arrived.

A skill stays a prompt unless a prompt can't do the job. If a person could say the workflow in a few sentences, it needs no script, runner or formal inputs. Scripts earn a place for mechanics a prompt does badly: parsing, exact formats, API calls, validating a file. A script that decides the workflow takes the agent's judgment away, and a script's output is the agent's next prompt, so it should say what matters and stop ([script-output-economy.md](references/script-output-economy.md)).

A skill gets installed into other repos and machines, so it can't lean on notes that exist only here. If it starts or coordinates other agents, it follows the installed `../_shared/agent-orchestration-policy.md` instead of carrying its own version.

## Before building one

Start from a few real asks the skill should handle and the nearest ask it should leave alone. Then decide whether a skill is the right thing. A one-off belongs in a prompt, a convention for one repo in that repo's AGENTS.md, a plan in a doc. A skill earns its place when the same kind of work keeps coming back and agents do it worse without the guidance. [leverage-and-scope.md](references/leverage-and-scope.md) goes deeper on what a skill should own, and [peer-groups-and-boundaries.md](references/peer-groups-and-boundaries.md) on sitting next to similar skills.

## What goes where

`SKILL.md` holds the frontmatter (`name`, `description`), the job, what the agent needs to understand to do it well, the usual path through it, and links to anything deeper. A skill doesn't need a section of rules. Real invariants, such as an exact command, a required approval or a safety line, are stated plainly where they apply.

`references/` holds detail only some uses need. `scripts/` holds deterministic mechanics, with a reason a prompt wasn't enough. `assets/` holds files used in outputs. `agents/openai.yaml` holds a display name, blurb, default prompt or invocation policy when one helps, and changes whenever the skill's visible contract changes. Nothing else belongs in the package: no README, changelog or working notes.

## Changing an existing skill

Find which part is failing before rewriting. A skill that loads at the wrong time, or never loads, has a description problem. One that loads and does the job badly has a body or reference problem. One that works for a turn and then degrades the session usually has a script flooding the context. [packaging-trigger-and-validation.md](references/packaging-trigger-and-validation.md) has the fuller diagnosis.

When a skill has grown into a pile of rules, the fix is not a shorter pile. Use `$intuition-building` to work out what the rules were protecting, write that, and keep any concrete case that still teaches as an example. Deleting a messy section without asking what it did loses whatever it was getting right.

## Checking a package

Load it fresh on a real ask, a paraphrase of that ask, and the nearest ask it should not take, and watch what the agent does. Did it load when it should and stay out when it shouldn't? Did the whole entry file arrive, and did the agent open the references it needed and no others? Was the work better than without the skill? Give whoever checks only the task, never the answer you hope for, or the check measures your hint instead of the skill. Packaging detail (naming, description length, frontmatter, metadata) and the repo's own checks are in [packaging-trigger-and-validation.md](references/packaging-trigger-and-validation.md).

## References

- [packaging-trigger-and-validation.md](references/packaging-trigger-and-validation.md): naming, descriptions, progressive disclosure, size, complete loading, `agents/openai.yaml`, validation and failure diagnosis. Read when building or restructuring a package.
- [leverage-and-scope.md](references/leverage-and-scope.md): whether something should be a skill, and what it should own.
- [peer-groups-and-boundaries.md](references/peer-groups-and-boundaries.md): when sibling skills overlap or the wrong one keeps loading.
- [script-output-economy.md](references/script-output-economy.md): when the skill ships a script whose output the agent reads.
- [openclaw-skills.md](references/openclaw-skills.md): OpenClaw only, for frontmatter, gating, slash commands, placement and security.
- [examples-and-anti-examples.md](references/examples-and-anti-examples.md): packaging examples, good and weak.
- `$intuition-building`: what an intuition is and how to build one, for whatever the skill teaches.
