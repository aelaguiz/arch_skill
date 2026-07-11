---
name: miniarch-step
description: "Operate the trimmed standalone full-arch workflow against one canonical plan artifact: `new`, `reformat`, `research`, `deep-dive`, `phase-plan`, `auto-plan`, `implement`, `implement-loop`, `auto-implement`, `full-auto`, `audit-implementation`, `status`, or `advance`. Use when the work still needs canonical architecture grounding, phased execution, and native goal-mode auto flow, but does not need the broader staged surface of `arch-step`. Not for one-pass mini planning, 1-3 phase feature flow, broad or ambiguity-heavy full-arch work, bugs, or open-ended loops."
metadata:
  short-description: "Trimmed full-arch workflow"
---

# Miniarch Step

Use this skill when the user wants the full arch shape and full auto support, but does not need the broader helper surface of `arch-step`.

The primary object is one canonical full-arch plan doc. `miniarch-step` keeps the same artifact discipline and full-work posture as `arch-step`, but with a trimmed public command surface. It is not a lower-effort workflow: finish the requested outcome completely, but do not confuse completeness with more machinery.

## When to use

- The task still benefits from canonical architecture grounding, phased execution, and one governing full-arch doc.
- The user wants phased planning, implementation, and audit against one full-arch doc.
- The user wants the trimmed command surface rather than `arch-step`'s broader helper surface.
- The user wants native goal-mode auto flow rather than one-pass planning only.
- The ask is command-shaped: `new`, `reformat`, `research`, `deep-dive`, `phase-plan`, `auto-plan`, `implement`, `implement-loop`, `auto-implement`, `full-auto`, `audit-implementation`, `status`, or `advance`.
- The user wants one canonical trimmed full-arch plan driven as far as possible through planning and implementation with native goal-mode continuation.

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
- Section 0 must contain the binding Scope and Simplicity Contract from
  `references/artifact-contract.md`: human authorization, smallest sufficient
  solution, initial convergence closure or `none`, scope freeze, enough proof,
  do-not-build boundary, and accepted residual risk.
- Treat overbuilding as a known default failure mode. Agents often confuse thoroughness with quality and keep adding abstractions, harnesses, edge cases, and proof after the real fix is already sufficient. Assume that bias is active; before adding machinery, try to reuse, delete, or simplify.
- Match the size of the solution and its proof to the demonstrated failure and blast radius. A systemic fix belongs at the narrowest shared boundary that eliminates the failure class; "systemic" does not mean "build a framework around the incident."
- Every Section 7 item must directly serve the human outcome, the pre-freeze
  minimal convergence closure, or enough proof. Remove items that serve none
  before calling the plan implementation-ready.
- Initial architecture may add only the smallest evidenced same-contract
  convergence closure before implementation readiness. The frozen contract
  outranks later plan expansion. A later planner, worker, review, audit, or
  Decision Log entry cannot authorize new work; only explicit human approval
  recorded as `Scope expansion (human-approved)` can widen it.
- During implementation, adding an unapproved adjacent path, framework,
  harness, verifier, abstraction, command, dependency, operational surface, or
  test category is a hard stop. Ask for human approval before changing plan or
  code. Apply `skills/_shared/scope-and-convergence.md`.
- Correctness and approved intent outrank convenience or scope trimming.
- The agent has no authority to cut requested behavior, acceptance criteria, or required implementation work unless the user or the governing plan already marked that item out of scope.
- Cutting, downgrading, deferring, or "simplifying away" approved behavior, acceptance criteria, or phase obligations is a hard stop. Surface to the user with what you want to cut, why, what Section 0 / TL;DR / Section 7 say about it, and the exact approval you need. Do not proceed until the user explicitly approves; record the approved cut in the Decision Log using the `Scope cut (user-approved)` shape.
- `miniarch-step` is a trimmed command surface, not a lower-effort workflow. Full effort means a complete result at the simplest sufficient architecture, not maximum code, testing, or ceremony.
- Section 7 uses the depth-first doctrine in `skills/_shared/depth-first-planning.md`: protect the full destination map, prove the first real working slice through the highest-risk seam, then expand along named axes.
- Phase boundaries are proof boundaries. Phase count is an outcome of dependency edges, proof gates, reversibility or migration boundaries, and user-review boundaries; split only when a phase blends separately provable work.
- A phase is not complete while any checklist item or exit criterion in that phase remains unmet.
- For modern Section 7 docs, `Work` is explanatory only. Every required phase obligation must live in `Checklist (must all be done)` or `Exit criteria (all required)`, and fresh audit must validate both before a phase can stay complete.
- During `implement` and `implement-loop`, the approved plan stays authoritative for requirements, scope, acceptance criteria, and phase obligations. Execution may record progress truth, but it may not rewrite the plan to make unfinished work disappear.
- During `implement` and `implement-loop`, execution scope is the current approved ordered implementation frontier: the earliest incomplete or reopened phase plus later phases whose prerequisites and proof gates are reachable in this implementation arc. Named later expansion is not current missing work until its proof gate is due; silent removal from the destination map is still a scope cut.
- Credible proof supports continued implementation. It does not justify stopping after one local fix, one phase, or one convenient subset while later approved phases are still reachable.
- If the doc is materially non-canonical, repair only the safe owned portion or route to `reformat`.
- Keep one planning source of truth. Do not create sidecar plan docs or competing checklists.
- All planning commands are docs-only. Only `implement` and `implement-loop` may change code; `full-auto` may reach code changes only by routing to `implement-loop`.
- In Codex, if a miniarch planning step explicitly uses parallel agents, spawn those planning agents with model `gpt-5.4-mini` and reasoning effort `xhigh`.
- Distinguish the human-authorized outcome from the initial minimal convergence
  closure, and freeze both before implementation.
- Search for the canonical existing path before designing a new one. Reuse it, refactor it as much as required to fully own the change, or justify why it cannot own the change.
- During initial planning, convergence may include the smallest evidenced
  touched-file or adopter set needed to eliminate a directly competing owner.
  After freeze, a newly found path requires a human decision.
- Any refactor, shared-path extraction, or consolidation must preserve existing behavior and name a credible verification signal before it is considered done.
- Use repo evidence first. Ask only for true product, UX, external-constraint, access, or doc-path gaps.
- Before asking the user any plan-shaping question, consult approved intent on the plan doc: Section 0 (North Star), TL;DR, and the Section 7 phase frontier. Only ask when intent plus repo evidence genuinely leave two credible branches. Record intent-derived resolutions in the Decision Log using the `Intent-derived` shape.
- If repo evidence cannot settle a plan-shaping decision, ask the user instead of guessing, defaulting, or parking the choice as a pseudo-complete plan.
- Before hardening target architecture or Section 7, inspect adjacent surfaces
  tied to the exact changed contract, source of truth, or migration boundary.
  Put directly competing paths in the pre-freeze closure, sequence them inside
  the frozen destination map, exclude merely similar neighbors, or ask the exact
  blocker question. Pattern parity alone is not scope authority.
- Compatibility posture is a first-class plan decision separate from `fallback_policy`.
- When the changed behavior is agent- or LLM-driven, inspect current prompt surfaces, runtime or agent configuration, native model capabilities, and existing tool/file/context exposure before designing.
- For agent-backed systems, prefer prompt engineering, grounding/context shaping, and better use of native capabilities before custom harnesses, wrappers, parsers, OCR stacks, fuzzy matchers, or deterministic sidecars.
- If the real lever is prompt repair, say so plainly and recommend `prompt-authoring` instead of inventing deterministic scaffolding.
- Default to fail-loud boundaries, hard cutover, and explicit deletes. Runtime shims are forbidden unless the plan explicitly approves them.
- `auto-plan` is one command. In native goal mode, keep advancing the real planning sequence until the artifact is decision-complete or a true blocker stops it. Outside goal mode, run one bounded pass and name the exact next command.
- `implement-loop` is one command. In native goal mode, keep running implementation-frontier work and fresh `audit-implementation` until the audit is clean or a true blocker stops it. Outside goal mode, run one bounded pass and name the exact next command.
- `full-auto` is a re-entrant doctrine mode that reads artifact truth and routes to the next existing command. It must plan before implementation and must not bypass readiness gates.
- Git is the history for retired live truth surfaces. Delete dead competing code paths, stale live docs, and stale comments instead of keeping them for archaeology.
- Broader docs audit, consolidation, and final plan/worklog retirement after a clean code audit belong to `arch-docs`, not to hidden `miniarch-step` commands.
- `status` is compact, read-only, and grounded in the actual artifact.
- `advance` owns the longer checklist surface and optional one-step execution.
- **No-progress rule.** After two consecutive passes with no real change (no repo file edit, no plan/doc edit, no new evidence a fresh audit has not seen), stop with the exact blocker instead of firing another identical pass.
- **No invented budgets.** Do not call authorized work blocked because it feels expensive. This does not authorize violating the frozen Scope and Simplicity Contract or adding unapproved machinery. In goal mode, keep moving until the objective is complete or a real blocker meets the native goal-mode stop rule.
- **Exhaust the frontier before auditing.** Do not hand to audit after one local fix when later frozen-contract-compliant phases are reachable. Finish that frontier or record the real blocker plainly.
- **Respect the tree state the user gave you.** Do not stash changes, create new branches, split the work across multiple PRs, or rewrite history. Commit hygiene, branch strategy, and PR shape are the user's decisions.
- **Parallel-agent edits are a pause signal, not a revert signal.** If the working tree contains edits this pass did not make (foreign file, unexpected compiler error, unfamiliar commit), pause briefly to let the other agent land its fix. Do not revert. Escalate to the user only after two pause-retry cycles fail.

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
   - a concrete Scope and Simplicity Contract and whether planned work stays inside it
6. Read `references/section-quality.md` for the sections this command depends on.
7. Read the matching command reference. If the command is `full-auto`, read `references/full-auto.md`.
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
- `full-auto`
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

### Explicit automatic commands

These stay explicit unless the user directly asks for them:

- `auto-plan`
- `implement-loop`
- `auto-implement`

`full-auto` is not in this list because it routes over the existing commands.

### Re-entrant full-auto mode

`full-auto` is an explicit mode for one canonical mini/full-arch plan. It does
not add a new controller, state file, runner, hook behavior, script, or
heuristic layer. It reads `DOC_PATH`, `WORKLOG_PATH`, and the implementation
audit block, then invokes the next existing command only when the artifact is
ready for that command.

Read `references/full-auto.md` before using this mode. The main rule is simple:
plan first with `auto-plan`, prove implementation readiness with the normal
miniarch readiness inventory, then implement with `implement-loop`. If the
North Star is still draft, a decision gap remains, Section 7 is not
execution-grade, stop honestly instead of chaining.

#### `auto-plan`

The automatic planning command for this trimmed full-arch surface. `DOC_PATH` is the planning ledger.

Workflow:

1. Read doc truth and North Star status.
2. Run the first incomplete planning stage in order: `research`, `deep-dive`, then `phase-plan`.
3. In native goal mode, continue taking the next incomplete stage until `phase-plan` clears decision gaps and the doc is implementation-ready, or until a true blocker stops the run.
4. Outside native goal mode, run one bounded stage and end with the exact next command.

`miniarch-step`-specific rules:

- User-facing invocation: `$miniarch-step auto-plan` or `$miniarch-step auto-plan <DOC_PATH>`.
- Rerunning `auto-plan` on a partially complete doc is legal; resume from the first incomplete stage already visible in `DOC_PATH`.
- Prefer the current session's canonical mini/full-arch doc when `DOC_PATH` is omitted.
- Do not claim the planning arc is complete or emit the `implement-loop` handoff while any decision gaps remain.

#### `implement-loop` / `auto-implement`

`implement-loop` is an implementation-frontier delivery command; `auto-implement` is an exact user-facing synonym resolving to the same behavior.

Workflow:

1. Read the approved plan and current audit/worklog truth.
2. Implement the current approved ordered implementation frontier.
3. Run `audit-implementation` after the implementation pass.
4. If audit is clean, hand off to `$arch-docs`.
5. If audit is not clean and work remains reachable, continue from the reopened or incomplete phase. In native goal mode, repeat until clean or truly blocked. Outside native goal mode, report the next exact implementation command.

`miniarch-step`-specific rules:

- User-facing invocation: `$miniarch-step implement-loop <DOC_PATH>` or `$miniarch-step auto-implement <DOC_PATH>`.
- Implementation covers the current approved ordered implementation frontier in order: the earliest incomplete or reopened phase plus later phases whose prerequisites and proof gates are reachable in this implementation arc.
- The implementation pass may ship code and sync plan/worklog truth, but the audit must be a real `audit-implementation` pass against current repo state before the loop can finish clean.

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
- `skills/_shared/scope-and-convergence.md` - human scope authority, initial planning convergence, scope freeze, finding dispositions, and scope-cycling prohibition
- `skills/_shared/depth-first-planning.md` - destination map, first working slice, expansion map, proof gates, scope-cut distinction, and failure-mode recognition tests
- `references/section-quality.md` - purpose, strong/weak bar, trust rules, and failure modes for each section and supporting block
- `references/arch-new.md` - bootstrap the canonical artifact and stop for North Star confirmation
- `references/arch-reformat.md` - convert an existing doc into the canonical artifact without losing meaning
- `references/arch-research.md` - research grounding contract
- `references/arch-deep-dive.md` - current architecture, target architecture, call-site audit, and single-pass planning rules
- `references/arch-phase-plan.md` - authoritative phase-plan contract
- `references/arch-auto-plan.md` - automatic planning over research, one deep-dive pass, and phase-plan
- `references/full-auto.md` - doctrine-only re-entrant mode over `auto-plan` and `implement-loop`
- `references/arch-implement.md` - implementation, worklog, and completion discipline
- `references/arch-implement-loop.md` - implementation-frontier implement/audit loop and proof contract
- `references/arch-audit-implementation.md` - code-completeness audit and phase reopening
- `references/status.md` - compact artifact-first status rules
- `references/advance.md` - full checklist, next-command selection, and optional one-step execution
