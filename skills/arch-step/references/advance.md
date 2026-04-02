# `advance` Command Contract

## What this command does

- inspect one canonical full-arch artifact end to end
- emit the full ordered checklist with evidence notes
- choose exactly one next `arch-step` command
- optionally execute only that one next step when `RUN=1`

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md`
- `status.md`

## Inputs and mode

- resolve `DOC_PATH` using the normal `arch-step` defaults
- optional `RUN=1`:
  - default behavior is recommend only
  - with `RUN=1`, execute exactly one chosen next command and stop

## What `advance` inspects first

Inspect the same artifact surfaces as `status`:

- required frontmatter
- `# TL;DR`
- `planning_passes`
- `# 0) Holistic North Star`
- exact canonical top-level sections `# 1)` through `# 10)`
- required command-owned blocks
- `WORKLOG_PATH` and `implementation_audit` when implementation has started

## Checklist statuses

Use exactly:

- `[DONE]`
- `[PENDING]`
- `[OPTIONAL]`
- `[UNKNOWN]`

Rules:

- required stages are `[DONE]` only when the artifact is strong enough to proceed without guesswork
- weak or missing required stages are `[PENDING]`
- helper commands and non-warranted external research are `[OPTIONAL]`
- use `[UNKNOWN]` only when the artifact genuinely does not let you determine the answer
- every line must include a short evidence note

## Ordered checklist

Emit every line in this order:

1. Plan artifact exists and is canonical enough to trust
2. North Star is confirmed and strong enough to plan against
3. Research grounding is present and credible
4. Deep dive pass 1 is complete enough to trust current architecture, target architecture, and call-site audit
5. External research is present when warranted
6. Deep dive pass 2 is complete when external research materially changed the design
7. The authoritative phase plan is present and execution-grade
8. `plan-enhance` helper is present when needed
9. `fold-in` helper is present when needed
10. `overbuild-protector` helper is present when needed
11. `review-gate` helper is present when needed
12. Implementation progress is grounded in code, `DOC_PATH`, and `WORKLOG_PATH`
13. Implementation audit is present and honest

Helper commands stay explicit:

- if absent, they should usually remain `[OPTIONAL]`
- only elevate a helper to the next move when the artifact clearly needs that helper's unique hardening

## Evidence model

- use `status.md` for artifact grading and stage evidence rules
- turn those grades into checklist states:
  - `strong` or trustworthy `decent` -> `[DONE]`
  - `weak` or `missing` on required stages -> `[PENDING]`
  - `not needed` -> `[OPTIONAL]`
- for deep dive, call out whether pass 1 or pass 2 is done using `planning_passes`
- for implementation, require both doc truth and worklog truth before calling it `[DONE]`

## Next-command selection rule

Choose exactly one next command using this precedence:

1. no plan doc yet -> `new`
2. existing doc is not canonical enough to trust -> `reformat`
3. North Star is still draft or too weak -> stop for confirmation or repair via `reformat`
4. earliest required structure or owned block is missing -> run the command that repairs it
5. required structure exists but the next critical sections are still weak -> run the command that strengthens them
6. otherwise follow the core arc:
   - `research`
   - `deep-dive`
   - `external-research` when warranted
   - `deep-dive` again when external research materially changed the design
   - `phase-plan`
   - `implement`
   - `audit-implementation`
7. if all required stages are complete, say there is no required next `arch-step` move

Default helper placement:

- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `review-gate`

These stay explicit unless the artifact clearly depends on one of them for correctness or execution safety.

## `RUN=1` execution rule

When `RUN=1` is present:

- print the checklist and chosen next command first
- then load the matching internal command reference from `references/`
- execute only that one command against the same artifact
- do not chain into a second command
- do not auto-run helper commands unless the chosen next command is itself that helper
- if the next move is North Star confirmation rather than a command, stop and ask for confirmation instead of mutating further

## Output shape

- one-line North Star reminder
- one-line punchline naming the next command
- `DOC_PATH`
- the full checklist with evidence notes
- the exact next `arch-step` invocation
- if `RUN=1` is absent, offer the next move without executing it
- if `RUN=1` is present, execute the chosen command and stop after that command finishes
