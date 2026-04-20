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
- Cutting, downgrading, deferring, or "simplifying away" approved behavior, acceptance criteria, or phase obligations is a hard stop. Surface to the user with what you want to cut, why, what Section 0 / TL;DR / Section 7 say about it, and the exact approval you need. Do not proceed until the user explicitly approves; record the approved cut in the Decision Log using the `Scope cut (user-approved)` shape.
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
- Before asking the user any plan-shaping question, consult approved intent on the plan doc: Section 0 (North Star), TL;DR, and the Section 7 phase frontier. Only ask when intent plus repo evidence genuinely leave two credible branches. Record intent-derived resolutions in the Decision Log using the `Intent-derived` shape.
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
- **No-progress rule.** After two consecutive parent passes with no real change (no repo file edit, no plan/doc edit, no new evidence the audit/evaluator has not seen), end with `requested_yield: {kind: "await_user", reason: "no progress after 2 passes: ..."}` instead of firing another identical pass. See `skills/_shared/controller-contract.md` §Parent-pass discipline.
- **No invented budgets.** The hook owns timing (`deadline_at`, iteration cap, parsed cadence). Do not self-declare `blocked` or "outside in-session budget" because remaining work feels expensive or the auditor is costly. Take the next reachable step, arm `requested_yield: sleep_for` for a paced pause, or yield `await_user` if the armed window is genuinely too small. Terminal verdicts come from the controller, not from invented budgets.
- **Exhaust the frontier before handing to audit.** Ending the turn is not a cheap checkpoint — each turn end pays for a full fresh audit or evaluator child run. End the turn when you believe you are done with everything reachable (full plan frontier, every reachable phase, every named audit), not after one local fix. If a blocker stops you short, yield explicitly via `await_user` or `sleep_for`; do not drop the turn silently mid-frontier.
- **Respect the tree state the user gave you.** Do not stash changes, create new branches, split the work across multiple PRs, or rewrite history. Commit hygiene, branch strategy, and PR shape are the user's decisions.
- **Parallel-agent edits are a pause signal, not a revert signal.** If the working tree contains edits this pass did not make (foreign file, unexpected compiler error, unfamiliar commit), pause via `requested_yield: {kind: "sleep_for", seconds: 300, ...}` to let the other agent land its fix. Do not revert. Escalate via `await_user` only after two pause-retry cycles fail.

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

**Arm first, disarm never.** This skill is hook-owned for the controller commands above. The very first step of every invocation runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` and then writes a session-scoped controller state file; the very last step of the parent turn is to end the turn. Parent turns do not run the Stop hook, do not delete state, and do not clean up early — the Stop hook is the only process that clears state, and it does so only on `CLEAN`, `BLOCKED`, or deadline. Core doctrine, arm-time ensure-install, session-id rules, conflict gate, staleness sweep, and manual recovery live in `skills/_shared/controller-contract.md`. The rules below describe only what is specific to `arch-step`.

#### `auto-plan`

A bounded planning controller. `DOC_PATH` is always the planning ledger; state is session-scoped at `.codex/auto-plan-state.<SESSION_ID>.json` (Codex) or `.claude/arch_skill/auto-plan-state.<SESSION_ID>.json` (Claude Code).

Workflow:

1. **Arm**: ensure-install → resolve session id → write state file → end the turn. On a fresh doc, the parent pass may additionally run only `research` before ending. It must not self-run `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, or `consistency-pass` in the same turn. On Claude Code, resolve the session id first via `arch_controller_stop_hook.py --current-session`; abort with the tool's error message if it fails.
2. **Body** (hook-owned): the Stop hook reads doc truth and feeds exactly one literal next command per later turn through `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`.
3. **Disarm** (hook-owned): only after `consistency-pass` confirms the doc is decision-complete and ready for `implement-loop`, the Stop hook clears state and emits the handoff.

`arch-step`-specific rules:

- User-facing invocation: `$arch-step auto-plan` or `$arch-step auto-plan <DOC_PATH>`.
- Rerunning `auto-plan` on a partially complete doc is legal; the hook resumes from the first incomplete stage already visible in `DOC_PATH`.
- Prefer the current session's canonical full-arch doc when `DOC_PATH` is omitted.
- The parent pass must not clear state, claim the planning arc is complete, or emit the `implement-loop` handoff while any decision gaps remain.
- If the North Star approval is missing, name it and stop (this is a skill-specific gate in addition to the shared ensure-install step).

#### `implement-loop` / `auto-implement`

`implement-loop` is a full-frontier delivery controller; `auto-implement` is an exact synonym resolving to the same behavior. State lives at `.codex/implement-loop-state.<SESSION_ID>.json` (Codex) or `.claude/arch_skill/implement-loop-state.<SESSION_ID>.json` (Claude Code).

Workflow:

1. **Arm**: ensure-install → resolve session id → write state file → end the turn. The parent pass may run one bounded implementation pass before ending; it must not hand back to audit mid-pass or claim clean from the implementation side. On Claude Code, resolve the session id first via `arch_controller_stop_hook.py --current-session`; abort with the tool's error message if it fails.
2. **Body** (hook-owned): the Stop hook runs `audit-implementation` as a fresh child (on Codex: default `gpt-5.4` `xhigh`; on Claude Code: hook-suppressed child run via `claude -p --settings '{"disableAllHooks":true}'`). If audit is not clean, the hook continues with another implementation pass.
3. **Disarm** (hook-owned): when the fresh audit child finishes clean, the hook clears state and the parent hands off to `$arch-docs`.

`arch-step`-specific rules:

- User-facing invocation: `$arch-step implement-loop <DOC_PATH>` or `$arch-step auto-implement <DOC_PATH>`. Do not introduce a second command, mode, or control surface.
- Implementation covers the full approved Section 7 frontier in order, from the earliest incomplete or reopened phase through later reachable phases.
- Execution does not rewrite requirements, scope, acceptance criteria, or phase obligations mid-coding. If the plan itself needs to change, stop and repair the plan instead of continuing on a rewritten story.
- The parent implementation pass may ship code and sync plan/worklog truth, but only the fresh `audit-implementation` child may author the authoritative audit outcome, emit the `arch-docs` handoff, or clear loop state.

#### Graceful yield (auto-plan / implement-loop / auto-implement)

Prefer not to need user feedback — approved plan intent and repo evidence should settle most decisions. When that fails and the parent must genuinely ask the user a question, or the parent has nothing useful to do until an async signal lands, write a single `requested_yield` object into the controller state before ending the turn. The Stop hook honors and clears it before the next audit:

```jsonc
"requested_yield": {
  "kind": "sleep_for" | "await_user",
  "seconds": 1200,   // sleep_for only; positive integer
  "reason": "asked the user to choose between canonical owner paths"
}
```

- `await_user`: the hook stops cleanly (`continue=False`) with the reason and leaves the controller armed. The next user turn resumes dispatch normally. This is the graceful exit when you asked the user a question; do not end the turn without writing the yield, or the Stop hook will tight-loop.
- `sleep_for`: the hook sleeps the requested seconds (bounded by the installed hook timeout) and then continues to the next audit/planning pass. Rare — typically only useful when a long external job is in flight.
- The field is single-shot. Write it once per turn; the hook clears it before taking action. Do not re-read it.

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
- `references/arch-implement-loop.md` - full-frontier implement/audit loop, required ensure-install step, and loop-state contract
- `references/arch-audit-implementation.md` - code-completeness audit and phase reopening
- `references/status.md` - compact artifact-first status rules
- `references/advance.md` - full checklist, next-command selection, and optional one-step execution
