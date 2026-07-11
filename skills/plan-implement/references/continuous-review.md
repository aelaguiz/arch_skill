# Continuous Review

Continuous review means reviewing useful slices while the code is still easy to
repair. It is not a formal code review runner and not a replacement for
`plan-audit implementation-audit` at the final boundary.

## When To Review

Review while warm:

- after the first narrow integrated slice
- after changing a canonical owner or caller shape
- after deleting, migrating, or closing side doors
- after leaving adjacent same-contract or same-behavior paths untouched
- after a slice claims simplification, unification, deletion, migration, or SSOT
  convergence
- after touching schemas, generated artifacts, prompts, docs, examples, config,
  routes, commands, or install surfaces
- before widening to more callers, variants, modes, or polish
- before marking a plan phase, section, or checklist item done

## What To Review

Use the plan's requirements and the `plan-audit` implementation-audit lenses:

- plan-code fit
- intent vs reality: whether the intended outcome is true in code, not only in
  names, wrappers, checkboxes, or phase labels
- requirement traceability
- canonical owner and SSOT
- existing pattern fit
- convergence across adjacent same-contract or same-behavior surfaces
- deletion and side-door closure
- drift-proof coupling
- caller invariant state
- elegance and code-judo
- tiny-team maintainability
- changed tests as code
- docs, prompts, examples, config, generated artifacts, and install surfaces
  when touched or routing-relevant

## Finding Handling

Give every material finding one scope disposition from
`skills/_shared/scope-and-convergence.md`. Repair directly only when it is
`authorized` or `frozen-convergence-required`. A real finding outside the
frozen contract, including a newly discovered same-contract path, is
`new-scope-needs-human` or `out-of-scope`; it does not enter the active ledger.
If code already implements it, classify it `unauthorized-built-scope` and
subtract it unless a human approves and re-freezes.

Repair trivial self-review issues directly when they are local and obvious.
Record them in the worklog only when they affect resumability, proof freshness,
or later review.

Open an `IMP-*` finding in the plan audit log when:

- the issue blocks implementation approval for the requested scope
- the issue may survive beyond the current edit
- the issue requires a decision, follow-up repair, or later proof
- the issue connects to an existing `PLA-*` finding

Close an `IMP-*` finding only when the repair has a code anchor and any needed
proof or proof-freshness rationale is recorded.

Reject or mark findings out of scope with a short reason; do not silently drop
them.

## Native Subagent Review

Use native subagents or parallel-agent features for independent read-only
review lenses when that saves time. Good split points:

- one lens per subagent
- side-door and delete search
- existing pattern comparison
- docs/prompts/examples drift
- changed tests reviewed as code
- drift-prone contracts and generated artifacts

The parent must spot-check anchors, dedupe findings, reject out-of-scope
findings, update artifacts, and own the final claim.

## What Not To Do

- Do not launch an external review runner unless the user or local instructions
  explicitly require it.
- Do not manually spawn `codex`, `claude`, `agent`, or `grok` binaries for
  ordinary continuous review.
- Do not block implementation on missing CI logs when this is plan-backed code
  review.
- Do not let review become a reason to widen scope beyond the frozen contract.
  Repetition by later reviewers does not change the finding's disposition.
- Do not wait until the final report to run the first serious architecture
  review.
