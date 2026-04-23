# Workflow contract: five modes the skill runs

The skill runs one mode per turn. The mode is chosen from the epic
doc's state, not from a user command. The user types whatever; the
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
2. Ask the user for `critic_runtime`, `critic_model`,
   `critic_effort` if any is missing from their invocation. One
   consolidated question per `model-and-effort.md`. Wait for
   answer before writing the doc.
3. Write the epic doc: frontmatter (with hashes), TL;DR in plain
   English, draft Decomposition per `decomposition-principles.md`
   (3–7 sub-plans typically, one sentence each, ordering by
   dependency then risk, gates as assertions not tasks).
4. Append one Orchestration Log entry: `Goal captured.
   Decomposition drafted (<N> sub-plans). Awaiting user approval.`
5. End turn. Surface the Decomposition and ask the user to approve
   or adjust.

### Where judgment lives
- Decomposition drafting. The skill reads the user's goal, its
  knowledge of the repos involved, and produces an ordered list.
  This is prose reasoning.
- Critic runtime/model/effort interpretation when the user gave
  partial answers.

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
- arch-step controller state files at both `.codex/` and
  `.claude/arch_skill/` paths.

### Outputs
- One arch-step command invoked, OR epic critic run, OR no action
  (hook is driving), with matching Orchestration Log entry.
- Updated sub-plan Status in the Decomposition.

### Actions
Run the routing logic in `arch-step-integration.md` against the
first sub-plan whose Status is not `complete`. Execute exactly one
transition per turn, then end the turn. Don't chain multiple
transitions in the same turn — the hook-backed controllers need a
full turn to arm and disarm cleanly.

### Where judgment lives
- Detecting state disagreements between stored Status and observed
  reality. When they differ, prose reasoning decides what the real
  state is.
- Deciding whether an epic critic verdict triggers halt (scope
  change) or auto-apply (all nice-to-have + defer-or-drop) per
  `scope-change-discipline.md`.

### Where determinism lives
- Reading state files.
- Invoking arch-step commands.
- Writing log entries.
- Running the critic subprocess via `scripts/run_arch_epic.py`.

### Failure modes
- auto-plan or implement-loop ended without expected completion
  markers. Surface to the user; do not silently re-arm.
- Audit block says NOT COMPLETE or has reopened phases. Halt with
  the arch-step audit's reported blockers; let the user decide.
- Critic verdict is `incomplete` (check 4 failed). Halt, surface
  the arch-step audit block contents.

## Mode: `resume-scope-change`

### Trigger
- Epic doc has `status: halted` and the user has replied to a
  scope-change prompt naming their choice.

### Inputs
- Epic doc with a pending scope-change entry in the most recent
  Decision Log section (or the critic verdict that halted the
  run).
- The user's decision: extend_current, new_sub_plan, defer, drop
  (or a custom mix when multiple discovered items exist).

### Outputs
- Decomposition updated per user's decision (new sub-plan inserted,
  existing sub-plan scope extended, or sub-plan marked complete
  with items parked/dropped).
- Epic doc `status: active`.
- Decision Log entry recording the resolution.

### Actions per user choice
- **extend_current**: Append the discovered items to the current
  sub-plan's Section 7 checklist and Exit Criteria in its arch-step
  DOC_PATH. Reset the sub-plan's Status in the epic doc to
  `implementing`. Next turn's `run` mode will invoke
  `$arch-step implement-loop` again.
- **new_sub_plan**: Insert a new sub-plan entry in the epic's
  Decomposition. Its name is the "what" field from the discovered
  item or a user-supplied name. Its one-sentence description is
  user-confirmed. Its Status is `pending`. Its DOC_PATH is empty.
  Insert it after the current sub-plan. Current sub-plan Status
  becomes `complete` (its own scope is met; the discovered items
  are carried in the new sub-plan).
- **defer**: Add the items to the epic-level Decision Log with
  `parked: true`. Current sub-plan Status becomes `complete`.
- **drop**: Add the items to the epic-level Decision Log with
  `dropped: true` and the rationale. Current sub-plan Status
  becomes `complete`.

Set `status: active`. Append Orchestration Log entry and Decision
Log entry. End turn. Next turn re-enters `run`.

### Where judgment lives
- Interpreting the user's reply when it doesn't map cleanly to
  one of the four options ("fold items 1 and 3 into the current
  sub-plan but make item 2 its own thing"). The skill parses,
  announces its interpretation, applies.

### Where determinism lives
- Writing the new sub-plan entry.
- Editing the existing sub-plan's arch-step Section 7 (when
  user chose extend_current).
- Log appends.

### Failure modes
- User's reply is ambiguous. Ask a targeted follow-up.
- User chooses `extend_current` but the item would violate the
  sub-plan's North Star (the item truly doesn't belong). Flag the
  mismatch, ask to reconfirm.

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
- Never run more than one state transition per turn. The
  hook-backed controllers need the full turn.
- Never silently advance past a gate (North Star approval, audit
  COMPLETE, critic pass). If a gate is unmet, surface it.
- Never overwrite past Orchestration Log or Decision Log entries.
  Append only.
- Never rewrite `raw_goal` or `raw_goal_sha256`. If the user wants
  to change the goal, start a new epic.
