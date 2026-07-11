---
name: lilarch
description: "Run the standalone small-feature 1-3 phase flow: create or repair a compact plan doc, lock requirements and defaults, write a tight implementation plan, implement locally, and self-audit. Use when a request is a contained feature or improvement that can realistically ship in 1-3 phases. Not for full-arch work, one-pass mini plans, bug investigations, or open-ended loops."
metadata:
  short-description: "Compact 1-3 phase feature flow"
---

# Lilarch

Use this skill for contained feature work that is too small for the full arch flow but still benefits from a real doc-backed plan.

## When to use

- The change is a small feature or improvement.
- The work should fit in 1-3 phases.
- The user wants the "little arch" workflow rather than the full arch plan.

## When not to use

- The task is a migration, a broad refactor, or clearly larger than 3 phases.
- The user wants a compressed one-pass arch plan instead of a start/plan/finish flow. Use `arch-mini-plan`.
- The user wants the full arch workflow or the doc already behaves like a full-arch artifact. Use `miniarch-step` or `arch-step`.
- Investigation dominates because the root cause is unknown. Use `bugs-flow` or `north-star-investigation`.

## Non-negotiables

- Keep one compact `DOC_PATH` as the SSOT for the change.
- Keep a compact Scope and Simplicity Contract in that doc: human outcome and
  anchors, smallest sufficient solution, initial minimal convergence closure or
  `none`, scope freeze, enough proof, do-not-build boundary, and accepted
  residual risk.
- Start and plan modes are docs-only. Code changes only happen in finish mode.
- Ask the small set of clarifying questions that must be answered before planning. Do not bulldoze past unresolved requirements.
- Keep the plan to 1-3 phases. If it grows beyond that, escalate instead of pretending the fit is still good.
- Initial architecture may include only the smallest evidenced same-contract
  convergence closure before plan mode declares readiness. Finish mode and
  self-review cannot expand it; later scope requires explicit human approval.
- `Local` means the active host owns execution and integration; it does not
  require one conversation thread. The parent may use new clean same-host
  native children for genuinely independent repo mapping, plan or completion
  review, and non-overlapping low-collision implementation slices.
- In Codex, start those clean children with `fork_turns: "none"`; in Claude
  Code, use clean named or custom subagents rather than a conversation fork.
  Mapping and review children are read-only by capability when available and
  always receive explicit no-edit/no-write guidance. The parent records and
  rechecks repo state, owns doc/worklog updates, and integrates every return.
- Give editful children explicit non-overlapping owner paths. Resume the exact
  implementer handle for authorized repair of its own slice; start an
  independent recheck as a new clean child. Children do not fan out unless the
  parent explicitly assigns a bounded nested scope and budget, and total
  fanout stays proportional to independent work, host slots, collision risk,
  and parent integration capacity.
- External review or work remains available when a concrete provider,
  load-bearing exact model/profile, lifecycle, isolation, automation, or
  receipt benefit is worth the extra process and integration cost. State that
  benefit when choosing the lane instead of treating external execution as
  the meaning of review freshness.
- When the changed behavior is agent- or LLM-driven, inspect prompt surfaces, native model capabilities, and existing tool/file/context exposure before designing.
- For agent-backed systems, prefer prompt engineering, grounding, and native-capability use before new harnesses, wrappers, parsers, OCR layers, or scripts.
- If the real lever is prompt repair, say so plainly and recommend `prompt-authoring` instead of inventing deterministic scaffolding.
- When source material includes prompts, agent instructions, or other instruction-bearing doctrine, preserve explicit structure by default instead of silently condensing it.
- No runtime fallbacks or compatibility shims unless explicitly approved in the doc.
- Escalation out of lilarch defaults to `miniarch-step reformat`, and then to `arch-step reformat` when the work is broader or more ambiguous than the faster full-arch tier.

## First move

1. Read `references/doc-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Read `../_shared/scope-and-convergence.md`.
4. Before creating or resuming another agent, read
   `../_shared/agent-orchestration-policy.md`.
5. Resolve whether you are in:
   - start mode
   - plan mode
   - finish mode
6. Resolve `DOC_PATH` and read it fully if it exists.
7. Check that the work still fits `lilarch`.
8. Read the mode reference and `references/quality-bar.md`.

## Workflow

### 1) Start mode

- Create or repair the compact plan doc.
- Draft the North Star, requirements, non-requirements, defaults, and the small list of clarifying questions.
- Stop for answers if those questions are required to plan safely.

### 2) Plan mode

- Update the minimal research grounding.
- Write the current architecture, target architecture, call-site audit, and a 1-3 phase plan.
- Run the internal lilarch plan audit, directly or through a clean native
  read-only reviewer, and let the parent tighten the doc before implementation.
- Freeze the compact scope contract before entering finish mode.

### 3) Finish mode

- Implement under active-host ownership against the doc, optionally assigning
  clean native children only non-overlapping low-collision slices.
- Keep a lightweight `WORKLOG_PATH`.
- Self-audit for completeness and mark the doc complete only when the code is actually complete.
- Subtract unauthorized built scope; do not rewrite the compact doc to bless it.

## Output expectations

- Update `DOC_PATH` in every mode.
- Update `WORKLOG_PATH` during finish mode.
- Keep the console summary short and practical:
  - North Star reminder
  - punchline
  - what changed
  - blockers or remaining questions
  - next action

## Reference map

- `references/doc-contract.md` - lilarch artifact, required blocks, status rules, worklog, and escalation rules
- `references/shared-doctrine.md` - small-feature doctrine, question policy, and anti-fallback rules
- `../_shared/agent-orchestration-policy.md` - transport, context,
  continuation, isolation, topology, and return evidence for optional native
  or external child work
- `references/start.md` - create or repair the compact doc and lock requirements/defaults
- `references/plan.md` - write the compact architecture blocks and 1-3 phase plan
- `references/finish.md` - implement, keep the worklog honest, and self-audit
- `references/quality-bar.md` - strong vs weak requirements, plan, plan audit, and finish-mode completion bars
