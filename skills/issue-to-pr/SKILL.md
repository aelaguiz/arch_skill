---
name: issue-to-pr
description: "Explicit-invocation delivery lane, fired only when the user invokes it by name (\"issue-to-pr on 4484\") or a wrapping skill the user invoked (epic-to-prs) delegates to it; never self-select it as a helper for adjacent work. Takes one GitHub issue to a merge-ready, externally reviewed PR through a fixed pipeline: ramp up on the issue, full implementation plan on disk shaped by $startup-pragmatism, one GPT Pro plan review via $chatgpt-web (literal Pro (5/5)), implement and test in a worktree, PR via $pr-authoring and $pr-review-followthrough, one GPT Pro review of the exact PR head, then stop at merge-ready with receipts. Fix-verification re-reviews are allowed until Pro approves; scope expansion from any reviewer is rejected or escalated. Never merges, never releases, never applies approval labels. Not for investigation-only asks (root cause without delivery), standalone planning, or work with no GitHub issue."
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
  bot, or agent may expand it; a genuine scope conflict escalates to the user
  as one question with a recommendation. Never silently shrink scope either.
- The implementation plan lives on disk before implementation starts, shaped
  by `$startup-pragmatism` (the overbuild cut happens at plan time).
- External review means GPT Pro through `$chatgpt-web`: the literal Pro (5/5)
  picker entry, in the most applicable ChatGPT project, honoring every rule
  in that skill. One review round per gate for the artifact; after applying
  fixes, fix-verification re-reviews are allowed until Pro approves the
  fixes. What is banned is the open-ended feedback loop and scope growth in
  any round.
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
   attached. Apply the verdict with judgment: take what is agreed with,
   escalate genuine scope disputes, never scope creep. Re-verify fixes with
   Pro until approved when the verdict demanded changes.
4. **Implement and test.** Dedicated worktree, smallest coherent change,
   self-documenting code with clear comments at boundaries and role seams.
   Run the relevant tests and the repo's required checks.
5. **PR.** `$pr-authoring` for the PR, then `$pr-review-followthrough` to
   drive review threads and CI to clean.
6. **Pro PR review.** One round on the exact current head. Apply fixes with
   the same verdict discipline; fix-verification re-reviews until approved;
   a changed head goes back to Pro.
7. **Stop at merge-ready.** Report: PR URL, one-line change summary, plan
   verdict, PR verdict on the final head, CI state, head SHA, and any
   escalations. Do not merge.

## Escalation contract

When blocked (ambiguous contract, scope conflict, failing dependency, a
reviewer demanding out-of-scope work), surface exactly one question with a
recommendation and stop that gate. Do not loop, do not decide scope, do not
quietly deliver less.

## Delegation

When this skill runs in a harness with child agents and the work is
delegated, read the installed `../_shared/agent-orchestration-policy.md`
before dispatch and apply `$prompt-authoring` to the populated child brief.
The pipeline order, verdict discipline, and receipts contract in this skill
travel into every brief unchanged.

## References

- [references/dispatch-evidence.md](references/dispatch-evidence.md): the
  verbatim dispatch templates and correction history this skill encodes.
