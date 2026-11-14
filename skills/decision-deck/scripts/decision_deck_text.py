"""The reader-facing text of a decision deck, slide by slide, for a legibility read before the owner sees it.

`decision_deck.py text --spec S [--out FILE]` prints it. Every word the round's spec puts on a slide comes out in slide
order: the cover title; per decision its slide title, the question when it moved under the evidence, the
recommendation's why, the evidence as text (table rows, the diff paragraph by paragraph, chart bars with their
values, side panel and source, pictures by column and caption), the context row with each option's caption, pros
and cons, and the answer buttons with the Recommended mark; then the summary's rows and the earlier rounds' answers.
Lines in square brackets say where the text sits; they are not on the slide. The deck's own fixed controls (Start,
the keys, Comment, Done) are left out: they are the tool's words, not the round's. The layout check reads boxes, not
words, so this text is what a fresh reader reads to find slides that do not make sense. Stdlib only, no rendering.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_chart import chart_lines  # noqa: E402
from decision_deck_deck import context_text  # noqa: E402
from decision_deck_diff import align, paragraphs  # noqa: E402
from decision_deck_inline import number  # noqa: E402
from decision_deck_marks import plain  # noqa: E402
from decision_deck_render import shown_title  # noqa: E402
from decision_deck_spec import evidence_of, option_keys  # noqa: E402

NOTE = "Lines in [square brackets] say where the text sits on the slide; they are not on the slide."


def _cell(val) -> str:
    return number(val) if isinstance(val, (int, float)) and not isinstance(val, bool) else str(val)


def _flat(text: str) -> str:
    """One paragraph on one line: inner line breaks become spaces, so a reader's quote matches one line."""
    return " ".join(str(text).split())


def _rule(text: str) -> str:
    """A paragraph of quoted rule text as the slide shows it: its Markdown markers gone (decision_deck_marks), flat."""
    return _flat(plain(text))


def evidence_lines(dec: dict) -> list[str]:
    ev = evidence_of(dec)
    kind = ev["kind"]
    if kind == "table":
        return (["[Evidence: a table; first line is the column headers]", " | ".join(_flat(c) for c in ev["columns"])]
                + [" | ".join(_flat(_cell(c)) for c in row) for row in ev["rows"]])
    if kind == "chart":                 # bars or points with their values and notes, then the side panel
        return chart_lines(ev, _flat)
    if kind == "diff":
        out = []
        if ev.get("rule_now"):
            out.append("[Panel: The rule now reads]")
            out += [_rule(p) for p in paragraphs(ev["rule_now"])]
        out.append("[Evidence: the change, paragraph by paragraph]")
        for old, new in align(paragraphs(ev["before"]), paragraphs(ev["after"])):
            if old is not None and new is not None and _flat(old) == _flat(new):
                out.append(f"Unchanged: {_rule(old)}")
                continue
            if old is not None:
                out.append(f"{'Was' if new is not None else 'Removed'}: {_rule(old)}")
            if new is not None:
                out.append(f"{'Now' if old is not None else 'Added'}: {_rule(new)}")
        return out
    if kind == "images":
        views = f"; tabs: {' / '.join(_flat(v) for v in ev['views'])}" if ev["views"] else ""
        out = [f"[Evidence: pictures in columns{views}]"]
        for col in ev["columns"]:
            head = _flat(col["tag"]) + (f": {_flat(col['caption'])}" if col["caption"] else "")
            caps = [_flat(f["caption"]) for f in col["figs"] if f["caption"]]
            n = len(col["figs"])
            out.append(f"Column {head} ({n} picture{'s' if n != 1 else ''}){': ' + '; '.join(caps) if caps else ''}")
        return out
    return []


def decision_lines(dec: dict, k: int, n: int) -> list[str]:
    title, moved = shown_title(dec)
    rec = dec["recommendation"]
    why = _flat(rec["why"]) if rec.get("option") else f"No recommendation. {_flat(rec['why'])}"
    out = [f"[Slide {k} of {n}: decision {dec['id']}, named \"{_flat(dec['title'])}\" in the summary]",
           f"[Title] {_flat(title)}", f"[Why we recommend it, under the title] {why}"]
    out += evidence_lines(dec)
    ctx = context_text(dec, moved)
    if ctx:
        out.append(f"[Context line, under the evidence] {_flat(ctx)}")
    if evidence_of(dec).get("source"):
        out.append(f"[Source line, at the foot] Source: {_flat(evidence_of(dec)['source'])}")
    out.append("[Answer buttons]")
    keys = {x["id"]: x["key"] for x in option_keys(dec)}
    for opt in dec["options"]:
        mark = " (Recommended)" if opt["id"] == rec.get("option") else ""
        out.append(f"{keys[opt['id']].upper()}. {_flat(opt['label'])}{mark}")
    return out


def deck_text(spec: dict) -> str:
    """The whole deck's reader-facing text, one slide after another, blank line between slides."""
    decs = spec["decisions"]
    n = len(decs)
    blocks = [[NOTE], ["[Cover]", _flat(spec["title"])]]
    blocks += [decision_lines(dec, k, n) for k, dec in enumerate(decs, 1)]
    summary = ["[Summary: one row per decision, with its answer once given]"]
    summary += [f"{dec['id']} {_flat(dec['title'])}" for dec in decs]
    if spec.get("decided"):
        summary.append("[Decided in earlier rounds]")
        summary += [f"{_flat(d['title'])}: {_flat(d['answer'])}" for d in spec["decided"]]
    blocks.append(summary)
    return "\n\n".join("\n".join(b) for b in blocks) + "\n"


def cmd_text(args, load_or_exit) -> int:
    """`decision_deck.py text`: print the deck's text, or write it to --out; exit 2 when --out cannot be written."""
    text = deck_text(load_or_exit(args.spec))
    if not args.out:
        sys.stdout.write(text)
        return 0
    out = Path(args.out).expanduser()
    try:
        out.write_text(text, encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"decision_deck text: {exc.strerror or exc}: {out}\n")
        return 2
    print(f"TEXT {out.resolve()} ({len(text.splitlines())} lines)")
    return 0


def add_text_parser(sub, load_or_exit) -> None:
    """Register the `text` subcommand on decision_deck.py's subparsers; load_or_exit is decision_deck's spec loader
    (passed in, so this module never imports decision_deck)."""
    t = sub.add_parser("text", help="the deck's words as plain text, slide by slide (for the legibility read)",
                       description="Print every word the spec puts on a slide, in slide order: the cover title; per "
                                   "decision the slide title, the question when it moved under the evidence, the "
                                   "recommendation's why, the evidence as text (table rows, the diff paragraph by "
                                   "paragraph, chart bars and values with the side panel and source, pictures by "
                                   "column and caption), the context line with each option's caption, pros and "
                                   "cons, and the answer buttons with the Recommended mark; then the summary rows and "
                                   "the earlier rounds' answers. Lines in [square brackets] say where the text sits; "
                                   "the deck's fixed controls (Start, keys, Comment, Done) are left out. Nothing is "
                                   "served, rendered or written but --out. Exit 2 for a bad spec or an unwritable "
                                   "--out.")
    t.add_argument("--spec", required=True, help="spec JSON")
    t.add_argument("--out", metavar="FILE", help="write the text here and print 'TEXT <path> (<n> lines)' "
                                                 "(default: print it)")
    t.set_defaults(func=lambda args: cmd_text(args, load_or_exit))
