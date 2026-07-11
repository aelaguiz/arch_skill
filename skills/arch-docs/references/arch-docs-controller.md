# arch-docs Auto Status

## Verdict Source

`arch-docs auto` uses a new clean review/evaluator child. While the parent
session is active, use a same-host native critic by default: Codex dispatch sets
`fork_turns: "none"`, and Claude uses a clean named or custom subagent rather
than a bare conversation fork or skill `context: fork` shorthand. Give the
critic `.doc-audit-ledger.md`, resolved scope, and current-code paths directly;
use bounded or full inherited context only for a named chat-only dependency.

The critic reads `.doc-audit-ledger.md` and current code, then recommends:

- `CONTINUE` when another grounded pass is credible for the resolved docs-health intent.
- `CLEAN` when the resolved stop condition is satisfied; the default pass deletes `.doc-audit-ledger.md` before the run ends.
- `BLOCKED` when the next pass would be speculative, taxonomy-imposing, disconnected from a narrowed scope, or materially unchanged.

Use the strongest read-only capability available and explicitly prohibit the
critic from editing or writing any file. It may not create children or invoke
delegation, consult, or review skills unless the parent assigned a bounded
nested scope and budget. The parent captures current git status and the
relevant diff before dispatch, compares current state afterward, accounts for
the critic result, spot-checks its evidence, and owns the accepted verdict and
any next-pass repair decision.

## Continuation Rule

Native goal mode supplies the repeated turns. Run a grounded DGTFO pass, run
the new clean review, then continue only while the accepted review verdict is
`CONTINUE`.

In this repo family, keep treating point-in-time docs older than 30 days as
presumptively stale until the pass records explicit code-grounded current-reader
value for each survivor. A pass that mainly refreshed metadata labels is not
progress.

Outside goal mode, complete one pass plus review and print the next exact
command.

The clean critic and the continuation mechanism are separate. If a background
child or external same-provider process is needed after the parent turn ends,
its benefit is lifecycle continuity, not evaluator freshness. Choose it only
when that concrete benefit is worth its process and integration cost under the
shared agent policy.
