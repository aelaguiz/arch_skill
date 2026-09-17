# Prompt Pattern Contract

This file is the contract for what a good prompt must contain and where each kind of guidance belongs.

## Table of contents

- Ordered flow and section ownership
- High-leverage sections that create richness
- Lightweight prompt shape
- Commander's intent and stop-line contract
- Fatal anti-patterns
- Section-placement rules
- Final self-check

## Ordered flow and section ownership

This is the full contract shape for durable prompts. Do not force every casual
prompt-writing ask into every section. For ordinary one-shot prompts, keep only
the parts that change behavior: role, goal, context, constraints, output shape,
and stop rules.

1. **Title + single-job preamble**
   - State the only job and make it clear the prompt is binding.
2. **Identity & mission**
   - Say who the agent is, what it is optimized for, and why its work matters.
3. **Success / failure**
   - Spell out what good and bad look like in concrete terms.
4. **Non-goals**
   - Name what the prompt must not do.
5. **System context**
   - Explain the larger system or downstream impact.
6. **Inputs & ground truth**
   - Clarify what is authoritative, optional, and unavailable.
7. **Tools & calling rules**
   - Say what tools exist, when to call them, and what not to do.
8. **Operating principles**
   - State the governing reasoning rules and tie-breaks.
9. **Process**
   - Teach the model how to think through the job in order.
10. **Quality bar**
   - Make the good outcome vivid and contrast it with bad output.
11. **Output contract**
   - State exactly what must be returned and how it should be validated.
12. **Error / reject handling**
   - Define fail-loud conditions and what should not count as fatal.
13. **Examples**
   - Show good and bad patterns with rationale.
14. **Anti-patterns**
   - Name the shortcuts that will poison the prompt.
15. **Checklist**
   - Give a compact final review loop.

## High-leverage sections that create richness

These sections are where strong prompts usually separate themselves from merely organized prompts:

- **System context**
  - Connect the agent to the larger system, the user-facing moment, and the downstream cost of a weak answer.
- **Quality bar**
  - Make the ideal output vivid and contrast it with the real failure mode you are trying to prevent.
- **Process with mentorship**
  - Teach how to inspect, reason, validate, repair, and decide when to stop instead of treating the work like a one-shot guess.
- **Output contract**
  - Define required fields, constraints, validation rules, and what "valid" means.
- **Error / reject handling**
  - Distinguish recoverable uncertainty from true failure. Do not teach the model to reject normal ambiguity.
- **Examples with rationale**
  - Show good and bad examples with enough reasoning to teach judgment rather than shape-matching.

If these sections are thin, the prompt may still look correct while feeling generic, brittle, or low-agency.

## Lightweight prompt shape

Use a lighter shape when the user wants a prompt for a normal task rather than
a durable agent contract:

```markdown
You are [role].

Goal: [the outcome].

Context: [facts, audience, sources, or constraints].

Instructions:
- [behavior that changes quality]
- [evidence, tool, safety, or validation rule if needed]
- [stop condition if needed]

Output: [format, length, tone, or fields].
```

This is not a mandatory template. It is a safe default when a full prompt
contract would be overbuilt.

## Commander’s intent and stop-line contract

Commander’s intent is not a task list. It should describe the improved world state the prompt is trying to create.

Good commander’s intent:
- says what success feels like at the mission level
- leaves room for judgment
- pairs well with a recognition test or stop-line question

Bad commander’s intent:
- hardcodes local actions
- turns one remembered example into a universal rule
- tells the model exactly which surface move to take every time

If the prompt needs specific behaviors, put them in:
- success / failure
- operating principles
- process
- examples

For lighter prompts, commander’s intent usually becomes the `Goal` plus a few
success criteria. Do not create a large mission section just to satisfy the
pattern.

## Fatal anti-patterns

Never ship a prompt that relies on:
- eval poisoning
- finite keyword lists
- lookup tables or hardcoded mappings
- keyword-triggered shortcuts
- phantom context or inaccessible files
- user-facing mode selection when the agent can infer the prompt shape
- process ceremony that hides the actual outcome

The test is simple:
- Could a new input tomorrow break this because the list is incomplete?
- Could the keyword rule be wrong in a different context?
- Would the prompt fail if the model cannot open the path you mentioned?

If yes, the prompt is teaching memorization, not reasoning.

## Section-placement rules

If the problem is:
- mission drift or local-action obsession: fix `Identity & mission` and `Success / failure`
- weak judgment or poor triage: fix `Operating principles` and `Process`
- prompt is overbuilt for a simple ask: collapse to role, goal, context, instructions, output, and stop rules
- prompt has the wrong shape for the job: consult `prompt-types-and-selection.md` and add only the missing lens
- missing boundaries: fix `Non-goals`
- generic or ungrounded output: fix `System context` and `Quality bar`
- structurally correct but still flat or low-agency: deepen `System context`, `Quality bar`, and `Examples`
- output shape is ambiguous or hard to debug: fix `Output contract`, `Error / reject handling`, and add rationale where choices matter
- answer must be grounded but evidence behavior is vague: fix `Inputs & ground truth`, `Tools & calling rules`, `Output contract`, and stop rules
- examples acting like rules: fix `Examples` and maybe extract the real principle upward
- inaccessible context: fix `Inputs & ground truth` and remove the dependency

## Final self-check

- Is the single job obvious?
- Is the prompt as small as the job allows?
- Does commander’s intent describe an outcome, not a menu of moves?
- Are examples illustrating a principle rather than defining it?
- Does system context explain what the output becomes for users or downstream agents?
- Does the process teach recovery and stop-line judgment rather than just listing steps?
- Does the quality bar describe genuinely strong output rather than generic polish?
- Are evidence, tools, validation, personality, audience, and formatting present only when they change the result?
- Could a reviewer validate the output contract and reject logic without guessing?
- Are the lower sections still elevated, or do they decay into heuristics?
- Could the prompt handle a new input without a hardcoded list?
- Does every referenced source actually exist in the context the prompt provides?
