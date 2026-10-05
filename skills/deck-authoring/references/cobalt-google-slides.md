# Building in Google Slides on the Cobalt template

The mechanics of turning a finished outline into a Poker Skill deck: the
template, the house build tools, images, rendering, and the traps that break
builds. Taste and structure live in `SKILL.md`; this file is how to make the
slides exist and look right.

## Contents

- The template and the look
- Making a new deck
- Building slides from code
- Images and mocks
- Rendering and looking
- Revising a live deck
- Traps

## The template and the look

- **Template:** "[TEMPLATE] Poker Skill deck — Cobalt report style",
  presentation ID `1TA2jkZ0U_usoLO4oEG0KO1lE2i71JQ3g9_k9nZ4rjbM`, in the Drive
  folder "Poker Skill slide template" (`1RNtynw4TRYduOMwr9sB7QP4ffio-tk4R`),
  which also holds the dark-background Poker Skill logo.
- **Its 12 slides** (object IDs `tpl_s01` to `tpl_s12`): cover, how to use the
  deck, contents, section divider, answer with supporting text, stat tiles and
  a hero number, paired chart cards, full-width chart, table, callouts and
  status, palette, sources and closing. Slides 2 and 11 are guides; never ship
  them. The template supplies the look, not the story: "the template's a look
  and feel not a narrative flow."
- **No theme to import.** Every Cobalt deck, the template included, is Simple
  Light with explicitly styled elements on BLANK slides. You copy the deck or
  draw slides in its style.
- **Page:** 16:9, 720 by 405 points. Page `#181C25`, cards `#202632`,
  hairlines `#282F3E`, borders `#384156`, emphasis white `#FCFBF8`, body text
  `#CDD4E0`, muted `#7785A6`, cyan signposts `#11B5E4`.
- **Type:** Blinker for the kicker (11 pt capitals, cyan), the headline (22 pt,
  one line, about 65 characters at most), divider titles, and display numbers;
  Inter for body text (about 10 to 14 pt) and the footer (9 pt).
- **Frame of a content slide:** kicker, headline, a hairline under the
  headline, the content, then a footer with a hairline: "Poker Skill · <deck
  name>" on the left, the section and page number on the right.
- **Charts:** the palette in fixed order starting at `#0D89AB` (then
  `#9A8409`, `#CF4672`, `#1E852C`, `#AF46A3`, `#C05A0C`, `#4562D9`, `#E25C50`).
  One question and one y-axis per chart. Status colors only with a status
  label beside them.
- **Copy rules:** "Poker Skill" is two words. No em dashes in slide text.

## Making a new deck

1. Copy the template into the target folder (Amir's My Drive root is
   `0AGv6IyaNcm0eUk9PVA`) with `gws drive files copy`, named
   "<Title> · <YYYY-MM-DD>".
2. Share it at once, editable by everyone at fun.country:

   ```sh
   gws drive permissions create --params '{"fileId":"<id>","supportsAllDrives":true,"fields":"id"}' \
     --json '{"type":"domain","role":"writer","domain":"fun.country"}'
   ```

   Do the same for any Drive folder you create for the deck's images.
3. Record the deck ID in a small file beside the builder so every later run
   edits the same deck.
4. Delete the template's own slides on the first build only.

## Building slides from code

- **Primitives:** `/Users/aelaguiz/workspace/psbrain/scripts/cobalt_slides/cobalt.py`
  draws Cobalt slides on BLANK pages: `Slide.frame` (kicker, headline,
  footer), `Slide.divider` (number, title, one sentence, the part's slides),
  `text`, `table`, `image`, `box` and `line` for native diagrams, `callout`,
  `pill`, `numbered`, and `batch` for the API call with retries. Its footer
  label is hard-coded; set your own.
- **A complete builder to copy from:**
  `/Users/aelaguiz/workspace/psagentspace/research/2026-10-02-energy-lesson-start/deck/build.py`
  creates the deck from the template, keeps the deck ID in `deck.json`,
  shares images only while they are placed, writes speaker notes, audits text
  fit on `--dry`, rebuilds single slides with `--only=`, and renders with
  `--render`. Its `upload_images.py` resizes and uploads screenshots and saves
  the file map after every upload. Copy the mechanics; write your own slides.
- **Words-file decks:**
  `/Users/aelaguiz/workspace/psagentspace/scripts/growth_deck/growth_deck.py`
  builds a deck from a Markdown words file (cover, numbered calls, tables,
  two-column slides with charts and big numbers) and renders it. It draws no
  pictures and no dividers, so it suits text-and-number decks such as the
  daily growth deck; read its README before using it.
- **Write a spec, dry-run, audit, then build.** Keep one spec entry per slide
  and one ordered list of slides grouped into sections, so the dividers, the
  cover's contents, the footers, and every cross-reference come from the same
  list. Run
  `python3 /Users/aelaguiz/workspace/psbrain/scripts/cobalt_slides/text_fit.py <requests.json>`
  on the dry run's request dump and build only at zero issues. It measures
  text with the real fonts and flags wrapped headlines and labels, text
  running past its box or into the footer, overlaps, and text off the edges.
- **Speaker notes:** write them after the slides are built; rebuilding a slide
  wipes its notes, so the builder should rewrite them every run.

## Images and mocks

- **The Slides API inserts only images it can fetch publicly.** Upload the
  image to a Drive folder, give the file an anyone-reader permission while its
  slide builds, insert it from
  `https://drive.google.com/uc?export=download&id=<fileId>`, then delete that
  permission. Skip both steps for a file that is already open to anyone, or
  you will undo someone's real sharing. Alternatively, host a folder of images
  with `$cf-share` and insert each by its URL.
- **Prepare images first:** resize large captures, flatten transparent PNGs
  onto the page color before converting to JPEG, and open every image at slide
  size to check that it shows what the caption claims.
- **Mocks:** make them with `$gpt-image` as edits of the newest real capture,
  changing only the thing proposed. For Poker Skill screens, follow
  `/Users/aelaguiz/workspace/psbrain/knowledge/ai-mock-style-guide.md`. GPT
  Image copies text from its reference images and drifts in characters and
  palette: spell out every heading and label in the brief, read every mock's
  on-screen copy, and keep rejected drafts. Label each mock on the slide.
- **Marking a real screenshot:** draw native outlines and arrows over the
  placed image; never edit its pixels by hand.

## Rendering and looking

```sh
rm -f render/deck.pdf
gws drive files export --params '{"fileId":"<id>","mimeType":"application/pdf"}' --output render/deck.pdf
pdfinfo render/deck.pdf | grep Pages
pdftoppm -r 110 -png render/deck.pdf render/p
```

- Read every new or changed page at full size, then make a contact sheet of
  the whole deck (`$contact-sheet-builder`, or six pages to a sheet) to judge
  the sequence.
- The export refuses very large or image-heavy decks
  (`exportSizeLimitExceeded`). Then use
  `/Users/aelaguiz/workspace/psbrain/scripts/cobalt_slides/split_export.py`,
  which exports the deck in slices, or `thumbs.py` beside it for a few slides.
  Per-slide `getThumbnail` calls are quota-limited and stall after a few dozen.
- The rendered PNGs are also what the cold reader gets.

## Revising a live deck

- Read the live deck's order and every element's text before building. Amir
  adds, edits, and reorders slides by hand: keep any slide your builder did not
  make, copy his order into your slide list, and never let a build delete or
  overwrite his work.
- Rebuild only the slides that changed. Inserting or removing a slide shifts
  every later page number: rewrite the other footers in place with one
  page-scoped `replaceAllText` each instead of rebuilding the deck. A small
  edit that turns into a full rebuild costs him time ("wtf 18 minutes to put
  in fucking dividers").
- Make a backup copy with `gws drive files copy` before replacing a deck's
  slides wholesale.

## Traps

- **Write quota:** 60 Slides write requests a minute per user. Pace builds and
  retry 429s with backoff.
- **Object IDs:** at least 5 characters, unique within the deck, and never the
  names the frame helpers already use (`_kick`, `_h2`, `_hr`, `_fhr`, `_fl`,
  `_fr`). Give your slides a prefix and assert uniqueness on the dry run.
- **Bold Inter renders regular** when the style sends weight 700 with
  `bold: false`. Send `bold` as `weight >= 700`.
- **Text boxes pad 7.2 points a side.** Short labels in narrow boxes wrap;
  draw label boxes wider than their shapes and join words that must stay
  together with no-break spaces.
- **Native tables:** columns at least 32 points wide, and rows grow with
  padding (a two-line 7.5-point cell is about 33 points tall). Budget about 16
  points per text line plus 10 per row, or split the table. For a dense data
  table, draw a grid of text boxes instead.
- **Empty text:** an empty text box can't be styled and fails the batch; use a
  placeholder such as "·".
- **Image fetches fail now and then** ("There was a problem retrieving the
  image") for a file that is fine. Retry that slide; the batch is atomic.
- **A network drop reads as an auth failure,** and `gws` can fail with "no
  native root CA certificates found" on macOS; `export
  SSL_CERT_FILE=/etc/ssl/cert.pem` fixes the second. After any crash, rebuild
  the remaining slides and rewrite the notes.
- **A background build that pipes into `tail` exits 0 even when it failed.**
  Check the log's last line, not the exit code.
- **Delete the old PDF before exporting;** an existing file is left in place
  without an error, and you will review the old deck.
- **App Store lookup screenshots come back as thumbnails.** Replace the
  trailing size segment (such as `392x696bb.jpg`) with `1290x0w.png` for the
  full-size image.

The full runbook, with the evidence behind each trap and many more edge cases,
is `/Users/aelaguiz/workspace/psbrain/knowledge/cobalt-slides-decks.md`. Read
the relevant part when a build fails in a way not listed here.
