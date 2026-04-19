---
name: prompt-authoring
description: "Write, edit, refactor, or audit prompts so they stay intent-driven, section-correct, and anti-heuristic. Use when a prompt needs stronger commander's intent, cleaner section placement, safer refactoring without losing useful magic, or a findings-first audit."
---

# Prompt Authoring

Use this skill when the work is prompt authoring or prompt repair, not generic writing.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- The user wants a new system prompt, skill prompt, agent prompt, reviewer prompt, or reusable prompt contract.
- The user wants to strengthen an existing prompt without rewriting its entire personality.
- The user wants a prompt refactored so brittle heuristics become examples, rationale, or litmus tests.
- The user wants a findings-first audit of a prompt for myopia, wrong-layer content, weak commander’s intent, or hidden heuristics.

## When not to use

- The task is ordinary copy editing, summarization, or product-spec writing rather than prompt design.
- The user only needs a sentence polished, not a prompt contract repaired.
- The prompt text or binding brief is unavailable and cannot be inspected.

## Non-negotiables

- Push back against heuristic and myopic prompt design aggressively.
- Keep commander’s intent mission-level; push concrete behaviors lower into success/failure, recognition tests, process, and examples.
- Teach principles and recognition tests, not keyword lists, lookup tables, or canned action menus.
- Fix the right section instead of smearing new guidance across the whole prompt.
- Preserve useful prompt magic during refactors by extracting the durable principle and demoting brittle heuristics into examples, rationale, or litmus tests.
- Work only from the prompt and the references listed here; do not assume hidden supporting material.
- If the prompt or needed context is missing, stop and say so instead of inventing context.

## First move

1. Classify the job as `author`, `edit`, `refactor`, or `audit`.
2. Read `references/prompt-pattern-contract.md`.
3. Read the smallest additional reference that matches the job:
   - `references/workflow-and-modes.md` for mode routing and output expectations
   - `references/high-leverage-sections.md` for system context, quality bar, output contracts, and rationale patterns
   - `references/edit-refactor-audit.md` for repair loops, litmus tests, and section-targeting
   - `references/examples-and-anti-examples.md` when you need grounded examples or want to sanity-check framing

## Workflow

1. Lock the single job and the desired outcome before touching wording.
2. Keep commander’s intent and success/failure higher than process mechanics.
3. Make the rich sections carry real weight: system context, quality bar, output contract, and error handling should teach stakes and judgment, not just fill space.
4. Place or repair sections in preferred-pattern order rather than patching opportunistically.
5. Use examples and rationale to illustrate the principle, never to replace the principle.
6. Run the anti-heuristic and hidden-context checks before returning.

## Output expectations

- `author`: return the finished prompt, plus only the shortest note needed to explain any important assumption.
- `edit`: return the patched prompt and a short explanation of which section changed and why.
- `refactor`: return the rewritten prompt and a short note on what useful behavior was preserved versus relocated.
- `audit`: return findings first. Name the issue, why it is risky, and exactly which section should change.

## Reference map

- `references/workflow-and-modes.md` — choose the right mode and keep the output shape honest.
- `references/prompt-pattern-contract.md` — the contract for section order, ownership, and anti-pattern bans.
- `references/high-leverage-sections.md` — how to make system context, quality bar, schema, and rationale sections actually teach.
- `references/edit-refactor-audit.md` — how to repair prompts without flattening them.
- `references/examples-and-anti-examples.md` — real repo-derived examples and anti-examples; use them to teach, not to cargo-cult.
