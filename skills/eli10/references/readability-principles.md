# ELI10 Readability Principles

Use this reference when an answer or rewrite is high-friction. It teaches why
ELI10 works: clear writing spends the reader's working memory on the idea, not
on parsing.

This is doctrine for response style. It is not a checklist to run mechanically.
Use the principles to decide what the current answer needs.

## Source-Name References

These names are here to anchor the doctrine, not to make the response academic.
Do not cite them in ordinary answers unless the user asks for source context.

- **Nelson Cowan:** working memory is small. Do not make readers hold many
  unattached ideas while waiting for the sentence to finish.
- **Edward Gibson:** long unresolved dependencies make sentences harder to
  process. Keep subjects close to verbs and avoid center-embedded clauses.
- **Allan Paivio:** concrete examples are easier to remember because readers
  can encode them verbally and visually.
- **Joseph Williams:** make main characters the subjects and important actions
  the verbs. Put old information before new information.
- **Steven Pinker:** the curse of knowledge is why experts write prose that
  feels obvious to them and opaque to everyone else.
- **Bryan Garner / Helen Sword:** nominalizations bury verbs. Turn actions back
  into verbs when the noun is doing the real work.
- **Julia Evans:** start from a concrete thing the reader has seen or done, then
  generalize.
- **Feynman:** analogies fail when the analogy needs the same explanation as
  the thing being explained.
- **Knuth / Kernighan / Pike:** examples should be real, minimal, and contrasted;
  names should explain purpose instead of making readers learn clever labels.

## The Core Test

Before emitting, ask:

```text
What am I making the reader hold, guess, decode, or re-parse?
```

Then remove that tax.

The answer does not need to be shorter at all costs. It should be denser in
ideas per unit of reader effort.

## Useful Labels

Use these labels as private diagnosis tools. Do not cite them in ordinary
answers unless the user asks for the writing model.

- **BLUF:** bottom line up front. Put the answer, cause, recommendation, or
  current state before the proof unless it would be meaningless without one
  prerequisite.
- **Nerdview:** expert shorthand that feels obvious to insiders but hides the
  missing relations from everyone else.
- **Functional fixity:** naming a thing by its abstract role instead of by what
  the reader can see or do. `Acoustic isolation condition` is worse than
  `quiet room`.
- **Stress position:** the end of a sentence carries emphasis. Put the thing
  the reader should remember there.

## Lead With The Point

The first sentence should carry the answer, recommendation, cause, current
state, or tradeoff.

Weak:

```text
In the modern distributed systems landscape, ensuring data integrity across
multiple nodes has become increasingly important.
```

Better:

```text
We are switching the order service from strong to eventual consistency.
```

Use background first only when the conclusion would be meaningless without one
prerequisite. In that case, the prerequisite is the point.

## Unstack Nouns

A noun stack is a chain of nouns or noun-like modifiers before the head noun.
Two-noun compounds are usually fine because readers often store them as one
unit: `load balancer`, `race condition`, `stack trace`, `type system`. Three
nouns are risky unless one pair is a familiar compound. Four nouns are usually
a defect unless the whole phrase is a proper or near-proper name.

Why it hurts: English puts the head noun last, so the reader holds loose
modifiers while guessing the hidden relations between them.

Use these repair moves:

1. Move the head noun forward and add the missing relation with `of`, `for`,
   `on`, `in`, `by`, `between`, `against`, or `with`.
2. Unbury the verb when the action is trapped in a noun like `implementation`,
   `analysis`, `failure`, `configuration`, or `optimization`.
3. Promote a modifier into a relative clause: `the template that verifies a
   user's account`.
4. Replace a vague head noun like `system`, `framework`, `mechanism`, `layer`,
   `context`, or `approach` with the concrete object.
5. Split the phrase into two sentences when it is really two or three ideas.

```text
live-vs-replay solver consistency
```

Better:

```text
whether the solver gives the same answer on live data as it does when replayed
on recorded data
```

```text
cross-region database failover latency
```

Better:

```text
how long it takes to fail a database over to another region
```

```text
failed password security question answer attempts limit
```

Better:

```text
the maximum number of wrong answers to a password-reset question before lockout
```

Identifier leakage is a common version of this problem. Code may need
`failedPasswordSecurityQuestionAnswerAttemptsLimit`; prose should translate it.

Acronym stacks have the same failure mode. `AWS IAM SCP policy boundary
evaluation order` hides too many relations. Expand the terms that matter and
split the explanation before the reader has to carry a lookup table.

## Unbury Verbs

Nominalizations turn actions into nouns: `implementation`, `analysis`,
`decision`, `failure`, `configuration`, `optimization`.

Weak:

```text
The implementation of the optimization of the storage layer caused a reduction
in latency.
```

Better:

```text
Optimizing the storage layer reduced latency.
```

Diagnostic: if the sentence leans on `make`, `perform`, `conduct`, `provide`,
`has`, or `is` plus an action noun, look for the real verb.

## Name The Actor

Use active voice when the actor matters.

Weak:

```text
It was decided that the migration would be deferred.
```

Better:

```text
The platform team deferred the migration.
```

Passive voice is allowed when the actor is unknown, irrelevant, or less
important than the thing acted on:

```text
The database was purged in January.
```

The rule is not "always active." The rule is "do not hide the actor when the
actor changes the meaning."

## Start Concrete, Then Generalize

Concrete claims save the reader from inventing examples.

Weak:

```text
The system exhibits suboptimal performance characteristics under high
concurrency.
```

Better:

```text
Past 200 concurrent users, p95 latency jumps from 80ms to 2 seconds.
```

For explanations, start with a request, command, visible failure, number, or
small worked example. Then name the broader concept.

## Define Jargon Deliberately

Jargon is useful when it compresses a real expert concept. It is harmful when
the reader does not share the term or when the term is doing status work.

Good pattern:

1. define in concrete behavior
2. give an example the reader can picture
3. contrast with the nearby wrong idea
4. name the term

Example:

```text
When you write a value to one replica, the other replicas do not see it
immediately. They catch up after a short delay. A read right after a write may
return the old value. That is different from strong consistency, where every
read must see the latest write. We call this model eventual consistency.
```

For a term like `idempotent`, a worked example can beat a definition:

```text
Calling DELETE /users/42 once deletes the user. Calling it again may return
404, but it does not create a new side effect. That is what idempotent means.
```

Do not define acronyms the reader already knows in context, such as API, URL,
HTTP, JSON, SQL, CPU, or RAM. Do define team-specific acronyms and acronyms with
multiple likely meanings.

## Keep Dependencies Short

Do not separate the subject from the verb with a long interruption.

Weak:

```text
The new caching layer, which was introduced in Q3 after a six-month effort by
the platform team and replaces the previous Redis implementation, is faster.
```

Better:

```text
The new caching layer is faster. We introduced it in Q3 after a six-month
effort. It replaces the Redis implementation.
```

The goal is not tiny sentences. The goal is to close each thought before the
reader loses the thread.

## Old Before New

Sentences flow when they start with information the reader already has and end
with the new point.

Choppy:

```text
Eventual consistency is what our replica set uses. The ability for replicas to
diverge briefly under load is created by this.
```

Better:

```text
Our replica set uses eventual consistency. That means replicas can diverge
briefly under load.
```

This is why proof usually comes after meaning. Once the reader has the point,
the file path or log line has a place to attach.

## Use Analogies Carefully

Use an analogy only when it shares the mechanism you are explaining.

Bad:

```text
A monad is like a burrito.
```

Why it fails: the analogy does not share the structure that makes the concept
work, so the reader learns the analogy instead of the concept.

Better:

```text
Backpressure in a stream is like a traffic jam: a slow consumer causes the
queue ahead of it to fill up.
```

Why it works: both systems share the same mechanism. A slow node creates
congestion upstream.

Use one analogy, use it once, then return to the real mechanism.

## Cut Fog

Remove words that make the answer look careful while making it less clear.

Common fog:

- hedges with no measurement: `somewhat`, `fairly`, `basically`, `arguably`
- weasel authority: `experts say`, `it is widely believed`, `many people think`
- minimizers: `just`, `obviously`, `simply`, `clearly`, `trivially`

Replace fog with a fact, a confidence statement, or a plain admission:

```text
I do not know from the available evidence.
```

If the right answer is "it depends," name what it depends on and which way each
factor pushes.

## Code Examples

Use code when it shows the one concept being explained.

Good examples:

- use code the reader could plausibly write
- show visible behavior
- contrast the weak and stronger version
- keep boilerplate out unless boilerplate is the lesson

Weak examples:

- toy inheritance examples that teach nothing about the real use
- comments that repeat the code
- snippets that introduce three new concepts while explaining one

For comments, explain intent or invariant, not the syntax:

```python
i += 1  # Advance past the delimiter so the next read starts at the payload.
```

## Final Recognition Test

A strong ELI10 answer should pass these tests:

- The first sentence tells me why I am reading.
- The hard term is explained before it is relied on.
- Dense phrases have been unpacked into relations.
- Examples teach the principle, not a template.
- Proof and paths support the point instead of hiding it.
- The answer is simple, but not smaller than the truth.
