# Goal Loop Controller Contract

Required controller blocks, worklog rules, status rules, and loop contract for goal-loop. Core doctrine and lifecycle live in references/controller-lifecycle.md. This document documents only the goal-loop-specific contract.

## DOC_PATH and WORKLOG_PATH

`DOC_PATH` is the goal-loop controller.
`WORKLOG_PATH` is the append-only memory:

- `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`

`WORKLOG_PATH` must exist before the loop is considered restart-safe.

## New-controller minimum contract

The controller should contain:

- North Star
- success metric or scoreboard
- anti-sidetrack contract
- lever inventory
- iteration protocol
- de-dupe rule
- current state or best current belief

## Required controller blocks

- `goal_loop:block:contract`
- `goal_loop:block:anti_sidetrack`
- `goal_loop:block:scoreboard`
- `goal_loop:block:levers`
- `goal_loop:block:iteration_protocol`
- `goal_loop:block:de_dupe`

Recommended:

- `goal_loop:block:state`
- `goal_loop:block:context_digest`

## Worklog rules

- append-only
- read it first every iteration
- exactly one entry per iteration
- every entry captures:

- bet
- decision rule
- work performed
- evidence
- result
- conclusion
- next bet

## Helper modes

flow-status: inspect readiness and recommend the single next move.
context digest: write or refresh a compact restart handoff only when explicitly requested.
de-dupe: before any new iteration, compare the proposed bet against the last 1-3 entries and avoid re-running the same experiment unchanged.

## Status rules

- New or unconfirmed controller docs stay `draft`.
- Active loops use `active`.
- Mark complete only when the goal is actually achieved or intentionally retired.
