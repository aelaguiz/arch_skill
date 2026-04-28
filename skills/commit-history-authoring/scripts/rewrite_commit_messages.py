#!/usr/bin/env python3
"""Safely rewrite local-only commit messages on the current branch."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


PROTECTED_BRANCHES = ("main", "master", "trunk", "develop")
PROTECTED_PREFIXES = ("release/", "hotfix/")


class SafetyError(RuntimeError):
    """Raised when the requested rewrite is not safe to apply."""


def run_git(
    repo: Path,
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    process = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
    )
    if check and process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip()
        raise SafetyError(f"git {' '.join(args)} failed: {detail}")
    return process


def git_stdout(repo: Path, args: list[str], *, check: bool = True) -> str:
    return run_git(repo, args, check=check).stdout.strip()


def repo_root(repo: Path) -> Path:
    root = git_stdout(repo, ["rev-parse", "--show-toplevel"])
    return Path(root).resolve()


def current_branch(repo: Path) -> str:
    branch = git_stdout(repo, ["symbolic-ref", "--quiet", "--short", "HEAD"], check=False)
    if not branch:
        raise SafetyError("current HEAD is detached; refusing to rewrite history")
    return branch


def is_protected_branch(branch: str) -> bool:
    return branch in PROTECTED_BRANCHES or branch.startswith(PROTECTED_PREFIXES)


def ensure_clean(repo: Path) -> None:
    status = git_stdout(repo, ["status", "--porcelain=v1"])
    if status:
        raise SafetyError("worktree or index is dirty; commit, stash, or remove changes before rewriting")


def resolve_upstream(repo: Path) -> str | None:
    process = run_git(
        repo,
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
        check=False,
    )
    if process.returncode != 0:
        return None
    upstream = process.stdout.strip()
    return upstream or None


def resolve_base(repo: Path, explicit_base: str | None) -> tuple[str, str, str | None]:
    upstream = resolve_upstream(repo)
    base_ref = explicit_base or upstream
    if not base_ref:
        raise SafetyError("current branch has no upstream; provide --base <ref>")
    base_sha = git_stdout(repo, ["rev-parse", "--verify", f"{base_ref}^{{commit}}"])
    return base_ref, base_sha, upstream


def ensure_base_ancestor(repo: Path, base_sha: str) -> None:
    process = run_git(repo, ["merge-base", "--is-ancestor", base_sha, "HEAD"], check=False)
    if process.returncode != 0:
        raise SafetyError("base is not an ancestor of HEAD; refusing ambiguous rewrite range")


def ensure_upstream_not_ahead(repo: Path, upstream: str | None) -> None:
    if not upstream:
        return
    process = run_git(repo, ["rev-list", "--left-right", "--count", f"HEAD...{upstream}"], check=False)
    if process.returncode != 0:
        return
    parts = process.stdout.strip().split()
    if len(parts) == 2 and int(parts[1]) > 0:
        raise SafetyError(f"upstream {upstream} is ahead of HEAD; update or resolve divergence first")


def local_commits(repo: Path, base_sha: str) -> list[str]:
    raw = git_stdout(repo, ["rev-list", "--reverse", f"{base_sha}..HEAD"])
    commits = [line for line in raw.splitlines() if line]
    if not commits:
        raise SafetyError("no local commits found in base..HEAD")
    return commits


def ensure_linear(repo: Path, base_sha: str) -> None:
    merges = git_stdout(repo, ["rev-list", "--merges", f"{base_sha}..HEAD"])
    if merges:
        first = merges.splitlines()[0]
        raise SafetyError(f"target range contains merge commit {first}; message-only linear rewrite required")


def remote_refs_containing(repo: Path, commit: str) -> list[str]:
    raw = git_stdout(
        repo,
        ["for-each-ref", "--contains", commit, "--format=%(refname)", "refs/remotes"],
    )
    return [line for line in raw.splitlines() if line]


def ensure_not_remote_reachable(repo: Path, commits: list[str]) -> None:
    for commit in commits:
        refs = remote_refs_containing(repo, commit)
        if refs:
            raise SafetyError(f"commit {commit} is reachable from remote ref {refs[0]}; refusing shared history rewrite")


def commit_info(repo: Path, commit: str) -> dict[str, str]:
    metadata = git_stdout(repo, ["show", "-s", "--format=%an%x00%ae%x00%aI%x00%T%x00%s", commit])
    parts = metadata.split("\x00", 4)
    if len(parts) != 5:
        raise SafetyError(f"could not parse metadata for commit {commit}")
    author_name, author_email, author_date, tree, subject = parts
    return {
        "sha": commit,
        "short": commit[:12],
        "author_name": author_name,
        "author_email": author_email,
        "author_date": author_date,
        "tree": tree,
        "subject": subject,
    }


def inspect_state(repo_arg: str, base_arg: str | None, allow_protected: bool) -> dict[str, Any]:
    root = repo_root(Path(repo_arg))
    branch = current_branch(root)
    if is_protected_branch(branch) and not allow_protected:
        raise SafetyError(f"current branch {branch!r} is protected; explicit approval is required")
    ensure_clean(root)
    base_ref, base_sha, upstream = resolve_base(root, base_arg)
    ensure_upstream_not_ahead(root, upstream)
    ensure_base_ancestor(root, base_sha)
    commits = local_commits(root, base_sha)
    ensure_linear(root, base_sha)
    ensure_not_remote_reachable(root, commits)
    head = git_stdout(root, ["rev-parse", "HEAD"])
    return {
        "status": "ok",
        "repo": str(root),
        "branch": branch,
        "base_ref": base_ref,
        "base": base_sha,
        "upstream": upstream,
        "head": head,
        "commit_count": len(commits),
        "commits": [commit_info(root, commit) for commit in commits],
        "message_file_pattern": "<messages-dir>/<full-old-sha>.msg",
    }


def read_message(messages_dir: Path, commit: str) -> str:
    path = messages_dir / f"{commit}.msg"
    if not path.is_file():
        raise SafetyError(f"missing replacement message file: {path}")
    message = path.read_text(encoding="utf-8")
    if "\x00" in message:
        raise SafetyError(f"replacement message contains NUL byte: {path}")
    if not message.strip():
        raise SafetyError(f"replacement message is empty: {path}")
    return message


def safe_branch_component(branch: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", branch).strip("-")
    return safe or "branch"


def create_backup_ref(repo: Path, branch: str, old_head: str) -> str:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    prefix = f"refs/heads/backup/commit-history-authoring/{safe_branch_component(branch)}-{timestamp}"
    ref = prefix
    suffix = 1
    while run_git(repo, ["show-ref", "--verify", "--quiet", ref], check=False).returncode == 0:
        suffix += 1
        ref = f"{prefix}-{suffix}"
    run_git(repo, ["update-ref", ref, old_head])
    return ref.removeprefix("refs/heads/")


def commit_tree(repo: Path, tree: str, parent: str, message_path: Path, info: dict[str, str]) -> str:
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": info["author_name"],
            "GIT_AUTHOR_EMAIL": info["author_email"],
            "GIT_AUTHOR_DATE": info["author_date"],
        }
    )
    process = run_git(
        repo,
        ["commit-tree", tree, "-p", parent, "-F", str(message_path)],
        env=env,
    )
    return process.stdout.strip()


def apply_rewrite(repo_arg: str, base_arg: str | None, messages_dir_arg: str, allow_protected: bool) -> dict[str, Any]:
    state = inspect_state(repo_arg, base_arg, allow_protected)
    root = Path(state["repo"])
    messages_dir = Path(messages_dir_arg).resolve()
    if not messages_dir.is_dir():
        raise SafetyError(f"messages directory does not exist: {messages_dir}")

    branch = state["branch"]
    old_head = state["head"]
    messages = {
        info["sha"]: read_message(messages_dir, info["sha"])
        for info in state["commits"]
    }
    old_head_tree = git_stdout(root, ["rev-parse", f"{old_head}^{{tree}}"])
    backup_ref = create_backup_ref(root, branch, old_head)

    parent = state["base"]
    mapping: list[dict[str, str]] = []
    for info in state["commits"]:
        old_sha = info["sha"]
        message = messages[old_sha]
        message_path = messages_dir / f"{old_sha}.msg"
        new_sha = commit_tree(root, info["tree"], parent, message_path, info)
        new_subject = message.strip().splitlines()[0]
        mapping.append(
            {
                "old": old_sha,
                "new": new_sha,
                "old_short": old_sha[:12],
                "new_short": new_sha[:12],
                "old_subject": info["subject"],
                "new_subject": new_subject,
            }
        )
        parent = new_sha

    new_head = parent
    new_head_tree = git_stdout(root, ["rev-parse", f"{new_head}^{{tree}}"])
    tree_equivalent = old_head_tree == new_head_tree
    if not tree_equivalent:
        raise SafetyError("rewritten head tree differs from old head tree; branch was not moved")

    run_git(
        root,
        [
            "update-ref",
            "-m",
            "commit-history-authoring: rewrite commit messages",
            f"refs/heads/{branch}",
            new_head,
            old_head,
        ],
    )

    return {
        "status": "ok",
        "mode": "apply",
        "repo": str(root),
        "branch": branch,
        "base_ref": state["base_ref"],
        "base": state["base"],
        "backup_ref": backup_ref,
        "old_head": old_head,
        "new_head": new_head,
        "commit_count": len(mapping),
        "tree_equivalent": tree_equivalent,
        "mapping": mapping,
        "recovery_command": f"git reset --hard {backup_ref}",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="inspect rewrite safety")
    inspect_parser.add_argument("--repo", default=".", help="repository path")
    inspect_parser.add_argument("--base", help="base ref; defaults to current branch upstream")
    inspect_parser.add_argument(
        "--allow-protected",
        action="store_true",
        help="allow protected branch names after explicit user approval",
    )

    apply_parser = subparsers.add_parser("apply", help="apply message-only rewrite")
    apply_parser.add_argument("--repo", default=".", help="repository path")
    apply_parser.add_argument("--base", help="base ref; defaults to current branch upstream")
    apply_parser.add_argument("--messages-dir", required=True, help="directory of <old-sha>.msg files")
    apply_parser.add_argument(
        "--allow-protected",
        action="store_true",
        help="allow protected branch names after explicit user approval",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect_state(args.repo, args.base, args.allow_protected)
        elif args.command == "apply":
            result = apply_rewrite(args.repo, args.base, args.messages_dir, args.allow_protected)
        else:
            parser.error("unknown command")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except SafetyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
