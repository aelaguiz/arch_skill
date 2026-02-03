---
title: arch_skill Prompt Index (Router Map)
purpose: "Map user intent → the correct /prompts:* command, without duplicating prompt bodies."
---

# arch_skill Prompt Index

Principle: prompts are the **procedures**; this index is just routing.

## 0) Setup / normalization
- Create a new plan doc: `/prompts:arch-new <freeform blurb>`
- Reformat an existing doc into canonical template: `/prompts:arch-reformat <path-to-doc.md> [OUT=docs/<...>.md]`
- Flow status / what’s next: `/prompts:arch-flow <DOC_PATH>`

## 0a) Ramp-up (read-only orientation)
- Quick ramp-up: `/prompts:arch-ramp-up <DOC_PATH or guidance>`
- Agent-assisted ramp-up (parallel read-only scans): `/prompts:arch-ramp-up-agent <DOC_PATH or guidance>`

## 1) Research grounding (planning-only)
- Write Research Grounding into DOC_PATH: `/prompts:arch-research <DOC_PATH>`
- Agent-assisted research grounding: `/prompts:arch-research-agent <DOC_PATH>`
- External research (browse only if truly needed): `/prompts:arch-external-research-agent <DOC_PATH>`

## 2) Architecture deep dive (planning-only)
- Current/Target architecture + call-site audit: `/prompts:arch-deep-dive <DOC_PATH>`
- Agent-assisted deep dive (parallel read-only): `/prompts:arch-deep-dive-agent <DOC_PATH>`

## 3) Implementation planning (planning-only)
- Harden plan (optional): `/prompts:arch-plan-enhance <DOC_PATH>`
- Generate depth-first phased plan: `/prompts:arch-phase-plan <DOC_PATH>`
- Agent-assisted phase plan: `/prompts:arch-phase-plan-agent <DOC_PATH>`
- Review gate (recommended for risky changes): `/prompts:arch-review-gate <DOC_PATH>`

## 4) Execution (writes code + worklog)
- Implement phase-by-phase + update worklog: `/prompts:arch-implement <DOC_PATH>`
- Agent-assisted implement: `/prompts:arch-implement-agent <DOC_PATH>`
- Progress update only (no replanning): `/prompts:arch-progress <DOC_PATH>`

## 5) Audits / completion checks
- “Gaps & concerns” audit: `/prompts:arch-audit <DOC_PATH>`
- “Implementation vs plan” audit: `/prompts:arch-audit-implementation <DOC_PATH>`

## 6) Automation QA (optional)
- Run automation harness on existing sim/emulator: `/prompts:arch-qa-autotest <DOC_PATH>`

## 7) Utilities
- Reformat doc into canonical structure: `/prompts:arch-reformat <path>`
- ASCII UI mockups (only for UI-touching changes): `/prompts:arch-ui-ascii <DOC_PATH>`
