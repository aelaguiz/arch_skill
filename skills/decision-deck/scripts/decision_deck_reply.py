"""The text copy of each ask in a decision deck, for the agent to paste into the chat message that goes with it.

The message carries the full text ask of each decision with the deck's URL, so the owner can answer from chat as well
as from the deck. `decision_deck.py asks --spec S [--url URL] [--out FILE]` prints it: the URL first when given, then per decision in spec
order its id, title and question; the recommendation (the option's label and why, or "No recommendation." and why);
the exact thing as the text export writes it (decision_deck_text.evidence_lines, so a diff comes out in its plain form,
never with Markdown markers); the context line; and the options, labelled with the decision id plus a letter in
option order (D1a, D1b). The spec's `decided` list holds answers from earlier rounds, not asks, so it is left out.
Stdlib only, no rendering.
"""
from __future__ import annotations

import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_deck import context_text  # noqa: E402
from decision_deck_spec import evidence_of  # noqa: E402
from decision_deck_text import _flat, evidence_lines  # noqa: E402

LETTERS = string.ascii_lowercase     # option letters after the decision id: D1a, D1b ... D1z, then D1aa, D1ab


def option_label(dec_id: str, index: int) -> str:
    """`D1a` for the first option of D1; past z the letters run on as aa, ab (a deck rarely has that many)."""
    head, tail = divmod(index, len(LETTERS))
    return dec_id + (LETTERS[head - 1] if head else "") + LETTERS[tail]


def ask_lines(dec: dict) -> list[str]:
    """One decision's ask, line by line, in the spec's own words."""
    labels = {opt["id"]: option_label(dec["id"], i) for i, opt in enumerate(dec["options"])}
    rec = dec["recommendation"]
    picked = next((o for o in dec["options"] if o["id"] == rec.get("option")), None)
    out = [f"{dec['id']} ({_flat(dec['title'])}): {_flat(dec['question'])}",
           f"Recommendation: {labels[picked['id']]} ({_flat(picked['label'])}). {_flat(rec['why'])}" if picked
           else f"No recommendation. {_flat(rec['why'])}"]
    out += evidence_lines(dec)
    ctx = context_text(dec, False)      # False: the question already heads the block
    if ctx:
        out.append(f"Context: {_flat(ctx)}")
    if evidence_of(dec).get("source"):
        out.append(f"Source: {_flat(evidence_of(dec)['source'])}")
    out += [f"{labels[opt['id']]}. {_flat(opt['label'])}" for opt in dec["options"]]
    return out


def asks_text(spec: dict, url: str | None = None) -> str:
    """Every decision's ask in spec order, a blank line between them, with `Deck: <url>` first when given."""
    blocks = [[f"Deck: {url}"]] if url else []
    blocks += [ask_lines(dec) for dec in spec["decisions"]]
    return "\n\n".join("\n".join(b) for b in blocks) + "\n"


def cmd_asks(args, load_or_exit) -> int:
    """`decision_deck.py asks`: print the asks, or write them to --out; exit 2 when --out cannot be written."""
    text = asks_text(load_or_exit(args.spec), args.url)
    if not args.out:
        sys.stdout.write(text)
        return 0
    out = Path(args.out).expanduser()
    try:
        out.write_text(text, encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"decision_deck asks: {exc.strerror or exc}: {out}\n")
        return 2
    print(f"ASKS {out.resolve()} ({len(text.splitlines())} lines)")
    return 0


def add_asks_parser(sub, load_or_exit) -> None:
    """Register the `asks` subcommand on decision_deck.py's subparsers (load_or_exit passed in, as for `text`)."""
    t = sub.add_parser("asks", help="a plain-text copy of each ask, to paste into the chat message with the deck",
                       description="Print the full text ask of every decision in the spec, in spec order, as plain "
                                   "text to paste into the chat message that goes with the deck, so the owner can "
                                   "answer there too. With --url the first line is 'Deck: <url>'. Per "
                                   "decision: '<id> (<title>): <question>'; 'Recommendation: <id><letter> (<label>). "
                                   "<why>' or 'No recommendation. <why>'; the exact thing as `text` writes it; "
                                   "'Context: ...' (the context line, with each option's caption, pros and cons); "
                                   "'Source: ...' for a chart with a source; then one line per option, "
                                   "'<id><letter>. <label>', lettered a, b, c in spec order. The spec's decided list "
                                   "is left out. No Markdown, no HTML. Exit 2 for a bad spec or an unwritable --out.")
    t.add_argument("--spec", required=True, help="spec JSON")
    t.add_argument("--url", help="the deck's URL (the 'URL <url>' line serve prints), put on the first line")
    t.add_argument("--out", metavar="FILE", help="write the text here and print 'ASKS <path> (<n> lines)' "
                                                 "(default: print it)")
    t.set_defaults(func=lambda args: cmd_asks(args, load_or_exit))
