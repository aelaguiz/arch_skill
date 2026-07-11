---
name: arch-step-goal-prompt
description: "Write Markdown-backed goal prompt files for ArcStep runs from a user ask plus an optional canonical DOC_PATH, especially `$arch-step auto-plan`, `implement-loop`, `auto-implement`, or `full-auto`. Use when the user wants a durable Codex/Claude goal prompt that references source truth without copying the plan, keeps implementation aligned with plan intent, and catches surface-level completion. Not for executing ArcStep itself or creating harnesses, runners, or controllers."
metadata:
  short-description: "Write ArcStep goal prompt files"
---

# ArcStep Goal Prompt

Use this skill when the user wants a high-quality goal prompt file for an
ArcStep run.

The job is to turn a rough ask and any canonical ArcStep plan path into a
durable Markdown goal prompt. The prompt should make the future goal-mode agent
better at staying aligned while it works: rereading the controlling plan,
using the real ArcStep command, noticing common false-finish patterns, going
deeper when the work is only name-complete or status-complete, and using
reviewers only when they are requested or already required.

## When to use

- The user wants a goal prompt for `$arch-step auto-plan`, `implement-loop`,
  `auto-implement`, or `full-auto`.
- The user has a canonical ArcStep plan doc and wants a stronger goal-mode
  prompt to drive or resume the run.
- The user wants alignment reminders, reviewer handling, or completion
  language encoded into the goal prompt.
- The user wants the goal prompt saved or returned as Markdown rather than
  compressed into a paste-sized `/goal` string.
- The user is correcting a pattern where agents stop after surface-level
  completion, stale plan reads, name-only work, status-only work, unfinished
  requested reviews, or copied plan content.

## When not to use

- The user wants ArcStep work executed now. Use `$arch-step`.
- The user wants a generic prompt unrelated to ArcStep. Use `$prompt-authoring`.
- The user wants a new or edited skill package. Use `$skill-authoring`.
- The user wants a multi-skill flow designed or audited. Use `$skill-flow`.
- The user wants a harness, launcher, controller, script, or deterministic
  runner around ArcStep.

## Non-negotiables

- Keep the ArcStep plan doc as the planning source of truth. The goal prompt is
  an execution brief, not a second plan.
- Point to the plan's Scope and Simplicity Contract and freeze anchor without
  copying them. The goal prompt, its reviewer language, and later goal edits
  cannot authorize scope.
- Do not copy plan phases, checklists, implementation details, examples,
  reviewer prompts, or long doctrine from linked files into the goal prompt.
- Reference source truth by path, skill name, command, or artifact role.
- Use `$prompt-authoring` doctrine for prompt quality, especially the Codex goal
  prompt reference.
- Use `$arch-step` doctrine for ArcStep command behavior. Do not re-invent its
  workflow, receipt rules, implementation frontier, or audit standard.
- Make false finish lines explicit without turning them into a giant checklist:
  marker-only planning, stale plan reads, docs-only completion, name-only
  completion, status-only completion, copied source truth, pending requested
  reviewers, and unhandled required repairs.
- Include these when applicable: an agent-authored plan revision or reviewer
  finding was treated as human scope authority; the goal kept "repairing"
  review findings until implementation exceeded the frozen initial scope.
- Treat reviewer rejection as repair input only when the finding is directly
  authorized or already in the frozen convergence closure. New scope needs a
  human decision; out-of-scope findings stay observations; unauthorized built
  scope is subtraction work. The goal prompt should not add reviewers by
  default.
- Do not add domain-specific proof requirements, heavyweight proof rituals, or
  harness-style process unless the controlling plan already requires them.
- Never add scripts, wrappers, formal parameter schemas, launchers, controllers,
  or harnesses. This skill writes prompt guidance only.

## First move

1. Read `references/arcstep-goal-prompt-contract.md`.
2. Apply `$prompt-authoring` guidance for Codex goal prompts or persistent goal
   objectives.
3. Identify the run type from the user's language:
   - planning: `auto-plan`
   - implementation: `implement-loop` or `auto-implement`
   - mixed continuation: `full-auto`
   - unknown: write the prompt so the future agent resolves the next ArcStep
     command from the canonical doc instead of guessing
4. Identify the controlling source truth:
   - the user-supplied `DOC_PATH`, if present
   - the current canonical ArcStep doc, if the user clearly points at one
   - any user-named audit log, worklog, reviewer output, or history summary
5. If a required source path is missing and cannot be inferred from context,
   produce a prompt skeleton that names the missing slot plainly instead of
   inventing hidden source truth.

## Workflow

1. Name the desired world state in one sentence.
2. List controlling sources by path or exact artifact name, with short role
   labels only.
3. State which ArcStep command the future agent should run, or how it should
   resolve the command from the canonical doc.
4. Add a light alignment loop: reread source truth, compare work to intent,
   check the most likely false finish line, then go deeper before closing.
5. Add reviewer or auditor handling only when the user asked for it, the plan
   already requires it, or the goal is explicitly repairing failed
   self-certification.
6. Define done as a lean completion line: final source reread, current ArcStep
   frontier satisfied, required repairs handled, no requested reviewer or worker
   still pending, and a final report tied to source truth.
7. Keep compressing until the prompt points to source truth instead of
   restating it.

## Output expectations

Return or create a Markdown goal prompt file. If the user gave a `DOC_PATH` and
did not give an output path, default to a sidecar file beside the plan named
`<PLAN_STEM>_GOAL_PROMPT.md`.

The file should contain the goal prompt itself, not a separate essay about how
it was written. Use headings only when they make the prompt easier for a future
agent to follow.

When returning the result in chat, include the output path and a short note
about any unresolved source path or assumption.

## Reference map

- `references/arcstep-goal-prompt-contract.md` - prompt shape, source-truth
  compression, ArcStep run types, reviewer gates, and completion traps.
