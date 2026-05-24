# Decomposition And Scheduling

The swarm ledger is schedule and evidence, not a competing plan. It is a
human-readable coordination aid that helps the parent agent decide which
workers can run in parallel.

## Slice Shape

Each slice needs:

- id and title
- goal
- source truth
- likely owning and adjacent areas
- dependencies
- likely collision risk
- parallelization strategy
- scarce resources
- proof needed
- assigned worker and session id when known
- status

Good slices are large enough for a capable worker to reason and small enough to
finish without owning the whole phase.

## Wave Types

- `implementation`: initial phase slices from the plan contract.
- `repair`: accepted review, test, integration, or worker findings batched into
  follow-up slices.
- `verification`: proof work assigned to a worker, especially for tests, builds,
  generators, simulators, browsers, devices, or other shared resources.

Repair and verification waves use the same decomposition judgment as initial
implementation. The parent may give a likely fix path, but should delegate the
actual fix or proof run.

## Split By

- canonical owner boundary
- dependency boundary
- proof boundary
- replacement-before-deletion boundary
- scarce resource boundary
- collision risk

Do not split by one file per worker, arbitrary equal chunks, or tiny TODOs that
share one design decision.

## Wave Rules

- Launch slices whose dependencies are complete and whose edits are unlikely to
  collide.
- Batch findings before dispatching follow-up work unless one blocker prevents
  every other slice from moving.
- Do not launch two workers into the same unsettled design decision.
- Do not let multiple workers monopolize the same expensive test, simulator,
  browser, generator, or migration resource.
- Give tightly coupled work to one worker or run it serially.
- Run replacement paths before deletion or cleanup paths.
- Prefer resuming the healthy worker who owns the related slice.
- Spawn fresh when the previous worker is stuck, introduced bad fixes, or the
  accepted finding moved to a different owner surface.
- Keep full-suite verification for a designated verification worker unless a
  different worker has an explicit lease.

## Chunk Table

Record the current chunking in the `Current Phase Work Slices` table in
`swarm-ledger.md`. Each row should make the parallelization strategy visible:
why the slice can run in parallel now, why it is waiting, or why it should be
owned by one worker serially. If two slices share one unsettled design decision,
the table should show that relationship instead of pretending they are
independent.

## Defaults

- Cursor Agent implementation max parallelism: `4`.
- Codex or Claude implementation max parallelism: `2` unless the user pins a
  different value.
- Parent may reduce parallelism when the repo state is conflicted, proof is
  unclear, or workers are touching unexpectedly overlapping surfaces.
