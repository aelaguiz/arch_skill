"""The --help text of decision_deck_check.py: what it renders, every problem kind it reports, the stamp and exit codes."""

HELP = """Check a decision deck before showing it: every slide at 1440x900 (desktop) and 390x844 (phone), every link
in it, and the size of each diff slide. A CLEAN run writes the check stamp that `decision_deck.py serve` looks for.

The fit rule: the answer row is always fully visible; evidence that does not fit scrolls inside one clearly bounded
box with no fade. On the desktop that is at most one scroll box per evidence zone; on the phone the page itself
scrolls and the evidence has no inner scroll box.

How it runs: the deck is served from the spec on 127.0.0.1 with a throwaway ledger in a temp folder (the round's own
ledger is never touched) and opened in headless Chromium through Python Playwright: the cover, each decision slide
and the summary, at both sizes.

Each layout problem is one line: `<KIND> <route> <width> <selector>: <what, in px>`. Px are CSS px of the slide (the
desktop stage is 960 x 540, scaled to the window) except OFFCARD, which is in screen px. The fit kinds:
  CLIPPED   content hidden by overflow: hidden (or clip), or running past the bottom of the desktop slide; a
            cut is allowed only when the full text is reachable (an ellipsis with a title attribute, or a
            control that opens it, such as Read all)
  FADED     a mask image fading evidence out
  OFFCARD   an answer button or the comment box that does not show whole without scrolling something other
            than the page: at either width, cut by a box between it and the page that clips or scrolls (the
            slide card itself included) or running past the card's bottom; on the desktop also not fully inside
            the viewport and its slide, or two of them overlapping
  WIDE      phone: an element wider than the viewport (or the page scrolling sideways)
  NESTED    phone: a scroll box inside the evidence zone
  SCROLLS   desktop: more than one scroll box in one evidence zone
The reading kinds, for what a reviewer would otherwise have to catch by eye:
  MIDWORD   text cut inside a word, by a fold button or by an ellipsis or line clamp
  MARKUP    Markdown markers showing as typed (`**`, a backtick pair, `[text](target)`, a `#` heading line): the
            deck formats Markdown only in a diff's before, after and rule_now; write plain words elsewhere
  LEGEND    the redline's legend names a mark (removed, added) the redline does not have
  GAP       more than 24 px of empty slide between the evidence and the line under it (a desktop picture fills
            its box by design and is not read)
  SMALL     chart text drawn under 11 px on the screen: an SVG chart's text, and a bar chart's labels, values,
            notes and legend
  KEYS      phone: a keyboard hint showing (a key cap, or a placeholder that names a key)
  TALL      phone: a slide more than 2.5 screens tall, so its answers are that far down; trim the evidence to
            what the decision turns on
  BROKEN    a command flag ("-g", "--dry-run") split after its hyphen at a line end, or a table heading split
            inside a word

Before the render the spec itself is checked; these lines are `<KIND> <decision id>:` (`deck` for the round's own
text):
  DEADLINK  an http(s) URL in the spec's text that answers with an error status or not at all (GET, 5 s timeout,
            redirects followed); a link the reader clicks must open
  TOOBIG    a diff whose before or after has more than 8 paragraphs (blank-line separated): show a shared change
            once as a rule and keep only the lines that need judgment
  NORECAP   a diff decision whose context is missing or under 20 characters: recap what changed there
  REPEAT    the same changed (old, new) paragraph pair on two slides or twice on one (paired as the deck pairs
            them; whitespace ignored, and a leading short "Label: " too when the rest still differs and has 3
            words; pairs under 3 words a side never count): show it once as a rule with its count
A 127.0.0.1 or localhost URL is probed from this machine too but only gets a `WARNING <id>: ...` line (it opens only
where a local server or tunnel exists); warnings do not make the round unclean. --no-link-probe skips the probe
(offline); the size checks always run. The last line is `CLEAN <n> routes at 1440x900 and 390x844` or
`PROBLEMS <k> in <n> routes at ...`.

--out <dir> saves one PNG per route and width (`desktop-cover.png`, `desktop-slide1.png`, ...,
`desktop-summary.png`; on the phone the whole slide, `phone-slide1.png`) and keeps `png-manifest.json` there (each
PNG's name to the SHA-256 of its bytes, rewritten every run). From the second run into the same folder, one line
before the last names what a review of the images still has to look at, for example
`PNGS 3 changed since the last run here: desktop-slide3.png phone-slide3.png phone-summary.png (5 unchanged)`: the
PNGs whose bytes changed or are new, then `; <m> removed: <names>` for any made last run and not this time, and the
count left byte-identical. It is never a problem. The first run, or a run after an unreadable or malformed manifest
(said on stderr), prints no PNGS line.

The stamp: a CLEAN run writes `<spec stem>.checked.json` beside the spec, one SHA-256 over the spec and every picture
the deck shows, taken when the check loaded them; a change during the check writes no stamp (exit 2). `serve` warns
about a spec without a matching stamp, or refuses it with --require-checked, so any edit means a new checked run.

Exit 0 clean, 1 when any problem is found, 2 on a usage error, a bad spec, a file error (such as an --out path that
is a file or cannot be written), or no Playwright or Chromium
(`python3 -m pip install playwright && python3 -m playwright install chromium`).
"""
