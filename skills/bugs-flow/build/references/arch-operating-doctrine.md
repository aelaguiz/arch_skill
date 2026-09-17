# Arch Skill Operating Doctrine

Shared operating doctrine for arch_skill. This document owns cross-skill planning and architecture rules that are easy to drift when copied locally. Local skills may add narrower consequences, but they do not redefine these policies.

## Question policy

Before asking the user any plan-shaping question, consult approved intent on the governing artifact (North Star, TL;DR, phase frontier). Only ask when intent plus repo evidence genuinely leave two credible branches. Record intent-derived resolutions in the Decision Log.

- If repo evidence cannot settle a plan-shaping decision, ask the user instead of guessing, defaulting, or parking the choice as a pseudo-complete plan.
- Ask only for true product, UX, external-constraint, access, or doc-path gaps.

## Evidence first

Use repo evidence first. Inspect current surfaces, runtime configuration, native capabilities, and existing tool/file/context exposure before designing.

- If the capability picture is still unclear after inspection, ask narrowly instead of assuming the agent cannot do it.
- Any new tooling for agent-backed behavior must justify why prompt-first and capability-first options were insufficient, and it must augment the agent instead of replacing the reasoning the product is supposed to get from the model.
- If the real lever is prompt repair, say so plainly and recommend `$prompt-authoring` instead of inventing deterministic scaffolding.

## Scope triage

Distinguish requested behavior scope from architectural convergence scope. Requested behavior scope governs user-visible behavior. Architectural convergence scope covers internal refactors needed to route the ask through canonical paths, remove duplicate truth, and prevent drift.

- Search for the canonical existing path before designing a new one. Reuse it, refactor it as much as required to fully own the change, or justify why it cannot own the change.
- Internal convergence work may broaden touched files or nearby adopters when needed to avoid parallel paths or shadow contracts, but it must not invent new product functionality, modes, or speculative infrastructure.
- Any refactor, shared-path extraction, or consolidation must preserve existing behavior and name a credible verification signal before it is considered done.

## Architectural convergence

Before hardening target architecture or the phase plan, inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story. Include them now, explicitly defer or exclude them, or ask the exact blocker question when repo truth and approved intent do not settle the disposition.

- Correctness and approved intent outrank speed, scope trimming, or minimum implementation.
- The agent has no authority to cut requested behavior, acceptance criteria, or required implementation work unless the user or the governing plan already marked that item out of scope.
- Cutting, downgrading, deferring, or simplifying away approved behavior, acceptance criteria, or phase obligations is a hard stop. Surface to the user with what you want to cut, why, what the governing artifact says about it, and the exact approval you need. Do not proceed until the user explicitly approves.

## Compatibility posture

Compatibility posture is a first-class plan decision separate from `fallback_policy`. Resolve whether the change preserves the existing contract, performs a clean cutover, or uses an explicitly approved timeboxed bridge. Do not silently assume backward compatibility just because it feels safer.

- Default to fail-loud boundaries, hard cutover, and explicit deletes. Runtime shims are forbidden unless the plan explicitly approves them.

## Prompt-first over harness

For agent-backed systems, prefer prompt engineering, grounding/context shaping, and better use of native capabilities before custom harnesses, wrappers, parsers, OCR stacks, fuzzy matchers, or deterministic sidecars.

- When porting agent instructions, prompt doctrine, or other instruction-bearing content, preserve explicit operational structure by default. Do not silently condense ordered steps, conditions, hard negatives, or escalation logic unless the artifact records why that condensation is safe and keeps the source text recoverable.

## Plan integrity

A plan is not ready, complete, or implementation-ready while any unresolved decision remains about requested behavior, adjacent surfaces that must stay in sync, compatibility posture, architecture, canonical owner path, required deletes, fallback policy, acceptance evidence, or implementation scope.

- Present-but-weak sections are not done.
- All planning commands are docs-only. Only `implement` and `implement-loop` may change code.
- Git is the history for retired live truth surfaces. Do not preserve dead competing code paths, stale live docs, or stale comments for posterity. Delete them. If a touched doc, comment, or instruction still matters after the change, update it to current reality in the same run.
- Phase plans should split work into coherent self-contained units, with the most fundamental units first and later phases clearly building on earlier ones. If two valid decompositions exist, bias toward more, smaller coherent phases rather than fewer blended phases.
- A phase is not complete while any checklist item or exit criterion in that phase remains unmet.

## Implementation discipline

During `implement` and `implement-loop`, the approved plan stays authoritative for requirements, scope, acceptance criteria, and phase obligations. Execution may record progress truth, but it may not rewrite the plan to make unfinished work disappear.

- Execution scope is the full approved phase frontier in order: start from the earliest incomplete or reopened phase and continue through later reachable phases until that frontier is done or a real blocker stops progress.
- Credible proof supports continued implementation. It does not justify stopping after one local fix, one phase, or one convenient subset while later approved phases are still reachable.
- `implement-loop` is one command. It either runs a real full-frontier implement-then-audit controller or fails loud. Prompt-only repetition does not count as the feature.
- `auto-plan` is one command. It either runs a real bounded planning sequence or fails loud. Prompt-only chaining does not count as the feature.
