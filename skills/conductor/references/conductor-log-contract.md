# Conductor Log Contract

One sidecar file beside the plan: `<PLAN_STEM>_CONDUCTOR_LOG.md` (for
`docs/PAYMENTS_MIGRATION_2026-07-01.md`, the log is
`docs/PAYMENTS_MIGRATION_2026-07-01_CONDUCTOR_LOG.md`). It is schedule,
evidence, and resume state — never a second plan. Record facts and anchors,
not transcripts. The log must not contain secrets.

Do not write into surfaces other skills own: never hand-edit
`arch_skill:block:*` receipt blocks (script-owned) and never write
`<PLAN_STEM>_PLAN_AUDIT.md` (plan-audit owns it; read its open findings as
constraints).

## Layout

```markdown
# Conductor Log
Plan: <path to the conducted plan or outcome map>
Start commit: <hash>
Workers: <transport/context; external runtime/model/effort when selected>
Max parallel: <N>   Wave cap: <N>
Boundary: <whole plan | phases X-Y>   Cold verifier: <on|off>
Final gate: <not run | clean | findings open>
Scope contract: <plan anchor>   Scope status: <frozen-clean | human decision needed | unresolved>
Human baseline: <plan/user anchor>   Initial closure: <plan anchor or none>

## Resume Snapshot
- Current state: <one paragraph>
- Next useful move: <one line>
- Do not redo unless stale: <bullets>
- Known blockers: <bullets or none>

## Execution Map
| Slice | Plan anchor | Depends on | Size rationale | Status | Worker/handle | Attempts | Evidence |
|---|---|---|---|---|---|---|---|

## Findings Ledger
### PC-001 - <title>
- Slice: <id>  Lens: <lens>  Evidence: <path:line>
- Factual status: accepted | rejected | unresolved
- Scope disposition: authorized | frozen-convergence-required | new-scope-needs-human | out-of-scope | unauthorized-built-scope
- Route: send-back | observe | human-decision | subtract | resolved
- Resolution evidence: <anchor>

## Proof Ledger
| Proof | Scope covered | Result | Ran by | Fresh until | Rerun trigger |
|---|---|---|---|---|---|

## Wave History
| Wave | Dispatched | Returned | Verdicts | Commit |
|---|---|---|---|---|

## Escalations
| Item | Decision needed | Blocking |
|---|---|---|
```

## Field Rules

- **Status enum** for slices:
  `open | dispatched | auditing | sent-back | accepted | blocked | escalated | deferred`.
- **Size rationale** is one line saying why this chunk (whole phase, named
  owner-boundary split, merged trivial phases) — it makes the chunking
  judgment visible and reviewable.
- **Worker/handle** names transport, starting context, and the exact native
  child handle or external session id. For an external lane it also records
  runtime/model/effort and the `$agent-delegate` run directory. These receipts
  preserve exact-role continuation without treating transport as workflow
  meaning.
- **Attempts** counts dispatch + send-backs + respawns toward the per-slice
  caps.
- **Evidence** for an `accepted` slice anchors the proof: diff anchors,
  independently reproduced verification results, checkpoint commit, plus a
  one-line refutation record naming which lens groups and lying-modes were
  checked — so a later reader can distinguish "audited" from "skimmed".
- **Scope contract fields** are anchors and a compact status only. Never copy
  or revise the plan's contract in the conductor log.
- **Finding status** answers whether a finding is technically valid; scope
  disposition answers whether it is authorized work. A valid finding is not
  automatically a send-back. Repeated findings keep the same disposition.
- **Proof Ledger** entries carry the freshness reasoning: what would force a
  rerun. Reuse passing proof until a recorded invalidator fires. **Ran by**
  names the independent child that produced the result; an entry marked
  `implementer-only` never satisfies decisive-proof acceptance and is never
  reused as passing proof — it is a claim awaiting reproduction.
- **Wave History** is one compact line per wave — enough breadcrumbs to
  recover progress, not a narrative.

## Update Cadence

Update at meaningful boundaries — dispatch, return, triage, acceptance,
checkpoint, escalation — not after every micro-step. Keep the log short
enough that a resumed conductor can read it quickly; the Resume Snapshot is
the first thing a post-compaction parent reads.

## Exit Probe

The run is complete when all three hold:

1. Zero Execution Map rows outside `accepted`/`deferred`, and every
   `deferred` row carries prior plan authority or explicit human approval.
2. Every phase's plan-required verification is recorded passing in the Proof
   Ledger (fresh, or valid-until untouched).
3. The `Final gate:` header line reads `clean`.
4. `Scope status:` reads `frozen-clean`, with no open
   `new-scope-needs-human` decision, scope-cycle finding, or
   `unauthorized-built-scope` subtraction.

A cheap approximate probe between waves (matches Execution Map status
cells; the map itself is authoritative):

```sh
grep -cE '\| *(open|dispatched|auditing|sent-back|blocked|escalated) *\|' <PLAN_STEM>_CONDUCTOR_LOG.md || true
```

Zero matches plus a clean final gate means done; anything else names the
remaining work.
