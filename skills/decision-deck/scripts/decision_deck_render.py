"""Decision deck page: the round as one 16:9 deck, a cover, one slide per decision, the closing summary with Done.

Rendered from the spec and the ledger on every load, so a reload or a second device shows everything recorded so
far; the page script (decision_deck_script.py) then keeps it current from /api/events and /api/state. Each fact appears
once per slide: the title is the question, the callout only the why, the Recommended mark sits on
its button, the status line is the one place a slide shows status, and the dots are the only progress.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_core import image_ids  # noqa: E402
from decision_deck_deck import context_text, ctx_row, e, evidence_html, keep_whole, linked  # noqa: E402
from decision_deck_ledger import deck_state  # noqa: E402
from decision_deck_script import SCRIPT  # noqa: E402
from decision_deck_spec import evidence_of, option_keys, takes_note  # noqa: E402
from decision_deck_css import page_css  # noqa: E402

TITLE_MAX = 62              # the longest question that fits the slide title on one line at 20 pt
HOW = ("One decision per slide. Each answer and comment reaches the session as you make it"
       '<span class="keyhint">; <span class="nb"><kbd>?</kbd> lists the keys</span></span>.')
END_DOT = ('<svg viewBox="0 0 12 12" aria-hidden="true"><rect x="1" y="1" width="10" height="10" fill="none" '
           'stroke="var(--ink-2)" stroke-width="1.5"/></svg>')
OPEN_DOT = ('<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7" fill="var(--paper)" '
            'stroke="var(--ink-2)" stroke-width="1.6"/></svg>')
KEYS = [("<kbd>&rarr;</kbd> <kbd>&larr;</kbd> or <kbd>J</kbd> <kbd>K</kbd>", "Next or previous slide"),
        ("<kbd>Home</kbd> <kbd>End</kbd>", "Opening slide, summary slide"),
        ("<kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd> or the letter on a button",
         "Answer; it is recorded at once and the next slide follows"),
        ("<kbd>C</kbd>", "Comment; it is sent when you pause or leave the box (<kbd>Esc</kbd>), and keeps the "
                         "decision open"),
        ("<kbd>V</kbd> <kbd>F</kbd> <kbd>B</kbd> <kbd>Z</kbd>", "Pictures: next view, flip in place, side by side, "
                                                                "real size"),
        ("<kbd>D</kbd>", "On the summary: tell the session the round is done")]


def shown_title(dec: dict) -> tuple[str, bool]:
    """(the slide title, whether the question moved under the evidence): the question when it fits one line."""
    if len(dec["question"]) <= TITLE_MAX:
        return dec["question"], False
    return dec["title"], True


def _js(data) -> str:
    """JSON safe inside a <script> element: no '<', '>' or '&' survives outside an escape."""
    text = json.dumps(data, ensure_ascii=False)
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def item_data(dec: dict, image_of: dict) -> dict:
    """What the page script needs for one decision: its options and keys, and its pictures by content hash."""
    ev = evidence_of(dec)
    keys = {k["id"]: k for k in option_keys(dec)}
    rec = dec["recommendation"]
    item = {"id": dec["id"], "name": dec["title"], "kind": ev["kind"], "note": takes_note(dec),
            "rec": {"option": rec.get("option"), "why": rec["why"]},
            "options": [{"id": o["id"], "label": o["label"], "key": keys[o["id"]]["key"], "alt": keys[o["id"]]["alt"],
                         "ask_note": bool(o.get("ask_note"))} for o in dec["options"]]}
    if ev["kind"] == "images":
        item.update(views=ev["views"], density=ev["density"], columns=[
            {"tag": c["tag"], "caption": c["caption"],
             "figs": [{"src": "/img/" + image_of[f["image"]], "caption": f["caption"],
                       "alt": f"{c['tag']}: {f['caption'] or c['caption'] or f['image']}"} for f in c["figs"]]}
            for c in ev["columns"]])
    return item


def _shell(i: int, total: int, inner: str, cls: str, did: str = "") -> str:
    data_id = f' data-id="{e(did)}"' if did else ""
    return (f'<section class="slide {cls}" id="sl-{i}" data-i="{i}"{data_id} aria-roledescription="slide" '
            f'aria-label="{i + 1} of {total}">{inner}</section>')


def _choices(dec: dict, item: dict) -> str:
    out = []
    for opt in item["options"]:
        sub = '<span class="m">Recommended</span>' if opt["id"] == item["rec"]["option"] else ""
        hint = " ".join(x.upper() for x in dict.fromkeys([opt["key"], opt["alt"]]) if x)
        out.append(f'<button type="button" class="choice" data-choose="{e(dec["id"])}|{e(opt["id"])}" '
                   f'aria-pressed="false" aria-keyshortcuts="{e(hint)}"><kbd>{e(opt["key"].upper())}</kbd>'
                   f'<span class="tx"><span class="l">{linked(opt["label"])}</span>{sub}</span></button>')
    return "".join(out)


def decision_slide(dec: dict, i: int, total: int, item: dict, comment: str) -> str:
    title, moved = shown_title(dec)
    rec = dec["recommendation"]
    if rec.get("option"):
        label = next(o["label"] for o in dec["options"] if o["id"] == rec["option"])
        why = f'<span class="sr-only">Why {e(label)} is recommended: </span><span class="why">{linked(rec["why"])}</span>'
    else:
        why = f'<span class="why"><b>No recommendation.</b> {linked(rec["why"])}</span>'
    ev = evidence_of(dec)
    note = item["note"]
    cbox = (f'<div class="cbox"><label for="c-{e(dec["id"])}" class="sr-only">Comment, optional; sent to the session '
            f'on its own</label><textarea id="c-{e(dec["id"])}" data-item="{e(dec["id"])}" rows="1" maxlength="500" '
            f'aria-keyshortcuts="C" placeholder="Comment (C)">{e(comment)}</textarea></div>' if note else "")
    src = f'<p class="src">Source: {linked(ev["source"])}</p>' if ev.get("source") else ""
    inner = (f'<h2 class="title" tabindex="-1" title="{e(dec["question"])}">{linked(title)}</h2><div class="trule"></div>'
             f'<p class="rec">{why}</p>{evidence_html(dec["id"], ev)}{ctx_row(dec["id"], context_text(dec, moved))}'
             f'<div class="grow"></div><div class="dock{"" if note else " nonote"}">{cbox}<div class="choices" role="group" '
             f'aria-label="Your answer" data-choices="{e(dec["id"])}">{_choices(dec, item)}</div>'
             f'<p class="status" data-status="{e(dec["id"])}" aria-live="polite"></p></div>{src}')
    return _shell(i, total, inner, "item", dec["id"])


def cover_title(title: str) -> str:
    """The cover title, escaped, with each short hyphenated word ("sign-up") kept whole so a line never ends on its
    hyphen; the CSS balances the lines."""
    return keep_whole(e(title))


def cover_slide(spec: dict, total: int) -> str:
    """The cover: the round's title, the how line and Start."""
    inner = (f'<div class="cover"><span class="bar6" aria-hidden="true"></span><h2 class="title-c" tabindex="-1">'
             f'{cover_title(spec["title"])}</h2></div><p class="how">{HOW}</p><div><button type="button" '
             f'class="btn primary start" data-goto="1">Start <kbd>&rarr;</kbd></button></div>')
    return _shell(0, total, inner, "cover-s")


def closing_slide(spec: dict, i: int, total: int) -> str:
    decided = "".join(f'<li>{linked(d["title"])}: {linked(d["answer"])}</li>' for d in spec.get("decided", []))
    earlier = (f'<div class="decided"><h3>Decided in earlier rounds</h3><ul>{decided}</ul></div>' if decided else "")
    inner = (f'<h2 class="title" tabindex="-1" data-closing-title></h2><div class="trule"></div>'
             f'<div class="closing-body"><div data-closing></div>{earlier}</div>'
             f'<div class="dock"><p class="status" data-status="closing" style="grid-column:1" aria-live="polite"></p>'
             f'<div class="choices"><button type="button" class="btn primary" id="done-btn" aria-keyshortcuts="D">'
             f'Done <kbd>D</kbd></button></div></div>')
    return _shell(i, total, inner, "closing")


def _dots(items: list, start: int) -> str:
    """One dot per slide: the cover and summary squares, a ring per decision."""
    n = len(items)
    out = []
    for i in range(n + 2):
        cur = ' aria-current="true"' if i == start else ""
        if i in (0, n + 1):
            name = "Opening slide" if i == 0 else "Summary slide"
            out.append(f'<button type="button" class="dot end" data-goto="{i}"{cur} aria-label="{name}">{END_DOT}'
                       f'</button>')
        else:
            dec = {"id": items[i - 1]["id"], "title": items[i - 1]["name"]}
            out.append(f'<button type="button" class="dot" data-goto="{i}"{cur} aria-label="{e(dec["id"])}, '
                       f'{e(dec["title"])}: open">{OPEN_DOT}</button>')
    return "".join(out)


def deck_page(spec: dict, records: list, start: int = 0, image_of: dict | None = None, gen: int = 0,
              source: str = "") -> str:
    """The whole deck. `source` is the header's second line, where the deck comes from (serve --source); empty
    shows the title alone."""
    image_of = image_ids(spec) if image_of is None else image_of
    decisions = spec["decisions"]
    n = len(decisions)
    total = n + 2
    start = max(0, min(int(start), total - 1))
    state = deck_state(spec, records)
    items, slides = [], [cover_slide(spec, total)]
    for k, dec in enumerate(decisions, 1):
        items.append(item_data(dec, image_of))
        slides.append(decision_slide(dec, k, total, items[-1], state["decisions"][dec["id"]]["comment"]))
    slides.append(closing_slide(spec, n + 1, total))
    data = {"title": spec["title"], "items": items, "state": state, "n": state["n"], "gen": gen, "lines": records,
            "start": start}
    keys = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in KEYS)
    src = f'<span class="from" title="{e(source)}">{e(source)}</span>' if source else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>{e(spec['title'])}</title><style>{page_css()}</style></head>
<body><header class="bar"><div class="who"><span class="round" title="{e(spec['title'])}">{e(spec['title'])}</span>{src}</div>
<nav class="dots" id="dots" aria-label="Slides">{_dots(items, start)}</nav>
<button type="button" class="btn icon help" id="help-btn" aria-label="Keyboard shortcuts" aria-keyshortcuts="?">?</button>
</header><main class="deck" aria-label="Decisions"><div class="stage" id="stage">
<button type="button" class="nav-arrow prev" data-step="-1" aria-label="Previous slide">&lsaquo;</button>
{''.join(slides)}
<button type="button" class="nav-arrow next" data-step="1" aria-label="Next slide">&rsaquo;</button></div></main>
<p class="sr-only" aria-live="polite" id="live"></p>
<dialog id="zoom" aria-labelledby="zoom-t"><div class="dlg-h"><h2 id="zoom-t"></h2><button type="button" class="btn"
 id="zoom-flip"></button><button type="button" class="btn" data-close="1">Close <kbd>Esc</kbd></button></div>
<div class="dlg-b"><img id="zoom-img" alt=""></div></dialog>
<dialog id="help" aria-labelledby="help-t"><div class="dlg-h"><h2 id="help-t">Keys</h2><button type="button" class="btn"
 data-close="1">Close <kbd>Esc</kbd></button></div><div class="dlg-b"><table class="keys"><tbody>{keys}</tbody></table>
</div></dialog>
<script type="application/json" id="data">{_js(data)}</script>
<script>{SCRIPT}</script></body></html>"""


def not_found(spec: dict) -> str:
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width, initial-scale=1"><title>Not found</title><style>{page_css()}</style></head>'
            f'<body><main style="padding:80px 24px"><h1 class="title">Not found</h1><p>That page or file is not here.'
            f'</p><p><a class="btn primary" href="/">Back to {e(spec["title"])}</a></p></main></body></html>')
