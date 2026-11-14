"""Decision deck evidence: the bar chart as inline SVG, the table, the context row, and the evidence zone per kind.

The text diff with its rule panel lives in decision_deck_diff.py; escaping, links and numbers in decision_deck_inline.py.
Pictures are drawn by the page script (decision_deck_script.py), since their views, Flip and Zoom change on the page.
Chart rules: one emphasised bar in --data-1, every other bar in --data-muted, each bar labelled directly (its name at
the left, its value at its end), no axis, no legend. A chart using note, prefix, decimals, series or type, or a label
this drawing would cut, is drawn by decision_deck_chart.py instead.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_diff import SCROLL_HINT, diff_html  # noqa: E402
from decision_deck_inline import e, linked, number  # noqa: E402
from decision_deck_chart import chart_html as rich_chart, rich  # noqa: E402

CHART_W = 560               # SVG user units; the SVG scales to its column
ROW_H, BAR_H = 34, 20
CHART_NARROW_W, LABEL_H = 358, 22    # the phone's drawing: a 390 px screen less the slide's padding; a label line
CTX_FOLD = 100              # a context line longer than this gets a "Read all" button


# ------------------------------------------------------------------ chart

def _clip(text: str, chars: int) -> str:
    return text if len(text) <= chars else text[: chars - 1].rstrip() + "…"


def chart_svg(ev: dict, narrow: bool = False) -> str:
    """Horizontal bars, longest scale first in spec order; labels left, values at each bar's end. `narrow` is the
    phone's drawing: CHART_NARROW_W wide with each label on its own line above its bar, so the text keeps its size
    (the wide drawing shrunk to a phone column draws its labels at about 9 px)."""
    bars, unit = ev["bars"], (" " + ev["unit"]) if ev.get("unit") else ""
    longest = max(len(b["label"]) for b in bars)
    width, lift = (CHART_NARROW_W, LABEL_H) if narrow else (CHART_W, 0)
    label_w = 0 if narrow else min(220, max(80, 8 * longest + 14))
    value_w = max(70, 7 * max(len(number(b["value"]) + unit) for b in bars) + 12)
    span = width - label_w - value_w
    top = max(b["value"] for b in bars) or 1
    rows, said = [], []
    for k, bar in enumerate(bars):
        y = k * (ROW_H + lift) + lift
        w = round(span * bar["value"] / top, 1)
        fill = "var(--data-1)" if bar.get("emphasis") else "var(--data-muted)"
        value = number(bar["value"]) + unit
        said.append(f'{bar["label"]} {value}')
        label_y = y - lift / 2 - 1 if narrow else y + BAR_H / 2 + 1
        rows.append(f'<text class="lab" x="0" y="{label_y}" dominant-baseline="middle">'
                    f'<title>{e(bar["label"])}</title>'
                    f'{e(_clip(bar["label"], (width if narrow else label_w - 14) // 8))}</text>'
                    f'<rect x="{label_w}" y="{y}" width="{w}" height="{BAR_H}" fill="{fill}"/>'
                    f'<text class="val" x="{label_w + w + 6}" y="{y + BAR_H / 2 + 1}" '
                    f'dominant-baseline="middle">{e(value)}</text>')
    height = len(bars) * (ROW_H + lift) - (ROW_H - BAR_H)
    return (f'<svg class="{"narrow" if narrow else "wide"}" viewBox="0 0 {width} {height}" role="img" '
            f'aria-label="{e("; ".join(said))}" preserveAspectRatio="xMinYMin meet">{"".join(rows)}</svg>')


def side_html(ev: dict) -> str:
    """A chart's side panel ("side": {"title"?, "items"}), or nothing."""
    side = ev.get("side")
    if not side:
        return ""
    head = f'<p class="h">{linked(side.get("title"))}</p>' if side.get("title") else ""
    return f'<div class="side">{head}<ul>{"".join(f"<li>{linked(x)}</li>" for x in side["items"])}</ul></div>'


def chart_html(ev: dict) -> str:
    panel = side_html(ev)
    if rich(ev):                        # a new key or a label this drawing would cut: decision_deck_chart.py
        return rich_chart(ev, panel)
    return (f'<div class="ev fit"><div class="cx{"" if panel else " one"}"><div class="chart">{chart_svg(ev)}'
            f'{chart_svg(ev, narrow=True)}</div>{panel}</div></div>')


# ------------------------------------------------------------------ table

NB_MAX = 16                 # a hyphenated word up to this long ("11-07", "sign-up") never breaks at its hyphen


def keep_whole(html: str) -> str:
    """Escaped text with each short hyphenated word wrapped in <span class="nb">, so a narrow column or a cover line
    never ends on its hyphen ("11- / 07"); longer compounds stay breakable so they fit a phone line."""
    return re.sub(r"(?<![\w-])(\w+(?:-\w+)+)(?![\w-])",
                  lambda m: f'<span class="nb">{m.group(1)}</span>' if len(m.group(1)) <= NB_MAX else m.group(1), html)


def _cell(val, tag: str = "td", label: str = "", role: str = "") -> str:
    """One cell; `label` (its column header) is what a phone shows above the value when the row becomes a card, and
    `role` its explicit ARIA role (the phone's display: block can drop table semantics in Safari and VoiceOver)."""
    lab = (f' role="{role}"' if role else "") + (f' data-label="{e(label)}"' if label else "")
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return f'<{tag} class="num"{lab}>{e(number(val))}</{tag}>'
    return f"<{tag}{lab}>{linked(val, lambda t: keep_whole(e(t)))}</{tag}>"


PHONE_COLS, PHONE_CHARS, PHONE_LINE, HEAD_WIDER = 4, 64, 44, 1.2


def phone_fits(columns: list, rows: list) -> bool:
    """Whether a table reads as a table on a phone line (about 358 px, PHONE_LINE characters): at most PHONE_COLS
    columns, whose longest cells together run to PHONE_CHARS characters (cells wrap), and whose widest words that
    cannot break (a hyphen-free run; a head counts HEAD_WIDER, being bold capitals) fit one line together with 2
    characters of padding a column. A table that does not fit shows one card per row there."""
    if len(columns) > PHONE_COLS:
        return False

    def widest(text: str) -> int:
        return max((len(w) for w in re.split(r"[\s-]+", text)), default=0)

    cols = [[number(c) if isinstance(c, (int, float)) and not isinstance(c, bool) else str(c) for c in col]
            for col in zip(*rows)] if rows else [[] for _ in columns]
    longest = [max([len(x) for x in col] or [0]) for col in cols]
    need = [max([widest(x) for x in col] + [HEAD_WIDER * widest(str(head))]) for col, head in zip(cols, columns)]
    return sum(longest) <= PHONE_CHARS and sum(need) + 2 * len(columns) <= PHONE_LINE


def table_html(ev: dict) -> str:
    cards = "" if phone_fits(ev["columns"], ev["rows"]) else " cards"
    filled = [[c for c in col if c not in ("", None)] for col in zip(*ev["rows"])] or [[] for _ in ev["columns"]]
    nums = [bool(col) and all(isinstance(c, (int, float)) and not isinstance(c, bool) for c in col) for col in filled]
    head = "".join('<th role="columnheader"' + (' class="num">' if num else ">")
                   + linked(c, lambda t: keep_whole(e(t))) + "</th>" for c, num in zip(ev["columns"], nums))
    body = "".join('<tr role="row">' + "".join(_cell(c, label=h, role="rowheader" if k == 0 else "cell")
                                                for k, (c, h) in enumerate(zip(row, ev["columns"]))) + "</tr>"
                   for row in ev["rows"])
    return (f'<div class="ev fit"><div class="tbl" tabindex="0"><table class="sumtbl dtbl{cards}" role="table">'
            f'<thead role="rowgroup"><tr role="row">{head}</tr></thead><tbody role="rowgroup">{body}</tbody></table>'
            f'</div>{SCROLL_HINT}</div>')


# ------------------------------------------------------------------ the context row

def context_text(dec: dict, question_moved: bool) -> str:
    """The question when it did not fit the title, the decision's context, and per option its caption (when it has
    no pictures of its own, whose column head shows it instead) and its pros and cons."""
    parts = [dec["question"]] if question_moved else []
    if dec.get("context"):
        parts.append(dec["context"])
    for opt in dec["options"]:
        said = [f"for: {'; '.join(opt['pros'])}" if opt.get("pros") else "",
                f"against: {'; '.join(opt['cons'])}" if opt.get("cons") else ""]
        said = ", ".join(s for s in said if s)
        cap = "" if opt.get("images") else (opt.get("caption") or "").strip()
        if cap:
            parts.append(f"{opt['label']}: {cap.rstrip('.')}{', ' + said if said else ''}.")
        elif said:
            parts.append(f"{opt['label']}, {said}.")
    return " ".join(parts)


def ctx_row(did: str, text: str) -> str:
    if not text:
        return ""
    more = (f'<button type="button" class="more" data-ctx="{e(did)}" aria-controls="ctx-{e(did)}" '
            f'aria-expanded="false">Read all</button>' if len(text) > CTX_FOLD else "")
    return f'<div class="ctxrow"><p class="ctx" id="ctx-{e(did)}">{linked(text)}</p>{more}</div>'


def evidence_html(did: str, ev: dict) -> str:
    """The evidence zone for one decision; pictures get an empty zone the page script fills."""
    kind = ev["kind"]
    if kind == "diff":
        return diff_html(ev)
    if kind == "chart":
        return chart_html(ev)
    if kind == "table":
        return table_html(ev)
    if kind == "images":
        return f'<div class="ev" data-ev="{e(did)}"></div>'
    return '<div class="ev"></div>'
