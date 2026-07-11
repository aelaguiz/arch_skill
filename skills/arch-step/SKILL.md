---
name: arch-step
description: "Operate the standalone full-arch workflow against one canonical plan artifact and explicit doctrine: `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `auto-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `consistency-pass`, `review-gate`, `implement`, `implement-loop`, `auto-implement`, `full-auto`, `audit-implementation`, `status`, or `advance`. Use when the user wants the full arch workflow, a specific full-arch step, or concise full-arch status. Initial architecture may include the smallest evidenced same-contract convergence closure before scope freezes; later expansion requires explicit human approval. Not for read-only checklist routing, mini plans, lilarch, bugs, or open-ended loops."
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
- The ask is command-shaped: `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `auto-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `consistency-pass`, `review-gate`, `implement`, `implement-loop`, `auto-implement`, `full-auto`, `audit-implementation`, `status`, or `advance`.
- The user wants one canonical plan driven as far as possible through planning and implementation with native goal-mode continuation.
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
- `auto-plan` stage order is enforced by generated command receipts in `DOC_PATH`. Do not hand-edit receipts or accept marker-only plan text as proof that a stage ran.
- Every invocation must check both structure and quality before doing command-local work.
- No command may leave the doc less canonical, less honest, or more contradictory than it found it.
- Present-but-weak sections are not done.
- A plan is not ready, complete, or implementation-ready while any unresolved decision remains about requested behavior, adjacent surfaces that must stay in sync, compatibility posture, architecture, canonical owner path, required deletes, fallback policy, acceptance evidence, or implementation scope.
- Section 0 must contain the binding Scope and Simplicity Contract from
  `references/artifact-contract.md`. Initial architecture may add only its
  evidenced minimal same-contract convergence closure; freeze that closure
  before implementation. After freeze, only explicit human approval expands
  scope. Apply `../_shared/scope-and-convergence.md`.
- Correctness and approved intent outrank speed, scope trimming, or "minimum implementation."
- The agent has no authority to cut requested behavior, acceptance criteria, or required implementation work unless the user or the governing plan already marked that item out of scope.
- Cutting, downgrading, deferring, or "simplifying away" approved behavior, acceptance criteria, or phase obligations is a hard stop. Surface to the user with what you want to cut, why, what Section 0 / TL;DR / Section 7 say about it, and the exact approval you need. Do not proceed until the user explicitly approves; record the approved cut in the Decision Log using the `Scope cut (user-approved)` shape.
- Section 7 uses the depth-first doctrine in `../_shared/depth-first-planning.md`: protect the full destination map, prove the first real working slice through the highest-risk seam, then expand along named axes.
- Phase boundaries are proof boundaries. Phase count is an outcome of dependency edges, proof gates, reversibility or migration boundaries, and user-review boundaries; split only when a phase blends separately provable work.
- A phase is not complete while any checklist item or exit criterion in that phase remains unmet.
- For modern Section 7 docs, `Work` is explanatory only. Every required phase obligation must live in `Checklist (must all be done)` or `Exit criteria (all required)`, and fresh audit must validate both before a phase can stay complete.
- During `implement` and `implement-loop`, the approved plan stays authoritative for requirements, scope, acceptance criteria, and phase obligations. Execution may record progress truth, but it may not rewrite the plan to make unfinished work disappear.
- During `implement` and `implement-loop`, execution scope is the current approved ordered implementation frontier: the earliest incomplete or reopened phase plus later phases whose prerequisites and proof gates are reachable in this implementation arc. Named later expansion is not current missing work until its proof gate is due; silent removal from the destination map is still a scope cut.
- Credible proof supports continued implementation. It does not justify stopping after one local fix, one phase, or one convenient subset while later approved phases are still reachable.
- If the doc is materially non-canonical, repair only the safe owned portion or route to `reformat`.
- Keep one planning source of truth. Do not create sidecar plan docs or competing checklists.
- All planning commands are docs-only. Only `implement` and `implement-loop` may change code; `full-auto` may reach code changes only by routing to `implement-loop`.
- Distinguish the human-authorized outcome from the initial minimal convergence
  closure. Both must be recorded before scope freeze; neither later review nor
  implementation may infer more scope from repo adjacency.
- Search for the canonical existing path before designing a new one. Reuse it, refactor it as much as required to fully own the change, or justify why it cannot own the change.
- During initial planning, convergence may include the smallest evidenced
  touched-file or adopter set needed to eliminate a directly competing owner.
  After scope freeze, a newly found path requires a human decision even when it
  would make the architecture cleaner.
- Any refactor, shared-path extraction, or consolidation must preserve existing behavior and name a credible verification signal before it is considered done.
- Use repo evidence first. Ask only for true product, UX, external-constraint, access, or doc-path gaps.
- Before asking the user any plan-shaping question, consult approved intent on the plan doc: Section 0 (North Star), TL;DR, and the Section 7 phase frontier. Only ask when intent plus repo evidence genuinely leave two credible branches. Record intent-derived resolutions in the Decision Log using the `Intent-derived` shape.
- If repo evidence cannot settle a plan-shaping decision, ask the user instead of guessing, defaulting, or parking the choice as a pseudo-complete plan.
- Before hardening target architecture or Section 7, inspect adjacent surfaces
  tied to the exact changed contract, source of truth, or migration boundary.
  Put directly competing paths in the pre-freeze minimal closure, sequence them
  inside the frozen destination map, exclude merely similar neighbors, or ask
  the exact blocker question. Pattern parity alone is not scope authority.
- Compatibility posture is a first-class plan decision separate from `fallback_policy`. Resolve whether the change preserves the existing contract, performs a clean cutover, or uses an explicitly approved timeboxed bridge. Do not silently assume backward compatibility just because it feels safer.
- When the changed behavior is agent- or LLM-driven, inspect current prompt surfaces, runtime or agent configuration, native model capabilities, and existing tool/file/context exposure before designing. If that capability picture is still unclear after inspection, ask narrowly instead of assuming the agent cannot do it.
- For agent-backed systems, prefer prompt engineering, grounding/context shaping, and better use of native capabilities before custom harnesses, wrappers, parsers, OCR stacks, fuzzy matchers, or deterministic sidecars.
- Any new tooling for agent-backed behavior must justify why prompt-first and capability-first options were insufficient, and it must augment the agent instead of replacing the reasoning the product is supposed to get from the model.
- If the real lever is prompt repair, say so plainly and recommend `prompt-authoring` instead of inventing deterministic scaffolding.
- When porting agent instructions, prompt doctrine, or other instruction-bearing content, preserve explicit operational structure by default. Do not silently condense ordered steps, conditions, hard negatives, or escalation logic unless the artifact records why that condensation is safe and keeps the source text recoverable.
- Default to fail-loud boundaries, hard cutover, and explicit deletes. Runtime shims are forbidden unless the plan explicitly approves them.
- `auto-plan` is one command. In native goal mode, keep advancing the real planning sequence until the artifact is decision-complete or a true blocker stops it. Outside goal mode, run one bounded pass and name the exact next command.
- `implement-loop` is one command. In native goal mode, keep running implementation-frontier work and fresh `audit-implementation` until the audit is clean or a true blocker stops it. Outside goal mode, run one bounded pass and name the exact next command.
- `full-auto` is a re-entrant doctrine mode that reads artifact truth and routes to the next existing command. It must plan before implementation and must not bypass readiness gates.
- Git is the history for retired live truth surfaces. Do not preserve dead competing code paths, stale live docs, or stale comments for posterity. Delete them. If a touched doc, comment, or instruction still matters after the change, update it to current reality in the same run.
- Broader docs audit, consolidation, and final plan/worklog retirement after a clean full-arch code audit belong to `arch-docs`, not to extra hidden `arch-step` commands.
- Core commands apply scope-triage and convergence rules even when helper commands are not run.
- Any command that creates or resumes another agent must apply
  `../_shared/agent-orchestration-policy.md`. `consistency-pass` uses two
  new clean same-host native read-only explorers with disjoint lenses and
  parent-owned synthesis. In Codex, set `fork_turns: "none"`; in Claude Code,
  use clean named or custom subagents rather than a conversation fork. Give
  every review child explicit no-edit/no-write guidance, use a read-only
  capability when the host confirms one, forbid unassigned nested fanout, and
  compare current repo state before accepting its return.
- `advance` must choose from structure first, quality second, stage order third. Helper commands stay explicit.
- `status` is compact, read-only, and grounded in the actual artifact.
- `advance` owns the longer checklist surface and optional one-step execution.
- **No-progress rule.** After two consecutive passes with no real change (no repo file edit, no plan/doc edit, no new evidence a fresh audit has not seen), stop with the exact blocker instead of firing another identical pass.
- **No invented budgets.** Do not call work blocked because it feels expensive. In goal mode, keep moving until the objective is complete or a real blocker meets the native goal-mode stop rule.
- **Exhaust the frontier before auditing.** Do not hand to audit after one local fix when later approved phases are reachable. Finish the current approved ordered implementation frontier or record the real blocker plainly.
- **Respect the tree state the user gave you.** Do not stash changes, create new branches, split the work across multiple PRs, or rewrite history. Commit hygiene, branch strategy, and PR shape are the user's decisions.
- **Parallel-agent edits are a pause signal, not a revert signal.** If the working tree contains edits this pass did not make (foreign file, unexpected compiler error, unfamiliar commit), pause briefly to let the other agent land its fix. Do not revert. Escalate to the user only after two pause-retry cycles fail.

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
7. Read the matching command reference. If the command is `full-auto`, read `references/full-auto.md`.
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
- `full-auto`
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

### Explicit automatic commands

These stay explicit unless the user directly asks for them:

- `auto-plan`
- `implement-loop`
- `auto-implement`

`full-auto` is not in this list because it routes over the existing commands.

### Re-entrant full-auto mode

`full-auto` is an explicit mode for one canonical full-arch plan. It does not add
a new controller, state file, runner, hook behavior, or heuristic layer.
It reads `DOC_PATH`, `WORKLOG_PATH`, and the implementation audit block, then
invokes the next existing command only when the artifact is ready for that command.

Read `references/full-auto.md` before using this mode. The main rule is simple:
plan first with `auto-plan`, prove implementation readiness with the normal
full-arch readiness inventory and the stage receipt gate, then implement with
`implement-loop`. If the North Star is still draft, a decision gap remains, the
receipt gate is not ready, or `consistency-pass` does not approve implementation,
stop honestly instead of chaining.

#### `auto-plan`

A bounded automatic planning command. `DOC_PATH` is always the planning ledger.

Workflow:

1. Read doc truth and North Star status.
2. Run `python3 skills/arch-step/scripts/arch_stage_gate.py status --doc <DOC_PATH>` and take only the gate-reported next stage.
3. The stage command must run `begin` before its doc edits and `complete` after its doc edits so the generated receipt proves that command path ran.
4. In native goal mode, continue taking the next gate-reported stage until `ready` returns `READY next=implement-loop`, or until a true blocker stops the run.
5. Outside native goal mode, run one bounded stage and end with the exact next command.

`arch-step`-specific rules:

- User-facing invocation: `$arch-step auto-plan` or `$arch-step auto-plan <DOC_PATH>`.
- Rerunning `auto-plan` on a partially complete doc is legal; resume from the first incomplete stage already visible in `DOC_PATH`.
- Prefer the current session's canonical full-arch doc when `DOC_PATH` is omitted.
- Do not treat plan markers alone as completion. Existing content without receipts is not auto-plan-ready; rerun the missing stage command.
- Do not claim the planning arc is complete or emit the `implement-loop` handoff while any decision gaps remain.
- Before saying the doc is ready for `implement-loop`, run `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>` and require exit 0.
- If the North Star approval is missing, name it and stop.

#### `implement-loop` / `auto-implement`

`implement-loop` is an implementation-frontier delivery command; `auto-implement` is an exact synonym resolving to the same behavior.

Workflow:

1. Read the approved plan and current audit/worklog truth.
2. Implement the current approved ordered implementation frontier.
3. Run `audit-implementation` after the implementation pass.
4. If audit is clean, hand off to `$arch-docs`.
5. If audit is not clean and work remains reachable, continue from the reopened or incomplete phase. In native goal mode, repeat until clean or truly blocked. Outside native goal mode, report the next exact implementation command.

`arch-step`-specific rules:

- User-facing invocation: `$arch-step implement-loop <DOC_PATH>` or `$arch-step auto-implement <DOC_PATH>`. Do not introduce a second command, mode, or control surface.
- Before implementation starts, run `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`; if it fails, report the planning stage it names instead of implementing from a marker-only plan.
- Implementation covers the current approved ordered implementation frontier in order: the earliest incomplete or reopened phase plus later phases whose prerequisites and proof gates are reachable in this implementation arc.
- Execution does not rewrite requirements, scope, acceptance criteria, or phase obligations mid-coding. If the frozen contract needs to expand, stop for explicit human approval and re-freeze it; an agent-authored plan repair is not authority.
- The implementation pass may ship code and sync plan/worklog truth, but the audit must be a real `audit-implementation` pass against current repo state before the loop can finish clean.

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
- `../_shared/agent-orchestration-policy.md` - transport, context, continuation, isolation, topology, and return-evidence rules for the consistency explorers
- `../_shared/scope-and-convergence.md` - human scope authority, initial planning convergence, scope freeze, finding dispositions, and scope-cycling prohibition
- `../_shared/depth-first-planning.md` - destination map, first working slice, expansion map, proof gates, scope-cut distinction, and failure-mode recognition tests
- `references/section-quality.md` - purpose, strong/weak bar, trust rules, and failure modes for each section and supporting block
- `references/arch-new.md` - bootstrap the canonical artifact and stop for North Star confirmation
- `references/arch-reformat.md` - convert an existing doc into the canonical artifact without losing meaning
- `references/arch-research.md` - research grounding contract
- `references/arch-deep-dive.md` - current architecture, target architecture, call-site audit, and planning-pass rules
- `references/arch-external-research.md` - external research contract and plan-integration rules
- `references/arch-phase-plan.md` - authoritative phase-plan contract
- `references/arch-auto-plan.md` - bounded automatic planning over research, deep-dive twice, phase-plan, and consistency-pass
- `references/full-auto.md` - re-entrant mode over `auto-plan`, the stage receipt gate, and `implement-loop`
- `references/arch-plan-enhance.md` - best-possible hardening of the main plan
- `references/arch-fold-in.md` - fold references into the main artifact and wire them into phases
- `references/arch-overbuild-protector.md` - explicit scope triage and remediation using the same rubric core commands should already apply
- `references/arch-consistency-pass.md` - end-to-end cold-read consistency review before implementation
- `references/arch-review-gate.md` - local idiomatic and completeness review
- `references/arch-implement.md` - implementation, worklog, and completion discipline
- `references/arch-implement-loop.md` - implementation-frontier implement/audit loop and proof contract
- `references/arch-audit-implementation.md` - code-completeness audit and phase reopening
- `references/status.md` - compact artifact-first status rules
- `references/advance.md` - full checklist, next-command selection, and optional one-step execution
