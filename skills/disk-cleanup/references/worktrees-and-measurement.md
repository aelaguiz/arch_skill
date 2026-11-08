# Removing checkouts and measuring the result

Quote every path, and work from a saved list of checkouts rather than a glob.

## Delete first what has nothing unsaved

A dead checkout has nothing unsaved when all of these are true:

- `git status --porcelain` is empty;
- `git rev-list --count HEAD --not --remotes` prints `0` after a pruning fetch;
- it has no nested repository with its own unsaved work.

A standalone clone, which is not a linked worktree, also needs no local branch and no stash that the remote lacks. Remove these checkouts right away: they free most of the space and need no backup. Then salvage the others in a batch.

To tell a linked worktree from a standalone clone, run `git -C "$wt" rev-parse --path-format=absolute --git-common-dir`. A linked worktree reports its primary repository's `.git` and appears in that repository's `git worktree list --porcelain`. Linked worktrees share branches and stashes with their primary repository. A standalone clone keeps its own.

## Salvage unsaved work

Build the commit with Git's plumbing, through a copy of the checkout's index, so the task's own branch, its staging area and its hooks are all left alone. If the push fails and the checkout stays, nothing in it has changed:

```sh
name="salvage/$(basename "$(dirname "$wt")")-$(basename "$wt")-$(date +%Y%m%d)"
git -C "$wt" fetch --prune --quiet origin
idx="$(mktemp -d)/index"
cp "$(git -C "$wt" rev-parse --path-format=absolute --git-path index)" "$idx" 2>/dev/null || true   # none yet is fine
export GIT_INDEX_FILE="$idx"                              # every git command below uses the copy
git -C "$wt" add -A -- . ':(exclude)<nested-repo-path>' || echo "add failed: keep $wt"   # .gitignore keeps ignored files out
git -C "$wt" diff --cached --stat HEAD 2>/dev/null || git -C "$wt" ls-files | head -100   # look before anything leaves the machine
tree=$(git -C "$wt" write-tree)
commit=$(git -C "$wt" commit-tree "$tree" -p HEAD -m "salvage: unsaved work from $wt [skip ci]") || commit=""
# no commits yet (HEAD doesn't resolve): leave out -p HEAD to make a root commit
# clean, with unpushed commits: commit=$(git -C "$wt" commit-tree "$(git -C "$wt" rev-parse 'HEAD^{tree}')" -p HEAD -m "salvage: unpushed commits from $wt [skip ci]")
[ -n "$commit" ] && git -C "$wt" push --no-verify origin "$commit:refs/heads/$name"      # an empty id would delete the branch instead
[ -n "$commit" ] && [ "$(git -C "$wt" ls-remote origin "refs/heads/$name" | cut -f1)" = "$commit" ] && echo saved
unset GIT_INDEX_FILE
```

The checkout can go only when the last line prints `saved`. An empty `$commit`, a failed `add`, a rejected push or an `ls-remote` that doesn't match means nothing was saved. Every pushed salvage head carries `[skip ci]` in its message, because a salvage branch never needs CI. One cleanup's pushes without it once started 475 CI jobs.

Before pushing, read that file list. Take credentials and large generated files (APKs, videos, archives, model files) out with `git -C "$wt" rm -r --cached --quiet -- <path>` while `GIT_INDEX_FILE` is still set, then build the tree again. Those files go with the checkout. If a push is rejected for a secret or a file's size, unstage the file it names and build the commit again.

For a standalone clone, also push each local branch the remote lacks and each stash, wrapped the same way. Give them names that can't collide with `$name`:

```sh
tip=$(git -C "$wt" rev-parse "refs/heads/$branch")   # or "stash@{$n}"
c=$(git -C "$wt" commit-tree "$(git -C "$wt" rev-parse "$tip^{tree}")" -p "$tip" -m "salvage: $branch from $wt [skip ci]")
git -C "$wt" push --no-verify origin "$c:refs/heads/$name-$branch"   # or $name-stash-$n
```

Nested repositories and submodules with their own unsaved work get the same salvage inside each one, against its own remote. Find them by looking for `.git` below the top level, because a nested clone that the parent ignores never shows up in `status`:

```sh
find "$wt" -maxdepth 6 \( -path "$wt/.git" -o -name node_modules -o -name target -o -name .venv \) -prune -o -name .git -print
```

Don't commit onto, push to or rewrite the task's own branch, which may back an open PR, and don't delete branches.

## Work with no remote

A checkout whose origin is a bundle or a local path, a repository with no origin, and a source folder with no Git at all still have somewhere to go. Store the work in a local repository that holds only source:

```sh
salvage_repo=~/.local/share/disk-cleanup/salvage.git
[ -d "$salvage_repo" ] || git init --bare --quiet "$salvage_repo"
ref="refs/salvage/$(basename "$wt")-$(date +%Y%m%d)"
# a checkout with Git but no remote: build $commit as above, then
[ -n "$commit" ] && git -C "$wt" push --quiet --no-verify "$salvage_repo" "$commit:$ref/work" "refs/heads/*:$ref/heads/*"   # the work and its local branches; stashes as above
[ -n "$commit" ] && [ "$(git --git-dir="$salvage_repo" rev-parse --verify --quiet "$ref/work")" = "$commit" ] && echo saved
```

The work goes under `$ref/work` and the branches under `$ref/heads/`, because a ref can't also be a folder of refs.

When the same project has a primary checkout on this machine, pushing to it works too: `git -C "$wt" push --no-verify "$primary" "$commit:refs/salvage/<name>"`.

Commit a folder with no Git at all straight from its files, through a private index, so nothing in the folder changes. The index must be a path that doesn't exist yet, because Git rejects an empty file:

```sh
idx="$(mktemp -d)/index"
G() { GIT_INDEX_FILE="$idx" git --git-dir="$salvage_repo" --work-tree="$dir" "$@"; }
G add -A -- . ':(exclude,glob)**/node_modules/**' ':(exclude,glob)**/target/**' ':(exclude,glob)**/build/**' \
  ':(exclude,glob)**/.venv/**' ':(exclude)*.zip' ':(exclude)*.apk'
G ls-files --stage | awk '{print $4}' | head -50                 # look at what went in before committing
commit=$(G commit-tree "$(G write-tree)" -m "salvage: $dir") || commit=""
[ -n "$commit" ] && G update-ref "$ref/work" "$commit" "" && [ "$(git --git-dir="$salvage_repo" rev-parse --verify --quiet "$ref/work")" = "$commit" ] && echo saved   # "" refuses to overwrite an existing ref
```

The folder's own `.gitignore` files are honoured. The salvage repository is for source and notes. If it grows large, something big went in: find it and leave it out. A folder can't be salvaged only when the commit itself fails, and then it stays this run, with the reason.

## Remove the checkout

```sh
git --git-dir="$common_gitdir" worktree remove --force "$wt"     # add a second --force for a stale lock
git --git-dir="$common_gitdir" worktree prune
```

If Git refuses, find out why before deleting anything. A path missing from `git worktree list` is a standalone clone, and it needs the standalone salvage first. Remove a standalone clone, or a folder that isn't a Git checkout at all, through a check that refuses the paths that must never be targets. Those are a home folder, a workspace root, a mount, anything outside the places task folders live, and any folder that holds a path you decided to keep (the live work you named, one path per line in `$run/keep.txt`):

```sh
remove_dir() {
  p=$(printf '%s' "$1" | sed 's#/*$##')                   # a trailing slash would hide a link
  [ -n "$p" ] && [ ! -L "$p" ] || { echo "refused, a link or empty: remove a link itself, never what it points at: $1"; return 1; }
  [ -r "$run/keep.txt" ] || { echo "refused, no keep list at $run/keep.txt"; return 1; }
  t=$(realpath "$p") || return 1
  case "$t" in "$HOME"/?*|/mnt/p[12]/?*|/tmp/?*|/private/tmp/?*|/private/var/folders/?*) ;; *) echo "refused, not a task location: $t"; return 1;; esac
  [ -d "$t" ] && [ "$t" != "$HOME/workspace" ] && [ "$t" != "$HOME/worktrees" ] || { echo "refused: $t"; return 1; }
  m=$(df -P "$t" | awk 'NR==2 {print $6}'); [ -n "$m" ] && [ "$m" != "$t" ] || { echo "refused, a mount or unknown mount: $t"; return 1; }
  if grep -qF -- "$t/" "$run/keep.txt" 2>/dev/null || grep -qxF -- "$t" "$run/keep.txt" 2>/dev/null; then echo "refused, kept or holds something kept: $t"; return 1; fi
  rm -rf -- "$t"
}
remove_dir "$wt" && [ ! -e "$wt" ] && echo removed
```

A link is refused because resolving it would aim the deletion at what it points to, such as a policy store. If the link itself is what should go, remove it with `rm -- "$link"` (no `-r`, no trailing slash). On Linux, `rm -rf --one-file-system` also keeps the removal from crossing into a drive mounted inside the folder. Add it there; macOS `rm` has no such flag.

A worktree whose `.git` file points at an admin folder that no longer exists breaks every Git command inside it. If its repository still lists it, `git -C <repository> worktree repair "$wt"` fixes it and the usual salvage applies. If the repository is gone, salvage it as a folder with no Git.

After each batch, check four things: the paths are gone, the registrations are pruned, every salvage ref resolves to its recorded commit, and the checkouts you kept are intact. Record each removal with its original path, HEAD, salvage ref and a line about what was discarded. To recreate one:

```sh
git --git-dir="$common_gitdir" fetch origin "refs/heads/$name:refs/heads/$name"
git --git-dir="$common_gitdir" worktree add "$original_path" "$name"
```

Dependencies, builds and ignored files don't come back. Rebuild them with the project's normal setup.

## Build output in checkouts that stay

A live checkout keeps the build output it is using. A checkout kept for another reason can lose inactive build output: Flutter `build/`, `.dart_tool/`, Pods, a virtual environment with `pyvenv.cfg`, or Cargo `target/debug` and `target/release`. Before removing a leaf, confirm it holds no tracked files (`git ls-files -- <relative-path>` prints nothing) and that no process uses it. A `target/` folder can hold tracked configuration or research alongside the build, so remove its build leaves, not the whole folder.

## Measuring

`df -k` on the volume is the free space that tools see. Measure before and after with the same command. `du` totals are estimates: APFS clones, hard links, sparse files and snapshots all make them differ from what deleting frees. Moving files to Trash or to another folder on the same disk frees nothing. When a deletion doesn't show as free space, the cause is almost always Time Machine's local snapshots ([time-machine-local-snapshots.md](../../_shared/time-machine-local-snapshots.md)), and occasionally a deleted file a process still holds open, which `lsof +L1` lists.
