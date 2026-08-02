# Session Evidence 1: Amir's Standard Run Recipe And Repeated Instructions

Date: 2026-08-02. Source: mining of 2,196 session JSONL files across all 18
aimgr claude homes plus `~/.claude/projects` — 5,280 distinct human-typed or
dictated user messages (tool results and sidechains excluded). Citation format:
`(home|project|session-prefix|date)`. Raw corpus retained in the session
scratchpad (`user_msgs.jsonl` + themed dumps).

Headline counts: 233 messages mention conductor, 173 worktree, 154 Sol,
87 cynical, 76 adversarial, 51 contain a "you own scope/architecture/quality"
clause, 37 wall-clock discipline, 26 explicit "scope creep", 19 sim-pinning,
19 worktree-pinning, 15 "lesser agent" plan-quality bar.

**Implication for the interview skill:** everything below is boilerplate Amir
re-dictates per run. The interview should capture it once per plan (mostly as
confirm-the-default questions) and write it into the plan so no downstream
agent ever needs it re-typed.

## 1. The canonical run recipe (reconstructed, with quotes)

Two model eras, identical structure. Era 1 (Jul 3–9): Codex GPT-5.5 xhigh
implements, Sonnet 5 runs cynical skills. Era 2 (Jul 22–Aug 2, current):
Sol Ultra implements via `/conductor`, Fable xhigh is the adversarial
reviewer, Terra xhigh runs the three cynical skills, parent (Fable 5) owns
scope/architecture/quality, Sol does the PR skills. Late addition: Luna Max as
an extra cheap reviewer (Aug 2). Note: "care xhigh" in dictation = Terra xhigh.

- **Step 0 — root cause / ramp up first.** "Go look at all the different
  challenges... Diagnose them. Root cause them. Put together a fixed plan using
  one of our planning skills." (pro4|snap|3bfbff85|07-29)
- **Step 1 — plan via mini-arch skill, "lesser agent" bar.** "use the Mini-Arc
  Plan skill to build a full implementation plan such that a lesser agent could
  even implement it" (main|fix-pvai-headers|cdce27a6|07-09). Hard requirements
  at the top of the plan (pro7|psagentspace|07f28fd0|07-30). Test plan fully
  defined pre-dispatch: "Fully define the test plan, the automation we're gonna
  add, how we're gonna test every one of these things... before you use the
  conductor skill with Ultra" (pro4|psagentspace|dfe0a152|07-24).
- **Step 2 — bounded plan review, 1–3 rounds max.** "review it up to twice with
  5.6 ultra" (main|psagentspace|b93c8509|07-23). "Don't iterate until SOL
  agrees. You'll go back and forth forever. Do one round of iteration then use
  the conductor skill" (claudalyst|psmobile|1cc40d8b|07-26). "Your job is to
  stop once they start becoming incredibly pedantic... maximum of three
  feedback turns." (qa|psagentspace|2044e804|08-01). Adversarial plan review
  usually Fable xhigh, up to two rounds (pro11|psagentspace|1f74f3c5|07-29).
- **Step 3 — pin environment into the plan doc.** "Cut a work tree, put it in
  the doc, pin a sim, pre-name the sim so that it's ours, put it in the doc.
  Then dispatch this to Conductor Sol Ultra." (pro9|psagentspace|463b85ba|
  08-01). Worktree cut off origin/main (pro6|psmobile|302572db|07-25). Sim must
  be new/unused, renamed, one per role: "please pin the sims. Don't have it be
  opening tons of sims." (main|psmobile|7c508947|07-24). "One fucking branch,
  one PR" (pro4|psagentspace|816f6eaa|07-26).
- **Step 4 — dispatch to conductor with the ownership clause** (~51
  occurrences): "You own scope so it's not going out of control. You own
  architecture so it's not violating our principles. You own code review."
  (qa|psagentspace|39798384|07-28). Cost rationale: "You cost a lot more but
  have better architectural judgment. so preserve your own context and have GPT
  be the dispatcher." (main|psmobile|ea079ccd|07-22).
- **Step 5 — parent verifies first-hand, especially visuals.** "You personally
  review what we built versus the mock because it likes to change things in all
  sorts of ways, even labeling and how we have it laid out" (pro5|psagentspace|
  e0fc4053|07-31). "Make sure you inspect screenshots... before approving it."
  (main|feat-perf-again|fc27589b|07-06).
- **Step 6 — review waves at "done".**
  - Wave A, adversarial Fable xhigh vs requirements: "find violations of the
    requirements/missing the point/new UX/still bifurcated patterns"
    (pro7|psagentspace|07f28fd0|07-30).
  - Wave B, three cynical skills on Terra xhigh: "anything that is clearly a
    miss from our plan, but don't let it scope creep." (pro10|psagentspace|
    40c36ad5|08-01).
  - Wave C, optional fresh cold reads vs requirements, capped: "No more than
    two adversarial reviews or you'll get stuck in a loop" (qa|psagentspace|
    2044e804|08-01).
  - Findings are inputs, never verdicts: "Only fix what you agree with. Don't
    let them scope creep either" (illustrator|psagentspace|3e5a0ee4|07-31).
- **Step 7 — worker (never parent) does PR; parent watches it land.** "Only
  once it's fully done and everybody signs off, do the PR authoring and peer
  review follow-through skills. Have Sol Ultra do that." (pro10|psagentspace|
  40c36ad5|08-01). PR contract: before/after screenshots of the journey,
  embeds not links, "an exhaustive list of all user-facing template changes
  [and] a screenshot of every user-facing change for it to be a valid PR"
  (qa|psagentspace|16341e74|08-02). Then verify deploy actually landed
  (growth|psagentspace|9d7a3b97|07-31).

## 2. Repeated-instruction inventory (≥2 occurrences, by theme)

### Model selection (role → model)
- Implementation = Sol Ultra via conductor (~150+).
- Adversarial reviewer = Fable xhigh (~40).
- Three cynical skills = Terra xhigh (10 in era 2).
- Plan feedback = Sol Ultra, 1–2 revisions (21).
- Opus 5 only for keys/secrets/tokens (19): "Fable is just strung too tight"
  (claudalyst|psagentspace|147e5fe8|07-27); otherwise Opus distrusted for
  judgment (5).
- Rate limits → `aim codex use` rotation, never model swap (4).
- Luna Max as extra cheap reviewer (2, new 08-02).

### Environment pinning
- Cut worktree off origin/main, path pinned in the plan doc (20+).
- Pin + rename a dedicated new sim in the doc (19); never steal booted sims.
- One branch, one PR (4). Workers never commit; parent commits after audit (3).
- Keep a worklog / save findings docs as you go (62).
- Physical devices named explicitly when relevant (~15): pixel 10a, iphone 13
  pro, iphone 14 via mobile mcp.

### Review discipline
- "Fix only what you agree with" (56).
- Adversarial review vs requirements/intent (76).
- Reviewers will scope creep — treat as one input (~8 explicit).
- Cap review loops at 2–3 rounds (8).
- Resume the same reviewer session for continuity (7).
- Fresh/cold reads as a separate lane (37).
- Stable reviewer target list: bifurcated code paths, duplicate sources of
  truth, quarantined-not-deleted code, missed-the-point-on-UX, untested
  claims, drift-prone design.

### Scope control
- "You own scope / don't let it spiral" (51+16+26): "Codex is very smart, but
  it likes to scope creep hard." (main|psagentspace|572131e2|07-22)
- Plan/original intent is the authority; go back to it (~10): "make sure you
  understand the North Star of the plan in the first place before you do
  anything." (pro9|psagentspace|cb550a53|07-24)
- No new features/UX during fixes (~10): "even if one of the reviewers comes
  back with new scope from a features perspective, that's not allowed."
  (qa|psagentspace|54e5f1ae|08-01)
- No hypothetical/pedantic work (~8). Delete, don't quarantine (10).
- Simplicity bias / no overbuild (~15): "as simple as would be useful and no
  more. No insane overbuilds for hypothetical future needs." (pro8|
  psagentspace|80593e8d|07-30)

### Testing
- Fully-specified test plan inside the plan before dispatch (66).
- User-journey-mapped coverage, adversarially reviewed (~6): "build a complete
  user journey map end to end... then map your full test plan to every one of
  those user journeys" (pro4|psagentspace|859a3e1f|07-31)
- State setup reachable the way a real user/tester reaches it (4).
- New automation joins the default suite (7).
- Wall-clock discipline: don't re-run passed tests, no soaks (37): "Treat my
  time as valuable." (pro11|psagentspace|befa77da|07-28)
- Comment code to trap regressions (11).

### Autonomy and communication
- Don't ask questions; unblock from first principles (6+): "I'm going to bed.
  Don't fucking ask me questions. Don't get blocked. Go back to first
  principles... You have more than enough information to unblock yourself."
  (qa|psagentspace|39798384|07-29)
- Overnight/away runs are a standard mode (20).
- Session restarts via pasted handoff blobs: "ramp up on / pick this back up"
  (dozens).

## 3. Phrasing bank (verbatim guardrails — training data for the skill)

1. "You own scope, code quality, and architecture. You keep it from spiraling
   on weird edge cases."
2. "Codex is very smart, but it likes to scope creep hard."
3. "I seriously doubt that sol will ever say good enough and it'll scope creep
   this forever. You have to stop and examine at some point."
4. "Make sure it didn't quarantine things rather than fucking delete them."
5. "Don't support the old way and the new way. There's just the one way."
6. "No more weird fucking bifurcated features and legacy patterns for no
   reason."
7. "Don't just take sonnet at its word and it's not an approver. You have to
   interpret it."
8. "Until the adversarial reviewer who is disinclined to accept a surrender
   agrees, they're not done."
9. "Would this really prove that it works? What edge cases are you missing?
   What flows are not actually tested?"
10. "Let it do the grunt work but you code review it suspiciously."
11. "such that a lesser agent could implement it, fully specified"
12. "Pin a work tree and pin a sim and put them in the doc." / "pre-name the
    sim so that it's ours"
13. "One fucking branch, one PR." / "We do the PR when we're fully fucking
    done."
14. "I prefer image embeds to links." / before-and-after journey screenshots
    required in PRs.
15. "an exhaustive list of all user-facing template changes [and] a screenshot
    of every user-facing change for it to be a valid PR"
16. "You own wall clock efficiency... Don't let it rerun the same 18 tests
    every fucking time."
17. "The reason I did all that planning up front was so you would understand
    the North Stars and now we're in it and all of a sudden I have to answer
    75 questions."
18. "Go back to first principles. Look at what I'm trying to accomplish. You
    have more than enough information to unblock yourself."
19. "anything involving keys or decryption or anything like that happens on an
    Opus 5 agent, not the main Fable 5 agent"
20. "if you hit rate limits with codex just use 'aim codex use' to rotate"
21. "I want a deep solve but I also don't want you to build a bunch of new
    user experience."
22. "Don't let it make all of our labels autistic and make sure it gets
    deployed and works actually live." (labels/copy must stay human)
23. "You keep it wall-clock efficient, keep it smart, keep it on track and on
    scope. Be paranoid about this."

Quote #17 is the thesis of the whole skill: planning up front exists so that
execution never has to ask.
