# `implement-loop` Command Contract

## What this command does

- runs the current implementation plan through the approved ordered implementation frontier
- requires each implementation pass to prove its claimed phase work before audit
- runs `audit-implementation` against current repo state
- repeats implement, prove, then audit until the audit is clean or a real blocker stops progress
- keeps the code, `DOC_PATH`, and `WORKLOG_PATH` aligned after each implementation pass

Native goal mode supplies the repeated turns. This skill does not install or
arm automation hooks. Outside goal mode, run one bounded implementation/audit
pass and end with the exact next command.

## Delivery North Star

Running `implement-loop` should end in one of two honest states:

- `clean`:
  - code is shipped
  - `DOC_PATH` is truthful
  - `WORKLOG_PATH` is truthful
  - `audit-implementation` says `Verdict (code): COMPLETE`
  - the next required move is `Use $arch-docs`
- `blocked`:
  - remaining missing work or blocker is explicit
  - the latest audit and phase status show that truth plainly
  - the loop stops instead of pretending one more pass will magically fix it

User-facing invocation is `implement-loop` or `auto-implement`.
`auto-implement` is an exact alias of `implement-loop`; do not create a second
mode or control surface.

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `skills/_shared/scope-and-convergence.md`
- `skills/_shared/depth-first-planning.md`
- `section-quality.md` for Sections 0, 5, 6, 7, 8, `WORKLOG_PATH`, and `implementation_audit`
- `arch-implement.md`
- `arch-audit-implementation.md`

## Inputs and `DOC_PATH` resolution

- treat the user ask as steering, constraints, and any relevant delivery preferences
- if the ask includes a `docs/<...>.md` path, use it
- otherwise resolve `DOC_PATH` from the conversation and repo context
- if the doc path is truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates

## Writes

Implementation pass:

- product code
- `WORKLOG_PATH`
- phase status and Decision Log in `DOC_PATH`

Audit pass:

- `arch_skill:block:implementation_audit`
- authoritative clean-or-not-clean audit outcome in `DOC_PATH`
- clean handoff text such as `Use $arch-docs`

## Hard Rules

- this command is an implementation-frontier implement/audit loop; do not invent a second planning surface or second audit format
- the current approved ordered implementation frontier is the earliest incomplete or reopened phase plus later phases whose prerequisites and proof gates are reachable in this loop cycle
- each cycle must run implementation first and `audit-implementation` second against the same `DOC_PATH`
- `implement-loop` must not continue from a plan that is not decision-complete
- `implement-loop` must not continue when the Scope and Simplicity Contract is
  missing, vague, unfrozen, contradicted by Section 7, or exceeded by the current
  implementation
- repeated review findings retain their original scope disposition. A newly
  discovered adjacent path stops for human approval; unauthorized built scope
  is subtracted before the loop advances
- `implement-loop` runs against the same approved plan; the implementation side may not rewrite requirements, scope, acceptance criteria, or phase obligations while the loop is active
- before auditing, the implementation pass must finish the current approved ordered implementation frontier or hit a real blocker, and the claimed phase work must have credible programmatic proof
- for modern Section 7 docs, fresh audit must validate both `Checklist (must all be done)` and `Exit criteria (all required)` before any phase can stay complete or the loop can finish clean
- `audit-implementation` owns the authoritative clean-versus-not-clean decision
- if execution discovers that the approved plan itself needs requirement, scope, or acceptance-bar changes, stop honestly and repair the plan instead of continuing on a rewritten story
- if execution proposes unapproved machinery or another test category beyond `Enough proof`, stop before building it and obtain explicit user approval rather than letting another loop cycle normalize the expansion
- when audit runs, pass the explicit `DOC_PATH` and current repo working context; do not ask the audit pass to rediscover the artifact from stale conversation state
- `audit-implementation` remains docs-only; never fix code while auditing
- if audit reaches `Verdict (code): COMPLETE`, stop clean and hand off docs cleanup to `arch-docs`
- if audit reaches `Verdict (code): NOT COMPLETE`, continue from the reopened phases and missing-code findings instead of hand-waving them away
- unproven fixes are unfinished implementation work, not something to punt to the auditor
- do not spin mechanically; if the latest audit shows the missing-code picture did not materially change and there is no credible next move, stop and report the blocker
- no fallbacks or shims unless the plan explicitly approves them

## Loop Procedure

1. Read `DOC_PATH` fully and run the same alignment checks required by `implement`.
2. Build or refresh the compact implementation ledger from Section 7, Section 6, migration notes, and touched live docs/comments/instructions.
3. Run one truthful implementation pass using the `implement` contract, starting from the earliest incomplete or reopened phase and continuing through later phases whose prerequisites and proof gates are reachable in this cycle. Run the required credible proof along the way, but do not stop just because one local fix is green.
4. Sync `DOC_PATH` and `WORKLOG_PATH` to the resulting execution truth and proof signals, but do not replace `arch_skill:block:implementation_audit`, write clean-handoff language from the implementation pass, or rewrite requirements, scope, acceptance criteria, or phase obligations to fit partial code.
5. Run `audit-implementation` against the same `DOC_PATH` and current repo state.
6. If audit is clean, report the clean handoff to `$arch-docs`.
7. If audit is not clean and a credible next move exists, continue from the earliest reopened or incomplete phase.
8. In native goal mode, keep repeating this loop until the Delivery North Star is met or a true blocker stops the run.
9. Outside native goal mode, stop after one bounded implement/audit cycle and print the next exact command.

## Fresh-Audit Requirement

Clean means `audit-implementation` validated the authoritative checklist and
the authoritative exit criteria for the current approved ordered implementation
frontier against current repo state. Broad implementation confidence, local
green checks, or implementation summaries are not enough.

When Codex launches a fresh auditor from miniarch workflow doctrine, use
`gpt-5.4-mini` at `xhigh` effort.

## Console Contract

- one-line North Star reminder
- one-line punchline that says either the loop finished clean or stopped blocked
- brief per-pass updates only when they add real information
- final next action, which is `Use $arch-docs` when the loop finished clean
