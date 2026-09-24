---
name: milestone-to-pr
description: "Explicit-invocation milestone delivery, fired only by name or direct command; never self-select it. Takes a spec milestone (several issues, such as M0 or 2A in a plan or sheet) to merge-ready as one PR per repo: Pro writes the milestone plan once, the verification path is proven first, overbuild-audit cuts the plan and the milestone diff, issues land as commits with a cheap primary read each, and the final (Pro by default) reviews the whole milestone once at the boundary while CI and bots run there, not per issue. Every coordinator uses delegated-implementation. Never merge or release. Not for a single issue (issue-to-pr) or an epic worked issue by issue into separate PRs (epic-to-prs)."
metadata:
  short-description: "Spec milestone delivered as one PR, reviewed once"
---

# Milestone To PR

Use only when the user explicitly invokes this lane by name or directly
commands this exact job: deliver a named milestone of a spec, several issues
built as one delivery, to merge-ready.

The point of this lane is throughput without losing quality. A milestone
pays for planning, review, CI, and closeout once, not once per issue. Pro
writes the plan once. Each issue gets a cheap read as it lands. The final
reviews the whole milestone once. CI runs at the boundary, not per issue.
Hours go into building and checking the work, not into waiting on repeated
ceremony.

Apply `$delegated-implementation` throughout. Workers implement, test, and
repair. The coordinator owns decisions, integration, and direct review of
every deliverable and changed code line. All skill authorship stays with the
coordinator.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- "milestone-to-pr on M0 in the pricing workbook."
- "milestone-to-pr on 2A, primary Opus max, final Pro."
- "Use $milestone-to-pr on milestone #5694 and stop at the boundary."

A single issue with its own PR is `issue-to-pr`. An epic worked issue by
issue into separate PRs is `epic-to-prs`. Status reads, planning-only asks,
and work without GitHub issues use the requested workflow instead.

## Delivery contract

- **Scope.** Freeze the milestone's accepted scope and non-goals from its
  issues, the plan or sheet it comes from, and the user's words. Reviewers
  and bots cannot expand it or quietly deliver less. A change to what the
  user asked for belongs to the user. Delivery rules the user already wrote
  on the issues or in the plan outrank this skill's defaults.
- **One branch and one PR per code repo per milestone,** wherever the
  issues are filed.
  - Issues land as commits on it.
  - Reuse the milestone's existing PR, or the project's working PR per repo
    when the user keeps one for the whole project.
  - Build on main, or on the previous milestone's PR when that one has not
    merged.
  - No per-issue PRs, no stack of per-issue rungs, and no draft PRs unless
    the user asks for one.
- **Authorization.** The run starts authorized for accepted in-scope work,
  including test accounts, QA environments, local databases, and the
  repairs they need. Work in a dedicated worktree under the target repo's
  AGENTS.md.
- **Quality.** Code is self-documenting, with clear comments at boundaries
  and role seams. Use `$startup-pragmatism` in planning and in decisions.
- **No overbuild.** Hold the milestone to `$overbuild-audit`'s intent: build
  exactly what its issues ask, the simplest way that works. The coordinator
  runs that audit itself, once on the written plan and once on the milestone
  diff before the boundary review, and applies the cuts. It adds no seat
  consultation.
- **Limits.** Never merge, release, apply approval labels such as
  `ufc-approved`, or touch production surfaces. A requirement that needs
  one of those is named as still owed, with who owes it. Stop at
  merge-ready.

## Keep moving

Most lost hours in long runs are an agent sitting still, not slow reviews.

- **Never leave work in flight unwatched:** a worker, a seat's answer, a
  device or simulator run, or CI. Do the next useful thing while it runs,
  and end a turn only when the harness will wake you as it lands, never to
  wait for the user to check.
- **Never stop for authority the run already has,** including QA-only
  actions and environment repairs. Never re-ask a decision the user already
  made.
- **Fix red checks and small blockers instead of reporting them.** Ask the
  user only when the matter needs their authority, their access, or a
  change to their ask: once, with a recommendation, while independent work
  continues.

## Seats

Two seats do the consulting, named by the user at invocation and read
exactly as named: "primary Opus max, final Pro."
- **The final** writes the milestone plan and reviews the milestone at its
  boundary. With none named, the final is GPT-6 Astra Pro.
- **The primary** reads each issue as it lands. With none named, the primary
  is a native child on the coordinator's own model, in a clean context.

These defaults replace the "Pro holds both" default in `issue-to-pr`.
Neither seat clears anything by token; the coordinator judges each answer.
Seats are consultants: a seat never edits the worktree, and a worker never
fills a seat.

Read `issue-to-pr`'s
[primary-and-final reference](../issue-to-pr/references/primary-and-final.md)
before the first consultation, and again if the user renames a seat. It says
how to reach Pro and other models, how to hand sources to a seat without
connectors, and what to record; its transport rules apply to a seat the user
named, not to the default primary. For a Pro seat, Pro is literal `Pro` in
the `Chat` surface's model picker, read back before every Send, in the
consultation profiles only, never the `Work` profile. Being in a profile
labeled Pro never makes a consultation Pro.

## Consulting the seats

**Templates.** Every consultation, in either seat, is written from the
matching family in `$chatgpt-web`'s
[consultation templates](../chatgpt-web/references/consultation-templates.md),
in the user's voice:
- K for the milestone plan
- A for the primary's read of one issue as it lands, as family L describes
- L for the final's milestone review
- B for one round after fixes
- G for diagnosing a bug that local work cannot crack
- E for an on-track check
- I for a retry
- J for a new thread or account

Write from the template's own sentences: fill its brackets and keep every
question it asks, in its words. Add what this milestone needs; never
shorten, paraphrase, or drop a question. Where a template says Pro, read the
model holding the seat. The plan is one continuing thread; the final's
boundary review starts clean in the same project, with the plan and its
thread's rulings attached.

**Sources.** Attach them whole:
- the canonical requirements source as a full export
- the plan
- every issue as filed
- the user's words verbatim
- raw test output
- the PRs with the `@GitHub` pill

Leave secret values out of everything attached. Let the seat read the
latest. Never ask for a verdict token, cap the answer, fence what the seat
may conclude, or pin a commit SHA.

**Waiting.** The coordinator watches for each answer and acts on it; it
never ends a turn saying a review is running or pending. How it waits is the
harness's business; that it waits is not. Pro regularly takes around 30
minutes. Let it finish, and do other milestone work meanwhile.

**Worklog.** Record each actual submission once in the plan doc's worklog:
- the seat
- the exact model and effort (for Pro, the picker text read from the page,
  never the profile label)
- the purpose, the thread or session, and the revision it read
- the running count for that seat

Count retries. Polling is not a new submission.

## Workflow

1. **Ramp up.** Read the plan or sheet the milestone comes from, every
   issue in it, linked PRs, and the user's words. Confirm which issues are
   open, still needed, and not already done. Settle the accepted scope.
   Name the milestone boundary. A milestone the plan splits into separately
   mergeable parts is one boundary per part. When earlier runs already built
   part of the milestone or have a consultation still answering, adopt that
   state and record it: an issue that landed without a primary read gets
   one now, and nothing still answering is sent again.
2. **Plan with the final.**
   - The final writes the milestone plan with family K in the milestone's
     thread: every part family K lists, including a work order per issue,
     who owns each piece of state, the real check that proves the
     milestone, and how it merges on its own without breaking what ships.
   - Ask questions until it is fully formed.
   - Carry it onto disk verbatim as the one canonical plan. Each issue gets
     its work order; the tracker, when there is one, gets a reference.
   - Run `$overbuild-audit` on the written plan against the milestone's
     accepted scope. Cut what does not trace to it; take anything that traces
     to the ask but looks heavy to the user once.
   - Comment the milestone's delivery rules on each issue it covers: it
     lands on the milestone PR, and CI and the final review happen at the
     milestone boundary, so CI may be red while the issue is done. Then a
     later single-issue run follows them instead of habit.
   - A plan the final already wrote that still covers the milestone
     satisfies this step; do not plan again because the skill was invoked or
     a session resumed.
3. **Prove the verification path first.**
   - Before the first issue, have a worker show that the checks the plan
     relies on actually run: the local test commands start, the QA, device,
     or simulator lane the plan needs boots with the right toolchain, and
     any CI prerequisites the plan names (services, fixtures, credentials)
     are in place. A test command counts when it exercises behavior, not
     only style.
   - Anything broken is fixed now, as the milestone's first work; when
     building that path is itself one of the milestone's issues, that issue
     goes first. Reviews are not a substitute for tests that cannot run.
4. **Build the issues.**
   - Workers implement work orders in the plan's order, in parallel where
     the plan allows, and run the focused checks for their change.
   - The coordinator reviews every changed line.
   - As each issue lands, the primary reads it with family A in a clean
     context. The next independent issue keeps moving during that read, and
     its findings go into the next repair or worker brief.
   - Intermediate pushes do not trigger CI where the repo allows it, for
     example `[skip ci]` in the commit message. Where CI runs anyway, nobody
     waits on it or reads it before the boundary.
   - Resolve ordinary decisions locally. Take a major unexpected blocker
     that local investigation cannot resolve to the final with family G.
5. **Reach the boundary.**
   - When every issue has landed and the primary's findings are fixed, run
     `$overbuild-audit` on the whole milestone diff against its accepted
     scope, have workers make the cuts, then run the plan's real check.
   - Push the commit that completes the milestone without the skip marker,
     so CI and the bots start on their own. A repo whose head already
     skipped CI gets its PR's own pipeline rerun on that head. Never use an
     empty commit or a manual build outside the PR.
   - Send the final family L right away; do not wait for CI. In this lane CI
     starts with the boundary push; that replaces `issue-to-pr`'s
     CI-after-review order.
6. **Fix once, then one more read.**
   - When the final answers, read the CI and bot results once as well.
     Assess every finding from all three against the milestone's scope and
     real risk. CI red that comes from work outside this milestone is named
     with its cause, not fixed here.
   - Batch the warranted fixes into one repair round. Workers repair and
     rerun the affected checks; the coordinator reviews the changes.
   - Run one B round with the final on the repaired milestone.
   - After that, a further fix inside the same design is confirmed by the
     primary, not by another round with the final. Start a fresh L only when
     a fix changed the design the review rested on.
   - A finding the coordinator declines is recorded with its reason.
   - The repair push runs CI again; read it once. Red in this milestone's
     own changes is fixed like any other finding.
7. **Report and close out once.**
   - Update the tracker, the issues, and any announcement once for the
     milestone.
   - Then close the run's browser pages.

## Browser pages

Many runs share one BrowserOS, so each page this run opens is this run's to
close.
- Note each page in the worklog as it opens.
- Keep a seat's thread page open while the milestone is in flight.
- When moving to another consultation profile, verify the new page first,
  then close the pages this run created in the profile it left.
- When the run ends, is cancelled, or is handed off, close every page
  this run created.
- Never close a page this run did not create, however idle it looks.

`$browseros` owns the mechanics.

## Unblocking and persistent goals

For a persistent run, author the goal prompt with `$prompt-authoring` and
`$startup-pragmatism`, carrying `$overbuild-audit`'s commander's intent. Name
in it:
- both seats with their exact model and effort, and their threads
- the milestone, its issues, and its boundary
- this lane's review and CI cadence
- the unblocker, per `$unblocker`
- the execution responsibilities, including coordinator-owned skill
  authorship
- the merge-ready condition

Arm the goal and unblocker using the active harness's supported mechanisms.
When the user changes the cadence mid-run, carry the change into the goal,
the unblocker charter, and active briefs.

## Delegation

`$delegated-implementation` owns worker selection, briefs, direct review, and
repair. Read the installed `../_shared/agent-orchestration-policy.md` before
dispatch and apply `$prompt-authoring` to each populated brief.

Each brief carries:
- the issue's work order and the milestone plan
- the milestone branch
- the checks to run
- the delivery rules: no PR, no CI waits
- the unblocker contact
- the expected handoff

The coordinator owns every seat submission; workers never consult seats.

## Merge-ready

The milestone is merge-ready when all of these hold. When its PR also
carries later milestones' unfinished work, the same bar makes the milestone
accepted rather than merge-ready; the PR merges when the user decides.

- **The final.** It wrote the plan, reviewed the milestone at its boundary,
  and said all three: it is implemented right, the PRs are ready, and each
  issue's part in this milestone is complete to its scope and
  requirements, with anything owed later named with the issue or milestone
  that owes it.
- **The primary.** It read each issue.
- **The coordinator.** It reviewed every deliverable and changed line
  directly.
- **Findings.** Material findings are resolved.
- **The real check.** It passed.
- **CI.** It ran at the boundary and on the repaired head and is green,
  except red named as coming from work outside this milestone. A repo
  without CI is reported as having none.

**Report** the PR URLs, what the milestone delivered per issue, current heads
and CI, and the revision each seat actually reviewed, with any later changes
that only the primary confirmed named separately. For each seat, name the
exact model, effort, thread, and submission count. For each review, keep
three things separate: what it was shown, what it said, and the
coordinator's conclusion.

**Pro evidence.** For every Pro consultation, quote the composer pill read
before Send (`6 Pro`) and the served-model slug on the answer
(`gpt-6-pro`). A review without both is reported as "model not verified" and
does not make the milestone merge-ready.

Never imply a seat reviewed a revision it did not see.
