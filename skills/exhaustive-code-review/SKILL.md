---
name: exhaustive-code-review
description: "Explicitly selected code review where systematic coverage is part of the deliverable: every applicable check in the bundled review catalog is accounted for, with a findings artifact on disk. When the user names a worker type or count, divides the catalog slices among that many clean native review children and keeps verification and the verdict in the parent. Use when the user chooses $exhaustive-code-review or binding task instructions require it. An ordinary code review or completion check does not select this workflow."
metadata:
  short-description: "Exhaustive catalog-driven code review saved to disk"
---

# Exhaustive Code Review

Use this workflow only after explicit selection as `$exhaustive-code-review` or a
binding task instruction requiring it. The job is to review the requested scope
against the bundled review catalog, account for every check that applies, save
the review artifact to disk, and report the verdict plus path.

The catalog is divided into slice files of a few checks each. A parent reviewer
decides which slices apply, reads them itself or hands them to child reviewers,
verifies every reported finding against the code, and owns the verdict. When the
user names a worker type or a count ("use 12 sonnet agents"), the slices are
dealt across that many children of exactly that type.

This skill does not dictate the user's workflow. It does not implement, repair,
commit, push, open PRs, route repair waves, run an external review subprocess,
or decide what workflow the user should use next.

## Use When

- The user asks for exhaustive, meticulous, line-by-line, file-by-file,
  abstraction-by-abstraction, feature-by-feature, or coverage-ledger code
  review.
- The user wants a full branch, current diff, commit range, explicit path set,
  or completion claim reviewed with every relevant touched surface accounted
  for.
- The user wants the review spread across a named number or type of cheaper
  review agents.
- The user specifically cares about split-brain abstractions, bypassed
  centralized owners, partial migrations, side doors, unrequested behavior,
  swallowed failures, stale docs/prompts/generated artifacts, or proof that
  tests the wrong thing.

## Do Not Use When

- The user wants a normal high-signal general review. Use the host agent's
  normal review response.
- The user wants implemented code reviewed mainly against a plan artifact. Use
  `plan-audit implementation-audit`.
- The user wants only a harsh maintainability pass. Use
  `thermo-nuclear-code-quality-review`.
- The user wants an external Codex/Claude/Cursor second opinion. Use the
  appropriate consult or delegation skill.
- The user wants fixes, implementation, PR shipping, or workflow orchestration.

## Non-Negotiables

- Review only. Do not edit reviewed files. By default nobody runs the
  project's build, test suite, code generators, or dependency installs, parent
  or child; a check that needs a run is recorded as could not evaluate, with
  what would have to be run. When the user says running the code is okay, the
  parent and children may run what a check needs, and `coverage.md` records
  what ran and what it left in the tree.
- Save the review artifact under `/tmp/exhaustive-code-review/<slug>-<timestamp>/`.
- Apply `../_shared/agent-orchestration-policy.md` whenever the review uses
  child agents.
- Coverage is led by the catalog. Every slice whose inputs are present in the
  target is applied, by the parent or by exactly one child per cell, and every
  applied check ends as finding, clean, or could not evaluate.
- Honor a named worker type exactly. If this host cannot start a native child of
  that type, stop before dispatch and say which types it can start. Never
  substitute a model or effort silently.
- Start every child as a new clean same-host native child, keep cells
  non-overlapping, and bound fanout by host slots, shared-file or shared-state
  collision risk, and parent integration capacity.
- Use the strongest read-only capability the host exposes, also tell every
  review child not to edit or write, and have the parent compare repository
  status and diffs with the pre-dispatch state before accepting child evidence.
- Children do not start other agents of any kind.
- Reviewers, parent and children, search only inside the target repository and
  only narrowly: the changed files, their neighbours, and the exact symbols a
  check names, with `git grep` at head for a single identifier when the whole
  repository must be consulted. No filesystem-wide or home-directory scans, no
  recursive scan of the tree for a common word with any tool (`find`, `rg`,
  `grep -r`, `fd`), no repeated whole-tree scans. The machine is shared.
- A child's report is evidence. The parent opens the code for every reported
  finding and accepts, rejects, or merges it before it enters the artifact. The
  parent owns child accounting, deduplication, finding scope disposition, the
  artifact, and the final verdict.
- Do not pass the parent's suspicions or an expected outcome into a child brief.
- Do not manually spawn `codex`, `claude`, `agent`, or other coding-harness
  executables.
- Do not invoke external agent/delegation/review skills as the review mechanism.
- Do not build a rule engine, runner, controller, scorer, harness, or script,
  and do not reduce a catalog check to matching words.
- Read repo truth directly: changed files, local instructions, relevant callers,
  owners, tests, docs, schemas, generated artifacts, prompts, examples, and
  configs.
- Findings must be concrete. Drop style preferences, generic advice, pedantic or
  hypothetical items, and "maybe centralize this" comments unless they name real
  changed-code risk.
- Competing-path, side-door, stale-truth, and competing-owner detection is
  default review behavior, not a special mode. If a live duplicate path affects
  the requested scope, treat it as a required repair unless the review can name
  the genuinely different contract or controlling out-of-scope anchor. For a
  fixed-scope plan or history-backed change, apply
  `../_shared/scope-and-convergence.md`: a reviewer-discovered adjacent path
  cannot enter repair scope. Require subtraction or redesign inside the approved
  boundary, or stop for an explicit human scope decision.
- A clean review is allowed. Do not invent findings to justify the run.

## First Move

1. Resolve the requested review target from normal language: current worktree,
   branch diff, commit range, explicit paths, or completion claim. Note what
   else the target includes: the request or issue, a PR description, run
   evidence, screenshots.
2. Read local instructions and nearby review-relevant conventions.
3. Create the run directory under `/tmp/exhaustive-code-review/`.
4. Read `references/review-catalog.md`, the index of every slice and check.
5. Read `references/checker-rules.md`.
6. Read `references/output-contract.md`.
7. If children will be used, read `references/swarm-slicing.md` and
   `../_shared/agent-orchestration-policy.md` before creating or resuming any
   child.
8. For a fixed-scope plan or history-backed change, read
   `../_shared/scope-and-convergence.md`.

## Workflow

1. Build the review target summary and save it as `target.md`.
2. Map the changed files, changed hunks, touched symbols, touched abstractions,
   visible features or behavior obligations, and likely adjacent surfaces.
3. Decide which catalog slices apply to this target and record the ones that do
   not, with the missing input.
4. Without children, read each applicable slice file and apply its checks
   yourself. With children, divide the slices into cells and brief the children
   as `references/swarm-slicing.md` describes. In Codex use
   `fork_turns: "none"`; in Claude use a clean named or custom subagent rather
   than an ambiguous conversation fork or skill `context: fork` shorthand.
5. Review every touched file and changed hunk. Read surrounding code when the
   hunk depends on a function, class, module, caller, lifecycle, or contract.
   The catalog directs attention; it does not replace reading the change.
6. Review touched abstractions and competing ways to accomplish the same goal:
   canonical owner, old and new paths, callers, readers, writers, side doors,
   duplicate helpers, command aliases, generated artifacts, docs, prompts,
   examples, and tests. Classify each in-scope competing path as a required
   repair, observation, genuinely different contract, or named out-of-scope
   follow-up. When scope is signed off, classify every material finding against
   its human-scope or pre-approval convergence anchor before naming a repair;
   review discovery is not scope authority.
7. Review touched behavior against the request: entrypoints, success paths,
   failure paths, state, persistence, user-visible or externally observable
   effects, and proof.
8. Verify every reported finding against the code and the catalog entry. Apply
   the quiet conditions in `references/checker-rules.md` and each entry's own
   counter-cases. When the change fixes or contains a failure, apply C-17
   yourself as well, whatever the children returned: can the thing that failed
   still fail, and does the change name its cause? Sort what remains into required repairs and observations. A
   verified finding stays a required repair when the request's own terms are
   unmet at head; do not downgrade it because a later step, another owner, or a
   follow-up could address it. Name the decision the requester would have to
   make instead of making it.
9. Save `coverage.md`, `findings.md`, and `verdict.md`.
10. Return a short findings-first answer with the verdict and run directory.

## Output Expectations

The final chat reply includes:

- verdict: `approve`, `not-approved`, or `coverage-incomplete`
- required repairs, if any
- observations, if material
- run directory path
- one next action from the review, not a workflow prescription

The full saved artifact follows `references/output-contract.md`.

## Reference Map

- `references/review-catalog.md` - index of every catalog slice: its checks,
  the question each answers, and the inputs it needs; read on every run
- `references/catalog-*.md` - the slice files: for each check, what to read and
  compare, when to block, when not to, and example findings; read the slices
  that apply, or hand them to children
- `references/checker-rules.md` - how any reviewer applies a check, when every
  check stays quiet, and the return shape; read on every run and by every child
- `references/swarm-slicing.md` - applicable slices, cells, dealing cells to a
  named number or type of children, the child brief, and parent verification;
  read when children are used
- `references/output-contract.md` - required saved files, verdicts, finding
  shape, and final chat summary shape
- `../_shared/agent-orchestration-policy.md` - transport, starting context,
  continuation, isolation, topology, and parent-integration policy
