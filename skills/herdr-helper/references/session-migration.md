# Cross-session workspace migration

Use this runbook to reconstruct a workspace in another Herdr session, preserve
the same resumable agent conversation when the agent runtime exposes a durable
handle, and remove the source only after a verified cutover.

Herdr has no cross-session `workspace move`. Each session owns separate panes,
PTYs, sockets, and process state. The safe operation is therefore:

```text
inspect source -> reconstruct destination -> attach exact agent -> verify -> confirm -> close source -> verify again
```

The installed CLI and its live JSON results outrank the examples below.

## 1. Establish authority and session identity

Before any Herdr control command:

```bash
test "${HERDR_ENV:-}" = 1
herdr --help
herdr session
herdr workspace
herdr tab
herdr pane
herdr agent
```

Do not run bare `herdr`; that launches or attaches the TUI. Confirm both
sessions and their running state:

```bash
herdr session list --json
herdr --session <source-session> workspace list
herdr --session <destination-session> workspace list
```

Use `default` as the explicit default-session name. If the destination session
does not exist or is not running, ask the user to open an outer terminal and
run `herdr session attach <destination-session>`. Do not enable nested Herdr or
launch a TUI inside the current pane merely to create it.

Resolve the source workspace by live label plus cwd, not sidebar number. If
multiple workspaces match the user's words, show the smallest disambiguating
set and ask one question. If the destination already has the same logical
workspace, inspect it before deciding whether the request is already complete,
a duplicate, or a collision. Never overwrite it.

## 2. Capture the source inventory

Keep every read scoped to the explicit source session:

```bash
herdr --session <source-session> workspace get <source-workspace-id>
herdr --session <source-session> tab list --workspace <source-workspace-id>
herdr --session <source-session> pane list --workspace <source-workspace-id>
herdr --session <source-session> agent list
```

For each tab, choose one pane and capture its layout. For each pane, inspect the
pane and foreground process. When Herdr recognizes an agent, inspect it and read
enough recent output to prove the conversation identity:

```bash
herdr --session <source-session> pane layout --pane <pane-id>
herdr --session <source-session> pane get <pane-id>
herdr --session <source-session> pane process-info --pane <pane-id>
herdr --session <source-session> agent get <pane-id>
herdr --session <source-session> agent read <pane-id> \
  --source recent-unwrapped --lines 120
```

Record the facts needed for reconstruction and proof:

- workspace label and root cwd;
- ordered tab labels and active tab;
- pane cwd, manual label, split tree, ratios, and zoom state;
- foreground command and whether replay could cause side effects;
- detected agent, lifecycle state, terminal title, visible conversation name,
  provider/model when visible, and durable session ID or path when available.

Do not treat `idle`, `done`, a matching title, or similar text as sufficient
continuation proof. A migration of a live agent needs the runtime's exact
durable session handle or an exact live-attachment identity.

## 3. Resolve agent continuation before creation

Read the installed
[agent orchestration policy](../../_shared/agent-orchestration-policy.md)
before attaching or resuming a model agent. This is an exact-role
continuation: preserve the same provider, model, role, cwd, and durable handle.
Do not substitute a fresh agent because it looks similar.

Use the agent runtime's installed help and structured listing rather than
guessing syntax. For Prime Agent, the useful inspection pattern is:

```bash
prime-agent --help
prime-agent help attach
prime-agent list --json
```

Match the Prime Agent entry against several source facts: session name or
title, cwd, recent first message or transcript, activity, and current client
count. Preserve both its short live ID and durable `sessionId` or `sessionFile`
in the migration receipt. A unique multi-fact match is proof; a title-only
match is not.

If the agent exposes only resume-after-exit rather than live attach, do not stop
the source yet. First record the durable handle, build the destination shell,
explain that cutover will briefly stop the source client, and obtain the same
destructive confirmation required for source closure.

If no durable handle can be found, continue only with workspace reconstruction
and report that the conversation cannot be migrated exactly.

## 4. Reconstruct the destination

Create the workspace without changing the destination client's focus:

```bash
herdr --session <destination-session> workspace create \
  --cwd <source-cwd> \
  --label <source-label> \
  --no-focus
```

Read `.result.workspace.workspace_id`, `.result.tab.tab_id`, and
`.result.root_pane.pane_id` from the JSON response. These are new destination
IDs; never derive them from source IDs or sidebar order.

For additional tabs, use the source tab label and cwd:

```bash
herdr --session <destination-session> tab create \
  --workspace <destination-workspace-id> \
  --cwd <tab-cwd> \
  --label <tab-label> \
  --no-focus
```

Recreate useful pane topology from the captured split tree with explicit pane
IDs, directions, ratios, and cwd:

```bash
herdr --session <destination-session> pane split <destination-pane-id> \
  --direction right \
  --ratio <ratio> \
  --cwd <pane-cwd> \
  --no-focus
```

Use `down` for horizontal splits. Parse each returned pane ID before the next
split. Preserve semantic layout rather than terminal-cell dimensions; clients
may have different sizes. Reapply manual pane names after creation. Leave
ordinary shell panes at their prompts unless the user explicitly wants their
foreground commands restarted and the side effects are understood.

## 5. Attach the exact agent

Run the verified continuation command in the matching destination pane. For a
live Prime Agent session:

```bash
herdr --session <destination-session> pane run <destination-pane-id> \
  "prime-agent attach <verified-agent-id>"
```

Use `pane wait-output` with a stable conversation marker, then read the pane:

```bash
herdr --session <destination-session> pane wait-output <destination-pane-id> \
  --match <stable-marker> \
  --source recent-unwrapped \
  --lines 120 \
  --timeout 30000

herdr --session <destination-session> pane read <destination-pane-id> \
  --source recent-unwrapped --lines 120
```

For a Herdr-supported agent kind with a native resume argument, use
`herdr agent start` only after verifying the destination pane is an available
shell and the runtime's exact continuation syntax. Put native agent arguments
after `--`. Do not send a new prompt merely to prove attachment.

An attached agent UI can show `unknown` in Herdr when the destination pane runs
only a client process while the worker remains elsewhere. Treat detection and
continuity as separate claims: disclose the detection downgrade, but accept
continuity only when the runtime handle and transcript prove it.

## 6. Verify before cutover

While the source still exists, verify all of the following:

```bash
herdr --session <destination-session> workspace get <destination-workspace-id>
herdr --session <destination-session> tab list --workspace <destination-workspace-id>
herdr --session <destination-session> pane list --workspace <destination-workspace-id>
herdr --session <destination-session> pane process-info --pane <destination-pane-id>
herdr --session <destination-session> pane read <destination-pane-id> \
  --source recent-unwrapped --lines 40
```

The completion evidence is:

- correct destination session, label, cwd, tabs, and useful pane topology;
- expected foreground UI or intentionally idle shell in every pane;
- exact same durable agent handle, matching conversation transcript, and no
  unfinished or streaming action before cutover;
- source workspace still present as rollback;
- no focus change unless requested.

For Prime Agent, `prime-agent list --json` should show the same session with two
attached clients before closing the source. If it does not, stop and explain
the discrepancy.

Ask the user to inspect the destination when an interactive UI is load-bearing.
Then obtain fresh confirmation to close the exact source workspace.

## 7. Cut over and verify again

For a copy-only request, stop before this section and report that the source was
intentionally retained. For a move or migration, obtain fresh confirmation,
then close only the recorded source workspace:

```bash
herdr --session <source-session> workspace close <source-workspace-id>
```

Immediately verify:

```bash
herdr --session <source-session> workspace list
herdr --session <destination-session> workspace get <destination-workspace-id>
herdr --session <destination-session> pane read <destination-pane-id> \
  --source recent-unwrapped --lines 40
```

For Prime Agent, verify the same ID now reports one attached client, remains
idle or in its expected state, and has no unfinished action. The removed Herdr
layout is not recoverable as a live PTY, but the exact saved conversation must
remain attached or resumable at its recorded session path.

## Failure handling

- **Destination creation fails:** leave the source untouched and report the
  Herdr error plus any destination ID that was allocated.
- **Agent attachment is ambiguous:** leave both workspaces intact. Report the
  candidate handles and the missing disambiguating fact.
- **Destination UI works but Herdr says `unknown`:** verify the process,
  transcript, and runtime handle; disclose detection separately.
- **Source closure returns an unknown result:** inspect both session workspace
  lists before retrying. Do not issue a second close blindly.
- **Post-cutover destination fails:** do not create another copy. Preserve the
  saved agent handle and repair or reattach in the existing destination pane.
