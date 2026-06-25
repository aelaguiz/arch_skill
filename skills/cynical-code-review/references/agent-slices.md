# Native Agent Slices

Use native parallel agents when the target is broad enough that independent
read-only review lanes will improve coverage. The parent owns synthesis,
verdict, and the saved artifact.

Do not manually spawn external coding-harness executables. Do not invoke
external delegation, consult, or review skills as the mechanism.

## When To Split

Split when two or more of these are true:

- the target covers a branch, broad diff, phase, or completion claim
- more than one authority path may exist
- old and new code paths both need tracing
- user workflow and proof/status surfaces need separate inspection
- prompt, skill, generated, config, or install surfaces changed with runtime
  code
- the user explicitly asked for parallel agents

Do not split a tiny review just to perform ceremony. A single careful pass is
fine when all relevant code fits in one reviewer's head.

## Parent Responsibilities

The parent must:

- write the implementation story before splitting
- give each slice a concrete read-only job
- tell slices to cite files and code paths they actually read
- keep slices from doing implementation or patch design
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
You are one read-only reviewer in a cynical implementation-integrity review.

Target:
- Repository/root:
- Review scope:
- Implementation story being tested:
- Files or paths you should prioritize:

Posture:
- Assume names, comments, docs, tests, status, and wrappers may be misleading.
- Current code behavior is authority.
- Do not edit files.
- Do not propose broad refactors unless they are needed to make a false
  implementation story true.

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

### `claim_mapper`

Map the user's completion claim, implementation story, or plan intent to code
obligations.

Ask:

- What exactly is claimed to be true?
- What code paths would have to exist for that claim to be real?
- Which due obligations are not traceable to current code?
- Did the claim narrow the user's intended done state?

### `old_path_hunter`

Search for legacy authority paths, aliases, fallback readers or writers,
commands, routes, schemas, prompts, generated artifacts, fixtures, configs, and
direct mutation paths.

Ask:

- What old path still expresses the same concept?
- Can user-visible behavior still enter through it?
- Does it delegate to the new owner, or does it remain its own authority?

### `runtime_flow_tracer`

Trace actual control flow and data flow from entrypoint to owner.

Ask:

- What happens at runtime, not just by name?
- Which owner reads, writes, validates, renders, persists, or routes the
  concept?
- Do success, failure, retry, refresh, and cleanup paths use the same owner?

### `split_brain_hunter`

Find duplicate owners, duplicate state, duplicate schema, duplicate prompt
doctrine, same-contract siblings, or two generated truths.

Ask:

- Can callers choose between two ways to be right?
- Can future work update one truth and leave another stale?
- Is the bridge explicit and owned, or implicit and fragile?

### `user_job_reviewer`

Check whether the code supports the user's actual job from the starting state
that matters.

Ask:

- What is the user's job in plain English?
- Can the user complete it from empty, legacy, silent, missing, errored, or
  otherwise relevant starting state?
- Did the implementation support only a narrower internal job?

### `overbuild_scope_reviewer`

Find overbuilt machinery, fake abstractions, policies, harnesses, flag systems,
scope contamination, and adjacent behavior drift.

Ask:

- Did the implementation add concepts without making the target behavior true?
- Did a small fix become a policy?
- Did adjacent behavior change outside the request?

### `proof_surface_reviewer`

Read changed tests, docs, worklogs, examples, comments, prompts, logs, status
blocks, generated artifacts, package metadata, and install docs only where they
claim code truth.

Ask:

- Does the proof prove the wrong thing?
- Does a status/doc/test surface hide a code gap?
- Does it teach a live old path?
- Would a future agent trust a false surface?

## Slice Finding Shape

Slice findings should be compact:

```markdown
### <short title>

- File: <repo-relative path>
- Claim being tested:
- Code evidence:
- Why this means the implementation story is false or incomplete:
- Repair target:
- Pattern:
```

The parent converts accepted slice findings into the final output contract.
