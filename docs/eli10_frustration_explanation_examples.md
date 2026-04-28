# ELI10 Frustration-Prevention Explanation Examples

This doc is the stronger example set for `eli10`.

It is authoring evidence, not runtime memory.

It focuses on the moments where the assistant caused frustration by explaining
the wrong thing, explaining at the wrong level, or turning an explanation into
unsolicited instructions.

The shipped skill cannot know these old chats. It should not pretend it has
personal history, hidden context, or a memory of prior failures. These examples
only teach the reply contract: how to choose the right explanation level from
the current conversation, how to keep the language simple, and when to stop.

The central rule:

> When the user asks for an explanation, explain. Do not append next steps,
> implementation advice, or a plan unless the user asked for that.

Good `eli10` explanation is not "shorter answer." It is:

- the right level of cause
- the real system behavior
- the plain-English mechanism
- no path wall
- no citation wall
- no invented workflow
- no hidden action agenda
- no fake memory of prior conversations

## Runtime Boundary

At runtime, `eli10` should behave like a style and clarity contract:

- Use only the current conversation and any files or artifacts the agent has
  actually inspected.
- Do not say "this is like the time you..." unless that context is present in
  the current thread.
- Do not imply the skill remembers the user's saved chats.
- Do not diagnose the user's personality or preferences as facts.
- Do explain the current issue in the shape that tends to work for this user:
  direct cause, simple mechanism, root cause, and a compact net.

## Best Explanation Shape

Use this shape when the user asks "why?", "what happened?", "what does this
mean?", or "why did this not work?"

```text
<direct cause in one sentence>

✅ What this is really about:
<the system-level question, not the surface symptom>

⚠️ Why the earlier answer was frustrating:
<what it focused on instead>

Better explanation:
<plain-English mechanism, with exact terms preserved>

Net: <one sentence that compresses the root cause>
```

Use `What this is really about` when the current wording clearly points to a
larger system question. If the user is only asking a narrow fact question, skip
that section and answer the fact directly.

No `Next:` section. No `Fix:` section. If the user wants next steps, they will
ask.

## Pattern 1: Symptom Versus Root Cause

Frustration signal:

> "Why does it think it's blocked? The Android simulator is starting. What is
> its problem? Answer me in simple terms."

What the bad answer did:

- Talked about the Android simulator as if the simulator itself was broken.
- Repeated the visible symptom.
- Failed to explain the agent's internal success condition.

Why that missed:

The question was not "is Android open?" The question was "what condition is the
worker checking that makes it believe Android is still unavailable?"

Best-case `eli10` explanation:

```text
It did not think Android was missing. It thought its own readiness check had
not passed.

✅ What this is really about:
Why does the worker keep restarting something that is visibly already open?

⚠️ Why the earlier answer was frustrating:
It explained the simulator symptom instead of the worker's belief system.

Better explanation:
The worker likely had a check like "wait until the simulator is booted and
reachable." macOS showed the simulator window, but the worker did not see the
specific ready signal it expected. So it kept treating the environment as not
ready, even though you could see the simulator launching.

Net: the visible symptom was Android popping up; the root cause was a mismatch
between what macOS showed and what the worker's readiness check accepted.
```

## Pattern 2: Myopic Evidence Versus System Failure

Frustration signal:

> "The gameplay card source was an example of the bigger problem. Did you focus
> on the cards or did you focus on the bigger problem?"

What the bad answer did:

- Treated the card issue as the whole bug.
- Focused on one artifact.
- Missed the larger loop failure.

Why that missed:

The user was using the card as evidence of a system-level failure: the loop was
not using the right skills, not inspecting the real UI, and not judging quality
from the user's actual screen experience.

Best-case `eli10` explanation:

```text
The card issue was just the visible clue. The real problem was the build loop's
quality model.

✅ What this is really about:
Is the loop using the right design process, or is it inventing output and then
grading itself too lightly?

⚠️ Why the earlier answer was frustrating:
It zoomed into the card instead of explaining what the card proved about the
system.

Better explanation:
The loop was treating "I produced something" as too close to "the product is
good." It needed to inspect device-level output and use the intended design
skills. Instead, it accepted local artifacts and receipts as proof. The card
mistake mattered because it exposed that deeper weakness.

Net: the card was not the root cause; it was evidence that the loop's quality
check was too shallow.
```

## Pattern 3: System Question Versus One Broken Case

Frustration signal:

> "Rally doesn't exist. How is this working at all? Put stepwise aside. What
> did that MCP hint do?"

What the bad answer did:

- Explained the immediate broken run.
- Treated Stepwise as the whole frame.
- Did not explain the system path that made the impossible thing appear to
work.

Why that missed:

The user was not asking how to continue the run. The user was asking how a
nonexistent integration could have appeared in the system's reasoning path.

Best-case `eli10` explanation:

```text
The MCP hint did not prove Rally was actually wired. It only gave the agent a
reason to believe Rally might be available.

✅ What this is really about:
How did the system reach for a path that should not exist?

⚠️ Why the earlier answer was frustrating:
It stayed inside the failing Stepwise run instead of explaining the broader
source of belief.

Better explanation:
The agent saw a hint that looked like a capability signal. Because the hint was
present, it treated the missing Rally surface as something it might be able to
use. That is different from the integration actually existing. The real failure
is a stale or misleading capability cue.

Net: the hint created a false belief; it was not evidence that Rally worked.
```

## Pattern 4: Over-Interpreting A Simple Ask

Frustration signal:

> "I just want a single easy command. Should I do it at phase one or phase two?
> How can I get ten thousand accepted samples?"

What the bad answer did:

- Answered with phase architecture.
- Made the user reason about internal pipeline boundaries.
- Added conceptual load instead of explaining the user-facing interface.

Why that missed:

The user was not asking for a theory of the pipeline. The user was saying the
pipeline had leaked too much internal machinery.

Best-case `eli10` explanation:

```text
The problem is that the workflow is exposing internal phases as user decisions.

✅ What this is really about:
Why do I have to know where this belongs? Why is there not one obvious command?

⚠️ Why the earlier answer was frustrating:
It explained phase ownership instead of explaining the interface failure.

Better explanation:
Phase one and phase two may be real internally, but they should not both be
things you have to think about for a normal sample run. If the goal is "give me
10,000 accepted samples," the system should hide the handoff and make the
operator intent clear.

Net: the root issue was not phase placement; it was that internal pipeline
structure leaked into the user experience.
```

## Pattern 5: Direct Files Versus Tool Theater

Frustration signal:

> "Why are you using MCP? This is files on disk."

What the bad answer did:

- Treated MCP as the natural starting point.
- Ignored the obvious local truth source.
- Explained tool usage instead of explaining why the tool was unnecessary.

Why that missed:

The user was pointing at a source-of-truth error: the files were present
locally, so extra tool mediation made the answer feel disconnected from the
actual workspace.

Best-case `eli10` explanation:

```text
The MCP was the wrong layer for that question.

✅ What this is really about:
Why did I reach for an integration when the truth was already on disk?

⚠️ Why the earlier answer was frustrating:
It made the task feel remote and abstract even though the files were local.

Better explanation:
The local checkout was the source of truth. MCP could only add distance unless
the local files were unavailable or incomplete. Using it first made the answer
look like it was avoiding the obvious evidence.

Net: the failure was tool-layer substitution: using an integration where direct
file inspection was the plain source of truth.
```

## Pattern 6: Known Incomplete Work Versus Real Defect

Frustration signal:

> "You keep saying the same thing. If the shipped language is not built, that's
> not a useful observation. Which of these are real issues in that context?"

What the bad answer did:

- Repeated "not built yet" as if it were a new finding.
- Mixed expected incompleteness with actual design problems.
- Used citations instead of a severity model.

Why that missed:

The user already knew some pieces were not built. The explanation needed to
separate boring incompleteness from defects that would still matter after the
missing work was built.

Best-case `eli10` explanation:

```text
There are two different categories, and only one is useful right now.

✅ Expected incompleteness:
Some shipped language is missing because that part is not built yet. That is
not a meaningful finding by itself.

⚠️ Real issue:
A real issue is something that would still be wrong even after the missing
language exists. For example: duplicate ownership, contradictory source truth,
or a prompt that points agents at the wrong surface.

Better explanation:
The audit should not count "not implemented" as a defect when everyone already
knows it is not implemented. It should only flag problems that reveal bad
structure, wrong ownership, stale guidance, or a gap between the intended model
and the live model.

Net: "not built yet" is status; "built around the wrong owner" is a real issue.
```

## Pattern 7: Citation Wall Blocking The Explanation

Frustration signal:

> "Say this simply without all the citations so I can't read it."

What the bad answer did:

- Led with source references.
- Made the user assemble the meaning from evidence.
- Treated audit proof as the explanation.

Why that missed:

The user was not rejecting evidence. The user was rejecting evidence-first
presentation.

Best-case `eli10` explanation:

```text
The answer had the right evidence in the wrong order.

✅ What this is really about:
What is the point, in plain English, before I look at proof?

⚠️ Why the earlier answer was frustrating:
The citations forced you to parse the evidence before you knew the conclusion.

Better explanation:
Evidence should support the explanation, not replace it. The readable answer
should say the finding first, then mention proof only after the idea is clear.

Net: proof belongs after meaning unless the user specifically asks for a
source-first audit.
```

## Pattern 8: File Path Wall Blocking The Concept

Frustration signal:

> "Say that again in simple terms without all the file names making it hard to
> read."

What the bad answer did:

- Put file paths inside the main explanation.
- Made every sentence look like a citation.
- Hid the concept under exact locations.

Why that missed:

The user needed the concept. The paths were only proof.

Best-case `eli10` explanation:

```text
The answer confused "where I found it" with "what it means."

✅ What this is really about:
What is the actual system problem, without making me decode paths?

⚠️ Why the earlier answer was frustrating:
The file names became noise before the main idea was clear.

Better explanation:
The plain explanation should name the broken contract first. File paths matter
only after that, when the user wants proof or wants to edit the exact surface.

Net: paths are evidence; they are not the explanation.
```

## Pattern 9: Overbuild Versus Best Work

Frustration signal:

> "What makes you think I want the minimum? I don't like minimum, I like best.
> Do what I asked and don't insert your own opinion."

What the bad answer did:

- Interpreted "don't overbuild" as "do the minimum."
- Treated simplicity as a lower quality bar.
- Added its own preference for smallest possible scope.

Why that missed:

The user was not asking for weaker work. The user was asking for work that
serves the goal without invented extras.

Best-case `eli10` explanation:

```text
"Do not overbuild" does not mean "do the least possible work."

✅ What this is really about:
Build the best version of the requested thing, without adding unrelated
machinery.

⚠️ Why the earlier answer was frustrating:
It turned your anti-scope-creep rule into a preference for minimalism.

Better explanation:
There are two different axes. Quality should be high. Scope should be faithful.
The bad behavior is not "doing too much work"; it is doing work that does not
serve the asked-for outcome.

Net: best is good; invented extras are bad.
```

## Pattern 10: Prompt Skill Versus Harness Instinct

Frustration signal:

> "Skills need way more push to be simple by default. They are being built with
> harness scripts when almost always they should be simple prompt engineering."

What the bad answer did:

- Treated "skill" as a software package first.
- Added scripts, validators, and parameters before proving prose was
  insufficient.
- Specialized around one incident.

Why that missed:

The system was mistaking reusable judgment for deterministic orchestration.

Best-case `eli10` explanation:

```text
The failure is mechanism choice.

✅ What this is really about:
Why do skill authors keep turning natural-language workflows into little
software systems?

⚠️ Why the earlier answer was frustrating:
It treated a skill like a harness by default, even when the job was better
handled as prompt guidance.

Better explanation:
A skill should usually be the prompt the user no longer wants to repeat. It
should teach the agent how to reason about the task. Scripts only make sense
when the same deterministic check keeps failing or exact validation is the real
job.

Net: most skill failures here came from choosing machinery before exhausting
plain prompt guidance.
```

## Pattern 11: Regression Archaeology Versus New Design

Frustration signal:

> "Are you inventing when you could just look at how it worked before by
> looking at the diff?"

What the bad answer did:

- Designed a fresh solution.
- Ignored the old working behavior.
- Treated the current state as greenfield.

Why that missed:

The user was asking for root-cause recovery. The relevant question was "what
changed from the working version?"

Best-case `eli10` explanation:

```text
This was a regression question, not a design question.

✅ What this is really about:
What did we change that broke the old behavior?

⚠️ Why the earlier answer was frustrating:
It invented a replacement instead of explaining the difference between the
working version and the broken version.

Better explanation:
When something used to work, the first explanation should be based on the diff.
The likely cause is the change that removed, bypassed, or contradicted the old
path. New design ideas are secondary until that history is understood.

Net: the root cause lives in the change from working to broken, not in a fresh
architecture sketch.
```

## Pattern 12: General System Ask Versus Narrow Use Case

Frustration signal:

> "You turned it into only an arch skill closeout thing. That's one way it can
> be used. The point is I can just run this in a repo."

What the bad answer did:

- Anchored on one visible use case.
- Scoped a general workflow to a narrow context.
- Explained the special case as if it were the whole system.

Why that missed:

The user was asking about the general operating model. The special case was
only one mode.

Best-case `eli10` explanation:

```text
The mistake was treating one use case as the whole product.

✅ What this is really about:
What is this workflow in general, outside the arch-plan case?

⚠️ Why the earlier answer was frustrating:
It explained the arch-closeout path and made that sound like the required
entrypoint.

Better explanation:
The workflow has a general job: run in a repo, inspect the docs, and improve
documentation according to the process. If an arch plan is present, it can add
context. But the arch plan is not the identity of the workflow.

Net: arch closeout is a context, not the core definition.
```

## Pattern 13: Jargon Term Introduced Without Meaning

Frustration signal:

> "What the fuck is a capability?"

What the bad answer did:

- Introduced an abstract term.
- Used the term as if its meaning were obvious.
- Made the user argue with the abstraction instead of the underlying idea.

Why that missed:

The term became an extra concept the user had to decode before understanding
the answer.

Best-case `eli10` explanation:

```text
The word "capability" was doing too much work.

✅ What this is really about:
What concrete thing did that label refer to?

⚠️ Why the earlier answer was frustrating:
It introduced a new abstraction without explaining what it bought us.

Better explanation:
In that answer, "capability" meant "a behavior the agent or runtime can
perform." But the word was too broad. If the real topic was Git history
descriptions, the explanation should have said that directly instead of
creating a new rail called capability.

Net: unexplained abstractions make the answer feel invented, even when the
underlying idea is simple.
```

## Pattern 14: Symptom Repair Versus Ownership Boundary

Frustration signal:

> "Did you modify Doctrine to do this pathing support? I make Doctrine changes,
> not you."

What the bad answer did:

- Solved a caller-side problem by editing a dependency.
- Treated the immediate technical blockage as permission to cross ownership.
- Did not explain the boundary.

Why that missed:

The user was focused on who owns the change, not only whether the path worked.

Best-case `eli10` explanation:

```text
The root issue was ownership, not pathing.

✅ What this is really about:
Why did the fix cross into a repo that this task did not own?

⚠️ Why the earlier answer was frustrating:
It treated a dependency edit as a technical shortcut instead of an ownership
violation.

Better explanation:
This repo can change how it calls or describes Doctrine behavior. It should not
change Doctrine itself unless that is explicitly part of the task. A working
patch in the wrong repo is still the wrong fix.

Net: the bug symptom was pathing; the real failure was crossing the owner
boundary.
```

## Pattern 15: Explanation Versus Instructions

Frustration signal:

> "I like my explanations to be explanations without telling me what to do.
> When I want to know next steps I'll ask."

What the bad answer did:

- Answered "why" and then added a plan.
- Turned diagnosis into instructions.
- Made the user fight extra advice instead of absorbing the explanation.

Why that missed:

An explanation and a next-step plan are different speech acts.

Best-case `eli10` explanation:

```text
The earlier answer mixed two jobs: explaining the cause and proposing action.

✅ What this is really about:
What happened, and why did the system behave that way?

⚠️ Why the earlier answer was frustrating:
The action tail made the answer feel like it was steering you instead of
explaining the system.

Better explanation:
For an explanation request, the answer should stop once the mechanism is clear.
It can name the root cause, the system belief, and the mismatch. It should not
add implementation steps unless the user asks for them.

Net: explain the system first; wait for the user to ask for action.
```

## Pattern 16: Repeated Known Issue Versus New Signal

Frustration signal:

> "You keep saying one over and over again."

What the bad answer did:

- Repeated a known issue.
- Failed to distinguish stale notes from new evidence.
- Made the audit feel like it was not learning.

Why that missed:

The user was asking for signal after accounting for known baseline defects.

Best-case `eli10` explanation:

```text
Repeating the known issue was not useful signal.

✅ What this is really about:
After ignoring the already-known gap, what is still actually wrong?

⚠️ Why the earlier answer was frustrating:
It treated a known baseline condition as a fresh finding.

Better explanation:
An audit should subtract known context before judging what remains. If the
language is known to be unbuilt, "language is missing" is not a finding. A real
finding would be something like "the plan says this is built" or "the missing
language causes the wrong owner to run."

Net: a repeated known gap is noise unless it contradicts the current claim.
```

## Pattern 17: Bad Question Form

Frustration signal:

> "Ask this in plain English. I don't know what you're actually asking."

What the bad answer did:

- Asked a decision in internal terms.
- Used labels from the implementation instead of the user's mental model.
- Made the question harder than the decision.

Why that missed:

The user was not refusing to decide. The question was badly framed.

Best-case `eli10` explanation:

```text
The question was phrased in system language, not user language.

✅ What this is really about:
What decision am I actually being asked to make?

⚠️ Why the earlier answer was frustrating:
It used internal labels before explaining the choice.

Better explanation:
A good question says the real-world choice first. The implementation names can
come after, in parentheses, if they are needed at all.

Net: if the user cannot restate the choice, the question is not plain enough.
```

## Pattern 18: "What It Does Today" Versus Future System Design

Frustration signal:

> "I know what it does today. I'm talking about if we work on Rally."

What the bad answer did:

- Answered current-state behavior.
- Missed that the user was asking a future-system design question.
- Treated "what exists now" as the entire answer.

Why that missed:

The user was asking about the implication of future work, not requesting a
current-state inventory.

Best-case `eli10` explanation:

```text
The question was about the future system, not today's behavior.

✅ What this is really about:
If Rally becomes part of this system, how should the pieces relate?

⚠️ Why the earlier answer was frustrating:
It answered "what does Rally do today?" even though you already knew today's
state.

Better explanation:
Current behavior is only background. The real explanation should describe the
future ownership model: which layer should own conventions, which layer should
compile or enforce them, and which parts should remain outside Rally.

Net: the root question was design direction, not current capability.
```

## Pattern 19: Confusing New Concept

Frustration signal:

> "Why did you introduce section? We have workflow. How is section different
> from workflow?"

What the bad answer did:

- Added a new noun.
- Did not define how it differed from the existing noun.
- Increased the conceptual model without justification.

Why that missed:

The user was checking whether the concept was real or accidental.

Best-case `eli10` explanation:

```text
The new word created a second concept without proving it was different.

✅ What this is really about:
Is "section" a real new layer, or did the answer accidentally rename part of
"workflow"?

⚠️ Why the earlier answer was frustrating:
It made the model bigger before explaining the boundary.

Better explanation:
If "section" and "workflow" mean the same thing, only one term should exist. If
they differ, the answer must say the difference in one sentence. Without that
difference, the new term is just conceptual noise.

Net: a new noun needs a new job; otherwise it should not be there.
```

## Pattern 20: Same Bug Repeating

Frustration signal:

> "Same bug you always do. The 'vs winner' fields always fail because they
> aren't in bootstrap."

What the bad answer did:

- Treated the failure as a one-off incident.
- Did not explain the recurring mechanism.
- Focused on patching the run rather than describing the repeated pattern.

Why that missed:

The user was pointing at a systemic prompt/data-shape mismatch.

Best-case `eli10` explanation:

```text
This is the same shape bug repeating.

✅ What this is really about:
Why does this class of field keep failing across runs?

⚠️ Why the earlier answer was frustrating:
It treated the run as isolated instead of explaining the recurring source of
the error.

Better explanation:
The worker expects fields that are not present in the bootstrap data. So every
time the prompt asks for "vs winner" evidence before that data exists, the
agent either guesses, emits blanks, or fails validation. The bug is not the
latest value. The bug is asking for a field before the prompt has supplied the
source for it.

Net: recurring failures usually mean the prompt contract asks for information
the input does not contain.
```

## Skill Lessons From These Examples

These are the rules the `eli10` skill should encode from the frustration
patterns. The skill should teach the response style, not carry the history:

- Explanation requests should not grow action tails.
- The first sentence should answer the user's actual "why."
- The answer should identify the system belief that caused the behavior.
- The explanation should separate symptom, mechanism, and root cause.
- If the user gives an example, check whether it is evidence of a wider
  system failure.
- Do not answer a future-system question with only current-state facts.
- Do not answer a system question with only the nearest broken artifact.
- Do not introduce a new noun unless it has a distinct job.
- Do not use paths or citations as the main explanation.
- Do not interpret "avoid overbuild" as "do minimum-quality work."
- Do not turn prompt guidance into scripts or harnesses by default.
- Do not ask the user to decode internal labels.
- Do not repeat known baseline gaps as fresh findings.
- Do not pretend to remember old chats. The examples are authoring evidence
  for the skill author, not facts available to the runtime agent.

Net: `eli10` should prevent frustration by explaining the right layer of the
system in plain English, then stopping there.
