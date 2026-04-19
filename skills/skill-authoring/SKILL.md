---
name: skill-authoring
description: "Write, edit, refactor, or audit agent skills so they are leverage-first, self-contained, and anti-heuristic. Use when a Codex, OpenClaw, OpenAI, Anthropic, or repo-local skill needs stronger use-case selection, trigger boundaries, runtime-specific packaging, gating, references, or validation before shipping."
metadata:
  short-description: "Author high-impact reusable skills"
---

# Skill Authoring

Use this skill when the work is creating or repairing an agent skill, not generic documentation.

This skill is intentionally self-contained. Use the references in this folder, not external repo docs, while doing the runtime work.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- The user wants a new shared or local skill with a real `SKILL.md` contract.
- An existing skill needs better triggers, scope boundaries, packaging, or references.
- The user wants to decide whether a workflow should be a skill rather than a prompt, repo note, or ordinary doc.
- The user wants a findings-first audit of a skill's leverage, progressive disclosure, self-containment, or validation plan.
- The user wants to refactor an overgrown or heuristic skill without losing useful workflow knowledge.
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
- Teach reusable workflow, judgment, and invariants; do not replace reasoning with slogans, keyword rules, canned menus, or giant checklists.
- Treat the `description` field as runtime trigger logic, not marketing copy.
- Encode runtime-specific behavior in machine-readable fields when the host supports them; do not hide load, gating, or invocation rules only in prose.
- Keep the shipped skill self-contained; do not depend on repo docs, hidden context, or local prompt packs at runtime.
- Keep `SKILL.md` lean and move heavy detail into `references/`.
- Add `scripts/` only when deterministic reliability or repeated complexity justifies them.
- Debug undertriggering, overtriggering, and poor execution separately.
- Validate the skill on representative tasks without leaking the intended answer into the evaluation surface.
- If the brief or existing package is missing, stop and say so instead of inventing a skill contract.

## First move

1. Classify the job as `author`, `edit`, `refactor`, or `audit`.
2. Read `references/skill-pattern-contract.md`.
3. Read the smallest additional reference that matches the job:
   - `references/workflow-and-modes.md` for mode routing and output expectations
   - `references/leverage-and-scope.md` for deciding what the skill should own and whether it should exist at all
   - `references/packaging-trigger-and-validation.md` for file layout, trigger quality, and shipping checks
   - `references/openclaw-skills.md` when the target runtime is OpenClaw or mirrors OpenClaw skill semantics
   - `references/examples-and-anti-examples.md` when you need grounded examples or want to sanity-check framing

## Workflow

1. Lock the job-to-be-done, the leverage claim, and 2-3 canonical user asks before touching wording.
2. Choose the right mechanism: skill, prompt, `AGENTS.md`, plan doc, or ordinary docs.
3. Define scope, one strong out-of-scope lookalike, and the runtime boundaries.
4. Write the trigger description so it says what the skill does, when to use it, and when not to.
5. Encode any runtime-specific load, gating, slash-command, or invocation behavior in the runtime's machine-readable schema before treating the prose as done.
6. Build the minimum viable package: `SKILL.md` first, then only the `references/`, `scripts/`, `assets/`, and `agents/` metadata the workflow truly needs.
7. Use progressive disclosure aggressively: core contract in `SKILL.md`, deeper guidance in `references/`, determinism in `scripts/`.
8. Validate trigger quality, package integrity, runtime-specific behavior, and execution quality before shipping.

## Output expectations

- `author`: return or create the finished skill package with the leanest viable file set.
- `edit`: patch the existing skill and briefly explain which part of the contract changed.
- `refactor`: preserve useful workflow knowledge while re-homing it into the correct layer.
- `audit`: return findings first. For each finding, state the problem, why it matters, and which file or layer should change.

## Reference map

- `references/skill-pattern-contract.md` - the contract for high-impact, anti-heuristic skills
- `references/workflow-and-modes.md` - choose the right mode and keep the output shape honest
- `references/leverage-and-scope.md` - decide whether the skill should exist and what it should own
- `references/packaging-trigger-and-validation.md` - file layout, trigger quality, progressive disclosure, and shipping checks
- `references/openclaw-skills.md` - OpenClaw-only frontmatter, gating, slash-command, fleet-isolation, and security rules
- `references/examples-and-anti-examples.md` - grounded good and bad patterns; use them to teach, not to cargo-cult
