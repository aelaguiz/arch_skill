---
name: prime-agent-ops
description: "Inventory and operate discoverable Prime Agent daemon/session universes on an approved local or SSH-reachable host through capability-gated public Prime and AIM CLIs. Use to reconstruct root/RLM trees, explain layered activity, deliver an exact message/prompt/steer/follow-up, or perform an exact authorized create/resume/fork/rename/stop with identity-safe receipts. Not for ordinary native-child delegation, external agent subprocesses, family-scoped observation/message, offline history, generic SSH/daemon administration, or AIM account administration."
---

# Prime Agent Ops

Operate Prime through its public host-local CLI. SSH is only transport to that
same CLI; AIM is only the account-projection and account-aware-create owner.
Never invent a wrapper, controller, socket client, registry, or background
harness.

## Route first

Use this skill when the job is cross-universe Prime inventory or an exact
operation on a persisted Prime root or descendant.

Route away when a narrower owner fits:

- use the current host's native child system for ordinary same-host delegation;
- use `agent-message` or `agent-observe` for the current Prime family's
  parent/sibling/direct-child lane;
- use `$agent-delegate` for a deliberately external Claude, Codex, Cursor,
  Grok, or Kimi process/session;
- use `$agent-history` where installed for offline Codex or Claude transcript/history search;
- handle generic SSH administration, Prime development, daemon cleanup, and AIM
  account administration outside this skill.

Do not interpret “latest,” a display name, cwd, PID, or a short ID as authority
to mutate. Clarify an ambiguous “start another agent,” “resume my agent,” or
“message the latest session” request before acting.

## Non-negotiables

- Before creating, resuming, replacing, forking, or coordinating a model
  session, read and apply `../_shared/agent-orchestration-policy.md`. Apply
  `$prompt-authoring` to the populated brief or material resume delta. Keep
  caller theories challengeable unless the user made them binding; preserve
  exact text when verbatim relay is requested.
- Compare the installed launcher's help/version, its source/dist/installed lane,
  and the running universe's hello/build/capability/schema. Checkout source is
  not proof of installed or running behavior.
- Resolve both the resident target and durable transcript. Re-check the exact
  universe and compound target immediately before a mutation.
- Follow **observe → resolve → authorize → re-resolve → act once → verify**.
  Read-only work never authorizes wake, attach, input, account selection,
  repair, stop, restart, or shutdown.
- Run only public commands advertised by the selected installed build and
  runtime capability schema. If `--brief-json`, `--request-json -`, `input`,
  `commands`, `create`, compound target preconditions, or AIM journaled create
  is absent, report that limitation. Never fall back to raw socket traffic,
  internal daemon verbs, private worker descriptors, RPC side sessions, or a
  custom script.
- Treat command acceptance, queue admission, delivery, execution start, action
  completion, task verdict, and the user's requested outcome as separate
  claims. Never flatten them into “done.”
- Do not expose messages, prompts, queue previews, recaps, diagnostics,
  fingerprints, credentials, environment, or full transcripts by default.
- Never blindly retry a mutation after a timeout or dropped connection. Observe
  the exact target and action identity first; unresolved dispatch is
  `uncertain`.

## First move

1. Establish whether the host is local or an explicitly approved SSH
   destination, and record the expected OS user/HOME, operation, payload class,
   account intent, and requested proof.
2. Read [universe-and-session-identity.md](references/universe-and-session-identity.md).
3. Resolve and pin an owner-safe launcher path. Inspect public help, version,
   lane, and advertised capabilities without touching a default live socket.
4. For a remote host, read
   [ssh-transport.md](references/ssh-transport.md) before connecting or forming
   a command.

## Workflow

### 1. Discover only the authorized scope

If the user asked for all universes visible to the approved OS user, run the
public machine inventory and keep every returned row/error:

```bash
prime-agent status --json
```

If the user supplied an exact socket set, do **not** expand it through machine
inventory: query only those sockets. For each in-scope reachable socket, use
the capability-gated product-owned brief list; include saved roots only when
the request needs durable inventory or continuation. Read
[discovery-and-status.md](references/discovery-and-status.md) for the flow,
tree projection, status evidence, sensitive-read boundary, and inventory
output.

### 2. Resolve identity and state

Build root/RLM trees only from explicit parent and RLM identifiers. Reconcile
durable duplicates by full session ID plus canonical session file while
preserving every universe in which the row was observed. Report orphaned,
cyclic, conflicting, incompatible, stale, and unknown evidence rather than
repairing it.

Project status in layers: universe reachability, worker health,
lifecycle/residency, direct runtime activity, action/queue state, descendants,
extension input count, task verdict, and recent progress. Do not invent one
`waiting` flag or call a model `needs_input` verdict proof that a human answer
is pending.

### 3. Authorize one exact action

Before mutation, show the verified host/user, socket/build/generation, active
and durable identity, current layered state, requested action, payload class,
account effect, and blast radius. The user's existing exact action-shaped
request is sufficient unless the target, payload, effect, or destructive scope
is ambiguous. Stop/archive/abort/clear/kill/delete and broad process actions
need fresh exact authorization.

Read [actions-and-receipts.md](references/actions-and-receipts.md). If AIM
account context or account-aware creation is requested, also read
[aim-account-context.md](references/aim-account-context.md).

### 4. Re-resolve, act once, and verify

Repeat the exact-socket lookup and require the public owner command to
server-check the expected universe and lifecycle-appropriate target
precondition. Use the lane that matches the intent: family message, operator
agent message, prompt, steer, follow-up, local attached UI, cold create, exact
resume, fork, true child, or journaled AIM-assisted create.

After the call, inspect its typed receipt and fresh target state. Waiting for an
exact action ticket proves only that Prime action's completion. Prove the
user's requested outcome separately when the request requires it.

## Return

- Discovery returns one inventory report spanning all reached and unreachable
  hosts/universes; never force it into a singular target.
- Mutation returns one receipt with authorization source, precondition,
  target/source before, typed disposition, target after, continuation handle,
  verification, and unknowns.
- State what coverage could not include: other UIDs, hidden client-owned
  workers, undiscoverable stopped custom sockets, and historical descendants
  not exposed by public catalogs.

## Reference map

- [universe-and-session-identity.md](references/universe-and-session-identity.md)
  — topology, identity, visibility, and public/private boundaries.
- [discovery-and-status.md](references/discovery-and-status.md) — inventory,
  tree reconstruction, layered status, and report shape.
- [actions-and-receipts.md](references/actions-and-receipts.md) — action lanes,
  authorization, compound preconditions, verification, and mutation receipts.
- [aim-account-context.md](references/aim-account-context.md) — Prime/AIM
  ownership, safe labels, journaled create, and excluded account mutations.
- [ssh-transport.md](references/ssh-transport.md) — approved destination,
  fixed remote commands, structured stdin, and uncertainty handling.
