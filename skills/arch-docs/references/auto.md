# `auto` Mode

`auto` is the real Codex controller for repeated docs-audit passes. It is not prompt-only chaining.

## Goal

Repeat grounded default passes with Stop-hook continuation and a fresh external evaluation until the resolved docs surface is healthy or honestly blocked.

## Required runtime preflight

Before arming the controller, verify all of these:

- Codex is the active host runtime
- installed Stop-hook support exists in `~/.codex/hooks.json`
- the installed suite controller runner exists under `~/.agents/skills/arch-step/scripts/`
- `codex features list` shows `codex_hooks` enabled
- current code truth is stable enough to ground docs
- if active arch context exists, the implementation audit is clean enough to trust that context as a narrowing input

If any preflight fails, name the broken prerequisite and stop instead of pretending `auto` is still real.

## State contract

Resolve `SESSION_ID` from `CODEX_THREAD_ID`, then create or refresh `.codex/arch-docs-auto-state.<SESSION_ID>.json` before the first pass.

Minimum shape:

```json
{
  "version": 1,
  "command": "arch-docs-auto",
  "session_id": "<SESSION_ID>",
  "scope_kind": "repo",
  "scope_summary": "repo docs surface",
  "context_sources": [],
  "pass_index": 0,
  "stop_condition": "no meaningful stale, duplicate, misleading, obviously dated, missing, or still-confusing docs remain in the resolved cleanup scope and every grounded topic has one canonical evergreen home",
  "ledger_path": ".doc-audit-ledger.md"
}
```

Recommended extra fields:

- `context_paths`
- `candidate_topics`
- `completed_topics`
- `blocked_topics`
- `current_risk`
- `notes`

If `scope_kind` is `explicit-context` or `arch-context`, include non-empty `context_paths` for the narrowed scope.

## Loop rules

- Run one truthful default `arch-docs` docs-health pass.
- Apply the same pre-delete backup-commit rule inside each pass before any bounded delete batch.
- Keep `.doc-audit-ledger.md` current while cleanup is still active.
- Let Codex stop naturally.
- Expect the installed Stop hook to launch a fresh external evaluator.
- Continue only when another grounded pass is still credible for the resolved docs-health intent.
- In repo scope, the next pass may widen across the repo docs surface when real grounded cleanup or missing evergreen truth still remains.
- In narrowed scopes, widen only enough to cover overlapping docs for the same topics.
- Use `git log` when a doc's lasting value depends on whether it was a one-off tied to some earlier point in time.
- Do not degrade into a remover-only loop. Update stale surviving docs, clarify confusing docs, and create or expand canonical evergreen docs when the repo clearly needs them.
- Stop blocked when the evaluator says the next pass would be speculative, taxonomy-imposing, disconnected from a narrowed scope, or materially unchanged.
- Stop clean only when the evaluator says the current stop condition is satisfied.

## Hard rules

- Do not downgrade to prompt-only looping.
- Keep the resolved scope explicit.
- In repo mode, keep each pass focused on a meaningful grounded cleanup slice, not the smallest possible topic cluster.
- Do not let `auto` drift into speculative, taxonomy-first, or aesthetic-only docs refactoring.
- Do not use age cutoffs or simplistic stale-doc heuristics. Use history as evidence and decide whether the doc still serves a lasting reader need.
- The temporary ledger should survive only while cleanup is active. It must be deleted before the overall docs cleanup is declared complete.
