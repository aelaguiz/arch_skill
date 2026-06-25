# Architecture Pattern Convergence

## Original Instructions

Review `arch-step` and the arch-series skills that involve deep diving and
researching. Add a phase to all relevant workflows that explicitly requires
cataloging all sources of truth, all competing patterns, and every pattern that
affects the codebase or the plan being built. The plan should include a
unification phase: when competing patterns are found, it must exhaustively
catalog how they will be unified so the architecture trends toward fewer bug
vectors over time. As long as `arch-step` and related skills are used, they
should collapse patterns instead of adding new ways of doing things. When more
than one way of doing something exists, the plan must build exhaustive
checklists and describe how those paths will be unified. That work is
automatically in scope because it is part of architecture work. Use
`skill-authoring` and `prompt-authoring`, run an exhaustive audit with parallel
agents, and save the resulting methodology as a new document in `docs/`.

This document explains how arch-series planning should stop a codebase from
growing duplicate ways to do the same thing.

The core rule is simple: before a plan adds or changes an architectural pattern,
it must catalog the existing sources of truth and competing patterns, choose the
canonical owner, and turn required unification work into the plan. If competing
patterns remain live without a reason, the architecture now has another bug
vector.

This is methodology, not a new runtime contract. Active plans own project
decisions. Skill references own command behavior. `README.md`, `Makefile`, and
`AGENTS.md` own install and routing summaries.

## Why This Exists

Good local work can still make the repo worse when it adds a clean new path next
to old live paths. The bad outcome is not just duplication. It is two readers,
writers, prompts, schemas, command paths, generated artifacts, docs, or examples
quietly teaching different truths.

Arch work should make that trend run the other way. Every real architecture pass
should either reuse the existing canonical pattern or move the repo closer to one
obvious pattern.

## When To Use

Use this method before an arch-series skill blesses a plan that introduces,
changes, or centralizes any of these:

- service, abstraction, state model, API shape, adapter, command path, workflow,
  event flow, hook, persistence path, generated artifact, prompt/runtime pattern,
  source format, migration boundary, install surface, or shared contract
- new ownership boundary for behavior that already exists elsewhere
- refactor, consolidation, or cutover that can leave old and new paths live
- phase plan where unification or deletion work may be needed before widening

For tiny changes, this can be a compact paragraph. For broad or migration-heavy
work, it should be a real inventory table. The important part is not the size of
the artifact; it is that every competing source of truth gets a disposition.

## Core Method

1. Catalog source truth before designing.
2. Catalog competing patterns before adding a new one.
3. Choose the canonical owner from repo evidence plus approved intent.
4. Classify every related live path.
5. Put required unification, migration, delete, and drift-proofing work into the
   authoritative phase plan.
6. Prove preserved behavior when converging or deleting.
7. Block readiness when unresolved competing patterns still affect the plan.

The default answer is not "make a new pattern." The default answer is "extend,
repair, or promote the best existing owner." A new pattern is allowed only when
the plan explains why the existing owners cannot cleanly own the behavior and
what happens to the older paths.

## Source-Truth Inventory

The inventory should answer: what currently defines the truth this plan depends
on?

For each relevant source, record the path or symbol, what truth it owns, why it
is authoritative or not, and how the plan will keep it in sync.

Use this shape inside the active plan's research, current architecture, target
architecture, or call-site audit section:

```text
## Source-Truth Inventory
| Source | Truth owned today | Authority level | Competes with | Plan disposition | Proof needed |
| ------ | ----------------- | --------------- | ------------- | ---------------- | ------------ |
| <path/symbol/surface> | <contract/behavior> | <canonical/debt/generated/example/doc/prompt/test> | <other source or none> | <keep/extend/move/delete/leave different/user decision> | <test/check/review> |
```

The inventory is exhaustive for the plan scope when it covers every source that
could change how the requested behavior is built, called, configured, tested,
generated, documented, or prompted.

## Competing-Pattern Inventory

The pattern inventory should answer: what else in the repo already solves this
kind of problem?

For each comparable pattern, capture:

- where it lives
- what problem it solves
- whether it is the best pattern to extend
- whether it is debt that should not be copied
- whether it has a genuinely different contract
- whether callers, docs, prompts, examples, fixtures, tests, or generated
  artifacts still route through it
- whether the new plan would leave old and new behavior split

Use this table when more than one pattern or truth surface affects the plan:

```text
## Competing-Pattern Inventory
| Pattern | Anchor | Current users | Strength | Weakness / debt | Should become canonical? | Disposition |
| ------- | ------ | ------------- | -------- | --------------- | ------------------------ | ----------- |
| <name> | <path/symbol> | <callers/surfaces> | <why reuse> | <why not copy> | <yes/no/partial/user decision> | <move now/delete now/leave different/named phase/user decision> |
```

Do not let "follow repo convention" mean "copy whichever local pattern was found
first." The plan has to say which convention wins and why.

## Canonical Owner Decision

After the inventory, choose one of these outcomes:

- `extend existing owner`: the best current path can own the behavior
- `promote existing owner`: a path already exists but needs to become the clear
  shared owner
- `merge patterns`: two or more live patterns should collapse into one owner
- `replace with new owner`: a new owner is justified, and the plan says what
  happens to every old path
- `leave variants different`: similar paths have genuinely different contracts,
  and the plan names the reason
- `user decision`: repo truth plus approved intent cannot settle the choice

The decision should name the canonical path, the losing paths, and the proof that
will show the repo did not silently split behavior.

## Disposition Ledger

Every competing source or pattern gets one disposition. These categories match
the existing plan-audit language and should stay boring:

- `move now`: migrate this related code or surface in the current plan because
  leaving it live would split the architecture
- `delete now`: remove an old path made obsolete by the canonical owner
- `leave different`: keep it because it has a real different contract
- `named later phase`: keep it visible in the destination map and assign it to a
  specific later phase, sub-plan, or proof gate
- `user decision`: stop until the user chooses because the repo cannot settle the
  behavior, scope, or compatibility question

No unlabeled "later" bucket. No vague "follow-up." If it matters to the same
contract family, source of truth, migration boundary, or parity story, it needs a
named disposition.

## Unification Phase Rule

Unification is automatically in architecture scope when it is required to remove
duplicate truth, migrate clearly related adopters, delete obsolete paths, or
prevent a new parallel path. It is not optional polish.

That does not mean every plan needs a phase literally named `Unification`.
Instead, Section 7 or the active phase plan must place unification work where its
proof gate belongs:

- in the first slice when the canonical owner must be proven before anything can
  safely widen
- in the migration or cutover phase when old callers must move after the new path
  works
- in a cleanup phase when deletion is safe only after replacement paths are
  proven
- in a named later phase or sub-plan when the destination map keeps the
  obligation visible but its proof gate is not due yet
- as a blocker question when repo truth cannot decide whether unification is
  required

If a competing pattern is included, the plan must say exactly how it will be
unified:

- which owner wins
- which callers or surfaces move
- which paths delete
- which docs, prompts, examples, fixtures, generated artifacts, or install
  surfaces update
- what compatibility posture applies: preserve, clean cutover, or approved
  timeboxed bridge
- what proof shows existing behavior was preserved
- what audit should fail if the old path remains

## Phase-Plan Checklist

Before a phase plan can be implementation-ready, check every catalog row against
the authoritative phase plan:

- every `move now` row appears in a checklist item or exit criterion
- every `delete now` row appears in a checklist item or exit criterion
- every `named later phase` row names the exact phase, sub-plan, or proof gate
- every `leave different` row states the contract difference
- every `user decision` row is resolved or blocks implementation readiness
- every required docs, comments, prompts, examples, fixtures, schemas, generated
  artifacts, and install/routing updates appears in the owning phase
- every consolidation/refactor row has behavior-preservation proof
- no required unification work lives only in `Work`, migration prose, helper
  blocks, or a worklog
- no old and new path can both remain live unless the plan says why that is safe

The active plan's Section 7 remains the one execution checklist. The catalog is
not a second plan; it feeds Section 7.

## How This Works With Depth-First Planning

This method complements `docs/depth_first_phase_planning.md`.

Depth-first planning says to know the full destination, prove the smallest real
working slice, then expand. Pattern convergence says the destination map must
include competing source-truth and pattern obligations, and the first slice must
prove the canonical owner when later work depends on that owner.

Visible later expansion is not a scope cut when it remains assigned to a named
phase or sub-plan. Silent removal is still a scope cut. A plan that proves a new
path but leaves the old path unclassified has not proven the architecture.

## Proof And Review

Convergence work is not done because the plan says it is done. It needs evidence
that fits the risk:

- owner path and representative callers were read
- old entrypoints, side doors, direct writers, alternate readers, and stale docs
  were searched
- preservation signals ran for behavior that should not change
- migration or delete work was verified at the behavior or contract level
- docs, prompts, examples, fixtures, schemas, generated artifacts, and install
  surfaces no longer teach retired behavior
- audits can fail the right thing if old and new paths split again

Prefer existing tests, typechecks, builds, integration checks, fixtures,
instrumentation, or stable manual checks. Do not create grep gates, absence
tests, or repo-shape policing as a substitute for architecture judgment.

## Skill Rollout Plan

This doc is the methodology. The live behavior change should be folded into the
skills in the smallest owning surfaces.

### Plan authors

- `skills/arch-step/references/arch-research.md`: require source-truth and
  competing-pattern inventory in Section 3 when comparable patterns exist.
- `skills/arch-step/references/arch-deep-dive.md`: strengthen the Pattern
  Consolidation Sweep so it names the winning owner, losing paths, disposition,
  unification work, and proof.
- `skills/arch-step/references/arch-phase-plan.md`: make the obligation sweep
  consume the catalog and place all required unification work in Section 7.
- `skills/arch-step/references/arch-auto-plan.md`: treat readiness as blocked
  when included catalog rows are not folded into Section 7 or resolved as
  blockers.
- `skills/arch-step/references/arch-external-research.md`: when outside
  guidance changes a pattern choice, require reconciliation with the internal
  source-truth catalog.
- `skills/miniarch-step/references/*`: mirror the same research, deep-dive,
  phase-plan, and auto-plan rules in the trimmed surface.
- `skills/arch-mini-plan/references/one-pass-plan.md`: add a compact catalog
  before target architecture and phase planning.
- `skills/lilarch/references/plan.md`: add the small-feature version; if the
  catalog creates more than 1-3 phases, escalate instead of compressing it.
- `skills/arch-epic/references/decomposition-principles.md`: add cataloging at
  decomposition time so sub-plans do not split one pattern family across
  multiple owners by accident.

### Enforcers

- `skills/plan-audit/references/architecture-quality-canon.md` and
  `skills/plan-audit/references/review-lenses.md`: fail plans that lack a
  source-truth / competing-pattern catalog when the work introduces or changes a
  pattern.
- `skills/plan-implement/references/artifact-contract.md`: keep catalog
  dispositions in the plan, not only in the implementation log.
- `skills/plan-implement/references/progressive-implementation-loop.md`: require
  implementation slices to keep dispositions current when code truth changes.
- `skills/plan-swarm/references/phase-contract.md`: include canonical source
  truth, competing live surfaces, disposition, and unification proof in worker
  phase contracts.
- `skills/plan-swarm/references/arbiter-and-review.md`: ask the arbiter whether
  unresolved competing patterns or split old/new behavior remain.
- `skills/north-star-investigation/references/shared-doctrine.md`: add only a
  handoff rule: when investigation becomes fixed-scope architecture delivery,
  carry ground-truth anchors, killed hypotheses, and suspected competing paths
  into the planning skill's catalog.

### Shared runtime reference

If this method becomes common enough that repeated copies appear in live skill
references, add a small shared runtime file:

```text
skills/_shared/source-truth-convergence.md
```

That file should be command-first and short. It should not become a script,
runner, scorer, grep gate, checklist executor, or second plan format.

## Anti-Patterns

- new clean path beside old live paths
- wrapper that hides unresolved ownership
- "repo convention" copied from local debt
- migration bridge with no removal phase
- worklog, proposal, audit log, or helper block becoming the real plan
- examples, fixtures, prompts, generated artifacts, or docs teaching retired
  behavior
- multiple writers for one truth
- multiple readers interpreting one format differently
- new deterministic harness because prompt/runtime capability was not inspected
- grep gate or deletion check pretending to prove architecture

## Update Discipline

Update this doc only when the methodology changes. Do not paste it wholesale into
every skill. Runtime skills should carry the short behavior they need and point
to this document only when deeper explanation helps.

Dated proposal docs remain history. The active plan owns active project
decisions. The skill contract owns how an agent behaves during a command. This
doc owns the durable method for making pattern count go down over time.

## Audit Notes — Instruction And Plan (2026-06-12)

These notes audit the original instruction (top of this doc) and the plan above
against the stated goal: arch skills should *collapse* patterns so the codebase
trends toward fewer bug vectors over time, without turning that into a dumb
heuristic or a shim. Findings are grounded in the current skill surfaces with
`path:line` evidence. Bottom line up front:

- The goal is right, and it is **already ~80-90% implemented** across the arch
  surfaces today. The plan reads as if convergence is new capability to add. It
  is mostly existing judgment to *name once* and point at.
- The plan's biggest risk is that its rollout would **create the exact
  duplication it exists to prevent**: hand-editing convergence language into
  ~20 reference files, and publishing two brand-new inventory tables plus a
  re-labeled disposition list beside structures that already exist.
- The one thing that is genuinely new — the *over-time ratchet* that makes
  pattern count actually go **down** across plans — is the least specified part
  of the plan.

### What the plan gets right (keep this)

- Framing convergence as **methodology, not a new runtime contract** (lines
  28-30), and refusing to mandate a literally-named "Unification" phase (lines
  160-180). That correctly resists the literal instruction ("Add a phase to all
  relevant workflows… include a unification phase") in favor of placing proof
  where it belongs. Good judgment; it matches `depth_first_phase_planning.md`.
- The **anti-pattern list** (lines 307-319) and the explicit ban on grep gates /
  absence tests as a substitute for architecture judgment (lines 241-243). These
  are consistent with `AGENTS.md` and `architecture-quality-canon.md:177-186`.
- The genuinely-new, judgment-shaped rollout items (see "What I'd keep" below):
  the north-star→planning handoff payload, the arbiter question, and a one-line
  arch-epic "don't scatter one owner across sub-plans" rule.

### Missed the point (the core risks)

1. **The rollout would manufacture the duplication this doc condemns.** The plan
   proposes editing convergence language into ~20 separate reference files
   (lines 250-293). That is ~20 copies of one doctrine that will drift — the
   precise "multiple writers for one truth" / "new clean path beside old live
   paths" anti-pattern listed at lines 309 and 315. The convergent solution
   already has a precedent in this repo: depth-first doctrine lives as **one**
   short runtime file, `skills/_shared/depth-first-planning.md`, that skills
   reference directly (e.g. `skills/arch-step/references/arch-phase-plan.md:13`),
   paired with the `docs/` explainer. This doc treats its own analog
   (`skills/_shared/source-truth-convergence.md`) as optional, "if this method
   becomes common enough" (lines 296-305). It is already common enough —
   "convergence" appears across 17 arch-step references, plan-audit, and
   miniarch-step today. Under-committing to the shared file *is* the
   "named later phase with no proof gate" move this doc warns against.

2. **The over-time ratchet — the actual North Star — is underspecified.** The
   instruction asks the architecture to "trend toward fewer bug vectors over
   time" and to "collapse patterns instead of adding new ways." The method as
   written is a **static, per-plan cataloging discipline**. Nothing carries an
   unresolved competing-pattern obligation *forward* across plans/epics, and
   nothing observes whether pattern count actually fell. The `named later phase`
   disposition (lines 151-154) is the escape hatch that lets duplication persist
   indefinitely under a respectable label — which is the doc's own
   "migration bridge with no removal phase" anti-pattern (line 312) wearing a
   disposition badge. To hit the goal the method needs a forcing function: a
   deferred convergence obligation must land in a real later proof gate (epic
   destination map, follow-up plan, or decision-log debt with a removal
   trigger), not a perpetual "later." Without that, the catalog can be filled
   forever while the repo keeps splitting.

3. **It measures process, not convergence.** The risk a per-plan catalog invites
   is "did they fill out the table?" instead of "did the repo converge?" A fully
   populated Source-Truth + Competing-Pattern table can sit atop a plan that
   still ships two live paths. The doc's value is the *judgment* (choose one
   owner, delete the loser, prove preservation), not the artifact. Anywhere the
   rollout rewards artifact presence, it has already drifted from the goal.

### Missed (gaps and wrong owners)

- **The method reinvents inventories that already exist, and never reconciles
  them.** The doc defines two new tables — Source-Truth Inventory (lines 87-91)
  and Competing-Pattern Inventory (lines 116-120) — without acknowledging that
  `arch-deep-dive.md` already owns a **Pattern Consolidation Sweep** (prose at
  `:77-87`, table at `:125-128`), and `arch-research.md` already catalogs
  "Canonical path / owner to reuse" and "Duplicate or drifting paths… why it may
  need convergence or deletion" (`:82-83`, `:96-97`). `section-quality.md`
  already threads this through every section: Section 5 "SSOT is clear / no
  parallel paths" (`:196-197`), Section 6 "consolidation sweep names related
  adopters and default dispositions" (`:229`), Section 0 "convergence work and
  product scope" distinguished (`:50`, `:66`). The deep-dive rollout bullet does
  say "strengthen" the existing sweep (line 254) — but the methodology *body*
  invents two competing tables, so the doc contradicts itself: one place says
  extend the single owner, another publishes a parallel format.

- **It introduces a divergent label for an existing category.** plan-audit's
  canonical disposition vocabulary is `move now / delete now / leave different /
  named follow-up / user decision` (`architecture-quality-canon.md:115-119`,
  `proper-audit-checklist.md:84-85`). This doc admits the categories "match the
  existing plan-audit language" (line 145) and then re-labels one of them as
  `named later phase` (lines 152, 199-202). A doc about not splitting one truth
  into two synonyms ships a synonym. Use the existing five labels verbatim.

- **Omitted the surfaces that already own the judgment:**
  - `skills/arch-step/references/arch-consistency-pass.md` is the real
    decision-completeness gate (`Decision: proceed to implement? yes`, see
    `arch-auto-plan.md:28`, `:107-109`). If convergence readiness is a gate, this
    is its semantic home — not `auto-plan`, whose readiness is enforced by a
    presence-checking script (`arch_stage_gate.py`, `arch-auto-plan.md:79-110`).
    The plan routes the readiness change to `auto-plan` (lines 259-261), which
    pushes toward making a script judge semantic catalog content — a grep gate.
  - `skills/plan-audit/references/implementation-audit-mode.md` already enforces
    convergence on *written code* (`canonical-owner-and-ssot`, `existing-pattern-
    fit`, `deletion-and-side-door-closure` at `:143-163`). The plan's plan-audit
    edit targets only the plan-readiness files and skips the code-side enforcer.
  - `skills/plan-audit/references/audit-log-contract.md:64-66,79-84` is the
    suite's *de-facto* disposition catalog already (ledger rows "Canonical owner
    path" / "Legacy and side-door paths" + the SSOT/convergence/deletion lenses).
  - `skills/plan-implement/references/output-contract.md:62-73` is the real
    completion gate ("old paths and side doors… deleted, migrated, or explicitly
    classified"; "source-truth decisions are carried into the plan").

- **"Mirror the same rules" into miniarch-step is a no-op.** miniarch-step
  already carries this doctrine, in places byte-identical: its Pattern
  Consolidation Sweep (`skills/miniarch-step/references/arch-deep-dive.md:117`)
  matches arch-step's; its `shared-doctrine.md` has the convergence rule
  (`:23-26`), SSOT default (`:206-208`), the four-way disposition (`:101-110`),
  and unification-auto-in-scope (`:217`). The instruction is already satisfied;
  re-applying it only risks drift between two copies.

### Over-specified (turns judgment into a heuristic or shim)

- **"Fail plans that lack a catalog" (lines 277-280) is an artifact-presence
  gate over judgment that already catches the real defect.** plan-audit already
  fails duplicate truth / parallel paths / missing deletes / side doors
  semantically: `review-lenses.md:52-65` (`canonical-owner-and-ssot`,
  `existing-pattern-and-convergence`), `architecture-quality-canon.md:106-123`,
  `:158-174`. Keying the failure to a *table's presence* invites both false-fail
  (a strong prose plan with no table) and false-pass (a shallow table that
  satisfies a checkbox while the lens reasoning is skipped). That is exactly the
  mechanical gate `AGENTS.md` and `architecture-quality-canon.md:177-186` reject.
  Keep failing the *condition* (two live paths for one truth), not the artifact.

- **The two fixed-column tables risk becoming fill-in-the-blank ritual.**
  Columns like "Authority level," "Strength," and "Should become canonical?
  (yes/no/partial)" can be completed mechanically without doing the convergence
  thinking. A plan can populate every cell and still not have chosen an owner or
  proven preservation. Prefer a compact prose disposition that names owner,
  losers, and proof — escalate to a table only when scale demands it (the doc
  half-says this at lines 55-57; the rollout then mandates the tables anyway).

- **lilarch's "if the catalog creates more than 1-3 phases, escalate" (line 270)
  is a preset phase-count heuristic — the thing `depth_first_phase_planning.md`
  explicitly names as a failure mode** ("Phase count is a result, not a target";
  "Preset phase count" is a listed Common Failure Mode). It also duplicates
  lilarch's already-correct, better-framed escalation (`plan.md:37-39`,
  `doc-contract.md:64-69`: escalate on a fourth phase or broad migration). Drop
  the number; lilarch already escalates exactly when convergence work balloons.

- **Forcing a catalog into the lightweight tiers violates their charters.**
  arch-mini-plan is explicitly one-pass and compressing ("Write only the
  evidence needed," `shared-doctrine.md:18-22`; good-fit is "I do not want
  staged research and deep-dive commands," `fit-and-escalation.md:7`). lilarch
  is explicitly "contained feature work, not miniature architecture theater"
  and "short enough to hold the whole plan in working memory"
  (`shared-doctrine.md:19-20`, `:36`). Mandating Source-Truth + Competing-Pattern
  tables there is the deep-dive ceremony those tiers exist to avoid, and it
  violates `AGENTS.md` ("include only the requested workflow… leave out invented
  checks, cross-checks"). The convergence *judgment* ("reuse the canonical path;
  delete side paths") already lives in both at the right altitude
  (`one-pass-plan.md:18,30,31`); leave them at that altitude.

- **Routing readiness enforcement to `auto-plan` pushes toward a script gate.**
  Covered above; the fix is to keep convergence readiness in the semantic
  `phase-plan` obligation sweep (`arch-phase-plan.md:36-37,71`) and
  `consistency-pass`, never in `arch_stage_gate.py`.

### What I'd actually change (net)

1. **Keep this as a single `docs/` explainer** (it earns its place, like
   `depth_first_phase_planning.md`). **Delete the two invented tables** from the
   body; point instead at the existing Pattern Consolidation Sweep and the
   research grounding lists. **Adopt plan-audit's five disposition labels
   verbatim** (replace `named later phase` with `named follow-up`).
2. **Replace the ~20-file hand-edit rollout with one short runtime file**,
   `skills/_shared/source-truth-convergence.md`, mirroring the depth-first
   precedent, and reference it only from surfaces that do **not** already carry
   the doctrine. arch-step, miniarch-step, plan-audit, and plan-implement
   already do — they need at most a one-line pointer, not new structure.
3. **Keep only the genuinely-new, judgment-shaped items:** the
   north-star-investigation → planning handoff *payload* (carry ground-truth
   anchors, killed hypotheses, suspected competing paths — but into "the planning
   skill," not "its catalog," since arch-step/lilarch own no catalog artifact);
   the plan-swarm arbiter question ("do unresolved competing patterns or split
   old/new behavior remain?"); a **one-sentence** arch-epic rule ("don't scatter
   one pattern owner across sub-plans"), respecting that file's explicit
   "no checklist… what you need is judgment" stance
   (`decomposition-principles.md:7-11`); and at most one new *field* (not a gate)
   in `plan-swarm/phase-contract.md` for "adjacent competing surfaces +
   disposition."
4. **Add the missing ratchet.** Specify how a deferred convergence obligation is
   guaranteed to come due: it must land in an epic destination map, a named
   follow-up plan, or a Decision-Log debt entry with an explicit removal trigger
   — never a bare "later." This is what makes pattern count fall *over time*
   rather than per-plan.
5. **Do not touch lilarch or arch-mini-plan** beyond the reuse-canonical-path
   judgment they already state.
6. **Run the rollout edits through `$skill-authoring`** before applying them, as
   the original instruction asked. That skill's anti-duplication / anti-heuristic
   lens is precisely what flags items 1-5; the methodology doc was saved, but the
   skill edits have not yet been put through that rigor.

The shortest honest summary: the instruction's goal is sound and mostly already
shipped. Convert this from "add convergence everywhere" to "name convergence
once, point the few thin surfaces at it, add the over-time forcing function, and
delete nothing that already works." Adding more structure to enforce convergence
would itself be a new parallel pattern — the exact thing the method is meant to
stop.
