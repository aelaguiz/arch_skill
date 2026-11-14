"""Decision deck inline text: escaping, links, command flags kept whole, and numbers as the deck shows them.

Every piece of spec text the deck renders goes through `e` (escaped) or `linked` (escaped, each http(s) URL a link
that opens in a new tab, each command flag in a span that never breaks at its hyphen). The redline (decision_deck_diff.py)
and the chart, table and context row (decision_deck_deck.py) build on these.
"""
from __future__ import annotations

import re
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_marks import MARKS, N0, N1  # noqa: E402


def e(text) -> str:
    return escape(str(text if text is not None else ""), quote=True)


# ------------------------------------------------------------------ links

# An http(s) URL in spec text: the scheme, then everything up to whitespace, a quote or an angle bracket. No other
# scheme ever becomes a link. The page script (decision_deck_script.py, `linkify`) uses the same pattern and trimming.
URL = re.compile(r"(?<![\w/])https?://[^\s<>\"'%s]+" % MARKS, re.I)     # a formatting mark ends a URL too
TRAIL = ".,;:!?"            # sentence punctuation after a URL stays outside the link
CLOSE = {")": "(", "]": "[", "}": "{"}


def _trim(url: str) -> str:
    """The URL without trailing punctuation, and without a closing bracket it never opened ("(see https://x.org)")."""
    while url:
        last = url[-1]
        if last in TRAIL or (last in CLOSE and url.count(last) > url.count(CLOSE[last])):
            url = url[:-1]
        else:
            break
    return url


def url_spans(text: str) -> list[tuple[int, int]]:
    """(start, end) of each linkable URL in raw text."""
    spans = []
    for m in URL.finditer(text):
        url = _trim(m.group(0))
        if "://" in url and not url.endswith("://"):
            spans.append((m.start(), m.start() + len(url)))
    return spans


def anchor(url: str) -> str:
    return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(url)}</a>'


FLAG = re.compile(r"(?<![\w-])--?[A-Za-z0-9][\w=./:-]{0,26}(?![\w=./:-])")
KEPT = re.compile(f"({N0}[^{N1}]*{N1})")                  # a code span that already never wraps


def keep_flags(html: str) -> str:
    """Escaped text with each command flag ("-g", "--dry-run") in <span class="nb">, so a line never ends on the
    flag's hyphen ("-g -" / "na"). A hyphen inside a word ("sign-in") or standing alone is left as it is."""
    return "".join(part if k % 2 else FLAG.sub(lambda m: f'<span class="nb">{m.group(0)}</span>', part)
                   for k, part in enumerate(KEPT.split(html)))


def flagged(text) -> str:
    return keep_flags(e(text))


def linked(text, plain=flagged) -> str:
    """Raw text as HTML with each http(s) URL a link that opens in a new tab: every part escaped first, the text
    between URLs through `plain` (escaped with its flags kept whole by default; keep_whole-wrapped for table cells)."""
    text = str(text if text is not None else "")
    out, last = [], 0
    for start, end in url_spans(text):
        out += [plain(text[last:start]), anchor(text[start:end])]
        last = end
    out.append(plain(text[last:]))
    return "".join(out)


def number(val) -> str:
    """12 -> '12', 1234 -> '1,234', 2.5 -> '2.5', 0.125 -> '0.13'."""
    if isinstance(val, int) or float(val).is_integer():
        return f"{int(val):,}"
    return f"{val:,.2f}".rstrip("0").rstrip(".")
