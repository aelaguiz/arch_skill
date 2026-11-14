# Bakery site example

A fictional bakery is relaunching its website and the owner has four choices to make before launch. The business, its survey and its order figures are invented for this example. `spec.json` asks them as one deck round:

1. D1, pictures: which homepage hero layout to use (`hero-split.svg` or `hero-banner.svg`).
2. D2, a diff: whether the returns policy takes the new wording, with the full rule as it would read.
3. D3, a bar chart: which delivery fee to charge, from twelve weeks of orders.
4. D4, a table: which opening hours to show.

Each decision carries a recommendation, and the `decided` list holds one choice made in an earlier round, which shows on the summary slide.

Run these from the skill folder (`skills/decision-deck/`).

Check the layout at desktop and phone width. This needs Python Playwright and its Chromium; it writes the PNGs to `--out` and a `spec.checked.json` stamp beside the spec when the result is CLEAN:

```sh
python3 scripts/decision_deck_check.py --spec examples/bakery-site/spec.json --out /tmp/bakery-check
```

Serve the deck on this machine and open the printed URL in a browser. Leave it running while the owner answers:

```sh
python3 scripts/decision_deck.py serve --spec examples/bakery-site/spec.json
```

Read the answers, from another terminal:

```sh
python3 scripts/decision_deck.py status --spec examples/bakery-site/spec.json
```

The answers land in `examples/bakery-site/ledger.jsonl`. Move that file and the stamp away when you are done if you want the example back as it was.
