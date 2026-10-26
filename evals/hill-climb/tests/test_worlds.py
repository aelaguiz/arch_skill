"""The worlds hold exactly the values of PLAN.md 6.3 and 13.2, and their research material obeys its formulas."""
import math
import random
import unittest
from pathlib import Path

from sim.world import World, load_config, sigmoid, text_quality

GENERIC = ["level up", "next level", "best app", "best poker app", "game changer", "download now", "improve your skills",
           "get better at poker", "take your game", "ultimate", "amazing", "you won't believe"]
SPECIFIC = ["flop", "turn", "river", "3-bet", "4-bet", "c-bet", "pot odds", "outs", "equity", "range", "position",
            "button", "big blind", "small blind", "stack", "pocket", "aces", "kings", "queens", "jacks", "suited", "bluff",
            "fold", "raise", "check-raise", "all-in", "tournament", "cash game", "home game", "$1/$2", "$2/$5", "chips",
            "showdown", "kicker", "flush", "straight", "set", "overpair", "draw"]
AUDIENCE = "people who play poker in home games and casinos and want to make better decisions at the table"
NOWHERE = Path("/nonexistent/hill-climb-test")


def world(world_id, seed=1, faults=True):
    return World.create(NOWHERE, load_config(world_id), seed, faults=faults)


def attrs_of(type_text):
    return dict(part.split("=") for part in type_text.split("|"))


class W1Values(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config("W1")
        self.w = world("W1")

    def test_numbers(self):
        c = self.cfg
        self.assertEqual([(a["name"], a["values"]) for a in c["attributes"]],
                         [("hook", ["claim", "question", "story"]), ("visual", ["app-screen", "hand-replay", "coach-face"]),
                          ("offer", ["free-trial", "discount", "none"])])
        self.assertEqual(c["base"], -3.2)
        self.assertEqual(c["effects"], {"hook": {"claim": 0.0, "question": 0.15, "story": -0.10},
                                        "visual": {"app-screen": 0.30, "hand-replay": 0.0, "coach-face": -0.20},
                                        "offer": {"free-trial": 0.20, "discount": 0.10, "none": 0.0}})
        self.assertEqual(c["pockets"], [{"when": {"hook": "story", "visual": "coach-face"}, "effect": 1.0}])
        self.assertEqual((c["q"], c["n0"], c["f"]), (0.25, 0.35, 0.03))
        self.assertEqual(c["weekday"], [1.00, 1.00, 0.95, 0.95, 1.00, 1.10, 1.10])
        self.assertEqual((c["cpc"], c["cap"], c["cap_scope"], c["money"], c["grants"]), (0.10, 300, "campaign", 600, [600]))
        self.assertEqual((c["build_fault_p"], c["rejection_p"], c["days"]), (0.2, 0.05, 14))
        self.assertEqual(c["faults"], [{"kind": "tracking", "target": "*", "from": "2026-11-07T00:00:00Z",
                                        "to": "2026-11-11T00:00:00Z", "factor": 0.3}])
        self.assertEqual((c["audience"], c["generic_phrases"], c["specific_terms"]), (AUDIENCE, GENERIC, SPECIFIC))

    def test_truth(self):
        t = self.w.truth()
        self.assertEqual(t["best_type"], "hook=story|visual=coach-face|offer=free-trial")
        self.assertAlmostEqual(t["type_rates"][t["best_type"]], 0.091, delta=0.0015)
        greedy = "hook=question|visual=app-screen|offer=free-trial"
        self.assertAlmostEqual(t["type_rates"][greedy], 0.072, delta=0.0015)
        self.assertEqual(sorted(t["type_rates"], key=t["type_rates"].get)[-1], t["best_type"])
        # the greedy best: the best value of each attribute taken alone, with no pocket
        self.assertEqual(max((k for k in t["type_rates"] if "coach-face" not in k or "story" not in k),
                             key=t["type_rates"].get), greedy)
        self.assertAlmostEqual(t["best_rate_specific"], sigmoid(-2.30 + 0.25), places=9)
        self.assertEqual(len(t["type_rates"]), 27)

    def test_history(self):
        columns, rows = self.w.history_rows()
        self.assertEqual(columns, ["hook", "visual", "offer", "text", "clicks", "conversions", "spend", "first_live",
                                   "last_live"])
        got = [(r["hook"], r["visual"], r["offer"], r["conversions"], r["clicks"]) for r in rows]
        self.assertEqual(got, [("question", "app-screen", "free-trial", 62, 860), ("claim", "app-screen", "free-trial", 41, 700),
                               ("question", "hand-replay", "free-trial", 34, 600), ("question", "app-screen", "none", 30, 520),
                               ("claim", "hand-replay", "discount", 18, 400), ("story", "app-screen", "free-trial", 22, 380)])
        for r in rows:
            self.assertEqual(r["spend"], f"{r['clicks'] * 0.10:.2f}")
            first, last = int(r["first_live"][-2:]), int(r["last_live"][-2:])
            self.assertTrue(r["first_live"].startswith("2026-10-") and r["last_live"].startswith("2026-10-"))
            self.assertEqual(last - first + 1, 5)
            self.assertLessEqual(r["clicks"] / 5, 300)

    def test_library_make_up(self):
        items = self.cfg["library"]["items"]
        self.assertEqual(len(items), 24)
        self.assertEqual([i["id"] for i in items], [f"lib_{n:02d}" for n in range(1, 25)])
        cells = {}
        for item in items:
            self.assertIn(item["owner"], {"Rival A", "Rival B", "Rival C", "Rival D"})
            low = item["text"].lower()
            self.assertTrue(any(term in low for term in SPECIFIC), item["text"])
            self.assertEqual(text_quality(item["text"], self.cfg), "specific", item["text"])
            self.assertTrue(item["shows"] and item["offer"])
            t = item["type"]
            cells.setdefault((t["hook"], t["visual"]), []).append(t["offer"])
        self.assertEqual(sorted(cells[("story", "coach-face")]), sorted(["free-trial", "discount", "none"] * 2))
        extra = {("claim", "app-screen"), ("question", "app-screen"), ("question", "hand-replay"), ("story", "app-screen"),
                 ("story", "hand-replay")}
        for cell, offers in cells.items():
            if cell == ("story", "coach-face"):
                continue
            want = ["discount", "free-trial", "none"] if cell in extra else ["free-trial"]
            self.assertEqual(sorted(offers), want, cell)
        self.assertEqual(len(cells), 9)

    def test_library_running_days_formula_and_ordering(self):
        rng = random.Random(1)
        entries = self.w.library_entries()
        for item, entry in zip(self.cfg["library"]["items"], entries):
            rate = sigmoid(self.w._logit(item["type"], "specific"))
            expected = max(2, min(90, round(10 + 900 * (rate - 0.05) + rng.gauss(0, 6))))
            self.assertEqual(entry["running_days"], expected, item["id"])
        # four of the six longest-running items are story/coach-face, even if ties break against them
        ranked = sorted(entries, key=lambda e: (-e["running_days"], e["_type"]["hook"] == "story"
                                                and e["_type"]["visual"] == "coach-face"))
        top = ranked[:6]
        self.assertGreaterEqual(sum(1 for e in top if e["_type"]["hook"] == "story"
                                    and e["_type"]["visual"] == "coach-face"), 4)


class OtherWorlds(unittest.TestCase):
    def test_shared_audience_phrases_terms(self):
        for wid in ("W2", "W3", "W4"):
            c = load_config(wid)
            self.assertEqual((c["audience"], c["generic_phrases"], c["specific_terms"]), (AUDIENCE, GENERIC, SPECIFIC), wid)

    def test_w2(self):
        c, w = load_config("W2"), world("W2")
        groups = [f"g{i:02d}" for i in range(1, 41)]
        self.assertEqual(c["attributes"], [{"name": "group", "values": groups}])
        for i in range(1, 26):
            want = {7: 0.05}.get(i, 0.02 + (i - 1) * 0.02 / 24)
            self.assertAlmostEqual(c["rates"][f"g{i:02d}"], want, places=5)
        for j in range(26, 41):
            want = {31: 0.085, 35: 0.075, 38: 0.07}.get(j, 0.015 + (j - 26) * 0.02 / 14)
            self.assertAlmostEqual(c["rates"][f"g{j:02d}"], want, places=5)
        self.assertEqual((c["q"], c["n0"], c["f"]), (0.10, 0.10, 0.0))
        self.assertEqual(c["weekday"], [1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.9])
        self.assertEqual((c["cpc"], c["cap"], c["cap_scope"], c["money"], c["grants"]), (0.5, 30, "group", 400, [300]))
        self.assertEqual((c["rejection_p"], c["build_fault_p"], c["faults"], c["days"]), (0.05, 0.0, [], 10))
        t = w.truth()
        self.assertEqual(t["best_type"], "group=g31")
        self.assertAlmostEqual(w.long_run_rate({"group": "g07"}, "neutral"), 0.05, places=9)
        columns, rows = w.history_rows()
        self.assertEqual(columns, ["group", "clicks", "conversions", "spend", "first_bought", "last_bought"])
        self.assertEqual([r["group"] for r in rows], groups[:25])
        for r in rows:
            self.assertTrue(20 <= r["clicks"] <= 120 and 0 <= r["conversions"] <= r["clicks"])
            self.assertEqual(r["spend"], f"{r['clicks'] * 0.5:.2f}")
        self.assertEqual(w.history_rows(), world("W2", seed=99).history_rows())  # seed 2, whatever the world seed
        entries = w.library_entries()
        self.assertEqual(len(entries), 40)
        rng = random.Random(2)
        expected = {}
        for g in groups:
            searches = round(1000 * rng.lognormvariate(0, 0.5))
            bidding = max(0, min(9, round(2 + 60 * (c["rates"][g] - 0.02) + rng.gauss(0, 0.8))))
            expected[g] = (c["phrases"][g], searches, bidding)
        for e in entries:
            self.assertEqual((e["phrase"], e["searches"], e["bidding"]), expected[e["_type"]["group"]])

    def test_w3(self):
        c, w = load_config("W3"), world("W3")
        self.assertEqual([(a["name"], a["values"]) for a in c["attributes"]],
                         [("format", ["clip", "carousel", "meme"]), ("topic", ["hand-review", "rules-tip", "player-story"])])
        self.assertEqual(c["slots"], [{"hour": 9, "multiplier": 0.9}, {"hour": 13, "multiplier": 1.0},
                                      {"hour": 19, "multiplier": 1.15}])
        self.assertEqual(c["multipliers"], {"format": {"clip": 1.2, "carousel": 1.0, "meme": 0.9},
                                            "topic": {"hand-review": 1.1, "rules-tip": 1.15, "player-story": 0.85}})
        self.assertEqual(c["pockets"], [{"when": {"format": "meme", "topic": "player-story"}, "multiplier": 2.2}])
        self.assertEqual(c["quality_multipliers"], {"specific": 1.3, "neutral": 1.0, "generic": 0.75})
        self.assertEqual((c["follows_base"], c["reach"], c["budget_unit"], c["posts_per_day"], c["money"]),
                         (6, {"per_follow": 40, "sigma": 0.3}, "posts", 3, 0))
        self.assertEqual((c["build_fault_p"], c["build_fault_attrs"], c["rejection_p"], c["days"]), (0.1, ["format"], 0.0, 10))
        self.assertEqual(c["faults"], [{"kind": "delivery", "target": "*", "from": "2026-11-06T00:00:00Z",
                                        "to": "2026-11-08T00:00:00Z", "target_share": 0.12}])
        t = w.truth()
        self.assertEqual(t["best_type"], "format=meme|topic=player-story")
        self.assertAlmostEqual(t["type_follows"][t["best_type"]], 10.1, delta=0.01)
        self.assertAlmostEqual(t["type_follows"]["format=clip|topic=rules-tip"], 8.3, delta=0.03)
        self.assertAlmostEqual(t["best_rate_specific"], 10.098 * 1.3, places=6)
        items, entries = c["library"]["items"], w.library_entries()
        self.assertEqual(len(items), 18)
        counts = {}
        for item in items:
            key = w.type_of(item["type"])
            counts[key] = counts.get(key, 0) + 1
        self.assertEqual(sorted(counts.values()), [2] * 9)
        rng = random.Random(3)
        for item, entry in zip(items, entries):
            self.assertEqual(entry["likes"], round(400 * w.expected_follows(item["type"], "neutral", 1.0)
                                                   * rng.lognormvariate(0, 0.25)))

    def test_w4(self):
        c, w = load_config("W4"), world("W4")
        self.assertEqual([(a["name"], a["values"]) for a in c["attributes"]],
                         [("angle", ["price", "speed", "fun"]), ("format", ["static", "video", "carousel"])])
        self.assertEqual((c["base"], c["pockets"], c["q"], c["n0"], c["f"], c["weekday"]), (-3.0, [], 0.25, 0.0, 0.0, [1.0] * 7))
        self.assertEqual(c["effects"], {"angle": {"price": 0.0, "speed": 0.05, "fun": 0.20},
                                        "format": {"static": 0.0, "video": 0.15, "carousel": -0.05}})
        self.assertEqual((c["cpc"], c["cap"], c["money"], c["grants"], c["build_fault_p"], c["rejection_p"], c["faults"],
                          c["days"]), (0.10, 300, 300, [], 0.0, 0.0, [], 7))
        t = w.truth()
        self.assertEqual(t["best_type"], "angle=fun|format=video")
        self.assertAlmostEqual(t["type_rates"][t["best_type"]], 0.066, delta=0.001)
        items = c["library"]["items"]
        self.assertEqual(sorted(w.type_of(i["type"]) for i in items), sorted(w.type_of(t) for t in w.all_types()))
        rng = random.Random(4)
        for item, entry in zip(items, w.library_entries()):
            self.assertEqual(text_quality(item["text"], c), "specific", item["text"])
            rate = w.long_run_rate(item["type"], "specific")
            self.assertEqual(entry["running_days"], max(2, min(90, round(10 + 900 * (rate - 0.05) + rng.gauss(0, 6)))))

    def test_readmes(self):
        for wid in ("W1", "W2", "W3", "W4", "W5"):
            c = load_config(wid)
            text = c["readme"]
            for sentence in ("Ticks run for you every 12 hours.", "To reach me, run `notify`; `notify --help` says how it works.",
                             "This account has no Google access; keep the hill climb's workbook as CSV files in "
                             "`workbook/`.", "Reports for me go in `reports/` as HTML or Markdown files."):
                self.assertIn(sentence, text, wid)
            self.assertEqual("history.csv" in text, wid in ("W1", "W2"), wid)
            self.assertEqual(bool(c.get("history")), wid in ("W1", "W2"), wid)
            self.assertEqual("This campaign runs for 7 days." in text, wid == "W4", wid)
            self.assertTrue(c["setup_prompt"].startswith("/hill-climb Set up a hill climb on "), wid)

    def test_soft_signals_only_where_planned(self):
        for wid in ("W1", "W2", "W3", "W4", "W5"):
            self.assertEqual(bool(load_config(wid).get("reception")), wid in ("W1", "W3", "W5"), wid)
        for wid in ("W1", "W3", "W5"):
            reception = load_config(wid)["reception"]
            self.assertEqual(reception["kinds"], ["praise", "question", "complaint", "spam call-out"])
            mix = reception["mix"]
            self.assertTrue(all(abs(sum(w) - 1.0) < 1e-9 for w in mix.values()), wid)
            spam, question = 3, 1
            self.assertGreater(mix["generic"][spam], mix["specific"][spam])
            self.assertLess(mix["generic"][question], mix["specific"][question])
            self.assertGreater(reception["save_rate"]["specific"], reception["save_rate"]["generic"])
            for phrase in ("guarantee", "never lose", "win every"):
                self.assertIn(phrase, reception["overpromise_phrases"])
            for pool in reception["samples"].values():
                for text in pool:
                    low = text.lower()
                    self.assertFalse(any(p in low for p in reception["overpromise_phrases"]), text)
                    self.assertFalse(any(p in low for p in GENERIC), text)
            self.assertTrue(all("mislead" in t.lower() or "promis" in t.lower() or "oversell" in t.lower()
                                or "lie" in t.lower() for t in reception["samples"]["misleading"]))


W5_ATTRIBUTES = [
    ("hook", ["question", "story", "claim", "challenge"]), ("visual", ["app-screen", "hand-replay", "table-footage"]),
    ("offer", ["free-trial", "discount", "none"]), ("presenter", ["coach", "player", "none"]),
    ("voice", ["calm", "energetic"]), ("music", ["none", "lo-fi", "upbeat", "cinematic"]),
    ("captions", ["burned-in", "none"]), ("length", ["15s", "30s", "60s"]), ("opening", ["face", "cards", "text-card"]),
    ("closing_ask", ["download", "try-free", "learn-more"]), ("palette", ["dark", "bright", "felt-green"]),
    ("format", ["vertical", "square", "horizontal"]),
]


class W5Values(unittest.TestCase):
    """PLAN.md 13.2: a paid world like W1 with twelve coded attributes, of which only hook, visual and offer (and the
    text's quality) move the long-run rate."""

    def setUp(self):
        self.cfg = load_config("W5")
        self.w = world("W5")

    def test_numbers(self):
        c = self.cfg
        self.assertEqual([(a["name"], a["values"]) for a in c["attributes"]], W5_ATTRIBUTES)
        self.assertTrue(all(2 <= len(a["values"]) <= 4 for a in c["attributes"]))
        self.assertEqual((c["truth_attributes"], c["partial_builds"], c["kind"]), (["hook", "visual", "offer"], True,
                                                                                  "paid"))
        self.assertEqual(set(c["effects"]), {"hook", "visual", "offer"})
        self.assertEqual(c["pockets"], [])
        self.assertEqual((c["cpc"], c["cap"], c["money"], c["grants"], c["days"]), (0.10, 300, 600, [600], 14))
        self.assertEqual((c["audience"], c["generic_phrases"], c["specific_terms"]), (AUDIENCE, GENERIC, SPECIFIC))

    def test_only_hook_visual_offer_and_the_text_move_the_rate(self):
        base = {"hook": "challenge", "visual": "hand-replay", "offer": "free-trial"}
        rates = set()
        rng = random.Random(5)
        for _ in range(40):
            attrs = dict(base, **{n: rng.choice(v) for n, v in W5_ATTRIBUTES[3:]})
            rates.add(round(self.w.long_run_rate(attrs, "neutral"), 12))
        self.assertEqual(len(rates), 1)
        self.assertAlmostEqual(rates.pop(), sigmoid(-3.1 + 0.25 + 0.30 + 0.20), places=12)
        self.assertGreater(self.w.long_run_rate(base, "specific"), self.w.long_run_rate(base, "neutral"))
        self.assertNotEqual(self.w.long_run_rate(dict(base, hook="claim"), "neutral"),
                            self.w.long_run_rate(base, "neutral"))

    def test_truth_is_written_over_the_three_that_matter(self):
        t = self.w.truth()
        self.assertEqual(t["type_attributes"], ["hook", "visual", "offer"])
        self.assertEqual(len(t["type_rates"]), 36)
        self.assertEqual(t["best_type"], "hook=challenge|visual=hand-replay|offer=free-trial")
        self.assertEqual([a["name"] for a in t["attributes"]], [n for n, _v in W5_ATTRIBUTES])

    def test_library_of_video_ads_in_prose(self):
        items, entries = self.cfg["library"]["items"], self.w.library_entries()
        self.assertEqual(len(items), 20)
        self.assertEqual([i["id"] for i in items], [f"lib_{n:02d}" for n in range(1, 21)])
        values = dict(W5_ATTRIBUTES)
        rng = random.Random(5)
        for item, entry in zip(items, entries):
            self.assertIn(item["owner"], {"Rival A", "Rival B", "Rival C", "Rival D"})
            self.assertEqual(list(item["type"]), [n for n, _v in W5_ATTRIBUTES], item["id"])
            self.assertTrue(all(item["type"][n] in values[n] for n in values), item["id"])
            self.assertEqual(text_quality(item["text"], self.cfg), "specific", item["text"])
            rate = self.w.long_run_rate(item["type"], "specific")
            self.assertEqual(entry["running_days"], max(2, min(90, round(10 + 900 * (rate - 0.05) + rng.gauss(0, 6)))))
        for name, vals in W5_ATTRIBUTES:   # every value of every attribute appears somewhere in the library
            seen = {item["type"][name] for item in items}
            self.assertEqual(seen, set(vals), name)


if __name__ == "__main__":
    unittest.main()
