---
name: epic-to-prs
description: "Explicit-invocation epic loop, fired only by name or direct command; never self-select it. Works an epic or milestone most-important-first through issue-to-pr to merge-ready PRs. Owns the live queue, persistent goal, unblocker, and shared planning and review through two seats the user names at invocation: the primary writes the epic plan and reviews batches, the final checks the plan once and reviews the stack once; GPT-6 Astra Pro holds both when none is named. Every coordinator uses delegated-implementation: workers code, test, and repair; the parent owns direct review of every deliverable and all skill authorship. Preserve accepted scope and honest receipts; continue independent work around blockers. Never merge or release. Not for status reads, decomposition via arch-epic, or open-ended optimization."
metadata:
  short-description: "Epic delivery with delegated code and shared Pro reviews"
---

# Epic To PRs

Use only when the user explicitly invokes this lane by name or directly
commands this exact job: work a named epic or milestone through its issues
to Pro-reviewed, merge-ready PRs. Touching an epic during other work does
not authorize this loop.

Deliver the epic's accepted scope most important first. Use `issue-to-pr`
for implementation and PR delivery, with shared planning and review across
related issues through the epic's primary and final seats, named once by the
user and inherited by every child. Keep delivering until the queue and required reviews
are complete, the user stops the run, or no useful unblocked work remains.

Apply `$delegated-implementation` across the epic. Workers implement, test, and
repair; the parent owns decisions, integration,
and direct review of every deliverable and changed code line. All skill
authorship stays with the parent, including skill work inside a child issue.

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

## Shared primary and final

Begin with one epic planning consultation with the primary in family D: it
writes the epic plan covering the goal, queue, implementation approach,
dependencies, and verification, and the coordinator asks the questions.
Then the final reads the written-up plan once against the code (family C)
before anyone builds. Reuse a plan the primary already wrote when it still
covers the accepted scope. A child fully covered by the epic plan carries
that part onto disk; a child that needs its own plan goes back to the
primary with family D rather than getting an agent-written plan. When one
model holds both seats, C is skipped if the plan has not moved.

The primary reviews batches (A, one B round, a fresh A when the basis moved)
until it finds nothing material. The final reviews the completed PR stack
once against the epic's goal and against each issue's full scope and
requirements, with the issues as filed attached, including interactions
between PRs, with the primary's batch findings and the fixes attached. The
epic is not done until the final has said the stack is implemented right,
the PRs are ready, and every issue is complete to its full scope and
requirements. A small coherent epic may
need only the plan, its check, and the final stack review. For larger work,
choose meaningful batches or milestones the primary can credibly assess. A checkpoint after two
related issues can be useful when their combined result exposes integration
or direction worth reviewing; there is no fixed issue count or mandatory
boundary check. Explain briefly what this checkpoint will resolve.

A primary's batch review does not discharge a child's final coverage; the
final's stack review does, or the final's early review of a batch that must
be merge-ready before the rest. A planning or status-only checkpoint
discharges nothing. Final epic review should focus
on the remaining changes and overall integration, using prior batch reviews
as context instead of repeating every completed child review. Review early
when a batch needs to be merge-ready before the rest of the epic.

Between these consultations, the coordinator reasons through architecture,
plan refinements, ordering, and scope; workers implement and repair code under
the execution contract. Consult the primary for a major unexpected blocker or
consequential technical uncertainty that remains beyond the
agent's reasoning after reasonable local investigation and is likely to
change the approach. An issue boundary, dependency discovery, or ordinary
uncertainty alone does not justify a check-in. Never serialize independently
buildable issues behind an unrelated blocker.

Batch accepted findings from either seat. Workers repair code and run
affected checks; the coordinator personally reviews the changes and evidence
and repairs skill content itself. Do not run an automatic resubmission loop
to obtain a seat's approval of every edit.
Seek another consultation for substantial redesign, unresolved consequential
disagreement, or a repair
that changes the basis of the review and needs independent judgment. The
normal cadence is a baseline, not a hard cap.

Both seats read the pushed branches (Pro through `@GitHub`, another model
through the worktree and `gh pr diff`) and need nothing from CI. Do not wait
on CI before a review, between rounds, or across the epic while reviews are
open, and do not fix CI or bot findings until the final has cleared the
work. CI is the very last step for each PR and for the stack: once the final
has cleared everything, let CI and the bots run once, fix what they find,
and return to the final only if a fix changed behavior. Assess post-review
changes by their effect on behavior, integration, and review conclusions; a
new SHA alone does not invalidate useful review. Record which revisions each
seat actually saw plus later local repairs and verification.

## Seats, threads, and receipts

Read the user's seat names exactly and carry them into every child. Reach
each seat as `issue-to-pr`'s
[primary-and-final reference](../issue-to-pr/references/primary-and-final.md)
says: Pro through `$chatgpt-web` with `$browseros`, literal `Pro` selected
in the model picker of the `Chat` surface and read back from the page before
every Send, in one epic thread per Pro seat supplied by the user or
created in the applicable ChatGPT project; another model as a clean native
child or an external process through `$agent-delegate` at the exact model
and effort, with one continuing planning session for D and a clean context
per review round. Extra High, xhigh, Ultra, Thinking, the highest
remaining setting, and a browser profile labeled `Pro` are not Pro: the
label names the profile, and only the page's picker reading proves the
model.

Write every submission from the matching family in `$chatgpt-web`'s
consultation templates (`../chatgpt-web/references/consultation-templates.md`),
in the user's voice: epic planning is family D, where
the primary writes the plan and the coordinator asks the questions until it
is fully formed; the final's check of the written-up plan is C; a batch
review by the primary or the stack review by the final is A;
one round after fixes is B; an on-track check is E; a retry is I; a
continuation thread or account move is J. Attach the sources whole (the
canonical requirements source as a full export, the plan, the issues, the
user's words verbatim, raw output, the PRs with the `@GitHub` pill) on every
round, and let Pro read the latest. Never ask for a verdict token, cap the
answer, fence what Pro may conclude, or pin a commit SHA. The coordinator
watches for Pro's answer and acts on it; it never ends a turn saying Pro is
running or that its review is pending. How it waits is the harness's
business; that it waits is not. Keep one short existing-worklog entry per
actual submission: purpose, what was attached, thread, and running count.
Count retries and failover submissions; response polling is not another
consultation.

If Pro is missing or disabled, treat it as a probable temporary account rate
limit; an explicit cap triggers the same switch. Follow `$chatgpt-web` and
`$browseros` to use only the already-open consultation profiles, the
BrowserOS profiles labeled `Pro 1` through `Pro5` or whichever exist, and
select and read back `Pro` again in the new page. Never use the user's `Work` profile, including
for fallback or an old thread; preserve its rate-limit capacity.
Note which eligible profile/window works and use it.
All should have the same projects. Continue in the
same-named project with the epic context restated. Record continuation thread
URLs and reuse the original when available in a consultation profile. Only after
their accounts are exhausted, report their observed conditions and the
blocked Pro decision. Continue
independent authorized work. Pause the whole run only when no useful
independent work remains, and wait for the user to say Pro is back. Never
substitute another model for a named seat or count a pending review as
passed.

## Workflow

1. **Adopt and plan.** Read the epic, live issues, supplied Pro thread, and
   existing plans. Settle the accepted scope and the initial order, then
   take the epic to the primary with family D, so it writes the plan and the
   coordinator asks the questions until it is fully formed, bringing
   `$startup-pragmatism` into that back-and-forth; carry the agreed plan
   onto disk verbatim and have the final read it once against the code
   (family C). Reuse a plan the primary already wrote when it still covers
   the scope. Identify useful reviewable batches where the work calls for
   them.
2. **Arm the run.** Stand up `$unblocker` with the user's ask, scope,
   production boundary, the seats, and this cadence. Author the goal prompt
   with `$prompt-authoring`, including both seats with exact model and
   effort, their threads, unblocker contact, queue,
   shared review scope, execution responsibilities including parent-owned
   skill authorship, and completion condition. Arm the goal and unblocker
   using the active harness's supported mechanisms. Carry user-directed
   cadence changes into the goal,
   charter, and active dispatch briefs during a run.
3. **Deliver issues.** Refresh the queue and run dependency-ready `issue-to-pr`
   work with inherited planning, review coverage, and execution responsibilities.
   Parallelize independent scopes when useful; keep shared design decisions
   and overlapping work coordinated. Personally review every deliverable and
   changed code line, including worker-delivered issues. Collect locally ready
   PRs without duplicate child submissions. Resolve routine decisions
   locally or through the unblocker, use meaningful batch checkpoints and
   major-blocker consultations when warranted, and continue independent
   scope while any real user question pends. Ask once; continuations do not
   supply an answer or justify repeated questions.
4. **Review and finish.** Take batches to the primary until it finds nothing
   material, then obtain the final's one review of the completed stack with
   the primary's findings and the fixes attached. Resolve material findings
   through the same execution contract and personally review fixes. Only
   then run CI and bot follow-through, once, as the very last step. Every
   delivered issue needs the coordinator's direct review, the primary's plan
   and the final's plan check and review coverage, and passing required
   checks before merge-ready.
   Do not mark the goal complete merely because all issues were dispatched;
   pending reviews and unresolved scope remain unfinished work.
5. **Report.** List delivered issues and PRs, current heads and CI, each
   seat's exact model and effort, review coverage and reviewed revisions,
   later local repairs, and the submission count per seat. For each review
   keep what the seat was shown, what it said, and the coordinator's own
   conclusion separate. Name any unresolved
   blocker or user escalation and
   preserve the remaining queue for continuation. Complete the goal only
   when its accepted work is merge-ready or the user explicitly removed it
   from scope; otherwise report the precise incomplete state.

## Delegation

`$delegated-implementation` owns worker selection, requirements briefs, direct
review, and code repair. The originating coordinator retains every deliverable's
acceptance and all skill authorship when assigning issues to workers; an issue
handoff does not replace it with another executive. Read the installed
`../_shared/agent-orchestration-policy.md` before dispatch and apply
`$prompt-authoring` to the populated brief. Leave spawning mechanics to the active
harness. Include accepted scope, boundary comments, unblocker contact, shared
planning and review coverage, and the expected handoff. The coordinator owns Pro
submissions and the submission count; children return artifacts and
consequential questions without launching duplicate consultations.

## References

- [references/epic-dispatch-evidence.md](references/epic-dispatch-evidence.md):
  historical epic prompts and owner corrections for maintainers.
