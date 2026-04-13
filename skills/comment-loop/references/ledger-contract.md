# Comment Ledger Contract

## Runtime artifacts

- `_comment_ledger.md` lives at repo root.
- The root `.gitignore` must contain `_comment_ledger.md` while the comment loop is active.
- `.codex/comment-loop-state.<SESSION_ID>.json` exists only while Codex `auto` is armed, with `SESSION_ID` taken from `CODEX_THREAD_ID`.

## Ledger shape

The ledger is the single source of truth for exhaustive mapping, explanation gaps, comment additions, explicit skips, and controller verdicts.

Keep this top block at the top of the file:

```md
# Comment Ledger
Started: YYYY-MM-DD
Last updated: YYYY-MM-DD

<!-- comment_loop:block:controller:start -->
Verdict: CONTINUE
Next Area:
Stop Reason:
Last Review:
<!-- comment_loop:block:controller:end -->
```

Then keep these sections in order:

```md
## Phase 1: Triage (complete/in-progress)
### 1A: Surface Inventory
| # | Surface | Kind | Why It Matters | Contract / Invariant | Downstream Dependents | Current Proof | Proof Quality | Current Explanation | Explanation Quality | Consequence if Misunderstood | Map Status |
|---|---------|------|----------------|----------------------|-----------------------|---------------|---------------|---------------------|---------------------|------------------------------|------------|

### 1B: Shared Contracts / Conventions / Gotchas Register
| # | Theme | Owning Surface | Why It Matters | What Is Easy To Get Wrong | Preferred Comment Site | Current Explanation | Status |
|---|-------|----------------|----------------|----------------------------|------------------------|---------------------|--------|

### 1C: Explanatory Surface Audit
| # | Current Site | Kind | Covers | Accuracy | Sharedness | Staleness Risk | Action |
|---|--------------|------|--------|----------|------------|----------------|--------|

### 1D: Ranked Comment Opportunities
| # | Comment Front | Surfaces | Consequence | Sharedness / Blast Radius | Explanation Weakness | Priority | Why Now |
|---|---------------|----------|-------------|---------------------------|----------------------|----------|---------|

### 1E: Comment Plan For Current Front
| Comment Front | Planned Sites | Required Proof | Why This Depth | Status |
|---------------|---------------|----------------|----------------|--------|

## Phase 2: Findings
| # | File:Line | Type | Description | Comment Plan | Status |
|---|-----------|------|-------------|--------------|--------|

## Phase 3: Comment Additions
| # | File | Kind | Explains | Why It Matters |
|---|------|------|----------|----------------|

## Decisions Log
```

## Controller block rules

- Do not rename or remove the controller markers once the ledger is live.
- `Verdict` values are exactly:
  - `CONTINUE`
  - `CLEAN`
  - `BLOCKED`
- `Next Area` is required for `CONTINUE`.
- `Next Area` may name an unfinished mapping tranche, broader comment front, or problem cluster that spans multiple files or surfaces.
- `Stop Reason` is required for `BLOCKED`.
- `Last Review` is written by `review` in `YYYY-MM-DD` form.
- `review` owns the authoritative controller verdict used by `auto`.

## Findings vocabulary

- `Type` values:
  - `CONTRACT`
  - `CONVENTION`
  - `GOTCHA`
  - `STALE`
  - `GAP`
- `Status` values:
  - `OPEN`
  - `IN PROGRESS`
  - `COMMENTED (working tree)`
  - `COMMENTED (verified)`
  - `SKIP`
  - `BLOCKED`

## Priority matrix

- `P0` = high-consequence shared contract, convention, or gotcha that is missing, misleading, or stale
- `P1` = high-consequence surface with partial explanation or a weak canonical owner comment
- `P2` = meaningful but lower-consequence surface with real explanation gaps or misleading nearby comments
- `P3` = everything else
- `SKIP` = explicitly not worth investing in now after consequence, proof quality, and current explanation were evaluated

Every `SKIP` needs a reason in `## Decisions Log`.

## Tool-signal rules

- Use existing repo-native tests, coverage, symbol indexes, doc generators, and text search first.
- If a signal is unavailable, record `unknown` in triage and explain it in `## Decisions Log`.
- Do not auto-install new tools just to satisfy the ledger.
- The exhaustive map must come from repo truth, not from canned category lists or grep-only shortcuts.

## Cleanup lifecycle

- When the workflow starts, ensure `_comment_ledger.md` exists and `.gitignore` contains `_comment_ledger.md`.
- Manual `run` leaves the ledger in place.
- `review` leaves the ledger in place.
- `auto` deletes `_comment_ledger.md` only when the final verdict is `CLEAN`.
- On clean cleanup, remove the `_comment_ledger.md` line from `.gitignore`.
- If the skill created `.gitignore` and it becomes empty after cleanup, delete `.gitignore`.
