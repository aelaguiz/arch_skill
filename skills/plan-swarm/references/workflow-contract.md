# Workflow Contract

`plan-swarm` turns one approved plan phase into a parallel implementation loop.
It does not write a new plan or broaden the requested boundary.

## Parent Agent Owns Orchestration

- Interpret the plan phase and applicable Definition of Done.
- Recover missing execution detail from owning code, tests, schemas, generated
  artifacts, and current behavior.
- Write the phase contract and swarm ledger next to the plan.
- Use `$agent-delegate` to launch and resume implementation workers.
- Write worker, arbiter, and repair prompts with prompt-authoring discipline.
- Put this line in every implementation, repair, verification, arbiter, and
  consult child prompt: `Maximize parallelism by using parallel agents. Do not
  invoke skills that spawn subagents.`
- Inspect worker reports, changed files, and proof after every batch.
- Batch review, test, integration, and worker findings before dispatching
  follow-up work.
- Decompose accepted findings into delegated repair and verification waves.
- Maintain an impact-aware verification map: plan-required checks, changed
  surfaces, plausibly affected adjacent behavior, scarce resources, proof
  already passing, and the reason each proof should run or stay trusted.
- Commit local progress checkpoints freely, including dirty inherited work that
  looks like resumed plan work.
- Coordinate expensive validation so workers do not stampede the same resource.
- Decide whether a review finding is accepted, rejected, or deferred.
- Decide whether to resume a worker, spawn fresh, pause, or ask the user.

## Coordination Shape

Parallelism is part of the parent agent's normal work: reason about
independence, launch workers with the existing delegation skill, inspect the
real worktree, and keep a human ledger. Any optional helper belongs below that
judgment layer as a narrow utility, such as a blank ledger template or stale
wording check.

The parent should not collapse into a solo implementation or test-rerun loop.
It may read files, inspect diffs, run cheap status/search commands, and give
workers strong hints. Source edits, repair implementation, and implementation
verification normally go to delegated workers.

## Lifecycle

1. Intake: plan path, phase, stop boundary, work root, implementation policy,
   review policy, and max parallelism.
2. Initial/resume checkpoint: inspect `git status` and commit tracked changes
   plus likely relevant untracked files before worker launch. Skip only
   concrete safety issues such as secrets, obvious machine-local junk, or files
   clearly unrelated to the repo.
3. Phase contract: source-of-truth requirements and proof obligations.
4. Swarm ledger: independent/dependent slices, likely collisions, scarce
   resources, assigned workers, session ids, and impact-aware proof needed.
5. Implementation batches: launch independent slices in parallel through
   `$agent-delegate`.
6. Merge/evidence checkpoint: read worker reports, inspect repo state, and
   commit meaningful landed progress.
7. Arbiter loop: delegated observation-only review against the phase contract.
8. Thermonuclear gate: strict maintainability review and triage.
9. Repair wave: batch accepted findings by owner, dependency, collision risk,
   proof needed, and worker session; delegate the resulting repair slices.
10. Verification wave: assign plan-required and impact-justified tests, builds,
    generators, simulators, browsers, or device checks to workers with leases
    when needed. Do not rerun broad default suites without a concrete plan,
    impact, review, or stale-proof reason.
11. Repair checkpoint: commit accepted repair-wave results after delegated
    verification.
12. Final report: evidence, findings, remaining gaps, final local commit
    checkpoint, and stop at boundary.

## Recursive Swarm Loop

Use the same swarm shape for follow-up work:

```text
implementation wave
-> parent inspection and report intake
-> delegated review or verification
-> finding triage
-> batched repair-wave decomposition
-> delegated repair workers
-> delegated verification workers
-> checkpoint commit
-> repeat until the phase contract is covered or findings are rejected/deferred
```

Do not dispatch one tiny repair at a time when a broader batch is available.
Do not turn test failures into parent-owned test reruns. The parent's job is to
keep the queue shaped, parallel, and evidenced.

## Verification Posture

Verification should buy confidence, not burn time. Start from the plan's
validation obligations and Definition of Done, then ask what the changed and
adjacent impacted surfaces need to prove. Prefer targeted proof, slice-local
checks, and delegated verification workers over broad default runners.

Keep already-passing proof in the ledger. Do not rerun it in later phases or
waves unless new changes could affect it, the plan explicitly requires fresh
proof, or a reviewer/test result makes it stale. A broad suite is still valid
when the phase changes shared infrastructure, cross-cutting behavior, generated
contracts, or a release gate that the plan names; record that reason instead of
using "run everything" as the default.

## Git Posture

Local commits are normal plan-swarm checkpoints, not polished PR history. Bias
toward getting useful work committed instead of pausing for Git ceremony. The
user can squash, reorder, or clean commits before opening a PR.

The parent agent owns commits by default. Parallel workers should not race to
commit unless the parent explicitly assigns one worker a commit checkpoint.
Never push, open PRs, stash, or revert unrelated work unless the user asks for
that exact operation.

## Stop Discipline

- Stop after the named phase unless the user asked for a phase range or whole
  plan.
- Whole-plan final review is only for whole-plan completion or explicit final
  signoff.
- Do not use worker success footers as completion proof by themselves.
