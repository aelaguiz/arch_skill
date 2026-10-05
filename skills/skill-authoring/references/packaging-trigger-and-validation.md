# Packaging, Trigger, And Validation

Use this file when turning the concept into a shippable skill package.

## Table of contents

- Packaging rules
- Package ladder
- Naming rules
- Description writing rules
- Peer-aware trigger rules
- Progressive disclosure rules
- Size and instruction order
- Complete loading
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

## Package ladder

Build the smallest package that solves the repeated user problem:

1. Start with a lean prompt-only `SKILL.md`.
2. Add `references/` only when the detail would bloat the entrypoint or be useful only on demand.
3. Add `agents/openai.yaml` only when UI metadata, a default prompt, or invocation policy helps.
4. Add `scripts/` only when deterministic validation, transforms, or repeated code are truly needed.
5. Add a runner, launcher, controller, harness, or formal input interface only when the user explicitly wants orchestration or the task cannot be expressed as prompt guidance.

Before adding anything beyond `SKILL.md`, write the reason in the package
design notes or review summary. If the reason is only "this makes the skill
feel more robust," keep the package prompt-only.

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

Keep the mission, essential constraints, common workflow, completion evidence,
and reference routing in `SKILL.md`. Put the instructions whose omission would
most change the outcome near the top, before setup or detailed procedures.
Do not require a fixed set of headings when a smaller structure works.

Move into `references/`:

- detailed doctrine
- examples and anti-examples
- schemas
- audit criteria
- deeper process detail

Link each reference directly from `SKILL.md` and say what task or situation
requires it. Loading a reference should answer a current need, not be a ritual
at the start of every invocation. Keep references one level deep where possible;
avoid chains that hide required instructions behind partial previews. Give a
reference longer than 100 lines a short contents list or useful section links.
For a large schema or catalog, provide search terms so the agent can retrieve
the relevant part. Do not copy the same detailed procedure into the entry file,
references, and `agents/openai.yaml`; metadata should invoke the owning skill.

If the target runtime is OpenClaw, keep the OpenClaw-only loader, gating, command-dispatch, placement, and security rules in a dedicated reference file such as `references/openclaw-skills.md` rather than smearing them across every generic section.

Add a `script` when:

- the same code keeps being re-written
- precise validation is valuable
- natural-language execution keeps failing in a repeatable way

Do not add a script, runner, launcher, controller, or formal input schema just
to make a prompt sequence look deterministic. If a human would reasonably type
the workflow as a few sentences, the skill should probably remain prompt-only.

Once the decision to ship a script is made, the script's stdout shape is a separate design problem and is owned by `references/script-output-economy.md`. Treat it as part of the skill's prompt-budget surface, not as a developer console.

## Size and instruction order

Use **under 500 body lines and approximately 5,000 tokens** as review thresholds
for `SKILL.md`, and aim substantially smaller when the task permits. These are
guidelines for useful context, not universal parser limits. Crossing either
threshold calls for a content and loading review; being below both does not
prove a skill is concise or reliably loaded. Preserve an essential instruction
even when doing so requires a justified exception.

Measure the Markdown body separately from frontmatter. Count lines and tokens
with the target tokenizer when available; identify the tokenizer or label an
estimate explicitly. Words, bytes, and tokens are different units. `wc -l -w -c
skills/<slug>/SKILL.md` is a useful whole-file inventory, not a token count.
Do not meet a line target by joining paragraphs into huge lines or making the
instructions cryptic.

Evaluate three different sizes:

1. **Discovery metadata:** the descriptions exposed before a skill is selected.
   Keep them precise and within the target runtime's actual field limits.
2. **Instructions for this invocation:** the entry body plus required companion
   skills and the references this task actually needs. This is the relevant
   context cost; a short entry file that immediately loads a manual is still
   expensive.
3. **The package on disk:** references, scripts, and assets may be substantial
   without entering context on every use. Review their necessity and selective
   access; do not apply an instruction-token limit to an image or template.

Order the entry file around decisions. Start with the outcome, the critical
operating constraints, and the evidence that makes the result usable. Follow
with the common execution path and conditional reference links. Keep examples,
troubleshooting recipes, installation commands, and rationale below the
instructions they support or in a relevant reference. Installation instructions
usually belong in the repository's installation docs, not in an already-loaded
runtime skill.

When refactoring, identify the user-required behaviors first. For each, retain
its essential rule in the entry file or route its conditional procedure to a
reference that will be read before that operation. Remove duplicate wording,
stale alternatives, and generic tutorials. Review the resulting workflow for
lost meaning; fewer lines alone is not success.

The numeric guidance has different wording in the primary sources:

- [Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
  recommends fewer than 500 body lines and selective, directly linked references.
- [Anthropic Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
  describes the instruction layer as under 5,000 tokens.
- [OpenAI's published skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)
  recommends under 500 lines and separately uses under 5,000 **words**.
- [OpenAI's Codex skill-creator](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md)
  emphasizes the shortest useful entry file with essential constraints and
  conditional references, without imposing a numeric body limit.

These links explain the recommendations; they are not required runtime reads.
Our token review threshold follows the more conservative token-based guidance.

## Complete loading

Before treating a skill as applied, read its entire entry file. Fetch relevant
references before their dependent operation. Inspect the delivered tool output
for truncation or omitted ranges, including wrappers that combine several tool
results. A command can read the whole file successfully while the outer tool
response silently omits the middle.

Budget the combined output when batching independent reads. Individual command
limits do not enlarge an outer response limit. Use separate returns or bounded,
contiguous file ranges when the full set will not fit; retrieve every missing
part before relying on the instructions. A first-page preview or search hit is
navigation, not proof that the complete contract was loaded.

During package validation, walk a representative invocation's required reading
path through the actual tool surface. Check that the entry file reaches the
agent intact, the needed references are discoverable and readable, and irrelevant
references stay unloaded. Report entry-body size and material companion-reading
cost in the change summary. Keep this proportionate: an ordinary text refactor
needs a loading check and behavioral walkthrough, not new workflow automation
or tests asserting exact doctrine wording.

## `agents/openai.yaml` rules

Include `agents/openai.yaml` only when it adds real value.

Useful reasons:

- you want a cleaner UI display name
- you want a short user-facing blurb
- you need a default prompt snippet
- you want to force explicit invocation by setting `allow_implicit_invocation: false`

Choose invocation deliberately per package. Elective lifecycles, persistent
loops, and specialist reviews normally use `policy.allow_implicit_invocation:
false`; omission permits implicit selection. Narrow helpers and repo-required
workflows remain available within their actual triggers. A selected parent may
load its necessary documented helpers, but a handoff must not silently activate
another elective workflow or override read-only/no-delegation scope.

Keep it minimal and accurate. Quote string values. If `default_prompt` exists,
mention `$skill-name` and the requested job; keep workflow doctrine in SKILL.md.

On updates:

- confirm `display_name`, `short_description`, and `default_prompt` still match the current `SKILL.md`
- co-edit the metadata in the same change when the skill's visible contract, required policy, or default behavior changes
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
   - critical instructions appear before detailed procedures
   - the entry file and required reading arrive without truncation
   - body size and combined reading cost were reviewed against the guidance above
   - the instructions are followable
   - the references are sufficient without hidden context
   - the skill preserves common-sense interpretation instead of forcing needless parameters
4. **Validation integrity**
   - representative tasks are realistic rather than cherry-picked
   - the evaluator does not receive the intended answer or hidden conclusions
   - success means the skill generalized, not that the validator reconstructed the target from leaked context

Do not treat these as one problem. A skill can trigger perfectly and still execute badly, or vice versa.

## Practical checks

- Run any local skill validator your environment already provides.
- Run the repo-level diagnostic when available:

```bash
npx skills add . --list
```

- Read the package top-to-bottom and ask:
  - is this self-contained?
  - is `SKILL.md` doing too much?
  - does the description sound like a trigger or an advertisement?
  - is the description at or under 1024 characters, or the stricter target
    runtime cap?
  - could the description also select a sibling skill?
  - are references being used for real doctrine rather than clutter?
  - does the package stay prompt-first unless determinism is proven?
  - did any concrete example become a rigid workflow rule by accident?
- Run at least one representative task from the main use cases and one nearby anti-case.
- Run one paraphrased task that names the target naturally instead of through exact keywords or formal inputs.
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
- became over-constrained, remove fake blockers, formal inputs, and scripted control flow before adding more rules
- appears to pass validation only when the evaluator already knows the expected answer, fix the validation setup before changing the skill
- keeps failing the same precise task, add or refine a script
