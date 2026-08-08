---
title: "Prime Agent Ops Skill — Implementation Plan"
date: 2026-08-07
status: implementation-ready
fallback_policy: forbidden
owners: [Amir]
reviewers:
  - Prime Agent runtime expert
  - AIM credential expert
  - skill-authoring reviewer
  - adversarial safety reviewer
doc_type: new_system
related:
  - /Users/aelaguiz/workspace/psagentspace/research/prime-agent-local-observability-2026-08-07.md
  - /Users/aelaguiz/workspace/prime-agent/packages/coding-agent/docs/daemon.md
  - /Users/aelaguiz/workspace/prime-agent/packages/coding-agent/docs/usage.md
  - /Users/aelaguiz/workspace/aimgr/README.md
---

# TL;DR

- **Outcome:** ship a prompt-first `prime-agent-ops` skill that lets an authorized Codex, Claude, or other shell-capable agent inventory every discoverable Prime Agent universe on an approved local or SSH-reachable host, reconstruct root/RLM trees, explain status without inventing a single “waiting” flag, and perform an exact authorized session operation with a verifiable receipt.
- **Approach:** use Prime's public host-local CLI as the normal control surface, SSH only as transport to that same CLI, and AIM only for account projection and account-aware root launch. Do not create a daemon wrapper, socket gateway, runner, controller, host registry, or background harness.
- **Required enabling work:** close a small set of product gaps in `prime-agent` before the skill promises explicit prompt/steer/follow-up injection or unattended resident-root creation. The current public CLI can discover/list/send/attach/rename/stop, but its advertised `send --steer|--follow-up` flags do not work and it has no public detached resident-root `create` command.
- **Package:** `skills/prime-agent-ops/SKILL.md` plus five focused references. No scripts or runtime service.
- **Install:** add the skill to the supported install inventories in `Makefile`, README, usage guide, and root routing doctrine. Validate only in isolated install destinations; never install into or operate Amir's live Prime environment as a test.
- **Non-negotiables:** exact host + OS user + socket/build + full active/durable identity before mutation; observation before action; no raw socket protocol recipes; no hidden `prime-agent daemon ...` commands; no secret or full-transcript relay by default; no blind mutation retry after an uncertain result.

## North Star

### Claim

> If an authorized agent uses `$prime-agent-ops`, it can identify exactly which visible Prime universe and persisted session it is observing or changing, explain the evidence for that session's current state, and carry out only the requested Prime/AIM action without inventing infrastructure, confusing account state with session state, or claiming more completion than the receipt proves.

### Canonical asks

1. “On this Mac, show every discoverable Prime Agent daemon and every visible root/subagent tree. Explain who is writing, running tools, waiting on a child, queued, idle, classifying, completed by verdict, inactive, failed, stale, or unknown.”
2. “On `<approved-host>`, deliver this exact message, steering correction, or follow-up to this exact Prime session, then report whether it was accepted, queued, started, completed, failed, or remains uncertain.”
3. “Create or resume a full Prime root in `<cwd>` on `<approved-host>` with this role/brief and account intent. Return the host, universe/socket/build, active session ID, durable session ID/path, configured AIM label, actually bound label, and exact continuation method.”

### Anti-cases

- Ordinary same-host delegated work: use a native child under `skills/_shared/agent-orchestration-policy.md`.
- A deliberate external Claude/Codex/Cursor/Grok/Kimi subprocess or session: use `$agent-delegate`.
- Family-scoped parent/sibling/direct-child communication from the current Prime tree: use `agent-message`; family-scoped observation: use `agent-observe`.
- Offline Codex or Claude transcript/history search: use `$agent-history`.
- Generic SSH administration, process cleanup, Prime daemon development, AIM account administration, or Redis maintenance.
- Broad “fix/restart/clean all daemons” requests. This skill may explain exact owner commands, but must not turn observation into cleanup.

### Acceptance evidence

- A disposable multi-daemon fixture shows two build/socket universes are independently inventoried, their visible root/RLM trees are reconstructed, durable duplicates are reconciled, and an exact mutation never crosses the selected universe.
- A busy target demonstrates different prompt, steer, follow-up, and agent-message semantics with receipts and post-state proof.
- A new resident root can be created without a hidden harness, seeded through stdin-safe input, and returned with both active and durable identities.
- A plain resume preserves the persisted account binding; configured-versus-bound AIM labels are reported distinctly and no secret/fingerprint appears.
- Fake-SSH tests prove exact host/user targeting, fixed noninteractive commands, no local fallback, and hostile request values arriving without shell interpretation.
- Cold reviewers can trace every command and status claim to the current public source contract and find no dependency on removed/internal CLI syntax.

### Key invariants

1. **Two identities, never one:** resident identity is `(host, uid/HOME, agentDir, socketPath, buildId, activeSessionId)`; durable identity is `(sessionId, canonical sessionFile)`. A name, cwd, PID, short suffix, or “latest” is never a mutation key.
2. **Two planes, never one:** Prime owns daemon/session/RLM runtime truth. AIM owns Redis-backed credential records, local Prime credential projection, and AIM-assisted launch. `aim prime status` is not session status.
3. **Host-local control:** remote operation means running the same Prime/AIM commands on the approved host as the owning OS user through SSH. Never expose, forward, chmod, copy, or network-wrap a Prime Unix socket.
4. **Observe → resolve → authorize → re-resolve → act once → verify.** A read-only request never authorizes attach, wake, message, account selection, repair, stop, restart, or shutdown.
5. **Receipts are layered:** command acceptance, queue admission, delivery, execution start, execution completion, task verdict, and user-requested outcome are distinct claims.
6. **Status is layered:** daemon reachability, worker health, persistence/lifecycle, runtime activity, queues/actions, descendants, heuristic task verdict, and recent progress are reported separately. Do not invent a universal `waiting` boolean.
7. **Mutation preconditions match lifecycle:** every action server-checks expected daemon build/generation. A live-target action also requires active + durable identity; a saved-target wake requires exact durable identity and expected active ID `null`; cold create has no target-before identity; resume/fork names an exact durable `source_target` distinct from the result. Any mismatch aborts instead of targeting a replacement universe or transcript.
8. **No hidden fallback:** if the current runtime lacks the supported public operation, say so or use an explicitly authorized attached UI. Do not silently use removed CLI verbs, raw JSONL sockets, worker descriptors, RPC side sessions, or a custom controller.
9. **Account labels are not credentials:** the skill may report only safe provider/source/label state when relevant. It never reads or returns tokens, provider IDs, fingerprints, raw Redis records, `auth.json`, backups, worker tokens, environment dumps, or helper output.
10. **No live-environment validation:** development tests use isolated HOME/agent/session/runtime directories, explicit non-default sockets, faux providers, fake SSH, and fixture accounts only.

## Scope

### In scope

- Local and explicitly approved SSH-host discovery.
- Every daemon universe discoverable to the current OS user through Prime's machine-wide status implementation.
- Per-universe resident roots, RLM descendants, passivated descendants exposed by the daemon, and saved roots returned by `list --all`.
- Detailed state projection and tree reconstruction from explicit identifiers.
- Public prompt/input, agent-message, attach, rename, resume/fork, create, and stop workflows after capability checks and authorization.
- Exact full-root creation/resume and true-child spawning through the owning parent.
- Read-only AIM projection/account context and explicitly authorized account-aware new-root launch.
- Synthetic/local receipts and remote SSH receipts.

### Out of scope

- Other OS users' daemons, unapproved hosts, stopped arbitrary socket paths that Prime cannot discover, and client-owned workers hidden from a different owner client.
- A fleet registry, daemon federation, network service, socket proxy, host scanner, controller, runner, or long-lived monitor.
- Direct Redis use for session discovery/control.
- Automatic account rotation/rebinding, login, reauthentication, uninstall, native-auth replacement, or account repair.
- Automatic response to extension UI prompts/approvals. A pending count may be reported; answering requires a human-visible attached client and exact approval.
- Raw generic daemon operations such as arbitrary bash, delete/import/export paths, queue clearing, global state/refinement, retry/restart/update, `doctor --fix`, force, or machine-wide shutdown as normal skill recipes.
- A promise to enumerate every historical descendant artifact under an inactive/archived root when current catalog APIs do not expose it.

## Research Snapshot And Confidence Boundary

This plan is grounded in the **current working trees on 2026-08-07**, not merely committed or installed behavior:

- `/Users/aelaguiz/workspace/prime-agent`, branch `aimgr-credential-broker`, contains uncommitted credential-binding reset changes.
- `/Users/aelaguiz/workspace/aimgr`, branch `main`, contains uncommitted AIM Prime run/resume/session-identity work.
- `/Users/aelaguiz/workspace/arch_skill` contains unrelated user work and untracked files.

No live Prime socket, session, AIM account, Redis service, SSH host, credential, process, or tmux session was queried or mutated during planning. Existing tests were read as executable specifications but were not run. Implementation must compare source, built `dist`, installed launcher help, and runtime hello separately before making a shipped claim.

### Research coverage

Parallel read-only reviews covered:

- all files under `packages/coding-agent/src/modes/daemon` and adjacent public CLI, main routing, agent connection, action store, RLM, session manager, external auth, socket, and relevant tests/docs;
- AIM Redis/account authority, Prime target adapter, descriptor/helper protocol, run/resume/use/status/uninstall, provider selection, session identity, and tests;
- multi-daemon discovery, remote SSH/TTY lifecycle, security boundaries, source/dist behavior, validation design, skill architecture, plan architecture, and adversarial failure modes;
- a line-by-line fact check of `/Users/aelaguiz/workspace/psagentspace/research/prime-agent-local-observability-2026-08-07.md`.

### Fact-check verdict on the existing observability note

Keep the note as useful time-scoped research, but do not treat its control design as authoritative. Correct these points in the new skill/reference truth:

- say **all discoverable daemons visible to the approved OS user**, not literally every daemon/session;
- use `prime-agent status --json`, never the removed `prime-agent daemon ps` or bare `prime-agent ps`;
- use `list --all --json` when saved roots matter and deduplicate durable rows by canonical session identity across universes that share an agent/session directory;
- distinguish active build-scoped rosters from shared durable catalogs and cross-process session leases;
- add `unfinishedActionCount`, `sessionActions`, parent active/durable links, RLM child/node/depth, reply, heartbeat, cron, and worker-health fields;
- label `taskState=needs_input` as a conservative model verdict, not proof a human response is pending;
- describe steering as arriving after the current assistant turn/tool batch and before another model call, not as arbitrary mid-tool injection;
- separate AIM `use`, `run`, plain `resume`, and rotating resume; the current rotate/session-identity path is wholly working-tree-only;
- replace any collector/authenticated-control-plane recommendation with a prompt-first skill over supported host-local commands.

## Current Architecture

### Process and storage topology

- One build-scoped supervisor owns one public Unix socket.
- The supervisor owns public routing, workers, health/recovery, attachments, cross-worker root messaging, the saved-session catalog child, and mutation journals.
- One resident worker owns one top-level root and all of its RLM descendants, kernels, tools, bash, schedules, and transcript state.
- Idle descendants may be passivated and rehydrated. A root worker may be evicted only under stricter idle/no-client/no-job conditions.
- A durable JSONL may not have two live writers; process-aware session leases enforce this across universes.
- A root runtime replacement can preserve its volatile `activeSessionId` while changing the durable `sessionId/sessionFile`. Therefore both identities must always be shown after new/resume/fork/switch.

Primary anchors:

- `prime-agent/packages/coding-agent/docs/daemon.md`
- `src/modes/daemon/daemon-supervisor.ts`
- `src/modes/daemon/daemon-mode.ts`
- `src/core/session-lease.ts`
- `src/core/agent-session-runtime.ts`

### Universe discovery

`prime-agent status --json` calls `runPs`, which merges:

1. live Unix listeners discovered through `ss` or `lsof`/`ps`;
2. socket files in the current default Prime socket directory;
3. supervisor sockets referenced by tracked workers in the current agent directory;
4. per-socket `daemon_hello` and `list` probes.

Rows report `current | stale | unreachable | orphan-file`, socket, process/runtime metadata, build/protocol/schema, a resident count when probeable, and whether the socket is the invoking build's default.

Limits that the skill must surface:

- orphan discovery is not exhaustive outside the current socket directory/agent directory;
- another UID is outside the permission boundary;
- hidden client-owned print/JSON/RPC workers are not visible to a different owner client;
- `current|stale` compares app version/protocol/schema, not build ID; a different dirty build can still be `current`, while `isDefault`, socket, and reported build identity remain distinct evidence;
- `stale` is not dead or safe to stop;
- `status.sessionCount` is a visible resident count, not saved total;
- alternate hosts must be queried host-locally through an approved transport.

Primary anchors:

- `src/cli/daemon-ps.ts`
- `src/cli/public-command.ts`
- `src/modes/daemon/daemon-socket.ts`
- `src/modes/daemon/daemon-runtime-identity.ts`

### Public, exported, and private surfaces

| Surface | Status | Skill policy |
|---|---|---|
| `status`, `list`, `agents`, `attach`, `stop`, `rename`, `send`, ordinary launcher/resume/fork | Current public CLI | Normal lane after capability/help check. |
| Exported `DaemonClient` / `DaemonAgentConnection` | Real local SDK, capability-gated | Product implementation may use it to add supported CLI commands. The shipped skill does not hand-roll or genericize it. |
| `prime-agent --mode rpc` | Supported, but owns a client-owned session | Not passive global control; do not start it just to inspect another universe. |
| `src/cli/daemon-command.ts` old/internal verbs | Internal adapter only | Never teach `prime-agent daemon ...`; public routing rejects it. |
| Public supervisor socket protocol | Trusted same-UID local API, no per-session ACL | Never network-expose or raw-write it. |
| Private worker socket/descriptors/tokens | Supervisor-worker coordination | Never inspect or use from the skill. |

### Current public commands and proven gaps

| Job | Current supported form | Current truth / gap |
|---|---|---|
| Discover machine universes | `prime-agent status --json` | JSON is an array; command must be first. |
| List resident/saved sessions | Current `list ... --json` is content-rich | Add `list ... --brief-json` with a versioned fixed allowlist; raw JSON requires sensitive-read authorization. Query every reachable universe and reconcile saved duplicates. |
| Interactive universe UI | `prime-agent agents --daemon-socket "$S"` | Can ensure/start the daemon; not read-only JSON. |
| Attach live target (current, insufficient alone) | `prime-agent attach "$ACTIVE" --daemon-socket "$S"` | Local human-owned TTY only; excluded from the shipped v1 skill until the compound attach precondition below lands. Remote v1 excludes attach. |
| Agent-message delivery | `prime-agent send --daemon-socket "$S" --json "$TARGET" --message "$TEXT"` | Idle prompts; busy queues steering; may wake saved target. Receipt is delivered/queued, not acted/completed. Normally omit `--from`. |
| Explicit steer/follow-up | Help advertises `send --steer|--follow-up` | **Broken:** current parser rejects both. Needs a supported public input command. |
| Rename/stop | `rename` / `stop` with exact socket + ID + JSON | `stop` archives/aborts/cascades the root tree and schedules; no per-target confirmation. |
| Interactive new/resume/fork | ordinary launcher with `--daemon-socket`, `--resume <path-or-id>`, `--fork <path-or-id>` | Current local human convenience only; noninteractive v1 uses public create/resume/fork receipts. Bare resume is rejected despite stale docs. |
| Detached resident create + receipt | Internal `create` handler/protocol exists | No supported public command. Add one rather than shipping a script/harness. |
| Safe multiline/hostile payload | Shell argv only | Add stdin input; do not rely on nested SSH quoting. |
| Session/extension command inventory | Protocol/connection `get_commands` exists; old internal adapter is not public | Add a narrow public read command before allowing headless command-shaped input. TUI-only `/new`/`!` behavior remains attached-UI-only. |
| Literal extension UI wait | Persistent attached events know it | One-shot list has no pending-request count. Add a safe count; never auto-answer. |
| AIM bound account in list | Agent connection exposes labels-only binding | Session list does not expose configured-vs-bound labels. Add labels-only summary fields; never fingerprints. |

### Status model

The skill must project a structured record, not a single synthesized enum:

1. **Universe:** `current|stale|unreachable|orphan-file`, socket, default flag, build/protocol/schema/executable.
2. **Worker:** `starting|ready|recovering|failed`, PID only as diagnostic.
3. **Persistence/residency:** `draft|live|archived`; resident active ID versus saved-only inactive row.
4. **Host activity evidence:** streaming, tools, bash, compaction, retry, active session, heartbeat/cron, and descendant activity.
5. **Action state:** exact unfinished count; queue count; steering/follow-up previews only when payload access is authorized; active action kind/phase.
6. **RLM state:** root/subagent, depth, explicit parent links, child ID/node, initial run status where available, reply-since-task, running descendants.
7. **Task verdict:** `needs_input|completed` only when current source emits it; phrase as `needs_input verdict` / `completed verdict`, not ground truth.
8. **Extension UI:** pending count, if supported; request body and response remain attached-client-only and human-controlled.
9. **Progress/advisory:** recap/recent timestamp may support “possibly stalled,” but never authorizes intervention.

Authoritative brief-field projection:

| Brief field group | Owner source | Interpretation |
|---|---|---|
| universe socket/build/generation/protocol/schema/status | daemon hello + `DaemonInfo` | Declared runtime identity and reachability; `current` ignores build difference. |
| active/durable/root/parent/RLM IDs | `SessionSummary` plus passive RLM registry projection | Topology/target identity only; never infer from names/order. |
| lifecycle/residency/worker state | `SessionSummary` / supervisor worker summary | Persistence and host process health, separate from task progress. |
| streaming/tools/bash/compaction/retry/children | active runtime summary | Objective current host activity evidence. |
| unfinished/action/queue counts and active phase | `SessionActionSnapshot` | Work admission/ordering; brief view omits payload previews. |
| task verdict | current `taskState` emitted by session summarizer | Advisory post-turn verdict; absent means unknown/unjudged. |
| pending extension UI count | active session extension request map | Literal pending dialog count only; no prompt/options/answer authority. |
| root configured/bound labels | immutable descriptor snapshot / persisted credential binding | Labels-only root facts with distinct pre-use and post-use provenance. |

Deterministic projection tests cover idle+queued, active action, classifying root, passively reconstructed descendant, unloaded durable root, archived/closed root, failed/recovering worker, pending UI, and absent/stale task verdict. The brief serializer must not synthesize a single status field.

Required human labels and their evidence:

- **writing:** active streaming/token output;
- **executing:** current tool or bash;
- **compacting/retrying:** direct flags;
- **waiting on descendant:** root is not itself streaming/tools/bash/compacting but has running descendants;
- **queued:** actions waiting, with separate steer/follow-up counts;
- **classifying:** top-level appears `working` while no direct activity and no current task verdict;
- **needs-input verdict:** idle with current `taskState=needs_input`; this is “not confidently complete,” not proof of a pending question;
- **completed verdict:** idle with current `taskState=completed`; still not proof the user's external done criteria passed;
- **extension input pending:** nonzero pending UI request count, if the new field is present;
- **replied:** RLM child explicitly messaged its parent after the task; not the same as done;
- **inactive/archived:** saved-only or archived lifecycle;
- **unknown:** fields unavailable on an older/incompatible build.

Do not call child snapshot `activity.kind=waiting` “waiting for user.” It means an active RLM run between writing/executing events.

### Messaging/input semantics

- **Agent message (`send`):** addressed custom message. CLI-origin is broader than nuclear-family messaging and may wake a saved target. Busy delivery queues steering. A delivered receipt only means target admission/context delivery.
- **Prompt:** normal user input to an idle session. It may parse AgentSession-owned or extension commands; it is more powerful than “text only.”
- **Steer:** delivered after the current assistant turn and current tool-call batch, before the next model call. Later steering outranks queued follow-ups.
- **Follow-up:** waits until current tool and steering work is exhausted, then starts the later turn.
- **TUI command:** `/new`, `/resume`, extension commands, `!`, and `!!` are surface-specific. Never assume sending a string beginning with `/` or `!` reproduces interactive UI routing.
- **Abort/clear/resume queue:** separate operations. Plain abort does not mean clear queue or kill every child. These are advanced, explicitly authorized attached/API operations, not core v1 recipes.

### RLM topology and true child creation

- `rlm()` is the only true child-spawn primitive. It returns immediately with a handle and never returns the child's answer.
- Default max depth is 1 unless the owning session's configuration says otherwise.
- Children inherit cwd/runtime resources/model constraints and the root's pinned external credential descriptors/bindings.
- Family `agent-message` reach is parent, sibling, and direct child; roots are siblings. Operator CLI messaging is broader and must not be disguised as family identity.
- Creating a fresh root or reopening a child transcript as a top-level session does **not** create a parent edge. To spawn a real child, explicitly message/attach the intended parent and ask it to call `rlm()`, then recover the returned handle from the tree/receipt.

### AIM/account model

Separate these states:

| State | Owner | Meaning |
|---|---|---|
| Redis account record | AIM | Secret credential/account authority. Never read directly for session control. |
| Global configured descriptor label | AIM target projection | Candidate account for future roots; mutable global state, never presented as a particular root's configuration. |
| Root-captured configured label | Prime immutable root descriptor snapshot / create receipt | Labels-only account configuration actually captured at root admission, before first provider use. |
| Persisted root binding label | Prime session JSONL / safe connection snapshot | Account actually resolved for that provider in this root tree. First actual credential use pins it. |
| Child binding | Prime runtime | Inherited from the root tree; children do not independently select AIM accounts. |

AIM current-source workflow truth:

- `aim prime status`: target/projection ownership and readiness; not daemon/session inventory. Its current binding field can reflect stale receipt state rather than the validated current descriptor.
- `aim prime use ...`: selects/installs descriptor; no Prime launch; changes future-root behavior. Current working-tree code also installs/updates a session-identity extension.
- `aim prime run codex|claude`: selects/installs and synchronously launches a fixed preset. Current shorthand disables the other managed provider and also installs/updates the extension.
- plain `aim prime resume <selector>`: current working-tree implementation bypasses Redis selection and invokes Prime resume, but still installs/updates the extension and has no structured noninteractive receipt.
- `aim prime resume --rotate`: current working-tree-only Codex flow installs another descriptor and forks with a selective reset. It is not same-session resume and may leave global selection changed if launch fails.

V1 account policy after the blocking AIM corrections below:

1. Read-only account context uses only `aim prime status --brief-json` and reports validated current `configuredBinding`, stale `lastSelectedBinding`, and Prime root-captured configured versus actually bound labels as separate provenance.
2. Exact account-aware new root uses only the journaled `aim prime create --request-json -` owner surface; the skill never composes `use` + Prime create.
3. Block in AIM itself on `pathConflict`, ownership conflict, unavailable capability, or source/dist mismatch before any write/launch.
4. Preserve the other provider by default; fixed flavor `run` is not the exact-create lane.
5. Verify root-captured configured labels before sending the first prompt, then report actually bound labels only after provider use.
6. Plain exact noninteractive resume is Prime-owned and does not reselect or install AIM extension code.
7. Do not support automatic rotating resume in v1. It remains a separate explicitly requested workflow after the current working-tree path is shipped and the deferred blockers below are fixed.

### Remote transport

SSH is transport, not a Prime authorization layer.

- Require an operator-approved host/alias. Pass it as one local process argv item, reject leading `-`, NUL/control/newline, whitespace, and shell metacharacters, and never treat an option-shaped destination as a host. Do not derive hosts from AIM Redis/Tailscale metadata, scan SSH config/network, or assume a historical alias remains authorized.
- Inspect `ssh -G` and present the effective host, user, hostname, proxy/jump, identity, and remote-command settings; then preflight `hostname`, `id -un`, `printf %s "$HOME"`, `uname`, owner-safe absolute launcher paths, Node/runtime, Prime/AIM help, and writable agent/session/runtime directories without changing them.
- Remote v1 is noninteractive only: use non-PTY SSH for fixed structured status/list/input/create/receipt commands. Remote attach, TUI launch, tmux ownership, and extension UI response are excluded.
- Use absolute remote paths. Noninteractive SSH may have a different PATH; do not source arbitrary profiles or silently choose a different installed build.
- Never disable host-key checking, use sudo implicitly, or fall back from a failed remote command to local execution.
- Use only the fixed `<verb> --request-json -` remote forms; every dynamic value is typed JSON on stdin and the remote shell sees no dynamic socket, selector, cwd, name, account, model, or payload text.
- Use only the product-owned `--brief-json`/brief AIM status views for ordinary remote inventory. Raw list rows can contain first/streaming messages, queue text, spawn code, recaps, diagnostics, paths, and model errors and require separate sensitive-read authorization.
- Never hand-concatenate any dynamic value into a remote shell command.
- A dropped connection after dispatch makes the outcome uncertain. Re-read state before any retry.

## Target Architecture

### Package shape

```text
skills/prime-agent-ops/
  SKILL.md
  references/
    universe-and-session-identity.md
    discovery-and-status.md
    actions-and-receipts.md
    aim-account-context.md
    ssh-transport.md
```

No `scripts/`, service, daemon, controller, socket client, host registry, generated prompt library, or `agents/openai.yaml` in v1. Add UI metadata only after a concrete product UI need appears.

### `SKILL.md` responsibilities

Keep the runtime contract concise and command-first:

1. Trigger and anti-cases.
2. Read and apply `../_shared/agent-orchestration-policy.md` before creating, resuming, replacing, or coordinating a model session; use `$prompt-authoring` on the actual populated brief/resume delta while preserving caller conjecture as challengeable context.
3. Establish approved host/UID and requested operation.
4. Inspect installed help/capabilities; do not assume checkout source equals installed or running code.
5. Discover all visible universes, then query exact sockets.
6. Resolve compound resident/durable identity and report ambiguity.
7. Interpret layered status; never flatten idle/needs-input/waiting.
8. Authorization rules and observe-act-verify loop.
9. Choose the correct action lane: family message, agent message, prompt, steer, follow-up, attached UI, new root, exact resume, fork, true child, or AIM-assisted new root.
10. Preserve exact user text when verbatim relay is requested; use `$prompt-authoring` for a newly created/resumed agent brief or material role/scope/success-bar reframe, while keeping conjecture challengeable under the shared policy.
11. Return an inventory report for discovery or a singular mutation receipt for one action; never force multi-universe state into a fake target.
12. Reference map.

### Reference responsibilities

`universe-and-session-identity.md`

- supervisor/worker/root/RLM topology;
- runtime identity and source/dist/build/socket distinctions;
- resident versus durable identity;
- explicit tree edges and durable deduplication;
- same-UID trust boundary and coverage limits;
- public versus SDK versus private surfaces.

`discovery-and-status.md`

- local/SSH read-only preflight;
- command-first `status --json` and per-socket `list` flows;
- product-owned content-free JSON views and their exact key allowlists;
- tree reconstruction and orphan/conflict handling;
- layered status model and labels;
- worker/protocol/schema incompatibility and partial inventory;
- output table examples with synthetic identifiers only.

`actions-and-receipts.md`

- exact authorization/revalidation flow;
- message/prompt/steer/follow-up/attach semantics;
- new/resume/fork/true-child decisions and continuation handles;
- destructive boundaries, uncertain results, verification, inventory reports, and mutation receipts.

`aim-account-context.md`

- AIM/Prime authority split;
- global configured, root-captured configured, and actually bound state;
- safe AIM brief status, journaled account-aware create, exact Prime resume, and v1 rotation exclusion;
- extension-install, path-conflict, cross-provider, and source/dist side effects.

`ssh-transport.md`

- approved host and effective `ssh -G` verification;
- fixed remote command plus per-verb structured JSON stdin;
- noninteractive-only remote ownership and the explicit attach/TUI exclusion;
- stdout/stderr/uncertainty/no-local-fallback rules and hostile-value fixtures.

### Runtime decision procedure

1. **Route:** if current-family APIs suffice, use them instead. If ordinary delegation is requested, route away from this skill.
2. **Scope:** identify local or explicit remote host, expected OS user/HOME, operation, payload, and whether the request itself is exact authorization.
3. **Capability:** inspect absolute launcher help/version, lane (`source|dist|installed`), runtime hello/build/schema, and AIM help only if account context is needed.
4. **Inventory:** `status --json`; keep every row and error. For every reachable socket, get resident list. When durable roots matter, also get `--all`, then deduplicate saved identities while preserving every universe provenance.
5. **Resolve:** build forest from explicit parent links; preserve orphan/cycle/duplicate errors. Resolve one exact active or durable target.
6. **Interpret:** project layered state and distinguish evidence, inference, and unknown.
7. **Authorize:** preview host, socket/build, exact identities, current status, operation, payload class, account effect, and blast radius. Ask only when the existing request is not already exact.
8. **Re-resolve:** repeat exact-socket target lookup immediately before mutation.
9. **Act once:** use the supported public command or attached UI. Never use raw protocol as an invisible fallback.
10. **Verify:** require command/receipt success, then fresh list/state/events appropriate to the requested claim. On uncertainty, inspect; do not blindly repeat.
11. **Return:** emit the receipt and remaining unknowns; do not claim task completion from delivery alone.

### Output contracts

Read-only discovery returns an **inventory report**, not a fake singular target receipt:

```yaml
scope:
  requested_hosts: [<approved host>]
  reached_hosts: [<verified host/user>]
  unreachable_hosts: [{host: <approved host>, error_code: <fixed code>}]
coverage:
  visibility: discoverable_same_uid
  exclusions: [hidden_client_owned, other_uid, undiscoverable_stopped_custom_socket, unexposed_historical_descendants]
universes:
  - host: <verified host>
    socket: <exact operator locator>
    build_id: <declared runtime identity>
    daemon_generation: <exact>
    protocol_schema: <exact>
    launcher_lane: source | dist | installed | unknown
    status: current | stale | unreachable | orphan-file
    errors: [<fixed structured code>]
    roots:
      - active_session_id: <exact or null>
        session_id: <exact>
        runtime_kind: top-level
        state_evidence: <layered content-free summary>
        descendants: [<explicit edge rows>]
unresolved_edges: []
durable_duplicates: [{session_id: <exact>, observed_in: [<universe refs>]}]
unknowns: []
```

A state-changing operation returns one **mutation receipt**:

```yaml
scope:
  host: <verified-host>
  os_user: <verified-user>
universe:
  socket: <exact>
  expected_build_id: <exact>
  expected_daemon_generation: <exact>
precondition:
  kind: live_target | saved_target | cold_create | resume_or_fork
  expected_active_session_id: <exact | null | not_applicable>
  expected_session_id: <exact | not_applicable>
  expected_session_file: <canonical path only when required>
target_before: <live/saved target card | null for cold_create>
source_target: <exact durable source card for resume/fork | null otherwise>
action:
  kind: message | prompt | steer | follow_up | attach | create | resume | fork | spawn_child | rename | stop
  authorization_source: <user request or explicit confirmation>
  payload: verbatim | shaped_brief | omitted
result:
  command_status: accepted | rejected | uncertain
  action_id: <exact or null>
  disposition: created | reused | forked | queued | started | not_applicable
  delivery_status: delivered | queued | not_applicable | unknown
  execution_status: not_started | started | action_completed | failed | unknown
  target_after: <new/fresh exact identities and safe account state | null on rejected create>
  continuation: <exact handle/command>
unknowns: []
```

`action_completed` is intentionally narrower than “the user's outcome is done.” Task-specific proof remains separate.

## Blocking Source Corrections Before Full Skill Claims

These are small owner-surface fixes, not a new harness.

### 1. Make source/dist runtime identity truthful

Current `prime-agent.sh` computes a dirty-source build ID before selecting `--dist`, so an older bundle can inherit a source-looking build/socket identity. This can make capability and universe reports misleading and can collide source and dist lanes.

Change:

- decide source versus dist lane before assigning build identity;
- source lane keeps a full tracked+untracked source fingerprint;
- dist lane uses its embedded release/bundle identity or a fingerprint of the actual bundle, never the source fingerprint;
- hello/status expose launcher/entrypoint/lane truth;
- source and dist can coexist on distinct implicit sockets when code differs.

Proof:

- dirty source + unchanged dist produce distinct build IDs/sockets;
- `status --json` reports the actual executed lane and capability schema;
- AIM `run`/plain resume using `--dist` cannot masquerade as current source.

### 2. Add a supported arbitrary-target input command

Add a public `input` owner surface rather than repairing stale help by overloading agent-message semantics:

```text
prime-agent input <agent> [--prompt | --steer | --follow-up]
  (--message <text> | --message-file -) [--wait [--wait-timeout-ms <ms>]]
  [--json] [--daemon-socket <path>]
```

Contract:

- command-first placement, exact socket, exact selector resolution;
- default prompt is allowed only when target is idle/admissible; busy target fails and tells the caller to choose steer or follow-up;
- steer and follow-up preserve current AgentSession timing and command-parsing behavior;
- `--message-file -` reads exact stdin bytes and is mutually exclusive with argv text;
- default returns after server admission with `actionId`, `accepted`, and `disposition`; it never waits for or implies task completion;
- explicit `--wait` waits for that exact action ticket to finish, with no default deadline; optional `--wait-timeout-ms` returns `wait_timed_out` plus the still-live action identity rather than cancelling or replaying it;
- a completed action receipt proves the Prime turn/action finished, not that external done criteria passed;
- no implicit `/`/`!` TUI routing;
- JSON returns command ID, exact active+expected durable target, requested mode, admission/disposition, optional wait result, and structured error info;
- existing `send` remains the addressed agent-message lane; remove its unsupported `--steer|--follow-up` help text and document `--message`/`--` accurately.

Add a narrow read-only inventory command backed by the existing connection API:

```text
prime-agent commands <agent> --brief-json [--daemon-socket <path>]
```

The ordinary brief response returns only a validated bounded invocation/registered name and source kind enum for the exact active+durable target. It omits free-form description, argument hint, source path/info, and arbitrary metadata; those fields are a separate explicitly authorized sensitive read and remain untrusted, not command guidance. Exact-key/canary tests place hostile secrets/instructions inside allowed source metadata and prove they do not enter the brief response. The skill must inspect the brief inventory before submitting command-shaped prompt input, must treat the command's underlying mutation as separately authorized, and must not claim this reproduces TUI-local `/new`, `/resume`, `/fork`, `!`, or `!!` routing. Commands that require extension UI remain interactive-only in v1.

### 3. Add public resident-root creation with a JSON receipt

Expose the existing supported daemon create owner logic as a public command:

```text
prime-agent create [--name <name>] [--cwd <dir>] [session runtime options]
  [--resume-session-id <full-id> --resume-session-file <canonical-file>
   | --fork-session-id <full-id> --fork-session-file <canonical-file>]
  [--json] [--daemon-socket <path>]
```

Contract:

- on an absent exact socket, uses a new create-specific **non-replacing** supervisor ensure policy built from Prime's owner/lease primitives, then creates a non-client-owned resident root; it never uses hidden process glue;
- this path must not call the current interactive stale-replacement helper: after an initial absent probe it acquires the socket launch lease, re-probes race-safely, starts only when still absent, and otherwise returns the observed owner;
- if the exact socket is occupied by any reachable incompatible/stale owner, fails without shutdown, replacement, cleanup, reap, or cross-build fallback—even when that owner is idle;
- accepts an explicit allowlist of session configuration (`cwd`, session directory, provider/model/thinking/service tier, goal, RLM depth, tool/capability policy); rejects API keys, `--no-session`, process/background/foreground flags, and unknown launcher/internal options;
- new create returns `disposition: created` with full active/durable identity and stays listable/attachable after the CLI client disconnects;
- exact resume requires the full `(sessionId, canonical sessionFile)` tuple for a top-level root; server-side catalog resolution compares both immediately before lease/admission and rejects copied/moved duplicates, ID/path mismatch, path swap, or ambiguity;
- resume ignores caller cwd as an ownership decision, preserves the same durable tuple, and never opens an interactive cross-project fork prompt;
- if that exact tuple is already resident on the selected socket, returns it idempotently as `disposition: reused` with no new worker/transcript; if another universe owns the lease, returns structured `session_already_active` and performs no mutation;
- exact fork requires the same full source tuple, creates a new durable root with the source untouched, and returns `disposition: forked`; ordinary credential bindings copy, while rotation/reset remains out of v1;
- `--continue`, names, partial IDs, and suffixes are excluded from the noninteractive exact lifecycle lane;
- no automatic prompt; seed a created/reused/forked root through the separate `input` command so lifecycle and prompt receipts stay distinct;
- no TUI, hidden tmux, print/RPC owner, or controller is required;
- the receipt includes root-captured configured credential labels; actual binding appears only after first provider use.

### 4. Add strict structured-stdin forms for remote operations

Arbitrary values other than the prompt still cross an SSH remote shell if the skill builds ordinary argv text. Stdin-safe prompt payload alone is insufficient.

For every in-scope public verb with dynamic values (`list`, `input`, `commands`, `create`, `send`, `rename`, and `stop`), add an operation-specific form:

```text
prime-agent <verb> --request-json -
```

Contract:

- stdin is one bounded JSON document validated against that verb's exact schema; unknown keys, wrong types, control characters in identifiers, and oversize values fail before daemon dispatch;
- all dynamic socket, active/durable identity, cwd, name, model/provider, account expectation, mode, and payload values live in the document, not the remote command string;
- stdout is one typed JSON response; stderr uses fixed value-free errors and never echoes the request;
- the remote command contains only a preapproved absolute launcher path, one allowlisted verb, and the fixed `--request-json -` tokens;
- the skill checks `ssh -G` and presents the effective host, user, hostname, proxy/jump/remote-command settings before the first mutation; SSH config is never treated as self-authenticating user intent;
- the approved launcher path must be an owner-safe absolute path matching a strict no-shell-metacharacter policy. Otherwise remote noninteractive operation is unsupported until the owner surface supplies a safe path;
- connection failure never falls back locally. A disconnect after dispatch yields `uncertain` and triggers observation, not replay.

This is deterministic parsing in the existing public CLI, not a generic daemon-command tunnel. Each verb keeps its own authorization and capability contract; there is no arbitrary command type or raw protocol envelope.

### 5. Expose safe status details instead of parsing sensitive files

Add a product-owned, versioned content-free view:

```text
prime-agent list [--all] --brief-json [--daemon-socket <path>]
```

The default response has an exact tested key allowlist: schema version; active/durable IDs; explicit parent/RLM IDs and depth; lifecycle/activity/task verdict; worker state; runtime flags; content-free action/queue/client/message counts; and timestamps. It omits `sessionName`, `cwd`, `sessionFile`, free-form account labels, and every message/content field.

A separate `--include-locators` sensitive-read flag may add bounded quoted `sessionName`, `cwd`, and canonical `sessionFile` only when the user's inventory/resume request explicitly authorizes those locators. `--include-account-labels` similarly gates provider/source/binding labels. These typed variants still never include messages, streaming text, prompt/queue previews, spawn code, recaps, diagnostics text, model fallback text, tool data, environment, or arbitrary future `SessionSummary` additions. Every returned string is length/control-character bounded, visibly quoted, and treated as untrusted display data—never instructions or argv. Canary tests place secrets/instructions inside locator/account/free-form raw fields and prove the default view omits them; sensitive variants prove only the explicitly enabled fixed keys can appear.

Extend `SessionSummary` and saved-session scanning with optional additive owner facts used by the brief projection:

- `configuredCredentialBindings: [{provider, source, binding}]` — public labels-only projection of descriptors captured immutably at root admission; the session privately persists the expected descriptor identity/fingerprint so pre-use resume cannot silently recapture a same-label replacement;
- `credentialBindings: [{provider, source, binding}]` — persisted actually **bound** labels after provider use;
- `pendingExtensionUiRequestCount` for active runtimes;
- retain exact queue/action counts but omit their text previews from the brief view.

Prime reports only its root-captured configured and actually bound session facts. It never joins against mutable current AIM target state or exposes identity/value fingerprints or credential versions.

The brief serializer must construct a new typed object rather than destructuring/removing known-dangerous fields. Exact-key tests seed hostile/additive fields and fail if any unallowlisted key or value crosses the boundary. Raw `list --json` is a separate sensitive-read lane.

Do **not** invent a unified waiting status. Do not expose request payloads, queue text, prompt text, fingerprints, or helper material merely to support the skill.

### 6. Fix public option/contract drift

- Make public option placement and JSON shapes explicit in help/tests.
- Correct bare-resume docs, `status` versus removed `ps`, protocol version drift, and machine-wide shutdown blast radius.
- Keep `doctor --fix` and shutdown out of the skill's normal action set.

### 7. Add server-checked compound target preconditions

A root can keep the same `activeSessionId` while `/new`, resume, fork, or another runtime replacement changes its durable transcript. A list-then-mutate loop that supplies only the active handle can therefore hit a different session even when it revalidated moments earlier.

The local sensitive-read form becomes:

```text
prime-agent attach <active-id> --expected-build-id <id> --expected-daemon-generation <generation> \
  --expected-session-id <full-id> --expected-session-file <canonical-file> \
  --daemon-socket <path>
```

Change:

- expose the daemon generation from hello in machine status/brief inventory and require every new CLI connection to carry `expectedBuildId` and `expectedDaemonGeneration`;
- define four typed target preconditions: `live_target` = full active + durable identity; `saved_target` = exact durable identity + `expectedActiveSessionId:null`; `cold_create` = expected universe with `targetBefore:null`; `resume_or_fork` = exact durable `(sessionId, canonical sessionFile)` `sourceTarget` plus expected universe;
- after socket/hello and target/source resolution and immediately before admission, compare the relevant lifecycle precondition; fail with structured `universe_changed`, `target_session_changed`, `target_became_active`, or `source_changed` responses on mismatch;
- return a newly assigned active ID only in `target_after` for saved wake/create, and keep source versus result identities separate for resume/fork;
- add a local-only attach form carrying `expectedBuildId`, `expectedDaemonGeneration`, `expectedActiveSessionId`, `expectedSessionId`, and canonical `expectedSessionFile`; the daemon verifies all fields **before** registering the client or emitting any snapshot/transcript event;
- bind the attached client subscription to that durable tuple: if the runtime behind the active ID is replaced later, emit only structured `target_session_changed` and disconnect before any replacement snapshot/message can cross the connection;
- include expected and observed identities in the redacted receipt;
- test runtime replacement between preflight and action for input, send, rename, stop, attach, and any later live mutation; attach tests prove no snapshot/transcript is emitted before the compound check and no replacement-session content is emitted after a bound subscription changes; separately test saved wake racing active admission, cold create on an absent/replaced universe, and resume/fork source changes.

This is the server-side close of the observe/action time-of-check gap. Repeated client-side polling alone is not sufficient.

### 8. Fail closed on same-label identity rebinding

Current external-auth source can allow a newly installed descriptor with the same label but a different expected identity fingerprint to override an old root's saved identity. Before the skill claims identity-stable exact resume:

- append a root-admission `credential_configuration` record for every managed provider before returning create success; it contains public provider/source/binding plus the private non-secret expected identity fingerprint, which never enters public output;
- exact resume restores that record for every still-unbound provider instead of recapturing mutable global AIM state; any later persisted binding becomes the stronger authority;
- the root's private admission-time configured identity and any later bound identity win on resume even when the label string matches;
- a same-label/different-identity descriptor produces an explicit `identity_conflict` before first use and after binding, never silent replacement;
- ordinary fork copies configuration and binding records; selective reset removes both records only for the explicitly reset provider; true children inherit the root's immutable configuration/binding and never select independently;
- public output remains labels-only; fix enforcement server-side rather than exposing fingerprints;
- cover initial external resolution, rejected-token reacquisition, resume, ordinary fork, selective-reset fork, and descendant inheritance tests;
- add the exact regression: journaled create → no provider use → root stop/eviction → global descriptor changes (including same label/new identity) → exact resume restores the original configuration or fails `identity_conflict`, and active/saved brief views retain the original configured label.

## Blocking AIM Owner-Surface Corrections For V1 Account Context

The skill must not paper over these with prompt preflight. They are owner-command invariants required before any AIM-assisted v1 action.

### Decouple session-identity extension installation

Current working-tree `aim prime use`, `run`, and even plain `resume` call `ensureHarnessSessionIdentityExtension`, which creates or replaces executable extension code. That side effect is not authorized by an account-selection or exact-resume request.

Change:

- remove implicit extension installation/update from `use`, `run`, `resume`, status, and the new create lane;
- expose a separate explicit `aim prime identity install|status` operation with its own effect/receipt and authorization;
- the skill never invokes identity installation as a prerequisite for session control.

### Add a safe truthful AIM status view

Add:

```text
aim prime status --brief-json
```

The fixed typed response reports coordination availability, managed/installed/owned/conflict booleans, `pathConflict`, current validated descriptor `configuredBinding`, and persisted `lastSelectedBinding` as separate labels. `configuredBinding` is derived from the current validated AIM descriptor, not copied from possibly stale local receipt state. It omits auth/backup/resolved/persisted paths, fingerprints, provider IDs, records, helper material, and arbitrary additive fields.

Tests cover missing local state, recovered descriptor, current-descriptor mismatch, ownership conflict, and exact-key/canary exclusion. The skill never parses `auth.json` or raw AIM status locally or remotely.

### Fail closed on target-path conflict in the owner command

Before any descriptor write or launch, AIM must either prove the persisted owner and current `PRIME_AGENT_CODING_AGENT_DIR` agree or fail with `path_conflict`. The chosen v1 policy is **block**, not silently launch against one path while writing another. Tests prove `use`, `create`, and any retained `run` path perform no auth write, extension write, selection change, or launch on conflict.

### Add one race-free journaled account-aware root creation transaction

Do not compose `aim prime use` and `prime-agent create` in the skill. Add one AIM owner surface plus read-only recovery lookup:

```text
aim prime create --request-json -
aim prime create status --request-json -
```

The strict v1 request is `{schemaVersion:1, operationId, targetAgentDir, provider, label, preserveOtherProvider:true, prime:{daemonSocket,cwd,name?,model?}}`; reject unknown keys and do not accept an arbitrary config bag or model prompt. AIM transforms it into Prime's typed stdin request `{schemaVersion:1, operationId, expectedAgentDir, daemonSocket, cwd, name?, provider, model?, expectedCredentialDescriptor:{provider,source:"aimgr",binding,expectedIdentityFingerprint}}`. The fingerprint is private input and never appears in output. Prime returns `{schemaVersion, operationId, disposition, universe, targetBefore:null, sourceTarget:null, targetAfter:{activeSessionId,sessionId,sessionFile,configuredCredentialBindings}}`; AIM wraps it with transaction/projection/rollback state. AIM persists a pending transition journal containing the prior/new descriptor receipts and Prime create command identity before the first write.

Add a distinct outer **Prime-target selection/create mutex** keyed by the owned target path. Every AIM target mutation (`use`, create, uninstall/repair, and any retained run/rotate path) must acquire it. This is not the short-lived `auth.json` file lock shared with Prime. AIM holds the outer mutex across the transaction, but each descriptor read/write acquires and releases the existing file lock before Prime starts, so Prime can take its own file lock and reload without deadlock. Non-AIM/manual descriptor drift is still caught by Prime's expected descriptor precondition.

Then AIM:

1. validates path/ownership, selector, launcher/source-dist compatibility, and account eligibility before mutation;
2. acquires the outer mutex, writes the pending journal, and selects/installs the descriptor under only the short-lived auth-file lock while preserving omitted providers;
3. releases the auth-file lock, keeps the outer mutex, and invokes Prime's public resident `create` with the same stable operation identity and a private expected descriptor label+identity precondition;
4. Prime independently acquires/reads the auth file, persists the root credential configuration and create result under that operation identity, and acknowledges admission;
5. AIM marks the transaction committed and releases the outer mutex only after it has the root's labels-only `configuredCredentialBindings` plus active/durable identity;
6. repeated status/recovery reads the journal and Prime result; it never replays an uncertain create under a new identity.

**Commit point and failure table:**

| Window | Required recovery/result |
|---|---|
| before descriptor write | `aborted_no_effect`; prior projection unchanged; retry requires a new explicit action or exact same idempotent operation ID. |
| descriptor written, root not admitted | while locked/recovering, restore the exact prior descriptor if the transition receipt still matches; finalize `rolled_back_no_root`. |
| root admitted/configuration persisted, AIM not finalized | observe the Prime operation result and finalize **committed**; never roll back the descriptor out from under the admitted root. |
| committed but response lost | `create status --request-json -` accepts the bounded `operationId` in typed stdin and returns the stored root/projection receipt; caller observes rather than replaying. |
| safe rollback cannot be proven or fails | `partial_effect` names the remaining global projection state, blocks automatic retry, and requires a separate human-authorized repair. |
| journal/descriptor/root evidence conflicts | `conflict_uncertain`; no retry, rollback, prompt, or cleanup is automatic. |

The committed effect intentionally leaves the selected global future-root projection in place and the receipt says so. The prompt is sent only after a committed transaction receipt, through the separate Prime `input` action. First provider use later adds `credentialBindings`; the receipt therefore distinguishes root-captured **configured** labels from actually **bound** labels without joining against mutable global status.

Crash-window tests cover every row, including lost response after root admission, process death during rollback, descriptor drift/tamper, and exact same-operation status recovery. Concurrency tests prove Prime can acquire/read its auth lock while the outer mutex is held, concurrent AIM target selection blocks, and manual drift fails the expected-descriptor check.

`aim prime run codex|claude` is not the skill's exact account-aware lane: it uses fixed auto presets and currently disables the other provider. Plain `aim prime use` remains an explicitly authorized future-root projection operation, not part of exact create.

### Exclude AIM plain resume from the noninteractive v1 lane

Current AIM resume has inherited TTY, no structured receipt, source/dist coupling, cross-cwd interactive fork behavior, and implicit extension installation. The skill uses the exact Prime resume contract defined below. AIM resume may remain a human interactive convenience after its side effects are separately authorized, but it is not the machine-control owner surface.

## Deferred AIM Hardening Before Rotating-Resume Support

Do not block read-only AIM context or explicit new-root selection on these, but keep `resume --rotate` out of v1 until all are resolved:

1. Resolve the source root's persisted binding first; rotation must avoid that label, not merely the currently installed global descriptor.
2. Validate selector, path, launcher, source capability, and account eligibility before mutating the global target descriptor, or provide rollback with an exact receipt.
3. Block persisted-versus-resolved `PRIME_AGENT_CODING_AGENT_DIR` conflicts and always launch against the owned path.
4. Decide whether `run codex|claude` should preserve the other managed provider rather than uninstall it.
5. Co-version AIM helper, Prime source, Prime dist, and session-identity extension; add a non-secret compatibility preflight.
6. Publish/commit the current working-tree resume/session-identity/reset behavior before the skill treats it as installed capability.

## Authorization And Safety Matrix

| Operation | Default classification | Required authorization |
|---|---|---|
| help/version, `status --json`, product-owned `list --brief-json`, AIM brief status | Read-only | Approved host/user scope. |
| detailed queue previews, recaps, transcript/messages/context, attach | Sensitive read / client presence | Exact target and explicit need for content/attach. |
| agent message, prompt, steer, follow-up | Model-work mutation | Exact host/universe/target/action/payload; the user's exact action-shaped request is sufficient. |
| create, exact resume, fork, true-child spawn | Lifecycle/model-work mutation | Exact host/cwd/continuation/account intent and role/return contract under shared orchestration policy. |
| rename, model/thinking/queue setting | State mutation | Exact target and requested value. |
| AIM journaled `prime create` | Locked credential projection + exact root admission | Exact provider/account/preserve-other policy, target path, captured-descriptor precondition, and disclosed rollback/partial-effect receipt. |
| stop/abort/clear/kill/delete/archive/cancel child | Destructive | Fresh explicit exact target + blast radius; no inference from “stuck.” |
| AIM use/run, identity-extension install, rotate/rebind/uninstall/native-auth replacement/login/Redis mutation | Credential/account/extension mutation | Separate explicit request; excluded from the normal exact v1 lanes. |
| retry/restart/update/doctor fix/shutdown/force/signals/manual PID/socket/file cleanup | Broad/destructive | Separate exact request and current blast radius; never a discovery fallback. |
| shell/extension/slash command that can mutate external state | Delegated high-risk action | The underlying exact external action must itself be authorized; sending through another agent is not a bypass. |

## Depth-First Phase Plan

### Phase 0 — Freeze versioned contracts and protect user work

**Goal:** establish the exact implementation baseline without touching live runtimes or overwriting current uncommitted work.

**Work:**

- Record commit/status/diff snapshots for `prime-agent`, `aimgr`, and `arch_skill`.
- Re-read installed/source/dist help and source contracts in an isolated environment; do not run status/list against default live sockets.
- Convert the current capability table in this plan into an implementation checklist with four states: shipped public, current working-tree only, internal/exported, unsupported.
- Confirm the final slug `prime-agent-ops`, supported installer surfaces, and exact public `input`/`create` syntax.
- Coordinate with owners of the dirty Prime/AIM work before editing overlapping files; never clean, restore, or rewrite their changes.

**Verification:**

- Source diff inventory reviewed by the implementer and Prime/AIM owner.
- No command log contains a default live socket, real account label, credential path, or remote host operation.

**Exit criteria:**

- Baseline and overlap ownership are explicit.
- No unresolved ambiguity remains in the public command/API names or JSON receipt contract.

**Rollback:** n/a; read-only planning step.

### Phase 1 — Close the minimum Prime public-contract gaps

**Goal:** make every core skill promise achievable through a supported host-local CLI without a hidden protocol runner.

**Work:**

- Correct source/dist runtime build identity.
- Add public `input` with prompt/steer/follow-up and `--message-file -`.
- Add public read-only `commands` inventory for exact targets.
- Add public resident-root `create` with JSON receipt.
- Add strict per-verb `--request-json -` schemas for every noninteractive remote operation.
- Add the versioned `list --brief-json` typed allowlist plus safe bound-label and pending-UI owner facts.
- Add server-checked active+durable target preconditions to every supported per-session mutation.
- Fix public help/docs contradictions and option ordering.
- Make same-label external-auth resolution and rejection/reacquisition fail closed.
- Decouple AIM session-identity extension installation into its own explicit operation.
- Add AIM `prime status --brief-json`, path-conflict fail-close, and journaled `prime create --request-json -` with root descriptor-capture precondition and preserve-other-provider default.
- Exclude AIM plain/rotating resume from the noninteractive v1 lane.
- For the user-authorized disposable `aim prime run codex` validation only, allow an exact `--codex <label>` plus a strict post-`--` allowlist of `--no-env`, `--offline`, `--daemon-socket <absolute>`, and `--session-dir <absolute>`; exact selection skips live usage probing. This remains a human/test convenience, not the skill's machine-control owner lane.
- Update capability/schema only as required by additive command/field changes; preserve old-daemon compatibility through explicit capability errors, not fallback behavior.

**Deterministic tests:**

- Public routing rejects removed `daemon` commands and accepts only the new public forms.
- Every structured-stdin verb rejects unknown/oversize/ill-typed fields; hostile values in socket, IDs, cwd, name, provider/model/account, mode, and payload never enter the remote command string or value-bearing stderr.
- Hostile input bytes: leading dashes, quotes, dollar/command substitutions, backticks, Unicode, and newlines arrive exactly through stdin; no template/shell interpretation.
- Busy prompt fails with an explicit mode requirement; steer and follow-up queue in the documented order; default input returns admission, `--wait` follows the exact action ticket, timeout leaves it live, and no receipt equates turn completion with task success.
- Brief command inventory exposes only bounded invocation name + source enum; canaries in descriptions/hints/source info stay out, and command-shaped input rejects unknown/TUI-only commands rather than guessing.
- Create's non-replacing ensure starts an absent exact socket under the launch lease, re-probes the race, leaves the resident root listable after client disconnect, and proves an idle incompatible/stale daemon is neither stopped, replaced, nor cleaned.
- Create returns active/durable identities; exact resume preserves the full durable tuple or returns `reused`, exact fork returns a new durable tuple, and copied/moved/path-swapped/ID-mismatched/already-active/ambiguous/cross-project cases are structured with no interactive prompt.
- Live mutations fail after stable-active/durable replacement; compound local attach emits no precheck or post-replacement transcript content; saved wake requires expected active `null` and reports the new active ID only afterward; cold create has `target_before:null`; resume/fork keep exact source and result identities distinct.
- Source/dist dirty-build identity differs correctly.
- Brief JSON exact-key tests exclude every content-bearing or additive hostile raw-summary field; locator strings are bounded and displayed as untrusted data.
- Root-captured configured versus actually bound labels never expose fingerprints; same-label identity conflict fails closed on initial resolution and rejected-token reacquisition.
- AIM brief status derives current configured binding from the validated descriptor and distinguishes stale last-selection state; no path/backup/raw status keys escape.
- AIM path conflict produces no auth/extension write or launch; account-aware create holds the owner lock through Prime descriptor capture, preserves the other provider, and returns structured rollback/partial-effect receipts.
- Current AIM use/run/resume no longer install executable session-identity extension code implicitly.
- Pending extension UI count appears/disappears without exposing request payload.

**Verification commands (from the Prime repo's native environment):**

```bash
cd packages/coding-agent
npx tsx ../../node_modules/vitest/dist/cli.js --run \
  test/public-command.test.ts \
  test/daemon-command.test.ts \
  test/daemon-ps.test.ts \
  test/daemon-session-list.test.ts \
  test/daemon-protocol.test.ts \
  test/agent-connection-daemon.test.ts \
  test/source-build-id.test.ts \
  test/external-credential-session.test.ts \
  test/credential-binding-reset.test.ts \
  test/daemon-supervisor-process.test.ts
```

Run every created/modified Prime test file through that exact package-root Vitest form and iterate until it passes. Then run the Prime repo-required `npm run check` with full output from an isolated/owner-approved worktree; it rewrites formatting, so never run it across unrelated user changes. Prime repo rules prohibit `npm test` and `npm run build`. Built-dist/source identity proof therefore runs only through the exact owner-approved release/bundle lane established in Phase 0; record that command before implementation rather than inventing one.

AIM targeted proof, from its repo-native environment:

```bash
node --test test/pi/prime-target.test.js test/pi/session-identity-extension.test.js
npm run lint
```

Add/run the exact new AIM test files for brief status, path-conflict fail-close, journaled create, extension decoupling, and partial-effect rollback. No test may use real Redis records, provider accounts, auth files, extensions, or launchers.

**Exit criteria:**

- Current public help, implementation, tests, README/usage, protocol schema, and actual built dist agree.
- No core action requires the removed CLI or a raw socket client.

**Rollback:** revert only the isolated Prime feature branch/commit; current public commands remain unchanged.

### Phase 2 — Author the prompt-first skill package

**Goal:** teach the source-truth decision procedure with progressive disclosure and no workflow-owning code.

**Work:**

- Create `skills/prime-agent-ops/SKILL.md` with trigger boundaries, an explicit “read and apply” shared-policy instruction, the discover/resolve/authorize/act/verify spine, concise authorization/return rules, and a reference router. Keep the detailed matrix and schemas in the owning references.
- Create the five reference files with the responsibilities listed above.
- Use synthetic hosts, sockets, IDs, labels, cwd values, and prompts in examples.
- Teach command-first option ordering and capability gating. Older runtimes missing `input`/`create` must produce an explicit limitation or attached-UI alternative.
- Teach the product-owned brief JSON views and structured-stdin SSH lane. Never ask a cold agent to author a security allowlist. Do not ship a projector, SSH wrapper, client, controller, or session registry.
- Keep raw protocol, worker descriptors, generic bash/delete/import/export, and automatic extension UI response out of the skill.

**Verification:**

```bash
npx skills check
```

Manual doctrine review against `$skill-authoring` and `$prompt-authoring`:

- frontmatter name matches folder;
- description is trigger-rich and under 1,024 characters;
- SKILL body is concise and references carry detail;
- relative paths resolve;
- no duplicated shared orchestration doctrine;
- no inflexible heuristics or wording-lock tests;
- examples use only current public commands.

Run cold trigger and execution evals on **each runtime before adding it to an install inventory**:

- positives: each canonical ask plus at least one natural paraphrase;
- nearest-peer negatives: current-family message/observe, ordinary delegation, external agent delegation, offline history, generic SSH, AIM account administration, and Prime daemon development;
- ambiguous: “start another agent,” “resume my agent,” and “message the latest session” must clarify/route rather than mutate;
- execution: give the evaluator only the user ask, installed candidate package, and synthetic fixture surface—not this populated plan, expected command map, or answer key;
- require exact inventory/status output, an input/create journey, an account-context journey, a remote structured-stdin journey, and a destructive-refusal journey for agents/Codex, Hermes, Claude, and Gemini wherever their owning inventory would install the skill.

**Exit criteria:**

- A cold agent can answer the three canonical asks and route every anti-case correctly without answer leakage.
- Every claimed runtime passes package, trigger, execution, and validation-integrity gates before Makefile inventory entry.
- No script/service/runtime dependency exists.

**Rollback:** delete only the new skill package.

### Phase 3 — Integrate routing and install surfaces

**Goal:** make the skill discoverable to supported agents without changing unrelated install behavior.

**Work:**

- Add `prime-agent-ops` only to inventories whose full consumer set passed cold package/trigger/execution/integrity evals. `SKILLS` currently feeds agents/Codex **and Hermes**, so both must pass before one shared entry is added; otherwise first split an owning Hermes inventory rather than claiming selective support. Apply the same explicit pass rule to `CLAUDE_SKILLS` and `GEMINI_SKILLS`.
- Add README inventory/install paths and a compact use example.
- Add one plain-English root `AGENTS.md` routing line distinguishing this skill from native family APIs, `$agent-delegate`, and `$agent-history`.
- Add a concise utility section to `docs/arch_skill_usage_guide.md`.
- Do not add `agents/openai.yaml` or a new shared doctrine file in v1.

**Verification:**

- Re-read edited docs and use `rg` to prove every added path/skill name exists.
- Run `npx skills check` again.
- Because install inventory changed, run `make verify_install` only with isolated temporary destinations for agents/Codex, Claude, Gemini, and Hermes. Never use the default live install paths for validation.

**Exit criteria:**

- Makefile and docs have one consistent install inventory.
- Supported runtimes receive the same prompt-first package and unsupported destinations do not.

**Rollback:** remove only the new inventory/docs entries; preserve unrelated install changes.

### Phase 4 — Disposable end-to-end validation

**Goal:** prove behavior through real isolated daemons and fake/loopback transport without touching Amir's live Prime/AIM environment.

**Fixture:**

- temporary `HOME`;
- temporary `PRIME_AGENT_CODING_AGENT_DIR` and `PRIME_AGENT_SESSION_DIR`;
- temporary `XDG_RUNTIME_DIR`;
- two explicit non-default socket paths;
- faux provider/no live credentials;
- fixture AIM records/target files only if the account lane needs integration proof;
- fake SSH executable first, optional disposable localhost/lab host second;
- canary secrets in fixture env/files for leak scans.

**Journeys:**

1. Start two isolated source/dist or explicit-socket universes with different identities; discover both exactly once.
2. Create distinct resident roots; list each socket and prove no resident cross-contamination.
3. Spawn a true RLM child through the parent; reconstruct root/child edges from public summaries.
4. Exercise direct prompt, busy steer, later follow-up, and agent-message. Verify exact payload, receipt, queue/action state, and later transcript/event only when authorized.
5. Create a root, return identities, seed its brief, detach, resume exact durable identity, and fork separately.
6. Exercise journaled AIM account-aware create: path/descriptor preconditions hold through Prime root capture, the other provider survives, no extension file changes implicitly, the root-captured configured label precedes first use, first provider use creates the bound label, exact Prime resume preserves it, and children inherit it.
7. Exercise extension UI pending count with no capable client and with an isolated attached client; never auto-confirm.
8. Rename on one exact socket. Stop an isolated child/root only after exact revalidation; prove cascade scope and other-universe survival.
9. Force worker failure/uncertain response in fixture; prove the skill reports uncertainty and observes before retry.
10. Fake SSH captures effective `ssh -G` policy, fixed non-PTY argv, structured stdin, stdout, stderr, and dispatch timing. Reject option-shaped/control-bearing destinations before `ssh -G`; test hostile host config plus spaces, apostrophes, `$HOME`, `$()`, semicolons, backticks, Unicode, leading dashes, and newlines in every dynamic request field—including AIM lost-receipt `operationId`; the remote command remains fixed, no sentinel runs, and no local fallback occurs.
11. Use only the product-owned brief views over SSH; canary scan every stdout/stderr/receipt/artifact and assert the exact key allowlists so additive raw prompt/token/fingerprint/worker fields cannot leave the target.

**Exit criteria:**

- All canonical asks pass on fixtures.
- Negative authorization tests prevent inspect→mutate escalation, ambiguous/latest selection, broad cleanup, force/shutdown, raw protocol, credential rotation, and secret relay.
- Evidence is labeled static, fixture/mock, disposable-daemon, or unproven/live-authorization-required.

**Rollback:** stop only PIDs/sockets recorded by the fixture and delete only its temp root. Refuse cleanup if ownership cannot be proven.

### Phase 5 — Cold expert and adversarial release gate

**Goal:** catch source drift, account mistakes, safety gaps, and skill bloat before publication.

**Reviewers:**

1. **Prime Agent expert:** trace every public command, option placement, JSON field, status interpretation, create/input receipt, recovery/uncertainty claim, and source/dist behavior.
2. **AIM expert:** trace Redis/descriptor ownership, configured-versus-bound account state, exact-resume behavior, new-root projection, path conflicts, and the explicit rotation exclusion.
3. **Adversarial safety reviewer:** attack host/same-UID trust, selector ambiguity, stale builds, raw JSON leakage, prompt injection, SSH quoting, hidden client-owned sessions, destructive escalation, and uncertain retries.
4. **Skill-authoring reviewer:** attack trigger overlap, always-on bulk, progressive disclosure, hidden heuristics, duplicated doctrine, and script/harness creep.

**Work:**

- Give each reviewer the populated plan, final package, relevant source diff, and validation receipts.
- Treat any unsupported command, secret-bearing output, account mutation ambiguity, source/dist mismatch, or hidden controller as blocking.
- Incorporate corrections in the smallest owner surface and rerun only affected proof plus `npx skills check`.

**Exit criteria:**

- All four reviewers return pass or only explicitly accepted non-blocking notes.
- Final docs state all coverage limits and working-tree/shipped boundaries honestly.

**Rollback:** keep the skill uninstalled/unpublished; do not weaken safety or add fallback machinery to force a pass.

## Verification Matrix

| Requirement | Static/source | Unit/fixture | Disposable daemon | Live/remote |
|---|---|---|---|---|
| All discoverable universes | CLI/source trace | status parser fixtures | two explicit sockets | unproven until exact host authorized |
| Root/RLM tree | summary/edge types | cycle/orphan/dedupe tests | real child spawn | hidden client-owned/historical limits remain |
| Detailed status | source field mapping | state classifier fixtures | active/idle/classifying/child/queue/UI cases | provider latency/stall remains advisory |
| Exact prompt/steer/follow-up | public input contract | action-order/input-byte tests | busy/idle target journey | no real provider required |
| Agent message | receipt contract | queue/rate/wake fixtures | resident and saved target | no completion claim from delivery |
| Resident create/resume/fork | public create contract | selector/lease tests | full lifecycle journey | no live session touched |
| AIM account context | safe label projection | fixture target/binding | faux first-use binding | real account/Redis excluded |
| Remote transport | SSH policy | fake SSH fixed argv/structured stdin | loopback/lab optional | approved host required; remote TTY excluded |
| Secret safety | versioned brief-schema review | exact-key/canary scan | product-owned brief output only | real-secret absolute proof not claimed |
| Install/routing | Makefile/docs review | isolated verify_install | n/a | no live install during development |

## Risks And Explicit Decisions

### Decision: skill name

Use `prime-agent-ops`. It is literal enough to trigger on Prime runtime operations, but does not imply a separate “control plane” product. `prime-agent-control` is an acceptable fallback only if routing evals show `ops` is too vague.

### Decision: no shipped helper

The mechanics already exist in Prime/AIM. A helper would own discovery, compatibility, host routing, command identities, retries, and receipts and would become the prohibited controller. Deterministic gaps belong in Prime's public CLI; judgment stays in the skill.

### Decision: no raw protocol fallback

The public socket trusts the same UID and exposes dangerous path/bash/delete/global operations. Raw protocol recipes would make every shell-capable model a generic same-UID control client and bypass the intended public owner surface. Product code may use the exported client to implement public commands; the skill does not genericize it.

### Decision: no automatic extension UI response

Extension UI requests require a persistent capable attachment; first valid response wins and another capable client may race. V1 reports a safe pending count and sends the human to an exact attached UI. It never confirms, selects, edits, or inputs automatically.

### Decision: no rotating resume in v1

The current behavior is uncommitted, source-only, mutates global target selection before launch proof, avoids the configured label rather than necessarily the source binding, and has path/source-dist coupling. Read-only account context and explicit new-root selection are enough for v1.

### Decision: no single “waiting” state

The runtime has multiple meanings: queued action, child runtime `waiting`, root waiting on a child, classifier `needs_input`, pending extension UI, idle, and classifying. The skill reports the raw axes and evidence-backed label, preserving “unknown” when the runtime cannot prove more.

## Remaining Validation Boundary

Remote v1 is deliberately noninteractive. It never claims attach, TUI/extension UI response, tmux ownership, or interactive launch over SSH. A user may separately open a human-owned terminal on the host and use Prime's local attach command, but that is outside this skill's remote automation contract.

All outcome-changing owner contracts—input admission/wait, resident cold create, exact resume/reuse, exact fork, brief projection, lifecycle-specific mutation preconditions, and journaled account-aware create—are frozen above before Phase 1 begins.

## Plan Review Gate

Four initially clean, read-only expert reviewers inspected the populated plan against current Prime/AIM source and skill doctrine. Their initial and follow-up blockers were folded into the owning contracts above. Each reviewer then re-read the relevant final text and returned **PASS**:

- Prime runtime/public CLI: PASS after structured input, non-replacing cold create, lifecycle preconditions, exact attach subscription safety, journal recovery, and approved test commands were frozen.
- AIM/external auth: PASS after truthful configured/bound status, path fail-close, extension decoupling, durable admission-time configuration, same-label enforcement, the outer target mutex, and journaled recovery were frozen.
- Skill/prompt/install design: PASS after product-owned brief projections, scheduling removal, split output contracts, lifecycle receipt variants, five progressive references, cold execution gates, and shared Hermes inventory handling were frozen.
- Adversarial security/operability: PASS after fixed structured SSH commands, remote TTY exclusion, safe default string projections, exact resume/fork tuples, auth-lock separation, and local attach transcript isolation were frozen.

This gate approves the **implementation plan**, not code that does not yet exist. Phase 4 still requires new cold reviewers to audit the implemented owner commands, package, proofs, and receipts.

## Definition Of Done

- `prime-agent-ops` is installed on approved agent surfaces with concise trigger/routing doctrine.
- Public Prime source and owner-approved built dist expose truthful source/dist identity, versioned brief JSON, per-verb structured stdin, exact input admission/wait modes, cold resident create, exact resume/reuse/fork receipts, compound universe+session preconditions, and safe binding/UI details.
- AIM exposes a safe truthful brief status, blocks path conflict before effects, never installs extension code implicitly, and owns one journaled preserve-other-provider account-aware create transaction.
- The skill uses only current public owner commands for normal work and never teaches removed/internal daemon syntax.
- Every mutation is server-bound to exact host/user/socket/build/generation plus its lifecycle-specific live, saved, cold-create, or source-target precondition and verified once.
- Status output separates all layers and never mislabels heuristic `needs_input` or child `waiting` as literal human blocking.
- Global configured, root-captured configured, and actually bound account labels are distinct; exact Prime resume preserves durable identity and binding; true children inherit; rotation remains excluded until hardened.
- Remote operation stays behind approved SSH/local-user authority with effective-config review, fixed noninteractive commands, structured stdin, no local fallback, and product-owned brief JSON output; remote TTY/attach is excluded.
- Cold package/trigger/execution/integrity evals pass before each runtime inventory entry, and disposable two-daemon, account fixture, fake-SSH, exact-key/secret-canary, and negative authorization proofs pass.
- Four cold reviewers approve the final package and receipts.
- No live daemon, session, account, credential, remote host, or installed skill surface was used as a development fixture.
