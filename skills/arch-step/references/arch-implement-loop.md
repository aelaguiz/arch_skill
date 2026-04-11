# `implement-loop` Command Contract

## What this command does

- run the current implementation plan through one bounded delivery loop
- arm the repo-local loop state needed for fresh auditing
- require each implementation pass to prove its claimed fixes before fresh auditing
- run a fresh `audit-implementation` pass when Codex reaches a stop point
- repeat that implement, prove, then audit cycle until the audit is clean or a real blocker stops progress
- keep the code, `DOC_PATH`, and `WORKLOG_PATH` aligned after each implementation pass, then let the fresh audit child author the authoritative audit block

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

User-facing invocation is `implement-loop` or `auto-implement`. `auto-implement` is an exact alias of `implement-loop`; keep the internal runtime state and hook behavior under `implement-loop`. If the installed runtime support for real automatic looping is absent or disabled, this command must fail loud instead of pretending prompt repetition is the same feature.

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Sections 0, 5, 6, 7, 8, `WORKLOG_PATH`, and `implementation_audit`
- `arch-implement.md`
- `arch-audit-implementation.md`

## Inputs and `DOC_PATH` resolution

- treat the user ask as steering, constraints, and any relevant delivery preferences
- if the ask includes a `docs/<...>.md` path, use it
- otherwise resolve `DOC_PATH` from the conversation and repo context
- if the doc path is truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates

## Writes

Parent implementation pass:

- product code
- `WORKLOG_PATH`
- phase status and Decision Log in `DOC_PATH`
- `.codex/implement-loop-state.<SESSION_ID>.json`

Fresh `audit-implementation` child only:

- `arch_skill:block:implementation_audit`
- authoritative clean-or-not-clean audit outcome in `DOC_PATH`
- clean handoff text such as `Use $arch-docs`

## Required runtime preflight

Before arming the loop, verify all of these:

- Codex runtime is the active host
- the installed Codex runtime support for this repo's `implement-loop` surface is present
- the installed `arch-step` runner exists under `~/.agents/skills/arch-step/`
- `codex features list` shows `codex_hooks` enabled

If any check fails, name the broken prerequisite and stop.

Do not downgrade to prompt-only same-session looping.

## Active loop-state contract

Resolve `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/implement-loop-state.<SESSION_ID>.json` before the first implementation pass.

Minimal shape:

```json
{
  "version": 1,
  "command": "implement-loop",
  "session_id": "<SESSION_ID>",
  "doc_path": "docs/<PLAN>.md"
}
```

Lifecycle:

- create or refresh it after preflight and before the implementation pass
- leave it armed while fresh auditing is active
- let fresh `audit-implementation` own the clean-versus-not-clean decision before clearing it
- the implementation side never deletes it
- only the fresh audit path clears it when the fresh audit finishes clean or when the audit path itself stops blocked

## Hard rules

- this command is a bounded controller over `implement` and `audit-implementation`; do not invent a second planning surface or second audit format
- `implement-loop` is one command; if the required runtime continuation support is absent or disabled, fail loud
- each cycle must run `implement` first and `audit-implementation` second against the same `DOC_PATH`
- before handing control back to fresh audit, the implementation pass must run the smallest credible programmatic proof for each claimed fix
- in Codex, the fresh audit pass after an implementation stop point owns the continue-versus-stop decision
- inside `implement-loop`, only the fresh `audit-implementation` child may write or replace `arch_skill:block:implementation_audit`, conclude the controller is clean, write the `Use $arch-docs` handoff, or delete `.codex/implement-loop-state.<SESSION_ID>.json`
- the implementation side must not act as the authoritative auditor just because it believes the code is complete
- when the fresh audit context launches, pass the explicit `DOC_PATH` and current repo working context; do not ask the fresh audit pass to rediscover the artifact from stale conversation state
- `audit-implementation` remains docs-only; never fix code while auditing
- if the fresh audit child reaches `Verdict (code): COMPLETE`, it clears loop state, stops, and hands off docs cleanup to `arch-docs`
- if the fresh audit child reaches `Verdict (code): NOT COMPLETE`, continue from the reopened phases and missing-code findings instead of hand-waving them away
- unproven fixes are unfinished implementation work, not something to punt to the auditor
- do not spin mechanically; if the latest fresh audit shows the missing-code picture did not materially change and there is no credible next move, let the fresh audit path stop and report the blocker
- no fallbacks or shims unless the plan explicitly approves them

## Loop procedure

1. Read `DOC_PATH` fully and run the same alignment checks required by `implement`.
2. Run the runtime preflight. If the installed hook path or `codex_hooks` is unavailable, fail loud.
3. Build or refresh the compact implementation ledger from Section 7, Section 6, migration notes, and touched live docs/comments/instructions.
4. Resolve `SESSION_ID` from `CODEX_THREAD_ID`, then create or refresh `.codex/implement-loop-state.<SESSION_ID>.json` for the current Codex session and `DOC_PATH`.
5. Run one truthful implementation pass using the `implement` contract, including the smallest credible programmatic proof for each claimed fix.
6. Sync `DOC_PATH` and `WORKLOG_PATH` to the resulting code reality and proof signals, but do not replace `arch_skill:block:implementation_audit` or write clean-handoff language from the parent implementation pass.
7. If the implementation pass stops before the run naturally stops, update the plan and worklog truthfully as awaiting fresh audit, leave `.codex/implement-loop-state.<SESSION_ID>.json` armed, and let fresh `audit-implementation` author the authoritative audit outcome.
8. Otherwise let Codex try to stop. The installed runtime should:
   - no-op when no active loop state matches the current session
   - launch a fresh `audit-implementation` child pass when the loop is active
   - allow stop when the audit is clean
   - inject a continuation prompt when the audit finds missing code
9. On each hook-driven continuation, read the refreshed audit findings, implement the missing code work, prove the claimed fixes, update execution truth, and keep the loop armed while awaiting the next fresh audit.
10. If a fresh audit concludes that the next pass would be speculative, blocked, or materially unchanged from the last failed audit, let the fresh audit path clear `.codex/implement-loop-state.<SESSION_ID>.json`, stop, and report that state plainly.

## Fresh-audit requirement

For Codex `implement-loop`, the authoritative audit must come from the fresh Stop-hook child run.
When `codex_hooks` is enabled and the installed hook path is present, same-session audit is forbidden.
If the required fresh child cannot start, stop blocked instead of letting the parent implementation pass author the audit outcome.

For the Codex Stop-hook child subprocess, launch the fresh auditor with
`codex exec --dangerously-bypass-approvals-and-sandbox`, not `--full-auto`, so
repo verification runs against the real host context instead of the child
sandbox.

Fresh means the audit should not rely on remembered implementation intent from the parent run. It should rely on:

- `DOC_PATH`
- current repo state
- tests, logs, builds, and other evidence surfaces
- the `audit-implementation` contract

## Console contract

- one-line North Star reminder
- one-line punchline that says either the loop finished clean or stopped blocked
- brief per-pass updates only when they add real information
- final next action, which is `Use $arch-docs` when the loop finished clean
