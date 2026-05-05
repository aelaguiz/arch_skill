# ELI10 Response Patterns

This is the runtime example library for `eli10`.

Use these examples to choose a clear answer shape and to learn the reasoning
behind it. Do not copy them as rigid templates. Do not claim hidden memory of
prior chats or saved preferences.

## Style Key

Use the marker meanings from `../SKILL.md`. This reference shows answer shapes;
it does not own the marker contract.

## How To Use These Patterns

For each answer, decide what the reader is struggling with:

- buried point
- symptom explained instead of root cause
- dense phrase or noun stack
- undefined jargon
- path or citation wall
- table that hides meaning
- unsolicited action tail
- over-simplification that deletes the hard part

Then apply the smallest pattern that removes that reader tax.

## Core Shapes

### Explanation Only

Use when the user asks "why?", "what happened?", "what does this mean?", or
"why did this not work?"

```text
<direct cause in one or two sentences>

✅ What this is really about:
<the system-level question, if the current wording points past the surface symptom>

🧠 Mechanism:
<how the system got there in plain English>

⚠️ Why it matters:
<what breaks, what becomes confusing, or what risk this creates>

Net: <one sentence that compresses the root cause>
```

No `🔧 Fix:` and no `➡️ Next:` unless the user asked for action.

### Action Requested

Use when the user asks for a plan, implementation, repair, or next steps. If
the user has already approved the direction, this means doing the work, not
restating the plan.

```text
<direct answer or chosen direction>

✅ Keep:
<what remains true or should stay>

🔧 Change:
<the concrete action>

⚠️ Watch:
<the risk or constraint>

Net: <one-line synthesis>
```

### Review Or Audit

Use when the user asks for review.

```text
Finding: <plain-English issue>

⚠️ Why it matters:
<what breaks, what the user sees, or what becomes misleading>

🧠 Mechanism:
<how the bug or confusion happens>

Proof:
<short file/path/evidence references after the meaning>

Net: <root issue in one sentence>
```

## Pattern 1: Direct Root Cause

Use when the user asks why something failed.

Weak shape:

- starts with a status recap
- lists logs before the cause
- says "the system got confused" instead of naming the gate
- adds a fix when the user only asked why

Better:

```text
It failed because the controller could not prove the research step belonged to
the current run.

🧠 Mechanism:
The research text existed, but the state file was newer than that edit. The
controller trusted the state timestamp more than the document content, so it
treated the work as stale.

⚠️ Why it matters:
From the user's side, this looks like the agent ignored completed work. Inside
the system, the proof gate failed.

Net: the work was present, but the controller could not prove it was current.
```

Why better: the cause comes first, the mechanism follows, and proof would only
appear after the reader knows what the proof means.

## Pattern 2: Symptom Versus Root Cause

Use when the visible symptom is not the actual cause.

Weak shape:

- explains the visible UI or log symptom
- misses the system belief behind the behavior
- repeats what the user can already see

Better:

```text
It did not think Android was missing. It thought its own readiness check had
not passed.

✅ What this is really about:
Why does the worker keep restarting something that is visibly already open?

🧠 Mechanism:
macOS can show the simulator window before the worker sees the exact ready
signal it is waiting for. If the worker checks "booted and reachable" and that
check fails, it still treats the simulator as unavailable.

Net: the visible symptom was Android opening; the root cause was a mismatch
between what the screen showed and what the worker's check accepted.
```

Why better: it names the system belief instead of narrating the visible symptom.

## Pattern 3: One Example As Evidence Of A System Failure

Use when the user's example is the clue, not the whole issue.

Weak shape:

- treats one card, file, prompt, or line as the whole issue
- repairs the nearest artifact
- misses the quality model or process failure the artifact revealed

Better:

```text
The card was only the clue. The real problem was the loop's quality model.

✅ What this is really about:
Is the system using the right process to judge the work, or is it grading its
own output too lightly?

🧠 Mechanism:
If the loop does not inspect the real user-facing surface, it can pass a local
artifact while missing the actual experience. The broken card matters because
it proves the loop accepted evidence that was too narrow.

Net: do not fix only the card; explain what the card proves about the system.
```

Why better: it preserves the example while moving the reader to the real layer.

## Pattern 4: Explanation Versus Instructions

Use when the user asks for explanation and does not ask what to do next.

Weak shape:

- ends with a plan
- adds `Next:` or `Fix:` automatically
- turns "why did this happen?" into an implementation assignment

Better:

```text
The answer drifted because it treated an explanation request as an action
request.

🧠 Mechanism:
"Why did this happen?" asks for cause. "What should we do?" asks for action.
Those are different jobs. Mixing them makes the explanation feel like it is
trying to steer the user instead of answering them.

⚠️ Why it matters:
Unasked next steps create friction because the user has to separate the actual
answer from advice they did not request.

Net: explain the cause, then stop.
```

Why better: it respects the user's requested job and avoids an action tail.

## Pattern 5: Path Or Citation Wall

Use when evidence is necessary but references are making the answer unreadable.

Weak shape:

- leads with many file paths or citations
- makes the user decode meaning from references
- treats proof as the main story

Better:

```text
The build spec is still only a planning document. It has not been turned into
the contract the builder actually reads.

⚠️ Why it matters:
The builder can ignore the plan because the runtime source of truth does not
contain the requirement yet.

Proof:
Put the relevant paths here, after the explanation.

Net: the plan exists; the executable contract is still missing.
```

Why better: the proof now has somewhere to attach.

## Pattern 6: Jargon Without Meaning

Use when a term is necessary but opaque.

Weak shape:

- introduces a broad noun like "capability" or "substrate" without defining it
- uses house labels as if they are self-explanatory
- forces the user to ask what the noun means

Better:

```text
In that answer, "capability" meant "a behavior the agent or runtime can
perform."

⚠️ Why it was confusing:
The word was broader than the thing being discussed. If the topic was Git
history rewriting, then "capability" hid the concrete point.

Better wording:
"Can this skill rewrite local commit messages safely?"

Net: use the specific behavior name unless the broader noun adds real meaning.
```

Why better: it defines the term through the behavior the user can observe.

## Pattern 7: Define, Exemplify, Contrast, Then Name

Use when the user needs a real technical term, not a watered-down replacement.

Weak:

```text
We use eventual consistency for the replica set.
```

Better:

```text
When you write a value to one replica, the other replicas do not see it
immediately. They catch up after a short delay. A read right after a write may
return the old value. That is different from strong consistency, where every
read must see the latest write. We call this model eventual consistency.
```

Why better: the reader sees the behavior first, then learns the term.

## Pattern 8: Dense Phrase Rewrite

Use when the prose contains a noun stack, team shorthand, or identifier leakage.

Weak:

```text
The live-vs-replay solver consistency check failed.
```

Better:

```text
The solver gave different answers on live data and on recorded replay data.
That means the check failed.
```

Weak:

```text
We need to reduce cross-region database failover latency.
```

Better:

```text
We need to make the database fail over to another region faster.
```

Weak:

```text
The failed password security question answer attempts limit is wrong.
```

Better:

```text
The lockout limit is wrong. Users can answer the password-reset question too
many times before the account locks.
```

Why better: the relation between the nouns becomes visible instead of implied.

## Pattern 9: Simple Does Not Mean Flat

Use when simplifying language risks shrinking the idea.

Weak shape:

- deletes the hard part
- turns a technical mechanism into a vague analogy
- makes the answer feel easy by making it less true

Better:

```text
Simpler wording should expose the hard part, not erase it.

🧠 Mechanism:
The right move is to define the key term once, keep the exact term after that,
and explain how it affects the user-facing result.

Example:
"AIVAT is the noise reducer. It does not make poker deterministic; it makes the
RTS versus non-RTS comparison less noisy when the policy probabilities are
known."

Net: plain speech should make the real mechanism easier to see.
```

Why better: the exact term stays, but the reader gets the mental model.

## Pattern 10: Analogy That Helps Versus Analogy That Replaces

Use when an analogy would make the concept more concrete.

Weak:

```text
A monad is like a burrito.
```

Why weak: the analogy does not share the mechanism that matters, so the reader
learns the analogy instead of the concept.

Better:

```text
Backpressure in a stream is like a traffic jam. A slow consumer causes the
queue ahead of it to fill up, so congestion moves upstream.
```

Why better: the analogy and the target share the same mechanism.

Rule: one analogy per concept, use it once, then return to the real mechanism.

## Pattern 11: Overbuild Versus Best Work

Use when "do not overbuild" gets misread as "do the minimum."

Weak shape:

- treats scope discipline as permission to do thin work
- equates simple with low-effort
- avoids the real quality bar

Better:

```text
"Do not overbuild" does not mean "do the smallest possible thing." It means
build at the right level.

✅ What this is really about:
The work should solve the real problem without inventing a larger system around
it.

🧠 Mechanism:
A narrow fix can still be high quality. It should hit the real user-facing
failure, preserve the right owner boundary, and include enough verification to
trust it.

Net: avoid extra architecture, not extra care.
```

Why better: it protects ambition while rejecting extra machinery.

## Pattern 12: Prompt Skill Versus Harness Instinct

Use when a natural-language skill gets over-engineered into tooling.

Weak shape:

- adds scripts, runners, schemas, or controllers before prompt guidance fails
- treats a response-style problem as an orchestration problem
- makes the skill depend on machinery it does not need

Better:

```text
This should stay a prompt skill.

✅ What this is really about:
The problem is answer shape, not deterministic execution.

🧠 Mechanism:
If the user can ask in normal language and the agent can answer with judgment,
a script adds surface area without improving the core behavior. The skill needs
clearer principles and examples, not a runner.

Net: use prompt guidance for response style; reserve tooling for repeatable
machine work.
```

Why better: it names the mechanism choice instead of adding fake determinism.

## Pattern 13: Known Incomplete Work Versus Real Defect

Use when the assistant repeats known missing work as if it discovered a new bug.

Weak shape:

- reports "not implemented yet" as a fresh finding
- misses the actual issue the user is asking about
- burns attention on baseline gaps

Better:

```text
That is known incomplete work, not the new defect.

✅ What this is really about:
The useful question is what changed, regressed, or contradicts the current
contract.

🧠 Mechanism:
A missing future feature can be true and still irrelevant. If the team already
knows it is missing, repeating it does not explain the current failure.

Net: separate known baseline gaps from new evidence.
```

Why better: it protects the reader's attention for new information.

## Pattern 14: Future System Versus Current State

Use when the user asks how a future system should work, not only what exists
today.

Weak shape:

- answers only "what it does today"
- treats future design as impossible because current wiring is incomplete
- avoids the architecture question

Better:

```text
Today-state facts are not enough here. The question is what shape the future
system should have.

✅ What this is really about:
If this becomes a real workflow, where should the responsibility live?

🧠 Mechanism:
Current behavior tells us the starting point. It does not decide the target
architecture. The target should be chosen by ownership, user experience, and
how often the workflow repeats.

Net: current wiring is evidence, not the whole answer.
```

Why better: it separates source truth from design judgment.

## Pattern 15: Status Update

Use when the user asks what happened or where things stand.

Weak shape:

- starts with process history
- says what the assistant did before saying what is true now
- hides the blocker or result

Better:

```text
The skill package is updated, but it has not been published yet.

✅ Done:
The runtime contract now explains the response style and points to the example
library.

⚠️ Not done:
Publishing is separate from editing. Until publish runs, other machines may
still have the old installed copy.

Net: the repo is updated; install/publish is the distribution step.
```

Why better: the current truth comes before the work history.

## Pattern 16: Recommendation

Use when the user asks for judgment but not a formal choice prompt.

Weak shape:

- hedges forever
- lists options without a practical read
- avoids saying which path is better

Better:

```text
Recommendation: keep this as a skill reference, not a second skill.

✅ Why:
The behavior is part of `eli10`'s answer style. Splitting it into another skill
would make routing harder without giving the agent a different job.

⚠️ Risk:
If the reference becomes too large, agents may stop reading it. Keep the main
contract in `SKILL.md` and detailed examples in the reference.

Net: one skill, one clear job, examples behind the reference door.
```

Why better: it gives judgment and names the tradeoff.

## Pattern 17: Real Decision Question

Use only when the user must choose.

Weak shape:

- asks an open-ended question without a recommendation
- gives options with no stakes
- uses decision format for a normal explanation

Better:

```text
D1 - Example Library Location
Project/branch/task: We are updating `eli10` so the runtime skill is clear but not bloated.
ELI10: The examples are useful, but they are too heavy for the main skill file. Put the short rules in `SKILL.md` and keep the rich examples in a reference file.
Stakes if we pick wrong: If the main file gets huge, the agent may miss the core rule and copy examples mechanically.
Recommendation: Put examples in `references/response-patterns.md` because it keeps the runtime contract lean.
Completeness: A=10/10, B=6/10
Pros / cons:
A) Reference file (recommended)
  ✅ Keeps `SKILL.md` short while preserving the rich examples.
  ✅ Lets the agent load examples only when the answer is high-friction.
  ❌ Requires the reference path to stay correct after packaging.
B) Inline everything
  ✅ Makes every example visible without another file read.
  ✅ Avoids a reference lookup when the agent needs a pattern.
  ❌ Bloats the always-loaded skill and encourages shape copying.
Net: references preserve the examples without turning the skill into a transcript.
```

Why better: it recommends a path, names the stakes, and makes the choice real.

## Pattern 18: Table Or No Table

Use when the answer has structured information but a table may make it harder
to read.

Weak shape:

- forces long paths, rationale, and decisions into one wide table
- uses Markdown pipe tables in Codex for important information
- lets wrapped cells destroy the row boundary
- treats visual structure as understanding

Better:

```text
This should not be one table. The rows carry too much prose, so the table makes
the reader reconstruct the meaning from wrapped cells.

✅ Include now
- Shared per-kind doctrine: emit one shared contract into every kind skill.
  Why: prevents 32 packages from drifting on evidence posture.

⚠️ Defer
- MCP playable-author contexts: read as adjacent evidence only.
  Why: useful for contradictions, but too wide for this pass.

❌ Exclude unless factual drift is found
- Runtime schemas/renderers: preserve runtime truth.
  Why: prompt work should not smuggle product changes.

Net: use tables for compact comparisons; use grouped sections for dense audit
logic.
```

Why better: related ideas stay grouped, and proof can come after meaning.

## Pattern 19: Readability Rewrite

Use when the user asks to rewrite dense prose.

Original:

```text
The implementation of the optimization of the cache invalidation mechanism
resulted in the observation of latency improvements.
```

Better:

```text
Changing how the cache invalidates entries reduced latency.
```

If the numbers are available, make it concrete:

```text
Changing how the cache invalidates entries cut p95 latency from 240ms to 80ms.
```

Why better: the action is a verb, the actor is visible enough for the context,
and the result is concrete.

## Pattern 20: Action Turn

Use when the user has already approved the direction and asks for implementation.

Weak shape:

- repeats the plan
- gives next-step options
- stops before doing the work

Better:

```text
I will make the skill edit now.

🔧 Work:
Patch the owning skill file, add the response-pattern reference, update public
metadata if it changed, then run the required skill check.

⚠️ Constraint:
The skill stays a response-style skill. It may use the Codex table renderer for
readable compact tables, but it does not become a runner or fake memory layer.

Net: this is an implementation turn, not another planning turn.
```

Why better: it respects the user's authorization and still names the constraint
that keeps the work from drifting.

## Pattern 21: Recurring Field Or Data-Shape Bug

Use when the same kind of field failure repeats across examples, runs, or
artifacts.

Weak shape:

- treats the latest failed field as isolated
- fixes one value
- misses that the requested data shape does not match the available input

Better:

```text
This is the same shape bug repeating.

✅ What this is really about:
Why does this class of field keep failing across runs?

🧠 Mechanism:
The worker expects fields that are not present in the bootstrap data. Every
time the prompt asks for that evidence before the source exists, the agent has
to guess, emit blanks, or fail validation.

Net: the bug is not the latest value; the bug is asking for a field before the
input supplies it.
```

Why better: it turns repeated examples into evidence about the contract between
the prompt and the data.

## Final Pattern Check

Before using any pattern, ask:

- Is this pattern answering the user's actual ask?
- Does it explain why the shape works?
- Am I preserving exact technical facts?
- Am I teaching the model a principle, or handing it a template to copy?
