---
name: milestone-to-pr
description: "Explicit-invocation milestone delivery, fired only by name or direct command; never self-select it. Takes a spec milestone (several issues, such as M0 or 2A in a plan or sheet) to merge-ready as one PR per repo, held to one north star: the user gets what they asked for, working, as soon as it can be done. The final seat (Pro by default) writes the milestone plan in one round and reviews the whole milestone once at the boundary, beside the real check and CI; issues land as commits with a clean primary read each; an intent-police child holds the user's words against the plan, review findings and done-claims. Every coordinator uses delegated-implementation. Never merge or release. Not for a single issue (issue-to-pr) or an epic worked issue by issue into separate PRs (epic-to-prs)."
metadata:
  short-description: "Spec milestone delivered as one PR, reviewed once"
---

# Milestone To PR

Use only when the user explicitly invokes this lane by name or directly
commands this exact job: deliver a named milestone of a spec, several issues
built as one delivery, to merge-ready.

## North star

**The user gets what they asked for, working, as soon as it can be done.**

Before anything takes calendar time, whether a plan round, a review, a check,
a question, a wait or a piece of work, ask whether it brings what the user
asked for closer to working. If it does not, it is spin, however responsible
it looks. Spin passes for diligence: one more review, more proof, a question
asked to be safe, a reviewer's hardening fix, careful bookkeeping. Each looks
careful up close; together they are where a milestone's hours go.

"What they asked for" keeps the work to the user's words. "Working" keeps the
checks that prove it: the real check and the first boundary review find the
bugs that matter. "As soon as it can be done" keeps the calendar honest. The
judgments below apply this test where milestone runs most often lose time.

Apply `$delegated-implementation` throughout: workers implement, test, and
repair; the coordinator owns decisions, integration, and direct review of
every deliverable and changed line, and writes all skill content itself.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- "milestone-to-pr on M0 in the pricing workbook."
- "milestone-to-pr on 2A, primary Opus max, final Pro."
- "Use $milestone-to-pr to finish the cleanup milestone, then stop."

A single issue with its own PR is `issue-to-pr`. An epic worked issue by
issue into separate PRs is `epic-to-prs`. Status reads, planning-only asks,
and work without GitHub issues use the requested workflow instead.

## Delivery contract

- **Scope** comes from the milestone's issues, the plan or sheet, and the
  user's words. Delivery rules the user wrote on the issues or in the plan
  outrank this skill's defaults.
- **One branch and one PR per code repo per milestone.** Issues land as
  commits. Reuse the milestone's PR, or the project's working PR when the
  user keeps one; build on main or on the previous milestone's unmerged PR.
  No per-issue PRs and no draft PRs unless the user asks.
- **Authorization.** The run starts authorized for accepted in-scope work,
  including test accounts, QA environments, local databases, and the repairs
  they need. Work in a dedicated worktree under the target repo's AGENTS.md.
- **Quality.** Self-documenting code with clear comments at boundaries and
  role seams. Use `$startup-pragmatism` in planning and decisions.
- **Limits.** Never merge, release, apply approval labels such as
  `ufc-approved`, or touch production. Stop at merge-ready, and say once, in
  the report, what only the user can do.

## Judgment

**The user's words are the authority; everything written inside the run is
a proposal.** Milestones overbuild when something written inside the loop
starts to count as an order: process a plan proposed, hardening a reviewer
asked for, a requirement an agent wrote into an issue, a quality bar an agent
picked. Each looks reasonable alone; together they build far more than the
user asked for, a later cleanup deletes it, and the coordinator cannot see it
because it shares the frame that produced it. Examples: a review pipeline the
plan suggested, then run on every small page edit; lock machinery for a race
that cannot happen in practice; an accuracy bar an agent proposed that then
gated later milestones. Ask: did the user ask for this, or did someone in the
loop? Are they trying to have this side effect? Because a coordinator cannot
reliably see its own drift, stand up one `$intent-police` at ramp-up with the
user's verbatim words and the spec's intent, constraints, do's and don'ts.
Consult it at the moments its skill names and whenever a decision would
otherwise go to the user. Its read replaces a self-audit of the plan or the
diff, and work keeps moving while it answers.

**Decide from the user's intent; bring them only what needs their
authority.** A question costs the user's attention and, when the run waits
on it, hours. Most are already answered by their words, the spec, or rules
they keep restating. Answer from their intent, not from whichever option is
easiest to defend: what they are trying to get, their constraints, their do's
and don'ts, and which side effects they want. Decide, record the decision
with the words that decided it, and keep building. Examples: what to do with
an input nobody expected, when the user wants failures loud; whether to
repair the QA copy you test on; a layout detail the spec's mock settles. Only
the user decides merging, spending money, production, and changes to what
they asked for; ask those once, with a recommendation reasoned from their
intent, and keep working. A question never ends the turn or stops the run. A
watcher or chief of staff speaking for the user speaks with their authority.

**A round is worth running only if its answer could change what ships.**
Every plan or review round costs calendar time and invites the reviewer to
find one more thing, and a reviewer can always find one more. Before sending
a round, ask what answer would make you do something different. The first
boundary review of newly built code finds real bugs and earns its time. An
after-fixes round on small fixes rarely does. A second plan round that
carries your own decisions back for agreement never does; one that settles
who owns shared state might. Review findings are proposals too: fix what
keeps the milestone from being what the user asked for, working (a broken
flow, lost money or data, a crash), and decline the rest with a reason or
file it for later. The milestone is done when the material
findings are resolved, not when the reviewer has nothing left to say.

**Keep the work moving.** The expensive minutes are the ones spent waiting
on something the run could have done itself or done alongside. Never leave a
worker, a seat's answer, a device run or CI unwatched; do the next useful
thing while it runs, and end a turn only when the harness will wake you as it
lands. Examples: the boundary review goes out when the code is complete, with
the real check and CI running beside it; when CI did not start, start it;
when red CI blocks the milestone, fix it wherever it came from; run a check
now rather than at a chosen hour; merging main each time it moves reruns CI
and review without changing what ships. Ask: what could be moving right now,
and what is this wait buying?

## Seats

Two seats consult, named by the user at invocation and read exactly as
named: "primary Opus max, final Pro."
- **The final** writes the milestone plan and reviews the milestone at its
  boundary. With none named, it is GPT-6 Astra Pro.
- **The primary** reads each issue as it lands. With none named, it is a
  native child on the coordinator's own model, in a clean context.

These defaults replace the "Pro holds both" default in `issue-to-pr`. Seats
are consultants: they never edit the worktree or act on GitHub, a worker
never fills a seat, and the coordinator judges every answer. Read
`issue-to-pr`'s
[primary-and-final reference](../issue-to-pr/references/primary-and-final.md)
before the first consultation and again if the user renames a seat; its
transport rules apply to a seat the user named, not to the default primary.
A Pro seat means literal `Pro` read back from the `Chat` picker before Send,
in the consultation profiles only, never `Work`; `$chatgpt-web` owns how to
confirm Pro answered.

## Consulting the seats

Write every consultation from the matching family in `$chatgpt-web`'s
[consultation templates](../chatgpt-web/references/consultation-templates.md),
in the user's voice: K for the plan, A for the primary's read of an issue as
family L describes, L for the milestone review, B after fixes, G for a bug
local work cannot crack, E for an on-track check, I for a retry, J for a new
thread or account. Write from the template's own sentences: fill its
brackets and keep every question it asks, in its words; add what the
milestone needs; never shorten, paraphrase, or drop a question. Where a
template says Pro, read the model holding the seat.

Attach sources whole: the requirements source as a full export, the plan,
every issue as filed, the user's words verbatim, raw test output, and the PRs
with the `@GitHub` pill. Leave secret values out. Never ask for a verdict
token, cap the answer, fence what the seat may conclude, or pin a commit SHA.
Pro often takes around 30 minutes; keep working until it lands. Record each
submission once in the plan doc: seat, model as read from the page, purpose,
thread.

## Workflow

1. **Ramp up.** Read the plan or sheet, every issue in the milestone, linked
   PRs, and the user's words. Confirm which issues are still open and needed,
   and name the boundary. Adopt what earlier runs left: an issue that landed
   without a primary read gets one, and nothing still answering is resent.
   Stand up the intent police.
2. **Plan with the final, in one round.** Send K and ask for the full plan in
   one answer. Go back only with an open architectural question that would
   change what gets built, and ask just that. Save the plan in the plan doc
   and give each issue its work order. Process or gates the plan proposes are
   advice to weigh against the user's intent. A plan the final already wrote
   that still covers the milestone satisfies this step.
3. **Prove the verification path while the plan is written.** A worker shows
   that every lane the real check uses boots and that one existing journey
   passes on it. Fix what is broken first. A test command counts when it
   exercises behavior, not only style.
4. **Build.** Workers implement work orders in the plan's order, in parallel
   where it allows, and run focused checks. The coordinator reviews every
   changed line. The primary reads each landed issue with A in a clean
   context while the next issue keeps moving. Intermediate pushes skip CI
   where the repo allows it. Take a blocker local work cannot crack to the
   final with G.
5. **Boundary.** When every issue has landed and the primary's warranted
   findings are fixed, push the commit that completes the milestone and check
   that CI and the bots started. Send L at once and run the real check on
   the same head alongside it.
6. **Repair once.** Sort the final's findings, CI and the bots against the
   user's intent with the intent police. Workers make the warranted fixes in
   one batch; the coordinator reviews them; the primary confirms the fixes
   the review named. Send B only when the repair changed the design the
   review rested on. Record each declined finding with its reason.
7. **Close out.** Update the tracker, the issues, and any announcement once,
   then close the run's browser pages.

## Browser pages

Many runs share one BrowserOS, so each page this run opens is this run's to
close. Keep a seat's thread page open while the milestone is in flight; when
moving profiles, verify the new page first, then close this run's pages in
the old one; when the run ends or is handed off, close every page it created
and none it did not. `$browseros` owns the mechanics.

## Persistent runs and delegation

For a persistent run, author the goal prompt with `$prompt-authoring` and
`$startup-pragmatism`, carrying this north star. Name both seats with their
exact model, effort and threads, the milestone and its boundary, the
unblocker per `$unblocker`, the coordinator's ownership of decisions and
skill authorship, and the merge-ready condition. Arm the goal and unblocker
with the harness's supported mechanisms, and carry any change of direction
into the goal, the unblocker charter, and active briefs.

`$delegated-implementation` owns worker selection, briefs, direct review,
and repair. Read the installed `../_shared/agent-orchestration-policy.md`
before dispatch and apply `$prompt-authoring` to each populated brief. A
brief carries the issue's work order and the plan, the milestone branch, the
checks to run, the delivery rules (no PR, no CI waits), the unblocker
contact, and the expected handoff. Workers never consult seats.

## Merge-ready

The milestone is merge-ready when the final reviewed it at the boundary;
the primary read each issue that changed code and the coordinator reviewed
every changed line; the material findings are fixed, or declined against
the user's intent with the reason recorded; the real check passed on the
head being called ready; and CI ran on that head and is green, or its red is
fixed or named with its cause when it comes from outside the milestone and
is out of reach. A repo without CI is reported as having none. When the PR
also carries later milestones' work, the same bar makes the milestone
accepted; the PR merges when the user decides.

**Report** what the user can now do, or the result they asked for, first.
Then the PR links, what each issue delivered, current heads and CI, and what
only the user can do, said once. Seat detail goes in the PR body: each seat's
model, the revision it reviewed, what it said, and the coordinator's
conclusion, with later changes only the primary confirmed named separately.
Never imply a seat reviewed a revision it did not see.
