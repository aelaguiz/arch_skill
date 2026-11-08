---
name: disk-cleanup
description: "Free disk space on Amir's machines by finding what is still alive and clearing the rest: old task checkouts and worktrees (unsaved work pushed to a salvage branch first), finished experiments' bulk output, leftover QA runs, captures and renders, reproducible builds and caches, stopped task simulators, emulators and VMs, inactive Prime state, and Time Machine snapshots the backup drive already has. Use for a full disk, a free-space target, developer junk piling up, or nightly housekeeping on the M5, the M3s and Mini 1; the Mac Studio and home server skills build on its judgment. Not for Codex's own databases and session history ($codex-cleanup)."
metadata:
  short-description: "Find what's alive, clear the rest, keep unsaved work"
---

# Disk Cleanup

A full disk stops every agent, build, CI job and Git operation on the machine, and Amir's machines fill fast. Dozens of agents start checkouts, experiments and QA runs every day, and their sessions end. Your job is to give the disk back while keeping what is still alive and what can't be replaced.

## Almost everything here is dead

A machine has two or three live projects at a time. Almost everything else on its disk is left over from tasks whose agents are gone. The agent that made a folder isn't coming back for it, won't be asked about it, and won't notice it's gone, and nobody else knows the folder exists. A folder you defer "for someone's decision" stays until the next run defers it again, so deferring is deciding to keep it forever.

So don't try to prove each folder is dead. You can't, and a cleanup that needs proof keeps everything. Find what's alive, which you can see, and treat the rest as done. On the home server in November, 10 of 223 RustAI checkouts were live. Removing the other 213 took the main disk from 24 GB free to over 300 GB, and all their unsaved work fit in 450 MB.

## What alive looks like

Something alive leaves marks you can check in a few minutes:

- **Something runs from it**: it has the folder open, works in it, or names it in its arguments. That covers a training run, a server, a build, a QA stack, or an agent session working there. Agent sessions are processes too: when none of a session's processes are left, its agent is gone.
- **Something points at it**: a service definition, a scheduled job, a container's mount, or a link from a live checkout.
- **Someone is working in it**: commits, edits or new output in the last couple of days, on a task that isn't finished. A merged or closed PR finishes the task now, whatever the clock says.
- **Someone wrote down that it's needed**: a note with a name and a date that hasn't passed.

[checking-use.md](references/checking-use.md) has the commands. You take one snapshot of every process and match all your candidates against it at once, then check the few other places use hides. Read it before the first deletion. It gets the answers in about a minute instead of one slow probe per folder.

Then read what you found. A server answering players, a training run writing checkpoints, a build that started an hour ago: that's use. Some processes are only leftovers of finished work: a `tail -f` on the log of a job that ended, a shell nobody is attached to whose parent is gone, a language server indexing a checkout nobody edits, a tool server that happened to start in that folder. Stopping those exact processes is part of cleaning up after them. One fresh file doesn't make a big folder alive either, so look at what was written. A script that rewrites `.env` in every checkout in the same minute is not work in any of them.

The other way round matters as much:

- On the home server, nothing had the `policies_hydrated_20260611` store open, but the live `rustai` checkout's `policies` link pointed into it.
- A Daily Puzzle backend on the Studio had been quiet for days, and an `OWNER.md` in it reserved it until November 10.
- A QA folder whose files were a week old was serving that afternoon's release-candidate test from its binaries.

Each of those was alive, and each was one look away.

Before deleting anything, write down the live projects on the machine in a line, for example: "home: Amir's `rustai` checkout, the Play vs AI serving worktree, the `ms12` round-26 runs, the 1500-hand Sit & Go runs". If you can't name them, you haven't looked yet.

## What dead things leave behind

**Checkouts** are caches of GitHub. The only thing of value in a dead one is work that exists nowhere else: uncommitted edits, commits not on the remote, stashes. That is small. Delete the dead checkouts with nothing unsaved first, because that takes seconds and frees the most space. Then push the rest to salvage branches and delete each one as its push lands. Submodules, dirty files, ignored files, an open PR, and a name without `-worktrees` are not reasons to keep a dead checkout. [worktrees-and-measurement.md](references/worktrees-and-measurement.md) has the salvage commands, including where work with no remote goes.

**Experiments** leave an answer. People come back for what a run found: the readings, the report, the manifest, the few small files that say what happened. They also come back for the winner, if it shipped. The bulk got the run to its answer: checkpoints and policies of finished runs, captures, generated datasets, intermediate rounds, logs. When nothing runs the experiment and nothing has been written for days, keep the small record and remove the bulk. What a run cost (28 billion iterations, a week of compute) says nothing about whether anyone needs it now. The newest candidates of a live project, and the baseline its current work compares against, are part of that live project.

**Task output** (QA nights, device captures, renders, downloaded builds, recovery copies, scratch) is done when its task is. Usually one small thing in it is worth keeping, such as a final cut, a report or a configuration file. Keep that and remove the rest.

**What regenerates** (build output, package caches, transfer mirrors) can go when nothing is building from it. Clearing a cache a running job refills within the hour gains nothing, and on a Mac with Time Machine it briefly costs double. A cache nothing uses gains its whole size.

**Devices, VMs and databases**: a stopped simulator, emulator or Colima VM named for a finished task is a task copy. A database or VM disk belongs to whatever uses it. The live service's database stays even when it is quiet tonight. A finished project's database, its stopped containers' volumes and its old backup dumps go with the project. The machine's main development VM and the databases in it stay.

## What stays

The list is short because few things belong on it:

- what is alive, as above;
- credentials, keys and login state;
- what serves players or production, and the policy stores it reads, including the RustAI policy drives;
- live databases and the service volumes under them;
- Amir's own files: documents, photos, downloads, legal and personal projects, and his working copies on his own laptop;
- one working copy of each live project, and shared Git owners such as `~/workspace/.psmobile-git-root`.

Before you add anything to this list, ask who would come back for it and what they would do with it.

## Safety lines

These hold in every case:

- **Delete only what you looked at.** Use its full resolved path. Never aim a deletion at a home folder, a workspace root, a mount, or a parent of something you're keeping. A session that ran `rm -rf` on the Studio's home folder emptied about 72 workspaces and took its logins and CI runners with it.
- **A backup that didn't land isn't a backup.** Delete a checkout with unsaved work only after you have seen its salvage commit on the remote, or in a local salvage ref. If a push fails, a commit id comes back empty, or a check errors, that checkout stays this run and you say why.
- **A failed use check has told you nothing.** If the snapshot came back empty, a permission was denied or it timed out, run it again, or leave the paths it covered for this run. A folder you didn't understand is different: that isn't a failed check, it's a reason to look inside.
- **Leave policy payloads unread.** Never read, hash, expand or fetch RustAI multiplayer policy payloads to decide anything. Their manifests, names, dates and links are enough.
- **Keep secrets off the page.** Never print command lines, environments or credential files. The use checks report process ids and names only.
- **Stop only exact leftovers.** Stop a process only when you've identified it as a leftover of finished work, by its pid, and never by name pattern. Other people's running work stays running.

## The run

1. Measure free space on each volume with `df -k`. On a Mac with Time Machine, read [time-machine-local-snapshots.md](../_shared/time-machine-local-snapshots.md) first, because deletions don't show as free space until the snapshots holding them go.
2. Make one size pass that also records each folder's newest file. Save it for the rest of this run and for the next one.
3. Take one process snapshot and run the other use checks for all the large candidates at once.
4. Name the live projects, and put the paths you're keeping in the run's `keep.txt`, one per line. The removal command in the worktrees reference refuses those paths and anything that holds them. Everything else that's large is a candidate.
5. Delete the dead checkouts with nothing unsaved and the dead output. Salvage the rest in a batch, and delete each one as its push lands. Take a fresh snapshot before each batch, not before each path.
6. Clear experiments' bulk, task output, unused caches, and stopped task devices and VMs.
7. On a Time Machine Mac, delete the local snapshots the backup drive already has, then measure again.
8. Write a short private record:
   - free space before and after;
   - the live projects you named;
   - what went and how big;
   - salvage refs;
   - for each of the largest things you kept, a reason a person would accept. "A server runs from it" is a reason. "Could not establish disposability" is not.

Earlier reports tell you where things are, not what to decide. Decide each large folder again from what you see now. A free-space target is a floor, not a finish line: keep clearing dead things after you pass it. When something truly is Amir's call (his own files, or something that serves players and looks unused), leave it and say so in one line. Don't build a list of deferrals.

## Other machines and owners

- The Mac Studio and the home server have their own skills, `$mac-studio-disk-cleanup` and `$home-disk-cleanup`. They carry each machine's map, schedule and report format, and use this judgment.
- [known-locations.md](references/known-locations.md) lists where space usually sits on the Macs.
- For a cluster-wide request, `$machines` gives the routes.
- Codex's own databases and session history belong to `$codex-cleanup`.
