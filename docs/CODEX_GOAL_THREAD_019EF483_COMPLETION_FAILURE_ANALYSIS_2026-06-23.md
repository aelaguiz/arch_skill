# Codex Goal Completion Failure Analysis - Thread 019ef483

Last reviewed: 2026-06-23.

Thread analyzed:

`019ef483-034b-71c1-a78f-d3b59c1af7ec`

Primary transcript:

`/Users/aelaguiz/.codex/sessions/2026/06/23/rollout-2026-06-23T07-44-47-019ef483-034b-71c1-a78f-d3b59c1af7ec.jsonl`

Short answer: the thread failed because the goal did not make completion
authority strict enough. The agent did real work, but it repeatedly treated
"looks complete from the current pass" as enough. The user had to keep forcing
the run back to the source plan, back to literal code requirements, and back to
strict reviewers that were allowed to find missed work.

The reusable lesson for a Codex goal-prompt skill is simple:

- A goal prompt must say what source document controls the work.
- It must require a fresh reread of that source before any completion claim.
- It must define completion as strict-review-clean, not parent-agent-clean.
- It must forbid completing while review agents are still running or while any
  required repair is untriaged.
- It must separate "no proof ceremony" from "no evidence." Minimal compile and
  focused unit proof can still be required when they prove literal code
  contracts.

## Evidence Sources

I used `$agent-history` first, then inspected the exact Codex JSONL transcript
for the target thread.

Agent-history helper results:

- Found the target thread in Codex state with cwd
  `/Users/aelaguiz/workspace/feat/scene-rendering-architecture-plan-2026-06-19`.
- Found the first user message:
  `read docs/PACKS/perspective_scene_systems_inventory_2026-06-19/PERSPECTIVE_SCENE_STABILITY_TARGET_ARCHITECTURE_2026-06-23.md and all of its referenced documents, lmk when you've read them`.
- Found repeated `thread_goal_updated` events and `update_goal {"status":"complete"}`
  events for the same thread.

Transcript evidence quality:

- Exact: goal text, user corrections, tool calls, plan updates, completion calls,
  review-agent status, and patch summaries are pulled from the local Codex
  transcript.
- Inferred: the diagnosis that completion was "surface-level complete" comes
  from comparing those exact events against later user corrections and later
  reviewer findings.
- Limitation: the transcript tail ended while two native audit agents were still
  running. This writeup should not claim the original thread reached a final
  clean close after those agents.

## What The User Asked For

The work started as an architecture-plan implementation flow around this plan:

`docs/PACKS/perspective_scene_systems_inventory_2026-06-19/PERSPECTIVE_SCENE_STABILITY_TARGET_ARCHITECTURE_2026-06-23.md`

The first user ask was not implementation. It was source loading:

- Transcript line `9`: read the plan doc and all referenced documents.
- Transcript line `183`: checkpoint commit those docs before doing more.

Then the user created a planning goal:

- Transcript line `241`: use `$arch-step auto-plan` to turn the target
  architecture doc into a detailed implementation plan, reduce complexity, and
  not implement.

Then the user created the implementation goal:

- Transcript line `865`: use `$arch-step auto-implement` on the same doc, avoid
  extra test/proof ceremony, implement deeply, and use a strict GPT-5.5 x-high
  reviewer plus `$exhaustive-code-review` before signing off.

The implementation prompt already contained the key human concern:

> "the biggest failure pattern is like you implemented in name but not in fact
> all the way down"

The problem is that this was not operationalized strongly enough. It named the
risk, but it did not fully bind completion to fresh source rereads, reviewer
completion, repair triage, and phase-by-phase code evidence.

## Timeline Of Corrections

### 1. Auto-plan completed, but the user had to tighten the plan

The first goal was planning-only.

Evidence:

- Line `241`: the auto-plan goal was created.
- Lines `556` and `586`: the agent said the plan was decision-complete and then
  called `update_goal {"status":"complete"}`.
- Line `590`: the final answer said the plan was ready for `implement-loop`.

Then the user had to correct the plan direction:

- Line `597`: the user said proof ownership stays with Amir, no command
  scaffolding, no simulator ceremony, no extra logs, no new proof process, and
  the plan should name architectural invariants.
- Line `675`: the user clarified minimal unit testing only and no automation.

Meaning:

The agent did complete a plan-shaped artifact. But the user had to keep the plan
from drifting into proof ceremony and had to restate what "prep for manual
device proof" meant.

### 2. Auto-implement goal already asked for strict review, but the run still self-certified

The implementation goal was much stronger than the planning goal.

Evidence:

- Line `865`: the goal explicitly asked for deep implementation, strict
  reviewer, duplicate-source-of-truth detection, and exhaustive code review.
- Line `1696`: the agent said minimal checks were green and it was invoking the
  strict reviewer.
- Line `1728`: the strict reviewer was running.
- Line `1873`: the agent said it was running the final `$exhaustive-code-review`.
- Lines `2164` and `2169`: the agent said the completion audit was clean and
  called `update_goal {"status":"complete"}`.
- Line `2173`: the final answer called it complete for the current SIM/device
  prep frontier.

What went wrong:

The run narrowed the claim to "current SIM/device prep frontier." That can be a
valid status phrase, but it became a side door for completion. The actual plan
still had broader code gates. The prompt did not force the agent to prove each
phase and hard gate against the current code before marking the goal complete.

### 3. The user had to force adversarial audits after completion

Immediately after the completion claim, the user reopened the trust question.

Evidence:

- Line `2180`: the user asked for parallel agents to exhaustively audit the work,
  assume the point had been missed, and reopen phases in the plan with writeups.
- Line `2183`: the agent acknowledged the previous complete claim as unproven.
- Line `2269`: the agent saw a truth-risk shape: the plan said code complete
  while all-route registry demotion, registry lifecycle deletion, lesson lane
  semantics, and device repaint proof were still open.

Meaning:

This is the central failure. A user should not have to say "assume we missed the
point" after the agent already marked the goal complete. That adversarial posture
should have been part of the completion gate.

### 4. The user had to redirect from docs to literal code requirements

The most important correction came later.

Evidence:

- Line `7174`: the user said the issue was not doc hygiene, it was literal code
  requirements that were not finished.
- Line `7176`: the agent acknowledged a concrete Phase 2 code miss: puzzle
  prewarm and visible mount used different lane keys.
- Line `7178`: the plan changed to cross-check Phase 2 lane identity against
  current code and report missed code requirements.
- Line `7191`: the agent tied Phase 2 to a specific rule: no role may inherit
  stable lane behavior from per-step, per-reveal, per-action, or per-runtime-id
  churn.
- Line `7695`: the final answer said the user was right: Phase 2 was not done,
  and puzzle lane identity still depended on replay/run identity.

Meaning:

The agent had been treating plan text, worklog truth, and artifact status as too
important. The user's correction forced the run back to code: why were
`table_scene_a5e542f3` and `table_scene_a4e54160` different for what should have
been one stable table lane?

### 5. The run finally reread the full plan as a requirements source

After the literal-code correction, the agent did the right shape of work.

Evidence:

- Line `7706`: the agent said it was going back to the plan as the source of
  truth, not treating the lane fix as the whole job.
- Line `7720`: the plan changed to load required instructions, reread the full
  target architecture, derive literal code requirements, and audit code against
  every required phase and gate.
- Line `7723`: the agent said phase complete was unproven until current code
  proved each checklist item and exit criterion.
- Line `7796`: the agent summarized the live code requirements as reopened
  Phase 2-7 items: stable lanes, one runtime proof path, registry demotion,
  lane-scoped readiness, live-frame repaint, and owner-boundary cleanup.

Meaning:

This is what should have happened before the first implementation completion
claim. The plan needed to be reread as a live code contract, not remembered as a
general direction.

### 6. More real code misses appeared after the reread

The stricter pass found additional concrete misses.

Evidence:

- Line `7867`: Play vs AI still named `tableRuntimeId` as the stable lane, but
  it appeared to be produced per hand.
- Line `7928`: the agent identified this as a real Phase 2 candidate, not doc
  wording.
- Line `7982`: a test still expected a new runtime id on next hand, preserving
  the old hand-churn requirement.
- Line `8130`: a Phase 2 audit agent independently found and patched the Play
  vs AI hand-derived lane bug.

Meaning:

This confirms the user's point. The previous "complete" label was not just
missing prose. There were more code-level identity violations after the first
fix.

### 7. Strict review found more required repairs

The late strict-review pass surfaced more actual code misses.

Evidence:

- Lines `9062` and `9138`: the repaint/reuse audit reported required repairs.
  One was that prewarm adoption ignored failed live-frame sync, leaving Phase 6
  mechanically open.
- Line `9069`: the x-high delegate found another real code miss in
  `PerspectiveTableScenePrewarmTargetOwner`.
- Line `9108`: the agent found the suspect boundary: source-cache readiness
  could let a child build too early, blanking previously proofed pixels while
  runtime proof caught up.
- Lines `9146` and `9152`: the target-owner gate was patched so it waited for
  exact runtime-proof progress before swapping in a new child, while keeping
  authority in `SceneRuntime.visibleProofFor(...)` and strict `present(...)`.
- Line `9220`: the review artifact recorded three repaired required findings:
  prewarm adoption sync, temporary trace toggles, and target-owner source-cache
  replacement.

Meaning:

The strict reviewers were not ceremonial. They found real code issues that the
parent pass had missed. Therefore a better goal prompt must say: launch, wait,
read, repair, and only then decide completion.

### 8. The transcript tail still had running reviewers

The transcript did not end with a fully closed clean verdict.

Evidence:

- Line `9198`: two native audit agents were still running.
- Line `9201`: the main agent said it was doing a code audit while those agents
  finished.
- Line `9226`: the transcript tail showed a `wait_agent` call.

Meaning:

Do not cite this thread as a clean success. Cite it as a failure and repair
case. The key evidence is not the final state of the app. The key evidence is
what the user had to do to make the agent stop self-certifying.

## The Actual Failure Pattern

The model did not simply ignore the plan. It used the plan at the beginning,
then gradually replaced the plan with a smaller local belief:

1. The current patch looks aligned.
2. The current checks are green.
3. The current artifact says review happened.
4. The current frontier sounds bounded.
5. Therefore the goal can be marked complete.

That is too weak for plan-backed architecture work.

For this kind of task, completion has to mean:

1. Reopen the governing plan.
2. Read the relevant phase/checklist/exit criteria again.
3. Translate them into literal code requirements.
4. Inspect current code for each one.
5. Run strict reviewers that assume misses.
6. Wait for every reviewer.
7. Patch every required repair or leave the goal active.
8. Only then call `update_goal complete`.

The parent agent's own confidence is not enough.

## Why The Original Goal Prompt Was Close But Not Enough

The implementation goal included good raw material:

- It named `$arch-step auto-implement`.
- It named the plan doc.
- It said to avoid test/proof churn.
- It said to implement deeply.
- It named the failure pattern: implemented in name, not in fact.
- It asked for a strict GPT-5.5 x-high reviewer.
- It asked for exhaustive code review before signoff.

But it did not close these loopholes:

### Loophole 1: Rereading was not a completion gate

The goal named the plan doc, but did not say:

Before claiming completion, reread the full plan and all reopened phases, then
map every phase/checklist/exit criterion to code evidence.

Without that, the agent used a stale mental summary.

### Loophole 2: Review launch counted too much like review completion

The goal said to use a strict reviewer and exhaustive review. It did not say:

Do not call `update_goal complete` until every reviewer has returned, every
required repair has been patched, and every reviewer finding has a written
disposition.

The thread later showed reviewers still running while repair work continued.

### Loophole 3: "Minimal testing" blurred into "weak evidence"

The user wanted no simulator automation and no proof ceremony. The agent needed
to preserve that while still running narrow evidence checks.

The better distinction is:

- Do not add simulator automation, command scaffolding, proof logs, or broad
  test churn.
- Do run the smallest compile/static/unit checks that prove changed code
  contracts.

That distinction became clear only after the user corrected the run.

### Loophole 4: Docs and artifacts looked like completion

The agent repeatedly fixed plan/worklog/review artifact truth. Some of that was
useful. But useful doc truth is not code completion.

A better goal prompt must say:

Docs, worklogs, audit blocks, and review artifacts can record evidence. They do
not prove code requirements unless they point to current code evidence.

### Loophole 5: The goal allowed a narrower "frontier" to replace the full plan

The line "current SIM/device prep frontier" became a scope shrink. The user's
real intent was code prep for the plan, with manual device proof left to Amir.
That means code-side phases could remain open only when the remaining proof was
manual app proof, not when code gates were still incomplete.

## What The User Had To Do Manually

The user had to do five jobs that the goal prompt should have forced:

1. Reassert source authority.

The user pushed the agent back to the target architecture plan and all
referenced documents instead of letting it rely on memory or doc-shaped status.

2. Reassert code over docs.

The user had to say the issue was literal code requirements, not document
hygiene.

3. Reopen false completion.

After `update_goal complete`, the user had to ask for parallel audits that
assumed the point had been missed.

4. Force adversarial review.

The user had to make the reviewers hostile to the completion claim, not friendly
confirmation passes.

5. Name the failure mode from app evidence.

The user brought the key symptom back to lane identity: prewarm prepared one
table lane while visible mounted another. That converted the task from abstract
architecture compliance into a concrete code requirement.

## Correction Taxonomy

### Source-truth Correction

Symptom:

The agent used the plan as context, then reasoned from memory.

Required behavior:

The agent must reread the governing plan before completion, especially reopened
phases and hard closure gates.

### Completion-authority Correction

Symptom:

The parent agent marked complete after its own audit.

Required behavior:

Completion authority must include strict reviewers. The parent cannot complete
while strict reviews are running or untriaged.

### Literal-code Correction

Symptom:

The agent repaired docs, artifacts, and status labels while code requirements
were still missed.

Required behavior:

Every plan requirement must map to a current code path, a current code diff, or
an explicitly manual app-proof item.

### Anti-scope-shrink Correction

Symptom:

"Current prep frontier" narrowed the completion claim.

Required behavior:

If a phase remains open, the agent must say whether it is open because of
manual app proof or because code work remains. Code work remaining means the
goal is not complete.

### Reviewer-gate Correction

Symptom:

Reviewer use was treated as a step, not a gate.

Required behavior:

Reviewers must be asked to assume misses, and every required repair must be
patched or explicitly left open before completion.

### Evidence-freshness Correction

Symptom:

Earlier green checks and artifacts carried too much weight.

Required behavior:

Completion evidence must be fresh against the current worktree after the last
patch and after all reviewer findings.

## Better Goal Prompt For This Situation

This is the kind of prompt the goal-coach skill should help generate:

```text
Use $arch-step auto-implement on:

docs/PACKS/perspective_scene_systems_inventory_2026-06-19/PERSPECTIVE_SCENE_STABILITY_TARGET_ARCHITECTURE_2026-06-23.md

The plan doc and its referenced docs are the source of truth. Before coding,
read the full plan and extract the literal code requirements by phase, checklist,
exit criterion, hard gate, and required deletion/demotion.

Do not treat docs, worklog entries, review artifacts, or "current frontier"
wording as completion. They only count if they point to current code evidence.

No simulator automation, no command scaffolding, no proof ceremony, and no broad
test churn. Do run the smallest format/analyze/unit checks that prove the changed
code contracts.

Before any completion claim:

1. Reread the full plan and all reopened phases.
2. Build a requirement-to-evidence list for the current worktree.
3. For every code-side requirement, show file/symbol evidence or keep working.
4. Distinguish manual Amir app proof from unfinished code work.
5. Run the requested strict GPT-5.5 x-high reviewer and $exhaustive-code-review.
6. The reviewers must assume we missed the point, created duplicate truth, left
   old authority paths alive, or implemented in name only.
7. Wait for every reviewer to finish.
8. Patch every required repair, then rerun only the narrow checks needed for
   those patches.
9. If any reviewer is still running, any required repair is untriaged, or any
   code-side phase is still open, do not call update_goal complete.

Completion means strict-review-clean code prep for the plan, with only manual
app/SIM proof left to Amir.
```

## What A Goal-Prompt Skill Should Add

The reusable skill should not become a harness. It should help the user turn a
strong instinct into a goal prompt with hard stop conditions.

For plan-backed implementation goals, the skill should add these blocks:

### 1. Source Truth Block

Name the canonical plan path and referenced docs.

Example:

```text
The source of truth is <plan path> plus its referenced documents.
Reread them before implementation and before completion.
```

### 2. Literal Requirements Block

Force extraction from source text into code obligations.

Example:

```text
Extract requirements by phase, checklist, exit criterion, hard gate, required
delete, and required demotion. Treat those as code requirements unless the plan
explicitly says they are manual proof only.
```

### 3. Anti-surface-completion Block

Prevent doc/status artifacts from passing as implementation.

Example:

```text
Docs and worklogs may record evidence, but they do not satisfy code requirements
unless current code evidence proves the requirement.
```

### 4. Strict Reviewer Block

Make review a gate, not a decorative step.

Example:

```text
Launch the strict reviewer only when the code is believed ready. The reviewer
must assume missed requirements, duplicate truth, old fallback paths, and
implemented-in-name-only work. Completion is forbidden until every reviewer
returns and every required repair is patched or explicitly left open.
```

### 5. Running-agent Block

Forbid completing while reviewers are still active.

Example:

```text
Do not mark the goal complete while any review agent is still running or any
review artifact says a required repair is open.
```

### 6. Minimal-evidence Block

Preserve the user's no-ceremony preference without weakening proof.

Example:

```text
Do not add simulator automation, proof logs, command scaffolding, or broad
testing. Do run focused format/analyze/unit checks when they directly prove the
changed code contract.
```

### 7. Manual-proof Boundary Block

Prevent "manual proof pending" from hiding code work.

Example:

```text
Manual app proof may remain pending only after code-side requirements are
strict-review-clean. If code work remains, keep the goal active.
```

## Recommended Skill Behavior

The best skill behavior is a prompt coach, not an executor.

When the user asks for a goal prompt, it should:

1. Ask what artifact is source of truth if the prompt lacks one.
2. Detect whether the task is plan-backed implementation, broad architecture,
   review, bug repair, or simple one-shot work.
3. Add completion gates that match the task type.
4. Add reviewer gates when the user asks for strict review, exhaustive review,
   or "do not miss the point."
5. Add an anti-surface-completion clause when the task can be falsely completed
   by docs, artifacts, checklists, or green narrow tests.
6. Add a "do not complete while reviewers are running" clause for any parallel
   audit flow.
7. Keep the final prompt compact enough to paste into `/goal`.

It should not:

- Create a YAML loop.
- Add a runner.
- Add a deterministic controller.
- Replace agent judgment with a harness.
- Force broad test automation when the user explicitly wants minimal checks.

## Strongest Lesson

The user's core issue was not that Codex lacked a reviewer, a plan, or a test
command. The issue was that the goal did not define who is allowed to say
"done."

For this kind of work, "done" must mean:

- the plan was freshly reread;
- literal code requirements were extracted;
- current code was checked requirement by requirement;
- strict reviewers finished;
- required repairs were patched;
- narrow proof was rerun after the final patch;
- only manual app proof remains.

Anything less is allowed to look complete while still being incomplete in the
way the user cares about most: implemented in name, not in fact.
