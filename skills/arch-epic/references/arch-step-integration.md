# arch-step integration

Interactive mode and the explicit same-session `arch-epic auto-plan` /
`arch-epic auto-implement` drivers invoke `$arch-step` commands in the
orchestrator's visible session. They do not shell out to `claude -p` or
`codex exec` merely to emulate the same-session lane.

Role-based automatic execution is a separate transport-neutral lane. Planner
and implementation roles apply arch-step doctrine directly against the durable
sub-plan DOC_PATH; they do not invoke `$arch-step auto-plan`, `implement-loop`,
or another nested continuation command. Prefer clean native same-host children.
The explicit external harness uses the same role contract when its provider,
exact model, lifecycle, isolation, automation, or receipt benefit is deliberate.
This avoids nested continuation while preserving arch-step's artifact, receipt,
and quality gates.

This reference maps sub-plan Status to the exact arch-step command
the skill issues next. It is the operational cheat sheet the
orchestrator prose leans on.

Same-session `arch-epic auto-plan` and `arch-epic auto-implement` share the
same status vocabulary but use a different stopping point: `auto-plan` stops at
Status `planned` for every sub-plan, and `auto-implement` is the only
same-session command that moves planned sub-plans into implementation.

## Mapping

### Status `pending`

Meaning: this sub-plan has a name and a one-sentence description in
the Decomposition, but no arch-step doc yet.

Next action:
1. If the sub-plan's DOC_PATH is empty in the Decomposition, propose
   an arch-epic grouped path:
   `docs/epic/<EPIC_SLUG_WITH_DATE>/PHASE_<NN>_<SUBPLAN_SLUG>_<YYYY-MM-DD>.md`.
   Derive `<EPIC_SLUG_WITH_DATE>` from the epic doc stem without the
   leading `EPIC_`; derive `<NN>` from the Decomposition order at the
   moment the DOC_PATH is assigned; derive `<SUBPLAN_SLUG>` from the
   sub-plan's name. Ask the user to accept or override. Silence means
   proceed with the proposed path. Preserve any already-created
   DOC_PATHs; if a later scope-change decision inserts a new sub-plan
   between existing numbered docs, use a sortable fractional slot such
   as `PHASE_01_5_<SUBPLAN_SLUG>_<YYYY-MM-DD>.md` instead of renaming
   existing docs or worklogs.
2. Fill the DOC_PATH field in the Decomposition entry.
3. Invoke `$arch-step new <DOC_PATH>` with the sub-plan's
   one-sentence description as the North Star seed (pass it through
   as the initial intent prose to arch-step).
4. Append to Orchestration Log: `Sub-plan N invoked: $arch-step new <DOC_PATH>`.
5. End the turn. arch-step's `new` command pauses for the user to
   confirm the North Star inside Section 0 of the new doc.

Do not update the sub-plan Status yet. The user's next turn will
either confirm the North Star (arch-step flow) or ask for
adjustments. On the turn after that, the skill reads the arch-step
doc's frontmatter.

Same-session `auto-plan` exception: when the user explicitly asked for
`arch-epic auto-plan`, do not invoke `$arch-step new` and stop for a separate
North Star approval turn. Instead, assign the grouped DOC_PATH and apply the
`arch-step new` artifact contract directly from the approved Decomposition,
raw epic goal, prior gates, and Epic Requirement Coverage. This setup is
scaffold-only: it does not write `arch-step` planning-stage receipts, and it
does not make Section 3-7 planning blocks ready by ArcEpic shortcut. This is
allowed only when the resulting sub-plan North Star is a direct, unambiguous
expansion of approved epic scope; otherwise stop and ask. After setup, route
immediately to the `north-star-approved` mapping in the same `auto-plan` pass so
the real `$arch-step auto-plan <DOC_PATH>` flow owns the planning work.

### Status transition: `pending` → `north-star-approved`

Detected by reading the sub-plan's arch-step DOC_PATH frontmatter:
`status: active` means the user confirmed the North Star. Update
the epic doc's sub-plan Status to `north-star-approved` and append
to log: `Sub-plan N North Star approved by user.`

### Status `north-star-approved`

Next action:
1. Invoke `$arch-step auto-plan <DOC_PATH>`.
2. Update Status to `planning`.
3. Append to log: `Sub-plan N auto-plan started.`
4. In native goal mode, let `$arch-step auto-plan` continue through
   research, two deep-dive passes, phase-plan, and consistency-pass.
   Outside goal mode, stop after the bounded pass and resume this mapping
   on the next user turn.

### Status `planning`

Run:

```text
python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>
```

This readiness command is the deciding proof. A consistency-pass marker,
plausible Section 3-7 text, copied planning content, or a prior stored epic
Status is not enough. If the command fails, keep or set the sub-plan Status to
`planning`, append a compact reconciliation log entry when stored status was
misleading, and invoke `$arch-step auto-plan <DOC_PATH>` again in goal mode or
report that exact command plus the gate-reported next stage outside goal mode.
Do not silently advance.

If the readiness command exits 0:

- In interactive `run` mode, update Status to `implementing`, invoke
  `$arch-step implement-loop <DOC_PATH>`, and append to log:
  `Sub-plan N auto-plan readiness gate passed. Sub-plan N implement-loop started.`
- In same-session `arch-epic auto-plan`, update Status to `planned`, append to
  log: `Sub-plan N auto-plan readiness gate passed. Status set to planned.`,
  then move to the next sub-plan in native goal mode or stop with the next exact
  command outside goal mode.

### Status `planned`

Meaning: this exact sub-plan DOC_PATH passed
`python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`
after real generated ArcStep auto-plan receipts, and implementation has not
started.

Next action:
1. For ordinary interactive `run`, do not skip into implementation unless the
   user asked to run or continue implementation. Surface that the next exact
   command is `$arch-epic auto-implement <EPIC_DOC_PATH>` or
   `$arch-step implement-loop <DOC_PATH>` for this sub-plan.
2. For same-session `arch-epic auto-implement`, run
   `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`.
   If it exits 0, invoke `$arch-step auto-implement <DOC_PATH>`, update or keep
   Status as `implementing`, and append to log:
   `Sub-plan N auto-implement started.`
3. If the gate is not ready, the stored `planned` status is stale. Reset or keep
   the Status as `planning`, append a reconciliation log entry, and route back
   to `$arch-epic auto-plan <EPIC_DOC_PATH>`.

### Status `implementing`

Read the sub-plan's DOC_PATH and look for
`arch_skill:block:implementation_audit` with `Verdict (code): COMPLETE`.

If COMPLETE: start a new clean epic critic (see `critic-contract.md` and
`critic-prompt.md`). Prefer a native child; use
`scripts/run_arch_epic.py critic-spawn` only for a deliberately selected
external critic. Wait for the verdict.
Apply per the `Critic verdict` rules below.

If the audit block is present but says something other than COMPLETE
(NOT COMPLETE, reopened phases): do NOT run the epic critic. This is
an arch-step-level completion issue. In same-session `arch-epic auto-implement`,
keep or set Status `implementing` and continue `$arch-step auto-implement
<DOC_PATH>` in native goal mode, or report that exact command plus the audit
blockers outside goal mode. In ordinary interactive `run`, surface the blockers
and the next exact command so the user can decide whether to continue.

If the audit block is absent entirely: implement-loop ended without
writing the audit. Run or request `$arch-step implement-loop <DOC_PATH>` or
`$arch-step auto-implement <DOC_PATH>` depending on the current command; do not
silently advance.

### Critic verdict: `pass`

- Update sub-plan Status to `complete`.
- Write the verdict path into the Epic-critic verdict field for
  that sub-plan.
- Append to log: `Epic critic run on sub-plan N: verdict=pass.`
- Append to log: `Sub-plan N marked complete.`
- Loop back through the mapping from step 1 (first sub-plan with
  Status not `complete`). If all sub-plans are `complete`, flip
  `status: complete` on the epic doc and write the final summary.

### Critic verdict: `scope_change_detected`

- Halt. The critic has no authority to expand or reduce scope.
- Set epic `status: halted`, update sub-plan Status to
  `scope-changed`, write the verdict path, append a Decision Log entry
  that names the discovered items and their provenance dispositions, then ask
  the human whether to approve and re-freeze an `extend_current` or
  `new_sub_plan` expansion, or keep scope and require subtraction/redesign.

### Critic verdict: `incomplete`

Rare — arch-step's audit normally catches incomplete work before
the critic runs. When it happens, do not mark the sub-plan complete and do not
advance. In same-session `arch-epic auto-implement`, keep or set sub-plan Status
`implementing`, append a compact mismatch log entry, and route back through
`$arch-step auto-implement <DOC_PATH>` unless the audit or verdict evidence is
unreadable or contradictory. In ordinary interactive mode, halt and ask whether
to rerun implement-loop or investigate manually.

## What arch-epic does NOT invoke

- `$arch-step reformat` — the skill always uses `new` for fresh
  sub-plans. If the user wants to reformat an existing non-canonical
  doc as a sub-plan, they call reformat themselves outside
  arch-epic, then point the sub-plan's DOC_PATH at the reformatted
  doc and set Status to `pending` manually.
- `$arch-step research`, `deep-dive`, `external-research`,
  `phase-plan`, `consistency-pass`, `review-gate` as individual
  commands — those are handled by `auto-plan`. The skill
  does not sequence them manually.
- Helper commands: `plan-enhance`, `fold-in`, `overbuild-protector`.
  Users invoke those ad hoc per sub-plan if they want the extra
  passes. The skill does not run them.
- `$arch-step advance` — the skill routes from Status, not from
  arch-step's advance router. Two routers would disagree and the
  user would not know which won.
- `$arch-step full-auto` — single-plan full-auto belongs to `arch-step`
  itself. `arch-epic` already owns the multi-plan routing layer, so it
  invokes or observes the underlying `new`, `auto-plan`, and
  `implement-loop` / `auto-implement` transitions directly in interactive or
  same-session auto modes.
- `$arch-step status` as part of the loop — only if the user
  explicitly asks "what does arch-step think of sub-plan N?", in
  which case the skill relays the answer without acting on it.

## Role-based automatic integration

Role-based automatic mode uses the same sub-plan Status vocabulary, but the
transition owner changes. Transport does not change these gates:

- `pending`: planner harness creates or repairs the numbered per-epic
  DOC_PATH and Epic Requirement Coverage, then a critic checks the
  North Star gate.
- `north-star-approved`: planner/implementation harness performs the
  planning stages from arch-step doctrine directly. It does not arm
  `auto-plan`.
- `planning`: critic checks plan readiness and decision completeness.
- `planned`: normally produced by same-session `auto-plan`; role-based
  mode may skip it because that lane checks planning gates with critics before
  implementation.
- `implementing`: implementation worker executes Section 7, updates the
  worklog, and leaves verification evidence. It does not arm
  `implement-loop`.
- completion: critic checks implementation audit, scope drift, and epic
  requirement coverage.

Role-based automatic mode still treats the sub-plan DOC_PATH and worklog as the
truth. Child returns are evidence, not a second plan. The top-level
orchestrator records only compact handle and artifact pointers in the epic doc.

If a critic finds in-scope unfinished work, the transition owner does not
change to a separate repair worker. The orchestrator resumes the exact planner
child for planning-gate failures or the exact implementation worker child for
implementation/completion failures, passing the critic verdict as
observation-only evidence through the original transport. Every independent
critic starts clean and does not prescribe repair steps.

## Cross-runtime parity

Everything above works identically on Claude Code and Codex because
`$arch-step`'s `auto-plan`, `implement-loop`, and `auto-implement` commands are native
goal-mode friendly in both runtimes. The epic skill checks sub-plan doc
truth rather than external automation state.

## When in doubt, surface

The decision tree above covers the common paths. Anything unusual
(doc contents contradict, missing audit block, status says planning while
the plan is already ready, etc.)
surfaces to the user. The skill does not hide exceptions. If you
find yourself tempted to paper over a weird state with an assumption,
don't — print what you see, name your best hypothesis, and ask.
