"""Builds a run folder from a scenario fixture, or a world's day-0 folder (PLAN.md 6.5, 13.2, INTERFACES.md).

A scenario's `scenarios/<ID>/fixture.json` (or a role test's `roles/<case>/fixture.json`) either stands alone or
`extends` a base (`scenarios/base_w1.json`, `scenarios/base_w5.json`). The base's ops run first, then the scenario's
(a scenario op with `"_replace": true` takes the place of the base op of the same kind and id); scenario rows update
base rows with the same key (field by field) and add the rest; `remove` deletes rows by key, and removing a test takes
everything that hangs on it. Dependent rows (checks, launch and pause decisions, idea statuses, the Map, Money
allocations, the Log, each Tests row's recipe, coding and summary of its checks, read and decision, Library coding, the
Overview as of the last tick) are derived unless the fixture gives them.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import math
import random
import re
import shlex
import shutil
import statistics
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from sim.world import DAY, HOUR, LIVE, World, iso, load_config, parse_time  # noqa: E402

SCENARIOS = LAB / "scenarios"
DEFAULT_PROMPT = "/hill-climb Run the tick."
# The simulated owner's brief for the intake interview (runner/owner.py): `scenarios/<ID>/owner.md` or
# `worlds/owners/<W>.md`, copied into the hidden folder, where no session can read it.
OWNER_BRIEF = "owner.md"
TAIL = ["written_at", "written_by"]
# The 4.7 layout plus the columns of PLAN.md 13.1 (3) to (5) as the skill's workbook reference places them: the
# Overview tab, Library and Tests `coding`, Tests `made_from`, `recipe`, `checks`, `read` and `decision`, Results
# `signals`.
TAB_COLUMNS = {
    "Charter": ["field", "value", "reason", "history"],
    "Overview": ["item", "value", "as_of"],
    "Library": ["library_id", "kind", "source", "link", "owner", "content", "signal", "type", "coding", "status",
                "notes", "legacy_ref"],
    "Ideas": ["idea_id", "source", "type", "description", "sources", "near_copy_of", "status", "reason", "legacy_ref"],
    "Map": ["type", "best_test_id", "best_result", "tests_count", "last_tested", "status", "history"],
    "Tests": ["test_id", "idea_id", "lane", "type", "comparison", "inspired_by", "hypothesis", "expected_range",
              "varies", "held_constant", "good_looks_like", "daily_budget", "days", "read_at", "guardrails", "rerun_of",
              "lesson_id", "built_on", "item_id", "made_from", "recipe", "coding", "platform_id", "status",
              "launched_at", "checks", "read", "decision", "legacy_ref", "history"],
    "Checks": ["check_id", "test_id", "item_id", "role", "verdict", "reasons"],
    "Results": ["result_id", "test_id", "window", "metric", "k", "n", "spend", "rate_text", "versus", "chance_beats",
                "method", "signals", "call", "moved", "notes", "legacy_ref"],
    "Decisions": ["decision_id", "test_id", "lesson_id", "kind", "reason", "data", "legacy_ref"],
    "Lessons": ["lesson_id", "subject", "statement", "winner", "loser", "status", "evidence", "predicts", "steering",
                "recheck_at", "legacy_ref", "history"],
    "Reviews": ["review_id", "role", "period", "findings", "call", "changes"],
    "Money": ["entry_id", "kind", "lane", "amount", "standing", "learned", "next", "note"],
    "Log": ["tick_id", "platform_time", "read", "learned", "did", "next"],
}
TAB_COLUMNS = {tab: cols + TAIL for tab, cols in TAB_COLUMNS.items()}
TABS = list(TAB_COLUMNS)
KEY_COLUMN = {tab: cols[0] for tab, cols in TAB_COLUMNS.items()}
KEY_PREFIX = {"Library": "LB", "Ideas": "ID", "Tests": "T", "Checks": "CK", "Results": "R", "Decisions": "D",
              "Lessons": "L", "Reviews": "RV", "Money": "M", "Log": "LG"}
OPEN = {"planned", "plan-checked", "built", "ready", "live", "paused"}
CLOSED = {"closed", "read"}
COMMITTED = {"plan-checked", "built", "ready", "live"}
CHECK_ROLES = ("plan-checker", "build-checker", "critic")
PAST_PRIOR_METHOD = ("Beta posteriors for both arms with the pooled rate of earlier results as a prior, weighted like "
                     "one typical earlier test; 20,000 draws")


class FixtureError(Exception):
    """A fixture that cannot be built as written."""


# ----------------------------------------------------------------------------------------------------------------------
# the three read methods (PLAN.md 6.4)


def _phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def normal_chance(kt, nt, kc, nc) -> float:
    pt, pc = kt / nt, kc / nc
    se = math.sqrt(pt * (1 - pt) / nt + pc * (1 - pc) / nc)
    if se == 0:
        return 1.0 if pt > pc else 0.0 if pt < pc else 0.5
    return _phi((pt - pc) / se)


def beta_chance(at, bt, ac, bc, draws: int = 20000, seed: int = 7) -> float:
    rng = random.Random(seed)
    wins = 0
    for _ in range(draws):
        if rng.betavariate(at, bt) > rng.betavariate(ac, bc):
            wins += 1
    return wins / draws


def reads(test: tuple, comparison: tuple, history: list) -> dict:
    """The chance the test beats its comparison for (k, n) pairs: the normal approximation on raw rates, Beta(1, 1)
    posteriors, and Beta posteriors whose prior on both arms has the pooled rate of `history` (k, n) pairs and a
    weight equal to their median n (flat when `history` is empty)."""
    kt, nt = int(test[0]), int(test[1])
    kc, nc = int(comparison[0]), int(comparison[1])
    out = {"normal": normal_chance(kt, nt, kc, nc),
           "flat": beta_chance(1 + kt, 1 + nt - kt, 1 + kc, 1 + nc - kc)}
    past = [(int(k), int(n)) for k, n in history if int(n) > 0]
    if past:
        p0 = sum(k for k, _ in past) / sum(n for _, n in past)
        weight = statistics.median(n for _, n in past)
        out["past_prior"] = beta_chance(weight * p0 + kt, weight * (1 - p0) + nt - kt,
                                        weight * p0 + kc, weight * (1 - p0) + nc - kc)
    else:
        out["past_prior"] = out["flat"]
    return out


def ids_in(text) -> list:
    return [t for t in re.split(r"[\s,;]+", str(text or "")) if t]


def window_counts(world: World, campaigns, since, until, count: str = "app") -> tuple:
    """(conversions, clicks) of these campaigns over [since, until): the app's count (every conversion) or the
    platform's."""
    since, until = parse_time(since), parse_time(until)
    k = n = 0
    for cid in campaigns:
        for hour in world.hourly(cid):
            if since <= parse_time(hour["hour"]) < until:
                n += hour["clicks"]
                k += hour["conversions"] if count == "app" else hour["platform_conversions"]
    return k, n


def read_inputs(world: World, rows: dict, test_id: str, comparison: str = "cp_0001", count: str = "app"):
    """(test (k, n), comparison (k, n), history) for a test's window: launch to its read date (or now), the
    comparison campaign over the same hours, and every Results row other than the test's own and its `rerun_of`'s."""
    test = next(r for r in rows["Tests"] if r["test_id"] == test_id)
    since = parse_time(test["launched_at"])
    until = min(parse_time(test["read_at"]), world.now) if test.get("read_at") else world.now
    exclude = {test_id, test.get("rerun_of") or ""}
    history = [(int(r["k"]), int(r["n"])) for r in rows["Results"]
               if r.get("test_id") not in exclude and str(r.get("k", "")).strip() and str(r.get("n", "")).strip()]
    return (window_counts(world, ids_in(test["platform_id"]), since, until, count),
            window_counts(world, [comparison], since, until, count), history)


# ----------------------------------------------------------------------------------------------------------------------
# loading and merging


def _read_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _key(tab: str, row: dict) -> str:
    return str(row.get(KEY_COLUMN[tab], "") or "")


def merge_rows(base: dict, scenario: dict) -> dict:
    out = {tab: [dict(r) for r in base.get(tab, [])] for tab in TABS}
    for tab, rows in (scenario or {}).items():
        if tab not in TAB_COLUMNS:
            raise FixtureError(f"unknown tab {tab!r}")
        for row in rows:
            key = _key(tab, row)
            existing = next((r for r in out[tab] if key and _key(tab, r) == key), None)
            if existing is not None and not row.get("_replace"):
                existing.update(row)
            elif existing is not None:
                out[tab][out[tab].index(existing)] = dict(row)
            else:
                out[tab].append(dict(row))
    return out


def merge_ops(base_ops: list, scenario_ops: list) -> list:
    """The base's ops, then the scenario's; a scenario op marked `"_replace": true` takes the place of the base op of
    the same kind and id instead (V25 rewrites the base's it_0004 this way)."""
    ops = copy.deepcopy(base_ops)
    for op in copy.deepcopy(scenario_ops):
        if op.pop("_replace", False):
            at = next((i for i, old in enumerate(ops) if old.get("op") == op.get("op") and old.get("id") == op.get("id")),
                      None)
            if at is None:
                raise FixtureError(f"_replace: the base has no {op.get('op')} op with id {op.get('id')}")
            ops[at] = op
        else:
            ops.append(op)
    return ops


def load_fixture(scenario: str, folder=None) -> dict:
    """The scenario's fixture with its base merged in: world, seed, now, money, overrides, ops, rows, remove, files,
    prompt and whether it has a workbook. `folder` holds a fixture outside `scenarios/` (a role test's case)."""
    spec = _read_json(Path(folder or SCENARIOS / scenario) / "fixture.json")
    base = _read_json(SCENARIOS / f"{spec['extends']}.json") if spec.get("extends") else {}
    files = dict(base.get("files", {}))
    for path, content in spec.get("files", {}).items():
        if content is None:
            files.pop(path, None)
        else:
            files[path] = content
    merged = {
        "scenario": scenario,
        "world": spec.get("world") or base.get("world"),
        "seed": spec.get("seed", base.get("seed")),
        "now": spec.get("now") or base.get("now"),
        "money": spec.get("money", base.get("money")),
        "overrides": dict(base.get("overrides", {}), **spec.get("overrides", {})),
        "allocations": dict(base.get("allocations", {}), **spec.get("allocations", {})),
        "ops": merge_ops(base.get("ops", []), spec.get("ops", [])),
        "rows": merge_rows(base.get("rows", {}), spec.get("rows", {})),
        "remove": list(base.get("remove", [])) + list(spec.get("remove", [])),
        "files": files,
        "prompt": spec.get("prompt") or base.get("prompt") or DEFAULT_PROMPT,
        "workbook": spec.get("workbook", base.get("workbook", True)),
    }
    if not merged["world"] or merged["seed"] is None or not merged["now"]:
        raise FixtureError(f"{scenario}: a fixture needs world, seed and now")
    return merged


def apply_removals(rows: dict, ops: list, keys: list):
    """Delete rows by key. A test takes its Checks, Results and Decisions rows, its campaigns, its item (when no
    other test uses it), their ops, and any lesson whose evidence was only that test."""
    gone_campaigns, gone_items = set(), set()
    existed = {_key(tab, r) for tab in TABS for r in rows[tab]}
    for key in keys:
        if key not in existed:
            raise FixtureError(f"remove: no row has the key {key}")
        test = next((r for r in rows["Tests"] if r["test_id"] == key), None)
        if test is None:
            for tab in TABS:
                rows[tab] = [r for r in rows[tab] if _key(tab, r) != key]
            continue
        rows["Tests"] = [r for r in rows["Tests"] if r["test_id"] != key]
        for tab in ("Checks", "Results", "Decisions"):
            rows[tab] = [r for r in rows[tab] if r.get("test_id") != key]
        rows["Lessons"] = [r for r in rows["Lessons"] if set(ids_in(r.get("evidence"))) != {key}]
        gone_campaigns.update(ids_in(test.get("platform_id")))
        item = test.get("item_id")
        if item and not any(r.get("item_id") == item for r in rows["Tests"]):
            gone_items.add(item)

    def keeps(op):
        ids = {op.get("id"), op.get("item"), op.get("campaign")}
        return not (ids & (gone_campaigns | gone_items))

    return rows, [op for op in ops if keeps(op)]


# ----------------------------------------------------------------------------------------------------------------------
# derived rows


def _charter(rows: dict, field: str) -> str:
    return next((str(r.get("value", "")) for r in rows["Charter"] if r.get("field") == field), "")


def _number(text, after: str = ""):
    match = re.search(rf"{after}\D*?(\d+(?:\.\d+)?)", str(text or ""))
    return float(match.group(1)) if match else None


def map_cells(world: World, rows: dict) -> list:
    """The Map's cells: every combination of the Charter's `map_attributes`, in catalog order."""
    wanted = re.sub(r"\(.*?\)", "", _charter(rows, "map_attributes"))
    names = [n for n in world.attribute_names() if re.search(rf"\b{re.escape(n)}\b", wanted)] or \
        world.attribute_names()
    cells = [[]]
    for name in names:
        cells = [c + [f"{name}={v}"] for c in cells for v in world.attribute_values(name)]
    return ["|".join(c) for c in cells]


def _rate(k, n) -> str:
    return f"{int(k) / int(n):.1%} ({int(k)} of {int(n)})" if int(n) else f"{k} of {n}"


def _money_text(value) -> str:
    value = float(value)
    return f"${value:.0f}" if value.is_integer() else f"${value:.2f}"


def _check_reason(role: str, test: dict, world: World) -> str:
    if role == "plan-checker":
        if test.get("lane") == "exploit":
            return "The plan keeps the best known option running with its read date and guardrails set before launch."
        return ("The plan can answer its own question by its read date at its budget: the change matches the "
                "question, the comparison runs on the same days, and success was named before any data.")
    if role == "build-checker":
        item = world.items.get(test.get("item_id"), {})
        built = ", ".join(f"{k}={v}" for k, v in item.get("attrs", {}).items())
        return f"The platform built what the plan describes: {built}."
    return ("Judged as a member of the audience against the current best item, this one would not lose on quality "
            "alone: it speaks to a real decision at the table.")


def _results_of(rows: dict, test_id: str) -> list:
    return [r for r in rows["Results"] if r.get("test_id") == test_id]


def _fill_result(rows: dict, result: dict, world: World, problems: list) -> None:
    """Fill a hill-climb Results row's derived fields from the records, and check its k and n against them."""
    test = next((t for t in rows["Tests"] if t["test_id"] == result.get("test_id")), None)
    if test is None or test.get("legacy_ref") or not test.get("launched_at"):
        return
    since, until = parse_time(test["launched_at"]), parse_time(test["read_at"])
    cids = ids_in(test.get("platform_id"))
    k, n = window_counts(world, cids, since, until, "platform")
    if str(result.get("k", "")) != str(k) or str(result.get("n", "")) != str(n):
        problems.append(f"{result.get('result_id')}: the records over {test['test_id']}'s window give {k} of {n}, "
                        f"not {result.get('k')} of {result.get('n')}")
        return
    comparison = "cp_0001"
    kc, nc = window_counts(world, [comparison], since, until, "platform")
    history = [(int(r["k"]), int(r["n"])) for r in rows["Results"]
               if r.get("test_id") not in {test["test_id"], test.get("rerun_of") or ""} and str(r.get("k", ""))]
    defaults = {
        "window": f"{iso(since)} to {iso(until)}",
        "metric": "platform conversions per click",
        "spend": f"{n * world.config['cpc']:.2f}",
        "rate_text": _rate(k, n),
        "versus": f"{comparison} {_rate(kc, nc)} over the same hours",
        "chance_beats": f"{reads((k, n), (kc, nc), history)['past_prior']:.2f}",
        "method": PAST_PRIOR_METHOD,
    }
    for name, value in defaults.items():
        if not str(result.get(name, "")).strip() or result.get(name) == "auto":
            result[name] = value


def _map_row(cell: str, rows: dict, start) -> dict:
    tests = [t for t in rows["Tests"] if not t.get("legacy_ref") and t.get("type") == cell
             and t.get("status") != "withdrawn"]
    exploit = [t for t in tests if t.get("lane") == "exploit" and t.get("status") in OPEN]
    read = []
    for t in tests:
        for r in _results_of(rows, t["test_id"]):
            if str(r.get("call", "")).lower() != "legacy" and str(r.get("n", "")).strip():
                read.append((int(r["k"]) / int(r["n"]), t, r))
    launched = sorted(t["launched_at"] for t in tests if t.get("launched_at"))
    row = {"type": cell, "best_test_id": "", "best_result": "", "tests_count": str(len(tests)),
           "last_tested": launched[-1][:10] if launched else "", "status": "untested", "history": "",
           "written_at": iso(start), "written_by": "main"}
    if read:
        _rate_value, test, result = max(read, key=lambda x: x[0])
        row.update(status="tested", best_test_id=test["test_id"],
                   best_result=f"{result['result_id']}: {_rate(result['k'], result['n'])}, call {result['call']}",
                   written_at=max(r.get("written_at", iso(start)) for _x, _t, r in read))
    if exploit:
        best = exploit[0]
        row.update(status="best", best_test_id=best["test_id"],
                   best_result=f"exploit since {best.get('launched_at', '')[:10]}; " + (row["best_result"] or "no read yet"),
                   written_at=best.get("launched_at") or iso(start))
    return row


def _derive_log(rows: dict, world: World) -> list:
    start, now = world.start, world.now
    tests = [t for t in rows["Tests"] if not t.get("legacy_ref")]
    legacy = [t for t in rows["Tests"] if t.get("legacy_ref")]
    results = [r for r in rows["Results"] if str(r.get("call", "")).lower() != "legacy"]
    out, t = [], start
    while t < now:
        stamp = iso(t)
        done = [f"{r['result_id']} ({r['test_id']}): {r['k']} of {r['n']}, call {r['call']}"
                for r in results if r.get("written_at") == stamp]
        did = []
        if t == start:
            did.append("set up the hill climb: the Charter, the Library, the Ideas and the Map"
                       + (f", with {len(legacy)} earlier runs imported as legacy tests" if legacy else ""))
        for x in tests:
            if x.get("written_at") == stamp and x.get("launched_at") != stamp:
                did.append(f"planned {x['test_id']}")
            if x.get("launched_at") == stamp:
                cid = next(iter(ids_in(x.get("platform_id"))), None)
                at_launch = world.budget_at(cid, t) if cid in world.campaigns else None
                did.append(f"launched {x['test_id']} on {x.get('platform_id')} at "
                           f"{_money_text(at_launch or x.get('daily_budget') or 0)}/day")
            if x.get("status") in CLOSED and x.get("read_at") and parse_time(x["read_at"]) == t:
                did.append(f"closed {x['test_id']} and paused {x.get('platform_id')}")
        for d in rows["Decisions"]:
            if d.get("written_at") == stamp and d.get("kind") not in ("launch", "pause"):
                did.append(f"{d.get('kind')} on {d.get('test_id')}: {d.get('data')}")
        for r in rows["Reviews"]:
            if r.get("written_at") == stamp:
                did.append(f"wrote the progress report {r.get('review_id')} ({r.get('call')})" if r.get("role") == "report"
                           else f"the {r.get('role')}'s review {r.get('review_id')}")
        upcoming = sorted((parse_time(x["read_at"]), x["test_id"]) for x in tests
                          if x.get("launched_at") and parse_time(x["launched_at"]) <= t and x.get("read_at")
                          and parse_time(x["read_at"]) > t)
        if upcoming:
            first = upcoming[0][0]
            due = [tid for when, tid in upcoming if when == first]
            nxt = f"next read: {' and '.join(due)} on {iso(first)[:10]}"
        else:
            nxt = "plan the next explore test"
        out.append({"platform_time": stamp,
                    "read": "; ".join(done) or ("sim catalog, the history and sim library" if t == start else
                                                "the platform's and the app's counts for the live tests; no read was due"),
                    "did": "; ".join(did) or "watched the live tests; nothing needed changing",
                    "next": nxt, "written_at": stamp, "written_by": "main"})
        t += 12 * HOUR
    return out


def assign_keys(rows: dict) -> None:
    for tab, prefix in KEY_PREFIX.items():
        col = KEY_COLUMN[tab]
        used = set()
        for r in rows[tab]:
            match = re.fullmatch(rf"{prefix}-(\d+)", str(r.get(col, "")))
            if match:
                used.add(int(match.group(1)))
        number = 1
        for r in sorted((r for r in rows[tab] if not r.get(col)), key=lambda r: r.get("written_at", "")):
            while number in used:
                number += 1
            r[col] = f"{prefix}-{number:04d}"
            used.add(number)


def derive_rows(rows: dict, world: World, allocations: dict | None = None) -> list:
    """Fill the derived rows in place (PLAN.md 6.5, 13.2); returns problems found on the way."""
    start, problems = world.start, []
    stamp0 = iso(start)
    library = {e["id"]: e for e in world.library_entries()}
    for row in rows["Library"]:
        entry = library.get(row.get("_lib"))
        if row.get("_lib") and entry is None:
            problems.append(f"{row.get('library_id')} names {row['_lib']}, which the world's library lacks")
        elif entry is not None:
            row.setdefault("owner", entry.get("owner", ""))
            row.setdefault("source", f"competitor ad {entry['id']} in the platform's ad library")
            row.setdefault("content", f"\"{entry['text']}\"; shows: {entry['shows']}; offer: {entry['offer']}")
            row.setdefault("signal", f"running {entry['running_days']} days")
            row.setdefault("coding", world.type_of(entry["_type"]))
    hill = sorted((t for t in rows["Tests"] if not t.get("legacy_ref")), key=lambda t: t.get("launched_at") or "~")
    for test in hill:
        if not test.get("launched_at"):
            continue
        launch = parse_time(test["launched_at"])
        when = max(launch - HOUR, parse_time(test.get("written_at") or stamp0))
        for role in CHECK_ROLES:
            if any(c.get("test_id") == test["test_id"] and c.get("role") == role for c in rows["Checks"]):
                continue
            rows["Checks"].append({"test_id": test["test_id"], "item_id": "" if role == "plan-checker" else
                                   test.get("item_id", ""), "role": role, "verdict": "pass",
                                   "reasons": _check_reason(role, test, world), "written_at": iso(when),
                                   "written_by": role})
    for result in rows["Results"]:
        if not result.get("result_id") and result.get("test_id", "").startswith("T-"):
            result["result_id"] = "R-" + result["test_id"][2:]
        _fill_result(rows, result, world, problems)
    for test in hill:
        tid = test["test_id"]
        if test.get("launched_at") and not any(d.get("test_id") == tid and d.get("kind") == "launch"
                                               for d in rows["Decisions"]):
            rows["Decisions"].append({
                "test_id": tid, "kind": "launch", "reason": "every check passed; launch at the planned budget",
                "data": f"plan-checker, build-checker and critic passed; launched {test.get('platform_id')} "
                        f"({test.get('item_id')}) at {_money_text(test.get('daily_budget') or 0)}/day",
                "written_at": test["launched_at"], "written_by": "main"})
        if test.get("status") in CLOSED and test.get("read_at") and not any(
                d.get("test_id") == tid and d.get("kind") == "pause" for d in rows["Decisions"]):
            result = next(iter(_results_of(rows, tid)), {})
            rows["Decisions"].append({
                "test_id": tid, "kind": "pause", "reason": "the read date came and the test was read once; close it",
                "data": f"{result.get('result_id', 'its result')}: {result.get('k')} of {result.get('n')}, call "
                        f"{result.get('call')}; paused {test.get('platform_id')}",
                "written_at": test["read_at"], "written_by": "main"})
    for idea in rows["Ideas"]:
        if not idea.get("status"):
            using = [t.get("status") for t in rows["Tests"] if t.get("idea_id") == idea.get("idea_id")]
            idea["status"] = "tested" if CLOSED & set(using) else "planned" if OPEN & set(using) else "new"
    given = {r.get("type"): r for r in rows["Map"]}
    rows["Map"] = [given.get(cell) or _map_row(cell, rows, start) for cell in map_cells(world, rows)] + \
        [r for t, r in given.items() if t not in map_cells(world, rows)]
    if not any(m.get("kind") == "allocate" for m in rows["Money"]):
        lanes, pace = _charter(rows, "lanes"), _number(_charter(rows, "speed") or _charter(rows, "pace"))
        for lane in ("exploit", "develop", "explore"):
            # the lanes are in words; the fixture's lab-only `allocations` gives each lane's share of the pace
            share = _number(lanes, lane)
            if share is None:
                share = (allocations or {}).get(lane)
            if share is None and lane == "develop":
                share = (allocations or {}).get("confirm")
            if share is None or pace is None:
                continue
            rows["Money"].append({"kind": "allocate", "lane": lane, "amount": f"{pace * share / 100:.2f}",
                                  "standing": "", "learned": "", "next": "",
                                  "note": f"this lane's part of the {_money_text(pace)}/day committed now, per the Charter's lanes",
                                  "written_at": stamp0, "written_by": "main"})
    if not rows["Log"]:
        rows["Log"] = _derive_log(rows, world)
    for tab in TABS:
        for r in rows[tab]:
            r.setdefault("written_at", stamp0)
            r.setdefault("written_by", "main")
    assign_keys(rows)
    for tab in TABS:
        if tab not in ("Charter", "Map", "Overview"):
            rows[tab].sort(key=lambda r: str(r.get(KEY_COLUMN[tab])))
    summarize_tests(rows, world)
    if not rows["Overview"]:
        rows["Overview"] = derive_overview(rows, world)
    return problems


def recipe_of(world: World, iid: str) -> str:
    """How an item was made, as its Tests row records it (PLAN.md 13.1 (3)): the command, the parent, the exact text
    and where the item is kept."""
    item = world.items[iid]
    keep = f"The platform keeps the built item as {iid} (see it with `sim manifest {iid}`); there are no other files."
    parent_id = item.get("made_from")
    if parent_id:
        parent = world.items.get(parent_id) or {}
        changes = {k: v for k, v in item["requested"].items() if (parent.get("attrs") or {}).get(k) != v}
        words = "" if item["text"] == parent.get("text") else f" --text \"{item['text']}\""
        changed = ", ".join(f"{k} to {v}" for k, v in changes.items()) or "nothing"
        return (f"Made on the platform with `sim build --from {parent_id} --attrs '{json.dumps(changes)}'{words}`: "
                f"{parent_id}'s own values and text, changing only {changed}. Parent: {parent_id}. "
                f"Text: \"{item['text']}\". {keep}")
    return (f"Made on the platform with `sim build --attrs '{json.dumps(item['requested'])}' --text "
            f"\"{item['text']}\"`. Text: \"{item['text']}\". {keep}")


def summarize_tests(rows: dict, world: World) -> None:
    """Each hill-climb Tests row's whole life on the row (PLAN.md 13.1 (5)), unless the fixture gives it: how its item
    was made (`recipe`, `made_from`), the item's values on the full coding once it ran (`coding`; a built item still
    waiting on its checks is left uncoded, so the record never shows a build fault before the build-checker looks), and
    the verdicts, read and decision behind it with their keys."""
    for test in rows["Tests"]:
        if test.get("legacy_ref"):
            continue
        tid, iid = test["test_id"], test.get("item_id") or ""
        item = world.items.get(iid)
        if item is not None:
            test.setdefault("recipe", recipe_of(world, iid))
            test.setdefault("made_from", item.get("made_from") or "")
            if test.get("launched_at"):
                test.setdefault("coding", world.type_of(item["attrs"]))
        checks = [c for c in rows["Checks"] if c.get("test_id") == tid
                  or (not c.get("test_id") and iid and c.get("item_id") == iid)]
        if checks:
            test.setdefault("checks", "; ".join(f"{c['role']} {c['verdict']} ({c['check_id']})" for c in checks))
        results = [r for r in _results_of(rows, tid) if str(r.get("call", "")).lower() != "legacy"]
        if results:
            r = max(results, key=lambda x: (x.get("written_at", ""), x.get("result_id", "")))
            test.setdefault("read", f"{r['result_id']}: {r.get('rate_text')} against {r.get('versus')}; chance it "
                                    f"beats the comparison {r.get('chance_beats')}; call {r.get('call')}")
        decisions = [d for d in rows["Decisions"] if d.get("test_id") == tid]
        if decisions:
            d = max(decisions, key=lambda x: (x.get("written_at", ""), x.get("decision_id", "")))
            test.setdefault("decision", f"{d['decision_id']} {d.get('kind')}: {d.get('reason')}")


def _cost_per_conversion(world: World, since, until):
    clicks = conversions = 0
    for cid in world.campaigns:
        for hour in world.hourly(cid):
            if since <= parse_time(hour["hour"]) < until:
                clicks += hour["clicks"]
                conversions += hour["platform_conversions"]
    return clicks * world.config.get("cpc", 0.0) / conversions if conversions else None


def derive_overview(rows: dict, world: World) -> list:
    """The Overview as the last tick before now left it (PLAN.md 13.1 (5)): the bar now and at the start, money left
    and how fast it is going, what is live and how each is reading, the best known option, strong lessons and what
    comes next."""
    start = world.start
    times = sorted(parse_time(r["platform_time"]) for r in rows["Log"] if r.get("platform_time"))
    if not times or not world.paid:
        return []
    as_of = times[-1]
    stamp = iso(as_of)
    now_bar = _cost_per_conversion(world, max(start, as_of - 3 * DAY), as_of)
    start_bar = _cost_per_conversion(world, start, start + DAY)
    live = []
    for test in sorted(rows["Tests"], key=lambda t: t["test_id"]):
        cids = ids_in(test.get("platform_id"))
        if test.get("legacy_ref") or not cids or not test.get("launched_at") or parse_time(test["launched_at"]) > as_of:
            continue
        if any(cid in world.campaigns and world.status_at(cid, as_of) == LIVE for cid in cids):
            live.append(test)
    lessons = [r for r in rows["Lessons"] if r.get("status") in ("strong", "proven")]
    committed = sum(float(t.get("daily_budget") or 0) for t in rows["Tests"] if t.get("status") in COMMITTED)
    cpc_text = (lambda x: "no conversions yet" if x is None else f"${x:.2f} per conversion")
    items = [
        ("bar now", f"{cpc_text(now_bar)} on the platform's count, all campaigns, the three days to {stamp}"),
        ("bar at start", f"{cpc_text(start_bar)} on the platform's count, all campaigns, the first day "
                         f"({iso(start)[:10]})"),
        ("money left", f"${world.money_received() - world.spend_between(None, as_of):.2f} of "
                       f"${world.money_received():.2f}"),
        ("speed", f"{_charter(rows, 'speed') or _charter(rows, 'pace')}; {_money_text(committed)} a day committed"),
        ("live", "; ".join(f"{t['test_id']} on {t['platform_id']} ({t.get('lane')}, "
                           f"{_money_text(t.get('daily_budget') or 0)}/day, reads {str(t.get('read_at'))[:10]})"
                           for t in live) or "nothing"),
        ("best known option", "; ".join(f"{t['test_id']}: {t.get('type')} ({t.get('item_id')}), exploit since "
                                        f"{t['launched_at'][:10]}" for t in live if t.get("lane") == "exploit")
         or "none yet"),
        ("strong lessons", "; ".join(f"{r['lesson_id']}: {r.get('statement')} (recheck {str(r.get('recheck_at'))[:10]})"
                                     for r in lessons) or "none yet"),
        ("next", next((r.get("next") for r in rows["Log"] if r.get("platform_time") == stamp), "") or "the next tick"),
    ]
    return [{"item": name, "value": value, "as_of": stamp, "written_at": stamp, "written_by": "main"}
            for name, value in items]


def check_rows(rows: dict, world: World) -> list:
    """Problems where the workbook and the platform disagree, or a row names a key that does not exist."""
    problems = []
    keys = {_key(tab, r) for tab in TABS for r in rows[tab]}
    for tab in TABS:
        for r in rows[tab]:
            extra = [c for c in r if not c.startswith("_") and c not in TAB_COLUMNS[tab]]
            if extra:
                problems.append(f"{tab} {_key(tab, r)} has unknown columns {extra}")
    for test in rows["Tests"]:
        tid = test["test_id"]
        for cid in ids_in(test.get("platform_id")):
            camp = world.campaigns.get(cid)
            if camp is None:
                problems.append(f"{tid}: campaign {cid} does not exist")
                continue
            if test.get("item_id") and camp["item"] != test["item_id"]:
                problems.append(f"{tid}: {cid} runs {camp['item']}, not {test['item_id']}")
            if test.get("status") == "live" and camp["status"] != LIVE:
                problems.append(f"{tid} is live but {cid} is {camp['status']}")
            if test.get("status") == "live" and float(world.current_budget(cid)) != float(test.get("daily_budget")):
                problems.append(f"{tid}: {cid} runs at {world.current_budget(cid)}/day, not {test.get('daily_budget')}")
            if test.get("status") in CLOSED and camp["status"] == LIVE:
                problems.append(f"{tid} is {test['status']} but {cid} is still live")
        if test.get("item_id") and test["item_id"] not in world.items:
            problems.append(f"{tid}: item {test['item_id']} does not exist")
        if test.get("platform_id") and test.get("launched_at"):
            first = world.campaigns.get(ids_in(test["platform_id"])[0], {})
            if first.get("launched_at") and first["launched_at"] != test["launched_at"]:
                problems.append(f"{tid}: launched_at {test['launched_at']} but the platform says {first['launched_at']}")
    for idea in rows["Ideas"]:
        for key in ids_in(idea.get("sources")):
            if key not in keys:
                problems.append(f"{idea['idea_id']} cites {key}, which does not exist")
    for lesson in rows["Lessons"]:
        for key in ids_in(lesson.get("evidence")):
            if key not in keys:
                problems.append(f"{lesson['lesson_id']}'s evidence {key} does not exist")
    return problems


# ----------------------------------------------------------------------------------------------------------------------
# writing a run folder


def _cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def write_workbook(rows: dict, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for tab in TABS:
        with open(folder / f"{tab}.csv", "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(TAB_COLUMNS[tab])
            for r in rows[tab]:
                writer.writerow([_cell(r.get(c, "")) for c in TAB_COLUMNS[tab]])


def read_workbook(folder: Path) -> dict:
    out = {}
    for tab in TABS:
        path = Path(folder) / f"{tab}.csv"
        if path.exists():
            with open(path, newline="", encoding="utf-8") as handle:
                out[tab] = list(csv.DictReader(handle))
    return out


def world_file(name: str, world: World) -> str:
    if name == "README.md":
        return world.config["readme"]
    if name == "history.csv":
        columns, rows = world.history_rows()
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(columns)
        for row in rows:
            writer.writerow([_cell(row.get(c, "")) for c in columns])
        return buffer.getvalue()
    raise FixtureError(f"the world has no file {name}")


def write_files(files: dict, work: Path, world: World) -> dict:
    """Write the fixture's files into work/; returns {path: sha256} of each."""
    hashes = {}
    for name, content in sorted(files.items()):
        text = world_file(Path(name).name, world) if content == "@world" else str(content)
        path = Path(work) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        data = text.encode("utf-8")
        path.write_bytes(data)
        hashes[name] = hashlib.sha256(data).hexdigest()
    return hashes


def write_wrappers(work: Path, hidden: Path, lab: Path, python: str) -> None:
    """work/bin/sim, notify and gws: /bin/sh wrappers that call the lab's CLI with the hidden folder."""
    bin_dir = Path(work) / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    cli = Path(lab).resolve() / "sim" / "cli.py"
    for tool in ("sim", "notify", "gws"):
        path = bin_dir / tool
        path.write_text(f"#!/bin/sh\nexec {shlex.quote(str(python))} -I {shlex.quote(str(cli))} {tool} --hidden "
                        f"{shlex.quote(str(Path(hidden).resolve()))} \"$@\"\n", encoding="utf-8")
        path.chmod(0o755)


def _finish_hidden(hidden: Path, work: Path, hashes: dict, meta: dict) -> None:
    for name in ("sim_actions.jsonl", "outbox.jsonl"):
        (hidden / name).write_text("", encoding="utf-8")
    initial = hidden / "initial_workbook"
    if initial.exists():
        shutil.rmtree(initial)
    shutil.copytree(work / "workbook", initial)
    (hidden / "initial_files.json").write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (hidden / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def copy_owner_brief(folder: Path, hidden: Path, name: str = OWNER_BRIEF) -> bool:
    """Copy the owner's brief (folder/name), when there is one, to HIDDEN/owner.md."""
    source = Path(folder) / name
    if not source.is_file():
        return False
    shutil.copyfile(source, Path(hidden) / OWNER_BRIEF)
    return True


def closing_pauses(rows: dict, ops: list) -> list:
    """A pause at its read for each closed test's campaigns that no op pauses already."""
    paused = {op.get("campaign") for op in ops if op.get("op") == "pause"}
    out = []
    for test in rows["Tests"]:
        if test.get("legacy_ref") or test.get("status") not in CLOSED or not test.get("read_at"):
            continue
        for cid in ids_in(test.get("platform_id")):
            if cid not in paused:
                out.append({"op": "pause", "campaign": cid, "at": test["read_at"]})
    return out


def build_scenario(scenario: str, run_dir: Path, hidden_dir: Path, lab: Path = LAB, python: str = sys.executable,
                   folder=None, kind: str = "scenario") -> dict:
    """Builds RUN/work and HIDDEN for scenario "V01".."V30" from scenarios/<id>/fixture.json (or from `folder`, a role
    test's case, with meta kind "role"); returns the meta dict written to HIDDEN/meta.json."""
    spec = load_fixture(scenario) if folder is None else load_fixture(scenario, folder)
    rows, ops = apply_removals(spec["rows"], spec["ops"], spec["remove"])
    config = load_config(spec["world"])
    money = config["money"] if spec["money"] is None else spec["money"]
    hidden, work = Path(hidden_dir), Path(run_dir) / "work"
    world = World.create(hidden, config, spec["seed"], faults=False, money=money, overrides=spec["overrides"])
    world.apply_ops(ops + closing_pauses(rows, ops))
    world.now = spec["now"]
    problems = world.validate()
    if spec["workbook"]:
        problems += derive_rows(rows, world, spec.get("allocations"))
        problems += check_rows(rows, world)
    if problems:
        raise FixtureError(f"{scenario} cannot be built: " + "; ".join(problems))
    work.mkdir(parents=True, exist_ok=True)
    world.save()
    hashes = write_files(spec["files"], work, world)
    (work / "workbook").mkdir(exist_ok=True)
    if spec["workbook"]:
        write_workbook(rows, work / "workbook")
    write_wrappers(work, hidden, lab, python)
    meta = {"kind": kind, "scenario": scenario, "world": spec["world"], "seed": spec["seed"],
            "now": iso(world.now), "prompt": spec["prompt"], "lab": str(Path(lab).resolve())}
    _finish_hidden(hidden, work, hashes, meta)
    copy_owner_brief(Path(folder) if folder is not None else SCENARIOS / scenario, hidden)
    return meta


def build_world(world: str, seed: int, run_dir: Path, hidden_dir: Path, lab: Path = LAB,
                python: str = sys.executable) -> dict:
    """Builds a backtest's day-0 folder (README.md, history.csv, wrappers, no workbook) for world W1..W5."""
    config = load_config(world)
    hidden, work = Path(hidden_dir), Path(run_dir) / "work"
    sim_world = World.create(hidden, config, seed, faults=True)
    work.mkdir(parents=True, exist_ok=True)
    sim_world.save()
    files = {"README.md": "@world"}
    if config.get("history"):
        files["history.csv"] = "@world"
    hashes = write_files(files, work, sim_world)
    (work / "workbook").mkdir(exist_ok=True)
    write_wrappers(work, hidden, lab, python)
    meta = {"kind": "world", "scenario": None, "world": world, "seed": int(seed), "now": iso(sim_world.now),
            "prompt": config["setup_prompt"], "lab": str(Path(lab).resolve())}
    _finish_hidden(hidden, work, hashes, meta)
    copy_owner_brief(LAB / "worlds" / "owners", hidden, f"{world}.md")
    return meta


SCENARIO_IDS = [f"V{i:02d}" for i in range(1, 32) if i != 22]
