# Resource Leases

Verification resources are shared. The parent agent coordinates them instead of
letting every worker run expensive checks.

Verification is also selective. The parent and workers choose proof from the
plan's stated validation obligations plus the surfaces changed or plausibly
impacted by the work. They do not run the full suite just because it is the
default command.

## Lease Examples

- full test suite
- simulator or emulator
- browser automation
- mobile device
- database migration
- code generation
- build cache-heavy compile

## Rules

- A slice that needs a scarce resource names it in the swarm ledger.
- The parent assigns at most one active worker to a scarce resource at a time.
- Workers without a lease may run cheap slice-local checks.
- A designated verification worker may hold the expensive test lease after
  implementation slices finish.
- Full-suite leases need a reason: plan requirement, changed shared
  infrastructure, cross-cutting impact, stale prior proof, or release gate. If
  targeted proof gives high confidence, prefer that.
- Reuse already-passing proof unless a later slice touched code, generated
  artifacts, configuration, data, or behavior that could invalidate it.
- The parent tracks leases and reads results; it should not become the normal
  runner for expensive tests, builds, generators, simulators, browsers, or
  devices.
- Release leases when a worker completes, fails, or is explicitly abandoned.
