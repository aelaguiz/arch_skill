# Message Quality

The goal is an informative commit stream, not prettier one-line subjects. A
future reader should be able to scan `git log` and understand what the branch
was trying to accomplish, how the work unfolded, and where plan context shaped
the change.

## Message shape

Use the smallest message that carries the truth:

```text
Imperative subject naming the concrete change

Optional body explaining why this step exists, what it enables, or how it fits
the surrounding plan. Include plan context only when evidenced.

Existing-Trailer: preserved exactly
```

Good subjects are specific and action-led:

- `Add local-only commit rewrite safety checks`
- `Document recovery path for rewritten commit messages`
- `Wire commit history skill into install surfaces`

Weak subjects hide the work:

- `WIP`
- `updates`
- `fix stuff`
- `more changes`
- `cleanup`

## What to inspect per commit

For each commit, inspect enough repo truth to avoid guessing:

- old subject and body
- `git show --stat --name-status`
- changed files and nearby context when the file names are not self-explaining
- plan docs or worklogs touched by that commit
- active arch-plan evidence, if any
- existing trailers

Do not write the same high-level branch summary into every commit. Each commit
should explain its own step.

## Active arch plans

Call out an active arch plan only when the evidence is real:

- the user named a `docs/<...>.md` plan path
- controller state names a `doc_path`
- exactly one strong canonical full-arch doc candidate is visible
- the commit itself touches or clearly implements that plan

Useful body line:

```text
Arch plan: docs/COMMIT_HISTORY_AUTHORING.md, phase 2.
```

If the plan path is known but the phase is not, omit the phase. If more than
one credible plan exists, ask the user to choose. If there is no evidence, do
not mention an arch plan.

## Trailer preservation

Preserve existing trailers exactly. Common examples:

- `Co-authored-by`
- `Signed-off-by`
- `Change-Id`
- `Reviewed-by`
- `Fixes`

Do not move trailers into prose. Keep the final trailer block as a trailer
block.

## Anti-patterns

- Inventing issue numbers, test runs, reviewers, or plan paths.
- Repeating file names instead of explaining behavior.
- Writing a broad PR description as every commit body.
- Claiming a commit completes a phase when it only contributes to it.
- Dropping useful old body details because the subject became better.
- Rewriting commit boundaries under a message-only request.
