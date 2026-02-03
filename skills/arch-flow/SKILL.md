---
name: arch-flow
description: "Flow status + next-step router for the arch_skill prompt suite. Use when the user asks 'what’s next?', wants a checklist, or wants you to advance the flow automatically."
---

# arch-flow

This skill is a thin wrapper around `/prompts:arch-flow`.

## When to use
- The user asks “what’s next?”, “continue”, “where are we in the flow?”, or explicitly says `arch-flow`.
- You want a deterministic next-step recommendation based on `DOC_PATH` contents, not memory.

## What to do
1) Resolve `DOC_PATH` (prefer an explicit `docs/<...>.md` path).
2) Run `/prompts:arch-flow DOC_PATH` to produce:
   - A checklist (regular + mini flow statuses),
   - A single recommended next `/prompts:*` command.
3) Offer to proceed:
   - If the user says yes (or asks you to run it), execute the recommended next command.
   - If they want it fully automatic, rerun `/prompts:arch-flow DOC_PATH RUN=1`.

## Invariants
- Use the plan doc (`DOC_PATH`) as the source of truth.
- Do not invent steps or ask questions that can be answered from the repo/doc.
