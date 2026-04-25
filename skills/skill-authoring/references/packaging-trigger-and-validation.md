# Packaging, Trigger, And Validation

Use this file when turning the concept into a shippable skill package.

## Table of contents

- Packaging rules
- Naming rules
- Description writing rules
- Peer-aware trigger rules
- Progressive disclosure rules
- `agents/openai.yaml` rules
- Validation loop
- Practical checks
- Failure diagnosis

## Packaging rules

Every skill needs:

- `SKILL.md`
  - valid YAML frontmatter
  - `name`
  - `description`
  - `description` length within the target runtime cap; default to
    `<= 1024` characters when the runtime does not document a stricter limit

If the target runtime supports additional frontmatter or load-time gating, treat those keys as part of the functional contract, not as decorative metadata.

Add only the extra folders the workflow truly needs:

- `references/` for detailed doctrine or examples
- `scripts/` for deterministic logic
- `assets/` for output resources
- `agents/openai.yaml` for UI metadata or invocation policy

Avoid extra files such as:

- `README.md`
- `CHANGELOG.md`
- `QUICK_REFERENCE.md`
- process diaries inside the skill directory

## Naming rules

Use names that are short, literal, and trigger-friendly.

- use lowercase letters, digits, and hyphens only
- keep the folder name exactly equal to the skill name
- prefer concise action-led names over broad topic labels
- keep the name short enough to scan quickly and say out loud without explanation
- namespace by tool or domain only when it improves clarity or triggering

Weak names usually:

- sound aspirational instead of operational
- collapse several workflows into one umbrella topic
- require the description to do all the disambiguation work

## Description writing rules

The `description` is runtime behavior. It should answer three things in one pass:

1. What the skill does
2. When the skill should be used
3. What nearby work is not the same thing

It must also fit the runtime limit. Treat a `description` over 1024 characters
as invalid unless the target runtime documents a stricter cap. Do not solve an
over-cap description by deleting the real discriminator and leaving a slogan;
move deeper detail into `SKILL.md`, `references/`, or a guide skill.

Strong descriptions usually:

- name the verbs, such as `write`, `edit`, `refactor`, `audit`
- name the artifact, such as `prompt`, `skill`, or `plan`
- name the quality bar or boundaries
- include recognizable user-language triggers
- distinguish the skill from its nearest visible peer when sibling skills share
  the same domain

Weak descriptions usually:

- sound like marketing copy
- omit the artifact entirely
- describe a topic area instead of a workflow
- say only "best practices" or "help with X"
- reuse the same domain phrase as sibling skills without naming ownership,
  stage, artifact, or handoff

## Peer-aware trigger rules

When a repo has related sibling skills, write trigger text for a model choosing
among peers, not for a reader admiring one package in isolation.

Ask the nearest-lookalike question:

- Which sibling skill is easiest to confuse with this one?
- What signal should appear in the user ask or artifact state before this skill
  wins?
- What signal should route to the sibling instead?
- If both are relevant, who goes first and what is handed off?

Prefer ownership words over intensity words. "Owns field-level feedback copy"
is stronger than "for detailed feedback work." "Read-only router" is stronger
than "for lightweight flow work."

Do not turn descriptions into long routing manuals. Put one sharp discriminator
in the description, keep the nearest rejection in `When not to use`, and move
deeper suite guidance into a reference or guide skill when it truly needs one.

## Progressive disclosure rules

Keep `SKILL.md` focused on:

- when to use
- when not to use
- non-negotiables
- first move
- workflow
- output expectations
- reference map

Move into `references/`:

- detailed doctrine
- examples and anti-examples
- schemas
- audit criteria
- deeper process detail

If the target runtime is OpenClaw, keep the OpenClaw-only loader, gating, command-dispatch, placement, and security rules in a dedicated reference file such as `references/openclaw-skills.md` rather than smearing them across every generic section.

Add a `script` when:

- the same code keeps being re-written
- precise validation is valuable
- natural-language execution keeps failing in a repeatable way

Once the decision to ship a script is made, the script's stdout shape is a separate design problem and is owned by `references/script-output-economy.md`. Treat it as part of the skill's prompt-budget surface, not as a developer console.

## `agents/openai.yaml` rules

Include `agents/openai.yaml` only when it adds real value.

Useful reasons:

- you want a cleaner UI display name
- you want a short user-facing blurb
- you need a default prompt snippet
- you want to force explicit invocation by setting `allow_implicit_invocation: false`

Keep it minimal and accurate. Quote string values. If `default_prompt` exists, mention the skill explicitly as `$skill-name`.

On updates:

- confirm `display_name`, `short_description`, and `default_prompt` still match the current `SKILL.md`
- remove metadata that no longer serves a UX or invocation purpose

## Validation loop

Validate four different things:

1. **Package integrity**
   - frontmatter is valid
   - `description` is present and within the runtime length cap
   - file names are sensible
   - no broken self-references
2. **Trigger quality**
   - obvious user asks trigger it
   - paraphrased asks still trigger it
   - unrelated lookalikes do not trigger it
   - the nearest sibling lookalike loses when the target skill should win, and
     wins when the target skill should stand down
3. **Execution quality**
   - once loaded, the skill actually improves the work
   - the instructions are followable
   - the references are sufficient without hidden context
4. **Validation integrity**
   - representative tasks are realistic rather than cherry-picked
   - the evaluator does not receive the intended answer or hidden conclusions
   - success means the skill generalized, not that the validator reconstructed the target from leaked context

Do not treat these as one problem. A skill can trigger perfectly and still execute badly, or vice versa.

## Practical checks

- Run any local skill validator your environment already provides.
- Run the repo-level diagnostic when available:

```bash
npx skills check
```

- Read the package top-to-bottom and ask:
  - is this self-contained?
  - is `SKILL.md` doing too much?
  - does the description sound like a trigger or an advertisement?
  - is the description at or under 1024 characters, or the stricter target
    runtime cap?
  - could the description also select a sibling skill?
  - are references being used for real doctrine rather than clutter?
- Run at least one representative task from the main use cases and one nearby anti-case.
- In a multi-skill package, run at least one nearest-peer anti-case.
- If you use an independent validation pass, give it only the minimum task-local context needed to judge whether the skill worked.
- For OpenClaw skill packs, also validate eligibility, placement, and config with the runtime's own tooling and session model. See `references/openclaw-skills.md`.

## Failure diagnosis

If the skill:

- overtriggers, tighten the description or use explicit invocation
- undertriggers, add clearer trigger language and explicit artifact names
- fails packaging because the description is too long, keep the discriminator
  and move explanation into the body or references
- picks the wrong sibling, fix the ownership discriminator, handoff line, or
  suite guide before adding more examples
- executes vaguely, improve `SKILL.md` or add the right reference
- appears to pass validation only when the evaluator already knows the expected answer, fix the validation setup before changing the skill
- keeps failing the same precise task, add or refine a script
