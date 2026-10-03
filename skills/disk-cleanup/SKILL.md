---
name: disk-cleanup
description: "Reclaim disk space on Amir's developer Macs by deleting old task checkouts and worktrees after pushing any unsaved work to a salvage branch, plus reproducible builds and caches, unused task simulators, and authorized inactive Prime state. Use for a full disk, accumulated developer junk, daily housekeeping, or a free-space target. Reuse inventories while refreshing Git registrations and live activity. Protect canonical checkouts, active work, credentials, model policies, and VM volumes; verify actual free space. Use codex-cleanup for work confined to Codex SQLite/session maintenance."
metadata:
  short-description: "Fast developer disk cleanup with work preserved"
---

# Disk Cleanup

Restore the user's requested disk headroom quickly while keeping their work
recoverable and their running tools usable. Optimize for substantial reclaimed
space and a shorter next cleanup. A long inventory or a small cache deletion
does not finish a request for hundreds of gigabytes.

**Keep the work, not the copy.** Most of the disk goes to copies: task
checkouts, their build output, per-task simulators and emulators. The only thing
of value in an old copy is work that exists nowhere else, and Git can save that
in seconds. Save it, then delete the copy. Keeping dead copies because they
contain submodules, uncommitted edits, or ignored files is not caution. It fills
the disk, and a full disk stops every agent, build, and Git operation on the
machine. That is the harm this skill exists to prevent. What stays: canonical
checkouts, anything in live use, work someone did recently, and data that is
not a copy of anything (credentials, model policies, VM volumes).

**Delete only what you know is safe to lose.** Every check before a deletion,
such as the salvage reaching the remote or nothing using the path, has to come
back with an answer you have seen for that path. A check that errors, times
out, prints nothing, or fails inside your own batch script has not answered;
keep that path, record why, and keep cleaning elsewhere. Before the first
deletion, read [irreversible-deletion.md](../_shared/irreversible-deletion.md):
its examples show how a failed check turns into lost work.

For routine or unattended runs without a numeric target, remove the obvious
authorized accumulation and identify the largest remaining opportunities. Reuse recent
inventories and inspect likely owners; do not repeat an exhaustive whole-disk
scan or invent a hundreds-of-gigabytes target every night. Finish when the
clear, authorized candidates are handled. When an action needs approval, leave
the data intact and report the exact opportunity instead of waiting for input
or expanding deletion scope to force a larger result.

Amir's daily housekeeping authorization includes old task checkouts and
worktrees (after salvaging their unsaved work as described below), confirmed
unused task simulators and emulators and their saved state, and inactive
Prime session/recovery state. Perform that cleanup without asking again,
including the salvage commits and pushes. Preserve active or recently used
devices associated with ongoing work, credentials, canonical checkouts, model
policies, and VM volumes. A current request to preserve a storage class
overrides this daily default. Cache-only cleanup is incomplete while obvious
authorized worktree, simulator, or Prime-state wins remain unchecked.

## When to use

- "I'm running out of disk space. Find the caches and old worktrees and clean them up."
- "Get this coding machine back to 1 TB free."
- "Clean up the developer junk again without scanning the whole disk."

This skill owns local disk housekeeping. It does not delete source functionality,
retire documentation, perform arbitrary application database maintenance, or
administer other machines.
For work confined to Codex's session/log SQLite state, use `$codex-cleanup` and
its live-process rules. A large `~/.codex` directory does not make stopping all
agents a prerequisite for cleaning unrelated worktrees.

## Start with the known map

Read [known-locations.md](references/known-locations.md) first. It gives the
likely large owners and the saved-inventory locations. Read
[worktrees-and-measurement.md](references/worktrees-and-measurement.md) before
removing checkouts or interpreting reclaimed bytes; it has the salvage commands.

1. Measure capacity and available bytes on the volume containing `~/workspace`.
   Carry forward the user's target and cleanup authorization from the conversation.
   Distinguish a target for total free space from an amount to reclaim.
   Establish the protected canonical roots below before selecting any candidates.
2. Look for a recent local cleanup manifest or report. Reuse its paths, recorded
   sizes, and recovery information as discovery hints. Refresh current existence,
   Git state, and process use before acting. Enumerate current worktree registrations
   once per common Git directory on every run, including routine runs, and find
   top-level task copies under `~/workspace`. Reuse recorded paths and
   measurements, never a previous report's conclusion that a checkout must stay.
   This targeted Git inventory is not a whole-disk scan.
3. Select enough large candidates to plausibly reach the target, or the clear
   wins for routine housekeeping without a target. Old task checkouts usually
   hold the most space; start there. Inspect and measure candidates once. Save
   bulky results locally and report totals and the largest owners. Do not
   recursively scan `/`, the home directory, `~/workspace`, and their children
   concurrently: those scans repeat the same expensive traversal.
4. Execute the authorized cleanup and measure the result. If an applicable
   instruction requires confirmation that the conversation has not supplied,
   prepare the exact paths, salvage plan, and estimated space first, then
   ask once. A preview-only request remains read-only.
5. Continue through the next material owner when actual free space is still
   below target. Broaden discovery only when the known locations do not explain
   the usage or cannot supply the needed reclaimable space. Stop when the target
   is reached, or identify the concrete remaining data that requires a user decision.

## Canonical checkouts are protected

A canonical checkout is the primary working copy of a repository:
`~/workspace/psmobile`, `psagentspace`, `prime-agent`, `arch_skill`, `rustai`,
`puzzledb`, `cjdev`, `website`, `lessons_studio`, the shared Git owner
`~/workspace/.psmobile-git-root`, and any other top-level project that is the
only or primary checkout of its repository. Never remove, rename, replace, or
empty one. Being old, clean, or registered as a linked worktree does not change
that.

A second copy of one of those repositories is a task checkout, wherever it
sits: `~/workspace/psmobile-5966`, `psmobile-l10n-m8`, `psmobile-wt-6509-before`,
`rustai2`, `puzzledb-l10n-m9`, everything under a `*-worktrees` collection, and
`.claude/worktrees/` entries nested inside a canonical checkout. Tell the two
apart by repository identity (the same common Git directory or origin remote as
a canonical checkout), not by location or name. When you cannot tell which of
two copies is the primary one, keep both and report them.

Before cleanup, record the protected paths and their resolved destinations.
Exclude those roots, their own files, and any ancestor whose removal would
contain them from every deletion list, including old manifests and scripts.
Resolve aliases and symlinks when checking containment. Canonical build and
dependency folders stay untouched unless the user asks for that folder's
cleanup. Deleting a task worktree nested inside a canonical checkout is
allowed; deleting the canonical checkout's own files is not.

Any reused or newly written cleanup script must enforce this protected set
before every deletion. A safe preview does not compensate for an executable
that lacks the same lexical and resolved containment checks.

## Old task checkouts: salvage, then delete

A task checkout lives as long as its task. It is old when nothing is using it
and nobody has worked in it for two days: no process has it as a working
directory, has files open in it, or names it on a command line, and its newest
commit, reflog entry, and edited file are all older than that. Amir set the same
two-day limit for the Mac Studio's worktrees. Build output, Git maintenance,
and indexing are not work; Git maintenance can rewrite reflog mtimes in every
worktree at once, so read commit and reflog times rather than file mtimes under
`.git`. Salvage makes deletion recoverable, so doubt about a dead-looking
checkout is settled by salvaging and deleting it, not by keeping it. Keep a
checkout when something is using it now or someone worked in it recently.

None of these is a reason to keep an old checkout:

- Uncommitted, staged, or untracked work: commit it to a salvage branch and push it.
- Commits that are not on the remote, including a detached HEAD: push them to a salvage branch.
- Submodules or nested repositories: salvage any unpushed work inside them the
  same way, then remove the parent with force. Git refuses a plain removal
  when submodules are present; that refusal is not a signal to keep.
- Ignored files (`.env`, logs, downloads, reports, generated assets,
  dependencies): they go with the checkout. A `.env` in a task checkout is a
  copy of configuration kept elsewhere, not one of the machine's credential
  stores. Never move ignored files to a preservation folder; moving files on
  the same disk frees nothing.
- An open PR or a task branch on the remote: the branch lives on the remote,
  and the checkout is only a copy of it.
- A top-level location or a name without `-worktrees`.

The one ignored class that is not a copy is model policies and training-run
output (RustAI). If an old checkout holds them, keep that checkout and report
it.

The salvage protects only what would otherwise be lost, so it needs no
ceremony: one commit with hooks skipped, pushed to
`salvage/<checkout-name>-<YYYYMMDD>` on the repository's own remote. Do not
commit onto, push to, or rewrite the task's own branch (it may back an open
PR), and do not delete branches. Keep
credentials and oversized generated binaries out of the salvage commit; if a
push is rejected for a secret or file size, drop that file and push again. If
the remote is unreachable, keep the salvage commit as a ref in the canonical
repository instead. Keep the checkout only when the work can be saved neither
way, and report why.

Refresh activity close to each deletion and throughout long batches. If a
candidate became active, skip it and continue. Record the original path,
common Git directory, HEAD, salvage ref and pushed commit, and a one-line
summary of what was discarded, so the checkout can be recreated.

Checkouts that stay because they are in use or recent keep their build output
too; the task may be between steps. A checkout kept only because its work could
not be saved, or because it holds model policies, can still lose its
reproducible build output (see the reference).

## Caches, simulators, and other storage

For caches and build folders, establish what regenerates them and whether a
running process uses them. Verify that selected build paths contain no tracked
source before deleting them. Keep credentials, live SQLite/WAL state, browser
profiles, and VM volumes outside generic cache deletion. Use their owning tool
when those storage classes become necessary to the task.

Protect shared caches while their owning builds or tools are active, even if
a snapshot shows no open file in that cache. Include process command-line path
references and parent directories in activity checks without printing secrets.
If another process recreates a removed path, leave the new contents alone; do
not retry deletion against ongoing work.

For simulator and emulator devices, Prime state, Docker/Colima storage, or suspected duplicate models,
read the corresponding guidance in [known-locations.md](references/known-locations.md).
A task simulator or emulator is a copy like a task checkout: judge it by its
owner, clients, last use, and live activity. Shutdown alone proves neither that
it is disposable nor that it must be kept forever. Two policy paths may be
aliases or different training runs, so keep them outside this cleanup.

## Leave a faster next run

Keep a small private local report under `~/disk-cleanup-<date>/` or an existing
cleanup-report directory. Record the host and volume, start/end free bytes,
examined owners, selected paths and measurements, removals, salvage refs, skips,
and recovery instructions. Record per-candidate skip reasons so the next run can
refresh decisions efficiently. Keep secrets out of report contents.

Existing local cleanup scripts are optional implementation artifacts. Read them
before reuse and check their scope, freshness checks, salvage behavior, and
failure handling against this skill. The skill must also work on a machine
where no previous script or manifest exists.

Report actual before/after free space, actual bytes reclaimed, the largest
removed categories, the salvage branches pushed, what was skipped and why, and
the local report path. State whether an explicit target was reached; for
routine runs, state whether any clear wins remain and name approval-dependent
opportunities with estimates. Label estimates separately; do not add nested
folder sizes or present `du` totals as measured free space. Take the completion
measurement after verification. If the disk remains busy, select a cleanup
batch with a few gigabytes of headroom beyond the requested threshold so
current writes do not consume the entire margin during checks.
