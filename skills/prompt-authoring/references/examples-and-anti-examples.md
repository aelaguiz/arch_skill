# Examples And Anti-Examples

These are adapted from real failures already seen in this repo, but rewritten as portable prompt-authoring patterns. Use them to teach the principle, not to cargo-cult the wording.

## Table of contents

- Case 1: commander's intent collapsed into procedure
- Case 2: one acceptable local move was mistaken for the stop line
- Case 3: examples hardened into a hidden action menu
- Case 4: wrong-layer edits flattened the prompt
- Case 5: phantom context
- Case 6: refactor deleted the useful magic
- Case 7: system context existed in name only
- Case 8: quality bar was too generic to guide judgment
- Case 9: output contract named fields but not validity
- How to use these examples safely

## Case 1: commander’s intent collapsed into procedure

Real failure pattern:
- the prompt tried to make commander’s intent own the exact interaction script instead of the outcome

Bad shape:
- "Always summarize the request, ask two clarifying questions, propose the plan, and end with next steps."

Better shape:
- "Help the user leave with a clearer decision, a stronger prompt, or a sharper diagnosis. Use judgment about how to get there; the process details belong lower in the prompt."

Why the better shape works:
- the mission stays high-level
- specific behaviors can still live lower in success/failure, process, or examples

Transferable principle:
- commander’s intent should describe the improved world state, not the menu of moves

## Case 2: one acceptable local move was mistaken for the stop line

Real failure pattern:
- the prompt rewarded the first locally correct move even when one more obvious in-scope improvement was still left

Bad shape:
- "Once you produce a correct answer, stop."

Better shape:
- "After the first acceptable move, ask whether one more obvious in-scope improvement would materially strengthen the result before stopping."

Why the better shape works:
- it preserves autonomy
- it teaches stop-line judgment instead of a brittle stopping rule

Transferable principle:
- prompts should teach when to stop, not just how to start

## Case 3: examples hardened into a hidden action menu

Real failure pattern:
- examples started functioning like the actual rulebook instead of illustrations

Bad shape:
- "Choose from these response types: summarize, escalate, defer, reject."

Better shape:
- "Use examples only to show what smart action can look like. The real rule is the recognition test and the desired outcome."

Why the better shape works:
- new cases can still be handled correctly
- examples stay illustrative rather than exhaustive

Transferable principle:
- examples should illuminate judgment, not replace it

## Case 4: wrong-layer edits flattened the prompt

Real failure pattern:
- the same shared wording was pasted everywhere, washing out role identity and section ownership

Bad shape:
- one generic block tries to carry mission, process, and role-specific rules for every surface

Better shape:
- shared mission stays high-level
- role identity stays in identity and system-context sections
- process and examples stay lower

Why the better shape works:
- each section owns one kind of reasoning
- the prompt keeps both coherence and personality

Transferable principle:
- fix the highest section that owns the problem before rewriting the lower ones

## Case 5: phantom context

Real failure pattern:
- prompts referenced files or docs the runtime could not actually access

Bad shape:
- "Use the design doc, the meeting notes, and the internal write-up when deciding."

Better shape:
- "Bundle the needed doctrine into the skill or paste the binding context into the prompt."

Why the better shape works:
- the prompt becomes portable
- the model is not asked to rely on invisible context

Transferable principle:
- never make a prompt depend on context that is not actually present

## Case 6: refactor deleted the useful magic

Real failure pattern:
- a refactor replaced a vivid, effective prompt with a generic template and lost the behavior that made the original work

Bad shape:
- "Replace the whole prompt with the standard template so everything is uniform."

Better shape:
- "Keep the useful behavior, extract the principle that makes it work, and relocate brittle wording into examples, rationale, or litmus tests instead of deleting it."

Why the better shape works:
- it preserves the prompt's strengths
- it upgrades structure without flattening tone or judgment

Transferable principle:
- refactoring should preserve durable behavior while removing brittle expression

## Case 7: system context existed in name only

Real failure pattern:
- the prompt had a section named `System context`, but it did not explain what the output becomes or why quality matters

Bad shape:
- "This prompt supports the review workflow."

Better shape:
- "This output becomes the brief users read before making a decision. They will use it under time pressure. If it hides the key tradeoff or invents certainty, the next decision goes wrong."

Why the better shape works:
- it ties the work to a real user or downstream moment
- it gives the model a reason to care about quality beyond formatting

Transferable principle:
- system context should create stakes, not just name the surrounding system

## Case 8: quality bar was too generic to guide judgment

Real failure pattern:
- the prompt asked for high quality but never defined what strong output looks like or what weak output does wrong

Bad shape:
- "Be clear, concise, and useful."

Better shape:
- "Strong output names the real decision, cites the strongest available evidence, and surfaces the main uncertainty without padding. Weak output is generic, overconfident, or technically correct but not decision-useful."

Why the better shape works:
- it gives the model a contrastive target
- it makes quality downstream-useful rather than ornamental

Transferable principle:
- quality bars should describe the real win condition and the real failure mode

## Case 9: output contract named fields but not validity

Real failure pattern:
- the prompt listed fields to return, but never explained how to validate them or when to reject

Bad shape:
- "Return title, summary, recommendation, and confidence."

Better shape:
- "Return `title`, `summary`, `recommendation`, and `confidence`. `recommendation` must be one clear action. `confidence` must match the evidence quality. Reject only when the core artifact required for a responsible answer is missing; ordinary uncertainty belongs inside the answer."

Why the better shape works:
- it distinguishes formatting from correctness
- it prevents the prompt from turning ordinary ambiguity into a false failure

Transferable principle:
- output contracts should define validity and reject semantics, not just field names

## How to use these examples safely

- Prefer the principle over the wording.
- If you borrow an example, say why it works.
- If the example starts feeling like a lookup table, stop and extract the higher-level rule instead.
