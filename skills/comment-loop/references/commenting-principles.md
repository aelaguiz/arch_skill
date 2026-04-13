# Commenting Principles

These principles distill the common guidance from mainstream language and API documentation standards. Use them as the quality bar for what this skill writes.

## What good comments explain

- purpose the reader cannot infer from names and types alone
- caller-visible contract and intended use
- side effects, ownership, lifetime, nullability, mutability, or dependency requirements
- defaults, ranges, units, boolean semantics, and allowed values when ambiguity would hurt
- errors, panics, safety obligations, or missing-dependency behavior
- ordering, concurrency, invalidation, caching, or other non-obvious implementation constraints
- rationale for a counterintuitive design choice
- why a test exists and what real behavior it protects

## Where the explanation should live

- Put contract and usage comments at declarations, module owners, package owners, or other canonical boundaries.
- Put implementation rationale next to the tricky block that needs it.
- Put shared conventions where the owning surface enforces them, not at every call site.
- Use examples only when a short example is the clearest way to show intended use or a trap.

## What not to write

- comments that restate the name, signature, or literal mechanics of the code
- comments that duplicate already-truthful nearby explanation
- historical migration notes that no longer help a current reader use or maintain the code
- style-guide trivia that does not clarify behavior
- speculative comments about behavior that has not been proven
- blanket docstrings for trivial obvious functions just because a file looks underdocumented

## Practical heuristics

- If a careful caller should be able to use a function without reading its body, the declaration or docstring should carry the needed contract.
- If the truth belongs to the implementation and would mislead a caller at the declaration, use a local inline comment instead.
- If the type and name already make the truth obvious, skip the comment.
- If the explanation would be longer than the code it justifies, first ask whether the code should be simplified instead.
- If a comment would only make sense because the behavior is buggy or unsettled, route to the owning fix workflow instead of freezing bad truth into the repo.
