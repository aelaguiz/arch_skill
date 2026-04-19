# Workflow And Modes

Always read `skill-pattern-contract.md` first. Then use this file to choose the right lane.

## Table of contents

- The four supported modes
- Mode router
- Four concrete use cases

## The four supported modes

### 1) Author

Use when there is no skill yet, or the existing material is only a loose brief.

Typical asks:

- "Build a skill for this workflow."
- "Create a shared skill for our team."
- "Turn these notes into a real `SKILL.md` package."
- "Build this as an OpenClaw skill with the right slash-command and gating behavior."

What to do:

1. State the repeated user problem and why a skill is the right mechanism.
2. Lock 2-3 canonical user asks and one out-of-scope lookalike.
3. Draft the `description` before drafting the body so the trigger boundary is explicit.
4. If the target runtime is OpenClaw, lock the frontmatter, gating, install scope, and slash-command behavior before treating the package as complete.
5. Build the leanest package that can teach the workflow well.
6. Push detailed material down into `references/` instead of expanding `SKILL.md`.
7. Run trigger, package, and runtime-specific validation before returning.

What to return:

- The finished skill package.
- Only the shortest note needed to explain an important assumption or deliberate boundary.

### 2) Edit

Use when the skill mostly works but one layer is weak, misplaced, or incomplete.

Typical asks:

- "Tighten this skill."
- "Improve the description."
- "Add the missing references without rewriting everything."
- "Fix the OpenClaw metadata, gating, or command-dispatch behavior."

What to do:

1. Identify the failing layer before rewriting.
2. Patch only the owning layer first: frontmatter, `description`, `SKILL.md`, `references/`, `scripts/`, or runtime metadata such as `openai.yaml`.
3. Re-read the whole package for drift, especially when a local edit reveals a broader scope problem.

What to return:

- The patched skill package.
- A short note naming what changed and where.

### 3) Refactor

Use when the skill has useful domain knowledge but is structurally wrong, bloated, or overly heuristic.

Typical asks:

- "Refactor this skill without losing what makes it useful."
- "Make this more self-contained and less cargo-cult."

What to do:

1. Identify the workflow knowledge worth preserving.
2. Extract the durable principles that explain why the old skill helped.
3. Re-home bulky doctrine, examples, or narrow rules into the correct layer.
4. Rebuild the top-level contract so the package is lean, bounded, and portable.

What to return:

- The refactored skill package.
- A short note on what was preserved versus relocated.

### 4) Audit

Use when the job is to judge skill quality, find structural weakness, or prepare an edit/refactor.

Typical asks:

- "Audit this skill."
- "Why is this skill overtriggering?"
- "Is this actually a skill or should it be something else?"

What to do:

1. Read the package as it exists before proposing fixes.
2. Separate trigger failures, packaging failures, and execution failures.
3. Point each finding to the exact layer that should change.

What to return:

- Findings first.
- For each finding: what is wrong, why it matters, and which file or layer should change.

## Mode router

Choose the smallest mode that matches the job:

- No skill yet or only a rough brief: `author`
- Existing skill with a local weakness: `edit`
- Existing skill is useful but structurally wrong: `refactor`
- Need diagnosis before rewriting: `audit`

If unsure, start with `audit`, then either stop with findings or continue into `edit` or `refactor`.

## Four concrete use cases

1. A team has a repeated workflow and wants a reusable skill package. Use `author`.
2. A good skill undertriggers because the description is vague. Use `edit`.
3. A skill works but has become a monolith of checklists and repo-specific trivia. Use `refactor`.
4. An OpenClaw skill needs better gating, install placement, or slash-command semantics. Use `edit` or `audit`.
5. A proposed skill might actually be an `AGENTS.md` note or one-shot prompt. Use `audit`.
