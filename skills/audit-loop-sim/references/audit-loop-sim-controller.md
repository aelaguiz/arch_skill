# audit-loop-sim Controller

Core doctrine and lifecycle live in `skills/_shared/controller-contract.md`.
This file documents only the `audit-loop-sim`-specific state schema and verdict
source.

## Verdict source

`audit-loop-sim auto` is an internal-verdict controller. The terminal verdict is
read from the `Controller verdict` block in `_audit_sim_ledger.md` after each
fresh `review` pass.

- `CONTINUE` — the Stop hook keeps state armed and launches the next
  `$audit-loop-sim` pass.
- `CLEAN` — the Stop hook clears state, deletes `_audit_sim_ledger.md`, and
  removes the `.gitignore` entry.
- `BLOCKED` — the Stop hook clears state and stops honestly.

The `review` pass itself runs in fresh context:

- Codex: `codex exec --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox`
  with `$audit-loop-sim review`
- Claude Code: `claude -p --settings '{"disableAllHooks":true}'` with explicit
  context and `/audit-loop-sim review`

## State file schema

Paths (session-scoped, per the shared contract):

- Codex: `.codex/audit-loop-sim-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/audit-loop-sim-state.<SESSION_ID>.json`

Minimal shape:

```json
{
  "version": 1,
  "command": "auto",
  "session_id": "<SESSION_ID>",
  "armed_at": 1760000000,
  "ledger_path": "_audit_sim_ledger.md",
  "gitignore_created": false,
  "gitignore_entry_added": true
}
```

## Continuation rule

The loop continues only while the review verdict is `CONTINUE` because mapping
work or real unresolved automation risk remains. Missing or deleted controller
state is not verdict truth; repair the state file or ledger from fresh repo
context before honoring a stop decision.
