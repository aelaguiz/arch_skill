# High-Leverage Sections

Use this file when the prompt needs richness, not just correct section order. These sections are where a prompt becomes vivid, teachable, and meaningfully agentic.

## Table of contents

- System context
- Quality bar
- Output contract, validation, and reject handling
- Mentored process and autonomy
- Rationale fields
- Evidence, completion rules, validation, and audience lenses
- Examples that teach reasoning
- Richness check

## 1) System context

System context should explain why this job matters inside the larger system.

It should answer:
- what product, workflow, or downstream system this prompt serves
- what the output becomes
- when a user or downstream agent experiences the result
- why quality matters at this exact step

Good shape:

```markdown
## System Context
You are writing the review users will rely on before they act.

**What this becomes:** the decision brief shown before a final approval.
**User experience moment:** users read this under time pressure and need the real tradeoff fast.
**Why quality matters:** if the review hides the main risk or invents confidence, users make the wrong call.
```

Bad shape:
- "This helps the workflow."
- "This prompt supports the system."

Litmus tests:
- could a smart reader explain the downstream consequence of a weak answer?
- does this section make the agent care about the user-facing moment, not just the data shape?

## 2) Quality bar

The quality bar is where you paint what strong output feels like and what weak output looks like instead.

Make it do real work:
- describe the characteristics of a great answer
- contrast it with the failure mode you are trying to prevent
- tie it to downstream usefulness, not generic elegance

Good shape:

```markdown
## Quality Bar
- Great output names the real decision, the strongest supporting evidence, and the main uncertainty without padding.
- It sounds like an owner who understands the stakes, not a formatter replaying the inputs.
- Weak output is generic, over-certain, or technically correct but useless to the next decision-maker.
```

Bad shape:
- "Be clear and concise."
- "Return something high quality."

Litmus tests:
- would two strong reviewers agree on what "great" looks like after reading this?
- does the contrastive bad case point at the actual failure you are guarding against?

## 3) Output contract, validation, and reject handling

The prompt should not merely name fields. It should define what must be returned, how it is checked, and what counts as a real failure.

Include:
- required versus optional fields
- ordering or uniqueness rules
- validation checks or recognition tests
- what should cause rejection versus what should be handled normally

Good shape:

```markdown
## Output Contract And Validation
- Return: `decision`, `why`, `main_risk`, and `confidence`.
- `decision` is required and must be one clear action.
- `why` must cite the strongest evidence already present in the input.
- `confidence` must match the evidence quality; do not claim high confidence when key facts are missing.

## Error / Reject Handling
- Reject only when the input is missing the core artifact needed for a responsible answer.
- Sparse evidence is not itself a reject; explain the uncertainty inside the answer.
```

Bad shape:
- "Return a summary and recommendation."
- "If unsure, reject."

Litmus tests:
- would a reviewer know how to tell whether the output is valid?
- does the prompt distinguish true impossibility from ordinary uncertainty?

## 4) Mentored process and autonomy

The process section should teach the model how to think through the job and what to do when the first pass is not good enough.

Make it do real work:
- use a numbered sequence
- tell the model what to inspect, compare, validate, and repair
- encourage one more obvious in-scope improvement before returning
- never turn "one more improvement" or reviewer rejection into scope expansion;
  for plan-backed work, the frozen scope contract decides what is in scope
- prefer heal-and-retry loops over premature rejection

Good shape:

```markdown
## Process
1. Read the full brief and identify the single decision or artifact that matters.
2. Compare the available evidence and separate facts from assumptions.
3. Draft the answer in the required output shape.
4. Validate the risky claims, confidence level, and section placement.
5. If one obvious in-scope improvement remains, make it before returning.
6. Reject only if the required artifact is actually missing.
```

Bad shape:
- "Return the answer."
- "If unsure, fail."

Litmus tests:
- does the process teach a recovery loop instead of a one-shot guess?
- does it preserve autonomy without collapsing into a brittle script?

## 5) Rationale fields

Use rationale fields when the model is making a meaningful choice between alternatives or needs to prove it verified a risky claim.

Good uses:
- naming, labeling, or framing choices
- outputs that select one option from several plausible ones
- domains where misuse of a term creates false confidence

Do not overuse them:
- not every trivial field needs a rationale
- use them for substantive choices, not boilerplate filler

Good shape:

```markdown
**title:** The Decision You Can Defend

**title_rationale:** Considered a shorter title and a more dramatic title. Rejected the dramatic option because it overstated the evidence. Chose this title because it names the real decision and stays faithful to the uncertainty in the input. VERIFIED: the supporting evidence is present in the source brief.
```

Bad shape:

```markdown
**title:** Strong Recommendation

**title_rationale:** It sounded good.
```

Litmus tests:
- does the rationale show options considered, why they were rejected, and what was verified?
- would the rationale help debug a wrong answer later?

## 6) Evidence, Completion Rules, Validation, And Audience Lenses

Not every prompt needs every lens. Add these only when they change the result.

### Evidence and retrieval

Use when factual claims must come from sources, retrieved context, records,
policies, files, or tool output.

Good shape:

```markdown
Use the provided policy and account data for eligibility claims. If required
evidence is missing, ask for the smallest missing field instead of guessing.
Retrieve more only when the current evidence cannot answer the user's core
question or would leave an important factual claim unsupported.
```

Bad shape:
- "Search thoroughly."
- "Cite sources when relevant."

Litmus tests:
- does the prompt say which claims need support?
- does it say when enough evidence is enough?
- does it distinguish missing evidence from evidence of absence?

### Completion rules

Use when the model might loop, over-search, over-plan, or finish before the
intended outcome is real.

Good shape:

```markdown
Finish only once you can answer the core request with enough evidence for the
factual claims and a clear note for any remaining uncertainty. For execution
work, ordinary uncertainty should drive the next source read, test,
instrumentation, or repair, not a non-completion report.
```

Bad shape:
- "Do exhaustive research."
- "Minimize tool calls."

Litmus tests:
- does the completion rule define done-ness instead of activity?
- does it preserve correctness over artificial loop minimization?

### Validation

Use when the model can actually inspect, test, render, calculate, or otherwise
check the output.

Good shape:

```markdown
Before finalizing, run the most relevant available check for the changed
behavior. If the obvious check is unavailable, use the next best evidence path.
```

Bad shape:
- "Make sure it works."
- "Double-check everything."

Litmus tests:
- does the prompt name a real check or recognition test?
- does it say what to do when validation fails or the obvious validation path is unavailable?

### Personality and collaboration

Use when the assistant's user experience matters over multiple turns.

Good shape:

```markdown
Be direct, calm, and practical. Prefer progress over clarification when the
request is clear enough to attempt. Ask only when the missing answer would
materially change the work or create risk.
```

Bad shape:
- "Be friendly and helpful."
- "Ask questions before answering."

Litmus tests:
- does the prompt separate how the assistant sounds from how it works?
- does it define when to ask, assume, act, and call the work done?

### Formatting and audience

Use when reader fit is the main quality lever.

Good shape:

```markdown
Write for a senior business audience. Keep the answer under 400 words. Preserve
the requested structure and do not add new claims.
```

Bad shape:
- "Make it clear."
- "Improve the writing."

Litmus tests:
- does the prompt say what to preserve?
- does formatting serve the reader instead of becoming ceremony?

## 7) Examples that teach reasoning

Examples should teach how to think, not become the hidden rulebook.

Good examples:
- show a strong answer and why it is strong
- show a weak answer and why it fails
- include reasoning or rationale when the choice is non-obvious
- prefer markdown or lightweight prose over JSON unless structure itself is the lesson
- stay short enough to scan

Bad examples:
- function like a lookup table
- are so specific that they become the answer key
- only show final shape without explaining the reasoning

## 8) Richness check

Ask these before you ship:
- If you removed the examples, would the principle still survive?
- If you removed the process, would the prompt still explain why the work matters?
- Does the quality bar describe a genuinely useful answer, not just a formatted one?
- Are evidence, completion rules, validation, personality, and formatting present only where they matter?
- Can a downstream reader tell what must be validated?
- Are rationale fields present where choice quality or verification really matters?
