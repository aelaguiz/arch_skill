---
name: arch-step
description: "Operate the standalone full-arch workflow against one canonical plan artifact and explicit doctrine: `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `auto-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `consistency-pass`, `review-gate`, `implement`, `implement-loop`, `auto-implement`, `audit-implementation`, `status`, or `advance`. Use when the user wants the full arch workflow, a specific full-arch step, or concise full-arch status for work that may require architectural convergence onto canonical repo paths. Internal refactors may widen enough to remove duplicate truth or parallel paths, but the skill must not invent new product functionality, modes, or speculative infrastructure. Not for read-only checklist routing, mini plans, lilarch, bugs, or open-ended loops."
metadata:
  short-description: "Standalone full-arch operator"
---

# Arch Step

Use this skill when the user wants the real full-arch workflow and one canonical plan doc should govern it end to end.

The primary object is one canonical full-arch plan doc. Commands exist to move that doc toward a finished, internally consistent, decision-complete artifact. They are not independent mini-workflows.

## When to use

- The user wants the full arch workflow for medium or large work and does not need a different workflow family.
- The ask is generic full arch language such as "do the full arch flow," "continue this architecture doc," "implement the plan," or "audit implementation against the plan."
- The work needs one canonical plan doc plus real architectural convergence onto existing repo patterns, shared code paths, or single-source-of-truth boundaries.
- The user wants explicit stage control instead of a more holistic or phase-family-driven flow.
- The ask is command-shaped: `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `auto-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `consistency-pass`, `review-gate`, `implement`, `implement-loop`, `auto-implement`, `audit-implementation`, `status`, or `advance`.
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
- A plan is not ready, complete, or implementation-ready while any unresolved decision remains about requested behavior, adjacent surfaces that must stay in sync, compatibility posture, architecture, canonical owner path, required deletes, fallback policy, acceptance evidence, or implementation scope.
- Correctness and approved intent outrank speed, scope trimming, or "minimum implementation."
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
- Distinguish requested behavior scope from architectural convergence scope. Requested behavior scope governs user-visible behavior. Architectural convergence scope covers internal refactors needed to route the ask through canonical paths, remove duplicate truth, and prevent drift.
- Search for the canonical existing path before designing a new one. Reuse it, refactor it as much as required to fully own the change, or justify why it cannot own the change.
- Internal convergence work may broaden touched files or nearby adopters when needed to avoid parallel paths or shadow contracts, but it must not invent new product functionality, modes, or speculative infrastructure.
- Any refactor, shared-path extraction, or consolidation must preserve existing behavior and name a credible verification signal before it is considered done.
- Use repo evidence first. Ask only for true product, UX, external-constraint, access, or doc-path gaps.
- If repo evidence cannot settle a plan-shaping decision, ask the user instead of guessing, defaulting, or parking the choice as a pseudo-complete plan.
- Before hardening target architecture or Section 7, inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story. Include them now, explicitly defer or exclude them, or ask the exact blocker question when repo truth and approved intent do not settle the disposition.
- Compatibility posture is a first-class plan decision separate from `fallback_policy`. Resolve whether the change preserves the existing contract, performs a clean cutover, or uses an explicitly approved timeboxed bridge. Do not silently assume backward compatibility just because it feels safer.
- When the changed behavior is agent- or LLM-driven, inspect current prompt surfaces, runtime or agent configuration, native model capabilities, and existing tool/file/context exposure before designing. If that capability picture is still unclear after inspection, ask narrowly instead of assuming the agent cannot do it.
- For agent-backed systems, prefer prompt engineering, grounding/context shaping, and better use of native capabilities before custom harnesses, wrappers, parsers, OCR stacks, fuzzy matchers, or deterministic sidecars.
- Any new tooling for agent-backed behavior must justify why prompt-first and capability-first options were insufficient, and it must augment the agent instead of replacing the reasoning the product is supposed to get from the model.
- If the real lever is prompt repair, say so plainly and recommend `prompt-authoring` instead of inventing deterministic scaffolding.
- When porting agent instructions, prompt doctrine, or other instruction-bearing content, preserve explicit operational structure by default. Do not silently condense ordered steps, conditions, hard negatives, or escalation logic unless the artifact records why that condensation is safe and keeps the source text recoverable.
- Default to fail-loud boundaries, hard cutover, and explicit deletes. Runtime shims are forbidden unless the plan explicitly approves them.
- `auto-plan` is one command. It either runs a real bounded planning sequence or fails loud. Prompt-only chaining does not count as the feature.
- `implement-loop` is one command. It either runs a real full-frontier implement-then-audit controller or fails loud. Prompt-only repetition does not count as the feature.
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
- `consistency-pass`
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

The finished artifact is not just a heading set. It is one internally consistent, decision-complete plan that says the same thing about outcome, requested behavior scope, architectural convergence scope, architecture, verification, rollout, and drift history from multiple angles.

### `advance` selection rule

Choose exactly one next command using this precedence:

1. No plan doc yet: run `new`.
2. Existing doc is not canonical enough to trust: run `reformat`.
3. North Star is still draft or too weak to support planning: stop for confirmation or repair the artifact with `reformat`.
4. After North Star confirmation, stop and wait for the user's explicit next command; do not auto-advance into `research` or any later stage.
5. Earliest required structure or owned block is missing: run the command that repairs it.
6. Required structure exists but the next critical sections are still weak or still contain unresolved decisions: run the command that strengthens them or stop and ask the user the exact blocker question.
7. Otherwise follow the canonical core arc:
   - `new` or `reformat`
   - North Star confirmation
   - `research`
   - `deep-dive`
   - `external-research` when warranted
   - `deep-dive` again when external research materially changed the design
   - `phase-plan`
   - `implement`
   - `audit-implementation`
8. If the code audit is clean and the feature still needs docs cleanup, hand off to `arch-docs`.

Do not auto-run more than one command.

### Helper commands

These stay explicit and do not auto-run from `advance`:

- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `consistency-pass`
- `review-gate`

Default placement is after `phase-plan` and before `implement`, unless the user explicitly asks otherwise. They are extra hardening surfaces, not the only place where scope, convergence, or preservation discipline exists.

### Explicit controller commands

These stay explicit unless the user directly asks for them:

- `auto-plan`
- `implement-loop`
- `auto-implement`

`auto-plan` is a bounded planning controller in Codex and Claude Code. `DOC_PATH` is always the planning ledger. The armed controller state lives under `.codex/` in Codex and under `.claude/arch_skill/` in Claude Code. On a fresh doc, the initial `auto-plan` pass arms state, runs only `research` against the same `DOC_PATH`, then ends its turn naturally. On reruns, the parent pass re-arms state against the same `DOC_PATH` and lets the installed Stop hook continue from the first incomplete stage already visible in the doc. It must not self-run `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, or `consistency-pass` in that same turn. After that first turn, the installed Stop hook owns stage-to-stage continuation: it reads doc truth, feeds exactly one literal next command per later turn, and only after `consistency-pass` clears state and says the doc is decision-complete and ready for `implement-loop`. The user-facing command stays simple:

- run `$arch-step auto-plan`
- or run `$arch-step auto-plan <DOC_PATH>`
- do not run the Stop hook yourself; after the controller is armed, just end the turn and let the installed Stop hook run
- the initial `auto-plan` pass must run only `research`, then end the turn
- rerunning `auto-plan` on a partially complete doc is legal; the hook resumes from the first incomplete stage already visible in `DOC_PATH`
- later planning stages are hook-owned only; one literal next command per turn through `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`
- the parent `auto-plan` pass must not clear successful controller state, claim the planning arc is complete, or emit the `implement-loop` handoff while any decision gaps remain
- prefer the current session's canonical full-arch doc when `DOC_PATH` is omitted
- preflight the real continuation surface for the active host runtime:
  - Codex: `~/.codex/hooks.json` must contain the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex`, that installed runner must exist, and `codex_hooks` must be enabled
  - Claude Code: `~/.claude/settings.json` must contain the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude`, and that installed runner must exist
- do not preflight against a copied hook file under `~/.codex/hooks/`; that is not the install contract
- if the active runtime hook entry, the installed runner, the Codex feature flag, or the North Star approval is missing, name the broken prerequisite and stop
- keep the runtime-local controller state armed for the live run and treat `DOC_PATH` as the progress ledger
- if a stage stops early after controller state is armed, stop honestly and let the Stop hook clear the matching state

`implement-loop` is a full-frontier delivery controller in Codex and Claude Code. It arms state before implementation work, runs `implement` across the current approved Section 7 frontier in order from the earliest incomplete or reopened phase through later reachable phases, requires credible programmatic proof along the way, then runs `audit-implementation`, and repeats against the same approved `DOC_PATH` until the audit verdict is clean or a real blocker stops progress. The parent implementation pass may ship code and sync plan/worklog truth, but only the fresh `audit-implementation` child may author the authoritative audit outcome, emit the `arch-docs` handoff, or clear loop state. Execution does not get to change requirements, scope, acceptance criteria, or phase obligations while coding; if the plan itself needs to change, stop and repair the plan instead of continuing on a rewritten story. Do not turn it into a generic open-ended loop.

`auto-implement` is an exact user-facing synonym for `implement-loop`. Resolve it to the same controller behavior and keep the internal runtime names, hook state, and file paths under `implement-loop`.

User-facing invocation stays simple:

- run `$arch-step implement-loop <DOC_PATH>`
- or run `$arch-step auto-implement <DOC_PATH>`
- do not run the Stop hook yourself; after the controller is armed, just end the turn and let the installed Stop hook run
- do not introduce a second command, mode, or user-facing control surface
- preflight the real loop surface for the active host runtime:
  - Codex: `~/.codex/hooks.json` must contain the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex`, that installed runner must exist, and `codex_hooks` must be enabled
  - Claude Code: `~/.claude/settings.json` must contain the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude`, that installed runner must exist, and hook-suppressed Claude child runs via `claude -p --settings '{"disableAllHooks":true}'` must work with the machine's normal Claude auth for fresh audit cycles
- do not preflight against a copied hook file under `~/.codex/hooks/`; that is not the install contract
- if the active runtime hook entry, the installed runner, the Codex feature flag, or Claude hook-suppressed child-run auth is missing, name the broken prerequisite and stop
- arm runtime-local implement-loop state before implementation work so the live loop cannot be forgotten mid-run
- do not hand control back to audit until the current full ordered implementation frontier is done or genuinely blocked, and its phase claims have credible proof
- keep the runtime-local implement-loop state aligned with the live run
- do not clear that state from the implementation side before fresh `audit-implementation` has run, even if the pass believes the work is done
- do not let the parent implementation pass stand in for the clean auditor by writing the authoritative audit block or the `Use $arch-docs` handoff
- when the fresh audit child finishes clean, hand off to `Use $arch-docs`

For controller state in this skill:

- Codex should derive `<SESSION_ID>` from `CODEX_THREAD_ID` and arm the session-scoped `.codex/...<SESSION_ID>.json` path for the current session.
- Claude Code should arm `.claude/arch_skill/...` for the active controller. When Claude exposes session id before the first Stop-hook turn, use the session-scoped path there too. Otherwise the unsuffixed runtime-local path is only a legacy single-slot fallback; the first Stop-hook turn must claim it into the session-scoped path.

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
- `references/arch-auto-plan.md` - bounded planning controller over research, deep-dive twice, phase-plan, and consistency-pass
- `references/arch-plan-enhance.md` - best-possible hardening of the main plan
- `references/arch-fold-in.md` - fold references into the main artifact and wire them into phases
- `references/arch-overbuild-protector.md` - explicit scope triage and remediation using the same rubric core commands should already apply
- `references/arch-consistency-pass.md` - end-to-end cold-read consistency review before implementation
- `references/arch-review-gate.md` - local idiomatic and completeness review
- `references/arch-implement.md` - implementation, worklog, and completion discipline
- `references/arch-implement-loop.md` - full-frontier implement/audit loop, required runtime preflight, and loop-state contract
- `references/arch-audit-implementation.md` - code-completeness audit and phase reopening
- `references/status.md` - compact artifact-first status rules
- `references/advance.md` - full checklist, next-command selection, and optional one-step execution
