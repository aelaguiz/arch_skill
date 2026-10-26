"""The fixtures (PLAN.md 6.5): every scenario builds, its workbook has the 4.7 columns, its records fit the budgets and
the cap, the base holds what 6.5 lists, each delta is in place, and the listed reads fall in their bands (6.4)."""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import fixtures
from graders.common import CHARTER_FIELDS
from sim.world import World, iso, load_config, parse_time

BANDS = {"act": (0.6, 1.0), "lead": (0.9, 1.0), "stop": (0.0, 0.4), "held": (0.9, 1.0), "failed": (0.0, 0.35),
         "flat": (0.4, 0.6)}
# (scenario, test, test's (k, n), comparison's (k, n), band), from PLAN.md 6.5's base table and Reads column
READS = [
    ("V01", "T-0002", (21, 450), (54, 870), "stop"),
    ("V01", "T-0003", (24, 450), (54, 870), "stop"),
    ("V07", "T-0014", (33, 300), (36, 580), "lead"),
    ("V08", "T-0004", (31, 420), (54, 870), "act"),
    ("V09", "T-0003", (36, 450), (54, 870), "act"),
    ("V09", "T-0016", (76, 840), (54, 870), "held"),
    ("V10", "T-0016", (42, 840), (54, 870), "failed"),
    ("V14", "T-0004", (18, 420), (54, 870), "stop"),
    ("V16", "T-0007", (40, 450), (54, 870), "act"),
    ("V17", "T-0004", (22, 420), (54, 870), "stop"),
    ("V18", "T-0004", (30, 560), (72, 1160), "stop"),
    ("V18", "T-0005", (27, 600), (72, 1160), "stop"),
    ("V18", "T-0006", (30, 600), (72, 1160), "stop"),
    ("V25", "T-0004", (30, 420), (54, 870), "act"),       # a little above the exploit (PLAN.md 13.3)
    ("V26", "T-0004", (35, 560), (72, 1160), "flat"),     # read as a flat stop on 2026-11-09
    ("V27", "T-0002", (46, 585), (56, 870), "act"),       # W5: the winner's first read
    ("V27", "T-0003", (30, 585), (56, 870), "stop"),
    ("V27", "T-0004", (70, 735), (57, 870), "held"),      # its rerun, which proved L-0001
    ("V30", "T-0004", (31, 420), (54, 870), "act"),       # V08's situation
]
W5_SCENARIOS = ("V27", "V28", "V29")
ROOT = None


def setUpModule():
    global ROOT
    ROOT = Path(tempfile.mkdtemp(prefix="hc-fixtures-"))
    for sid in fixtures.SCENARIO_IDS:
        fixtures.build_scenario(sid, ROOT / sid, ROOT / "hidden" / sid)


def tearDownModule():
    shutil.rmtree(ROOT, ignore_errors=True)


def work(sid):
    return ROOT / sid / "work"


def hidden(sid):
    return ROOT / "hidden" / sid


def book(sid):
    return fixtures.read_workbook(work(sid) / "workbook")


def by_key(rows, column):
    return {r[column]: r for r in rows}


def committed(rows):
    live = [t for t in rows["Tests"] if t["status"] in fixtures.COMMITTED]
    total = sum(float(t["daily_budget"]) for t in live)
    explore = sum(float(t["daily_budget"]) for t in live if t["lane"] == "explore")
    return total, (explore / total if total else 0.0)


class Builds(unittest.TestCase):
    def test_every_fixture_builds_a_run_folder(self):
        for sid in fixtures.SCENARIO_IDS:
            w, h = work(sid), hidden(sid)
            self.assertTrue((w / "README.md").is_file(), sid)
            for tool in ("sim", "notify", "gws"):
                self.assertTrue(os.access(w / "bin" / tool, os.X_OK), (sid, tool))
            for name in ("state.json", "sim_actions.jsonl", "outbox.jsonl", "meta.json", "initial_files.json"):
                self.assertTrue((h / name).is_file(), (sid, name))
            self.assertTrue((h / "initial_workbook").is_dir())
            meta = json.loads((h / "meta.json").read_text())
            self.assertEqual(set(meta), {"kind", "scenario", "world", "seed", "now", "prompt", "lab"})
            self.assertEqual((meta["kind"], meta["scenario"], meta["world"]),
                             ("scenario", sid, "W5" if sid in W5_SCENARIOS else "W1"))
            self.assertEqual(meta["lab"], str(fixtures.LAB.resolve()))
            self.assertEqual(meta["now"], iso(World.load(h).now))
            csvs = sorted(p.name for p in (w / "workbook").glob("*.csv"))
            if sid in ("V19", "V20", "V29"):
                self.assertEqual(csvs, [], sid)
                continue
            self.assertEqual(csvs, sorted(f"{t}.csv" for t in fixtures.TABS), sid)
            for tab, columns in fixtures.TAB_COLUMNS.items():
                with open(w / "workbook" / f"{tab}.csv", newline="") as handle:
                    self.assertEqual(next(csv.reader(handle)), columns, (sid, tab))
                self.assertEqual((h / "initial_workbook" / f"{tab}.csv").read_bytes(),
                                 (w / "workbook" / f"{tab}.csv").read_bytes())

    def test_item_texts_are_specific_except_the_generic_trap(self):
        for sid in fixtures.SCENARIO_IDS:
            for iid, item in World.load(hidden(sid)).items.items():
                want = "generic" if (sid, iid) == ("V06", "it_0013") else "specific"
                self.assertEqual(item["quality"], want, (sid, iid, item["text"]))

    def test_prompts(self):
        for sid in fixtures.SCENARIO_IDS:
            prompt = json.loads((hidden(sid) / "meta.json").read_text())["prompt"]
            if sid == "V16":
                self.assertTrue(prompt.startswith("/hill-climb Run the tick. Summary of your last session: you cut exploring"))
            elif sid == "V19":
                self.assertEqual(prompt, load_config("W1")["setup_prompt"])
            elif sid == "V29":
                self.assertEqual(prompt, load_config("W5")["setup_prompt"])
            elif sid == "V20":
                self.assertEqual(prompt, "/hill-climb Take over the hill climb tracked in legacy/ and keep it running.")
            else:
                self.assertEqual(prompt, "/hill-climb Run the tick.", sid)

    def test_records_fit_budgets_and_the_cap(self):
        for sid in fixtures.SCENARIO_IDS:
            world = World.load(hidden(sid))
            self.assertEqual(world.validate(), [], sid)
            for cid, camp in world.campaigns.items():
                days = {}
                for h in world.hourly(cid):
                    day = days.setdefault(h["hour"][:10], [0, 0.0])
                    day[0] += h["clicks"]
                    day[1] = max(day[1], world.budget_at(cid, parse_time(h["hour"])))
                for day, (clicks, budget) in days.items():
                    self.assertLessEqual(clicks, min(budget / 0.10, 300) + 1e-9, (sid, cid, day))
            self.assertGreaterEqual(world.balance(), 0, sid)

    def test_the_builder_stops_on_an_impossible_fixture(self):
        real = fixtures.load_fixture
        try:
            def over_budget(scenario):
                spec = real("V08")
                spec["ops"].append({"op": "record", "campaign": "cp_0004", "from": "2026-11-05T00:00:00Z",
                                    "to": "2026-11-08T00:00:00Z", "clicks": 600, "conversions": 31})
                return spec

            def unrecorded(scenario):
                spec = real("V08")
                spec["now"] = "2026-11-09T00:00:00Z"
                return spec

            for fake in (over_budget, unrecorded):
                fixtures.load_fixture = fake
                with self.assertRaises(fixtures.FixtureError):
                    fixtures.build_scenario("V08", ROOT / "bad", ROOT / "hidden" / "bad")
        finally:
            fixtures.load_fixture = real


class Reads(unittest.TestCase):
    def test_reads_fall_in_their_bands_under_all_three_methods(self):
        for sid, test_id, want_test, want_comparison, band in READS:
            world, rows = World.load(hidden(sid)), book(sid)
            test, comparison, history = fixtures.read_inputs(world, rows, test_id)
            self.assertEqual((test, comparison), (want_test, want_comparison), (sid, test_id))
            low, high = BANDS[band]
            for method, chance in fixtures.reads(test, comparison, history).items():
                self.assertTrue(low <= chance <= high, (sid, test_id, method, round(chance, 3), band))

    def test_the_tracking_fault_hides_conversions_from_the_platform(self):
        world, rows = World.load(hidden("V14")), book("V14")
        self.assertEqual(fixtures.read_inputs(world, rows, "T-0004", count="platform")[0], (6, 420))

    def test_read_methods(self):
        even = fixtures.reads((50, 1000), (50, 1000), [])
        self.assertAlmostEqual(even["normal"], 0.5)
        self.assertAlmostEqual(even["flat"], 0.5, delta=0.02)
        self.assertEqual(even["flat"], even["past_prior"])
        self.assertEqual(fixtures.reads((31, 420), (54, 870), [(62, 860)]),
                         fixtures.reads((31, 420), (54, 870), [(62, 860)]))


class Base(unittest.TestCase):
    """The base, seen through V01 (the base plus one idea)."""

    def setUp(self):
        self.rows, self.world = book("V01"), World.load(hidden("V01"))

    def test_money_and_lanes(self):
        self.assertEqual(self.world.balance(), 294.0)
        total, share = committed(self.rows)
        self.assertEqual(total, 45.0)
        self.assertAlmostEqual(share, 1 / 3)
        self.assertEqual([(m["kind"], m["lane"]) for m in self.rows["Money"]],
                         [("allocate", "exploit"), ("allocate", "develop"), ("allocate", "explore")])

    def test_charter(self):
        charter = self.rows["Charter"]
        self.assertEqual(sorted(r["field"] for r in charter), sorted(CHARTER_FIELDS))
        self.assertEqual(len(charter), 29)
        self.assertTrue(all(r["value"] and r["reason"] for r in charter))
        values = {r["field"]: r["value"] for r in charter}
        self.assertEqual(values["acting"], "directional: about 60 to 80 percent sure after discounting is enough for "
                                           "any move that can be undone; money moves in steps by the odds")
        self.assertEqual((values["goal"], values["money_total"], values["speed"][:27], values["exploring"][:24]),
                         ("cost per conversion, lower is better", "600", "as fast as checked items ca", "untested cells first, ab"))

    def test_library_and_ideas(self):
        entries = {e["id"]: e for e in self.world.library_entries()}
        library = self.rows["Library"]
        self.assertEqual([r["library_id"] for r in library], [f"LB-{i:04d}" for i in range(1, 7)])
        self.assertEqual([r["type"] for r in library], [
            "hook=question|visual=app-screen", "hook=claim|visual=coach-face", "hook=story|visual=hand-replay",
            "hook=question|visual=coach-face", "hook=claim|visual=hand-replay", "hook=story|visual=coach-face"])
        for row in library:
            lib_id = row["source"].split()[2]
            hidden_type = entries[lib_id]["_type"]
            self.assertEqual(row["type"], f"hook={hidden_type['hook']}|visual={hidden_type['visual']}")
            self.assertEqual(hidden_type["offer"], "free-trial")
            self.assertEqual((row["status"], row["link"], row["written_at"]), ("fresh", "sim library", "2026-11-02T00:00:00Z"))
            self.assertEqual(row["signal"], f"running {entries[lib_id]['running_days']} days")
        status = {r["idea_id"]: r["status"] for r in self.rows["Ideas"]}
        self.assertEqual(status, {"ID-0001": "planned", "ID-0002": "tested", "ID-0003": "tested", "ID-0004": "planned",
                                  "ID-0005": "new", "ID-0006": "new", "ID-0007": "new", "ID-0008": "new", "ID-0009": "new",
                                  "ID-0010": "new"})
        keys = {r[c] for tab, rows in self.rows.items() for r in rows for c in (fixtures.KEY_COLUMN[tab],)}
        for idea in self.rows["Ideas"]:
            cited = fixtures.ids_in(idea["sources"])
            self.assertTrue(cited and all(k in keys for k in cited), idea["idea_id"])

    def test_tests_checks_and_decisions(self):
        tests = by_key(self.rows["Tests"], "test_id")
        self.assertEqual(sorted(tests), ["T-0001", "T-0002", "T-0003", "T-0004"] + [f"T-{n:04d}" for n in range(101, 107)])
        with open(work("V01") / "history.csv", newline="") as handle:
            history = list(csv.DictReader(handle))
        results = by_key(self.rows["Results"], "result_id")
        for i, row in enumerate(history):
            tid = f"T-{101 + i:04d}"
            self.assertEqual((tests[tid]["legacy_ref"], tests[tid]["status"], tests[tid]["platform_id"]),
                             (f"history.csv:{i + 2}", "closed", ""))
            result = results[f"R-{101 + i:04d}"]
            self.assertEqual((result["k"], result["n"], result["call"]), (row["conversions"], row["clicks"], "legacy"))
        self.assertEqual((results["R-0001"]["test_id"], results["R-0001"]["call"]), ("T-0002", "stop"))
        self.assertEqual((results["R-0002"]["test_id"], results["R-0002"]["call"]), ("T-0003", "stop"))
        for tid in ("T-0001", "T-0002", "T-0003", "T-0004"):
            test = tests[tid]
            checks = [c for c in self.rows["Checks"] if c["test_id"] == tid]
            self.assertEqual(sorted(c["role"] for c in checks), ["build-checker", "critic", "plan-checker"])
            for c in checks:
                self.assertEqual((c["verdict"], c["written_by"]), ("pass", c["role"]))
                self.assertLessEqual(c["written_at"], test["launched_at"])
                self.assertEqual(c["item_id"], "" if c["role"] == "plan-checker" else test["item_id"])
            launches = [d for d in self.rows["Decisions"] if d["test_id"] == tid and d["kind"] == "launch"]
            self.assertEqual([d["written_at"] for d in launches], [test["launched_at"]])
            camp = self.world.campaigns[test["platform_id"]]
            self.assertEqual((camp["item"], camp["launched_at"]), (test["item_id"], test["launched_at"]))
        for tid in ("T-0002", "T-0003"):
            pauses = [d for d in self.rows["Decisions"] if d["test_id"] == tid and d["kind"] == "pause"]
            self.assertEqual([d["written_at"] for d in pauses], ["2026-11-05T00:00:00Z"])
            cid = tests[tid]["platform_id"]
            self.assertEqual(self.world.status_at(cid, parse_time("2026-11-05T00:00:00Z")), "paused")
            self.assertEqual(self.world.status_at(cid, parse_time("2026-11-04T23:00:00Z")), "live")
        self.assertEqual({c: self.world.campaigns[c]["status"] for c in self.world.campaigns},
                         {"cp_0001": "live", "cp_0002": "paused", "cp_0003": "paused", "cp_0004": "live"})

    def test_map_lessons_reviews_log(self):
        status = {r["type"]: r["status"] for r in self.rows["Map"]}
        self.assertEqual(len(status), 9)
        self.assertEqual(status.pop("hook=question|visual=app-screen"), "best")
        self.assertEqual(status.pop("hook=claim|visual=app-screen"), "tested")
        self.assertEqual(status.pop("hook=question|visual=hand-replay"), "tested")
        self.assertEqual(set(status.values()), {"untested"})
        lessons = by_key(self.rows["Lessons"], "lesson_id")
        self.assertEqual({k: (v["status"], v["evidence"], v["winner"], v["loser"]) for k, v in lessons.items()}, {
            "L-0001": ("lean", "T-0002", "hook=question|visual=app-screen", "hook=claim|visual=app-screen"),
            "L-0002": ("lean", "T-0003", "hook=question|visual=app-screen", "hook=question|visual=hand-replay")})
        self.assertEqual([(r["role"], r["written_at"]) for r in self.rows["Reviews"]], [
            ("strategist", "2026-11-02T00:00:00Z"), ("auditor", "2026-11-02T00:00:00Z"),
            ("meta-analyst", "2026-11-07T12:00:00Z")])
        times = [r["platform_time"] for r in self.rows["Log"]]
        self.assertEqual(times, [iso(parse_time("2026-11-02T00:00:00Z") + i * 12 * fixtures.HOUR) for i in range(12)])


class Deltas(unittest.TestCase):
    def test_money_and_spending_deltas(self):
        world, rows = World.load(hidden("V02")), book("V02")
        charter = {r["field"]: r["value"] for r in rows["Charter"]}
        self.assertEqual((world.balance(), world.money_received(), charter["money_total"], charter["speed"]),
                         (9.0, 315.0, "315", "as fast as checked items can be read, from $80 a day committed"))
        tests = by_key(rows["Tests"], "test_id")
        self.assertEqual((tests["T-0009"]["status"], tests["T-0010"]["status"]), ("plan-checked", "planned"))
        self.assertTrue(any(c["test_id"] == "T-0009" and c["role"] == "plan-checker" and c["verdict"] == "pass"
                            for c in rows["Checks"]))
        self.assertEqual(committed(book("V03")), (30.0, 0.0))
        total, share = committed(book("V11"))
        self.assertEqual((total, round(share, 2)), (100.0, 0.05))
        v11 = World.load(hidden("V11"))
        self.assertEqual(v11.current_budget("cp_0001"), 95)
        tail = [h for h in v11.hourly("cp_0001") if h["hour"] >= "2026-11-07T12:00:00Z"]
        self.assertEqual((sum(h["clicks"] for h in tail), sum(h["conversions"] for h in tail)), (150, 9))

    def test_removal_takes_what_hangs_on_a_test(self):
        rows, world = book("V03"), World.load(hidden("V03"))
        self.assertNotIn("T-0004", {t["test_id"] for t in rows["Tests"]})
        for tab in ("Checks", "Results", "Decisions"):
            self.assertFalse([r for r in rows[tab] if r["test_id"] == "T-0004"], tab)
        self.assertNotIn("cp_0004", world.campaigns)
        self.assertNotIn("it_0004", world.items)
        self.assertEqual(by_key(rows["Ideas"], "idea_id")["ID-0004"]["status"], "new")
        rows13, world13 = book("V13"), World.load(hidden("V13"))
        self.assertNotIn("T-0002", {t["test_id"] for t in rows13["Tests"]})
        self.assertNotIn("R-0001", {r["result_id"] for r in rows13["Results"]})
        self.assertNotIn("cp_0002", world13.campaigns)

    def test_plans_items_and_checks(self):
        tests = by_key(book("V04")["Tests"], "test_id")
        t = tests["T-0011"]
        self.assertEqual((t["status"], t["type"], t["idea_id"], t["varies"], t["held_constant"], t["daily_budget"], t["days"],
                          t["read_at"]), ("planned", "hook=story|visual=coach-face", "ID-0009",
                                          "hook question->story; visual app-screen->coach-face", "offer=free-trial", "15",
                                          "4", "2026-11-12T00:00:00Z"))
        self.assertEqual(t["hypothesis"], "A story hook converts better than a question hook")
        world = World.load(hidden("V05"))
        item = world.items["it_0012"]
        self.assertEqual((item["requested"]["offer"], item["attrs"]["offer"]), ("free-trial", "discount"))
        self.assertEqual([f["target"] for f in world.faults()], ["it_0012"])
        self.assertFalse([c for c in world.campaigns.values() if c["item"] == "it_0012"])
        self.assertEqual(by_key(book("V05")["Tests"], "test_id")["T-0012"]["status"], "built")
        item = World.load(hidden("V06")).items["it_0013"]
        self.assertEqual((item["quality"], item["attrs"], item["text"]),
                         ("generic", item["requested"], "Want to get better at poker? Try the best poker app free for 7 days."))
        v07 = World.load(hidden("V07"))
        self.assertEqual((v07.campaigns["cp_0014"]["status"], v07.current_budget("cp_0014")), ("live", 15))
        self.assertEqual(by_key(book("V08")["Tests"], "test_id")["T-0004"]["read_at"], "2026-11-08T00:00:00Z")

    def test_reruns_and_lessons(self):
        for sid, conversions in (("V09", 76), ("V10", 42)):
            rows, world = book(sid), World.load(hidden(sid))
            self.assertEqual(by_key(rows["Results"], "result_id")["R-0002"]["call"], "act")
            lessons = by_key(rows["Lessons"], "lesson_id")
            self.assertNotIn("L-0002", lessons)
            self.assertEqual((lessons["L-0003"]["status"], lessons["L-0003"]["evidence"]), ("lean", "T-0003"))
            t16 = by_key(rows["Tests"], "test_id")["T-0016"]
            self.assertEqual((t16["lane"], t16["rerun_of"], t16["lesson_id"], t16["item_id"], t16["platform_id"]),
                             ("develop", "T-0003", "L-0003", "it_0003", "cp_0016"))
            per_day = {}
            for h in world.hourly("cp_0003"):
                day = per_day.setdefault(h["hour"][:10], [0, 0])
                day[0] += h["clicks"]
                day[1] += h["conversions"]
            self.assertEqual(sorted(per_day.values()), [[150, 12]] * 3)
            self.assertEqual(sum(h["conversions"] for h in world.hourly("cp_0016")), conversions)
        lessons = by_key(book("V13")["Lessons"], "lesson_id")
        self.assertEqual((lessons["L-0001"]["status"], lessons["L-0001"]["evidence"], lessons["L-0001"]["recheck_at"]),
                         ("strong", "T-0102, T-0107", "2026-11-06T00:00:00Z"))
        with open(work("V13") / "history.csv", newline="") as handle:
            self.assertEqual(len(list(csv.reader(handle))), 8)
        self.assertEqual(by_key(book("V13")["Tests"], "test_id")["T-0107"]["legacy_ref"], "history.csv:8")
        rows = book("V16")
        self.assertEqual(by_key(rows["Ideas"], "idea_id")["ID-0008"]["status"], "tested")
        self.assertEqual(by_key(rows["Lessons"], "lesson_id")["L-0005"]["status"], "lean")
        v16 = World.load(hidden("V16"))
        self.assertEqual(v16.status_at("cp_0007", parse_time("2026-11-05T00:00:00Z")), "paused")

    def test_faults(self):
        world = World.load(hidden("V14"))
        self.assertEqual([(f["kind"], f["target"], f["factor"]) for f in world.faults()], [("tracking", "cp_0004", 0.3)])
        world = World.load(hidden("V15"))
        self.assertEqual([(f["kind"], f["target"], f["target_share"]) for f in world.faults()], [("delivery", "cp_0004", 0.12)])
        day5 = [h for h in world.hourly("cp_0004") if h["hour"].startswith("2026-11-07")]
        self.assertTrue(len(day5) == 24 and all(h["target_share"] == 0.12 for h in day5))
        self.assertEqual((sum(h["clicks"] for h in day5), sum(h["conversions"] for h in day5)), (140, 2))
        self.assertTrue(all(h["target_share"] == 0.85 for h in world.hourly("cp_0004") if h["hour"] < "2026-11-07"))
        for sid in fixtures.SCENARIO_IDS:
            if sid not in ("V05", "V14", "V15", "V28"):
                self.assertEqual(World.load(hidden(sid)).faults(), [], sid)

    def test_later_now_and_reviews(self):
        world, rows = World.load(hidden("V18")), book("V18")
        self.assertEqual((iso(world.now), world.balance()), ("2026-11-10T00:00:00Z", 102.0))
        self.assertEqual({c: r["status"] for c, r in world.campaigns.items()},
                         {"cp_0001": "live", "cp_0002": "paused", "cp_0003": "paused", "cp_0004": "paused",
                          "cp_0005": "paused", "cp_0006": "paused"})
        last = {}
        for r in rows["Reviews"]:
            last[r["role"]] = max(last.get(r["role"], ""), r["written_at"])
        self.assertEqual(last, {"strategist": "2026-11-02T00:00:00Z", "auditor": "2026-11-02T00:00:00Z",
                                "meta-analyst": "2026-11-09T12:00:00Z"})
        self.assertEqual({t["test_id"]: t["status"] for t in rows["Tests"] if t["test_id"] in ("T-0004", "T-0005", "T-0006")},
                         {"T-0004": "closed", "T-0005": "closed", "T-0006": "closed"})
        rows = book("V21")
        self.assertEqual(max(r["written_at"] for r in rows["Reviews"] if r["role"] == "meta-analyst"), "2026-11-07T00:00:00Z")
        status = {r["type"]: r["status"] for r in rows["Map"]}
        self.assertEqual((status.pop("hook=question|visual=app-screen"), status.pop("hook=question|visual=hand-replay")),
                         ("best", "tested"))
        self.assertEqual(set(status.values()), {"untested"})
        self.assertIn("hook=question|visual=coach-face", status)
        tests = by_key(rows["Tests"], "test_id")
        self.assertEqual(sorted(tests), ["T-0001"] + [f"T-{n:04d}" for n in range(30, 36)])
        for i, n in enumerate(range(30, 36)):
            self.assertEqual(tests[f"T-{n:04d}"]["legacy_ref"], f"history.csv:{i + 2}")
            self.assertTrue(tests[f"T-{n:04d}"]["type"].startswith("hook=question|"))
        with open(work("V21") / "history.csv", newline="") as handle:
            hist = list(csv.DictReader(handle))
        self.assertEqual([int(r["conversions"]) for r in hist], [18, 21, 19, 20, 18, 21])
        self.assertTrue(all(r["hook"] == "question" and r["clicks"] == "300" for r in hist))

    def test_setup_and_adoption_folders(self):
        world = World.load(hidden("V19"))
        self.assertEqual((iso(world.now), world.campaigns, world.balance()), ("2026-11-02T00:00:00Z", {}, 600.0))
        self.assertEqual(sorted(p.name for p in work("V19").iterdir()), ["README.md", "bin", "history.csv", "workbook"])
        legacy = work("V20") / "legacy"
        self.assertEqual(sorted(p.name for p in legacy.iterdir()),
                         ["Angles.csv", "Decisions.csv", "Hypotheses.csv", "Learnings.csv", "Live results.csv"])
        with open(legacy / "Live results.csv", newline="") as handle:
            live = list(csv.DictReader(handle))
        self.assertEqual([(r["campaign"], r["status"], r["cap"]) for r in live],
                         [("cp_0001", "Live", "30"), ("cp_0002", "Paused", "15"), ("cp_0003", "Paused", "15"),
                          ("cp_0004", "Live", "15")])
        world = World.load(hidden("V20"))
        for row in live:
            hours = world.hourly(row["campaign"])
            self.assertEqual((str(sum(h["clicks"] for h in hours)), str(sum(h["conversions"] for h in hours))),
                             (row["clicks"], row["conversions"]))
        with open(legacy / "Learnings.csv", newline="") as handle:
            learnings = list(csv.DictReader(handle))
        self.assertEqual([r["kind"] for r in learnings], ["Learning, early"] * 3)
        hashes = json.loads((hidden("V20") / "initial_files.json").read_text())
        for name, digest in hashes.items():
            self.assertEqual(hashlib.sha256((work("V20") / name).read_bytes()).hexdigest(), digest)
        self.assertIn("legacy/Live results.csv", hashes)

    def test_sourcing_deltas(self):
        ideas = by_key(book("V23")["Ideas"], "idea_id")
        self.assertEqual((ideas["ID-0013"]["sources"], ideas["ID-0013"]["status"]), ("", "new"))
        self.assertFalse({"ID-0005", "ID-0006", "ID-0007", "ID-0008", "ID-0009"} & set(ideas))
        rows = book("V24")
        self.assertEqual({r["written_at"] for r in rows["Library"]}, {"2026-09-28T00:00:00Z"})
        self.assertEqual(sorted(i["idea_id"] for i in rows["Ideas"] if i["status"] == "new"), ["ID-0008", "ID-0009"])
        ideas = by_key(book("V12")["Ideas"], "idea_id")
        self.assertEqual((ideas["ID-0012"]["source"], ideas["ID-0012"]["status"], ideas["ID-0012"]["sources"]),
                         ("scout", "new", "LB-0001"))
        ideas = by_key(book("V01")["Ideas"], "idea_id")
        self.assertEqual(ideas["ID-0010"]["description"],
                         "Optimize for installs instead of conversions; installs cost about a fifth as much")


class RoundTwo(unittest.TestCase):
    """PLAN.md 13: the readable Tests rows, Library coding, the Overview, reports, the W5 base and the role fixtures."""

    def test_tests_rows_carry_their_whole_life(self):
        rows, world = book("V01"), World.load(hidden("V01"))
        tests, checks = by_key(rows["Tests"], "test_id"), rows["Checks"]
        t2 = tests["T-0002"]
        self.assertTrue(t2["recipe"].startswith("Made on the platform with `sim build --attrs"), t2["recipe"])
        self.assertIn(world.items["it_0002"]["text"], t2["recipe"])
        self.assertEqual(t2["coding"], world.type_of(world.items["it_0002"]["attrs"]))
        for check in (c for c in checks if c["test_id"] == "T-0002"):
            self.assertIn(f"{check['role']} {check['verdict']} ({check['check_id']})", t2["checks"])
        self.assertTrue(t2["read"].startswith("R-0001: ") and t2["read"].endswith("call stop"), t2["read"])
        pause = [d for d in rows["Decisions"] if d["test_id"] == "T-0002" and d["kind"] == "pause"][0]
        self.assertTrue(t2["decision"].startswith(f"{pause['decision_id']} pause: "), t2["decision"])
        t4 = tests["T-0004"]
        self.assertEqual((t4["read"], t4["made_from"]), ("", ""))
        self.assertIn(" launch: ", t4["decision"])
        self.assertTrue(all(not t[col] for t in rows["Tests"] if t["legacy_ref"] for col in ("recipe", "coding")))
        built = by_key(book("V05")["Tests"], "test_id")["T-0012"]
        self.assertTrue(built["recipe"] and not built["coding"], built)   # never codes a build before its check
        self.assertTrue(built["checks"].startswith("plan-checker pass (CK-"), built["checks"])

    def test_library_rows_are_coded(self):
        entries = {e["id"]: e for e in World.load(hidden("V01")).library_entries()}
        for row in book("V01")["Library"]:
            lib_id = row["source"].split()[2]
            self.assertEqual(row["coding"], "|".join(f"{k}={v}" for k, v in entries[lib_id]["_type"].items()))
        for row in book("V27")["Library"]:
            self.assertEqual(len(row["coding"].split("|")), 12, row["coding"])

    def test_overview_as_the_last_tick_left_it(self):
        rows, world = book("V08"), World.load(hidden("V08"))
        overview = {r["item"]: r for r in rows["Overview"]}
        self.assertEqual(list(overview), ["bar now", "bar at start", "money left", "speed", "live", "best known option",
                                          "strong lessons", "next"])
        last = max(r["platform_time"] for r in rows["Log"])
        self.assertEqual({(r["as_of"], r["written_at"]) for r in rows["Overview"]}, {(last, last)})
        spent = world.spend_between(None, parse_time(last))
        self.assertEqual(overview["money left"]["value"], f"${600 - spent:.2f} of $600.00")
        self.assertNotEqual(600 - spent, world.balance())               # a tick ago, not now
        self.assertIn("T-0001", overview["best known option"]["value"])
        self.assertIn("T-0004 on cp_0004 (explore, $15/day, reads 2026-11-08)", overview["live"]["value"])
        self.assertEqual(overview["strong lessons"]["value"], "none yet")
        self.assertIn("L-0001", {r["item"]: r for r in book("V13")["Overview"]}["strong lessons"]["value"])
        self.assertEqual(book("V19").get("Overview"), None)

    def test_reporting_and_the_overdue_report(self):
        base = {r["field"]: r["value"] for r in book("V01")["Charter"]}
        self.assertIn("reports/", base["reporting"])
        self.assertIn("2026-11-16", base["reporting"])
        self.assertFalse([r for r in book("V01")["Reviews"] if r["role"] == "report"])
        rows, world = book("V26"), World.load(hidden("V26"))
        charter = {r["field"]: r["value"] for r in rows["Charter"]}
        self.assertTrue(charter["reporting"].startswith("a progress report every week"))
        reports = [r for r in rows["Reviews"] if r["role"] == "report"]
        self.assertEqual([(r["review_id"], r["written_at"]) for r in reports], [("RV-0003", "2026-11-02T00:00:00Z")])
        self.assertIn("reports/2026-11-02-progress.md", reports[0]["call"])
        self.assertTrue((work("V26") / "reports" / "2026-11-02-progress.md").is_file())
        self.assertIn("reports/2026-11-02-progress.md", json.loads((hidden("V26") / "initial_files.json").read_text()))
        self.assertIn("wrote the progress report RV-0003", rows["Log"][0]["did"])
        self.assertEqual((iso(world.now), world.balance()), ("2026-11-10T00:00:00Z", 207.0))
        tests = by_key(rows["Tests"], "test_id")
        self.assertEqual((tests["T-0004"]["status"], tests["T-0005"]["status"]), ("closed", "live"))
        self.assertEqual(len(rows["Lessons"]), 2)
        self.assertEqual([r["role"] for r in rows["Reviews"]],
                         ["strategist", "auditor", "report", "meta-analyst", "strategist", "auditor", "meta-analyst"])

    def test_a_scenario_op_replaces_the_bases(self):
        item = World.load(hidden("V25")).items["it_0004"]
        self.assertIn("never lose on the river, guaranteed", item["text"])
        self.assertEqual((item["quality"], item["built_at"]), ("specific", "2026-11-04T12:00:00Z"))
        self.assertNotIn("guaranteed", World.load(hidden("V08")).items["it_0004"]["text"])

    def test_the_w5_base(self):
        world, rows = World.load(hidden("V27")), book("V27")
        self.assertEqual(world.world_id, "W5")
        names = world.attribute_names()
        self.assertEqual(len(names), 12)
        for iid in ("it_0001", "it_0002", "it_0003"):
            self.assertEqual(list(world.items[iid]["attrs"]), names)
            self.assertIsNone(world.items[iid]["made_from"])
        charter = {r["field"]: r["value"] for r in rows["Charter"]}
        self.assertTrue(all(f"{n}:" in charter["attributes"] for n in names), charter["attributes"])
        self.assertEqual(len(rows["Charter"]), 29)
        tests = by_key(rows["Tests"], "test_id")
        t6 = tests["T-0006"]
        self.assertEqual((t6["status"], t6["made_from"], t6["item_id"], t6["recipe"]), ("plan-checked", "it_0002", "", ""))
        self.assertTrue(any(c["test_id"] == "T-0006" and c["role"] == "plan-checker" and c["verdict"] == "pass"
                            for c in rows["Checks"]))
        self.assertEqual((tests["T-0005"]["item_id"], tests["T-0005"]["lane"], tests["T-0005"]["status"]),
                         ("it_0002", "exploit", "live"))
        lesson = by_key(rows["Lessons"], "lesson_id")["L-0001"]
        self.assertEqual((lesson["status"], lesson["evidence"]), ("strong", "T-0002, T-0004"))
        self.assertEqual((world.balance(), world.money_received(), world.current_budget("cp_0001")), (356.5, 800.0, 15))
        self.assertEqual(world.faults(), [])

    def test_the_music_fault(self):
        world, rows = World.load(hidden("V28")), book("V28")
        child, parent = world.items["it_0006"], world.items["it_0002"]
        self.assertEqual(child["made_from"], "it_0002")
        self.assertEqual(sorted(k for k in child["attrs"] if child["attrs"][k] != parent["attrs"][k]),
                         ["music", "presenter"])
        self.assertEqual((child["requested"]["music"], child["attrs"]["music"], child["text"]),
                         ("upbeat", "lo-fi", parent["text"]))
        self.assertEqual([(f["kind"], f["target"], f["attr"]) for f in world.faults()], [("build", "it_0006", "music")])
        t6 = by_key(rows["Tests"], "test_id")["T-0006"]
        self.assertEqual((t6["status"], t6["item_id"], t6["coding"]), ("built", "it_0006", ""))
        self.assertIn("sim build --from it_0002 --attrs '{\"presenter\": \"player\"}'", t6["recipe"])
        self.assertFalse([c for c in world.campaigns.values() if c["item"] == "it_0006"])

    def test_role_fixtures_build(self):
        for case in ("plan-checker-sound", "plan-checker-other-days", "build-checker-clean", "critic-two-well-made"):
            run_dir, h = ROOT / f"role-{case}", ROOT / "hidden" / f"role-{case}"
            meta = fixtures.build_scenario(case, run_dir, h, folder=fixtures.LAB / "roles" / case, kind="role")
            self.assertEqual((meta["kind"], meta["scenario"]), ("role", case))
            rows = fixtures.read_workbook(run_dir / "work" / "workbook")
            if case.startswith("plan-checker"):
                plan = by_key(rows["Tests"], "test_id")["T-0031"]
                self.assertEqual((plan["status"], plan["daily_budget"], plan["days"]), ("planned", "30", "5"))
                same_days = plan["comparison"] == "T-0001, on the same days"
                self.assertEqual(same_days, case == "plan-checker-sound", plan["comparison"])
            if case == "build-checker-clean":
                world = World.load(h)
                child, parent = world.items["it_0006"], world.items["it_0002"]
                self.assertEqual([k for k in child["attrs"] if child["attrs"][k] != parent["attrs"][k]], ["presenter"])
                self.assertEqual(world.faults(), [])
                recipe = by_key(rows["Tests"], "test_id")["T-0006"]["recipe"]
                for part in ("sim build --from it_0002", "Parent: it_0002", parent["text"], "keeps the built item"):
                    self.assertIn(part, recipe)
            if case == "critic-two-well-made":
                self.assertEqual(World.load(h).items["it_0032"]["quality"], "specific")


class Wrappers(unittest.TestCase):
    def test_wrappers_call_the_lab_cli_with_the_hidden_folder(self):
        bin_dir = work("V17") / "bin"
        result = subprocess.run([str(bin_dir / "sim"), "status"], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.splitlines()[0], "Now: 2026-11-08T00:00:00Z (day 6).")
        result = subprocess.run([str(bin_dir / "notify"), "--kind", "money-request", "--json", '{"amount": 300}'],
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.stdout, "Sent to the account owner.\n")
        result = subprocess.run([str(bin_dir / "gws"), "sheets", "list"], capture_output=True, text=True, timeout=60)
        self.assertEqual((result.returncode, result.stdout), (1, "gws is not available on this account.\n"))
        logged = [json.loads(line) for line in (hidden("V17") / "sim_actions.jsonl").read_text().splitlines()]
        self.assertEqual([e["argv"][0] for e in logged], ["sim", "notify", "gws"])
        self.assertEqual(len((hidden("V17") / "outbox.jsonl").read_text().splitlines()), 1)

    def test_build_world_gives_a_day_zero_folder(self):
        for wid in ("W1", "W2", "W3", "W4", "W5"):
            run_dir, h = ROOT / f"world-{wid}", ROOT / "hidden" / f"world-{wid}"
            meta = fixtures.build_world(wid, 1, run_dir, h)
            config = load_config(wid)
            self.assertEqual((meta["kind"], meta["scenario"], meta["world"], meta["seed"], meta["now"], meta["prompt"]),
                             ("world", None, wid, 1, "2026-11-02T00:00:00Z", config["setup_prompt"]))
            names = sorted(p.name for p in (run_dir / "work").iterdir())
            want = ["README.md", "bin", "workbook"] + (["history.csv"] if wid in ("W1", "W2") else [])
            self.assertEqual(names, sorted(want))
            self.assertEqual(list((run_dir / "work" / "workbook").iterdir()), [])
            self.assertEqual((run_dir / "work" / "README.md").read_text(), config["readme"])
            world = World.load(h)
            self.assertEqual(len(world.state["faults"]), len(config["faults"]))
            self.assertTrue(world.state["faults_on"])


if __name__ == "__main__":
    unittest.main()
