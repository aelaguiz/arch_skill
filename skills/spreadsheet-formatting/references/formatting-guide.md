# Spreadsheets for humans: the formatting and consistency guide

This guide is for an agent that builds or repairs a spreadsheet that a human
will read, scan, change and trust. Google Sheets first, Excel second. It covers
formatting, layout, text, numbers, colour, and the input-versus-formula
discipline. It does not simplify the data; it makes the data readable.

Every rule below has a reason and a source class. When a rule says "never",
the reason is that the cost lands on the reader every time they open the file.
Rules marked **contested** name the disagreement and the choice made here.
Source keys: `FAST` (FAST Standard 02c/02d), `ICAEW` (Twenty Principles 2024,
Financial Modelling Code 2024), `SMART` (Corality/Mazars), `WSP/TTS/BIWS`
(banking training conventions), `Panko` (EuSpRIG error research),
`Few` (Show Me the Numbers; Information Dashboard Design), `Schwabish`
(Ten Guidelines for Better Tables, JBCA 2020), `Butterick` (Practical
Typography), `UKGAF` (UK Government Analysis Function spreadsheet standard),
`Broman&Woo` (Data Organization in Spreadsheets), `WCAG` (2.2 AA),
`NN/g` (Nielsen Norman Group), `Google`/`MS` (vendor docs, Sheets API v4 facts
verified live in 2026-09).

## Table of contents

0. How to think about a sheet (read this first)
1. The ten laws
2. Screen budget: freeze panes and the title block
3. Workbook architecture: tabs, order, names, Read Me
4. Who owns each number: observations, assumptions, formulas
5. Text in cells
6. Tables: alignment, headers, rules, totals, widths
7. Numbers, dates and missing values
8. Colour, type and status
9. Formulas a reader can audit
10. Consistency across tabs
11. Verification: how to prove the sheet is right
12. Evidence and resolved disagreements
13. Field lessons: what went wrong the first time agents used this

## 0. How to think about a sheet

Rules below are consequences of a few facts about how a person reads a
grid. When a situation is not covered by a rule, reason from these.

- **A cell is a window, not a container.** The reader sees only what fits
  in the column at the current width. Text that does not fit is either cut
  off (clip) or spilled across the row (overflow); both break the reader's
  model that one cell holds one thing. So either the content fits the
  window, or it is not cell content: it belongs in a wider column, a Notes
  column, a cell note, or the Read Me. Widths, lengths and wrap are one
  decision, made together, and confirmed by looking at the rendered sheet.
- **A row is a record, a column is a type.** The eye scans down a column
  expecting the same kind of thing at the same alignment and precision, and
  across a row expecting the same entity. Anything that violates that
  (numbers in a text column, prose in a data row, a label spilling into the
  first value column, a section explanation sitting where values sit) costs
  the reader a re-read. When a table is transposed (attributes down,
  entities across), the type lives in the row; align and format by row.
- **Structure is shown by position and space before ink.** Headers, groups
  and sections are understood from where they sit and the room around them;
  rules, fills and bold are second-order cues. Add ink only when space and
  position have failed. This is why full grids, vertical rules, dark
  header fills and bold data cells make a sheet feel loud and cramped.
- **Colour is a signal with a budget.** Every coloured cell asks for
  attention. If a state is painted on a whole column or repeated on every
  row, the reader stops hearing it and the real exception disappears. Show
  a state once, where the eye lands, with a word; let everything else stay
  quiet. Colour that encodes role (input, link) is a legend, not an alarm,
  and must be light enough to read through.
- **Repetition is noise when it restates one fact.** A value, a label, a
  caveat or a source belongs where it is owned, once. Eighteen cells
  reading "No current restoration" for one campaign say what one status
  cell says, and hide the eighteen values that would otherwise be there.
  The same status word across many records in a tracker is data: one fact
  per record.
- **Whitespace is reading room.** Default row heights and padding are tuned
  for typing into a grid, not reading one. A tab a person is meant to read
  gets taller rows, wider gutters and a blank row between blocks; density
  is not rigour, it is fatigue.
- **Every number has an owner.** An observation comes from outside and may
  be a literal shown as data; an assumption is a choice someone is entitled
  to make and is a literal in the input style; everything derived is a
  formula, so the sheet stays true when the inputs move. A constant hidden
  inside a formula is an assumption the reader cannot see, test or change.
- **Summaries, templates and checks inherit the conditions of the
  principle they illustrate.** A law, a house-style row, a recipe or a
  readback item is a compressed reminder of a principle, not a new
  unconditional command; when a summary and its principle disagree, the
  principle wins and the summary is wrong.
- **The API is not the reader.** A successful batchUpdate proves nothing
  about what a person sees. Formatting is finished only after looking at
  the rendered tab at laptop width and reading it as a stranger would.

## 1. The ten laws

These are the rules a reader complains about first. Break one of these and
nothing else in the guide will rescue the sheet.

1. **Freeze only what identifies columns, and build that area from row 1.**
   Frozen rows are a contiguous prefix: Sheets cannot freeze row 3 without
   rows 1 and 2. So on a scrolling table the identification area starts at
   row 1 and every row in it earns its place: a spanner row (when columns
   come in groups) and the column-header row, with the tab identity in the
   corner cell of that area rather than in a separate title row above it.
   Never a title block, never a notes row, never five rows. On a 13-inch
   laptop about 33 default rows are visible; each frozen default row costs
   about 3 percent of every screen the reader will ever see, and each frozen
   40 px header row costs about 6 percent (`NN/g`, `FAST` 2.03, laptop
   arithmetic verified against Sheets' 21 px default row). Freeze an axis, not a
   document category: stacked sections that share one column axis share one
   frozen prefix; unrelated tables on one tab get local header rows and no
   frozen rows; a tab that fits one screen freezes nothing.
2. **Every number has an owner, and the owner decides how it is shown.**
   An *observation* is a fact from outside the workbook: synced data, a
   pulled total, a reported rate with its evidence. It may be a literal, it
   is shown as data (plain ink), and its source is named once in the header
   or key. An *assumption* is a value the reader is invited to change: a
   growth rate, a mix, a threshold. It is a literal with the input style.
   Everything *derived* is a formula. A constant typed inside a formula
   (`=B5*70%/20%`, `=C8*2`) is a hidden assumption the reader cannot see,
   test or change; extract it. Replace a literal with a formula only when the
   workbook holds the authoritative ingredients and the same definition:
   linking a reported total to a source table proves nothing about its
   derivation, and re-deriving a reported rate from rounded evidence changes
   it. Structural numerals (12 months, 1000 for scaling, 0 and 1, a ROUND
   precision, a `#gid` in a link) are syntax, not decisions
   (`FAST` 3.03, `ICAEW` P10, `Macabacus` partial-input rule).
3. **Assumptions look like assumptions, everywhere.** Every lever has a fill
   or border and a distinct font colour, appears exactly once, carries a
   unit, and sits in an inputs block or inputs tab the reader can find
   without scrolling through calculations. Observations do not get that
   treatment; painting three thousand synced facts as levers tells the reader
   to edit them. Font colour alone is not enough (`ICAEW` FMC: fill and/or
   border; `WSP`: blue inputs, black formulas, green cross-sheet links).
4. **One line per cell.** A cell holds a label, a value, or one short phrase
   (about 45-90 characters, 50-70 ideal). Anything longer is split into
   label + value, one point per row, a Notes column, a cell note, or the
   Read Me tab. No paragraphs, no bullet lists with line breaks inside a
   cell (`Butterick` line length, `MS` style, `Broman&Woo`, `FAST` 3.05).
2. **Every number has an owner, and the owner decides how it is shown.**
   An *observation* is a fact from outside the workbook: synced data, a
   pulled total, a reported rate with its evidence. It may be a literal, it
   is shown as data (plain ink), and its source is named once in the header
   or key. An *assumption* is a value the reader is invited to change: a
   growth rate, a mix, a threshold. It is a literal with the input style.
   Everything *derived* is a formula. A constant typed inside a formula
   (`=B5*70%/20%`, `=C8*2`) is a hidden assumption the reader cannot see,
   test or change; extract it. Replace a literal with a formula only when the
   workbook holds the authoritative ingredients and the same definition:
   linking a reported total to a source table proves nothing about its
   derivation, and re-deriving a reported rate from rounded evidence changes
   it. Structural numerals (12 months, 1000 for scaling, 0 and 1, a ROUND
   precision, a `#gid` in a link) are syntax, not decisions
   (`FAST` 3.03, `ICAEW` P10, `Macabacus` partial-input rule).
3. **Assumptions look like assumptions, everywhere.** Every lever has a fill
   or border and a distinct font colour, appears exactly once, carries a
   unit, and sits in an inputs block or inputs tab the reader can find
   without scrolling through calculations. Observations do not get that
   treatment; painting three thousand synced facts as levers tells the reader
   to edit them. Font colour alone is not enough (`ICAEW` FMC: fill and/or
   border; `WSP`: blue inputs, black formulas, green cross-sheet links).
6. **Numbers right, text left, headers match the column.** Never centre a
   numeric column. Same decimals for every value of a type in a column.
   Units and scale in the header, not in the cells (`Schwabish` G2-G4,
   `Few`, `Butterick`).
7. **One header row, styled by weight and a rule, not a dark fill.** The
   header is bold, sentence case, one to two words plus unit, with a thin
   light rule under it. Totals are bold with a rule above (`Schwabish`,
   `Few`, `UKGAF`). One dark brand band is allowed for the tab title only.
8. **Colour means something or is absent.** Structure is grey, text is
   near-black on white, one accent draws the eye, red is for alerts. Every
   text/fill pair meets 4.5:1. Colour never carries meaning alone: pair it
   with a word, sign or glyph (`WCAG` 1.4.1 and 1.4.3, `Few`, `Stone`).
9. **Same thing, same look, everywhere.** Same column purposes in the same
   letters on every tab, same header row number, same fonts, same number
   formats, same colour key. Consistency is the thing the reader notices
   first and complains about most (`ICAEW` P5-P6, `FAST`, `Schwabish` G10).
10. **Short formulas, one per row, readable without the formula bar.** Short
    formulas are found wrong 84 percent of the time in inspection versus 53
    percent for long ones (`Panko` 1999). Bring cross-sheet ingredients into
    a local labelled row first; never do arithmetic on a cross-sheet
    reference inside another formula (`FAST` 3.02, `Panko`).

## 2. Screen budget: freeze panes and the title block

**The reader's screen is the scarce resource.** Design for a 13-inch laptop at
100 percent zoom: about 700 px of grid, about 33 default rows, roughly 10-12
columns of 100 px. Everything frozen is subtracted from every screenful.

- Freeze the single header row that names the columns; freeze a second row
  only when it is a real group header directly above the column header.
  Freeze the first column only when it is the human-readable row identifier
  and the table is wider than the screen (`FAST` 2.03-01, `Schwabish`,
  `Adobe` table study: frozen headers speed tasks; `NN/g`: keep sticky chrome
  small and ask whether it is needed at all).
- Do not freeze title rows, subtitle rows, refresh-date rows, link rows,
  spacer rows or notes rows. Because frozen rows are a contiguous prefix,
  a table that needs its header kept must put the header (and its spanner
  row, if any) at the very top. The tab identity then lives in the corner
  cell (A1 of the spanner row, or of the header row when there is no
  spanner), styled as the title; the banner's other contents (refresh date,
  source, links) go to the Read Me, a note on the corner cell, or a muted
  cell at the right end of the header area. A separate title row is for
  tabs that do not scroll.
- Summary or dashboard tabs that fit on one screen freeze nothing
  (`Few` IDD: single screen, no scrolling). Stacked tables that share one
  column axis (the same periods, versions or scenarios in the same letters)
  share one frozen identification prefix; stacked tables with unrelated
  columns get a local header row each and nothing frozen, because no single
  header row identifies every column below it.
- A model with checks may keep exactly one master check cell in the frozen
  area; nothing else earns a frozen row (`FAST` 2.03-05).
- Title block on a non-scrolling tab: one row. Left: sheet title (what,
  where, when, unit if uniform). Right, muted: data-as-of date and source,
  driven by a cell, not typed into the title. Never a second title row for a
  subtitle; put the subtitle in the Read Me or as a short muted line under
  the title only when the tab is a one-screen dashboard (`Few`,
  `Schwabish` G7, `L1`).
- Put text in A1 on every tab. Screen readers start there; sort, filter,
  QUERY header detection and "select all" assume a rectangle that starts at
  A1 (`MS`, `Google`, `Broman&Woo`).
- Frozen rows double as the repeated print header in Sheets; that is a
  reason to freeze the header row, not a reason to freeze the banner.
- Row height is a reading decision, not a default: taller than the typing
  default so the tab breathes (section 6), but uniform, and never so tall
  that data drops below the fold or the eye reads downward instead of
  across (`Raffensperger`). Frozen rows count double: every pixel there is
  paid on every screen.

## 3. Workbook architecture: tabs, order, names, Read Me

- Order tabs in reading order: Read Me (or Summary first, then Read Me
  second), Inputs, Summary/Output, calculation "chapters", raw data, checks.
  The workbook should read like a book: top-to-bottom, left-to-right, tab by
  tab (`FAST` 1.01, `ICAEW` P9, `SMART`, `Few` A13).
- One purpose per tab. A tab is a summary, an inputs sheet, a calculation
  chapter, or a raw data landing zone; not two of these. Raw data tabs keep
  gridlines on, one header row, no formatting beyond the header
  (`Broman&Woo`, `UKGAF`).
- Name tabs briefly and descriptively (`Inputs`, `Model 90d`, `Keywords raw`),
  never `Sheet1`. Avoid characters that complicate references. Use tab colour
  by role (inputs one colour, outputs another, raw data grey) and keep the
  mapping in the Read Me key (`FAST` 1.02, `ICAEW` P9).
- Never hide tabs or rows to tidy up; group rows instead. Remove relics
  (unused inputs, dangling calculations, empty tabs, formatting beyond the
  used range) only once their absence is understood: who reads that
  address, whether a sync script writes there, whether a blank is a future
  data destination. "Looks unused" is not evidence (`FAST` 1.03, `ICAEW`
  P16, `Raffensperger`).
- Read Me tab, always, inside the workbook: purpose in one sentence, owner,
  version and date, what changed, tab map with hyperlinks, the format key
  (every font colour, fill, border and tab colour with its meaning), units
  and sign convention, source of each input with pull date, known
  limitations. One short sentence per row, label in column A, text in column
  B overflowing to the right (`ICAEW` P4 and P18, `FAST` 1.04, `CFI`,
  `Few` E7).
- Version and data-as-of live in the Read Me and in a cell; the file title
  carries the version only when copies are distributed (`ICAEW` P18).

## 4. Who owns each number: observations, assumptions, formulas

**Classify by ownership before touching a number.** Three owners exist:

- An *observation* is a fact from outside the workbook: a synced metric, a
  pulled count, a reported rate, a published estimate with its sample size.
  The workbook does not own its derivation, so it may be a literal. Show it
  as data: plain ink, its source named once in the header, key or Read Me,
  and (when a script writes it) the range protected and marked as synced.
- An *assumption* (a lever) is a value the reader is invited to change: a
  growth rate, a mix, a capture rate, a threshold, a price. It is a literal
  with the input style, once, with a unit and validation.
- A *derived* value is computed from observations, assumptions and other
  derived values. It is always a formula. Outputs are derived values with
  presentation formatting.

Ownership is not dependency. "Would the sheet recalculate if this changed?"
is true of an observed CPI as much as of a growth assumption; it tells you
what depends on the cell, not who is entitled to choose its value. Ask
instead: who is authorised to set this value for this use? A person making
a modelling choice owns an assumption; a system, a measurement or a
published source owns an observation; a formula owns a derived value. An
editable choice may be a number, a date or a category (a scenario name, a
policy); an authored status (`Shipped`, `Folded into N106`) in a tracker is
an observation about work unless an existing rule computes it.

Recognition tests: is someone invited to change this as a choice? Then it
is an assumption. Could the
workbook recompute it from ingredients it actually holds, with the same
definition? Then it is derived and must be a formula. Does it come from
somewhere the workbook cannot see? Then it is an observation; leave it a
literal and say where it came from. Test the label, not the word: a
"total" is derived only if its components are here; a reported total whose
components live in a warehouse is an observation.

- **Trackers and other authored records.** A tracker row is one
  independently sortable work item: identity, state, target, next required
  action, each in its own cell, with longer requirements in keyed details
  (a note on the identity cell, a details tab keyed by the ID). The same
  status word repeated down a column is data here, one fact per record;
  the repetition to avoid is decoration duplicated inside one record.
- **Do not manufacture inputs.** Moving thousands of observations into an
  "inputs" table and linking every presentation cell to them satisfies a
  rule and helps no one: it doubles the workbook, hides nothing that was
  hidden, and invites edits to facts. Style observations as data where they
  are. The one reason to relocate observations is a genuine raw-data tab
  that other tabs derive from.
- **Do not re-derive a reported value.** `0.9% (6/677)` is a reported rate
  and its evidence; `6/677` is 0.89 percent and rounds differently. Keep the
  reported measure as the observation and keep the evidence traceable
  beside it or in a note; do not replace the measure with a formula over
  rounded evidence.
- **A hidden decision is defined by meaning, not by its numeral.** Extract a
  constant from a formula when it is an assumption the reader may need to
  inspect or vary. Leave structural arguments in place: unit conversions
  (12, 7, 24, 1000), 0 and 1, a ROUND precision, an offset in a lookup, a
  `#gid` in a link, a format string. A lexical search finds candidates; the
  formula's purpose decides (`FAST` 3.03-01, `ICAEW` P10, `WSP`, `Few` D10,
  K3).
- **Assumptions leave the formula.** `=B8*2` becomes `=B8*$B$4` with `B4`
  labelled `Growth multiplier per month` and formatted as an input.
  `=$B$5*70%/20%` becomes `=$B$5*C$12/$B$8` with the mix and capture rate as
  labelled inputs (`FAST` 3.03, `Macabacus` ignore-list 0/1/100/1000).
- **One choice per cell.** `"70% / 20% / 10%"` in one cell is a label
  pretending to be three inputs. Store each lever in its own cell with its
  own format and its real domain (a number, a date or a category); if the reader wants to see the trio, a formula
  can compose the display string next to them.
- **Each input appears once** and is referenced everywhere else; never
  re-type a date, a name, a rate or a subtotal (`FAST` 3.03-03, `ICAEW` P10,
  `SMART`).
- **Inputs block placement.** Small single-purpose sheets: an inputs block at
  the top of the tab, immediately under the title, before any calculation.
  Anything reused, shared, or with more than about 20 inputs: a dedicated
  Inputs tab immediately after the Read Me (`FAST` 1.01, `ICAEW` FMC,
  `WSP` small-model exception; `Kruck` experiment: well-segmented sheets
  averaged 4 errors versus 24). **Contested** (Raffensperger/Bewig prefer
  inputs adjacent to their formulas); the segmented layout wins on the
  evidence and on the reader's ability to find the levers.
- **Input cell style** (assumptions only). Distinct font colour **and** a
  light fill or border, applied identically to every lever in the workbook,
  with the key on the Read Me. Observations stay plain; the reader must be
  able to tell "you may change this" from "this was measured" at a glance. Banking convention: blue font hard-codes, black formulas, green
  links from other tabs, red links to other files. Fill is what makes the
  scheme survive greyscale and colour-blindness (`ICAEW` FMC, `WSP`, `TTS`,
  `BIWS`, `Few` D11). **Contested**: FAST uses blue for imports and red for
  exports, the opposite meaning; pick one scheme, document it, never mix.
- **Each input has a label, a unit and a source.** Label in the column to the
  left, unit in the label or a units column (`USD`, `%`, `per month`,
  `clicks`), source or note in a Notes column to the right, one line
  (`FAST` 3.05, `ICAEW` P10, `CFI`).
- **Levers get validation.** Data validation with a bounded range or a list
  and a short help message; a lever that accepts any value is a trap
  (`ICAEW` P11, `FAST` 1.05, `Google` setDataValidation).
- **Flex cells for sensitivities.** A base-case input times a sensitivity
  multiplier (default 1.0) preserves the base case while the reader plays
  (`FAST` 3.04, `SMART`).
- **Checks.** Every identity the model implies gets a check row: mixes sum
  to 100 percent, quarters sum to years, shares of a total sum to the total,
  a lookup returns something. Display the check as a word (`OK` / `CHECK`),
  colour second. Roll all checks into one master check on the Read Me or in
  the single frozen check cell (`FAST` 5.01, `ICAEW` P17, `SMART`).
- **Protect formula areas** when the sheet is shared with editors; warn-only
  protection is enough for internal work (`ICAEW` P11, `Google`
  addProtectedRange).
- **Never round inside calculations**; round on display with a number format
  (`FAST` 3.06, `ICAEW` P14, `Few` B9).
- **Trap only expected errors.** `IFERROR` around a whole calculation hides
  bugs; use it only for a known blank-row case, and let unexpected errors
  show (`FAST` 3.07, `ICAEW` P17, `Hermans` Enron corpus: 24 percent of
  formula sheets contain an error value).

## 5. Text in cells

- **One line per cell.** Target 45-90 characters at the column's natural
  width; 50-70 is the comfortable reading measure. Anything longer belongs
  in a Notes column, a cell note, a row per point, or the Read Me
  (`Butterick`, `Schriver`, `MS` style: "ideally one line", `Baymard`).
- **Label + value, never a sentence with the value inside it.** `Multiple at
  month 12` | `4,096×` is right. `After 12 steps each metric is 4,096× its
  baseline` in one cell is wrong: the number is unreadable by formula, the
  sentence goes stale, and the row gets tall (`Few` B3, `FAST` 3.05).
- **Lists: one point per row.** A bullet list goes in one column, one bullet
  per row, optionally prefixed with `•` or `–`; never line breaks inside a
  cell (`Few` E3, `Broman&Woo`).
- **Fit is the test, not length.** A cell either fits its window at the
  chosen width or it is not cell content. Decide width, text and wrap
  together for each column: a label column is as wide as its longest label
  on one line; a value column is as wide as its widest formatted value plus
  a gutter; if that width is absurd, the content is too long for a cell and
  the qualifier moves to a Notes column or a cell note. Never leave the
  outcome to chance: read the rendered tab and look for cut-off strings
  (`Butterick`, `Schwabish`, `UKGAF`).
- **Overflow is for short notes beside a value, not for prose.** A note
  under about 90 characters may keep `wrapStrategy: OVERFLOW_CELL` and span
  the empty cells to its right; that is how a string "spans multiple cells"
  without a merge. Overflow is not a way to fit a sentence that is longer
  than the table is wide, and it never runs into a column that holds values
  elsewhere on the tab. Use `WRAP` where a header or a wide Notes column
  needs two lines, with strings short enough for two lines; row height follows the tallest
  cell, so one long wrapped cell makes the whole row tall
  (`Google` WrapStrategy, `Few` E5, `MS` wrap docs).
- **Labels are names, not definitions.** `Revenue to date, net store
  proceeds ($, App Store payouts after commission, tier-1)` is a definition
  wearing a label's clothes; it cannot fit any label column and it spills
  into the first value column, where it reads as data. The label is
  `Revenue to date ($)`; the definition goes to the Notes column or a cell
  note on the label. The same applies to headers.
- **Section rows carry the heading only.** An explanation of the block
  (what the metric means, where it comes from, which cohorts are mature) is
  not a section heading. It goes to the Notes column, a note on the heading
  cell, or the Read Me. A description paragraph under the title row is the
  same mistake at tab level: one title row, then the inputs or the table.
- **Shortening must preserve the reading task.** Every original string can
  survive in a note and the table can still mislead: if a caveat changes
  comparability, completeness or confidence (this cohort is provisional,
  this rate is over 6 users, this window is to-date), it stays beside the
  value or the group it qualifies, in the lightest form that works: a
  status word in a row, a `Provisional` mark on the spanner, a footnote row
  under the block, a compact evidence column. Definitions and provenance
  may be deferred, but only to a place the reader can discover from where
  they are: a `Details →` link, a note on the label, the Read Me. A Notes
  column at the far right of a 50-column table is not discoverable.
- **Notes are not a dumping ground.** A note on every cell puts a marker
  on every cell; the reader sees texture, not information. Put provenance
  once, on the header or label that owns it, and reserve per-cell notes
  for the few cells whose story differs from their row.
- **IDs and codes are text.** Campaign IDs, SKUs and hashes are identifiers:
  left-aligned, stored as text so leading zeros survive, and shortened for
  display (last 6 characters, a prefix, or the human name) with the full
  value in a cell note or the raw tab.
- **Never `CLIP`** on a presentation tab: a clipped string hides information
  with no hover to recover it. Shorten it or move it (`Schwabish`,
  `Material`/`Carbon` truncation applies to UI tables with tooltips only).
- **Where explanations live**, in order of preference: a Notes/Source column
  at the far right of the table (visible, printable, filterable); a cell note
  (right-click, Insert note) for provenance that must stay with one cell
  (source URL, query, pull date); the Read Me for anything longer than a
  sentence. Cell *comments* are for live discussion only (`FAST` 3.05-12,
  `TTS`, `Few` E4-E6, `Google` notes vs comments). **Contested**: FAST says
  never use cell notes; WSP says over-comment. Resolution: a Notes column
  for anything a reader must see; cell notes for provenance and for a
  definition on the label that owns it.
- **"So-what" lines.** If a takeaway must appear on the tab, it is one line
  of at most about 75 characters directly above or below the block it
  explains, generated by a formula from the numbers when possible, never a
  free-floating paragraph or an "Insights" box (`Knaflic`, `Few`, `Wilson`).
- **Sentence case** for labels, headers and values. No ALL CAPS except units
  and true acronyms. No end punctuation on fragments. Parallel form within a
  column (`MS`/`Google` style guides; the legibility claim against caps is
  contested, the style claim is not).
- **Headers stand alone.** `Revenue ($K)`, `Sessions, 7-day avg`,
  `Month starting`, never `Value`, `Number`, `Name`. Abbreviate only when
  space forces it and expand once in the Read Me (`FAST` 3.05, `Few` F2-F5).
- **Labels are short, unique and precise.** Spend the time to get a good
  label; do not write prose in the label column (`FAST` 3.05-01: at least 30
  seconds per label).

## 6. Tables: alignment, headers, rules, totals, widths

**Alignment**
- Numbers right, text left, dates left in a fixed-width format, headers
  aligned like the data beneath them. Never centre a numeric column. Centre
  only fixed-width codes or single characters (`Schwabish` G1, `Butterick`,
  `Few`, `Wong`; **contested**: CMOS/CSE centre headers over numbers; match
  the data on screen).
- Vertical alignment: `MIDDLE` for the header row, `TOP` for wrapped body
  cells; Sheets' default is `BOTTOM`, which looks broken on a two-line
  header (`Google` default verified live, `Butterick`).
- Do not fake hierarchy with typed spaces or indentation; use a level column
  or a section row (`UKGAF`, `Broman&Woo`).

**Header row**
- Exactly one header row per table (plus a spanner row when columns come in
  groups). Bold, sentence case, one to two words plus the unit in round
  brackets, wrap allowed to two lines, with the row tall enough to show
  both. A thin light rule under it. A light neutral fill is acceptable; a dark fill with white
  text is not the default for data headers (`Schwabish` G7, `Few`, `UKGAF`).
- **Group labels ("spanners") say "these columns belong together", and a
  label sitting in the first column of the group does not say that.**
  Centre the spanner over its columns; when a group is wider than a
  screen, a centred label sits off-screen at the first view, so place it at
  the group's left edge and name the group in the frozen corner as well.
  The reason merges are banned is
  that they break the data rectangle (sort, filter, select, screen readers);
  a spanner row above the column-header row is not data and no one sorts it,
  so a horizontal merge in that one row is the correct tool in Sheets, which
  has no "center across selection". Bold it, put a light rule under it that
  spans exactly the group, and leave a little space between groups (a
  narrow spacer column or a left rule on the first column of each group). In
  raw data tables prefix the header instead and keep one header row
  (`Schwabish` G8, `Few` J3, `FAST` 4.02-02 rationale).
- **Choose the comparison unit before widths, aliases or evidence
  placement.** Name what the reader compares: which entity, over which
  period or horizon, on which measure, for which population. Then keep that
  association intact while the reader moves: size comparable columns as a
  pair, shorten labels around the distinction being compared (two unequal
  values must not look equal because their aliases match), put evidence on
  the axis that keeps it with its measure and population with the least eye
  movement (a sub-row under the measure in a version table, a paired column
  in a two-entity comparison, a note only when it is rarely consulted), and
  add totals only when the definition makes an additive whole.
- **Transposed tables.** When attributes run down and entities run across
  (a settings comparison, a cohort matrix), the type lives in the row: text
  rows left-aligned, numeric rows right-aligned with one format per row, a
  status row shown once. The "one format per column" rule is really "one
  format per type axis"; apply it to whichever axis carries the type.
- **Repeated column groups** (channel × cohort, region × quarter) keep the
  same column order and widths in every group, a spanner per group, and a
  visible seam between groups: a narrow spacer column or a single light
  left rule on the group's first column. That seam is the one vertical mark
  a table may carry (`FAST` 2.02, `Schwabish` G10).
- **Wide tables are read by scrolling, and that is fine.** "Laptop width"
  means every viewport the reader lands on supports a coherent reading
  task, not that the whole dataset fits at once. Keep identity recoverable
  at every position: label column frozen, spanner naming the group above
  every column, units in the header, the newest or most important group
  first. Split a wide table only at a boundary that means something to the
  reader (a different entity, a different grain); splitting a time axis
  across tabs breaks comparison. Then look at the first view and at
  representative views across the full extent, not only the top-left.
- Never rotate or stack header text; abbreviate, wrap to two lines or
  transpose (`Schwabish`, `UKGAF`).

**Rules, borders, fills**
- Start with no borders. Add back only horizontal rules that carry
  structure: under the header, above totals, optionally at the table foot,
  optionally every 3-5 rows in long tables. Thin (1 px), light grey, solid.
  No vertical rules except the light seam between column groups, never
  full grids, never thick or double lines except
  the finance double rule under a grand total (`Schwabish` G3, `Few`,
  `Tufte` data-ink, `ACAPS`).
- Delineate rows by white space first, then a near-white band, then a thin
  rule. Zebra striping only for wide tables (about 7+ columns) or tables
  longer than a screen; one very light tint on alternate rows. Evidence:
  striping shows no measured speed or accuracy gain in short tables
  (`Enders`, `Adobe` 2023) but readers prefer it in wide ones.
- Do not use fills to divide sections; use a blank row plus a section
  heading. Do not stack banding, per-cell fills and conditional-format fills
  on the same range; one fill owner per range (`Google` banding priority).
- Gridlines off on presentation tabs, on for data-entry and raw tabs
  (**contested**: Raffensperger keeps the grid; `TTS` removes it; Microsoft's
  accessibility guidance favours strong visible structure).

**Totals**
- Bottom of a detail table, bold, thin rule above, labelled `Total`. On a
  summary the headline total goes top-left as a KPI with the breakdown
  below. Totals are formulas over the whole range, never typed, and never
  feed downstream logic (`Schwabish` G6, `Few` K1-K3, `FAST` display totals).
- When shares of an additive whole appear, show the whole; do not total
  columns that are separate populations (versions, cohorts) just because
  they sit side by side.

**Widths, heights, density**
- Set widths explicitly by column type after writing values: label column
  wide enough for the longest label on one line (about 200-300 px), numeric
  columns 80-130 px sized to the widest formatted value plus a small gutter,
  all time-period columns the same width, Notes column 300-480 px. Never
  stretch a table to the page; never leave numeric columns wide
  (`Schwabish`, `Butterick`, `FAST` 4.02).
- **Give the tab room to breathe.** Sheets' defaults (21 px rows, 2-3 px
  padding, 100 px columns) are typing defaults. A tab meant to be read gets
  taller rows (roughly 26-30 px), more side padding, columns with a real
  gutter beyond the widest value, a blank row between blocks, and a title
  row taller than the body. Uniform row height throughout the body; header
  and spanner rows as tall as their wrapped content needs, no taller. If a tab feels tight, it is: fix the
  room before adding rules or fills (`Butterick`, `Material`/`Carbon`
  density guidance, `Adobe` table study on padding).
- A comparison table that a person reads whole holds about 7-10 data
  columns; beyond that, ask whether the reader compares across all of them
  (a time axis, a version series: keep it wide and scroll) or only within
  a few (split, transpose, or move detail to another tab) (`Schwabish`,
  `Few`).
- Derived columns sit immediately right of the columns they come from;
  compared columns sit adjacent; order left to right: identifier, primary
  measure, comparison or delta, supporting measures, notes (`Few` J2).
- No blank spacer rows inside a table and no blank columns inside a group;
  separate stacked tables with one blank row and a section heading, and
  column groups with the narrow seam above (`UKGAF`, `FAST` 4.02,
  `Few` I5). Spacer rows inherited from an old layout are relics: remove
  them once you know nothing reads their addresses.
- Order rows by meaning (rank, size, time, tier), not alphabetically by
  default; most important row first (`Few` J1, `Schwabish`).

## 7. Numbers, dates and missing values

- **One number format per type axis**: per column in an ordinary table, per row in a transposed one, per block in a label/value table.
  Same decimals for every value of a type. Default precision: counts and
  money at scale 0 decimals; percentages, multiples and indices 1 decimal;
  per-share or unit prices 2; factors 4. Too many decimals is ICAEW's "most
  common formatting mistake" (`ICAEW` FMC, `BIWS`, `Few` B8, `Schwabish`).
- **Thousands separators** on every integer of 1,000 or more, via number
  format and locale, never typed. Never group years (`Schwabish`, `ISO`).
- **Scale with the format, not by dividing**: `0.0,"K"` and `0.0,,"M"`
  divide on display; state the scale once in the header (`Revenue ($M)`).
  One scale per column or block; never `1.2M` beside `850K` (`Few` D3-D5,
  `Google` format tokens).
- **Units in the header or a units column**, never inside the value cell
  (`Few` D8, `Schwabish` G4, `FAST` 3.05-13).
- **Negatives**: leading minus for general readers, parentheses in financial
  statements; either way the whole block uses one convention and red is at
  most a second cue. Use the explicit `positive;negative;zero;text` custom
  format so signs and zero display are deliberate (`Schwabish`, `WSP`,
  `Few` D7). Show zero as `0` (or the finance dash `–` in a financial
  schedule); never show `0` for unknown.
- **Missing values**: unknown, not applicable, not yet mature and true zero
  are different facts. Decide one display mark for "no value" (`—` or
  `n/a`) and apply it through number formats or the presentation formula,
  so the underlying cell keeps its meaning: a blank that a formula tests, a
  future destination a sync script will fill, or an inapplicable
  intersection must not be overwritten with text that breaks arithmetic or
  the writer. `0` only for a true zero; never sentinel numbers; a visible
  empty-state line for a block with no data yet (`Few` I1-I4, `UKGAF`).
- **Composite evidence strings** (`0.9% (6/677)`, `2.1 (59/28)`) hold two
  facts: the reported measure and its evidence. Separate them so the
  measure gets a numeric format and the evidence stays visible on the axis
  that keeps it with its measure (a muted evidence sub-row under each
  measure row in a wide version table; a paired column in a narrow one; a
  note only when it is rarely consulted). Keep qualifiers such as to-date,
  lower-bound or excluded beside the evidence. Keep the reported measure as
  the observation; do not recompute it from the rounded evidence.
- **Source-owned blanks.** Separate the missing state from its display.
  Where a presentation formula or format already owns the cell, render the
  workbook's mark there. Where a synced observation is genuinely blank and
  no such layer exists, leave the blank and explain its meaning once (a
  header note, a maturity row, a key); do not invent a source table solely
  to draw a dash, and do not let an alert replace a value that exists. Keep
  zero, undefined (n = 0), unavailable and immature recoverable beside the
  measure.
- **Dates**: store real dates, display ISO `yyyy-mm-dd` on data tabs and a
  short unambiguous form (`Sep 2026`, `2026-09`, `Q3 2026`) on summaries;
  four-digit years, never locale slash dates. Generate period headers with
  `EDATE`/`EOMONTH` from one baseline cell; never type a date series
  (`Few` G1-G6, `FAST` timelines, `ISO 8601`).
- **Percentages** stored as fractions and displayed with `%`; 0-1 decimals;
  share-of-total columns sum to 100 percent with the total shown (`Few` D9).
- **Multiples** carry `x` via format (`0.0"x"`), never typed text.
- **Currency symbol** in a financial schedule: first row or header only,
  not every cell (`BIWS`, `Schwabish`); in a mixed-measure table, a money
  format on the money rows is what tells them apart.
- **Sign convention** chosen once, written in the key, applied everywhere;
  label rows where direction could be misread (`ICAEW`, `WSP`, `FAST`).

## 8. Colour, type and status

**Colour**
- Default is monochrome: near-black text on white, light grey for structure.
  Add colour only to encode one meaning: input versus formula versus link,
  one highlight, one alert. At most 6-8 colours in the workbook, identical
  meaning on every tab and every chart, documented in the key (`Few` A16,
  `Schwabish` G5, `WSP`, `Macabacus` colour count).
- Every text/fill pair meets WCAG AA: 4.5:1 for normal text, 3:1 for large
  or bold 14 pt+ text and for non-text marks such as rules and icons. Do not
  round 4.47 up (`WCAG` 1.4.3, `WebAIM`).
- Colour is never the only carrier of meaning: pair it with a word, a sign,
  a glyph or position. Design it to work in greyscale (`WCAG` 1.4.1, `ICAEW`
  FMC, `Few`, `Stone`: "get it right in black and white").
- Avoid red/green pairs as the only distinction; if categorical colour is
  unavoidable, use a colour-blind-safe set such as Okabe-Ito.
- Fills stay near-white; no fills on numeric cells except the input fill, a
  single highlight or a light heat-map; no white-on-dark text for data.
  One dark brand band for the tab title is the sanctioned exception.
- Conditional formatting sparingly and only for simple rules: check
  failures, alerts, greying out inactive periods; never decoration
  (`ICAEW` FMC, `FAST` 4.03).

**Type**
- One font family for the workbook (a second only for the title or
  headings). Sans-serif with tabular lining figures by default: Arial,
  Inter, Roboto, Calibri-class pass; test any candidate by typing eleven
  zeros over eleven ones and checking the rows are the same width
  (`Butterick`). Sheets cannot switch OpenType figure sets, so the default
  figures must already be tabular.
- Body 10 pt minimum; 10-11 for dense models, 11-12 for reading-oriented
  summaries. Headers within 1 pt of body, emphasised with weight not size.
  Title 13-14 pt bold. No italics or underline for emphasis, no condensed or
  decorative faces, no letter-spacing (`Schwabish`, `UKGAF`, `Few` A15).
- Bold is reserved for the header row, totals, section headings and at most
  a handful of highlighted values.
- Size hierarchy on a summary: one hero number largest, supporting KPIs
  about a third of it, body text below that (`Few` A6).

**Status and direction**
- Every status carries a word or glyph (`On track`, `▲ +4%`, `OK`, `CHECK`);
  at most two alert levels; show the alert only when something needs
  attention, nothing (not a green tick) when all is well (`Few` H1-H2,
  `WCAG` 1.4.1).
- **A state is shown once.** If a campaign has no current counterpart, one
  status cell says `No current restoration` and the cells below show `—`.
  Filling a whole column red and repeating the sentence in every row turns
  the signal into wallpaper, hides the values that could have been there,
  and leaves nothing for a real exception to stand out against. The same
  applies to a whole row or block: mark the row label or a status column,
  not every cell (`Few` H2, `Tufte` data-ink).
- **Bold is not a state.** Bold data cells read as "important" but say
  nothing; a reader cannot tell emphasis from an error. Reserve weight for
  headers, totals and section headings; carry state with a word plus, at
  most, a light fill.
- **Machine-written cells are a role, not an alert.** Values pushed by a
  sync script are imported data: plain ink, named in the header or key
  (`Synced from BigQuery, refreshed <cell>`), never yellow or red, which the
  reader has learned to read as warning. If the reader must know which
  cells a script owns, protect them and say so in the key.
- Direction of change with `▲`/`▼` or `+`/`−` glyphs beside the number; a
  custom format such as `[color50]0.0% ▲;[color3]-0.0% ▼;0.0%` keeps the
  cell numeric.
- Vary intensity of one hue for levels (light red warning, dark red
  critical) rather than red/yellow/green; the flag column sits beside the
  metric it judges, not in a far column (`Few` H3, H6).

## 9. Formulas a reader can audit

- **Short.** A formula fits the thumb on screen, is explained in under 24
  seconds, and never wraps to a second line. Break multi-step logic into
  separate labelled rows (`FAST` 3.02, `Panko` 84 percent vs 53 percent
  detection, `ICAEW` P13).
- **One formula per row (time series) or per column (vertical table),**
  written once and copied across the whole range; no partial ranges, no
  exceptions hidden in the middle of a row. If a first-period cell must
  differ, make it loud: square-bracketed label or a note (`FAST` 3.01,
  `SMART`, `ICAEW` P12).
- **Ingredients local.** Link precedents from other tabs into a labelled row
  on the current tab (green font), then compute from local cells. Never
  `='Other tab'!C9*2` inside arithmetic. Link to the original source cell,
  never to a link ("no daisy chains") (`FAST` 3.02-04, `ICAEW`, `WSP`).
- **Boring functions.** SUM, MIN, MAX, INDEX/MATCH, SUMIF/COUNTIF,
  FILTER, EDATE/EOMONTH, simple IF/AND/OR. Avoid OFFSET, INDIRECT, volatile
  functions in calculation chains, nested IFs (use 1/0 flags on their own
  rows), and array formulas in the human-read calculation chain; accept
  ARRAYFORMULA/QUERY/MAP on data-prep tabs where "copy the first cell across"
  review is not the point (`FAST` 3.02, `ICAEW` P12 and P15, **contested**:
  Raffensperger's nest-and-erase; LET is fine where it removes duplication in
  one row).
- **Anchor only what the copy requires.** Over-anchoring and same-sheet
  names in references are noise (`FAST` 3.02-09).
- **Never rely on iterative calculation.** Sheets has it off by default;
  collaborators will not know to turn it on (`FAST`, `ICAEW`, `SMART`).
- **Named ranges sparingly**: a few global levers referenced from many tabs
  and validation lists; not every row. Names did not improve error detection
  in experiment (`McKeever&McDaid`; `FAST` 3.02, `WSP`).
- **Readable text formulas.** A "reading" or status sentence generated by
  `IF` from a threshold input keeps the words true when the numbers move;
  keep the sentence under about 75 characters.
- **Hyperlinks** to other tabs use `=HYPERLINK("#gid=<sheetId>","Label")`
  with a short label; workbook navigation lives in the Read Me tab map or a
  muted link cell in the header area; a `Details →` link on a record or
  metric row is not navigation, it is that row's keyed detail.

## 10. Consistency across tabs

- Same column purposes in the same letters on every tab of the same kind:
  label column, units column, first period column, notes column
  (`FAST` 2.01, `ICAEW` P5, `Few` J6).
- Same header row number, same title row treatment, same fonts, same number
  formats per type, same colour key, same freeze rule, same tab colour
  scheme (`ICAEW` P5-P6, `Schwabish` G10: small multiples of tables).
- Same time axis in the same columns on every time-series tab, running the
  same length; roll up on separate rows or tabs; never mix monthly and
  annual columns in one row (`FAST` 2.02, `ICAEW`).
- Same format key applied by rule, not by hand: define the styles once
  (a house-style reference or a documented key) and apply them with
  `repeatCell` ranges, never ad hoc per cell (`ICAEW` P6, `FAST` 4.01).
- Same words for the same thing everywhere: one label per concept, one
  abbreviation per term, one missing-value code, one date format per tab
  type.

## 11. Verification: how to prove the sheet is right

Assume the sheet contains errors until tested: lab cell error rates average
3.9 percent and 94 percent of audited operational spreadsheets contain at
least one error (`Panko` 2015). Formatting conventions raise detection, they
do not prevent errors. So verify twice: the format, and the logic.

**Preserve the reference contract while you rebuild.** A tab is read by
other tabs, by hyperlinks, by cell notes and often by a sync script that
writes to fixed addresses. Before moving or replacing cells: keep a baseline
(the copy you are working on, plus a saved grid dump that includes the
state controlling visibility and addressing: hidden or grouped rows and
columns, filters, merges, named ranges, protected ranges), find out who
reads and writes the addresses you will move, prefer native row and column moves
(`moveDimension`) over clear-and-rewrite so references follow, and expand
the grid before writing formulas that point beyond it (a reference written
past `rowCount` and then shifted by the expansion silently points at the
wrong row). Verify the dependency surface: every formula on the tab and on
tabs that reference it evaluates without error, and every original output
still matches, not just two or three attractive ones. Separate pre-existing
errors and deliberate presentation changes from introduced changes.
Formatting success and calculation success need different evidence, and a
value present in the API is not yet evidence that a reader can find it: a
column that inherited `hiddenByUser`, a collapsed group or a filter hides a
perfectly formatted, perfectly preserved field.

**Look at it first.** Open the tab in the browser (BrowserOS: one
background tab on the sheet URL with its `gid`, then `screenshot`) and read
it as a stranger at laptop width: is anything cut off, spilling, repeated,
loud, or cramped? Does the first screen show the title, the inputs and a
table with a header? Could you say what each column is without the label
column? A sheet that has not been looked at has not been formatted; the
API cannot see clipping, collisions between overflowing strings, or a row
that reads as a paragraph. Know what you captured: BrowserOS's screenshot
size option scales the image, it does not narrow the viewport, so measure
the real viewport (`evaluate` `window.innerWidth`) and say what width the
proof represents; typing an address in the name box selects but does not
scroll frozen panes; a selected cell with a note shows a tooltip over the
grid. Scroll to representative positions on wide or tall tabs and inspect
each image yourself. Bind every proof to the state actually captured:
record the measured layout viewport for each final view, distinguish image
pixels from CSS pixels, and confirm the capture includes the intended
extent. After a navigation or scroll, judge the identity and content
visible in the image rather than trusting the range you requested; Sheets
sometimes re-scrolls to the selection, and a shared browser's zoom can
change under you. These are tool-agnostic duties; the BrowserOS mechanics
live in the recipes.

**Format readback (after every batch of changes)**
- Read the grid back with the API (`includeGridData`, including
  `effectiveValue` so error values and numeric results are visible) and
  check, per tab: frozen rows cover only the identification area (spanner
  plus header at most) and frozen columns ≤ 1; merges only in a spanner
  row; A1 non-empty; one header row;
  every numeric cell right-aligned, one number format per type axis
  (the column, or the row in a transposed table);
  every text cell ≤ ~90 characters or in a Notes column; no cell with
  `wrapStrategy: CLIP`; body rows uniform within a table, header and
  spanner rows as tall as their wrapped content needs and no taller; every literal number classified (observation shown as
  data, assumption in the input style, nothing derived left typed); colour
  pairs at 4.5:1.
- Fit: for every text cell whose right neighbour is non-empty, compare the
  string's rendered width with the column width (about 6-7 px per character
  at 10 pt for Inter or Arial; use it to find suspects, then look). Flag
  labels that run past the label column, values that run past their
  column, and any `formattedValue` over about 90 characters outside a
  Notes column.
- Signal budget: count filled and bold cells; if a whole column, row or
  block carries a state fill, or the same caveat or decoration is restated
  in every row of one record's block, the signal has become wallpaper. The
  same status value across many records is data, not wallpaper.
- Search formulas for embedded constants: a digit sequence that is not a
  reference is a candidate; read the formula and decide whether it is an
  assumption (extract it) or syntax (leave it). Do not turn precision
  arguments, offsets, unit conversions or link ids into "inputs".
- The browser screenshot is the artifact: does the first screen show the
  title, the inputs and the first table? Is anything clipped? Are the fonts
  rendering (a bogus font name is stored silently and renders as a
  fallback)? Export to PDF only when the sheet will be printed or shared as
  a PDF.

**Logic tests (before calling the numbers right)**
- Predict, change one assumption, compare against the result you
  predicted for this model; push a lever to its validation bounds; extreme
  and impossible inputs should produce visible check failures, not silent
  numbers. These are model tests for the model's owner; a formatting pass
  proves preservation (every original output unchanged), not model
  behaviour, and never alters live assumptions to run a test
  (`Panko`, `ICAEW` P17-P19).
- Every check row reads `OK`; the master check reads `OK`.
- Cell-by-cell inspection of every unique formula; for anything important,
  a second independent reader. Self-review catches about half of errors;
  three inspectors catch about 90 percent (`Panko` inspection data).
- Expect logic and omission errors, not typos: review the sheet against the
  requirement, not only against itself.

**Defect severity for audit reports**
- P0: hidden assumptions (constants in formulas, typed derived totals,
  several levers packed into one string); observations painted as levers or relocated to fake
  inputs; merged cells in a data range; clipped text; colour-only meaning;
  a broken reference or changed output after the restyle.
- P1: frozen title block; paragraphs in cells; inconsistent number formats
  or alignment within a column; no inputs style or key; missing header rule;
  cross-sheet arithmetic.
- P2: centred numbers; dark header fills on data; vertical gridlines in a
  presentation table; wrap-induced tall rows; unlabelled units; tab names
  like `Sheet1`.
- P3: cosmetic inconsistency (fonts, widths, tab colours) that does not
  change reading order or meaning.

## 12. Evidence and resolved disagreements

The research behind this guide read the full text of about 150 sources across
four lanes: modelling standards (FAST 02c, ICAEW Twenty Principles 2024 and
Financial Modelling Code 2024, SMART, WSP/TTS/BIWS/Macabacus, CFI, Panko
2000/2015, Powell-Baker-Lawson 2008, Raffensperger 2001, Bewig 2005, Grossman
and Ozluk 2010, Hermans Enron corpus); table design (Schwabish 2020/2021,
Few, Tufte, Wong, Butterick, Strom, Coyle, UK Government Analysis Function,
Broman and Woo, Enders and Adobe striping studies, WCAG 2.2, Okabe-Ito,
Material, Carbon, APA/CMOS/CSE); Sheets mechanics (Google Sheets API v4
reference and samples, Google and Microsoft accessibility and style docs,
NN/g, a live API probe); and dashboard readability (Few IDD, Fairhurst,
Chandoo, Ben Collins, Knaflic, Wilson, Baymard, Arditi and Cho 2007).

Where authorities disagree, this guide chose:

| Question | Sides | Choice here |
|---|---|---|
| Inputs tab vs inputs beside formulas | FAST/ICAEW/SMART vs Raffensperger/Bewig | Inputs block at top for small sheets; Inputs tab beyond ~20 inputs |
| Many tabs vs one long tab | FAST/SMART vs WSP/Bewig | Few purposeful tabs; local ingredient rows |
| Short stepwise vs nested formulas | FAST/WSP/Panko vs Raffensperger | Short, one per row; LET only to remove duplication |
| Colour scheme | Banking blue/black/green vs FAST blue-import/red-export vs Macabacus | Banking font colours plus a light input fill and a key |
| Header styling | Bold + rule (Schwabish/Few/UKGAF) vs dark fill (banking templates) | Bold + light rule; one dark band for the tab title only |
| Header alignment | Match data (design) vs centre (CMOS/CSE) | Match the data |
| Zebra striping | Preferred but unmeasured (Enders/Adobe) | Only wide or long tables, near-white tint |
| Gridlines | Keep (Raffensperger) vs remove (TTS) | Off on presentation tabs, on for raw data |
| Frozen rows | No standard gives a number | 1 (max 2) + 1 column; none on a one-screen summary |
| Cell notes | Never (FAST) vs over-comment (WSP) | Notes column for anything the reader must see; cell notes for provenance |
| Negatives | Minus (general) vs parentheses (finance) | Minus by default; parentheses in financial statements; one per block |
| ALL CAPS | Less legible (style guides) vs more legible at small sizes (Arditi and Cho) | Sentence case, on style grounds |
| Named ranges | Avoid (FAST/WSP) vs name everything (Operis/Bewig) | A few global levers and validation lists only |
| Circular references | Forbid (FAST/ICAEW) vs allow with breaker (WSP) | Forbid |
| Wrap text | Wrap every text column (UKGAF) vs never rely on wrap (Few) | Overflow for short notes beside values; wrap only in a wide Notes column, ≤ 2 lines |

Verbatim anchors worth remembering:

- "Formatting for formatting's sake is unnecessary and formats do not
  automatically communicate their meanings to the user." (ICAEW FMC)
- "Do not merge cells." (FAST 4.02-02)
- "Include master error checks and alert indicators in the freeze pane."
  (FAST 2.03-05)
- Put input explanations in a dedicated comments column, "visible on
  print-outs; do not use cell comments for such information." (FAST 2.04-02)
- "Get it right in black and white." (Maureen Stone)
- "Maximize the content-to-chrome ratio by keeping it small." (NN/g on sticky
  headers)

## 13. Field lessons: what went wrong the first time agents used this

Two tabs built by another agent with this skill in hand, and what the
reader saw. Each is a judgment failure, not a missing rule; the fix is to
reason from section 0.

**Case A: a channel × cohort matrix (51 columns, 1,000 rows).**
- Ten cells held 160-345-character sentences: a two-row description under
  the title, an explanation in every section-heading row, and a maturity
  note per cohort. They overflowed across the whole width and, where two
  met, collided into unreadable text. The agent read "overflow into empty
  neighbours" as permission for prose. Lesson: overflow is for a short note
  beside a value; a sentence longer than the table is wide is Read Me or
  Notes content, and a section row holds a heading only.
- Labels up to 85 characters in a 240 px column spilled into the first
  value column, so rows read `Revenue by D30, net store proceeds (` then
  `$)` then numbers. Lesson: labels are names; definitions go to notes.
- The first value column doubled as the text column, so its 17 numbers were
  left-aligned while every other column was right-aligned. Lesson: a column
  has one role on a tab; text never lives in a column that holds numbers.
- Two parameters (`Modeled LTV per payer`, `First-open cohort`) were plain
  black cells. Lesson: a lever on a dashboard is still a lever; it is only
  one if the reader can see it.
- Group headers (`August 2026 cohort`) sat left-aligned in the first column
  of six. Lesson: a spanner has to sit over its group; centre it (see
  section 6).
- Title in B1, A1 empty, no frozen header, 110 px columns, 22 px rows,
  3 px padding. Lesson: the reader needs A1, a header they can keep, and
  room.

**Case B: a campaign settings comparison (attributes down, campaigns
across).**
- 65 of 278 cells were wider than their 120 px column and were cut off:
  campaign names, IDs, audiences, placements, markets. The agent set
  widths once and never looked. Lesson: fit is decided per column with the
  content in front of you, then confirmed on the render; IDs and long
  names are shortened with the full value in a note.
- 54 cells were filled red and `No current restoration` was written 18
  times down one column; the March column of the first campaign was bold
  throughout. Lesson: show a state once with a word; bold is not a state;
  when everything is highlighted nothing is.
- 274 cells carried vertical borders (a full grid) on 22 px rows with 3 px
  padding. Lesson: structure by position and space; ink last; give the tab
  room.
- Missing values appeared as `N/A` in some rows and blank in others.
  Lesson: one missing-value code, everywhere.
- A description paragraph occupied rows 2-3; a data row (`Campaign name`)
  was styled as a header. Lesson: one title row; header styling belongs to
  the row that names the columns and nowhere else.

What would have caught all of it: opening the tab in the browser and
reading it once as a stranger before reporting done.

**Case C: the first lab round (four tabs by a careful agent).** The
results were far better, and the agent's critique exposed contradictions
in the skill itself, all fixed above: the matrix template froze three rows
while the law allowed two (frozen rows are a prefix, so identity goes in
the corner cell); "hard-code only inputs" gave imported observations no
home, so 3,914 synced facts were relocated to a fake inputs table and
linked back (ownership now decides); evidence strings such as `0.9%
(6/677)` had no recipe (separate measure from evidence, never recompute
the measure); every cell got a provenance note, which reads as texture
(provenance once, on the owner); old spacer rows were preserved as if they
were data (relics leave once their absence is understood); and a group
column was dropped from a scorecard to make room (a group is information:
make it a section row, not a casualty).

**Case D: the second lab round (eight tabs, revised skill).** Results now
read cleanly at 1366 px: centred two-level headings on the transposed
comparison, one `Current · absent` status instead of eighteen red cells,
group section rows and a muted evidence sub-row per measure on the
scorecard, an inputs tab whose `Basis · caveat` column tells observed from
policy from modelled, a tracker with one item per row and hidden columns
brought back. The agent's remaining findings were about the skill's
consistency and its blind spots, all folded in above: keep one layout
contract across laws, templates, recipes and readback; ownership is not
dependency, and trackers are authored records; choose the comparison unit
before widths or evidence placement; inspect visibility state, not just
values; give source-owned blanks a presentation contract instead of a
rule; bind visual proof to the captured viewport.
