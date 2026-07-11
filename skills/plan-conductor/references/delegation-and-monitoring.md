# Delegation And Monitoring

Every dispatch maps onto `$agent-delegate` with no new machinery. That skill
owns invocation mechanics — command shapes, run directories, session capture,
hook suppression, model/effort resolution, and failure handling. This
reference only maps conductor situations onto its modes and defines the
conductor's monitoring and token-economy posture.

## Mode Mapping

- **Initial slice dispatch → `fresh-resumable`** (agent-delegate's default).
  The child starts cold from disk plus the slice contract. Record the run
  directory and captured session id in the conductor log.
- **Send-back / repair → `resume`** with the exact captured session id, same
  runtime, and a new bounded findings prompt. The session already holds the
  slice context — that continuity is exactly why the resumable path exists.
  Never `--continue`, never "latest," never cross-runtime.
- **Respawn → new `fresh-resumable`** child with a sharpened brief. Use when
  the session is unhealthy (caps in the audit reference), the repair moved to
  a different owner surface, or a cold implementation view is needed.
- **Cold verifier → `fresh-one-shot`**, final gate only. Statelessness is the
  feature: no conductor context, no resume, just refutation from code
  reality. Give it the plan path, human baseline anchors, frozen initial
  closure, freeze anchor, and explicit human approvals; its findings cannot
  expand scope.
- **Parallel waves** use agent-delegate's parallel group path: one group
  directory, one ordinary child run directory per worker, every child briefed
  that siblings may be editing the repo, must not revert unfamiliar changes,
  and must report actual conflicts with file evidence rather than resolving
  them by guesswork.

## Worker Identity

The user supplies worker runtime and effort at kickoff plus a model/profile
for non-Codex lanes. When the selected lane is Codex and the model is omitted,
use `gpt-5.6-sol`; accept explicit `sol`, `luna`, and `terra` as
`gpt-5.6-sol`, `gpt-5.6-luna`, and `gpt-5.6-terra`. Ask one consolidated
question for other missing execution values. The intended fleet is "smart but
not the smartest" — fast, cheap implementation models — while the conductor
runs on the expensive model. Announce the raw-to-resolved model mapping before
the first launch, per agent-delegate's resolution doctrine. Do not silently
change runtime, model, or effort mid-run; if a worker model is clearly failing
the work, that is a user decision, not a silent substitution.

## Patient Monitoring

Every dispatched slice gets a background watchdog, armed as part of the
dispatch itself and re-armed on every resume and respawn. Tear it down only
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
  consume the real result when the delegate process exits — the heartbeat is a
  liveness and wedge signal, not the account of what the worker did.
- **Each beat emits one compact line from cheap signals only**: process
  liveness, `git diff --stat` shape, changed-file mtimes, `stderr.log` growth.
  Relay it to the user as a brief "still moving, N files touched" check-in.
  **Never stream `events.jsonl` into conductor context during normal
  operation** — it is a diagnostic artifact for post-mortems on non-zero exits
  or malformed output.
- **The watchdog must speak up on failure, not just progress.** Emit a wedge
  alert when the process dies unexpectedly, when it is alive but cheap signals
  show zero progress across consecutive beats, or when it overruns the slice's
  expected ceiling. A quiet healthy worker and a dead one must not produce the
  same silence.
- **Quiet is not stuck.** Big slices, high-effort thinking, long tests,
  installs, and simulators go silent for minutes. A heartbeat showing the
  process alive with fresh mtimes is progress even with no new diff yet. A
  wedge alert is the trigger to *inspect* — cheap signals first, then
  `events.jsonl` if needed — not to reflexively replace. Replace or respawn
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
