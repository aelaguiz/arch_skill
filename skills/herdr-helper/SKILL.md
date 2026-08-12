---
name: herdr-helper
description: "Run reusable higher-level Herdr operations that compose multiple session, workspace, pane, and agent steps. Use when the user asks to migrate, copy, transfer, or reorganize a workspace between Herdr sessions while preserving its directory, layout, and exact resumable agent continuity when available. Not for ordinary one-session navigation, splitting panes, creating workspaces, or raw CLI control; use $herdr for those primitives."
metadata:
  short-description: "Higher-level Herdr session workflows"
---

# Herdr Helper

Use this skill for reusable Herdr workflows that are larger than one primitive
CLI action. The current operation is cross-session workspace migration. Add a
new operation as a focused reference only when it has its own repeated user
problem, safety boundary, and proof of completion.

## Scope

This skill owns the throughline across multiple Herdr sessions: source
inventory, destination reconstruction, exact agent continuation, verification,
and safe cutover. `$herdr` remains the nearest peer and owns ordinary pane,
tab, workspace, and agent control inside one session.

Use this skill when:

- a workspace must move or be copied from the default session to a named
  session, between two named sessions, or back to default;
- the destination should preserve the workspace label, cwd, tabs, pane layout,
  and resumable coding-agent conversation where the runtime supports it;
- the user wants the old workspace removed only after the destination is
  proved usable.

Do not use it for routine focus, navigation, splitting, renaming, or same-session
pane moves. Apply `$herdr` directly for those primitives. Do not claim a live
cross-session PTY move: Herdr sessions own separate servers and process trees,
so migration is a verified reconstruction and cutover.

## Required context

- Apply the installed `$herdr` contract before issuing Herdr control commands
  when that peer skill is available. Otherwise use this package's preflight and
  treat the installed CLI as authoritative when examples drift.
- For a workspace migration, read
  [references/session-migration.md](references/session-migration.md) completely
  before changing either session.
- When the workflow attaches, resumes, replaces, or restarts a model agent,
  read `../_shared/agent-orchestration-policy.md`. Preserve the exact role and
  durable session handle. Apply `$prompt-authoring` to any new or materially
  changed brief; an exact attach with no new prompt is continuation, not a new
  dispatch.

## Non-negotiables

- Verify `HERDR_ENV=1` before any Herdr control command. Stop if this agent is
  not inside Herdr.
- Resolve source and destination sessions explicitly. Use `--session` for
  cross-session commands and parse every new ID from JSON; IDs never carry
  across sessions.
- Inspect before mutating. Record the source workspace label, cwd, tab and pane
  structure, foreground processes, agent identity, and durable continuation
  handle when one exists.
- Keep the original workspace intact while building and verifying the
  destination. Use `--no-focus` unless the user asks for a focus change.
- Never relaunch an unknown foreground process merely to imitate the source.
  Attaching an exact live agent is allowed when verified; restarting a server,
  test, editor, or other side-effectful command needs explicit intent.
- Require fresh user confirmation immediately before closing the source
  workspace. The initial migration request authorizes destination creation and
  verification, not deletion of the rollback copy.
- If exact agent continuation cannot be proved, migrate the shell layout only
  and report the missing continuity. Never present a fresh conversation as the
  migrated one.

## First move

1. Read the session migration reference.
2. Verify the Herdr environment and inspect the installed `session`,
   `workspace`, `tab`, `pane`, and `agent` command groups.
3. Resolve the user's natural-language source workspace and destination
   session from live lists. Ask one short question only if the live state does
   not identify them uniquely.
4. Capture a read-only source inventory and define the evidence that will prove
   the destination is equivalent enough for cutover.

## Workflow

1. **Inventory.** Resolve both sessions, reject a same-session no-op, and
   inspect destination collisions before creating anything.
2. **Snapshot.** Capture workspace metadata, tab labels, pane topology and cwd,
   foreground processes, recent screen state, and exact agent continuation
   evidence.
3. **Reconstruct.** Create the destination workspace without focus, parse its
   new IDs, reproduce the useful tab and pane structure, and leave ordinary
   shell panes idle.
4. **Continue.** Attach or resume only the verified same agent conversation.
   Keep role, provider/model, cwd, and durable session identity unchanged.
5. **Verify.** Prove the destination workspace, process/UI state, and agent
   handle while the source still exists. Surface any Herdr detection downgrade
   such as `unknown` separately from conversation continuity.
6. **Cut over.** Ask for confirmation, close only the exact source workspace,
   then verify it is absent and the destination remains healthy.

For a copy-only request, stop after verification and report that the source was
intentionally retained. Run the cutover step only for a move or migration.

If verification becomes ambiguous, stop with both copies intact and report the
source ID, destination ID, and smallest unresolved fact. Do not create a third
copy or clean up an uncertain destination to make the run look finished.

## Output expectations

Lead with `migrated`, `copied but source retained`, or `blocked before cutover`.
Report:

- source session, workspace label, and old workspace ID;
- destination session and new workspace ID;
- preserved cwd, tab count, pane count, and any layout difference;
- exact agent/session handle and continuation proof, or the precise gap;
- whether the source was retained or removed, plus post-cutover verification.

## Reference map

- `references/session-migration.md` — cross-session inventory,
  reconstruction, agent continuation, verification, cutover, and recovery
