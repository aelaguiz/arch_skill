---
name: spreadsheet-formatting
description: "Build, restyle, or audit Google Sheets (and Excel) workbooks so a human can read, scan, change and trust them: header-only frozen rows, one line per cell, merges only for group headers, numbers right and text left, consistent number formats, one documented colour key, and every number owned: observations shown as data, assumptions styled as inputs, everything derived as formulas. Use when the user asks to make a spreadsheet readable, consistent, presentable or user-friendly, to fix freeze panes, paragraphs in cells, hardcoded numbers or inconsistent formatting, to apply a house style through the Sheets API or gws CLI, or to audit a sheet's formatting. Not for choosing the analysis or metrics, data cleaning or statistics, chart or dashboard design outside the grid, or HTML/PDF report styling."
metadata:
  short-description: "Make spreadsheets readable, consistent and formula-driven"
---

# Spreadsheet Formatting

Use this skill when the work is the shape of a spreadsheet a person will
read: layout, freeze panes, text length, alignment, number formats, colour,
fonts, tab structure, and who owns each number (observation, assumption, or formula).
The data stays exactly as rich as it was; only its presentation changes.

The reader's complaints this skill exists to end: five frozen rows eating the
screen, paragraphs typed into single cells, formatting that differs from tab
to tab, and numbers hard-coded where a formula belongs.

This is a prompt-only skill. It ships doctrine, a concrete house style, and
API request shapes; it ships no scripts or runners.

## When to use

- The user wants a new spreadsheet or tab built for a human reader.
- The user wants an existing sheet made readable, consistent, presentable,
  "user-friendly", or brought to a house style.
- The user complains about freeze panes, merged cells, long text in cells,
  centred numbers, mixed decimals, colours without a key, or hard-coded
  numbers inside formulas.
- The user wants a formatting audit of a sheet with findings and fixes.
- Another workflow produced a sheet (analysis export, model, tracker) and
  the deliverable now needs to be consumable.

## When not to use

- The question is what to measure, how to analyse it, or whether the numbers
  are right. Do the analysis first; bring the result here.
- The deliverable is a chart image, an HTML or PDF report, or a slide; use
  the report or design skill for that surface.
- The task is data cleaning, deduplication, or import plumbing with no
  reader-facing layout.
- The user wants Excel VBA or Apps Script automation as the product.

## How to think

The rules are consequences of how a person reads a grid; when a case is not
covered, reason from these (section 0 of the guide expands each one):

- A cell is a window: content fits it or is not cell content.
- A row is a record and a column is a type; in a transposed table the row
  carries the type. Align and format by whichever axis carries the type.
- Structure comes from position and space; rules, fills and bold are last
  resorts.
- Colour is a signal with a budget: show a state once, with a word.
- Repetition is noise when it restates one fact; the same status in many
  records is data.
- Summaries, templates and checks inherit the conditions of the principle
  they illustrate; none of them turns a contextual rule into an
  unconditional command.
- Whitespace is reading room; typing defaults are too tight for reading.
- Every number has an owner: an observation (a fact from outside) may be a
  literal shown as data; an assumption (a lever) is a literal in the input
  style; anything derived is a formula. Ownership is about who is entitled
  to choose the value, not about what depends on it. A constant inside a
  formula is a hidden assumption; a structural numeral is syntax.
- Decide what the reader compares (entity, period, measure, population)
  before deciding widths, aliases or where evidence goes.
- The API is not the reader; only the rendered tab is.

## Non-negotiables

- Freeze an axis, not a document category: only the rows that identify
  columns (a spanner row plus the header row at most) and at most one label
  column. Frozen rows are a prefix from row 1, so on a scrolling table the
  identification area starts at row 1 and the tab identity lives in its
  corner cell; never freeze a title block. Stacked sections that share one
  column axis share that one frozen prefix; unrelated tables on one tab get
  local header rows and nothing frozen; a tab that fits one screen freezes
  nothing.
- Classify every literal by owner before changing it. Observations (synced
  data, pulled totals, reported rates and their evidence) stay literal and
  plain, with their source named once; do not relocate them into a fake
  inputs table or paint them as levers, and do not re-derive a reported
  value from rounded evidence. Assumptions are literals in the input style,
  once each, with unit and validation over the actual choice domain (a
  number, a date or a category), never several choices packed into one
  string like `70% / 20% / 10%`. Everything derived is a formula, including dates in a
  series, totals whose components are present, shares, multiples and
  status sentences. A constant inside a formula is an assumption to
  extract unless it is syntax (unit conversions, 0 and 1, a precision, an
  offset, a link id): meaning decides, not the numeral.
- Assumptions look like assumptions everywhere: distinct font colour plus a
  light fill or border, identical on every tab, documented in a key.
- One idea per cell, and the cell fits its window. Labels are names, not
  definitions; definitions and provenance go to a Notes column, a note on
  the owning label or header, or the Read Me, somewhere discoverable from
  where the reader is. Caveats that change how a value should be read
  (provisional, to-date, small sample) stay visible beside the value or its
  group. Section rows hold a heading only. Overflow is for a short note
  beside a value, never for prose. Never clip on a presentation tab. A note
  on every cell is texture, not information.
- Never merge cells in a data range or in the column-header row. The one
  sanctioned merge is a group header (spanner) in its own row above the
  column headers: centred when the group fits the screen, placed at the
  group's leading edge with the group named in the frozen corner when it
  does not.
- Numbers right, text left, headers aligned like their column; IDs are
  text. One format and one decimal count per type axis. Units in the
  header. One display mark for "no value", applied through formats or the
  presentation formula, never by overwriting blanks that formulas or a
  sync writer depend on.
- One header row per table, bold with a thin rule; totals bold with a rule
  above; no vertical borders except a light seam between column groups, no
  full grids, no dark fills on data headers.
  One dark brand band is allowed for the tab title row only. A1 holds the
  title.
- Colour is monochrome plus meaning: inputs, cross-tab links, one alert,
  one highlight. A state is shown once with a word where one fact is being
  stated; never a whole column, row or block painted, never bold as a
  state. Every text/fill pair at 4.5:1.
- Same look for the same thing on every tab: fonts, sizes, formats, column
  roles, header row, key, tab colours.
- Short formulas, one per row or column, cross-tab ingredients linked into a
  local labelled row first.
- Change the sheet the user named. If they did not authorise edits to a live
  file, work on a copy and say so.
- A restyle preserves the workbook's reference contract: know who reads and
  writes the addresses you move, prefer native moves over clear-and-rewrite,
  expand the grid before writing past it, and prove that every formula on
  and around the tab still evaluates and every original output still
  matches. Wide tables are read by scrolling; keep identity recoverable at
  every position and look at more than the top-left.
- A field the reader cannot find is not delivered: hidden or grouped
  columns, filters and collapsed groups are part of the reading surface and
  of the baseline.
- Nothing is done until you have looked at the tab the way the reader will:
  open it in the browser through `$browseros` (one background tab on the
  sheet URL with its `gid`, `screenshot`, close the tab when done) and read
  it as a stranger. Formatting that has not been looked at has not been
  formatted. PDF export is a print check, not a substitute.

## First move

1. Read `references/formatting-guide.md` section 1 (the ten laws) and skim
   the section that matches the complaint. Read `references/house-style.md`
   for the concrete spec, including the brand adaptation if the user or
   workbook has one.
2. Inspect the target: pull the grid with `includeGridData` (see
   `references/sheets-api-recipes.md`) and list the defects by severity: hidden
   inputs, merges, frozen banner, long cells, alignment and format drift,
   missing key.
3. Decide the layout template (single-table detail tab, small model or
   dashboard tab, inputs tab, raw data tab) and where inputs will live.
4. Decide scope with the user's words: a whole workbook, named tabs, or a
   copy for demonstration.

## Workflow

1. **Plan the tab** on paper before writing: title row, inputs block, one
   header row per table (plus a spanner row for grouped columns),
   notes area, one role per column letter, widths decided against the
   longest real content, freeze rule, and the room the tab needs (row
   height, padding, blank rows between blocks).
2. **Classify and extract**: decide the owner of every literal
   (observation, assumption, derived). Extract assumptions hiding in
   formulas, turn typed derived values (date series, totals with present
   components, shares, status text) into formulas, leave observations as
   plain data with a named source. Save a grid dump first; keep the numbers
   identical and verify every output matches before and after.
3. **Rewrite text**: split paragraphs into label + value rows or notes lines,
   shorten labels, sentence case, units into headers, headers that stand
   alone.
4. **Write values and formulas**, numbers as numbers, `USER_ENTERED`.
5. **Apply the house style by range** in the order given in
   `references/house-style.md`: baseline, roles, borders, dimensions, sheet
   properties, validation, conditional formats, protection, notes.
6. **Look, then verify**: open the tab in BrowserOS (`$browseros`),
   screenshot it, and read it at laptop width for anything cut off,
   spilling, colliding, repeated, loud or cramped; then read the grid back and run the readback checklist
   (fit, alignment, formats, constants, input style, signal budget);
   recompute or eyeball two or three outputs against the original. Fix and
   look again. Do not report done on the strength of a successful API call.
7. **Report** what changed per tab in the user's terms (frozen rows before
   and after, inputs extracted, cells shortened, formats unified), the file
   and tab links, and any judgment calls.

## Output expectations

- Build or restyle: the sheet itself, plus a short change list per tab and
  the link. Name every assumption cell you created or extracted and where it lives.
- Audit: findings first, ordered P0 to P3 with the cell ranges, then the
  fix plan; do not restyle unless asked.
- Never trade data for tidiness: if a value or column would be lost, keep it
  and move it to a better place.

## Reference map

- `references/formatting-guide.md` - the full doctrine with reasons,
  numbers, sources, and resolved disagreements
- `references/house-style.md` - the concrete default spec, layout templates,
  brand adaptation (Poker Skill tokens as the worked example), apply order
- `references/sheets-api-recipes.md` - gws invocation, batchUpdate request
  shapes for every style element, gotchas, how to look (BrowserOS) and the
  readback checklist
- `$browseros` (installed sibling skill) - the browser contract for opening
  the sheet and taking the screenshot you judge by
