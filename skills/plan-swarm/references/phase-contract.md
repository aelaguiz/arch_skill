# Phase Contract

The phase contract is the small source-of-truth brief every worker and reviewer
can read without absorbing the whole plan.

## Required Fields

- Plan path
- Active phase heading
- Stop boundary
- Target state
- In-scope surfaces
- Out-of-scope surfaces
- Owner boundaries
- Cleanup obligations
- Validation obligations
- Plan-required verification, including commands, scenarios, devices, generated
  artifacts, or manual proof explicitly named by the plan
- Impact-aware verification notes: what changed, what adjacent behavior is
  plausibly affected, and what already-passing proof can stay trusted unless
  touched
- Save, persistence, or QA behavior obligations
- Applicable Definition of Done excerpts
- Recovered code/test/schema facts
- Unknowns workers may resolve from repo evidence
- Unknowns requiring user input

## Extraction Rules

- Read the active phase and nearby plan-level Definition of Done before
  editing.
- If the phase is high-level, recover the real contract from owning code,
  tests, schemas, generated artifacts, current behavior, and local
  instructions.
- Recovered facts support execution; they do not expand approved product scope.
- Keep the contract compact. Link to long plan sections instead of pasting them
  into every child prompt.
- Write the contract next to the plan so workers and reviewers share one
  readable briefing.

## Completion Bar

A phase is complete only when the contract is covered by implementation
evidence, required cleanup is done or explicitly walled off by the plan,
plan-required verification is satisfied, impact-aware verification covers the
changed and affected surfaces, review findings are triaged, and the requested
boundary has not been exceeded.
