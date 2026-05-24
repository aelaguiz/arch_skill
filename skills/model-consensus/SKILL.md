---
name: model-consensus
description: "Run a prompt-only, parent-agent orchestrated dialogue between two named Claude/Codex/Cursor Agent models to cross-check, critique, and converge on a lean plan, architecture, debugging strategy, investigation, design, or concept. Use when the user wants iterative two-model agreement or adversarial simplification. Repo-backed runs make both models read real evidence, but open investigations preserve child discovery freedom. Not for one-shot cold opinions, deterministic code review, ordered implementation loops, or broad idea tournaments."
metadata:
  short-description: "Agent-run two-model consensus for lean repo-grounded plans"
---

# Model Consensus

Use this skill when the user wants two selected models to think together until
they converge on the best answer. The parent agent is the runner: it
orchestrates the dialogue, preserves the goal, routes evidence between the two
child sessions, checks for agreement, and reports the result. Do not add or
depend on a deterministic runner, script, controller, state machine, or harness
layer for this skill.

The work is not "ask two models and concatenate the answers." The goal is a
disciplined conversation that removes weaker ideas, preserves independent
evidence discovery when the task is investigative, converges on existing repo
patterns when the task is architectural, and avoids kitchen-sink plans.
## Use When

- The user wants two Claude/Codex/Cursor Agent models to iterate on a plan,
  architecture, design, migration, debugging strategy, investigation, or
  concept.
- The user wants a cross-check where the value comes from independent model
  judgment, critique, and convergence rather than one model answering once.
- The user wants one model in adversarial mode to challenge assumptions,
  propose simpler alternatives, or argue against overbuilt choices.
- The question is repo-backed and the answer should minimize new pathways by
  adopting canonical code patterns, owner modules, tests, and conventions.
- The final answer needs explicit agreement, explicit non-agreement, or a small
  set of remaining decision points.

## Do Not Use When

- The user wants one cold second opinion without dialogue or convergence: use
  `fresh-consult`.
- The user wants deterministic code-review findings: use `code-review`.
- The user wants ordered implementation or epic execution: use `stepwise` or
  `arch-epic`.
- The user wants broad idea generation across many options: use an ideation
  skill instead.
- The user only wants the current agent's own answer.

## Non-Negotiables

- Keep the runner intelligent. The parent agent may judge whether a reply is
  grounded, whether the next round needs a tighter prompt, and whether the
  models have actually converged. It must not reduce the work to a brittle
  script or fake state machine.
- The parent agent must not solve the problem itself. It may restate the goal,
  enforce the process, ask for missing model choices, request repo evidence,
  and synthesize only what the child sessions actually agreed on.
- Preserve child discovery freedom. The parent records the raw goal, resolved
  model mapping, explicit constraints, desired output, and exact user-named
  artifacts. The child models choose the evidence path and frame the
  investigation themselves.
- Preserve the user's raw goal. Use prompt-authoring discipline to create a
  faithful goal brief that clarifies success criteria without injecting a
  solution.
- For repo-backed work, start children from the raw goal and exact user-named
  inputs. If the user wants a plan, the children should find the existing owner
  path before proposing where work belongs. If the user wants an investigation,
  the children should choose and cite the evidence trail themselves.
- Ask once for missing model choices. Each participant needs runtime, runnable
  model id or exact model phrase, and effort. If the user names shorthand such
  as "gpt 5.5 xhigh" or "Claude Opus 4.7 high", resolve it with the shared
  model-resolution rules and announce the raw-to-resolved mapping.
- For repo-backed work, both child models must read real evidence before they
  are allowed to recommend or agree. In open investigation mode, require them to
  choose and cite the code, docs, research, tests, and commands they need. In
  architecture mode, require canonical owner paths and existing patterns.
- In architecture mode, prefer one existing path over two new ones. A new
  abstraction, mode, file family, or workflow is valid only after both models
  have inspected the canonical owner path and explained why the existing path
  cannot absorb the work.
- Agreement is not accumulation. If one model proposes five ideas and the
  other proposes four, the final plan is not nine ideas. Push them to the
  smallest architecture that satisfies the goal.
- Prompt the models as collaborators. Teach the mission, context, quality bar,
  and why simplicity and repo convergence matter. Do not treat them as stupid
  prompt runners.
## First Move

Read these references before invoking children:

- `references/workflow-contract.md`
- `references/prompt-contracts.md`
- `references/model-and-invocation.md`
- `references/repo-grounding.md` when a repo, codebase, or local project is
  involved
- `references/convergence-and-synthesis.md`

Then:

1. Capture the raw user goal and whether the user asked for ordinary
   collaboration or adversarial critique.
2. Build a faithful goal brief using prompt-authoring discipline. Clarify the
   goal, constraints, desired output, and exact user-named inputs without adding
   the caller's diagnosis or investigation frame.
3. Resolve the two participant execution choices. Ask one concise question if
   any runtime/model/effort choice is missing or ambiguous. For Cursor Agent,
   effort is encoded in the model id.
4. Create a per-run artifact directory by hand, for example
   `.arch_skill/model-consensus/<slug>-<timestamp>/`. Store prompts, final
   replies, event streams, and a short run index there. Do not create a script.
5. If repo-backed, make the first child prompt require real evidence. Tell the
   models to start from user-named artifacts or symptoms, then choose and cite
   whatever code, docs, research, tests, commands, or local evidence they need.
6. Before launching children, reread the prompt. If it contains caller-written
   diagnosis or a caller-selected investigation map that is not in the user's
   ask, delete that material.

## Workflow

1. Start two fresh, resumable child sessions with the same faithful goal brief.
   Give each model the same mode-specific evidence obligations and role
   framing, including the instruction to maximize parallelism by using parallel
   agents and not invoke skills that spawn subagents.
2. Collect independent first passes. Do not let either model see the other's
   answer before it has formed its own view.
3. Send Model A's pass to Model B for critique and simplification. In
   adversarial mode, tell the adversary to look for a more elegant alternate
   architecture and to reject kitchen-sink compromises.
4. Send Model B's critique and proposal back to Model A. Ask Model A to revise,
   concede, or defend with repo evidence.
5. Continue focused rounds until both models either agree or expose a real
   unresolved decision. Most runs should need one to four rounds. Continue when
   a reply is ungrounded, overbuilt, contradictory, or ignores a user
   requirement.
6. Produce a final consensus only from agreed material. If they do not agree,
   report the smallest unresolved choice with each side's evidence and the
   decision the user needs to make.
7. Leave artifact handles in the final response. Do not paste long transcripts.

## Output

Final responses should include:

- the resolved participant mapping
- whether the run converged
- the consensus plan or concept, kept lean
- repo evidence that shaped the result when applicable
- rejected alternatives and why they were rejected
- unresolved decisions, if any
- artifact directory path

## Reference Map

- `workflow-contract.md` - how the parent agent runs the dialogue without a
  deterministic runner
- `prompt-contracts.md` - prompt shapes for first pass, critique, adversarial
  mode, revision, and signoff
- `model-and-invocation.md` - model shorthand resolution, direct Claude/Codex
  invocation, resumable sessions, streaming, and long-run monitoring posture
- `repo-grounding.md` - required repo reading, open-investigation evidence
  discovery, and single-path architecture pressure
- `convergence-and-synthesis.md` - how to tell agreement from accumulation and
  how to report no-consensus outcomes
- `examples.md` - example invocations and operating patterns
