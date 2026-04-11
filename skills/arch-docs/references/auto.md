# `auto` Mode

`auto` is the real Codex controller for repeated docs-audit passes. It is not prompt-only chaining.

## Goal

Repeat bounded default passes with Stop-hook continuation and a fresh external evaluation until the resolved docs cleanup is clean or honestly blocked.

## Required runtime preflight

Before arming the controller, verify all of these:

- Codex is the active host runtime
- installed Stop-hook support exists in `~/.codex/hooks.json`
- the installed suite controller runner exists under `~/.agents/skills/arch-step/scripts/`
- `codex features list` shows `codex_hooks` enabled
- current code truth is stable enough to ground docs
- if active arch context exists, the implementation audit is clean enough to trust that context as a narrowing input

If any preflight fails, stop immediately with the exact remediation instead of pretending `auto` is still real.

## State contract

Create or refresh `.codex/arch-docs-auto-state.json` before the first pass.

Minimum shape:

```json
{
  "version": 1,
  "command": "arch-docs-auto",
  "scope_kind": "repo",
  "scope_summary": "repo docs surface",
  "context_sources": [],
  "pass_index": 0,
  "stop_condition": "no high-confidence stale or duplicate topic cluster remains and every cleaned topic has one canonical evergreen home",
  "ledger_path": ".doc-audit-ledger.md"
}
```

Recommended extra fields:

- `session_id`
- `context_paths`
- `candidate_topics`
- `completed_topics`
- `blocked_topics`
- `current_risk`
- `notes`

If `scope_kind` is `explicit-context` or `arch-context`, include non-empty `context_paths` for the narrowed scope.

## Loop rules

- Run one truthful default `arch-docs` cleanup pass.
- Apply the same pre-delete backup-commit rule inside each pass before any bounded delete batch.
- Keep `.doc-audit-ledger.md` current while cleanup is still active.
- Let Codex stop naturally.
- Expect the installed Stop hook to launch a fresh external evaluator.
- Continue only when another bounded pass is still credible inside the same resolved scope.
- Stop blocked when the evaluator says the next pass would be speculative, scope-widening, taxonomy-imposing, or materially unchanged.
- Stop clean only when the evaluator says the current stop condition is satisfied.

## Hard rules

- Do not downgrade to prompt-only looping.
- Keep the resolved scope explicit.
- In repo mode, keep each pass bounded to the highest-confidence remaining topic cluster or explicit stop condition.
- Do not let `auto` silently turn into an unbounded docs refactor.
- The temporary ledger should survive only while cleanup is active. It must be deleted before the overall docs cleanup is declared complete.
