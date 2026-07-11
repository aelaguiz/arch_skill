# Examples

## Collaborative Architecture Plan

User:

```text
Use $model-consensus with Claude Opus 4.7 xhigh and Codex gpt-5.6-sol xhigh to
find the simplest architecture for making this repo's planner resumable.
```

Parent behavior:

- resolve and announce both model mappings
- inspect the active host and resolve transport independently: a same-host
  participant uses a clean native child only if native model selection can
  honor the requested model; the cross-provider or unavailable exact-model
  participant uses an external session
- use `fork_turns: "none"` for each new Codex-native participant, or a clean
  named/custom subagent for each new Claude-native participant
- create `.arch_skill/model-consensus/resumable-planner-<timestamp>/`
- prompt both models to start from the user's target and identify the repo
  instructions, owner files, existing patterns, and proof surfaces they need
- collect independent first passes
- relay critiques through the parent, resuming each exact participant until
  both sign off or expose the smallest unresolved decision

## Adversarial Simplification

User:

```text
Use $model-consensus. Put Codex gpt-5.6-sol xhigh in adversarial mode against
Claude Fable 5 high. The goal is the most elegant plan for removing the
duplicate install path without breaking existing users.
```

Parent behavior:

- assign Claude as collaborator and Codex as adversary unless the user says
  otherwise
- resolve transport per participant rather than forcing both through external
  CLIs; keep separate clean first passes and exact handles
- tell the adversary to find simpler alternatives and resist kitchen-sink
  compromise
- require both models to identify the install owners, docs, and verification
  surfaces that decide the answer
- stop when both agree on one retirement path or report the unresolved
  compatibility decision

## Open Root-Cause Cross-Check

User:

```text
Have $model-consensus gpt-5.6-sol xhigh and Opus 4.7 max review everything we did
for docs/FAILURE_PLAN.md and start a new doc with every theory for why this
path is producing uniform results. I want them to read everything, including
the research, and build fast traps to prove where the bug starts.
```

- resolves and announces the model mappings
- resolves native or external transport independently for both participants
- records the raw goal, the named doc path, repo root, desired new docs output,
  hard constraints, and any user-stated non-goals
- tells both models to start from the named doc, then independently choose the
  code, docs, papers, tests, commands, and history they need
- asks for theories, evidence, falsifiers, and fast traps only after the models
  have done their own reading
- sends each first pass to the other model for critique, then converges only on
  theories and proof plans both models can defend from evidence, always
  resuming the exact participant through the parent relay
- keeps participants read-only; after convergence, the parent writes only the
  agreed material to the requested new document and asks both exact
  participants to sign off if the written synthesis could change meaning

## Conceptual Non-Repo Run

User:

```text
Use $model-consensus with two models of your choice? Actually ask me first. I
want them to think through whether this product should be local-first.
```

Parent behavior:

- ask one model-choice question because the user requested it
- choose transport after the participant choices are known; same-host native
  children are the default when their model capability suffices
- build a goal brief with product constraints and non-goals
- omit repo-grounding obligations unless the user provides a repo or artifact
- use the same dialogue pattern, but judge evidence by product goals and
  tradeoffs rather than `path:line` citations

## Bad Outcome To Avoid

Do not produce:

```text
The final plan includes Model A's plugin architecture, Model B's event bus, a
new config system, adapter layers, a migration engine, and three future
extensions.
```

That is accumulation, not consensus. Send it back through a simplification
round:

```text
Both proposals currently add multiple new pathways. Re-read the existing owner
paths and produce the smallest design that satisfies the hard requirements.
Name which proposed pieces are unnecessary and why.
```

Also do not produce a "consensus" run where the parent gave both models the
same detailed theory map before either model investigated. That is anchoring,
not cross-checking. Repair it by restarting with a shorter prompt that preserves
the raw goal, user-named inputs, constraints, and discovery freedom.

Do not put two same-host participants into a peer team merely because the host
offers teams. Parent relay is the default. A team is appropriate only when the
user genuinely wants direct participant messaging and that topology serves the
method.
