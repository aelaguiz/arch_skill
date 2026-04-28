import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills/commit-history-authoring/scripts/rewrite_commit_messages.py"


def run(cmd, cwd: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    process = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and process.returncode != 0:
        raise AssertionError(
            f"command failed: {cmd}\nstdout:\n{process.stdout}\nstderr:\n{process.stderr}"
        )
    return process


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], repo, check=check)


class TempRepo:
    def __init__(self, tmp: Path) -> None:
        self.tmp = tmp
        self.origin = tmp / "origin.git"
        self.work = tmp / "work"
        run(["git", "init", "--bare", str(self.origin)], tmp)
        run(["git", "clone", str(self.origin), str(self.work)], tmp)
        git(self.work, "config", "user.name", "Test User")
        git(self.work, "config", "user.email", "test@example.com")
        (self.work / "app.txt").write_text("base\n", encoding="utf-8")
        git(self.work, "add", "app.txt")
        git(self.work, "commit", "-m", "Initial commit")
        git(self.work, "branch", "-M", "main")
        git(self.work, "push", "-u", "origin", "main")
        git(self.work, "checkout", "-b", "feature/history")
        git(self.work, "branch", "--set-upstream-to", "origin/main")

    def commit(self, filename: str, text: str, message: str) -> str:
        path = self.work / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(text)
        git(self.work, "add", filename)
        git(self.work, "commit", "-m", message)
        return git(self.work, "rev-parse", "HEAD").stdout.strip()


def run_script(*args: str, repo: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["python3", str(SCRIPT), *args], repo, check=check)


def write_messages(repo: Path, messages_dir: Path, suffix: str = "") -> list[str]:
    inspect = run_script("inspect", "--repo", str(repo), repo=repo)
    data = json.loads(inspect.stdout)
    shas = [item["sha"] for item in data["commits"]]
    messages_dir.mkdir(parents=True, exist_ok=True)
    for index, sha in enumerate(shas, start=1):
        (messages_dir / f"{sha}.msg").write_text(
            f"Rewrite step {index}{suffix}\n\nExplain local change {index}.\n",
            encoding="utf-8",
        )
    return shas


class CommitHistoryAuthoringTests(unittest.TestCase):
    def test_apply_rewrites_messages_preserves_commit_count_and_final_tree(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = TempRepo(Path(td))
            temp.commit("app.txt", "one\n", "WIP")
            temp.commit("app.txt", "two\n", "more stuff")
            temp.commit("docs/note.md", "docs\n", "updates")
            old_head = git(temp.work, "rev-parse", "HEAD").stdout.strip()
            old_tree = git(temp.work, "rev-parse", "HEAD^{tree}").stdout.strip()
            old_count = git(temp.work, "rev-list", "--count", "origin/main..HEAD").stdout.strip()
            messages_dir = Path(td) / "messages"
            write_messages(temp.work, messages_dir)

            result = run_script(
                "apply",
                "--repo",
                str(temp.work),
                "--messages-dir",
                str(messages_dir),
                repo=temp.work,
            )
            data = json.loads(result.stdout)

            new_head = git(temp.work, "rev-parse", "HEAD").stdout.strip()
            new_tree = git(temp.work, "rev-parse", "HEAD^{tree}").stdout.strip()
            new_count = git(temp.work, "rev-list", "--count", "origin/main..HEAD").stdout.strip()
            subjects = git(temp.work, "log", "--format=%s", "--reverse", "origin/main..HEAD").stdout.splitlines()

            self.assertEqual(data["status"], "ok")
            self.assertEqual(data["old_head"], old_head)
            self.assertEqual(data["new_head"], new_head)
            self.assertEqual(data["commit_count"], 3)
            self.assertTrue(data["tree_equivalent"])
            self.assertEqual(old_tree, new_tree)
            self.assertEqual(old_count, new_count)
            self.assertEqual(subjects, ["Rewrite step 1", "Rewrite step 2", "Rewrite step 3"])
            self.assertEqual(git(temp.work, "status", "--porcelain=v1").stdout, "")
            git(temp.work, "show-ref", "--verify", f"refs/heads/{data['backup_ref']}")

    def test_dirty_worktree_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = TempRepo(Path(td))
            temp.commit("app.txt", "one\n", "WIP")
            (temp.work / "dirty.txt").write_text("dirty\n", encoding="utf-8")
            result = run_script("inspect", "--repo", str(temp.work), repo=temp.work, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("dirty", result.stderr)

    def test_remote_reachable_commit_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = TempRepo(Path(td))
            temp.commit("app.txt", "one\n", "WIP")
            git(temp.work, "push", "origin", "HEAD:refs/heads/feature/history")
            result = run_script("inspect", "--repo", str(temp.work), repo=temp.work, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("remote ref", result.stderr)

    def test_upstream_ahead_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = TempRepo(Path(td))
            temp.commit("app.txt", "feature\n", "WIP")
            git(temp.work, "checkout", "main")
            (temp.work / "main.txt").write_text("new main\n", encoding="utf-8")
            git(temp.work, "add", "main.txt")
            git(temp.work, "commit", "-m", "Advance main")
            git(temp.work, "push", "origin", "main")
            git(temp.work, "checkout", "feature/history")

            result = run_script("inspect", "--repo", str(temp.work), repo=temp.work, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("upstream origin/main is ahead", result.stderr)

    def test_merge_commit_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = TempRepo(Path(td))
            temp.commit("app.txt", "feature\n", "WIP")
            git(temp.work, "checkout", "-b", "side", "origin/main")
            temp.commit("side.txt", "side\n", "Side work")
            git(temp.work, "checkout", "feature/history")
            git(temp.work, "merge", "--no-ff", "side", "-m", "Merge side")

            result = run_script("inspect", "--repo", str(temp.work), repo=temp.work, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("merge commit", result.stderr)

    def test_protected_branch_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = TempRepo(Path(td))
            git(temp.work, "checkout", "main")
            temp.commit("app.txt", "main-local\n", "WIP")

            result = run_script("inspect", "--repo", str(temp.work), repo=temp.work, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("protected", result.stderr)

    def test_missing_replacement_message_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = TempRepo(Path(td))
            temp.commit("app.txt", "one\n", "WIP")
            messages_dir = Path(td) / "messages"
            messages_dir.mkdir()

            result = run_script(
                "apply",
                "--repo",
                str(temp.work),
                "--messages-dir",
                str(messages_dir),
                repo=temp.work,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("missing replacement message", result.stderr)

    def test_arch_plan_callout_can_be_preserved_in_new_message(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = TempRepo(Path(td))
            temp.commit("docs/PLAN.md", "# TL;DR\n\n<!-- arch_skill:block:phase_plan:start -->\n", "WIP")
            messages_dir = Path(td) / "messages"
            shas = write_messages(temp.work, messages_dir, suffix="")
            (messages_dir / f"{shas[0]}.msg").write_text(
                "Document commit history plan\n\nArch plan: docs/PLAN.md, phase 1.\n",
                encoding="utf-8",
            )

            run_script(
                "apply",
                "--repo",
                str(temp.work),
                "--messages-dir",
                str(messages_dir),
                repo=temp.work,
            )
            body = git(temp.work, "log", "-1", "--format=%B").stdout
            self.assertIn("Arch plan: docs/PLAN.md, phase 1.", body)


if __name__ == "__main__":
    unittest.main()
