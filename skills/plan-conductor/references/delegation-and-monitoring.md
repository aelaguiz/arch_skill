# Delegation And Monitoring

The conductor chooses transport under
`../../_shared/agent-orchestration-policy.md`; transport does not choose the
workflow. Same-host phase work normally stays under the active host's native
child lifecycle. `$agent-delegate` remains the external editful adapter when a
different provider, load-bearing exact cheaper model/profile, durable session,
worktree/process isolation, automation surface, structured receipt, or another
concrete benefit is worth the additional process and integration cost. Those
examples teach the decision; they are not a closed allowlist.

## Dispatch And Continuation Mapping

- **Initial slice dispatch → new clean child.** Give it the plan path, log
  path, slice anchors, constraints, and return contract. In Codex set
  `fork_turns: "none"`; in Claude use a clean named subagent. If the external
  lane was selected, use `$agent-delegate` `fresh-resumable`. Record the
  transport, starting context, exact handle, and external run directory when
  one exists.
- **Send-back / repair → exact-child resume.** Send one bounded findings delta
  to the same native child handle or the exact external session id through its
  original transport. Never select "latest," cross runtimes, or replace the
  implementer merely because another handle is convenient.
- **Respawn → new clean replacement.** Use when the role truly needs a cold
  restart, its prior handle is lost or unhealthy under the audit caps, or its
  owner surface changed enough to invalidate the earlier view. Record why the
  replacement was necessary.
- **Cold verifier → new clean critic**, final gate only. Independence is the
  feature: no conductor narrative, no resume, just refutation from plan and
  code reality. In Codex set `fork_turns: "none"`; in Claude use another clean
  named subagent. Give it the plan path, human baseline anchors, frozen initial
  closure, freeze anchor, and explicit human approvals; its findings cannot
  expand scope. An external one-shot remains valid when its provider, exact
  profile, isolation, or receipt is the deliberate value.
- **Parallel waves** are parent-owned. Use only the active host slots or
  external sessions that independent, non-overlapping slices justify. Every
  child knows that siblings may be editing the repo, must not revert unfamiliar
  changes, must not create more agents unless explicitly assigned a bounded
  nested scope, and must report actual conflicts with file evidence.

## Native Starting Context

Clean context is the default because the plan and conductor log already carry
the durable inputs. In Codex, every native spawn states `fork_turns`:
`"none"` for ordinary phase workers and critics, a positive count only for a
small chat-only dependency, and `"all"` only when the whole conversation is
load-bearing. In Claude, a clean named subagent is distinct from an explicit
full conversation fork; a skill declared with `context: fork` is an isolated
clean subagent context, not full inheritance.

Context inheritance is separate from permissions, capabilities, filesystem
sharing, and worktree isolation. State those independently. Native clean
children commonly share the current worktree. For a read-only critic, use an
enforced read-only capability when the host exposes one, keep the no-edit
prompt rule, and have the conductor compare repository state before and after.

## External Worker Identity

Resolve these values only when an external lane was selected. The user supplies
worker runtime and effort plus a model/profile for non-Codex lanes. When the
selected external lane is Codex and the model is omitted, use `gpt-5.6-sol`;
accept explicit `sol`, `luna`, and `terra` as
`gpt-5.6-sol`, `gpt-5.6-luna`, and `gpt-5.6-terra`. Ask one consolidated
question for other missing execution values. The intended fleet is "smart but
not the smartest" — fast, cheap implementation models — while the conductor
runs on the expensive model. Announce the raw-to-resolved model mapping before
the first launch, per agent-delegate's resolution doctrine. Do not silently
change runtime, model, or effort mid-run; if a worker model is clearly failing
the work, that is a user decision, not a silent substitution.

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
  state or external process liveness, `git diff --stat` shape, changed-file
  mtimes, and external `stderr.log` growth when available.
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

The conductor's context is the most expensive resource in the run. Explicit
spending rules:

- The plan gets one full read, at intake. Afterwards re-read only the
  anchored sections named by the slice under audit.
- The conductor log is the durable memory. Never re-derive what the log
  records; after interruption or compaction, rebuild from log plus plan,
  never from chat history.
- Evidence intake is layered, cheapest first: (1) the worker's status footer
  from `final.txt` — read solely to enumerate the claims to falsify, never as
  the account of what happened; (2) `git status` / `git diff --stat` to check
  the `CHANGED FILES` and `DELETES EXECUTED` claims against reality; (3)
  targeted `git diff -- <paths>` hunks, file reads, and authority-path traces
  for the actual audit. Never "read the repo to see what happened," and never
  read worker transcripts. Cheap intake bounds token spend; it never lowers
  the audit bar — the burden of proof stays on the worker's output
  (`references/audit-and-send-back.md`).
- Batch findings into one resume prompt per repair round, not one message per
  nit. Each round-trip costs conductor context and wall clock.
- All proof runs are delegated. The conductor reads proof results; it does
  not produce them.
- Chat output stays compact: one small status table per wave; detail goes to
  the log.
