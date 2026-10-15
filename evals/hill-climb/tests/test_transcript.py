"""Layer 1: parsing the stream-json transcripts (PLAN.md 6.4, 6.8) on the probe transcripts of 2026-10-14."""
import json
import tempfile
import unittest
from pathlib import Path

from runner import transcript

GOLDEN = Path(__file__).resolve().parent / "golden"
PROBE1 = GOLDEN / "probe1_skill_and_subagent.jsonl"
PROBE2 = GOLDEN / "probe2_slash_skill.jsonl"
PROBE3 = GOLDEN / "probe3_gated_wait_stamped.jsonl"


class ProbeOneSkillAndSubagent(unittest.TestCase):
    """Unstamped stream: a Skill call, a background Agent dispatch, the subagent's Bash call and a main Write."""

    @classmethod
    def setUpClass(cls):
        cls.tr = transcript.parse(PROBE1)

    def test_calls_in_arrival_order(self):
        self.assertEqual([c["name"] for c in self.tr.calls], ["Skill", "Agent", "Bash", "Write"])
        self.assertFalse(self.tr.stamped)

    def test_parent_ids_and_depth(self):
        skill, agent, bash, write = self.tr.calls
        self.assertIsNone(agent["parent_id"])
        self.assertEqual(bash["parent_id"], agent["id"])
        self.assertEqual(bash["parent_id"], "toolu_01XoENEHotWCA7sJ9pwRUyeZ")
        self.assertEqual([c["depth"] for c in self.tr.calls], [0, 0, 1, 0])
        self.assertTrue(self.tr.is_subagent(bash))
        self.assertFalse(self.tr.is_subagent(write))
        self.assertIs(self.tr.dispatch_of(bash), agent)
        self.assertEqual(bash["agent_id"], "a940b92176e0e296d")

    def test_agent_dispatches(self):
        dispatches = self.tr.agent_calls
        self.assertEqual(len(dispatches), 1)
        self.assertEqual(dispatches[0]["input"]["model"], "sonnet")
        self.assertIn("Async agent launched", dispatches[0]["result_text"])

    def test_windows_from_event_timestamps(self):
        _skill, agent, bash, _write = self.tr.calls
        # the background dispatch returns at once; the subagent's call runs after it
        self.assertLess(agent["t_result"], bash["t_use"])
        self.assertAlmostEqual(bash["t_result"] - bash["t_use"], 0.325, places=2)
        self.assertEqual(bash["result_text"], "(Bash completed with no output)")
        self.assertFalse(bash["is_error"])

    def test_final_text_is_the_last_result(self):
        self.assertEqual(len(self.tr.results), 2)
        self.assertTrue(self.tr.final_text.startswith("The subagent finished and ran"))

    def test_cost_is_cumulative(self):
        self.assertAlmostEqual(self.tr.cost_usd, 0.0810038, places=6)

    def test_aim_lines_kept_raw(self):
        texts = [text for _t, text in self.tr.raw_lines]
        self.assertIn("[aim] Resume this session with:", texts)


class ProbeTwoSlashSkill(unittest.TestCase):
    def test_slash_invoked_skill(self):
        tr = transcript.parse(PROBE2)
        self.assertEqual([c["name"] for c in tr.calls], ["Write"])
        self.assertEqual(tr.final_text, "probe done")
        self.assertAlmostEqual(tr.cost_usd, 0.0184158, places=6)
        self.assertEqual(sorted(tr.init["tools"]), ["Bash", "Edit", "Read", "Skill", "Task", "Write"])
        self.assertIn("probe-skill", tr.init["skills"])
        self.assertEqual(tr.agent_calls, [])


class ProbeThreeGatedWaitStamped(unittest.TestCase):
    """Stamped stream: the checker's write lands before the gated command (PLAN.md 6.10: 25.1 s and 28.0 s)."""

    @classmethod
    def setUpClass(cls):
        cls.tr = transcript.parse(PROBE3)

    def test_stamped(self):
        self.assertTrue(self.tr.stamped)
        self.assertAlmostEqual(self.tr.t0, 1792028756.0345159, places=4)

    def test_windows_are_arrival_stamps(self):
        agent, sub_bash, cat, gated = self.tr.calls
        self.assertEqual(agent["name"], "Agent")
        self.assertAlmostEqual(agent["t_use"], 1792028758.560452, places=4)
        self.assertAlmostEqual(agent["t_result"], 1792028781.915779, places=4)
        self.assertAlmostEqual(sub_bash["t_use"], 1792028760.7216241, places=4)
        self.assertAlmostEqual(sub_bash["t_result"], 1792028781.125251, places=4)
        self.assertEqual(sub_bash["parent_id"], agent["id"])
        self.assertEqual(sub_bash["depth"], 1)
        self.assertEqual(cat["result_text"], "PASS")
        self.assertEqual(gated["input"]["command"], "echo launched > launch.txt")

    def test_checker_write_before_gated_command(self):
        _agent, sub_bash, _cat, gated = self.tr.calls
        t0 = self.tr.t0
        self.assertAlmostEqual(sub_bash["t_result"] - t0, 25.1, delta=0.1)
        self.assertAlmostEqual(gated["t_use"] - t0, 28.0, delta=0.1)
        self.assertLess(sub_bash["t_result"], gated["t_use"])

    def test_foreground_dispatch_waits(self):
        agent = self.tr.agent_calls[0]
        self.assertFalse(agent["input"]["run_in_background"])
        self.assertIn("[Subagent hand-back]", agent["result_text"])
        start, end = self.tr.window(agent)
        self.assertGreater(end - start, 20)

    def test_final_text_and_cost(self):
        self.assertTrue(self.tr.final_text.startswith("The checker finished"))
        self.assertAlmostEqual(self.tr.cost_usd, 0.0499294, places=6)
        self.assertTrue(self.tr.ok)
        self.assertFalse(self.tr.budget_hit)

    def test_raw_lines_stamped(self):
        self.assertEqual([text for _t, text in self.tr.raw_lines][:2], ["", "[aim] Resume this session with:"])
        self.assertTrue(all(t is not None for t, _text in self.tr.raw_lines))


class Robustness(unittest.TestCase):
    def write(self, lines):
        folder = tempfile.mkdtemp()
        path = Path(folder) / "stream.jsonl"
        path.write_text("".join(line + "\n" for line in lines), encoding="utf-8")
        return path

    @staticmethod
    def use(t, cid, name, parent=None, inp=None):
        return json.dumps({"t": t, "e": {"type": "assistant", "parent_tool_use_id": parent, "message": {
            "content": [{"type": "tool_use", "id": cid, "name": name, "input": inp or {}}]}}})

    @staticmethod
    def result(t, cid, content="ok", parent=None, is_error=False):
        return json.dumps({"t": t, "e": {"type": "user", "parent_tool_use_id": parent, "message": {
            "content": [{"type": "tool_result", "tool_use_id": cid, "content": content, "is_error": is_error}]}}})

    def test_nested_subagent_depth_and_task_name(self):
        path = self.write([
            self.use(1.0, "a1", "Task", inp={"prompt": "outer"}),
            self.use(2.0, "a2", "Agent", parent="a1", inp={"prompt": "inner"}),
            self.use(3.0, "b1", "Bash", parent="a2", inp={"command": "echo hi"}),
            self.result(4.0, "b1", [{"type": "text", "text": "hi"}, {"type": "text", "text": "there"}], parent="a2"),
            self.result(5.0, "a2", "done", parent="a1"),
            self.result(6.0, "a1", "done"),
        ])
        tr = transcript.parse(path)
        by = {c["id"]: c for c in tr.calls}
        self.assertEqual([by[i]["depth"] for i in ("a1", "a2", "b1")], [0, 1, 2])
        self.assertIs(tr.dispatch_of(by["b1"]), by["a1"])
        self.assertTrue(tr.is_subagent(by["a2"]))
        self.assertEqual(by["b1"]["result_text"], "hi\nthere")
        self.assertEqual([c["id"] for c in tr.agent_calls], ["a1"])

    def test_missing_result_runs_to_the_end(self):
        path = self.write([self.use(1.0, "b1", "Bash"), json.dumps({"t": 9.5, "raw": "killed"})])
        tr = transcript.parse(path)
        self.assertIsNone(tr.calls[0]["t_result"])
        self.assertEqual(tr.window(tr.calls[0]), (1.0, 9.5))
        self.assertIsNone(tr.cost_usd)
        self.assertEqual(tr.final_text, "")

    def test_truncated_line_and_error_flags(self):
        path = self.write([
            self.use(1.0, "b1", "Bash"),
            self.result(2.0, "b1", "boom", is_error=True),
            '{"t": 3.0, "e": {"type": "assist',
            json.dumps({"t": 4.0, "e": {"type": "result", "subtype": "error_max_budget_usd", "is_error": True,
                                        "total_cost_usd": 5.01}}),
        ])
        tr = transcript.parse(path)
        self.assertTrue(tr.calls[0]["is_error"])
        self.assertTrue(tr.budget_hit)
        self.assertFalse(tr.ok)
        self.assertAlmostEqual(tr.cost_usd, 5.01)

    def test_missing_file_is_empty(self):
        tr = transcript.parse(Path(tempfile.mkdtemp()) / "nope.jsonl")
        self.assertEqual(tr.calls, [])
        self.assertIsNone(tr.last_result)


if __name__ == "__main__":
    unittest.main()
