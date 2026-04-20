# `implement-loop` Command Contract

## What this command does

- run the current implementation plan through one full ordered implementation frontier per loop cycle
- arm the repo-local loop state needed for fresh auditing
- arm loop state before implementation work starts so the live loop cannot be forgotten mid-run
- require each implementation pass to prove its claimed phase work before fresh auditing
- run a fresh `audit-implementation` pass when the active host runtime reaches a stop point and have it exhaustively validate the authoritative phase-exit contract
- repeat that full-frontier implement, prove, then audit cycle until the audit is clean or a real blocker stops progress
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

User-facing invocation is `implement-loop` or `auto-implement`. `auto-implement` is an exact alias of `implement-loop`; keep the internal runtime state and hook behavior under `implement-loop`. Do not run the Stop hook yourself. After the controller is armed, just end the turn and let the installed Stop hook run. If the installed runtime support for real automatic looping is absent or disabled, this command must fail loud instead of pretending prompt repetition is the same feature.

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
- the host-aware miniarch-step implement-loop controller state path:
  - Codex: `.codex/miniarch-step-implement-loop-state.<SESSION_ID>.json`
  - Claude Code: `.claude/arch_skill/miniarch-step-implement-loop-state.<SESSION_ID>.json`

Fresh `audit-implementation` child only:

- `arch_skill:block:implementation_audit`
- authoritative clean-or-not-clean audit outcome in `DOC_PATH`
- clean handoff text such as `Use $arch-docs`

## Required arm-time install

Arm-time ensure-install and dispatch-time loud verify are documented in `skills/_shared/controller-contract.md`. Before arming, run:

```bash
python3 ~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py \
  --ensure-installed --runtime <codex|claude>
```

Proceed only if it returns 0. The installer is idempotent and flock-guarded; it writes the canonical Stop entry (and the SessionStart entry on Claude) without races. If it fails loud, repair the named prerequisite and rerun — do not downgrade to prompt-only same-session looping.

## Active loop-state contract

Resolve the controller state path for the active host runtime before the first implementation pass:

- Codex: derive `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/miniarch-step-implement-loop-state.<SESSION_ID>.json`
- Claude Code: resolve the session id via `arch_controller_stop_hook.py --current-session`, then create `.claude/arch_skill/miniarch-step-implement-loop-state.<SESSION_ID>.json`. If the helper fails (SessionStart cache missing), abort with its message — do not write an unsuffixed file.

Minimal shape:

```json
{
  "version": 1,
  "command": "miniarch-step-implement-loop",
  "session_id": "<SESSION_ID>",
  "doc_path": "docs/<PLAN>.md"
}
```

Lifecycle:

- create or refresh it immediately after ensure-install succeeds and before any implementation work
- leave it armed while fresh auditing is active
- let fresh `audit-implementation` own the clean-versus-not-clean decision before clearing it
- the implementation side never deletes it
- only the fresh audit path clears it when the fresh audit finishes clean or when the audit path itself stops blocked

## Hard rules

- this command is a full-frontier controller over `implement` and `audit-implementation`; do not invent a second planning surface or second audit format
- `implement-loop` is one command; if the required runtime continuation support is absent or disabled, fail loud
- each cycle must run `implement` first and `audit-implementation` second against the same `DOC_PATH`
- `implement-loop` must not continue from a plan that is not decision-complete
- `implement-loop` runs against the same approved plan; the implementation side may not rewrite requirements, scope, acceptance criteria, or phase obligations while the loop is active
- before handing control back to fresh audit, the implementation pass must finish the current reachable ordered plan frontier or hit a real blocker, and the claimed phase work must have credible programmatic proof
- for modern Section 7 docs, fresh audit must validate both `Checklist (must all be done)` and `Exit criteria (all required)` before any phase can stay complete or the loop can finish clean
- in Codex, the fresh audit pass after an implementation stop point owns the continue-versus-stop decision
- inside `implement-loop`, only the fresh `audit-implementation` child may write or replace `arch_skill:block:implementation_audit`, conclude the controller is clean, write the `arch-docs` handoff, or delete the armed implement-loop state
- the implementation side must not act as the authoritative auditor just because it believes the code is complete
- if execution discovers that the approved plan itself needs requirement, scope, or acceptance-bar changes, stop honestly and repair the plan instead of continuing on a rewritten story
- when the fresh audit context launches, pass the explicit `DOC_PATH` and current repo working context; do not ask the fresh audit pass to rediscover the artifact from stale conversation state
- `audit-implementation` remains docs-only; never fix code while auditing
- if the fresh audit child reaches `Verdict (code): COMPLETE`, it clears loop state, stops, and hands off docs cleanup to `arch-docs`
- if the fresh audit child reaches `Verdict (code): NOT COMPLETE`, continue from the reopened phases and missing-code findings instead of hand-waving them away
- unproven fixes are unfinished implementation work, not something to punt to the auditor
- do not spin mechanically; if the latest fresh audit shows the missing-code picture did not materially change and there is no credible next move, let the fresh audit path stop and report the blocker
- no fallbacks or shims unless the plan explicitly approves them

## Loop procedure

1. Read `DOC_PATH` fully and run the same alignment checks required by `implement`.
2. Run arm-time ensure-install (`arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>`). It fails loud on drift; do not proceed unless it returns 0.
3. Build or refresh the compact implementation ledger from Section 7, Section 6, migration notes, and touched live docs/comments/instructions.
4. Resolve the active runtime controller state path, then create or refresh the armed miniarch-step implement-loop state for the current session and `DOC_PATH`.
5. Run one truthful implementation pass using the `implement` contract, starting from the earliest incomplete or reopened phase and continuing through the remaining approved phases in order until the current reachable frontier is done or genuinely blocked. Run the required credible proof along the way, but do not stop just because one local fix is green.
6. Sync `DOC_PATH` and `WORKLOG_PATH` to the resulting execution truth and proof signals, but do not replace `arch_skill:block:implementation_audit`, write clean-handoff language from the parent implementation pass, or rewrite requirements, scope, acceptance criteria, or phase obligations to fit partial code.
7. If the implementation pass stops before the run naturally stops, update the plan and worklog truthfully as awaiting fresh audit, leave the armed miniarch-step implement-loop state in place, and let fresh `audit-implementation` author the authoritative audit outcome.
8. Otherwise let the installed runtime try to stop. The Stop hook should:
   - no-op when no active loop state matches the current session
   - launch a fresh `audit-implementation` child pass when the loop is active
   - allow stop when the audit is clean
   - inject a continuation prompt when the audit finds missing code
9. On each hook-driven continuation, read the refreshed audit findings, resume from the earliest reopened or incomplete phase, continue linearly through the remaining approved phases, prove the claimed work as you go, update execution truth, and keep the loop armed while awaiting the next fresh audit.
10. If a fresh audit concludes that the next pass would be speculative, blocked, or materially unchanged from the last failed audit, let the fresh audit path clear the armed miniarch-step implement-loop state, stop, and report that state plainly.

## Fresh-audit requirement

For `implement-loop`, the authoritative audit must come from the fresh Stop-hook child run.
When the active runtime hook entry points at the installed runner, same-session audit is forbidden.
If the required fresh child cannot start, stop blocked instead of letting the parent implementation pass author the audit outcome.

Use host-native child execution:

- Codex: launch the fresh auditor with `codex exec --dangerously-bypass-approvals-and-sandbox`, not `--full-auto`, so repo verification runs against the real host context instead of the child sandbox. The miniarch fresh audit child is intentionally pinned to `--model gpt-5.4-mini` and `-c model_reasoning_effort="xhigh"` so the workflow still gets a high-effort independent audit.
- Claude Code: launch the fresh auditor with `claude -p --settings '{"disableAllHooks":true}'` plus explicit context so the audit runs without hook recursion while keeping normal host auth.

Fresh means the audit should not rely on remembered implementation intent from the parent run. It should rely on:

- `DOC_PATH`
- current repo state
- tests, logs, builds, and other evidence surfaces
- the `audit-implementation` contract

Clean means the fresh audit validated the authoritative checklist and the authoritative exit criteria for the reachable ordered frontier. Broad implementation confidence, local green checks, or parent-pass summaries are not enough.

## Console contract

- one-line North Star reminder
- one-line punchline that says either the loop finished clean or stopped blocked
- brief per-pass updates only when they add real information
- final next action, which is `Use $arch-docs` when the loop finished clean
