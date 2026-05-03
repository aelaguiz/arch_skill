# Codex Goal Prompts

Use this reference when the artifact is a Codex `/goal` prompt or a persistent
goal objective for a long-running agent session.

The job is not to fill out a form. The job is to turn rough intent into a short
mission brief that helps a future agent know what world should be true when the
goal is done.

## Table of contents

- Mental model
- What good feels like
- Authoring workflow
- Signoff as part of done
- Lightweight shapes
- Outcome examples
- Anti-patterns
- Final self-check

## Mental model

A `/goal` prompt is an operating contract for future work. It sits above a
normal task prompt because the agent may work for many turns, compact context,
resume after interruptions, call tools, or bring in reviewers.

Good goal prompts teach judgment:

- what result matters
- why quality matters at this layer
- which sources outrank guesses
- which workflow rules change the result
- which shortcuts would create a false success
- what evidence proves done
- when outside signoff is required
- when to stop and ask instead of silently deciding

Weak goal prompts only describe activity:

- "fix it properly"
- "bring it up to speed"
- "make this better"
- "use the right skills"
- "get another model to look at it"

Those phrases may express real intent, but they force the agent to invent the
acceptance test.

## What good feels like

Strong `/goal` prompts usually read like this:

1. **Mission first.** The first sentence names the desired world state, not the
   process.
2. **Quality bar in human terms.** If the work is subjective or high-stakes,
   explain what good output feels like and what false success looks like.
3. **Ground truth before workflow.** Name the files, docs, logs, owner skills,
   live surfaces, tests, or model outputs that outrank guesses.
4. **Workflow rules only when they matter.** Add a tool, skill, model, or
   sequence only if it changes behavior.
5. **Forbidden shortcuts protect intent.** Ban the likely wrong path, not every
   imaginable bad move.
6. **Evidence defines done.** Say what must be inspected, tested, compared,
   rendered, reviewed, or saved.
7. **Signoff is a gate when used.** External review, consensus, or an
   adversarial critic belongs inside "done," not after it.
8. **Stop rules prevent silent scope decisions.** Tell the agent when to ask
   instead of guessing.

The prompt should still be readable. Labels are allowed when they help scanning,
but the goal should not feel like a schema the agent is mindlessly completing.

## Authoring workflow

1. Read the user's rough ask and name the intended outcome in one sentence.
2. Identify the likely false finish line: the local result that could look done
   while violating the user's intent.
3. Add system context only when it changes judgment or quality.
4. Add a vivid quality bar when "good" is subjective, domain-sensitive, or easy
   to flatten into generic polish.
5. Name ground truth. Distinguish authoritative sources from stale context.
6. Add workflow rules only where a specific skill, model, or tool changes the
   result.
7. Name the smallest set of forbidden shortcuts that protects the hard path.
8. Define the evidence and final report expected before the goal can be marked
   complete.
9. Add signoff when requested or when the work is risky enough that the agent
   should not self-certify.
10. Add a stop rule for true blockers, scope cuts, missing source truth, or
    unresolved model disagreement.

Do not ask the user to choose a prompt type. Infer the blend. Codex `/goal`
prompts usually combine outcome-first task prompting, tool-use rules, evidence
policy, validation, and runtime stop behavior.

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
  critic, or fresh consult;
- reviewer inputs: files, diff, artifacts, screenshots, logs, plan, or receipts;
- model and effort when known;
- non-leading rule: do not provide the expected verdict;
- done rule: the reviewer agrees, or the final report names the smallest
  unresolved objection.

Bad signoff:

```text
Get another model to review it.
```

Good signoff:

```text
Use `$codex-review-yolo` as a blind, non-leading review of the final diff and receipts. Do not provide the expected verdict. You are not done until it agrees the goal is satisfied, or you report the exact remaining objection and keep fixing.
```

Good consensus:

```text
Use `$model-consensus` with `gpt 5.5 xhigh` and `opus 4.7 max`. Both models must inspect the same source material. Done requires agreement on the same plan, or a final note naming the smallest unresolved disagreement.
```

## Lightweight shapes

Use prose by default:

```text
/goal [Mission in one sentence.]

[Why this matters or what good feels like, when that changes the work.]

Use [ground truth sources] as source truth. Treat [weak or stale sources] as context only.

[Workflow, tool, or model rules that matter.]

Do not [likely bad shortcuts].

Done means [evidence, validation, report, and signoff gate]. Stop and ask only if [true blocker or scope decision].
```

Use a compact one-paragraph goal when the task is small:

```text
/goal [Outcome] in [repo/workspace]. Source truth: [sources]. Use [workflow/tools only if required]. Do not [likely wrong shortcut]. Done means [proof plus review/signoff if required]. Stop only for [true blocker].
```

Do not force all labels into every goal. If a field does not change behavior,
omit it.

## Outcome examples

These examples are adapted from real goal-writing patterns. Use them to teach
the principle, not to copy the exact wording.

### Vague repair

```text
/goal Fix the current `lessons_studio` issue in the owning workflow, not by patching around it.

The desired end state is simple: the learner-facing behavior is actually correct, the repo's skill architecture is still intact, and the fix would survive a quality review without needing excuses.

Use current owner skill readbacks, live/current psmobile surfaces when relevant, and the repo's quality-review requirements as source truth. Old reports, stale worklogs, and backfill artifacts are context only.

Do the repair through the proper studio skill or primitive. If the owner skill is what is wrong, fix that skill under `$skill-authoring` and `$prompt-authoring` instead of bypassing it.

Do not use heuristic scripts, smart backfills, raw JSON patching into a plausible shape, softened requirements, or fake receipts.

Before calling the goal done, show the original failure, the owner-path fix, the validation or review you reran, and the exact receipts. Stop and ask only if the issue requires a real scope decision or the owner path cannot be determined from the repo.
```

Why this works: it turns "fix it properly" into a visible quality bar and an
owner-path repair rule.

### Guided walkthrough compliance

```text
/goal Bring Track 4 Section 2 guided walkthroughs in `/Users/aelaguiz/workspace/lessons_studio` into real compliance with `$studio-curriculum-quality-review`.

The goal is not just green data. The learner experience should be accurate, fair, coherent, mobile-readable, non-leaky, proof-backed where required, and aligned with the section's teaching intent.

Use the owning studio skills, current lesson artifacts, current psmobile surfaces, and `$studio-curriculum-quality-review` as source truth. Treat stale reports and old backfill artifacts as history only.

Make repairs through the proper authoring path. Meaningful learner-facing copy must go through `$agent-delegate` with `opus 4.7 xhigh`. If an upstream skill blocks correct output, fix the upstream skill instead of patching downstream artifacts.

Do not hack around the requirements, soften standards, skip steps, invent receipts, use heuristic repair scripts, or mutate downstream JSON when the upstream owner path is wrong.

You are not done until the section passes the quality bar and `$codex-review-yolo` gives a blind, non-leading review with no unresolved blocker. Final report should name the changed artifacts, owner skills used, review result, and proof receipts.
```

Why this works: it keeps learner quality above process, while still naming the
workflow rules that prevent known bad repairs.

### Responsibility split

```text
/goal Produce a clean solver-proof responsibility architecture where `lessons_studio` owns curriculum judgment and proof requirements, while `psmobile` stays structural.

This matters because proof errors may look like data plumbing, but to a poker learner they are trust failures. The architecture should make it hard to accidentally launder bad proof into valid-looking lesson data.

Use current `lessons_studio` skills, current `psmobile` primitives, existing solver-proof docs, and live artifacts as source material. The final answer should explain the current failure, the corrected boundary, and what must be redone through owning skills.

Use `$model-consensus` with `gpt 5.5 xhigh` and `opus 4.7 max`. Both models should inspect the same source material and converge on the fix plan.

Reject any plan that puts curriculum judgment in `psmobile`, infers solver-proof meaning from Python or structural data, preserves invalid artifacts as "legacy backfill," or massages bad data into a valid-looking shape.

You are not done until both models agree on the architecture, or the final doc names the smallest unresolved disagreement for the user. The final doc should be clear enough that future agents know which layer owns each decision without rediscovering it.
```

Why this works: the system context makes the boundary important, not cosmetic.

### Cross-layer diagnosis

```text
/goal Diagnose and fix whether the bad AI play is caused by a mismatch between Flutter, Go, and RustAI.

The target state is not "the symptom disappeared." The target state is RTS opponents working through the real app stack the way RustAI intends.

RustAI alone has not shown this behavior in extensive testing. The suspicious behavior appears when gameplay flows through Flutter and Go, so the investigation must compare the same action or decision across all three layers.

Use live RustAI logs, Go backend logs, Flutter/client observations, CLI-driven gameplay, and RustAI's intended RTS config behavior as source truth. Drive the game through the CLI and capture comparable evidence before changing behavior.

Do not fall back to the blueprint projection pad, neuter RTS, change settings merely to avoid the bug, or claim success because a weakened path hides the symptom.

Done means the root cause is named, the bad translation or layer mismatch is fixed, exact logs or command receipts prove it, and RTS still uses the intended config path through Flutter -> Go -> RustAI.
```

Why this works: it names the false finish line and forces proof across the real
stack.

### Product design iteration

```text
/goal Iterate the Figma design until it feels like a native PokerSkill app feature, not a generic redesign.

The quality bar is product-real: it should use the existing app's visual language, real-feeling poker data, tight layout, and clear post-game decision value. It should not look like a detached SaaS mockup or a pretty concept board.

Use existing PokerSkill app components, current styling, realistic data from real poker rounds, `$figma-best-practices`, and the research docs `docs/RESEARCH/CHESS_GPT.md`, `docs/RESEARCH/CHESS_COM_POST_GAME_ANALYSIS.md`, and `docs/RESEARCH/CLAUDE_CHESS.md`.

Run at least three serious iteration rounds with consensus from `gpt 5.5 xhigh` and `opus 4.7 xhigh`. Then run an adversarial poker critic using `gpt 5.5 xhigh` whose job is to find missed product, poker, or UX issues.

Give every spawned reviewer the same constraints: it must look like this app, use realistic poker data, avoid wasted space and misalignment, and incorporate the named research learnings.

You are not done until the consensus reviewers and adversarial critic can no longer name substantive improvements. Preserve each round's critique, changes made, remaining objections, and final visual receipts.
```

Why this works: it defines "good design" as product fit, not generic polish.

### Planning-only consensus

```text
/goal Produce a fully specified v2 `$arch-epic` and `$arch-step` planning package for PokerSkill Post-Game Review. Do not implement code in this run.

The destination is full end-to-end implementation of `docs/PACKS/post_game_analysis_2026-05/README.md`. This turn's job is to make the implementation plan ready, not to start building.

Use `docs/PACKS/post_game_analysis_2026-05/README.md`, `docs/PACKS/mock_post_game/`, current repo code, current owner paths, and existing research as source truth.

Use `$model-consensus` with `opus 4.7 max` and `gpt 5.5 xhigh` to decide the plan shape. The parent agent should not substitute its own manual phase design when the models disagree.

The plan should be depth-first: know the final destination, prove the architecture with the smallest real working slice, then expand. Do not hide final scope as "later," force a preset phase count, or write a breadth-first Phase 1 that touches everything without proving the risky path.

Done means the repo contains the model prompts/outputs, consensus synthesis, epic decomposition, and implementation-ready sub-plan docs. Each sub-plan needs a clear outcome, owner path, proof gate, expansion path, and stop condition. Both models must agree on the final v2 plan shape, or the final doc must name the smallest unresolved decision.
```

Why this works: it makes both "planning only" and "ready to implement"
observable, while preserving depth-first planning as a quality bar.

### Merge reintegration

```text
/goal Reintegrate `origin/main` into `/Users/aelaguiz/workspace/feat/play_poker_live` while preserving the branch's intended RustAI behavior.

This repo is reached through `/Users/aelaguiz/workspace/feat/play_poker/rustai`. The merge should bring the branch current without hiding behavior regressions behind compatibility leftovers.

Use current branch intent, `origin/main`, RustAI behavior tests, and relevant RustAI docs or fixtures as source truth. Resolve conflicts in favor of preserving intended branch behavior unless upstream evidence proves the requirement changed.

Do not silently drop behavior, keep duplicate stale compatibility helpers, weaken tests, leave conflict residue, or keep dead merge scaffolding just because it compiles.

Done means the branch builds, focused behavior tests pass, stale merge leftovers are removed, and the final report lists meaningful conflicts, chosen resolutions, deleted stale surfaces, exact commands run, and remaining risks.
```

Why this works: it turns "thoughtfully" into concrete merge judgment.

## Anti-patterns

- A fixed field list that makes every goal look the same.
- A giant process script that hides the desired world state.
- A quality bar that only says "good," "proper," "polished," or "high quality."
- A source-truth line that treats stale artifacts as equal to live owner paths.
- A review line that is not part of done.
- A consensus line that does not define convergence.
- A forbidden-shortcuts list so broad that it becomes a brittle rulebook.
- A goal that asks the agent to use a named skill but not what that skill is
  meant to preserve.

## Final self-check

- Does the first sentence name the desired world state?
- Does the prompt teach the intuition, not just the steps?
- Is the quality bar vivid enough to reject false success?
- Are ground-truth sources and stale/context sources separated?
- Are tool and workflow rules present only where they change behavior?
- Does signoff, when present, define reviewer inputs and the acceptance gate?
- Does done require evidence the agent can actually produce?
- Is there a stop rule for true blockers or scope decisions?
- Would this still work for a similar workflow the examples did not mention?
