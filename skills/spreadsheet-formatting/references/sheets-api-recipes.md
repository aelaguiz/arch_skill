# Sheets API recipes (gws CLI and batchUpdate)

Request shapes for applying the house style with the Google Sheets API v4.
Every JSON block is one element of `{"requests": [...]}` for
`spreadsheets.batchUpdate`. `SHEET_ID` is the numeric `sheetId`, not the tab
name. Indices are zero-based, end-exclusive. Shapes marked verified were
executed live against a scratch sheet in 2026-09.

## Calling through `gws`

```
gws sheets spreadsheets get --params '{"spreadsheetId": ID, "ranges": ["'Tab'!A1:N40"], "includeGridData": true}'
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId": ID}' --json '{"requests": [...]}'
gws sheets spreadsheets values batchUpdate --params '{"spreadsheetId": ID}' --json '{"valueInputOption": "USER_ENTERED", "data": [{"range": "'Tab'!A1", "values": [[...]]}]}'
gws drive files copy --params '{"fileId": ID}' --json '{"name": "[COPY] ..."}'
```

Gotchas that cost time:

- Build the JSON in Python and pass it through `shlex.quote(json.dumps(obj,
  ensure_ascii=False))`. Escaped `\u00b7`-style sequences inside a shell
  string are mangled by the CLI's argument parser; tab names with `·`, `—`
  or quotes only work with `ensure_ascii=False` and proper quoting.
- `gws` prints `Using keyring backend: keyring` on the first line; strip it
  before `json.loads`.
- Work on a copy (`drive files copy`) when the user has not asked for edits
  to the live file; say which file you touched.
- `values.update` with `RAW` stores formulas as text; use `USER_ENTERED`.
- Field masks: `fields` lists exactly the properties you send. A bare
  `"fields": "userEnteredFormat"` resets every unlisted format property on
  the range to default; that is useful once when rebuilding a tab and
  destructive otherwise.
- `padding` requires all four sides in one object.
- `autoResizeDimensions` sizes to content only (45 px for `12.3%`); use it
  as a measurement step and then set widths by column type.
- Fonts are not validated; read back `effectiveFormat.textFormat.fontFamily`
  and export a PDF once if a non-default font matters.
- Merged cells: send `unmergeCells` on the range before restyling.
- `HYPERLINK("#gid=<sheetId>&range=A1","Label")` links inside the workbook.

## Read the current state

```json
{"spreadsheetId": "ID", "ranges": ["'Tab'!A1:N60"], "includeGridData": true,
 "fields": "namedRanges,sheets(properties,merges,bandedRanges,conditionalFormats,protectedRanges,basicFilter,filterViews,rowGroups,columnGroups,data(rowData(values(userEnteredValue,effectiveValue,formattedValue,effectiveFormat,note,hyperlink)),rowMetadata(pixelSize,hiddenByUser,hiddenByFilter),columnMetadata(pixelSize,hiddenByUser,hiddenByFilter)))"}
```
Then list: frozen rows/cols, merges, hidden or grouped rows and columns,
filters, per-cell `formulaValue` (search for digits not in references),
`formattedValue` length, `effectiveFormat` (alignment, wrap, numberFormat,
fonts, fills), column `pixelSize`. Hidden dimensions are part of the
reading surface: a preserved, formatted column the reader cannot see is a
failed deliverable. Unhide with `updateDimensionProperties`
`{"hiddenByUser": false}` and `fields: "hiddenByUser"` when the field is
meant to be read.

## Sheet properties: freeze, gridlines, tab colour (verified)

```json
{"updateSheetProperties": {"properties": {"sheetId": SHEET_ID,
   "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": 1, "hideGridlines": true},
   "tabColorStyle": {"rgbColor": {"red": 0.094, "green": 0.11, "blue": 0.145}}},
  "fields": "gridProperties(frozenRowCount,frozenColumnCount,hideGridlines),tabColorStyle"}}
```

## Move rows or columns so references follow

```json
{"moveDimension": {"source": {"sheetId": SHEET_ID, "dimension": "ROWS", "startIndex": 5, "endIndex": 6}, "destinationIndex": 0}}
{"updateSheetProperties": {"properties": {"sheetId": SHEET_ID, "gridProperties": {"rowCount": 120, "columnCount": 60}}, "fields": "gridProperties(rowCount,columnCount)"}}
```
`moveDimension` keeps every formula, note and hyperlink pointing at the
moved cells; clear-and-rewrite does not. Set `rowCount`/`columnCount`
before writing anything that references cells beyond the current grid: a
reference written past the edge and then shifted by the expansion points
at the wrong row.

## Unmerge and clear a range before rebuilding

```json
{"unmergeCells": {"range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 40, "startColumnIndex": 0, "endColumnIndex": 14}}}
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 40, "startColumnIndex": 0, "endColumnIndex": 14},
  "cell": {"userEnteredFormat": {}}, "fields": "userEnteredFormat"}}
```
Clear values with `values.clear` or an `updateCells` with `fields: "userEnteredValue"` and no rows.

## Body baseline (font, ink, vertical alignment)

```json
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 40, "startColumnIndex": 0, "endColumnIndex": 14},
  "cell": {"userEnteredFormat": {"textFormat": {"fontFamily": "Inter", "fontSize": 10, "bold": false,
      "foregroundColorStyle": {"rgbColor": {"red": 0.094, "green": 0.11, "blue": 0.145}}},
    "verticalAlignment": "MIDDLE", "wrapStrategy": "OVERFLOW_CELL",
    "backgroundColorStyle": {"rgbColor": {"red": 1, "green": 1, "blue": 1}}}},
  "fields": "userEnteredFormat(textFormat,verticalAlignment,wrapStrategy,backgroundColorStyle)"}}
```

## Scrolling table: the identification prefix (spanner + header from row 1)

```json
{"updateCells": {"range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 1},
  "rows": [{"values": [{"userEnteredValue": {"stringValue": "Channel performance · tier-1"}, "userEnteredFormat": {"textFormat": {"bold": true}}}]}],
  "fields": "userEnteredValue,userEnteredFormat.textFormat.bold"}}
{"mergeCells": {"range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 1, "endColumnIndex": 7}, "mergeType": "MERGE_ALL"}}
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 1, "endColumnIndex": 7},
  "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "textFormat": {"bold": true}}}, "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"}}
{"updateSheetProperties": {"properties": {"sheetId": SHEET_ID, "gridProperties": {"frozenRowCount": 2, "frozenColumnCount": 1}}, "fields": "gridProperties(frozenRowCount,frozenColumnCount)"}}
```
Row 1 is the spanner row with the tab identity in A1 and one merged
label per group (centred when the group fits the screen, at its leading
edge when it does not); row 2 is the column-header row (style it with the
header recipe below at `startRowIndex: 1`); freeze through row 2. A table
without groups puts the identity in A1 of the header row and freezes one
row. Nothing else goes above the header: refresh date, source and links go
to the Read Me or a note on A1.

## Title row (row 1) on a non-scrolling tab: band, font, height, cyan rule

```json
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 14},
  "cell": {"userEnteredFormat": {"backgroundColorStyle": {"rgbColor": {"red": 0.094, "green": 0.11, "blue": 0.145}},
    "textFormat": {"fontFamily": "Blinker", "fontSize": 14, "bold": true, "foregroundColorStyle": {"rgbColor": {"red": 0.988, "green": 0.984, "blue": 0.973}}},
    "verticalAlignment": "MIDDLE", "horizontalAlignment": "LEFT", "wrapStrategy": "OVERFLOW_CELL"}},
  "fields": "userEnteredFormat(backgroundColorStyle,textFormat,verticalAlignment,horizontalAlignment,wrapStrategy)"}}
{"updateDimensionProperties": {"range": {"sheetId": SHEET_ID, "dimension": "ROWS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 32}, "fields": "pixelSize"}}
{"updateBorders": {"range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 14},
  "bottom": {"style": "SOLID_MEDIUM", "colorStyle": {"rgbColor": {"red": 0.067, "green": 0.71, "blue": 0.894}}}}}
```
The muted "as of" cell at the right end of row 1 gets a smaller size (9 pt),
`horizontalAlignment: RIGHT`, and a formula such as
`="Refreshed "&TEXT(Inputs!B3,"yyyy-mm-dd")&" · source "&Inputs!B4`.

## Spanner (group header) row: the one sanctioned merge

The scrolling-table recipe above already shows the spanner at row 1 with
the identity in A1 and the freeze through the header. The same merge
serves a local, unfrozen block inside a stacked dashboard: put the spanner
directly above that block's own header row and freeze nothing.

```json
{"mergeCells": {"range": {"sheetId": SHEET_ID, "startRowIndex": 18, "endRowIndex": 19, "startColumnIndex": 2, "endColumnIndex": 4}, "mergeType": "MERGE_ALL"}}
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 18, "endRowIndex": 19, "startColumnIndex": 2, "endColumnIndex": 6},
  "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "textFormat": {"bold": true}}},
  "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"}}
{"updateBorders": {"range": {"sheetId": SHEET_ID, "startRowIndex": 18, "endRowIndex": 19, "startColumnIndex": 2, "endColumnIndex": 4},
  "bottom": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.467, "green": 0.522, "blue": 0.651}}}}}
{"updateDimensionProperties": {"range": {"sheetId": SHEET_ID, "dimension": "COLUMNS", "startIndex": 7, "endIndex": 8}, "properties": {"pixelSize": 12}, "fields": "pixelSize"}}
```
One merge per group, in a spanner row only; the column header row stays
unmerged. Centre the label when the group fits the screen; for a group
wider than the viewport use `"horizontalAlignment": "LEFT"` so the label
sits at the group's leading edge, and name the group in the frozen corner
cell too. The last request is the 12 px seam column between groups
(alternative: a `left` border on the first column of each group).

## Section heading row

```json
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 3, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": 14},
  "cell": {"userEnteredFormat": {"textFormat": {"bold": true, "fontSize": 10, "foregroundColorStyle": {"rgbColor": {"red": 0.035, "green": 0.357, "blue": 0.447}}}}},
  "fields": "userEnteredFormat.textFormat"}}
{"updateBorders": {"range": {"sheetId": SHEET_ID, "startRowIndex": 3, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": 7},
  "bottom": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.804, "green": 0.831, "blue": 0.878}}}}}
```

## Column header row (verified shape; `startRowIndex` is wherever the header row is)

```json
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 5, "endRowIndex": 6, "startColumnIndex": 0, "endColumnIndex": 7},
  "cell": {"userEnteredFormat": {"backgroundColorStyle": {"rgbColor": {"red": 0.922, "green": 0.918, "blue": 0.918}},
    "textFormat": {"bold": true}, "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP"}},
  "fields": "userEnteredFormat(backgroundColorStyle,textFormat.bold,verticalAlignment,wrapStrategy)"}}
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 5, "endRowIndex": 6, "startColumnIndex": 1, "endColumnIndex": 7},
  "cell": {"userEnteredFormat": {"horizontalAlignment": "RIGHT"}}, "fields": "userEnteredFormat.horizontalAlignment"}}
{"updateBorders": {"range": {"sheetId": SHEET_ID, "startRowIndex": 5, "endRowIndex": 6, "startColumnIndex": 0, "endColumnIndex": 7},
  "bottom": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.467, "green": 0.522, "blue": 0.651}}}}}
```
Numeric-column headers right-aligned (second request); the label header stays left.

## Numeric columns: format + alignment (verified)

```json
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 6, "endRowIndex": 9, "startColumnIndex": 1, "endColumnIndex": 3},
  "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}, "horizontalAlignment": "RIGHT"}},
  "fields": "userEnteredFormat(numberFormat,horizontalAlignment)"}}
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 6, "endRowIndex": 9, "startColumnIndex": 3, "endColumnIndex": 4},
  "cell": {"userEnteredFormat": {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}, "horizontalAlignment": "RIGHT"}},
  "fields": "userEnteredFormat(numberFormat,horizontalAlignment)"}}
```
Pattern cheat-sheet: `#,##0` count; `#,##0;(#,##0);"–"` finance; `$#,##0`
money; `0.0%` percent; `0.00"x"` multiple; `#,##0"×"` large multiple;
`#,##0,` thousands; `0.0,,"M"` millions; `yyyy-mm-dd` date; `mmm yyyy`
month header; `0.0000` factor.

## Input and lever cells

```json
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 4, "endRowIndex": 8, "startColumnIndex": 1, "endColumnIndex": 2},
  "cell": {"userEnteredFormat": {"backgroundColorStyle": {"rgbColor": {"red": 0.851, "green": 0.961, "blue": 0.988}},
    "textFormat": {"foregroundColorStyle": {"rgbColor": {"red": 0.161, "green": 0.29, "blue": 0.792}}},
    "borders": {"top": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.804, "green": 0.831, "blue": 0.878}}},
                "bottom": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.804, "green": 0.831, "blue": 0.878}}},
                "left": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.804, "green": 0.831, "blue": 0.878}}},
                "right": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.804, "green": 0.831, "blue": 0.878}}}}}},
  "fields": "userEnteredFormat(backgroundColorStyle,textFormat.foregroundColorStyle,borders)"}}
{"setDataValidation": {"range": {"sheetId": SHEET_ID, "startRowIndex": 4, "endRowIndex": 5, "startColumnIndex": 1, "endColumnIndex": 2},
  "rule": {"condition": {"type": "NUMBER_BETWEEN", "values": [{"userEnteredValue": "0"}, {"userEnteredValue": "1"}]},
    "inputMessage": "Capture rate as a decimal between 0 and 1", "strict": true}}}
{"setDataValidation": {"range": {"sheetId": SHEET_ID, "startRowIndex": 5, "endRowIndex": 6, "startColumnIndex": 1, "endColumnIndex": 2},
  "rule": {"condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": "Low"}, {"userEnteredValue": "Base"}, {"userEnteredValue": "High"}]},
    "inputMessage": "Scenario", "strict": true, "showCustomUi": true}}}
```

## Cross-tab link cells (green ink)

```json
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 10, "endRowIndex": 14, "startColumnIndex": 1, "endColumnIndex": 2},
  "cell": {"userEnteredFormat": {"textFormat": {"foregroundColorStyle": {"rgbColor": {"red": 0.09, "green": 0.392, "blue": 0.129}}}}},
  "fields": "userEnteredFormat.textFormat.foregroundColorStyle"}}
```

## Notes beside values: overflow, not wrap, not merge

```json
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 10, "endRowIndex": 14, "startColumnIndex": 2, "endColumnIndex": 3},
  "cell": {"userEnteredFormat": {"wrapStrategy": "OVERFLOW_CELL", "horizontalAlignment": "LEFT",
    "textFormat": {"foregroundColorStyle": {"rgbColor": {"red": 0.318, "green": 0.365, "blue": 0.482}}}}},
  "fields": "userEnteredFormat(wrapStrategy,horizontalAlignment,textFormat.foregroundColorStyle)"}}
```
Cells to the right must be empty for overflow to show. For a dedicated wide
Notes column use `"wrapStrategy": "WRAP", "verticalAlignment": "TOP"` and keep
strings under two lines at the column width.

## Cell note for provenance

```json
{"updateCells": {"range": {"sheetId": SHEET_ID, "startRowIndex": 4, "endRowIndex": 5, "startColumnIndex": 1, "endColumnIndex": 2},
  "rows": [{"values": [{"note": "Source: AHREFS-KW-2026-09-04, US monthly volume."}]}], "fields": "note"}}
```

## Total row, body hairlines, banding

```json
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 20, "endRowIndex": 21, "startColumnIndex": 0, "endColumnIndex": 7},
  "cell": {"userEnteredFormat": {"textFormat": {"bold": true}}}, "fields": "userEnteredFormat.textFormat.bold"}}
{"updateBorders": {"range": {"sheetId": SHEET_ID, "startRowIndex": 20, "endRowIndex": 21, "startColumnIndex": 0, "endColumnIndex": 7},
  "top": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.22, "green": 0.255, "blue": 0.337}}}}}
{"updateBorders": {"range": {"sheetId": SHEET_ID, "startRowIndex": 6, "endRowIndex": 20, "startColumnIndex": 0, "endColumnIndex": 7},
  "innerHorizontal": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.804, "green": 0.831, "blue": 0.878}}}}}
{"addBanding": {"bandedRange": {"range": {"sheetId": SHEET_ID, "startRowIndex": 5, "endRowIndex": 200, "startColumnIndex": 0, "endColumnIndex": 9},
  "rowProperties": {"headerColorStyle": {"rgbColor": {"red": 0.922, "green": 0.918, "blue": 0.918}},
    "firstBandColorStyle": {"rgbColor": {"red": 1, "green": 1, "blue": 1}},
    "secondBandColorStyle": {"rgbColor": {"red": 0.922, "green": 0.918, "blue": 0.918}}}}}}
```
Banded ranges may not overlap; the reply carries `bandedRangeId` for later
`deleteBanding`.

## Column widths and row heights

```json
{"updateDimensionProperties": {"range": {"sheetId": SHEET_ID, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 280}, "fields": "pixelSize"}}
{"updateDimensionProperties": {"range": {"sheetId": SHEET_ID, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 7}, "properties": {"pixelSize": 120}, "fields": "pixelSize"}}
{"updateDimensionProperties": {"range": {"sheetId": SHEET_ID, "dimension": "ROWS", "startIndex": 1, "endIndex": 40}, "properties": {"pixelSize": 22}, "fields": "pixelSize"}}
```

## Status via conditional format (text carries the meaning)

```json
{"addConditionalFormatRule": {"index": 0, "rule": {
  "ranges": [{"sheetId": SHEET_ID, "startRowIndex": 26, "endRowIndex": 27, "startColumnIndex": 1, "endColumnIndex": 4}],
  "booleanRule": {"condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "below"}]},
    "format": {"backgroundColorStyle": {"rgbColor": {"red": 0.976, "green": 0.871, "blue": 0.863}},
               "textFormat": {"foregroundColorStyle": {"rgbColor": {"red": 0.412, "green": 0.094, "blue": 0.067}}}}}}}}
{"addConditionalFormatRule": {"index": 1, "rule": {
  "ranges": [{"sheetId": SHEET_ID, "startRowIndex": 26, "endRowIndex": 27, "startColumnIndex": 1, "endColumnIndex": 4}],
  "booleanRule": {"condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "OK"}]},
    "format": {"backgroundColorStyle": {"rgbColor": {"red": 0.871, "green": 0.969, "blue": 0.882}},
               "textFormat": {"foregroundColorStyle": {"rgbColor": {"red": 0.059, "green": 0.263, "blue": 0.086}}}}}}}}
```
Rules evaluate in index order; first true wins. Keep ranges bounded.

## Protection and named ranges (verified)

```json
{"addProtectedRange": {"protectedRange": {"range": {"sheetId": SHEET_ID, "startRowIndex": 9, "endRowIndex": 40, "startColumnIndex": 0, "endColumnIndex": 14},
  "description": "Formulas. Change the inputs block instead.", "warningOnly": true}}}
{"addNamedRange": {"namedRange": {"name": "lever_growth_multiplier",
  "range": {"sheetId": SHEET_ID, "startRowIndex": 4, "endRowIndex": 5, "startColumnIndex": 1, "endColumnIndex": 2}}}}
```

## Room: row height and padding for a tab that is read

```json
{"updateDimensionProperties": {"range": {"sheetId": SHEET_ID, "dimension": "ROWS", "startIndex": 1, "endIndex": 60}, "properties": {"pixelSize": 28}, "fields": "pixelSize"}}
{"repeatCell": {"range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 60, "startColumnIndex": 0, "endColumnIndex": 14},
  "cell": {"userEnteredFormat": {"padding": {"top": 4, "right": 8, "bottom": 4, "left": 8}, "verticalAlignment": "MIDDLE"}},
  "fields": "userEnteredFormat(padding,verticalAlignment)"}}
```

## Look, then read back

Look the way the reader looks: in the browser. Apply the installed
`$browseros` skill contract, then open one background tab on
`https://docs.google.com/spreadsheets/d/<id>/edit?gid=<sheetId>#gid=<sheetId>`
(`tabs` action `new`, `hidden=false`, `background=true`), `wait` for the
title text, `screenshot` the page, save the image, and `close` the tab when
the round is over. Scroll (`act` or `evaluate`) and screenshot again for
tabs taller or wider than a screen. The screenshot `size` option scales
the image; it does not change the viewport. Measure the viewport with
`evaluate` (`window.innerWidth`) and state what width the proof
represents. Typing an address in the name box selects a cell but does not
scroll frozen panes; a selected cell with a note shows its tooltip over the
grid, so select a plain cell before capturing. That is the only view that shows
clipping, collisions between overflowing strings, wallpaper colour, real
fonts and cramped rows the way a person sees them. PDF export
(`gws drive files export`, `mimeType: application/pdf`) is a print check;
large workbooks refuse it (`This file is too large to be exported`) and it
does not show frozen panes or on-screen widths.

Then fetch the grid and check:

- `frozenRowCount` covers only header rows (spanner + header at most),
  `frozenColumnCount <= 1`; `merges` only in a spanner row; A1 non-empty.
- Fit: for each text cell whose right neighbour is non-empty, estimate the
  rendered width (roughly 6-7 px per character at 10 pt Inter/Arial, plus
  padding) against `columnMetadata[].pixelSize`; every hit is a cell to
  look at on the render. Labels running past the label column and any
  `formattedValue` over about 90 characters outside a Notes column are
  findings.
- Every cell with an `effectiveValue.numberValue` is right-aligned with a
  `numberFormat`; one format per type axis (column, or row in a transposed
  table); no `wrapStrategy: CLIP`.
- Signal budget: count cells with a non-white fill and cells with bold; a
  filled or bold column, row or block, or one record's caveat restated in
  every row, means the state is wallpaper. The same status across many
  records in a tracker is data.
- Every formula read for hidden assumptions: a digit that is not a
  reference is a candidate, its purpose decides (unit conversion, 0/1,
  precision, offset and link ids are syntax). Every literal number has an
  owner: observations plain with a named source, assumptions in the input
  style, nothing derived left typed.
- Every original output matches the saved dump and no formula on or around
  the tab has acquired a new error (`effectiveValue.errorValue`);
  pre-existing errors are reported separately, not repaired by a
  formatting pass.
- Blanks inside a numeric block show the workbook's "no value" mark through
  a format or presentation formula; source-owned blanks that formulas test
  or a sync writer fills are left as they are.
- Fonts and colours as intended (the API does not validate font names).

Fix, screenshot again, look again.
