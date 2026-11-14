"""Decision deck redline: the text diff with its rule panel and legend.

A diff decision's before and after are split into paragraphs, aligned in order and each shown either word by word
(an edit: removed runs in <del>, added runs in <ins>) or whole (a rewrite: old struck, new underlined). A long
unchanged run folds its middle behind a button. The paragraphs are rule text, so their Markdown is prepared and
finished by decision_deck_marks.py; escaping and links come from decision_deck_inline.py.
"""
from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_inline import e, linked, url_spans  # noqa: E402
from decision_deck_marks import MARKS, SP, balanced, finish, prepare, shown_len  # noqa: E402

FOLD_AT = 240               # an unchanged run longer than this folds to about its first and last 80 characters

# ------------------------------------------------------------------ diff

SPACE = re.compile(r"\s")


def _fold(text: str) -> str:
    """An unchanged run, linked; past FOLD_AT it shows about its first and last 80 characters and folds the middle.
    Each cut moves to a word boundary so no word is split: the head ends on the last whitespace at or before its cut
    and the tail starts on the first whitespace at or after its cut (a side with no such whitespace keeps its cut).
    A cut that would land inside a URL moves to the URL's edge instead, so a URL is never cut either."""
    if shown_len(text) <= FOLD_AT:
        return linked(text)
    cut1, cut2 = 80, len(text) - 80
    url1 = url2 = False
    for start, end in url_spans(text):
        if start < cut1 < end:
            cut1, url1 = end, True
        if start < cut2 < end:
            cut2, url2 = start, True
    if not url1:
        spaces = [m.start() for m in SPACE.finditer(text, 0, cut1 + 1)]
        cut1 = spaces[-1] + 1 if spaces else cut1
    if not url2:
        space = SPACE.search(text, cut2 - 1)
        cut2 = space.start() if space else cut2
    if cut2 <= cut1:
        return linked(text)
    head, mid, tail = text[:cut1], text[cut1:cut2], text[cut2:]
    if not (balanced(head) and balanced(mid) and balanced(tail)):      # a cut inside one formatted word: show it whole
        return linked(text)
    return (f'{linked(head)}<button type="button" class="fold" aria-expanded="false">&hellip; {shown_len(mid):,} more '
            f'characters</button><span class="folded" hidden>{linked(mid)}</span>{linked(tail)}')


# Under a desktop evidence box that scrolls, until it is scrolled to the end (the page script shows and hides it).
SCROLL_HINT = '<p class="scrollhint" data-scrollhint hidden aria-hidden="true">Scroll for the rest &darr;</p>'
REWRITE_AT = 0.5            # a paragraph pair sharing less than half its words (difflib ratio) is a rewrite


def paragraphs(text: str) -> list[str]:
    """Blank-line-separated paragraphs, stripped; empty ones dropped."""
    return [x.strip() for x in re.split(r"\n\s*\n", text.strip()) if x.strip()]


def word_ratio(a: str, b: str) -> float:
    """How much of two paragraphs' words match, 0 to 1 (difflib's 2*matches / total words)."""
    return difflib.SequenceMatcher(None, a.split(), b.split(), autojunk=False).ratio()


def align(before: list[str], after: list[str]) -> list[tuple[str | None, str | None]]:
    """Pair old and new paragraphs in order, maximising the words they share: (old, new) pairs, (old, None) for a
    removed paragraph and (None, new) for an added one. With equal counts and nothing better, they pair in order."""
    n, m = len(before), len(after)
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            best[i][j] = max(best[i + 1][j + 1] + word_ratio(before[i], after[j]), best[i + 1][j], best[i][j + 1])
    out, i, j = [], 0, 0
    while i < n and j < m:
        pair = best[i + 1][j + 1] + word_ratio(before[i], after[j])
        if pair >= best[i][j] - 1e-9 and (pair >= best[i + 1][j] and pair >= best[i][j + 1]):
            out.append((before[i], after[j]))
            i, j = i + 1, j + 1
        elif best[i + 1][j] >= best[i][j + 1]:
            out.append((before[i], None))
            i += 1
        else:
            out.append((None, after[j]))
            j += 1
    return out + [(x, None) for x in before[i:]] + [(None, y) for y in after[j:]]


def _words(text: str) -> tuple[str, list[tuple[str, str]]]:
    """A paragraph's leading whitespace and its (word, whitespace after it) pairs."""
    return text[: len(text) - len(text.lstrip())], re.findall(r"(\S+)(\s*)", text)


def _run(words: list[tuple[str, str]]) -> tuple[str, str]:
    """A run of words joined with their own whitespace, and the whitespace after its last word."""
    return "".join(w + s for w, s in words[:-1]) + words[-1][0], words[-1][1]


STOPS = (".", "!", "?", ":", ";")


def _edge_score(prev: str | None, last: str) -> int:
    """How well a change sits between sentences: its first word follows a sentence end (or opens the paragraph) and
    its last word ends one."""
    def ends(word):
        return word.rstrip("\"')]”’" + MARKS).endswith(STOPS)
    return 2 * (prev is None or ends(prev)) + ends(last)


def settle(ops: list[tuple], a: list[str], b: list[str]) -> list[tuple]:
    """The opcodes with each pure insertion or removal slid, where its words allow, to start on a sentence.
    "x. A | new. A | y" and "x. | A new. | A y" are the same change; the second marks the added sentence from its first
    word. A slide moves the mark only: the words on each side stay as they are. Ties keep difflib's place."""
    ops = [list(op) for op in ops]
    for k, (tag, i1, i2, j1, j2) in enumerate(ops):
        if tag not in ("insert", "delete") or k == 0 or ops[k - 1][0] != "equal":
            continue
        seq, lo, hi = (b, j1, j2) if tag == "insert" else (a, i1, i2)
        room = ops[k - 1][2] - ops[k - 1][1]                   # words in the unchanged run before the change
        best, at = _edge_score(seq[lo - 1] if lo else None, seq[hi - 1]), 0
        n = 0
        while n < room and lo - n - 1 >= 0 and seq[lo - n - 1] == seq[hi - n - 1]:
            n += 1
            score = _edge_score(seq[lo - n - 1] if lo - n else None, seq[hi - n - 1])
            if score > best:
                best, at = score, n
        if not at:
            continue
        ops[k - 1][2] -= at
        ops[k - 1][4] -= at
        ops[k][1:] = [i1 - at, i2 - at, j1 - at, j2 - at]
        if k + 1 < len(ops) and ops[k + 1][0] == "equal":
            ops[k + 1][1] -= at
            ops[k + 1][3] -= at
        else:                                                 # the change ended the paragraph: the slid words follow it
            ops.insert(k + 1, ["equal", i2 - at, i2, j2 - at, j2])
    return [tuple(op) for op in ops if op[2] > op[1] or op[4] > op[3]]


INWORD = "-'’_/"            # with letters and digits, what a word is made of: a mark never starts or ends inside one


def peel(old: str, new: str) -> tuple[str, str, str, str] | None:
    """A replaced run that is one addition or removal beside punctuation: (unchanged start, "ins" or "del", the
    changed text, unchanged end), else None. Words carry their punctuation, so `script.` to `script or a tool.` reads
    word by word as the whole phrase replaced; here it is " or a tool" added before the full stop. None when the two
    runs differ in more than one place, or the mark would start or end inside a word, a number, a URL, a quoted
    phrase or a formatted phrase."""
    short, long, kind = (old, new, "ins") if len(old) < len(new) else (new, old, "del")
    whole = url_spans(long) + [m.span() for m in re.finditer(r"\S+", long) if SP in m.group()]   # never cut inside

    def inside(left: str, right: str) -> bool:
        return bool(left and right) and all(c.isalnum() or c in INWORD for c in (left[-1], right[0]))

    most = next((k for k, (x, y) in enumerate(zip(short, long)) if x != y), len(short))
    for pre in range(most, -1, -1):
        tail = short[pre:]
        if not long.endswith(tail):
            continue
        head, mid = long[:pre], long[pre: len(long) - len(tail)]
        cuts = (pre, len(long) - len(tail))
        if (mid.strip() and not inside(head, mid) and not inside(mid, tail) and not inside(head, tail)
                and not any(start < cut < end for cut in cuts for start, end in whole)
                and balanced(head) and balanced(mid) and balanced(tail)):
            return head, kind, mid, tail
    return None


def _peeled(cut: tuple[str, str, str, str]) -> str:
    head, kind, mid, tail = cut
    body = mid.strip()
    lead, trail = mid[: len(mid) - len(mid.lstrip())], mid[len(mid.rstrip()):]
    return f"{linked(head)}{e(lead)}<{kind}>{linked(body)}</{kind}>{e(trail)}{linked(tail)}"


def word_diff(before: str, after: str) -> str:
    """One paragraph's change word by word: removed runs in <del>, added runs in <ins>, unchanged runs as they are.
    Words are matched on their own, so the spaces between words never split a changed phrase into alternating
    one-word pairs; a changed region is one removed run followed by one added run. An added or removed sentence is
    marked from its first word (settle), and an addition or removal beside punctuation marks only itself (peel)."""
    _, a = _words(before)
    lead_b, b = _words(after)
    segs = []                                   # (kind, text, gap after it)
    wa, wb = [w for w, _ in a], [w for w, _ in b]
    for tag, i1, i2, j1, j2 in settle(difflib.SequenceMatcher(None, wa, wb, autojunk=False).get_opcodes(), wa, wb):
        if tag == "equal":
            text, gap = _run(b[j1:j2])
            segs.append(("equal", text, gap or a[i2 - 1][1]))   # the new text ended here but old words follow
            continue
        cut = peel(_run(a[i1:i2])[0], _run(b[j1:j2])[0]) if tag == "replace" else None
        if cut:
            segs.append(("peel", cut, b[j2 - 1][1] or a[i2 - 1][1]))
            continue
        if i2 > i1:
            segs.append(("del", *_run(a[i1:i2])))
        if j2 > j1:
            segs.append(("ins", *_run(b[j1:j2])))
    out = [e(lead_b)]
    for k, (kind, text, gap) in enumerate(segs):
        nxt = segs[k + 1][0] if k + 1 < len(segs) else None
        gap = gap or (" " if nxt else "")
        if kind == "equal":
            out.append(_fold(text) + e(gap))
        elif kind == "peel":
            out.append(_peeled(text) + e(gap))
        else:
            out.append(_marked(kind, text + gap, keep_gap=not (kind == "del" and nxt == "ins")))
    return "".join(out)


def rewrite_diff(before: str, after: str) -> str:
    """A rewritten paragraph: the whole old paragraph struck through and, on the next line, the whole new paragraph
    underlined, shared opening words included, so each reads as a complete paragraph."""
    return f"<del>{linked(before)}</del><br><ins>{linked(after)}</ins>"


def paragraph_diff(before: str | None, after: str | None) -> str:
    """One paragraph pair: word by word for an edit, whole old then whole new for a rewrite. The paragraphs are rule
    text, so their Markdown is prepared first (decision_deck_marks) and the caller finishes the HTML."""
    old, new = (None if x is None else prepare(x) for x in (before, after))
    if after is None:
        return f"<del>{linked(old)}</del>"
    if before is None:
        return f"<ins>{linked(new)}</ins>"
    if before == after:
        return _fold(old)
    return word_diff(old, new) if word_ratio(before, after) >= REWRITE_AT else rewrite_diff(old, new)


def inline_diff(before: str, after: str) -> str:
    """The change as a redline, one <p class="line"> per paragraph: paragraphs aligned in order, each an edit marked
    word by word or a rewrite shown whole (old struck, new underlined); removed text in <del>, added in <ins>."""
    if not before.strip():
        new = "\n\n".join(prepare(x) for x in paragraphs(after))
        return finish(f'<p class="line"><span class="newline">New text</span> <ins>{linked(new)}</ins></p>')
    return finish("".join(f'<p class="line">{paragraph_diff(x, y)}</p>'
                          for x, y in align(paragraphs(before), paragraphs(after))))


def _marked(tag: str, text: str, keep_gap: bool = True) -> str:
    """A removed or added run with its trailing whitespace outside the tag, so the line never runs into the gap. A
    removed run directly followed by an added one drops its gap (del + ins carries its own margin)."""
    body = text.rstrip()
    return f"<{tag}>{linked(body)}</{tag}>{e(text[len(body):]) if keep_gap else ''}"


def diff_html(ev: dict) -> str:
    """The rule panel (one paragraph per blank-line-separated part of rule_now; single line breaks kept by CSS) beside
    the redline, both in one scroll box on the desktop."""
    rule = ev.get("rule_now") or ""
    paras = "".join(f"<p>{finish(linked(prepare(x)))}</p>" for x in paragraphs(rule))
    panel = (f'<div class="panel"><p class="h">The rule now reads</p>{paras}</div>' if rule else "")
    lines = inline_diff(ev["before"], ev["after"])
    return (f'<div class="ev fit"><div class="tx{"" if rule else " one"}">{panel}<div class="lines" tabindex="0" '
            f'aria-label="The change">{legend_html(lines)}{lines}</div></div>{SCROLL_HINT}</div>')


def legend_html(lines: str) -> str:
    """The key to the redline's marks, naming only the marks it has; nothing for a redline with no change."""
    said = [(tag, word) for tag, word in (("del", "removed"), ("ins", "added")) if f"<{tag}>" in lines]
    if not said:
        return ""
    heard = " and ".join(f"{'struck-through' if tag == 'del' else 'underlined'} text is {word}" for tag, word in said)
    marks = " &middot; ".join(f'<{tag} aria-hidden="true">{word}</{tag}>' for tag, word in said)
    return f'<p class="legend"><span class="sr-only">{heard[0].upper()}{heard[1:]}. </span>{marks}</p>'
