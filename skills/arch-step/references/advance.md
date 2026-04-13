# `advance` Command Contract

## What this command does

- inspect one canonical full-arch artifact end to end
- emit the full ordered checklist with evidence notes
- choose exactly one next move
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
  - with `RUN=1`, execute exactly one chosen next command when that move still belongs to `arch-step`

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

- required stages are `[DONE]` only when the artifact is strong enough to proceed without guesswork or unresolved decisions
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
11. `consistency-pass` helper is present when needed
12. `review-gate` helper is present when needed
13. Implementation progress is grounded in code, `DOC_PATH`, and `WORKLOG_PATH`
14. Implementation audit is present and honest
15. Docs cleanup is either clearly next or already retired from the live surface

Helper commands stay explicit:

- if absent, they should usually remain `[OPTIONAL]`
- only elevate a helper to the next move when the artifact clearly needs that helper's unique hardening
- core commands should already be applying the same convergence, scope-triage, and preservation rules even when helpers are absent

## Evidence model

- use `status.md` for artifact grading and stage evidence rules
- turn those grades into checklist states:
  - `strong` or trustworthy `decent` -> `[DONE]`
  - `weak` or `missing` on required stages -> `[PENDING]`
  - `not needed` -> `[OPTIONAL]`
- for deep dive, call out whether pass 1 or pass 2 is done using `planning_passes`
- for implementation, require both doc truth and worklog truth before calling it `[DONE]`
- treat missing canonical-path analysis or missing preservation verification as real weakness, not optional polish
- treat unresolved plan-shaping decisions as `[PENDING]`, even when the surrounding section is otherwise strong

## Next-command selection rule

Choose exactly one next move using this precedence:

1. no plan doc yet -> `new`
2. existing doc is not canonical enough to trust -> `reformat`
3. North Star is still draft or too weak -> stop for confirmation or repair via `reformat`
4. after North Star confirmation, stop and wait for the user's explicit next command; do not auto-advance into `research` or any later stage
5. unresolved decision gap remains that repo truth cannot settle -> ask the user the exact blocker question
6. earliest required structure or owned block is missing -> run the command that repairs it
7. required structure exists but the next critical sections are still weak, including canonical-path analysis, preservation verification, or decision-completeness -> run the command that strengthens them
8. otherwise follow the core arc:
   - `research`
   - `deep-dive`
   - `external-research` when warranted
   - `deep-dive` again when external research materially changed the design
   - `phase-plan`
   - `consistency-pass` when the artifact clearly needs an end-to-end cold-read repair or the user explicitly wants it
   - `implement` by default
   - `implement-loop` when the user explicitly wants the bounded delivery loop to a clean audit
   - `audit-implementation`
7. if the code audit is clean and the feature still needs docs cleanup, hand off to `Use $arch-docs`
8. if all required stages are complete and the live feature residue is already retired, say there is no required next move

Default helper placement:

- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `consistency-pass`
- `review-gate`

These stay explicit unless the artifact clearly depends on one of them for correctness or execution safety.

## `RUN=1` execution rule

When `RUN=1` is present:

- print the checklist and chosen next move first
- then load the matching internal command reference from `references/`
- execute only that one command against the same artifact when the next move is still an `arch-step` command
- do not chain into a second command
- do not auto-run helper commands unless the chosen next command is itself that helper
- if the next move is a blocker question or North Star confirmation rather than a command, stop and ask instead of mutating further
- if the next move is `arch-docs`, print the handoff and stop; do not silently auto-switch skills from inside `advance`

## Output shape

- one-line North Star reminder
- one-line punchline naming the next move
- `DOC_PATH`
- the full checklist with evidence notes
- the exact next invocation
- if the next move is a blocker question, print that exact question instead of an invocation
- if `RUN=1` is absent, offer the next move without executing it
- if `RUN=1` is present, execute the chosen `arch-step` command and stop after that command finishes
