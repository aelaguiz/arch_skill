# Epic dispatch evidence

Current cadence (owner direction, 2026-09-04): use Pro for initial planning,
meaningful batch checkpoints, major problems unresolved by local reasoning,
and final review. Related issues share planning and reviews; ordinary fixes
are verified locally. If all available accounts are limited, pause the blocked Pro
decision while independent authorized work continues. `../SKILL.md` owns
this runtime contract. The historical prompts below do not reinstate
per-child reviews, automatic reapproval loops, or blanket whole-goal pauses.

Current model and account selection (owner direction, 2026-09-13): GPT-6 Astra
with the literal `Pro` option and Extended thinking in ChatGPT's `Chat` surface,
per `$chatgpt-web` with required `$browseros` usage. Pro is not Extra High,
xhigh, Ultra, Thinking, or the highest available setting. Missing or disabled
Pro probably means a temporary account rate limit. Use only the already-open
numbered Pro profiles, such as Pro 1 through Pro 5 or whichever exist. The
user's `Work` profile is reserved for their personal use and rate-limit capacity;
never use it, even as a fallback. Note which eligible profile/window currently
offers Pro and use that account. Continue in the same-named project
with the needed context; all accounts should have the same projects.
Only after eligible Pro accounts are exhausted, pause the blocked Pro decision
while independent authorized work continues. This supersedes the historical
top-tier equivalence, Work-profile fallback, two-account limit, and whole-goal
pause guidance below;
verbatim quotations remain historical evidence, not current model selection.

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
  pro un rate limits i'll let you know when." At that time a second BrowserOS
  profile, `Pro One`, sat beside `Work`, with the same ChatGPT projects in
  both: "If one is limited they should use the other one." And: "there is
  no substitute for Pro. If they can't get Pro, they can't use xhigh.
  There's no substituting." The historical rule was: failover to the other profile
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

- Pro consultation voice (2026-09-16): the owner traced a Codex run
  (`01a0abbe-a311-75f0-9b87-ed006b673ccb`) that held the full planning
  workbook but sent Pro the issue body and test output, and reviewed the
  621-prompt inventory. Verbatim: "I have long suspected that the agents
  prompt in this incredibly myopic way... an agent will tell me, 'Oh I got
  a code review and Pro passed it,' and then I'll do the same code review
  with Pro and get a very different answer." "It's got a spreadsheet,
  right? It should be giving it the spreadsheet. It's not giving it the
  context." How he would prompt it: "Hey we're working on this plan. Here's
  the spreadsheet that we've been working out of. I've been working out of
  this branch. Here's the GitHub connector. Here's the branch. There's a PR
  you can read. I was working on this issue and I think I'm done. I'm
  looking for: did I implement the intent right?" For a review: "Look for
  things like: Where did I overbuild around edge cases? Where did I create
  new patterns where there were existing clean ones? Where did I create
  split brain? Where did I create a web of individual calls rather than a
  single centralized clear abstraction? Where am I working around an
  architectural limitation that I should be tackling first?" and "Is this
  the cleanest, most pragmatic way to do this? Where am I introducing risk
  that really wasn't necessary for this feature?" On heads: "you don't
  have to specify the exact head... putting in a SHA hash is an
  anti-pattern." On planning: "there's an inversion of responsibilities,
  right? You write up the plan. Outline this for me... I want Pro to
  outline the plan in all the places where there's a plan being written.
  I want Pro to do it not the agent... I will ask you questions and we'll
  go back and forth until it's a fully formed plan." What the plan
  contains: "a clear outcome we're after, top-level acceptance criteria,
  clear extremely clear requirements, a clear architectural plan, clear
  do's, clear do not's, a clear test plan." On the scaffold: "what I'm
  saying right now supersedes prompt authoring." On waiting, after an
  agent ended its turn with "read Pro's review when it lands": "No, don't
  tell me too, dude. You have to watch for it." Encoded as the family
  templates in `$chatgpt-web`'s `references/consultation-templates.md`,
  which this skill's Pro sections now point at.

- CI last (2026-09-17): agents waited on 30-minute CI runs before and
  between Pro rounds. Owner, verbatim: "Dude, we don't need to keep waiting
  for CI on every fucking turn. We can do CI at the very end after pro has
  cleared everything." and "we don't give a flying fuck about CI until it's
  the very very last step." Encoded as: Pro reads the pushed branch and needs
  nothing from CI; no CI waits or CI fixes before or between Pro rounds; CI
  and bot follow-through run once after Pro has cleared the PR.

Maintainer background (not needed at runtime):
/Users/aelaguiz/workspace/psagentspace/factory/workflows/feature-development.md
and factory/plans/drafts/2026-08-30-issue-to-pr-and-check-my-agents-skills.md.
