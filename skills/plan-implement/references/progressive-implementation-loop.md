# Progressive Implementation Loop

Use this as the main execution path. The goal is speed through fewer repeated
reads, fewer duplicate checks, and earlier review.

## 1. Resolve Scope

Read:

- the user request
- the plan artifact
- the active phase, section, checklist, or stop boundary
- the plan audit log when present
- the implementation log when present
- local instructions
- current worktree state

State the active scope plainly. Do not silently widen into adjacent phases,
whole-plan signoff, or unrelated cleanup.

## 2. Choose The Next Narrow Slice

Choose the smallest depth-first slice that moves the plan toward its North Star
and crosses a meaningful integration seam.

Prefer slices that:

- make one requirement true end to end
- prove owner path and caller shape early
- delete or close one real side door
- reduce live concept count
- keep proof targeted

Avoid slices that:

- build broad scaffolding before integration
- add helpers, modes, wrappers, or config before proving the core path
- defer the risky seam until the end
- widen to more callers before the prior layer is real

## 3. Build The Local Truth Cache

Before editing, record the useful current facts in the implementation log:

- relevant plan anchors
- code areas read
- owner path and caller families
- legacy paths and side doors found
- comparable patterns
- proof already fresh
- proof likely needed after this slice
- implementation-audit lenses likely to matter

This is a human cache, not a state machine. Keep it short.

## 4. Use Native Parallelism Where It Saves Time

When the current coding harness provides native subagents or parallel-agent
features, use them for independent work that would otherwise be serial:

- code mapping
- side-door search
- existing-pattern comparison
- docs, prompts, examples, config, or generated-artifact drift checks
- changed tests reviewed as code
- one implementation-audit lens
- independent low-collision implementation slices when the host supports safe
  native parallel editing

The parent owns synthesis, source-truth updates, artifact updates, and final
claims.

Do not manually spawn separate coding-harness executables such as `codex`,
`claude`, or `agent` for ordinary acceleration.

## 5. Implement The Slice

Work through the repo's existing patterns:

- read the owning code and representative callers
- use the canonical owner path when possible
- make the smallest code change that makes the plan truth real
- delete old paths when the plan calls for replacement
- keep caller usage obvious
- move invariants into code or API shape, not developer memory
- avoid speculative abstractions and compatibility junk

## 6. Review While Warm

After a meaningful slice lands, do a plan-backed implementation review before
widening.

Use the relevant lenses from `plan-audit` implementation-audit doctrine:

- plan-code fit
- requirement traceability
- canonical owner and SSOT
- existing pattern fit
- deletion and side-door closure
- drift-proof coupling
- caller invariant state
- elegance and code-judo
- tiny-team maintainability
- changed tests as code
- docs, prompts, examples, config, or generated-artifact drift when triggered

For broad changes, split independent read-only lenses across native subagents.
For small changes, review directly.

## 7. Verify Impact

Run, assign, or reuse proof because it buys confidence, not because it exists.

Run checks when:

- the plan requires them
- changed behavior needs proof
- a caller or integration seam could break
- generated artifacts, schemas, config, prompts, docs, or examples could drift
- prior proof is stale
- review findings need proof after repair

Reuse prior proof when:

- it covers the same behavior
- nothing touched can invalidate it
- the plan does not require fresh proof
- no review finding makes it suspect

Record proof freshness and stale triggers in the implementation log.

## 8. Close The Slice

Before widening:

- update the implementation log resume snapshot
- update scope ledger status with code and proof anchors
- update audit findings if any opened or closed
- update the plan when source truth changed
- name which proof remains fresh and what would stale it
- name the next useful move

The slice is closed only when code state, plan state, review state, and proof
state agree.

## 9. Widen From Proven Ground

Add the next caller, variant, platform, mode, or polish layer only after the
core path is implemented, reviewed, and sufficiently proven.

This is the implementation version of depth-first planning: complexity is added
only after previous complexity has earned its place.

## 10. Finalize The Requested Scope

At the stop boundary:

- read the implementation log resume snapshot
- read open audit findings
- confirm in-scope plan items are closed or explicitly not closed
- run a final lightweight plan-backed implementation check over the requested
  scope
- update plan, audit log, and implementation log so they tell the same story
- report remaining gaps plainly

The final answer can stay short because the artifacts hold the detail.
