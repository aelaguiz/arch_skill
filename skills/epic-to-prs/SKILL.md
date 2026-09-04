---
name: epic-to-prs
description: "Explicit-invocation epic loop, fired only by name or direct command (\"epic-to-prs on epic 4700\"); never self-select it. Works an epic or milestone most-important-first through issue-to-pr to merge-ready PRs. Owns the live queue, persistent goal, armed $unblocker, and shared GPT-6 Pro thread. Use Pro for initial epic planning, meaningful batch checkpoints, major blockers the agent cannot resolve locally, and final review of the completed PR stack; do not duplicate plan/final consultations for every child or check in at every issue boundary. Astra owns routine decisions and verifies ordinary repairs locally. Keeps accepted scope, advisory bots, and honest review receipts; continues independent work around blockers. Never merges or releases. Not for status reads, decomposition (arch-epic), or open-ended optimization."
metadata:
  short-description: "Epic delivery with shared Pro planning and batch reviews"
---

# Epic To PRs

Use only when the user explicitly invokes this lane by name or directly
commands this exact job: work a named epic or milestone through its issues
to Pro-reviewed, merge-ready PRs. Touching an epic during other work does
not authorize this loop.

Deliver the epic's accepted scope most important first. Use `issue-to-pr`
for implementation and PR delivery, with shared Pro planning and review
across related issues. Keep delivering until the queue and required reviews
are complete, the user stops the run, or no useful unblocked work remains.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- "epic-to-prs on <epic issue or milestone>", optionally with a Pro thread.
- A /goal ask that directly commands this delivery loop over a named epic.
- "Put a goal loop over epic <N> and work it down."

Status reads do not trigger execution. If child issues do not exist,
decomposition belongs to `arch-epic` or ordinary planning. Open-ended work
without an issue queue belongs to native goal mode.

## Queue and delivery contract

- Use live GitHub state. Re-read the epic between issues; skip work that
  closed or changed owner. Follow stated priorities, otherwise use user
  impact and unblocking value and record the reasoning briefly.
- Preserve the user's accepted scope. Agents, reviewers, and bots cannot
  expand it or quietly deliver less. Decide routine ordering, dependencies,
  and scope interpretation locally with `$startup-pragmatism`.
- The run starts authorized for in-scope work. The armed `$unblocker`
  resolves self-imposed approval gates and real blockers from intent. Pro
  consultation follows the cadence below; user authority, access, or a
  change to the ask goes to the user once with a recommendation.
- Run each issue through `issue-to-pr`, carrying the shared review scope.
  Code must be self-documenting with clear comments at boundaries and role
  seams. Handle bots with judgment; they are advisory. Never merge,
  release, apply approval labels, or touch production surfaces.
- Track locally ready PRs separately from merge-ready PRs awaiting only the
  user's merge. A locally ready child may wait for a shared final review
  while the next independent issue proceeds. Do not close issues or imply
  they are merged merely because their PRs are ready.

## Shared Pro cadence

Begin with one epic planning consultation covering the goal, queue,
implementation approach, dependencies, and verification. Reuse relevant
existing Pro planning when it still covers the accepted scope. Child plans
remain on disk but do not each require another planning consultation.

Use Pro again for final review of the completed PR stack against the epic's
goal, including interactions between PRs. A small coherent epic may need
only initial planning and final review. For larger work, choose meaningful
batches or milestones that Pro can credibly assess. A checkpoint after two
related issues can be useful when their combined result exposes integration
or direction worth reviewing; there is no fixed issue count or mandatory
boundary check. Explain briefly what this checkpoint will resolve.

A batch checkpoint that reviews finished PRs can satisfy their final review;
a planning or status-only checkpoint cannot. Final epic review should focus
on the remaining changes and overall integration, using prior batch reviews
as context instead of repeating every completed child review. Review early
when a batch needs to be merge-ready before the rest of the epic.

Between these consultations, Astra reasons through routine implementation,
plan refinements, ordering, and repairs. Consult Pro for a major unexpected
blocker or consequential technical uncertainty that remains beyond the
agent's reasoning after reasonable local investigation and is likely to
change the approach. An issue boundary, dependency discovery, or ordinary
uncertainty alone does not justify a check-in. Never serialize independently
buildable issues behind an unrelated blocker.

Batch accepted Pro findings and verify ordinary corrections locally. Do
not run an automatic resubmission loop to obtain Pro approval of every edit.
Seek another consultation for substantial redesign, unresolved consequential
disagreement, or a repair
that changes the basis of the review and needs independent judgment. The
normal cadence is a baseline, not a hard cap.

Have expected edits and relevant checks finished before final review where
practical; honor an explicit request for Pro and CI in parallel. Assess
post-review changes by their effect on behavior, integration, and review
conclusions. A new SHA alone does not invalidate useful review. Consolidate
any warranted recheck, and record which revisions Pro actually saw plus
later local repairs and verification.

## Pro thread and receipts

Use one GPT-6 Pro thread for the epic, supplied by the user or created in
the applicable ChatGPT project. Keep the epic's consultations in that
thread. `$chatgpt-web` owns browser mechanics: GPT-6 Pro with Extended
thinking at the newest generation's maximum reasoning power, verified in
ChatGPT's `Chat` surface. `Work` and Ultra are not Pro.

Apply `$prompt-authoring` to every submission. Give Pro the user's intent,
accepted scope, relevant artifacts, queue and progress, believed critical
path, and the consequential questions. It should judge progress and work
against the goal, with enough context to catch drift and integration
problems. Keep one short existing-worklog entry per actual submission:
purpose, artifacts/revisions and thread, and running count. Count retries
and failover submissions; response polling is not another consultation.

If the current account is limited, follow `$chatgpt-web` to continue in the
same-named project in the other profile window with the epic context
restated. Record both thread URLs and reuse the original when available.
If both accounts are limited, report the blocked Pro decision and continue
independent authorized work. Pause the whole run only when no useful
independent work remains, and wait for the user to say Pro is back. Never
substitute another model for a required Pro review or count it as passed.

## Workflow

1. **Adopt and plan.** Read the epic, live issues, supplied Pro thread, and
   existing plans. Establish acceptance and the initial order. Write the
   plan, apply `$startup-pragmatism`, and obtain or reuse shared Pro planning.
   Identify useful reviewable batches where the work calls for them.
2. **Arm the run.** Stand up `$unblocker` with the user's ask, scope,
   production boundary, and this Pro cadence. Author the goal prompt with
   `$prompt-authoring`, including the thread, unblocker contact, queue,
   shared review scope, and completion condition. In Prime Agent, arm the
   goal and spawn the unblocker; otherwise provide the exact /goal text and
   spawn instruction. Carry user-directed cadence changes into the goal,
   charter, and active dispatch briefs during a run.
3. **Deliver issues.** Refresh the queue and run the next `issue-to-pr`
   with inherited planning and review coverage. Collect locally ready PRs
   without duplicate child Pro submissions. Resolve routine decisions
   locally or through the unblocker, use meaningful batch checkpoints and
   major-blocker consultations when warranted, and continue independent
   scope while any real user question pends. Ask once; continuations do not
   supply an answer or justify repeated questions.
4. **Review and finish.** Obtain final Pro review of the completed stack,
   using batch reviews as coverage where applicable. Resolve material
   findings and verify fixes. Every delivered issue needs Pro planning and
   final review coverage plus passing required checks before merge-ready.
   Do not mark the goal complete merely because all issues were dispatched;
   pending reviews and unresolved scope remain unfinished work.
5. **Report.** List delivered issues and PRs, current heads and CI, Pro
   review coverage and reviewed revisions, later local repairs, and the
   submission count. Name any unresolved blocker or user escalation and
   preserve the remaining queue for continuation. Complete the goal only
   when its accepted work is merge-ready or the user explicitly removed it
   from scope; otherwise report the precise incomplete state.

## Delegation

Issues may run in-session or as children. Before dispatch, read the installed
`../_shared/agent-orchestration-policy.md` and apply `$prompt-authoring` to
the populated brief. Include accepted scope, boundary comments, unblocker
contact, shared planning and review coverage, and the merge-ready terminal
state. The coordinator owns Pro submissions and the submission count;
children return artifacts and consequential questions without launching
duplicate consultations.

## References

- [references/epic-dispatch-evidence.md](references/epic-dispatch-evidence.md):
  historical epic prompts and owner corrections for maintainers.
