# Epic dispatch evidence

Current cadence (owner direction, 2026-09-04): use Pro for initial planning,
meaningful batch checkpoints, major problems unresolved by local reasoning,
and final review. Related issues share planning and reviews; ordinary fixes
are verified locally. If both accounts are limited, pause the blocked Pro
decision while independent authorized work continues. `../SKILL.md` owns
this runtime contract. The historical prompts below do not reinstate
per-child reviews, automatic reapproval loops, or blanket whole-goal pauses.

Current model selection: GPT-6 Pro with Extended thinking in ChatGPT's `Chat`
surface, per `$chatgpt-web`. The dated model names in the verbatim evidence
below describe past runs; they do not select the current review model.

`epic-to-prs` originated from the owner's epic goal prompts (2026-08-30,
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

Historical rulings (cadence superseded above):

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
- Pro rate limits (2026-09-01): the standing instruction the owner sent
  to running agents, verbatim: "if you get rate limited 'You've hit your
  rate limit. Please try again later' by pro clear the goal for now until
  pro un rate limits i'll let you know when." Since then a second BrowserOS
  profile, `Pro One`, sits beside `Work`, with the same ChatGPT projects in
  both: "If one is limited they should use the other one." And: "there is
  no substitute for Pro. If they can't get Pro, they can't use xhigh.
  There's no substituting." Encoded as: failover to the other profile
  window per `$chatgpt-web` (the one exception to one thread per epic:
  a continuation thread in the other account, both URLs recorded); both
  limited means pause the goal and wait for
  the owner, never a lesser tier, effort, model, or reviewer.

- Chat surface, not Work (2026-09-02): an agent ran a "max power" review
  as `5.6 Sol Ultra` in ChatGPT's `Work` surface and reported it as Pro.
  Owner, verbatim: "So you're running it in work mode. You need to run it
  in chat mode and Sol Ultra is not the same as Pro. You have to re-do
  this." and "There is 'chat' and 'work' tabs in chatgpt. if it starts it
  in work it doesn't get pro. Ultra != Pro." Encoded as: `$chatgpt-web`
  checks the `Select chat surface` radio is `Chat` before the model pill
  and before every send; Pro exists only in `Chat`; a `Work` send is not
  a Pro verdict and is redone.

Maintainer background (not needed at runtime):
/Users/aelaguiz/workspace/psagentspace/factory/workflows/feature-development.md
and factory/plans/drafts/2026-08-30-issue-to-pr-and-check-my-agents-skills.md.
