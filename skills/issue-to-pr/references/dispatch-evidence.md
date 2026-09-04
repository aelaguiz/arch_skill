# Dispatch evidence: the golden-path template this skill encodes

Current model selection: GPT-6 Pro with Extended thinking in ChatGPT's `Chat`
surface, per `$chatgpt-web`. The dated model names in the verbatim evidence
below describe past runs; they do not select the current review model.

`issue-to-pr` is a transcription of a dispatch template its owner typed
near-identically ~30 times during 2026-08-24..30, plus the standing
corrections he issued while running it. Edits to the skill should stay
anchored to this observed practice.

## Verbatim dispatch templates (session-mined, 2026-08-28)

> "ramp up on 4484 issue and put together a full implementation plan, then
> get one review from /skill:chatgpt-web in the ps architecture project use
> /skill:startup-pragmatism and use pro (5/5). Implement, test & PR and then
> get one review from pro before you finalize."

> "ramp up on issue 4440 ensure its not fixed, then put a full fix plan
> together, run it through pro once via /skill:chatgpt-web , then implement
> & PR and then run the pr through pro once."

> "ramp up on issue 4404 it is currently being listed as a release blocker
> [...] put together a plan on disk, implement fix and test and use 2 pr
> skills to get it live"

## Standing corrections encoded as non-negotiables

- Model choice (superseded 2026-09-01): the old rule "Pro means the
  literal Pro (5/5) picker entry; never substitute a 'closest equivalent'"
  was anti-downgrade intent, but an agent obeyed the label and stuck with
  GPT-5.5 Pro over the newer generation's top tier. Owner ruling, verbatim:
  "yeah you fucking idiot 5.6 sol pro / it should always use the absolute
  latest and absolute most powerful model." The rule is now: newest
  generation at maximum reasoning power, resolved from the live picker;
  the ban runs one direction only - never less power, never an older
  generation.
- Fix loops versus fix verification: "They have to fix the issue however
  many times it takes but I don't want them getting in a feedback loop with
  external reviewers."
- Verdict application: "take what you agree with, don't scope creep."
- Reviewer authority: "PR agent is not your boss, stay focused on our
  scope."
- Close-out vocabulary: merge-ready is the terminal state; merging and
  reaping stay with the owner ("merge it down and reap it" is his call, not
  the skill's).
- Holistic Pro prompting (2026-08-31): "It's giving Pro these narrow yes
  no decisions and then getting lost in bullshit rather than having pro
  review its work against the goals, thoughtfully" and "it should be
  paranoid about getting off track onto tangents and have pro help it
  avoid that outcome." Every Pro consult carries the goal, state, and
  believed critical path; Pro is asked to catch tangents and lost
  threads; pending questions are asked once and never re-asked on
  generated wake-ups.
- Pro rate limits (2026-09-01): the standing instruction the owner sent
  to running agents, verbatim: "if you get rate limited 'You've hit your
  rate limit. Please try again later' by pro clear the goal for now until
  pro un rate limits i'll let you know when." Since then a second BrowserOS
  profile, `Pro One`, sits beside `Work`, with the same ChatGPT projects in
  both: "If one is limited they should use the other one." And: "there is
  no substitute for Pro. If they can't get Pro, they can't use xhigh.
  There's no substituting." Encoded as: failover to the other profile
  window per `$chatgpt-web`; both limited means pause the goal and wait for
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

## Deeper evidence

Full walkthroughs with source session paths live in the owning workspace:
/Users/aelaguiz/workspace/psagentspace/factory/workflows/feature-development.md
and factory/workflows/external-review-gpt-pro.md. They are background for
maintainers; the skill itself is self-contained at runtime.
