"""Backtest grading (PLAN.md 6.7, 6.8 and the backtest gates of section 8, draft 8).

`grade_backtest(run)` returns the process checks every skill run must pass and the run's outcome metrics. The outcome
gates compare runs (skill against no-skill, against `thompson.py`), so `run_backtest.py` applies them across the batch
with `outcome_gates`.
"""
from __future__ import annotations

import statistics
import sys
from datetime import timedelta
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def sourced_launches(run):
    """(launches without sourced ideas, {explore test: idea cites a Library row})."""
    unsourced = []
    explore = {}
    for launch in run.launches():
        test, idea, has, library = run.launch_sources(launch)
        if not has:
            unsourced.append(f"{launch.target} ({(test or {}).get('test_id') or 'no Tests row'}, idea "
                             f"{(idea or {}).get('idea_id') or (test or {}).get('idea_id') or '?'})")
        if test is not None and c.norm_label(test.get("lane")) == "explore":
            key = test.get("test_id")
            explore[key] = explore.get(key, False) or library
    return unsourced, explore


def _median(values):
    values = [v for v in values if isinstance(v, (int, float))]
    return round(statistics.median(values), 4) if values else None


def _tick_of(session) -> int:
    """The tick a session belongs to: its tick.json's `tick` (the setup's interview spans several sessions, all tick
    0), else its own index."""
    value = (session.tick or {}).get("tick")
    return value if isinstance(value, int) else session.index


def tick_speed(run) -> list:
    """PLAN.md 13.4, per tick: its wall time, its reported cost and its role dispatches (the main agent's Agent or Task
    calls). The sessions of one tick (the setup's intake interview) add up, so the setup still counts as one tick."""
    out, by_tick = [], {}
    for session in run.sessions:
        info = session.info
        start, end = info.get("started_t"), info.get("ended_t")
        wall = round(end - start, 1) if isinstance(start, (int, float)) and isinstance(end, (int, float)) else None
        cost = info.get("cost_usd") if isinstance(info.get("cost_usd"), (int, float)) else session.transcript.cost_usd
        tick = _tick_of(session)
        entry = by_tick.get(tick)
        if entry is None:
            entry = by_tick[tick] = {"tick": tick, "wall_s": wall, "cost_usd": cost, "dispatches": 0, "sessions": 0}
            out.append(entry)
        else:
            entry["wall_s"] = None if wall is None or entry["wall_s"] is None else round(entry["wall_s"] + wall, 1)
            entry["cost_usd"] = None if cost is None or entry["cost_usd"] is None else entry["cost_usd"] + cost
        entry["dispatches"] += len(session.transcript.agent_calls)
        entry["sessions"] += 1
    return out


def metrics(run) -> dict:
    speed = tick_speed(run)
    out = {"world": run.world_name, "ticks": len(speed), "sessions": len(run.sessions)}
    out["per_tick"] = speed
    out["median_tick_wall_s"] = _median([t["wall_s"] for t in speed])
    out["median_tick_cost_usd"] = _median([t["cost_usd"] for t in speed])
    out["median_tick_dispatches"] = _median([t["dispatches"] for t in speed])
    statuses = [s.info.get("status") or _status(s.info) for s in run.sessions]
    out["failed_ticks"] = sum(1 for status in statuses if status != "ok")
    out["tick_statuses"] = statuses
    costs = [s.info.get("cost_usd") for s in run.sessions if isinstance(s.info.get("cost_usd"), (int, float))]
    out["cost_usd"] = round(sum(costs), 4)
    walls = [s.info["ended_t"] - s.info["started_t"] for s in run.sessions
             if isinstance(s.info.get("started_t"), (int, float)) and isinstance(s.info.get("ended_t"), (int, float))]
    out["wall_s"] = round(sum(walls), 1)
    out["launches"] = len(run.launches())
    out["money_requests"] = sum(1 for n in run.notifies if c.norm_label(n.get("kind")) == "moneyrequest")
    world = run.world
    if world is None:
        out["error"] = "world unavailable"
        return out
    days = c.horizon_days(run)
    if run.world_name == "W3":
        out["follows_captured"] = round(c.follows_captured(world, days), 4)
    else:
        out["conversions_captured"] = round(c.conversions_captured(world, run.world_name, days), 4)
        money, spend, expected, efficiency = c.spend_and_efficiency(world)
        out.update({"money_received": round(money, 2), "spend": round(spend, 2),
                    "expected_conversions": round(expected, 1),
                    "efficiency": None if efficiency is None else round(efficiency, 4)})
    launch, when = c.first_best(run)
    out["first_best"] = None if launch is None else {"target": launch.target, "item": launch.item,
                                                     "sim_time": c.iso(when),
                                                     "day": _day(when)}
    if run.world_name == "W2":
        stars = []
        for item_launch in run.launches():
            item = (getattr(world, "items", {}) or {}).get(item_launch.item) or {}
            group = (item.get("attrs") or {}).get("group")
            when = item_launch.action.sim_time
            if group in c.NEVER_BOUGHT_STARS and when is not None and when <= c.WORLD_START + timedelta(days=10):
                stars.append({"group": group, "target": item_launch.target, "sim_time": c.iso(when)})
        out["never_bought_star_launched"] = stars[0] if stars else None
    return out


def _status(info: dict) -> str:
    if not info:
        return "missing"
    if info.get("timed_out"):
        return "timeout"
    if info.get("budget_hit"):
        return "budget"
    if info.get("result_ok"):
        return "ok"
    return "crashed"


def _day(when):
    if when is None:
        return None
    return (when - c.WORLD_START).days


def process_checks(run) -> list:
    checks = []
    ok, evidence = run.every_launch_checked()
    checks.append(c.check("every launch checked", ok, evidence))
    unsourced, explore = sourced_launches(run)
    checks.append(c.check("every launched test's idea had sources", not unsourced,
                          "; ".join(unsourced) if unsourced else f"{len(run.launches())} launches, all sourced"))
    cited = sum(1 for value in explore.values() if value)
    checks.append(c.check("at least half of explore tests' ideas cite a Library row",
                          bool(explore) and cited * 2 >= len(explore),
                          f"{cited} of {len(explore)} explore tests" if explore else "no explore test launched"))
    # Reads before a test's planned date are how the climb reads as results come in (VELOCITY_PLAN.md): not a gate.
    checks.append(run.autonomy_check())
    on_time, total, misses = run.platform_clock()
    share = on_time / total if total else 1.0
    checks.append(c.check("at least 90% of rows written in ticks carry the platform's time", share >= 0.9,
                          f"{on_time} of {total} ({share * 100:.1f}%)" + (f"; e.g. {misses[:3]}" if misses else "")))
    report = c.faults_report(run)
    if report.get("error"):
        checks.append(c.check("at least 80% of injected faults caught", False, report["error"]))
    elif report["total"] == 0:
        checks.append(c.check("at least 80% of injected faults caught", True, "no injected faults (skipped)"))
    else:
        rate = report["caught"] / report["total"]
        missed = [f"{f['kind']} {f['target']}: {f['evidence']}" for f in report["faults"] if not f["caught"]]
        checks.append(c.check("at least 80% of injected faults caught", rate >= 0.8,
                              f"{report['caught']} of {report['total']}" + (f"; missed {missed}" if missed else "")))
    if run.world is None:
        checks.append(c.check("at most one false proven lesson", False, "world unavailable"))
    else:
        lessons = c.false_proven_lessons(run)
        checks.append(c.check("at most one false proven lesson", len(lessons["false"]) <= 1,
                              f"{len(lessons['false'])} false of {lessons['proven']} proven"
                              + (f": {lessons['false']}" if lessons["false"] else "")
                              + (f"; unverifiable {lessons['unverifiable']}" if lessons["unverifiable"] else "")))
    ticks = c.explore_share_ticks(run)
    under = [t for t in ticks if t["under"]]
    checks.append(c.check("exploring never stops: at most two tick-ends with nothing committed to exploring while a "
                          "test could still read", len(under) <= 2,
                          f"{len(under)} of {len(ticks)} tick-ends under" +
                          (": " + "; ".join(f"tick {t['tick']} {t['note']}" for t in under[:5]) if under else "")))
    return checks


def grade_backtest(run) -> dict:
    checks = process_checks(run)
    return {"checks": checks, "process_pass": c.all_pass(checks), "metrics": metrics(run),
            "tampering": run.tampering(),
            "faults": c.faults_report(run) if run.world is not None else None,
            "explore_share": c.explore_share_ticks(run)}


def outcome_gates(results: dict) -> list:
    """Section 8's outcome gates over a batch. `results` maps "W1:1", "W1:1:noskill", "W4:1:thompson", ... to metrics
    dicts. Gates whose runs are missing are reported as not evaluated."""
    gates = []

    def get(key):
        return results.get(key) or {}

    w1 = [s for s in ("1", "2") if f"W1:{s}" in results]
    if w1:
        best = [s for s in w1 if (get(f"W1:{s}").get("first_best") or {}).get("day") is not None
                and get(f"W1:{s}")["first_best"]["day"] <= 14]
        above = [s for s in w1 if f"W1:{s}:noskill" in results and
                 (get(f"W1:{s}").get("conversions_captured") or 0) > (get(f"W1:{s}:noskill").get("conversions_captured") or 0)]
        gates.append(c.check("W1: true best launched by day 14 in at least 1 of 2 seeds", len(best) >= 1,
                             f"seeds with the best launched: {best or 'none'}"))
        gates.append(c.check("W1: conversions captured above the no-skill run on both seeds",
                             len(above) == 2 and len(w1) == 2, f"seeds above no-skill: {above or 'none'} of {w1}"))
    if "W2:1" in results:
        star = get("W2:1").get("never_bought_star_launched")
        gates.append(c.check("W2: a never-bought group among g31, g35, g38 launched by day 10", bool(star),
                             str(star) if star else "none launched by day 10"))
    if "W3:1" in results and "W3:1:noskill" in results:
        mine, theirs = get("W3:1").get("follows_captured") or 0, get("W3:1:noskill").get("follows_captured") or 0
        gates.append(c.check("W3: follows captured above the no-skill run", mine > theirs,
                             f"{mine:.3f} against {theirs:.3f}"))
    for seed in ("1", "2"):
        mine, theirs = get(f"W1:{seed}"), get(f"W1:{seed}:noskill")
        if f"W1:{seed}" in results and f"W1:{seed}:noskill" in results:
            a, b = mine.get("median_tick_wall_s"), theirs.get("median_tick_wall_s")
            gates.append(c.check(f"W1 seed {seed}: the median tick takes at most twice the no-skill run's median tick",
                                 bool(a) and bool(b) and a <= 2 * b,
                                 f"{a} s against {b} s" + (f" ({a / b:.2f}x)" if a and b else "")))
    if "W4:1" in results and "W4:1:thompson" in results:
        mine = get("W4:1").get("conversions_captured") or 0
        theirs = get("W4:1:thompson").get("conversions_captured") or 0
        gates.append(c.check("W4: conversions captured at least 85% of thompson.py's", theirs > 0 and mine >= 0.85 * theirs,
                             f"{mine:.3f} against thompson {theirs:.3f}"))
    return gates
