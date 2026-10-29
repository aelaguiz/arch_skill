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

Deletion is the one step of a cleanup that cannot be retried, unless a backup holds the path. A path you delete
wrongly costs the person work that existed nowhere else, or breaks a job that was running. These runs are unattended,
so nobody sees a check fail quietly; the person finds out days later, when they look for the work. Checks fail most
often on the unusual cases: a repository with no commits, no remote, a nested clone, a permission boundary. The
unusual cases are also where unique work tends to live.

Keeping has a cost too, and it is just as real. A path kept "to be safe" stays until someone decides about it, and on
machines where agents make things and then leave, nobody ever does. On the Mac Studio, run after run deferred the same
folders, or never opened them, until 155 GB of finished tasks' output sat in the agents' home folder and CI ran with
15 GB free. A full disk stops every agent, build and Git operation on the machine. So a check that failed is a reason
to keep a path; a folder nobody opened is not. Look first, then decide.

## When the question is whether a task is over

Most of what agents leave on a disk is not a copy of anything and doesn't regenerate: QA runs, device captures,
renders, tuning runs, recovery copies, scratch. It was made for a task, and it is done when the task is. The task is
over when nothing is doing its work any more: no process is running from the folder, serving from it or writing into
it, and nobody has worked in it for a couple of days. Those are answers you can see, and they are the ones to look
for. The agent that made it is gone, so waiting for its permission means keeping it forever.

Read what the evidence is, not only that it exists. A `.env` rewritten in every checkout in the same minute is a sync
script, not work; so are a rebuilt virtualenv, a refreshed `.pid` file and a touch across hundreds of folders at once.
A `tail -f` left on the log of a render that finished two days ago is a leftover, not use, and goes with the folder.
So is a process whose parent is gone and that has done nothing for days: on the M3 Max on October 28, about 54
download workers from October 15 sat at 0% CPU, still holding 31 GB of policy files deleted a week earlier. Stopping
those exact processes is part of cleaning up after their task, and it frees what they hold open. The other way round, a note in the folder that
says who owns it and until when (an `OWNER.md` saying a batch's backend is needed until November 10) is the best
evidence there is that a quiet folder's task is still running, and a past report that saw services running from it
counts too. Work comes in bursts; two quiet days in the middle of a batch is not the end of it.

Then ask what in it anyone would come back for. Usually it is one small thing that belongs somewhere else: the final
cut of a render, a report, a configuration file. Put that where it belongs, or name it in the report, and the rest is
the task's scratch. Something nobody else has that someone would come back for (a scraped corpus with no remote,
unpublished work, the only copy of what a broken service needs to start again) needs a home or a person's decision,
not a cleanup's. On a machine whose backups are current (see
[time-machine-local-snapshots.md](time-machine-local-snapshots.md)), a wrong call about a task folder comes back from
the backup. A backup buys time, not a home: it keeps a deleted folder for weeks, not for good.

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
