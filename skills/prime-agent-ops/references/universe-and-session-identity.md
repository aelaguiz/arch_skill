# Universe And Session Identity

Read this before interpreting a Prime inventory or selecting a mutation target.

## Topology and authority

A Prime build-scoped supervisor owns one public Unix socket. It owns public
routing, resident root workers, health/recovery, attachments, root-to-root
operator messages, the saved-root catalog, and mutation journals. One resident
worker owns one top-level root and that root's RLM descendants, kernels, tools,
schedules, and transcript state.

An idle RLM descendant can be passivated and later rehydrated. A saved root can
exist without a resident worker. A durable transcript may not have two live
writers; a lease conflict across universes is an error, not a reason to choose
one by recency.

Prime owns daemon, session, action, and RLM runtime truth. AIM does not. AIM
owns account records, the local credential projection used by future roots,
and the account-aware create transaction.

## Keep both identities

Treat these as separate identity layers:

- **Universe:** verified host, OS user/HOME, agent directory, exact socket,
  build ID, daemon generation, protocol/schema, executable, and launcher lane.
- **Resident target:** universe plus full active session ID.
- **Durable target:** full session ID plus canonical session file.
- **Live mutation target:** the selected universe, full active ID, and full
  durable tuple together.

The active ID is a runtime address. The durable ID/file identifies the
persisted transcript. A runtime replacement can retain its active ID while
switching durable session state, so neither is sufficient alone.

Names, cwd values, PIDs, list order, timestamps, short suffixes, “current,” and
“latest” are locators or diagnostics only. They can help the user identify a
candidate, but are never a mutation key.

Lifecycle-specific preconditions are:

- `live_target`: expected universe plus full active and durable identity;
- `saved_target`: expected universe plus exact durable identity and expected
  active ID `null`;
- `cold_create`: expected universe with no target-before identity;
- `resume_or_fork`: expected universe plus an exact durable source tuple,
  kept distinct from the result target.

Every supported mutation must have the daemon compare the relevant compound
precondition immediately before admission. Client-side polling alone does not
close the replacement race.

## Source, dist, installed, and running are different

Record which executable and entrypoint will run and whether it is a source,
dist, or installed lane. Compare that with the runtime hello/capability/build
identity on the exact socket.

Do not infer any of these from a checkout's source files. An installed launcher
can be older than source; a dist bundle can be older than both; a socket can be
owned by a different dirty build. A daemon row called `current` can still have
a different build identity because current/stale compatibility may compare
only app version, protocol, and schema.

If the executable lane, build, generation, protocol, schema, or public help is
missing or contradictory, keep the universe in the report and block mutation
until the selected public contract is unambiguous.

## Reconstruct trees from explicit edges

Use only public explicit fields:

- root/top-level versus RLM kind;
- active and durable IDs;
- parent active and durable IDs;
- RLM child/node ID and depth;
- root identity;
- child run/reply state when exposed.

Never infer parentage from names, timing, shared cwd, session-file adjacency, or
list order. Preserve nodes with missing parents as unresolved orphans. Report
cycles, multiple-parent claims, root conflicts, and links that cross
incompatible universes rather than repairing them.

A fresh root, a fork, or reopening a child transcript as a root does not create
an RLM parent edge. A true child exists only after the intended parent calls its
native `rlm()` primitive and the public tree exposes that relationship. Default
maximum depth is one unless the owning root's configuration says otherwise;
children inherit the root's cwd/runtime resources, model constraints, and
credential configuration/bindings.

## Deduplicate durable rows without erasing provenance

Universes that share an agent/session directory can each expose the same saved
catalog row. Deduplicate only by the full durable tuple `(sessionId,
canonicalSessionFile)`. Preserve every observing universe, lifecycle conflict,
resident claim, and lease error.

The same session ID at a different canonical path is not an automatic match.
Treat moved/copied duplicates, ID/path mismatch, path swaps, and ambiguous
catalog resolution as conflicts.

## Visibility boundary

“Every session” means every universe and root discoverable to the approved OS
user through the public machine-status and per-socket catalog surfaces. Always
state these exclusions:

- daemons owned by another UID;
- stopped custom sockets outside discoverable directories;
- client-owned text/JSON/RPC workers hidden from another owner client;
- historical descendants not exposed by the current catalog;
- unreachable hosts or incompatible universes.

A stale row is not proof of a dead daemon or authority to stop it. A visible PID
is diagnostic, not identity or authorization.

## Use only the public owner surface

This skill uses supported public Prime/AIM CLI commands only.

- An exported local SDK can be a legitimate product implementation surface,
  but it is not a reason for the skill to author a client.
- RPC/text/JSON launch modes own their client session; do not start one as a
  passive inventory shortcut.
- The public supervisor socket is a same-UID trust boundary, not a network API.
  Never raw-write, forward, proxy, expose, chmod, or copy it.
- Worker descriptors, tokens, sockets, private protocol messages, removed
  nested daemon commands, and internal adapters are never fallbacks.
