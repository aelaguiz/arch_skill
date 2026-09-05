---
name: spreadsheet-formatting
description: "Build, restyle, or audit Google Sheets (and Excel) workbooks so a human can read, scan, change and trust them: one-row frozen headers, one line per cell, no merged cells, numbers right and text left, consistent number formats, one documented colour key, and hard-coded values only for inputs and levers with everything else as formulas. Use when the user asks to make a spreadsheet readable, consistent, presentable or user-friendly, to fix freeze panes, paragraphs in cells, hardcoded numbers or inconsistent formatting, to apply a house style through the Sheets API or gws CLI, or to audit a sheet's formatting. Not for choosing the analysis or metrics, data cleaning or statistics, chart or dashboard design outside the grid, or HTML/PDF report styling."
metadata:
  short-description: "Make spreadsheets readable, consistent and formula-driven"
---

# Spreadsheet Formatting

Use this skill when the work is the shape of a spreadsheet a person will
read: layout, freeze panes, text length, alignment, number formats, colour,
fonts, tab structure, and the line between hard-coded inputs and formulas.
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

## Non-negotiables

- Freeze only the row(s) that identify columns (one, at most two) and at
  most one label column. Never freeze a title block. A one-screen summary
  or a multi-table tab freezes nothing.
- Hard-code only inputs and levers. Every other number, date in a series,
  total, share, multiple, and status sentence is a formula. No constants
  inside formulas except obvious unit conversions (12, 24, 1000, 1, 0).
- Levers are numeric cells, one per lever, with a label, unit, validation
  and the input style; never a string like `70% / 20% / 10%`.
- Inputs look like inputs everywhere: distinct font colour plus a light fill
  or border, identical on every tab, documented in a key.
- One line per cell, about 45-90 characters. Longer text becomes label +
  value, one point per row, a Notes column, a cell note, or a Read Me line.
  Text beside a value overflows into empty neighbours; it does not wrap or
  merge.
- Never merge cells. Never clip text on a presentation tab.
- Numbers right, text left, headers aligned like their column. One number
  format and one decimal count per column. Units in the header.
- One header row per table, bold with a thin rule; totals bold with a rule
  above; no dark fills on data headers. One dark brand band is allowed for
  the tab title row only.
- Colour is monochrome plus meaning: inputs, cross-tab links, one alert,
  one highlight. Every text/fill pair at 4.5:1. A word or glyph always
  accompanies a colour.
- Same look for the same thing on every tab: fonts, sizes, formats, column
  purposes, header row, key, tab colours.
- Short formulas, one per row or column, cross-tab ingredients linked into a
  local labelled row first.
- Change the sheet the user named. If they did not authorise edits to a live
  file, work on a copy and say so. Read the grid back after applying and
  look at the result before reporting.

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
   header row per table, notes area, column purposes by letter, freeze rule.
2. **Extract hidden inputs**: every constant in a formula, every typed total,
   every lever-as-text, every typed date series becomes a labelled input
   cell or a formula. Keep the numbers identical; verify the outputs match
   before and after.
3. **Rewrite text**: split paragraphs into label + value rows or notes lines,
   shorten labels, sentence case, units into headers, headers that stand
   alone.
4. **Write values and formulas**, numbers as numbers, `USER_ENTERED`.
5. **Apply the house style by range** in the order given in
   `references/house-style.md`: baseline, roles, borders, dimensions, sheet
   properties, validation, conditional formats, protection, notes.
6. **Verify**: read the grid back and run the readback checklist; recompute
   or eyeball two or three outputs against the original; export or
   screenshot at laptop width; fix anything clipped, tall, mis-aligned or
   still hard-coded.
7. **Report** what changed per tab in the user's terms (frozen rows before
   and after, inputs extracted, cells shortened, formats unified), the file
   and tab links, and any judgment calls.

## Output expectations

- Build or restyle: the sheet itself, plus a short change list per tab and
  the link. Name every input or lever you created and where it lives.
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
  shapes for every style element, gotchas, readback checklist
