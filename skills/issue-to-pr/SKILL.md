---
name: issue-to-pr
description: "Explicit-invocation delivery lane, fired only by name (\"issue-to-pr on 4484\") or by user-invoked epic-to-prs; never self-select it. Takes one GitHub issue to a merge-ready, externally reviewed PR: ramp up, plan on disk shaped by $startup-pragmatism, one goal-framed GPT Pro plan review via $chatgpt-web (literal Pro (5/5)), implement/test in a worktree, PR via $pr-authoring and $pr-review-followthrough, one goal-framed Pro review of the exact PR head, then stop at merge-ready with receipts. Every Pro consult carries the issue's goal, scope, and believed critical path so Pro catches tangents and lost threads; never narrow yes/no approvals. Fix re-reviews until Pro approves. Run starts authorized: invented approval gates and blockers go once, with full context, to the run's unblocker ($unblocker) or Pro, never parked in waiting-for-user; user escalation only for user-owned matters. Never merges or releases. Not for investigation-only asks, standalone planning, or work with no GitHub issue."
metadata:
  short-description: "One issue to a Pro-reviewed merge-ready PR"
---

# Issue To PR

Use this skill only when the user explicitly invokes it. The user saying
"issue-to-pr on <issue>" (or an equivalent direct command naming this exact
job), or the user-invoked `epic-to-prs` skill delegating one issue, are the
only valid triggers. Never fire it because a task merely resembles delivery
work: the user owns the decision to run this lane.

The job: take one GitHub issue from cold start to a merge-ready pull request
whose plan and final head were both reviewed by GPT Pro, with the smallest
change that delivers the issue's accepted scope, then stop.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- The user says "issue-to-pr on <number or issue URL>", singly or as a list
  (a list is independent sequential or parallel invocations, not a batch
  manager).
- The user gives a direct command that names this exact pipeline: plan the
  issue, one Pro review of the plan, implement, PR, one Pro review of the PR,
  stop at merge-ready.
- The user-invoked `epic-to-prs` loop hands over one issue.

## When not to use

- Nobody explicitly invoked it. Working an issue, fixing a bug, or opening a
  PR inside other work does not authorize this skill; do what the user
  actually asked instead.
- The ask is investigation or root cause without delivery ("ramp up on 4408
  and root cause it").
- The ask is a standalone plan, review, or PR step; use the owning skill
  directly.
- There is no GitHub issue. Ask for one or work outside this skill.

## Non-negotiables

- Scope is the issue's accepted scope, frozen at contract time. No reviewer,
  bot, or agent may expand it; a genuine scope conflict goes to the Pro
  thread to arbitrate against the frozen contract, and only a real change to
  what the user asked for goes to the user as one question with a
  recommendation. Never silently shrink scope either.
- The implementation plan lives on disk before implementation starts, shaped
  by `$startup-pragmatism` (the overbuild cut happens at plan time).
- External review means GPT Pro through `$chatgpt-web`: the literal Pro (5/5)
  picker entry, in the most applicable ChatGPT project, honoring every rule
  in that skill. One review round per gate for the artifact; after applying
  fixes, fix-verification re-reviews are allowed until Pro approves the
  fixes. What is banned is the open-ended feedback loop and scope growth in
  any round.
- Pro is a thinking partner reviewing work against the goal, never an
  approval buzzer. Author every Pro prompt with `$prompt-authoring` - this
  is required, not optional - and give Pro the whole picture: the issue's
  intent in the user's words, the frozen scope, what has happened so far,
  and what you believe the critical path is, alongside the artifact. Ask
  Pro to judge the work against the goal - is this on track, is the next
  step the right critical path, has the thread been lost - never a narrow
  yes/no on a context-free snapshot.
- Be paranoid about tangents. Any work the issue does not name - a new
  dependency, a recovery task, a production operation, an infrastructure
  detour - is presumed drift until Pro, shown the full goal context,
  confirms it belongs on the critical path. When Pro says the thread is
  lost, that is a verdict: drop the tangent and return to the issue.
- The run starts authorized. If the issue's accepted scope names the work
  and it touches no production surface, permission already exists;
  inventing a mid-run approval gate is the failure, not caution. An "I
  need authorization" moment goes to the run's unblocker (per
  `$unblocker`) when one is armed, else the Pro thread, and gets decided
  from the issue's intent. Waiting-for-user is never a resting state.
- The PR review round binds to the exact current head; a changed head
  invalidates the verdict.
- PR Agent and other repo bots are advisory. Handle their threads with
  judgment per `$pr-review-followthrough`; they are not the boss and never a
  reason to expand scope.
- Terminal state is merge-ready with receipts. This skill never merges, never
  releases, never applies `ufc-approved` or any approval label, and never
  touches production surfaces.
- Implementation happens in a dedicated worktree per the target repo's own
  conventions (read its AGENTS.md; repo law outranks this skill on local
  mechanics).

## Workflow

1. **Ramp up.** Read the issue, its parent epic, linked PRs, and recent
   discussion. Live GitHub state is authority. Confirm the issue is still
   open, unclaimed, and not already fixed; for bug-typed issues, confirm the
   defect still reproduces (repro-first) before planning a fix.
2. **Plan on disk.** Write a full implementation plan to a file, apply
   `$startup-pragmatism` to it, and record acceptance, non-goals, and the
   verification the change needs.
3. **Pro plan review.** One round via `$chatgpt-web` with the plan file
   attached, framed per the Pro-prompting rule: the issue's goal, the
   frozen scope, and the question of whether this plan delivers that goal
   on the shortest sound path. Apply the verdict with judgment: take what
   is agreed with, arbitrate genuine scope disputes in the Pro thread,
   never scope creep. Re-verify fixes with Pro until approved when the
   verdict demanded changes.
4. **Implement and test.** Dedicated worktree, smallest coherent change,
   self-documenting code with clear comments at boundaries and role seams.
   Run the relevant tests and the repo's required checks.
5. **PR.** `$pr-authoring` for the PR, then `$pr-review-followthrough` to
   drive review threads and CI to clean.
6. **Pro PR review.** One round on the exact current head, framed the same
   way: the goal, the scope, what shipped, and whether the delivered change
   still serves the issue's goal. Apply fixes with the same verdict
   discipline; fix-verification re-reviews until approved; a changed head
   goes back to Pro.
7. **Stop at merge-ready.** Report: PR URL, one-line change summary, plan
   verdict, PR verdict on the final head, CI state, head SHA, and any
   escalations. Do not merge.

## Unblocking contract

Blocked or unclear means consult, not stall. On any blocker (ambiguous
contract, scope conflict, failing dependency, a reviewer demanding
out-of-scope work), take it to the run's unblocker when one is armed,
else the Pro thread this issue is already using, with the full goal
context: state the blocker, the options, and your
recommendation, and ask two things - the right way to proceed, and whether
this blocker is actually on the issue's critical path or independent
in-scope work can continue while it pends. The goal is to get unblocked
and keep delivering. Only when Pro cannot resolve it - the matter needs
the user's authority, their access, or changes what they asked for -
surface exactly one question with a recommendation to the user and stop
that gate. Ask any question once: while an answer pends, work the
remaining unblocked scope or stop the gate; never re-ask, and a generated
continuation or wake-up is not a new answer. Do not idle waiting, do not
decide scope unilaterally, do not quietly deliver less.

## Running as a persistent goal

When this lane runs under a persistent goal (a long or overnight run),
author the goal prompt yourself via `$prompt-authoring`: it names the Pro
thread, the unblocker per `$unblocker` and how to reach it, and the rule
that blocked or needing authorization means consult the unblocker, never
park in waiting-for-user. In Prime Agent, arm the goal and spawn the
unblocker yourself; otherwise present the exact /goal text and unblocker
spawn instruction for the user to arm.

## Delegation

When this skill runs in a harness with child agents and the work is
delegated, read the installed `../_shared/agent-orchestration-policy.md`
before dispatch and apply `$prompt-authoring` to the populated child brief.
The pipeline order, verdict discipline, and receipts contract in this skill
travel into every brief unchanged.

## References

- [references/dispatch-evidence.md](references/dispatch-evidence.md): the
  verbatim dispatch templates and correction history this skill encodes.
