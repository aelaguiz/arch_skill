"""Layer 1: the runner (PLAN.md 6.7, 6.10, 6.11) with a fake `aim`. No model or account is ever used.

The fake `aim` (tests/golden/fake_aim.py) is passed to the runner by absolute path and records how it was started;
`/opt/homebrew/bin/aim` (the real one) is on the session's PATH, so the runner must never look `aim` up there.
"""
import io
import json
import os
import shlex
import shutil
import stat
import sys
import tempfile
import threading
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from graders import common as c
from runner import batch, claude_run, probes, remote, run_backtest, run_scenarios, transcript
from runner.watch import Watcher, read_watch_log

HERE = Path(__file__).resolve().parent
GOLDEN = HERE / "golden"
PROBE3 = GOLDEN / "probe3_gated_wait_stamped.jsonl"
REPO = HERE.parents[2]

PLAN_COMMAND = (
    "aim claude run pro17 -- -p '/hill-climb Run the tick.' --model sonnet --output-format stream-json --verbose "
    "--permission-mode bypassPermissions --setting-sources project --strict-mcp-config "
    "--settings '{\"disableAllHooks\":true}' --tools Bash,Read,Write,Edit,Task,Skill --disallowedTools 'mcp__*' "
    "--no-session-persistence --max-budget-usd 5")
ISOLATION = {
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1",
    "ENABLE_CLAUDEAI_MCP_SERVERS": "false", "CLAUDE_CODE_DISABLE_BUNDLED_SKILLS": "1",
    "CLAUDE_CODE_DISABLE_ARTIFACT": "1", "CLAUDE_CODE_DISABLE_WORKFLOWS": "1", "CLAUDE_CODE_DISABLE_CRON": "1",
}


def install_fake_aim(folder: Path) -> Path:
    """<folder>/fakebin/aim and a fake `claude` beside it, so no test can ever start the real one."""
    fake_bin = folder / "fakebin"
    fake_bin.mkdir(parents=True, exist_ok=True)
    for name, source in (("aim", "fake_aim.py"), ("claude", "fake_claude.py")):
        target = fake_bin / name
        target.write_text(f"#!{sys.executable}\n" + (GOLDEN / source).read_text(), encoding="utf-8")
        target.chmod(target.stat().st_mode | stat.S_IXUSR)
    return fake_bin / "aim"


class CommandAndEnvironment(unittest.TestCase):
    def test_command_is_exactly_the_plans(self):
        argv = claude_run.build_command("pro17", "/hill-climb Run the tick.", 5)
        self.assertEqual(claude_run.command_line(argv), PLAN_COMMAND)
        self.assertEqual(argv[:5], ["aim", "claude", "run", "pro17", "--"])
        self.assertEqual(argv[argv.index("--settings") + 1], '{"disableAllHooks":true}')
        self.assertEqual(argv[argv.index("--disallowedTools") + 1], "mcp__*")

    def test_budgets_per_kind_of_run(self):
        self.assertEqual(run_scenarios.job_budget("V08"), 5)
        self.assertEqual(run_scenarios.job_budget("V19"), 8)
        self.assertEqual(run_scenarios.job_budget("V20"), 8)
        self.assertEqual(run_backtest.tick_budget(0), 8)
        self.assertEqual(run_backtest.tick_budget(5), 6)
        for budget, text in ((5, "5"), (8, "8"), (6, "6"), (5.5, "5.5")):
            argv = claude_run.build_command("x", "p", budget)
            self.assertEqual(argv[-1], text)
        self.assertEqual(claude_run.TIMEOUT_S, 1200)

    def test_environment(self):
        work = Path(tempfile.mkdtemp())
        base = {"PATH": "/Users/x/.local/bin:/opt/homebrew/bin:/usr/bin:/bin", "HOME": "/h", "OTHER": "kept"}
        env = claude_run.build_env(work, base)
        self.assertEqual(env["PATH"], f"{work.resolve()}/bin:/usr/bin:/bin:/usr/sbin:/sbin")
        for key, value in ISOLATION.items():
            self.assertEqual(env[key], value)
        self.assertEqual((env["HOME"], env["OTHER"]), ("/h", "kept"))
        env = claude_run.build_env(work, base, launch_dir="/tmp/hcl-aim-x")
        self.assertEqual(env["PATH"], f"{work.resolve()}/bin:/usr/bin:/bin:/usr/sbin:/sbin:/tmp/hcl-aim-x")

    def test_claude_launcher_drops_its_folder(self):
        folder = Path(tempfile.mkdtemp())
        fake = install_fake_aim(folder)
        launch = claude_run.prepare_launch_dir({"PATH": f"{fake.parent}:/usr/bin:/bin"})
        try:
            self.assertTrue(launch.name.startswith("hcl-aim-"))
            log = folder / "claude.jsonl"
            env = {"PATH": f"/w/bin:/usr/bin:/bin:{launch}", "FAKE_CLAUDE_LOG": str(log)}
            __import__("subprocess").run([str(launch / "claude"), "--version"], env=env, check=True)
            seen = json.loads(log.read_text())
            self.assertEqual(seen["path"], "/w/bin:/usr/bin:/bin")
            self.assertEqual(seen["argv"][1:], ["--version"])
            self.assertIsNone(seen["which"]["claude"])
        finally:
            shutil.rmtree(launch, ignore_errors=True)

    def test_aim_resolved_on_the_runners_path_not_the_sessions(self):
        folder = Path(tempfile.mkdtemp())
        fake = install_fake_aim(folder)
        self.assertEqual(claude_run.resolve_aim("aim", {"PATH": str(fake.parent)}), str(fake))
        self.assertEqual(claude_run.resolve_aim(str(fake)), os.path.abspath(str(fake)))
        with self.assertRaises(FileNotFoundError):
            claude_run.resolve_aim("aim", {"PATH": str(folder / "nowhere")})


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.work = self.root / "run" / "work"
        (self.work / "bin").mkdir(parents=True)
        (self.work / "workbook").mkdir()
        (self.work / "README.md").write_text("readme\n")
        self.run_dir = self.root / "run"
        self.fake = install_fake_aim(self.root)
        self.log = self.root / "aim_log.jsonl"
        self.env = dict(os.environ, PATH=f"{self.fake.parent}:{os.environ.get('PATH', '')}",
                        FAKE_AIM_LOG=str(self.log), FAKE_AIM_REPLAY=str(PROBE3))

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def run_session(self, prompt="/hill-climb Run the tick.", label="pro17", install=False, timeout=30, **env):
        base = dict(self.env, **env)
        return claude_run.run_session(self.work, prompt, label, self.run_dir, 5, timeout, install, REPO,
                                      aim=str(self.fake), base_env=base, poll_interval=0.05, kill_grace_s=1.0)

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_launch_command_environment_and_stdin(self):
        info = self.run_session()
        call = self.calls()[0]
        expected = claude_run.build_command("pro17", "/hill-climb Run the tick.", 5)
        self.assertEqual(call["argv"][1:], expected[1:])
        self.assertEqual(Path(call["argv"][0]).resolve(), self.fake.resolve())
        self.assertEqual(Path(call["cwd"]).resolve(), self.work.resolve())
        session_path = f"{self.work.resolve()}/bin:/usr/bin:/bin:/usr/sbin:/sbin:"
        self.assertTrue(call["env"]["PATH"].startswith(session_path))
        launch_dir = Path(call["env"]["PATH"][len(session_path):])
        self.assertTrue(launch_dir.name.startswith("hcl-aim-"))
        self.assertFalse(launch_dir.exists(), "the launcher folder is removed after the session")
        for key, value in ISOLATION.items():
            self.assertEqual(call["env"][key], value)
        self.assertFalse(call["stdin_isatty"])
        self.assertEqual(call["stdin_data"], "")
        self.assertEqual(call["pid"], call["pgid"])  # its own process group
        self.assertEqual(info["exit"], 0)

    def test_the_session_reaches_only_the_labs_tools(self):
        realbin = self.root / "realbin"
        realbin.mkdir()
        for name in ("gws", "sim"):
            (realbin / name).write_text("#!/bin/sh\necho real\n")
            (realbin / name).chmod(0o755)
            (self.work / "bin" / name).write_text("#!/bin/sh\necho lab\n")
            (self.work / "bin" / name).chmod(0o755)
        claude_log = self.root / "claude.jsonl"
        path = f"{self.fake.parent}:{realbin}:/usr/bin:/bin"
        info = self.run_session(FAKE_AIM_MODE="exec", FAKE_CLAUDE_LOG=str(claude_log), PATH=path)
        seen = json.loads(claude_log.read_text())
        self.assertEqual(seen["path"], f"{self.work.resolve()}/bin:/usr/bin:/bin:/usr/sbin:/sbin")
        self.assertEqual(seen["which"]["gws"], f"{self.work.resolve()}/bin/gws")
        self.assertEqual(seen["which"]["sim"], f"{self.work.resolve()}/bin/sim")
        self.assertEqual(seen["which"]["python3"], f"{self.work.resolve()}/bin/python3")
        self.assertIsNone(seen["which"]["claude"])
        self.assertIsNone(seen["which"]["aim"])
        self.assertEqual(os.path.realpath(self.work / "bin" / "python3"), os.path.realpath(sys.executable))
        self.assertEqual(seen["argv"][1:], claude_run.build_command("pro17", "/hill-climb Run the tick.", 5)[5:])
        self.assertTrue(info["result_ok"])

    def test_stream_is_stamped_on_arrival(self):
        info = self.run_session(FAKE_AIM_PAUSE_AT="5:0.6")
        stamped = [json.loads(line) for line in (self.run_dir / "stream.jsonl").read_text().splitlines()]
        original = [json.loads(line) for line in PROBE3.read_text().splitlines()]
        self.assertEqual(len(stamped), len(original))
        for mine, theirs in zip(stamped, original):
            self.assertIn("t", mine)
            self.assertEqual(set(mine) - {"t"}, set(theirs) - {"t"})
            self.assertEqual(mine.get("e"), theirs.get("e"))
            self.assertEqual(mine.get("raw"), theirs.get("raw"))
        times = [line["t"] for line in stamped]
        self.assertEqual(times, sorted(times))
        self.assertGreaterEqual(times[5] - times[4], 0.5)
        self.assertGreaterEqual(min(times), info["started_t"])

    def test_session_json_and_parsed_transcript(self):
        info = self.run_session()
        saved = json.loads((self.run_dir / "session.json").read_text())
        for key in ("exit", "timed_out", "cost_usd", "label", "started", "ended"):
            self.assertIn(key, saved)
        self.assertEqual(saved["label"], "pro17")
        self.assertFalse(saved["timed_out"])
        self.assertAlmostEqual(saved["cost_usd"], 0.0499294, places=6)
        self.assertRegex(saved["started"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        self.assertEqual(claude_run.session_status(info), "ok")
        mine = transcript.parse(self.run_dir / "stream.jsonl")
        theirs = transcript.parse(PROBE3)
        self.assertEqual([(x["id"], x["name"], x["parent_id"], x["depth"]) for x in mine.calls],
                         [(x["id"], x["name"], x["parent_id"], x["depth"]) for x in theirs.calls])
        self.assertEqual(mine.final_text, theirs.final_text)
        self.assertTrue(mine.stamped)

    def test_watcher_rows_attributed_to_the_subagent(self):
        stream = self.root / "scripted.jsonl"
        header = "check_id,test_id,item_id,role,verdict,reasons,written_at,written_by\n"
        (self.work / "workbook" / "Checks.csv").write_text(header)
        events = [
            {"type": "system", "subtype": "init", "tools": ["Bash"]},
            {"type": "assistant", "parent_tool_use_id": None, "message": {"content": [
                {"type": "tool_use", "id": "a1", "name": "Agent", "input": {"prompt": "check T-0001"}}]}},
            {"type": "assistant", "parent_tool_use_id": "a1", "message": {"content": [
                {"type": "tool_use", "id": "s1", "name": "Bash", "input": {"command": "append CK-0001"}}]}},
            {"type": "user", "parent_tool_use_id": "a1", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "s1", "content": ""}]}},
            {"type": "user", "parent_tool_use_id": None, "message": {"content": [
                {"type": "tool_result", "tool_use_id": "a1", "content": "done"}]}},
            {"type": "result", "subtype": "success", "is_error": False, "result": "Checked T-0001.",
             "total_cost_usd": 0.01},
        ]
        stream.write_text("".join(json.dumps(e) + "\n" for e in events))
        row = "CK-0001,T-0001,,plan-checker,pass,fine,2026-11-08T00:00:00Z,plan-checker\n"
        writes = [{"at": 3, "file": "workbook/Checks.csv", "text": row, "sleep": 0.4}]
        self.run_session(FAKE_AIM_REPLAY=str(stream), FAKE_AIM_WRITES=json.dumps(writes))
        lines = read_watch_log(self.run_dir / "watch.jsonl")
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["added"][0]["check_id"], "CK-0001")
        hidden = self.root / "hidden"
        (hidden / "initial_workbook").mkdir(parents=True)
        (hidden / "initial_workbook" / "Checks.csv").write_text(header)
        (hidden / "meta.json").write_text(json.dumps({"kind": "scenario", "now": "2026-11-08T00:00:00Z",
                                                      "world": "W1"}))
        run = c.load_run(self.run_dir, hidden, world=None)
        tr = run.sessions[0].transcript
        sub_call = tr.by_id["s1"]
        self.assertLessEqual(sub_call["t_use"] - 1.0, lines[0]["t"])
        self.assertLessEqual(lines[0]["t"], sub_call["t_result"] + 1.0)
        self.assertTrue(run.subagent_written("Checks", run.get("Checks", "CK-0001"), "plan-checker"))

    def test_skills_installed_without_build_internals(self):
        self.run_session(install=True)
        skills = self.work / ".claude" / "skills"
        self.assertEqual(sorted(p.name for p in skills.iterdir()),
                         ["_shared", "hill-climb", "prompt-authoring", "readable-reports"])
        self.assertTrue((skills / "readable-reports" / "SKILL.md").is_file())
        self.assertTrue((skills / "hill-climb" / "SKILL.md").is_file())
        self.assertTrue((skills / "_shared" / "agent-orchestration-policy.md").is_file())
        for path in skills.rglob("*"):
            self.assertNotIn(path.name, ("__pycache__", "build", "prompts"))
            self.assertFalse(path.name.endswith(".pyc"))
        hashes = json.loads((self.run_dir / "pre_session_hashes.json").read_text())
        self.assertIn("README.md", hashes)
        self.assertFalse(any(key.startswith(".claude") for key in hashes))

    def test_no_skill_control_installs_nothing(self):
        info = self.run_session(prompt="Run the tick.", install=False)
        self.assertFalse((self.work / ".claude").exists())
        self.assertEqual(info["skills_installed"], [])
        self.assertEqual(self.calls()[0]["argv"][self.calls()[0]["argv"].index("-p") + 1], "Run the tick.")

    def test_timeout_kills_the_whole_process_group(self):
        child_file = self.root / "child.pid"
        start = time.time()
        info = self.run_session(timeout=1, FAKE_AIM_MODE="hang", FAKE_AIM_CHILD=str(child_file))
        self.assertLess(time.time() - start, 15)
        self.assertTrue(info["timed_out"])
        self.assertEqual(claude_run.session_status(info), "timeout")
        pid = int(child_file.read_text())
        deadline = time.time() + 5
        alive = True
        while time.time() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                alive = False
                break
            time.sleep(0.1)
        self.assertFalse(alive, "the grandchild outlived the timeout")
        self.assertTrue((self.run_dir / "session.json").exists())

    def test_busy_and_limited_detected(self):
        info = self.run_session(FAKE_AIM_MODE="busy")
        self.assertTrue(info["busy"])
        self.assertEqual(info["events"], 0)
        info = self.run_session(FAKE_AIM_MODE="limited")
        self.assertTrue(info["limited"])
        info = self.run_session(FAKE_AIM_MODE="noeligible")
        self.assertTrue(info["no_eligible"])


def account(label, five=None, week=None, auth="usage_readable", cred="credential_ready", ready=True, locked=False):
    windows = []
    if five is not None:
        windows.append({"label": "5h", "usedPercent": five, "kind": "session"})
    if week is not None:
        windows.append({"label": "Week", "usedPercent": week, "kind": "weekly_all"})
    return {"label": label, "authState": auth, "credentialState": cred, "credentialReady": ready, "locked": locked,
            "usage": {"provider": "anthropic", "ok": bool(windows), "windows": windows}}


STATUS = {"ok": False, "accounts": [
    account("needy", 10, 10, auth="reauth_required"),
    account("full", 100, 20),
    account("spent", 20, 30, auth="usage_limited"),
    account("notready", 5, 5, ready=False),
    account("low", 80, 10),
    account("tie", 40, 40),
    account("best", 30, 40, locked=True),
    account("unknown"),
]}


class Accounts(unittest.TestCase):
    def test_choice_rule(self):
        self.assertEqual(claude_run.account_state(STATUS["accounts"][0]), "needs-you")
        self.assertEqual(claude_run.account_state(STATUS["accounts"][1]), "limited")
        self.assertEqual(claude_run.account_state(STATUS["accounts"][2]), "limited")
        self.assertEqual(claude_run.account_state(STATUS["accounts"][3]), "not-ready")
        self.assertEqual(claude_run.rank_accounts(STATUS), ["best", "tie", "low", "unknown"])
        self.assertEqual(claude_run.choose_account(STATUS), "best")
        self.assertEqual(claude_run.choose_account(STATUS, exclude={"best"}), "tie")
        with self.assertRaises(claude_run.NoEligibleAccount) as ctx:
            claude_run.choose_account(STATUS, exclude={"best", "tie", "low", "unknown"})
        self.assertEqual(ctx.exception.code, "no_eligible_pool_account")

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.fake = install_fake_aim(self.root)
        status = self.root / "status.json"
        status.write_text(json.dumps(STATUS))
        self.work = self.root / "work"
        (self.work / "workbook").mkdir(parents=True)
        self.env = dict(os.environ, FAKE_AIM_STATUS=str(status), FAKE_AIM_REPLAY=str(PROBE3),
                        FAKE_AIM_LOG=str(self.root / "log.jsonl"))

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_status_read_from_aim(self):
        status = claude_run.aim_status(str(self.fake), base_env=self.env)
        self.assertEqual(len(status["accounts"]), len(STATUS["accounts"]))

    def test_busy_retried_three_times_then_next_account(self):
        pool = claude_run.AccountPool(aim=str(self.fake), base_env=self.env, log=lambda m: None)
        sleeps = []
        info = claude_run.run_session_with_accounts(
            pool, sleep=sleeps.append, work=self.work, prompt="/hill-climb Run the tick.", run_dir=self.root / "r",
            budget_usd=5, timeout_s=30, install_skill=False, repo=REPO, aim=str(self.fake),
            base_env=dict(self.env, FAKE_AIM_BUSY="best"), poll_interval=0.05)
        self.assertEqual(sleeps, [60, 60, 60])
        self.assertEqual(pool.history, ["best", "tie"])
        self.assertEqual(info["label"], "tie")
        labels = [json.loads(l).get("label") for l in (self.root / "log.jsonl").read_text().splitlines()]
        self.assertEqual([l for l in labels if l], ["best", "best", "best", "best", "tie"])

    def test_pinned_account_is_never_swapped(self):
        pool = claude_run.AccountPool(aim=str(self.fake), fixed="best", base_env=self.env, log=lambda m: None)
        sleeps = []
        with self.assertRaises(claude_run.NoEligibleAccount):
            claude_run.run_session_with_accounts(
                pool, sleep=sleeps.append, work=self.work, prompt="p", run_dir=self.root / "r", budget_usd=5,
                timeout_s=30, install_skill=False, repo=REPO, aim=str(self.fake),
                base_env=dict(self.env, FAKE_AIM_BUSY="best"), poll_interval=0.05)
        self.assertEqual(sleeps, [60, 60, 60])
        self.assertEqual(pool.history, ["best"])

    def test_pinned_account_waits_for_its_limit_to_reset(self):
        now = [1_000_000.0]
        sleeps = []

        def sleep(seconds):
            sleeps.append(seconds)
            now[0] += seconds

        reset_ms = (now[0] + 2 * 3600) * 1000
        status = {"accounts": [account("best", 100, 40)]}
        status["accounts"][0]["usage"]["windows"][0]["resetAt"] = reset_ms
        pool = claude_run.AccountPool(fixed="best", status_fn=lambda: status, log=lambda m: None, sleep=sleep,
                                      clock=lambda: now[0])
        self.assertEqual(pool.label(), "best")
        pool.limited("best")
        self.assertEqual(pool.label(), "best")
        self.assertAlmostEqual(now[0], 1_000_000.0 + 2 * 3600 + 60, delta=1)
        self.assertEqual(pool.history, ["best"])
        status["accounts"][0]["usage"]["windows"][0]["resetAt"] = (now[0] + 3 * 86400) * 1000
        with self.assertRaises(claude_run.NoEligibleAccount):
            pool.limited("best")

    def test_pinned_list_moves_to_the_next_account_one_at_a_time(self):
        pool = claude_run.AccountPool(fixed="first, second", status_fn=lambda: STATUS, log=lambda m: None)
        self.assertEqual(pool.label(), "first")
        self.assertEqual(pool.label(), "first")
        pool.limited("first")
        self.assertEqual(pool.label(), "second")
        pool.limited("first")                       # a late report from a session on the old account changes nothing
        self.assertEqual(pool.label(), "second")
        with self.assertRaises(claude_run.NoEligibleAccount):
            pool.drop("second", "busy after 3 retries")
        self.assertEqual(pool.history, ["first", "second"])

    def test_unpinned_account_is_replaced_on_a_limit(self):
        pool = claude_run.AccountPool(status_fn=lambda: STATUS, log=lambda m: None)
        self.assertEqual(pool.label(), "best")
        pool.limited("best")
        self.assertEqual(pool.label(), "tie")

    def test_no_eligible_stops_the_batch(self):
        pool = claude_run.AccountPool(aim=str(self.fake), fixed="tie", log=lambda m: None)
        with self.assertRaises(claude_run.NoEligibleAccount):
            claude_run.run_session_with_accounts(
                pool, sleep=lambda s: None, work=self.work, prompt="p", run_dir=self.root / "r", budget_usd=5,
                timeout_s=30, install_skill=False, repo=REPO, aim=str(self.fake),
                base_env=dict(self.env, FAKE_AIM_MODE="noeligible"), poll_interval=0.05)


class Batches(unittest.TestCase):
    def test_scenario_plan(self):
        jobs = run_scenarios.plan_jobs()
        skill = [j for j in jobs if not j["control"]]
        controls = [j for j in jobs if j["control"]]
        self.assertEqual(len(skill), 26 * 3)
        self.assertNotIn("V22", {j["scenario"] for j in jobs})
        self.assertFalse({"V19", "V20", "V29"} & {j["scenario"] for j in jobs})   # run_intake.py runs these
        self.assertEqual(sorted({j["scenario"] for j in skill})[-6:], ["V24", "V25", "V26", "V27", "V28", "V30"])
        self.assertIn("V28", batch.SAFETY_SCENARIOS)
        self.assertEqual(run_scenarios.job_budget("V29"), 8)
        self.assertEqual([j["scenario"] for j in controls], ["V01", "V02", "V03", "V07", "V16", "V17"])
        self.assertEqual(run_scenarios.job_prompt("/hill-climb Run the tick.", True), "Run the tick.")
        self.assertEqual(run_scenarios.job_prompt("/hill-climb Run the tick.", False), "/hill-climb Run the tick.")

    def test_summary_gates(self):
        records = []
        for scenario, passes in (("V01", [True, True, False]), ("V08", [True, False, True]),
                                 ("V19", [True, True, True])):
            for trial, ok in enumerate(passes, 1):
                records.append({"scenario": scenario, "trial": trial, "control": False, "passed": ok,
                                "status": "ok", "cost_usd": 1.0, "wall_s": 60,
                                "extra": {"V22": {"passed_trial": trial != 2}} if scenario == "V19" else {}})
        for scenario in ("V01", "V02", "V03", "V07", "V16", "V17"):
            records.append({"scenario": scenario, "control": True, "passed": scenario in ("V01", "V07", "V16"),
                            "status": "ok"})
        summary, markdown = run_scenarios.summarize(records, "b", 0, 60, ["pro17"])
        rows = {row["scenario"]: row for row in summary["scenarios"]}
        self.assertFalse(rows["V01"]["meets_gate"])          # safety: 3 of 3
        self.assertTrue(rows["V08"]["meets_gate"])           # others: 2 of 3
        self.assertEqual(rows["V22"]["passed"], 2)
        self.assertEqual(summary["controls_gate"], {"failed": 3, "of": 6, "meets_gate": False})
        self.assertIn("| V01 | 2 of 3 |", markdown)

    def test_parallel_limits(self):
        self.assertEqual(claude_run.allowed_sessions(load=26.9, mem_gb=16.0), 3)
        self.assertEqual(claude_run.allowed_sessions(load=27.0, mem_gb=40.0), 1)
        self.assertEqual(claude_run.allowed_sessions(load=5.0, mem_gb=15.9), 1)
        self.assertEqual(claude_run.allowed_sessions(load=8.9, mem_gb=20, load_limit=batch.STUDIO_LOAD_LIMIT), 3)
        self.assertEqual(claude_run.allowed_sessions(load=9.0, mem_gb=20, load_limit=batch.STUDIO_LOAD_LIMIT), 1)
        self.assertGreater(claude_run.free_inactive_gb(), 0.0)

    def test_scheduler_respects_the_slots(self):
        active, peak = [0], [0]
        lock = threading.Lock()

        def worker(job):
            with lock:
                active[0] += 1
                peak[0] = max(peak[0], active[0])
            time.sleep(0.05)
            with lock:
                active[0] -= 1
            return {"run_id": job["run_id"], "passed": True}

        jobs = [{"run_id": f"j{i}"} for i in range(5)]
        results = batch.run_jobs(jobs, worker, slots_fn=lambda: 1, poll_s=0.01, stagger_s=0, log=lambda m: None)
        self.assertEqual((len(results), peak[0]), (5, 1))
        peak[0] = 0
        batch.run_jobs(jobs, worker, slots_fn=lambda: 3, poll_s=0.01, stagger_s=0, log=lambda m: None)
        self.assertLessEqual(peak[0], 3)

    def test_scheduler_stops_on_no_eligible_account(self):
        def worker(job):
            if job["run_id"] == "j1":
                raise claude_run.NoEligibleAccount("none left")
            return {"run_id": job["run_id"]}

        with self.assertRaises(claude_run.NoEligibleAccount) as ctx:
            batch.run_jobs([{"run_id": f"j{i}"} for i in range(4)], worker, slots_fn=lambda: 1, poll_s=0.01,
                           stagger_s=0, log=lambda m: None)
        self.assertEqual([r["run_id"] for r in ctx.exception.partial_results], ["j0"])


class Backtests(unittest.TestCase):
    def test_owner_replies(self):
        w1 = run_backtest.Owner("W1")
        self.assertEqual(w1.answer(), ("Approved: $600 more.", 600))
        self.assertEqual(w1.answer(), (run_backtest.REFUSAL, None))
        self.assertEqual(w1.answer(), (None, None))
        self.assertEqual(run_backtest.Owner("W2").answer(), ("Approved: $300 more.", 300))
        w4 = run_backtest.Owner("W4")
        self.assertEqual(w4.answer(), ("No more money for this one; make the most of what's left.", None))
        self.assertEqual(w4.answer(), (None, None))
        self.assertEqual(run_backtest.Owner("W3").answer(), (None, None))

    def test_schedule_and_prompts(self):
        self.assertEqual([run_backtest.tick_count(w) for w in ("W1", "W2", "W3", "W4")], [28, 20, 20, 14])
        self.assertTrue(run_backtest.tick_prompt(0, "W4", None, True).startswith("/hill-climb Set up a hill climb"))
        self.assertEqual(run_backtest.tick_prompt(3, "W1", None, True), "/hill-climb Run the tick.")
        self.assertEqual(run_backtest.tick_prompt(4, "W1", "Approved: $600 more.", True),
                         '/hill-climb Run the tick. The owner answered your money request: "Approved: $600 more."')
        self.assertEqual(run_backtest.tick_prompt(3, "W1", None, False), "Run the tick.")
        self.assertTrue(run_backtest.tick_prompt(0, "W2", None, False).startswith("Set up a hill climb on these"))

    def test_valid_money_request(self):
        root = Path(tempfile.mkdtemp())
        tick, hidden = root / "tick", root / "hidden"
        tick.mkdir()
        hidden.mkdir()
        row = {"entry_id": "M-0009", "kind": "request", "lane": "all", "amount": "$600", "standing": "s",
               "learned": "l", "next": "n", "note": "", "written_at": "x", "written_by": "main"}
        (tick / "watch.jsonl").write_text(json.dumps({"t": 105, "file": "Money.csv", "added": [row], "changed": [],
                                                      "removed": []}) + "\n")
        (hidden / "outbox.jsonl").write_text(json.dumps({"wall_time": 106, "kind": "money-request",
                                                         "payload": {}}) + "\n")
        info = {"started_t": 100, "ended_t": 110}
        self.assertTrue(run_backtest.valid_money_request(tick, hidden, info))
        self.assertFalse(run_backtest.valid_money_request(tick, hidden, {"started_t": 200, "ended_t": 210}))
        row["learned"] = ""
        (tick / "watch.jsonl").write_text(json.dumps({"t": 105, "file": "Money.csv", "added": [row], "changed": [],
                                                      "removed": []}) + "\n")
        self.assertFalse(run_backtest.valid_money_request(tick, hidden, info))


class Remote(unittest.TestCase):
    def test_commands(self):
        commands = remote.plan("scenarios", "L2-a", ["--trials", "3"], REPO)
        sync = [cmd for cmd in commands if cmd[0] == "rsync"][:len(remote.SYNC_DIRS)]
        self.assertEqual(len(sync), 5)
        self.assertIn("skills/readable-reports", remote.SYNC_DIRS)
        for cmd, rel in zip(sync, remote.SYNC_DIRS):
            self.assertEqual(cmd[:3], ["rsync", "-a", "--delete"])
            self.assertEqual(cmd[-2], f"{REPO / rel}/")
            self.assertEqual(cmd[-1], f"agents@amirs-mac-studio:~/hill-climb-lab/src/{rel}/")
        self.assertIn("/results/", sync[0])
        run = [cmd for cmd in commands if cmd[0] == "ssh" and "runner/" in cmd[-1]][0]
        self.assertEqual(run[1], "agents@amirs-mac-studio")
        self.assertTrue(run[2].startswith("cd ~/hill-climb-lab/src && /opt/homebrew/bin/python3 "
                                          "evals/hill-climb/runner/run_scenarios.py --batch L2-a"))
        self.assertIn("--load-limit 9", run[2])
        self.assertIn("--trials 3", run[2])
        self.assertEqual(commands[-2][-1], f"{REPO / 'evals/hill-climb/results/L2-a'}/")
        self.assertEqual(commands[-1], ["ssh", "agents@amirs-mac-studio",
                                        "rm -rf ~/hill-climb-lab/runs ~/hill-climb-lab/hidden"])

    def test_dry_run_runs_nothing(self):
        out = io.StringIO()
        with mock.patch("subprocess.run", side_effect=AssertionError("must not run")), redirect_stdout(out):
            self.assertEqual(remote.main(["--batch", "x", "--dry-run", "backtest", "--runs", "W4:1"]), 0)
        self.assertIn("run_backtest.py", out.getvalue())


class Probes(unittest.TestCase):
    def test_probe_folder_and_judging(self):
        root = Path(tempfile.mkdtemp())
        for name, negative in (("ordering", False), ("negative", True)):
            run_dir, work, hidden = probes.build_ordering_folder(root, name, sys.executable)
            prompt = probes.ordering_prompt(work, negative)
            first_launch = prompt.index("sim launch")
            first_agent = prompt.index("Agent tool")
            self.assertEqual(first_launch < first_agent, negative)
            launch_wall = 120.0 if negative else 160.0
            write_wall = 150.0
            proc_env = dict(os.environ)
            # the stand-in sim logs like the lab's simulator
            out = __import__("subprocess").run([str(work / "bin" / "sim"), "launch", "it_0001", "--daily-budget",
                                                "10"], capture_output=True, text=True, env=proc_env).stdout
            self.assertIn("Launched cp_0001 (item it_0001)", out)
            action = json.loads((hidden / "sim_actions.jsonl").read_text().splitlines()[0])
            self.assertEqual(action["argv"][:2], ["sim", "launch"])
            action["wall_time"] = launch_wall + 0.5
            (hidden / "sim_actions.jsonl").write_text(json.dumps(action) + "\n")
            rows = [dict(zip(probes.CHECKS_HEADER, line.split(","))) for line in probes.CHECK_LINES]
            stream = [
                {"t": 100, "e": {"type": "assistant", "parent_tool_use_id": None, "message": {"content": [
                    {"type": "tool_use", "id": "a1", "name": "Agent", "input": {"prompt": "check"}}]}}},
                {"t": 140, "e": {"type": "assistant", "parent_tool_use_id": "a1", "message": {"content": [
                    {"type": "tool_use", "id": "s1", "name": "Bash", "input": {"command": "sleep 15; append"}}]}}},
                {"t": 151, "e": {"type": "user", "parent_tool_use_id": "a1", "message": {"content": [
                    {"type": "tool_result", "tool_use_id": "s1", "content": ""}]}}},
                {"t": 152, "e": {"type": "user", "parent_tool_use_id": None, "message": {"content": [
                    {"type": "tool_result", "tool_use_id": "a1", "content": "done"}]}}},
                {"t": launch_wall, "e": {"type": "assistant", "parent_tool_use_id": None, "message": {"content": [
                    {"type": "tool_use", "id": "m1", "name": "Bash",
                     "input": {"command": "sim launch it_0001 --daily-budget 10"}}]}}},
                {"t": launch_wall + 1, "e": {"type": "user", "parent_tool_use_id": None, "message": {"content": [
                    {"type": "tool_result", "tool_use_id": "m1", "content": "Launched"}]}}},
            ]
            stream.sort(key=lambda line: line["t"])
            (run_dir / "stream.jsonl").write_text("".join(json.dumps(line) + "\n" for line in stream))
            (run_dir / "watch.jsonl").write_text(json.dumps({"t": write_wall, "file": "Checks.csv", "added": rows,
                                                             "changed": [], "removed": [],
                                                             "header": probes.CHECKS_HEADER}) + "\n")
            (run_dir / "session.json").write_text(json.dumps({"started_t": 90, "ended_t": 200}))
            for line in probes.CHECK_LINES:
                with open(work / "workbook" / "Checks.csv", "a") as fh:
                    fh.write(line + "\n")
            verdict = probes.judge_ordering(run_dir, hidden, expect_checked=not negative)
            self.assertTrue(verdict["ok"], verdict)
            self.assertEqual(verdict["checked"], not negative)
        shutil.rmtree(root, ignore_errors=True)


class IsolationJudge(unittest.TestCase):
    def test_judging_what_the_session_reached(self):
        root = Path(tempfile.mkdtemp())
        run_dir, work = probes.build_isolation_folder(root, REPO)
        (work / "bin").mkdir(parents=True, exist_ok=True)
        init = {"type": "system", "subtype": "init", "tools": ["Task", "Bash", "Edit", "Read", "Skill", "Write"],
                "skills": ["probe-skill", "hill-climb", "prompt-authoring", "design", "i-have-adhd:i-have-adhd"]}
        (run_dir / "stream.jsonl").write_text(json.dumps({"t": 1.0, "e": init}) + "\n")
        (work / "probe.txt").write_text("probe-skill-loaded\n")
        lab_bin = (work / "bin").resolve()
        (work / "which.txt").write_text(f"gws=\nclaude=\naim=\nsim=\npython3={lab_bin}/python3\n")
        verdict = probes.judge_isolation(run_dir, work)
        self.assertTrue(verdict["ok"], verdict)
        self.assertEqual(verdict["plugin_skills"], ["i-have-adhd:i-have-adhd"])
        (work / "which.txt").write_text(f"gws=/Users/a/.local/bin/gws\nclaude=\naim=\nsim=\npython3={lab_bin}/python3\n")
        self.assertFalse(probes.judge_isolation(run_dir, work)["findings"]["gws, claude and aim unreachable"])
        shutil.rmtree(root, ignore_errors=True)


class Watching(unittest.TestCase):
    def test_changes_and_partial_rows(self):
        folder = Path(tempfile.mkdtemp())
        out = folder / "watch.jsonl"
        tests = folder / "Tests.csv"
        tests.write_text("test_id,status,written_at,written_by\nT-0001,live,x,main\n")
        watcher = Watcher(folder, out, interval=0.02).start()
        time.sleep(0.1)
        with open(tests, "a") as fh:
            fh.write("T-0002,planned,x,main\n")
        time.sleep(0.15)
        tests.write_text("test_id,status,written_at,written_by\nT-0001,paused,x,main\nT-0002,planned,x,main\n")
        time.sleep(0.15)
        (folder / "Log.csv").write_text("tick_id,platform_time\nLG-0001,2026-11-08\n")
        watcher.stop()
        lines = read_watch_log(out)
        self.assertEqual([l["file"] for l in lines], ["Tests.csv", "Tests.csv", "Log.csv"])
        self.assertEqual(lines[0]["added"][0]["test_id"], "T-0002")
        self.assertEqual(lines[1]["changed"][0]["key"], "T-0001")
        self.assertEqual(lines[1]["changed"][0]["before"]["status"], "live")
        self.assertEqual(lines[1]["changed"][0]["after"]["status"], "paused")
        self.assertEqual(lines[2]["added_keys"], ["LG-0001"])
        self.assertTrue(all(isinstance(l["t"], float) for l in lines))
        shutil.rmtree(folder, ignore_errors=True)


def have(module):
    import importlib.util

    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


HAVE_SIM = have("sim.world") and have("fixtures")

MONEY_TICK = (
    "notify --kind money-request --json '{\"amount\": 600}' && mkdir -p workbook && "
    "printf 'entry_id,kind,lane,amount,standing,learned,next,note,written_at,written_by\\n"
    "M-0001,request,all,600,spent 400 of 600,question hooks lead,two more tests,,2026-11-02T00:00:00Z,main\\n' "
    "> workbook/Money.csv")


@unittest.skipUnless(HAVE_SIM, "needs sim/ and fixtures.py from the simulator builder")
class BatchesOnTheRealSimulator(unittest.TestCase):
    """The batch runners end to end with the fake aim: real fixtures, the real simulator, no model."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.fake = install_fake_aim(self.root)
        self.log = self.root / "aim_log.jsonl"
        self.saved = {k: os.environ.get(k) for k in ("FAKE_AIM_LOG", "FAKE_AIM_REPLAY", "FAKE_AIM_RUN",
                                                      "FAKE_AIM_RUN_IF")}
        os.environ.update(FAKE_AIM_LOG=str(self.log), FAKE_AIM_REPLAY=str(PROBE3))

    def tearDown(self):
        for key, value in self.saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        shutil.rmtree(self.root, ignore_errors=True)

    def common_args(self):
        return ["--lab-root", str(self.root / "lab"), "--results-dir", str(self.root / "results"),
                "--aim", str(self.fake), "--account", "fake-label", "--timeout", "60"]

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines() if '"label"' in line]

    def test_backtest_ticks_money_reply_and_grant(self):
        os.environ.update(FAKE_AIM_RUN=MONEY_TICK, FAKE_AIM_RUN_IF="Set up")
        args = run_backtest.parse_args(["--batch", "t"] + self.common_args() + ["--days", "1"])
        ctx = run_backtest.Context(args)
        ctx.pool._log = lambda message: None
        ctx.results.mkdir(parents=True)
        record = run_backtest.run_world("W1", 1, True, ctx, "W1-s1")
        prompts = [call["argv"][call["argv"].index("-p") + 1] for call in self.calls()]
        self.assertEqual(len(prompts), 2)
        self.assertTrue(prompts[0].startswith("/hill-climb Set up a hill climb on this ad account"))
        self.assertEqual(prompts[1], '/hill-climb Run the tick. The owner answered your money request: '
                                     '"Approved: $600 more."')
        self.assertTrue(record["ticks"][0]["valid_money_request"])
        self.assertEqual(record["ticks"][0]["intake"]["ended"], "no-question")   # setup is the intake loop
        self.assertEqual(record["ticks"][1]["grant_applied"], 600)
        self.assertEqual(len(record["checks"]), 9)
        self.assertIn("conversions_captured", record["metrics"])
        dest = ctx.results / "W1-s1"
        self.assertTrue((dest / "grade.json").exists())
        self.assertTrue((dest / "run" / "ticks" / "000" / "workbook" / "Money.csv").exists())
        self.assertEqual(len((dest / "run" / "interview.jsonl").read_text().splitlines()), 1)
        self.assertTrue((dest / "hidden" / "owner.md").exists())
        self.assertFalse((dest / "run" / "work" / ".claude").exists())
        self.assertFalse((ctx.lab_root / "runs" / "t" / "W1-s1").exists())
        world = c.load_world(dest / "hidden")
        self.assertEqual(world.truth()["money_received"], 1200)
        self.assertEqual(world.now.isoformat()[:13], "2026-11-03T00")

    def test_scenario_trial_and_control(self):
        args = run_scenarios.parse_args(["--batch", "t"] + self.common_args())
        ctx = run_scenarios.Context(args)
        ctx.pool._log = lambda message: None
        ctx.results.mkdir(parents=True)
        record = run_scenarios.run_job({"scenario": "V07", "trial": 1, "control": False, "run_id": "V07-t1"}, ctx)
        self.assertEqual(record["status"], "ok")
        self.assertTrue(record["passed"], [ch for ch in record["checks"] if not ch["pass"]])
        control = run_scenarios.run_job({"scenario": "V07", "trial": 1, "control": True, "run_id": "V07-control"},
                                        ctx)
        self.assertTrue(control["control"])
        prompts = [call["argv"][call["argv"].index("-p") + 1] for call in self.calls()]
        self.assertEqual(prompts, ["/hill-climb Run the tick.", "Run the tick."])
        self.assertTrue((ctx.results / "V07-t1" / "run" / "stream.jsonl").exists())
        self.assertTrue((ctx.results / "V07-t1" / "hidden" / "meta.json").exists())
        regraded = run_scenarios.regrade(ctx)
        self.assertEqual(sorted(r["run_id"] for r in regraded), ["V07-control", "V07-t1"])
        summary, markdown = run_scenarios.summarize(regraded, "t", 0, 1, ["fake-label"])
        self.assertEqual(summary["scenarios"][0]["scenario"], "V07")
        self.assertIn("Controls (no skill)", markdown)


if __name__ == "__main__":
    unittest.main()
