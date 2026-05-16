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
- the child should stop or ask for missing information instead of guessing

## Goal Brief Contract

Use prompt-authoring discipline to create the goal brief.

Required sections:

```text
Raw Goal
Resolved Participants
User-Named Inputs
Desired Output
Hard Constraints
Success Criteria
Non-Goals
Discovery Freedom
```

Rules:

- Preserve user language where it carries intent.
- Clarify ambiguity without choosing an implementation.
- Do not add a solution, library, pattern, path, hypothesis, failure-layer
  taxonomy, ranked theory, or diagnostic question that the user did not name.
- `User-Named Inputs` means artifacts the user explicitly gave, plus exact
  path resolution needed to open those artifacts. It is not a parent-selected
  reading list.
- `Discovery Freedom` must tell child models that they may choose the evidence
  surface they need and reject the parent framing if evidence points elsewhere.
- Keep the brief short enough to reuse in every child prompt.

## Contamination Check

Before launching child sessions, read the prompt and ask:

- Did I add a hypothesis the user did not state?
- Did I tell the models where the cause probably lives?
- Did I turn user intent into a taxonomy?
- Did I require files that the children should choose for themselves?
- Could this prompt make both models agree with me instead of each other?

If yes, remove that material or mark it only as a user-named input when the user
actually named it.

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

Authoritative Inputs
- Raw goal: <raw_goal>
- Faithful goal brief: <goal_brief>
- Your role: <collaborator|adversary>
- Prompt mode: <open investigation|architecture plan|concept>
- Work root: <path or none>
- Explicit user constraints: <constraints>

Evidence Grounding
If a work root is provided, read real evidence before proposing or agreeing.
Start with user-named artifacts, then independently choose the code, docs,
research, tests, commands, or other local evidence needed for the goal. Cite
paths, and use line numbers when exact evidence matters. Do not limit yourself
to the parent brief if a better evidence trail appears.

Quality Bar
Prefer the smallest answer that satisfies every hard requirement and survives
evidence. Reject kitchen-sink compromise. If this is an investigation, separate
evidence-backed theories from guesses and name fast falsifiers. If this is an
architecture plan, reuse existing pathways when possible and justify any new
path from repo evidence.

Output Contract
Return:
- concise proposed answer or plan
- evidence read, if applicable
- existing paths/patterns to adopt, if applicable
- alternatives rejected and why
- risks or open questions
- what you would need from the other model to converge

Stop Instead Of Continuing If
- the goal is missing a critical decision
- the requested model role is unclear
- repo access is required but unavailable
- you cannot substantiate repo claims from files
```

## Architecture Prompt Add-On

Use this only when the prompt mode is architecture or implementation planning:

```text
Architecture Grounding
Identify canonical owner paths, patterns to adopt, parallel or drifting
implementations, tests or proof surfaces, and the smallest place this work
should live. The goal is to minimize new pathways and converge on one way of
doing the work where possible. If you propose a new path, explain why the
existing path cannot absorb the requirement.
```

## Open Investigation Prompt Add-On

Use this when the user wants a cross-check, root-cause investigation,
failure-analysis plan, broad review, or second-opinion dialogue:

```text
Open Investigation Grounding
Do not assume the parent has identified the right files, layers, theories, or
failure categories. Start from the user-named artifact or symptom, then choose
your own evidence path through code, docs, research, tests, command output, and
local history as needed. Your first pass should report what you inspected, what
you ruled out, what remains plausible, and the fastest evidence that would
separate the plausible explanations.
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

Output Contract
Return:
- agreements
- disagreements
- simplifications you recommend
- repo evidence that decides the disagreement
- revised proposal
- whether you are ready to sign off
```

## Adversarial Prompt Add-On

Use this when the user asks for adversarial mode or when one model is assigned
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
```

Do not call the result consensus if either model refuses signoff on a material
point.
