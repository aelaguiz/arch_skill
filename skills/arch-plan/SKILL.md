---
name: arch-plan
description: "Create, continue, implement, or audit full architecture-plan docs for medium/large changes: North Star setup, research grounding, deep dive, external research, phase plans, local implementation, and implementation audits. Use when a request mentions architecture plans, phased refactors, deep dives, external research, phase plans, implementation audits, or continuing a serious multi-phase plan. Not for the explicit one-step full-arch command surface (`arch-step`), tiny 1-3 phase changes (`lilarch`), one-pass mini plans (`arch-mini-plan`), bug triage (`bugs-flow`), or open-ended optimization loops (`goal-loop`, `north-star-investigation`)."
metadata:
  short-description: "Full arch planning and execution flow"
---

# Arch Plan

Use this skill when the user wants the full arch workflow, not a thin router.

Prompts in this repo are legacy references only. Do not depend on saved prompts at runtime; execute the workflow directly from this skill and its references.

## When to use

- The user wants a full architecture plan or phased refactor for medium/large work.
- The ask mentions research grounding, deep dive, external best-practice research, phase planning, implementation audits, or "do the serious arch flow."
- There is already a canonical `docs/<...>.md` plan and the user wants to continue, implement, audit, or finish it.
- The work is cross-cutting enough that a single SSOT plan doc, call-site audit, and explicit phase sequencing materially reduce risk.

## When not to use

- The work is a tiny 1-3 phase feature or improvement. Use `lilarch`.
- The user wants a compressed one-pass planning pass without the full multi-step arch flow. Use `arch-mini-plan`.
- The task is primarily a bug report, regression, crash, or Sentry investigation. Use `bugs-flow`.
- The goal is open-ended optimization or investigation where the path is unknown. Use `goal-loop` or `north-star-investigation`.
- The user is only asking "what's next?" or wants a checklist/status readout. Use `arch-flow`.
- The user wants the explicit one-step full-arch surface with one stage at a time or a concise stage-quality readout. Use `arch-step`.

## Non-negotiables

- Keep one canonical `DOC_PATH` under `docs/` as the SSOT for planning, architecture, decisions, and phase tracking.
- Treat code as ground truth. Anchor claims in file paths, symbols, tests, logs, or explicit sources.
- Planning passes are docs-only. Do not modify code during doc setup, research, external research, deep dive, plan shaping, or audits.
- Default to local implementation. Do not delegate implementation. If the runtime/user explicitly permits delegation, keep it read-only and limited to planning scans.
- Do not add runtime fallbacks, compatibility shims, placeholder behavior, or silent alternate paths unless the governing doc explicitly approves it with a timeboxed removal plan.
- Ask questions only when repo/docs/tools cannot answer them.

## First move

1. Resolve the mode from the ask:
   - new or repair doc
   - research grounding
   - external research
   - deep dive
   - phase planning / plan shaping
   - implementation / progress
   - implementation audit
2. Read `references/doc-contract.md`.
3. Resolve `DOC_PATH` and read it fully before acting.
4. If the doc is new or still `status: draft`, draft or repair the North Star first and get confirmation before continuing deeper into the flow.

## Workflow

### 1) Route the ask to the right phase

- If the user asks for a specific phase, do that phase only.
- If the user asks for the full flow, default to:
  - create/repair doc
  - research grounding
  - deep dive pass 1
  - external research when the plan touches domains with reusable external best practices
  - deep dive pass 2 when external research materially changes the target architecture
  - phase plan and plan-shaping passes
  - local implementation
  - implementation audit

### 2) Planning modes

- Research grounding:
  - capture internal anchors first
  - add external anchors only when they materially affect correctness or idiomatic design
- Deep dive:
  - update current architecture, target architecture, and call-site audit together
  - keep planning-pass bookkeeping honest but warn-first rather than hard-blocking
- External research:
  - browse only for plan-adjacent topics with broadly reusable guidance
  - use a small topic budget and synthesize how the guidance changes this plan
- Phase planning:
  - write the authoritative depth-first plan
  - tighten it with optional plan-shaping passes only when they add signal

### 3) Execution mode

- Implement against `DOC_PATH` locally and phase-by-phase.
- Maintain `WORKLOG_PATH` as you go.
- Run the smallest credible signal after meaningful changes.
- Keep manual/UI verification as a follow-up unless the plan explicitly makes it code-blocking.

### 4) Audit mode

- Implementation audits are code-completeness audits, not bureaucracy audits.
- Reopen phases only for missing or incorrect code work.
- Missing screenshots or manual QA evidence is non-blocking follow-up unless the plan says otherwise.

## Output expectations

- Update `DOC_PATH` every time the skill materially changes the plan, architecture, implementation status, or audit truth.
- Update `WORKLOG_PATH` during implementation/progress work.
- Keep the console summary short and high-signal:
  - North Star reminder
  - punchline
  - what changed
  - risks or blockers
  - next action
  - pointers to the doc/worklog

## Reference map

- `references/doc-contract.md` - canonical doc, worklog, markers, and status rules
- `references/workflow-details.md` - phase routing, plan-shaping options, and legacy prompt coverage
