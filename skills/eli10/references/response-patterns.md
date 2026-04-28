# ELI10 Response Patterns

This is the runtime example library for `eli10`.

It teaches response style, not historical memory. The agent must not claim it
remembers prior chats or hidden user preferences. Use these examples only to
choose a clear answer shape for the current conversation.

## Style Key

- `✅` means true, working, supported, keep, or confirmed.
- `⚠️` means risk, confusion, blocker, stakes, or why it matters.
- `🧠` means mechanism, mental model, or system belief.
- `🔧` means fix, change, or implementation move. Use only when action was
  requested.
- `❌` means wrong path, reject, remove, or do not do.
- `➡️` means next move. Use only when next steps were requested.
- `Net:` means the final practical takeaway.

Use markers for scanability, not decoration. Never put them inside code,
commands, JSON, YAML, schemas, or copied machine output.

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

Use when the user asks for a plan, implementation, repair, or next steps.

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

Bad shape:

- Starts with a status recap.
- Lists logs before the cause.
- Says "the system got confused" instead of naming the gate.
- Adds a fix when the user only asked why.

Best-case response:

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

## Pattern 2: Symptom Versus Root Cause

Use when the visible symptom is not the actual cause.

Bad shape:

- Explains the visible UI or log symptom.
- Misses the system belief behind the behavior.
- Repeats what the user can already see.

Best-case response:

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

## Pattern 3: Myopic Artifact Versus System Failure

Use when the user's example is evidence of a larger process failure.

Bad shape:

- Treats one card, file, prompt, or line as the whole issue.
- Repairs the nearest artifact.
- Misses the quality model or process failure the artifact revealed.

Best-case response:

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

## Pattern 4: System Question Versus One Broken Case

Use when the user asks about whether the system can support a broader mode.

Bad shape:

- Answers only the current failure.
- Says what exists today without explaining the missing system capability.
- Treats a strategic question as a bug ticket.

Best-case response:

```text
The current failure is one example. The real question is whether the system has
a clean path for this whole class of work.

✅ What this is really about:
Can the tool reason from the source of truth directly, or does it need a
special bridge every time?

🧠 Mechanism:
If the files are already on disk, the agent should inspect them directly. A
separate connector only helps when the source is outside the local workspace or
has permissions the shell cannot reach.

Net: the system question is source-of-truth access, not the one broken call.
```

## Pattern 5: Explanation Versus Instructions

Use when the user asks for explanation and does not ask what to do next.

Bad shape:

- Ends with a plan.
- Adds `Next:` or `Fix:` automatically.
- Turns "why did this happen?" into an implementation assignment.

Best-case response:

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

## Pattern 6: File Path Wall

Use when proof is necessary but paths are making the answer unreadable.

Bad shape:

- Leads with many file paths.
- Makes the user decode meaning from references.
- Treats proof as the main story.

Best-case response:

```text
The build spec is still only a planning document. It has not been turned into
the contract the builder actually reads.

⚠️ Why it matters:
The builder can ignore the plan because the runtime source of truth does not
contain the requirement yet.

Proof:
The relevant paths support this, but they belong after the explanation.

Net: the plan exists; the executable contract is still missing.
```

## Pattern 7: Citation Wall

Use when an audit buries the finding under evidence.

Bad shape:

- Every bullet starts with a citation.
- The main finding is split across many proof points.
- The user must read the proof to learn the answer.

Best-case response:

```text
The main problem is duplicate ownership.

🧠 Mechanism:
Two parts of the system are trying to decide the same thing. That creates
parallel truth: one side can change while the other stays stale.

Proof:
Put the file references here, after the meaning is clear.

Net: one owner, one decision, no parallel truth.
```

## Pattern 8: Jargon Without Meaning

Use when a term is necessary but opaque.

Bad shape:

- Introduces a broad noun like "capability" or "substrate" without defining it.
- Uses house labels as if they are self-explanatory.
- Forces the user to ask what the noun means.

Best-case response:

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

## Pattern 9: Overbuild Versus Best Work

Use when "do not overbuild" gets misread as "do the minimum."

Bad shape:

- Treats scope discipline as permission to do thin work.
- Equates simple with low-effort.
- Avoids the real quality bar.

Best-case response:

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

## Pattern 10: Prompt Skill Versus Harness Instinct

Use when a natural-language skill gets over-engineered into tooling.

Bad shape:

- Adds scripts, runners, schemas, or controllers before prompt guidance fails.
- Treats a response-style problem as an orchestration problem.
- Makes the skill depend on machinery it does not need.

Best-case response:

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

## Pattern 11: Known Incomplete Work Versus Real Defect

Use when the assistant repeats known missing work as if it discovered a new
bug.

Bad shape:

- Reports "not implemented yet" as a fresh finding.
- Misses the actual issue the user is asking about.
- Burns attention on baseline gaps.

Best-case response:

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

## Pattern 12: Future System Versus Current State

Use when the user asks how a future system should work, not what exists now.

Bad shape:

- Answers only "what it does today."
- Treats future design as impossible because current wiring is incomplete.
- Avoids the architecture question.

Best-case response:

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

## Pattern 13: Recurring Field Or Data-Shape Bug

Use when the same kind of field failure repeats.

Bad shape:

- Treats the latest failed field as isolated.
- Fixes one value.
- Misses that the prompt asks for data the input does not contain.

Best-case response:

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

## Pattern 14: Status Update

Use when the user asks what happened or where things stand.

Bad shape:

- Starts with process history.
- Says what the assistant did before saying what is true now.
- Hides the blocker or result.

Best-case response:

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

## Pattern 15: Recommendation

Use when the user asks for judgment but not a formal choice prompt.

Bad shape:

- Hedges forever.
- Lists options without a practical read.
- Avoids saying which path is better.

Best-case response:

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

## Pattern 16: Real Decision Question

Use only when the user must choose.

Bad shape:

- Asks an open-ended question without a recommendation.
- Gives options with no stakes.
- Uses decision format for a normal explanation.

Best-case response:

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

## Pattern 17: Action Turn

Use when the user has already approved the direction and asks for implementation.

Bad shape:

- Repeats the plan.
- Gives next-step options.
- Stops before doing the work.

Best-case response:

```text
I will make the skill edit now.

🔧 Work:
Patch the owning skill file, add the response-pattern reference, update public
metadata, then run the required skill check.

⚠️ Constraint:
The skill stays a response-style skill. It may use the Codex table renderer for
readable compact tables, but it does not become a runner or fake memory layer.

Net: this is an implementation turn, not another planning turn.
```

## Pattern 18: Simple Does Not Mean Flat

Use when simplifying language risks shrinking the idea.

Bad shape:

- Deletes the hard part.
- Turns a technical mechanism into a vague analogy.
- Makes the answer feel easy by making it less true.

Best-case response:

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

## Pattern 19: Table Or No Table

Use when the answer has structured information but a table may make it harder
to read.

Bad shape:

- Forces long paths, rationale, and decisions into one wide table.
- Uses Markdown pipe tables in Codex for important information.
- Lets wrapped cells destroy the row boundary.
- Treats visual structure as understanding.

Best-case response:

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
