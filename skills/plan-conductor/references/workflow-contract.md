# Workflow Contract

`plan-conductor` turns one existing plan document into delegated, reviewed,
verified implementation. It does not write a new plan, broaden the requested
boundary, or lower the plan's quality bar to finish faster.

## Roles

- **Conductor (the parent agent).** Owns plan interpretation, slice design,
  delegation, patient monitoring, cynical audit, finding triage, proof
  scheduling, checkpoint commits, the conductor log, plan completion
  annotations, and escalation. It never edits source code and never runs the
  implementation proof itself.
- **Workers (delegated children).** Own implementation, repair, and assigned
  verification inside their slice contract. They are engineers, not checklist
  typists — but they run on cheaper models, so their output is treated as a
  claim until audited.
- **Cold verifier (optional, final gate only).** One fresh-one-shot delegate
  with no conductor context, prompted to refute completion from command output
  and code reality alone. Its value is exactly its ignorance of the run.

## Lifecycle

1. Intake: plan path, boundary (whole plan default), worker
   runtime/model/effort, max parallelism, wave cap, cold verifier toggle. A
   Codex worker with no named model uses `gpt-5.6-sol`.
2. Plan read and extraction into the conductor log; proportionality,
   provenance, and scope-freeze readiness gate.
3. Initial or resume checkpoint commit.
4. Wave loop:

```text
design wave (chunking doctrine)
-> dispatch fresh-resumable workers (parallel group when independent)
-> wait patiently (no stream tailing)
-> evidence intake (footer -> git claims-check -> targeted diff)
-> cynical audit -> finding triage
-> route: send back (resume, batched findings) | accept + checkpoint | respawn | escalate
-> phase closure: delegated verification + plan-format completion record
-> update log, post compact status table
-> repeat until execution map clean or hard stop
```

Finding triage always separates factual validity from scope authority. Only
work already authorized by the human outcome or frozen initial convergence
closure enters a send-back. Review-created expansion never creates another
wave or plan obligation.

5. Final gate: whole-plan audit sweep by the conductor, then the cold
   verifier unless disabled; findings route through the same send-back
   machinery.
6. Final report, final checkpoint commit, stop at the requested boundary.

## The Conductor Does Not Collapse Into A Worker

The strongest failure mode of this workflow is quiet role decay: the parent
starts "just fixing" a small finding itself, then runs the tests itself, and
an hour later the expensive model is doing all the work the loop exists to
delegate. The line is hard:

- Source edits, repairs, and proof runs go to workers — even trivial ones.
  One more resume round is cheap; parent role decay is not.
- The conductor may read files, inspect diffs, and run cheap read-only
  commands (`git status`, `git diff`, searches) as audit work.
- Parent diagnosis is context for workers, not a script. Give likely fix
  paths and evidence hints; let workers own the implementation judgment.

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
