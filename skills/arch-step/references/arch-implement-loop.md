# `implement-loop` Command Contract

## What this command does

- run the current implementation plan through one bounded delivery loop
- arm the repo-local loop state needed for fresh auditing
- run a fresh `audit-implementation` pass when Codex reaches a stop point
- repeat that implement then audit cycle until the audit is clean or a real blocker stops progress
- keep the code, `DOC_PATH`, `WORKLOG_PATH`, and authoritative audit block aligned after each pass

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

User-facing invocation is just `implement-loop`. If the installed runtime support for real automatic looping is absent or disabled, this command must fail loud instead of pretending prompt repetition is the same feature.

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

- product code
- `WORKLOG_PATH`
- phase status and Decision Log in `DOC_PATH`
- `arch_skill:block:implementation_audit`
- `.codex/implement-loop-state.json`

## Required runtime preflight

Before arming the loop, verify all of these:

- Codex runtime is the active host
- the installed Codex runtime support for this repo's `implement-loop` surface is present
- the installed `arch-step` runner exists under `~/.agents/skills/arch-step/`
- `codex features list` shows `codex_hooks` enabled

If any check fails, stop immediately and print the exact remediation:

- `make install`
- `codex features enable codex_hooks`

Do not downgrade to prompt-only same-session looping.

## Active loop-state contract

Create `.codex/implement-loop-state.json` before the first implementation pass.

Minimal shape:

```json
{
  "version": 1,
  "command": "implement-loop",
  "doc_path": "docs/<PLAN>.md"
}
```

Lifecycle:

- create or refresh it after preflight and before the implementation pass
- let the first fresh-audit pass claim the current `session_id` into the state file
- leave it armed while fresh auditing is active
- delete it when the audit finishes clean
- delete it before stopping on a real blocker so the loop does not re-enter falsely

## Hard rules

- this command is a bounded controller over `implement` and `audit-implementation`; do not invent a second planning surface or second audit format
- `implement-loop` is one command; if the required runtime continuation support is absent or disabled, fail loud
- each cycle must run `implement` first and `audit-implementation` second against the same `DOC_PATH`
- in Codex, the fresh audit pass after an implementation stop point owns the continue-versus-stop decision
- when the fresh audit context launches, pass the explicit `DOC_PATH` and current repo working context; do not ask the fresh audit pass to rediscover the artifact from stale conversation state
- `audit-implementation` remains docs-only; never fix code while auditing
- if the audit verdict is `COMPLETE`, clear loop state and stop
- when the audit verdict is `COMPLETE`, hand off docs cleanup to `arch-docs` and let it use the current artifact as context instead of inventing another hidden `arch-step` phase
- if the audit verdict is `NOT COMPLETE`, continue from the reopened phases and missing-code findings instead of hand-waving them away
- do not spin mechanically; if the latest implement pass did not materially change the missing-code picture and there is no credible next move, clear loop state, stop, and report the blocker
- no fallbacks or shims unless the plan explicitly approves them

## Loop procedure

1. Read `DOC_PATH` fully and run the same alignment checks required by `implement`.
2. Run the runtime preflight. If the installed hook path or `codex_hooks` is unavailable, fail loud.
3. Build or refresh the compact implementation ledger from Section 7, Section 6, migration notes, and touched live docs/comments/instructions.
4. Create or refresh `.codex/implement-loop-state.json` for the current Codex session and `DOC_PATH`.
5. Run one truthful implementation pass using the `implement` contract.
6. Sync `DOC_PATH` and `WORKLOG_PATH` to the resulting code reality.
7. If a real blocker stops progress before the run naturally stops, delete `.codex/implement-loop-state.json`, update the plan and worklog truthfully, and stop.
8. Otherwise let Codex try to stop. The installed runtime should:
   - no-op when no active loop state matches the current session
   - launch a fresh `audit-implementation` child pass when the loop is active
   - allow stop when the audit is clean
   - inject a continuation prompt when the audit finds missing code
9. On each hook-driven continuation, read the refreshed audit findings, implement the missing code work, and keep the loop armed.
10. If the next pass would be speculative, blocked, or materially unchanged from the last failed audit, delete `.codex/implement-loop-state.json`, stop, and report that state plainly.

## Fresh-audit preference

When the fresh audit launches, use this preference ladder:

1. fresh same-runtime child session or subprocess with isolated context
2. fresh isolated subagent or new thread when that is the cleanest available boundary
3. same-session audit only when no real isolation surface exists

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
