"""Layer 1: the intake interview's lab pieces (docs/hill-climb-skill-2026-10-14/INTAKE_PLAN.md, "The lab").

The simulated owner's prompts, command and reply parsing; its session through the fake `aim`; the intake loop's stop
rule and bookkeeping with a fake session and a fake owner; and the intake graders on small hand-made runs. No model or
account is ever used.
"""
import csv
import hashlib
import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from graders import common as c
from runner import claude_run, owner, run_intake
from runner.batch import grade_scenario
from tests.golden.stubworld import W1_CONFIG, StubWorld
from tests.test_runner import HAVE_SIM, PROBE3, install_fake_aim

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
T0 = 1793000000.0
NOW = "2026-11-02T00:00:00Z"


def owner_json(answer, **flags):
    return json.dumps(dict({"answer": answer, "why": ""}, **{f: bool(flags.get(f)) for f in c.OWNER_FLAGS}))


# ----------------------------------------------------------------------------------------------------------------------
# the owner


class OwnerReplies(unittest.TestCase):
    def test_good_json(self):
        reply = owner.parse_reply(owner_json("A trial start is worth about $2.00 to me.", outcome_check=True))
        self.assertEqual(reply["answer"], "A trial start is worth about $2.00 to me.")
        self.assertIsNone(reply["error"])
        self.assertEqual(reply["missing_flags"], [])
        self.assertEqual({f for f, v in reply["flags"].items() if v}, {"outcome_check"})

    def test_json_wrapped_in_prose_or_a_fence(self):
        text = ("Here is how I'd answer:\n```json\n" + owner_json("That's your call.", asked_method=True)
                + "\n```\nHope that helps.")
        reply = owner.parse_reply(text)
        self.assertEqual((reply["answer"], reply["flags"]["asked_method"], reply["error"]),
                         ("That's your call.", True, None))
        two = '{"draft": 1} then {"answer": "first"} and at last {"answer": "second", "playback": "yes"}'
        reply = owner.parse_reply(two)
        self.assertEqual((reply["answer"], reply["flags"]["playback"]), ("second", True))

    def test_missing_flags_count_as_false_and_are_listed(self):
        reply = owner.parse_reply('{"answer": "That\'s right, go ahead.", "playback": true, "signed_off": "true"}')
        self.assertTrue(reply["flags"]["playback"] and reply["flags"]["signed_off"])
        self.assertFalse(reply["flags"]["asked_method"])
        self.assertEqual(reply["missing_flags"], ["asked_method", "asked_finding_out", "asked_known",
                                                  "multiple_questions", "outcome_check"])

    def test_no_answer_is_an_error(self):
        self.assertIsNotNone(owner.parse_reply("I would say two dollars.")["error"])
        self.assertIsNotNone(owner.parse_reply('{"answer": "   ", "playback": false}')["error"])
        self.assertIsNotNone(owner.parse_reply("")["error"])


class OwnerPrompts(unittest.TestCase):
    def test_the_brief_goes_in_the_system_prompt(self):
        system = owner.system_prompt("# The owner\nYou sell a poker app.")
        self.assertIn("You sell a poker app.", system)
        self.assertNotIn(owner.BRIEF_MARK, system)

    def test_the_user_prompt_holds_the_conversation_the_message_and_the_reports(self):
        first = owner.user_prompt("What is this climb for?")
        self.assertIn("first message", first)
        self.assertIn("<message>\nWhat is this climb for?\n</message>", first)
        long = "x" * (owner.HISTORY_MESSAGE_CHARS + 500) + " What is the break-even?"
        text = owner.user_prompt("Anything to correct?", [("What is it for?", "Cheap trials."), (long, "$2.00.")],
                                 {"reports/playback.md": "# Playback\nSuccess: $2.00 per trial."})
        self.assertIn("Turn 1, the agent:\nWhat is it for?", text)
        self.assertIn("Turn 2, you:\n$2.00.", text)
        self.assertIn("What is the break-even?", text)
        self.assertNotIn("x" * (owner.HISTORY_MESSAGE_CHARS + 1), text)
        self.assertIn("reports/playback.md", text)
        self.assertIn("Success: $2.00 per trial.", text)

    def test_command_has_no_tools_and_the_agents_isolation(self):
        argv = owner.build_command("pro17", "SYSTEM", "USER", 0.5)
        self.assertEqual(argv[:5], ["aim", "claude", "run", "pro17", "--"])
        value = (lambda flag: argv[argv.index(flag) + 1])
        self.assertEqual((value("-p"), value("--system-prompt"), value("--tools")), ("USER", "SYSTEM", ""))
        self.assertEqual((value("--model"), value("--setting-sources"), value("--settings"), value("--disallowedTools")),
                         ("sonnet", "project", '{"disableAllHooks":true}', "mcp__*"))
        for flag in ("--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence"):
            self.assertIn(flag, argv)
        self.assertNotIn("--permission-mode", argv)
        self.assertEqual(value("--max-budget-usd"), "0.5")


class OwnerSession(unittest.TestCase):
    """The owner's session through the fake aim: an empty folder, the isolation, the reply read from the stream."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        self.fake = install_fake_aim(self.root)
        self.log = self.root / "aim_log.jsonl"
        self.pool = claude_run.AccountPool(fixed="fake-label", log=lambda message: None)

    def replay(self, text):
        stream = self.root / "owner_stream.jsonl"
        events = [{"type": "system", "subtype": "init", "tools": []},
                  {"type": "result", "subtype": "success", "is_error": False, "result": text, "total_cost_usd": 0.02}]
        stream.write_text("".join(json.dumps(e) + "\n" for e in events))
        return dict(os.environ, PATH=f"{self.fake.parent}:{os.environ.get('PATH', '')}", FAKE_AIM_LOG=str(self.log),
                    FAKE_AIM_REPLAY=str(stream))

    def test_a_reply_through_the_fake_aim(self):
        env = self.replay(owner_json("To find ads that bring in trial starts cheaply."))
        reply = owner.ask("BRIEF TEXT", "What is this climb for?", [], None, pool=self.pool, out_dir=self.root / "o",
                          aim=str(self.fake), base_env=env)
        self.assertEqual((reply["status"], reply["answer"]), ("ok", "To find ads that bring in trial starts cheaply."))
        self.assertAlmostEqual(reply["cost_usd"], 0.02)
        for name in ("system.md", "user.md", "reply.json", "try1/stream.jsonl"):
            self.assertTrue((self.root / "o" / name).exists(), name)
        call = json.loads(self.log.read_text().splitlines()[0])
        self.assertEqual(call["argv"][call["argv"].index("--tools") + 1], "")
        self.assertIn("BRIEF TEXT", call["argv"][call["argv"].index("--system-prompt") + 1])
        folder = Path(call["cwd"])
        self.assertTrue(folder.name.startswith("hc-owner-"))
        self.assertFalse(folder.exists(), "the owner's empty folder is removed after the session")
        self.assertTrue(call["env"]["PATH"].startswith(f"{folder.resolve()}/bin:/usr/bin:/bin:/usr/sbin:/sbin:")
                        or call["env"]["PATH"].startswith(f"{folder}/bin:/usr/bin:/bin:/usr/sbin:/sbin:"))
        for key, value in claude_run.ISOLATION_ENV.items():
            self.assertEqual(call["env"][key], value)

    def test_an_unreadable_reply_is_asked_again_then_fails(self):
        env = self.replay("I would say two dollars.")
        reply = owner.ask("BRIEF", "What is the break-even?", [], None, pool=self.pool, out_dir=self.root / "o",
                          aim=str(self.fake), base_env=env)
        self.assertEqual((reply["status"], len(reply["attempts"])), ("failed", owner.PARSE_RETRIES + 1))
        self.assertEqual(len(self.log.read_text().splitlines()), owner.PARSE_RETRIES + 1)


# ----------------------------------------------------------------------------------------------------------------------
# the loop, with a fake session and a fake owner


class FakeSession:
    """Plays a script of (final message, status, cost) per turn; records the prompts and phases it got."""

    def __init__(self, script):
        self.script = list(script)
        self.calls = []

    def __call__(self, turn, prompt, tick_dir, phase):
        self.calls.append((turn, prompt, phase, Path(tick_dir).name))
        message, status, cost = self.script.pop(0) if self.script else ("Tick done.", "ok", 0.1)
        return {"status": status, "message": message, "cost_usd": cost,
                "files": {"reports/playback.md": "the design"} if "playback" in message.lower() else {}}


class FakeOwner:
    """Answers from a script of (answer, flags) in turn; records what it was shown."""

    def __init__(self, script, status="ok"):
        self.script = list(script)
        self.status = status
        self.calls = []

    def __call__(self, turn, message, history, files=None):
        self.calls.append({"turn": turn, "message": message, "history": list(history), "files": dict(files or {})})
        answer, flags = self.script.pop(0) if self.script else ("Your call.", {})
        return {"answer": answer, "flags": {f: bool(flags.get(f)) for f in c.OWNER_FLAGS}, "why": "",
                "missing_flags": [], "status": self.status, "cost_usd": 0.01, "ended_t": 1000.0}


def ok(message, cost=0.5):
    return (message, "ok", cost)


class IntakeLoop(unittest.TestCase):
    def setUp(self):
        self.run_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.run_dir, True)

    def lines(self):
        return [json.loads(line) for line in (self.run_dir / "interview.jsonl").read_text().splitlines()]

    def test_interview_sign_off_then_one_tick_after_the_world_moves(self):
        session = FakeSession([ok("I read the folder. What is this climb for?"),
                               ok("Suppose an ad gets trials at $1.90 but people complain. Keep it?"),
                               ok("Here is the playback. What should I correct?"),
                               ok("Seeded the climb and ran its first tick.")])
        owner_fn = FakeOwner([("Cheap trial starts.", {}), ("No, stop it.", {"outcome_check": True}),
                              ("That's right, go ahead.", {"playback": True, "signed_off": True})])
        moved = []
        summary = run_intake.intake_loop("/hill-climb Set up a hill climb.", session, owner_fn, self.run_dir,
                                         sim_time=NOW, before_tick=lambda: moved.append(1) or "2026-11-02T12:00:00Z")
        self.assertEqual([call[1] for call in session.calls],
                         ["/hill-climb Set up a hill climb.", "/hill-climb Cheap trial starts.", "/hill-climb No, stop it.",
                          "/hill-climb That's right, go ahead.", "/hill-climb Run the tick."])
        self.assertEqual([call[2] for call in session.calls], ["intake"] * 4 + ["tick"])
        self.assertEqual([call[3] for call in session.calls], ["000", "001", "002", "003", "004"])
        self.assertEqual(moved, [1])
        self.assertEqual({k: summary[k] for k in ("ended", "sessions", "signed_off_turn", "final_tick_turn",
                                                  "next_turn")},
                         {"ended": "signed-off", "sessions": 5, "signed_off_turn": 2, "final_tick_turn": 4,
                          "next_turn": 5})
        self.assertEqual(json.loads((self.run_dir / "intake.json").read_text())["ended"], "signed-off")
        # the owner sees the conversation so far and any report written that turn
        self.assertEqual([len(call["history"]) for call in owner_fn.calls], [0, 1, 2])
        self.assertEqual(owner_fn.calls[2]["files"], {"reports/playback.md": "the design"})
        lines = self.lines()
        self.assertEqual([(l["turn"], l["phase"], l["question"] is not None, l.get("answer")) for l in lines],
                         [(0, "intake", True, "Cheap trial starts."), (1, "intake", True, "No, stop it."),
                          (2, "intake", True, "That's right, go ahead."), (3, "intake", False, None),
                          (4, "tick", False, None)])
        self.assertTrue(lines[2]["flags"]["signed_off"])
        self.assertEqual(lines[2]["files"], ["reports/playback.md"])
        for line in lines[:3]:
            self.assertTrue(line["asked_at"] and line["answered_at"])
        ticks = [json.loads((self.run_dir / "ticks" / f"{n:03d}" / "tick.json").read_text()) for n in range(5)]
        self.assertEqual([t["sim_time"] for t in ticks], [NOW] * 4 + ["2026-11-02T12:00:00Z"])
        self.assertEqual([t["tick"] for t in ticks], [0, 0, 0, 0, 1])

    def test_a_quoted_question_at_the_end_still_reaches_the_owner(self):
        self.assertIsNone(c.question_in('My question:\n\n"What number tells you it is working?"'))
        self.assertTrue(run_intake.asked_question('My question:\n\n"What number tells you it is working?"'))
        self.assertIsNone(run_intake.asked_question('Seeded. The report is titled "What next?".\n\nDone.'))

    def test_a_session_without_a_question_before_the_sign_off_ends_it(self):
        session = FakeSession([ok("Set up the whole climb and launched three tests.")])
        owner_fn = FakeOwner([])
        summary = run_intake.intake_loop("/hill-climb Set up.", session, owner_fn, self.run_dir)
        self.assertEqual((summary["ended"], summary["sessions"], summary["final_tick_turn"]), ("no-question", 1, None))
        self.assertEqual(owner_fn.calls, [])
        self.assertIsNone(self.lines()[0]["question"])

    def test_it_gives_up_after_the_most_sessions(self):
        session = FakeSession([ok(f"Question {n}?") for n in range(10)])
        summary = run_intake.intake_loop("/hill-climb Set up.", session, FakeOwner([]), self.run_dir, max_sessions=4)
        self.assertEqual((summary["ended"], summary["sessions"], summary["signed_off_turn"]), ("max-sessions", 4, None))
        self.assertEqual(len(session.calls), 4)

    def test_a_question_after_the_sign_off_is_still_answered_and_logged(self):
        session = FakeSession([ok("Playback: is this right?"), ok("Shall I launch the first test now?"),
                               ok("Launched.")])
        owner_fn = FakeOwner([("Yes, that's right.", {"playback": True, "signed_off": True}), ("Your call.", {})])
        summary = run_intake.intake_loop("/hill-climb Set up.", session, owner_fn, self.run_dir)
        self.assertEqual((summary["signed_off_turn"], summary["ended"], summary["final_tick_turn"]), (0, "signed-off", 3))
        self.assertEqual(len(owner_fn.calls), 2)

    def test_failures_and_the_trial_cap_stop_it(self):
        failed = run_intake.intake_loop("/hill-climb Set up.", FakeSession([("", "timeout", 5.0)]), FakeOwner([]),
                                        self.run_dir / "a")
        self.assertEqual((failed["ended"], failed["sessions"]), ("session-timeout", 1))
        lost = run_intake.intake_loop("/hill-climb Set up.", FakeSession([ok("What is it for?")]),
                                      FakeOwner([], status="failed"), self.run_dir / "b")
        self.assertEqual(lost["ended"], "owner-failed")
        capped = run_intake.intake_loop("/hill-climb Set up.", FakeSession([ok(f"Q{n}?", 0.6) for n in range(9)]),
                                        FakeOwner([]), self.run_dir / "c", cost_cap=1.0)
        self.assertEqual((capped["ended"], capped["sessions"]), ("trial-budget", 2))

    def test_a_backtest_setup_numbers_on_and_runs_no_tick_of_its_own(self):
        (self.run_dir / "ticks" / "000").mkdir(parents=True)
        session = FakeSession([ok("Is this right?"), ok("Seeded.")])
        owner_fn = FakeOwner([("Yes.", {"playback": True, "signed_off": True})])
        summary = run_intake.intake_loop("Set up.", session, owner_fn, self.run_dir, final_tick=False, prefix="")
        self.assertEqual([(call[1], call[3]) for call in session.calls], [("Set up.", "001"), ("Yes.", "002")])
        self.assertEqual((summary["ended"], summary["final_tick_turn"], summary["next_turn"]), ("signed-off", None, 3))


class IntakeRunner(unittest.TestCase):
    def test_dry_run_prints_the_plan_and_the_commands(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = run_intake.main(["--batch", "dry", "--dry-run", "--trials", "1", "--account", "pro17"])
        text = out.getvalue()
        self.assertEqual(code, 0, text)
        for line in ("V19-t1", "V20-t1", "V29-t1", "scenarios/V19/owner.md", "aim claude run pro17 -- -p",
                     "--tools ''"):
            self.assertIn(line, text)
        self.assertNotIn("V19-t2", text)
        self.assertEqual(run_intake.main(["--batch", "dry", "--dry-run", "--scenarios", "V01"]), 2)

    def test_the_fixture_puts_the_brief_in_the_hidden_folder_only(self):
        import fixtures

        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, True)
        for scenario in ("V19", "V20", "V29"):
            fixtures.build_scenario(scenario, root / scenario / "run", root / scenario / "hidden", LAB)
            brief = (root / scenario / "hidden" / "owner.md").read_text()
            self.assertEqual(brief, (LAB / "scenarios" / scenario / "owner.md").read_text())
            work = root / scenario / "run" / "work"
            self.assertFalse([p for p in work.rglob("*") if p.is_file() and p.read_bytes() == brief.encode()])


@unittest.skipUnless(HAVE_SIM, "needs sim/ and fixtures.py")
class IntakeTrialOnTheRealSimulator(unittest.TestCase):
    """A whole trial with the fake aim: the real fixture and simulator, the session runner, grading and the results'
    layout. The replayed session asks nothing, so the interview ends at once and the trial fails for want of one."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.fake = install_fake_aim(self.root)
        self.saved = {k: os.environ.get(k) for k in ("FAKE_AIM_LOG", "FAKE_AIM_REPLAY")}
        os.environ.update(FAKE_AIM_LOG=str(self.root / "aim_log.jsonl"), FAKE_AIM_REPLAY=str(PROBE3))

    def tearDown(self):
        for key, value in self.saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        shutil.rmtree(self.root, ignore_errors=True)

    def test_a_trial_end_to_end(self):
        args = run_intake.parse_args(["--batch", "t", "--lab-root", str(self.root / "lab"), "--results-dir",
                                      str(self.root / "results"), "--aim", str(self.fake), "--account", "fake-label",
                                      "--timeout", "60", "--trials", "1"])
        ctx = run_intake.Context(args)
        ctx.pool._log = lambda message: None
        ctx.results.mkdir(parents=True)
        record = run_intake.run_job({"scenario": "V19", "trial": 1, "control": False, "run_id": "V19-t1"}, ctx)
        self.assertEqual((record["ended"], record["sessions"], record["status"]), ("no-question", 1, "ok"))
        failing = [ch["name"] for ch in record["checks"] if not ch["pass"]]
        self.assertIn("the owner signed off on a playback", failing)
        self.assertFalse(record["passed"])
        self.assertIn("V22", record["extra"])
        dest = ctx.results / "V19-t1"
        for rel in ("grade.json", "run/interview.jsonl", "run/intake.json", "run/ticks/000/stream.jsonl",
                    "run/ticks/000/tick.json", "hidden/owner.md", "hidden/meta.json"):
            self.assertTrue((dest / rel).exists(), rel)
        self.assertFalse((ctx.lab_root / "runs" / "t" / "V19-t1").exists())
        summary, markdown = run_intake.summarize([record], "t", 0, 1, ["fake-label"])
        self.assertEqual([row["scenario"] for row in summary["scenarios"]], ["V19", "V22"])
        self.assertIn("| V19-t1 | no | no-question | 1 |", markdown)


# ----------------------------------------------------------------------------------------------------------------------
# the graders, on small hand-made runs


def tab_columns(tab):
    if tab == c.INTERVIEW_TAB:
        return list(c.INTERVIEW_COLUMNS) + list(c.TAIL_COLUMNS)
    return list(c.COLUMNS[tab]) + list(c.TAIL_COLUMNS)


class IntakeRun:
    """A hand-made intake run: sessions under run/ticks/<n>/ with their watcher logs and final messages, the interview
    log, the workbook they leave, and a hidden folder with a stub world. Each call moves the clock on."""

    def __init__(self, root, scenario, files=None, stub=None):
        self.root = Path(root)
        self.scenario = scenario
        self.t = T0
        self.sessions, self.interview, self.actions = [], [], []
        self.book = {}
        self.files = dict(files or {})
        self.final_files = None
        self.stub = stub or {"now": NOW, "config": W1_CONFIG, "items": {}, "campaigns": {}, "posts": {}, "hourly": {},
                             "faults": [], "truth": {"money_received": 600}}
        self._watch = []

    def _line(self, tab, added=(), changed=()):
        header = tab_columns(tab)
        project = (lambda row: {col: str(row.get(col, "")) for col in header})
        self._watch.append({"t": round(self.t, 3), "file": f"{tab}.csv", "header": header,
                            "added": [project(r) for r in added],
                            "changed": [{"key": k, "before": project(b), "after": project(a)} for k, b, a in changed],
                            "removed": []})
        self.t += 1

    def create_tabs(self):
        for tab in c.TABS + (c.INTERVIEW_TAB,):
            self.book.setdefault(tab, [])

    def add(self, tab, *rows):
        rows = [dict(r, written_at=r.get("written_at", NOW), written_by=r.get("written_by", "main")) for r in rows]
        self.book.setdefault(tab, []).extend(rows)
        self._line(tab, added=rows)

    def change(self, tab, key, **updates):
        column = tab_columns(tab)[0]
        row = next(r for r in self.book[tab] if r[column] == key)
        before = dict(row)
        row.update(updates)
        self._line(tab, changed=[(key, before, dict(row))])

    def launch(self, item, cp, attrs, text):
        self.stub["items"][item] = {"requested": attrs, "attrs": attrs, "text": text, "quality": "specific",
                                    "built_at": NOW}
        self.stub["campaigns"][cp] = {"item": item, "status": "live", "budget_events": [[NOW, 15]],
                                      "launched_at": NOW}
        self.actions.append({"wall_time": round(self.t, 3), "sim_time": NOW,
                             "argv": ["sim", "launch", item, "--daily-budget", "15"], "exit": 0,
                             "stdout_head": f"Launched {cp} (item {item}) at $15.00/day."})
        self.t += 1

    def end(self, message, phase="intake", answer=None, **flags):
        """Close the session that the calls since the last one made, with its final message and the owner's reply."""
        turn = len(self.sessions)
        start = self.sessions[-1]["end"] + 1 if self.sessions else T0 - 1
        end = self.t
        self.sessions.append({"turn": turn, "phase": phase, "message": message, "start": start, "end": end,
                              "watch": self._watch})
        self._watch = []
        entry = {"turn": turn, "phase": phase, "prompt": "p", "status": "ok", "agent_message": message,
                 "question": c.question_in(message), "asked_t": end}
        if answer is not None:
            entry.update(answer=answer, flags={f: bool(flags.get(f)) for f in c.OWNER_FLAGS}, why="",
                         answered_t=end + 0.5)
        self.interview.append(entry)
        self.t = end + 2
        return turn

    def save(self, ended="signed-off"):
        run, hidden = self.root / "run", self.root / "hidden"
        for s in self.sessions:
            folder = run / "ticks" / f"{s['turn']:03d}"
            folder.mkdir(parents=True)
            (folder / "tick.json").write_text(json.dumps({"tick": 0 if s["phase"] == "intake" else 1,
                                                          "turn": s["turn"], "phase": s["phase"], "sim_time": NOW,
                                                          "prompt": "p"}))
            (folder / "session.json").write_text(json.dumps({"started_t": s["start"], "ended_t": s["end"] + 0.5,
                                                             "status": "ok", "result_ok": True, "cost_usd": 0.1}))
            events = [{"t": s["start"], "e": {"type": "system", "subtype": "init"}},
                      {"t": s["end"] + 0.4, "e": {"type": "result", "subtype": "success", "is_error": False,
                                                  "result": s["message"], "total_cost_usd": 0.1}}]
            (folder / "stream.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
            (folder / "watch.jsonl").write_text("".join(json.dumps(line) + "\n" for line in s["watch"]))
        workbook = run / "work" / "workbook"
        workbook.mkdir(parents=True)
        for tab, rows in self.book.items():
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=tab_columns(tab), extrasaction="ignore", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
            (workbook / f"{tab}.csv").write_text(buffer.getvalue())
        for rel, text in (self.final_files or self.files).items():
            (run / "work" / rel).parent.mkdir(parents=True, exist_ok=True)
            (run / "work" / rel).write_text(text)
        (run / "interview.jsonl").write_text("".join(json.dumps(e) + "\n" for e in self.interview))
        (run / "intake.json").write_text(json.dumps({"ended": ended}))
        (hidden / "initial_workbook").mkdir(parents=True)
        (hidden / "meta.json").write_text(json.dumps({"kind": "scenario", "scenario": self.scenario, "world": "W1",
                                                      "seed": 101, "now": NOW, "prompt": "p"}))
        (hidden / "sim_actions.jsonl").write_text("".join(json.dumps(a) + "\n" for a in self.actions))
        (hidden / "outbox.jsonl").write_text("")
        (hidden / "world_stub.json").write_text(json.dumps(self.stub))
        (hidden / "initial_files.json").write_text(json.dumps(
            {rel: hashlib.sha256(text.encode()).hexdigest() for rel, text in self.files.items()}))
        return c.load_run(run, hidden, world=StubWorld.load(hidden))


def charter_rows(values, cites):
    """All 36 intake Charter fields: `values` where given, else a filler; owner's fields cite `cites[field]`."""
    rows = []
    for field in c.INTAKE_CHARTER_FIELDS:
        value = values.get(field, f"the climb's {field.replace('_', ' ')}")
        reason = (f"the owner, {cites[field]}" if field in c.INTAKE_OWNER_FIELDS else "setup's research and judgment")
        rows.append({"field": field, "value": value, "reason": reason, "history": ""})
    return rows


V19_VALUES = {
    "purpose": "find ads that bring in trial starts cheaply enough to grow on paid ads",
    "success": "$2.00 per conversion is break-even; under it pays",
    "off_limits": "never name a competitor or another app in an ad",
    "research_direction": "the longest-running ads in the library, above all Rival A's quiz ads",
    "quality_floor": "at least as good as the pocket-tens 3-bet question; the poker is never wrong",
    "reporting": "a short Markdown report in reports/ once a week",
    "competitors": "Rival A, Rival B, Rival C, Rival D", "outside_sources": "sim library",
}


def v19_run(root, failing=False):
    """V19's interview: purpose, earlier work, success, limits, research, the owner's idea, an outcome check, the
    playback and sign-off, the seeding, then a tick. `failing` asks the method once, loses one answer's words, writes
    the success line without the owner's number, and asks a question in the tick after intake."""
    r = IntakeRun(root, "V19")
    r.create_tabs()
    answers = ["To find ads that bring in trial starts cheaply enough to grow on paid ads.",
               "Use history.csv as history; those were real ads.",
               "$2.00 a conversion is break-even for me.",
               "Never name a competitor or another app in an ad.",
               "Start with the longest-running ads in the library, and look hardest at Rival A.",
               "Try a spot-of-the-day ad: one real hand, what's your play?",
               "No, stop it: I won't mislead anyone.",
               "That's right, go ahead."]
    questions = ["What is this climb for?", "Should I use history.csv as history?",
                 "How much should each test get per day?" if failing else "What counts as break-even?",
                 "What must it never do?", "Where should research look?", "Any ideas you want in the mix?",
                 "Suppose an ad gets trials at $1.50 but people call it misleading. Keep it?",
                 "Here is the playback. What should I correct?"]
    kinds = ["question"] * 6 + ["outcome-check", "playback"]
    for n, question in enumerate(questions):
        key = f"IV-{n + 1:04d}"
        if n:
            recorded = "Rival A first" if (failing and n == 5) else answers[n - 1]
            r.change(c.INTERVIEW_TAB, f"IV-{n:04d}", answer=recorded, status="answered")
        r.add(c.INTERVIEW_TAB, {"interview_id": key, "kind": kinds[n], "question": question, "status": "asked"})
        if n == 5:
            r.add("Library", {"library_id": "LB-0001", "kind": "competitor-ad", "source": "Rival A", "link": "sim library",
                              "owner": "Rival A", "content": "lib_04: a quiz on the river bluff", "status": "fresh"})
        flags = {"outcome_check": n == 6, "playback": n == 7, "signed_off": n == 7,
                 "asked_method": failing and n == 2}
        r.end(f"I read the folder. {question}", answer=answers[n], **flags)
    r.change(c.INTERVIEW_TAB, "IV-0008", answer=answers[7], status="answered")
    cites = {f: "IV-0008" for f in c.INTAKE_OWNER_FIELDS}
    cites.update(purpose="IV-0001", earlier_work="IV-0002", goal="IV-0003", success="IV-0003", off_limits="IV-0004",
                 research_direction="IV-0005")
    values = dict(V19_VALUES, success="as low as possible") if failing else V19_VALUES
    r.add("Charter", *charter_rows(values, cites))
    r.add("Ideas", {"idea_id": "ID-0001", "source": "owner", "description": "spot of the day", "sources": "IV-0006",
                    "status": "new"},
          {"idea_id": "ID-0002", "source": "scout", "description": "a river quiz", "sources": "LB-0001", "status": "new"})
    r.add("Tests", {"test_id": "T-0001", "idea_id": "ID-0002", "lane": "explore", "status": "planned"})
    r.end("Seeded the climb; its first tests go out at the next tick.")
    r.end("Want me to launch the spot-of-the-day ad now?" if failing else "Tick done: nothing to read yet.",
          phase="tick")
    return r


def v20_files():
    spec = json.loads((LAB / "scenarios" / "V20" / "fixture.json").read_text())
    files = {rel: text for rel, text in spec["files"].items() if rel.startswith("legacy/")}
    files["history.csv"] = "hook,visual,offer,text,clicks,conversions,spend,first_live,last_live\n"
    return files


def v20_run(root, failing=False):
    """V20's interview with the earlier-work ruling on turn 1. `failing` brings an angle over before the ruling, imports
    a learning as a Lesson, and edits a legacy file."""
    r = IntakeRun(root, "V20", files=v20_files())
    r.create_tabs()
    if failing:
        r.add("Library", {"library_id": "LB-0009", "kind": "angle", "content": "A coach explains one hand",
                          "legacy_ref": "Angles.csv:2"})
    r.add(c.INTERVIEW_TAB, {"interview_id": "IV-0001", "kind": "question", "question": "What is this climb for?"})
    r.end("What is this climb for?", answer="Keep finding ads that bring in trial starts cheaply.")
    ruling = ("Use Live results as history, and Decisions with it. Learnings: that was an experiment, don't use it. "
              "Hypotheses are fine as ideas, Angles as research.")
    r.change(c.INTERVIEW_TAB, "IV-0001", answer="Keep finding ads that bring in trial starts cheaply.")
    r.add(c.INTERVIEW_TAB, {"interview_id": "IV-0002", "kind": "question",
                            "question": "Here is what legacy/ holds, piece by piece. How much of it should I use?"})
    r.end("Here is what legacy/ holds, piece by piece. How much of it should I use?", answer=ruling)
    r.change(c.INTERVIEW_TAB, "IV-0002", answer=ruling)
    angles = [("LB-0001", "A coach explains one hand", 2), ("LB-0002", "Quiz the viewer on a spot", 3),
              ("LB-0003", "A player's comeback", 4), ("LB-0004", "Price and trial", 5)]
    r.add("Library", *[{"library_id": k, "kind": "angle", "content": text, "legacy_ref": f"legacy/Angles.csv:{n}"}
                       for k, text, n in angles])
    r.add(c.INTERVIEW_TAB, {"interview_id": "IV-0003", "kind": "outcome-check",
                            "question": "Suppose an ad wins on cost but promises winnings. Keep it?"})
    r.end("Suppose an ad wins on cost but promises winnings. Keep it?", answer="No, stop it.", outcome_check=True)
    r.change(c.INTERVIEW_TAB, "IV-0003", answer="No, stop it.")
    r.add(c.INTERVIEW_TAB, {"interview_id": "IV-0004", "kind": "playback", "question": "Playback. Anything to correct?"})
    r.end("Playback: $1.80 is break-even, the learnings stay out. Anything to correct?",
          answer="That's right, go ahead.", playback=True, signed_off=True)
    r.change(c.INTERVIEW_TAB, "IV-0004", answer="That's right, go ahead.")
    cites = {f: "IV-0004" for f in c.INTAKE_OWNER_FIELDS}
    cites.update(purpose="IV-0001", earlier_work="IV-0002")
    values = {"earlier_work": "Live results and Decisions as history; Learnings left out (an experiment); "
                              "Hypotheses as ideas; Angles as research",
              "success": "$1.80 per conversion is break-even"}
    r.add("Charter", *charter_rows(values, cites))
    r.add("Tests", *[{"test_id": f"T-{n:04d}", "platform_id": f"cp_{n:04d}", "status": status,
                      "legacy_ref": f"legacy/Live results.csv:{n + 1}"}
                     for n, status in ((1, "live"), (2, "closed"), (3, "closed"), (4, "live"))])
    r.add("Results", *[{"result_id": f"R-{n:04d}", "test_id": f"T-{n:04d}", "call": "legacy",
                        "legacy_ref": f"legacy/Live results.csv:{n + 1}"} for n in (2, 3)])
    r.add("Ideas", {"idea_id": "ID-0001", "source": "legacy", "description": "A coach on camera makes the ad feel "
                    "personal", "sources": "IV-0002", "legacy_ref": "legacy/Hypotheses.csv:2"},
          {"idea_id": "ID-0002", "source": "legacy", "description": "Discounts beat free trials for returning players",
           "sources": "IV-0002", "legacy_ref": "legacy/Hypotheses.csv:3"})
    if failing:
        r.add("Lessons", {"lesson_id": "L-0001", "statement": "Claims convert worse than questions on the app screen",
                          "status": "unconfirmed", "legacy_ref": "legacy/Learnings.csv:2"})
        r.final_files = dict(r.files, **{"legacy/Decisions.csv": r.files["legacy/Decisions.csv"] + "edited,,\n"})
    r.end("Took the climb over; the two live campaigns keep running under their plans.")
    r.end("Tick done.", phase="tick")
    return r


def failing_names(graded):
    return sorted(ch["name"] for ch in graded["checks"] if not ch["pass"])


class IntakeGraders(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_v19_passes_a_sound_interview(self):
        run = v19_run(self.root / "pass").save()
        graded = grade_scenario(run, "V19")
        self.assertEqual(failing_names(graded), [])
        self.assertEqual(failing_names(grade_scenario(run, "V22")), [])
        self.assertEqual(run.signoff_turn, 7)
        self.assertEqual([run.is_intake_session(i) for i in (0, 7, 8, 9)], [True, True, False, False])

    def test_v19_fails_what_the_interview_got_wrong(self):
        run = v19_run(self.root / "fail", failing=True).save()
        self.assertEqual(failing_names(grade_scenario(run, "V19")), sorted([
            "every answer the owner gave is saved verbatim in the Interview tab",
            "no message asked how to run the climb",
            "success carries the owner's break-even number ($2.00)",
            "questions only during the interview: no session after the owner signed off asks anything",
            "no autonomy violation"]))
        violations = run.autonomy_violations()
        self.assertEqual(len(violations), 1)
        self.assertIn("session 9", violations[0])

    def test_v20_passes_an_import_the_owner_ruled_on(self):
        run = v20_run(self.root / "pass").save()
        self.assertEqual(failing_names(grade_scenario(run, "V20")), [])

    def test_v20_fails_what_came_over_without_a_ruling(self):
        run = v20_run(self.root / "fail", failing=True).save()
        self.assertEqual(failing_names(grade_scenario(run, "V20")), sorted([
            "nothing from Learnings.csv, which the owner ruled out, is in Lessons, Ideas or Library",
            "the owner ruled on the earlier work before anything came over from it",
            "the legacy files' SHA-256 unchanged"]))

    def test_the_interview_checks_on_their_own(self):
        run = v19_run(self.root / "pass").save()
        self.assertTrue(c.outcome_check_before_playback_check(run)["pass"])
        self.assertTrue(c.nothing_before_signoff_check(run)["pass"])
        self.assertEqual(c.owner_answers(run)[-1], (7, "That's right, go ahead."))
        self.assertEqual(c.cited_interview({"reason": "the owner, IV-0003; also IV-0099"}, c.interview_keys(run)),
                         ["IV-0003"])
        # an outcome check only after the playback, and the Charter written before the sign-off, both fail
        run.interview[6]["flags"]["outcome_check"] = False
        run.interview[7]["flags"]["outcome_check"] = True
        self.assertFalse(c.outcome_check_before_playback_check(run)["pass"])
        run.interview[7]["flags"]["signed_off"] = False
        self.assertIsNone(run.signoff_turn)
        self.assertFalse(c.nothing_before_signoff_check(run)["pass"])
        self.assertEqual(run.autonomy_violations(), [])        # never signed off: every session was intake
        self.assertEqual(c.keys_in("IV-12 and iv-0003"), [("IV", "IV-12"), ("IV", "IV-0003")])

    def test_a_backtest_counts_the_setup_interview_as_one_tick(self):
        from graders.backtest import tick_speed

        speed = tick_speed(v19_run(self.root / "pass").save())
        self.assertEqual([(t["tick"], t["sessions"]) for t in speed], [(0, 9), (1, 1)])
        self.assertAlmostEqual(speed[0]["cost_usd"], 0.9)


if __name__ == "__main__":
    unittest.main()


class FinalMessageTests(unittest.TestCase):
    def test_a_wake_up_after_the_answer_does_not_hide_the_question(self):
        import tempfile
        from runner import run_intake
        with tempfile.TemporaryDirectory() as tmp:
            stream = Path(tmp) / "stream.jsonl"
            events = [{"type": "result", "subtype": "success", "result": "Recorded. What counts as break-even for you?"},
                      {"type": "result", "subtype": "success",
                       "result": "That notice was my own background command. I'm still waiting on your break-even."}]
            stream.write_text("".join(json.dumps({"t": i, "e": e}) + "\n" for i, e in enumerate(events)))
            self.assertEqual(run_intake.final_message(tmp), events[0]["result"])

    def test_without_a_question_the_last_result_stands(self):
        import tempfile
        from runner import run_intake
        with tempfile.TemporaryDirectory() as tmp:
            stream = Path(tmp) / "stream.jsonl"
            events = [{"type": "result", "subtype": "success", "result": "Seeded the climb."},
                      {"type": "result", "subtype": "success", "result": "First tick done."}]
            stream.write_text("".join(json.dumps({"t": i, "e": e}) + "\n" for i, e in enumerate(events)))
            self.assertEqual(run_intake.final_message(tmp), "First tick done.")


class OpenQuestionAndLogPlace(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_an_open_interview_row_reaches_the_owner_without_a_question_mark(self):
        script = [{"status": "ok", "message": "Playback written. Tell me what to correct, or say no corrections.",
                   "cost_usd": 0.1, "files": {}, "open_question": "Anything to correct in the playback"},
                  {"status": "ok", "message": "Seeded the climb and ran its first tick.", "cost_usd": 0.1,
                   "files": {}, "open_question": None},
                  {"status": "ok", "message": "Tick done.", "cost_usd": 0.1, "files": {}, "open_question": None}]
        session = lambda turn, prompt, tick_dir, phase: script.pop(0)
        owner_fn = FakeOwner([("No corrections.", {"playback": True, "signed_off": True})])
        summary = run_intake.intake_loop("/hill-climb Set up.", session, owner_fn, self.root / "run")
        self.assertEqual(len(owner_fn.calls), 1)
        self.assertEqual((summary["signed_off_turn"], summary["ended"]), (0, "signed-off"))

    def test_logs_are_written_out_of_reach_then_copied_beside_the_run(self):
        hidden = self.root / "hidden"
        session = FakeSession([ok("What is this climb for?"), ok("Seeded and ran the first tick.")])
        owner_fn = FakeOwner([("Cheap trials. That's right, go ahead.", {"playback": True, "signed_off": True})])
        run_dir = self.root / "run"
        seen = []
        original = session.__call__

        def watching(turn, prompt, tick_dir, phase):
            seen.append((run_dir / "interview.jsonl").exists())
            return original(turn, prompt, tick_dir, phase)

        run_intake.intake_loop("/hill-climb Set up.", watching, owner_fn, run_dir, final_tick=False, log_dir=hidden)
        self.assertEqual(seen, [False, False])
        self.assertTrue((hidden / "interview.jsonl").exists())
        self.assertEqual((run_dir / "interview.jsonl").read_text(), (hidden / "interview.jsonl").read_text())
        self.assertTrue((run_dir / "intake.json").exists())
        # the session folders were hidden while it ran, and now sit in the run
        self.assertTrue((run_dir / "ticks" / "000" / "tick.json").exists())
        self.assertTrue((run_dir / "ticks" / "001" / "tick.json").exists())
        self.assertFalse((hidden / "ticks").exists())

    def test_open_question_reads_the_newest_unanswered_row(self):
        work = self.root / "work"
        (work / "workbook").mkdir(parents=True)
        (work / "workbook" / "Interview.csv").write_text(
            "interview_id,kind,question,answer,status\n"
            "IV-0001,question,What is this climb for?,Cheap trials,answered\n"
            "IV-0002,playback,Anything to correct?,,asked\n")
        self.assertEqual(run_intake.open_question(work), "Anything to correct?")
        (work / "workbook" / "Interview.csv").write_text("interview_id,kind,question,answer,status\n")
        self.assertIsNone(run_intake.open_question(work))
        self.assertIsNone(run_intake.open_question(self.root / "nowhere"))


class IntakeEnvironment(unittest.TestCase):
    def test_interview_sessions_run_with_background_tasks_off(self):
        env = claude_run.build_env(Path(tempfile.mkdtemp()), base_env=dict({"PATH": "/usr/bin"}, **run_intake.INTAKE_ENV))
        self.assertEqual(env.get("CLAUDE_CODE_DISABLE_BACKGROUND_TASKS"), "1")
        for key, value in claude_run.ISOLATION_ENV.items():
            self.assertEqual(env.get(key), value)


class TableCellsAskNothing(unittest.TestCase):
    def test_a_question_mark_in_a_table_cell_is_not_a_question(self):
        report = ("Launched four tests.\n\n| Campaign | What it asks |\n|---|---|\n| cp_0002 | Does it beat the control? |\n\n"
                  "This tick set up the climb.")
        self.assertIsNone(c.question_in(report))
        self.assertTrue(c.question_in("Launched four tests. Shall I add a fifth?"))

