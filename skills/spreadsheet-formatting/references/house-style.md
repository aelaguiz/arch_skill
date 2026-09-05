# House style: the concrete default spec

This is the one style an agent applies unless the user names another. It
implements `formatting-guide.md`; when the two disagree, the guide wins.
Numbers are Google Sheets pixels and points; they are starting points that
looked right on a laptop, not gates. Adjust them to the content in front of
you (widths to the longest real label or value, row height to how dense the
tab is), then look at the render. Apply every value by range with
`repeatCell`, never cell by cell by hand.

## Neutral default (any workbook)

| Element | Spec |
|---|---|
| Font | One family for the workbook: Arial or Inter (both have tabular figures). Body 10 pt. Title 14 pt bold. Section heading 10 pt bold. |
| Ink | Near-black `#202124` on white. Muted metadata `#5F6368`. |
| Title row (row 1) | Tab title in A1, bold 14 pt, height about 36 px, left-aligned, `OVERFLOW_CELL`, no merge. Data-as-of and source in a muted cell at the right end of row 1, driven by a formula. No description rows under it; that text is Read Me or a note on A1. |
| Column header row | Bold, sentence case, unit in brackets, fill `#F1F3F4`, bottom border `SOLID` `#9AA0A6`, `WRAP`, `verticalAlignment: MIDDLE`, height = body height. Text headers left, numeric headers right. Header styling goes on this row only, never on a data row. |
| Spanner (group header) row | Only when columns come in groups. Its own row directly above the column headers; each group label horizontally merged across its group and centred, bold, bottom rule spanning exactly the group. A seam between groups: a 12 px spacer column or a left rule on the first column of each group. |
| Section heading | Bold 10 pt ink, one blank row above, bottom border `SOLID` `#DADCE0`, nothing else on the row. |
| Body rows | Height about 26-30 px on a tab meant to be read (Sheets' 21 px default is a typing height), uniform; padding `{4, 8, 4, 8}`; `verticalAlignment: MIDDLE` (`TOP` where a Notes column wraps). No fills. One blank row between blocks. |
| Row rules | Horizontal hairline `SOLID` `#DADCE0` under each body row in tables of 6+ rows; none in short label/value blocks. No vertical borders, ever. |
| Banding | Only tables wider than 7 columns or longer than a screen: second band `#F8F9FA`. Never together with per-cell fills. |
| Totals | Bold, top border `SOLID` `#5F6368`, label `Total`. |
| Inputs and levers | Font `#0000FF`, fill `#FFF2CC`, border `SOLID` `#DADCE0`, number format by type, data validation with a help message. |
| Cross-tab links | Font `#326405`. |
| Synced / machine-written data | Plain ink, no fill; the header or key says `Synced from <system>, refreshed <cell>`; protect the range if editors might type over it. Never yellow or red. |
| Formulas | Ink, no fill. |
| Check / status OK | Text `OK` in `#0F4316` on `#DEF7E1`; shown only for check rows. |
| Check / status alert | Text (`CHECK`, `Far below need`) in `#691811` on `#F9DEDC` via conditional format; one alert level unless two are truly needed (`#863F09` on `#FBDDC5` for warning). Shown once per entity in a status row or column; the cells it explains show `—`. |
| Numbers | Right-aligned. `#,##0` counts; `#,##0;(#,##0);"–"` finance schedules; `0.0%` percentages; `0.00"x"` multiples; `#,##0.0` one-decimal quantities; `$#,##0` money; `yyyy-mm-dd` dates on data tabs, `mmm yyyy` month headers on summaries. |
| Text | Left-aligned, sentence case, fits its column; short notes (under about 90 characters) may `OVERFLOW_CELL` into empty neighbours; `WRAP` only in a Notes column. IDs and codes are text, left, shortened for display with the full value in a note. Never `CLIP`. |
| Column widths | Decided against the longest real content plus a gutter: label 240-320 px (shorten the label before going wider); numeric 100-140 px, all period columns equal; date 100 px; short code 70 px; text-value columns in comparison tables as wide as their longest kept value; Notes 360-480 px. |
| Freeze | Header row only (2 if a group header exists) plus the label column on wide tables; nothing on one-screen or multi-table tabs. |
| Gridlines | Hidden on presentation tabs; shown on raw data tabs. |
| Tab colours | Read Me grey; Inputs blue; Summary/Output dark; raw data light grey; calculation tabs uncoloured. |
| Read Me | First or second tab: purpose, owner, version, data-as-of, tab map with `HYPERLINK("#gid=...")`, colour key, units, sources, limitations; one row each. |

Contrast on white (WCAG AA needs 4.5:1 text, 3:1 bold 14 pt+ and marks):
`#202124` 15.7; `#5F6368` 5.9; `#0000FF` on `#FFF2CC` 7.7; `#326405` 7.1;
`#0F4316` on `#DEF7E1` 10.1; `#691811` on `#F9DEDC` 9.5.

## Layout templates

**Single-table detail tab** (rows scroll):
row 1 title; row 2 column headers (frozen, with column A frozen when wide);
rows 3+ data; blank row; `Total` row; blank row; source line, muted.

**Comparison or matrix tab** (attributes down, entities across; or repeated
column groups such as channel × cohort): row 1 title; row 2 spanner row
(merged, centred group labels) when columns are grouped; row 3 column
headers; frozen through the header row plus the label column; type and
format by row for attribute tables; a status row shown once; seams between
groups; the newest or most important group first.

**Small model or dashboard tab** (fits one to two screens, stacked blocks):
row 1 title; blank; `Inputs and levers` heading and block (label | value |
unit or note); blank; one heading per table with its own single header row;
blank; `Notes` heading with one short line per row; blank; `Format key` (only
when there is no Read Me). Freeze nothing, or the title row only.

**Inputs tab**: row 1 title; row 2 headers `Input | Value | Unit | Source | Notes`;
one input per row, grouped by section headings, validation on levers,
every value cell in input style, protected everything else.

**Raw data tab**: row 1 headers; data; gridlines on; ISO dates; no formatting
beyond bold headers and number formats; one row per record, one fact per cell.

## Brand adaptation: how to add a house brand without breaking the rules

A brand shows up in at most four places: the title band, the section heading
colour, the input tint, and the fonts. Everything else stays neutral. Test:
if the sheet were printed in greyscale, would it still follow the guide?
If a brand colour fails 4.5:1 as text, use it only as a fill under dark ink
or as a rule, never as body text.

### Poker Skill (Fun Country) tokens, light theme for spreadsheets

Tokens come from `pokerskill-brand/design_system.md`; do not invent hexes.
The product UI is dark cobalt; spreadsheets stay light and borrow the cobalt
and cyan as accents.

| Role | Token | Hex | Contrast note |
|---|---|---|---|
| Ink (body text, formulas) | Cobalt/900 | `#181C25` | 16.5:1 on white |
| Muted metadata | Cobalt/300 | `#515D7B` | 6.3:1 |
| Title band fill | Cobalt/900 | `#181C25` | white text 16.5:1 |
| Title band text | White | `#FCFBF8` | Blinker 14 bold |
| Title band bottom rule | Cyan/500 | `#11B5E4` | `SOLID_MEDIUM`, the one flat-cyan accent |
| Section heading text | Cyan/900 | `#095B72` | 7.4:1 (Cyan/700 `#0D89AB` is 3.9:1, bold 10 pt only, avoid) |
| Column header fill | Gray/100 | `#EBEAEA` | ink 14.2:1 |
| Column header rule | Cobalt/200 | `#7785A6` | 3.6:1 mark |
| Body hairline | Cobalt/100 | `#CDD4E0` | decorative |
| Total rule | Cobalt/500 | `#384156` | 9.9:1 mark |
| Input font | Blue/500 | `#294ACA` | 6.3:1 on input fill |
| Input fill | Cyan/100 | `#D9F5FC` | |
| Input border | Cobalt/100 | `#CDD4E0` | |
| Cross-tab link font | Green/700 | `#176421` | 7.0:1 |
| Status OK | Green/900 on Green/100 | `#0F4316` on `#DEF7E1` | 10.1:1 |
| Status warning | Orange/900 on Orange/100 | `#863F09` on `#FBDDC5` | 6.0:1 (Yellow/900 on Yellow/100 fails at 3.4:1) |
| Status alert | Red/900 on Red/100 | `#691811` on `#F9DEDC` | 9.5:1 |
| Banding second band | Gray/100 | `#EBEAEA` | wide or long tables only |
| Tab colour: summary/goal | Cobalt/900 | `#181C25` | |
| Tab colour: inputs | Cyan/500 | `#11B5E4` | |
| Tab colour: raw data | Gray/300 | `#B9B6B6` | |
| Tab colour: Read Me | Cobalt/500 | `#384156` | |

Fonts: `Inter` for everything, `Blinker` for the title band only. Both are
Google Fonts; the Sheets API accepts them in `textFormat.fontFamily`, they
render in the browser and are embedded in PDF export (verified 2026-09). The
API does not validate font names: a typo is stored silently and renders as a
fallback, so read back and export once to confirm.

What "subtle" means here: one cobalt band with a cyan rule at the top of
each tab, cyan-tinted inputs, cyan-ink section headings, Inter. No cobalt
fills on headers or data, no cyan text on white, no suit glyphs, no dark
theme. The brand is recognisable at a glance and invisible while reading.

## Applying a style with the API

Order of operations that avoids fighting yourself:

1. Write values and formulas first (`values.batchUpdate` with
   `USER_ENTERED`), numbers as numbers.
2. Clear stale formatting on the touched range once (`repeatCell` with
   `fields: "userEnteredFormat"` and an empty `userEnteredFormat`) when
   rebuilding a tab; otherwise use narrow field masks so untouched
   properties survive.
3. Apply the body baseline to the whole used range (font, size, ink,
   vertical alignment).
4. Apply role styles by range: title row, section headings, header rows,
   numeric columns (format + right align), input cells, link cells, total
   rows, notes cells (`OVERFLOW_CELL` or `WRAP`).
5. Borders: header rule, total rule, body hairlines.
6. Dimensions: column widths by type; title row height; leave body rows at
   default or one uniform value.
7. Sheet properties: frozen rows/columns, gridlines, tab colour.
8. Validation, conditional formats, protection, notes, named ranges.
9. Read back with `includeGridData` and check the format readback list in
   the guide, then export one PDF or screenshot and look at it.

See `sheets-api-recipes.md` for the exact request shapes.
