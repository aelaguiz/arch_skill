# Plan Intake And Readiness

The conductor works with any plan document that has recoverable requirements
and phases. Intake is a one-time extraction pass by the parent, not format
parsing, and it is the single largest deliberate spend of parent tokens —
worth it because every later decision keys off this read.

## What To Extract

Read the plan once, end to end, and record in the conductor log:

- **Requirements and non-goals** — whatever the plan calls them: North Star,
  definition of done, requirements block, issue checklist, acceptance list.
- **The phase or work-item list with dependency order.** The plan's own
  ordering is authoritative; depth-first plans are ordered for a reason. If
  the plan has requirements but no phases, derive waves from dependency
  reasoning and record that derivation as conductor judgment, not plan truth.
- **Per-phase contract** — goal, must-do checklist, required verification
  (exact commands, scenarios, or manual proof when the plan names them), exit
  criteria, cleanup and **delete obligations** (the most commonly dropped
  items and a named audit target), rollback notes.
- **Anchors, not prose.** Record plan section headings and `path:line` code
  anchors. Link to long plan sections; never paste them. The plan stays the
  single source of truth; the log is schedule and evidence.
- **Scope authority and proportionality.** Record anchors for the original
  human outcome, explicit later human approvals, smallest sufficient solution,
  initial minimal convergence closure or `none`, pre-implementation freeze,
  enough proof, do-not-build boundary, and accepted residual risk. Do not copy
  the contract into the log.

## Readiness Gate

If, after a genuine attempt, the plan yields no observable done-ness anywhere
— no requirements, no checklists, no exit criteria, no verification
obligations — stop before dispatching any worker. Report exactly what is
missing and suggest a planning pass (`$plan-audit` readiness mode,
`$arch-mini-plan`, or `$lilarch`). Driving workers against unobservable
done-ness produces confident wandering, not implementation.

Underspecified-but-recoverable plans do **not** trip the gate. When a phase
says "migrate the callers" without listing them, recover the real contract
from owning code, tests, schemas, and current behavior, and record the
recovered facts in the log only when the frozen contract already authorizes
that caller family. Recovered facts support execution; they never expand
approved scope.

Also stop before dispatch when the plan is visibly overbroad, cites only its
own agent-authored text as authority, lacks a defensible scope-freeze boundary,
has an open-ended convergence promise, or asks for proof and machinery
disproportionate to the human outcome. If initial planning is still open, route
the defect to the planning owner. If implementation has begun or the plan is
legacy and the boundary cannot be recovered, request one human scope decision.
The conductor never performs a late initial-architecture pass itself.

## Arch-Format Fast Path

When the doc carries arch-suite structure, map it directly instead of
re-deriving it:

- `arch_skill:block:phase_plan` or a `Depth-First Phased Implementation Plan`
  section is the authoritative phase list.
- Per-phase fields `Goal`, `Checklist (must all be done)`,
  `Verification (required proof)`, `Exit criteria (all required)`, and
  `Rollback` map straight into the per-phase contract. Checklist and exit
  criteria are jointly the authoritative phase-exit surface; `Work` prose
  alone never carries obligations.
- Requirements come from the Holistic North Star subsections (claim, in
  scope, out of scope, definition of done, invariants) or
  `lilarch:block:requirements`.
- Scope authority comes from the Scope and Simplicity Contract and its Section
  10 human-approval anchors. An agent-authored Decision Log entry proves only
  that a change was recorded; it does not prove approval.
- Existing `Status:` annotations under phase headings tell you what prior
  runs already completed; trust them only after spot-checking the code
  anchors, since false-complete phases are exactly what the audit exists to
  catch.
- An existing `<PLAN_STEM>_PLAN_AUDIT.md` with open `PLA-*`/`IMP-*` findings
  supplies pre-existing findings. Treat only findings dispositioned
  `authorized` or `frozen-convergence-required` as slice constraints. Other
  findings remain observations, subtraction work, or human decisions.

This is recognition of structure that happens to be present — never a
requirement, and never a reason to reject a plan that lacks it.

## Ambiguity After Intake

Outcome-changing ambiguity discovered mid-run — a requirement two slices
interpret differently, an unsettled design decision a phase silently assumes —
is an escalation event, not a judgment call to delegate to a worker. Record
it in the log's escalation section, keep independent slices flowing, and put
the specific decision in front of the user. Ordinary implementation-level
choices implied by repo evidence stay with workers.

## Resume Behavior

If `<PLAN_STEM>_CONDUCTOR_LOG.md` already exists at intake, this is a resumed
run: read the log's resume snapshot and execution map, spot-check that
recorded slice states still match repo reality (a recorded `accepted` whose
code anchors are gone is stale), refresh what changed, and continue. Do not
re-extract the plan from scratch and do not redo audits the log records as
current unless evidence says they are stale.
