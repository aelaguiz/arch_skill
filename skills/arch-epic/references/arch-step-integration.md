# arch-step integration

The skill invokes `$arch-step` commands as slash commands in the
orchestrator's own session. It does NOT shell out to `claude -p` or
`codex exec` for arch-step work — that would spawn parallel
controllers and collide with the session-scoped state arch-step
relies on. arch-step runs in the same session as `arch-epic`.

This reference maps sub-plan Status to the exact arch-step command
the skill issues next. It is the operational cheat sheet the
orchestrator prose leans on.

## Mapping

### Status `pending`

Meaning: this sub-plan has a name and a one-sentence description in
the Decomposition, but no arch-step doc yet.

Next action:
1. If the sub-plan's DOC_PATH is empty in the Decomposition, propose
   a path using the arch-step convention:
   `docs/<SLUG_SCREAMING_SNAKE>_<YYYY-MM-DD>.md` where `<SLUG>` is
   derived from the sub-plan's name. Ask the user to accept or
   override. Silence means proceed with the proposed path.
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

### Status transition: `pending` → `north-star-approved`

Detected by reading the sub-plan's arch-step DOC_PATH frontmatter:
`status: active` means the user confirmed the North Star. Update
the epic doc's sub-plan Status to `north-star-approved` and append
to log: `Sub-plan N North Star approved by user.`

### Status `north-star-approved`

Next action:
1. Invoke `$arch-step auto-plan <DOC_PATH>`.
2. Update Status to `planning`.
3. Append to log: `Sub-plan N auto-plan armed.`
4. End the turn. arch-step's `auto-plan` is hook-backed; the Stop
   hook will drive research → deep-dive → phase-plan →
   consistency-pass across subsequent turns.

### Status `planning`

Check the auto-plan controller state file at:
- Codex: `.codex/auto-plan-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/auto-plan-state.<SESSION_ID>.json`

If the state file exists: do nothing. The hook is running. End the
turn.

If the state file is absent: auto-plan completed. Read the
sub-plan's DOC_PATH and look for `arch_skill:block:consistency_pass`
with `Decision-complete: yes`. If present, the planning is done.
Update Status to `implementing` and invoke `$arch-step implement-loop <DOC_PATH>`.
Append to log: `Sub-plan N auto-plan completed. Sub-plan N implement-loop armed.`
End the turn.

If the state file is absent but there is no consistency-pass block
or `Decision-complete: no`: something is off. Do NOT silently
advance. Surface to the user: auto-plan ended without reaching
completion. Ask whether to re-run `$arch-step auto-plan`, intervene
manually, or halt.

### Status `implementing`

Check the implement-loop controller state file at:
- Codex: `.codex/implement-loop-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/implement-loop-state.<SESSION_ID>.json`

If the state file exists: do nothing. The hook is running. End the
turn.

If the state file is absent: implement-loop completed. Read the
sub-plan's DOC_PATH and look for
`arch_skill:block:implementation_audit` with `Verdict (code): COMPLETE`.

If COMPLETE: run the epic critic (see `critic-contract.md` and
`critic-prompt.md`). The critic spawns as a subprocess via
`scripts/run_arch_epic.py critic-spawn`. Wait for the verdict.
Apply per the `Critic verdict` rules below.

If the audit block is present but says something other than COMPLETE
(NOT COMPLETE, reopened phases): do NOT run the epic critic. This is
an arch-step-level completion issue. Surface to the user with the
audit's reported blockers. The user decides whether to re-arm
implement-loop or intervene.

If the audit block is absent entirely: implement-loop ended without
writing the audit. Same as the planning edge case — surface, do not
silently advance.

### Critic verdict: `pass`

- Update sub-plan Status to `complete`.
- Write the verdict path into the Epic-critic verdict field for
  that sub-plan.
- Append to log: `Epic critic run on sub-plan N: verdict=pass.`
- Append to log: `Sub-plan N marked complete.`
- Loop back through the mapping from step 1 (first sub-plan with
  Status `pending`). If all sub-plans are `complete`, flip
  `status: complete` on the epic doc and write the final summary.

### Critic verdict: `scope_change_detected`

- Apply the auto-act rule from `scope-change-discipline.md`: if and
  only if all discovered items are nice-to-have and recommendation
  is defer-or-drop, auto-apply and continue. Otherwise halt.
- Halt branch: set epic `status: halted`, update sub-plan Status to
  `scope-changed`, write the verdict path, append a Decision Log
  entry that names the discovered items and the options, end the
  turn with the user question.

### Critic verdict: `incomplete`

Rare — arch-step's audit normally catches incomplete work before
the critic runs. When it happens: halt. Set `status: halted`,
update sub-plan Status back to `implementing`, append log, ask the
user whether to re-arm implement-loop or investigate manually.

## What arch-epic does NOT invoke

- `$arch-step reformat` — the skill always uses `new` for fresh
  sub-plans. If the user wants to reformat an existing non-canonical
  doc as a sub-plan, they call reformat themselves outside
  arch-epic, then point the sub-plan's DOC_PATH at the reformatted
  doc and set Status to `pending` manually.
- `$arch-step research`, `deep-dive`, `external-research`,
  `phase-plan`, `consistency-pass`, `review-gate` as individual
  commands — those are handled by `auto-plan`'s hook. The skill
  does not sequence them manually.
- Helper commands: `plan-enhance`, `fold-in`, `overbuild-protector`.
  Users invoke those ad hoc per sub-plan if they want the extra
  passes. The skill does not run them.
- `$arch-step advance` — the skill routes from Status, not from
  arch-step's advance router. Two routers would disagree and the
  user would not know which won.
- `$arch-step status` as part of the loop — only if the user
  explicitly asks "what does arch-step think of sub-plan N?", in
  which case the skill relays the answer without acting on it.

## Cross-runtime parity

Everything above works identically on Claude Code and Codex because
`$arch-step`'s `auto-plan` and `implement-loop` controllers ship
for both runtimes with their Stop hooks. The state file paths
differ (`.codex/` vs `.claude/arch_skill/`); the skill checks both
paths when looking for a live controller.

## When in doubt, surface

The decision tree above covers the common paths. Anything unusual
(state file present but doc contents contradict, missing audit
block, multiple controllers armed on the same session, etc.)
surfaces to the user. The skill does not hide exceptions. If you
find yourself tempted to paper over a weird state with an assumption,
don't — print what you see, name your best hypothesis, and ask.
