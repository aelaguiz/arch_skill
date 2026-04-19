---
name: agents-md-authoring
description: "Write, edit, refactor, or audit `AGENTS.md` files for coding projects so they stay concise, repo-present, plain-English, command-first, scope-aware, and non-inferable. Use when a repo needs a new root or path-local `AGENTS.md`, an `AGENTS.override.md`, a compressed docs index, or a findings-first review of existing agent instructions."
---

# AGENTS.md Authoring

Use this skill when the work is authoring repo instruction files for coding agents, not generic documentation writing or OpenClaw workspace-bootstrap design.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- The user wants a new repo-root or path-local `AGENTS.md` for Codex, Copilot, Cursor, Claude Code, or another compatible coding agent.
- The user wants to tighten, split, or refactor an existing `AGENTS.md` so it stops wasting prompt budget every run.
- The user wants an `AGENTS.override.md` for a subtree, release freeze, incident mode, or security-sensitive service.
- The user wants a findings-first audit of instructions for missing commands, weak definition-of-done rules, stale scope boundaries, or noisy inferred content.
- The user wants to add a compressed docs index or a compact map of deeper docs without copying a whole documentation tree into always-on context.

## When not to use

- The task is writing `SOUL.md`, `SKILL.md`, prompt contracts, or other agent surfaces rather than repo `AGENTS.md`.
- The right artifact is ordinary docs, a project plan, or a README rather than a persistent instruction file.
- The content is generic style guidance or architecture summary the agent can infer from the codebase or tooling.
- The target repo or existing instruction file cannot be inspected and there is no reliable local context from which to author one.

## Non-negotiables

- Treat `AGENTS.md` as always-on prompt budget. Every line must earn its keep.
- Write current repo truth only. `AGENTS.md` is about how the repo works now, not how you planned the file, what you might add later, or what just happened in a prior edit.
- Every authored `AGENTS.md` should either contain or inherit a short plain-English communication invariant. Root files should usually own it unless an equivalent stronger rule already exists in inherited repo guidance.
- Start with the repo's verification path: setup, build, lint, test, typecheck, file-scoped commands when possible, definition of done, and blocked-state rules.
- Prefer non-inferable repo truths: unusual commands, dangerous paths, required approvals, critical docs, required skills, and exceptions to default behavior.
- Do not use `AGENTS.md` as a generic architecture dump, style manifesto, or codebase mirror.
- Do not leak authoring-process narration into the file: no planning talk, no retrospective notes, no "this file exists to...", and no self-referential instructions about this skill unless the repo itself has a real operational need for that rule.
- Plain-speak rules should be concrete, not philosophical: write in plain natural English, lead with the concrete answer in 1-3 sentences, name the exact thing that changed, translate shorthand immediately, and avoid workflow jargon unless the user explicitly asked for it.
- Separate always-on rules from on-demand depth. Point to docs, indexes, or skills instead of copying entire references inline.
- Design root, path-local, and override files consciously. Scope is part of correctness.
- Keep commands runnable and current. If the file names checks that should pass after edits, run them whenever feasible.
- If the repo context is missing, stop and say so instead of inventing commands, paths, or conventions.

## First move

1. Classify the job as `author`, `edit`, `refactor`, or `audit`.
2. Read `references/agents-md-pattern-contract.md`.
3. Read the smallest additional reference that matches the job:
   - `references/structure-and-scope.md` for discovery, layering, overrides, and monorepo placement
   - `references/content-budget-and-docs-index.md` for command priority, non-inferable content, compressed docs indexes, and anti-bloat rules
   - `references/examples-and-anti-examples.md` when you need grounded file shapes, section patterns, or audit examples
   - `references/maintenance-and-portability.md` for cross-tool compatibility, self-improving loops, and long-term upkeep

## Workflow

1. Lock 2-3 canonical user asks and one nearby anti-case before drafting.
2. Decide whether the right artifact is `AGENTS.md`, `AGENTS.override.md`, a path-local file, ordinary docs, or a skill.
3. Inventory the repo truths the agent cannot reliably infer: exact commands, dangerous paths, required approvals, critical docs, and special-case workflows.
4. Put commands first: setup, build, lint, test, typecheck, file-scoped variants when possible, then definition of done and blocked-state rules.
5. Shape scope intentionally: root for cross-cutting rules, deeper files for local doctrine, overrides only when replacement is safer than inheritance.
6. Add or preserve a short plain-speak section in the owning layer. Root files should usually own it; deeper files should only add to it when local jargon or special user-facing terms need stricter rules.
7. Keep the file lean. Move depth into linked docs or a compressed index instead of copying whole references.
8. Run a meta scrub before you finish: delete any sentence about the drafting process, future plans for the file, or which skill or workflow produced it.
9. Validate the result for cold-start usefulness: can a new coding agent tell what to run, when to stop, where truth lives, and how to answer in plain English?

## Output expectations

- `author`: return or create the finished `AGENTS.md` package with the leanest viable file set.
- `edit`: patch the instruction file and briefly name which layer changed: commands, scope, done criteria, escalation, or docs map.
- `refactor`: preserve the useful repo doctrine while relocating noise into the correct layer.
- `audit`: return findings first. For each finding, state the issue, why it hurts agent performance, and which file or section should change.

## Reference map

- `references/agents-md-pattern-contract.md` - the contract for high-signal repo instruction files
- `references/structure-and-scope.md` - precedence, root vs path-local placement, overrides, and directory strategy
- `references/content-budget-and-docs-index.md` - command-first content, non-inferable detail, passive context, and anti-patterns
- `references/examples-and-anti-examples.md` - strong section shapes, templates, and common failure modes
- `references/maintenance-and-portability.md` - cross-tool compatibility, self-improvement, and upkeep loops
