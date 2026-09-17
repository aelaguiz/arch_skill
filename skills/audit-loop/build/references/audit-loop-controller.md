# Audit Loop Controller

Audit-loop-specific state schema and verdict source. Core doctrine and lifecycle live in references/controller-lifecycle.md. This document documents only the audit-loop-specific additions.

## Verdict source

`audit-loop auto` is an internal-verdict controller. The terminal verdict is read from the `Controller verdict` block in `_audit_ledger.md` after each fresh `review` pass.

- `CONTINUE` — the Stop hook keeps state armed and launches the next `$audit-loop` pass (mapping or fix).
- `CLEAN` — the Stop hook clears state, deletes `_audit_ledger.md`, and removes the `.gitignore` entry.
- `BLOCKED` — the Stop hook clears state and stops honestly.

The `review` pass itself runs in fresh context:

- Codex: `codex exec --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox` with `$audit-loop review`
- Claude Code: `claude -p --settings '{"disableAllHooks":true}'` with explicit context and `/audit-loop review`

## State file schema

Paths (session-scoped, per the shared contract):

- Codex: `.codex/audit-loop-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/audit-loop-state.<SESSION_ID>.json`

Minimal shape:

### Audit-loop state fields

_definitions_

- **Version** — Integer schema version. Currently `1`.
- **Command** — The controller command string: `auto`.
- **Session ID** — The session id the state was armed under.
- **Armed At** — Epoch seconds when the state was written.
- **Ledger Path** — Path to the audit ledger file, typically `_audit_ledger.md`.
- **Gitignore Created** — Boolean: whether the skill created the root `.gitignore` file itself (as opposed to merely adding an entry to an existing one).
- **Gitignore Entry Added** — Boolean: whether the `_audit_ledger.md` entry was added to the root `.gitignore`.

## Continuation rule

The loop continues only while the review verdict is `CONTINUE` because mapping work or real unresolved risk remains. The first turns may be mapping-only — that is correct behavior, not a failure to make progress.
