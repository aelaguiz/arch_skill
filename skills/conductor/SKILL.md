---
name: conductor
description: "Conduct work to verified completion from a finished plan, a partial plan, or a described outcome; the parent is executive architect and cynical reviewer while workers implement, repair, and prove. Outcome or partial-plan intake first runs an executive shaping stage — parallel worker research, a parent trim to the smallest sufficient solution, a lightweight outcome map, one scope approval — and workers never dispatch before observable done-ness and a frozen scope boundary exist. Default execution is the cheap parallel external fleet (Codex gpt-5.6-sol at ultra via agent-delegate, one-word swaps to Kimi, Grok, Cursor, or Claude); native children stay a narrow exception, and Codex usage limits rotate via aim without losing sessions. The `conductor terra` preset keeps its dedicated-worktree, Terra xhigh, three-review, PR-publication, and follow-through path. Not for single bugs, open-ended metric loops, multi-plan epics, plan audits, one delegated task, parent-implemented plans, or read-only opinions."
metadata:
  short-description: "Plan-or-outcome conductor with executive shaping and a cheap external fleet"
---

# Conductor

Use this skill when the user wants a goal conducted to verified completion by
delegated workers while the parent agent preserves its own context and serves
as executive architect and deeply cynical reviewer. Intake spans a spectrum —
a finished plan document, a partial plan, or a described outcome. What already
exists on disk decides how much shaping happens first; the execution
machinery is identical for all three.

The role economy is the point. The parent spends its scarce context on
judgment, not keystrokes: it reads the plan once, designs well-sized slices,
delegates implementation through transport selected under the shared agent
policy, and spends its tokens on evidence-based review. Workers implement,
repair, and run proof. The send-back loop — resume the exact worker with batched
audit findings until the slice contract is true in code — is what makes
delegated workers safe.

This is a prompt-first orchestration skill. It ships no runner, controller,
state machine, or script. The parent agent is the orchestrator; the conductor
log beside the plan is its durable memory.

## North Stars

- A plan or outcome goes in; verified, reviewed, contract-faithful code comes
  out.
- Parent tokens go to plan understanding, slice design, cynical audit
  judgment, and first-hand verification of finished work products. Fleet
  tokens go to investigation, implementation, repair, proof runs, and heavy
  review reading. Native subagents bill the parent's expensive model — they
  are not a cheap lane, so bulk work never routes to them.
- The parent is the scope judge. Fast cheap workers are genuinely smart but
  over-scope and over-iterate; the parent trims every proposal to the
  smallest sufficient solution and holds the frozen boundary against
  expansion pressure from any direction.
- Chunk size balances two failure modes: micro-tasks turn the parent into a
  slow programmer with extra round-trips; mega-tasks produce unreviewable
  diffs. Default one plan phase per worker.
- Awareness without burn: a size-scoped background heartbeat on every slice
  proves liveness and catches a wedge early with cheap signals. Never tail
  raw worker event streams.
- Every worker return starts NOT ACCEPTED. Worker output — status, summary,
  quoted proof, labels, conclusions — is a claims manifest to falsify against
  repo truth, never a report to consume. The authority is what the conductor
  verifies first-hand: current code, and the work products it has personally
  loaded and checked.

## Use When

- The user names an existing plan doc and wants the whole thing (or a phase
  range) implemented by delegated phase workers with the parent as reviewer.
- The user has a described outcome or a partial plan — not a finished plan —
  and wants the parent to decompose it, using worker research where useful,
  approve a scope boundary once, and then conduct execution without a
  separate planning invocation.
- The user wants the parent to preserve architectural and review context while
  capable workers own implementation and proof inside plan-authorized slices.
- The plan is arch-step, miniarch-step, arch-mini-plan, or lilarch shaped — or
  any format with recoverable requirements, phases, and done-ness.
- The user wants implementation velocity plus cost control on one long-running
  plan execution.
- The user explicitly invokes `conductor terra` or asks for their
  standard Terra delivery path: dedicated worktree, Terra xhigh execution,
  three new clean external cynical reviews, PR publication, and PR
  follow-through.

## Do Not Use When

- The plan artifact itself is the deliverable, or the work needs full
  architecture ceremony (research, deep-dives, staged review gates) before
  any execution. Use `$arch-step`, `$arch-mini-plan`, or `$lilarch`, then
  hand the finished plan back here.
- The goal is clear but no definable done-state exists even in principle —
  open-ended optimization or metric improvement. Use `$goal-loop`; the
  conductor requires observable done-ness before dispatch.
- The user wants the parent to implement the plan itself rather than remain a
  non-implementing architect. Use `$plan-implement`.
- The user wants one concrete external delegated task rather than plan-sized
  orchestration. Use `$agent-delegate`; dispatch an ordinary same-host task
  directly through the active host's native child system.
- The user wants a plan audited, not implemented. Use `$plan-audit`.
- The work is a multi-plan epic decomposition. Use `$arch-epic`.
- The workflow is a strict ordered process from another repo's doctrine. Use
  `$stepwise`.
- The user wants a read-only second opinion. Use `$fresh-consult`.

## Non-Negotiables

- The conducted artifact — the finished plan, or the approved outcome map
  when shaping produced one — is the single source of truth, and "the plan"
  below always means that artifact. The conductor log
  (`<PLAN_STEM>_CONDUCTOR_LOG.md` beside it) is schedule, evidence, and
  resume state — never a second plan.
- Whole plan is the default boundary; honor an explicit phase range exactly.
- Apply `../_shared/agent-orchestration-policy.md` at every worker and
  reviewer dispatch, and apply `$prompt-authoring` to every actual populated
  first brief or materially reframed follow-up. The conductor's default
  execution lane is the cheap parallel external fleet — clean resumable
  Codex workers through `$agent-delegate` — as a deliberate standing policy
  choice: conduction exists to preserve parent context and buy fast cheap
  worker cycles, and that exact cheaper/faster model is the concrete benefit
  the shared policy asks external transport to name. The fleet default
  applies to every role — phase workers, research workers, verification
  workers, the cynical review instruments, and the cold verifier. Native
  children run the parent's expensive model, so they are never the cheap
  lane and never the default for reviews or any other bulk reading; reserve
  them for a genuinely tiny errand a fleet round-trip would dwarf, a
  capability only the host exposes, an explicit user ask, or an unavailable
  external runtime. Honor explicit user choices in both directions.
- For an external lane, runtime and normally model/profile plus effort are
  supplied by the user. An external Codex worker with no named model defaults
  to `gpt-5.6-sol`, and an omitted effort on that Sol worker defaults to
  `ultra`; a Kimi worker with omitted model and effort defaults to
  `kimi-code/k3` at `max`. Accept `sol`, `luna`, and `terra` as
  `gpt-5.6-sol`, `gpt-5.6-luna`, and `gpt-5.6-terra`. Ask one consolidated
  question only for load-bearing external values. Provider routing remains:
  Codex runs GPT/GBT/OpenAI ids and Fugu profiles, Claude Code runs supported
  Claude models, Cursor Agent runs `composer-2.5-fast`, natural Grok wording
  resolves to `grok-4.5`, and Kimi runs `kimi-code/k3` with an omitted-effort
  default of `max`. Explicit legacy Grok ids remain exact and discovery-gated.
- When intake is a described outcome or a partial plan, run the executive
  shaping stage per `references/shaping-and-outcome-map.md` before any plan
  intake: worker research as evidence, a parent-owned trim to the smallest
  sufficient solution, an outcome map written beside the work, and one user
  approval of the scope boundary — skippable only by an explicit user
  `full-auto` grant. Research workers propose; they never decide, and no
  worker implements anything during shaping.
- Read the plan once, end to end, at intake. If it yields no observable
  done-ness anywhere — no requirements, checklists, exit criteria, or
  verification obligations — stop before dispatching any worker and report
  what is missing instead of inventing scope. The readiness gate applies to
  a shaped outcome map exactly as to a finished plan and is never waived;
  shaping happens before the gate, never around it.
- Apply `../_shared/scope-and-convergence.md`. Intake must recover the
  human-authorized outcome and approval anchors, smallest sufficient solution,
  initial minimal convergence closure, scope-freeze boundary, enough proof,
  do-not-build boundary, and accepted residual risk. Observable checklists are
  insufficient when that provenance is missing, contradictory, or obviously
  overbroad. Do not dispatch an unfrozen or scope-laundered plan. When
  shaping produced the outcome map, the recorded scope approval (or the
  explicit `full-auto` grant) is the human authorization anchor and the
  freeze.
- The initial architecture window is already closed when conductor execution
  begins. Workers, the conductor, warm audits, cold verification, cynical
  reviews, PR feedback, and repeated findings cannot add to the frozen closure.
  A newly discovered same-contract adjacent path requires a human decision.
- The conductor never edits source code. It edits only coordination artifacts
  and plan completion annotations. It never edits the plan's requirements,
  checklists, or exit criteria to match what was built; scope changes escalate
  to the user.
- Plan completion annotations may record execution truth only. The conductor
  may not edit scope, requirements, or the initial closure to normalize worker
  or reviewer discoveries. Post-freeze expansion requires explicit human
  approval and a re-frozen plan before dispatch resumes.
- Initial workers are new clean fleet sessions (native children only under
  the narrow exceptions above). Repairs resume the exact captured session
  through its original transport. Never resume "latest" or reuse an
  unrelated handle. The optional cold verifier and every independent review
  gate start as new clean fleet sessions — external cheap-model workers,
  never native subagents by default, because review reading is bulk work
  and native subagents bill the parent's model.
- Native starting context is explicit at dispatch. Codex always sets
  `fork_turns` to `"none"` for a clean phase worker or critic, to a positive
  count for deliberately bounded chat context, or to `"all"` only when the
  whole conversation is genuinely required. Claude uses a clean named
  subagent by default; an explicit conversation fork means full inherited
  conversation, while a skill with `context: fork` is an isolated clean
  subagent context. Context choice never implies permissions, capabilities, or
  worktree isolation.
- The parent owns decomposition, fanout, and integration. Every child prompt
  forbids creating more model agents or invoking delegation/consult skills
  unless the parent deliberately assigns a bounded nested scope and budget.
- Chunk default is one plan phase per worker. Split only along owner
  boundaries the plan itself names; merge trivial adjacent phases that share
  one design intent; when unsure, chunk bigger. Never one file per worker,
  never micro-tasks, never two workers into one unsettled design decision.
- Parallelize only dependency-ready slices on disjoint surfaces. Serial
  execution is correct when the plan is serial.
- Arm a size-scoped liveness monitor on every dispatched slice: heartbeat
  floor five minutes, ceiling thirty, scaled to the slice's expected
  duration. Each beat emits one compact liveness-and-progress line, relayed to
  the user as a brief check-in, plus a wedge alert when the worker dies, stalls
  with no progress across beats, or overruns its ceiling. This is standing
  practice on every dispatch, resume, and respawn — never wait for the user to
  ask for it, and never clear it after a slice and forget to re-arm the next.
  Cheap signals only; never stream an external lane's `events.jsonl` into
  parent context during normal operation. Quiet with a live heartbeat is not
  stuck; act on evidence, not silence.
- Audit with inverted burden of proof before accepting any slice: enumerate
  the worker's claims, falsify them against git and current code, trace the
  authority path beyond the diff (side doors live in files the diff did not
  touch), and apply the integrity, architecture, and cruft lens groups from
  `references/audit-and-send-back.md`. Worker-quoted verification is a claim;
  decisive proof is independently reproduced by a different clean fleet
  worker before acceptance. A worker rebuttal never closes a finding without
  conductor-verified evidence. A clean pass must record which lying-modes
  were checked.
- Verify the work product itself before believing any completion claim, and
  treat that verification as sanctioned first-class parent spend — loading
  the artifact is never token waste. Existence is not evidence, and neither
  is plausible shape. A screenshot is accepted only after the conductor has
  viewed it and confirmed it shows the claimed state — not a blank page,
  error screen, wrong screen, or stale build; a spreadsheet or data model
  only after the conductor opened it and checked the math — representative
  totals spot-recomputed, formulas traced to stated assumptions, key
  numbers tied to their sources; a report only after its assertions were
  checked against current code; a generated file only after it was opened
  and spot-checked against its claimed source. Delegate inspection only for
  an artifact class the conductor genuinely cannot render, and require
  extracted evidence back — values, quotes, described screen content —
  never a verdict. The implementing worker's description of its own
  artifact never counts as inspection.
- Never adopt a worker's analytical conclusion at face value. A conclusion
  the conductor acts on, relays, or closes a finding with must carry
  anchors the conductor has verified; an unanchored conclusion goes back
  for evidence as a hypothesis, not forward as a fact.
- Separate factual validity from scope authority for every finding. Record one
  shared scope disposition. Only `authorized` and
  `frozen-convergence-required` become send-backs. `new-scope-needs-human` is
  escalated, `out-of-scope` stays an observation, and
  `unauthorized-built-scope` requires subtraction unless a human ratifies and
  re-freezes it. Repetition never changes the disposition.
- Batch all accepted findings into one resume prompt per repair round. Caps:
  3 send-backs per worker handle, then 1 new clean respawn with a sharpened
  brief, then escalate the slice and continue independent work. The same finding surviving
  two consecutive send-backs marks the worker unhealthy immediately. Two
  consecutive malformed or failed child runs on one slice escalate it.
- A Codex fleet worker that dies on a hard usage limit is continued, not
  replaced: rotate accounts and resume the exact captured session per
  `$agent-delegate`'s usage-limit continuity and
  `../_shared/aim-rotation.md`. Rotation is not a send-back, respawn, or
  failed run for cap purposes; record it in the conductor log.
- Delegate all proof runs (tests, builds, generators, simulators) to
  workers; decisive proof counts only when a different clean fleet worker
  reproduced it. The parent runs read-only inspection, which includes
  personally loading and reading work-product artifacts — that verification
  belongs to the parent and is never delegated for economy. Reuse fresh
  passing proof; rerun only on a real invalidator.
- The parent commits local checkpoints after accepted slices and meaningful
  batches. During the conductor stage it never pushes or opens PRs. Delivery
  past that boundary — when the user asked for the work to be published, and
  always under the Terra shortcut — is itself delegated: a dedicated
  delivery worker, a child and never the parent, runs `$pr-authoring` and
  then `$pr-review-followthrough` on the finished branch until CI is green
  and the PR is merge-ready. The parent verifies the outcome first-hand —
  the published PR loaded and read, CI state checked — before closing, and
  never merges or enables auto-merge without a separate user ask. Other
  workers never commit, push, stash, or revert unrelated work; only the
  explicitly assigned delivery worker touches push and PR operations.
- Before phase closure, plan-required proof must be recorded passing. Before
  plan closure, run the final gate: one whole-plan cynical audit sweep —
  which personally loads the plan's end-state work products, a check no
  toggle disables — plus a new clean cold verifier (default on; user may
  disable).
- Record completion the way the plan format already records it (for example
  `Status: COMPLETE` under arch phase headings plus a worklog entry, or
  checkbox ticks). Never hand-edit script-owned `arch_skill:block:*` receipt
  blocks and never write the `plan-audit` sidecar; those belong to their
  owning skills.
- Default wave cap is 25 (one wave = design, dispatch, wait, audit, route),
  user-tunable. When a cap or the readiness gate stops the run, report
  blockers plainly with the log as evidence; escalation is a first-class
  outcome, not a failure.

## First Move

1. If the user explicitly invoked the Terra delivery shortcut, read
   `references/terra-delivery-shortcut.md` and apply its locked execution and
   delivery policy. Do not activate the shortcut merely because an ordinary
   conductor request selected a Terra worker.
2. Read `references/workflow-contract.md`.
3. Place the intake on the spectrum. A finished plan with recoverable
   done-ness continues directly. A described outcome or a partial plan first
   runs the shaping stage — read `references/shaping-and-outcome-map.md`,
   produce the approved outcome map, and continue with that map as the
   conducted artifact.
4. Read `references/plan-intake-and-readiness.md`.
5. Read `../_shared/scope-and-convergence.md`.
6. Resolve the artifact path, boundary (whole plan unless the user named a
   phase range), per-role transport and starting context, max parallelism,
   wave cap, and cold-verifier toggle. The fleet default is external Codex
   `gpt-5.6-sol` at `ultra`; a user-named provider swaps the whole fleet —
   Kimi to `kimi-code/k3` at `max`, Grok to `grok-4.5`, Cursor to
   `composer-2.5-fast`, Claude to a supported Claude model — resolved
   through `$agent-delegate`. Ask one consolidated question only for
   load-bearing missing values. The Terra shortcut supplies its own external
   execution values, so do not ask for them.
7. Read the plan once end to end and extract the execution map in context.
8. Before creating or updating the conductor log, inspect `git status` and
   capture the start commit and inherited worktree state. Then write the
   extracted execution map to `<PLAN_STEM>_CONDUCTOR_LOG.md` and record the
   start commit, then apply and record the readiness gate. If the gate passes,
   take an initial or resume checkpoint before launching workers only when the
   inherited worktree already held plan work to preserve (per Git Posture) —
   never an empty checkpoint just to mark intake. Skip it on a concrete safety
   issue such as secrets or clearly unrelated files.
9. Read `references/chunking-and-parallelism.md`, then design and dispatch
   the first wave.

## Workflow

1. If intake is a described outcome or a partial plan, run the shaping stage
   per `references/shaping-and-outcome-map.md`: worker research as evidence,
   parent trim to the smallest sufficient solution, the outcome map written
   beside the work, one scope approval, freeze. The approved map is the
   conducted artifact everywhere "the plan" appears below.
2. Extract the plan into the conductor log: requirements, non-goals, phases
   with dependency order, per-phase checklist, verification, exit criteria,
   and cleanup/delete obligations — as anchors into the plan, not copied
   prose.
3. Each wave: pick the next dependency-ready slice or slices, sized by the
   chunking doctrine.
4. Dispatch each slice as a new clean child using the worker prompt contract —
   by default a fresh-resumable external fleet worker through
   `$agent-delegate`, or a native child when that lane was selected. Record
   transport, starting context, exact child or session handle, and any
   external run directory in the log.
5. Arm the slice's size-scoped watchdog, then wait patiently per the
   monitoring doctrine. A hard usage-limit death is continued by rotate and
   exact-session resume, not by replacement.
6. On return, audit per `references/audit-and-send-back.md`: enumerate the
   claims to falsify, check them against git, trace the authority path
   beyond the diff, personally load and verify every claimed work product,
   falsify analytical conclusions at their anchors, apply the three lens
   groups, and require decisive proof to be independently reproduced. Judge
   factual validity separately from scope disposition. Only factually valid
   findings already inside the frozen contract become repair work.
7. Route: batch accepted findings into one resume prompt and send the session
   back; or accept the slice with evidence anchors and commit a checkpoint;
   or respawn fresh; or escalate and continue independent slices.
8. When a phase's slices are accepted, delegate the phase's plan-required
   verification, record proof in the log, and record phase completion in the
   plan's own format.
9. Repeat until the execution map is clean or a hard stop triggers.
10. Run the final gate: whole-plan cynical audit sweep, then the cynical
   review instruments when installed — each dispatched as its own clean
   external fleet session, never a native subagent (`$cynical-code-review`
   by default for non-trivial plans, `$cynical-architecture-review` and
   `$cynical-cruft-removal` by judgment from what the plan changed), then
   the fleet cold verifier unless disabled. Triage and repair findings
   through the same send-back machinery. Under the Terra shortcut, defer the
   instrument portion to step 11's three new clean external sessions instead of
   duplicating those reviews; still run the conductor sweep and cold verifier.
   Give every final reviewer the plan path, human baseline anchors, approval
   entries, frozen initial closure, and freeze anchor. Their findings use the
   same scope triage and cannot expand the plan.
11. If the Terra delivery shortcut is active, run its stronger delivery gate:
    all three cynical reviews in independent new clean external Terra
    sessions, with accepted findings repaired and re-reviewed.
12. When the user asked for the work to be published (always true under
    Terra), dispatch a dedicated delivery worker — a child, never the
    parent — to run `$pr-authoring` and then `$pr-review-followthrough` on
    the finished branch until CI is green and the PR is merge-ready. Track
    it with the normal heartbeat doctrine, then verify the result
    first-hand: load the published PR, read what was posted, and check CI
    state. Give the user the Delivery Report when the PR goes up and again,
    refreshed, at merge-ready.
13. Write the final report, commit the final checkpoint, and stop at the
    requested boundary.

## Progress Updates

After each wave and whenever the user asks for status, give one compact
Markdown table: slice, goal, worker/handle, state, attempts, and current
blocker or next action. Refresh from the conductor log and repo state before
answering. Keep chat lean; detail lives in the log.

## Delivery Report

When the delivery worker publishes the PR, and again when follow-through
reaches merge-ready, give the user the same at-a-glance report, refreshed
from the conductor log and first-hand-verified PR state — never from memory
or the worker's narrative:

| Field | Value |
|---|---|
| PR | \<url\> (\<branch\> → \<base\>) |
| State | published \| merge-ready |
| CI | passing \| failing (name the check) \| pending |

Then four short bullet sections:

- **Accomplished** — what shipped, stated against the plan's requirements
  with their anchors.
- **Tested** — the decisive proof: each check, its scope, its result, and
  who ran it (from the proof ledger's `Ran by`).
- **Reviewed** — which audits, review instruments, and verifiers ran, their
  verdicts, and finding counts: accepted / repaired / rejected.
- **Issues** — escalations, notable send-backs, usage-limit rotations,
  deferred items, and anything the user should know; `none` when true.

The merge-ready report updates the publication report; it does not retell
the run story.

## Output

Report compactly:

- conducted artifact path (plan or outcome map), boundary, and conductor log
  path
- worker policy (transport, starting context, and any external
  runtime/model/effort) and max parallelism
- per-wave status table
- slices accepted, sent back, respawned, escalated, or deferred, with attempt
  counts
- proof run, reused, or still owed, with the invalidator reasoning
- findings triage summary and any rejected-finding evidence
- scope-integrity summary: contract anchor, human decisions requested, scope
  cycles found, and unauthorized work subtracted
- commits made, files changed, and plan completion annotations written
- escalations with the specific user decision each one needs
- the Delivery Report when delivery ran (PR, CI, accomplished / tested /
  reviewed / issues)
- next action or final verdict with evidence

## Reference Map

- `references/shaping-and-outcome-map.md` - executive shaping stage for
  outcome or partial-plan intake, and the outcome map contract
- `references/workflow-contract.md` - conductor lifecycle, roles, git posture,
  and stop discipline
- `references/plan-intake-and-readiness.md` - format-agnostic extraction,
  readiness gate, and the arch-format fast path
- `references/chunking-and-parallelism.md` - slice sizing litmus tests and
  parallel launch judgment
- `references/delegation-and-monitoring.md` - transport selection, native and
  external continuation, patient monitoring, and the parent token economy
- `references/audit-and-send-back.md` - cynical audit lenses, finding triage,
  send-back caps, escalation, and the final gate
- `references/terra-delivery-shortcut.md` - explicit standard Terra worktree,
  implementation, independent review, repair, PR, and follow-through path
- `references/worker-prompt-contract.md` - worker slice prompt skeleton,
  required footer, and send-back prompt shape
- `references/conductor-log-contract.md` - conductor log layout, status
  enums, proof ledger, and exit probe
