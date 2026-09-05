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

1. The ten laws
2. Screen budget: freeze panes and the title block
3. Workbook architecture: tabs, order, names, Read Me
4. Inputs and levers versus formulas
5. Text in cells
6. Tables: alignment, headers, rules, totals, widths
7. Numbers, dates and missing values
8. Colour, type and status
9. Formulas a reader can audit
10. Consistency across tabs
11. Verification: how to prove the sheet is right
12. Evidence and resolved disagreements

## 1. The ten laws

These are the rules a reader complains about first. Break one of these and
nothing else in the guide will rescue the sheet.

1. **Freeze only what identifies columns.** One header row (two at most) plus
   at most one label column. Never a title block, never a notes row, never
   five rows. On a 13-inch laptop about 33 default rows are visible; each
   frozen default row costs about 3 percent of every screen the reader will
   ever see, and each frozen 40 px header row costs about 6 percent
   (`NN/g`, `FAST` 2.03, laptop arithmetic verified against Sheets' 21 px
   default row). A summary tab that fits on one screen freezes nothing.
2. **Hard-code only inputs and levers.** Every other number is a formula or a
   link. A constant typed inside a formula (`=B5*70%/20%`, `=C8*2`) is a
   hidden input the reader cannot see, test or change. The only tolerated
   embedded constants are universal ones whose meaning is obvious in place
   (12 months, 24 hours, 1000 for scaling, 1 and 0, a ROUND precision digit) (`FAST` 3.03, `ICAEW`
   P10, `Macabacus` partial-input rule).
3. **Inputs look like inputs.** Every hard-coded input has a fill or border
   and a distinct font colour, appears exactly once, carries a unit, and sits
   in an inputs block or inputs tab that the reader can find without
   scrolling through calculations. Font colour alone is not enough (`ICAEW`
   FMC: fill and/or border; `WSP`: blue inputs, black formulas, green
   cross-sheet links).
4. **One line per cell.** A cell holds a label, a value, or one short phrase
   (about 45-90 characters, 50-70 ideal). Anything longer is split into
   label + value, one point per row, a Notes column, a cell note, or the
   Read Me tab. No paragraphs, no bullet lists with line breaks inside a
   cell (`Butterick` line length, `MS` style, `Broman&Woo`, `FAST` 3.05).
5. **Never merge cells.** A title lives in the first cell of its row and
   overflows into empty neighbours. Merges break sorting, selection, screen
   readers and audit tools; Sheets has no "center across selection"
   (`FAST` 4.02-02, `MS` accessibility, `UKGAF`).
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
  spacer rows or notes rows. If the table starts at row 4 because rows 1-3
  are a banner, either move the banner into one compact title row and freeze
  two rows total, or drop the banner into the tab name and Read Me.
- Summary or dashboard tabs that fit on one screen freeze nothing
  (`Few` IDD: single screen, no scrolling). Multi-table tabs (several small
  tables stacked) freeze nothing or only the title row, because no single
  header row identifies every column below it.
- A model with checks may keep exactly one master check cell in the frozen
  area; nothing else earns a frozen row (`FAST` 2.03-05).
- Title block: one row. Left: sheet title (what, where, when, unit if
  uniform). Right, muted: data-as-of date and source, driven by a cell, not
  typed into the title. Never a second title row for a subtitle; put the
  subtitle in the Read Me or as a short muted line under the title only when
  the tab is a one-screen dashboard (`Few`, `Schwabish` G7, `L1`).
- Put text in A1 on every tab. Screen readers start there; sort, filter,
  QUERY header detection and "select all" assume a rectangle that starts at
  A1 (`MS`, `Google`, `Broman&Woo`).
- Frozen rows double as the repeated print header in Sheets; that is a
  reason to freeze the header row, not a reason to freeze the banner.
- Row heights stay at the default (21 px in Sheets) except the title row
  (about 28-32 px). Tall rows push data below the fold and make the reader
  read downward instead of across (`Raffensperger`).

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
- Never hide tabs or rows to tidy up; group rows instead, and delete relics
  (unused inputs, dangling calculations, empty tabs, formatting beyond the
  used range) (`FAST` 1.03, `ICAEW` P16, `Raffensperger`).
- Read Me tab, always, inside the workbook: purpose in one sentence, owner,
  version and date, what changed, tab map with hyperlinks, the format key
  (every font colour, fill, border and tab colour with its meaning), units
  and sign convention, source of each input with pull date, known
  limitations. One short sentence per row, label in column A, text in column
  B overflowing to the right (`ICAEW` P4 and P18, `FAST` 1.04, `CFI`,
  `Few` E7).
- Version and data-as-of live in the Read Me and in a cell; the file title
  carries the version only when copies are distributed (`ICAEW` P18).

## 4. Inputs and levers versus formulas

**Definition.** An *input* is a fact the model takes from outside (a baseline,
a price, a date, a count from a source). A *lever* is an assumption the reader
is invited to change (a growth rate, a mix, a capture rate, a threshold).
Everything else is a *formula*: derived from inputs, levers, and other
formulas. Outputs are formulas with presentation formatting.

- **Hard-code only inputs and levers.** A number typed anywhere else is a
  defect. Recognition test: if the reader changed this number, would they
  expect the sheet to recalculate? If yes and it is typed, it is a hidden
  input. If the number is a total, a share, a multiple, a date in a series,
  a "reading" sentence derived from a threshold, or a count of rows, it must
  be a formula (`FAST` 3.03-01, `ICAEW` P10, `WSP`, `Few` D10, K3).
- **No constants inside formulas.** `=B8*2` becomes `=B8*$B$4` with `B4`
  labelled `Growth multiplier per month` and formatted as an input.
  `=$B$5*70%/20%` becomes `=$B$5*C$12/$B$8` with the mix and capture rate as
  labelled inputs. Tolerated in place: 12, 24, 7, 1000, 1, 0, 100 when they
  are unit conversions whose meaning is obvious (`FAST` 3.03, `Macabacus`
  ignore-list 0/1/100/1000/1000000).
- **Levers are numbers, not strings.** `"70% / 20% / 10%"` in one cell is a
  label pretending to be three inputs. Store each lever in its own numeric
  cell with its own format; if the reader wants to see the trio, a formula
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
- **Input cell style.** Distinct font colour **and** a light fill or border,
  applied identically to every input in the workbook, with the key on the
  Read Me. Banking convention: blue font hard-codes, black formulas, green
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
- **Overflow, do not merge, do not wrap by default.** For a short note next
  to a value, keep `wrapStrategy: OVERFLOW_CELL` and leave the cells to the
  right empty so the text spans them. That is how a string "spans multiple
  cells" without a merge. Use `WRAP` only in a dedicated wide Notes column,
  and keep strings short enough for at most two lines; row height follows
  the tallest cell, so one long wrapped cell makes the whole row tall
  (`Google` WrapStrategy, `Few` E5, `MS` wrap docs).
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
  for anything a reader must see, cell notes for provenance only.
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
- Exactly one header row per table. Bold, sentence case, one to two words
  plus the unit in round brackets, wrap allowed to two lines. A thin light
  rule under it. A light neutral fill is acceptable; a dark fill with white
  text is not the default for data headers (`Schwabish` G7, `Few`, `UKGAF`).
- Group labels ("spanners") only in presentation tables, in their own
  unmerged row, with white space rather than lines separating groups; in
  data tables prefix the header instead (`Schwabish` G8, `Few` J3).
- Never rotate or stack header text; abbreviate, wrap to two lines or
  transpose (`Schwabish`, `UKGAF`).

**Rules, borders, fills**
- Start with no borders. Add back only horizontal rules that carry
  structure: under the header, above totals, optionally at the table foot,
  optionally every 3-5 rows in long tables. Thin (1 px), light grey, solid.
  Never vertical rules, never full grids, never thick or double lines except
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
- Show the total row whenever percentages of a total appear.

**Widths, heights, density**
- Set widths explicitly by column type after writing values: label column
  wide enough for the longest label on one line (about 200-300 px), numeric
  columns 80-130 px sized to the widest formatted value plus a small gutter,
  all time-period columns the same width, Notes column 300-480 px. Never
  stretch a table to the page; never leave numeric columns wide
  (`Schwabish`, `Butterick`, `FAST` 4.02).
- Uniform row height throughout, header the same height as data. Sheets'
  default 21 px is tight but fine; 24-26 px reads better for dense tables.
- Keep tables to about 7-10 data columns; split, transpose or move detail to
  another tab beyond that (`Schwabish`, `Few`).
- Derived columns sit immediately right of the columns they come from;
  compared columns sit adjacent; order left to right: identifier, primary
  measure, comparison or delta, supporting measures, notes (`Few` J2).
- No blank spacer rows or columns inside a table; separate stacked tables
  with one blank row and a section heading (`UKGAF`, `FAST` 4.02, `Few` I5).
- Order rows by meaning (rank, size, time, tier), not alphabetically by
  default; most important row first (`Few` J1, `Schwabish`).

## 7. Numbers, dates and missing values

- **One number format per column** (or per block in a label/value table).
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
- **Missing values**: decide one code and use it everywhere; `n/a` or `—`
  for not measured, `0` only for a true zero, a visible empty-state line for
  a block with no data yet, never a blank data cell that means "unknown",
  never sentinel numbers (`Few` I1-I4, `UKGAF` shorthand convention).
- **Dates**: store real dates, display ISO `yyyy-mm-dd` on data tabs and a
  short unambiguous form (`Sep 2026`, `2026-09`, `Q3 2026`) on summaries;
  four-digit years, never locale slash dates. Generate period headers with
  `EDATE`/`EOMONTH` from one baseline cell; never type a date series
  (`Few` G1-G6, `FAST` timelines, `ISO 8601`).
- **Percentages** stored as fractions and displayed with `%`; 0-1 decimals;
  share-of-total columns sum to 100 percent with the total shown (`Few` D9).
- **Multiples** carry `x` via format (`0.0"x"`), never typed text.
- **Currency symbol** on the first row of a schedule or in the header only,
  not every cell (`BIWS`, `Schwabish`).
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
  with a short label; navigation links live in the Read Me tab map or a
  muted link cell in the title row, not in data rows.

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

**Format readback (after every batch of changes)**
- Read the grid back with the API (`includeGridData`) and check, per tab:
  frozen rows ≤ 2 and frozen columns ≤ 1; no merges; A1 non-empty; one
  header row; every numeric column right-aligned with one number format;
  every text cell ≤ ~90 characters or in a Notes column; no cell with
  `wrapStrategy: CLIP`; no row taller than the title row except a two-line
  wrapped Notes cell; every hard-coded numeric cell outside the inputs block
  flagged; every input cell carrying the input style; colour pairs at 4.5:1.
- Search formulas for embedded constants: any digit sequence in a formula
  that is not a row/column reference, 0, 1, 12, 24, 100 or 1000 is a
  finding.
- Screenshot or PDF-export the tab and look at it at laptop width: does the
  first screen show the title, the inputs and the first table? Is anything
  clipped? Are the fonts rendering (a bogus font name is stored silently and
  renders as a fallback)?

**Logic tests (before calling the numbers right)**
- Predict, change one input, compare. Set all inputs to zero and confirm
  outputs go to zero. Push a lever to its validation bounds. Extreme and
  impossible inputs should produce visible check failures, not silent
  numbers (`Panko`, `ICAEW` P17-P19).
- Every check row reads `OK`; the master check reads `OK`.
- Cell-by-cell inspection of every unique formula; for anything important,
  a second independent reader. Self-review catches about half of errors;
  three inspectors catch about 90 percent (`Panko` inspection data).
- Expect logic and omission errors, not typos: review the sheet against the
  requirement, not only against itself.

**Defect severity for audit reports**
- P0: hidden inputs (constants in formulas, typed totals, levers as text);
  merged cells in a data range; clipped text; colour-only meaning.
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
