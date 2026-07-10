# `full-auto` Mode Contract

`full-auto` is doctrine-only. It does not add a controller, state file, script,
runner, hook, or formal input schema. It is a re-entrant router over the existing
`auto-plan` and `implement-loop` commands.

## What this mode does

- drive one canonical mini/full-arch plan as far as it can honestly go
- preserve the normal North Star confirmation gate
- run automatic planning through `auto-plan`
- run automatic implementation through `implement-loop`
- stop loudly when the plan is not ready for the next command

## Required inventory before implementation

Before `full-auto` may invoke `implement-loop`, the artifact must satisfy the
same readiness bar that `implement-loop` depends on:

- frontmatter `status` is `active` or `complete`
- TL;DR and Section 0 are concrete, scoped, and free of unresolved decisions
- Section 0 has a confirmed Simplicity Contract naming the smallest sufficient fix, enough proof, and what not to build
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
- every Section 7 item directly serves the smallest sufficient fix or enough proof, and no planned machinery violates `Do not build`
- `status.md` / `section-quality.md` would grade the artifact, research, deep
  dive, and phase plan strong enough to proceed without guessing
Marker presence alone is not enough. `miniarch-step` has no `consistency-pass`
command, so `full-auto` must not pretend `phase-plan` completion alone proves
readiness. If a section is present but weak, route to the owning planning
command or ask the exact blocker question.

## Routing procedure

1. Resolve `DOC_PATH` using normal `miniarch-step` rules.
2. If no doc exists, run `new` and stop for North Star confirmation.
3. If the doc is not canonical enough to trust, run `reformat` and stop at the
   normal North Star gate.
4. If the North Star is still draft or weak, stop for confirmation or edits.
5. If planning is incomplete, invoke `auto-plan <DOC_PATH>` and continue in
   native goal mode, or stop after one bounded pass outside goal mode.
6. If planning is complete but the readiness inventory above is not satisfied,
   run the owning planning repair command when it is obvious; otherwise ask the
   exact blocker question.
7. If implementation audit already says `Verdict (code): COMPLETE`, hand off to
   `$arch-docs`.
8. Otherwise invoke `implement-loop <DOC_PATH>` and continue in native goal mode,
   or stop after one bounded pass outside goal mode.

## Hard rules

- Do not start `implement-loop` until `auto-plan` has completed and the readiness inventory passes.
- Do not add or invoke `consistency-pass`; that helper belongs to `arch-step`,
  not `miniarch-step`.
- Do not bypass unresolved user decisions, missing access, draft North Stars, or
  non-canonical docs.
- Do not treat a prompt-only same-turn chain as automation.
- Do not add a new full-auto script or hook entry to make this mode work.

## Console contract

- one-line North Star reminder
- one-line current state
- exact next command invoked or exact blocker question
- if code audit is clean, name `$arch-docs` as the next move
