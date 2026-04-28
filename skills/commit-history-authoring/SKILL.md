---
name: commit-history-authoring
description: "Rewrite the current branch's local-only Git commit messages into an informative narrative while preserving patches and commit boundaries. Use when the user wants WIP/vague commits re-authored, local branch history clarified, or an active arch plan called out in commit bodies before sharing. Safety-first: inspect repo truth, rewrite only unpushed linear commits by default, create a backup branch, never push/force-push, and do not squash/split/reorder unless the user explicitly asks for a separate history-editing flow. Not for PR bodies, changelogs, release notes, code review, or editing shared/remote history."
metadata:
  short-description: "Re-author local commit messages safely"
---

# Commit History Authoring

Use this skill when the user wants the current branch's local-only commit
history rewritten so the commit stream explains the work clearly.

Default behavior is message-only: preserve every patch, tree snapshot, commit
boundary, and commit order. Do not squash, split, reorder, push, force-push, or
rewrite shared history.

This skill ships one script because the dangerous part is deterministic Git
safety. The agent authors the messages; `scripts/rewrite_commit_messages.py`
only inspects and applies a safe message-only rewrite.

## When to use

- The user wants `WIP`, vague, or placeholder commits re-authored into useful
  local commit messages.
- The user wants current-branch local history to tell the story of what changed
  before sharing, opening a PR, or handing the branch to someone else.
- The user wants active arch-plan context called out in commit bodies when the
  repo provides real evidence of that plan.
- The user asks to make the commit stream maximally informative while keeping
  the branch's actual code changes intact.

## When not to use

- The target commits are already pushed, reachable from a remote ref, or on a
  shared/protected branch without explicit approval.
- The user wants a PR title/body. Use `$pr-authoring`.
- The user wants a changelog, release notes, or docs narrative instead of Git
  history.
- The user wants a findings-first review. Use `$code-review`.
- The user wants to squash, split, reorder, drop, or combine commits. Treat
  that as a separate higher-risk history-editing task, not this default flow.
- The repo has no concrete local commit range to rewrite.

## Non-negotiables

- Work from repo truth: current branch, upstream/base, local commits, commit
  diffs, old messages, trailers, active arch-plan evidence, and repo
  instructions.
- Rewrite only commits that are provably local-only and not reachable from any
  remote ref.
- Require a clean worktree and index before applying a rewrite.
- Use the branch upstream as the default base. If there is no upstream, require
  an explicit base ref.
- Preserve commit boundaries and patch content by default. Never use squash,
  split, reorder, cherry-pick cleanup, or interactive rebase unless the user
  explicitly asks for that different workflow.
- Create a backup branch before moving the current branch.
- Preserve author metadata and existing trailers such as `Co-authored-by`,
  `Signed-off-by`, `Change-Id`, `Reviewed-by`, and `Fixes`.
- Never invent intent, ticket numbers, tests, reviewers, plan paths, or phase
  status.
- Never push or force-push. Return the local rewrite receipt and recovery
  command.

## First move

1. Read `references/git-safety.md`.
2. Read `references/message-quality.md`.
3. Run inspect mode from the repo root:
   ```bash
   python3 skills/commit-history-authoring/scripts/rewrite_commit_messages.py inspect --repo .
   ```
   If the repo has no upstream and the user supplied a base, add
   `--base <ref>`.
4. Resolve active arch-plan evidence from, in order:
   - an explicit `docs/<...>.md` path from the user
   - current controller state under `.codex/` or `.claude/arch_skill/`
   - a single strong canonical docs candidate with full-arch markers
5. If multiple credible plan candidates remain, ask the user to choose from the
   top candidates. Otherwise proceed with `active arch plan: none`.

## Workflow

1. **Inspect safety.** Use the helper's inspect output plus `git status`,
   `git log`, and `git show` as needed. Stop on any unsafe state.
2. **Map each commit.** For every local-only commit, read the old message,
   changed files, stats, and diff enough to understand what the commit did and
   why it belongs as its own step.
3. **Draft messages.** Write one message file per commit using the full SHA
   filename expected by the helper: `<messages-dir>/<old-sha>.msg`.
4. **Validate the story.** Read the messages in order and check that the stream
   explains the branch, preserves trailers, calls out evidenced arch-plan
   context, and does not overclaim.
5. **Apply only when asked to rewrite.** If the user's request is only a
   review, preview, or proposal, stop after showing the proposed messages.
   Otherwise run:
   ```bash
   python3 skills/commit-history-authoring/scripts/rewrite_commit_messages.py apply --repo . --messages-dir <messages-dir>
   ```
6. **Report the receipt.** Include rewritten commit count, backup branch,
   old/new head, active arch plan used or `none`, verification result, and the
   recovery command.

## Quality bar

- Great commit streams let a future reader understand the problem, the
  implementation sequence, and the plan context without opening every diff.
- Subjects are specific, imperative, and scoped to the commit's actual change.
- Bodies explain why the step exists when the subject alone is not enough.
- Arch-plan callouts are concrete and evidenced, for example
  `Arch plan: docs/PLAN.md, phase 2`. Missing evidence stays unmentioned.
- Weak output merely replaces `WIP` with generic polish, repeats filenames,
  invents motivation, drops trailers, or rewrites code history while pretending
  it only rewrote messages.

## Output expectations

- On success: return a compact receipt with the backup branch and recovery
  command.
- On blocked rewrite: name the exact safety blocker and the next concrete step
  required before retrying.
- On preview-only work: return the proposed messages and say no history was
  rewritten.
- Do not include a force-push command unless the user asks how to publish
  rewritten local history; even then, frame it as outside this skill's action.

## Reference map

- `references/git-safety.md` - local-only rewrite boundary, blocked states,
  backup/recovery, and script contract
- `references/message-quality.md` - informative message shape, active arch-plan
  handling, trailer preservation, and anti-patterns
