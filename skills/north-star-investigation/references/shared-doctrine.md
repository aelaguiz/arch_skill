# North Star Investigation Shared Doctrine

## Core rules

- The investigation doc and worklog are the source of truth.
- Math-first means separating measured facts from assumptions every time.
- Hypotheses must be ranked and kept current.
- One highest-information bet at a time.
- Prefer brutal tests that can falsify a theory quickly.

## Strong investigation behavior

- quantify the current belief where possible
- use simple sanity checks before deep tooling
- kill weak theories explicitly
- choose traps, toggles, or oracles that can settle the question fast

## Weak investigation behavior

- broad logging with no settlement rule
- carrying five equal hypotheses forever
- vague claims like "performance seems bad" with no model
- turning the loop into generic implementation planning

## Boundary rules

- If the issue is now a normal bug with a concrete failure mode, move to `bugs-flow`.
- If the work becomes a broad open-ended loop without heavy quant reasoning, move to `goal-loop`.
- If the outcome is now fixed-scope delivery, move to `arch-step` or `lilarch`.
