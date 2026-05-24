# Worker Prompt Contract

Prompt workers like capable colleagues entering cold. Give them enough truth to
move fast without turning them into brittle checklist executors.

## Include

- Mission: one slice outcome.
- Authoritative inputs: plan path, phase contract, swarm ledger slice, and
  relevant repo paths.
- Sibling context: other workers may be editing nearby code; do not revert
  unfamiliar changes.
- Success bar: behavior, tests, owner boundaries, cleanup, and proof needed.
- Verification intent: plan-required proof, changed/impacted surfaces that need
  confidence, tests already passing that should not be rerun unless affected,
  and any scarce verification lease.
- Freedom: workers may inspect adjacent owning code and make necessary
  task-relevant edits.
- Native parallelism: `Maximize parallelism by using parallel agents. Do not
  invoke skills that spawn subagents.`
- Parent hints: likely fix paths, suspected files, and evidence to inspect are
  advisory, not a script. The worker still owns the implementation judgment.
- Constraint: do not broaden product scope, push, stash, or revert unrelated
  work. Parent owns commit checkpoints unless this worker prompt explicitly
  assigns you one.

## Avoid

- Micromanaged file-by-file scripts.
- "Do not touch anything else" guardrails that prevent required adjacent fixes.
- Large copied plan sections when a path and heading is enough.
- Asking workers to run scarce full-suite checks without a lease and a concrete
  reason tied to the plan, changed/impacted surfaces, stale proof, or review
  findings.
- Asking the parent to rerun implementation tests as the normal proof path.
- Treating workers as checklist executors. They are engineers responsible for
  real implementation within the slice mission.

## Required Footer

```text
STATUS: done | blocked | needs-parent | failed
SLICE: <slice id>
CHANGED FILES: <paths or none>
VERIFICATION: <commands/results or not run: reason>
PROOF: <phase requirements and impacted behavior covered; already-passing proof reused if relevant>
SESSION HEALTH: healthy | struggling | stuck | unknown
BLOCKERS: <none or concrete blocker>
FOLLOW-UP: <none or next recommended action>
SUMMARY: <one paragraph>
```
