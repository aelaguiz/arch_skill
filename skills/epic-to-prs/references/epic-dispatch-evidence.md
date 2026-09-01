# Epic dispatch evidence

`epic-to-prs` transcribes the owner's live epic goal prompts (2026-08-30,
multiple running concurrently). The canonical verbatim example:

> "/goal your job is to review
> https://chatgpt.com/g/g-p-6a89c1cafaec8191b7016f9d3ca90d2a-ps-architecture/c/6a940958-c0c4-83ea-9fa8-09695ef60e14
> and pull each of the new issues most important first (they are on
> milestone epic), build a plan to implement, get one round of feedback from
> Pro on the plan, implement the plan and test it then get a review on the
> PR(s) you touched from Pro, before marking the issue off as complete and
> moving to the next one. Use the gpt web skill to interact with pro on this
> thread. You can re-review with Pro after doing fixes until Pro approves
> the fixes but do not scope expand on those reviews. I want you to comment
> the code, especially as part of your planning work, especially when we're
> identifying boundaries and roles. It needs to be really clear so the code
> needs to be self-documenting. I want you to be very careful to not end up
> in a feedback loop especially when getting PR agent reviews on the PR. PR
> agent is not your boss, stay focused on our scope."

Rulings folded in:

- One thread per epic, always (owner ruling 2026-08-30); the thread may be
  supplied or created, and it carries every review for the epic.
- Fix re-reviews until Pro approves are sanctioned; scope expansion in any
  round is not. The banned thing is the open-ended reviewer feedback loop.
- Boundary and role comments are a planning deliverable, not polish.
- In Prime Agent the agent sets the goal itself; the /goal text above is
  the Codex-form of the same contract.
- Holistic Pro prompting (owner ruling 2026-08-31, after a five-hour epic
  session death-looped): "It's giving Pro these narrow yes no decisions
  and then getting lost in bullshit rather than having pro review its
  work against the goals, thoughtfully" and "it should be paranoid about
  getting off track onto tangents and have pro help it avoid that
  outcome." Observed failure: the loop promoted an undeclared dependency
  into the critical path, serialized independently buildable issues
  behind it, self-imposed an approval gate, and re-asked the same two
  pending questions hundreds of times across generated goal
  continuations, while Pro only ever saw narrow plan/PR snapshots and so
  approved locally correct work on the wrong path.

Maintainer background (not needed at runtime):
/Users/aelaguiz/workspace/psagentspace/factory/workflows/feature-development.md
and factory/plans/drafts/2026-08-30-issue-to-pr-and-check-my-agents-skills.md.
