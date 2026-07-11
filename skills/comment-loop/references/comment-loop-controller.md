# comment-loop Auto Status

## Verdict Source

`comment-loop auto` reads the `Controller verdict` block in
`_comment_ledger.md` after each new clean `review` critic has returned and the
parent has accepted the verdict. The critic is a same-host native child by
default while the parent session is active: Codex uses
`fork_turns: "none"`; Claude uses a clean named or custom subagent rather than
a bare conversation fork or skill `context: fork` shorthand.

- `CONTINUE` means mapping work or high-impact unresolved explanation work remains.
- `CLEAN` means no credible high-impact comment work remains; delete `_comment_ledger.md` and remove the `.gitignore` entry before finishing.
- `BLOCKED` means the next pass would be speculative, low-value narration, or materially unchanged.

## Continuation Rule

Native goal mode supplies the repeated turns. Run `run`, then `review`, then
continue only while the review verdict is `CONTINUE`. The first turns may be
mapping-only; that is correct behavior, not a failure to make progress.

Outside goal mode, complete one `run` plus `review` cycle and print the next
exact command.

The clean critic and the continuation mechanism are different roles. If the
next turn must be started by a background child or an external same-provider
process after the parent turn has ended, that mechanism buys lifecycle
continuity; it does not create review independence. Choose it only when that
concrete benefit is worth the added process and integration cost under the
shared agent policy. The parent remains the owner of the ledger, result
accounting, accepted repair direction, and controller verdict.
