# Edit, Refactor, And Audit

Use this file when the prompt already exists and the job is to diagnose, repair, or elevate it.

## Symptom-to-fix map

| Symptom | What it usually means | Fix location |
| --- | --- | --- |
| Commander’s intent reads like a checklist of actions | mission-level intent collapsed into mechanics | `Identity & mission`, `Success / failure`, then move details lower |
| Prompt starts strong, then ends in keyword rules or hardcoded mappings | lower-half heuristic drift | `Operating principles`, `Process`, `Examples`, `Anti-patterns` |
| Examples feel like the real rulebook | examples are carrying too much logic | extract the principle upward; keep examples illustrative |
| Shared wording flattened the prompt’s personality or role | identity and stakes are too generic | `Identity & mission`, `System context`, `Quality bar` |
| Prompt has the right headings but still feels generic | the rich sections are thin or perfunctory | `System context`, `Quality bar`, `Examples` |
| Output is hard to judge or debug | schema, validation, or reject semantics are underspecified | `Output contract`, `Error / reject handling` |
| The model makes important choices but the prompt gives no way to inspect them | rationale is missing where verification matters | `Output contract`, `Examples` |
| Prompt depends on files or docs the model cannot open | phantom context | `Inputs & ground truth`; bundle the needed context or remove the dependency |
| Refactor removed behavior that used to help | useful magic got deleted instead of relocated | restore the principle, then re-home the brittle text as examples or litmus tests |

## Refactor-without-losing-magic loop

1. Mark the parts of the old prompt that seem to produce useful behavior.
2. Ask what durable principle those lines are trying to protect.
3. Promote that principle upward into mission, success/failure, operating principles, or process.
4. Demote brittle shortcuts into examples, rationale, or litmus tests.
5. Re-read from top to bottom and look for lower-half decay back into heuristics.

## Audit questions

Ask these before you change anything:

1. What is the single job?
2. Does commander’s intent describe the desired outcome or just a sequence of moves?
3. Would a strong human owner still see one obvious in-scope move left before stopping?
4. Are any sections doing work that belongs higher or lower in the prompt?
5. Are the examples teaching reasoning, or are they secretly the rules?
6. Are there keyword lists, lookup tables, or brittle mappings?
7. Does the prompt assume context the runtime cannot actually access?
8. Does the bottom half stay elevated, or does it become tactical and myopic?
9. Does system context explain what the output becomes and why users or downstream agents care?
10. Is the quality bar vivid enough that "great" and "bad" output are meaningfully different?
11. Could a reviewer validate the output and reject logic without guessing?
12. Should any high-stakes choice include a rationale field or verification note?

## Edit discipline

- Patch the smallest section that owns the problem.
- If a section is healthy, leave its voice alone.
- If multiple sections are wrong for the same reason, fix the highest one first and see what lower text becomes unnecessary.

## Audit output shape

For each finding, say:
- what is wrong
- why it matters
- where the fix belongs
- what the stronger shape should do instead

Prefer findings like:
- "Commander’s intent is trying to own process mechanics; move those details to process and success/failure."
- "The examples are functioning as an action menu; extract the principle and keep the examples as illustrations only."
- "The headings are present, but system context and quality bar are too thin to teach why this work matters."
- "The prompt names output fields but does not define how a reviewer would know the answer is valid."

Avoid findings like:
- "This feels off."
- "Maybe tighten wording."
