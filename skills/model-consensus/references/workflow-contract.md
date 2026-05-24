# Workflow Contract

`model-consensus` is an agent-run skill. The parent agent executes this
workflow directly. It does not call a dedicated runner script, create a local
controller, or hide the process behind a harness.

The parent agent's job is orchestration only:

- preserve the user's goal and constraints
- ask for missing model choices once
- prepare high-quality prompts
- preserve child discovery freedom when the task is a cross-check or
  investigation
- invoke the two child model sessions directly
- relay the relevant outputs between them
- require evidence when a claim depends on a repo
- identify convergence, non-convergence, or malformed replies
- report the agreed result without adding a third plan of its own

## Operating Principles

- Keep agency at every layer. The parent, Model A, and Model B are all capable
  reasoning agents. Prompts should explain the goal, why the process exists,
  and what good judgment looks like.
- Do not poison the children with the parent's diagnosis. For investigative
  work, the parent names the user's artifact or symptom and the output target;
  the children choose the evidence path.
- The dialogue is not a vote. If one model is right and the other is wrong, the
  work is to make the evidence clear enough that they converge or expose the
  unresolved decision.
- The parent is allowed to interrupt the pattern when the next useful step is
  obvious, such as asking a child to read missing files, tightening a prompt
  after scope drift, or stopping because the models have genuinely agreed.
- Do not mistake mechanical symmetry for rigor. Rounds should be focused and
  purposeful, not automatic alternation.

## Phase 1: Capture The Goal

Keep both forms:

- `raw_goal`: the user's words
- `goal_brief`: a faithful, prompt-authoring-quality restatement

The goal brief may clarify:

- desired output type
- hard requirements
- quality bar
- repo root or artifact paths
- constraints and non-goals
- whether one participant should be adversarial

The goal brief must not introduce the caller's diagnosis or investigation map.
It should preserve the user's ask, exact user-named inputs, hard constraints,
desired output, and participant choices.

## Phase 2: Resolve Participants

Resolve two participant blocks:

```text
participant_a: runtime, model, effort, role
participant_b: runtime, model, effort, role
```

The default roles are `collaborator` and `collaborator`. If the user asks for
adversarial mode, set one role to `adversary`. The adversary is not hostile; it
is responsible for simpler alternatives, counterarguments, failure modes, and
resisting bloated compromise.

If runtime, model, or effort is missing or ambiguous, ask one consolidated
question before invoking external models. Model choices affect cost, latency,
and answer quality, so do not invent hidden defaults.

## Phase 3: Create Artifacts

Create a run directory manually, such as:

```text
.arch_skill/model-consensus/<goal-slug>-<UTC timestamp>/
```

Useful files:

```text
goal.md
participants.md
round-01/model-a-prompt.md
round-01/model-a-events.jsonl
round-01/model-a-final.md
round-01/model-b-prompt.md
round-01/model-b-events.jsonl
round-01/model-b-final.md
round-02/...
summary.md
```

This directory is an artifact log, not a controller state store. Do not create
or require a script to manage it.

## Phase 4: Independent First Passes

Start two fresh, resumable sessions. Give both models:

- the raw goal and goal brief
- the participant roles
- repo root and evidence obligations when a repo or workspace is involved
- the instruction: Maximize parallelism by using parallel agents. Do not invoke skills that spawn subagents.
- the quality bar
- the output contract

Do not show either participant the other's first answer until both first passes
are complete. Independent first passes reduce anchoring and make disagreement
useful.

## Phase 5: Dialogue Rounds

Each round should have a concrete purpose:

- critique the other model's plan
- challenge parent or peer framing that evidence does not support
- simplify the architecture
- find a canonical repo path to adopt
- resolve a contradiction
- challenge an unsupported claim
- produce final signoff

Use resumable child sessions so each model can carry its own reasoning history.
The parent relays the relevant other-model material into each resume prompt.

Stop early when both models agree on the same lean answer and have satisfied
the repo-grounding obligations. Continue when either model:

- ignores a hard user requirement
- proposes a new path without checking existing owners
- accumulates every idea instead of simplifying
- gives no file evidence for repo claims
- agrees only superficially while retaining incompatible assumptions

## Phase 6: Final Synthesis

The parent writes the final response from child-agreed material only. It may
organize and compress the result, but it must not invent an unreviewed third
architecture.

If the models do not converge, say so. A useful no-consensus result names the
smallest unresolved choice, the evidence each side used, and what decision
would unblock the work.

## Long-Running Work

Architectural and repo-grounded rounds can take real time. A normal child round
often takes 5+ minutes; broad repo reads, `xhigh`, or `max` can reasonably take
20-40 minutes. Choose the execution posture deliberately:

- Use foreground execution for short prompts where blocking keeps the flow
  simple.
- Use background shell processes for long repo-reading rounds, but preserve
  live event streams and inspect them on a minutes-scale cadence.
- Do not call a child hung only because no final file exists after a few
  minutes. Look for process liveness, stream activity, tool calls, thinking
  traces where available, and stderr errors.
- For long background waits, poll every few minutes by default. A 60 second
  floor is reasonable for active monitoring; multi-minute cadence is better
  when the streams show life. Avoid tight two-second polling.
- Treat "no stream events, no tool calls, no stderr movement, and no CPU/process
  activity for several minutes after an already generous floor" as a reason to
  investigate, not as automatic proof of a hung model.
