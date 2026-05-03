# Codex Goal Prompt Authoring Analysis

Last reviewed: 2026-05-03.

This document analyzes how `/goal` has been used in recent Codex sessions and
recommends a prompt-authoring variant for writing stronger, outcome-driven goal
prompts.

The short version: your best goals are not task descriptions and not duplicated
plan docs. They are compact operating contracts. They name the world state you
want, the source of truth, the work boundaries, the forbidden shortcuts, the
proof required, and the independent review gate. The painful goals usually
leave one of those pieces implicit, or copy so much source material into the
goal that the goal becomes a competing source of truth.

2026-05-03 form-factor update: the live runtime guidance now lives in
`skills/prompt-authoring/references/codex-goal-prompts.md`. Treat its compact
examples as authoritative. Codex `/goal` prompts have a 4,000-character hard
cap, usually work best around 2,000-3,000 characters, and should be shorter
when they can point at a rich source doc by path.

## Scope And Method

Reviewed local Codex history through `$agent-history` for:

- `/Users/aelaguiz/workspace/lessons_studio`
- `/Users/aelaguiz/workspace/feat/play_poker`
- `/Users/aelaguiz/workspace/feat/play_poker/rustai`, which resolves to
  `/Users/aelaguiz/workspace/feat/play_poker_live`

Time window: `2026-01-01` through `2026-05-03`.

Main evidence sources:

- `~/.codex/state_5.sqlite` thread goal state, especially
  `codex_state.thread_goals`.
- `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` for exact `update_goal`
  completions and surrounding transcript records.
- `$agent-history` helper runs:
  - all-project goal scan:
    `/var/folders/cr/8sccc69d0rg1b8dsp42v7q900000gn/T/agent-history/20260503T145948Z-goals-1079a7b6`
  - `lessons_studio` goal scan:
    `/var/folders/cr/8sccc69d0rg1b8dsp42v7q900000gn/T/agent-history/20260503T150057Z-goals-4cd42f0c`
  - `play_poker` goal scan:
    `/var/folders/cr/8sccc69d0rg1b8dsp42v7q900000gn/T/agent-history/20260503T150049Z-goals-0e31df63`
  - `play_poker/rustai` symlink goal scan:
    `/var/folders/cr/8sccc69d0rg1b8dsp42v7q900000gn/T/agent-history/20260503T150125Z-goals-ca8ac29a`

Important evidence caveat: Codex slash-command text is not an append-only
command history stream. The most durable record is the resulting goal state and
exact `update_goal` calls. Rows marked `inferred` came from the persisted
current goal state. Rows marked `exact` came from rollout JSONL events.

## Core Finding

The recurring pattern is simple.

When the goal is just "fix this" or "bring this up to speed," the agent has to
invent the definition of success. It may still complete the work, but it has too
much room to choose the wrong source of truth, stop at a superficial pass, or
accept a workaround.

When the goal says "this is the outcome, these are the sources, these shortcuts
are forbidden, this is the evidence, and this outside reviewer must sign off,"
the agent has a much better target. It can still make mistakes, but the mistakes
are easier to catch because the goal defines what done means.

So the prompt-authoring variant should not produce pretty task prompts. It
should produce `/goal` prompts that are small mission contracts.

## Places You Had To Correct It

### 1. Architecture Responsibility Drift

Evidence:

- `lessons_studio`
- Thread `019de334-e124-77b3-b8d9-486646ac6c95`
- Timestamp `2026-05-01T07:11:48-05:00`
- `$agent-history` row `r0024`
- Source: `~/.codex/state_5.sqlite`, inferred goal state

The correction was about the agent choosing or accepting the wrong ownership
model. The goal demanded `$model-consensus` with `gpt 5.5 xhigh` and
`opus 4.7 max`, a cleaner architecture, no brittle Python inference, no broken
functional encapsulation, and no "legacy backfill" normalization of work that
did not meet requirements.

What this teaches:

- The goal needs an explicit source-of-truth boundary.
- The goal needs to say which repo or layer owns the smarts.
- The goal needs to ban compatibility stories that preserve bad data.
- The goal needs to explain the user-facing stakes, not just the technical
  shape.
- Consensus is not decoration here. It is the gate that prevents one agent from
  self-certifying a risky architectural call.

The better generic shape is:

```text
/goal Outcome: redesign the responsibility split so [repo/layer A] owns [smart behavior] and [repo/layer B] stays [structural role].

Source of truth: [current skills], [current surfaces], and [named docs/files].

Forbidden: inferred behavior from the wrong layer, compatibility backfills that preserve nonconforming artifacts, or any plan that breaks the encapsulation boundary.

External signoff: run `$model-consensus` with [models/efforts]. You are not done until both models agree on the fix plan and the final doc records any remaining disagreement.
```

### 2. Vague "Fix It Properly" Goals

Evidence:

- `lessons_studio`
- Thread `019de975-724c-7cd1-863d-99860c992221`
- Timestamp `2026-05-02T16:06:18-05:00`
- `$agent-history` row `r0011`
- Source: `~/.codex/state_5.sqlite`, inferred goal state

The whole goal was effectively: fix the issue properly using the right skills,
"idk just fix it." It completed, but this is exactly the shape that forces the
agent to guess the real standard.

What this teaches:

- "Properly" is not a success criterion.
- "Using skills or whatever" is not a routing rule.
- The goal needs to say what evidence proves the issue is fixed.
- The goal needs to say whether upstream skill fixes are allowed or required.
- The goal needs a stop rule for when the owning path is unclear.

The better generic shape is:

```text
/goal Outcome: fix [specific issue] so [observable behavior] is correct through the owning workflow.

Use: the repo's owning skills and primitives for this surface. If the owner skill is wrong, repair the skill under `$skill-authoring` instead of bypassing it.

Evidence: reproduce or inspect the failure, make the smallest owner-path fix, rerun the relevant check, and report the exact receipt.

Done means: the original failure no longer occurs, the fix did not weaken the requirement, and [review/check] agrees.
```

### 3. Layer-Mistranslation And Workaround Risk

Evidence:

- `play_poker`
- Thread `019dd606-8523-77f1-8efe-e84d4e4c8083`
- Timestamp `2026-04-28T17:56:40-05:00`
- `$agent-history` row `r0015`
- Source: `~/.codex/state_5.sqlite`, inferred goal state

The correction was not "make the behavior look sane." It was: rule out a
mistranslation between Flutter, Go, and RustAI by driving the game through the
CLI, cross-reference all three layers, and fix the implementation difference.
The goal also banned the easy wrong answer: using the blueprint projection pad
or neutering RTS instead of making RTS work as intended.

What this teaches:

- For cross-layer bugs, the goal must require diagnostic proof across each
  layer.
- "Fix it" must include "rule out the implementation difference."
- The goal should name forbidden workarounds because otherwise the agent may
  choose a behavior-preserving shortcut that destroys the product intent.
- The goal should preserve the intended engine behavior, not just the visible
  symptom.

The better generic shape is:

```text
/goal Outcome: prove and fix whether [bad behavior] is caused by a mismatch across [client], [middle layer], and [engine].

Method: drive the real flow through [tool/CLI], capture comparable evidence at all three layers, and trace the same decision/action across the boundary.

Forbidden: disabling [core feature], falling back to [old hack], changing settings to avoid the bug, or declaring success because the symptom disappears after neutering the intended path.

Done means: [core feature] works through the real stack as intended, the root cause is named, the fix is implemented, and the report includes layer-by-layer evidence.
```

### 4. Design Drift From Product Reality

Evidence:

- `play_poker`
- Thread `019de136-3699-7c60-a706-63796bba2279`
- Timestamp `2026-05-01T06:26:34-05:00`
- `$agent-history` row `r0009`
- Source: `~/.codex/state_5.sqlite`, inferred goal state

The correction was that iterations were getting further from the app's existing
styling and components. The goal forced model consensus, an adversarial poker
critic, at least three full rounds, `$figma-best-practices`, realistic sample
data from real rounds, and incorporation of named research docs.

What this teaches:

- Design goals need product-anchor constraints, not just "make it high
  fidelity."
- Iteration count is useful only when paired with a quality gate.
- An adversarial critic is valuable when the likely failure is blind spots, not
  just polish.
- Spawned agents must receive the same hard constraints or they will optimize
  for generic design quality.

The better generic shape is:

```text
/goal Outcome: iterate [design/artifact] until it looks and behaves like a native part of [product], not a generic redesign.

Ground truth: existing components, current app styling, named screenshots, and [research docs].

Review loop: run [model consensus] for design quality, then an adversarial domain critic for missed product/domain issues. Give every reviewer the same source constraints.

Done means: the artifact uses realistic domain data, aligns with existing product components, has no obvious layout waste or misalignment, and reviewers can no longer name substantive improvements.
```

### 5. Merge Goals That Are Too Trusting

Evidence:

- `play_poker/rustai` symlink target `/Users/aelaguiz/workspace/feat/play_poker_live`
- Thread `019deb20-e51d-7580-98b9-feac3789abec`
- Timestamp `2026-05-02T20:13:39-05:00`
- `$agent-history` row `r0001`
- Source: `~/.codex/state_5.sqlite`, inferred goal state

The goal was: reintegrate `rustai origin/main` into the branch and bring it up
to speed thoughtfully. It completed, and surrounding transcript records show
useful north-star behavior around removing stale compatibility code and rerunning
focused tests. But the goal itself was weak: it did not define what "up to
speed" meant, what conflict choices should optimize for, which tests mattered,
or whether review was required.

What this teaches:

- "Thoughtfully" is useful tone, not an acceptance test.
- Merge goals should name the integration target, behavior preservation, stale
  code policy, conflict-resolution principle, and verification commands.
- If the merge touches product-sensitive poker engine behavior, review or
  consensus should be explicit.

The better generic shape is:

```text
/goal Outcome: integrate `origin/main` into this branch while preserving [branch feature/intended behavior] and removing stale compatibility code that no longer belongs.

Conflict rule: prefer the implementation that preserves [current intended behavior] unless source evidence proves `origin/main` changed the requirement.

Forbidden: keeping duplicate compatibility helpers, silently dropping branch behavior, or resolving conflicts by making tests weaker.

Evidence: list conflicts resolved, behavior preserved, stale surfaces deleted, and exact commands run.

Done means: the branch builds, the focused behavior tests pass, and [review/signoff if risk is high] agrees the integration did not hide a regression.
```

## Places That Seemed To Work

This section uses "seemed" deliberately. The history has goal text and some
exact completion records, but it does not always contain an explicit "I am
happy" message. I am treating a goal as a positive pattern when it either
reached `update_goal {"status":"complete"}` or its prompt shape clearly matched
later successful patterns. I am not treating these as proof that every artifact
was perfect.

### Guided Walkthrough Compliance Goals

Evidence:

- `lessons_studio`
- Thread `019deb2a-7308-7520-b693-b77a12aea11e`
- Timestamp `2026-05-02T20:21:25-05:00`
- `$agent-history` rows `r0003` and exact completion `r0004`

This was a strong goal shape. It narrowed scope to Track 4 Section 2 guided
walkthroughs, used studio skills, banned hacks, allowed upstream skill fixes
when aligned with `$skill-authoring` and `$prompt-authoring`, required
`opus 4.7 xhigh` copywriting through `$agent-delegate`, and required blind
`$codex-review-yolo` signoff.

Why it works:

- Scope is specific.
- The owner workflow is explicit.
- Forbidden shortcuts are named.
- Upstream unblocking is allowed.
- Independent review is a hard done gate.
- The reviewer is blind and non-leading.

### Track 4 Learner-Ready Goal

Evidence:

- `lessons_studio`
- Thread `019de3d1-7705-7462-84d4-9554edbf2e96`
- Timestamp `2026-05-01T15:56:30-05:00`
- `$agent-history` row `r0023`; nearby exact completion record `r0022`

This goal had a clear "Goal:" line: make `TRACK_04` learner-ready end to end.
The persisted goal text was paused at review time, so I am using it as a strong
prompt-shape example rather than a clean completion example. It named the
workspace, source-of-truth surfaces, stale artifacts to treat as history only,
learner-experience success criteria, owner lanes, and a ban on heuristic scripts
or smart backfills.

Why it works:

- It says what user-facing good means: accurate, fair, coherent,
  mobile-readable, non-leaky, proof-backed where graded, and aligned to lesson
  intent.
- It treats green data as necessary but not sufficient.
- It separates owner skills from raw JSON patching.
- It tells outside copy help not to bypass owner skills.

### Post-Game Review Planning Goal

Evidence:

- `play_poker`
- Thread `019dee44-7e5d-7532-8acc-3c3998fba8c7`
- Timestamp `2026-05-03T10:00:21-05:00`
- `$agent-history` row `r0001`, active at review time

This is a good planning-only pattern. It asks `opus 4.7 max` and
`gpt 5.5 xhigh` to drive `$arch-epic` and `$arch-step` planning through
`$model-consensus`, anchors the plan in named research docs, and states that
the outcome is a fully specified v2 plan with subphases ready to implement.

Why it works:

- It says "planning no implementation," which prevents premature edits.
- It uses consensus as the source of planning authority.
- It anchors the goal in named packs and mocks.
- It names the implementation destination even though the current work is only
  planning.

The main improvement would be to make the external signoff completion condition
more explicit: the plan is done only when both models agree on the same final
phase shape or the doc records the smallest unresolved decision.

### Figma Iteration Goal

Evidence:

- `play_poker`
- Thread `019de136-3699-7c60-a706-63796bba2279`
- Timestamp `2026-05-01T06:26:34-05:00`
- `$agent-history` rows `r0009` and exact completion `r0010`

This goal is useful because it does not merely say "make the Figma better." It
requires model consensus, an adversarial poker critic, multiple rounds,
`$figma-best-practices`, realistic sample data, named research docs, and strict
alignment with existing styling and components.

Why it works:

- It encodes the actual failure mode: generic design drift.
- It gives reviewers the domain constraints.
- It requires iteration until there are no substantive ideas left.
- It requires realistic poker data, which prevents empty decorative layouts.

## The Goal Prompt Authoring Variant

Recommended name if this becomes a skill: `goal-prompt-authoring`.

Recommended mechanism: start as a lean prompt-only skill or a dedicated
`prompt-authoring` reference. A script, runner, controller, or formal parameter
schema is not justified yet. The recurring failure is not deterministic parsing;
it is missing prompt structure and missing done gates.

The job:

> Turn a rough user intent into a copyable `/goal` prompt that defines the
> desired outcome, source of truth, constraints, proof, and external signoff
> needed for Codex's goal feature.

The important adjustment is that this should use `$prompt-authoring` principles,
not a rigid form. A good `/goal` should read like a short mission brief:

- mission and desired world state first;
- quality bar in human terms when the work is subjective or high-stakes;
- ground truth before process;
- workflow rules only where they change behavior;
- forbidden paths only where they prevent likely failure;
- evidence and stop rules that define done;
- external signoff as part of done when the user asks for it or risk warrants
  it.

Nearest lookalike:

- `$prompt-authoring` writes prompts broadly.
- `goal-prompt-authoring` should specialize in Codex `/goal` objectives that
  guide long-running implementation, planning, investigation, or review loops.

When it should trigger:

- The user asks for a Codex `/goal` prompt.
- The user wants to set or rewrite a `/goal`.
- The user gives rough implementation intent and asks for a stronger goal.
- The user mentions goal outcome, done criteria, signoff, review, consensus, or
  "make this a good goal prompt."

When it should not trigger:

- The user wants the agent to execute the work now, not draft the goal.
- The user wants a general reusable prompt unrelated to Codex goals; use
  `$prompt-authoring`.
- The user wants to design or modify the skill package itself; use
  `$skill-authoring`.

## Revised Authoring Plan

The variant should normally return one copyable `/goal` prompt first and a short
note only when an assumption matters. It should not bury the usable prompt under
analysis unless the user asked for analysis.

The form-factor rule is load-bearing:

- 4,000 characters is the hard cap, not the target.
- Complex goals should usually land around 2,000-3,000 characters.
- Goals that point at a rich source doc should often be 800-1,800 characters.
- Source docs, plans, consensus outputs, thought exercises, and detailed test
  fixtures should be referenced by path/name, not restated inside the `/goal`.
- If the goal duplicates the plan, it creates a competing source of truth.

The authoring plan should be:

1. Convert the rough ask into the desired end state.
2. Add system context when quality depends on why the work matters.
3. Add a vivid quality bar when the likely failure is generic, superficial, or
   technically green but user-wrong.
4. Name the ground truth: files, docs, owner skills, live surfaces, logs, tests,
   or model outputs that outrank guesses.
5. Compress source truth: point at controlling docs instead of copying their
   doctrine, examples, thought exercises, reviewer prompts, or command lists.
6. Add workflow or tool rules only when they change the result.
7. Name the forbidden shortcuts that match the actual risk.
8. Define evidence: what the agent must inspect, test, render, compare, or save.
9. Make signoff first-class when requested or warranted.
10. Add a stop rule so the agent does not loop forever or silently make a scope
    decision.
11. Delete any sentence that restates the source doc without changing execution.

The prompt should usually be prose with compact paragraphs. Use labels only when
they make the goal easier to scan. Do not force every goal into the same field
schema.

Good lightweight shape:

```text
/goal [Mission in one sentence.]

[Why this matters or what quality feels like, when that changes the work.]

Use [ground truth sources] as source truth. Treat [weak/stale sources] as context only.

[Workflow/tool/model rules that matter.]

Do not [likely bad shortcuts].

Done means [evidence, validation, report, and signoff gate]. Stop and ask only if [true blocker or scope decision].
```

Good source-doc-heavy shape:

```text
/goal Implement [outcome] using `[source doc]` as controlling source truth.

The doc owns [doctrine/examples/fixtures/validation details]. This goal only names the mission, guardrails, and done gate; do not create a second plan.

Use [owner skills/files/tools]. Do not [likely overfit/bypass/manual proof path].

Done means [validation], [signoff], and [final report evidence]. Stop only for [missing source, unavailable exact model/tool, or real scope conflict].
```

Very compact shape when the goal should stay short:

```text
/goal [Outcome] in [repo/workspace]. Source truth: [sources]. Use [workflow/tools only if required]. Do not [likely wrong shortcut]. Done means [proof plus review/signoff if required]. Stop only for [true blocker].
```

## Signoff Must Be First-Class

A weak goal treats review as a final nice-to-have. Your successful goals treat
review as part of the work.

The goal-authoring variant should always decide whether the job needs external
signoff. It should include signoff automatically when:

- the user asks for it;
- the task changes architecture, cross-repo contracts, or model/agent skill
  behavior;
- the task is product-sensitive, especially poker strategy, curriculum quality,
  learner-facing content, or real user experience;
- the user has recently had to correct the same class of failure;
- the agent might be tempted to self-certify a subjective result;
- the implementation could pass local tests while still violating intent.

The signoff block should specify:

- reviewer type: `blind audit`, `model consensus`, `adversarial critic`,
  `domain critic`, or `fresh consult`;
- models and efforts when known, such as `gpt 5.5 xhigh` and
  `opus 4.7 max`;
- whether reviewers should inspect artifacts, repo code, screenshots, logs, or
  plans;
- non-leading instruction: do not tell the reviewer the expected verdict;
- convergence rule: done only when reviewers agree, or when the final doc names
  the smallest unresolved disagreement for the user.

Bad signoff:

```text
Get another model to review it.
```

Good signoff:

```text
External signoff: run `$codex-review-yolo` as a blind, non-leading review of the final diff and receipts. Do not provide the expected verdict. You are not done until it agrees the implementation satisfies the goal, or you report the exact remaining objection and keep fixing.
```

Good consensus:

```text
External signoff: use `$model-consensus` with `gpt-5.5` at `xhigh` and `claude-opus-4-7` at `max`. Both models must read the same source docs and candidate plan. Done requires agreement on the same final plan, or a final note that names the smallest unresolved decision for the user.
```

## Outcome Examples

These examples are based on actual goals from the reviewed history, but rewritten
using the revised prompt-authoring plan above. They are intentionally less
schema-like than the earlier examples. The goal is a readable mission contract,
not a form.

These historical examples are not the runtime source for current `/goal`
authoring. For current examples, especially source-doc-heavy goals that must
avoid duplicating a plan, use
`skills/prompt-authoring/references/codex-goal-prompts.md`.

### Vague Repair Goal

```text
/goal Fix the current `lessons_studio` issue in the owning workflow, not by patching around it.

The desired end state is simple: the learner-facing behavior is actually correct, the repo's skill architecture is still intact, and the fix would survive a quality review without needing excuses.

Use the current owner skill readbacks, live/current psmobile surfaces when relevant, and the repo's quality-review requirements as source of truth. Old reports, stale worklogs, and backfill artifacts are context only.

Do the repair through the proper studio skill or primitive. If the owner skill is what is wrong, fix that skill under `$skill-authoring` and `$prompt-authoring` instead of bypassing it.

Do not use heuristic scripts, smart backfills, raw JSON patching into a plausible shape, softened requirements, or fake receipts.

Before calling the goal done, show the original failure, the owner-path fix, the validation or review you reran, and the exact receipts. Stop and ask only if the issue requires a real scope decision or the owner path cannot be determined from the repo.
```

This preserves the useful intent behind "fix it properly" while making
"properly" observable.

### Track 4 Guided Walkthrough Compliance

```text
/goal Bring Track 4 Section 2 guided walkthroughs in `/Users/aelaguiz/workspace/lessons_studio` into real compliance with `$studio-curriculum-quality-review`.

The goal is not just green data. The learner experience should be accurate, fair, coherent, mobile-readable, non-leaky, proof-backed where required, and aligned with the section's teaching intent.

Use the owning studio skills, current lesson artifacts, current psmobile surfaces, and `$studio-curriculum-quality-review` as source of truth. Treat stale reports and old backfill artifacts as history only.

Make repairs through the proper authoring path. Meaningful learner-facing copy must go through `$agent-delegate` with `opus 4.7 xhigh`. If an upstream skill blocks correct output, fix the upstream skill instead of patching downstream artifacts.

Do not hack around the requirements, soften standards, skip steps, invent receipts, use heuristic repair scripts, or mutate downstream JSON when the upstream owner path is wrong.

You are not done until the section passes the quality bar and `$codex-review-yolo` gives a blind, non-leading review with no unresolved blocker. Final report should name the changed artifacts, owner skills used, review result, and proof receipts.
```

This keeps the learner quality bar above the process checklist. The workflow
rules are present because they prevent known bad repairs.

### Solver-Proof Responsibility Split

```text
/goal Produce a clean solver-proof responsibility architecture where `lessons_studio` owns curriculum judgment and proof requirements, while `psmobile` stays structural.

This matters because proof errors may look like data plumbing, but to a poker learner they are trust failures. The architecture should make it hard to accidentally launder bad proof into valid-looking lesson data.

Use current `lessons_studio` skills, current `psmobile` primitives, existing solver-proof docs, and live artifacts as source material. The final answer should explain the current failure, the corrected boundary, and what must be redone through owning skills.

Use `$model-consensus` with `gpt 5.5 xhigh` and `opus 4.7 max`. Both models should inspect the same source material and converge on the fix plan.

Reject any plan that puts curriculum judgment in `psmobile`, infers solver-proof meaning from Python or structural data, preserves invalid artifacts as "legacy backfill," or massages bad data into a valid-looking shape.

You are not done until both models agree on the architecture, or the final doc names the smallest unresolved disagreement for the user. The final doc should be clear enough that future agents know which layer owns each decision without rediscovering it.
```

This uses system context to make the architecture boundary feel load-bearing,
not cosmetic.

### Cross-Layer RustAI Debug Goal

```text
/goal Diagnose and fix whether the bad AI play is caused by a mismatch between Flutter, Go, and RustAI.

The target state is not "the symptom disappeared." The target state is RTS opponents working through the real app stack the way RustAI intends.

RustAI alone has not shown this behavior in extensive testing. The suspicious behavior appears when gameplay flows through Flutter and Go, so the investigation must compare the same action or decision across all three layers.

Use live RustAI logs, Go backend logs, Flutter/client observations, CLI-driven gameplay, and RustAI's intended RTS config behavior as source truth. Drive the game through the CLI and capture comparable evidence before changing behavior.

Do not fall back to the blueprint projection pad, neuter RTS, change settings merely to avoid the bug, or claim success because a weakened path hides the symptom.

Done means the root cause is named, the bad translation or layer mismatch is fixed, exact logs or command receipts prove it, and RTS still uses the intended config path through Flutter -> Go -> RustAI.
```

This names the false finish line: hiding the symptom by weakening RTS.

### Figma Design Drift

```text
/goal Iterate the Figma design until it feels like a native PokerSkill app feature, not a generic redesign.

The quality bar is product-real: it should use the existing app's visual language, real-feeling poker data, tight layout, and clear post-game decision value. It should not look like a detached SaaS mockup or a pretty concept board.

Use existing PokerSkill app components, current styling, realistic data from real poker rounds, `$figma-best-practices`, and the research docs `docs/RESEARCH/CHESS_GPT.md`, `docs/RESEARCH/CHESS_COM_POST_GAME_ANALYSIS.md`, and `docs/RESEARCH/CLAUDE_CHESS.md`.

Run at least three serious iteration rounds with consensus from `gpt 5.5 xhigh` and `opus 4.7 xhigh`. Then run an adversarial poker critic using `gpt 5.5 xhigh` whose job is to find missed product, poker, or UX issues.

Give every spawned reviewer the same constraints: it must look like this app, use realistic poker data, avoid wasted space and misalignment, and incorporate the named research learnings.

You are not done until the consensus reviewers and adversarial critic can no longer name substantive improvements. Preserve each round's critique, changes made, remaining objections, and final visual receipts.
```

This tells the agents what good feels like and prevents generic design polish
from replacing product fit.

### Planning-Only Model Consensus Goal

```text
/goal Produce a fully specified v2 `$arch-epic` and `$arch-step` planning package for PokerSkill Post-Game Review. Do not implement code in this run.

The destination is full end-to-end implementation of `docs/PACKS/post_game_analysis_2026-05/README.md`. This turn's job is to make the implementation plan ready, not to start building.

Use `docs/PACKS/post_game_analysis_2026-05/README.md`, `docs/PACKS/mock_post_game/`, current repo code, current owner paths, and existing research as source truth.

Use `$model-consensus` with `opus 4.7 max` and `gpt 5.5 xhigh` to decide the plan shape. The parent agent should not substitute its own manual phase design when the models disagree.

The plan should be depth-first: know the final destination, prove the architecture with the smallest real working slice, then expand. Do not hide final scope as "later," force a preset phase count, or write a breadth-first Phase 1 that touches everything without proving the risky path.

Done means the repo contains the model prompts/outputs, consensus synthesis, epic decomposition, and implementation-ready sub-plan docs. Each sub-plan needs a clear outcome, owner path, proof gate, expansion path, and stop condition. Both models must agree on the final v2 plan shape, or the final doc must name the smallest unresolved decision.
```

This makes "planning only" and "implementation-ready" both explicit. It also
adds the depth-first principle as a quality bar, not a decorative preference.

### Merge/Reintegration Goal

```text
/goal Reintegrate `origin/main` into `/Users/aelaguiz/workspace/feat/play_poker_live` while preserving the branch's intended RustAI behavior.

This repo is reached through `/Users/aelaguiz/workspace/feat/play_poker/rustai`. The merge should bring the branch current without hiding behavior regressions behind compatibility leftovers.

Use current branch intent, `origin/main`, RustAI behavior tests, and relevant RustAI docs or fixtures as source truth. Resolve conflicts in favor of preserving intended branch behavior unless upstream evidence proves the requirement changed.

Do not silently drop behavior, keep duplicate stale compatibility helpers, weaken tests, leave conflict residue, or keep dead merge scaffolding just because it compiles.

Done means the branch builds, focused behavior tests pass, stale merge leftovers are removed, and the final report lists meaningful conflicts, chosen resolutions, deleted stale surfaces, exact commands run, and remaining risks.
```

This turns "thoughtfully" into concrete merge judgment.

## Anti-Patterns To Avoid

- "Fix it properly" without naming the observable correct behavior.
- "Thoughtfully" without proof, source truth, or acceptance tests.
- "Use skills or whatever" instead of naming owner skills or a routing rule.
- "Done when it works" without saying how to prove it works.
- A review gate that does not say whether the reviewer is blind, what artifacts
  they inspect, or what verdict is required.
- Consensus that asks two models for opinions but never defines convergence.
- Letting an agent choose a workaround when the user's real intent is to
  preserve the hard path.
- Letting stale artifacts become source of truth because they are convenient.
- Long emotional correction text with no normalized structure. Keep the stakes,
  but convert them into outcome, source truth, forbidden shortcuts, proof, and
  signoff.

## Skill Design Recommendation

If this becomes a shipped skill, start with a prompt-only package:

- `skills/goal-prompt-authoring/SKILL.md`
- optional `skills/goal-prompt-authoring/references/examples.md`
- optional `agents/openai.yaml` only if the UI needs a short default prompt

Do not add scripts or a harness yet. The goal text should remain natural
language because the input is usually a rough intent, not a structured spec.

Suggested `description`:

```text
Write or rewrite Codex `/goal` prompts as outcome-driven operating contracts with source truth, scope, forbidden shortcuts, proof gates, and first-class review/model-consensus signoff. Use when the user wants to set, repair, or strengthen a `/goal`; use `$prompt-authoring` for general prompts and `$skill-authoring` for changing the skill package itself.
```

Suggested non-negotiables:

- Output the copyable `/goal` first.
- Preserve the user's intent and stakes, but normalize them into a readable
  mission brief.
- Put the desired world state before mechanics.
- Add system context and a quality bar when they change judgment.
- Prefer outcome and evidence over process ceremony.
- Add workflow labels only when they make the prompt easier to scan.
- Make external signoff explicit whenever requested or warranted by risk.
- Treat signoff as a done gate, not a trailing review suggestion.
- Do not ask for details that can be inferred from the repo, local docs, or the
  user's named skills.
- Do not turn normal language into a parameter schema.
- Do not force every `/goal` into a fixed field list.
- Include stop rules so the goal does not produce infinite investigation or
  premature completion.

Suggested final self-check:

- Could a fresh Codex agent know what done means without reading the user's
  mind?
- Does the first sentence name the desired end state?
- Does the quality bar describe real good output instead of generic polish?
- Does the goal name the source of truth?
- If a rich source doc exists, does the goal point at it instead of copying it?
- Does the goal ban the likely wrong shortcut without becoming a brittle list?
- Does the goal say what evidence must exist?
- If signoff is needed, is it blind/non-leading and part of done?
- Does the goal say when to stop and ask?
- Is the prompt under the 4,000-character hard cap, and preferably within the
  2,000-3,000 character working range or shorter for source-doc-heavy goals?

## Bottom Line

The new variant should train the agent to ask one question:

> What contract would prevent future-me from having to yell the missing
> requirement back into the session?

For your usage, the answer is almost always:

- name the outcome;
- name the source of truth;
- name the quality bar when judgment matters;
- name what not to do;
- require receipts;
- make independent signoff part of done.
