# Comment Loop Controller

Comment-loop-specific state schema and verdict source. Core doctrine and lifecycle live in references/controller-lifecycle.md. This document documents only the comment-loop-specific additions.

## Verdict source

`comment-loop auto` is an internal-verdict controller. The terminal verdict is read from the `Controller verdict` block in `_comment_ledger.md` after each fresh `review` pass.

- `CONTINUE` — the Stop hook keeps state armed and launches the next `$comment-loop` pass.
- `CLEAN` — the Stop hook clears state, deletes `_comment_ledger.md`, and removes the `.gitignore` entry.
- `BLOCKED` — the Stop hook clears state and stops honestly.

The `review` pass itself runs in fresh context:

- Codex: `codex exec --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox` with `$comment-loop review`
- Claude Code: `claude -p --settings '{"disableAllHooks":true}'` with explicit context and `/comment-loop review`

## State file schema

Paths (session-scoped, per the shared contract):

- Codex: `.codex/comment-loop-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/comment-loop-state.<SESSION_ID>.json`

Minimal shape:

### Comment-loop state fields

_definitions_

- **Version** — Integer schema version. Must be `1`.
- **Command** — The controller command string: `auto`.
- **Session ID** — The session id the state was armed under.
- **Armed At** — Epoch seconds when the state was written.
- **Ledger Path** — Path to the comment ledger file (typically `_comment_ledger.md`).
- **Gitignore Created** — Boolean. Whether the skill created the root `.gitignore` file itself.
- **Gitignore Entry Added** — Boolean. Whether the skill added the `_comment_ledger.md` entry to `.gitignore`.

## Continuation rule

The loop continues only while the review verdict is `CONTINUE` because mapping work or high-impact unresolved explanation work remains. The first turns may be mapping-only — that is correct behavior, not a failure to make progress.
