# Workflow And Modes

Always read `prompt-pattern-contract.md` first. Then use this file to choose the right lane.

## The four supported modes

### 1) Author
Use when there is no prompt yet, or the existing material is just a loose brief.

Typical asks:
- "Write a prompt for this agent."
- "Create a reusable system prompt for this workflow."

What to do:
1. State the single job.
2. Lock commander’s intent, success/failure, and non-goals.
3. Make system context explain the downstream user or system moment, not just the abstract workflow.
4. Make the quality bar, output contract, and reject handling concrete enough to guide judgment.
5. Add rationale patterns when the prompt asks the model to choose between plausible options or verify risky claims.
6. Build the prompt in preferred-pattern order.
7. Run the anti-heuristic checklist before returning.

What to return:
- The full prompt.
- Only the shortest note needed for assumptions or open edges.

### 2) Edit
Use when the prompt mostly works but one or two sections are weak, misplaced, or incomplete.

Typical asks:
- "Tighten this prompt."
- "Fix the commander’s intent."
- "Move this guidance to the right section."

What to do:
1. Identify the failing section before rewriting.
2. Patch only the section that owns the problem.
3. If the prompt is structurally correct but still thin, inspect `System context`, `Quality bar`, `Output contract`, and `Examples` before touching tone.
4. Re-read the whole prompt for lower-half drift back into heuristics.

What to return:
- The patched prompt.
- A short note saying what changed and where.

### 3) Refactor
Use when the prompt has useful behavior but is structurally wrong, overly heuristic, or brittle.

Typical asks:
- "Refactor this prompt without losing its magic."
- "Turn the heuristics into something more principled."

What to do:
1. Identify what behavior is worth preserving.
2. Extract the durable principle that explains that behavior.
3. Move brittle lists, examples, and shortcuts into the lowest layer that still preserves value.
4. Restore commander’s intent, success/failure, and section boundaries.
5. Rebuild any thin rich sections so the prompt still carries stakes, validation, and teachable judgment after the cleanup.

What to return:
- The refactored prompt.
- A short note on what was preserved versus relocated.

### 4) Audit
Use when the job is to judge prompt quality, find structural weaknesses, or prepare a refactor.

Typical asks:
- "Audit this prompt."
- "Why is this prompt still too heuristic?"

What to do:
1. Read the prompt as-written before proposing fixes.
2. Call out heuristic drift, wrong-layer content, weak commander’s intent, bad examples, or phantom context.
3. Point each finding to the exact section that should change.

What to return:
- Findings first.
- For each finding: what is wrong, why it matters, and where the fix belongs.

## Mode router

Choose the smallest mode that matches the job:
- No prompt yet or only a rough brief: `author`
- Existing prompt with a local weakness: `edit`
- Existing prompt works but is brittle or layered wrong: `refactor`
- Need diagnosis before rewriting: `audit`

If unsure, start with `audit`, then either stop with findings or continue into `edit` or `refactor`.

## Three concrete use cases

1. A new reviewer prompt needs the preferred pattern from scratch. Use `author`.
2. A solid prompt starts strong but devolves into keyword rules near the bottom. Use `refactor`.
3. A prompt feels vague, repetitive, or too local-action-heavy. Use `audit`, then patch only the failing section.
4. A prompt has the right headings but still feels generic and low-agency. Use `edit` or `refactor`, then deepen the rich sections instead of rewriting everything.
