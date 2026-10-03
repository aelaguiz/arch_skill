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
do not run a broad parent scan alongside scans of its descendants.

Use `GB = bytes / 10**9`, `TB = bytes / 10**12`, and `GiB = bytes / 2**30`.
APFS clones, sparse files, hardlinks, snapshots, and concurrent writers explain
why path totals differ from actual recovered space. Measure after deletion;
moving files into Trash or a preservation directory on the same disk frees
no space by itself.

## Protected set

Build the protected canonical-root set first (see `SKILL.md`). Before any
deletion, compare both the lexical path and its resolved path with protected
roots and their resolved destinations. Reject equal paths and ancestors that
would contain a protected checkout. A path inside a canonical checkout is
eligible only when it is itself a registered task worktree, such as an entry
under `.claude/worktrees/`. This applies to every manifest row and cache
deletion, not just checkout removal.

To classify a top-level folder under `~/workspace`, compare its
`git rev-parse --path-format=absolute --git-common-dir` and
`git remote get-url origin` with the canonical checkouts'. A match with a
different path is a task copy.

## Decide whether a checkout is old

```sh
git -C "$wt" rev-parse --path-format=absolute --git-common-dir
git -C "$wt" rev-parse HEAD
git -C "$wt" symbolic-ref -q HEAD
git -C "$wt" log -1 --format='%ct %h %s'
git -C "$wt" reflog -1 --format='%ct %h %gs'
GIT_OPTIONAL_LOCKS=0 git -C "$wt" status --porcelain=v1 -z --untracked-files=normal
```

The newest of the commit time, the reflog time, and the modification times of
the paths `status` lists is when someone last worked there. Do not use mtimes
under `.git` or of build output. `git worktree list --porcelain` shows
`locked <reason>`: a lock that points at a live session or current task counts
as use; a lock left on a finished task does not.

## Exclude running work

```sh
lsof -n -P -a -d cwd -F pn
lsof -n -P -F pcn
```

Capture and parse these locally. Map working directories and open file paths
to checkout roots, matching whole path components. Include references from
processes whose current directory is elsewhere. Do not mark a checkout active
only because the cleanup's own `du`, `git`, or `lsof` inspection has it open.
Do not ignore unrelated user processes just because their command names also
match an inspection tool. Refresh the activity inventory periodically during
long batches and check each candidate close to deletion. Keep parent-directory
and nested-worktree relationships in view so one removal cannot take another
live checkout with it.

Inspect command-line references in memory, returning only matched paths, PIDs,
and sanitized executable names. Do not print raw `ps` output, including `comm`:
processes can place credentials in their displayed titles. A failed or partial
activity query is not evidence of inactivity.

## Salvage unsaved work

Salvage whatever exists only in this checkout: working-tree changes, and
commits the remote does not have. Build the commit with plumbing so the task's
own branch is never moved and no hooks run:

```sh
name="salvage/$(basename "$wt")-$(date +%Y%m%d)"
git -C "$wt" fetch --quiet origin         # fresh remote refs for the check below
git -C "$wt" add -A -- . ':(exclude)<nested-repo-path>'   # .gitignore keeps ignored files out
tree=$(git -C "$wt" write-tree)
commit=$(git -C "$wt" commit-tree "$tree" -p HEAD -m "salvage: unsaved work from $wt")
# no commits yet (HEAD does not resolve): omit -p HEAD to build a root commit
# clean checkout: commit=$(git -C "$wt" rev-parse HEAD)
git -C "$wt" rev-list --count "$commit" --not --remotes   # 0 means already on the remote
git -C "$wt" push --no-verify origin "$commit:refs/heads/$name"
git -C "$wt" ls-remote origin "refs/heads/$name"          # must print $commit
```

The checkout's deletion depends on that last line printing `$commit`. An empty
`$commit`, a count computed from an empty value, a rejected push, or an empty
`ls-remote` means nothing was saved, and the checkout stays.

Before committing, look at the staged file list for credentials and for large
generated binaries (APKs, videos, archives, model files). Unstage them with
`git -C "$wt" rm -r --cached --quiet -- <path>`; they are deleted with the
checkout. If the push is rejected for a secret or file size, remove the named
file the same way and rebuild the commit.

A linked worktree shares branches and stashes with its common repository, so
the commit above covers it. A standalone clone keeps its own: also push every
local branch that has commits missing from the remote, and each stash entry.
Use names that cannot collide with `$name` (Git cannot hold a branch and a
folder of the same name):

```sh
git -C "$wt" push --no-verify origin "refs/heads/$branch:refs/heads/$name-$branch"
git -C "$wt" push --no-verify origin "$(git -C "$wt" rev-parse "stash@{$n}"):refs/heads/$name-stash-$n"
```

For submodules and nested repositories with their own dirty work or unpushed
commits, run the same salvage inside each one against its own remote. Find them
by looking for `.git` entries below the top level, not from `status`: a nested
clone that the parent ignores (a `backend/.native`-style checkout) never appears
there, and its unpushed work is lost with the parent.

```sh
find "$wt" -mindepth 2 -maxdepth 6 -name .git -not -path '*/node_modules/*' -prune -print
```

Exclude each nested repository from the parent's `git add` with the
`:(exclude)` pathspec above so the parent does not record an embedded
repository.

If the remote is unreachable or has no push access, store the commit in the
canonical repository instead:

```sh
git -C "$canonical" fetch "$wt" "$commit:refs/salvage/$(basename "$wt")"
```

Only when neither works, keep the checkout and report the reason. A standalone
repository with no remote and no related canonical repository is such a case:
everything in it exists only on this disk.

## Remove the checkout

```sh
git --git-dir="$common_gitdir" worktree remove --force "$wt"
# stale lock: add a second --force
```

If Git still refuses, find out why before deleting anything. A path that
`git worktree list` does not show is a standalone clone, not a linked worktree,
and needs the standalone salvage above first. Once the reason is understood
and the work is saved, delete the resolved path after the protected-set check,
then run `git --git-dir="$common_gitdir" worktree prune`. Remove a standalone
clone by deleting its resolved path after the same check. Do not delete
branches, reset refs, or rewrite commits.

After each batch, verify the paths are gone, their registrations are pruned,
every salvage ref resolves to its recorded commit, and the canonical checkouts
are intact. Then measure actual free bytes. Record skips and failures as such,
never as removals.

To recreate a removed checkout:

```sh
git --git-dir="$common_gitdir" fetch origin "refs/heads/$name:refs/heads/$name"
git --git-dir="$common_gitdir" worktree add "$original_path" "$name"
```

Dependencies, builds, and ignored files are not restored; rebuild with the
project's normal setup.

## Build output in checkouts that stay

A checkout that is in use or recent keeps its build output. A checkout kept
only because its work could not be saved, or because it holds model policies,
can still lose its inactive build output: Flutter `build/`, `.dart_tool/`, Pods, a
Python virtual environment with `pyvenv.cfg`, or Cargo output. Confirm the
exact leaf holds no tracked files (`git ls-files -- <relative-path>`) and that
no running process uses it; a generated-looking parent may also contain tracked
configuration or unique research.
