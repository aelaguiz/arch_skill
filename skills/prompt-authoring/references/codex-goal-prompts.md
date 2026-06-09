# Codex Goal Prompts

Use this reference when the artifact is a Codex `/goal` prompt or a persistent
goal objective for a long-running agent session.

The job is not to fill out a form or duplicate a plan. The job is to write a
short mission brief that tells a future agent what world should be true, which
sources control the details, what false success looks like, and what evidence
proves done.

## Table of contents

- Mental model
- Form factor budget
- Source truth compression
- Authoring workflow
- Signoff as part of done
- Lightweight shapes
- Outcome examples
- Anti-patterns
- Final self-check

## Mental model

A `/goal` prompt is an index card for future work. It may guide many turns,
survive context compaction, resume after interruptions, call tools, or bring in
reviewers. It should be smaller than the plan, not a second plan.

Good goal prompts teach judgment:

- what result matters
- why quality matters at this layer
- which sources outrank guesses
- which workflow rules change the result
- which shortcuts would create a false success
- what evidence proves done
- when outside signoff is required
- how to keep moving when the path is unclear without silently cutting scope

Weak goal prompts either under-specify the result or over-specify the source
material. Both create guessing. A tiny "fix it properly" goal makes the agent
invent the acceptance test. A giant pasted plan makes the goal a competing
source of truth and hides the actual mission.

## Form factor budget

Codex `/goal` prompts have a hard cap of 4,000 characters. Treat that as an
emergency ceiling, not the target.

- Complex goals should usually land around 2,000-3,000 characters.
- Goals that point at a rich source doc should usually be 800-1,800 characters.
- Small repair goals can be one paragraph.
- If drafting in a file or shell and the prompt may be near the ceiling, check
  the `/goal` text with `wc -m` or an equivalent character count before handing
  it back.

The budget belongs to the copyable `/goal` text. Explanatory notes can sit
after it, but keep them short. If the note becomes another plan, the goal is
probably carrying the wrong job.

## Source truth compression

When an authoritative document, plan, consensus output, fixture, skill, or diff
already exists, reference it by path or exact name. Do not summarize it
paragraph by paragraph inside the goal.

The `/goal` owns:

- mission
- source truth pointers
- the false finish line
- the few workflow rules that matter
- likely shortcuts to avoid
- evidence and signoff gates
- completion and persistence rules

The source material owns:

- full doctrine
- detailed examples
- thought exercises
- command lists
- reviewer prompts
- long background
- complete implementation plans

Good compression:

```text
Use `docs/PLAN.md` as controlling source truth for doctrine, examples, test fixtures, and validation expectations. Do not restate it or create a second plan.
```

Bad compression:

```text
Paste the whole plan doc into the goal, then add a second list of the same examples, constraints, reviewer prompts, and tests.
```

If the source path is missing or inaccessible, either ask for it or include only
the minimum context needed to keep the goal executable. Do not invent invisible
source truth.

## Authoring workflow

1. Name the desired world state in one sentence.
2. Identify the likely false finish line: the result that could look done while
   violating the user's intent.
3. Look for a controlling source doc, plan, diff, fixture, skill, or model
   output. Point to it instead of copying it.
4. Add a vivid quality bar only when it changes judgment.
5. Name authoritative sources separately from stale context.
6. Add workflow rules only where a specific skill, model, tool, or sequence
   changes the result.
7. Ban the smallest set of shortcuts that would poison the outcome.
8. Define proof: tests, artifacts, inspections, generated outputs, screenshots,
   review receipts, or final report details.
9. Add signoff when requested or when the work should not self-certify.
10. For execution and repair goals, add persistence rules for uncertainty: read
    deeper source truth, form sharper theories, build disproof tests, instrument
    the real path, use required reviewers to choose the next move, and keep
    repairing until the desired state is real.
11. Compress. If a sentence restates the source doc instead of changing
    execution, remove it.

Do not ask the user to choose a prompt type. Infer the blend. Codex `/goal`
prompts usually combine outcome-first task prompting, evidence policy,
validation, tool-use rules, and completion behavior.

## Signoff as part of done

Signoff should be first-class when:

- the user explicitly asks for review, consensus, signoff, or another model;
- the work changes architecture, cross-repo contracts, skill behavior, or
  durable prompt doctrine;
- the result could pass tests while still violating intent;
- the result is subjective, product-sensitive, learner-facing, or
  domain-sensitive;
- recent history shows the user had to correct this class of failure.

Good signoff names:

- reviewer type: blind review, model consensus, adversarial critic, domain
  critic, fresh consult, or delegated implementation/testing worker;
- reviewer inputs: source truth, final diff, artifacts, logs, screenshots,
  receipts, or test outputs;
- model and effort when known;
- non-leading rule: do not provide the expected verdict;
- done rule: the reviewer agrees the goal is satisfied. If review rejects the
  result, its objection becomes the next repair input, not the ending, unless
  the user explicitly requested a planning-only or review-only artifact.

Bad signoff:

```text
Get another model to review it.
```

Good signoff:

```text
Use `$codex-review-yolo` as a blind review of the final diff and receipts. Do not provide the expected verdict. Done requires reviewer agreement that the goal is satisfied; if review rejects the result, use that objection to keep fixing and rerun review.
```

Good delegated testing:

```text
Use `$agent-delegate` with Claude Fable 5 high for one fresh testing/signoff pass. Give it the source truth path, final diff, artifacts, and anti-poisoning constraints; do not tell it what verdict to reach.
```

## Lightweight shapes

Use prose by default:

```text
/goal [Mission in one sentence.]

[Quality bar or false finish line, if it changes the work.]

Use [source truth paths/names] as controlling source truth. Treat [weak or stale sources] as context only.

[Workflow, tool, or model rules that matter.]

Do not [likely bad shortcuts].

When the path is unclear, keep moving by reading source truth, forming sharper theories, adding tests or instrumentation, and using required review to choose the next repair.

Done means [the intended outcome works], [evidence], [validation], [report], and [signoff gate].
```

Use this shape when a rich source doc already exists:

```text
/goal Implement [outcome] using `[source doc]` as controlling source truth.

The doc owns [doctrine/examples/fixtures/validation details]. This goal only names the mission, guardrails, and done gate; do not create a second plan.

Use [owner skills/files/tools] for implementation. Do not [likely overfit/bypass/manual proof path].

When evidence is thin or contradictory, deepen the proof instead of narrowing the goal: inspect the owner path, add focused tests, and use review/consensus to choose the next repair.

Done means [the outcome in the source doc works], [validation], [signoff], and [final report evidence].
```

Use a compact one-paragraph goal when the task is small:

```text
/goal [Outcome] in [repo/workspace]. Source truth: [sources]. Do not [likely wrong shortcut]. Keep investigating and repairing through the owning path until [outcome] works. Done means [proof plus review/signoff if required].
```

Do not force all labels into every goal. If a field does not change behavior,
omit it.

## Outcome examples

These examples are adapted from real goal-writing patterns. Use them to teach
the principle, not to copy the exact wording. The code blocks are intentionally
compact; the rationale after each block is not part of the goal.

### Rich source doc implementation

```text
/goal Implement the coach-text intuition work described in `docs/COACH_TEXT_INTUITION_MODEL_CONSENSUS_2026-05-03.md` into the owning `lessons_studio` skills/prompts.

The doc is controlling source truth for doctrine, bad Track 4 examples, thought exercises, and validation expectations. Do not restate it or create a second plan. Desired state: future coach-text passes naturally distinguish poker truth from learner-earned knowledge, preserve the support gradient, avoid invented poker phrases, and make quality review catch shallow or unsupported coaching.

Use `$skill-authoring` and `$prompt-authoring` for reusable skill/prompt edits. Edit source prompts/skills, not generated `build/SKILL.md`. Use Track 4 bad copy and the doc's thought exercises only as evaluation fixtures.

Do not hardcode Track 4, hand-write final learner copy as proof, bypass PokerKB/owner skills, add keyword detectors, lead reviewers toward the desired verdict, or treat reviewer rejection as a finish line.

Done means generated outputs are refreshed through repo commands, validation runs, bad examples and thought exercises are tested without answer leakage, GPT-5.5 X-High and `$agent-delegate` Opus 4.7 xhigh independently sign off that the goal is satisfied, and the final report lists changed files, commands, artifacts, signoff results, and risks. If review rejects the result, use the objection to keep fixing and rerun validation.
```

Why this works: one path carries the full doctrine. The goal carries mission,
anti-poisoning, signoff, and proof without becoming a competing source of
truth.

### Vague repair

```text
/goal Fix the current `lessons_studio` issue through the owning workflow, not by patching around it.

The target state is learner-facing behavior that is actually correct, preserves the repo's skill architecture, and survives quality review without excuses.

Use current owner skill readbacks, live/current psmobile surfaces when relevant, and repo quality-review requirements as source truth. Treat old reports, stale worklogs, and backfill artifacts as context only.

If the owner skill is wrong, fix that skill under `$skill-authoring` and `$prompt-authoring` instead of bypassing it. Do not use heuristic scripts, smart backfills, raw JSON patching into a plausible shape, softened requirements, fake receipts, or a diagnosis-only ending.

When the owner path is unclear, inspect repo truth until it is clear enough to act. Done means the original failure is shown, the owner-path fix is implemented, validation or review is rerun, and exact receipts prove the behavior is correct.
```

Why this works: it turns "fix it properly" into a visible owner-path quality
bar without listing every possible repair branch.

### Planning-only consensus

```text
/goal Produce an implementation-ready v2 planning package for PokerSkill Post-Game Review. Do not implement code in this run.

Use `docs/PACKS/post_game_analysis_2026-05/README.md`, `docs/PACKS/mock_post_game/`, current repo code, owner paths, and existing research as source truth.

Use `$model-consensus` with `opus 4.7 max` and `gpt 5.5 xhigh` to decide the plan shape. The plan should be depth-first: know the final destination, prove the architecture with the smallest real working slice, then expand.

Do not substitute a manual phase design when models disagree, hide final scope as "later," force a preset phase count, or write a breadth-first Phase 1 that touches everything without proving the risky path.

Done means the repo contains model prompts/outputs, consensus synthesis, epic decomposition, and implementation-ready sub-plan docs. Each sub-plan needs outcome, owner path, proof gate, expansion path, and completion condition. Both models must agree on the plan shape; if they disagree, continue the consensus loop until the disagreement is reduced to a user-owned product choice.
```

Why this works: it names the planning destination and the depth-first quality
bar without copying the whole pack.

Planning-only goals are the exception: if the user asked only for a plan,
the artifact may surface a remaining user-owned product choice. Execution and
repair goals should not use that shape.

### Cross-layer diagnosis

```text
/goal Diagnose and fix whether the bad AI play is caused by a mismatch between Flutter, Go, and RustAI.

The target state is not "the symptom disappeared." The target state is RTS opponents working through the real app stack the way RustAI intends.

Use live RustAI logs, Go backend logs, Flutter/client observations, CLI-driven gameplay, and RustAI's intended RTS config behavior as source truth. Compare the same action or decision across all three layers before changing behavior.

Do not fall back to the blueprint projection pad, neuter RTS, change settings merely to avoid the bug, or claim success because a weakened path hides the symptom.

Done means the root cause is named, the layer mismatch is fixed, exact logs or command receipts prove it, and RTS still uses the intended config path through Flutter -> Go -> RustAI.
```

Why this works: it names the false finish line and forces proof across the real
stack.

### Merge reintegration

```text
/goal Reintegrate `origin/main` into `/Users/aelaguiz/workspace/feat/play_poker_live` while preserving the branch's intended RustAI behavior.

This repo is reached through `/Users/aelaguiz/workspace/feat/play_poker/rustai`. Bring the branch current without hiding behavior regressions behind compatibility leftovers.

Use current branch intent, `origin/main`, RustAI behavior tests, and relevant docs or fixtures as source truth. Resolve conflicts in favor of preserving intended branch behavior unless upstream evidence proves the requirement changed.

Do not silently drop behavior, keep duplicate stale compatibility helpers, weaken tests, leave conflict residue, or keep dead merge scaffolding just because it compiles.

Done means the branch builds, focused behavior tests pass, stale merge leftovers are removed, and the final report lists meaningful conflicts, chosen resolutions, deleted stale surfaces, exact commands, and risks.
```

Why this works: it turns "thoughtfully" into concrete merge judgment while
staying small enough to paste into `/goal`.

## Anti-patterns

- A fixed field list that makes every goal look the same.
- A giant process script that hides the desired world state.
- A pasted source doc that turns the goal into a competing source of truth.
- A goal that reprints examples, thought exercises, command lists, reviewer
  prompts, or implementation-plan detail already owned by a referenced doc.
- A quality bar that only says "good," "proper," "polished," or "high quality."
- A source-truth line that treats stale artifacts as equal to live owner paths.
- A review line that is not part of done.
- A consensus line that does not define convergence.
- A signoff line that makes reviewer rejection or model disagreement sound like
  a valid ending for execution work instead of the next repair input.
- A goal that lets the agent finish with a diagnosis, refusal, narrow report, or
  obstacle summary when the user asked for the system to work.
- A forbidden-shortcuts list so broad that it becomes a brittle rulebook.
- A goal that asks the agent to use a named skill but not what that skill is
  meant to preserve.
- A goal that exceeds the 4,000-character hard cap or uses the cap as the
  normal target.

## Final self-check

- Does the first sentence name the desired world state?
- Is the goal under 4,000 characters, and preferably 2,000-3,000 or less?
- If a rich source doc exists, does the goal reference it instead of duplicating
  it?
- Does the prompt teach the intuition, not just the steps?
- Is the quality bar vivid enough to reject false success?
- Are ground-truth sources and stale/context sources separated?
- Are tool and workflow rules present only where they change behavior?
- Does signoff, when present, define reviewer inputs and the acceptance gate?
- Does done require evidence the agent can actually produce?
- Could an agent honestly finish this goal without the desired system state
  becoming real? If yes, rewrite.
- If the path is unclear, does the goal teach the next evidence, test, review,
  or repair move instead of offering non-completion language?
- Would this still work for a similar workflow the examples did not mention?
