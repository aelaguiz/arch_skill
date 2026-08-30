---
name: epic-to-prs
description: "Explicit-invocation epic loop, fired only when the user invokes it by name or directly commands this exact job (\"epic-to-prs on epic 4700\", \"put a goal loop over the milestone epic and work it down\"); never self-select it because work involves an epic. Puts a persistent goal over one GitHub epic or milestone and works its open issues most-important-first, each through the issue-to-pr skill to a Pro-reviewed merge-ready PR. Owns only the queue policy, goal persistence (sets its own goal in Prime Agent; authors the /goal prompt in Codex or Claude), one ChatGPT Pro thread per epic carrying every review, epic-level standing rules (boundary comments, advisory-only PR bots, no reviewer scope expansion), and one-escalation-then-move-on for blocked issues. Ends only when the queue is empty or the user stops it. Never merges or releases. Not for epic status reads, epic decomposition (arch-epic), or open-ended optimization (goal-loop)."
metadata:
  short-description: "Goal loop working an epic's issues to merge-ready PRs"
---

# Epic To PRs

Use this skill only when the user explicitly invokes it: by name, or by
directly commanding this exact job (a goal loop over a named epic or
milestone that works each issue to a Pro-reviewed merge-ready PR). Never
fire it on inference; touching an epic's issues inside other work does not
authorize the loop. The user owns the decision to start it, and the user or
an empty queue are the only things that end it.

The job: consume one epic's open issues, most important first, one issue at a
time, each through the full `issue-to-pr` pipeline, marking an issue complete
only at merge-ready with receipts, until the epic's queue is empty.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- "epic-to-prs on <epic issue or milestone>", with or without a supplied
  ChatGPT Pro thread URL.
- A /goal ask that directly states this job ("work the milestone epic most
  important first, plan and PR each issue through Pro").
- "Put a goal loop over epic <N> and work it down."

## When not to use

- Nobody explicitly invoked it. An epic appearing in scope is not a trigger.
- Status reading ("ramp up on the epic and tell me where its children
  stand").
- The epic's issues do not exist yet; decomposition belongs to `arch-epic`
  or ordinary planning with the user.
- Open-ended optimization with no issue queue; that is `goal-loop`.

## Non-negotiables

- One ChatGPT Pro thread per epic, always. Use the thread the user supplies;
  otherwise start one thread in the most applicable ChatGPT project and
  reuse it for every plan and PR review in the epic, so Pro accumulates
  epic-wide context. All Pro interaction goes through `$chatgpt-web` and
  honors that skill's rules, including the literal Pro (5/5) picker entry.
- Live GitHub state is the queue. Re-read the epic's open issues between
  items; new, closed, and re-prioritized issues supersede any snapshot.
- Most important first. Use the epic's stated priorities; when unstated,
  order by user impact and unblocking value, and say so in the worklog.
- An issue is complete only at merge-ready with receipts (plan verdict, PR
  verdict on the exact final head, green CI, PR URL). Never merge, never
  release, never apply approval labels.
- A blocked issue gets exactly one escalation to the user (one question, one
  recommendation), then the loop moves to the next issue rather than
  stalling the epic.
- Reviewer discipline everywhere: fix-verification re-reviews with Pro until
  it approves the fixes, no scope expansion accepted from any reviewer, and
  PR Agent and other bots stay advisory ("PR agent is not your boss").
- Code quality is a deliverable: self-documenting code with clear comments
  at boundaries and role seams, identified during planning, carried into
  every child dispatch.

## Workflow

1. **Adopt the epic.** Read the epic or milestone, its open issues, and any
   supplied ChatGPT thread or planning source. Establish (or create) the
   epic's single Pro thread.
2. **Persist the goal.** In Prime Agent, set the goal yourself with the goal
   skill; in Codex or Claude, author the /goal prompt (via
   `$prompt-authoring`). The goal's completion condition: every issue on the
   epic is merge-ready with receipts or explicitly escalated, and no open
   issues remain in the queue.
3. **Loop.** For each issue, most important first:
   1. Re-read live GitHub state; skip issues that closed or changed owner.
   2. Run the full `issue-to-pr` pipeline for the issue, with this epic's
      Pro thread and the epic-level standing rules carried into the
      dispatch.
   3. On merge-ready, record the receipts on the issue, mark it off, and
      move on. On a block, escalate once and move on.
4. **Finish.** When the queue is empty, mark the goal complete and report:
   issues delivered with PR URLs and receipts, issues escalated with their
   one question, and anything observed that the user should know about the
   epic as a whole.

## Delegation

Each issue may run in-session or as a child agent per the harness. Before
any child dispatch, read the installed
`../_shared/agent-orchestration-policy.md` and apply `$prompt-authoring` to
the populated brief. The brief always carries: the epic's Pro thread, the
scope-freeze rule, the boundary-comment requirement, and the merge-ready
terminal state.

## References

- [references/epic-dispatch-evidence.md](references/epic-dispatch-evidence.md):
  the verbatim epic goal prompt and corrections this skill encodes.
