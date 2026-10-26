"""The lab's simulated platform: world model, ground truth, library, traffic and faults (PLAN.md 6.2, 6.3, 13.2).

`World` holds one run's whole state in `HIDDEN/state.json`. Graders treat it as read-only; `sim/cli.py` and
`fixtures.py` change it. Random draws come from `random.Random` seeded with
sha256(f"{world_seed}:{kind}:{id}:{hour}"), so a campaign's numbers do not depend on command order.

W5 (`partial_builds`) builds from the attributes given and draws the rest, or from a parent item (`made_from`); its
truth depends only on `truth_attributes`. Worlds with a `reception` draw soft signals (comments, saves, hides) from each
item's hidden reception, on their own random streams, so they never change a conversion.
"""
from __future__ import annotations

import contextlib
import copy
import fcntl
import hashlib
import json
import math
import os
import random
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

LAB = Path(__file__).resolve().parent.parent
WORLDS_DIR = LAB / "worlds"
EPOCH = "2026-11-02T00:00:00Z"
HOUR = timedelta(hours=1)
DAY = timedelta(days=1)
LIVE, PAUSED, REJECTED, EXHAUSTED = "live", "paused", "rejected", "exhausted"
SHARE_NORMAL, SHARE_FAULT, DELIVERY_RATE = 0.85, 0.12, 0.3
QUALITIES = ("specific", "neutral", "generic")


# ----------------------------------------------------------------------------------------------------------------------
# time and number helpers


def parse_time(text) -> datetime:
    """Lenient ISO reader: a date, a date and hour, with or without seconds or `Z`. Always UTC."""
    if isinstance(text, datetime):
        return text if text.tzinfo else text.replace(tzinfo=timezone.utc)
    s = str(text).strip()
    if not s:
        raise ValueError("empty time")
    s = s.replace(" ", "T")
    if s.endswith("Z") or s.endswith("z"):
        s = s[:-1]
    s = re.sub(r"[+-]00:?00$", "", s)
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"cannot read the time {text!r}; use ISO 8601 such as 2026-11-08T00:00:00Z")


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def floor_hour(dt: datetime) -> datetime:
    return dt.replace(minute=0, second=0, microsecond=0)


def floor_day(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def hours_between(a: datetime, b: datetime):
    """Each hour start in [a, b)."""
    h = floor_hour(a)
    if h < a:
        h += HOUR
    while h < b:
        yield h
        h += HOUR


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def seeded(world_seed, kind: str, ident: str, hour) -> random.Random:
    hour_text = iso(hour) if isinstance(hour, datetime) else str(hour)
    digest = hashlib.sha256(f"{world_seed}:{kind}:{ident}:{hour_text}".encode()).hexdigest()
    return random.Random(int(digest, 16))


def poisson(rng: random.Random, mean: float) -> int:
    if mean <= 0:
        return 0
    limit, k, p = math.exp(-mean), 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1


def binomial(rng: random.Random, n: int, p: float) -> int:
    if p <= 0 or n <= 0:
        return 0
    if p >= 1:
        return n
    return sum(1 for _ in range(n) if rng.random() < p)


def spread(total: int, slots: int) -> list:
    """`total` spread as evenly as integers allow over `slots` (hour i gets floor((i+1)T/S) - floor(iT/S))."""
    return [((i + 1) * total) // slots - (i * total) // slots for i in range(slots)]


def pick_evenly(total: int, among: list) -> list:
    """Spread `total` events evenly over the events listed per slot in `among`, never more than a slot holds."""
    events = [i for i, n in enumerate(among) for _ in range(n)]
    out = [0] * len(among)
    if total <= 0 or not events:
        return out
    if total > len(events):
        raise ValueError(f"cannot place {total} events among {len(events)}")
    for j in range(total):
        out[events[int((j + 0.5) * len(events) / total)]] += 1
    return out


def load_config(world_id: str) -> dict:
    path = WORLDS_DIR / f"{world_id}.json"
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def text_quality(text: str, config: dict) -> str:
    """The hidden rubric: generic first (a generic phrase or fewer than 6 words), then specific (a digit or a
    specific term), else neutral. Substring matches on the lowercased text."""
    low = str(text or "").lower()
    if any(p in low for p in config.get("generic_phrases", [])) or len(low.split()) < 6:
        return "generic"
    if any(ch.isdigit() for ch in low) or any(t in low for t in config.get("specific_terms", [])):
        return "specific"
    return "neutral"


@contextlib.contextmanager
def locked(hidden: Path):
    """An exclusive lock on the hidden folder for one command."""
    hidden = Path(hidden)
    hidden.mkdir(parents=True, exist_ok=True)
    with open(hidden / ".lock", "a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class SimError(Exception):
    """A refused command: the message is shown to the caller and the command exits 1."""


# ----------------------------------------------------------------------------------------------------------------------
# the world


class World:
    def __init__(self, hidden: Path, state: dict):
        self.hidden = Path(hidden)
        self.state = state

    # -- persistence ---------------------------------------------------------------------------------------------------

    @classmethod
    def create(cls, hidden, config: dict, seed: int, faults: bool = True, money=None, start=None,
               overrides=None) -> "World":
        start_dt = parse_time(start or config.get("start") or EPOCH)
        state = {
            "format": 1,
            "world": config["id"],
            "config": copy.deepcopy(config),
            "seed": int(seed),
            "start": iso(start_dt),
            "now": iso(start_dt),
            "faults_on": bool(faults),
            "overrides": dict(overrides or {}),
            "money_start": float(config.get("money", 0) if money is None else money),
            "grants": [],
            "items": {},
            "campaigns": {},
            "posts": {},
            "records": {},
            "post_results": {},
            "faults": [dict(f, source="scheduled") for f in config.get("faults", [])] if faults else [],
            "counters": {"it": 0, "cp": 0, "po": 0},
        }
        return cls(hidden, state)

    @classmethod
    def load(cls, hidden: Path) -> "World":
        with open(Path(hidden) / "state.json", encoding="utf-8") as handle:
            return cls(hidden, json.load(handle))

    def save(self) -> None:
        self.hidden.mkdir(parents=True, exist_ok=True)
        tmp = self.hidden / f".state.{os.getpid()}.tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(self.state, handle, separators=(",", ":"))
        os.replace(tmp, self.hidden / "state.json")

    # -- plain views -------------------------------------------------------------------------------------------------

    @property
    def now(self) -> datetime:
        return parse_time(self.state["now"])

    @now.setter
    def now(self, value) -> None:
        self.state["now"] = iso(parse_time(value))

    @property
    def start(self) -> datetime:
        return parse_time(self.state["start"])

    @property
    def config(self) -> dict:
        return self.state["config"]

    @property
    def items(self) -> dict:
        return self.state["items"]

    @property
    def campaigns(self) -> dict:
        return self.state["campaigns"]

    @property
    def posts(self) -> dict:
        return self.state["posts"]

    @property
    def seed(self) -> int:
        return self.state["seed"]

    @property
    def world_id(self) -> str:
        return self.state["world"]

    @property
    def paid(self) -> bool:
        return self.config.get("kind") == "paid"

    def day_number(self, when=None) -> int:
        return (floor_day(when or self.now) - floor_day(self.start)).days

    def param(self, name: str):
        """A world value after `--no-faults` and fixture overrides."""
        if name in self.state["overrides"]:
            return self.state["overrides"][name]
        if name in ("build_fault_p", "rejection_p") and not self.state["faults_on"]:
            return 0.0
        return self.config.get(name)

    def attribute_names(self) -> list:
        return [a["name"] for a in self.config["attributes"]]

    def attribute_values(self, name: str) -> list:
        for a in self.config["attributes"]:
            if a["name"] == name:
                return list(a["values"])
        raise KeyError(name)

    def truth_attribute_names(self) -> list:
        """The attributes the long-run rate depends on: W5's `truth_attributes`, else all of them."""
        wanted = self.config.get("truth_attributes")
        return [n for n in self.attribute_names() if n in wanted] if wanted else self.attribute_names()

    def all_types(self, names=None) -> list:
        combos = [{}]
        for a in self.config["attributes"]:
            if names is not None and a["name"] not in names:
                continue
            combos = [dict(c, **{a["name"]: v}) for c in combos for v in a["values"]]
        return combos

    def type_of(self, attrs: dict, names=None) -> str:
        return "|".join(f"{name}={attrs.get(name)}" for name in (names or self.attribute_names()))

    @property
    def partial_builds(self) -> bool:
        return bool(self.config.get("partial_builds"))

    def quality_of(self, text: str) -> str:
        return text_quality(text, self.config)

    # -- the model ---------------------------------------------------------------------------------------------------

    def _logit(self, attrs: dict, quality: str) -> float:
        cfg = self.config
        qterm = {"specific": cfg["q"], "neutral": 0.0, "generic": -cfg["q"]}[quality]
        if "rates" in cfg:
            return logit(cfg["rates"][attrs[self.attribute_names()[0]]]) + qterm
        # an attribute with no effects entry (W5's nine coded but inert attributes) moves nothing
        x = cfg["base"] + sum(cfg["effects"].get(name, {}).get(attrs.get(name), 0.0) for name in self.attribute_names())
        for pocket in cfg.get("pockets", []):
            if all(attrs.get(k) == v for k, v in pocket["when"].items()):
                x += pocket["effect"]
        return x + qterm

    def long_run_rate(self, attrs: dict, quality: str = "neutral") -> float:
        """Paid worlds: the conversion rate without novelty, fatigue or weekday."""
        return sigmoid(self._logit(attrs, quality or "neutral"))

    def expected_follows(self, attrs: dict, quality: str = "neutral", slot_multiplier: float = 1.0) -> float:
        """W3: mean follows of a post of this type and text quality in a slot with this multiplier."""
        cfg = self.config
        mean = cfg["follows_base"]
        for name in self.attribute_names():
            mean *= cfg["multipliers"][name][attrs.get(name)]
        for pocket in cfg.get("pockets", []):
            if all(attrs.get(k) == v for k, v in pocket["when"].items()):
                mean *= pocket["multiplier"]
        return mean * cfg["quality_multipliers"][quality or "neutral"] * slot_multiplier

    def slot_multiplier(self, when: datetime) -> float:
        for slot in self.config.get("slots", []):
            if when.hour == slot["hour"]:
                return slot["multiplier"]
        return 1.0

    def true_rate(self, item: dict, hour: datetime) -> float:
        cfg = self.config
        rate = self.long_run_rate(item["attrs"], item["quality"])
        first = item.get("first_live")
        age = max(0, (hour - parse_time(first)) // DAY) if first else 0
        novelty = 1.0 + cfg.get("n0", 0.0) * math.exp(-age / 2.0)
        fatigue = max(0.6, 1.0 - cfg.get("f", 0.0) * max(0, age - 7))
        return min(1.0, rate * novelty * fatigue * cfg["weekday"][hour.weekday()])

    def truth(self) -> dict:
        """Types are written over the attributes the truth depends on (`type_attributes`): every attribute in W1 to W4,
        W5's hook, visual and offer (its other nine attributes move nothing, and their 11,664 combinations would only
        repeat each rate)."""
        names = self.truth_attribute_names()
        types = self.all_types(names)
        cfg = self.config
        out = {
            "world": self.world_id,
            "attributes": [{"name": a["name"], "values": list(a["values"])} for a in cfg["attributes"]],
            "type_attributes": list(names),
            "money_received": self.money_received(),
            "days": cfg.get("days"),
        }
        if self.paid:
            rates = {self.type_of(t, names): self.long_run_rate(t, "neutral") for t in types}
            best = max(types, key=lambda t: rates[self.type_of(t, names)])
            out.update(best_type=self.type_of(best, names), best_rate_specific=self.long_run_rate(best, "specific"),
                       type_rates=rates, cpc=cfg["cpc"], cap=cfg["cap"], cap_scope=cfg.get("cap_scope", "campaign"))
        else:
            follows = {self.type_of(t, names): self.expected_follows(t, "neutral", 1.0) for t in types}
            best = max(types, key=lambda t: follows[self.type_of(t, names)])
            out.update(best_type=self.type_of(best, names),
                       best_rate_specific=self.expected_follows(best, "specific", 1.0),
                       type_follows=follows, cpc=0.0, cap=cfg.get("posts_per_day", 3),
                       slot_multipliers={f"{s['hour']:02d}:00": s["multiplier"] for s in cfg.get("slots", [])})
        return out

    # -- faults ------------------------------------------------------------------------------------------------------

    def _active_fault(self, kind: str, target: str, when: datetime):
        for fault in self.state["faults"]:
            if fault["kind"] != kind or fault.get("target") not in ("*", target):
                continue
            if parse_time(fault["from"]) <= when < parse_time(fault["to"]):
                return fault
        return None

    def faults(self) -> list:
        """Every fault, a window fault on every live campaign listed once per campaign (or post) it touched."""
        out = []
        for fault in self.state["faults"]:
            base = {k: v for k, v in fault.items() if k != "source"}
            base["source"] = fault.get("source", "injected")
            if fault["kind"] == "build" or fault.get("target") != "*":
                out.append(base)
                continue
            start, end = parse_time(fault["from"]), parse_time(fault["to"])
            for cid in sorted(self.campaigns):
                if any(start <= parse_time(h) < end for h in self.state["records"].get(cid, {})):
                    out.append(dict(base, target=cid, scope="*"))
            if fault["kind"] == "delivery":
                for pid in sorted(self.posts):
                    if start <= parse_time(self.posts[pid]["slot"]) < end:
                        out.append(dict(base, target=pid, scope="*"))
        return out

    # -- records and money -------------------------------------------------------------------------------------------

    def _record(self, cid: str, hour: datetime):
        return self.state["records"].get(cid, {}).get(iso(hour))

    def hourly(self, campaign_or_post: str) -> list:
        ident = str(campaign_or_post)
        if ident in self.posts:
            result = self.state["post_results"].get(ident)
            return [dict(result)] if result else []
        if ident not in self.campaigns:
            return []
        cpc = self.config.get("cpc", 0.0)
        out = []
        for hour_text in sorted(self.state["records"].get(ident, {})):
            clicks, conv, platform, share, a0, a1, a2 = self.state["records"][ident][hour_text]
            hour = parse_time(hour_text)
            arrivals = [[iso(hour + d * DAY), n] for d, n in enumerate((a0, a1, a2)) if n]
            out.append({"hour": hour_text, "clicks": clicks, "conversions": conv, "platform_conversions": platform,
                        "spend": round(clicks * cpc, 2), "app_arrivals": arrivals, "target_share": share})
        return out

    def money_received(self) -> float:
        return round(self.state["money_start"] + sum(a for _t, a in self.state["grants"]), 2)

    def spend_between(self, since=None, until=None, cid=None) -> float:
        cpc = self.config.get("cpc", 0.0)
        lo = iso(since) if since else ""
        hi = iso(until) if until else "~"
        total = 0
        for c, recs in self.state["records"].items():
            if cid is not None and c != cid:
                continue
            total += sum(r[0] for h, r in recs.items() if lo <= h < hi)
        return round(total * cpc, 2)

    def spend_total(self) -> float:
        return self.spend_between()

    def balance(self) -> float:
        return round(self.money_received() - self.spend_total(), 2)

    def budget_at(self, cid: str, when: datetime):
        budget = None
        for t, value in self.campaigns[cid]["budget_events"]:
            if parse_time(t) <= when:
                budget = value
        return budget

    def status_at(self, cid: str, when: datetime):
        status = None
        for t, value in self.campaigns[cid].get("status_events", []):
            if parse_time(t) <= when:
                status = value
        return status

    def current_budget(self, cid: str):
        events = self.campaigns[cid]["budget_events"]
        return events[-1][1] if events else None

    def committed_live(self) -> list:
        return sorted(c for c, rec in self.campaigns.items() if rec["status"] == LIVE)

    # -- research material -------------------------------------------------------------------------------------------

    def library_entries(self) -> list:
        """The library as research material: shown fields plus the hidden `_type` (never printed)."""
        lib = self.config.get("library", {})
        kind = lib.get("kind")
        rng = random.Random(lib.get("seed", 0))
        out = []
        if kind == "ads":
            spec = lib["running_days"]
            for item in lib["items"]:
                rate = self.long_run_rate(item["type"], self.quality_of(item["text"]))
                raw = spec["offset"] + spec["scale"] * (rate - spec["center"]) + rng.gauss(0.0, spec["noise_sd"])
                days = int(max(spec["min"], min(spec["max"], round(raw))))
                out.append({"id": item["id"], "owner": item["owner"], "running_days": days, "text": item["text"],
                            "shows": item["shows"], "offer": item["offer"], "_type": item["type"]})
        elif kind == "keywords":
            name = self.attribute_names()[0]
            searches, bidding = lib["searches"], lib["bidding"]
            rows = []
            for group in self.attribute_values(name):
                rate = self.config["rates"][group]
                n = round(searches["scale"] * rng.lognormvariate(0.0, searches["sigma"]))
                b = round(bidding["offset"] + bidding["scale"] * (rate - bidding["center"])
                          + rng.gauss(0.0, bidding["noise_sd"]))
                rows.append({"phrase": self.config["phrases"][group], "searches": int(n),
                             "bidding": int(max(bidding["min"], min(bidding["max"], b))), "_type": {name: group}})
            rows.sort(key=lambda r: r["phrase"])
            for index, row in enumerate(rows, 1):
                out.append(dict(row, id=f"lib_{index:02d}"))
        elif kind == "posts":
            likes = lib["likes"]
            for item in lib["items"]:
                mean = self.expected_follows(item["type"], "neutral", 1.0)
                count = round(likes["per_follow"] * mean * rng.lognormvariate(0.0, likes["sigma"]))
                out.append({"id": item["id"], "account": item["account"], "likes": int(count),
                            "caption": item["caption"], "shows": item["shows"], "_type": item["type"]})
        return out

    # -- soft signals (PLAN.md 13.2): the hidden reception, never shown to agents ----------------------------------

    @property
    def reception(self) -> dict:
        return self.config.get("reception") or {}

    def item_reception(self, item: dict):
        """(the text's quality, whether the text overpromises): the hidden rules an item's comments, saves and hides
        are drawn from. Generic copy draws spam call-outs and few questions, specific copy questions and saves, and
        copy that overpromises draws complaints that call it misleading, whatever it converts."""
        low = str(item.get("text") or "").lower()
        overpromise = any(p in low for p in self.reception.get("overpromise_phrases") or [])
        return item.get("quality") or self.quality_of(item.get("text")), overpromise

    def _exposures(self, ident: str, since=None, until=None) -> list:
        """[(hour, exposure)] in [since, until): a campaign's clicks per recorded hour, or a post's reach."""
        def inside(hour_text):
            hour = parse_time(hour_text)
            return (since is None or hour >= since) and (until is None or hour < until)

        if ident in self.posts:
            result = self.state["post_results"].get(ident)
            return [(result["hour"], int(result.get("reach", 0)))] if result and inside(result["hour"]) else []
        return [(h, rec[0]) for h, rec in sorted(self.state["records"].get(ident, {}).items()) if rec[0] > 0
                and inside(h)]

    def _item_of(self, ident: str):
        record = self.campaigns.get(ident) or self.posts.get(ident) or {}
        return self.items.get(record.get("item"))

    def _hour_comments(self, ident: str, hour: str, exposure: int, quality: str, overpromise: bool) -> list:
        rec = self.reception
        rng = seeded(self.seed, "comments", ident, hour)
        count = poisson(rng, exposure * float(rec.get("comment_rate", 0.0)))
        kinds, weights = list(rec["kinds"]), [float(w) for w in rec["mix"][quality]]
        if overpromise:
            share, at = float(rec["overpromise_complaint_share"]), kinds.index("complaint")
            rest = sum(w for i, w in enumerate(weights) if i != at)
            weights = [share if i == at else w * (1.0 - share) / rest for i, w in enumerate(weights)]
        out = []
        for _ in range(count):
            u, acc, kind = rng.random() * sum(weights), 0.0, kinds[-1]
            for name, weight in zip(kinds, weights):
                acc += weight
                if u < acc:
                    kind = name
                    break
            pool = rec["samples"]["misleading" if kind == "complaint" and overpromise else kind]
            out.append({"hour": hour, "kind": kind, "text": pool[rng.randrange(len(pool))]})
        return out

    def _hour_saves_hides(self, ident: str, hour: str, exposure: int, quality: str, overpromise: bool):
        rec = self.reception
        hide = rec["overpromise_hide_rate"] if overpromise else rec["hide_rate"][quality]
        return (poisson(seeded(self.seed, "saves", ident, hour), exposure * float(rec["save_rate"][quality])),
                poisson(seeded(self.seed, "hides", ident, hour), exposure * float(hide)))

    def comments(self, ident: str, since=None, until=None) -> list:
        """[{hour, kind, text}] for a campaign or post over [since, until); [] in a world without reception."""
        item = self._item_of(ident)
        if not self.reception or item is None:
            return []
        quality, overpromise = self.item_reception(item)
        out = []
        for hour, exposure in self._exposures(ident, since, until):
            out += self._hour_comments(ident, hour, exposure, quality, overpromise)
        return out

    def saves_hides(self, ident: str, since=None, until=None):
        """(saves, hides) for a campaign or post over [since, until); (0, 0) in a world without reception."""
        item = self._item_of(ident)
        if not self.reception or item is None:
            return 0, 0
        quality, overpromise = self.item_reception(item)
        saves = hides = 0
        for hour, exposure in self._exposures(ident, since, until):
            s, h = self._hour_saves_hides(ident, hour, exposure, quality, overpromise)
            saves, hides = saves + s, hides + h
        return saves, hides

    def history_rows(self):
        """(columns, rows) of the world's `history.csv`, or None when it has none."""
        hist = self.config.get("history")
        if not hist:
            return None
        cpc = self.config["cpc"]
        if "rows" in hist:
            rows = []
            for row in hist["rows"]:
                rows.append(dict(row, spend=f"{row['clicks'] * cpc:.2f}"))
            return hist["columns"], rows
        rng = random.Random(hist["seed"])
        name = self.attribute_names()[0]
        first = parse_time(hist["first_bought"])
        rows = []
        for index, group in enumerate(hist["groups"]):
            clicks = rng.randint(hist["clicks_min"], hist["clicks_max"])
            conversions = binomial(rng, clicks, self.long_run_rate({name: group}, "neutral"))
            began = first + (index % 7) * DAY
            rows.append({"group": group, "clicks": clicks, "conversions": conversions,
                         "spend": f"{clicks * cpc:.2f}", "first_bought": began.strftime("%Y-%m-%d"),
                         "last_bought": (began + hist["span_days"] * DAY).strftime("%Y-%m-%d")})
        return hist["columns"], rows

    # -- ids and argument checks -------------------------------------------------------------------------------------

    def _next_id(self, prefix: str) -> str:
        self.state["counters"][prefix] += 1
        return f"{prefix}_{self.state['counters'][prefix]:04d}"

    def _bump_counter(self, ident: str) -> None:
        prefix, _, number = str(ident).partition("_")
        if prefix in self.state["counters"] and number.isdigit():
            self.state["counters"][prefix] = max(self.state["counters"][prefix], int(number))

    def _check_attrs(self, attrs, partial: bool = False) -> dict:
        """The attributes of a build request, in catalog order. W1 to W4 need every attribute; `partial` (W5) takes
        any of them."""
        names = self.attribute_names()
        example = json.dumps({n: self.attribute_values(n)[0] for n in (names[:2] if partial else names)})
        if not isinstance(attrs, dict):
            raise SimError(f"--attrs must be a JSON object such as '{example}'.")
        unknown = [k for k in attrs if k not in names]
        missing = [n for n in names if n not in attrs]
        if partial and unknown:
            raise SimError(f"--attrs takes only these attributes: {', '.join(names)} (for example '{example}').")
        if not partial and (unknown or missing):
            raise SimError(f"--attrs needs exactly these attributes: {', '.join(names)} (for example '{example}').")
        for name in names:
            if name in attrs and attrs[name] not in self.attribute_values(name):
                raise SimError(f"{name} must be one of: {', '.join(self.attribute_values(name))}.")
        return {n: attrs[n] for n in names if n in attrs}

    def _check_budget(self, budget) -> float:
        low, high = self.config["budget_min"], self.config["budget_max"]
        try:
            value = float(str(budget).replace("$", "").replace(",", "").strip())
        except ValueError:
            raise SimError(f"A daily budget is a number of dollars from {low} to {high}.") from None
        if not low <= value <= high:
            raise SimError(f"A daily budget must be from ${low:.2f} to ${high:.2f}.")
        return round(value, 2)

    def _campaign(self, cid: str) -> dict:
        if cid not in self.campaigns:
            raise SimError(f"There is no campaign {cid}.")
        return self.campaigns[cid]

    def _set_status(self, cid: str, status: str, when: datetime) -> None:
        record = self.campaigns[cid]
        events = record.setdefault("status_events", [])
        events.append([iso(when), status])
        events.sort(key=lambda e: e[0])
        record["status"] = events[-1][1]

    def _went_live(self, iid: str, when: datetime) -> None:
        item = self.items[iid]
        if not item.get("first_live") or parse_time(item["first_live"]) > when:
            item["first_live"] = iso(when)

    def _need_paid(self) -> None:
        if not self.paid:
            raise SimError("This account has no paid campaigns; it posts built items into free slots "
                           "(sim slots, then sim post ITEM --at ISO).")

    # -- agent-facing commands that change state -----------------------------------------------------------------------

    def build(self, attrs, text, at=None, fault=None, item_id=None, draw_fault=True, from_item=None) -> str:
        """Build an item. W1 to W4 take every attribute and the text. W5 (`partial_builds`) takes any of its
        attributes and draws each one left out at random, as making the video from scratch would; with `from_item`
        it starts from that item's values and text and changes only what is given. A build fault, drawn or forced,
        gives one requested attribute another value; `sim manifest` shows what was built."""
        partial = self.partial_builds
        if from_item is not None and not partial:
            raise SimError("This platform builds every item from scratch; give every attribute with --attrs.")
        attrs = self._check_attrs({} if attrs is None else attrs, partial=partial)
        parent = None
        if from_item is not None:
            parent = self.items.get(from_item)
            if parent is None:
                raise SimError(f"There is no item {from_item} to build from.")
        text = str(text or "").strip() or (parent["text"] if parent else "")
        if not text:
            raise SimError("--text is required: the words of the item.")
        when = parse_time(at) if at else self.now
        if item_id:
            if item_id in self.items:
                raise SimError(f"{item_id} already exists.")
            self._bump_counter(item_id)
            iid = item_id
        else:
            iid = self._next_id("it")
        names = self.attribute_names()
        requested = dict(parent["attrs"], **attrs) if parent is not None else dict(attrs)
        requested = {n: requested[n] for n in names if n in requested}
        built, changed, drawn = dict(requested), None, []
        if partial and parent is None:
            rng = seeded(self.seed, "draw", iid, floor_hour(when))
            for name in names:
                if name not in built:
                    built[name] = rng.choice(self.attribute_values(name))
                    drawn.append(name)
            built = {n: built[n] for n in names}
        if fault:
            for name, value in fault.items():
                if value not in self.attribute_values(name):
                    raise SimError(f"fault value {value!r} is not a value of {name}")
                built[name] = value
                changed = name
        elif draw_fault:
            p = float(self.param("build_fault_p") or 0.0)
            rng = seeded(self.seed, "build", iid, floor_hour(when))
            if p > 0 and rng.random() < p:
                pool = list(self.config.get("build_fault_attrs") or names)
                if partial:
                    pool = [n for n in pool if n in requested]   # a value drawn for an unrequested attribute is no fault
                if pool:
                    changed = rng.choice(pool)
                    built[changed] = rng.choice([v for v in self.attribute_values(changed) if v != requested[changed]])
        record = {"requested": requested, "attrs": built, "text": text, "quality": self.quality_of(text),
                  "built_at": iso(when), "first_live": None}
        if partial:
            record.update(made_from=from_item, drawn=drawn)
        self.items[iid] = record
        if changed and built[changed] != requested.get(changed):
            self.state["faults"].append({"kind": "build", "target": iid, "from": iso(when), "to": iso(when),
                                         "attr": changed, "requested": requested.get(changed), "built": built[changed],
                                         "source": "forced" if fault else "drawn"})
        return iid

    def launch(self, iid: str, budget, at=None, cid=None, review=True, status=None):
        """(campaign id, went live). A rejected launch leaves a `rejected` campaign that `resubmit` can retry."""
        self._need_paid()
        if iid not in self.items:
            raise SimError(f"There is no item {iid}; build one with sim build.")
        budget = self._check_budget(budget)
        when = parse_time(at) if at else self.now
        if review and self.balance() < self.config["cpc"]:
            raise SimError(f"The balance is ${self.balance():.2f}; nothing can launch until money is added.")
        if cid:
            if cid in self.campaigns:
                raise SimError(f"{cid} already exists.")
            self._bump_counter(cid)
        else:
            cid = self._next_id("cp")
        if status == REJECTED:
            rejected = True
        elif review:
            p = float(self.param("rejection_p") or 0.0)
            rejected = seeded(self.seed, "review", f"{cid}#1", floor_hour(when)).random() < p
        else:
            rejected = False
        self.campaigns[cid] = {"item": iid, "status": REJECTED if rejected else LIVE,
                               "budget_events": [[iso(when), budget]],
                               "launched_at": None if rejected else iso(when), "status_events": [],
                               "review_attempts": 1}
        self._set_status(cid, REJECTED if rejected else LIVE, when)
        if not rejected:
            self._went_live(iid, when)
        return cid, not rejected

    def resubmit(self, cid: str) -> bool:
        self._need_paid()
        record = self._campaign(cid)
        if record["status"] != REJECTED:
            raise SimError(f"{cid} is {record['status']}; only a rejected campaign can be resubmitted.")
        if self.balance() < self.config["cpc"]:
            raise SimError(f"The balance is ${self.balance():.2f}; nothing can launch until money is added.")
        record["review_attempts"] = record.get("review_attempts", 1) + 1
        p = float(self.param("rejection_p") or 0.0)
        ok = seeded(self.seed, "review", f"{cid}#{record['review_attempts']}", floor_hour(self.now)).random() >= p
        if ok:
            self._set_status(cid, LIVE, self.now)
            if not record.get("launched_at"):
                record["launched_at"] = iso(self.now)
            self._went_live(record["item"], self.now)
        return ok

    def pause(self, cid: str, at=None) -> bool:
        record = self._campaign(cid)
        when = parse_time(at) if at else self.now
        if record["status"] == REJECTED and at is None:
            raise SimError(f"{cid} was rejected by review and is not running; resubmit it or leave it.")
        if self.status_at(cid, when) == PAUSED:
            return False
        self._set_status(cid, PAUSED, when)
        return True

    def resume(self, cid: str, at=None) -> bool:
        self._need_paid()
        record = self._campaign(cid)
        when = parse_time(at) if at else self.now
        if record["status"] == LIVE and at is None:
            return False
        if record["status"] == REJECTED and at is None:
            raise SimError(f"{cid} was rejected by review; retry with: sim resubmit {cid}")
        if at is None and self.balance() < self.config["cpc"]:
            raise SimError(f"The balance is ${self.balance():.2f}; campaigns cannot run until money is added.")
        self._set_status(cid, LIVE, when)
        if not record.get("launched_at"):
            record["launched_at"] = iso(when)
        self._went_live(record["item"], when)
        return True

    def set_budget(self, cid: str, budget, at=None) -> float:
        self._need_paid()
        record = self._campaign(cid)
        value = self._check_budget(budget)
        record["budget_events"].append([iso(parse_time(at) if at else self.now), value])
        record["budget_events"].sort(key=lambda e: e[0])
        return value

    def free_slots(self, hours: int = 48) -> list:
        if self.paid:
            return []
        taken = {p["slot"] for p in self.posts.values()}
        end = self.now + hours * HOUR
        out, day = [], floor_day(self.now)
        while day <= end:
            for slot in self.config["slots"]:
                t = day.replace(hour=slot["hour"])
                if self.now < t <= end and iso(t) not in taken:
                    out.append(t)
            day += DAY
        return out

    def post(self, iid: str, at, pid=None, check=True) -> str:
        if self.paid:
            raise SimError("This account runs paid campaigns; launch a built item with: sim launch ITEM --daily-budget N")
        if iid not in self.items:
            raise SimError(f"There is no item {iid}; build one with sim build.")
        slot = parse_time(at)
        if check and iso(slot) not in {iso(s) for s in self.free_slots()}:
            raise SimError(f"{iso(slot)} is not a free slot in the next 48 hours; see the free ones with: sim slots")
        if pid:
            self._bump_counter(pid)
        else:
            pid = self._next_id("po")
        self.posts[pid] = {"item": iid, "slot": iso(slot), "status": "scheduled", "scheduled_at": iso(self.now)}
        return pid

    def followers(self, until=None) -> int:
        until = until or self.now
        total = int(self.config.get("followers_start", 0))
        for result in self.state["post_results"].values():
            total += sum(n for at, n in result.get("arrivals", []) if parse_time(at) <= until)
        return total

    # -- the clock (lab only) ------------------------------------------------------------------------------------------

    def advance(self, hours: int) -> None:
        for _ in range(int(hours)):
            hour = floor_hour(self.now)
            if self.paid:
                self._simulate_hour(hour)
            else:
                self._realize_posts(hour)
            self.now = hour + HOUR

    def grant(self, amount) -> None:
        self.state["grants"].append([iso(self.now), round(float(amount), 2)])
        if self.paid and self.balance() >= self.config["cpc"]:
            for cid, record in sorted(self.campaigns.items()):
                if record["status"] == EXHAUSTED:
                    self._set_status(cid, LIVE, self.now)

    def _simulate_hour(self, hour: datetime) -> None:
        live = self.committed_live()
        if not live:
            return
        cfg = self.config
        cpc, cap = cfg["cpc"], cfg["cap"]
        balance = self.balance()
        budgets = {cid: self.current_budget(cid) for cid in live}
        group_name = self.attribute_names()[0]
        group_total = {}
        if cfg.get("cap_scope") == "group":
            for cid in live:
                group = self.items[self.campaigns[cid]["item"]]["attrs"][group_name]
                group_total[group] = group_total.get(group, 0.0) + budgets[cid]
        day = floor_day(hour)
        p0, p1 = (cfg.get("app_lag_p") or [1.0, 0.0, 0.0])[:2]
        records = self.state["records"]
        for cid in live:
            item = self.items[self.campaigns[cid]["item"]]
            budget = budgets[cid]
            cap_c = cap * budget / group_total[item["attrs"][group_name]] if group_total else cap
            clicks = poisson(seeded(self.seed, "clicks", cid, hour), min(budget / 24.0 / cpc, cap_c / 24.0))
            so_far = sum(r[0] for h, r in records.get(cid, {}).items() if iso(day) <= h < iso(hour))
            allowance = int(math.floor(min(budget / cpc, cap_c) + 1e-9)) - so_far
            clicks = max(0, min(clicks, allowance, int(math.floor(balance / cpc + 1e-9))))
            balance = round(balance - clicks * cpc, 2)
            delivery = self._active_fault("delivery", cid, hour)
            rate = self.true_rate(item, hour) * (DELIVERY_RATE if delivery else 1.0)
            share = float(delivery.get("target_share", SHARE_FAULT)) if delivery else SHARE_NORMAL
            conv = binomial(seeded(self.seed, "conversions", cid, hour), clicks, rate)
            tracking = self._active_fault("tracking", cid, hour)
            platform = binomial(seeded(self.seed, "tracking", cid, hour), conv, tracking["factor"]) if tracking else conv
            lags, rng = [0, 0, 0], seeded(self.seed, "app", cid, hour)
            for _ in range(conv):
                u = rng.random()
                lags[0 if u < p0 else 1 if u < p0 + p1 else 2] += 1
            records.setdefault(cid, {})[iso(hour)] = [clicks, conv, platform, share] + lags
        if balance < cpc:
            for cid in live:
                self._set_status(cid, EXHAUSTED, hour + HOUR)

    def _realize_posts(self, hour: datetime) -> None:
        cfg = self.config
        for pid in sorted(self.posts):
            post = self.posts[pid]
            if post["status"] != "scheduled" or not hour <= parse_time(post["slot"]) < hour + HOUR:
                continue
            item = self.items[post["item"]]
            mean = self.expected_follows(item["attrs"], item["quality"], self.slot_multiplier(hour))
            delivery = self._active_fault("delivery", pid, hour)
            if delivery:
                mean *= DELIVERY_RATE
            follows = poisson(seeded(self.seed, "follows", pid, hour), mean)
            spread_draw = seeded(self.seed, "reach", pid, hour).lognormvariate(0.0, cfg["reach"]["sigma"])
            reach = int(round(follows * cfg["reach"]["per_follow"] * spread_draw))
            rng = seeded(self.seed, "followers", pid, hour)
            at_once = sum(1 for _ in range(follows) if rng.random() < cfg["follower_lag_p"][0])
            self.state["post_results"][pid] = {
                "hour": iso(hour), "follows": follows, "reach": reach, "platform_follows": follows,
                "target_share": float(delivery.get("target_share", SHARE_FAULT)) if delivery else SHARE_NORMAL,
                "arrivals": [[iso(hour), at_once], [iso(hour + DAY), follows - at_once]]}
            post["status"] = "done"

    # -- fixtures (lab only) -------------------------------------------------------------------------------------------

    def record(self, cid: str, start, end, clicks: int, conversions: int, platform_conversions=None,
               app_lag: str = "none", target_share: float = SHARE_NORMAL) -> None:
        """Exact numbers for a campaign's hours in [start, end), spread evenly; replaces earlier records there."""
        self._campaign(cid)
        hours = list(hours_between(parse_time(start), parse_time(end)))
        platform = conversions if platform_conversions is None else platform_conversions
        if not hours:
            raise SimError(f"record for {cid}: the window {start} to {end} holds no hour")
        if not 0 <= platform <= conversions <= clicks:
            raise SimError(f"record for {cid}: need platform <= conversions <= clicks")
        per_clicks = spread(int(clicks), len(hours))
        per_conv = pick_evenly(int(conversions), per_clicks)
        per_platform = pick_evenly(int(platform), per_conv)
        p0, p1 = (self.config.get("app_lag_p") or [1.0, 0.0, 0.0])[:2]
        records = self.state["records"].setdefault(cid, {})
        for hour, k, conv, plat in zip(hours, per_clicks, per_conv, per_platform):
            lags = [conv, 0, 0]
            if app_lag not in (None, "none"):
                lags, rng = [0, 0, 0], seeded(self.seed, "app", cid, hour)
                for _ in range(conv):
                    u = rng.random()
                    lags[0 if u < p0 else 1 if u < p0 + p1 else 2] += 1
            records[iso(hour)] = [k, conv, plat, float(target_share)] + lags

    def inject(self, kind: str, target: str, start, end, factor=None, target_share=None) -> None:
        fault = {"kind": kind, "target": target, "from": iso(parse_time(start)), "to": iso(parse_time(end)),
                 "source": "injected"}
        if kind == "tracking":
            fault["factor"] = float(0.3 if factor is None else factor)
        elif kind == "delivery":
            fault["target_share"] = float(SHARE_FAULT if target_share is None else target_share)
        else:
            raise SimError(f"unknown fault kind {kind!r}")
        self.state["faults"].append(fault)

    def apply_ops(self, ops) -> None:
        for op in ops:
            kind = op.get("op")
            at = op.get("at")
            if kind == "build":
                self.build(op.get("attrs"), op.get("text"), at=at or self.state["now"], fault=op.get("fault"),
                           item_id=op.get("id"), draw_fault=False, from_item=op.get("from"))
            elif kind == "launch":
                self.launch(op["item"], op["daily_budget"], at=at, cid=op.get("id"), review=False,
                            status=op.get("status"))
            elif kind == "record":
                self.record(op["campaign"], op["from"], op["to"], op["clicks"], op["conversions"],
                            op.get("platform_conversions"), op.get("app_lag", "none"),
                            op.get("target_share", SHARE_NORMAL))
            elif kind == "inject":
                self.inject(op["fault"], op.get("campaign") or op.get("post") or op.get("target", "*"), op["from"],
                            op["to"], op.get("factor"), op.get("target_share"))
            elif kind == "set-budget":
                self.set_budget(op["campaign"], op["daily_budget"], at=at)
            elif kind == "pause":
                self.pause(op["campaign"], at=at)
            elif kind == "resume":
                self.resume(op["campaign"], at=at)
            elif kind == "post":
                self.post(op["item"], op["slot"], pid=op.get("id"), check=False)
            elif kind == "grant":
                self.state["grants"].append([iso(parse_time(at or self.state["now"])), round(float(op["amount"]), 2)])
            elif kind == "now":
                self.now = at
            else:
                raise SimError(f"unknown op {kind!r}")

    def _cap_share(self, cid: str, when: datetime) -> float:
        cfg = self.config
        if cfg.get("cap_scope") != "group":
            return float(cfg["cap"])
        name = self.attribute_names()[0]
        group = self.items[self.campaigns[cid]["item"]]["attrs"][name]
        total = sum(self.budget_at(other, when) or 0.0 for other, rec in self.campaigns.items()
                    if self.items[rec["item"]]["attrs"][name] == group and self.status_at(other, when) == LIVE)
        return cfg["cap"] * (self.budget_at(cid, when) or 0.0) / total if total else float(cfg["cap"])

    def validate(self) -> list:
        """Problems that make a fixture impossible: unrecorded live hours, records outside live hours or after now,
        counts out of order, a day's clicks beyond what the budget and cap allow over the hours it was live, or spend
        beyond the money received. This checks exact fixture records; simulated hours are Poisson draws that the
        simulator clamps to each day's budget and cap, so a simulated partial day can sit a few clicks above the
        prorated allowance used here."""
        if not self.paid:
            return []
        problems = []
        cpc, now = self.config["cpc"], self.now
        for cid, record in sorted(self.campaigns.items()):
            recs = self.state["records"].get(cid, {})
            events = record.get("status_events") or []
            if events:
                for hour in hours_between(parse_time(events[0][0]), now):
                    live = self.status_at(cid, hour) == LIVE
                    rec = recs.get(iso(hour))
                    if live and rec is None:
                        problems.append(f"{cid} is live at {iso(hour)} but has no record there")
                        break
                    if not live and rec is not None and rec[0] > 0:
                        problems.append(f"{cid} has clicks at {iso(hour)} while {self.status_at(cid, hour)}")
                        break
            days = {}
            for hour_text, rec in sorted(recs.items()):
                hour = parse_time(hour_text)
                if hour >= now:
                    problems.append(f"{cid} has a record at {hour_text}, at or after now")
                    break
                if not 0 <= rec[2] <= rec[1] <= rec[0]:
                    problems.append(f"{cid} at {hour_text}: counts out of order {rec[:3]}")
                day = days.setdefault(hour_text[:10], [0, 0.0])
                day[0] += rec[0]
                if self.status_at(cid, hour) == LIVE:
                    budget = self.budget_at(cid, hour) or 0.0
                    day[1] += min(budget / 24.0 / cpc, self._cap_share(cid, hour) / 24.0)
            for day, (clicks, allowed) in sorted(days.items()):
                if clicks > allowed + 1e-6:
                    problems.append(f"{cid} has {clicks} clicks on {day}; its budget and the cap allow {allowed:.2f}")
        if self.balance() < -1e-6:
            problems.append(f"recorded spend ${self.spend_total():.2f} exceeds the money received "
                            f"${self.money_received():.2f}")
        return problems
