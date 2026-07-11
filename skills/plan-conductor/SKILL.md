---
name: plan-conductor
description: "Drive an existing plan or phase range to verified completion with the parent as architect and cynical reviewer while transport-selected workers handle implementation, repair, and proof. Use for whole-plan delegated execution with resumable phase-sized slices, a conductor log, diff audits, send-backs, checkpoint commits, and a final gate. Same-host work normally uses clean native children; external sessions remain available when their provider, exact model/profile, lifecycle, isolation, automation, or receipt benefit is deliberate. The explicit `plan-conductor terra` preset keeps its dedicated-worktree, Terra xhigh, three-review, PR-publication, and PR-follow-through path. Not for plan writing, one delegated task, parent-implemented plans, plan audits, multi-plan epics, foreign ordered processes, or read-only opinions."
metadata:
  short-description: "Whole-plan conductor with Terra delivery shortcut"
---

# Plan Conductor

Use this skill when the user wants an entire existing plan document implemented
by phase workers while the smart parent agent preserves its own context and
serves as architect and deeply cynical reviewer.

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

- The plan goes in; verified, reviewed, plan-faithful code comes out.
- Parent tokens go to plan understanding, slice design, and cynical audit.
  Worker tokens go to implementation, repair, and proof runs.
- Chunk size balances two failure modes: micro-tasks turn the parent into a
  slow programmer with extra round-trips; mega-tasks produce unreviewable
  diffs. Default one plan phase per worker.
- Awareness without burn: a size-scoped background heartbeat on every slice
  proves liveness and catches a wedge early with cheap signals. Never tail
  raw worker event streams.
- Every worker return starts NOT ACCEPTED. Worker output — status, summary,
  quoted proof, labels — is a claims manifest to falsify against repo truth,
  never a report to consume. Current code is the only authority.

## Use When

- The user names an existing plan doc and wants the whole thing (or a phase
  range) implemented by delegated phase workers with the parent as reviewer;
  an exact cheaper/faster external fleet may be selected when that is part of
  the desired execution policy.
- The user wants "smart parent, dumb fast hands": an expensive model checking
  work it did not write.
- The plan is arch-step, miniarch-step, arch-mini-plan, or lilarch shaped — or
  any format with recoverable requirements, phases, and done-ness.
- The user wants implementation velocity plus cost control on one long-running
  plan execution.
- The user explicitly invokes `plan-conductor terra` or asks for their
  standard Terra delivery path: dedicated worktree, Terra xhigh execution,
  three new clean external cynical reviews, PR publication, and PR
  follow-through.

## Do Not Use When

- The plan does not exist yet. Use `$arch-step`, `$arch-mini-plan`, or
  `$lilarch`.
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

- The plan remains the single source of truth. The conductor log
  (`<PLAN_STEM>_CONDUCTOR_LOG.md` beside the plan) is schedule, evidence, and
  resume state — never a second plan.
- Whole plan is the default boundary; honor an explicit phase range exactly.
- Apply `../_shared/agent-orchestration-policy.md` at every worker and
  reviewer dispatch. Ordinary same-host slices start as clean native children
  from the plan and conductor-log artifacts. Use an external session when a
  concrete provider, exact cheaper model/profile, durable lifecycle, worktree
  isolation, automation surface, structured receipt, or another real benefit
  is worth the added process and integration cost. These are recognition aids,
  not an allowlist. Honor explicit user choices.
- For an external lane, runtime and effort are supplied by the user. Model or
  profile is also supplied except that an external Codex worker with no named
  model defaults to `gpt-5.6-sol`. Accept `sol`, `luna`, and `terra` as
  `gpt-5.6-sol`, `gpt-5.6-luna`, and `gpt-5.6-terra`. Ask one consolidated
  question only for load-bearing external values. Provider routing remains:
  Codex runs GPT/GBT/OpenAI ids and Fugu profiles, Claude Code runs supported
  Claude models, Cursor Agent runs `composer-2.5-fast`, and Grok runs
  `grok-build` or `grok-composer-2.5-fast`.
- Read the plan once, end to end, at intake. If it yields no observable
  done-ness anywhere — no requirements, checklists, exit criteria, or
  verification obligations — stop before dispatching any worker and report
  what is missing instead of inventing scope.
- Apply `../_shared/scope-and-convergence.md`. Intake must recover the
  human-authorized outcome and approval anchors, smallest sufficient solution,
  initial minimal convergence closure, scope-freeze boundary, enough proof,
  do-not-build boundary, and accepted residual risk. Observable checklists are
  insufficient when that provenance is missing, contradictory, or obviously
  overbroad. Do not dispatch an unfrozen or scope-laundered plan.
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
- Initial workers are new clean children. Repairs resume the exact captured
  child or external session through its original transport. Never resume
  "latest" or reuse an unrelated handle. The optional cold verifier and every
  independent review gate start as new clean children.
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
  decisive proof is independently reproduced by a different clean child before
  acceptance. A worker rebuttal never closes a finding without
  conductor-verified evidence. A clean pass must record which lying-modes
  were checked.
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
- Delegate all verification runs (tests, builds, generators, simulators) to
  workers. The parent runs only cheap read-only inspection commands. Reuse
  fresh passing proof; rerun only on a real invalidator.
- The parent commits local checkpoints after accepted slices and meaningful
  batches. During the conductor stage it never pushes or opens PRs. Only the
  explicit Terra delivery shortcut continues past that boundary, by handing
  the clean implementation to `$pr-authoring` and then
  `$pr-review-followthrough`. Workers never commit, push, stash, or revert
  unrelated work.
- Before phase closure, plan-required proof must be recorded passing. Before
  plan closure, run the final gate: one whole-plan cynical audit sweep plus a
  new clean cold verifier (default on; user may disable).
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
   plan-conductor request selected a Terra worker.
2. Read `references/workflow-contract.md`.
3. Read `references/plan-intake-and-readiness.md`.
4. Read `../_shared/scope-and-convergence.md`.
5. Resolve the plan path, boundary (whole plan unless the user named a phase
   range), per-role transport and starting context, max parallelism, wave cap,
   and cold-verifier toggle. Prefer clean native same-host roles. Resolve and
   ask for runtime/model/effort only when the chosen external lane needs them;
   default an omitted external Codex model to `gpt-5.6-sol`. The Terra shortcut
   supplies its own external execution values, so do not ask for them.
6. Read the plan once end to end. Create or update
   `<PLAN_STEM>_CONDUCTOR_LOG.md` with the extracted execution map, and apply
   the readiness gate.
7. Inspect `git status` and commit an initial or resume checkpoint before
   launching workers, unless a concrete safety issue such as secrets blocks
   it.
8. Read `references/chunking-and-parallelism.md`, then design and dispatch
   the first wave.

## Workflow

1. Extract the plan into the conductor log: requirements, non-goals, phases
   with dependency order, per-phase checklist, verification, exit criteria,
   and cleanup/delete obligations — as anchors into the plan, not copied
   prose.
2. Each wave: pick the next dependency-ready slice or slices, sized by the
   chunking doctrine.
3. Dispatch each slice as a new clean child using the worker prompt contract.
   Prefer the active host's native child; use `$agent-delegate` only for the
   selected external lane. Record transport, starting context, exact child or
   session handle, and any external run directory in the log.
4. Arm the slice's size-scoped watchdog, then wait patiently per the
   monitoring doctrine.
5. On return, audit per `references/audit-and-send-back.md`: enumerate the
   claims to falsify, check them against git, trace the authority path
   beyond the diff, apply the three lens groups, and require decisive proof
   to be independently reproduced. Judge factual validity separately from
   scope disposition. Only factually valid findings already inside the frozen
   contract become repair work.
6. Route: batch accepted findings into one resume prompt and send the session
   back; or accept the slice with evidence anchors and commit a checkpoint;
   or respawn fresh; or escalate and continue independent slices.
7. When a phase's slices are accepted, delegate the phase's plan-required
   verification, record proof in the log, and record phase completion in the
   plan's own format.
8. Repeat until the execution map is clean or a hard stop triggers.
9. Run the final gate: whole-plan cynical audit sweep, the cynical review
   instruments when installed (`$cynical-code-review` by default for
   non-trivial plans, `$cynical-architecture-review` and
   `$cynical-cruft-removal` by judgment from what the plan changed), then
   the delegated cold verifier unless disabled. Triage and repair findings
   through the same send-back machinery. Under the Terra shortcut, defer the
   instrument portion to step 10's three new clean external sessions instead of
   duplicating those reviews; still run the conductor sweep and cold verifier.
   Give every final reviewer the plan path, human baseline anchors, approval
   entries, frozen initial closure, and freeze anchor. Their findings use the
   same scope triage and cannot expand the plan.
10. If the Terra delivery shortcut is active, run its stronger delivery gate:
    all three cynical reviews in independent new clean external Terra sessions,
    repair and re-review accepted findings, then hand off in order to
    `$pr-authoring` and `$pr-review-followthrough` until the PR is merge-ready.
11. Write the final report, commit the final checkpoint, and stop at the
    requested boundary.

## Progress Updates

After each wave and whenever the user asks for status, give one compact
Markdown table: slice, goal, worker/handle, state, attempts, and current
blocker or next action. Refresh from the conductor log and repo state before
answering. Keep chat lean; detail lives in the log.

## Output

Report compactly:

- plan path, boundary, and conductor log path
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
- next action or final verdict with evidence

## Reference Map

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
