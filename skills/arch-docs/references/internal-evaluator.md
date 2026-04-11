# Internal Auto Evaluator

This is the suite-only evaluator used by the Stop-hook child run for `arch-docs auto`.

Do not suggest this surface to users.

## Goal

Read the armed controller state plus current repo docs and decide one of exactly three honest outcomes:

- `clean`
- `continue`
- `blocked`

## Inputs

- `STATE_PATH`: `.codex/arch-docs-auto-state.json`
- scope metadata from the state file, including `scope_kind`, `scope_summary`, and any `context_sources` or `context_paths`
- `.doc-audit-ledger.md` when it still exists
- current repo docs in the resolved scope
- current README or docs index surfaces touched by the cleanup

## Read-only rule

- Do not modify repo files.
- Do not rewrite docs, delete files, or "help" the controller from the evaluator.
- Judge the last pass only from current repo truth plus the controller state.

## Evaluate these questions

- Is code truth stable enough that docs can be trusted?
- Did the run actually profile the repo doc system?
- Was discovery broad enough for the resolved scope?
- Are stale or duplicate in-scope docs still present?
- Has durable truth been promoted into one canonical evergreen home per topic?
- Are obsolete working docs still present without good reason?
- Are broken references or stale nav entries still present in touched scope?
- Would the next pass stay inside the same resolved scope?
- Did the last pass produce enough progress that another pass is still credible?

## Verdict rules

- `clean`:
  - no meaningful stale in-scope docs remain
  - durable truth has surviving evergreen homes
  - obsolete working-doc residue is retired or cleanly transformed in place
  - broken references in touched scope are repaired
- `continue`:
  - bounded cleanup still remains
  - another pass is credible
- `blocked`:
  - code truth is still unstable
  - the canonical home is ambiguous
  - the cleanup would need a wider or different scope than the resolved one
  - the latest pass did not materially improve the cleanup state

## Output contract

Return structured JSON only, matching the schema supplied by the controller.

Keep the reasoning fields concise and concrete.
