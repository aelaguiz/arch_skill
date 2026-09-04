# Workflow Contract

`conductor` turns one conducted artifact — an existing plan document, or the
outcome map the shaping stage produced and the user approved — into
delegated, reviewed, verified implementation. Once execution starts it does
not rewrite that artifact, broaden the requested boundary, or lower the
quality bar to finish faster.

## Roles

- **Conductor (the parent agent).** Owns plan interpretation, slice design,
  delegation, patient monitoring, cynical audit, finding triage, proof
  scheduling, checkpoint commits, the conductor log, plan completion
  annotations, and escalation. It never edits source code and never runs the
  implementation proof itself.
- **Workers (delegated children).** Own implementation, repair, and assigned
  verification inside their slice contract. They are engineers, not checklist
  typists. Their output is treated as a claim until audited regardless of
  transport or model.
- **Cold verifier (optional, final gate only).** One new clean child with no
  conductor narrative, prompted to refute completion from command output and
  code reality alone. Its value is exactly its ignorance of the run.

## Lifecycle

1. Intake: plan path, boundary (whole plan default), per-role transport and
   starting context, any external runtime/model/effort, max parallelism, wave
   cap, and cold-verifier toggle. An external Codex worker with no named model
   uses `gpt-6-astra`; that Astra worker uses `xhigh` when effort is omitted.
2. Plan read and extraction in context; capture the start commit and inherited
   worktree state before writing the conductor log.
3. Write the log, recording the start commit, then apply and record the
   proportionality, provenance, and scope sign-off readiness gate. On a passing
   gate, take an initial or resume checkpoint only when the inherited worktree
   held plan work to preserve (see Git Posture).
4. Wave loop:

```text
design wave (chunking doctrine)
-> dispatch new clean workers (parallel group when independent)
-> wait patiently (no stream tailing)
-> evidence intake (footer -> git claims-check -> targeted diff)
-> cynical audit -> finding triage
-> route: send back (resume, batched findings) | accept + checkpoint | respawn | escalate
-> phase closure: delegated verification + plan-format completion record
-> update log, post compact status table
-> repeat until execution map clean or hard stop
```

Finding triage always separates factual validity from scope authority. Only
work already authorized by the human outcome or approved initial convergence
closure enters a send-back. Review-created expansion never creates another
wave or plan obligation.

5. Final gate: whole-plan audit sweep by the conductor, then the cold
   verifier unless disabled; findings route through the same send-back
   machinery.
6. Final report, final checkpoint commit, stop at the requested boundary.

## The Conductor Does Not Collapse Into A Worker

The strongest failure mode of this workflow is quiet role decay: the parent
starts "just fixing" a small finding itself, then runs the tests itself, and
an hour later the parent is doing all the work the loop exists to
delegate. The line is hard:

- Source edits, repairs, and proof runs go to workers — even trivial ones.
  Resume the worker instead of taking over its role.
- The conductor may read files, inspect diffs, and run cheap read-only
  commands (`git status`, `git diff`, searches) as audit work.
- A materially useful parent diagnosis may travel only as a challengeable lead
  with its evidence or provenance, not as task truth. Let workers reject it,
  choose the evidence path, and own implementation judgment inside the approved
  contract.

## Git Posture

- Local commits are ordinary checkpoints, not PR-ready history. Commit after
  accepted slices, meaningful repair rounds, phase closure, and the final
  report. The user can squash or reorder before any PR.
- If the run inherits a dirty worktree, treat it as likely resumed plan work
  and take an initial checkpoint unless there is a concrete safety issue such
  as secrets or files clearly unrelated to the repo.
- The conductor owns commits. Workers never commit, push, stash, or revert
  unrelated work. Never push or open PRs from this skill.

## Stop Discipline

- Stop at the requested boundary: whole plan by default, an explicit phase
  range when the user named one.
- A cap firing (wave cap, per-slice attempt caps, process-failure rule) is a
  stop-and-report event, not permission to lower the audit bar.
- An escalated slice stops only its own dependency chain; independent slices
  keep flowing. The run halts when nothing dispatchable remains, then reports
  every escalation with the specific user decision it needs.
- Never claim completion while any slice is outside `accepted`/`deferred`,
  any deferral lacks a recorded rationale, plan-required proof is missing, or
  the final gate has open accepted findings.
- Never claim completion while scope provenance is unresolved, a human scope
  decision is open, unauthorized built scope remains, or the wave history shows
  scope cycling.
