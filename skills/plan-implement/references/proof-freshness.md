# Proof Freshness

Proof is cached knowledge with explicit invalidators. The goal is not to avoid
verification. The goal is to run checks when they matter and avoid rerunning
them because context was lost.

## Record Every Useful Proof Entry

For each meaningful check, supplied result, manual validation, generated output,
or accepted prior proof, record:

- proof name or context
- scope covered
- result or supplied status
- plan obligation or impacted behavior covered
- freshness condition
- rerun trigger

Use the implementation log's `Proof Freshness Ledger` for this.

## Fresh Proof

Proof can stay fresh when:

- it covers the same behavior
- no touched file, dependency, config, generated artifact, data shape, caller,
  prompt, doc, or route can invalidate it
- the plan does not require fresh proof
- no review finding makes it suspect
- no new code landed after the proof on a relevant path

If unsure whether a later change invalidates proof, inspect the changed path
and impacted callers before rerunning broad checks by habit.

## Stale Proof

Proof becomes stale when:

- the files, symbols, schemas, generated artifacts, prompts, docs, config, or
  callers it covered changed
- a new side door or caller path enters scope
- a review finding challenges the behavior it claimed to cover
- the plan explicitly requires fresh proof at the phase or final boundary
- local instructions require a fresh check for the changed surface
- a failing related check contradicts it

## Choosing Checks

Start with:

- the plan's stated validation obligations
- changed code surfaces
- plausibly impacted adjacent behavior
- review findings that need proof after repair
- high-risk integration seams

Prefer targeted integration-level proof when risk crosses modules, commands,
persistence, generated artifacts, UI paths, agent/tool contracts, or runtime
boundaries.

Unit tests are useful for tricky isolated rules. They are weak when they only
prove the compiler, framework, mocks, or implementation details.

## Examples

```text
Proof: `uv run pytest tests/test_command_service.py`
Covered: command metadata routes through canonical service
Fresh until: command service, metadata schema, adapter registration, or caller
routes change
Rerun trigger: changes to those files, a review finding about command routing,
or a plan requirement for fresh proof
```

```text
Proof: supplied CI pass from user
Covered: broad regression context only
Fresh until: local changes after that CI pass
Rerun trigger: new commits after CI, changed shared infrastructure, or release
gate requiring current CI
```

```text
Proof: visual simulator pass from prior slice
Covered: first narrow end-to-end render path
Fresh until: renderer, route, fixture, layout contract, or asset loading path
changes
Rerun trigger: any touched render path or a review finding about visual drift
```

## Anti-Patterns

- Rerunning the same broad suite after every compaction.
- Treating a green unit test as enough proof for a cross-module integration
  change.
- Ignoring prior proof because it is not in chat history.
- Marking proof fresh without saying what would stale it.
- Running checks only to satisfy ceremony when no changed or impacted surface
  can be named.
