"""Layer 1: the Thompson baseline (PLAN.md 6.9). It runs one tick on every world (a full run of W1 takes about 14 s,
so the horizons are left to run_backtest.py); the sampling and budget rules are tested directly."""
import importlib.util
import json
import random
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from baselines import thompson


def have(module):
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


HAVE_SIM = have("sim.world") and have("fixtures")


class Rules(unittest.TestCase):
    def test_seed_is_1000_plus_world_seed(self):
        mine, theirs = thompson.make_rng(2), random.Random(1002)
        self.assertEqual([mine.random() for _ in range(5)], [theirs.random() for _ in range(5)])

    def test_daily_budget_is_two_thirds_of_the_ticks_money_clamped(self):
        self.assertAlmostEqual(thompson.tick_daily_budget(300, 14), round(300 / 14 * 2 / 3, 2))
        self.assertEqual(thompson.tick_daily_budget(10, 10), 5.0)
        self.assertEqual(thompson.tick_daily_budget(3000, 2), 100.0)
        self.assertEqual(thompson.tick_daily_budget(400, 4, cap_budget=15.0), 15.0)   # W2: 30 clicks x $0.50

    def test_top_three(self):
        samples = {"a": 0.2, "b": 0.9, "c": 0.5, "d": 0.5, "e": 0.1}
        self.assertEqual(thompson.top_arms(samples), ["b", "c", "d"])
        self.assertEqual(thompson.top_arms(samples, 1), ["b"])

    def test_posteriors(self):
        arms = ["x", "y"]
        stats = {"x": (100, 7)}
        got = thompson.sample_paid(random.Random(5), arms, stats)
        rng = random.Random(5)
        self.assertEqual(got, {"x": rng.betavariate(8, 94), "y": rng.betavariate(1, 1)})
        got = thompson.sample_posts(random.Random(5), arms, {"y": (12, 2.05)})
        rng = random.Random(5)
        self.assertEqual(got, {"x": rng.gammavariate(1, 1.0), "y": rng.gammavariate(13, 1 / 3.05)})

    def test_free_slots_in_the_next_12_hours(self):
        def at(hour, day=2):
            return datetime(2026, 11, day, hour, tzinfo=timezone.utc)
        self.assertEqual(thompson.free_slots(at(0), []), [at(9)])
        self.assertEqual(thompson.free_slots(at(12), []), [at(13), at(19)])
        self.assertEqual(thompson.free_slots(at(12), [at(13)]), [at(19)])
        self.assertEqual(thompson.free_slots(at(20), []), [])          # 09:00 is 13 hours away
        self.assertEqual(thompson.free_slots(at(0, 3), []), [at(9, 3)])


@unittest.skipUnless(HAVE_SIM, "needs sim/ and fixtures.py from the simulator builder")
class RunsEveryWorld(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def run_world(self, world, seed=1, ticks=1, name=None):
        result = thompson.run(world, seed, root=self.root / (name or f"{world}-{seed}"), max_ticks=ticks)
        outbox = self.root / (name or f"{world}-{seed}") / "hidden" / "outbox.jsonl"
        self.assertEqual(outbox.read_text() if outbox.exists() else "", "", "the baseline asks for no money")
        return result

    def test_every_world(self):
        for world in ("W1", "W2", "W3", "W4"):
            with self.subTest(world=world):
                result = self.run_world(world)
                self.assertEqual(result["ticks"], 1)
                self.assertEqual(result["horizon_ticks"], {"W1": 28, "W2": 20, "W3": 20, "W4": 14}[world])
                self.assertGreater(result["launches"], 0)
                metric = "follows_captured" if world == "W3" else "conversions_captured"
                self.assertGreaterEqual(result[metric], 0.0)
                self.assertLessEqual(result[metric], 1.5)

    def test_same_seed_same_result(self):
        first = self.run_world("W4", ticks=2, name="a")
        second = self.run_world("W4", ticks=2, name="b")
        first.pop("root")
        second.pop("root")
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
