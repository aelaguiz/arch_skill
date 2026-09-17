---
name: issue-to-pr
description: "Explicit-invocation issue delivery, fired by name or by user-invoked epic-to-prs; never self-select it. Takes a GitHub issue to a merge-ready PR with a plan on disk, startup-pragmatism, GPT-6 Astra Pro planning/final review, and PR authoring/follow-through. Astra and Fable coordinators use delegated-implementation: workers code, test, and repair; the parent owns decisions, every deliverable's direct review, and all skill authorship. Related issues can share Pro coverage. Preserve accepted scope and review receipts; never merge or release. Not for investigation-only asks, standalone planning, or work without a GitHub issue."
metadata:
  short-description: "Issue delivery with delegated code and parent review"
---

# Issue To PR

Use only when the user explicitly invokes this lane by name or directly
commands this exact pipeline, or when user-invoked `epic-to-prs` delegates an
issue. Ordinary issue work does not trigger it.

Take the issue to a merge-ready PR with the smallest change that delivers
its accepted scope. Use Pro for initial planning and final review; use the
working agent's judgment to carry the work between them.

For an Astra or Fable coordinator, apply `$delegated-implementation` throughout
the work: delegate code, reproduction, tests, and repairs; personally review
every deliverable and changed code line. All skill authorship stays with the
parent. An assigned implementation worker keeps its bounded role and reports
to the originating coordinator under that contract.

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
- Have Pro write the implementation plan and carry the agreed plan onto disk
  verbatim before implementation; apply `$startup-pragmatism` to it. Keep the
  same judgment during delivery: enough investigation and verification for
  the actual change, without invented approval gates or proof machinery.
- The run starts authorized for accepted in-scope work. Work in a dedicated
  worktree under the target repo's AGENTS.md. Require self-documenting code
  with clear comments at boundaries and role seams, relevant tests, and
  required repo checks. The execution contract above determines who authors
  each deliverable and who runs verification.
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

The coordinator owns routine decisions, plan refinements, dependency ordering,
and scope checks. Workers own implementation details and code repairs under
the execution contract. Extra Pro consultations are appropriate when a
meaningful batch of related work is ready to assess, or
a major unexpected blocker or consequential technical uncertainty remains
beyond the agent's reasoning after reasonable local investigation. State
what the consultation can resolve and why it matters to the goal. Neither
an issue boundary, a changed plan, a newly discovered dependency, nor vague
uncertainty alone requires a Pro message. A useful checkpoint after two
related issues is welcome; an every-two-issues rule is not.

Assess Pro's findings with judgment and batch the warranted fixes. Have workers
repair code and run affected checks, then review the changes and evidence
directly; the parent repairs skill content. Do not automatically resubmit plans
or PRs until Pro approves every edit. Consult again when a substantial redesign,
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

Use GPT-6 Astra with the literal `Pro` option and Extended thinking through
`$chatgpt-web`. Read and apply `$browseros` before BrowserOS calls. Verify
`Pro` in ChatGPT's `Chat` surface: Extra High, xhigh, Ultra, Thinking, and the
highest remaining setting are not Pro. Follow `$chatgpt-web` for input delivery
and account switching when Pro is missing, disabled, or explicitly capped.

Use the run's existing thread in an eligible numbered Pro profile, inheriting
the epic's thread when applicable. Write every submission from the matching
family in `$chatgpt-web`'s consultation templates, in the user's voice:
planning is family D, where Pro writes the plan and the coordinator asks the
questions until it is fully formed; a check of the written-up plan is C; the
PR review is A; one round after fixes is B; an on-track check is E; a retry
is I; a new thread or account is J. Attach the sources whole (the canonical
requirements source as a full export, the plan, the issue, the user's words
verbatim, raw test output, the PR through the connector) and let Pro read the
latest. Never ask for a verdict token, cap the answer, fence what Pro may
conclude, or pin a commit SHA. The coordinator watches for Pro's answer and
acts on it; it never ends a turn telling the user Pro's review is pending.

Record each actual Pro submission once in the existing worklog: purpose,
artifact/revision and thread, plus the running submission count. Include
retries and failover submissions; polling an existing response is not a new
consultation. Keep this a short entry, not a separate tracking system.

Missing Pro probably means a temporary account rate limit. Under `$chatgpt-web`
and `$browseros`, use only the already-open numbered Pro profiles, such as
Pro 1 through Pro 5 or whichever exist. Never use the user's `Work` profile,
including for fallback or an old thread; preserve its rate-limit capacity.
Note which eligible profile/window works and use its same-named project with
the needed context. All should have the same projects. Only after eligible Pro
accounts are exhausted, report their observed conditions and pause the blocked Pro
consultation or decision. Continue independent authorized work; pause
the whole run only when no useful independent work remains. Wait for the
user to say Pro is available again. Do not substitute another model for a
required Pro review or claim a pending review passed.

## Workflow

1. **Ramp up and plan.** Read live issue, parent, linked PRs, and discussion.
   Confirm the issue is open, available, and not already fixed; reproduce a
   bug before planning its fix, delegating reproduction under the execution
   contract. Write acceptance, non-goals, implementation, and appropriate
   verification on disk. Take the issue to Pro with family D so Pro writes
   the plan (outcome, acceptance criteria, requirements, architecture, do's,
   do not's, test plan); ask questions until it is fully formed, then carry
   it onto disk verbatim. Existing Pro planning that still covers the
   accepted scope satisfies this step.
2. **Implement and verify.** Deliver the smallest coherent change in the
   worktree under the execution contract. Give workers tight requirements and
   appropriate checks, review every deliverable and changed code line, and
   return code findings for repair. Author skill content directly. Resolve
   ordinary decisions locally, consult the run's unblocker when needed, and
   use Pro at the cadence above.
3. **Publish and stabilize.** Use both PR skills to publish the PR and
   handle review threads and CI, retaining the same authorship, test, and
   direct-review responsibilities during follow-through. For shared reviews,
   hand the coordinator the PR, revision, verification, and unresolved findings
   without launching duplicate child reviews. Independent issues can proceed
   meanwhile.
4. **Final review and repair.** Submit the stable PR, or have it included
   in the coordinator's batch/stack review. Route accepted findings through
   the same execution contract, personally review repairs, and decide whether
   their impact warrants a Pro recheck.
5. **Report merge-ready.** Require completed Pro planning and final review
   coverage, the originating coordinator's direct review of every deliverable
   and changed code line, resolved material findings, and passing required
   checks.
   Report PR URL, change summary, current head and CI, the revision Pro
   actually reviewed, and any later changes with their local verification.
   Include the Pro thread and submission count, and keep three things
   separate: what Pro was shown, what Pro said, and the coordinator's own
   conclusion. Never imply Pro reviewed a newer revision it did not see.

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
unblocker per `$unblocker`, accepted scope, execution responsibilities including
parent-owned skill authorship, and merge-ready completion condition. Arm the
goal and unblocker using the active harness's supported mechanisms.
When adopting a user-directed cadence change during a run, update the goal,
unblocker charter, and active dispatch briefs so they carry the same rule.

## Delegation

For Astra and Fable coordinators, `$delegated-implementation` owns the worker
selection, brief, direct review, and repair contract, including parent-owned
skill authorship. For other dispatches, read the installed
`../_shared/agent-orchestration-policy.md` and apply `$prompt-authoring` to the
populated brief. Leave spawning mechanics to the active harness. Carry the
scope, inherited review coverage and cadence, unblocker contact, and handoff
into each brief. The originating coordinator owns shared Pro submissions and
final acceptance; children return artifacts without duplicating consultations.

## References

- [references/dispatch-evidence.md](references/dispatch-evidence.md):
  historical dispatches and owner corrections for maintainers.
