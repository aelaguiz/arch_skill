"""Decision deck redline text: rule text written in Markdown shows formatted, and short phrases are marked whole.

The text a diff decision quotes (before, after, rule_now) is usually Markdown. `prepare` turns one paragraph into the
same text with its markers replaced by private-use characters, each word carrying its own pair, so the redline can
cut between any two words and every tag still closes; `finish` turns those characters into tags once the HTML is
built, and `plain` drops them for the text export. What is formatted: `**bold**`, `` `code` ``, a `# heading` line
(bold, without its hashes), a list item's `- ` (a bullet) and `[text](target)` (the text; an http(s) target follows
it in brackets as a link, any other target is kept out of sight but still counts as a change). Anything unpaired
stays as typed.
Marked whole: a code span up to CODE_ATOM characters and a double-quoted phrase up to QUOTE_WORDS words are one word
to the redline, so a change inside one strikes the whole phrase and underlines the whole new one. A code span up to
NB_MAX characters never wraps.
"""
from __future__ import annotations

import re

B0, B1, C0, C1, SP, N0, N1, L0, L1 = (chr(c) for c in range(0xE000, 0xE009))
MARKS = B0 + B1 + C0 + C1 + SP + N0 + N1 + L0 + L1
PAIRS = ((B0, B1), (C0, C1), (N0, N1), (L0, L1))
TAGS = {B0: "<strong>", B1: "</strong>", C0: "<code>", C1: "</code>", SP: " ", N0: '<span class="nb">', N1: "</span>"}
HIDDEN = re.compile(f"{L0}[^{L1}]*{L1}")
STRIP = re.compile(f"[{MARKS}]")
CODE_ATOM = 60              # a code span up to this long is one word to the redline
NB_MAX = 28                 # a code span or flag up to this long never wraps (it fits a phone line)
QUOTE_WORDS = 8             # a double-quoted phrase up to this many words is one word to the redline
QUOTE_CHARS = 80

HEADING = re.compile(r"[ \t]{0,3}#{1,6}[ \t]+(\S.*?)(?:[ \t]+#+)?[ \t]*")   # closing hashes need a space before them
BOLD_BEFORE, BOLD_AFTER = "([{\"'“‘", ".,;:!?)]}\"'”’"      # what may touch a bold marker's outer side
BULLET = re.compile(r"^([ \t]*)[-*+][ \t]+(?=\S)")      # a list item's marker, shown as a bullet
PIECE = re.compile(r"(?P<code>(?<!`)`(?!`)(?P<c>[^`\n]+?)`(?!`))"
                   r"|(?P<link>\[(?P<t>[^\]\[\n]+)\]\((?P<h>[^()\s]+)\))"
                   r"|(?P<bold>\*\*)")
OPENERS, CLOSERS = '"“', '"”'
QUOTES = '"“”'


def _pieces(text: str) -> list[tuple]:
    """("text", s) | ("code", s) | ("link", text, target) | ("bold",) in order."""
    out, last = [], 0
    for m in PIECE.finditer(text):
        if m.start() > last:
            out.append(("text", text[last:m.start()]))
        if m.group("code"):
            out.append(("code", m.group("c")))
        elif m.group("link"):
            out.append(("link", m.group("t"), m.group("h")))
        else:
            out.append(("bold",))
        last = m.end()
    if last < len(text):
        out.append(("text", text[last:]))
    return out


def _edge(piece: tuple | None, first: bool) -> str:
    """The character a piece shows at its start (first) or end; "" for none."""
    if piece is None or piece[0] == "bold":
        return "*" if piece else ""
    return piece[1][:1] if first else piece[1][-1:]


def _bold_pairs(pieces: list[tuple]) -> dict[int, bool]:
    """{index of a `**` piece: True for an opener, False for its closer}; a `**` in neither stays as typed. An opener
    starts a word (text right after it; before it a space, an opening bracket or quote, or nothing) and a closer ends
    one (text right before it; after it a space, closing punctuation or nothing), so the `**` of a glob, a URL or a
    power (`src/**/x`, `2**3`) is never a marker."""
    role, opened = {}, None
    for k, piece in enumerate(pieces):
        if piece[0] != "bold":
            continue
        before = _edge(pieces[k - 1], False) if k else ""
        after = _edge(pieces[k + 1], True) if k + 1 < len(pieces) else ""
        inner_left, inner_right = bool(before) and not before.isspace(), bool(after) and not after.isspace()
        if opened is not None and inner_left and k > opened + 1 and (not inner_right or after in BOLD_AFTER):
            role[opened], role[k], opened = True, False, None
        elif opened is None and inner_right and (not inner_left or before in BOLD_BEFORE):
            opened = k
    return role


def _wrap(run: str, bold: bool, code: bool, nowrap: bool) -> str:
    out = f"{N0}{run}{N1}" if nowrap else run
    out = f"{C0}{out}{C1}" if code else out
    return f"{B0}{out}{B1}" if bold else out


def _styled(text: str, bold: bool, code: bool = False, nowrap: bool = False, atom: bool = False) -> str:
    """Each word of `text` in its own marks; an atom keeps each inner space as one SP, so it stays one word and a
    space added inside a command is still a change."""
    if atom:
        return _wrap(re.sub(r"\s", SP, text), bold, code, nowrap)
    return "".join(part if part.isspace() or not part else _wrap(part, bold, code, nowrap)
                   for part in re.split(r"(\s+)", text))


def _inline(text: str, bold_all: bool = False) -> str:
    pieces = _pieces(text)
    role, bold, out = _bold_pairs(pieces), bold_all, []
    for k, piece in enumerate(pieces):
        kind = piece[0]
        if kind == "bold":
            if k in role:
                bold = bold_all or role[k]
            else:
                out.append(_styled("**", bold))
        elif kind == "code":
            code = piece[1].strip() or piece[1]
            out.append(_styled(code, bold, code=True, nowrap=len(code) <= NB_MAX, atom=len(code) <= CODE_ATOM))
        elif kind == "link":
            label, target = piece[1], piece[2]
            if re.match(r"https?://", target, re.I):
                out.append(_styled(f"{label} ({target})", bold))
            else:
                out.append(_styled(label, bold) + f"{L0}{target}{L1}")
        else:
            out.append(_styled(piece[1], bold))
    return "".join(out)


def _shown(word: str) -> str:
    return STRIP.sub("", HIDDEN.sub("", word))


def _quotes(text: str) -> str:
    """Join each short double-quoted phrase into one word (its inner spaces become SP)."""
    words = re.findall(r"(\S+)(\s*)", text)
    lead = text[: len(text) - len(text.lstrip())]
    out, k = [], 0
    while k < len(words):
        word, gap = words[k]
        seen = _shown(word).lstrip("([")
        opens = bool(seen) and seen[0] in OPENERS and not any(c in seen[1:] for c in QUOTES)
        end = None
        if opens:
            for j in range(k + 1, min(k + QUOTE_WORDS, len(words))):
                inner = _shown(words[j][0])
                if any(c in inner for c in CLOSERS):
                    end = j if sum(inner.count(c) for c in QUOTES) == 1 else None
                    break
                if "\n" in words[j - 1][1]:
                    break
        if end is not None and "\n" not in words[end - 1][1]:
            joined = SP.join(w for w, _ in words[k:end + 1])
            if len(_shown(joined)) <= QUOTE_CHARS:
                out.append(joined + words[end][1])
                k = end + 1
                continue
        out.append(word + gap)
        k += 1
    return lead + "".join(out)


def prepare(text: str) -> str:
    """One paragraph of rule text with its Markdown markers as private-use marks (module docstring)."""
    text = STRIP.sub("", str(text))
    out, plain = [], []

    def flush():
        if plain:
            out.append(_inline("\n".join(plain)))
            plain.clear()

    for line in text.split("\n"):
        m = HEADING.fullmatch(line)
        if m:
            flush()
            out.append(_inline(m.group(1), bold_all=True))
        else:
            plain.append(BULLET.sub("\\1• ", line))
    flush()
    return _quotes("\n".join(out))


def balanced(text: str) -> bool:
    """True when every mark pair in `text` closes inside it (so a cut around it leaves well-formed HTML)."""
    return all(text.count(a) == text.count(b) for a, b in PAIRS)


def shown_len(text: str) -> int:
    """How many characters of `text` show on the slide (an SP shows as its space)."""
    return len(_shown(text.replace(SP, " ")))


def finish(html: str) -> str:
    """Built HTML with the marks turned into tags; a link's hidden target goes."""
    if not any(c in html for c in MARKS):
        return html
    return STRIP.sub(lambda m: TAGS.get(m.group(0), ""), HIDDEN.sub("", html))


def plain(text: str) -> str:
    """A paragraph as the slide shows it, without tags: for the text export."""
    return STRIP.sub(lambda m: " " if m.group(0) == SP else "", HIDDEN.sub("", prepare(text)))
