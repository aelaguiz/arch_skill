# Workflow And Internal Lanes

Always read `prompt-pattern-contract.md` first. Then use this file to choose the
right internal work lane.

These lanes are for the agent, not the user. The user can ask in normal
language: "write me a prompt that does this," "fix this prompt," "make this
less brittle," or "why is this prompt bad?" Do not ask the user to choose a
mode or prompt type before doing useful work.

## The four internal lanes

### 1) Create
Use when there is no prompt yet, or the existing material is just a loose brief.

Typical asks:
- "Write me a prompt that does this."
- "Write a prompt for this assistant."
- "Create a reusable system prompt for this workflow."

What to do:
1. Infer the job, audience, and success criteria from the brief.
2. Identify the lightest prompt shape that will work.
3. Load `prompt-types-and-selection.md` when the prompt needs personality, evidence, drafting, tools, validation, runtime communication, planning, or other type-specific guidance.
4. Use a compact prompt for ordinary one-shot asks.
5. Use the fuller prompt-pattern contract only when reuse, risk, tools, examples, validation, or runtime boundaries justify it.
6. Add assumptions briefly after the prompt when they matter.
7. Run the anti-heuristic and overbuild checks before returning.

What to return:
- The finished prompt.
- Only the shortest note needed for assumptions or open edges.

### 2) Edit
Use when the prompt mostly works but one or two sections are weak, misplaced, or incomplete.

Typical asks:
- "Tighten this prompt."
- "Fix the commander’s intent."
- "Move this guidance to the right section."
- "Make this prompt shorter without losing the behavior."

What to do:
1. Identify the failing section before rewriting.
2. Patch only the section that owns the problem.
3. If the problem is really prompt shape rather than wording, use `prompt-types-and-selection.md` to add only the missing guidance.
4. If the prompt is structurally correct but still thin, inspect `System context`, `Quality bar`, `Output contract`, and `Examples` before touching tone.
5. Re-read the whole prompt for lower-half drift back into heuristics.

What to return:
- The patched prompt.
- A short note saying what changed and where.

### 3) Refactor
Use when the prompt has useful behavior but is structurally wrong, overly heuristic, or brittle.

Typical asks:
- "Refactor this prompt without losing its magic."
- "Turn the heuristics into something more principled."
- "This prompt works but feels overbuilt."

What to do:
1. Identify what behavior is worth preserving.
2. Extract the durable principle that explains that behavior.
3. Move brittle lists, examples, and shortcuts into the lowest layer that still preserves value.
4. Remove unnecessary prompt-type ceremony when a simpler outcome-first prompt would work.
5. Restore commander’s intent, success/failure, and section boundaries.
6. Rebuild any thin rich sections so the prompt still carries stakes, validation, and teachable judgment after the cleanup.

What to return:
- The refactored prompt.
- A short note on what was preserved versus relocated.

### 4) Audit
Use when the job is to judge prompt quality, find structural weaknesses, or prepare a refactor.

Typical asks:
- "Audit this prompt."
- "Why is this prompt still too heuristic?"
- "Why does this prompt keep making stuff up?"

What to do:
1. Read the prompt as-written before proposing fixes.
2. Call out heuristic drift, wrong-layer content, weak commander’s intent, bad examples, phantom context, missing evidence policy, missing stop rules, or overbuilt prompt shape.
3. Point each finding to the exact section or lens that should change.

What to return:
- Findings first.
- For each finding: what is wrong, why it matters, and where the fix belongs.

## Lane router

Choose the smallest internal lane that matches the job:
- No prompt yet or only a rough brief: create
- Existing prompt with a local weakness: edit
- Existing prompt works but is brittle, layered wrong, or overbuilt: refactor
- Need diagnosis before rewriting: audit

If unsure, start by reading the artifact. If the fix is obvious and low-risk,
patch it. If the failure is structural, lead with findings before rewriting.

## Concrete use cases

1. A user says "write me a prompt that helps a support bot decide refunds." Create a compact outcome-first prompt with evidence and escalation rules if the brief implies them.
2. A new reviewer prompt needs the preferred pattern from scratch. Create a reusable contract.
3. A solid prompt starts strong but devolves into keyword rules near the bottom. Refactor the brittle rules into principles, examples, or recognition tests.
4. A prompt feels vague, repetitive, or too local-action-heavy. Audit, then patch only the failing section.
5. A prompt has the right headings but still feels generic and low-agency. Edit or refactor, then deepen the rich sections instead of rewriting everything.
