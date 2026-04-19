# `auto` Mode

`auto` is the real controller for repeated docs-audit passes in Codex and Claude Code. It is not prompt-only chaining.
Do not run the Stop hook yourself. After `auto` is armed, just end the turn and let the installed Stop hook run.

## Goal

Repeat grounded default passes with Stop-hook continuation and a fresh external evaluation until stale point-in-time docs are retired, durable truth lives in real evergreen homes, and the resolved docs surface is honestly clean or blocked.

## Required runtime preflight

Before arming the controller, verify all of these:

- the active host runtime is Codex or Claude Code
- installed Stop-hook support exists for the active runtime: `~/.codex/hooks.json` in Codex or `~/.claude/settings.json` in Claude Code
- the installed suite controller runner exists under `~/.agents/skills/arch-step/scripts/`
- in Codex, `codex features list` shows `codex_hooks` enabled
- in Claude Code, hook-suppressed child runs via `claude -p --settings '{"disableAllHooks":true}'` work with the machine's normal Claude auth for the fresh evaluator
- current code truth is stable enough to ground docs
- if active arch context exists, the implementation audit is clean enough to trust that context as a narrowing input

If any preflight fails, name the broken prerequisite and stop instead of pretending `auto` is still real.

## State contract

Create or refresh the host-aware state path before the first pass:

- Codex: derive `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/arch-docs-auto-state.<SESSION_ID>.json`
- Claude Code: prefer `.claude/arch_skill/arch-docs-auto-state.<SESSION_ID>.json` when the session id is available before the first Stop-hook turn; otherwise create `.claude/arch_skill/arch-docs-auto-state.json` and let the first Stop-hook turn claim session ownership

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
  "stop_condition": "no meaningful stale, duplicate, misleading, obviously dated, missing, or still-confusing docs remain in the resolved cleanup scope, no unjustified point-in-time docs older than 30 days still survive, every grounded topic has one canonical evergreen home, and any required public-repo baseline docs exist as standalone canonical homes",
  "ledger_path": ".doc-audit-ledger.md"
}
```

Recommended extra fields:

- `context_paths`
- `repo_posture`
- `repo_posture_evidence`
- `candidate_topics`
- `completed_topics`
- `blocked_topics`
- `missing_canonical_docs`
- `current_risk`
- `notes`

If `scope_kind` is `explicit-context` or `arch-context`, include non-empty `context_paths` for the narrowed scope.

## Loop rules

- Run one truthful default `arch-docs` docs-health pass.
- Apply the same pre-delete backup-commit rule inside each pass before any bounded delete batch.
- Keep `.doc-audit-ledger.md` current while cleanup is still active.
- Let the installed runtime stop naturally.
- Expect the installed Stop hook to launch a fresh external evaluator.
- Continue only when another grounded pass is still credible for the resolved docs-health intent.
- In repo scope, the next pass may widen across the repo docs surface when real grounded cleanup or missing evergreen truth still remains.
- In narrowed scopes, widen only enough to cover overlapping docs for the same topics.
- In this repo family, treat point-in-time docs older than 30 days as presumptively stale until the pass records explicit code-grounded current-reader value for each survivor.
- Use `git log` when a doc's lasting value depends on whether it was a one-off tied to some earlier point in time.
- Do not degrade into a remover-only loop. Update stale surviving docs, clarify confusing docs, and create or expand canonical evergreen docs only when the repo clearly needs them and the split-versus-expand judgment says they deserve to stand alone.
- Do not count metadata-only freshness edits as progress.
- When the repo is `public OSS`, keep going while required standard community-doc homes are still missing.
- Stop blocked when the evaluator says the next pass would be speculative, taxonomy-imposing, disconnected from a narrowed scope, or materially unchanged.
- Stop clean only when the evaluator says the current stop condition is satisfied.

## Hard rules

- Do not downgrade to prompt-only looping.
- Keep the resolved scope explicit.
- In repo mode, keep each pass focused on a meaningful grounded cleanup slice, not the smallest possible topic cluster.
- Do not let `auto` drift into speculative, taxonomy-first, or aesthetic-only docs refactoring.
- Do not use age alone as the full verdict. Use history and current code as evidence, but keep the 30-day presumption strong and require old point-in-time docs to earn survival.
- Do not trust doc self-labels such as `docs/living`, `Status: LIVING`, or `Last verified` without code-grounded confirmation.
- Do not re-guess repo posture every pass when the earlier evidence is still valid. Persist it in controller state.
- The temporary ledger should survive only while cleanup is active. It must be deleted before the overall docs cleanup is declared complete.
