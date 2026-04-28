# Git Safety

This skill changes Git history. Treat safety as part of the work, not as a
cleanup step after the messages are written.

## Allowed rewrite

The default rewrite is message-only for the current branch's local linear
commit range:

- same number of commits
- same commit order
- same tree snapshot for every logical step
- same final branch tree
- same author name, author email, and author date
- new commit messages

The helper recreates commits with `git commit-tree`, then moves the branch with
`git update-ref`. It does not run interactive rebase and does not push.

## Base selection

- Use the current branch upstream by default.
- If no upstream exists, the user or invocation must provide `--base <ref>`.
- The base must be an ancestor of `HEAD`.
- If the configured upstream is ahead of `HEAD`, stop. The local branch must be
  brought up to date or the base choice must be made explicit in a separate
  safe workflow.

## Blocked states

Stop instead of rewriting when:

- the worktree or index is dirty
- the current branch is detached
- the branch is protected or shared, such as `main`, `master`, `trunk`,
  `develop`, `release/*`, or `hotfix/*`, unless the user explicitly approved
  that exact branch risk
- the local range is empty
- any commit in the target range is reachable from any remote ref
- the target range contains a merge commit
- any replacement message file is missing or empty
- the helper cannot create a backup branch
- the final tree after rewrite differs from the old head tree

Untracked files count as dirty. This keeps the user's uncommitted work out of a
history rewrite.

## Script contract

Inspect mode:

```bash
python3 skills/commit-history-authoring/scripts/rewrite_commit_messages.py inspect --repo . [--base <ref>]
```

Apply mode:

```bash
python3 skills/commit-history-authoring/scripts/rewrite_commit_messages.py apply --repo . --messages-dir <dir> [--base <ref>]
```

Replacement message files must be named with the full old commit SHA:

```text
<messages-dir>/<old-sha>.msg
```

The script exits nonzero and prints one clear error on unsafe state. On success,
it prints JSON with the base, backup branch, old head, new head, per-commit
mapping, tree-equivalence result, and recovery command.

## Recovery

Every apply creates a local backup branch before moving the current branch:

```text
backup/commit-history-authoring/<branch-safe>-<timestamp>
```

To recover:

```bash
git reset --hard <backup-ref>
```

Do not run that recovery command automatically unless the user explicitly asks
for rollback. It is destructive to the rewritten branch state.
