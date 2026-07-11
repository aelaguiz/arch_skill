# Chunking And Parallelism

Slice sizing is the heart of the workflow because both failure modes are
expensive:

- **Micro-tasking.** Slices so narrow the worker cannot reason — "add these
  five lines." Every slice costs a fixed parent overhead (prompt, wait,
  audit, route), so tiny slices maximize expensive round-trips while denying
  workers the context to make even implementation-level decisions. The parent
  has become a slow programmer with extra steps.
- **Mega-tasking.** "Implement phases 1 through 6." The diff is unreviewable,
  the worker drowns in decisions the plan left open, one bad early choice
  contaminates everything, and there are no intermediate acceptance points.

## Default: One Plan Phase Per Worker

Plan authors already sized phases as coherent, proof-gated units. Trust that.
Adjust in exactly two directions:

- **Split a phase** only along boundaries the plan itself names — owner
  surfaces in a call-site audit, independent subsystems in a change map.
  Never one file per worker, never arbitrary equal chunks, never a split
  that crosses a shared unsettled design decision.
- **Merge phases** when adjacent phases are trivial and share one design
  intent (a small implementation phase plus its doc-propagation phase), so
  the worker gets a whole thought.

All splits and merges must stay inside the frozen plan contract. Chunk size is
an execution decision, never authority to pull in another caller family,
cleanup area, proof category, or reviewer suggestion.

## Sizing Litmus Tests

Judgment aids, not a rule engine:

1. **Cold-start test.** Could a strong mid-level engineer, walking in cold
   with the slice brief, the plan section, and the repo, finish this in one
   focused sitting? If it needs staff-level architectural taste, the slice is
   carrying a design decision that belongs to the plan or the user — pull it
   out. If it needs no judgment at all, it is too small — widen it.
2. **One-decision rule.** A slice may contain many implementation choices but
   zero unsettled design decisions. Two slices sharing one unsettled decision
   are one slice, or an escalation — never parallel work.
3. **Review-tractability test.** The expected diff must be auditable by the
   conductor in one pass — roughly one subsystem's worth of change; more only
   when the change is mechanical and the plan enumerates it.
4. **Failure-description test.** If the worker gets it wrong, can the
   conductor express what is wrong as a findings batch without redoing the
   work? If describing the failure requires writing the code, the slice
   contract was too vague — tighten the contract, not the leash.

**Tie-break: when unsure, chunk bigger inside the same frozen scope.** The send-back loop is the safety
net and worker attempts are cheap; parent round-trips are the scarce
resource. The review-tractability test is the ceiling that keeps "bigger"
from becoming "unreviewable."

## Parallel Launch Judgment

Parallelism is a bonus the plan either offers or does not:

- Fan out only when slices are dependency-ready under the plan's own
  ordering, touch disjoint owner surfaces, and share no unsettled decision.
- The conductor owns the fanout budget and integration. Workers do not create
  more agents unless the conductor explicitly assigns a bounded nested scope.
- Do not create a new slice from a post-freeze audit finding. Route it by scope
  disposition: repair authorized work, subtract unauthorized work, or ask the
  human decision owner.
- Run replacement paths before deletion paths; never parallel-delete what a
  sibling still calls.
- Do not let multiple workers monopolize one scarce resource — full test
  suite, simulator, device, generator, migration. The conductor sequences
  those explicitly.
- Consecutive depth-first phases stay sequential. Within-phase owner-boundary
  slices and plan-declared independent phases are the parallel candidates.
- **Serial is fine.** A two-phase plan runs one worker at a time and that is
  correct behavior, not a failure. The speedup comes as much from cheap fast
  workers and batched send-backs as from fanout.

## Concurrency Judgment

Set max parallelism from real independent slices, available host slots,
shared-worktree collision risk, external process cost, and the conductor's
ability to audit every return. The user may pin a value at kickoff, but it is a
ceiling, not a target. Reduce fanout when the worktree gets conflicted, proof is
unclear, or workers touch unexpectedly overlapping surfaces. Serial execution
remains correct when those constraints leave one safe slice.
