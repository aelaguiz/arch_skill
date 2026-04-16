# Internal Auto Evaluator

This is the suite-only evaluator used by the Stop-hook child run for `arch-docs auto`.

Do not suggest this surface to users.

## Goal

Read the armed controller state plus current repo docs and decide one of exactly three honest outcomes:

- `clean`
- `continue`
- `blocked`

## Inputs

- `STATE_PATH`: the resolved `.codex/arch-docs-auto-state.<SESSION_ID>.json` path for the current session
- scope metadata from the state file, including `scope_kind`, `scope_summary`, any `context_sources` or `context_paths`, and any repo-posture fields already recorded
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
- Did the run make and record a grounded repo-posture call?
- Was discovery broad enough for the resolved scope?
- Are stale or duplicate in-scope docs still present?
- Are stale surviving docs still present in docs that clearly should have been updated?
- Are obviously dated docs with no lasting reader value still present?
- Are point-in-time docs older than 30 days still present without explicit code-grounded current-reader value?
- Did the run trust doc self-labels such as `docs/living`, `Status: LIVING`, or `Last verified` instead of proving currentness from code?
- If the repo is `public OSS`, are any standard community-doc homes still missing?
- Are grounded topics still missing a viable canonical evergreen home?
- Has durable truth been promoted into one canonical evergreen home per topic?
- Did the run preserve a stale wrapper that should have been folded into an existing evergreen home instead?
- Are confusing docs still obscuring how readers should use, operate, or understand the system?
- Are obsolete working docs still present without good reason?
- Are broken references or stale nav entries still present in touched scope?
- When time context mattered, did the run inspect git history and the last meaningful content change?
- Did the run make a dead doc look current through metadata-only freshness edits?
- For narrowed scopes, would the next pass stay tied to the same requested topics or their grounded overlaps?
- Did the last pass produce enough progress that another pass is still credible?

## Verdict rules

- `clean`:
  - no meaningful stale in-scope docs remain
  - no stale surviving docs remain in reader-critical docs that should have been updated
  - no obviously dated low-value docs remain unless they still serve a clear current reader need
  - no point-in-time docs older than 30 days survive without an explicit code-grounded current-reader justification visible in the cleanup record
  - doc self-labels and freshness metadata were not treated as proof of currentness
  - if the repo is `public OSS`, the standard community-doc baseline exists as standalone canonical homes
  - no grounded topic is still missing a viable canonical evergreen home
  - durable truth has surviving evergreen homes
  - no stale wrapper survived when its durable truth could have been folded into an existing evergreen home
  - confusing docs that still matter have been clarified enough for current readers
  - obsolete working-doc residue is retired or cleanly transformed in place
  - no doc was made to look current through metadata-only freshness edits
  - broken references in touched scope are repaired
- `continue`:
  - grounded docs-health work still remains
  - more stale, missing, confusing, or low-value docs work remains
  - more delete-first retirement work remains for old point-in-time docs, stale wrappers, or unjustified survivors
  - another pass is credible
- `blocked`:
  - code truth is still unstable
  - a required canonical home is still genuinely ambiguous after profiling repo gravity and applying the default `private/internal` posture
  - for a narrowed scope, the cleanup would need a materially wider or different topic scope than the resolved one
  - the next pass would drift into speculative or taxonomy-first reorganization
  - the latest pass did not materially improve the cleanup state

Repo-posture ambiguity by itself is not a blocker. Default `private/internal` unless strong `public OSS` evidence exists. Age alone is also not a blocker, but in this repo family it should create a strong 30-day stale-doc presumption.

## Output contract

Return structured JSON only, matching the schema supplied by the controller.

Keep the reasoning fields concise and concrete.
