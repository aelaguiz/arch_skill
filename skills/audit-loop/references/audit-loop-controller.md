# audit-loop Controller

Core doctrine and lifecycle live in `skills/_shared/controller-contract.md`. This
file documents only the `audit-loop`-specific state schema and verdict source.

## Verdict source

`audit-loop auto` is an internal-verdict controller. The terminal verdict is
read from the `Controller verdict` block in `_audit_ledger.md` after each fresh
`review` pass.

- `CONTINUE` — the Stop hook keeps state armed and launches the next
  `$audit-loop` pass (mapping or fix).
- `CLEAN` — the Stop hook clears state, deletes `_audit_ledger.md`, and removes
  the `.gitignore` entry.
- `BLOCKED` — the Stop hook clears state and stops honestly.

The `review` pass itself runs in fresh context:

- Codex: `codex exec --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox`
  with `$audit-loop review`
- Claude Code: `claude -p --settings '{"disableAllHooks":true}'` with explicit
  context and `/audit-loop review`

## State file schema

Paths (session-scoped, per the shared contract):

- Codex: `.codex/audit-loop-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/audit-loop-state.<SESSION_ID>.json`

Minimal shape:

```json
{
  "version": 1,
  "command": "auto",
  "session_id": "<SESSION_ID>",
  "armed_at": 1760000000,
  "ledger_path": "_audit_ledger.md",
  "gitignore_created": false,
  "gitignore_entry_added": true
}
```

## Continuation rule

The loop continues only while the review verdict is `CONTINUE` because mapping
work or real unresolved risk remains. The first turns may be mapping-only —
that is correct behavior, not a failure to make progress.
