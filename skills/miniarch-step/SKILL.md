---
name: miniarch-step
description: "Operate the trimmed standalone full-arch workflow against one canonical plan artifact: `new`, `reformat`, `research`, `deep-dive`, `phase-plan`, `auto-plan`, `implement`, `implement-loop`, `auto-implement`, `audit-implementation`, `status`, or `advance`. Use when the work still needs canonical architecture grounding, phased execution, and real auto controllers, but does not need the broader staged surface of `arch-step`. Not for one-pass mini planning, 1-3 phase feature flow, broad or ambiguity-heavy full-arch work, bugs, or open-ended loops."
metadata:
  short-description: "Trimmed full-arch workflow"
---

# Miniarch Step

Use this skill when the user wants the full arch shape and full auto support, but does not need the broader helper surface of `arch-step`.

The primary object is one canonical full-arch plan doc. `miniarch-step` keeps the same artifact discipline and full-work posture as `arch-step`, but with a trimmed public command surface. It is not a lower-effort workflow.

## When to use

- The task still benefits from canonical architecture grounding, phased execution, and one governing full-arch doc.
- The user wants phased planning, implementation, and audit against one full-arch doc.
- The user wants the trimmed command surface rather than `arch-step`'s broader helper surface.
- The user wants real auto controllers rather than one-pass planning only.
- The ask is command-shaped: `new`, `reformat`, `research`, `deep-dive`, `phase-plan`, `auto-plan`, `implement`, `implement-loop`, `auto-implement`, `audit-implementation`, `status`, or `advance`.

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
- Correctness and approved intent outrank convenience or scope trimming.
- The agent has no authority to cut requested behavior, acceptance criteria, or required implementation work unless the user or the governing plan already marked that item out of scope.
- Cutting, downgrading, deferring, or "simplifying away" approved behavior, acceptance criteria, or phase obligations is a hard stop. Surface to the user with what you want to cut, why, what Section 0 / TL;DR / Section 7 say about it, and the exact approval you need. Do not proceed until the user explicitly approves; record the approved cut in the Decision Log using the `Scope cut (user-approved)` shape.
- `miniarch-step` is a trimmed command surface, not a lower-effort workflow.
- Section 7 phases should split work into coherent self-contained units, with the most fundamental units first and later phases clearly building on earlier ones.
- If two valid decompositions exist, bias toward more distinct coherent phases rather than fewer blended phases.
- A phase is not complete while any checklist item or exit criterion in that phase remains unmet.
- For modern Section 7 docs, `Work` is explanatory only. Every required phase obligation must live in `Checklist (must all be done)` or `Exit criteria (all required)`, and fresh audit must validate both before a phase can stay complete.
- During `implement` and `implement-loop`, the approved plan stays authoritative for requirements, scope, acceptance criteria, and phase obligations. Execution may record progress truth, but it may not rewrite the plan to make unfinished work disappear.
- During `implement` and `implement-loop`, execution scope is the full approved Section 7 frontier in order: start from the earliest incomplete or reopened phase and continue through later reachable phases until that frontier is done or a real blocker stops progress.
- Credible proof supports continued implementation. It does not justify stopping after one local fix, one phase, or one convenient subset while later approved phases are still reachable.
- If the doc is materially non-canonical, repair only the safe owned portion or route to `reformat`.
- Keep one planning source of truth. Do not create sidecar plan docs or competing checklists.
- All planning commands are docs-only. Only `implement` and `implement-loop` may change code.
- In Codex, if a miniarch planning step explicitly uses parallel agents, spawn those planning agents with model `gpt-5.4-mini` and reasoning effort `xhigh`.
- Distinguish requested behavior scope from architectural convergence scope.
- Search for the canonical existing path before designing a new one. Reuse it, refactor it as much as required to fully own the change, or justify why it cannot own the change.
- Internal convergence work may broaden touched files or nearby adopters when needed to avoid parallel paths or shadow contracts, but it must not invent new product functionality, modes, or speculative infrastructure.
- Any refactor, shared-path extraction, or consolidation must preserve existing behavior and name a credible verification signal before it is considered done.
- Use repo evidence first. Ask only for true product, UX, external-constraint, access, or doc-path gaps.
- Before asking the user any plan-shaping question, consult approved intent on the plan doc: Section 0 (North Star), TL;DR, and the Section 7 phase frontier. Only ask when intent plus repo evidence genuinely leave two credible branches. Record intent-derived resolutions in the Decision Log using the `Intent-derived` shape.
- If repo evidence cannot settle a plan-shaping decision, ask the user instead of guessing, defaulting, or parking the choice as a pseudo-complete plan.
- Before hardening target architecture or Section 7, inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story.
- Compatibility posture is a first-class plan decision separate from `fallback_policy`.
- When the changed behavior is agent- or LLM-driven, inspect current prompt surfaces, runtime or agent configuration, native model capabilities, and existing tool/file/context exposure before designing.
- For agent-backed systems, prefer prompt engineering, grounding/context shaping, and better use of native capabilities before custom harnesses, wrappers, parsers, OCR stacks, fuzzy matchers, or deterministic sidecars.
- If the real lever is prompt repair, say so plainly and recommend `prompt-authoring` instead of inventing deterministic scaffolding.
- Default to fail-loud boundaries, hard cutover, and explicit deletes. Runtime shims are forbidden unless the plan explicitly approves them.
- `auto-plan` is one command. It either runs the real planning sequence or fails loud.
- `implement-loop` is one command. It either runs a real full-frontier implement-then-audit controller or fails loud.
- Git is the history for retired live truth surfaces. Delete dead competing code paths, stale live docs, and stale comments instead of keeping them for archaeology.
- Broader docs audit, consolidation, and final plan/worklog retirement after a clean code audit belong to `arch-docs`, not to hidden `miniarch-step` commands.
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
7. Otherwise follow the core arc:
   - `new` or `reformat`
   - North Star confirmation
   - `research`
   - `deep-dive`
   - `phase-plan`
   - `implement`
   - `audit-implementation`
8. If the code audit is clean and the feature still needs docs cleanup, hand off to `arch-docs`.

Do not auto-run more than one command.

### Explicit controller commands

These stay explicit unless the user directly asks for them:

- `auto-plan`
- `implement-loop`
- `auto-implement`

**Arm first, disarm never.** This skill is hook-owned for the controller commands above. The very first step of every invocation runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` and then writes a session-scoped controller state file; the very last step of the parent turn is to end the turn. Parent turns do not run the Stop hook, do not delete state, and do not clean up early — the Stop hook is the only process that clears state, and it does so only on `CLEAN`, `BLOCKED`, or deadline. Core doctrine, arm-time ensure-install, session-id rules, conflict gate, staleness sweep, and manual recovery live in `skills/_shared/controller-contract.md`. The rules below describe only what is specific to `miniarch-step`.

#### `auto-plan`

The planning controller for this trimmed full-arch surface. `DOC_PATH` is the planning ledger; state is session-scoped at `.codex/miniarch-step-auto-plan-state.<SESSION_ID>.json` (Codex) or `.claude/arch_skill/miniarch-step-auto-plan-state.<SESSION_ID>.json` (Claude Code).

Workflow:

1. **Arm**: ensure-install → resolve session id → write state file → end the turn. On a fresh doc, the parent pass may additionally run only `research` before ending. It must not self-run `deep-dive` or `phase-plan` in the same turn. On Claude Code, resolve the session id first via `arch_controller_stop_hook.py --current-session`; abort with the tool's error message if it fails.
2. **Body** (hook-owned): the Stop hook reads doc truth and feeds exactly one literal next command per later turn, through `deep-dive` and `phase-plan`.
3. **Disarm** (hook-owned): after `phase-plan` clears decision gaps and the doc is implementation-ready, the Stop hook clears state and emits the `implement-loop` handoff.

`miniarch-step`-specific rules:

- User-facing invocation: `$miniarch-step auto-plan` or `$miniarch-step auto-plan <DOC_PATH>`.
- Rerunning `auto-plan` on a partially complete doc is legal; the hook resumes from the first incomplete stage already visible in `DOC_PATH`.
- Prefer the current session's canonical mini/full-arch doc when `DOC_PATH` is omitted.
- The parent pass must not clear state, claim the planning arc is complete, or emit the `implement-loop` handoff while any decision gaps remain.

#### `implement-loop` / `auto-implement`

`implement-loop` is a full-frontier delivery controller; `auto-implement` is an exact user-facing synonym resolving to the same behavior. State lives at `.codex/miniarch-step-implement-loop-state.<SESSION_ID>.json` (Codex) or `.claude/arch_skill/miniarch-step-implement-loop-state.<SESSION_ID>.json` (Claude Code).

Workflow:

1. **Arm**: ensure-install → resolve session id → write state file → end the turn. The parent pass may run one bounded implementation pass before ending; it must not hand back to audit mid-pass or claim clean from the implementation side. On Claude Code, resolve the session id first via `arch_controller_stop_hook.py --current-session`; abort with the tool's error message if it fails.
2. **Body** (hook-owned): the Stop hook runs `audit-implementation` as a fresh child (on Codex: `--model gpt-5.4-mini` at `xhigh`; on Claude Code: hook-suppressed child run via `claude -p --settings '{"disableAllHooks":true}'`). If audit is not clean, the hook continues with another implementation pass.
3. **Disarm** (hook-owned): when the fresh audit child finishes clean, the hook clears state and the parent hands off to `$arch-docs`.

`miniarch-step`-specific rules:

- User-facing invocation: `$miniarch-step implement-loop <DOC_PATH>` or `$miniarch-step auto-implement <DOC_PATH>`.
- Implementation covers the full approved Section 7 frontier in order, from the earliest incomplete or reopened phase through later reachable phases.
- The parent pass never writes the authoritative audit block or the `Use $arch-docs` handoff; only the fresh audit child may.
- The parent pass never clears state from the implementation side before fresh `audit-implementation` has run.

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
- `sleep_for`: the hook sleeps the requested seconds (bounded by the installed hook timeout) and then continues to the next audit/planning pass. Use this whenever the next step is an automated check the parent itself can re-run — polling a marker file, re-checking CI, waiting on a detached job of any wall-clock length. If the work outlasts a single hook-timeout window, arm repeated `sleep_for` pauses rather than escalating. See `skills/_shared/controller-contract.md` §Choosing the yield kind.
- The field is single-shot. Write it once per turn; the hook clears it before taking action. Do not re-read it.

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
- `references/arch-auto-plan.md` - planning controller over research, one deep-dive pass, and phase-plan
- `references/arch-implement.md` - implementation, worklog, and completion discipline
- `references/arch-implement-loop.md` - full-frontier implement/audit loop, required ensure-install step, and loop-state contract
- `references/arch-audit-implementation.md` - code-completeness audit and phase reopening
- `references/status.md` - compact artifact-first status rules
- `references/advance.md` - full checklist, next-command selection, and optional one-step execution
