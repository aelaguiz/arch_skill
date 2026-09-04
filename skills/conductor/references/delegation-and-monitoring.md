# Delegation And Monitoring

The conductor chooses transport under
`../../_shared/agent-orchestration-policy.md`; transport does not choose the
workflow. Resolve the **worker profile** first — provider and model, thinking
level, durability, isolation, receipts — then take the cheapest lane that can
actually deliver that profile. The fleet is a profile, not a runtime: workers handle investigation,
implementation, proof, and review reading on the selected model and effort.

The cost rule is about pinning, not about transport. A native child inherits
the parent's model and thinking level unless the dispatch pins them, so an
unpinned native worker may not use the selected fleet profile. A pinned one bills its own model. Pin the profile or
take the external lane; never route bulk work to an unpinned native child.

Take the native lane when all four hold:

- **Reachable** — the fleet model is in this host's native child catalog.
- **Pinnable** — this host can set that model *and* that thinking level.
- **Durable enough** — the pin survives this run's resume pattern, which for a
  conductor means surviving up to three send-back rounds against the same
  handle.
- **No external-only benefit is load-bearing.**

Take the external lane through `$agent-delegate` when any of those fails, and
say which one. These recognizably fail it: cross-provider work from a host that
binds a child to the parent's provider, usage-limit rotation across accounts,
sessions that must outlive the parent process, required run-directory receipts,
concurrency past the host's native cap, worktree or process isolation the host
cannot give, and the `conductor terra` preset. Honor explicit user choices in
both directions.

`../../_shared/native-child-capabilities.md` holds the current per-host facts
and their sharp edges. Verify a capability against the live tool schema before
promising it.

## Dispatch And Continuation Mapping

- **Initial slice dispatch → new clean child on the selected lane.** Give it
  the plan path, log path, slice anchors, constraints, and return contract.
  On the external lane that is `$agent-delegate` `fresh-resumable` on the
  fleet model; on the native lane it is a clean child pinned to the same
  model and thinking level. Record the lane, model, thinking level, starting
  context, exact handle, and external run directory when one exists.
- **Send-back / repair → exact-child resume.** Send one bounded findings delta
  to the same native child handle or the exact external session id through its
  original transport. Never select "latest," cross runtimes, or replace the
  implementer merely because another handle is convenient.
- **Respawn → new clean replacement.** Use when the role truly needs a cold
  restart, its prior handle is lost or unhealthy under the audit caps, or its
  owner surface changed enough to invalidate the earlier view. Record why the
  replacement was necessary.
- **Requested cynical reviews → new clean children on the fleet profile.** The
  cynical review skills run only when the user asked for them, and each one
  runs as its own clean session that invokes the installed review skill itself
  against the repo. Its own native slices are expected and need no assignment:
  they bill the reviewer's own host and model, not the conductor's. The
  conductor consumes each review's findings as advisory claims under the normal
  audit machinery. Whole-skill review reading is the largest single block of
  bulk tokens in a run, so it never goes to an unpinned native child.
- **Cold verifier → new clean one-shot on the fleet profile**, final gate only.
  Independence is the feature: no conductor narrative, no resume, just
  refutation from plan, code, and the artifacts it loads itself. A whole-plan
  cold read is bulk reading, so it runs on the selected profile on whichever lane
  carries it — and a one-shot with no resume is the easiest role to pin
  natively, because no eviction can quietly re-price it. Give it the plan path,
  human baseline anchors, approved initial closure, approval anchor, and explicit
  human approvals; its findings cannot expand scope.
- **Parallel waves** are parent-owned. Use only the active host slots or
  external sessions that independent, non-overlapping slices justify. Every
  child knows that siblings may be editing the repo, must not revert unfamiliar
  changes, must not start external agents of its own, and must report actual
  conflicts with file evidence.

## Native Starting Context

Clean context is the default because the plan and conductor log already carry
the durable inputs. In Codex, every native spawn states `fork_turns` explicitly:
`"none"` for ordinary phase workers and critics, a positive count only for a
small chat-only dependency, and `"all"` only when the whole conversation is
load-bearing. Omitting it is not the same as `"none"` — the current default is
full inheritance, which is the wrong context and the wrong bill for a phase
worker. In Claude, a clean named subagent is distinct from an explicit full
conversation fork, and that fork also forces the parent's model, so it is never
the way to pin a different worker profile; a skill declared with `context: fork` is an
isolated clean subagent context, not full inheritance. In Prime Agent every
child is clean and no fork exists, so a load-bearing recent decision must be
written into the brief.

Context inheritance is separate from permissions, capabilities, filesystem
sharing, and worktree isolation. State those independently. Native clean
children commonly share the current worktree. For a read-only critic, use an
enforced read-only capability when the host exposes one, keep the no-edit
prompt rule, and have the conductor compare repository state before and after.

## Worker Identity And Profile

The worker profile is one set of values that applies on either lane: model,
thinking level, durability, isolation, and receipts. Resolve it before choosing
transport, and carry the same model and thinking level across whichever lane you
choose — the fleet is defined by that profile, not by the runtime that hosts it.

The user supplies the runtime and normally the thinking level plus a
model/profile outside the defaults. When the fleet is Codex and the model is
omitted, use `gpt-6-astra`; when that Astra lane also omits the level, use
`xhigh`. When it is Kimi, use `kimi-code/k3` and default an omitted level to
`max`. For Codex, accept explicit `astra`, `luna`, and `terra` as `gpt-6-astra`,
`gpt-5.6-luna`, and `gpt-5.6-terra`. Ask one consolidated question for other
missing execution values. The default fleet is Astra at xhigh; do not assume it is cheaper than the
parent. Announce the raw-to-resolved model mapping and the selected lane before
the first launch, per agent-delegate's resolution doctrine. Do not silently
change runtime, model, or thinking level mid-run; if a worker model is clearly
failing the work, that is a user decision, not a silent substitution.

On the native lane, pin both values at dispatch and confirm the host accepted
them. A host that pins the model but not the thinking level gives you a half-pin
and the parent's session effort; a host whose pin expires when a child is
evicted and rebuilt gives you a worker that silently returns to the conductor's
own model mid-repair. Either one is a concrete reason to run that role
externally instead, and the log should say so.

These external-only mechanics apply when the external lane was selected. A Kimi
worker inherits `$agent-delegate`'s process contract:
`KIMI_CODE_NO_AUTO_UPDATE=1`, effort via `KIMI_MODEL_THINKING_EFFORT`, same-cwd
exact `kimi -r <session-id>` resume, and fresh `session.resume_hint` receipts.
Kimi always persists a session and cannot satisfy a load-bearing
stateless/no-persist requirement. Missing assistant text or a required fresh
hint is unrecoverable; never reuse the input id, select a latest session, or
fall back to another provider, model, or effort.

Natural `grok`, `grok cli`, or `grok build` wording resolves to `grok-4.6`;
explicit legacy `grok-*` ids remain exact.

## Patient Monitoring

Every dispatched slice gets a liveness monitor suited to its transport, armed
as part of dispatch and re-armed on every resume and respawn. Native children
use host status/wait signals; external sessions use process and run-directory
receipts. Tear it down only
when the slice is accepted, escalated, or abandoned. This is standing
practice — the conductor does not wait for the user to ask for a monitor, and
does not clear one after a slice and then forget to arm the next. Its job is
twofold: prove the worker is alive and moving, and catch a wedge early,
without pulling the raw event stream into conductor context. Where the host
provides a background-monitor capability, arm it so heartbeats push to you
while you wait or work; where it does not, poll at the scoped interval.

- **Scope the heartbeat interval to the slice's expected duration**, floor
  five minutes, ceiling thirty. A narrow single-owner slice that should finish
  in minutes gets a ~5-minute beat; a broad, high-effort slice that reasonably
  runs 20-40 minutes beats toward the 30-minute ceiling. Match the beat to the
  work: frequent enough to catch a wedge, rare enough to stay cheap. Still
  consume the real result when the child finishes — the heartbeat is a
  liveness and wedge signal, not the account of what the worker did.
- **Each beat emits one compact line from cheap signals only**: native child
  state from the host's own status or list call, or external process liveness,
  plus `git diff --stat` shape, changed-file mtimes, and external `stderr.log`
  growth when available. Native lanes may not report a child's token spend back
  to the parent, so do not treat a quiet parent-side cost total as proof the
  run is cheap. Record the pinned profile; cost depends on that model and usage.
  Relay it to the user as a brief "still moving, N files touched" check-in.
  **Never stream an external lane's `events.jsonl` into conductor context
  during normal operation** — it is a diagnostic artifact for post-mortems on
  non-zero exits or malformed output.
- **The watchdog must speak up on failure, not just progress.** Emit a wedge
  alert when the child dies unexpectedly, when it is alive but cheap signals
  show zero progress across consecutive beats, or when it overruns the slice's
  expected ceiling. A quiet healthy worker and a dead one must not produce the
  same silence.
- **Quiet is not stuck.** Big slices, high-effort thinking, long tests,
  installs, and simulators go silent for minutes. A heartbeat showing the
  process alive with fresh mtimes is progress even with no new diff yet. A
  wedge alert is the trigger to *inspect* — cheap signals first, then an
  external lane's `events.jsonl` if needed — not to reflexively replace.
  Replace or respawn
  only on evidence the worker is stuck, harmful, or dead — never on silence
  alone.

## Conductor Token Economy

The conductor's context is the most expensive resource in the run, and the
economy is about spending it on the right layer — not about spending less.
The ledger has two sides:

**Sanctioned spend — judgment and first-hand verification.** Decomposition,
scope calls, planning back-and-forth with workers, cynical audit, and
personally loading the finished work product to verify it qualitatively:
opening the spreadsheet and checking its numbers, viewing the screenshot,
reading the report or generated document. Verifying what a worker *produced*
is one of the core things the expensive model exists to do. It is never
token waste and is never capped by the intake ladder below.

**Delegated spend — investigation, production, and review labor.**
Nitty-gritty investigation, tracing through piles of files to understand how
something works, reconstructing what a worker did from raw output,
implementing anything, and the heavy review reading: requested cynical
reviews, cold verification, re-reviews, and delegated artifact inspections. That work
routes to fleet workers, who read the files so the conductor does not — on the
selected pinned profile, on whichever lane carries it.

Operating rules:

- The plan gets one full read, at intake. Afterwards re-read only the
  anchored sections named by the slice under audit.
- The conductor log is the durable memory. Never re-derive what the log
  records; after interruption or compaction, rebuild from log plus plan,
  never from chat history.
- Reconstructing what the worker *did* is layered, cheapest first: (1) the
  worker's status footer from `final.txt` — read solely to enumerate the
  claims to falsify, never as the account of what happened; (2) `git status`
  / `git diff --stat` to check the `CHANGED FILES` and `DELETES EXECUTED`
  claims against reality; (3) targeted `git diff -- <paths>` hunks, file
  reads, and authority-path traces for the actual audit. Never "read the
  repo to see what happened," and never read worker transcripts. This
  ladder bounds *did*-side intake only; it is not a cap on loading
  deliverables for the work-product verification the audit requires
  (`references/audit-and-send-back.md`).
- Batch findings into one resume prompt per repair round, not one message per
  nit. Each round-trip costs conductor context and wall clock.
- All proof runs (tests, builds, generators, simulators) are delegated. The
  conductor reads proof results; it does not produce them — and decisive
  proof counts only when independently reproduced by a different clean
  child, never from the implementing worker's own quoted run
  (`references/audit-and-send-back.md`). Loading and reading a finished
  artifact is verification the conductor owns, not a proof run to delegate.
- Chat output stays compact: one small status table per wave; detail goes to
  the log.
