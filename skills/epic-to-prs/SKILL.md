---
name: epic-to-prs
description: "Explicit-invocation epic loop, fired only by name or direct command (\"epic-to-prs on epic 4700\"); never self-select it. Works one epic or milestone under a persistent goal, its issues most-important-first through issue-to-pr to Pro-reviewed merge-ready PRs. Owns queue policy, goal persistence with an armed run unblocker ($unblocker) baked into the goal prompt (self-armed in Prime Agent; exact /goal text handed over otherwise), one GPT-6 Pro thread per epic as standing goal advisor (every review plus on-track checks catching tangents, undeclared dependencies, wrong critical paths, lost threads), epic standing rules (boundary comments, advisory-only bots, no reviewer scope expansion), and unblocker-first consults (self-imposed approval gates get decided, not parked; questions asked once; independent issues never serialized behind an unrelated blocker). Ends only on empty queue or user stop. Never merges or releases. Not for epic status reads, decomposition (arch-epic), or open-ended optimization (goal-loop)."
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

- One GPT-6 Pro thread per epic, always. Use the thread the user supplies;
  otherwise start one thread in the most applicable ChatGPT project and
  reuse it for every plan and PR review in the epic, so Pro accumulates
  epic-wide context. All Pro interaction goes through `$chatgpt-web` and
  honors that skill's model rule: GPT-6 Pro with Extended thinking, the
  newest generation at maximum reasoning power verified in the live picker,
  always in ChatGPT's `Chat` surface. Work's reasoning slider does not select
  Chat Pro; redo any review sent from `Work` in `Chat`. Threads live in one
  ChatGPT account, so the one sanctioned exception is a rate-limit failover
  per `$chatgpt-web`: when the thread's BrowserOS profile window (`Pro One`
  or `Work`) is rate limited, start a continuation thread in the same-named
  project in the other window, restate the epic context there, record both
  URLs in the goal prompt and worklog, and return to the epic's original
  thread once its account is available.
- There is no substitute for Pro. If both profile windows are rate limited
  (`You've hit your rate limit. Please try again later` in each), do not
  review with a lower tier, a lower effort, an older model, another
  provider, or a different reviewer, and do not mark an issue complete
  without its Pro verdicts. Clear or pause the goal for now, report the rate
  limit, and wait for the user to say Pro is back.
- Pro is the epic's standing advisor, never an approval buzzer. Author
  every consult with `$prompt-authoring` - required, not optional - and
  give Pro the epic's goal, the live queue state, what is done, and what
  the loop proposes next, then ask it to review the work against the
  epic's goal rather than answer a context-free yes/no.
- Be paranoid about losing the thread. At every issue boundary, and
  whenever the plan, dependencies, or critical path change, ask the Pro
  thread the holistic question: is the loop still delivering this epic, is
  the next item the right critical path, has it promoted a dependency the
  epic never declared, is it doing work another lane owns? Work the epic
  does not name is presumed a tangent until Pro, shown the full context,
  confirms otherwise; when Pro says the loop has drifted, drop the tangent
  and return to the queue.
- The run starts authorized. Authorization gates come from the user's ask,
  the epic, or the production boundary - never from mid-run anxiety.
  Deciding partway in that you need the user's approval is presumed a
  self-imposed gate: take it to the epic's unblocker (per `$unblocker`),
  or to the Pro thread when none is armed, and get a decision from the
  plan's intent. Waiting-for-user is never a resting state.
- Decide like a startup. Apply `$startup-pragmatism` to every judgment
  call in the loop - ordering, blockers, when to move on - and decide at
  current information instead of building certainty. The pipeline's named
  receipts are the complete proof set: never invent extra limits,
  thresholds, proof harnesses, evidence bundles, or verification ceremony
  the epic did not ask for.
- Live GitHub state is the queue. Re-read the epic's open issues between
  items; new, closed, and re-prioritized issues supersede any snapshot.
- Most important first. Use the epic's stated priorities; when unstated,
  order by user impact and unblocking value, and say so in the worklog.
- An issue is complete only at merge-ready with receipts (plan verdict, PR
  verdict on the exact final head, green CI, PR URL). Never merge, never
  release, never apply approval labels.
- Blocked means consult, not stall. A blocked or unclear issue goes to the
  epic's unblocker first when one is armed, else the epic's Pro thread,
  with full goal context: state the blocker, the
  options, and a recommendation, ask whether the blocker actually gates
  the remaining queue or independently buildable issues can proceed, and
  work it with Pro until there is a way forward. Never serialize
  independent issues behind an unrelated blocker. Only a matter Pro cannot
  resolve because it genuinely needs the user (their authority, their
  access, or a change to what they asked for) gets one escalation - one
  question, one recommendation - and then the loop moves to the next issue
  rather than stalling the epic. Ask any question once; while an answer
  pends, work other queue items, and a generated goal continuation or
  wake-up is never license to re-ask.
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
2. **Arm the run.** Stand up the epic's unblocker per `$unblocker`,
   charged with the user's verbatim ask, the epic, and the production
   boundary. Then author the goal prompt via `$prompt-authoring`, shaped
   by `$startup-pragmatism` so it drives delivery rather than ceremony: it
   names the Pro thread, the unblocker and how to reach it, the rule that
   blocked or needing authorization means consult the unblocker - never
   park in waiting-for-user - and no proof or receipt demands beyond the
   pipeline's own. In Prime Agent, set the goal yourself
   with the goal skill and spawn the unblocker; in Codex or Claude,
   present the exact /goal text and unblocker spawn instruction for the
   user to arm. The goal's completion condition: every issue on the epic
   is merge-ready with receipts or explicitly escalated, and no open
   issues remain in the queue.
3. **Loop.** For each issue, most important first:
   1. Re-read live GitHub state; skip issues that closed or changed owner.
   2. Run the full `issue-to-pr` pipeline for the issue, with this epic's
      Pro thread and the epic-level standing rules carried into the
      dispatch.
   3. On merge-ready, record the receipts on the issue, mark it off, run
      the issue-boundary on-track check in the Pro thread, and move on. On
      a block, take it to the epic's Pro thread and get unblocked; only if
      it still needs the user, escalate once and move on.
4. **Finish.** When the queue is empty, mark the goal complete and report:
   issues delivered with PR URLs and receipts, blockers Pro resolved and
   how, any issues escalated with their one question, and anything observed
   that the user should know about the epic as a whole.

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
