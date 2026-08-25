# Shaping And The Outcome Map

This stage exists for intake that is not yet a conductable plan: a described
outcome ("get X working end to end") or a partial plan (real requirements,
missing done-ness or ordering). Its output is the **outcome map** — the
smallest artifact that passes the same readiness gate a finished plan must
pass. Shaping happens before the gate, never around it: if the map still
lacks observable done-ness or an approved boundary, the run stops exactly as it
would for a defective plan.

Skip this stage entirely when the intake is a finished plan. Do not "improve"
a plan the user already finished; that is scope laundering.

## The executive stance

The parent is the scope judge, and this stage is where that judgment earns
its cost. Fast cheap workers are genuinely smart and will propose more than
the outcome needs: extra abstraction, adjacent refactors, speculative
hardening, pedantic completeness. Expect it, use the good parts, and cut the
rest. The bar for every slice is: the user's outcome is not true without it.
When a proposal is valuable but not necessary, record it as a non-goal or an
escalation candidate, not as scope.

The parent writes the outcome map itself. Workers research and propose;
their output is evidence for the parent's decision, never the decision.

## Research delegation

Optional, sized to real uncertainty. When the parent already knows the code,
shape directly and dispatch nothing.

- Dispatch research workers under `../../_shared/agent-orchestration-policy.md`
  with `$prompt-authoring` applied to each populated brief. Clean context,
  read-only role, no implementation. A research worker may use its own native
  sub-agents on its host; it may not start external agents.
- Parallelize genuinely independent questions: map the subsystem, find the
  authority paths, enumerate the touchpoints, propose candidate slices.
- Require compact returns: findings with file and symbol anchors, a proposed
  slice list with claimed done-ness, and open risks. The parent's context is
  the expensive resource; workers read the files so the parent does not.
- Treat proposals skeptically. A research worker asserting "X must also
  change" is a claim with an anchor to verify, not a scope expansion.

## The outcome map contract

Write the map beside the work as `<GOAL_SLUG>_OUTCOME_MAP.md`. Its stem
names the conductor log (`<GOAL_SLUG>_OUTCOME_MAP_CONDUCTOR_LOG.md`), so the
normal log convention holds unchanged.

Required blocks — content, not ceremony; each may be short:

- **North Star** — the outcome in the user's language, plus how anyone would
  observe that it is true.
- **Non-Goals / Do-Not-Build** — the trimmed proposals and adjacent work
  deliberately excluded. This block is what makes the sign-off auditable.
- **Slices** — ordered, phase-sized work units, each with observable
  done-ness and its verification obligation (the command, test, or check
  that proves it). Slices follow the chunking doctrine: default one coherent
  phase of work per worker, never micro-tasks.
- **Dependencies** — which slices block which, and which are genuinely
  independent (these become the parallel dispatch candidates).
- **Approval** — who approved the scope boundary and when, or the explicit
  `full-auto` grant that stood in for the pause.

For partial-plan intake, the existing plan text stays authoritative for
everything it actually decides. The map anchors into it and fills only the
gaps — done-ness for requirements that lack it, ordering where none exists,
non-goals where scope is implicit. Never rewrite or re-scope the author's
decisions; a real conflict between the partial plan and repo truth is an
escalation, not an edit.

## Approval and sign-off

Present the map compactly for approval: North Star, the slice list with
done-ness, and the non-goals. One pause, one decision. The user may adjust
scope freely at this moment — that is the point of the pause.

Approval (or an explicit prior `full-auto` grant from the user, recorded in
the Approval block) signs off the boundary with the same discipline as a
finished plan's scope sign-off: workers, audits, reviews, and repeated
findings cannot expand it, and a newly discovered same-contract adjacent
path requires a human decision. From this moment the map is "the plan" for
every downstream rule in `SKILL.md` and the other references.
