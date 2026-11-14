"""Spec checks for decision_deck_check.py: the deck's links answer, no slide asks for a blanket approval, and no
change shows twice.

Checks that need no browser, run before the render:
- Links: every http(s) URL in the spec's text (found with decision_deck_deck.url_spans, the pattern the deck links
  with) is fetched once, GET with a 5 s timeout, redirects followed, body never read. An error status (4xx, 5xx) or
  a connection failure is a DEADLINK problem. A loopback URL (127.x, ::1, localhost) is probed from this machine
  too, but only warned about: it opens only where a local server or tunnel exists.
- Review size: a diff decision whose before or after has more than MAX_PARAGRAPHS blank-line-separated paragraphs
  is TOOBIG (a shared change goes once as a rule; only the lines that need judgment are shown one by one), and a
  diff decision without a recap of what changed in its context (under MIN_RECAP characters) is NORECAP.
- Repeats: each diff's paragraphs are paired as the deck pairs them (decision_deck_deck.paragraphs and align); a
  changed pair whose (old, new) key shows on two slides, or twice on one, is REPEAT: a deck asks each decision once,
  so a rule applied in many places is one slide. The key collapses whitespace and drops a leading short label
  ("Homepage: ") only when the stripped sides still differ and run to 3 words; a key under 3 words a side is too
  generic to report; the comparison is case-sensitive (pair_key).
"""
from __future__ import annotations

import http.client
import ipaddress
import re
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from decision_deck_diff import align
from decision_deck_diff import paragraphs as deck_paragraphs
from decision_deck_inline import url_spans

TIMEOUT_S = 5
MAX_PARAGRAPHS = 8
MIN_RECAP = 20
MAX_LABEL = 60                                            # a leading "<label>: " under this many characters is dropped
# a label holds no sentence punctuation: no ! ? ; and no "." ending a word ("index.html" is fine, "It works." is not)
LABEL = re.compile(r"(?=[^:\n]{1,%d}:\s)((?:[^.!?;:\n]|\.(?=[^\s:]))+):\s+" % (MAX_LABEL - 1))
MIN_WORDS = 3                                             # a repeat key side needs this many words to count
AGENT = "Mozilla/5.0 decision_deck_check/1"     # some sites refuse urllib's default agent outright
SKIP_KEYS = {"root", "path"}                    # added by load_spec; not deck text


def _strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for key, val in node.items():
            if key not in SKIP_KEYS:
                yield from _strings(val)
    elif isinstance(node, list):
        for val in node:
            yield from _strings(val)


def urls_by_owner(spec: dict) -> dict[str, list[str]]:
    """{url: [owner, ...]} in first-seen order; the owner is a decision id, or "deck" for the round's own text."""
    found: dict[str, list[str]] = {}

    def add(owner, node):
        for text in _strings(node):
            for start, end in url_spans(text):
                owners = found.setdefault(text[start:end], [])
                if owner not in owners:
                    owners.append(owner)

    add("deck", {k: v for k, v in spec.items() if k != "decisions"})
    for dec in spec.get("decisions") or []:
        add(str(dec.get("id")), dec)
    return found


def is_local(url: str) -> bool:
    try:
        host = (urllib.parse.urlsplit(url).hostname or "").lower()
    except ValueError:                  # a malformed URL ("http://[bad"): not local; the probe reports it
        return False
    if host == "localhost" or host.endswith(".localhost"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def probe(url: str, timeout: float = TIMEOUT_S) -> str:
    """"" when the URL answers 2xx or 3xx (after redirects), else why not ("HTTP 404", "no answer: ...")."""
    try:                                # a malformed URL or answer is a dead link, never a traceback
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": AGENT, "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:     # closed unread: no body kept
            code = resp.status
    except urllib.error.HTTPError as exc:
        exc.close()
        if 300 <= exc.code < 400:                                      # urllib gave up following redirects
            return f"HTTP {exc.code}, redirects never settle"
        code = exc.code
    except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError) as exc:
        reason = getattr(exc, "reason", None) or exc
        return f"no answer: {reason}"
    return "" if 200 <= code < 400 else f"HTTP {code}"


def link_lines(spec: dict, probe_fn=None) -> tuple[list[str], list[str]]:
    """(problems, warnings): a DEADLINK line per dead URL and owner; a WARNING line per loopback URL and owner."""
    found, probe_fn = urls_by_owner(spec), probe_fn or probe
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(zip(found, pool.map(probe_fn, found)))
    problems, warnings = [], []
    for url, owners in found.items():
        why = results[url]
        for owner in owners:
            if is_local(url):
                here = f"no answer here either ({why})" if why else "answers on this machine"
                warnings.append(f"WARNING {owner}: {url} opens only where a local server or tunnel exists; {here}")
            elif why:
                problems.append(f"DEADLINK {owner}: {url} ({why})")
    return problems, warnings


def paragraphs(text) -> int:
    text = str(text or "").replace("\r\n", "\n").replace("\r", "\n")     # CRLF and CR line endings
    return len([p for p in re.split(r"\n[ \t]*\n", text) if p.strip()])


def size_lines(spec: dict) -> list[str]:
    """TOOBIG and NORECAP lines for diff decisions."""
    out = []
    for dec in spec.get("decisions") or []:
        ev = dec.get("evidence") or {}
        if ev.get("kind") != "diff":
            continue
        did = dec.get("id")
        n = max(paragraphs(ev.get("before")), paragraphs(ev.get("after")))
        if n > MAX_PARAGRAPHS:
            out.append(f"TOOBIG {did}: {n} changes on one slide; show a shared change once as a rule and keep only "
                       f"the lines that need judgment, or split the change into decisions of their own")
        if len(str(dec.get("context") or "").strip()) < MIN_RECAP:
            out.append(f"NORECAP {did}: add a recap of what changed in context")
    return out


def collapse(text) -> str:
    return " ".join(str(text or "").split())


def normalize(text) -> str:
    """A paragraph with whitespace collapsed and a leading short label dropped."""
    text = collapse(text)
    m = LABEL.match(text)
    return text[m.end():] if m else text


def pair_key(old, new) -> tuple[str, str] | None:
    """The (old, new) key the repeat check compares, or None for a pair it never reports.
    Unchanged (equal with the label kept) is None. The label-stripped sides are the key only when they still differ
    and the longer has MIN_WORDS words; otherwise the label stays (so "Enable backups: No" and "Publish data: No"
    stay apart, and a label-only edit still counts). A key whose sides both have under MIN_WORDS words is too
    generic to be the same decision ("Yes" -> "Yes.") and is None."""
    raw = (collapse(old), collapse(new))
    if raw[0] == raw[1]:
        return None
    bare = (normalize(old), normalize(new))
    def words(pair):
        return max(len(x.split()) for x in pair)
    key = bare if bare[0] != bare[1] and words(bare) >= MIN_WORDS else raw
    return key if words(key) >= MIN_WORDS else None


def repeat_lines(spec: dict) -> list[str]:
    """One REPEAT line per set of slides that show the same changed (old, new) pair, in first-seen order."""
    seen: dict[tuple[str, str], list[str]] = {}
    for dec in spec.get("decisions") or []:
        ev = dec.get("evidence") or {}
        if ev.get("kind") != "diff":
            continue
        did = str(dec.get("id"))
        pairs = align(deck_paragraphs(str(ev.get("before") or "")), deck_paragraphs(str(ev.get("after") or "")))
        for old, new in pairs:
            key = pair_key(old, new)
            if key:
                seen.setdefault(key, []).append(did)
    out = []
    for ids in seen.values():
        if len(ids) > 1:
            line = (f"REPEAT {', '.join(dict.fromkeys(ids))}: the same change shows more than once; "
                    f"show it once as a rule with its count")
            if line not in out:
                out.append(line)
    return out


def spec_lines(spec: dict, links: bool = True, probe_fn=None) -> tuple[list[str], list[str]]:
    """(problems, warnings) from all checks; links=False skips the probe (offline)."""
    problems, warnings = link_lines(spec, probe_fn) if links else ([], [])
    return size_lines(spec) + repeat_lines(spec) + problems, warnings
