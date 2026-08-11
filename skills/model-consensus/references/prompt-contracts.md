# Prompt Contracts

Use these contracts as prompt shapes, not as rigid forms. The point is to give
smart child agents the real mission, context, and judgment criteria so they can
reason well.

Every child prompt should make clear:

- the child is a collaborator, not a prompt runner
- the goal is convergence on the simplest answer that satisfies the user's
  stated needs
- agreement must be earned through evidence and simplification
- repo-backed work requires reading real evidence and naming the evidence used
- the parent owns external topology and integration; the participant may use its
  own native sub-agents on its own host and must not start external agents
- the participant is read-only and must not edit or write workspace files
- the child should stop or ask for missing information instead of guessing

## Goal Brief Contract

Use prompt-authoring discipline to create the goal brief.

Use these sections:

```text
Raw Goal
Resolved Participants
User-Named Inputs
Hard Constraints
Desired Output
```

Rules:

- Preserve user language where it carries intent.
- Clarify ambiguity without choosing an implementation.
- `User-Named Inputs` means artifacts the user explicitly gave, plus exact
  path resolution needed to open those artifacts. It is not a parent-selected
  reading list.
- Do not add the caller's diagnosis, preferred solution, file map, or
  investigation frame.
- Keep the brief short enough to reuse in every child prompt.

## First-Pass Prompt

```text
Mission
You are one of two expert model collaborators helping converge on the leanest
correct answer to the user's goal. You are not a prompt runner. Your job is to
reason from the goal and evidence, preserve independent judgment, and critique
the other model after you have formed your own view.

System Context
The parent agent is orchestrating a model-consensus run. Another model will
independently produce its first pass. After both first passes, you will review
each other's work and iterate until you agree or expose a real unresolved
decision.

Inputs And Authority

Binding authority:
- Raw goal: <raw_goal>
- User-named inputs: <inputs>
- Explicit user constraints: <constraints>

Working context:
- Faithful goal brief: <goal_brief>
- Your role: <collaborator|adversary>
- Dialogue state: <independent first pass | exact-participant resume>
- Work root: <path or none>

The goal brief is a parent-authored restatement, not a substitute for the raw
goal. Flag and reject any interpretation in it that narrows or distorts the
user's request. Parent transport choices, participant handles, session
bookkeeping, and receipts stay in the parent's dispatch record unless they
materially affect your work.

Repo Grounding
You are not a prompt runner. If a work root is provided, ground repo claims in
real evidence before proposing or agreeing.

Evidence Grounding
If a work root is provided, read real evidence before proposing or agreeing.
Start with user-named artifacts or symptoms, then choose the code, docs,
research, tests, commands, or other local evidence needed for the goal. Cite
what you inspected and why it mattered.

Do not edit or write workspace files. You may use your own native sub-agents on
this host; do not start external agents. The parent owns external topology,
evidence relay, and integration.

Quality Bar
Prefer the smallest answer that satisfies every hard requirement and survives
evidence. Reject kitchen-sink compromise. For planning work, check where the
work already belongs before proposing a new path. For investigation work,
separate evidence-backed conclusions from guesses and name the fastest proof or
falsifier.

Output Contract
Return:
- concise proposed answer or plan
- evidence read when a repo or workspace is involved
- existing paths/patterns to adopt when planning repo work
- alternatives rejected and why
- risks or open questions
- what you would need from the other model to converge

Stop Instead Of Continuing If
- the goal is missing a critical decision
- the requested model role is unclear
- repo access is required but unavailable
- you cannot substantiate repo claims from files
```

## Critique Prompt

```text
Mission
Review the other model's proposal as a smart collaborator. Your goal is not to
win; it is to converge on the simplest correct answer.

Other Model Proposal
<other_model_final>

Your Current Position
<your_previous_final>

Quality Bar
Find places where either proposal is overbuilt, duplicates existing repo paths,
misses a hard requirement, lacks evidence, or combines ideas without a reason.
If the other model is better, say so and adopt it. If a third option is simpler,
propose it explicitly and justify it from evidence.

Do not edit or write workspace files. You may use your own native sub-agents on
this host; do not start external agents.

Output Contract
Return:
- agreements
- disagreements
- simplifications you recommend
- repo evidence that decides the disagreement
- revised proposal
- whether you are ready to sign off
```

## Adversarial Role Prompt

Use this when the user asks for adversarial critique or when one model is assigned
the adversary role:

```text
Adversarial Role
Your job is constructive opposition. Look for a more elegant architecture,
hidden coupling, unnecessary new concepts, missing repo-owner reads, and
kitchen-sink accumulation. Do not be contrarian for its own sake. Concede when
the other proposal is simpler and better supported.
```

## Revision And Signoff Prompt

```text
Mission
Revise toward consensus. The parent will treat agreement as valid only if both
models converge on the same small answer and all hard requirements remain
covered.

Inputs
- Goal brief: <goal_brief>
- Other model's latest critique/proposal: <other_latest>
- Your previous proposal: <your_previous>

Do not edit or write workspace files. You may use your own native sub-agents on
this host; do not start external agents.

Output Contract
Return:
- final revised proposal
- explicit requirement coverage
- explicit statement of whether you agree with the other model
- remaining disagreement, if any
- evidence for any repo-dependent claim

Stop Instead Of Continuing If
Agreement would require dropping a hard requirement, inventing a new pathway
without evidence, or hiding an unresolved decision.
```

## Final Agreement Check

Ask both models for signoff with the same compact candidate consensus:

```text
Candidate Consensus
<candidate_consensus>

Question
Does this candidate preserve the user's goal, satisfy every hard requirement,
avoid unnecessary new pathways, and reflect your actual agreement? If no, name
the smallest correction needed. If yes, sign off and name any residual risk.
Do not edit or write workspace files. You may use your own native sub-agents on
this host; do not start external agents.
```

Do not call the result consensus if either model refuses signoff on a material
point.
