# `full-auto` Mode Contract

`full-auto` is a re-entrant router over the existing `auto-plan` and
`implement-loop` commands. It does not add a controller, state file, runner,
hook, or formal input schema. It uses the same stage-gate helper as `auto-plan`
to prove that planning stages actually ran before implementation starts.

## What this mode does

- drive one canonical full-arch plan as far as it can honestly go
- preserve the normal North Star confirmation gate
- run automatic planning through `auto-plan`
- run automatic implementation through `implement-loop`
- stop loudly when the plan is not ready for the next command

## Required inventory before implementation

Before `full-auto` may invoke `implement-loop`, the artifact must satisfy the
same readiness bar that `implement-loop` depends on:

- frontmatter `status` is `active` or `complete`
- TL;DR and Section 0 are concrete, scoped, and free of unresolved decisions
- Section 0 contains a complete Scope and Simplicity Contract with human
  authorization anchors, an initial minimal convergence closure or `none`, and
  a freeze boundary; target architecture, Section 7, and proof do not exceed it
- `arch_skill:block:research_grounding` is present and Section 3.3 has no
  unresolved blocker questions
- current architecture, target architecture, and call-site audit blocks are
  present and strong enough to identify the canonical owner path
- adjacent-surface, compatibility-posture, fallback, migration, delete, and
  live-doc/comment/instruction decisions are settled or explicitly out of scope
- `arch_skill:block:phase_plan` is present
- every modern phase has `Checklist (must all be done)` and
  `Exit criteria (all required)`
- required proof signals are named in Section 7 or Section 8
- `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`
  exits 0
- `arch_skill:block:consistency_pass` says `Decision-complete: yes`,
  `Unresolved decisions: none`, and `Decision: proceed to implement? yes`
Marker presence alone is not enough. If a section is present but weak, route to
the owning planning command or ask the exact blocker question.

## Routing procedure

1. Resolve `DOC_PATH` using normal `arch-step` rules.
2. If no doc exists, run `new` and stop for North Star confirmation.
3. If the doc is not canonical enough to trust, run `reformat` and stop at the
   normal North Star gate.
4. If the North Star is still draft or weak, stop for confirmation or edits.
5. If planning is incomplete, invoke `auto-plan <DOC_PATH>` and continue in
   native goal mode, or stop after one bounded pass outside goal mode.
6. If `arch_stage_gate.py ready --doc <DOC_PATH>` fails, follow the stage it
   names instead of implementing from marker-only text.
7. If planning is complete but the readiness inventory above is not satisfied,
   run the owning planning repair command when it is obvious; otherwise ask the
   exact blocker question.
8. If implementation audit already says `Verdict (code): COMPLETE`, hand off to
   `$arch-docs`.
9. Otherwise invoke `implement-loop <DOC_PATH>` and continue in native goal mode,
   or stop after one bounded pass outside goal mode.

## Hard rules

- Do not start `implement-loop` until `auto-plan` has completed and the readiness inventory passes.
- Do not start `implement-loop` until the stage gate prints `READY next=implement-loop`.
- Do not skip `consistency-pass` for `arch-step` full-auto.
- Do not bypass unresolved user decisions, missing access, draft North Stars, or
  non-canonical docs.
- Do not treat a prompt-only same-turn chain as automation.
- Do not add a full-auto runner, controller, hook entry, or second state surface.

## Console contract

- one-line North Star reminder
- one-line current state
- exact next command invoked or exact blocker question
- if code audit is clean, name `$arch-docs` as the next move
