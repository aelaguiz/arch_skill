"""Decision deck evidence: the grid bar chart and the line chart, and every chart's plain-text lines.

decision_deck_deck.chart_html draws a plain chart as an SVG (labels left, values at each bar's end) unless it uses
note, prefix, decimals, series or type, or a label the SVG would cut (over SVG_LABEL_CHARS characters); then it
comes here.
- Bars are HTML in a grid, not SVG text, so their type keeps its size at any scale: label, bar, value and note in
  one row each. The label column is as wide as the longest label up to LABEL_CAP of the chart, and a longer label
  wraps (rows grow, nothing is cut); values sit in one right-aligned column (prefix, decimals, unit); a note is the
  row's fourth column. Two series (a before/after pair) draw two bars per label, the first grey and the second in
  the accent, each with its own value, under a small legend. On a phone each label sits above its bar.
- A line (type "line") is an SVG drawn at its column's own width on the stage (COL_W, or COL_SIDE_W beside a side
  panel), so its text is drawn at its CSS size: points joined by a line, every point's value written beside it up
  to LABEL_ALL points and past that only the first, last and highest, x labels under the axis (as many as fit).
- Either kind scrolls in its bounded box (with the deck's "Scroll for the rest" line) when taller than its zone,
  rather than shrinking its text.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_diff import SCROLL_HINT  # noqa: E402
from decision_deck_inline import e, linked, number  # noqa: E402

SVG_LABEL_CHARS = 25            # the SVG chart cuts a label longer than this ((220 - 14) // 8)
GRID_KEYS = ("prefix", "decimals", "series", "type")
LABEL_CAP = "45%"               # the label column's widest
COL_W, COL_SIDE_W, NARROW_W = 864, 556, 358   # stage px: the slide's text width, less a side panel; a phone line
LINE_H, LINE_NARROW_H = 200, 180
PAD_T, PAD_B, PAD_X = 22, 30, 10              # room above the highest point's value, below the axis for x labels
LABEL_ALL = 8                   # up to this many points, each is labelled; past it the first, last and highest
CHAR_W = 7.0                    # an x label's width per character at 12 px, with room to spare
XL_GAP = 14
LINE_PLOT_MIN = 160             # stage px: the narrowest a line's plot may be, on the phone drawing (NARROW_W)
LEGEND_H, LEGEND_W = 20, 130    # a two-line chart's legend row above the plot, and each entry's room


def rich(ev: dict) -> bool:
    """Whether the chart needs this drawing: it uses note, prefix, decimals, series or type, or a label the SVG would cut."""
    bars = ev.get("bars") or []
    return (any(k in ev for k in GRID_KEYS) or any("note" in b or "values" in b for b in bars)
            or any(len(b["label"]) > SVG_LABEL_CHARS for b in bars))


def fmt(ev: dict, val) -> str:
    """A value as the chart writes it: prefix, the number (fixed decimals when given), then the unit."""
    body = f"{abs(val):,.{ev['decimals']}f}" if "decimals" in ev else number(abs(val))
    unit = f" {ev['unit']}" if ev.get("unit") else ""
    return f"{'-' if val < 0 else ''}{ev.get('prefix', '')}{body}{unit}"


def values_of(ev: dict, bar: dict) -> list:
    return list(bar["values"]) if ev.get("series") else [bar["value"]]


# ------------------------------------------------------------------ bars

def _legend(ev: dict) -> str:
    if not ev.get("series"):
        return ""
    keys = "".join(f'<span class="k s{k}" aria-hidden="true"></span><span>{linked(name)}</span>'
                   for k, name in enumerate(ev["series"]))
    return f'<p class="hleg">{keys}</p>'


def bars_html(ev: dict) -> str:
    two, notes = bool(ev.get("series")), any(b.get("note") for b in ev["bars"])
    top = max(max(values_of(ev, b)) for b in ev["bars"]) or 1
    rows = []
    for bar in ev["bars"]:
        vals = values_of(ev, bar)
        cls = [f"s{k}" for k in range(len(vals))] if two else ["em" if bar.get("emphasis") else ""]
        track = "".join(f'<i class="b{(" " + c) if c else ""}" style="width:{100 * v / top:.2f}%"></i>'
                        for v, c in zip(vals, cls))
        said = "".join(f'<span>{e(fmt(ev, v))}</span>' for v in vals)
        if two:
            said = "".join(f'<span><span class="sr-only">{e(name)} </span>{e(fmt(ev, v))}</span>'
                           for name, v in zip(ev["series"], vals))
        note = f'<span class="hn">{linked(bar.get("note") or "")}</span>' if notes else ""
        rows.append(f'<div class="r{" em" if bar.get("emphasis") else ""}" role="listitem">'
                    f'<span class="hl">{linked(bar["label"])}</span><span class="track" aria-hidden="true">{track}</span>'
                    f'<span class="hv">{said}</span>{note}</div>')
    return (f'{_legend(ev)}<div class="hb{" notes" if notes else ""}{" two" if two else ""}" role="list">'
            f'{"".join(rows)}</div>')


# ------------------------------------------------------------------ line

def _xl_step(labels: list, plot_w: float) -> int:
    widest = max(len(x) for x in labels) * CHAR_W + XL_GAP
    fit = max(2, int(plot_w // widest))
    return max(1, math.ceil((len(labels) - 1) / (fit - 1))) if len(labels) > fit else 1


def line_pads(ev: dict) -> tuple[float, float]:
    """The room left and right of a line's plot: half its first x label, and half the wider of its last x label and
    its longest value. decision_deck_chart_spec refuses a line whose pads leave NARROW_W under LINE_PLOT_MIN."""
    pts, flat = ev["bars"], [v for p in ev["bars"] for v in values_of(ev, p)]
    pad_l = PAD_X + CHAR_W * len(pts[0]["label"]) / 2
    return pad_l, PAD_X + CHAR_W * max(len(pts[-1]["label"]), max(len(fmt(ev, v)) for v in flat)) / 2


def line_svg(ev: dict, width: int, narrow: bool) -> str:
    pts, series = ev["bars"], ev.get("series") or [None]
    top_pad = PAD_T + (LEGEND_H if ev.get("series") else 0)
    height = (LINE_NARROW_H if narrow else LINE_H) + top_pad - PAD_T
    grid = [values_of(ev, p) for p in pts]
    flat = [v for row in grid for v in row]
    lo, hi = min(flat), max(flat)
    if hi == lo:
        lo, hi = lo - 1, hi + 1
    pad_l, pad_r = line_pads(ev)
    plot_w, plot_h = width - pad_l - pad_r, height - top_pad - PAD_B
    xs = [pad_l + plot_w * k / (len(pts) - 1) for k in range(len(pts))]

    def y(v):
        return round(top_pad + plot_h * (hi - v) / (hi - lo), 1)

    out = [f'<line class="ax" x1="{pad_l - PAD_X / 2:.1f}" x2="{width - pad_r + PAD_X / 2:.1f}" '
           f'y1="{height - PAD_B + 6}" y2="{height - PAD_B + 6}"/>']
    for s in range(len(series)):
        col = [row[s] for row in grid]
        cls = f"ln s{s}" if series[0] is not None else "ln s1"
        out.append(f'<polyline class="{cls}" points="{" ".join(f"{x:.1f},{y(v)}" for x, v in zip(xs, col))}"/>')
        show = range(len(pts)) if len(pts) <= LABEL_ALL else sorted({0, len(pts) - 1, col.index(max(col))})
        for k in show:
            above = s == len(series) - 1 or col[k] >= grid[k][-1]
            ty = y(col[k]) - 8 if above else y(col[k]) + 16
            out.append(f'<circle class="pt {cls.split()[1]}" cx="{xs[k]:.1f}" cy="{y(col[k])}" r="3"/>'
                       f'<text class="pv" x="{xs[k]:.1f}" y="{ty}" text-anchor="middle">{e(fmt(ev, col[k]))}</text>')
    step = _xl_step([p["label"] for p in pts], plot_w)
    ticks = sorted(set(range(0, len(pts), step)) | {len(pts) - 1})
    if len(ticks) > 1 and ticks[-1] - ticks[-2] < step:
        ticks.pop(-2)                    # the last label never crowds the one before it
    out += [f'<text class="xl" x="{xs[k]:.1f}" y="{height - 6}" text-anchor="middle">{e(pts[k]["label"])}</text>'
            for k in ticks]
    legend = ""
    if series[0] is not None:
        legend = "".join(f'<text class="lg" x="{PAD_X + LEGEND_W * k:.1f}" y="12"><tspan class="k s{k}">■</tspan> '
                         f'{e(name)}</text>' for k, name in enumerate(series))
    said = "; ".join(f'{p["label"]} ' + ", ".join(
        (f"{name} " if name else "") + fmt(ev, v) for name, v in zip(series, values_of(ev, p))) for p in pts)
    return (f'<svg class="{"narrow" if narrow else "wide"}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-label="{e(said)}" preserveAspectRatio="xMinYMin meet">{legend}{"".join(out)}</svg>')


# ------------------------------------------------------------------ the zone, and the words

def chart_html(ev: dict, panel: str) -> str:
    """The chart zone: the drawing in a bounded scroll box (beside the side panel when there is one)."""
    if ev.get("type") == "line":
        wide = COL_SIDE_W if panel else COL_W
        body, cls = line_svg(ev, wide, False) + line_svg(ev, NARROW_W, True), "lc"
    else:
        body, cls = bars_html(ev), "hbc"
    return (f'<div class="ev fit"><div class="cx{"" if panel else " one"}"><div class="chart tbl {cls}" tabindex="0">'
            f'{body}</div>{panel}</div>{SCROLL_HINT}</div>')


def chart_lines(ev: dict, flat) -> list[str]:
    """The chart as plain text, one bar or point per line (the SVG chart's lines: number, then the unit)."""
    line, series = ev.get("type") == "line", ev.get("series")
    if not line and not series:
        head = "[Evidence: a bar chart, one bar per line]"
    elif not line:
        head = f"[Evidence: a bar chart, two bars per line: {flat(series[0])}, then {flat(series[1])}]"
    elif series:
        head = f"[Evidence: a line chart, two lines: {flat(series[0])}, then {flat(series[1])}; one point per line, in order]"
    else:
        head = "[Evidence: a line chart, one point per line, in order]"
    out = [head]
    for bar in ev["bars"]:
        said = (", ".join(f"{flat(name)} {fmt(ev, v)}" for name, v in zip(series, bar["values"])) if series
                else fmt(ev, bar["value"]))         # number, then the unit
        hl = " (highlighted)" if bar.get("emphasis") else ""
        note = f"; {flat(bar['note'])}" if bar.get("note") else ""
        out.append(f"{flat(bar['label'])}: {said}{hl}{note}")
    side = ev.get("side")
    if side:
        out.append(f"[Panel beside the chart{': ' + flat(side['title']) if side.get('title') else ''}]")
        out += [f"- {flat(x)}" for x in side["items"]]
    return out
