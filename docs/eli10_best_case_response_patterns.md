# ELI10 Best-Case Response Patterns

This doc turns mined Codex chat patterns into clean authoring examples for the
`eli10` skill.

It is authoring evidence, not runtime memory. The shipped skill should not
pretend it remembers old chats or depend on this doc at runtime; reusable
runtime examples belong inside `skills/eli10/references/`.

Use it as the example bank when updating `skills/eli10`. The examples are
written in the target style, not as raw transcript excerpts.

## Style Key

- `✅` means what works, what is true, or what to keep.
- `⚠️` means risk, confusion, blocker, or why it matters.
- `🔧` means fix, change, or implementation move. Use only when action was
  requested.
- `➡️` means next move. Use only when next steps were requested.
- `❌` means reject, remove, or do not do.
- `Net:` means the final practical takeaway.

Use markers for scanability, not decoration. Never put them inside exact code,
commands, JSON, YAML, schemas, or copied machine output.

## The Shape To Aim For

Best-case `eli10` answers usually follow this order:

1. Direct answer.
2. The right layer: symptom, mechanism, root cause, system boundary, or
   tradeoff.
3. Why it matters, when the stakes are not obvious.
4. Any proof or technical detail the user needs.
5. `Net:` takeaway.

Only include "what to do" when the user asked for action, a plan,
implementation, or next steps.

The point is not to sound casual. The point is to make the answer easy to
understand without losing the technical truth.

## Pattern 1: Direct Root Cause

Use when the user asks: "why did this fail?", "why did it not work?", or "what
happened?"

Bad answer shape:

- Starts with a status recap.
- Lists files or logs before explaining the cause.
- Says "the system got confused" instead of naming the exact gate.

Best-case response:

```text
It failed because the controller could not prove the research step was complete
for this run.

⚠️ Why that matters:
The research text existed, but the state file was newer than that edit. So the
controller treated the work as stale.

🧠 Mechanism:
The controller trusted the state timestamp more than the document content.

Net: the work was there, but the controller could not prove it belonged to the
current run.
```

## Pattern 2: Too Many File Paths

Use when the answer is technically grounded but unreadable because every
sentence has paths, line numbers, or artifact names.

Bad answer shape:

- Leads with path soup.
- Makes the user decode the meaning from citations.
- Treats proof as more important than understanding.

Best-case response:

```text
The build spec is still only a planning document. It has not been turned into
the contract the builder actually reads.

⚠️ Why that matters:
The builder can accidentally ignore the plan because the real runtime contract
does not contain it yet.

🔧 Fix:
Move the real requirements into the builder's source-of-truth file.

Proof:
The relevant paths can come after this summary, not before it.

Net: the plan exists, but the executable contract is still missing.
```

## Pattern 3: Citation Wall

Use when an audit or review answer buries the main idea under proof.

Bad answer shape:

- Every bullet starts with a citation.
- The main finding is split across many references.
- The user has to read the proof to learn the answer.

Best-case response:

```text
The main problem is duplicate ownership.

Two parts of the system are trying to decide the same thing. That is risky
because one side can change while the other stays stale.

🔧 Fix:
Pick one owner. Make the other side consume that result instead of deciding
again.

Proof:
The file references support this, but they are not the main story.

Net: one owner, one decision, no parallel truth.
```

## Pattern 4: Scope Creep Or Overbuild

Use when the assistant turns a narrow request into a larger system, new skill,
new runner, harness, schema, or extra phase.

Bad answer shape:

- Adds global infrastructure for a local fix.
- Adds scripts when prompt wording is enough.
- Makes the user approve work they did not ask for.

Best-case response:

```text
I over-expanded the task.

✅ Actual problem:
The current lesson is choosing the wrong playable surface.

⚠️ Why it matters:
If we solve this globally, we create new contracts before fixing the user-facing
lesson.

🔧 Right fix:
Patch the lesson policy and repair the current lesson.

❌ Stop doing:
Do not add a global proof skill unless the user asks for that.

➡️ Next move:
Land the narrow content fix first.

Net: this is a local lesson repair, not a studio-wide infrastructure project.
```

## Pattern 5: One Clear Question

Use when the user needs to choose, but the assistant is burying the choice in a
menu, caveats, or long setup.

Bad answer shape:

- Gives three paragraphs before the question.
- Asks several questions at once.
- Includes choices the repo can answer by inspection.

Best-case response:

```text
Which output should be canonical: the Markdown handoff or the JSON handoff?
```

If a little context is needed:

```text
One decision blocks the plan.

Question:
Which output should be canonical: the Markdown handoff or the JSON handoff?

Net: once that is chosen, the rest is implementation detail.
```

## Pattern 6: Real Decision Brief

Use only when the user actually has to choose between meaningful options.

Bad answer shape:

- Uses a decision template for a normal explanation.
- Hides the recommendation.
- Scores options when the options differ in kind, not coverage.

Best-case response:

```text
D1 — Should we keep this fix local or make it global?
Project/task: We are fixing a lesson behavior that currently chooses the wrong
playable surface.

ELI10:
The local fix solves the actual problem. The global fix changes the whole
authoring system before we know that the problem repeats elsewhere.

Stakes if we pick wrong:
We could spend time building new infrastructure while the broken lesson stays
broken.

Recommendation: keep it local because it solves the current failure with less
blast radius.

Completeness: Note: options differ in kind, not coverage — no completeness
score.

Pros / cons:
A) Local lesson fix (recommended)
  ✅ Solves the user-facing failure directly without changing the whole studio.
  ✅ Keeps the implementation easier to review and easier to revert.
  ❌ If the same failure repeats elsewhere, we may need a later global rule.
B) Global authoring rule
  ✅ Could prevent this class of issue across many lessons if it is widespread.
  ❌ Adds new contracts before we have proved the broader need.

Net: fix the lesson first; promote the rule later only if the pattern repeats.
```

## Pattern 7: Confusing Name Or Label

Use when a field, mode, skill, or section name sounds like a judgment instead
of describing behavior.

Bad answer shape:

- Explains around the confusing name.
- Keeps the old label for compatibility without saying why.
- Treats wording as cosmetic.

Best-case response:

```text
The problem is the label.

⚠️ Why it confuses people:
`corporate_ai` sounds like a quality judgment. It does not say what the mode
actually does.

🔧 Better name:
Use `formal_tone` if the behavior is formal wording.

❌ Remove:
Do not keep the old vague field unless there is a real compatibility need.

Net: the name should describe behavior, not make the reader guess the author's
opinion.
```

## Pattern 8: Repo Truth Before Invention

Use when the assistant starts designing from scratch even though the repo,
diff, logs, or previous behavior can answer the question.

Bad answer shape:

- Guesses how the system should work.
- Asks the user for facts that are on disk.
- Invents a replacement instead of inspecting the old behavior.

Best-case response:

```text
We should not design this from scratch.

✅ First:
Inspect the old diff and find the behavior that already worked.

🔧 Then:
Preserve the working behavior unless it cannot handle the current need.

⚠️ Only design new machinery if:
The old behavior is missing, broken, or incompatible with the current contract.

Net: recover proven behavior before inventing a replacement.
```

## Pattern 9: Ownership Boundary

Use when the answer crosses repo, layer, or team ownership.

Bad answer shape:

- Silently edits another repo.
- Solves a caller problem by changing a dependency.
- Does not say who owns which surface.

Best-case response:

```text
This repo should not patch Doctrine.

✅ This repo owns:
The skill wording and local behavior.

✅ Doctrine owns:
Compiler path behavior.

🔧 Right plan:
Change this skill so it does not require Doctrine changes.

Net: fix the caller side here; leave Doctrine changes to the Doctrine owner.
```

## Pattern 10: Not Built Yet Versus Real Issue

Use when normal incompleteness and actual design risk are getting mixed
together.

Bad answer shape:

- Puts missing work and broken architecture in one list.
- Makes the user infer severity.
- Treats all gaps as equal.

Best-case response:

```text
There are two different buckets.

Not built yet:
The adapter does not have the final runtime path wired.

Real issue:
Two layers both think they own the same handoff.

➡️ What to do next:
Finish the missing adapter, then remove the duplicate owner.

Net: unfinished work is expected; duplicate ownership is the real risk.
```

## Pattern 11: Status Update

Use when the user asks what is done, what is weak, or what is left.

Bad answer shape:

- Replays every command.
- Lists activity instead of state.
- Hides whether the work is healthy or blocked.

Best-case response:

```text
Current state: the feature is implemented, but the proof is still thin.

✅ Done:
The main behavior is wired and runs locally.

⚠️ Weak:
The tests cover the happy path, but not the failure case that caused the bug.

➡️ Next:
Add one regression test for the failure case and rerun the targeted check.

Net: implementation is mostly there; confidence is not high until the regression
test exists.
```

## Pattern 12: Machine-Readable Output Needs Human Companion

Use when JSON, schema, or structured handoff is correct but hard for humans to
review.

Bad answer shape:

- Gives only JSON.
- Puts explanatory emojis inside JSON.
- Treats machine readability and human readability as the same thing.

Best-case response:

```text
Keep the JSON clean.

✅ JSON owns:
Exact fields the runner needs.

✅ Markdown owns:
The human-readable summary.

⚠️ Do not:
Put emojis or prose markers inside the JSON itself.

Net: machines get exact syntax; humans get a clean rendered summary.
```

## Pattern 13: Weak Examples

Use when the answer says the right rule but examples are too thin to teach it.

Bad answer shape:

- "Use clear names."
- "Make it simpler."
- "Avoid jargon."

Best-case response:

```text
Weak example:
"Use a clear name."

Strong example:
"Rename `mode: corporate_ai` to `mode: formal_tone` because the first name
sounds like a judgment and the second name describes the behavior."

✅ Why this works:
It shows the bad label, the better label, and the reason.

Net: examples should teach the decision, not decorate the rule.
```

## Pattern 14: Reading Level Is Acceptance

Use when text is structurally correct but too formal, abstract, or packed with
nouns.

Bad answer shape:

- Treats plain English as polish.
- Keeps long abstract phrases.
- Says "this is already clear" because the logic is correct.

Best-case response:

```text
Before:
"The agent must preserve provenance boundaries across generated artifacts."

After:
"The agent must say where each output came from, and it must not mix sources."

✅ Why the second version works:
It uses common words and says the action directly.

Net: reading level is part of whether the instruction works.
```

## Pattern 15: Simple Does Not Mean Flat

Use when simplification removes useful texture, contrast, or examples.

Bad answer shape:

- Cuts everything down until the answer is sterile.
- Removes the example that made the rule understandable.
- Confuses concise with useful.

Best-case response:

```text
Too flat:
"The result is worse."

Better:
"The result is shorter, but it lost the part that made the user understand why
the rule matters."

✅ What to keep:
The contrast that explains the tradeoff.

Net: simple should feel clear, not lifeless.
```

## Pattern 16: Plain Language Must Not Shrink The Job

Use when "simple," "small," or "bounded" wording accidentally tells the agent
to do less than the user wants.

Bad answer shape:

- Calls the task "little" or "tiny" in the instruction to the executor.
- Hides ambition behind safety language.
- Turns a real command into a low-effort check.

Best-case response:

```text
Do not tell the executing agent this is "little."

Tell it:
"Run the command, inspect the repo, make the required edits, verify the result,
and report the exact outcome."

✅ Why:
The wording is still plain, but it does not weaken the assignment.

Net: simplify the language without lowering the bar.
```

## Pattern 17: General ELI10 Overlay

Use when `$eli10` is invoked for any answer type.

Bad answer shape:

- Adds one "ELI10 version" paragraph.
- Leaves the rest of the answer dense.
- Treats the skill as a decision workflow.

Best-case response:

```text
Use `eli10` on the whole answer.

✅ Explanation
✅ Review
✅ Plan
✅ Recommendation
✅ Status update
✅ Decision question

⚠️ Important:
Only use the decision-brief format when the user actually needs to choose.

Net: ELI10 is the answer shape, not a paragraph title.
```

## Pattern 18: Process Chatter

Use when the assistant starts with reload notes, implementation history, or
authoring process instead of the answer.

Bad answer shape:

- "Reloaded from disk..."
- "Historically, this skill..."
- "I used the skill cleanly enough..."

Best-case response:

```text
I over-expanded the task.

✅ Actual problem:
The requested fix was local.

⚠️ Why it matters:
I turned it into a broader system change before proving that was needed.

🔧 Right fix:
Return to the requested surface and land the narrow correction.

Net: current action beats process history.
```

## Pattern 19: Magnitude Or Unit Confusion

Use when a number could mean rows, chunks, files, examples, hands, books, runs,
or another unit.

Bad answer shape:

- Treats "30" as obvious.
- Starts a huge job from a small-sample request.
- Does not restate the unit.

Best-case response:

```text
I read "30" as 30 full documents, but you meant about 30 chunks.

🔧 Correct unit:
Use 30 tokenized rows as the sample.

⚠️ Why it matters:
The wrong unit turns a quick sample into a huge job.

Net: confirm the unit before scaling the work.
```

## Pattern 20: Avoidable Questions

Use when the assistant asks the user to answer something the repo can answer.

Bad answer shape:

- "Which file owns this?"
- "How does this currently work?"
- "Should I inspect the repo?"

Best-case response:

```text
I should inspect this first.

✅ Discoverable:
How the current flow works.

✅ Discoverable:
Which files own the behavior.

❓ Real user decision:
Whether to preserve that behavior or intentionally change it.

Net: do not ask the user for facts the repo can answer.
```

## Pattern 21: Capability Or Support Verdict

Use when the user asks whether a system can support something now.

Bad answer shape:

- Hedges without a verdict.
- Lists partial evidence before saying yes or no.
- Mixes "supported" and "missing" in one paragraph.

Best-case response:

```text
Verdict: supported with one gap.

✅ Supported:
The compiler can load the shared prompt root and resolve the route.

⚠️ Gap:
The emitted readable output does not yet show the support path clearly.

🔧 Fix:
Add the support path to the readable output and test that render.

Net: the core capability works; the human proof needs one more line.
```

## Pattern 22: Practical Read Before Caveats

Use when the user asks for judgment and routine uncertainty caveats would not
change the action.

Bad answer shape:

- Starts with "I cannot know for sure."
- Over-explains uncertainty the user already understands.
- Avoids giving the practical read.

Best-case response:

```text
My read: this is partial progress, not a full fix.

⚠️ Why:
It shows movement, but it does not resolve the underlying issue.

➡️ What to do:
Treat it as useful evidence, but keep pushing for the structural fix.

Net: acknowledge the progress without pretending the real problem is solved.
```

## Pattern 23: User Wants Options

Use when the user asks for options in plain English.

Bad answer shape:

- Gives a taxonomy instead of choices.
- Uses labels that sound technical but do not help the decision.
- Does not recommend a default.

Best-case response:

```text
Recommendation: choose the local fix first.

✅ Local fix:
Fastest path to repair the user-facing problem.

✅ Global rule:
Useful later if the same failure repeats across the system.

❌ Global rule first:
Too much blast radius before we prove the broader pattern.

Net: fix the current problem now; generalize only after repetition proves it is
worth it.
```

## Pattern 24: User Wants Action, Not More Explanation

Use when the user has already approved the direction and now wants the work
done.

Bad answer shape:

- Repeats the plan.
- Gives next-step options.
- Stops before executing.

Best-case response:

```text
I will make the narrow edit now.

🔧 Work:
Patch the owning file, update the matching docs if the public behavior changed,
then run the required check.

Net: no more planning; this is an implementation turn.
```

## Pattern 25: What To Put In The Skill

The strongest reusable rules for `skills/eli10` are:

- Apply the style to the whole answer.
- Start with the direct answer.
- Use short sentences and common words.
- Preserve exact technical facts.
- Define jargon once.
- Name the stakes.
- Put proof after meaning.
- Use visual markers when they improve scanning.
- Use `Net:` for plans, reviews, risks, tradeoffs, and recommendations.
- Keep examples real and instructive.
- Do not shrink the task while simplifying the words.
- Do not turn a style request into a workflow.

Net: `eli10` should make the answer easier to understand on the first read,
without making it less true, less useful, or less ambitious.
