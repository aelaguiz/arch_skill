"""The simulator (PLAN.md 6.2): determinism, faults, truth, command outputs, the rubric, `apply`, and what the agents
never see."""
import contextlib
import io
import json
import re
import shutil
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from sim import cli
from sim.world import World, iso, load_config, parse_time, text_quality

SPECIFIC_TEXT = "Practice the river decision with pocket jacks in 2 minutes a day."
NEUTRAL_TEXT = "Learn what strong players think about at the table"
NOW_LINE = re.compile(r"^Now: \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ \(day \d+\)\.$")
W1_ATTRS = {"hook": "story", "visual": "coach-face", "offer": "free-trial"}


def run(hidden, *args, tool="sim"):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = cli.main([tool, "--hidden", str(hidden), *args])
    return code, out.getvalue()


def admin(hidden, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(["simadmin", "--hidden", str(hidden), *args])
    return code, out.getvalue() + err.getvalue()


def lines_of(hidden):
    path = Path(hidden) / "sim_actions.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class LabCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="hc-sim-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def init(self, name, world="W1", seed=1, *extra):
        hidden = self.tmp / name
        code, out = admin(hidden, "init", "--world", world, "--seed", str(seed), *extra)
        self.assertEqual(code, 0, out)
        return hidden


class Rubric(unittest.TestCase):
    def test_listed_examples(self):
        cfg = load_config("W1")
        cases = {
            "Level up your game with the best poker app!": "generic",
            "Practice the river decision with pocket jacks in 2 minutes a day.": "specific",
            NEUTRAL_TEXT: "neutral",
            "Fold more often, friend.": "generic",                      # fewer than 6 words
            "Ultimate river practice for home game players": "generic",  # generic is checked first
            "THE RIVER IS WHERE MOST PLAYERS LOSE": "specific",          # lowercased first
            "Our app helps you think clearly in 30 seconds": "specific",  # a digit
            "Our app helps you think clearly every single night": "neutral",
            "This settles every argument about the rules": "specific",   # substring: "set"
        }
        for text, want in cases.items():
            self.assertEqual(text_quality(text, cfg), want, text)


class Determinism(LabCase):
    def _script(self, hidden, noisy):
        run(hidden, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
        if noisy:
            run(hidden, "report")
            run(hidden, "library", "--owner", "Rival B")
        run(hidden, "build", "--attrs", json.dumps({"hook": "question", "visual": "app-screen", "offer": "none"}),
            "--text", NEUTRAL_TEXT)
        run(hidden, "launch", "it_0001", "--daily-budget", "20")
        if noisy:
            run(hidden, "status")
            run(hidden, "catalog")
        run(hidden, "launch", "it_0002", "--daily-budget", "35")
        if noisy:
            admin(hidden, "advance", "--hours", "7")
            run(hidden, "attribution", "--by", "day")
            admin(hidden, "advance", "--hours", "23")
        else:
            admin(hidden, "advance", "--hours", "30")

    def test_same_seed_same_reports_in_any_order(self):
        a, b = self.init("a", "W1", 5), self.init("b", "W1", 5)
        self._script(a, noisy=False)
        self._script(b, noisy=True)
        wa, wb = World.load(a), World.load(b)
        for cid in ("cp_0001", "cp_0002"):
            self.assertEqual(wa.hourly(cid), wb.hourly(cid))
        self.assertEqual(run(a, "report", "--by", "day", "--audience")[1], run(b, "report", "--by", "day", "--audience")[1])
        self.assertEqual(run(a, "attribution")[1], run(b, "attribution")[1])

    def test_a_campaign_does_not_depend_on_others_or_on_how_the_clock_moved(self):
        a, c = self.init("a", "W1", 5, "--overrides", '{"rejection_p": 0}'), self.init("c", "W1", 5, "--overrides",
                                                                                         '{"rejection_p": 0}')
        for hidden in (a, c):
            run(hidden, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
            run(hidden, "launch", "it_0001", "--daily-budget", "20")
        run(a, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
        run(a, "launch", "it_0002", "--daily-budget", "40")
        admin(a, "advance", "--hours", "48")
        for _ in range(4):
            admin(c, "advance", "--hours", "12")
        self.assertEqual(World.load(a).hourly("cp_0001"), World.load(c).hourly("cp_0001"))


class Faults(LabCase):
    def test_tracking_fault_thins_platform_counts_in_its_window_only(self):
        hidden = self.init("t", "W1", 2, "--overrides", '{"rejection_p": 0}')
        run(hidden, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
        self.assertEqual(run(hidden, "launch", "it_0001", "--daily-budget", "30")[0], 0)
        admin(hidden, "advance", "--hours", str(24 * 12))
        world = World.load(hidden)
        start, end = parse_time("2026-11-07T00:00:00Z"), parse_time("2026-11-11T00:00:00Z")
        inside = [h for h in world.hourly("cp_0001") if start <= parse_time(h["hour"]) < end]
        outside = [h for h in world.hourly("cp_0001") if not start <= parse_time(h["hour"]) < end]
        self.assertTrue(all(h["platform_conversions"] == h["conversions"] for h in outside))
        app, platform = sum(h["conversions"] for h in inside), sum(h["platform_conversions"] for h in inside)
        self.assertGreater(app, 60)
        self.assertTrue(0.15 < platform / app < 0.45, (platform, app))
        listed = [f for f in world.faults() if f["kind"] == "tracking"]
        self.assertEqual([(f["target"], f["from"], f["to"], f["factor"]) for f in listed],
                         [("cp_0001", "2026-11-07T00:00:00Z", "2026-11-11T00:00:00Z", 0.3)])

    def test_build_faults_drawn_forced_and_off(self):
        hidden = self.init("b", "W1", 3)
        for i in range(60):
            run(hidden, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
        world = World.load(hidden)
        faulty = [iid for iid, it in world.items.items() if it["attrs"] != it["requested"]]
        self.assertTrue(4 <= len(faulty) <= 24, len(faulty))
        for iid in faulty:
            item = world.items[iid]
            self.assertEqual(sum(item["attrs"][k] != item["requested"][k] for k in item["attrs"]), 1)
            manifest = run(hidden, "manifest", iid)[1]
            self.assertIn(", ".join(f"{k}={v}" for k, v in item["attrs"].items()), manifest)
            echo_is_request = ", ".join(f"{k}={v}" for k, v in item["requested"].items())
            self.assertNotIn(echo_is_request + ".", manifest)
        self.assertEqual(sorted(f["target"] for f in world.faults() if f["kind"] == "build"), sorted(faulty))
        quiet = self.init("q", "W1", 3, "--no-faults")
        for i in range(30):
            run(quiet, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
        self.assertEqual(World.load(quiet).faults(), [])
        forced = World.create(self.tmp / "f", load_config("W1"), 1, faults=False)
        forced.apply_ops([{"op": "build", "id": "it_0012", "attrs": W1_ATTRS, "text": SPECIFIC_TEXT,
                           "fault": {"offer": "discount"}, "at": "2026-11-07T12:00:00Z"}])
        self.assertEqual(forced.items["it_0012"]["attrs"]["offer"], "discount")
        self.assertEqual(forced.faults()[0]["target"], "it_0012")

    def test_w3_build_faults_change_only_the_format(self):
        hidden = self.init("w3b", "W3", 4)
        for i in range(80):
            run(hidden, "build", "--attrs", '{"format": "meme", "topic": "player-story"}', "--text", SPECIFIC_TEXT)
        world = World.load(hidden)
        faulty = [it for it in world.items.values() if it["attrs"] != it["requested"]]
        self.assertTrue(2 <= len(faulty) <= 20, len(faulty))
        self.assertTrue(all(it["attrs"]["topic"] == "player-story" and it["attrs"]["format"] != "meme" for it in faulty))

    def test_delivery_faults(self):
        hidden = self.init("w3", "W3", 2)
        run(hidden, "build", "--attrs", '{"format": "meme", "topic": "player-story"}', "--text", SPECIFIC_TEXT)
        world = World.load(hidden)
        for day in range(7):
            for slot in World.load(hidden).free_slots():
                code, out = run(hidden, "post", "it_0001", "--at", iso(slot))
                self.assertEqual(code, 0, out)
            admin(hidden, "advance", "--hours", "24")
        world = World.load(hidden)
        start, end = parse_time("2026-11-06T00:00:00Z"), parse_time("2026-11-08T00:00:00Z")
        done = [(pid, p) for pid, p in world.posts.items() if p["status"] == "done"]
        self.assertGreater(len(done), 15)
        for pid, post in done:
            share = world.hourly(pid)[0]["target_share"]
            self.assertEqual(share, 0.12 if start <= parse_time(post["slot"]) < end else 0.85, post["slot"])
        hit = sorted(f["target"] for f in world.faults() if f["kind"] == "delivery")
        self.assertEqual(hit, sorted(pid for pid, p in world.posts.items() if start <= parse_time(p["slot"]) < end))
        self.assertIn("target audience 12%", run(hidden, "report", "--audience")[1])
        paid = World.create(self.tmp / "d", load_config("W1"), 1, faults=False)
        paid.apply_ops([{"op": "build", "id": "it_0001", "attrs": W1_ATTRS, "text": SPECIFIC_TEXT},
                        {"op": "launch", "id": "cp_0001", "item": "it_0001", "daily_budget": 30, "at": "2026-11-02T00:00:00Z"},
                        {"op": "launch", "id": "cp_0002", "item": "it_0001", "daily_budget": 30, "at": "2026-11-02T00:00:00Z"},
                        {"op": "inject", "fault": "delivery", "campaign": "cp_0001", "from": "2026-11-02T00:00:00Z",
                         "to": "2026-11-12T00:00:00Z", "target_share": 0.12}])
        paid.advance(24 * 10)
        hit, clean = paid.hourly("cp_0001"), paid.hourly("cp_0002")
        self.assertTrue(all(h["target_share"] == 0.12 for h in hit) and all(h["target_share"] == 0.85 for h in clean))
        self.assertLess(sum(h["conversions"] for h in hit), 0.6 * sum(h["conversions"] for h in clean))

    def test_rejection_and_resubmit(self):
        hidden = self.init("r", "W1", 1, "--overrides", '{"rejection_p": 1}')
        run(hidden, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
        code, out = run(hidden, "launch", "it_0001", "--daily-budget", "20")
        self.assertEqual(code, 1)
        self.assertEqual(out.splitlines()[1], "Rejected by platform review. Retry with: sim resubmit cp_0001")
        world = World.load(hidden)
        self.assertEqual((world.campaigns["cp_0001"]["status"], world.campaigns["cp_0001"]["launched_at"]), ("rejected", None))
        self.assertEqual(run(hidden, "resubmit", "cp_0001")[0], 1)
        world.state["overrides"]["rejection_p"] = 0
        world.save()
        code, out = run(hidden, "resubmit", "cp_0001")
        self.assertEqual((code, out.splitlines()[1]), (0, "Launched cp_0001 (item it_0001) at $20.00/day after review."))
        self.assertEqual(World.load(hidden).campaigns["cp_0001"]["launched_at"], "2026-11-02T00:00:00Z")


class Money(LabCase):
    def test_balance_runs_out_then_a_grant_resumes(self):
        hidden = self.init("m", "W1", 1, "--money", "5", "--no-faults")
        run(hidden, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
        run(hidden, "launch", "it_0001", "--daily-budget", "30")
        admin(hidden, "advance", "--hours", "12")
        world = World.load(hidden)
        self.assertEqual(world.campaigns["cp_0001"]["status"], "exhausted")
        self.assertTrue(0 <= world.balance() < 0.10)
        self.assertIn("Out of money: cp_0001", run(hidden, "status")[1])
        self.assertEqual(run(hidden, "resume", "cp_0001")[0], 1)
        self.assertEqual(run(hidden, "launch", "it_0001", "--daily-budget", "10")[0], 1)
        admin(hidden, "grant", "100")
        world = World.load(hidden)
        self.assertEqual((world.campaigns["cp_0001"]["status"], world.money_received()), ("live", 105.0))
        admin(hidden, "advance", "--hours", "6")
        self.assertGreater(World.load(hidden).spend_total(), 5.0)
        self.assertEqual(World.load(hidden).truth()["money_received"], 105.0)

    def test_daily_budget_and_cap_hold(self):
        hidden = self.init("c", "W1", 1, "--no-faults")
        for budget in ("100", "5"):
            run(hidden, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
        run(hidden, "launch", "it_0001", "--daily-budget", "100")
        run(hidden, "launch", "it_0002", "--daily-budget", "5")
        admin(hidden, "advance", "--hours", "96")
        world = World.load(hidden)
        for cid, limit in (("cp_0001", 300), ("cp_0002", 50)):
            days = {}
            for h in world.hourly(cid):
                days[h["hour"][:10]] = days.get(h["hour"][:10], 0) + h["clicks"]
            self.assertEqual(len(days), 4)
            self.assertTrue(all(v <= limit for v in days.values()), days)
        self.assertEqual(world.validate(), [])

    def test_w2_cap_is_shared_by_a_groups_campaigns(self):
        hidden = self.init("w2", "W2", 1, "--no-faults")
        for _ in range(2):
            run(hidden, "build", "--attrs", '{"group": "g05"}', "--text", SPECIFIC_TEXT)
        run(hidden, "launch", "it_0001", "--daily-budget", "15")
        run(hidden, "launch", "it_0002", "--daily-budget", "5")
        admin(hidden, "advance", "--hours", "120")
        world = World.load(hidden)
        for cid, limit in (("cp_0001", 22), ("cp_0002", 7)):
            days = {}
            for h in world.hourly(cid):
                days[h["hour"][:10]] = days.get(h["hour"][:10], 0) + h["clicks"]
            self.assertTrue(all(v <= limit for v in days.values()), (cid, days))
        self.assertEqual(world.validate(), [])


class Truth(LabCase):
    def test_truth_matches_the_world_files(self):
        for wid in ("W1", "W2", "W3", "W4", "W5"):
            cfg = load_config(wid)
            world = World.create(self.tmp / wid, cfg, 1)
            truth = world.truth()
            self.assertEqual([a["name"] for a in truth["attributes"]], [a["name"] for a in cfg["attributes"]])
            self.assertEqual(truth["money_received"], float(cfg["money"]))
            rates = truth.get("type_rates") or truth["type_follows"]
            n_types = 1
            for a in cfg["attributes"]:
                if a["name"] in cfg.get("truth_attributes", [a["name"]]):
                    n_types *= len(a["values"])
            self.assertEqual(len(rates), n_types)
            self.assertEqual(max(rates, key=rates.get), truth["best_type"])
            if cfg["kind"] == "paid":
                self.assertEqual((truth["cpc"], truth["cap"]), (cfg["cpc"], cfg["cap"]))
        code, out = admin(self.init("t", "W1", 1), "truth")
        self.assertEqual(json.loads(out)["best_type"], "hook=story|visual=coach-face|offer=free-trial")


class Apply(LabCase):
    OPS = [{"op": "build", "id": "it_0001", "attrs": W1_ATTRS, "text": SPECIFIC_TEXT, "at": "2026-11-02T00:00:00Z"},
           {"op": "launch", "id": "cp_0001", "item": "it_0001", "daily_budget": 15, "at": "2026-11-02T00:00:00Z"},
           {"op": "record", "campaign": "cp_0001", "from": "2026-11-02T00:00:00Z", "to": "2026-11-05T00:00:00Z",
            "clicks": 420, "conversions": 31, "platform_conversions": 20}]

    def test_apply_builds_the_exact_recorded_numbers(self):
        world = World.create(self.tmp / "a", load_config("W1"), 1, faults=False)
        world.apply_ops(self.OPS)
        world.now = "2026-11-05T00:00:00Z"
        hours = world.hourly("cp_0001")
        self.assertEqual(len(hours), 72)
        self.assertEqual((sum(h["clicks"] for h in hours), sum(h["conversions"] for h in hours),
                          sum(h["platform_conversions"] for h in hours)), (420, 31, 20))
        for h in hours:
            self.assertTrue(0 <= h["platform_conversions"] <= h["conversions"] <= h["clicks"])
            self.assertEqual(h["spend"], round(h["clicks"] * 0.10, 2))
            self.assertEqual(sum(n for _t, n in h["app_arrivals"]), h["conversions"])
            self.assertTrue(all(t == h["hour"] for t, _n in h["app_arrivals"]))
            self.assertEqual(h["target_share"], 0.85)
        self.assertEqual(world.validate(), [])
        before = sum(h["conversions"] for h in hours if not h["hour"].startswith("2026-11-03"))
        world.apply_ops([{"op": "record", "campaign": "cp_0001", "from": "2026-11-03T00:00:00Z",
                          "to": "2026-11-04T00:00:00Z", "clicks": 100, "conversions": 5}])
        hours = world.hourly("cp_0001")
        self.assertEqual(sum(h["clicks"] for h in hours), 380)
        self.assertEqual(sum(h["conversions"] for h in hours), before + 5)

    def test_validate_refuses_impossible_records(self):
        world = World.create(self.tmp / "v", load_config("W1"), 1, faults=False)
        world.apply_ops(self.OPS[:2] + [{"op": "record", "campaign": "cp_0001", "from": "2026-11-02T00:00:00Z",
                                         "to": "2026-11-04T00:00:00Z", "clicks": 500, "conversions": 30}])
        world.now = "2026-11-05T00:00:00Z"
        problems = world.validate()
        self.assertTrue(any("budget and the cap allow" in p for p in problems), problems)
        self.assertTrue(any("no record" in p for p in problems), problems)

    def test_simadmin_apply(self):
        hidden = self.init("cli", "W1", 1, "--no-faults")
        ops = self.tmp / "ops.json"
        ops.write_text(json.dumps({"ops": self.OPS, "now": "2026-11-05T00:00:00Z"}))
        self.assertEqual(admin(hidden, "apply", str(ops))[0], 0)
        self.assertIn("conversions 20", run(hidden, "report")[1])
        self.assertEqual(lines_of(hidden)[-1]["argv"], ["sim", "report"])
        bad = self.init("bad", "W1", 1, "--no-faults")
        ops.write_text(json.dumps({"ops": self.OPS, "now": "2026-11-06T00:00:00Z"}))
        code, out = admin(bad, "apply", str(ops))
        self.assertEqual(code, 1)
        self.assertIn("apply refused", out)


class Outputs(LabCase):
    def test_paid_command_shapes(self):
        hidden = self.init("o", "W1", 1, "--overrides", '{"rejection_p": 0, "build_fault_p": 0}')
        outs = {}
        for name, args in [("status", ["status"]), ("catalog", ["catalog"]), ("library", ["library"]),
                           ("build", ["build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT]),
                           ("manifest", ["manifest", "it_0001"]), ("launch", ["launch", "it_0001", "--daily-budget", "20"])]:
            code, outs[name] = run(hidden, *args)
            self.assertEqual(code, 0, outs[name])
        admin(hidden, "advance", "--hours", "60")
        for name, args in [("pause", ["pause", "cp_0001"]), ("resume", ["resume", "cp_0001"]),
                           ("budget", ["set-budget", "cp_0001", "30"]), ("report", ["report"]),
                           ("byday", ["report", "--by", "day", "--audience"]), ("attribution", ["attribution"]),
                           ("attr_day", ["attribution", "--campaign", "cp_0001", "--by", "day"]), ("status2", ["status"]),
                           ("since", ["report", "--since", "2026-11-03", "--until", "2026-11-04T00:00:00Z"])]:
            code, outs[name] = run(hidden, *args)
            self.assertEqual(code, 0, outs[name])
        for text in outs.values():
            self.assertRegex(text.splitlines()[0], NOW_LINE)
        self.assertEqual(outs["status"].splitlines()[1],
                         "Balance $600.00 of $600.00. Live: none. Spend today $0.00, yesterday $0.00.")
        self.assertRegex(outs["status2"].splitlines()[1], r"^Balance \$[\d,]+\.\d\d of \$600\.00\. Live: cp_0001\. "
                                                         r"Spend today \$\d+\.\d\d, yesterday \$\d+\.\d\d\.$")
        catalog = outs["catalog"]
        for part in ("hook: claim, question, story", "visual: app-screen, hand-replay, coach-face",
                     "offer: free-trial, discount, none", "$5 to $100", "pause; resume; resubmit",
                     "Cost per click: $0.10.", "Volume cap: 300 clicks per campaign per day.",
                     "Audience: people who play poker in home games and casinos and want to make better decisions at the table.",
                     "up to 2 days", "`sim library` holds what competitors run"):
            self.assertIn(part, catalog)
        lib = outs["library"].splitlines()
        self.assertEqual(lib[1], "Library: 24 items.")
        self.assertEqual(len(lib), 26)
        self.assertRegex(lib[2], r'^lib_01 · Rival [A-D] · running \d+ days · ".+" · shows: .+ · offer: .+$')
        self.assertEqual(outs["build"].splitlines()[1], "Built it_0001 from your request (hook=story, visual=coach-face, "
                                                        "offer=free-trial). See what was built with: sim manifest it_0001")
        self.assertEqual(outs["manifest"].splitlines()[1:], [
            "it_0001, built 2026-11-02T00:00:00Z: hook=story, visual=coach-face, offer=free-trial.",
            f'Text: "{SPECIFIC_TEXT}"'])
        self.assertEqual(outs["launch"].splitlines()[1], "Launched cp_0001 (item it_0001) at $20.00/day.")
        self.assertEqual(outs["pause"].splitlines()[1], "Paused cp_0001.")
        self.assertEqual(outs["resume"].splitlines()[1], "Resumed cp_0001 at $20.00/day.")
        self.assertEqual(outs["budget"].splitlines()[1], "Set cp_0001's daily budget to $30.00.")
        row = r"cp_0001 · live · it_0001 · \$30\.00/day · spend \$\d+\.\d\d · clicks [\d,]+ · conversions \d+ · " \
              r"(\$\d+\.\d\d per conversion|no conversions) · saves \d+ · hides \d+"
        self.assertRegex(outs["report"].splitlines()[2], "^" + row + "$")
        days = outs["byday"].splitlines()[2:]
        self.assertEqual([d.split(" · ")[1] for d in days], ["2026-11-02", "2026-11-03", "2026-11-04"])
        self.assertTrue(all(d.endswith("target audience 85%") for d in days))
        self.assertRegex(outs["attribution"].splitlines()[2], r"^cp_0001 · it_0001 · \d+ conversions arrived$")
        self.assertIn("up to 2 days", outs["attribution"])
        self.assertEqual(len(outs["attr_day"].splitlines()), 5)
        self.assertEqual(len(outs["since"].splitlines()), 3)
        for args, code in ((["launch", "it_0001", "--daily-budget", "500"], 1), (["build", "--attrs", "{}", "--text", "x"], 1),
                           (["fly"], 2), (["launch"], 2), (["manifest", "it_0999"], 1)):
            got, text = run(hidden, *args)
            self.assertEqual(got, code, text)
            self.assertRegex(text.splitlines()[0], NOW_LINE)

    def test_post_commands_notify_and_gws(self):
        hidden = self.init("p", "W3", 1, "--no-faults")
        status = run(hidden, "status")[1].splitlines()
        self.assertIn("Free slots in the next 48 hours: 2026-11-02T09:00:00Z, 2026-11-02T13:00:00Z", status[3])
        self.assertIn("format: clip, carousel, meme", run(hidden, "catalog")[1])
        run(hidden, "build", "--attrs", '{"format": "meme", "topic": "player-story"}', "--text", SPECIFIC_TEXT)
        slots = run(hidden, "slots")[1].splitlines()
        self.assertEqual(slots[1:3], ["Free slots in the next 48 hours:", "2026-11-02T09:00:00Z"])
        self.assertEqual(len(slots), 2 + 6)
        code, out = run(hidden, "post", "it_0001", "--at", "2026-11-02T13:00:00Z")
        self.assertEqual((code, out.splitlines()[1]), (0, "Scheduled po_0001 (item it_0001) for 2026-11-02T13:00:00Z."))
        self.assertEqual(run(hidden, "post", "it_0001", "--at", "2026-11-02T13:00:00Z")[0], 1)
        self.assertEqual(run(hidden, "post", "it_0001", "--at", "2026-11-05T13:00:00Z")[0], 1)
        self.assertEqual(run(hidden, "launch", "it_0001", "--daily-budget", "10")[0], 1)
        admin(hidden, "advance", "--hours", "48")
        report = run(hidden, "report", "--audience")[1].splitlines()
        self.assertRegex(report[2], r"^po_0001 · done · it_0001 · slot 2026-11-02T13:00:00Z · reach [\d,]+ · follows \d+ · "
                                    r"saves \d+ · hides \d+ · target audience 85%$")
        self.assertRegex(run(hidden, "attribution")[1].splitlines()[1], r"^The profile's own follower count: [\d,]+\.")
        code, out = run(hidden, "--kind", "money-request", "--json", '{"amount": 100}', tool="notify")
        self.assertEqual((code, out), (0, "Sent to the account owner.\n"))
        run(hidden, "--kind", "note", "--json", "not json", tool="notify")
        self.assertEqual(run(hidden, "--json", "{}", tool="notify")[0], 2)
        outbox = [json.loads(line) for line in (hidden / "outbox.jsonl").read_text().splitlines()]
        self.assertEqual([(o["kind"], o["payload"]) for o in outbox], [("money-request", {"amount": 100}), ("note", "not json")])
        self.assertEqual(set(outbox[0]), {"wall_time", "sim_time", "kind", "payload"})
        self.assertEqual(outbox[0]["sim_time"], "2026-11-04T00:00:00Z")
        self.assertEqual(run(hidden, "drive", "files", "list", tool="gws"), (1, "gws is not available on this account.\n"))

    def test_every_agent_facing_call_is_logged_and_simadmin_is_not(self):
        hidden = self.init("l", "W1", 1)
        run(hidden, "status")
        run(hidden, "nope")
        run(hidden, "--kind", "money-request", "--json", "{}", tool="notify")
        run(hidden, "sheets", tool="gws")
        admin(hidden, "advance", "--hours", "1")
        logged = lines_of(hidden)
        self.assertEqual([(e["argv"], e["exit"]) for e in logged],
                         [(["sim", "status"], 0), (["sim", "nope"], 2),
                          (["notify", "--kind", "money-request", "--json", "{}"], 0), (["gws", "sheets"], 1)])
        for entry in logged:
            self.assertEqual(set(entry), {"wall_time", "sim_time", "argv", "exit", "stdout_head"})
            self.assertEqual(entry["sim_time"], "2026-11-02T00:00:00Z")
            self.assertLessEqual(len(entry["stdout_head"]), 500)


W5_WINNER = {"hook": "challenge", "visual": "hand-replay", "offer": "free-trial", "presenter": "coach",
             "voice": "energetic", "music": "upbeat", "captions": "burned-in", "length": "15s", "opening": "cards",
             "closing_ask": "try-free", "palette": "felt-green", "format": "vertical"}
OVERPROMISE = "I kept losing my stack at the home game. Now I never lose on the river, guaranteed. Try it free for 7 days."
GENERIC_TEXT = "Level up your game with the best poker app!"


class W5Builds(LabCase):
    """PLAN.md 13.2: a W5 build sets what it is given and draws the rest; `--from` copies a parent and changes only
    what is given; the manifest shows all twelve values, the text and `made_from`. W1 to W4 build as before."""

    def test_partial_builds_draw_the_rest_the_same_way_for_the_same_seed(self):
        a, b = self.init("a", "W5", 3, "--no-faults"), self.init("b", "W5", 3, "--no-faults")
        given = {"hook": "challenge", "visual": "hand-replay", "offer": "free-trial"}
        for hidden in (a, b):
            code, out = run(hidden, "build", "--attrs", json.dumps(given), "--text", SPECIFIC_TEXT)
            self.assertEqual(code, 0, out)
            self.assertIn("The 9 attributes you left out came out as the production made them.", out)
            self.assertNotIn("presenter=", out)   # the echo is the request, not what was built
        wa, wb = World.load(a), World.load(b)
        self.assertEqual(wa.items["it_0001"]["attrs"], wb.items["it_0001"]["attrs"])
        item = wa.items["it_0001"]
        self.assertEqual((item["requested"], item["made_from"]), (given, None))
        self.assertEqual(sorted(item["drawn"]), sorted(n for n in wa.attribute_names() if n not in given))
        self.assertEqual(list(item["attrs"]), wa.attribute_names())
        other = self.init("c", "W5", 4, "--no-faults")
        drawn = []
        for i in range(8):
            run(other, "build", "--attrs", json.dumps(given), "--text", SPECIFIC_TEXT)
        for item in World.load(other).items.values():
            drawn.append(tuple(item["attrs"][n] for n in item["drawn"]))
        self.assertGreater(len(set(drawn)), 1, "a rebuild from scratch changes things nobody chose")

    def test_build_from_a_parent_changes_only_what_is_given(self):
        hidden = self.init("f", "W5", 1, "--no-faults")
        run(hidden, "build", "--attrs", json.dumps(W5_WINNER), "--text", SPECIFIC_TEXT)
        code, out = run(hidden, "build", "--from", "it_0001", "--attrs", '{"presenter": "player"}')
        self.assertEqual((code, out.splitlines()[1]), (0, "Built it_0002 from your request: it_0001 with "
                                                           "presenter=player. See what was built with: sim manifest it_0002"))
        world = World.load(hidden)
        child = world.items["it_0002"]
        self.assertEqual(child["attrs"], dict(W5_WINNER, presenter="player"))
        self.assertEqual((child["text"], child["made_from"], child["drawn"]), (SPECIFIC_TEXT, "it_0001", []))
        code, out = run(hidden, "build", "--from", "it_0001", "--attrs", '{"music": "none"}', "--text", NEUTRAL_TEXT)
        self.assertIn("with music=none and new text", out)
        self.assertEqual(World.load(hidden).items["it_0003"]["text"], NEUTRAL_TEXT)
        self.assertEqual(run(hidden, "build", "--from", "it_0099")[0], 1)
        self.assertEqual(run(hidden, "build", "--from", "it_0001", "--attrs", '{"presenter": "robot"}')[0], 1)
        self.assertEqual(run(hidden, "build", "--attrs", '{"tone": "warm"}', "--text", SPECIFIC_TEXT)[0], 1)

    def test_manifest_shows_twelve_values_the_text_and_the_parent(self):
        hidden = self.init("m", "W5", 1, "--no-faults")
        run(hidden, "build", "--attrs", json.dumps(W5_WINNER), "--text", SPECIFIC_TEXT)
        run(hidden, "build", "--from", "it_0001", "--attrs", '{"presenter": "player"}')
        lines = run(hidden, "manifest", "it_0002")[1].splitlines()
        self.assertEqual(lines[1], "it_0002, built 2026-11-02T00:00:00Z: " + ", ".join(
            f"{k}={v}" for k, v in dict(W5_WINNER, presenter="player").items()) + ".")
        self.assertEqual(lines[2:], [f'Text: "{SPECIFIC_TEXT}"', "Made from: it_0001."])
        self.assertEqual(run(hidden, "manifest", "it_0001")[1].splitlines()[3], "Made from: nothing; it was built new.")

    def test_a_build_fault_from_a_parent_changes_one_requested_value(self):
        hidden = self.init("bf", "W5", 2, "--overrides", '{"build_fault_p": 1}')
        run(hidden, "build", "--attrs", json.dumps(W5_WINNER), "--text", SPECIFIC_TEXT)
        run(hidden, "build", "--from", "it_0001", "--attrs", '{"presenter": "player"}')
        world = World.load(hidden)
        child = world.items["it_0002"]
        changed = [k for k in child["attrs"] if child["attrs"][k] != child["requested"][k]]
        self.assertEqual(len(changed), 1)
        fault = [f for f in world.faults() if f["target"] == "it_0002"][0]
        self.assertEqual((fault["attr"], fault["built"]), (changed[0], child["attrs"][changed[0]]))
        self.assertIn(f"{changed[0]}={child['attrs'][changed[0]]}", run(hidden, "manifest", "it_0002")[1])

    def test_w1_to_w4_still_need_every_attribute_and_have_no_from(self):
        for wid in ("W1", "W2", "W3", "W4"):
            hidden = self.init("old" + wid, wid, 1, "--no-faults")
            first = {a["name"]: a["values"][0] for a in load_config(wid)["attributes"]}
            partial = dict(list(first.items())[:1]) if len(first) > 1 else {}
            code, out = run(hidden, "build", "--attrs", json.dumps(partial), "--text", SPECIFIC_TEXT)
            self.assertEqual(code, 1, (wid, out))
            self.assertIn("--attrs needs exactly these attributes", out)
            run(hidden, "build", "--attrs", json.dumps(first), "--text", SPECIFIC_TEXT)
            code, out = run(hidden, "build", "--from", "it_0001", "--attrs", "{}")
            self.assertEqual((code, out.splitlines()[1]), (2, "Error: unknown option --from."), wid)
            item = World.load(hidden).items["it_0001"]
            self.assertNotIn("made_from", item)
            self.assertEqual(len(run(hidden, "manifest", "it_0001")[1].splitlines()), 3)
            catalog = run(hidden, "catalog")[1]
            self.assertNotIn("sim build --from", catalog)

    def test_w5_catalog_names_all_twelve_and_what_a_build_sets(self):
        catalog = run(self.init("cat", "W5", 1), "catalog")[1]
        for a in load_config("W5")["attributes"]:
            self.assertIn(f"  {a['name']}: {', '.join(a['values'])}", catalog)
        self.assertIn("A build sets the attributes you give it in --attrs; every attribute you leave out comes out "
                      "however this production happens to make it", catalog)
        self.assertIn("`sim build --from ITEM --attrs JSON` keeps that item's values and text", catalog)
        self.assertIn("sim build --from ITEM [--attrs JSON] [--text TEXT]", catalog)


class SoftSignals(LabCase):
    """PLAN.md 13.2: comments by kind and saves and hides, drawn per seed from each item's hidden reception, with no
    effect on conversions."""

    def _three_ads(self, hidden):
        attrs = {"hook": "story", "visual": "app-screen", "offer": "free-trial"}
        for text in (OVERPROMISE, SPECIFIC_TEXT, GENERIC_TEXT):
            run(hidden, "build", "--attrs", json.dumps(attrs), "--text", text)
        for item in ("it_0001", "it_0002", "it_0003"):
            run(hidden, "launch", item, "--daily-budget", "30")
        admin(hidden, "advance", "--hours", "96")

    def test_reception_follows_the_copy_and_never_moves_a_conversion(self):
        hidden = self.init("s", "W1", 6, "--no-faults")
        self._three_ads(hidden)
        world = World.load(hidden)
        kinds = {}
        for cid in ("cp_0001", "cp_0002", "cp_0003"):
            found = world.comments(cid)
            kinds[cid] = {k: sum(1 for c in found if c["kind"] == k) for k in ("praise", "question", "complaint",
                                                                              "spam call-out")}
            self.assertGreater(len(found), 15, cid)
        misleading, specific, generic = kinds["cp_0001"], kinds["cp_0002"], kinds["cp_0003"]
        self.assertGreater(misleading["complaint"], max(v for k, v in misleading.items() if k != "complaint"))
        self.assertTrue(all("mislead" in c["text"].lower() or "promis" in c["text"].lower() or "oversell" in
                            c["text"].lower() or "lie" in c["text"].lower()
                            for c in world.comments("cp_0001") if c["kind"] == "complaint"))
        self.assertGreater(generic["spam call-out"], specific["spam call-out"])
        self.assertGreater(specific["question"], generic["question"])
        saves = {cid: world.saves_hides(cid) for cid in ("cp_0001", "cp_0002", "cp_0003")}
        self.assertGreater(saves["cp_0002"][0], saves["cp_0003"][0])
        self.assertGreater(saves["cp_0001"][1], saves["cp_0002"][1])
        # the same run with no reception at all: identical clicks and conversions, hour by hour
        quiet_cfg = load_config("W1")
        quiet_cfg.pop("reception")
        quiet = World.create(self.tmp / "quiet", quiet_cfg, 6, faults=False)
        quiet.save()
        self._three_ads(self.tmp / "quiet")
        for cid in ("cp_0001", "cp_0002", "cp_0003"):
            self.assertEqual(World.load(self.tmp / "quiet").hourly(cid), world.hourly(cid))
        self.assertEqual(World.load(self.tmp / "quiet").comments("cp_0001"), [])

    def test_comments_command_and_report_columns(self):
        a, b = self.init("ca", "W1", 8, "--no-faults"), self.init("cb", "W1", 8, "--no-faults")
        for hidden in (a, b):
            self._three_ads(hidden)
        run(b, "report")
        run(b, "comments", "cp_0002")
        self.assertEqual(run(a, "comments", "cp_0001")[1], run(b, "comments", "cp_0001")[1])
        lines = run(a, "comments", "cp_0001")[1].splitlines()
        self.assertRegex(lines[1], r"^Comments on cp_0001 \(item it_0001\) from 2026-11-02T00:00:00Z to "
                                   r"2026-11-06T00:00:00Z: \d+ in all\.$")
        self.assertRegex(lines[2], r"^praise \d+ · question \d+ · complaint \d+ · spam call-out \d+$")
        self.assertEqual(lines[3], "Some of them:")
        self.assertTrue(1 <= len(lines[4:]) <= 4 and all(re.match(r'^  [a-z -]+: ".+"$', line) for line in lines[4:]))
        day = run(a, "comments", "cp_0001", "--from", "2026-11-03", "--to", "2026-11-04")[1].splitlines()[1]
        self.assertIn("from 2026-11-03T00:00:00Z to 2026-11-04T00:00:00Z", day)
        whole = int(re.search(r"(\d+) in all", lines[1]).group(1))
        parts = sum(int(re.search(r"(\d+) in all", run(a, "comments", "cp_0001", "--from", f"2026-11-0{d}", "--to",
                                                       f"2026-11-0{d + 1}")[1]).group(1)) for d in range(2, 6))
        self.assertEqual(parts, whole)
        total = run(a, "report", "--campaign", "cp_0001")[1].splitlines()[2]
        by_day = run(a, "report", "--campaign", "cp_0001", "--by", "day")[1].splitlines()[2:]
        saves = lambda line: int(re.search(r"saves (\d+)", line).group(1))
        self.assertEqual(saves(total), sum(saves(line) for line in by_day))
        self.assertEqual(run(a, "comments", "cp_0099")[0], 1)
        self.assertEqual(run(a, "comments")[0], 2)

    def test_posts_draw_comments_and_paid_worlds_without_reception_show_none(self):
        hidden = self.init("w3", "W3", 2, "--no-faults")
        run(hidden, "build", "--attrs", '{"format": "meme", "topic": "player-story"}', "--text", SPECIFIC_TEXT)
        run(hidden, "post", "it_0001", "--at", "2026-11-02T13:00:00Z")
        admin(hidden, "advance", "--hours", "24")
        self.assertRegex(run(hidden, "comments", "po_0001")[1].splitlines()[1],
                         r"^Comments on po_0001 \(item it_0001\) from .*: \d+ in all\.$")
        self.assertIn("sim comments POST", run(hidden, "catalog")[1])
        for wid in ("W2", "W4"):
            other = self.init("none" + wid, wid, 1, "--no-faults")
            attrs = {a["name"]: a["values"][0] for a in load_config(wid)["attributes"]}
            run(other, "build", "--attrs", json.dumps(attrs), "--text", SPECIFIC_TEXT)
            run(other, "launch", "it_0001", "--daily-budget", "20")
            admin(other, "advance", "--hours", "24")
            code, out = run(other, "comments", "cp_0001")
            self.assertEqual((code, out.splitlines()[1]), (2, "Error: unknown command 'comments'."), wid)
            self.assertNotIn("saves", run(other, "report")[1], wid)
            self.assertNotIn("comments", run(other, "catalog")[1], wid)


class Preview(LabCase):
    def test_labels_only_where_the_role_test_wrote_them(self):
        hidden = self.init("p", "W1", 1, "--no-faults")
        run(hidden, "build", "--attrs", json.dumps(W1_ATTRS), "--text", SPECIFIC_TEXT)
        self.assertEqual(run(hidden, "preview", "A")[0], 2)
        (hidden / "previews.json").write_text(json.dumps({"A": "it_0001"}))
        code, out = run(hidden, "preview", "a")
        self.assertEqual(out.splitlines()[1:], ["Ad A, as the platform serves it: hook=story, visual=coach-face, "
                                                "offer=free-trial.", f'Text: "{SPECIFIC_TEXT}"'])
        self.assertNotIn("it_0001", out)
        self.assertEqual(run(hidden, "preview", "B")[0], 1)
        self.assertNotIn("preview", run(hidden, "help")[1])


class WhatAgentsNeverSee(LabCase):
    def _outputs(self, wid):
        hidden = self.init(wid, wid, 1)
        attrs = {a["name"]: a["values"][0] for a in load_config(wid)["attributes"]}
        reception = bool(load_config(wid).get("reception"))
        outs = []
        for args in (["status"], ["catalog"], ["library"], ["library", "--search", "a"], ["help"],
                     ["build", "--attrs", json.dumps(attrs), "--text", SPECIFIC_TEXT], ["manifest", "it_0001"],
                     ["build", "--attrs", "{}", "--text", NEUTRAL_TEXT]):
            outs.append(run(hidden, *args)[1])
        if load_config(wid)["kind"] == "paid":
            outs.append(run(hidden, "launch", "it_0001", "--daily-budget", "20")[1])
            admin(hidden, "advance", "--hours", "30")
            outs += [run(hidden, *a)[1] for a in (["report", "--by", "day", "--audience"], ["attribution", "--by", "day"])]
            if reception:
                outs.append(run(hidden, "comments", "cp_0001")[1])
        else:
            outs.append(run(hidden, "post", "it_0001", "--at", "2026-11-02T13:00:00Z")[1])
            admin(hidden, "advance", "--hours", "30")
            outs += [run(hidden, *a)[1] for a in (["report", "--audience"], ["attribution", "--by", "day"], ["slots"])]
            if reception:
                outs.append(run(hidden, "comments", "po_0001")[1])
        return outs

    def test_the_rubric_and_its_word_lists_never_show(self):
        for wid in ("W1", "W2", "W3", "W4", "W5"):
            cfg = load_config(wid)
            hidden_words = cfg.get("reception", {}).get("overpromise_phrases", [])
            for text in self._outputs(wid):
                low = text.lower()
                for word in ("generic", "neutral", "specific", "rubric", "quality", "reception", "overpromis"):
                    self.assertNotIn(word, low, (wid, text[:200]))
                for phrase in cfg["generic_phrases"]:
                    self.assertNotIn(phrase, low, (wid, phrase))
                for words in (cfg["generic_phrases"], cfg["specific_terms"], hidden_words):
                    for a, b in zip(words, words[1:]):
                        self.assertNotIn(f"{a}, {b}", low)
                        self.assertNotIn(f'"{a}", "{b}"', low)

    def test_the_library_is_never_tagged_with_the_maps_attributes(self):
        for wid in ("W1", "W2", "W3", "W4", "W5"):
            cfg = load_config(wid)
            world = World.create(self.tmp / ("lib" + wid), cfg, 1)
            names = [a["name"] for a in cfg["attributes"]]
            values = [v for a in cfg["attributes"] for v in a["values"]]
            lines = [cli.library_line(e) for e in world.library_entries()]
            self.assertTrue(lines)
            for line in lines:
                low = line.lower()
                # "offer:" is the plain-words offer line of PLAN.md 6.2's library format, not a tag
                self.assertFalse(any(f"{n}=" in low or (f"{n}:" in low and n != "offer") for n in names), line)
                self.assertFalse(any(v in low for v in values if "-" in v), line)
                self.assertNotRegex(low, r"\bg\d\d\b")
                if wid == "W5":
                    continue   # W5's prose says "a coach" or "dark" as a person would; it is never `presenter=coach`
                described = " ".join(part for part in line.split(" · ") if part.startswith(("shows:", "offer:")))
                for value in values:
                    self.assertNotRegex(described.lower(), rf"\b{re.escape(value)}\b", (wid, line))
            hidden = self.init("page" + wid, wid, 1)
            shown = run(hidden, "library")[1].splitlines()[2:]
            if len(lines) > 30:
                self.assertEqual(len(shown), 31)
                self.assertEqual(shown[-1], f"... {len(lines) - 30} more (narrow with --search or --owner)")
            else:
                self.assertEqual(shown, lines)
        hidden = self.init("owner", "W1", 1)
        owned = run(hidden, "library", "--owner", "rival b")[1].splitlines()[2:]
        self.assertTrue(owned and all(" · Rival B · " in line for line in owned))
        self.assertTrue(all("river" in line.lower() for line in run(hidden, "library", "--search", "RIVER")[1].splitlines()[2:]))


if __name__ == "__main__":
    unittest.main()
