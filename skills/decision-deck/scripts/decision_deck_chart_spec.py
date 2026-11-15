"""Decision deck spec: the chart evidence kind's keys, checked (decision_deck_spec._chart calls check_chart).

The keys are documented once, in decision_deck.py's --help (decision_deck_help.py); drawn by decision_deck_chart.py:
"bars" [{"label", "value" (0 or more), "emphasis"? (on at most one bar), "note"?}], "unit"?, "source"?, "side"?,
"prefix"? (before each value, such as "$"), "decimals"? (0 to 4), "series"? (two names; each bar then gives "values",
one number per series, and no "value"), and "type"? ("bar", the default, or "line": the bars are the points of an
ordered series, any number, at least 2). A line is refused when its first and last x labels and its longest value
would leave its phone drawing under decision_deck_chart.LINE_PLOT_MIN px of plot.
"""
from __future__ import annotations

import math

TYPES = ("bar", "line")
PREFIX_MAX = 3                  # characters: "$", "€", "US$"
DECIMALS_MAX = 4
SERIES_N = 2                    # a before/after pair
LINE_MIN = 2
LINE_LABEL_HINT = 20            # characters: two end labels this long leave a phone line room (decision_deck_chart)


def _number(val) -> bool:
    return isinstance(val, (int, float)) and not isinstance(val, bool) and math.isfinite(val)


def _str(obj: dict, key: str, where: str, errors: list, required: bool = False) -> None:
    if key not in obj and not required:
        return
    val = obj.get(key)
    if not isinstance(val, str) or not val.strip():
        errors.append(f"{where}: '{key}' must be a non-empty string")


def _bar(bar: dict, bw: str, line: bool, series: list | None, errors: list) -> None:
    _str(bar, "label", bw, errors, required=True)
    least = "a number" if line else "a number of 0 or more"
    ok = (lambda v: _number(v)) if line else (lambda v: _number(v) and v >= 0)
    if series:
        vals = bar.get("values")
        if not isinstance(vals, list) or len(vals) != len(series) or not all(ok(v) for v in vals):
            errors.append(f"{bw}: 'values' must be a list of {len(series)} numbers, one per series"
                          f"{'' if line else ', each 0 or more'}")
        if "value" in bar:
            errors.append(f"{bw}: give 'values' (one per series), not 'value'")
        if "emphasis" in bar:
            errors.append(f"{bw}: 'emphasis' is for one series; with 'series' the second one is drawn in the accent")
    else:
        if not ok(bar.get("value")):
            errors.append(f"{bw}: 'value' must be {least}")
        if "emphasis" in bar and not isinstance(bar["emphasis"], bool):
            errors.append(f"{bw}: 'emphasis' must be true or false")
    if "note" in bar:
        if line:
            errors.append(f"{bw}: 'note' is for a bar chart; a line's points carry no note")
        else:
            _str(bar, "note", bw, errors)


def check_chart(ev: dict, ew: str, errors: list) -> None:
    """Append a problem for each chart key that breaks the schema above."""
    before = len(errors)
    _keys(ev, ew, errors)
    if ev.get("type") == "line" and len(errors) == before:
        _line_room(ev, ew, errors)


def _line_room(ev: dict, ew: str, errors: list) -> None:
    """A valid line whose first and last x labels and longest value leave the phone's drawing too little plot."""
    from decision_deck_chart import LINE_PLOT_MIN, NARROW_W, line_pads   # noqa: PLC0415  (the drawing's own sums)
    pad_l, pad_r = line_pads(ev)
    if NARROW_W - pad_l - pad_r < LINE_PLOT_MIN:
        errors.append(f"{ew}: the line's first and last point labels and its longest value (with prefix and unit) "
                      f"leave the phone's drawing {max(0, round(NARROW_W - pad_l - pad_r))} px of {NARROW_W} for the "
                      f"line, under {LINE_PLOT_MIN}; shorten them (an x label of about {LINE_LABEL_HINT} characters "
                      "or fewer, a short unit)")


def _keys(ev: dict, ew: str, errors: list) -> None:
    kind = ev.get("type", "bar")
    if kind not in TYPES:
        errors.append(f"{ew}: 'type' must be one of {', '.join(TYPES)}")
    line = kind == "line"
    series = ev.get("series")
    if "series" in ev and (not isinstance(series, list) or len(series) != SERIES_N
                           or not all(isinstance(s, str) and s.strip() for s in series)):
        errors.append(f"{ew}: 'series' must be a list of {SERIES_N} non-empty names, such as [\"Today\", \"New\"]")
        series = None
    bars = ev.get("bars")
    if not isinstance(bars, list) or not bars:
        errors.append(f"{ew}: 'bars' must be a non-empty list of {{\"label\", \"value\", \"emphasis\"?}}")
        bars = []
    if line and bars and len(bars) < LINE_MIN:
        errors.append(f"{ew}: a line needs at least {LINE_MIN} points in 'bars'")
    for k, bar in enumerate(bars, 1):
        if not isinstance(bar, dict):
            errors.append(f"{ew} bar {k}: must be an object with 'label' and 'value'")
            continue
        _bar(bar, f"{ew} bar {k}", line, series, errors)
    if sum(1 for b in bars if isinstance(b, dict) and b.get("emphasis") is True) > 1:
        errors.append(f"{ew}: at most one bar may carry 'emphasis'")
    for key in ("unit", "source"):
        if ev.get(key) is not None and not isinstance(ev[key], str):         # absent, null or a string
            errors.append(f"{ew}: '{key}' must be a non-empty string")
    if "prefix" in ev and (not isinstance(ev["prefix"], str) or not ev["prefix"].strip()
                           or len(ev["prefix"]) > PREFIX_MAX):
        errors.append(f"{ew}: 'prefix' must be a short string of 1 to {PREFIX_MAX} characters, such as \"$\"")
    if "decimals" in ev and (isinstance(ev["decimals"], bool) or not isinstance(ev["decimals"], int)
                             or not 0 <= ev["decimals"] <= DECIMALS_MAX):
        errors.append(f"{ew}: 'decimals' must be a whole number from 0 to {DECIMALS_MAX}")
    if "side" in ev:
        side = ev["side"]
        if not isinstance(side, dict):
            errors.append(f"{ew}: 'side' must be an object with 'title' and 'items'")
        else:
            if side.get("title") is not None and not isinstance(side["title"], str):
                errors.append(f"{ew} side: 'title' must be a non-empty string")
            if not isinstance(side.get("items"), list) or not all(isinstance(x, str) for x in side["items"]):
                errors.append(f"{ew} side: 'items' must be a list of strings")
