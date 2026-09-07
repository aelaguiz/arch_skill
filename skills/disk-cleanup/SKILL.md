---
name: disk-cleanup
description: "Reclaim substantial disk space on Amir's developer Macs by starting with known worktree, build, cache, and log locations and reusing local cleanup inventories. Use for a full disk, accumulated agent worktrees, routine developer cleanup, or a target such as 1 TB free. Protects canonical checkouts, active work, Git commits, and unique local files; verifies actual free space. Use codex-cleanup for a task confined to Codex SQLite/session maintenance, and arch-docs for stale documentation."
metadata:
  short-description: "Fast developer disk cleanup with work preserved"
---

# Disk Cleanup

Restore the user's requested disk headroom quickly while keeping their work
recoverable and their running tools usable. Optimize for substantial reclaimed
space and a shorter next cleanup. A long inventory or a small cache deletion
does not finish a request for hundreds of gigabytes.

## When to use

- "I'm running out of disk space. Find the caches and old worktrees and clean them up."
- "Get this coding machine back to 1 TB free."
- "Clean up the developer junk again without scanning the whole disk."

This skill owns local disk housekeeping. It does not delete source functionality,
retire documentation, prune application databases, or administer other machines.
For work confined to Codex's session/log SQLite state, use `$codex-cleanup` and
its live-process rules. A large `~/.codex` directory does not make stopping all
agents a prerequisite for cleaning unrelated worktrees.

## Start with the known map

Read [known-locations.md](references/known-locations.md) first. It gives the
likely large owners and the saved-inventory locations. Read
[worktrees-and-measurement.md](references/worktrees-and-measurement.md) before
removing checkouts or interpreting reclaimed bytes.

1. Measure capacity and available bytes on the volume containing `~/workspace`.
   Carry forward the user's target and cleanup authorization from the conversation.
   Distinguish a target for total free space from an amount to reclaim.
   Establish the protected canonical roots below before selecting any candidates.
2. Look for a recent local cleanup manifest or report. Reuse its paths, recorded
   sizes, and recovery information as discovery hints. Refresh current existence,
   Git state, and process use before acting; a saved deletion decision is not
   current proof. Without a saved inventory, enumerate the known worktree roots
   and their owning Git repositories first.
3. Select enough large candidates to plausibly reach the target. Inspect and
   measure those candidates once. Save bulky results locally and report totals
   and the largest owners. Do not recursively scan `/`, the home directory,
   `~/workspace`, and their children concurrently: those scans repeat the same
   expensive traversal.
4. Execute the authorized cleanup and measure the result. If an applicable
   instruction requires confirmation that the conversation has not supplied,
   prepare the exact paths, preservation plan, and estimated space first, then
   ask once. A preview-only request remains read-only.
5. Continue through the next material owner when actual free space is still
   below target. Broaden discovery only when the known locations do not explain
   the usage or cannot supply the needed reclaimable space. Stop when the target
   is reached, or identify the concrete remaining data that requires a user decision.

## Canonical checkouts are protected

Never remove, rename, replace, or empty a canonical checkout. In particular,
`~/workspace/psmobile` and `~/workspace/psagentspace` are permanent working
locations, not disposable copies. Apply the same protection to the other
top-level project checkouts under `~/workspace`, including `prime-agent`,
`arch_skill`, and the shared Git owner `.psmobile-git-root`. Age, clean status,
merged commits, or being registered as a linked worktree never waive this rule.

Before cleanup, record the protected paths and their resolved destinations.
Exclude those roots, their contents, and any ancestor whose removal would
contain them from every deletion or relocation list, including old manifests
and scripts. Resolve aliases and symlinks when checking containment. Routine
cleanup uses disposable checkouts outside these roots and external caches;
canonical build and dependency folders also stay untouched unless the user
specifically requests that folder's cleanup. Reading canonical Git inventories
and Git's normal registration updates when removing a separate worktree are
allowed. If a checkout's role is unclear, keep it.

Any reused or newly written cleanup script must enforce this protected set
before every deletion or relocation. A safe preview does not compensate for
an executable that lacks the same lexical and resolved containment checks.

## Preserve work while removing copies

Use Git's worktree inventory, current working-tree status, and live process
references to decide whether a checkout can go. Directory names and ages are
prioritization clues, not proof. Git maintenance can rewrite reflog mtimes for
every worktree at once; use commit/reflog records and current activity instead
of treating those mtimes as recent coding work.

Keep active or locked worktrees, staged edits,
unstaged edits, and untracked work. A clean worktree on an unmerged branch can
still be removed when that branch and its commit remain in the common Git
repository. Preserve the branch; removing a duplicate checkout does not require
deleting or merging it. For a detached worktree, establish retained commit
reachability before removal.

Inspect ignored files too. `git status` being clean does not protect `.env`,
downloaded data, reports, logs, or local configuration from `git worktree remove`.
Preserve unique ignored files outside the removal roots with their original
paths recorded. Recognized reproducible dependencies and build outputs can be
discarded within the cleanup scope. An ignored directory name alone does not
make its contents disposable. Moving files within the same volume is cheap but
does not free space; subtract preserved data from the estimate.

Remove selected worktrees with normal `git worktree remove`, rechecking their
head, branch, dirty state, and activity close to removal. Do not use force,
`git clean`, hard resets, or branch deletion to make cleanup succeed. If a
candidate changed, skip it and continue through the other candidates. Retain
the original path, common Git directory, branch, commit, and preserved-file
mapping so the checkout can be recreated.

Refresh process activity throughout long batches, not only at startup. Detect
worktrees containing submodules during selection and keep them; do not
deinitialize submodules or retry unsupported removal mechanisms as part of
generic housekeeping.

For caches and build folders, establish what regenerates them and whether a
running process uses them. Verify that selected build paths contain no tracked
source before deleting them. Keep credentials, live SQLite/WAL state, browser
profiles, simulator user data, and VM volumes outside generic cache deletion.
Use their owning tool when those storage classes become necessary to the task.

## Leave a faster next run

Keep a small private local report under `~/disk-cleanup-<date>/` or an existing
cleanup-report directory. Record the host and volume, start/end free bytes,
examined owners, selected paths and measurements, removals, skips, preserved
paths, and recovery instructions. Keep secrets out of report contents.

Existing local cleanup scripts are optional implementation artifacts. Read them
before reuse and check their scope, freshness checks, preservation behavior,
and failure handling against this skill. The skill must also work on a machine
where no previous script or manifest exists.

Report actual before/after free space, actual bytes reclaimed, the largest
removed categories, what was preserved or skipped, and the local receipt path.
State whether the requested target was reached. Label estimates separately;
do not add nested folder sizes or present `du` totals as measured free space.
Take the completion measurement after verification. If the disk remains busy,
select a cleanup batch with a few gigabytes of headroom beyond the requested
threshold so current writes do not consume the entire margin during checks.
