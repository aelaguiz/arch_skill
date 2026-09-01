# Dispatch evidence: the golden-path template this skill encodes

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

- Literal Pro: "Pro means the literal Pro (5/5) picker entry; never
  substitute a 'closest equivalent'."
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

## Deeper evidence

Full walkthroughs with source session paths live in the owning workspace:
/Users/aelaguiz/workspace/psagentspace/factory/workflows/feature-development.md
and factory/workflows/external-review-gpt-pro.md. They are background for
maintainers; the skill itself is self-contained at runtime.
