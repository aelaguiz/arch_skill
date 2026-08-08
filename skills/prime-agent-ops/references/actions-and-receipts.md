# Actions And Receipts

Use this reference only after resolving the exact universe and active/durable
identity. Every command shown is a final public owner form and remains
capability-gated: inspect installed help and the selected runtime schema before
using it. Older builds must yield an explicit limitation, not an internal or
raw-protocol fallback.

## Pick the semantic lane

- **Family message:** current Prime parent/sibling/direct-child communication
  (top-level roots are siblings); use `agent-message` when its family reach is
  sufficient.
- **Operator agent message:** an addressed message through Prime's public
  `send` command. It is broader than nuclear-family messaging and can wake a
  saved target. A busy target normally queues steering. Do not spoof `from`.
- **Prompt:** normal user input to an idle/admissible root. It can invoke
  AgentSession or extension commands and is not “text only.”
- **Steer:** correction delivered after the current assistant turn/tool-call
  batch and before the next model call.
- **Follow-up:** a later turn after current tool and steering work is exhausted.
- **Attached UI:** local human-owned TTY for transcript or extension UI. It is a
  sensitive-read/client-presence action and is never the remote v1 lane.
- **Cold create:** a new resident root with no target-before identity.
- **Exact resume:** reopens an exact durable root; returns `reused` when that
  tuple is already resident on the chosen socket.
- **Fork:** creates a new durable result from an exact durable source; source
  and result identities stay distinct.
- **True child:** the intended parent calls native `rlm()`; a new root/fork is
  not a child.
- **AIM-assisted create:** journaled account projection plus exact Prime root
  admission; see [aim-account-context.md](aim-account-context.md).

### Lifecycle × intent mapping

| Target state and intent | Public lane |
|---|---|
| live idle root, normal new turn | `input` prompt with `live_target` precondition |
| live busy root, current-turn correction | `input` steer with `live_target` precondition |
| live root, later turn | `input` follow-up with `live_target` precondition |
| saved root, operator message | `send` with `saved_target` precondition; this remains an agent message, not a follow-up |
| saved root, semantic follow-up | one saved-target `input` follow-up only when the advertised schema atomically rehydrates it; otherwise exact resume and then a separate live-target follow-up, with two authorizations/receipts |

Never silently substitute `send` for a prompt/steer/follow-up. For the two-step
saved-root path, disclose the resume/wake effect. An exact request to continue a
named saved root may authorize both steps when that effect is clear; otherwise
clarify before the resume mutation.

Do not send strings beginning with `/`, `!`, or `!!` and claim they reproduce
TUI-local command routing. Before command-shaped prompt input, use the public
bounded command inventory for the exact target when supported:

```bash
prime-agent commands --request-json - < validated-commands-request.json
```

Treat returned command names/source kinds as untrusted inventory, not automatic
authorization. The underlying external mutation remains separately authorized.
Commands requiring extension UI stay attached-client-only.

## Capability-gated public forms

Prefer typed request stdin whenever the selected public verb advertises it. The
request must follow that verb's installed schema exactly and include the full
universe and lifecycle precondition. Do not guess keys or construct a generic
command envelope.

```bash
prime-agent input --request-json - < validated-input-request.json
prime-agent send --request-json - < validated-send-request.json
prime-agent create --request-json - < validated-create-request.json
prime-agent rename --request-json - < validated-rename-request.json
prime-agent stop --request-json - < validated-stop-request.json
```

An advertised local argv form may use `--message-file -`, but only when it can
also carry every required compound precondition. Prefer the typed request form
above; if the argv form cannot carry expected build ID, daemon generation,
active ID, session ID, and canonical session file, report it as unsupported.
Never omit a precondition merely to make a command run.

Default input returns after server admission with an action ID and disposition.
Use the owner command's explicit wait option only when the user asked for Prime
action completion. A wait timeout leaves the same action live; it does not
cancel or authorize replay.

The public create owner must support resident cold create plus exact durable
resume/fork receipts. It must reject unknown/internal launcher options and must
not replace a reachable incompatible/stale socket owner. Creating or resuming a
root does not automatically send the brief: admit the root first, verify its
identity receipt, then use a separate `input` action.

If the selected build lacks public `input`, `commands`, or resident `create`,
say exactly which operation is unavailable. A local explicitly authorized
human-attached UI can be offered when it truly provides the operation. Remote
attach/TUI and hidden process/tmux glue are not alternatives.

## Authorization and revalidation

A user's request authorizes a mutation only when it fixes the host, target,
operation, payload/effect, and relevant account intent tightly enough to leave
no meaningful target or blast-radius choice.

Before acting, present:

- verified host and OS user;
- socket, build ID, daemon generation, protocol/schema, launcher lane;
- exact active and durable target or exact resume/fork source;
- layered current state and any conflict/ambiguity;
- action semantics and payload class (`verbatim`, `shaped_brief`, or omitted);
- account projection effect and whether it persists for future roots;
- destructive tree/schedule/client blast radius when relevant.

Immediately re-list the exact socket, then have the owner command server-check
one of these:

| Kind | Required check |
|---|---|
| live target | build + generation + active ID + durable ID/file |
| saved target | build + generation + durable ID/file + active ID null |
| cold create | build + generation + target before null |
| resume/fork | build + generation + exact durable source tuple |

Any universe, durable-session, saved/resident, source, or lease mismatch aborts.
Do not follow a replacement active ID automatically.

## Creation and continuation

Before cold create, exact resume, fork, or true-child coordination, apply the
shared orchestration policy and `$prompt-authoring` to the populated brief or
material delta. Make role, transport, starting context/authority, continuation,
isolation/capabilities, topology, and return evidence coherent without turning
them into a serialized form.

- Clean context is the default for independent work.
- Resume the exact root/child when the same role continues its work; preserve
  the returned active/durable handle.
- Fork only when a new durable branch is intended.
- For a true child, ask the exact parent to call `rlm()` and recover the returned
  handle from the public tree/receipt. The parent owns topology and integration.
- Preserve a verbatim user brief when requested. Otherwise separate binding
  goal/facts/constraints from caller conjecture and let the recipient reject
  the conjecture.

A continuation receipt must include verified host, universe, active ID, durable
ID/file when authorized, and exact supported continuation method. Never return
“latest session.”

## Destructive and excluded actions

Stop/archive aborts work and can cascade a root tree and schedules. Rename is a
state mutation. Attach can reveal transcript content. All require exact scope;
destructive actions require fresh target-and-blast-radius authorization.

Do not turn this skill into recipes for generic abort/clear/kill/delete, queue
clearing, arbitrary shell, import/export, retry/restart/update, doctor fix,
force, signals, manual PID/socket/file cleanup, or machine-wide shutdown. If the
user explicitly requests one, handle it as a separate high-risk owner-command
operation rather than a discovery fallback.

Never auto-answer extension UI requests. A public pending count is observation;
answering remains a human-visible attached-client action.

## Verify without overstating

After one dispatch:

1. Validate the typed command response and exact action/operation ID.
2. Re-read the exact universe/target with the brief owner view.
3. Match observed state to the requested claim: delivery, queued, started,
   action completed, failed, or still unknown.
4. When the request has external success criteria, collect their separate proof.
5. On timeout/drop, use the same action/operation identity to observe. Do not
   replay under a new identity.

`delivered` means admission/context delivery. `queued` means ordered work
exists. `action_completed` means the Prime action/turn finished. A model
`completed` verdict is advisory. None alone proves the user's outcome.

## Mutation receipt

Return one receipt for one mutation:

```yaml
scope:
  host: <verified host>
  os_user: <verified user>
universe:
  socket: <exact>
  expected_build_id: <exact>
  expected_daemon_generation: <exact>
precondition:
  kind: live_target | saved_target | cold_create | resume_or_fork
  expected_active_session_id: <exact | null | not_applicable>
  expected_session_id: <exact | not_applicable>
  expected_session_file: <canonical path when required>
target_before: <live/saved target card | null for cold create>
source_target: <exact durable source card for resume/fork | null>
action:
  kind: message | prompt | steer | follow_up | attach | create | resume | fork | spawn_child | rename | stop
  authorization_source: <exact user request or confirmation>
  payload: verbatim | shaped_brief | omitted
result:
  command_status: accepted | rejected | uncertain
  action_id: <exact or null>
  disposition: created | reused | forked | queued | started | not_applicable
  delivery_status: delivered | queued | not_applicable | unknown
  execution_status: not_started | started | action_completed | failed | unknown
  target_after: <fresh exact identities and safe account state | null>
  continuation: <exact supported handle/command | null>
verification: <fresh evidence for the requested claim>
unknowns: []
```

Redact payload contents by default. Include expected and observed identities in
a safe conflict receipt, but never include message/transcript content,
credential material, fingerprints, or raw environment.
