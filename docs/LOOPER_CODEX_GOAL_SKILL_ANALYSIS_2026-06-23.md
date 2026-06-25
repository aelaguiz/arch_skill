# Looper To Codex Goal Skill Analysis

Last reviewed: 2026-06-23.

This document answers two questions:

1. How does `vendor/looper` work?
2. Can its useful ideas become a generic Codex skill for writing better `/goal`
   prompts?

Short answer: yes, but not by porting Looper directly. The best reusable piece
is Looper's goal-coaching and verification discipline. The wrong move would be
to bring over the full YAML loop spec, model registry, slash command, and
external runner unless the user explicitly wants a portable loop scaffolder.

The best first implementation is either:

- add a Looper-informed reference to the existing `prompt-authoring` skill,
  because it already owns compact Codex `/goal` mission briefs; or
- create a small explicit skill such as `codex-goal-coach` if a separate
  invocation surface is useful.

In both cases, keep it prompt-only first.

## Source Material Reviewed

Looper sources:

- `vendor/looper/README.md`
- `vendor/looper/SKILL.md`
- `vendor/looper/looper-spec.md`
- `vendor/looper/commands/looper.md`
- `vendor/looper/agents/openai.yaml`
- `vendor/looper/references/goal-rubric.md`
- `vendor/looper/references/verification-rubric.md`
- `vendor/looper/references/council-rubric.md`
- `vendor/looper/references/control-rubric.md`
- `vendor/looper/references/model-detection.md`
- `vendor/looper/scripts/looper.py`
- `vendor/looper/templates/loop.yaml`
- `vendor/looper/templates/run-loop.py`
- `vendor/looper/schemas/loop.v1.schema.json`
- `vendor/looper/schemas/loop.resolved.v1.schema.json`
- `vendor/looper/examples/ai-workflow-mapping/*`
- `vendor/looper/tests/test_looper.py`

Local arch_skill sources:

- `skills/prompt-authoring/SKILL.md`
- `skills/prompt-authoring/references/codex-goal-prompts.md`
- `skills/goal-loop/SKILL.md`
- `skills/arch-skills-guide/references/skill-map.md`
- `docs/CODEX_GOAL_PROMPT_AUTHORING_ANALYSIS_2026-05-03.md`
- `README.md`
- `Makefile`

Skill-authoring guidance used:

- `/Users/aelaguiz/.agents/skills/skill-authoring/SKILL.md`
- `/Users/aelaguiz/.agents/skills/skill-authoring/references/skill-pattern-contract.md`
- `/Users/aelaguiz/.agents/skills/skill-authoring/references/leverage-and-scope.md`
- `/Users/aelaguiz/.agents/skills/skill-authoring/references/packaging-trigger-and-validation.md`

## What Looper Is

Looper is a Claude Code skill and slash command that helps a user design an
agent loop before running it.

Its core promise is:

> Goal -> Plan -> Review -> Deliver -> Judge -> Stop clean.

It does not primarily execute a task. It designs a loop that can execute a
task. That distinction matters.

Looper sits in front of execution tools. Claude Code `/goal` can keep a model
working toward an objective. Claude Code `/loop` can schedule repeated prompts.
Looper tries to make sure the thing handed to those tools is clear,
checkable, reviewed, and bounded before anything starts running.

## How Looper Works

Looper has four main layers.

### 1. Slash Command Entrypoint

`vendor/looper/commands/looper.md` defines `/looper`.

The command does a small bootstrap job:

- find the global Looper skill directory;
- read that installed `SKILL.md`;
- treat the slash-command argument as the target output directory;
- hand control to the Looper skill workflow.

This is Claude-specific. It depends on Claude Code's command and skill layout.

### 2. Skill Workflow

`vendor/looper/SKILL.md` is the runtime contract.

It tells the agent to run a seven-stage interview:

1. Goal
2. Verification
3. Host model
4. Council
5. Gates and control
6. Confirmation flow preview
7. Emit or run option

The skill uses stage-specific references:

- `goal-rubric.md` for tightening the goal.
- `verification-rubric.md` for turning done-ness into checks.
- `council-rubric.md` for reviewer and judge selection.
- `control-rubric.md` for caps, no-progress stops, and execution boundary.
- `model-detection.md` for model CLI detection and privacy details.

The skill emits these files into a target directory:

- `loop.yaml`
- `loop.resolved.json`
- `LOOP.md`
- `RUN_IN_SESSION.md`
- `run-loop.py`
- `loop-workspace/`
- `README.md`

The most important emitted file is `RUN_IN_SESSION.md`. It is the easy path:
the current agent can follow that handoff prompt directly.

The Python runner is the advanced path.

### 3. Compile And Render Helper

`vendor/looper/scripts/looper.py` is the scaffolding helper.

It owns deterministic mechanics:

- detect installed model CLIs and write `~/.looper/models.json`;
- register custom model invocations;
- compile `loop.yaml` into `loop.resolved.json`;
- validate the loop shape;
- normalize shell-ish commands into argv arrays;
- render `LOOP.md`;
- render `RUN_IN_SESSION.md`;
- render the ASCII flow preview.

It explicitly says it must not invoke model CLIs to do loop work. That keeps
the helper on the scaffolding side, not the execution side.

The compile step validates and normalizes these major fields:

- `goal.statement`
- `goal.definition_of_done`
- `goal.context_sources`
- `goal.verification`
- `host`
- `council`
- `gates.plan_gate`
- `gates.delivery_gate`
- `loop_control`
- `execution`
- `observability`
- `privacy`
- `workspace`

It also adds useful defaults:

- no-progress detection;
- wall-clock budget;
- current-workspace execution;
- gate-level observability;
- default redaction globs.

### 4. Optional External Runner

`vendor/looper/templates/run-loop.py` is the external executor template.

Its job is to read `loop.resolved.json` and run the designed loop:

1. Gather context.
2. Ask the host model to draft `plan.md`.
3. Run the plan gate.
4. Revise until the gate passes or the revision cap is reached.
5. Ask the host model to write `delivery-N.md`.
6. Run the delivery gate.
7. Repeat until pass, max iteration, budget breach, or no-progress stop.
8. Keep `state.json` and `run-log.md` current.

The runner has real execution behavior:

- calls host and judge model CLIs;
- runs programmatic checks;
- asks for human signoff;
- asks for consent before non-local model egress;
- parses structured judge output;
- treats unparseable judge output as a revision warning;
- stops on hard caps.

That runner is useful for Looper, but it is the part least suited to a generic
Codex `/goal` prompt skill.

## Looper's Data Model

Looper's `loop.yaml` has a clear schema. The important fields are:

| Field | Meaning |
| --- | --- |
| `goal.statement` | The outcome the loop is trying to produce. |
| `goal.context_sources` | Files or commands the loop should inspect before acting. |
| `goal.definition_of_done` | The state or artifact that proves the loop finished. |
| `goal.verification` | Typed checks: `programmatic`, `judge`, or `human`. |
| `host` | The model CLI that does the work. |
| `council` | Reviewers or judges that critique or gate the work. |
| `gates` | Plan and delivery checkpoints. |
| `loop_control` | Iteration caps, revision caps, no-progress stops, and budgets. |
| `execution` | Where the loop may run and modify state. |
| `observability` | State and log files. |
| `privacy` | What can leave the machine and what must be redacted. |
| `workspace` | The files the loop will write. |

The strongest design choice is the verification taxonomy:

- `programmatic`: a command or deterministic check passes or fails.
- `judge`: a model applies a rubric and returns a structured verdict.
- `human`: a person must sign off.

This is exactly the kind of thinking Codex `/goal` prompts need, but Codex
does not need it as YAML by default.

## The Core Ideas Worth Reusing

Looper's reusable value is not the full loop package. The reusable value is the
pre-flight coaching.

The useful ideas are:

### Outcome Before Activity

Looper pushes the user from activity language to outcome language.

Weak:

```text
Improve onboarding.
```

Better:

```text
Produce a five-step onboarding workflow map with each step assigned to a product surface, email, human owner, or missing capability, and no unresolved TBDs.
```

For Codex `/goal`, this maps directly to the first sentence: name the desired
world state, not the action list.

### Definition Of Done Must Be Checkable

Looper makes done-ness explicit.

For a Codex goal prompt, this becomes:

- exact tests or commands;
- visible artifact changes;
- screenshots or generated outputs when relevant;
- reviewer signoff;
- final report contents.

The goal prompt should make false completion hard.

### Verification Should Be Typed

Looper separates deterministic checks, model judgment, and human judgment.

For Codex, that should become a simple proof ladder:

1. Prefer programmatic proof when it exists.
2. Use a judge or reviewer for semantic quality.
3. Use human signoff for taste, private business knowledge, safety, or final authority.

Do not ask the same model doing the work to be the only judge of whether the
work is good.

### Reviewer And Judge Are Different Jobs

Looper's distinction is clean:

- A reviewer gives notes.
- A judge returns a blocking pass/revise verdict.

For goal prompts, this matters because "get feedback" is not a done gate. A
goal that needs independent signoff should say what verdict counts as done and
what happens if the verdict fails.

Good Codex-goal shape:

```text
Done requires a fresh reviewer to agree the goal is satisfied. If review rejects the result, use the objection as the next repair input and rerun review.
```

### Stop Conditions Prevent Fake Persistence

Looper requires caps and no-progress handling.

Codex `/goal` already provides persistence, but persistence alone is not
quality. A strong goal prompt should say what to do when the path is unclear:
read source truth, form sharper theories, add disproof tests, inspect the real
path, and keep repairing until the desired state is real.

It should also define real blockers rather than letting the model stop at "I
am uncertain."

### Privacy Is Part Of Cross-Model Review

Looper names what leaves the user's machine when using another model CLI.

A Codex goal skill should keep that habit. If the prompt asks for Claude,
Grok, Cursor Agent, ChatGPT, or another external reviewer, it should name the
inputs sent to that reviewer and avoid sending secrets.

## What Should Not Be Ported Directly

These Looper parts are useful inside Looper but wrong as the default for a
generic Codex goal-prompt skill.

### Do Not Port The YAML Spec As The Default Interface

Codex `/goal` wants a compact mission brief, not a second plan document.

The local prompt-authoring guidance already says Codex `/goal` prompts have a
4,000-character hard cap and usually work best far below that. A YAML schema
would make normal goal writing heavier than needed.

### Do Not Port The External Runner By Default

Codex native goal mode is already the runner.

A goal-prompt skill should improve the goal text that Codex receives. It
should not create a second loop engine unless the user explicitly asks for an
external orchestrator.

### Do Not Port Claude-Specific Slash Command Mechanics

`commands/looper.md`, `disable-model-invocation`, `${CLAUDE_SKILL_DIR}`, and
Claude Code install paths are not generic Codex skill mechanics.

The portable value is the prompt contract, not the Claude command wrapper.

### Do Not Force Plan/Delivery Gates Onto Every Goal

Looper's plan gate and delivery gate are good for designed loops.

Many Codex goals are simpler:

- fix a bug;
- implement a plan;
- write a doc;
- refactor a prompt;
- run a review.

Those goals still need proof and signoff, but they do not always need a
separate `plan.md`, `delivery-N.md`, `state.json`, and `run-log.md`.

### Do Not Add Model CLI Detection To The Prompt Skill

Looper's model detection is useful for an executable runner. A prompt-only
Codex skill can simply name the reviewer skill or model when needed and let
the owning review/delegation skill handle invocation.

## Existing Skill Overlap

This repo already has nearby skills.

### `prompt-authoring`

`prompt-authoring` already owns:

- prompts;
- reusable prompt contracts;
- Codex `/goal` mission briefs;
- prompt repair and audit;
- anti-heuristic refactors.

It already has `references/codex-goal-prompts.md`, which is very close to the
proposed destination.

That makes `prompt-authoring` the default owner unless there is a strong reason
to create a separate UX.

### `goal-loop`

`goal-loop` is not the same thing.

It owns open-ended goal-seeking work with:

- a controller doc;
- an append-only worklog;
- repeated bets;
- North Star confirmation.

A Codex goal prompt coach should not become `goal-loop`. It should help write
the `/goal` instruction itself.

### `arch-skills-guide`

`arch-skills-guide` already distinguishes native `/goal` from specialized loop
skills. It says native `/goal` is right when requirements are free-form and no
arch-skill artifact contract is needed.

That supports the recommendation here: use Looper ideas to improve native
goals, not to force every goal into a loop package.

## Skill-Authoring Decision

Using the `$skill-authoring` lens, the repeated user problem is real:

- "Help me write a better `/goal` prompt for this task."
- "Turn this vague objective into a Codex goal that will not self-certify too early."
- "Review this `/goal` prompt and tell me what it is missing."
- "Make this goal include proof, signoff, and no shortcut exits."

The leverage claim is also real:

> A goal-prompt coach reduces repeated prompt-writing, makes done-ness explicit,
> and prevents common Codex goal failures: vague success, wrong source truth,
> hidden false finish lines, weak proof, and self-certification.

The mechanism choice is the main question.

### Recommendation

Prefer this order:

1. Extend `prompt-authoring` with a Looper-derived reference or section.
2. Create a new explicit-only `codex-goal-coach` skill only if the separate
   user-facing entrypoint matters.
3. Do not create a runner, schema, slash command, or model registry until a
   real repeated failure proves prompt-only guidance is insufficient.

That follows the local skill-authoring rule: start prompt-first, add references
only when they reduce repeated prompting, and add scripts only for deterministic
work.

## Proposed Skill Shape

If we create a new skill, the cleanest shape is prompt-only.

Suggested name:

```text
codex-goal-coach
```

Nearest peer:

```text
prompt-authoring
```

Reason to keep it separate:

- the user wants an explicit, memorable skill for `/goal` prompt coaching;
- we want a narrow trigger that does not also handle ordinary prompt writing;
- we want the skill to behave like a goal pre-flight checklist.

Reason to fold it into `prompt-authoring`:

- `prompt-authoring` already owns Codex `/goal` prompts;
- a new skill could overtrigger or confuse peer selection;
- the proposed workflow is mostly a specialized prompt-authoring mode.

### Candidate Description

If separate:

```yaml
description: "Write, rewrite, or audit compact Codex /goal prompts by coaching a fuzzy task into an outcome-driven mission brief with source truth, false-finish guardrails, proof, reviewer or human signoff, and persistence rules. Use when the user asks for a better Codex goal, goal-mode prompt, long-running task objective, or review of an existing /goal. Not for executing the goal, designing a full YAML loop, or running an open-ended controller-doc loop."
```

This is under the 1024-character default cap.

### Minimal `SKILL.md` Contract

The skill should teach this workflow:

1. Classify the ask as create, rewrite, or audit.
2. Name the desired world state in one sentence.
3. Identify the likely false finish line.
4. Find source truth: repo files, docs, plan, existing prompt, issue, diff, or
   current failing behavior.
5. Separate controlling sources from stale context.
6. Translate verification into proof:
   - programmatic checks where available;
   - judge/reviewer signoff for semantic quality;
   - human signoff for user-owned decisions.
7. Add only the workflow rules that change execution.
8. Add a short forbidden-shortcuts line for the likely bad exits.
9. Add persistence behavior for unclear paths.
10. Define done with evidence and signoff.
11. Compress the prompt so it stays usable as `/goal` text.

### Output Contract

For create/rewrite:

- return one copyable `/goal` prompt;
- add a short note only if an assumption matters.

For audit:

- list findings first;
- explain why each issue can make the goal fail;
- return a revised `/goal` prompt.

### Canonical Use Cases

Good triggers:

```text
Help me write a better Codex /goal for this task.
```

```text
This goal keeps stopping too early. Rewrite it so Codex knows what done means.
```

```text
Audit this /goal prompt before I run it.
```

Nearby anti-cases:

```text
Design a portable multi-model loop with YAML, judges, and an external runner.
```

That should route to Looper-style loop scaffolding, not a goal prompt coach.

```text
We have an open-ended metric goal and need a controller doc plus worklog.
```

That should route to `goal-loop`.

```text
Write a system prompt for a reviewer agent.
```

That should stay with `prompt-authoring`.

## Looper-To-Codex Translation Table

| Looper concept | Codex goal-prompt translation |
| --- | --- |
| `goal.statement` | First sentence naming the desired world state. |
| `goal.context_sources` | "Use these files/docs/commands as source truth." |
| `goal.definition_of_done` | "Done means..." sentence with proof. |
| `programmatic` criterion | Exact tests, commands, build, lint, generated artifacts, screenshots, or receipts. |
| `judge` criterion | Fresh reviewer, model consensus, or domain critic signoff. |
| `human` criterion | User signoff for subjective or business-owned decisions. |
| `plan_gate` | Optional planning signoff before implementation. |
| `delivery_gate` | Final proof and review gate. |
| `max_revisions` | "If review rejects, repair and rerun review; do not stop at rejection." |
| `no_progress` | "When the same blocker repeats, sharpen evidence or ask for the specific missing decision." |
| `budget` | Time/cost/iteration cap only when it changes behavior. |
| `execution.isolation` | Worktree/branch/current-workspace boundary if relevant. |
| `privacy.egress` | What gets sent to external reviewers and what must be redacted. |
| `state.json` and `run-log.md` | Usually final report or lightweight worklog only for long-running goals. |

## Example Output Shape

A goal coach should usually produce something like this:

```text
/goal Implement [desired world state] in [repo/path].

Use [source truth paths] as controlling source truth. Treat [stale or weaker sources] as context only.

The false finish line is [likely shortcut that looks done but violates intent].

Do not [small set of likely bad shortcuts].

When the path is unclear, keep moving by reading source truth, reproducing the real behavior, forming sharper theories, adding focused tests or instrumentation, and using required review to choose the next repair.

Done means [system state works], [exact proof commands/artifacts], [review or human signoff], and the final report lists changed files, commands, evidence, signoff result, and remaining risks.
```

Not every goal needs every paragraph. The skill should remove lines that do
not change behavior.

## Why This Should Stay Prompt-First

A good Codex `/goal` prompt is not an executable workflow spec. It is a compact
mission brief.

The local prompt-authoring guidance says the goal should carry:

- mission;
- source truth pointers;
- false finish line;
- a few workflow rules that matter;
- likely shortcuts to avoid;
- evidence and signoff gates;
- completion and persistence rules.

It should not carry:

- the whole plan;
- duplicated reference docs;
- every command list;
- every example;
- a runner contract;
- a schema unless the user explicitly needs one.

That means Looper's full package is too heavy for the default Codex goal use
case.

## Risks If We Build This As A New Skill

### Risk 1: It Duplicates `prompt-authoring`

The existing `prompt-authoring` skill already says it writes Codex `/goal`
mission briefs. A new skill must have a narrow trigger and clear peer boundary
or it will create routing confusion.

Mitigation:

- make the new skill explicit-only; or
- fold the Looper-derived guidance into `prompt-authoring` instead.

### Risk 2: It Over-Formalizes Natural Language

Looper's schema is useful because Looper emits runnable artifacts. A goal
prompt coach does not need formal fields for normal user asks.

Mitigation:

- output prose `/goal` prompts, not YAML;
- use the Looper taxonomy as internal reasoning, not user-facing ceremony.

### Risk 3: It Encourages Self-Certification

Codex goal mode can keep working, but the same model is still often judging
its own completion.

Mitigation:

- make reviewer, judge, or human signoff first-class when the work is risky;
- define what happens when review rejects the result.

### Risk 4: It Becomes A Thin Wrapper Around Looper

If the new skill copies Looper's file set, it becomes a second loop scaffolder
instead of a Codex goal prompt helper.

Mitigation:

- no scripts initially;
- no runner initially;
- no generated workspace initially;
- no model registry initially.

## Concrete Build Recommendation

Best next step:

1. Do not add a new runnable loop system.
2. Add a focused reference to `skills/prompt-authoring/references/`, likely
   named `goal-coaching-from-looper.md`.
3. Update `skills/prompt-authoring/SKILL.md` so Codex `/goal` asks read that
   reference when the user wants stronger goal development, goal review, or
   long-running goal-mode prompt repair.
4. Keep the existing `codex-goal-prompts.md` as the controlling reference for
   final prompt shape and character budget.
5. If that feels too buried after use, split a new explicit-only
   `codex-goal-coach` skill with a lean `SKILL.md` and one reference.

If a new skill is created later, update:

- `skills/codex-goal-coach/SKILL.md`
- optional `skills/codex-goal-coach/agents/openai.yaml`
- `README.md`
- `Makefile`
- `docs/arch_skill_usage_guide.md` if the skill map needs it

Then run:

```bash
rtk npx skills check
```

If install behavior changes, also run:

```bash
rtk make verify_install
```

## Proposed Reference Contents

If implemented as a `prompt-authoring` reference, the reference should include
only the portable Looper pieces:

- outcome versus activity;
- context sources and source-truth hierarchy;
- false-finish identification;
- typed proof:
  - programmatic;
  - judge;
  - human;
- reviewer versus judge;
- signoff as part of done;
- no-progress and blocker handling;
- privacy for external reviewers;
- compression back into a pasteable `/goal`.

It should not include:

- Looper install instructions;
- `loop.yaml`;
- model detection;
- full external runner behavior;
- Claude slash-command details;
- generated workspace file contract;
- broad loop orchestration.

## Verification Notes

This analysis is based on source inspection.

I attempted two local validation commands while inspecting the vendored package:

```bash
rtk python3 -m pytest vendor/looper/tests -q
rtk python3 vendor/looper/tests/test_looper.py
```

They did not validate Looper behavior in this environment:

- `pytest` is not installed for the active Python.
- `PyYAML` is not installed for the active Python, so the unittest path failed
  during `loop.yaml` compilation.

That does not block this document because no Looper code was changed. If we
later change `vendor/looper` itself or depend on its compiler behavior, install
the test dependencies and rerun the tests.

Because this change is documentation-only, the repo's required code
verification is a re-read plus path/command consistency check, not
`rtk npx skills check`.

## Bottom Line

Looper is a strong loop design coach. Its best idea is not "run a loop with
Python." Its best idea is "do not let an agent loop start until the goal,
proof, reviewer, privacy, and stop rules are clear."

That idea maps very well to Codex `/goal` prompts.

The right Codex skill should help the user turn a fuzzy objective into a small
mission contract:

- outcome;
- source truth;
- false finish line;
- proof;
- signoff;
- persistence rules;
- no shortcut exits.

Start by strengthening `prompt-authoring`. Create a separate
`codex-goal-coach` skill only if you want a dedicated explicit entrypoint.
