"""A stand-in for `sim.world.World` (INTERFACES.md) used by the grader tests.

The golden run folders keep `hidden/world_stub.json` instead of the simulator's `state.json`, so the graders can be
tested before and apart from the simulator. The stub exposes the same read-only surface the graders use: `now`,
`config`, `items`, `campaigns`, `posts`, `hourly()`, `type_of()`, `long_run_rate()`, `expected_follows()`, `truth()`,
`faults()` and `balance()`. Rates follow PLAN.md 6.2, 6.3 and 13.2 for the parameters in `config`; a config's
`truth_attributes` (W5) names the attributes its types are written over.
"""
from __future__ import annotations

import itertools
import json
import math
from datetime import datetime, timezone
from pathlib import Path

QUALITY_TERMS = {"specific": 1, "neutral": 0, "generic": -1}
W3_QUALITY = {"specific": 1.3, "neutral": 1.0, "generic": 0.75}


def _parse(value):
    if isinstance(value, datetime):
        return value
    text = str(value).replace("Z", "+00:00")
    stamp = datetime.fromisoformat(text)
    return stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


class StubWorld:
    def __init__(self, data: dict):
        self.data = data
        self.now = _parse(data.get("now", "2026-11-08T00:00:00Z"))
        self.config = data.get("config") or {}
        self.items = data.get("items") or {}
        self.campaigns = data.get("campaigns") or {}
        self.posts = data.get("posts") or {}
        self._hourly = data.get("hourly") or {}
        self._faults = data.get("faults") or []
        self._truth = data.get("truth") or {}

    @classmethod
    def load(cls, hidden) -> "StubWorld":
        return cls(json.loads((Path(hidden) / "world_stub.json").read_text(encoding="utf-8")))

    # ----- the World surface -----
    def hourly(self, campaign_or_post):
        return list(self._hourly.get(campaign_or_post, []))

    def attributes(self):
        return list((self.config.get("attributes") or {}).keys())

    def type_of(self, attrs: dict) -> str:
        return "|".join(f"{name}={attrs.get(name)}" for name in self.attributes())

    def long_run_rate(self, attrs: dict, quality: str) -> float:
        cfg = self.config
        q = float(cfg.get("q", 0.0)) * QUALITY_TERMS.get(quality, 0)
        if "group_rates" in cfg:
            rate = float(cfg["group_rates"][attrs.get("group")])
            return sigmoid(math.log(rate / (1 - rate)) + q)
        logit = float(cfg.get("base", 0.0))
        for name, effects in (cfg.get("effects") or {}).items():
            logit += float(effects.get(attrs.get(name), 0.0))
        for pocket in cfg.get("pockets") or []:
            if all(attrs.get(k) == v for k, v in pocket["when"].items()):
                logit += float(pocket["effect"])
        return sigmoid(logit + q)

    def expected_follows(self, attrs: dict, quality: str, slot_multiplier: float = 1.0) -> float:
        cfg = self.config
        mean = float(cfg.get("follows_base", 6.0))
        for name, factors in (cfg.get("factors") or {}).items():
            mean *= float(factors.get(attrs.get(name), 1.0))
        for pocket in cfg.get("pockets") or []:
            if all(attrs.get(k) == v for k, v in pocket["when"].items()):
                mean *= float(pocket["effect"])
        return mean * W3_QUALITY.get(quality, 1.0) * slot_multiplier

    def balance(self) -> float:
        """The platform's balance: the stub's `balance` when given, else money received less recorded spend."""
        if "balance" in self.data:
            return float(self.data["balance"])
        spend = sum(float(h.get("spend", 0) or 0) for hours in self._hourly.values() for h in hours)
        return round(float(self._truth.get("money_received") or 0) - spend, 2)

    def all_types(self):
        attrs = self.config.get("attributes") or {}
        names = [n for n in attrs if n in self.config.get("truth_attributes", attrs)]
        for combo in itertools.product(*(attrs[n] for n in names)):
            yield dict(zip(names, combo))

    def truth(self) -> dict:
        out = dict(self._truth)
        follows = "factors" in self.config
        rates = {}
        names = [n for n in self.attributes() if n in self.config.get("truth_attributes", self.attributes())]
        for attrs in self.all_types():
            value = self.expected_follows(attrs, "neutral") if follows else self.long_run_rate(attrs, "neutral")
            rates["|".join(f"{n}={attrs.get(n)}" for n in names)] = value
        if rates:
            best = max(rates, key=rates.get)
            best_attrs = dict(part.split("=", 1) for part in best.split("|"))
            out.setdefault("best_type", best)
            out.setdefault("best_rate_specific", self.expected_follows(best_attrs, "specific") if follows
                           else self.long_run_rate(best_attrs, "specific"))
            out.setdefault("type_follows" if follows else "type_rates", rates)
        out.setdefault("attributes", [{"name": name, "values": list(values)}
                                      for name, values in (self.config.get("attributes") or {}).items()])
        out.setdefault("days", self.config.get("days"))
        if follows:
            out.setdefault("cpc", 0.0)
            out.setdefault("cap", 3)
            out.setdefault("slot_multipliers", {"09:00": 0.9, "13:00": 1.0, "19:00": 1.15})
        else:
            out.setdefault("cpc", self.config.get("cpc", 0.10))
            out.setdefault("cap", self.config.get("cap", 300))
            out.setdefault("cap_scope", self.config.get("cap_scope", "campaign"))
        return out

    def faults(self):
        return list(self._faults)


W1_CONFIG = {
    "name": "W1", "days": 14,
    "attributes": {"hook": ["claim", "question", "story"], "visual": ["app-screen", "hand-replay", "coach-face"],
                   "offer": ["free-trial", "discount", "none"]},
    "base": -3.2,
    "effects": {"hook": {"question": 0.15, "story": -0.10}, "visual": {"app-screen": 0.30, "coach-face": -0.20},
                "offer": {"free-trial": 0.20, "discount": 0.10}},
    "pockets": [{"when": {"hook": "story", "visual": "coach-face"}, "effect": 1.0}],
    "q": 0.25, "cpc": 0.10, "cap": 300,
}

W3_CONFIG = {
    "name": "W3", "days": 10,
    "attributes": {"format": ["clip", "carousel", "meme"], "topic": ["hand-review", "rules-tip", "player-story"]},
    "follows_base": 6.0,
    "factors": {"format": {"clip": 1.2, "carousel": 1.0, "meme": 0.9},
                "topic": {"hand-review": 1.1, "rules-tip": 1.15, "player-story": 0.85}},
    "pockets": [{"when": {"format": "meme", "topic": "player-story"}, "effect": 2.2}],
}

W5_CONFIG = {
    "name": "W5", "days": 14,
    "attributes": {"hook": ["question", "story", "claim", "challenge"],
                   "visual": ["app-screen", "hand-replay", "table-footage"], "offer": ["free-trial", "discount", "none"],
                   "presenter": ["coach", "player", "none"], "voice": ["calm", "energetic"],
                   "music": ["none", "lo-fi", "upbeat", "cinematic"], "captions": ["burned-in", "none"],
                   "length": ["15s", "30s", "60s"], "opening": ["face", "cards", "text-card"],
                   "closing_ask": ["download", "try-free", "learn-more"], "palette": ["dark", "bright", "felt-green"],
                   "format": ["vertical", "square", "horizontal"]},
    "truth_attributes": ["hook", "visual", "offer"],
    "base": -3.1,
    "effects": {"hook": {"question": 0.10, "claim": -0.05, "challenge": 0.25},
                "visual": {"app-screen": 0.15, "hand-replay": 0.30}, "offer": {"free-trial": 0.20, "discount": 0.05}},
    "pockets": [], "q": 0.25, "cpc": 0.10, "cap": 300,
}
