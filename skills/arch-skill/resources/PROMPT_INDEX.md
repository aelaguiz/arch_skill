---
title: arch_skill Prompt Index (Router Map)
purpose: "Map user intent → the correct /prompts:* command, without duplicating prompt bodies."
---

# arch_skill Prompt Index

Principle: prompts are the **procedures**; this index is just routing.

## 0) Setup / normalization
- Create a new plan doc: `/prompts:arch-new <freeform blurb>`
- Reformat an existing doc into canonical template: `/prompts:arch-reformat <path-to-doc.md> [OUT=docs/<...>.md]`
- Flow status / what's next: `/prompts:arch-flow <DOC_PATH>`
- Kickoff (research setup + checkpoints): `/prompts:arch-kickoff <DOC_PATH>`

## 0c) Mini-arch (tiny tasks)
For small features/improvements that can ship in **1–3 phases** (not new architectures, not big migrations):

- Start (new + research + requirements): `/prompts:lilarch-start <freeform request> [docs/<...>.md]`
- Plan (deep dive + plan + audits): `/prompts:lilarch-plan <DOC_PATH>`
- Finish (implement + review): `/prompts:lilarch-finish <DOC_PATH>`

If the work expands beyond 3 phases or is investigation-heavy:
- Switch to `/prompts:arch-flow <DOC_PATH> FLOW=regular` (or)
- Use `/prompts:bugs-analyze <evidence>`

## 0a) Ramp-up (read-only orientation)
- Quick ramp-up: `/prompts:arch-ramp-up <DOC_PATH or guidance>`
- Agent-assisted ramp-up (parallel read-only scans): `/prompts:arch-ramp-up-agent <DOC_PATH or guidance>`

## 0b) Context management
- Context load (derive brief for agent handoff): `/prompts:arch-context-load <DOC_PATH>`

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
- Phase plan granularize (optional; single SSOT microtasks): `/prompts:arch-phase-plan-granularize <DOC_PATH>`
- Phase plan granularize (agent-assisted): `/prompts:arch-phase-plan-granularize-agent <DOC_PATH>`
- Review gate (recommended for risky changes): `/prompts:arch-review-gate <DOC_PATH>`
- Fold in references (inline docs/links into phases): `/prompts:arch-fold-in <DOC_PATH>`
- Plan audit (score readiness across phases): `/prompts:arch-plan-audit <DOC_PATH>`
- Plan audit (agent-assisted): `/prompts:arch-plan-audit-agent <DOC_PATH>`
- Mini plan (one-pass research + deep dive + plan): `/prompts:arch-mini-plan-agent <DOC_PATH>`

## 4) Execution (writes code + worklog)
- Implement phase-by-phase + update worklog: `/prompts:arch-implement <DOC_PATH>`
- Agent-assisted implement: `/prompts:arch-implement-agent <DOC_PATH>`
- Progress update only (no replanning): `/prompts:arch-progress <DOC_PATH>`

## 5) Audits / completion checks
- "Gaps & concerns" audit: `/prompts:arch-audit <DOC_PATH>`
- Agent-assisted audit: `/prompts:arch-audit-agent <DOC_PATH>`
- "Implementation vs plan" audit: `/prompts:arch-audit-implementation <DOC_PATH>`
- Implementation audit (agent-assisted): `/prompts:arch-audit-implementation-agent <DOC_PATH>`

## 6) Automation QA (optional)
- Run automation harness on existing sim/emulator: `/prompts:arch-qa-autotest <DOC_PATH>`

## 7) Utilities
- Reformat doc into canonical structure: `/prompts:arch-reformat <path>`
- ASCII UI mockups (only for UI-touching changes): `/prompts:arch-ui-ascii <DOC_PATH>`

## 8) Bug workflow
- Bug analysis (create/update bug doc, form hypotheses): `/prompts:bugs-analyze <DOC_PATH or evidence>`
- Bug fix (plan + implement + verify): `/prompts:bugs-fix <DOC_PATH>`
- Bug review (external audit of fix): `/prompts:bugs-review <DOC_PATH>`

## 9) Goal-seeking loops
- New goal loop (create SSOT doc + running log): `/prompts:goal-loop-new <freeform goal>`
- Iterate (execute one bet, append to log): `/prompts:goal-loop-iterate <DOC_PATH>`
- Flow (check readiness, recommend next step): `/prompts:goal-loop-flow <DOC_PATH>`
- Context load (write digest for restarts): `/prompts:goal-loop-context-load <DOC_PATH>`

## 10) Debug
- Debug (plan-aware root cause + elegant fix): `/prompts:arch-debug <DOC_PATH or guidance>`
- Brutal debug (fast root cause, temp hacks OK): `/prompts:arch-debug-brutal <DOC_PATH or guidance>`

## 11) Developer experience
- DevX (CLI-output mocks + artifacts): `/prompts:arch-devx <DOC_PATH>`
- DevX (agent-assisted): `/prompts:arch-devx-agent <DOC_PATH>`

## 12) Code review & finalization
- Code review (cross-tool external review, Claude↔Codex): `/prompts:arch-codereview <DOC_PATH + scope>`
- Open PR (merge, preflight, push, open draft PR): `/prompts:arch-open-pr [title/constraints]`

## 13) Rendering
- HTML full-fidelity render: `/prompts:arch-html-full <DOC_PATH>`
- ASCII chart (visualize topic or pipeline): `/prompts:arch-ascii <DOC_PATH or topic>`

## 14) Ralph
- Ralph retarget (bootstrap-safe seed from templates): `/prompts:arch-ralph-retarget <SPEC_PATH>`
- Ralph enhance (re-review + granularize tasks): `/prompts:arch-ralph-enhance <SPEC_PATH>`

## 15) Maestro / QA automation
- Maestro autopilot (run tests, fix, re-run): `/prompts:maestro-autopilot <DOC_PATH or guidance>`
- Maestro rerun last failed flow: `/prompts:maestro-rerun-last`
- Maestro kill (stop stuck runs): `/prompts:maestro-kill`
- QA autopilot (run QA, fix broken flows): `/prompts:qa-autopilot <DOC_PATH or guidance>`

## 16) North Star investigation
- Bootstrap investigation doc: `/prompts:north-star-investigation-bootstrap <ARGUMENTS>`
- Investigation loop (iterate on investigation): `/prompts:north-star-investigation-loop <DOC_PATH>`

## 17) Misc
- New arch from docs (transform requirements folder into plan): `/prompts:new-arch-from-docs <folder or paths>`
