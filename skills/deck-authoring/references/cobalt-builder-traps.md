# Building and editing Cobalt decks from code: the traps, by where they bite

Owner: Chief · Written September 22, 2026 from the [Milkshake Economy deck](/Users/aelaguiz/workspace/psbrain/projects/product-economy/economy-deck.md) rebuild. On October 26 its eighty traps, several told three or four times as they recurred, were merged under the step each belongs to; the image-model traps moved to the [AI mock style guide](/Users/aelaguiz/workspace/psbrain/knowledge/ai-mock-style-guide.md) and Amir's deck preferences to the [deck guidance](/Users/aelaguiz/workspace/psbrain/shared/communication/decks.md). Each case's evidence folder is in this page's Git history.

## When to use it

Use this to build or restyle a Google Slides deck in the Poker Skill Cobalt style from code, or to keep editing one where each slide is a small spec. What a deck says and how it reads are `$deck-authoring`'s and the [deck guidance](/Users/aelaguiz/workspace/psbrain/shared/communication/decks.md)'s; this runbook covers the mechanics.

## The two things these builders get wrong

**A rebuild knows only the spec.** Each builder deletes a slide, draws it fresh from the spec and then moves every slide into the spec's `ORDER`. So anything the spec does not know is lost or moved on the next build, even an `--only=` build of one slide: a slide Amir added or moved, his edits to words, speaker notes, a hand-made element, the template's own slides, and the links other documents made to a slide by its number or object ID. On September 24 he added two slides to User Journeys minutes after a full rebuild, and the next run would have deleted them as stale; on September 27 a one-slide build would have quietly undone the order he had set by hand in the team focus deck. So before any build, read the live deck (order, every element's text and position, notes) and compare it with a `--dry` run; bring his changes into the spec (his order into `ORDER`, his slides kept); then build only the slides that changed and the ones whose text cites other slides' numbers, and fix every other footer in place.

**Text that fits by eye or by character count does not fit.** Estimates of 0.53 to 0.57 times the size per character left 123 text defects in the 65-slide trials research deck and 20 in its companion, all missed by eye on the contact sheets (C-166, September 26). Measure with the real fonts: [`scripts/cobalt_slides/text_fit.py`](/Users/aelaguiz/workspace/psbrain/scripts/cobalt_slides/text_fit.py) lays text out in Inter and Blinker the way Slides does and matched the PDF export's line breaks exactly.

## Before you start

1. Make a backup copy with `gws drive files copy` before replacing a deck's slides.
2. You can't import a Cobalt theme into an existing deck. Every Cobalt deck, the template included, is Simple Light with explicitly styled elements on BLANK slides, so restyle in place (same link) by building new slides and deleting the old ones. For a deck Amir is still writing, snapshot its JSON first, rebuild his slides with his words unchanged, and have the builder compare his originals with the snapshot right before deleting them, stopping if he edited them meanwhile (`.local-sources/meeting-notes-friday-2026-09-25/deck/build_mn.py`).
3. **A new deck:** copy the Cobalt template into the target folder with `gws drive files copy`, share the copy (and any new image folder) editable with everyone at fun.country ([sharing rule](/Users/aelaguiz/workspace/psbrain/knowledge/google-workspace-access.md#sharing-new-drive-items)), and delete the template's 12 slides (IDs `tpl_`) on the first build only (`--drop-template` in `.local-sources/skills-tracking-2026-09-24/deck/build_skills.py`). `0AGv6IyaNcm0eUk9PVA` is the root of Amir's My Drive, not a shared drive; files made there are his and still get the domain permission.
4. Source images from the old deck, the template logo or other decks through `contentUrl`, fetched right before the build, since it expires in about 30 minutes.

## Steps

1. **Write a spec.** One `Slide(sid, footer)` per slide in a Python file, using the helpers in [`scripts/cobalt_slides/cobalt.py`](/Users/aelaguiz/workspace/psbrain/scripts/cobalt_slides/cobalt.py): `frame`, `text`, `callout`, `card`, `pill`, `table` (with `us_cols` for Poker Skill columns), `box` and `line` for native diagrams, and `image`. End it with an `ORDER` list grouped into sections, each opened by a divider (`Slide.divider()`; why: `$deck-authoring`). Worked example: [`projects/product-economy/deck-build/spec.py`](/Users/aelaguiz/workspace/psbrain/projects/product-economy/deck-build/spec.py). A long, data-driven deck is best generated from a Markdown or data file in the repo (the lessons deck from `projects/milkshake/lessons/lessons.md` by `lessons_parse.py`; the onboarding deck's strips from the lanes' `flows/*.json`), so a corrected source changes the slide and a number can't drift from its screen. Edit the source, never the spec. Set `cobalt.FOOTER = "Poker Skill · <pod> · <deck name>"` in the spec before building, so each slide's foot says whose deck it is (Amir, November 12: "so I don't have to guess"); the default is plain "Poker Skill".
2. **Dry-run and measure.** `--dry` writes the request dump; run `python3 text_fit.py <request dump>.json` and build only at 0 issues (it flags WRAP, TALL, SPILL, UNDER, CLASH, EDGE and FOOT). Assert one-line headlines in `frame()` with `text_fit.lines_of`, and assert unique element IDs per slide (`build_home.py` in `.local-sources/home-deck-2026-09-24/deck/` does both).
3. **Compare with the live deck** as above, then **build** from a scratch directory: `python3 <repo>/projects/product-economy/deck-build/run.py eco_10 eco_12`, or no arguments for everything.
4. **Restore speaker notes** with `notes.py` (or the builder's `--notes`) after every build; rebuilding a slide wipes its notes.
5. **Render** with `python3 <repo>/scripts/cobalt_slides/pdfrender.py` (whole-deck PDF, `pdftoppm`, `pdf/p-NN.png` plus contact sheets) and read every changed page at full size.

## Traps, by where they bite

### Order, numbers and links

- **Never write a slide number by hand; compute it from `ORDER`.** The cover, dividers, footers and every "slide N" go stale after an insertion or a removal unless the builder learns them: the onboarding problem deck's builder (`projects/milkshake/onboarding-by-entry/problem/build.py`) builds every slide twice in memory, the first pass filling a slide-id-to-page map, the second writing `{p:<slide id>}` placeholders; `SN(sid)` and `SR(a, b)` in `.local-sources/pvai-sng-2026-09-25/deck/spec.py` do the same. A spec that plans IDs ahead must count only the slides it builds (the bots deck's last slide read "66 of 52").
- **Inserting or removing slides must not rebuild the deck.** Eleven dividers once started an 88-slide, 18-minute rebuild (Amir: "wtf 18 minutes to put in fucking dividers."). Build only the new slides and the ones that cite page numbers, then rewrite every other footer in place with one page-scoped `replaceAllText` each (the growth team builder's `--renumber`, 1 minute 40 seconds). Then check every live footer against its position through the API.
- **Builders delete live slides missing from `ORDER`, even on an `--only=` run.** Guard what isn't yours: `build_mocks.py` treats any slide whose ID lacks its prefix (`mk_`) as Amir's, never deletes it, keeps it after the builder slide it follows and counts it in footers; the problem deck's runner deletes only its own retired slides (`pb_`). A builder that refuses a partial build into the real deck can still build sections in parallel into scratch copies of the template (`LC_ONLY`, `LC_DECK` in the lifecycle research deck, C-167, brief `.local-sources/lifecycle-2026-09-26/deck/SECTION_BRIEF.md`); read the assembled dry run for material drawn twice before the full build.
- **Other documents link into a deck by slide object ID.** Pin the IDs (a `Slide ID` field written once in the source) before renumbering, give new slides a different prefix, diff the slide orders before and after, and fix linked slide numbers with [`scripts/cobalt_slides/remap_slide_links.py`](/Users/aelaguiz/workspace/psbrain/scripts/cobalt_slides/remap_slide_links.py) (dry first). When rewriting a Sheets cell's text with `updateCells` or `values update`, a whole-cell link is dropped: read its `textFormatRuns` first and send them back (two Master Sheet to-do links were lost this way on September 24).
- **`updateSlidesPosition` needs its IDs in their current deck order;** move one slide per request.
- **Slides can't move between files.** To split a deck, copy the whole file, delete the unwanted slides from each copy and renumber both decks' footers; object IDs survive the copy ([`split_appendix_deck.py`](/Users/aelaguiz/workspace/psbrain/projects/andrew-2026-09-25/split_appendix_deck.py)).
- **Check which source the builder reads.** The Milkshake attack builder once embedded a copy of `roadmap_slide.py`, so editing that file changed nothing. A long build also uses the specs as they were when it started: rebuild what changed with `--only=` after it finishes.

### Making text fit

- **Text boxes have 7.2 points of padding a side** (less at the top of a box under 14 points tall), so a short label in a narrow box wraps ("2.4" became "2." and "4"). Draw a label's box 7.2 points wider than its shape on each side, put a number and its name in one box as two runs, and join words that must stay together with no-break spaces (U+00A0): intervals and parenthetical counts in `growth_deck.py` tables, divider slide lists, pills.
- **Headlines fit one line:** Blinker 600 at 22 pt holds about 65 characters, fewer with wide letters. A bold heading that nearly fills its box can measure as two lines and render as one, so keep one-line bold headings well short of the width and read the render for gaps as well as overlaps. The kicker is a section tag only; the headline must read on its own.
- **Native tables:** columns at least 32 points wide (a narrower one fails the whole batch, "at least 406400 EMU"); cell padding makes a two-line 7.5-point cell about 33 points tall and a one-line 9 to 10 pt row about 0.3 in, whatever height you ask for. Budget about 16 points a line plus 10 a row, or split the slide. For 12 rows or more, draw a grid of text boxes (`table()` in [`build_data_section.py`](/Users/aelaguiz/workspace/psbrain/projects/andrew-2026-09-25/build_data_section.py) fits a 12-row, 13-column P&L at 17 points a row).
- **Size text columns from their text,** never by hand: `side(..., step='auto', max_h=…)` in the trials builder's `helpers_tp.py` measures each item and shrinks to 7 points until the column fits. Captions under images need about 25 points for two lines at 7 points and stay within their image's width. `text_fit` lays every run of a mixed box at its largest size, so a bold 10 pt lead over a 9 pt body measures conservatively; size such boxes the same way. `fit()` shortens text with "…" silently: search the request dump for a trailing "…".
- **Bold Inter renders regular when the style also sends `bold: false`:** send `bold` as `weight >= 700` (`tstyle()` in `projects/ai-search-growth/data/chatgpt-ads-early-read/deck/build.py`) and check `pdffonts` for `Inter-Bold`.
- **Hanging indent for typed bullets:** `updateParagraphStyle` with `indentStart` about 9 points and `indentFirstLine` 0. Leave text-box autofit off (NONE).
- **Never send an empty string to a text box:** `updateTextStyle` then fails the whole batch ("has no text"); skip the element or use "·".

### Builder code

- **Element and object IDs.** Object IDs need at least 5 characters (prefix slide IDs, such as `gx_`). Body elements must not reuse the frame's names (`<slide>_kick`, `_h2`, `_hr`, `_fhr`, `_fl`, `_fr`), and a helper's generated names can collide with yours (`ex` plus `a1`): a duplicate fails the batch partway, before the notes pass, so assert unique IDs on `--dry`.
- **Specs and helpers share one namespace** (`exec`), so a spec variable named `L`, `items` or `_re`, or a second helper file's `grid()`, silently replaces a helper and crashes a later slide. Name spec variables apart from the helpers, and load a second helper file into its own namespace.
- **Keep files that aren't a lane out of a loader's folder** (a `valuations.json` in `flows/` broke the spec).
- **zsh passes an unquoted variable as one word** (`$JOBS_LIST`): use `${=JOBS_LIST}` or `$(cat file)`.

### The API and Drive

- **Slides allows 60 write requests a minute per user.** A full rebuild spends two writes a slide, so a deck over about 30 slides fails partway with "Quota exceeded", and a delete that succeeded before a failed create leaves the slide missing. Pace the runner (2.2 seconds a slide) or rebuild only changed slides; `batch()` retries 429s with backoff.
- **Retry the transient failures, and read the log, not the exit code.** `gws` can fail mid-build with a timeout, a 5xx, "There was a problem retrieving the image" on a Drive image that is fine, or `401 ... Connection failure ... dns error` (a network drop that reads as an auth failure); put all of them in the builder's retry list (the batch is atomic, so a retry is safe). A build piped into `tail` exits 0 anyway: check the log's last line (`order ok N`); after a crash rebuild from the failed slide to the end with `--only=` (it reorders at the end), then `--notes`, then read the order and notes back. An empty `--only=` crashes with `KeyError: ''`.
- **`gws` fails with "no native root CA certificates found"** when it can't read the Mac's trust store: `export SSL_CERT_FILE=/etc/ssl/cert.pem`.
- **`gws drive files create --upload` and `gws drive files export --output` work only inside the current directory;** run a builder and its render from its own folder (an export started elsewhere failed after deleting the old PDF). Delete the old PDF before exporting and check the page count with `pdfinfo`, since an existing file is left in place without an error.
- **Exports and thumbnails have limits.** `pages.getThumbnail` stalls after a few dozen calls; use the PDF export. Drive refuses to export a big deck (`exportSizeLimitExceeded`, at 63 to 89 slides with many screenshots): render changed slides with [`thumbs.py`](/Users/aelaguiz/workspace/psbrain/scripts/cobalt_slides/thumbs.py), or export in slices with [`split_export.py`](/Users/aelaguiz/workspace/psbrain/scripts/cobalt_slides/split_export.py) from the start for a screenshot-heavy deck. For email, compress with Ghostscript (`-dPDFSETTINGS=/ebook`, images at 110 dpi; 55 MB to 8.6 MB, under Gmail's 25 MB cap), and drop internal pages with `qpdf --pages`.

### Images

- **The API inserts only publicly fetchable images.** A local file goes to Drive, gets anyone-with-the-link access while its slide builds, and has it revoked right after; skip the revoke on a file that already had an `anyone` permission, or the build deletes Amir's own sharing (`share()` in `build_attack.py`). `gws drive permissions delete` drops an empty `download.html` in the working folder; run it from the output folder and delete strays.
- **Save the image map after every upload** (a Drive 502 midway through 99 uploads lost 45 file IDs once): `upload_images.py` saves after each file, retries and reuses a same-named file. `gws drive files update --upload` replaces an image's content and keeps its ID.
- **Flatten transparent PNGs onto the page color before JPEG conversion,** or stray strips appear around a phone mockup.
- **Check that a screenshot shows the words you quote, at slide size;** crop the panel that carries the quote and record the crop in the lane's manifest.
- **Landscape captures need wide cells** (`grid_imgs`) or stacking, never phone slots. App Store screenshots from the iTunes lookup API come back as thumbnails: replace the size segment (`392x696bb.jpg`) with `1290x0w.png`.
- **To mark results on a real image, draw native shapes over it** (rectangles from the label coordinates, styled by outcome, plus a legend), so nothing edits the image's pixels (slide 11 of the [solver deck](/Users/aelaguiz/workspace/psbrain/projects/subgame-solver/overview/README.md)).
- **Live store pages as a foreign user sees them:** `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --user-data-dir=<fresh dir> --window-size=1280,1500 --virtual-time-budget=8000 --screenshot=<png> "https://play.google.com/store/apps/details?id=<pkg>&hl=ja&gl=JP"` (or `apps.apple.com/<cc>/app/id<id>`) renders without touching BrowserOS neo, but never exits: run it in the background, wait for the file, then kill it.
- **Mocks made with GPT Image** follow the [AI mock style guide](/Users/aelaguiz/workspace/psbrain/knowledge/ai-mock-style-guide.md).

### Diagrams

- **Lines run from the top-left to the bottom-right of their box:** a rising segment sets `scaleY` to −1 with `translateY` at its start (`seg()` in `build_data_section.py`), a leftward one `scaleX` −1, and arrows pointing up or left switch to `startArrow`.
- **Flow diagrams from a flows file:** `flowgraph()` in `.local-sources/lifecycle-2026-09-26/deck/helpers_lc.py` lays out steps as boxes and arrows and shrinks the text until every word fits; keep a diagram to about ten boxes, drop a looping step and put the outcome in the branch text, keep a branch's end note short (or `stub=False`), label only one of two paths leaving a box from the bottom, and right-align timeline labels near the edge.

## PS Brain files on a slide

A link helps only if its reader can open it, and PS Brain is Amir's private memory: he does not want the team reading it (October 11: "in my organization only I have access to this repo. I don't want my team members seeing the contents of this repo."). So a deck the team reads carries what they need on the slide or in its notes, and a PS Brain path is a pointer for agents and Amir; who can open its GitHub copy has changed more than once, so check [PS Brain on GitHub](/Users/aelaguiz/workspace/psbrain/knowledge/psbrain-github.md) before writing a link to one of its files.

## Checks

- `text_fit.py` on the request dump: 0 issues.
- Every changed slide rendered and looked at: no wrapped headline, nothing running into a callout or the footer, images legible, diagrams readable.
- The live order, count, footers and notes read back and equal to the `--dry` run.
- Sources in the speaker notes for every fact you added.

## Record of the first run

[Economy deck record](/Users/aelaguiz/workspace/psbrain/projects/product-economy/economy-deck.md): a 36-slide team deck rebuilt as 51 Cobalt slides on September 22, 2026, with a backup and every slide rendered and checked.
