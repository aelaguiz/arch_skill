---
name: arch-step
description: "Operate the standalone full-arch workflow against one canonical plan artifact and explicit doctrine: `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `auto-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `review-gate`, `implement`, `implement-loop`, `auto-implement`, `audit-implementation`, `status`, or `advance`. Use when the user wants the full arch workflow, a specific full-arch step, or concise full-arch status for work that may require architectural convergence onto canonical repo paths. Internal refactors may widen enough to remove duplicate truth or parallel paths, but the skill must not invent new product functionality, modes, or speculative infrastructure. Not for read-only checklist routing, mini plans, lilarch, bugs, or open-ended loops."
metadata:
  short-description: "Standalone full-arch operator"
---

# Arch Step

Use this skill when the user wants the real full-arch workflow and one canonical plan doc should govern it end to end.

The primary object is one canonical full-arch plan doc. Commands exist to move that doc toward a finished, internally consistent artifact. They are not independent mini-workflows.

## When to use

- The user wants the full arch workflow for medium or large work and does not need a different workflow family.
- The ask is generic full arch language such as "do the full arch flow," "continue this architecture doc," "implement the plan," or "audit implementation against the plan."
- The work needs one canonical plan doc plus real architectural convergence onto existing repo patterns, shared code paths, or single-source-of-truth boundaries.
- The user wants explicit stage control instead of a more holistic or phase-family-driven flow.
- The ask is command-shaped: `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `auto-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `review-gate`, `implement`, `implement-loop`, `auto-implement`, `audit-implementation`, `status`, or `advance`.
- The user wants one specific plan-doc shape with exact headings, stable markers, and consistent stage ownership.
- The user wants `advance` to print the full checklist, choose exactly one next command, and optionally execute that one step.
- The user wants `status` to evaluate the actual plan artifact, not emit a generic checklist.

## When not to use

- The user wants a read-only router or "what's next?" answer. Use `arch-flow`.
- The remaining job is docs cleanup or consolidation after full-arch code work is clean. Use `arch-docs`; it can use the current plan/worklog as context.
- The task is a one-pass mini plan, a 1-3 phase small-feature flow, a bug flow, or an open-ended loop. Use `arch-mini-plan`, `lilarch`, `bugs-flow`, `goal-loop`, or `north-star-investigation`.
- The user is asking which arch skill to use. Use `arch-skills-guide`.

## Non-negotiables

- `DOC_PATH` is the primary state. Commands are subordinate to the artifact.
- Every invocation must check both structure and quality before doing command-local work.
- No command may leave the doc less canonical, less honest, or more contradictory than it found it.
- Present-but-weak sections are not done.
- If the doc is materially non-canonical, repair only the safe owned portion or route to `reformat`.
- Keep one planning source of truth. Do not create sidecar plan docs or competing checklists.
- All planning commands are docs-only. Only `implement` and `implement-loop` may change code.
- Distinguish requested behavior scope from architectural convergence scope. Requested behavior scope governs user-visible behavior. Architectural convergence scope covers internal refactors needed to route the ask through canonical paths, remove duplicate truth, and prevent drift.
- Search for the canonical existing path before designing a new one. Reuse it, minimally refactor it, or justify why it cannot own the change.
- Internal convergence work may broaden touched files or nearby adopters when needed to avoid parallel paths or shadow contracts, but it must not invent new product functionality, modes, or speculative infrastructure.
- Any refactor, shared-path extraction, or consolidation must preserve existing behavior and name a credible verification signal before it is considered done.
- Use repo evidence first. Ask only for true product, UX, external-constraint, access, or doc-path gaps.
- When the changed behavior is agent- or LLM-driven, inspect current prompt surfaces, runtime or agent configuration, native model capabilities, and existing tool/file/context exposure before designing. If that capability picture is still unclear after inspection, ask narrowly instead of assuming the agent cannot do it.
- For agent-backed systems, prefer prompt engineering, grounding/context shaping, and better use of native capabilities before custom harnesses, wrappers, parsers, OCR stacks, fuzzy matchers, or deterministic sidecars.
- Any new tooling for agent-backed behavior must justify why prompt-first and capability-first options were insufficient, and it must augment the agent instead of replacing the reasoning the product is supposed to get from the model.
- If the real lever is prompt repair, say so plainly and recommend `prompt-authoring` instead of inventing deterministic scaffolding.
- When porting agent instructions, prompt doctrine, or other instruction-bearing content, preserve explicit operational structure by default. Do not silently condense ordered steps, conditions, hard negatives, or escalation logic unless the artifact records why that condensation is safe and keeps the source text recoverable.
- Default to fail-loud boundaries, hard cutover, and explicit deletes. Runtime shims are forbidden unless the plan explicitly approves them.
- `auto-plan` is one command. It either runs a real bounded planning sequence or fails loud. Prompt-only chaining does not count as the feature.
- `implement-loop` is one command. It either runs a real bounded implement-then-audit loop or fails loud. Prompt-only repetition does not count as the feature.
- Git is the history for retired live truth surfaces. Do not preserve dead competing code paths, stale live docs, or stale comments for posterity. Delete them. If a touched doc, comment, or instruction still matters after the change, update it to current reality in the same run.
- Broader docs audit, consolidation, and final plan/worklog retirement after a clean full-arch code audit belong to `arch-docs`, not to extra hidden `arch-step` commands.
- Core commands apply scope-triage and convergence rules even when helper commands are not run.
- `advance` must choose from structure first, quality second, stage order third. Helper commands stay explicit.
- `status` is compact, read-only, and grounded in the actual artifact.
- `advance` owns the longer checklist surface and optional one-step execution.

## First move

1. Read `references/artifact-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Resolve the requested command and `DOC_PATH` when the command needs an existing doc.
4. If the ask is generic full-arch execution rather than a named command:
   - no full-arch doc yet: treat the first move as `new`
   - doc exists or the user gave a doc path: treat the first move as `advance`
5. Inspect the current doc against:
   - required frontmatter
   - `# TL;DR`
   - `planning_passes`
   - exact canonical headings
   - command-owned blocks
   - obvious contradictions across TL;DR, Section 0, target architecture, call-site audit, phase plan, verification, rollout, and decision log
   - canonical-path ownership and behavior-preservation claims
6. Read `references/section-quality.md` for the sections this command depends on.
7. Read the matching command reference.
8. If the command is `advance`, read `references/advance.md`, choose the one move that most improves artifact integrity or flow progress, and stop unless `RUN=1` explicitly asks for that one step to execute.

## Workflow

### Public command surface

- `new`
- `reformat`
- `research`
- `deep-dive`
- `external-research`
- `phase-plan`
- `auto-plan`
- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `review-gate`
- `implement`
- `implement-loop`
- `auto-implement`
- `audit-implementation`
- `status`
- `advance`

### Top-level model

`arch-step` always reasons about one canonical full-arch artifact with this exact shape:

- required frontmatter
- `# TL;DR`
- `planning_passes`
- `# 0)` through `# 10)` with exact canonical headings and subsection structure
- optional helper blocks folded into the same plan doc
- `WORKLOG_PATH` once implementation begins

The finished artifact is not just a heading set. It is one internally consistent plan that says the same thing about outcome, requested behavior scope, architectural convergence scope, architecture, verification, rollout, and drift history from multiple angles.

### `advance` selection rule

Choose exactly one next command using this precedence:

1. No plan doc yet: run `new`.
2. Existing doc is not canonical enough to trust: run `reformat`.
3. North Star is still draft or too weak to support planning: stop for confirmation or repair the artifact with `reformat`.
4. Earliest required structure or owned block is missing: run the command that repairs it.
5. Required structure exists but the next critical sections are still weak: run the command that strengthens them.
6. Otherwise follow the canonical core arc:
   - `new` or `reformat`
   - North Star confirmation
   - `research`
   - `deep-dive`
   - `external-research` when warranted
   - `deep-dive` again when external research materially changed the design
   - `phase-plan`
   - `implement`
   - `audit-implementation`
7. If the code audit is clean and the feature still needs docs cleanup, hand off to `arch-docs`.

Do not auto-run more than one command.

### Helper commands

These stay explicit and do not auto-run from `advance`:

- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `review-gate`

Default placement is after `phase-plan` and before `implement`, unless the user explicitly asks otherwise. They are extra hardening surfaces, not the only place where scope, convergence, or preservation discipline exists.

### Explicit controller commands

These stay explicit unless the user directly asks for them:

- `auto-plan`
- `implement-loop`
- `auto-implement`

`auto-plan` is a bounded planning controller. It runs `research`, then `deep-dive`, then `deep-dive` again, then `phase-plan` against the same `DOC_PATH`, then stops and says the doc is ready for `implement-loop`. The user-facing command stays simple:

- run `$arch-step auto-plan`
- or run `$arch-step auto-plan <DOC_PATH>`
- prefer the current session's canonical full-arch doc when `DOC_PATH` is omitted
- if the installed runtime support is absent, disabled, or the North Star is still unapproved, name the broken prerequisite and stop
- keep `.codex/auto-plan-state.json` aligned with the live run
- if a stage stops early, clear `.codex/auto-plan-state.json` and stop honestly

`implement-loop` is a bounded delivery controller. It runs `implement`, requires the implementation pass to prove its claimed fixes with credible programmatic signals, then runs `audit-implementation`, and repeats against the same `DOC_PATH` until the audit verdict is clean or a real blocker stops progress. Prefer a fresh audit context when the host runtime offers a truly isolated child session, subprocess, or subagent. Do not turn it into a generic open-ended loop.

`auto-implement` is an exact user-facing synonym for `implement-loop`. Resolve it to the same controller behavior and keep the internal runtime names, hook state, and file paths under `implement-loop`.

User-facing invocation stays simple:

- run `$arch-step implement-loop <DOC_PATH>`
- or run `$arch-step auto-implement <DOC_PATH>`
- do not introduce a second command, mode, or user-facing control surface
- if the installed runtime support is absent or disabled, name the broken prerequisite and stop
- do not hand control back to audit until the current implementation pass has credible proof for its claimed fixes
- keep `.codex/implement-loop-state.json` aligned with the live run
- if a real blocker appears before stopping, clear `.codex/implement-loop-state.json` and stop honestly
- when the loop finishes clean, hand off to `Use $arch-docs`

### Output expectations

- Keep console output high-signal and natural.
- Start with a one-line North Star reminder.
- Then give the punchline plainly.
- Put exhaustive detail in `DOC_PATH` or `WORKLOG_PATH`, not in console output.
- For generic full-arch asks that did not name a command, say which command you resolved to and why.
- `status` should emit:
  - one artifact line
  - one line per core stage
  - one helper summary line
  - one best-next-move line
- `advance` should emit:
  - the full ordered checklist with evidence notes
  - the exact next move, even when that handoff is `arch-docs`
  - optional one-step execution only when `RUN=1`

## Reference map

- `references/artifact-contract.md` - canonical full-arch plan artifact, exact section shape, frontmatter, block inventory, and worklog contract
- `references/shared-doctrine.md` - cross-cutting doctrine: question policy, alignment checks, evidence, SSOT, scope defaults, and consistency repair
- `references/section-quality.md` - purpose, strong/weak bar, trust rules, and failure modes for each section and supporting block
- `references/arch-new.md` - bootstrap the canonical artifact and stop for North Star confirmation
- `references/arch-reformat.md` - convert an existing doc into the canonical artifact without losing meaning
- `references/arch-research.md` - research grounding contract
- `references/arch-deep-dive.md` - current architecture, target architecture, call-site audit, and planning-pass rules
- `references/arch-external-research.md` - external research contract and plan-integration rules
- `references/arch-phase-plan.md` - authoritative phase-plan contract
- `references/arch-auto-plan.md` - bounded planning controller over research, deep-dive twice, and phase-plan
- `references/arch-plan-enhance.md` - best-possible hardening of the main plan
- `references/arch-fold-in.md` - fold references into the main artifact and wire them into phases
- `references/arch-overbuild-protector.md` - explicit scope triage and remediation using the same rubric core commands should already apply
- `references/arch-review-gate.md` - local idiomatic and completeness review
- `references/arch-implement.md` - implementation, worklog, and completion discipline
- `references/arch-implement-loop.md` - bounded implement/audit loop, required runtime preflight, and loop-state contract
- `references/arch-audit-implementation.md` - code-completeness audit and phase reopening
- `references/status.md` - compact artifact-first status rules
- `references/advance.md` - full checklist, next-command selection, and optional one-step execution
