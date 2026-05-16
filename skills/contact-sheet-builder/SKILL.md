---
name: contact-sheet-builder
description: "Build local contact sheet images from existing image files, folders, globs, or attached local image paths. Use when the user asks to make, label, compare, paginate, or adjust a grid/contact sheet of screenshots, renders, before/after shots, visual candidates, or image folders. Defaults to a labeled, dense, near-native, edge-to-edge sheet and opens it in Preview on macOS without questions. Not for generating or editing images, video/GIF extraction, Figma boards, slide/doc layouts, provider APIs, or theme-specific generation workflows."
metadata:
  short-description: "Build quick labeled contact sheets from local images"
---

# Contact Sheet Builder

Use this skill to quickly arrange existing local images into a useful contact
sheet. The default is intentionally low-friction: build a labeled sheet, choose
a dense image-first grid with almost no whitespace, open it in Preview, write it to a safe temp
directory, and return the path.

The skill is prompt-first, but it ships one script because image decoding,
grid math, pagination, transparency handling, and overwrite safety are
deterministic rendering work.

## When to use

- "Make a contact sheet from these images."
- "Show this folder of renders in a grid."
- "Compare these before and after shots."
- "Make the same sheet but no labels."
- "Use 4 columns and shorter labels."
- "Split this into pages."

## When not to use

- The user wants to generate new images or variants.
- The user wants to edit, retouch, crop, or transform image content.
- The target artifact is a Figma board, slide deck, Google Doc, PDF, or app
  gallery.
- The input is video or GIF frame extraction.
- The request belongs to a theme-specific generation workflow, such as
  `theme_builder` creating generated chair/theme sheets.
- The task requires a provider API or media-generation service.

## Non-negotiables

- Do not ask setup questions when the defaults are enough.
- Prioritize image size and comparison clarity over page-like whitespace.
- In dynamic mode, pack images edge-to-edge: no outside margin and only a tiny
  separator unless the user asks for more space.
- Default to labels on.
- Preserve image aspect ratios and contain-fit thumbnails by default.
- Use a dynamic canvas by default, with no outside margin, `2px` gutters, and
  no card boxes.
- Write outputs outside the source repo unless the user names an output path.
- Open generated sheets in macOS Preview by default when available.
- Do not overwrite existing files unless the user explicitly said overwrite or
  replace.
- Treat before/after pairing as agent judgment. The script should not guess
  semantic relationships from filenames.
- Keep the user reply short: output path, image count, page count, skipped
  count, and manifest path when useful.

## First move

1. Resolve the user's inputs: image files, folders, globs, or attached local
   image paths.
2. If the request names layout changes, map them to script flags directly.
3. Run `scripts/build_contact_sheet.py`.
4. Read the one-line result and warnings.
5. Reply with the contact sheet path and any important skipped-input note.

Only ask the user when there are zero usable images, an explicit output path
already exists without overwrite permission, or the instruction is genuinely
contradictory.

## Common mappings

```text
"no labels"                 -> --no-labels
"use full filenames"        -> --labels-from filename
"use parent folder names"   -> --labels-from parent
"make it 3 columns"         -> --columns 3
"stack them"                -> --columns 1
"before and after"          -> order inputs, use --columns 2, pass labels if clear
"native size"               -> keep dynamic defaults; raise --max-thumb-* if needed
"make a page"               -> use --page-width and --page-height
"white background"          -> --bg white
"black background"          -> --bg black
"title it X"                -> --title X
"do not open it"            -> --no-open
"add more breathing room"   -> --margin 16 --gutter 8
"edge to edge"              -> keep dynamic defaults, or use --margin 0 --gutter 0
"overwrite" or "replace"    -> --force
```

## Script use

From the skill directory:

```bash
python3 scripts/build_contact_sheet.py PATH [PATH ...]
```

Invoke the script directly with `python3` or with the executable script path.
Avoid wrapping it in another shell unless you know that shell resolves the same
Python environment. If Pillow is missing, run a quick preflight with:

```bash
python3 -c "import PIL; print(PIL.__version__)"
```

Useful flags:

```text
--out PATH_OR_DIR
--columns auto|N
--no-labels
--labels-from stem|filename|parent|index
--labels CSV
--labels-file PATH
--label-max N
--margin N
--gutter N
--title TEXT
--page-width N
--page-height N
--max-thumb-width N
--max-thumb-height N
--max-page-height N
--bg neutral|white|black|checker|#RRGGBB
--recursive
--no-open
--force
```

Defaults:

- output root: `/tmp/contact-sheet-builder/<UTC-timestamp>/`
- canvas: dynamic, image-first, usually near native resolution
- format: PNG
- columns: `auto`
- labels: on, filename stem, 32 characters max
- margins/gutters: dynamic mode uses `0px` outside margin and `2px` gutters
- open in Preview: on by default on macOS
- manifest: always written beside the output

Use `--page-width 2048 --page-height 2560` when the user explicitly wants a
fixed page-style overview.

Read `references/rendering-behavior.md` only when you need exact layout,
pagination, label, or exit-code rules.

## Output expectations

The script prints a compact result, for example:

```text
OK contact_sheet pages=2 images=28 skipped=1 labels=on columns=4 preview=opened out=/tmp/contact-sheet-builder/20260515T220000Z/contact_sheet_page_001.png manifest=/tmp/contact-sheet-builder/20260515T220000Z/manifest.json
warning: skipped notes.txt (unsupported file type)
```

User-facing response:

```text
Built a labeled contact sheet: /tmp/contact-sheet-builder/20260515T220000Z/contact_sheet_page_001.png
Opened in Preview. 28 images, 2 pages, 1 skipped. Manifest: /tmp/contact-sheet-builder/20260515T220000Z/manifest.json
```

Do not paste the manifest unless the user asks for details.

## Reference map

- `references/rendering-behavior.md` - exact defaults, pagination, labels,
  stdout, manifest, and exit codes
- `scripts/build_contact_sheet.py` - deterministic Pillow renderer
