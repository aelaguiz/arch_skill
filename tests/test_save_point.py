import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "skills/save-point/scripts/savepoint.py"
SPEC = importlib.util.spec_from_file_location("savepoint", SCRIPT)
sp = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sp)

RUNTIME = "/opt/aimgr-claude-runtime/artifacts/2d03cd27e2b0df3f/claude"


class FindsClaude(unittest.TestCase):
    def test_the_programs_claude_code_runs_as(self):
        self.assertTrue(sp.is_claude("/Users/a/.local/share/claude/versions/2.1.321 --effort xhigh"))
        self.assertTrue(sp.is_claude(RUNTIME + " --effort xhigh"))
        self.assertTrue(sp.is_claude(RUNTIME))

    def test_not_the_processes_around_it(self):
        launcher = "/opt/aimgr-claude-runtime/artifacts/2d03cd27e2b0df3f/launcher v1 protected /h/.claude " + RUNTIME + " --effort xhigh"
        self.assertFalse(sp.is_claude(launcher))
        self.assertFalse(sp.is_claude("/opt/homebrew/bin/node /x/aimgr.js claude run pro1 opus"))
        self.assertFalse(sp.is_claude("/Users/a/.local/share/claude/versions/2.1.321 supervisor"))

    def test_record_is_found_in_the_account_folder(self):
        with tempfile.TemporaryDirectory() as home:
            sessions = Path(home) / ".aimgr/claude-homes/pro7/.claude/sessions"
            sessions.mkdir(parents=True)
            (sessions / "4242.json").write_text(json.dumps({"sessionId": "abc", "name": "n", "cwd": "/w"}))
            with patch.dict(os.environ, {"HOME": home}):
                rec = sp.claude_record(RUNTIME + " --effort xhigh", 4242)
        self.assertEqual((rec["session_id"], rec["account"]), ("abc", "pro7"))


class CarriesScratch(unittest.TestCase):
    def test_scratch_is_the_sessions_folder_in_the_launchs_private_folder(self):
        with tempfile.TemporaryDirectory() as home:
            private = Path(home) / ".aimgr/claude-homes/pro7/.claude/.aim-private-runtime-Ab12"
            mine = private / "claude-501/-w/abc"
            (mine / "scratchpad").mkdir(parents=True)
            (private / "claude-501/-w/other").mkdir()
            ps = {10: (1, "-zsh"), 20: (10, f"node /x/aimgr.js v1 protected {home}/.aimgr/claude-homes/pro7/.claude {private} 3"),
                  30: (20, RUNTIME + " --effort xhigh")}
            self.assertEqual(sp.private_folder(ps, 30), str(private))
            self.assertEqual(sp.scratch_of(ps, 30, "abc"), str(mine))
            self.assertIsNone(sp.scratch_of(ps, 30, "missing"))
            self.assertIsNone(sp.scratch_of({30: (1, RUNTIME)}, 30, "abc"))


if __name__ == "__main__":
    unittest.main()
