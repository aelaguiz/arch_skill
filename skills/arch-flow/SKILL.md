---
name: arch-flow
description: "Read-only flow-status and next-step router for arch-plan, arch-mini-plan, and lilarch docs. Use when the user asks 'what's next?', wants a checklist, wants to continue a plan doc, or wants the single best next move without re-running the whole planning workflow. Not for doing the planning or implementation work itself."
---

# arch-flow

Use this skill to inspect an existing arch-style doc and recommend the next move.

Read `references/checklist-rules.md` before building the checklist.

## When to use
- The user asks "what's next?", "continue", "where are we in the flow?", or wants a checklist.
- You want a deterministic next-step recommendation from `DOC_PATH` and `WORKLOG_PATH`, not memory.
- The doc is part of the full arch flow, the arch-mini-plan path, or the lilarch flow.

## When not to use

- The user wants you to actually perform research, planning, implementation, or auditing. Use `arch-plan` or `lilarch`.
- The doc is a bug doc or a goal-loop doc. Use the governing skill for that workflow family.

## What to do

1. Resolve `DOC_PATH` and the derived `WORKLOG_PATH`.
2. Infer whether the doc is:
   - full arch
   - arch-mini-plan follow-through
   - lilarch
3. Build a full evidence-based checklist:
   - mark each required step `DONE`, `PENDING`, `OPTIONAL`, or `UNKNOWN`
   - include the evidence note for each line
4. Recommend the single best next move:
   - `arch-plan` for full arch steps
   - `arch-plan` for post-mini-plan continuation into implementation or audits
   - `lilarch` for lilarch steps
5. If the user asks to run the next step, switch to the governing skill and do the work there.

## Invariants
- Use the plan doc (`DOC_PATH`) as the source of truth.
- Keep this skill read-only unless the user explicitly asks you to proceed into the next step.
- Do not invent steps or ask questions that can be answered from the repo/doc.

## Reference map

- `references/checklist-rules.md` - flow detection and evidence-based checklist rules
