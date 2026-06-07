---
name: plan-swarm
description: "Prompt-first implementation swarm orchestrator for finishing a named phase or phase range from an existing plan document. The parent extracts the phase contract, decomposes independently delegable slices, runs/resumes parallel workers through agent-delegate, batches review/test findings into delegated repair and verification waves, commits checkpoints, writes worklogs, and gates closure through arbiter plus thermonuclear review. Do NOT use for creating plans, one-shot delegation, strict ordered processes, review-only work, pushes, PRs, or worktrees."
metadata:
  short-description: "Parallel plan-phase implementation orchestrator"
---

# Plan Swarm

Use this skill when the user wants to implement an existing plan document faster
by splitting one approved phase into independent work slices, running capable
implementation workers in parallel, and holding phase closure behind real
review and proof.

`plan-swarm` exists to maximize implementation velocity without lowering code
quality. Its default posture is to find safe parallelism, keep workers moving,
remove avoidable serial bottlenecks, and reserve serial execution only for real
dependency, collision, or scarce-resource constraints.

This is a prompt-first orchestration skill. The parent agent is the
orchestrator: it reasons about the phase, launches and resumes workers through
existing capabilities such as `$agent-delegate`, inspects the real worktree,
keeps the human worklogs current, and commits local progress checkpoints
without treating Git history as PR-ready.

## North Stars

- The job is batching, delegation, and parallelization. `plan-swarm` should make
  plan execution faster than a normal single-agent implementation loop.
- The parent is the scheduler, triager, worklog owner, scarce-resource
  coordinator, and commit checkpoint owner.
- Workers are the implementers, repairers, and verification runners.
- After reviews, test failures, integration failures, or worker blockers, the
  parent batches the work, decomposes it again, and sends it back out to
  workers instead of becoming the coder or test runner.
- Parent diagnosis is useful context, not a script. Give workers likely fix
  paths and evidence hints, then let them own implementation judgment.

## Use When

- The user names an existing plan doc and asks to finish one phase quickly.
- A plan phase has independent owner surfaces that can be delegated in
  parallel.
- The user asks for Codex GPT/GBT, Claude Opus, Cursor Composer, or Grok
  workers to implement plan slices.
- A phase needs an external arbiter and strict maintainability pass before it
  can be called done.

## Do Not Use When

- The plan does not exist yet. Use `$arch-step`, `$miniarch-step`, or
  `$arch-mini-plan`.
- The work is a multi-plan epic decomposition. Use `$arch-epic`.
- The workflow is a strict ordered process from another repo's doctrine. Use
  `$stepwise`.
- The user only wants one child worker. Use `$agent-delegate`.
- The user only wants a review or second opinion. Use `$fresh-consult`, ordinary
  host review, or a named review skill.
- The user wants worktrees, pushes, PRs, or detached workers. Those are not v1
  defaults and require an explicit separate ask.

## Non-Negotiables

- One active phase or explicit phase range at a time.
- The plan doc remains source of truth. The swarm ledger is schedule and
  evidence, not a second plan.
- Stop at the requested boundary. Do not continue into final-pack signoff when
  the user asked for one phase.
- When the user chooses Cursor Agent for implementation, Composer 2.5 means
  `composer-2.5-fast`; accept `composer`, `composer 2.5`, `composer-2.5`, or
  bare `2.5` in Cursor Agent context as that model.
- When the user chooses Grok for implementation, plain Grok means
  `grok-build`; Grok Composer means `grok-composer-2.5-fast`.
- Implementation and review policy are independent. Cursor implementation does
  not make review run through Cursor, and Grok implementation does not make
  review run through Grok.
- Provider routing is fixed: Codex runs GPT/GBT/OpenAI models, Claude Code runs
  Opus, Cursor Agent runs only `composer-2.5-fast`, and Grok CLI runs
  `grok-build` or `grok-composer-2.5-fast`.
- Arbiter, consult, and review work must use Codex GPT/GBT or Claude Opus.
  Do not pass GPT/GBT, Claude, Cursor Agent, or Grok model ids across runtimes.
- Workers are prompted like capable engineers, not micromanaged checklist
  executors.
- Every child prompt, including implementation, repair, verification, arbiter,
  and consult prompts, tells the child: "Maximize parallelism with native
  subagents or parallel-agent features provided by your current coding harness.
  Do not manually spawn separate coding-harness executables, or invoke skills
  whose main effect is to shell out to `codex`, `claude`, `agent`, or `grok`,
  from inside this child prompt unless the parent explicitly assigns that
  action."
- The parent commits freely. If the run inherits a dirty worktree, assume it is
  likely resumed plan work and create an initial checkpoint unless there is a
  concrete safety issue such as secrets, obvious machine-local junk, or files
  clearly unrelated to the repo.
- Commit after meaningful worker batches, accepted repair waves, review cleanup,
  and final phase reporting. Prefer a messy local checkpoint over blocking on
  Git ceremony; the user can squash, reorder, or clean history before a PR.
- Parent owns commits by default. Workers do not push, stash, revert unrelated
  work, or independently commit unless the parent explicitly assigns one worker
  a commit checkpoint.
- Parent coordinates scarce verification resources; workers do not all run the
  full suite at once.
- Parent assigns verification to workers. It may inspect state with cheap
  read-only commands, but it should not become the normal runner for tests,
  builds, generators, simulators, browsers, or devices.
- Verification is impact-aware. Start from the plan's stated validation
  obligations, then add proof for changed and plausibly impacted surfaces. Do
  not run every default test just because it exists.
- Track already-passing proof across phases and waves. Rerun it only when new
  changes could affect that proof, when the plan explicitly requires fresh
  proof, or when review/verification evidence calls it stale.
- Parent gives periodic and user-requested Markdown table updates from the
  swarm ledger so the user can see phase progress, current chunks, active
  workers, and current difficulties at a glance.
- Do not rush to abandon quiet workers. Large slices, high-thinking models,
  long tests, sleeps, simulators, and scarce-resource waits can go quiet; short
  silence is not a stall.
- Related repairs resume the same healthy worker session by default.
- Arbiter review is delegated and observation-only.
- Thermonuclear maintainability review is required before phase closure unless
  the user explicitly disables it.
- Reviews and verification should try to produce a useful batch of phase-scope
  findings, not stop after the first issue.
- Accepted findings become delegated repair or verification slices. Rejected or
  deferred findings need a recorded scope or evidence rationale.
- Parent edits coordination artifacts; workers edit source code and run assigned
  verification unless the user explicitly overrides the swarm doctrine.
- Never claim completion from worker self-certification alone.

## First Move

1. Read `references/workflow-contract.md`.
2. Read `references/phase-contract.md`.
3. Read `references/decomposition-and-scheduling.md`.
4. Resolve the plan path, active phase, stop boundary, work root,
   implementation policy, review policy, and max parallelism.
5. Read the active phase plus plan-level Definition of Done items relevant to
   owner boundaries, validation, persistence, cleanup, and review.
6. Extract the plan-required validation obligations and draft an impact-aware
   verification map before launching workers.
7. Inspect `git status` and commit an initial/resume checkpoint for tracked
   changes and likely relevant untracked files before launching workers.
8. Write a compact phase contract and swarm ledger next to the plan before
   launching workers.
9. Send the first progress update with the required tables.
10. Launch independent workers with `$agent-delegate`, then keep the ledger,
   worklogs, session ids, proof, and review triage current by hand.

## Workflow

1. Extract the phase contract from the plan and repo evidence.
2. Decompose into slices by owner boundary, dependency, proof, cleanup, and
   scarce-resource boundaries.
3. For each slice, identify the proof target: plan-required tests, changed
   surfaces, impacted adjacent behavior, scarce resources, and already-passing
   proof that should not be rerun unless affected.
4. Launch as many independent slices in parallel as the worktree and resource
   constraints can safely support.
5. After each batch, inspect worker reports, changed files, resource use, and
   repo state with cheap parent-side inspection before launching more work.
6. When worker results, reviews, tests, or integration expose gaps, gather a
   useful batch, triage it, decompose accepted gaps into repair or verification
   waves, and delegate those waves back to workers.
7. Commit local progress after meaningful worker, repair, or verification
   batches, and record checkpoint hashes in the ledger.
8. Update the ledger and send a table update whenever workers launch, finish,
   block, retry, hit an issue, or move into review/repair.
9. Route valid gaps back to workers, usually by resuming the related session.
10. Launch an observation-only arbiter to compare implementation against the
   phase contract and architectural cleanliness.
11. Run thermonuclear maintainability review. Triage findings as accepted,
   rejected, or deferred.
12. Delegate accepted findings and verification reruns until the phase contract
    is covered, then write the final phase report, commit the final phase
    checkpoint, and stop at the requested boundary.

## Progress Updates

Give concise Markdown table updates after phase-contract creation, after each
worker batch launches or finishes, after review gates, and before final report.
When the user asks for an update, status, what is running, what is blocked, or
where the phase stands while `plan-swarm` is active, answer with the same table
format. Refresh from the swarm ledger, worker logs, current repo state, and
known child-session results before answering. Do not fake precision: percent
is a judgment estimate backed by evidence.

Each update includes:

- `Phase Progress`: `Phase`, `Scope`, `%`, `Status`, `Evidence`, `Note`
- `Current Phase Work Slices`: `Slice`, `Goal`, `Worker`,
  `Parallelization`, `Status`, `Proof`
- `Workers Now`: `Worker`, `Runtime/Model`, `Slice`, `State`,
  `Current Task`, `Session`
- `Phase Difficulties And Retries`: `Issue`, `Where`, `Impact`,
  `Retry/Response`, `Current State`, `Next Action`

Use the difficulties table for blockers, failed or struggling workers, review
findings, test failures, merge/collision trouble, scarce-resource contention,
unclear ownership, and repeated retries. If no difficulty is known yet, include
one `none observed` row instead of omitting the table.

Percent guidance:

- `0%`: not started
- `10-30%`: contract and decomposition underway
- `40-70%`: implementation slices actively landing
- `80-90%`: implementation done; review, verification, or repair in progress
- `100%`: contract covered, accepted findings repaired or triaged, proof
  recorded, and stop boundary honored

## Output

Report compactly:

- active phase and stop boundary
- progress tables when a phase, batch, review, or final-report boundary changes
- the same progress tables when the user manually asks for an update during a
  `plan-swarm` run
- implementation and review policies
- implementation, repair, verification, and review slices launched, completed,
  blocked, or waiting
- difficulties, retries, issues, and next recovery action
- delegated verification commands, impact rationale, already-passing proof kept,
  and proof gaps
- arbiter and thermonuclear findings triage
- files changed, worklog paths, and commit checkpoints
- next action

## Reference Map

- `workflow-contract.md` - parent-agent lifecycle and stop discipline
- `phase-contract.md` - how to extract the active phase without inventing scope
- `decomposition-and-scheduling.md` - parallel slice design and launch judgment
- `worker-prompt-contract.md` - implementation worker prompt shape and footer
- `arbiter-and-review.md` - delegated arbiter, thermonuclear gate, and triage
- `resource-leases.md` - scarce verification resources
- `session-reuse.md` - when to resume or respawn workers
- `run-state-and-artifacts.md` - human worklog layout and ledger expectations
- `examples.md` - compact orchestration and worker prompt examples
