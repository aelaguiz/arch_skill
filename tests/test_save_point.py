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


class PutsScratchBack(unittest.TestCase):
    def run_case(self, resumed_id):
        with tempfile.TemporaryDirectory() as home:
            saved = Path(home) / "save/scratch/pods_w1_p1"
            (saved / "scratchpad/notes").mkdir(parents=True)
            (saved / "scratchpad/a.txt").write_text("a")
            (saved / "scratchpad/notes/b.txt").write_text("b")
            private = Path(home) / ".aimgr/claude-homes/pro7/.claude/.aim-private-runtime-New1"
            new = private / "claude-501/-w" / resumed_id
            (new / "scratchpad").mkdir(parents=True)
            (new / "scratchpad/a.txt").write_text("written since the resume")
            pane = {"session": "pods", "pane": "w1:p1", "agent": {"session_id": "abc", "stop": {
                "scratch_saved": str(saved), "scratch_from": f"{home}/.aimgr/claude-homes/pro7/.claude/.aim-private-runtime-Old1/claude-501/-w/abc"}}}
            ps = {20: (1, f"node /x/aimgr.js v1 protected {private} 3"), 30: (20, RUNTIME)}
            with patch.object(sp, "pane_claude", return_value=({"pid": 30, "session_id": resumed_id}, ps)):
                done = sp.scratch_back(pane)
            return done, saved.exists(), (new / "scratchpad/a.txt").read_text(), (new / "scratchpad/notes/b.txt").exists()

    def test_same_session_gets_its_files_and_keeps_what_it_wrote_since(self):
        done, copy_left, a, b = self.run_case("abc")
        self.assertEqual(done["files"], 2)
        self.assertEqual((copy_left, a, b), (False, "written since the resume", True))

    def test_a_session_moved_to_another_account_gets_none(self):
        done, copy_left, a, b = self.run_case("other-id")
        self.assertTrue(done["moved"])
        self.assertEqual((copy_left, b), (True, False))


if __name__ == "__main__":
    unittest.main()
