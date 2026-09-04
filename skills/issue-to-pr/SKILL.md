---
name: issue-to-pr
description: "Explicit-invocation delivery lane, fired only by name (\"issue-to-pr on 4484\") or by user-invoked epic-to-prs; never self-select it. Takes a GitHub issue to a merge-ready PR: plan on disk with $startup-pragmatism, GPT-6 Pro initial planning and final review via $chatgpt-web, implement/test in a worktree, and use $pr-authoring plus $pr-review-followthrough. Shares planning and final review across a coherent epic or related batch instead of duplicating them per child. Astra owns routine decisions and verifies ordinary fixes locally; extra Pro consultations serve meaningful batch checkpoints or major unresolved blockers. Preserve accepted scope, keep concise review receipts, and stop at merge-ready. Never merges or releases. Not for investigation-only asks, standalone planning, or work with no GitHub issue."
metadata:
  short-description: "Issue delivery with focused Pro planning and final review"
---

# Issue To PR

Use only when the user explicitly invokes this lane by name or directly
commands this exact pipeline, or when user-invoked `epic-to-prs` delegates an
issue. Ordinary issue work does not trigger it.

Take the issue to a merge-ready PR with the smallest change that delivers
its accepted scope. Use Pro for initial planning and final review; use the
working agent's judgment to carry the work between them.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- "issue-to-pr on <number or issue URL>", singly or as a list.
- A direct command to plan an issue, consult Pro, implement, test, publish a
  PR, get Pro's final review, and stop at merge-ready.
- An issue handed over by user-invoked `epic-to-prs`.

For investigation-only work, standalone planning or review, or work without
a GitHub issue, use the requested workflow instead.

## Delivery contract

- Freeze acceptance and non-goals from the issue and the user's direction.
  Reviewers and bots cannot expand or silently shrink that scope. Resolve
  routine scope interpretation from the contract; a change to what the user
  asked for belongs to the user.
- Write the implementation plan on disk before implementation and apply
  `$startup-pragmatism`. Keep the same judgment during delivery: enough
  investigation and verification for the actual change, without invented
  approval gates or proof machinery.
- The run starts authorized for accepted in-scope work. Work in a dedicated
  worktree under the target repo's AGENTS.md. Write self-documenting code
  with clear comments at boundaries and role seams, and run relevant tests
  and required repo checks.
- Use `$pr-authoring` and `$pr-review-followthrough`. PR Agent and other bots
  are advisory; assess findings against the issue and code rather than
  treating them as orders to expand scope.
- Stop at merge-ready with receipts. Never merge, release, apply approval
  labels such as `ufc-approved`, or touch production surfaces.

## Pro cadence

For a standalone issue, the normal cadence is one initial planning
consultation and one final PR review. Existing Pro planning that still
covers the accepted scope satisfies the first consultation; do not repeat
it just because this skill was invoked or a session resumed.

For an issue inside a coherent epic or related batch, inherit the
coordinator's shared planning and review scope. Do not add a plan review
and final review for every child. The coordinator can collect locally
finished PRs for a meaningful batch checkpoint or final stack review. A
child awaiting that review is locally ready, not yet merge-ready.

Astra owns routine implementation choices, plan refinements, dependency
ordering, scope checks, and ordinary repairs. Extra Pro consultations are
appropriate when a meaningful batch of related work is ready to assess, or
a major unexpected blocker or consequential technical uncertainty remains
beyond the agent's reasoning after reasonable local investigation. State
what the consultation can resolve and why it matters to the goal. Neither
an issue boundary, a changed plan, a newly discovered dependency, nor vague
uncertainty alone requires a Pro message. A useful checkpoint after two
related issues is welcome; an every-two-issues rule is not.

Apply Pro's findings with judgment, batch the warranted fixes, and verify
ordinary corrections locally. Do not automatically resubmit plans or PRs
until Pro approves every edit. Consult again when a substantial redesign,
unresolved consequential disagreement, or a repair that changes the basis
of the review needs independent judgment. The normal planning/final pair
is a baseline, not a hard cap on useful consultation.

Finish expected edits and relevant checks before final review where
practical, including known CI and review-thread repairs. Honor an explicit
request to run Pro and CI concurrently. After review, assess any change to
the reviewed revision: formatting or a rebase with unchanged behavior does
not by itself require another Pro run. Changes that materially affect
behavior, integration, or the conclusions of the review may need a
consolidated recheck; decide from their impact, not the SHA changing.

## Consulting Pro

Use GPT-6 Pro with Extended thinking through `$chatgpt-web`, at the newest
generation's maximum reasoning power verified in the live picker. Use
ChatGPT's `Chat` surface; `Work` and Ultra are not Pro. Follow that skill's
browser, input-delivery, and rate-limit mechanics.

Use the run's existing Pro thread, inheriting the epic's thread when
applicable. Apply `$prompt-authoring` to every submission. Include the
user's intent, accepted scope, relevant plan or PR artifacts, progress,
important findings, and the believed critical path. Ask Pro to assess the
work against the goal and the consequential decisions; provide enough
context to reason instead of requesting a context-free approval.

Record each actual Pro submission once in the existing worklog: purpose,
artifact/revision and thread, plus the running submission count. Include
retries and failover submissions; polling an existing response is not a new
consultation. Keep this a short entry, not a separate tracking system.

If both profile windows are rate limited, report it and pause the blocked
Pro consultation or decision. Continue independent authorized work; pause
the whole run only when no useful independent work remains. Wait for the
user to say Pro is available again. Do not substitute another model for a
required Pro review or claim a pending review passed.

## Workflow

1. **Ramp up and plan.** Read live issue, parent, linked PRs, and discussion.
   Confirm the issue is open, available, and not already fixed; reproduce a
   bug before planning its fix. Write acceptance, non-goals, implementation,
   and appropriate verification on disk. Obtain or inherit the initial Pro
   planning consultation and incorporate warranted findings locally.
2. **Implement and verify.** Make the smallest coherent change in the
   worktree. Resolve ordinary decisions and repairs locally, consult the
   run's unblocker when needed, and use Pro at the cadence above.
3. **Publish and stabilize.** Use both PR skills to publish the PR and
   handle review threads and CI. For shared reviews, hand the coordinator
   the PR, revision, verification, and unresolved findings without launching
   duplicate child reviews. Independent issues can proceed meanwhile.
4. **Final review and repair.** Submit the stable PR, or have it included
   in the coordinator's batch/stack review. Address accepted findings,
   verify repairs, and decide whether their impact warrants a Pro recheck.
5. **Report merge-ready.** Require completed Pro planning and final review
   coverage, resolved material findings, and passing required checks.
   Report PR URL, change summary, current head and CI, the revision Pro
   actually reviewed, and any later changes with their local verification.
   Include the Pro thread/verdict and submission count. Never imply Pro
   reviewed a newer revision it did not see.

## Unblocking and persistent goals

Investigate blockers from the accepted scope and current evidence. If an
unblocker is armed, take it the intent, blocker, attempted reasoning,
options, and recommendation. It should settle routine authorization and
engineering decisions; escalate to Pro only for the consequential unresolved
problems described above. Without an unblocker, make those decisions
locally under the same standard. A matter needing the user's authority,
access, or a change to their ask gets one concise question with a
recommendation. Continue independent scope while the answer pends; a
continuation or wake-up is not an answer or a reason to ask again.

For a persistent run, author its goal prompt with `$prompt-authoring` and
`$startup-pragmatism`, naming the Pro thread, review scope and cadence,
unblocker per `$unblocker`, accepted scope, and merge-ready completion
condition. In Prime Agent, arm the goal and spawn the unblocker yourself;
otherwise provide the exact /goal text and unblocker spawn instruction.
When adopting a user-directed cadence change during a run, update the goal,
unblocker charter, and active dispatch briefs so they carry the same rule.

## Delegation

Before dispatch, read the installed
`../_shared/agent-orchestration-policy.md` and apply `$prompt-authoring` to
the populated brief. Carry the scope, inherited review coverage and cadence,
unblocker contact, and merge-ready contract into each brief. The coordinator
owns shared Pro submissions so children do not independently duplicate them.

## References

- [references/dispatch-evidence.md](references/dispatch-evidence.md):
  historical dispatches and owner corrections for maintainers.
