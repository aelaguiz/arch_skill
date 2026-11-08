# Before a deletion

Read this before the first deletion of a cleanup run. Two questions decide every deletion: is anything still using this, and if it holds work that exists nowhere else, has that work landed somewhere? You answer both by looking, and on these machines looking is cheap.

## Keeping costs as much as deleting

A wrong deletion costs someone work, or breaks a job between its steps. A wrong keep costs the disk, and on these machines a full disk is the more common harm by far. On the Studio, a disk at 117 MB free corrupted the filesystem inside its Docker VM, and an agent had to rebuild Redis from saved keys. For weeks, nightly runs on several machines deferred the same folders "until someone decides". Nobody did, because the agents that made those folders had gone. So the bar is not certainty. The bar is that you looked for use, found none, and saved anything unsaved.

## A check that failed is not an answer

Every check you run before a deletion exists to give you a positive answer: the salvage commit is on the remote, nothing in the snapshot uses the path, the output regenerates. When a check errors, times out, prints nothing, or loses its result inside your own script, you don't have that answer. Keep that path for this run, say why, and carry on with the rest. That is different from a folder you don't understand yet. Not understanding a folder is a reason to open it and look, not a reason to keep it.

The cases where a failed check turns into a loss look alike:

- **A repository with no commits.** The usual salvage builds `commit-tree "$tree" -p HEAD`. With no HEAD that fails, the commit variable comes back empty, a count computed from the empty value prints nothing, and a script reads that as "nothing to save". A clone holding 45 untracked files and no remote was removed that way. A root commit (no `-p`) could have saved it into the local salvage repository.
- **A probe that didn't finish.** An `lsof` that came back empty or a `ps` that was denied looks exactly like "no use" unless you notice it was incomplete. A snapshot with hundreds of processes is a snapshot. A tiny one is a failure.
- **A fallback that changes what is deleted.** `git worktree remove` refuses, and the script falls back to `rm -rf`. Sometimes the refusal is a stale lock. Sometimes the path is a standalone clone with branches and stashes that a worktree salvage never covered. Find out which before you fall back.
- **A protection that didn't apply.** Writing a path into a keep list fails with a permission error, the activity re-check comes back clean because a job is between steps, and the path is deleted. The failed write was the warning.

## Scripts you write for a batch

Most deletions happen inside a script written minutes earlier, and that is where an unanswered check quietly becomes a deletion. `|| true`, a bare `except`, a default of `""` and a loop that logs and continues all turn a failed check into a pass nobody sees. Make each path's deletion depend on that path's own evidence: the salvage ref that resolves to the commit, and the snapshot that shows no use. Read the script's output for skips and errors before reporting, and report kept paths as kept.

## The aim

Never point a deletion at a home folder, a workspace root or a mount, and never at a parent of something you're keeping. Resolve the path, delete that path, and check that it is gone. A session once ran `rm -rf` on the Studio's whole home folder and emptied about 72 workspaces, with their logins and CI runners. Every other mistake in this guide costs one folder.

On a Mac whose Time Machine backups are current ([time-machine-local-snapshots.md](time-machine-local-snapshots.md)), a wrong deletion comes back from the backup drive for about a month, unless the folder was excluded from backups (`tmutil isexcluded <path>`). The home server has no such backup, so there, a deletion is final.
