# Worktree and measurement mechanics

Use these command shapes inside a scope selected from live evidence. Quote
paths and prefer subprocess argument arrays for manifests containing many
paths. Do not paste secret-bearing process arguments into output.

## Measure once

`df` or Python's disk-usage API measures the actual volume. For exact byte
comparisons, use the same path before and after:

```python
from pathlib import Path
import shutil

volume = Path.home() / "workspace"
usage = shutil.disk_usage(volume)
print({"total_bytes": usage.total, "free_bytes": usage.free})
```

`du -sk <selected-path>` estimates allocated blocks. Save one result per
non-overlapping path, and reuse it during that run. For many paths, a small
bounded thread pool can run independent measurements and stream summaries;
do not run a broad parent scan alongside scans of its descendants. Inventory
Git state before spending time measuring checkouts that will be retained.

Use `GB = bytes / 10**9`, `TB = bytes / 10**12`, and `GiB = bytes / 2**30`.
APFS clones, sparse files, hardlinks, snapshots, and concurrent writers explain
why path totals differ from actual recovered space. Measure after deletion;
moving files into Trash or a preservation directory on the same disk frees
no space by itself.

## Inspect selected worktrees

Build the protected canonical-root set first. Before any deletion or move,
compare both the lexical path and its resolved path with protected roots and
their resolved destinations. Reject equal paths, descendants, and ancestors
that would contain a protected checkout. This applies to every manifest row
and standalone cache deletion, not just the worktree-removal command. All
top-level project checkouts under `~/workspace` are protected by default;
`psmobile`, `psagentspace`, and `.psmobile-git-root` must never become candidates
because of age, clean status, a `.git` file, or a cached cleanup decision.

```sh
git -C "$repo" worktree list --porcelain
git -C "$worktree" rev-parse --path-format=absolute --git-common-dir
git -C "$worktree" rev-parse HEAD
git -C "$worktree" symbolic-ref -q HEAD
GIT_OPTIONAL_LOCKS=0 git -C "$worktree" status --porcelain=v1 --untracked-files=all
git -C "$worktree" ls-files --others --ignored --exclude-standard --directory -z
```

Parse NUL-delimited paths rather than splitting paths on spaces. Preserve
staged and unstaged edits and untracked files; a failed status command is not
evidence of a clean checkout. Leave locked worktrees alone.

Check `git ls-files --stage -z` for entries with mode `160000` before measuring
or moving ignored files. Keep worktrees containing these submodule entries.
In the live evaluation, normal Git removal refused them even after clean
submodule deinitialization; deinitializing added recovery work without removing
the parent checkout. Do not repeat that workaround during routine cleanup.

A retained local branch protects committed work even if it was never pushed
or its changes were squash-merged. Do not require merge ancestry for that case.
For detached checkouts, prove reachability from a retained ref or keep the
checkout. Record exact commits before removal so recovery does not depend on
where a branch points later.

For age evidence use commit/reflog entries when useful:

```sh
git -C "$worktree" log -1 --format='%ct %h %s'
git -C "$worktree" reflog -1 --format='%ct %h %gs'
```

The filesystem mtime of `logs/HEAD` can reflect repository maintenance rather
than work in that checkout. There is no universal age cutoff that proves a
worktree unused.

## Exclude running work

```sh
lsof -n -P -a -d cwd -F pn
lsof -n -P -F pcn
```

Capture and parse these locally. Map working directories and open file paths
to worktree roots, matching whole path components. Include references from
processes whose current directory is elsewhere. Do not mark a worktree active
only because the cleanup's own `du`, `git`, or `lsof` inspection has it open.
Identify the cleanup's own processes; do not ignore unrelated user processes
just because their command names also match an inspection tool. Refresh the
activity inventory periodically during long batches and check candidates close
to mutation. Skip a selected path if fresh activity
or changed Git state invalidates the selection. Keep parent-directory and
nested-worktree relationships in view so one removal cannot take another
checkout with it.

## Preserve ignored data and remove the checkout

Inspect ignored paths before removal. For recognized build/dependency folders,
check for tracked contents with `git ls-files -- <relative-path>`; custom
folders can contain source despite looking generated. Preserve unknown or
unique ignored data in a private directory outside every selected removal
root, recording source/destination paths. Avoid traversing symlinks; preserve
the link and its original location without deleting its target.

For collapsed ignored directories, check for tracked descendants and nested
repositories before moving the directory. Preserve only the intended local
files. Keep a recovery record as files move, and restore moved files if the
worktree removal fails and the original checkout remains.

```sh
git --git-dir="$common_gitdir" worktree remove "$worktree"
git --git-dir="$common_gitdir" rev-parse "$retained_branch"
```

Use the normal removal command without `--force`. Do not stage, reset, stash,
delete branches, or alter commits to get a checkout removed. Recheck local
state immediately before each removal, including any ignored files that
appeared since inspection.

To recreate a removed checkout at the recorded commit:

```sh
git --git-dir="$common_gitdir" worktree add --detach "$original_path" "$saved_head"
```

Restore its preserved local files to their recorded relative paths. This does
not recreate deleted build products or installed dependencies; use the
project's normal setup commands when that checkout is needed again.

After a batch, verify expected path removal, retained Git refs/commits,
canonical checkout paths, and the preservation location, then measure actual
free bytes. Save per-path skips and failures without calling them successful
removals. If current writers consume a narrow margin during verification,
continue through another eligible cache or disposable candidate and measure
again. A pending manifest or successful preview is preparation, not proof
that disk space was reclaimed.
