# Commenting Principles

Distilled external best practices for useful comments. These principles distill the common guidance from mainstream language and API documentation standards. Use them as the quality bar for what this skill writes.

## What good comments explain

- Purpose the reader cannot infer from names and types alone.
- Caller-visible contract and intended use.
- Side effects, ownership, lifetime, nullability, mutability, or dependency requirements.
- Defaults, ranges, units, boolean semantics, and allowed values when ambiguity would hurt.
- Errors, panics, safety obligations, or missing-dependency behavior.
- Ordering, concurrency, invalidation, caching, or other non-obvious implementation constraints.
- Rationale for a counterintuitive design choice.
- Why a test exists and what real behavior it protects.

## Where the explanation should live

- Put contract and usage comments at declarations, module owners, package owners, or other canonical boundaries.
- Put implementation rationale next to the tricky block that needs it.
- Put shared conventions where the owning surface enforces them, not at every call site.
- Use examples only when a short example is the clearest way to show intended use or a trap.

## What not to write

- Comments that restate the name, signature, or literal mechanics of the code.
- Comments that duplicate already-truthful nearby explanation.
- Historical migration notes that no longer help a current reader use or maintain the code.
- Style-guide trivia that does not clarify behavior.
- Speculative comments about behavior that has not been proven.
- Blanket docstrings for trivial obvious functions just because a file looks underdocumented.

## Practical heuristics

- If a careful caller should be able to use a function without reading its body, the declaration or docstring should carry the needed contract.
- If the truth belongs to the implementation and would mislead a caller at the declaration, use a local inline comment instead.
- If the type and name already make the truth obvious, skip the comment.
- If the explanation would be longer than the code it justifies, first ask whether the code should be simplified instead.
- If a comment would only make sense because the behavior is buggy or unsettled, route to the owning fix workflow instead of freezing bad truth into the repo.
