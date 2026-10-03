---
name: issue-to-pr
description: "Explicit-invocation issue delivery, fired by name or by user-invoked epic-to-prs; never self-select it. Takes a GitHub issue to a merge-ready PR through two seats the user names at invocation: a primary that writes the plan with the coordinator and takes the early review rounds, and a final that checks the plan once and reviews the PR once; GPT-6 Astra Pro holds both when none is named. Plan on disk, startup-pragmatism, overbuild-audit on plan and diff, PR authoring, CI last. Every coordinator uses delegated-implementation: workers code, test, and repair; the parent owns decisions, every deliverable's direct review, and all skill authorship. Related issues can share Pro coverage. Preserve accepted scope and review receipts; never merge or release. Not for investigation-only asks, standalone planning, or work without a GitHub issue."
metadata:
  short-description: "Issue delivery with delegated code and parent review"
---

# Issue To PR

Use only when the user explicitly invokes this lane by name or directly
commands this exact pipeline, or when user-invoked `epic-to-prs` delegates an
issue. Ordinary issue work does not trigger it.

Take the issue to a merge-ready PR with the smallest change that delivers
its accepted scope. Two seats do the consulting. The primary is the
collaborator: it writes the plan with the coordinator and takes the early PR
review rounds. The final is the ultimate check: it reads the written-up plan
once before anyone builds and reviews the PR once at the end. The user names
the seats at invocation, for example "primary Sol xhigh, final Pro"; with
none named, GPT-6 Astra Pro holds both. The coordinator's judgment carries
the work between them.

Apply `$delegated-implementation` throughout the work: delegate code,
reproduction, tests, and repairs; personally review
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
- A direct command to plan an issue with the primary, implement, test,
  publish a PR, get the final's review, and stop at merge-ready.
- The same with seats named: "issue-to-pr on #N, primary Fable xhigh, final
  Pro." Read the model and effort exactly as named.
- An issue handed over by user-invoked `epic-to-prs`.

For investigation-only work, standalone planning or review, or work without
a GitHub issue, use the requested workflow instead.

## Delivery contract

- Freeze the accepted scope and non-goals from the issue and the user's direction.
  Reviewers and bots cannot expand or silently shrink that scope. Resolve
  routine scope interpretation from the contract; a change to what the user
  asked for belongs to the user.
- Have the primary write the implementation plan; bring `$startup-pragmatism`
  into the back-and-forth, carry the agreed plan onto disk verbatim, and have
  the final read it once against the code before implementation. Keep that judgment during delivery: enough investigation
  and verification for the actual change, without invented approval gates or
  proof machinery.
- Hold the work to `$overbuild-audit`'s intent: build exactly what the issue
  asks, the simplest way that works. The coordinator runs that audit itself,
  once on the written plan before the final's plan check and once on the diff
  before publishing, and applies the cuts. It adds no consultation or review
  round.
- The run starts authorized for accepted in-scope work. Work in a dedicated
  worktree under the target repo's AGENTS.md. Require self-documenting code
  with clear comments at boundaries and role seams, relevant tests, and
  required repo checks. The execution contract above determines who authors
  each deliverable and who runs verification.
- Use `$pr-authoring` to publish and `$pr-review-followthrough` only at the
  very end. CI is the last step of the whole job: nobody waits on it, fixes
  it, or reports it until the final has cleared the PR. PR Agent and other bots are
  advisory; assess findings against the issue and code rather than treating
  them as orders to expand scope.
- Stop at merge-ready with receipts and the run's own browser pages closed.
  Never merge, release, apply approval labels such as `ufc-approved`, or
  touch production surfaces.

## Primary and final

The primary writes the plan (family D) and takes every early PR round: the
first review (A), the one round after fixes (B), and a fresh A when a fix
changed the basis of the review, until it finds nothing material. It answers
the unblocker's major-blocker consults and any on-track check (E). The final
reads the written-up plan once against the code before anyone builds (C),
with the primary's planning exchange attached, and reviews the PR once after
the primary is clean (A), with the issue as filed attached and the completion
question asked. The final reads the PR itself first; the primary's
findings and the fixes ride along as files in the brief's "what I did", as
what happened since, not as the frame of the ask. Its findings get fixed and
one B round; then CI.
Neither seat clears anything by token; the coordinator judges each answer.
Seats are consultants. Workers are `$delegated-implementation`'s and default
separately; a seat never edits the worktree and a worker never fills a seat.

When one model holds both seats, or none is named, this is one planning
consultation and one final review with judgment in between: workflow steps 4
and 5 become one review lane with that model (A, fixes, one B, a fresh A when
the basis moved). A plan the
primary already wrote that still covers the accepted scope satisfies
planning; do not repeat it because this skill was invoked or a session
resumed. Family C is the final's one look at the plan, not a second planning
consultation; when one model holds both seats and the plan has not moved
since it was written, skip it. A primary is not `$fresh-consult` or
`$codex-review-yolo`; those keep a verdict footer by design and are selected
separately.

For an issue inside a coherent epic or related batch, inherit the
coordinator's seats and shared planning and review scope. Do not add a plan review
and final review for every child. The coordinator can collect locally
finished PRs for a meaningful batch checkpoint or final stack review. A
child awaiting that review is locally ready, not yet merge-ready.
An issue that belongs to a milestone delivered through `milestone-to-pr`,
or whose body carries that milestone's delivery rules, follows them: its
commits land on the milestone PR, the primary reads it as it lands, and CI
and the final review wait for the milestone boundary.

The coordinator owns routine decisions, plan refinements, dependency ordering,
and scope checks. Workers own implementation details and code repairs under
the execution contract. Extra consultations with the primary are appropriate
when a meaningful batch of related work is ready to assess, or
a major unexpected blocker or consequential technical uncertainty remains
beyond the agent's reasoning after reasonable local investigation. State
what the consultation can resolve and why it matters to the goal. Neither
an issue boundary, a changed plan, a newly discovered dependency, nor vague
uncertainty alone requires a consultation. A useful checkpoint after two
related issues is welcome; an every-two-issues rule is not.

Assess each seat's findings with judgment and batch the warranted fixes. Have
workers repair code and run affected checks, then review the changes and
evidence directly; the parent repairs skill content. Do not automatically
resubmit plans or PRs until a seat approves every edit. Consult again when a
substantial redesign,
unresolved consequential disagreement, or a repair that changes the basis
of the review needs independent judgment. The normal planning/final pair
is a baseline, not a hard cap on useful consultation.

Both seats read the pushed branch (Pro through `@GitHub`, another model
through the worktree and `gh pr diff`) and need nothing from CI. Do not wait
on CI before a review, between rounds, or while any seat's round is open, and
do not fix CI or bot findings until the final has cleared the PR. Workers run
the local tests for the change under the execution contract; that is the
verification the seats see. CI is the very
last step: once the final has cleared everything, let CI and the bots run
once, fix what they find, and go back to the final only if a CI fix changed
behavior. Formatting, a
flake, a shard, or a rebase with unchanged behavior does not reopen the
review; decide from impact, not the SHA changing.

## Consulting the primary and the final

Every consultation, in either seat, is written from the matching family in
`$chatgpt-web`'s consultation templates
(`../chatgpt-web/references/consultation-templates.md`), in the user's voice:
D for the plan, where the seat writes it and the coordinator asks the
questions until it is fully formed; C for the check of the written-up plan; A
for a PR review; B for one round after fixes; E for an on-track check; G for
diagnosing a bug before its fix is planned; I for a retry; J for a new thread
or account. Where a template says Pro, read the
model holding the seat. Attach the sources whole (the canonical requirements
source as a full export, the plan, the issue, the user's words verbatim, raw
test output, the PR) and let the seat read the latest. Never ask for a
verdict token, cap the answer, fence what the seat may conclude, or pin a
commit SHA. The coordinator watches for the answer and acts on it; it never
ends a turn saying a review is running or pending. How it waits is the
harness's business; that it waits is not.

Read [references/primary-and-final.md](references/primary-and-final.md)
before the first consultation of a run, and again if the user renames a
seat. It says how to reach each seat: Pro through `$chatgpt-web` with
`$browseros`, literal `Pro` selected in the model picker of the `Chat`
surface and read back from the page before every Send, in the consultation
profiles only (the BrowserOS profiles labeled `Pro 1`, `Pro2`, and so on),
never the `Work` profile, with `$chatgpt-web`'s rate-limit and
account-switching rules. Those profile labels name browser profiles; being
in one never makes a review a Pro review. For any other model, that reference's
collapse-or-hand-off rule applies to every parent: a seat on your own model is
your native subagent, and a seat on a different model is a handoff to that
model. Say which model each seat ran on. A planning collaborator keeps one
continuing session for the D back-and-forth; a review round starts clean.
Otherwise do not substitute another model for a named seat, and never claim
a pending review passed.

Record each actual submission once in the existing worklog (the plan doc's
worklog section when the run has no other): seat, exact model and effort
(for Pro, the picker text as read from the page, never the profile label),
purpose, artifact/revision and thread or session, plus the running count for
that seat. A D exchange is one consultation; note its turn count. Include retries and failover submissions;
polling an existing response is not a new consultation. Keep this a short
entry, not a separate tracking system.

## Browser pages

Many runs of this skill share one BrowserOS at the same time, so pages a run
leaves open pile up in the user's browser. Each page a run opens is that
run's to close. Note each one in the worklog as it opens, the way
`$browseros` tracks task-created pages.

The test for closing a page is whether this run will come back to it. While
the issue is in flight, a seat's thread page is working context through
every round, wait, and rate-limit pause, and closing it early loses that
context; when unsure mid-run, keep the page. A page whose one purpose is
finished, such as a sign-in popup or a single lookup, can close then. The
rest close at two points:

- **Leaving a profile.** When a consultation moves to another consultation
  profile or account, verify the new page first, then close the pages this
  run created in the profile it left.
- **The run ends.** At merge-ready, or when the run is cancelled, handed
  off, or abandoned, check that each seat's thread is in the worklog, then
  close every page this run created, in every profile. The conversation
  stays in ChatGPT, and the worklog entry reopens it if the issue comes back.

`$browseros` owns the closing mechanics and the ownership proof. Close only
pages this run created and recorded, by their recorded identity. Another
run's thread page looks just like this one's, so a title, project name, or
idle look never makes a page closable; adopted pages, the user's pages, and
other agents' pages stay open. Inside an epic, the shared thread pages are
the coordinator's and stay open until the epic's last shared review.

## Workflow

1. **Ramp up and plan.** Read live issue, parent, linked PRs, and discussion.
   Confirm the issue is open, available, and not already fixed; reproduce a
   bug before planning its fix, delegating reproduction under the execution
   contract. Settle the accepted scope and non-goals, then take the issue to
   the primary with family D so it writes the plan (outcome, acceptance
   criteria, requirements, architecture, do's, do not's, test plan); ask
   questions until it is fully formed, then carry it onto disk verbatim and
   into the issue. Run `$overbuild-audit` on the written plan against the
   accepted scope and cut what does not trace to it; anything that traces to
   the ask but looks heavy goes to the user once. Have the final read the
   written-up plan once against the code (family C) before anyone builds. A plan the primary already wrote
   that still covers the accepted scope satisfies this step.
2. **Implement and verify.** Deliver the smallest coherent change in the
   worktree under the execution contract. Give workers tight requirements and
   appropriate checks, review every deliverable and changed code line, and
   return code findings for repair. Author skill content directly. Resolve
   ordinary decisions locally, consult the run's unblocker when needed, and
   use the primary at the cadence above. Before publishing, run
   `$overbuild-audit` on the full diff against the accepted scope and have
   workers make its cuts.
3. **Publish.** Publish the PR with `$pr-authoring` and go straight to the
   primary. Do not wait on CI, and do not start review-thread or CI
   follow-through.
   For shared reviews, hand the coordinator the PR, revision, local
   verification, and unresolved findings without launching duplicate child
   reviews. Independent issues can proceed meanwhile.
4. **Primary review and repair.** Submit the PR to the primary with family
   A, or have it included in the coordinator's batch review. Route accepted
   findings through the same execution contract, personally review repairs,
   run one B round, and start a fresh A when a fix changed the basis of the
   review, until the primary finds nothing material. Still no CI.
5. **Final review.** Submit the PR to the final with family A, with the
   issue as filed attached, the primary's findings and the fixes attached,
   and both questions asked: is it implemented right, and is the original
   ask complete to its full scope and requirements. A read that asks only
   about the fixes or "the fixed revisions" is not the final review. Fix
   what it finds, run one B round, and return to the final only if a later
   fix changed behavior. The work is not done until the final has said all
   three: implemented right, PR ready, complete to the full scope and
   requirements. Still no CI.
6. **CI and bots, last.** Only after the final has cleared the PR, run
   `$pr-review-followthrough`: let CI and the bots run once, fix what they
   find, and return to the final only if a fix changed behavior.
7. **Report merge-ready.** Require the primary's plan, the final's plan check
   and PR review with its explicit answer that the work is implemented right,
   the PR is ready, and the original issue is complete to its full scope and
   requirements, the originating coordinator's direct review of every
   deliverable and changed code line, resolved material findings, and passing
   required checks (local checks by workers throughout, CI once at the end). Report PR URL, change summary, current head and CI, the
   revision each seat actually reviewed, and any later changes with their
   local verification. Name each seat's exact model and effort, thread, and
   submission count, and keep three things separate for each: what it was
   shown, what it said, and the coordinator's own conclusion. Never imply a
   seat reviewed a newer revision it did not see. For every Pro review, quote
   the two model readings `$chatgpt-web` requires: the composer pill before
   Send (`6 Pro`) and the served-model slug on that answer (`gpt-6-pro`). A
   review without both readings is reported as "model not verified", is not a
   Pro review, and the PR is not merge-ready. Once those receipts are in the
   worklog, close the run's pages as Browser pages says, and name any page
   kept open and why.

## Unblocking and persistent goals

Investigate blockers from the accepted scope and current evidence. If an
unblocker is armed, take it the intent, blocker, attempted reasoning,
options, and recommendation. It should settle routine authorization and
engineering decisions; escalate to the primary only for the consequential
unresolved problems described above. Without an unblocker, make those decisions
locally under the same standard. A matter needing the user's authority,
access, or a change to their ask gets one concise question with a
recommendation. Continue independent scope while the answer pends; a
continuation or wake-up is not an answer or a reason to ask again.

For a persistent run, author its goal prompt with `$prompt-authoring` and
`$startup-pragmatism`, carrying `$overbuild-audit`'s commander's intent and
naming both seats with exact model and effort, their
threads, review scope and cadence, unblocker per `$unblocker`, accepted
scope, execution responsibilities including
parent-owned skill authorship, and merge-ready completion condition. Arm the
goal and unblocker using the active harness's supported mechanisms.
When adopting a user-directed cadence change during a run, update the goal,
unblocker charter, and active dispatch briefs so they carry the same rule.

## Delegation

`$delegated-implementation` owns the worker selection, brief, direct review, and
repair contract, including parent-owned skill authorship. Read the installed
`../_shared/agent-orchestration-policy.md` before dispatch and apply
`$prompt-authoring` to the populated brief. Leave spawning mechanics to the active
harness. Carry the scope, inherited review coverage and cadence, unblocker
contact, and handoff into each brief. The originating coordinator owns the seats, their
submissions, and final acceptance; children return artifacts without
duplicating consultations.

## References

- [references/primary-and-final.md](references/primary-and-final.md): how
  to reach, brief, and receipt each named seat. Read before the first
  consultation of a run.
- [references/dispatch-evidence.md](references/dispatch-evidence.md):
  historical dispatches and owner corrections for maintainers.
