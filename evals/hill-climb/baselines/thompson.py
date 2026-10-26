"""Thompson sampling baseline (PLAN.md 6.9): an outcome reference only; nothing here reaches the agents.

Arms are every type of the full catalog (W1 27, W2 40, W3 9, W4 9). Every 12 simulated hours it reads the app's
counts, samples each arm from Beta(1 + conversions, 1 + clicks - conversions) (W3: Gamma(1 + follows, 1 + slot-weighted
posts)), and puts this tick's money (money left / ticks left) on the top three sampled arms as campaigns at a daily
budget of two thirds of it each, clamped to $5 to $100, pausing campaigns not in the new top three (W2 also keeps each
budget within what the group's daily click cap can spend; W3 fills each free slot in the next 12 hours with the top
sampled arm). It builds one item per type with the specific text below, reads manifests and books results to the true
type, ignores the library, asks for no money, and samples with random.Random(1000 + world seed).

    python3 evals/hill-climb/baselines/thompson.py W4 1 [--root DIR] [--max-ticks N]
"""
from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402

TEXT = "Practice the river decision with pocket jacks in 2 minutes a day."
TICK_HOURS = 12
MIN_BUDGET = 5.0
MAX_BUDGET = 100.0
BUILD_TRIES = 3
RESUBMIT_TRIES = 5
SLOT_HOURS = (9, 13, 19)


def make_rng(world_seed: int) -> random.Random:
    return random.Random(1000 + int(world_seed))


def attrs_of(type_text: str) -> dict:
    return dict(part.partition("=")[::2] for part in str(type_text).split("|") if "=" in part)


def arm_types(world) -> list:
    _names, _values, rates = c.world_types(world)
    return sorted(rates)


def tick_daily_budget(money_left: float, ticks_left: int, cap_budget=None) -> float:
    """Two thirds of this tick's money (money left / ticks left), clamped to $5..$100 (and to the cap's spend)."""
    tick_money = money_left / max(1, ticks_left)
    budget = min(MAX_BUDGET, max(MIN_BUDGET, tick_money * 2.0 / 3.0))
    if cap_budget is not None:
        budget = min(budget, max(MIN_BUDGET, cap_budget))
    return round(budget, 2)


def top_arms(samples: dict, count: int = 3) -> list:
    return [arm for arm, _value in sorted(samples.items(), key=lambda kv: (-kv[1], kv[0]))[:count]]


def free_slots(now: datetime, taken, hours: int = TICK_HOURS) -> list:
    """Post slots (09:00, 13:00, 19:00 UTC) in [now, now + hours) that no post holds."""
    taken = {c.iso(t) for t in taken if t is not None}
    out = []
    day = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    end = now + timedelta(hours=hours)
    for offset in range(0, 3):
        for hour in SLOT_HOURS:
            slot = day + timedelta(days=offset, hours=hour)
            if now <= slot < end and c.iso(slot) not in taken:
                out.append(slot)
    return out


def sample_paid(rng: random.Random, arms, stats: dict) -> dict:
    samples = {}
    for arm in arms:
        clicks, conversions = stats.get(arm, (0, 0))
        conversions = min(conversions, clicks)
        samples[arm] = rng.betavariate(1 + conversions, 1 + clicks - conversions)
    return samples


def sample_posts(rng: random.Random, arms, stats: dict) -> dict:
    samples = {}
    for arm in arms:
        follows, weighted = stats.get(arm, (0, 0.0))
        samples[arm] = rng.gammavariate(1 + follows, 1.0 / (1.0 + weighted))
    return samples


class Sim:
    """The agent-facing `sim` through the run's wrapper, plus `simadmin`."""

    def __init__(self, work: Path, hidden: Path, python: str, lab: Path = LAB):
        self.work = Path(work)
        self.hidden = Path(hidden)
        self.python = python
        self.lab = Path(lab)

    def sim(self, *args):
        wrapper = self.work / "bin" / "sim"
        if wrapper.exists():
            argv = [str(wrapper)] + [str(a) for a in args]
        else:
            argv = [self.python, str(self.lab / "sim" / "cli.py"), "sim", "--hidden", str(self.hidden)] + \
                [str(a) for a in args]
        proc = subprocess.run(argv, capture_output=True, text=True, cwd=str(self.work), timeout=300)
        return proc.returncode, proc.stdout + proc.stderr

    def simadmin(self, *args):
        argv = [self.python, str(self.lab / "sim" / "cli.py"), "simadmin", "--hidden", str(self.hidden)] + \
            [str(a) for a in args]
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=600)
        if proc.returncode != 0:
            raise RuntimeError(f"simadmin {args} failed: {proc.stderr.strip()[:300]}")
        return proc.stdout


def load_world(hidden):
    from sim.world import World

    return World.load(Path(hidden))


def paid_stats(world, mine: dict, now) -> tuple:
    """({true type: (clicks, app conversions arrived by now)}, total spend) over this baseline's campaigns."""
    stats = {}
    spend = 0.0
    for cid in world.campaigns:
        hourly = world.hourly(cid) or []
        spend += sum(float(h.get("spend", 0) or 0) for h in hourly)
        item = mine.get(cid)
        if item is None:
            continue
        arm = world.type_of(world.items[item]["attrs"])
        clicks = conversions = 0
        for h in hourly:
            hour = c.parse_time(h.get("hour"))
            if hour is None or hour >= now:
                continue
            clicks += int(h.get("clicks", 0) or 0)
            for at, count in h.get("app_arrivals") or []:
                arrived = c.parse_time(at)
                if arrived is not None and arrived <= now:
                    conversions += int(count)
        old = stats.get(arm, (0, 0))
        stats[arm] = (old[0] + clicks, old[1] + conversions)
    return stats, spend


def post_stats(world, now) -> dict:
    truth = world.truth()
    stats = {}
    for pid, post in (getattr(world, "posts", {}) or {}).items():
        slot = c.parse_time(post.get("slot"))
        if slot is None or slot >= now or post.get("item") not in world.items:
            continue
        arm = world.type_of(world.items[post["item"]]["attrs"])
        entries = world.hourly(pid) or []
        follows = sum(int(e.get("follows", 0) or 0) for e in entries)
        old = stats.get(arm, (0, 0.0))
        stats[arm] = (old[0] + follows, old[1] + c.slot_multiplier(slot, truth))
    return stats


def run(world_name: str, seed: int, lab: Path = LAB, root=None, python: str = sys.executable, max_ticks=None,
        log=None) -> dict:
    """Build the world's day-0 folder, run the baseline to the horizon (or max_ticks), and return its metrics."""
    import fixtures  # owned by the simulator builder

    log = log or (lambda message: None)
    root = Path(root) if root else Path(tempfile.mkdtemp(prefix=f"thompson-{world_name}-{seed}-"))
    run_dir, hidden = root / "run", root / "hidden"
    fixtures.build_world(world_name, seed, run_dir, hidden, Path(lab), python)
    sim = Sim(run_dir / "work", hidden, python, lab)
    rng = make_rng(seed)
    world = load_world(hidden)
    truth = world.truth()
    days = truth.get("days") if isinstance(truth.get("days"), (int, float)) else None
    if days is None:
        days = (world.config or {}).get("days") or c.WORLD_DAYS.get(world_name, 14)
    days = int(days)
    ticks = int(days * 24 // TICK_HOURS)
    if max_ticks is not None:
        ticks_run = min(ticks, int(max_ticks))
    else:
        ticks_run = ticks
    arms = arm_types(world)
    items_by_type = {}
    campaign_item = {}
    item_campaign = {}
    launches = []

    def ensure_item(arm):
        if arm in items_by_type:
            return items_by_type[arm]
        for _attempt in range(BUILD_TRIES):
            code, out = sim.sim("build", "--attrs", json.dumps(attrs_of(arm)), "--text", TEXT)
            match = re.search(r"Built\s+(it_\d+)", out)
            if code != 0 or not match:
                return None
            item = match.group(1)
            fresh = load_world(hidden)
            true_type = fresh.type_of(fresh.items[item]["attrs"])
            items_by_type.setdefault(true_type, item)
            if true_type == arm:
                return item
        return items_by_type.get(arm)

    def launch(item, budget, when):
        code, out = sim.sim("launch", item, "--daily-budget", f"{budget:.2f}")
        match = re.search(r"Launched\s+(cp_\d+)", out) or re.search(r"resubmit\s+(cp_\d+)", out)
        if not match:
            return None
        cid = match.group(1)
        tries = 0
        while code != 0 and tries < RESUBMIT_TRIES:
            code, out = sim.sim("resubmit", cid)
            tries += 1
        if code != 0:
            return None
        launches.append({"target": cid, "item": item, "sim_time": c.iso(when)})
        return cid

    for index in range(ticks_run):
        world = load_world(hidden)
        now = world.now
        if world_name == "W3":
            samples = sample_posts(rng, arms, post_stats(world, now))
            best = top_arms(samples, 1)[0]
            item = ensure_item(best)
            taken = [c.parse_time(p.get("slot")) for p in (world.posts or {}).values()]
            if item:
                for slot in free_slots(now, taken):
                    code, out = sim.sim("post", item, "--at", c.iso(slot))
                    match = re.search(r"Scheduled\s+(po_\d+)", out)
                    if code == 0 and match:
                        launches.append({"target": match.group(1), "item": item, "sim_time": c.iso(now)})
        else:
            stats, spend = paid_stats(world, campaign_item, now)
            samples = sample_paid(rng, arms, stats)
            money_left = float(truth.get("money_received") or 0) - spend
            cap_budget = None
            if world_name == "W2":
                cap_budget = float(truth.get("cap") or 0) * float(truth.get("cpc") or 0)
            budget = tick_daily_budget(money_left, ticks - index, cap_budget)
            keep = set()
            if money_left > 0.5:
                for arm in top_arms(samples, 3):
                    item = ensure_item(arm)
                    if item is None:
                        continue
                    cid = item_campaign.get(item)
                    if cid is None:
                        cid = launch(item, budget, now)
                        if cid is None:
                            continue
                        item_campaign[item] = cid
                        campaign_item[cid] = item
                    else:
                        sim.sim("set-budget", cid, f"{budget:.2f}")
                        status = (load_world(hidden).campaigns.get(cid) or {}).get("status")
                        if status == "paused":
                            sim.sim("resume", cid)
                    keep.add(cid)
            fresh = load_world(hidden)
            for cid in campaign_item:
                if cid not in keep and (fresh.campaigns.get(cid) or {}).get("status") == "live":
                    sim.sim("pause", cid)
        log(f"[thompson {world_name}:{seed}] tick {index} done")
        sim.simadmin("advance", "--hours", TICK_HOURS)
    world = load_world(hidden)
    result = {"world": world_name, "seed": seed, "ticks": ticks_run, "horizon_ticks": ticks,
              "launches": len(launches), "money_requests": 0, "root": str(root)}
    best_type = truth.get("best_type")
    first = next((l for l in launches if world.type_of(world.items[l["item"]]["attrs"]) == best_type), None)
    result["first_best"] = None if first is None else dict(first, day=(c.parse_time(first["sim_time"])
                                                                        - c.WORLD_START).days)
    if world_name == "W3":
        result["follows_captured"] = round(c.follows_captured(world, days), 4)
    else:
        result["conversions_captured"] = round(c.conversions_captured(world, world_name, days), 4)
        result["spend"] = round(sum(sum(float(h.get("spend", 0) or 0) for h in world.hourly(cid) or [])
                                    for cid in world.campaigns), 2)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("world")
    parser.add_argument("seed", type=int)
    parser.add_argument("--root", default=None)
    parser.add_argument("--max-ticks", type=int, default=None)
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args(argv)
    result = run(args.world.upper(), args.seed, root=args.root, python=args.python, max_ticks=args.max_ticks,
                 log=lambda message: print(message, file=sys.stderr))
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
