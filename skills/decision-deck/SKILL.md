---
name: decision-deck
description: "Put approvals and choices to a person (the owner) as a decision deck: one interactive HTML presentation per round, one decision per slide, the exact thing being decided on the slide (pictures, a redline of a text change, a chart or a table), the options as one-click buttons, each click and comment recorded at once in an append-only ledger the asking agent watches and acts on, and a plain-text copy of every ask for the chat message. Use when an agent needs someone's yes, no or pick on something they must see to judge (mockups, wording changes, numbers, options side by side), when several decisions are waiting at once, or when the owner will answer from a phone or later. Not for one quick question that fits in a chat message, for presenting findings as slides ($deck-authoring), for written reports, or for card or inbox approval systems, which are a different surface."
metadata:
  short-description: "Ask for approvals one decision per slide and act on each click"
---

# Decision Deck

When you need the owner's approval or choice and a page is the right place to
ask, serve a decision deck: one interactive HTML presentation per round, one
decision per slide. Four ideas make it work, and every choice below serves one
of them:

- **One decision per slide, with the question as the title.** Nothing gets
  approved in a bundle or lost halfway down a long page.
- **The exact thing being decided is on the slide, at a size the owner can
  judge**: the picture, the redline of the text change, the chart, the table.
  A summary never stands in for it.
- **The owner answers by clicking where the evidence is.** Each click and
  comment lands at once in an append-only ledger. You act on each answer as it
  lands and write what you did back onto the slide.
- **Every ask also travels as plain text in the chat message** (the `asks`
  output), so the owner can answer from a phone or from chat, and an answer
  there counts the same as a click.

The tool is `scripts/decision_deck.py` (standard library only) plus a layout
checker, `scripts/decision_deck_check.py`, which needs Python Playwright. Below,
`<this skill>` is this skill's folder and `<dir>` is the round's task folder.
`python3 <this skill>/scripts/decision_deck.py --help` is the reference for
spec keys, evidence kinds, ledger records and what each subcommand prints; read
it before writing your first spec. A complete example round is in
`examples/bakery-site/`.

## Deck or chat question

Use a deck when the owner has to see something to judge it (two mockups, a
change to rule or policy wording, numbers that decide between options), when
several decisions are waiting at once, or when the owner may answer later or
from another device. Ask in chat when it is one question whose whole ask fits
in a few lines of text and the owner is in the conversation now. Never collect
several decisions on one scrolling page; that is the failure the deck exists to
replace.

Don't ask what is already settled. If the owner's own words already state the
direction, act on them instead of putting a mockup to them as a question.

## What a decision slide holds

Each slide holds one decision and only the ask:

- **The question** as the title: one sentence the owner can answer.
- **The recommendation's why** in the callout, tied to the owner's goal. The
  Recommended mark sits on its button, so the callout never repeats the answer.
  With no recommendation, say why not.
- **One kind of evidence**, chosen by what the decision turns on: `images` for
  a choice by eye, `diff` for a text change, `chart` for numbers being
  compared, `table` for options that differ on several attributes.
- **Two to four options**, recommended first, each a label the owner would say
  as an answer, plus the comment box (on by default).
- **One context line**: what the options share, or what the change does.

Everything else stays off: how the work was checked, review findings, history,
process. Those go in the chat message or a linked file. Each fact appears once
per slide: captions never repeat option labels, and nothing restates the title.

A comparison opens on the proposed version, with the current one after it
marked as current. A rule applied in many places is asked once: one slide with
the rule, its exceptions, two or three examples and a count, never one slide
per place. Use words the owner already knows: an id such as D1 is a handle for
the answer, never the explanation, and an earlier decision is described by
what it decided, not by its label.

[references/decision-slides.md](references/decision-slides.md) covers choosing
the evidence kind and sizing it, with a worked example. Read it when writing a
spec.

## Running a round

1. **Write the spec.** Re-read the live state first and drop anything already
   settled. Write `<dir>/spec.json` with every picture inside `<dir>`. Give each
   decision a short id (`D1`, `D2`); ids are never reused for a different
   decision.
2. **Check the layout at desktop and phone width, then look at it.**
   ```bash
   python3 <this skill>/scripts/decision_deck_check.py --spec <dir>/spec.json --out <dir>/check
   ```
   Fix every problem line in the spec until the last line reads `CLEAN`; a
   clean run writes the check stamp beside the spec. Then look at the PNGs in
   `<dir>/check` yourself, desktop and phone. The checker measures boxes, not
   whether a slide makes sense. On a rerun, its `PNGS` line names the images
   that changed, which are the ones to look at again.
3. **Have a fresh reader read the words cold.**
   ```bash
   python3 <this skill>/scripts/decision_deck.py text --spec <dir>/spec.json --out <dir>/deck-text.txt
   ```
   Give that file to a reader with no context from your work (a clean child
   agent under `../_shared/agent-orchestration-policy.md`) and ask, for each
   slide, whether they could answer it from the slide alone and what they
   would ask back. Fix what they find, then go back to step 2: any spec edit
   needs a new `CLEAN` run.
4. **Serve it in the background** and take the URL from the first line of the
   log, `URL <url>`:
   ```bash
   nohup python3 <this skill>/scripts/decision_deck.py serve --spec <dir>/spec.json --require-checked > <dir>/server.log 2>&1 &
   ```
   It binds loopback by default. When the owner looks from another device, see
   [references/running-a-round.md](references/running-a-round.md) for `--host`.
5. **Give the owner the URL together with the full text asks.**
   ```bash
   python3 <this skill>/scripts/decision_deck.py asks --spec <dir>/spec.json --url <url>
   ```
   Paste its output whole into the message, and add what the spec does not
   hold: what a yes changes and the evidence behind the recommendation. Open
   the URL where the owner is looking when you can.
6. **Watch the ledger.** Run `watch` as a background watcher where your host
   has one; it prints one `PICK`, `COMMENT`, `SKIP` or `DONE` line per event:
   ```bash
   python3 <this skill>/scripts/decision_deck.py watch --spec <dir>/spec.json
   ```
   Otherwise run `status` each turn. Run `status` before telling the owner a
   decision is still open, and after any resume, since a background watch does
   not survive one.
7. **Act on each pick and comment as it lands.** The owner's Done press gates
   nothing. Mark the decision acting, do the work, then report it, always
   naming the pick with the `pick=<ts>` value from its `PICK` line:
   ```bash
   python3 <this skill>/scripts/decision_deck.py act D1 --spec <dir>/spec.json --state acting --pick-ts <ts>
   python3 <this skill>/scripts/decision_deck.py act D1 --spec <dir>/spec.json --state done --result "Switched the homepage to the split hero" --pick-ts <ts>
   ```
   Use `--state failed` with the reason when it fails. Answer a comment with
   `reply D2 --spec <dir>/spec.json --text "..."`; a comment alone leaves the
   decision open. A new `PICK` for a decision you already acted on means the
   owner changed the answer: reverse or redo the work and report against the
   new pick's timestamp. An answer given in chat counts the same; record it on
   the deck as [references/running-a-round.md](references/running-a-round.md)
   shows, then act on it. Quote the owner's picks back
   when you report.
8. **Carry only open decisions into the next round.** A later round is a new
   spec in a new folder, so it gets its own ledger (the default ledger is
   `ledger.jsonl` beside the spec), holding only what is still open, with earlier answers
   in the spec's `decided` list, which shows read-only on the summary slide. A
   decided item never comes back as a decision; a real change to one is a new
   decision with a new id. `serve` and `watch` read the spec once, so restart
   both after editing it.

The server stops by itself once every decision is picked and a grace period has
passed, or at its maximum lifetime; `watch --spec` then prints
`SERVER_STOPPED` and exits.

## Done when

- The check printed `CLEAN`, you looked at the desktop and phone PNGs, and the
  cold reader's findings are fixed.
- The owner has the URL and the full text asks in one message.
- `status` shows, for every picked decision, a `STATE ... done` or `failed`
  line with a result, and you have told the owner what you did, quoting each
  pick. Anything still `OPEN` is named to the owner as still waiting.

## References

- [references/decision-slides.md](references/decision-slides.md): what a slide
  holds, choosing and sizing the evidence, and a worked example. Read when
  writing or fixing a spec.
- [references/running-a-round.md](references/running-a-round.md): the bind
  address for another device, installing Playwright for the checker, the files
  a round leaves, recording an answer given in chat, and reading `watch` and
  `status`. Read before serving to another device or when something in a
  round surprises you.
- `python3 <this skill>/scripts/decision_deck.py --help` and
  `python3 <this skill>/scripts/decision_deck_check.py --help`: every spec key,
  evidence kind, ledger record, output line and problem kind.
