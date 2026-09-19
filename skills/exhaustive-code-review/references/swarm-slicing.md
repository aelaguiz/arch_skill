# Dividing The Review Among Children

Read this when the review will use child reviewers: the user named a worker
type or a count, or the target is large enough that parallel slices improve
coverage. Apply `../../_shared/agent-orchestration-policy.md` for transport,
starting context, pinning, isolation, and cleanup. This file owns only how the
catalog and the target are divided, what a child is told, and what the parent
does with the returns.

The division of labour is the point. Children are cheap readers who each hold a
few checks. The parent keeps the judgment: what applies, what is real, what is
in scope, and the verdict.

## Which slices apply

`review-catalog.md` lists every slice file, its checks, and what each needs in
hand. A slice applies when the review target actually contains its inputs: a
diff, the request or issue, a completion claim or PR description, tests, run
evidence, or screenshots and a mock. Leave out slices
whose inputs are absent and record them in `coverage.md` as not applicable with
the missing input. Do not invent an input to make a slice apply.

## Cells

The unit of work is a cell: one slice over one path family. A change that one
child can hold in context has a single path family, so its cells are its
slices. Split a larger change into path families first, by owner or subsystem,
so that each family plus one slice fits comfortably. Checks that compare the
whole change against the request (scope, size, completion claims) always get
the whole change summary even when other slices are split by path.

Every cell has exactly one owner. No cell is left unowned, and two children
never own the same cell.

## Dealing cells to workers

Interpret the user's words with judgment; they are ordinary language, not
parameters.

- A type and a count: the count is how many children run at once. If it covers
  every cell, give each child one cell and use spare workers to split the
  largest path families further. If there are more cells than workers, run
  further waves of the same size instead of loading one child with many
  slices. A child that holds more than two slice files reads each one less
  carefully and starts returning "clean" on a sample, so two is the ceiling.
- A type and no count: one child per cell, launched in waves that fit the
  host's concurrency.
- Neither: choose a proportional number of cells and children for the change,
  as the main workflow describes.

Resolve the named type under the shared policy and
`../../_shared/native-child-capabilities.md`. If this host cannot start a
native child of that type, stop before dispatch and tell the user which types
it can start. Never substitute a different model or effort silently, and record
in `coverage.md` the type that actually ran and whether running the code was
allowed. A child that ran something it was not allowed to run is recorded as a
violation in `coverage.md`; what it saw is still evidence, and the parent's
repository-state check tells you what the run left behind.

## The child brief

Apply `$prompt-authoring` to the populated brief. Give each child:

- the review target: repository path, base and head or the path set, and where
  to find the request, plan, PR description, or evidence that its checks need;
- its cell: the slice file or files to read and the paths it owns, and that
  its searches stay inside the target repository and those paths plus their
  direct callers;
- the instruction to read `references/checker-rules.md` in full and then its
  slice files, with their installed paths;
- in its first lines, whether the user allowed running the code. By default
  they did not, and the child reads only: no file created in the target, no
  build, test suite, generator, or install;
- nothing else. Do not pass your own suspicions, a summary of what you think is
  wrong, or the expected outcome. A child that is led will confirm the lead.

Start each child clean and read-only, as the shared policy describes.

## What the parent does with the returns

1. Account for every cell: each assigned check came back as finding, clean, or
   could not evaluate, in the return's opening lines. A return that narrates the
   change, reports test runs, or omits an assigned check id is incomplete:
   re-dispatch that cell with the same brief. Do not fill the gap by inferring
   a state from the narrative.
2. Compare repository state with the state before dispatch.
3. Open the code for every reported finding and decide it yourself against the
   catalog entry: accept, reject with the reason, or merge with a duplicate
   from another cell. Treat a "clean" the same way when the check compares the
   change with the request: if the child cleared a user-visible element by
   tracing it to a line in an issue, plan, or spec the agent wrote, find the
   user's words behind that line yourself before accepting the clean. A finding goes under the check whose "Block when" it
   satisfies as written. Do not invent an inverse, extended, or related form of
   a check; if no entry's block condition fits, it is at most an observation.
   One defect is one finding, however many checks saw it:
   report it under the check whose comparison is most direct and list the other
   check ids as corroboration. A verdict with a dozen required repairs that
   describe three defects is harder to act on than one with three. A child's report is evidence. It is never a finding until
   you have verified it.
4. Apply the quiet conditions in `checker-rules.md`, the entry's own "Do not
   block when" cases, and, for a fixed-scope or history-backed change,
   `../../_shared/scope-and-convergence.md`. Reject a finding whose repair
   would extend something the catalog treats as the defect, such as applying
   more masking to diagnostic data, adding another flag, or adding more proof
   machinery. When two returns pull in opposite directions, the catalog entry
   decides which one stands.
5. When the change fixes a failure, apply C-17 yourself as well, whatever the
   children returned: read the description and the issue for the cause the
   change claims, and find the hunk that touches it. A symptom made quieter
   with the cause unknown is a required repair, and it goes first.
6. Sort what remains into what must be repaired before approval and what is
   only worth noting. Drop pedantic and hypothetical items. A verified finding
   is a required repair when the request's own terms are unmet at head, or when
   the change leaves its own stated outcome unfinished. Do not downgrade it
   because a later step, another acceptance item, another owner, or a follow-up
   could address it; only the requester can defer it, so name the decision that
   is needed instead of making it. For work nobody requested, the repair
   target is removal; the option of approving it belongs to the requester and
   takes one clause, not a finding of its own.
7. Write the artifact and give one verdict.

If the same finding keeps arriving from a check as noise, the repair is to the
catalog entry's wording, not a filter.
