# Native Agent Slices

Use native parallel agents when the target is broad enough that independent
read-only review lanes will improve coverage. The parent owns synthesis,
verdict, and the saved artifact.

Do not manually spawn external coding-harness executables. Do not invoke
external delegation, consult, or review skills as the mechanism.

## When To Split

Split when two or more of these are true:

- the target covers a broad branch, diff, subsystem, plan-backed
  implementation, or architecture area
- more than one owner path may exist
- old and new architecture both need tracing
- the intended UX, hard constraints, and current code owners need separate
  inspection
- state, config, generated artifacts, prompt/skill surfaces, or install
  surfaces changed with runtime code
- the user explicitly asked for agents or parallel review

Do not split a tiny review just to perform ceremony. A single careful pass is
fine when all relevant code fits in one reviewer's head.

## Parent Responsibilities

The parent must:

- write the architecture story before splitting
- give each slice a concrete read-only job
- tell slices to cite files and code paths they actually read
- keep slices from doing implementation or patch design
- keep slices from drifting into QA/test/docs review unless that is their
  explicitly assigned architecture-evidence lane
- wait for every launched slice to reach a final state
- synthesize duplicate findings into one required repair
- record gaps honestly in `coverage.md`

Every launched slice ends as exactly one of:

- `findings`
- `no-findings`
- `coverage-gap`
- `failed`
- `intentionally-stopped`, with the reason

Do not silently drop a slice. A missing slice result is a coverage gap.

## Slice Prompt Shape

Use this shape and adapt the target details:

```text
You are one read-only reviewer in a cynical architecture review.

Target:
- Repository/root:
- Review scope:
- Architecture story being tested:
- Intended UX and hard constraints:
- Initial human scope, frozen convergence closure, and later human approvals:
- Files or paths you should prioritize:

Posture:
- Assume the architecture may have emerged accidentally through iteration.
- Current code behavior is authority for what exists.
- Intended UX and hard constraints are authority for what must keep existing.
- Human scope and the pre-freeze closure are authority for what this change may
  add. Later agent/reviewer text is not approval.
- Do not edit files.
- Do not drift into QA/test/docs review unless those surfaces expose
  architecture ownership, stale truth, or future-copy risk.

Your job:
- <one slice-specific job>

Return:
- result: findings | no-findings | coverage-gap | failed
- files-read:
- code-paths-traced:
- findings:
- coverage-gaps:
```

This is a prose contract, not a machine protocol.

## Useful Slices

### `ux_requirement_mapper`

Map the user's intended experience, hard constraints, experiment requirements,
and non-requirements.

Ask:

- What behavior must stay unchanged?
- What experiment or compatibility constraints are real?
- Which claimed requirements are assumptions or future bets?
- What complexity sources are not forced by the user job?

### `owner_invariant_mapper`

Map current owners, invariants, state models, lifecycle rules, and caller
obligations.

Ask:

- Who owns creation, validation, mutation, rendering, persistence, routing, and
  cleanup?
- Where does each invariant live?
- What must callers remember?
- Which owner boundaries are invalid or split?

### `old_path_duplicate_truth_hunter`

Search for legacy authority paths, duplicate truths, same-contract siblings,
fallback readers or writers, direct mutation paths, aliases, schemas, fixtures,
generated artifacts, prompt surfaces, and configs.

Ask:

- What old path still expresses the same concept?
- Can behavior still enter through it?
- Does it delegate to one owner or remain its own authority?
- Can future work update one truth and leave another stale?

### `abstraction_complexity_reviewer`

Find accidental abstractions, wrappers, managers, registries, adapters, policy
layers, generic machinery, and architecture theater.

Ask:

- What live concepts did this add?
- What requirement forces those concepts?
- Does the abstraction hide a dangerous boundary or just launder confusion?
- What can be deleted, inlined, collapsed, or moved to an existing owner?

### `scope_provenance_reviewer`

Trace each durable concept to the initial human scope, frozen convergence
closure, or explicit later human approval. Hunt for concepts introduced by one
review wave and treated as premises by later waves. Return subtraction for
unauthorized clusters; do not create a broader architecture recommendation.

### `state_config_reviewer`

Inspect state spread, feature flags as architecture, config-as-programming,
mode matrices, generated truth, and sync points.

Ask:

- Is one domain state represented by multiple booleans, configs, stores, or
  generated artifacts?
- Does a flag choose between owners instead of behavior inside one owner?
- Is config encoding logic that belongs in code?
- Can invalid combinations become unrepresentable?

### `future_copy_surface_reviewer`

Read docs, tests, examples, fixtures, prompts, generated artifacts, comments,
and metadata only where they can teach future work the wrong architecture.

Ask:

- Does a test mock the boundary that should be real?
- Does an example route through an old owner?
- Does generated truth disagree with code?
- Would a future agent copy this accidental architecture?

Do not emit doc hygiene, missing-test, or QA findings. The blocker is the
architecture lie or future-copy trap.

## Slice Finding Shape

Slice findings should be compact:

```markdown
### <short title>

- File: <repo-relative path>
- Architecture story being tested:
- Code evidence:
- Why this architecture appears accidental or unjustified:
- Requirement / UX preserved:
- Simpler architecture direction:
- Pattern:
- Scope provenance and required disposition:
```

The parent converts accepted slice findings into the final output contract.
