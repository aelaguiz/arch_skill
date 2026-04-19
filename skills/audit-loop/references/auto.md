# `auto` Mode

## Goal

Run repeated strong repo-audit passes until the exhaustive map is complete and a fresh review says no credible major unresolved risk remains, or the loop is genuinely blocked.

## What `auto` does

- verifies the active host runtime preflight
- creates or refreshes the host-aware `audit-loop` controller state
- runs one truthful `run` pass
- lets the installed Stop hook launch a fresh `review` pass
- continues only while the review verdict remains `CONTINUE`

The first turns may be mapping-only. That is correct behavior, not a failure to make progress.

User-facing invocation is just `audit-loop auto` in the active host runtime. If real hook support is absent or disabled, fail loud instead of pretending prompt-only repetition is the same feature.
Do not run the Stop hook yourself. After `auto` is armed, just end the turn and let the installed Stop hook run.

## Required runtime preflight

Before arming the controller, verify all of these:

- the active host runtime is Codex or Claude Code
- the installed suite controller runner exists at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`
- in Codex, `~/.codex/hooks.json` contains the arch_skill-managed `Stop` entry pointing at that runner; in Claude Code, `~/.claude/settings.json` contains the equivalent entry
- in Codex, `codex features list` shows `codex_hooks` enabled
- in Claude Code, hook-suppressed child runs via `claude -p --settings '{"disableAllHooks":true}'` work with the machine's normal Claude auth for fresh review passes

If any check fails, name the broken prerequisite and stop.
Do not preflight against a copied hook file under `~/.codex/hooks/`; that is not the install contract.

Dirty or untracked files are not part of this runtime preflight. A dirty worktree does not stop `auto` by itself; leave unrelated dirty or untracked files alone unless they directly conflict with the current audit story or make verification unsafe.

## State file contract

Create the host-aware state path before the first `run` pass:

- Codex: derive `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/audit-loop-state.<SESSION_ID>.json`
- Claude Code: prefer `.claude/arch_skill/audit-loop-state.<SESSION_ID>.json` when the session id is available before the first Stop-hook turn; otherwise create `.claude/arch_skill/audit-loop-state.json` only as a legacy single-slot fallback and let the first Stop-hook turn claim it into the session-scoped path

Minimal shape:

```json
{
  "version": 1,
  "command": "auto",
  "session_id": "<SESSION_ID>",
  "ledger_path": "_audit_ledger.md",
  "gitignore_created": false,
  "gitignore_entry_added": true
}
```

Lifecycle:

- create or refresh it after preflight and before the first `run`
- keep it armed while verdicts are `CONTINUE`
- the Stop hook deletes it before stopping on `BLOCKED`
- the Stop hook deletes it on `CLEAN` before removing the ledger and `.gitignore` entry

## Hard rules

- `auto` is one controller command, not a suggestion to keep winging it forever
- `auto` must not degrade into a tiny-safe-fix treadmill
- `auto` must not skip exhaustive mapping just to land a quick patch
- do not refuse to arm only because the repo has unrelated dirty or untracked files
- when the runtime supports delegation, use parallel read-only agents during mapping; otherwise complete the same exhaustive map sequentially
- the review pass must run in fresh context
- `review` stays docs-only
- do not continue after `BLOCKED`
- do not continue after `CLEAN`
- do not auto-commit findings

## Hook behavior

When the loop is armed, the installed suite Stop hook should:

1. no-op when no active audit-loop state matches the current session
2. launch the fresh review in the active host runtime:
   - Codex: `codex exec --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox` with `$audit-loop review`
   - Claude Code: `claude -p --settings '{"disableAllHooks":true}'` with explicit context and `/audit-loop review`
3. read the controller verdict from `_audit_ledger.md`
4. on `CONTINUE`, keep state armed and continue with the next `$audit-loop` pass, whether the next area is unfinished mapping work or a ranked risk front
5. on `BLOCKED`, clear state and stop honestly
6. on `CLEAN`, clear state, delete `_audit_ledger.md`, and remove the `.gitignore` entry
