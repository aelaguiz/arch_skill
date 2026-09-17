# Arch Docs Auto Controller

Arch-docs-auto-specific state schema and verdict source. Core doctrine and lifecycle live in references/controller-lifecycle.md. This document documents only the arch-docs-auto-specific additions.

## Verdict source

`arch-docs auto` uses a fresh external evaluator launched by the Stop hook (see `references/internal-evaluator.md` for the evaluator contract). The evaluator reads `.doc-audit-ledger.md` and current code, then emits:

- `CONTINUE` — another grounded pass is credible for the resolved docs-health intent. The Stop hook keeps state armed and launches the next `$arch-docs` pass.
- `CLEAN` — the evaluator says the resolved stop condition is satisfied. The Stop hook clears state; the default pass deletes `.doc-audit-ledger.md` before the run ends.
- `BLOCKED` — the evaluator says the next pass would be speculative, taxonomy-imposing, disconnected from a narrowed scope, or materially unchanged. The Stop hook clears state.

## State file schema

Paths (session-scoped, per the shared contract):

- Codex: `.codex/arch-docs-auto-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/arch-docs-auto-state.<SESSION_ID>.json`

Minimum shape:

### Arch-docs auto state fields

_definitions_

- **Version** — Integer schema version. Currently `1`.
- **Command** — The controller command string: `arch-docs-auto`.
- **Session ID** — The session id the state was armed under.
- **Armed At** — Epoch seconds when the state was written.
- **Scope Kind** — The scope resolution result: `repo`, `explicit-context`, or `arch-context`.
- **Scope Summary** — Human-readable summary of the resolved scope.
- **Context Sources** — List of context sources used to resolve scope (paths, artifact references).
- **Pass Index** — Zero-based pass counter.
- **Stop Condition** — The resolved stop condition for the auto loop.
- **Ledger Path** — Path to the doc audit ledger, typically `.doc-audit-ledger.md`.

Recommended extra fields (persisted between passes so repo posture and topic progress do not have to be rediscovered every pass):

- `context_paths` — required when `scope_kind` is `explicit-context` or `arch-context`
- `repo_posture` and `repo_posture_evidence`
- `candidate_topics`
- `completed_topics`
- `blocked_topics`
- `missing_canonical_docs`
- `current_risk`
- `notes`

## Continuation rule

The loop continues only while the evaluator returns `CONTINUE`. In this repo family, the evaluator should keep treating point-in-time docs older than 30 days as presumptively stale until the pass records explicit code-grounded current-reader value for each survivor. A pass that mainly refreshed metadata labels is not progress.
