# Workflow contract: re-entrant modes the skill runs

The skill runs one mode per turn. Most modes are chosen from the epic
doc's state, not from a user command. The explicit automation modes
also use the user's command-shaped ask: `auto-plan`, `auto-implement`,
or role-based automatic execution. The user types whatever; the
skill reads the doc and picks the right mode.

This file names each mode, its trigger, its inputs, its outputs,
its failure modes, and exactly where judgment happens vs where
determinism happens.

## Mode: `start`

### Trigger
- User invokes `$arch-epic` with a goal in prose, and either:
  - No epic doc path was named, no epic doc is visible in the
    session context, and the `docs/` directory contains no
    matching `EPIC_*.md`, OR
  - The user explicitly said "start a new epic" or equivalent.

### Inputs
- The user's verbatim goal prose.
- The current working directory (becomes the orchestrator repo
  root for path resolution).

### Outputs
- A fresh epic doc at the proposed (or user-overridden) path with
  full frontmatter, TL;DR, draft Decomposition, empty
  Orchestration Log (one entry), empty Decision Log.
- The Decomposition surfaced to the user for approval.

### Actions
1. Propose the epic doc path following the convention in
   `epic-doc-contract.md`. If the user's invocation named a path,
   use it. If the user is silent and the proposed path exists
   already, append `_v2` and re-propose.
2. Resolve critic transport per `model-and-effort.md`. Prefer a clean native
   child in the active host and do not invent runtime/model/effort fields the
   host cannot confirm. If an external critic was deliberately selected, ask
   one consolidated question for missing external values. Same-session
   `auto-plan` runs no critic during planning. An explicit external harness
   defers its role values to the role-table gate in `auto-run`; the legacy
   interactive critic tuple may remain pending/null.
3. Write the epic doc: frontmatter (with hashes), TL;DR in plain
   English, draft Decomposition per `decomposition-principles.md`
   (one sentence each, ordering by dependency then risk, gates as
   assertions not tasks, count chosen from proof boundaries rather than
   a preset range).
4. Append one Orchestration Log entry: `Goal captured.
   Decomposition drafted (<N> sub-plans). Awaiting user approval.`
5. End turn. Surface the Decomposition and ask the user to approve
   or adjust.

### Where judgment lives
- Decomposition drafting. The skill reads the user's goal, its
  knowledge of the repos involved, and produces an ordered list.
  This is prose reasoning.
- Critic transport and any external runtime/model/effort interpretation when
  the user gave partial answers.

### Where determinism lives
- Path proposal (slugify the goal, append date).
- Hash computation.
- Frontmatter write.
- Log entry append.

### Failure modes
- The user's goal references a system or concept that cannot be
  located. Announce the gap and ask before drafting. Do not guess
  at sub-plan boundaries.
- Two equally valid decompositions exist. Present both briefly at
  the approve-decomposition gate; let the user pick.
- The proposed epic doc path already exists and contains a
  different epic. Ask before overwriting — do NOT overwrite
  silently.

## Mode: `approve-decomposition`

### Trigger
- Epic doc exists, `sub_plans_approved: false`, and the user has
  replied to the drafted Decomposition (approval or adjustments).

### Inputs
- The user's reply text.
- The current epic doc.

### Outputs
- Updated Decomposition reflecting any user adjustments.
- Epic doc frontmatter with `sub_plans_approved: true`,
  `status: active`.
- Orchestration Log updated with the approval event.

### Actions
1. Interpret the user's reply:
   - Explicit approval ("looks good", "approved", "yes"): apply
     no changes, flip flag.
   - Adjustments ("swap 2 and 3", "combine 2 and 3", "drop 4",
     "rename 2 to X"): apply the adjustments to the Decomposition
     in order. Re-validate (one-sentence test, gates as
     assertions, etc.). Flip flag.
   - Rejection ("no, I don't like this split"): do NOT flip the
     flag. Re-enter `start` mode's drafting step with the user's
     feedback as context.
2. Write epic doc changes.
3. Append Orchestration Log entry naming the adjustments (or
   confirming clean approval).
4. End turn.

### Where judgment lives
- Interpreting the user's reply. "Keep 1 and 3, I'm not sure about
  2" is an adjustment request disguised as approval; treat it as
  such.

### Where determinism lives
- Frontmatter flip.
- Log append.

### Failure modes
- User reply is ambiguous. Ask a targeted question, do not guess.
- User adjustment would violate the decomposition principles
  (e.g., "split sub-plan 1 into two parts where part B needs part
  A's internals"). Push back with the principle and the example;
  let the user decide whether to overrule.

## Mode: `run`

### Trigger
- Epic doc has `sub_plans_approved: true`, `status: active`, and
  no pending scope-change question.

### Inputs
- Epic doc.
- All sub-plan DOC_PATHs (as they exist on disk).
- all sub-plan planning, worklog, and audit truth visible in each DOC_PATH.

### Outputs
- One arch-step command invoked, OR epic critic run, with matching Orchestration Log entry.
- Updated sub-plan Status in the Decomposition.

### Actions
Run the routing logic in `arch-step-integration.md` against the
first sub-plan whose Status is not `complete`. Execute exactly one
transition per turn, then end the turn. Don't chain multiple
transitions in the same turn; each transition needs fresh doc truth before
the next routing decision.

### Where judgment lives
- Detecting disagreements between stored Status and observed
  reality. When they differ, prose reasoning decides what the real
  state is.
- Deciding whether an epic critic verdict can be repaired inside the
  current sub-plan or needs a new sub-plan per
  `scope-change-discipline.md`. Material scope findings always halt
  for a scope-preserving user decision.

### Where determinism lives
- Reading sub-plan docs.
- Invoking arch-step commands.
- Writing log entries.
- Dispatching the critic through the selected transport; external invocation
  and parsing use `scripts/run_arch_epic.py`.

### Failure modes
- auto-plan or implement-loop ended without expected completion
  markers. Surface to the user; do not silently advance.
- Audit block says NOT COMPLETE or has reopened phases. Halt with
  the arch-step audit's reported blockers; let the user decide.
- Critic verdict is `incomplete` (check 4 failed). Halt, surface
  the arch-step audit block contents.

## Mode: `auto-plan`

### Trigger
- Epic doc has `sub_plans_approved: true`.
- User explicitly asks for `arch-epic auto-plan`, asks to plan every
  sub-plan before implementation, or resumes an existing same-session
  auto-plan pass.

### Inputs
- Epic doc.
- Approved Decomposition.
- All existing sub-plan DOC_PATHs.
- `arch-step` planning truth inside each sub-plan doc.

### Outputs
- Missing sub-plan DOC_PATHs assigned under the normal per-epic path.
- At most one sub-plan DOC_PATH set up or advanced in a bounded turn, with a
  matching Orchestration Log entry.
- Sub-plan Status kept at or downgraded to `planning` until the exact
  DOC_PATH passes the ArcStep generated receipt gate.
- Sub-plan Status set to `planned` only after
  `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`
  exits 0 for that same DOC_PATH.

### Actions
1. Select the first sub-plan whose Status is not `planned` or `complete`.
2. If no such sub-plan exists, report that every non-complete sub-plan is
   planned and the next command is `$arch-epic auto-implement <EPIC_DOC_PATH>`.
3. If the sub-plan has no DOC_PATH, assign the grouped per-epic path and write
   it into the Decomposition.
4. If the DOC_PATH is missing, create it by applying the `arch-step` `new`
   artifact contract directly in the visible session. If the DOC_PATH exists
   but lacks the required `arch-step new` scaffold, repair only that scaffold
   before continuing. Do not fill or repair Section 3-7 planning content as an
   ArcEpic shortcut. Seed setup from the approved Decomposition entry, the raw
   epic goal, prior sub-plan gates, and Epic Requirement Coverage. This is not a
   spawned planner and not a new script.
5. Treat the approved Decomposition as enough authority only when the sub-plan
   North Star is a direct, unambiguous expansion of approved epic scope. If two
   valid interpretations remain, stop and ask the user.
6. Invoke or continue the real `$arch-step auto-plan <DOC_PATH>` flow for the
   selected sub-plan. ArcEpic must not emulate `research`, either `deep-dive`
   pass, `phase-plan`, `consistency-pass`, or the receipt block itself.
7. After the bounded ArcStep continuation, inspect the gate with `status` or
   `ready`. Before marking the sub-plan `planned`, run
   `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`
   and require exit 0. If it fails, leave the sub-plan at `planning` and
   continue or report `$arch-step auto-plan <DOC_PATH>` with the gate's next
   required stage.
8. Only after the gate exits 0 may ArcEpic append the `planned` log entry and
   move to the next sub-plan. In native goal mode, continue sub-plan by sub-plan
   until all non-complete sub-plans are `planned` or a real blocker stops the
   run. Outside native goal mode, stop after one bounded transition and name the
   exact next command.

### Where judgment lives
- Expanding the approved Decomposition into a truthful sub-plan North Star and
  Epic Requirement Coverage without losing raw-goal scope.
- Deciding whether the approved Decomposition really resolves the sub-plan
  scope or whether the user must choose between two real interpretations.

### Where determinism lives
- DOC_PATH assignment.
- `arch_stage_gate.py ready` proof.
- Status update to `planned` after the readiness proof exits 0.
- Orchestration Log append.

### Failure modes
- Decomposition is not approved: stop and ask for approval first.
- Sub-plan scope is ambiguous: ask the smallest user question.
- Stage gate is not ready: keep or set Status `planning`, then continue or
  report `$arch-step auto-plan <DOC_PATH>` with the gate-reported next stage.
- A sub-plan has marker-looking planning blocks, copied Section 3-7 content, or
  a stored `planned` Status but `ready --doc <DOC_PATH>` fails: treat that state
  as not planned and reconcile before acting.
- A sub-plan doc has implementation already started before all sub-plans are
  planned: surface the mixed state; do not rewrite history.

## Mode: `auto-implement`

### Trigger
- Epic doc has `sub_plans_approved: true`.
- User explicitly asks for `arch-epic auto-implement`, asks to implement the
  planned epic end to end, or resumes an existing same-session auto-implement
  pass.

### Inputs
- Epic doc.
- Approved Decomposition.
- Every non-complete sub-plan DOC_PATH.
- Current worklogs and `arch-step` implementation audit blocks.

### Outputs
- One sub-plan advanced through the real `$arch-step auto-implement <DOC_PATH>`
  implement/prove/audit loop or the existing epic critic, with matching
  Orchestration Log entries.
- Sub-plan Status updated to `implementing` or `complete`.
- Epic `status: complete` only after every sub-plan is complete.

### Actions
1. If any non-complete sub-plan has Status other than `planned` or
   `implementing`, stop with:
   `Use $arch-epic auto-plan <EPIC_DOC_PATH>`.
2. Select the first sub-plan whose Status is `planned` or `implementing`.
3. Run `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`;
   if it fails, set or keep Status `planning` and route back to `auto-plan`.
4. If the sub-plan does not have an implementation audit COMPLETE block, invoke
   or continue `$arch-step auto-implement <DOC_PATH>` and set or keep Status
   `implementing`. One invocation is not completion. In native goal mode,
   continue the same ArcStep implement/prove/audit loop until
   `arch_skill:block:implementation_audit` says `Verdict (code): COMPLETE` or a
   true blocker stops progress. Outside native goal mode, stop after the
   bounded transition and name `$arch-step auto-implement <DOC_PATH>` as the
   next command when audit is still not clean.
5. If the `arch-step` implementation audit is COMPLETE, start a new clean epic
   critic. Prefer a native child; use `scripts/run_arch_epic.py critic-spawn`
   only when the external critic lane was deliberately selected.
6. If the critic passes, mark the sub-plan `complete` and continue to the next
   planned sub-plan in native goal mode. Outside native goal mode, stop after
   the bounded transition and name the exact next command.
7. If the critic returns `incomplete`, keep or set the sub-plan Status as
   `implementing`, append a compact mismatch log entry, and route back through
   `$arch-step auto-implement <DOC_PATH>` unless the audit or verdict evidence
   is unreadable or contradictory. Do not mark the sub-plan complete or advance.
8. If all sub-plans are `complete`, set epic `status: complete` and render the
   final summary.

### Where judgment lives
- Deciding whether a critic finding is ordinary in-scope unfinished work,
  material scope drift, or a state mismatch that needs user attention.
- Reconciling stored Status with sub-plan audit truth before acting.

### Where determinism lives
- Readiness gate command.
- `$arch-step auto-implement <DOC_PATH>` invocation.
- Epic critic dispatch and verdict parsing; the script owns external
  invocation only.
- Status and log updates.

### Failure modes
- Planning is incomplete: stop and route to `auto-plan`.
- `arch-step` audit is NOT COMPLETE: keep Status `implementing` and continue
  the same sub-plan through `$arch-step auto-implement <DOC_PATH>` instead of
  running the epic critic. In native goal mode this means keep going until audit
  is COMPLETE or truly blocked.
- Epic critic finds scope drift: halt for a scope-preserving user decision.
- Epic critic returns `incomplete`: keep Status `implementing` and route back
  through `$arch-step auto-implement <DOC_PATH>` unless evidence is unreadable
  or contradictory. Never advance to the next sub-plan.
- If an external Codex critic was selected and its model is missing, use
  `gpt-5.6-sol`. If another required external critic value is missing, ask the
  same consolidated policy question used by interactive mode. Do not ask for
  model values for an ordinary capable native critic.

## Mode: `auto-run`

### Trigger
- Epic doc has `sub_plans_approved: true`.
- User asks for role-based automatic execution, asks which agents/models to
  use, explicitly requests the external harness, or resumes an existing native
  role run or external `auto_execution` run.

### Inputs
- Epic doc.
- Approved Decomposition.
- Active-host child capabilities and any existing native child handles.
- For the external lane only: a user role table or existing `auto_execution`,
  plus automatic run-directory state.
- All sub-plan DOC_PATHs and worklogs as they exist on disk.

### Outputs
- One new clean planner/worker/critic action, one exact-role resume action, or
  one transport-appropriate monitor check while a child is active.
- For the external lane only: resolved `auto_execution` and a run directory
  under `.arch_skill/arch-epic/auto/<epic-slug>/run-<ts>/`.
- Compact Orchestration Log and Decision Log entries.

### Actions
1. Resolve each role under the shared orchestration policy. Prefer clean native
   children of the active host because the epic doc and sub-plan DOC_PATHs are
   durable inputs. Record transport, clean starting context, continuation,
   capabilities/worktree posture, topology, and return evidence in the
   smallest useful dispatch note.
2. For native roles, start planners/workers clean and preserve their exact
   handles; start every critic as another clean child. In Codex set
   `fork_turns: "none"`. In Claude use a clean named subagent, not a full
   conversation fork. Context remains separate from permissions and worktree.
3. If the external harness was deliberately selected, present and resolve the
   `epic_planner`, `implementation_worker`, and `critic` role table via
   `../../_shared/model_resolution.py`; default an omitted external Codex role
   model to `gpt-5.6-sol`, ask once for other missing values, then initialize
   the run directory with `scripts/run_arch_epic.py auto-init`.
4. Select the first sub-plan whose Status is not `complete`.
5. Drive that sub-plan depth-first:
   - planner uses the numbered per-epic sub-plan DOC_PATH from the
     Decomposition, creating or repairing that doc and Epic Requirement
     Coverage.
   - a new clean critic runs the North Star / coverage gate.
   - implementation worker executes the approved sub-plan and updates
     worklog evidence.
   - new clean critics run plan-readiness and completion/scope gates.
   - in-scope critic failures resume the exact planner or implementation
     worker with observation-only feedback through its original transport.
6. The parent owns sequencing and integration; role prompts prohibit nested
   fanout unless the parent assigned a bounded scope and budget. Role-based
   planning and implementation remain sequential across sub-plans.
7. Monitor native roles with host status/wait primitives. In the external lane,
   choose foreground or detached invocation deliberately; detached children
   write `events.jsonl`, `stderr.log`, and `stream.log`, and use the pinned
   long-run floors rather than short polling.
8. Mark the sub-plan complete only after the critic has no blocking
   findings. Then move to the next sub-plan.
9. If all sub-plans are complete, set epic `status: complete`, write the
   applicable report/receipts, and render the final summary.

### Where judgment lives
- The orchestrator decides which gate is next, whether a critic finding
  is in-scope repair versus material scope change, and when to halt for
  the user.
- The resumed planner or implementation worker owns repair reasoning.
  Critic output is evidence, not an instruction list.
- Worker and critic prompts teach the child roles why the approved epic
  goal, decomposition, and coverage map matter. Children are not treated
  as prompt runners.

### Where determinism lives
- Durable epic/sub-plan path and gate reads.
- Exact child/session handle capture and structured critic verdict parsing.
- In the external lane only: role-policy normalization/hashing, command
  rendering, run-directory layout, 180-second default wait cadence, streamed
  child artifacts, session-id capture, and `latest_worker_attempts` pointers.
- The script never chooses transport, role ownership, repair routing, or scope.

### Failure modes
- Missing/ambiguous external role policy: ask once before using that lane.
- Exact external model cannot resolve from shorthand: ask for the runnable ID.
- Native child still active: wait through the host surface. External child
  still active: use the pinned `poll_seconds` and stream recency.
- An external child has no final artifact but recent stream activity: keep
  waiting. Apply `quiet_floor_seconds`, `stuck_floor_seconds`, and
  `max_runtime_seconds` as attention signals, not silent kill switches.
- Child exits without inspectable return evidence: halt with the native handle
  or external run directory.
- Critic finds missing epic requirement coverage or unfinished in-scope
  implementation work: resume the exact planner or implementation worker that
  owns the failed gate until the retry budget is exhausted.
- Critic finds post-freeze expansion, unauthorized built scope, scope cycling,
  material product-intent change, or two valid scope paths: halt and ask the
  user; do not resume a worker with expansion as required work.
- Failing worker cannot be resumed: halt with its handle and available receipts,
  then ask whether to start a new clean replacement for that role.
- Repair budget exhausted: halt with the latest critic verdict and
  diagnostic record.

## Mode: `resume-scope-change`

### Trigger
- Epic doc has `status: halted` and the user has replied to a
  scope-change prompt naming their choice.

### Inputs
- Epic doc with a pending scope-change entry in the most recent
  Decision Log section (or the critic verdict that halted the
  run).
- The user's decision: approve expansion through `extend_current` or
  `new_sub_plan`, or keep frozen scope and require subtraction/redesign.

### Outputs
- Decomposition and sub-plan contract updated only when the user approved
  expansion; otherwise the frozen boundary remains unchanged.
- Epic doc `status: active`.
- Decision Log entry recording the resolution.

### Actions per user choice
- **extend_current**: Append the discovered items to the current
  sub-plan's Section 7 checklist and Exit Criteria in its arch-step
  DOC_PATH. Reset the sub-plan's Status in the epic doc to
  `implementing`. Next turn's `run` mode will invoke
  `$arch-step implement-loop` again. Record the human approval and new
  re-freeze boundary before implementation.
- **new_sub_plan**: Insert a new sub-plan entry in the epic's
  Decomposition. Its name is the "what" field from the discovered
  item or a user-supplied name. Its one-sentence description is
  user-confirmed. Its Status is `pending`. Its DOC_PATH is empty.
  Insert it after the current sub-plan. Current sub-plan Status
  becomes `complete` (its own scope is met; the discovered items
  are carried in the new sub-plan).
- **keep_scope**: Leave the decomposition and frozen contract unchanged.
  Reopen the current implementation for subtraction/redesign when unauthorized
  built scope exists; otherwise record the observation and continue only when
  all authorized work is complete.

Set `status: active`. Append Orchestration Log entry and Decision
Log entry. End turn. Next turn re-enters `run`.

### Where judgment lives
- Interpreting the user's reply when it doesn't map cleanly to
  one of the scope-preserving options ("fold items 1 and 3 into the current
  sub-plan but make item 2 its own thing"). The skill parses,
  announces its interpretation, applies.

### Where determinism lives
- Writing the new sub-plan entry.
- Editing the existing sub-plan's Scope and Simplicity Contract and Section 7
  only when the user chose and approved expansion.
- Log appends.

### Failure modes
- User's reply is ambiguous. Ask a targeted follow-up.
- User chooses `extend_current` but the item would violate the
  sub-plan's North Star (the item truly doesn't belong). Flag the
  mismatch, ask to reconfirm.
- User asks to remove approved scope or postpone it without a named owner and
  gate. Explain that arch-epic does not have a scope-reduction path; the
  scope-preserving choices are extend_current, new_sub_plan, named later
  ownership, or blocked.
- A critic calls new scope "required" but the user has not approved it: keep
  the epic halted and present the approval-or-subtraction choice.

## Mode: `summary`

### Trigger
- User asks a status question ("where are we on the epic?",
  "what's left?", "status"). OR
- The skill just flipped `status: complete` and is wrapping up.

### Inputs
- Epic doc.

### Outputs
- A compact status table printed to the user. No file changes.

### Actions
1. Render a table:
   ```
   | # | Sub-plan                   | Status                | Verdict |
   |---|----------------------------|-----------------------|---------|
   | 1 | Ship SSO in the auth ...   | complete              | pass    |
   | 2 | Build admin dashboard ...  | implementing          | —       |
   | 3 | Migrate admin users ...    | pending               | —       |
   ```
2. List the three most recent Orchestration Log entries.
3. If a sub-plan is active, name the exact next action the skill
   will take on the next invocation.
4. If `status: halted`, name the pending user decision.
5. End turn.

### Where judgment lives
- Deciding the "next action" phrasing in plain English.

### Where determinism lives
- Table rendering.
- Log reading.

### Failure modes
- Epic doc cannot be located. Ask the user to name the path.

## Invariants across all modes

- Never edit the target repo's code directly. Sub-plans do that
  via arch-step's implement-loop.
- Outside native goal-mode `auto-plan` and `auto-implement`, never run more
  than one state transition per turn. Each transition needs fresh doc truth
  before the next routing decision.
- Never silently advance past a gate (North Star approval, audit
  COMPLETE, critic pass). If a gate is unmet, surface it.
- Never overwrite past Orchestration Log or Decision Log entries.
  Append only.
- Never rewrite `raw_goal` or `raw_goal_sha256`. If the user wants
  to change the goal, start a new epic.
