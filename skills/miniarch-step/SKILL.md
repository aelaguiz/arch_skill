---
name: miniarch-step
description: "Operate a faster standalone full-arch workflow against one canonical plan artifact for smaller well-defined features: `new`, `reformat`, `research`, `deep-dive`, `phase-plan`, `auto-plan`, `consistency-pass`, `implement`, `implement-loop`, `auto-implement`, `audit-implementation`, `status`, or `advance`. Use when the work still needs canonical architecture grounding, phased execution, and real auto controllers, but does not need the broader staged surface of `arch-step`. Not for one-pass mini planning, tiny 1-3 phase feature flow, broad or ambiguity-heavy full-arch work, bugs, or open-ended loops."
metadata:
  short-description: "Faster full-arch for smaller features"
---

# Miniarch Step

Use this skill when the user wants the full arch shape and full auto support, but the work is small enough and well-defined enough to run a faster core arc.

The primary object is one canonical full-arch plan doc. `miniarch-step` keeps that artifact discipline, but trims the workflow to the minimum stages that still produce an honest plan, phased execution, and authoritative audit.

## When to use

- The task is a smaller well-defined feature or refactor that still benefits from canonical architecture grounding.
- The user wants phased planning, implementation, and audit against one full-arch doc.
- The work should move faster than `arch-step` because it does not need external research, repeated architecture passes, or extra hardening helpers.
- The user wants real auto controllers rather than one-pass planning only.
- The ask is command-shaped: `new`, `reformat`, `research`, `deep-dive`, `phase-plan`, `auto-plan`, `consistency-pass`, `implement`, `implement-loop`, `auto-implement`, `audit-implementation`, `status`, or `advance`.

## When not to use

- The user wants a read-only router or "what's next?" answer. Use `arch-flow`.
- The user wants one-pass planning only. Use `arch-mini-plan`.
- The task is a tiny 1-3 phase feature flow. Use `lilarch`.
- The task is ambiguity-heavy, migration-heavy, broad, or likely to need external research or extra hardening helpers. Use `arch-step`.
- The remaining job is docs cleanup or consolidation after code work is clean. Use `arch-docs`.
- The problem is primarily a bug or open-ended loop. Use `bugs-flow`, `goal-loop`, or `north-star-investigation`.

## Non-negotiables

- `DOC_PATH` is the primary state. Commands are subordinate to the artifact.
- Every invocation must check both structure and quality before doing command-local work.
- No command may leave the doc less canonical, less honest, or more contradictory than it found it.
- Present-but-weak sections are not done.
- A plan is not ready, complete, or implementation-ready while any unresolved decision remains about requested behavior, adjacent surfaces that must stay in sync, compatibility posture, architecture, canonical owner path, required deletes, fallback policy, acceptance evidence, or implementation scope.
- Correctness and approved intent outrank speed or scope trimming.
- The agent has no authority to cut requested behavior, acceptance criteria, or required implementation work unless the user or the governing plan already marked that item out of scope.
- Section 7 phases should split work into coherent self-contained units, with the most fundamental units first and later phases clearly building on earlier ones.
- If two valid decompositions exist, bias toward more, smaller coherent phases rather than fewer blended phases.
- A phase is not complete while any checklist item or exit criterion in that phase remains unmet.
- For modern Section 7 docs, `Work` is explanatory only. Every required phase obligation must live in `Checklist (must all be done)` or `Exit criteria (all required)`, and fresh audit must validate both before a phase can stay complete.
- During `implement` and `implement-loop`, the approved plan stays authoritative for requirements, scope, acceptance criteria, and phase obligations. Execution may record progress truth, but it may not rewrite the plan to make unfinished work disappear.
- During `implement` and `implement-loop`, execution scope is the full approved Section 7 frontier in order: start from the earliest incomplete or reopened phase and continue through later reachable phases until that frontier is done or a real blocker stops progress.
- Credible proof supports continued implementation. It does not justify stopping after one local fix, one phase, or one convenient subset while later approved phases are still reachable.
- If the doc is materially non-canonical, repair only the safe owned portion or route to `reformat`.
- Keep one planning source of truth. Do not create sidecar plan docs or competing checklists.
- All planning commands are docs-only. Only `implement` and `implement-loop` may change code.
- Distinguish requested behavior scope from architectural convergence scope.
- Search for the canonical existing path before designing a new one. Reuse it, refactor it as much as required to fully own the change, or justify why it cannot own the change.
- Internal convergence work may broaden touched files or nearby adopters when needed to avoid parallel paths or shadow contracts, but it must not invent new product functionality, modes, or speculative infrastructure.
- Any refactor, shared-path extraction, or consolidation must preserve existing behavior and name a credible verification signal before it is considered done.
- Use repo evidence first. Ask only for true product, UX, external-constraint, access, or doc-path gaps.
- If repo evidence cannot settle a plan-shaping decision, ask the user instead of guessing, defaulting, or parking the choice as a pseudo-complete plan.
- Before hardening target architecture or Section 7, inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story.
- Compatibility posture is a first-class plan decision separate from `fallback_policy`.
- When the changed behavior is agent- or LLM-driven, inspect current prompt surfaces, runtime or agent configuration, native model capabilities, and existing tool/file/context exposure before designing.
- For agent-backed systems, prefer prompt engineering, grounding/context shaping, and better use of native capabilities before custom harnesses, wrappers, parsers, OCR stacks, fuzzy matchers, or deterministic sidecars.
- If the real lever is prompt repair, say so plainly and recommend `prompt-authoring` instead of inventing deterministic scaffolding.
- Default to fail-loud boundaries, hard cutover, and explicit deletes. Runtime shims are forbidden unless the plan explicitly approves them.
- `auto-plan` is one command. It either runs a real bounded planning sequence or fails loud.
- `implement-loop` is one command. It either runs a real full-frontier implement-then-audit controller or fails loud.
- Git is the history for retired live truth surfaces. Delete dead competing code paths, stale live docs, and stale comments instead of keeping them for archaeology.
- Broader docs audit, consolidation, and final plan/worklog retirement after a clean code audit belong to `arch-docs`, not to hidden `miniarch-step` commands.
- `status` is compact, read-only, and grounded in the actual artifact.
- `advance` owns the longer checklist surface and optional one-step execution.

## First move

1. Read `references/artifact-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Resolve the requested command and `DOC_PATH` when the command needs an existing doc.
4. If the ask is generic mini full-arch execution rather than a named command:
   - no doc yet: treat the first move as `new`
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
- `phase-plan`
- `auto-plan`
- `consistency-pass`
- `implement`
- `implement-loop`
- `auto-implement`
- `audit-implementation`
- `status`
- `advance`

### Top-level model

`miniarch-step` reasons about one canonical full-arch artifact with this exact shape:

- required frontmatter
- `# TL;DR`
- `planning_passes`
- `# 0)` through `# 10)` with exact canonical headings and subsection structure
- optional helper blocks folded into the same plan doc only when they belong to the mini surface
- `WORKLOG_PATH` once implementation begins

The finished artifact is one internally consistent, decision-complete plan that says the same thing about outcome, requested behavior scope, architectural convergence scope, architecture, verification, rollout, and drift history from multiple angles.

### `advance` selection rule

Choose exactly one next command using this precedence:

1. No plan doc yet: run `new`.
2. Existing doc is not canonical enough to trust: run `reformat`.
3. North Star is still draft or too weak to support planning: stop for confirmation or repair the artifact with `reformat`.
4. After North Star confirmation, stop and wait for the user's explicit next command; do not auto-advance into `research` or any later stage.
5. Earliest required structure or owned block is missing: run the command that repairs it.
6. Required structure exists but the next critical sections are still weak or still contain unresolved decisions: run the command that strengthens them or stop and ask the exact blocker question.
7. Otherwise follow the mini core arc:
   - `new` or `reformat`
   - North Star confirmation
   - `research`
   - `deep-dive`
   - `phase-plan`
   - `consistency-pass`
   - `implement`
   - `audit-implementation`
8. If the code audit is clean and the feature still needs docs cleanup, hand off to `arch-docs`.

Do not auto-run more than one command.

### Explicit controller commands

These stay explicit unless the user directly asks for them:

- `auto-plan`
- `implement-loop`
- `auto-implement`

`auto-plan` is a bounded planning controller. In Codex, `DOC_PATH` is the planning ledger and `.codex/miniarch-step-auto-plan-state.<SESSION_ID>.json` is only the armed controller state for that doc/session. On a fresh doc, the initial `auto-plan` pass arms state, runs only `research` against the same `DOC_PATH`, then ends its turn naturally. On reruns, the parent pass re-arms state against the same `DOC_PATH` and lets the installed Stop hook continue from the first incomplete stage already visible in the doc. It must not self-run `deep-dive`, `phase-plan`, or `consistency-pass` in that same turn. After that first turn, the installed Stop hook owns stage-to-stage continuation: it reads doc truth, feeds exactly one literal next command per later turn, and only after `consistency-pass` clears state and says the doc is decision-complete and ready for `implement-loop`.

User-facing invocation stays simple:

- run `$miniarch-step auto-plan`
- or run `$miniarch-step auto-plan <DOC_PATH>`
- do not run the Stop hook yourself; after the controller is armed, just end the turn and let Codex run the installed Stop hook
- the initial `auto-plan` pass must run only `research`, then end the turn
- rerunning `auto-plan` on a partially complete doc is legal; the hook resumes from the first incomplete stage already visible in `DOC_PATH`
- later planning stages are hook-owned only: `deep-dive`, `phase-plan`, and `consistency-pass`
- the parent `auto-plan` pass must not clear successful controller state, claim the planning arc is complete, or emit the `implement-loop` handoff while any decision gaps remain
- prefer the current session's canonical mini/full-arch doc when `DOC_PATH` is omitted
- preflight the real continuation surface: `~/.codex/hooks.json` must contain the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`, and that installed runner must exist
- keep `.codex/miniarch-step-auto-plan-state.<SESSION_ID>.json` armed for the live run; treat `DOC_PATH` as the progress ledger
- if a stage stops early, clear `.codex/miniarch-step-auto-plan-state.<SESSION_ID>.json` and stop honestly

`implement-loop` is a full-frontier delivery controller. It arms state before implementation work, runs `implement` across the current approved Section 7 frontier in order from the earliest incomplete or reopened phase through later reachable phases, requires credible programmatic proof along the way, then runs `audit-implementation`, and repeats against the same approved `DOC_PATH` until the audit verdict is clean or a real blocker stops progress.

`auto-implement` is an exact user-facing synonym for `implement-loop`. Resolve it to the same controller behavior and keep the internal runtime names, hook state, and file paths under `implement-loop`.

User-facing invocation stays simple:

- run `$miniarch-step implement-loop <DOC_PATH>`
- or run `$miniarch-step auto-implement <DOC_PATH>`
- do not run the Stop hook yourself; after the controller is armed, just end the turn and let Codex run the installed Stop hook
- preflight the real loop surface: `~/.codex/hooks.json` must contain the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`, and that installed runner must exist
- arm `.codex/miniarch-step-implement-loop-state.<SESSION_ID>.json` before implementation work so the live loop cannot be forgotten mid-run
- do not hand control back to audit until the current full ordered implementation frontier is done or genuinely blocked, and its phase claims have credible proof
- keep `.codex/miniarch-step-implement-loop-state.<SESSION_ID>.json` aligned with the live run
- do not clear `.codex/miniarch-step-implement-loop-state.<SESSION_ID>.json` from the implementation side before fresh `audit-implementation` has run, even if the pass believes the work is done
- do not let the parent implementation pass stand in for the clean auditor by writing the authoritative audit block or the `Use $arch-docs` handoff
- when the fresh audit child finishes clean, hand off to `Use $arch-docs`

For any Codex controller state in this skill, derive `<SESSION_ID>` from `CODEX_THREAD_ID` and arm the session-scoped `.codex/...<SESSION_ID>.json` path for the current session.

### Output expectations

- Keep console output high-signal and natural.
- Start with a one-line North Star reminder.
- Then give the punchline plainly.
- Put exhaustive detail in `DOC_PATH` or `WORKLOG_PATH`, not in console output.
- For generic mini full-arch asks that did not name a command, say which command you resolved to and why.
- `status` should emit:
  - one artifact line
  - one line per core stage
  - one best-next-move line
- `advance` should emit:
  - the full ordered checklist with evidence notes
  - the exact next move, even when that handoff is `arch-docs`
  - optional one-step execution only when `RUN=1`

## Reference map

- `references/artifact-contract.md` - canonical mini full-arch artifact, exact section shape, frontmatter, block inventory, and worklog contract
- `references/shared-doctrine.md` - cross-cutting doctrine: question policy, alignment checks, evidence, SSOT, scope defaults, and consistency repair
- `references/section-quality.md` - purpose, strong/weak bar, trust rules, and failure modes for each section and supporting block
- `references/arch-new.md` - bootstrap the canonical artifact and stop for North Star confirmation
- `references/arch-reformat.md` - convert an existing doc into the canonical artifact without losing meaning
- `references/arch-research.md` - research grounding contract
- `references/arch-deep-dive.md` - current architecture, target architecture, call-site audit, and single-pass planning rules
- `references/arch-phase-plan.md` - authoritative phase-plan contract
- `references/arch-auto-plan.md` - bounded planning controller over research, one deep-dive pass, phase-plan, and consistency-pass
- `references/arch-consistency-pass.md` - end-to-end cold-read consistency review before implementation
- `references/arch-implement.md` - implementation, worklog, and completion discipline
- `references/arch-implement-loop.md` - full-frontier implement/audit loop, required runtime preflight, and loop-state contract
- `references/arch-audit-implementation.md` - code-completeness audit and phase reopening
- `references/status.md` - compact artifact-first status rules
- `references/advance.md` - full checklist, next-command selection, and optional one-step execution
