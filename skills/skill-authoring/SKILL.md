---
name: skill-authoring
description: "Write, edit, refactor, or audit prompt-first agent skills so they stay simple by default, self-contained, anti-heuristic, and distinct from nearby peers. Use when a Codex, OpenClaw, OpenAI, Anthropic, or repo-local skill needs stronger intent, trigger boundaries, packaging, references, runtime metadata, or validation before shipping."
metadata:
  short-description: "Author prompt-first reusable skills"
---

# Skill Authoring

Write the smallest reusable instructions that preserve the user's intended
outcome and let the agent exercise judgment. Use this skill for skill packages;
apply `$prompt-authoring` to their prose.

## Critical authoring rules

- Put the mission and highest-consequence instructions immediately after the
  title: required tools or context, authorization boundaries, evidence needed,
  and what counts as completion. Include only those that matter to this skill.
  Setup recipes, examples, and long explanations come later or in references.
- Preserve essential constraints when shortening. Remove repetition and
  generic advice before moving conditional detail; never hide a rule needed
  on every invocation behind an optional reference. Important placement helps
  attention; it does not make a truncated read acceptable.
- Aim well below **500 body lines and approximately 5,000 tokens**. These are
  authoring review thresholds, not fill-to targets or universal runtime limits.
  Measure both; long lines can conceal a large prompt. A justified exception
  still needs a complete, practical loading path.
- Design for selective reading: keep the shared workflow in `SKILL.md`, link
  each supporting reference directly with a clear condition for reading it,
  and keep each detailed instruction in one owning place. Do not load every
  reference by default or replace a useful small skill with a needless router.
- Validate what the agent actually receives. Account for required companion
  skills, selected references, and both individual and combined tool-output
  budgets. Read complete entry files in suitably sized calls; if output is
  truncated, retrieve the missing content before using the skill. Successful
  file access is not proof that the instructions reached the agent.

For size measurement, reference layout, and loading checks, read
[packaging-trigger-and-validation.md](references/packaging-trigger-and-validation.md)
when editing package structure or an overgrown skill.

## When to use

- The user wants a new shared or local skill with a real `SKILL.md` contract.
- An existing skill needs better triggers, scope boundaries, packaging, or references.
- The user wants to decide whether a workflow should be a skill rather than a prompt, repo note, or ordinary doc.
- A skill's role is blurry relative to sibling skills, a suite guide, or a nearby tool wrapper.
- The user wants a findings-first audit of a skill's leverage, progressive disclosure, self-containment, or validation plan.
- The user wants to refactor an overgrown or heuristic skill without losing useful workflow knowledge.
- The user wants to remove accidental scripts, parameters, fake blockers, or harness behavior from a skill that should be simple prompt guidance.
- The target runtime is OpenClaw and the skill needs slash-command behavior, loader gating, metadata rules, or per-agent/shared installation guidance.

## When not to use

- The task is ordinary copy editing, summarization, or README writing rather than skill design.
- The right artifact is repo-local `AGENTS.md` guidance, a project plan, or a one-shot prompt rather than a reusable skill.
- The workflow is so small or one-off that the packaging overhead would exceed the leverage.
- The work is only an OpenClaw config or `tools.allow` change; capabilities and permissions still live in the host runtime, not in skill prose.
- The existing skill package or binding brief cannot be inspected.

## Non-negotiables

- Start from 2-3 concrete user asks and the leverage claim before designing files.
- Decide whether a skill is the right mechanism before writing one.
- Apply `$prompt-authoring` discipline to all skill prose, including `SKILL.md`, references, bundled agents, and output contracts.
- Default to simple prompt engineering. Add references, scripts, or harness behavior only after the lean prompt contract proves insufficient.
- Generalize from the user's intent, not from the first concrete incident. Preserve common-sense interpretation instead of adding formal inputs for natural-language asks.
- Teach reusable workflow, judgment, and invariants; do not replace reasoning with slogans, keyword rules, canned menus, or giant checklists.
- Treat the `description` field as runtime trigger logic, not marketing copy.
- Keep the frontmatter `description` inside the runtime length cap; treat over-1024-character descriptions as invalid unless the target runtime documents a stricter cap.
- Shape trigger boundaries against the visible peer group when related skills exist; do not judge a skill only in isolation.
- Encode runtime-specific behavior in machine-readable fields when the host supports them; do not hide load, gating, or invocation rules only in prose.
- Keep the package self-contained through bundled references and explicitly
  required installed companions. Do not depend on hidden context or repo-only
  docs, and do not duplicate companion instructions.
- If a skill creates, resumes, replaces, or coordinates model agents, make the running agent read the installed sibling `../_shared/agent-orchestration-policy.md` before dispatch and apply `$prompt-authoring` to the actual populated child brief. That policy owns shared transport, starting-context, brief-authority, continuation, isolation, topology, and integration semantics; the skill should retain only its role, domain judgment, task slicing, handoffs, and result contract.
- Do not copy a local orchestration mini-policy into an agent-using skill or add a dispatcher, controller, or skill-local script that owns those cross-skill decisions. Runtime adapters may still own narrow deterministic invocation and receipt mechanics when that is their actual job.
- Add `scripts/` only when deterministic reliability or repeated complexity justifies them, and record why a simple prompt-only package is not enough.
- Do not create a runner, launcher, controller, or formal parameter schema unless the user explicitly asked for orchestration or the workflow genuinely cannot be expressed as prompt guidance.
- Treat any script the skill ships as part of the agent's prompt budget; default to a high-signal verdict and a handle for detail, not an inline blob.
- Debug undertriggering, overtriggering, and poor execution separately.
- When an edit changes a skill's visible contract, inspect and co-edit the relevant `agents/openai.yaml` metadata, especially its default prompt, instead of letting runtime metadata drift from `SKILL.md`.
- Validate the skill on representative tasks without leaking the intended answer into the evaluation surface.
- If the brief or existing package is missing, stop and say so instead of inventing a skill contract.

## First move

1. Classify the job as `author`, `edit`, `refactor`, or `audit`.
2. Read `references/skill-pattern-contract.md`.
3. Apply `$prompt-authoring` best practices: single job, mission-level intent, success/failure, section-correct guidance, and anti-heuristic checks.
4. If the target skill dispatches model agents, read `../_shared/agent-orchestration-policy.md` and separate shared orchestration semantics from the skill's role-local workflow before editing.
5. Read the smallest additional reference that matches the job:
   - `references/workflow-and-modes.md` for mode routing and output expectations
   - `references/leverage-and-scope.md` for deciding what the skill should own and whether it should exist at all
   - `references/peer-groups-and-boundaries.md` when related sibling skills, suite routing, or overlap are in scope
   - `references/packaging-trigger-and-validation.md` for file layout, trigger quality, and shipping checks
   - `references/openclaw-skills.md` when the target runtime is OpenClaw or mirrors OpenClaw skill semantics
   - `references/script-output-economy.md` when the skill ships a script, command wrapper, or tool whose stdout the agent will read
   - `references/examples-and-anti-examples.md` when you need grounded examples or want to sanity-check framing

## Workflow

1. Lock the job-to-be-done, the leverage claim, and 2-3 canonical user asks before touching wording.
2. Choose the right mechanism: skill, prompt, `AGENTS.md`, plan doc, or ordinary docs.
3. Start with the lean prompt-only shape. Add references only when they reduce repeated prompting or keep `SKILL.md` small.
4. If the skill has visible peers, name the target lane and the nearest lookalike before rewriting trigger prose.
5. Define scope, one strong out-of-scope lookalike, and the runtime boundaries.
6. For an agent-using skill, point to the shared policy once, require
   `$prompt-authoring` on the actual dispatch brief, keep role-local doctrine
   in the owning skill, and leave launch-time choices to the agent applying
   both contracts.
7. Write the trigger description so it says what the skill does, when to use it, and when not to.
8. Encode any runtime-specific load, gating, slash-command, or invocation behavior in the runtime's machine-readable schema before treating the prose as done.
9. Build the minimum viable package: `SKILL.md` first, then only the `references/`, `scripts/`, `assets/`, and `agents/` metadata the workflow truly needs.
10. Co-edit `agents/openai.yaml` whenever the package's visible contract changes enough to make its current metadata inaccurate or incomplete.
11. Review the opening for the critical instructions, then measure the entry
    body and the normal invocation's combined reading load. Move conditional
    detail into directly linked references; verify no essential rule was lost.
12. Before adding a script, runner, launcher, or formal input interface, write the proof that prompt guidance is insufficient. If the proof is weak, keep it prompt-only.
13. Validate trigger quality, package integrity, runtime-specific behavior, execution quality, and anti-heuristic quality before shipping.

## Output expectations

- `author`: return or create the finished skill package with the leanest viable file set.
- `edit`: patch the existing skill and briefly explain which part of the contract changed.
- `refactor`: preserve useful workflow knowledge while re-homing it into the correct layer.
- `audit`: return findings first. For each finding, state the problem, why it matters, and which file or layer should change.

## Reference map

- `references/skill-pattern-contract.md` - the contract for high-impact, anti-heuristic skills
- `references/workflow-and-modes.md` - choose the right mode and keep the output shape honest
- `references/leverage-and-scope.md` - decide whether the skill should exist and what it should own
- `references/peer-groups-and-boundaries.md` - place a skill inside its visible peer group without turning boundaries into routing tables
- `references/packaging-trigger-and-validation.md` - file layout, trigger quality, progressive disclosure, and shipping checks
- `references/openclaw-skills.md` - OpenClaw-only frontmatter, gating, slash-command, fleet-isolation, and security rules
- `references/script-output-economy.md` - design the stdout of skill-shipped scripts as a prompt fragment, not a developer console
- `references/examples-and-anti-examples.md` - grounded good and bad patterns; use them to teach, not to cargo-cult
- `../_shared/agent-orchestration-policy.md` - required shared semantics for skills that create, resume, replace, or coordinate model agents
