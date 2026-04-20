import json
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UPSERT_CODEX_PATH = REPO_ROOT / "skills/arch-step/scripts/upsert_codex_stop_hook.py"
UPSERT_CLAUDE_PATH = REPO_ROOT / "skills/arch-step/scripts/upsert_claude_stop_hook.py"
UPSERT_CLAUDE_START_PATH = REPO_ROOT / "skills/arch-step/scripts/upsert_claude_session_start_hook.py"


class UpsertConcurrentTests(unittest.TestCase):
    def _run_upsert(self, script: Path, settings_file: Path, skills_dir: Path) -> subprocess.CompletedProcess:
        if script == UPSERT_CODEX_PATH:
            flag_name = "--hooks-file"
        else:
            flag_name = "--settings-file"
        return subprocess.run(
            [
                sys.executable,
                str(script),
                flag_name,
                str(settings_file),
                "--skills-dir",
                str(skills_dir),
            ],
            capture_output=True,
            text=True,
        )

    def test_codex_parallel_upserts_converge_and_preserve_third_party(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hooks_file = root / "codex/hooks.json"
            skills_dir = root / "installed-skills"
            hooks_file.parent.mkdir(parents=True, exist_ok=True)
            hooks_file.write_text(
                json.dumps(
                    {
                        "hooks": {
                            "Stop": [
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/third-party.py",
                                            "timeoutSec": 60,
                                            "statusMessage": "third-party",
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            with ThreadPoolExecutor(max_workers=4) as pool:
                futures = [
                    pool.submit(self._run_upsert, UPSERT_CODEX_PATH, hooks_file, skills_dir)
                    for _ in range(4)
                ]
                for fut in as_completed(futures):
                    proc = fut.result()
                    self.assertEqual(proc.returncode, 0, msg=proc.stderr)

            hooks = json.loads(hooks_file.read_text(encoding="utf-8"))
            stop_groups = hooks["hooks"]["Stop"]

            self.assertEqual(len(stop_groups), 2)
            commands = [g["hooks"][0]["command"] for g in stop_groups]
            self.assertTrue(any("third-party" in c for c in commands))
            managed = [c for c in commands if "arch_controller_stop_hook.py" in c]
            self.assertEqual(len(managed), 1)

    def test_claude_session_start_parallel_upserts_converge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            settings_file = root / "claude/settings.json"
            skills_dir = root / "installed-skills"
            settings_file.parent.mkdir(parents=True, exist_ok=True)

            with ThreadPoolExecutor(max_workers=4) as pool:
                futures = [
                    pool.submit(
                        self._run_upsert,
                        UPSERT_CLAUDE_START_PATH,
                        settings_file,
                        skills_dir,
                    )
                    for _ in range(4)
                ]
                for fut in as_completed(futures):
                    proc = fut.result()
                    self.assertEqual(proc.returncode, 0, msg=proc.stderr)

            settings = json.loads(settings_file.read_text(encoding="utf-8"))
            start_groups = settings["hooks"]["SessionStart"]
            managed = [
                g
                for g in start_groups
                if any(
                    "arch_controller_stop_hook.py" in str(h.get("command", ""))
                    for h in g.get("hooks", [])
                )
            ]
            self.assertEqual(len(managed), 1)


if __name__ == "__main__":
    unittest.main()
