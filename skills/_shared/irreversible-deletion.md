# Deleting only what you know is safe to lose

Read this before the first deletion of a cleanup run. It is about one judgment:
whether you actually know that a path is safe to lose.

Every check you run before a deletion exists to give you a positive answer: the
unsaved work is on the remote, nothing is using this, this is a copy of
something kept elsewhere, this output regenerates. A deletion is safe when you
have seen those answers for that path. When a check errors, times out, prints
nothing, cannot work on this kind of repository, or loses its result somewhere
inside your own script, you do not have an answer, and no answer is not a safe
answer. Keep the path, record what you could not establish, and carry on with
the rest of the cleanup.

## Why it matters

Deletion is the one step of a cleanup that cannot be retried. A path you keep
tonight costs some disk until the next run, which can try again with a better
check. A path you delete wrongly costs the person work that existed nowhere
else, or breaks a job that was running. These runs are unattended, so nobody
sees a check fail quietly; the person finds out days later, when they look for
the work. Checks fail most often on the unusual cases: a repository with no
commits, no remote, a nested clone, a permission boundary. The unusual cases
are also where unique work tends to live.

## What it looks like

These are the same mistake in different places. They show how to recognize
the situation; they are not a list to match against.

**A repository with no commits.** A standalone repository holds 45 untracked
files, no commits and no remote. The usual salvage runs
`git commit-tree "$tree" -p HEAD`, but a repository with no commits has no
HEAD, so the command fails and the script's commit variable is empty. The next
step, counting commits missing from the remote, prints nothing for an empty
input, and the script reads that as "nothing to save" and removes the
directory. Everything in it existed only on that disk: it was the most unique
thing in the run, and the failed salvage was the only sign. A salvage that
produced no ref you can resolve on the remote has saved nothing. Here the right
outcome is to keep the directory and report it. A root commit (no `-p`) can be
built, but with no remote there is nowhere to push it.

**A protection step that fails.** On a build server, the agent suspects a
release build folder belongs to a live agent lane and tries to mark it
protected in its candidate list. The write fails with a permission error. The
activity re-check comes back clean because the lane's build exited a moment
ago, so the agent deletes the folder, and the lane, which was between steps,
has to rebuild. The failed write was the check telling the agent it did not
have the protection it was relying on, and a lane between steps is still a
lane in use.

**A probe that does not finish.** An open-files or process check that times
out, returns partial output, or lacks the permissions it needs says nothing
about whether the path is in use. A clean result from an incomplete probe looks
exactly like a clean result from a complete one unless you notice it was
incomplete.

**A fallback that changes what is being deleted.** `git worktree remove`
refuses a path and the script falls back to deleting the directory. Sometimes
the refusal is a stale lock. Sometimes it means the path is not a linked
worktree at all but a standalone clone, with its own branches and stashes that
a linked worktree's salvage never covers. Run the fallback only once you know
which of the two you are looking at.

## Scripts you write for a batch

Most deletions in a cleanup run inside a script the agent wrote minutes
earlier, and that is where an unanswered check most often becomes a deletion.
`|| true`, a bare `except`, a default of `""` or `None`, and a loop that logs
and continues all turn a failed check into a pass that nobody sees. Make each
path's deletion depend on that path's own evidence being in hand: the salvage
commit and the remote ref that resolves to it, or a completed activity check
for that path. When the evidence is missing for any reason, the script skips
the path and records why. Read the script's output for skips and errors before
you report the batch, and report kept paths as kept, never as salvaged or
removed.

## The question to ask

Before each deletion, or before running a script that deletes many paths: what
have I seen that tells me this is safe to lose, and if I am wrong, what is
gone? If the honest answer to the first part is "nothing objected", look again.
