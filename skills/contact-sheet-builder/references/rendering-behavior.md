# Rendering Behavior

This reference owns the stable rendering details for
`scripts/build_contact_sheet.py`. Keep it short; the skill should remain a
convenience tool, not a layout framework.

## Default output and canvas

Without `--out`, the script creates a unique run directory:

```text
/tmp/contact-sheet-builder/<UTC-timestamp>/
```

For one page:

```text
contact_sheet.png
manifest.json
```

For multiple pages:

```text
contact_sheet_page_001.png
contact_sheet_page_002.png
manifest.json
```

If `--out foo.png` is explicit, one page writes `foo.png`. Multiple pages write
`foo_page_001.png`, `foo_page_002.png`, and `foo.manifest.json`.

If `--out some-dir` is a directory or path without a suffix, outputs are placed
inside that directory with the default page names.

Existing outputs block unless `--force` is present.

Default rendering uses a dynamic image-first canvas. The script sizes the sheet
around the images instead of forcing them into a fixed page. It keeps thumbnails
near native size, only shrinking images that exceed `--max-thumb-width` or
`--max-thumb-height`. Default max thumbnail size is `2048x2048`.

Dynamic mode uses `0px` outside margin, `2px` gutters, compact label rows, and
no card boxes around each image. This is the convenience default because contact
sheets are usually for comparing images, not for printing a page. Use
`--margin` and `--gutter` only when the user asks for more breathing room or an
even tighter sheet.

Use `--page-width` and/or `--page-height` only when the user asks for a fixed
page-style overview. Missing fixed-page dimensions default to `2048x2560`.

## Preview opening

After a successful build, the script opens generated sheet PNGs in macOS Preview
by default:

```bash
open -a Preview <generated-pages>
```

Use `--no-open` when running headless, in batches, or when the user asks not to
open the sheet. Preview open failures do not fail the build; the script prints a
warning and records the preview status in the manifest.

## Input handling

The script accepts files, folders, and globs. Folder reads are non-recursive by
default. Use `--recursive` only when the user asks for recursive/all images.

Folder inputs are sorted by natural path order, hidden files are skipped by
default, and common Pillow-readable image formats are accepted. Non-image or
broken files are skipped with warnings. The script still succeeds when at least
one usable image remains.

## Columns

`--columns auto` uses:

```text
n=1       -> 1 column
n=2       -> 2 columns
n=3..4    -> 2 columns
n=5..6    -> 3 columns
n>=7      -> 4 columns
```

Explicit column counts always win.

## Page and cell layout

Default canvas size is dynamic. In dynamic mode, each output PNG can be wider or
taller than `2048x2560` when that lets the images stay readable.

Thumbnails preserve aspect ratio and use contain-fit. The script does not crop
by default. Dynamic mode starts a new page when the next row would exceed
`--max-page-height`. Fixed-page mode starts a new page when the next row would
overflow the fixed page height.

Spacing is intentionally minimal in dynamic mode. The renderer should not add a
page-like border, card padding, or decorative empty space unless the user asks
for it.

Transparent images are composited over a checkerboard inside the image box so
alpha is visible. The sheet background stays neutral unless `--bg` says
otherwise.

## Labels

Labels are on by default.

Default label source is filename stem. The script replaces `_` and `-` with
spaces, trims repeated whitespace, wraps to at most two lines, and ellipsizes
when text still does not fit. `--label-max` defaults to `32`.

Duplicate labels get parent-folder context only for the colliding labels.

Exact labels can be passed with `--labels` or `--labels-file`. The number of
explicit labels must match the number of usable images.

## Stdout and manifest

Stdout is a prompt fragment, not a debug console. The first line is enough for
the agent to report success:

```text
OK contact_sheet pages=3 images=42 skipped=2 labels=on columns=4 preview=opened out=/tmp/contact-sheet-builder/20260515T220000Z/contact_sheet_page_001.png manifest=/tmp/contact-sheet-builder/20260515T220000Z/manifest.json
```

Warnings are capped in stdout. Full details live in `manifest.json`.

The manifest contains the command, page paths, layout mode, canvas dimensions,
preview status, image paths, labels, dimensions, skipped inputs, and Pillow
version.

## Python environment

The renderer uses Pillow. Invoke it directly with the `python3` that has Pillow
installed, or with the executable script path after install. Avoid nested shell
wrappers that may resolve a different Python environment.

Preflight:

```bash
python3 -c "import PIL; print(PIL.__version__)"
```

## Exit codes

```text
0  success, including success with skipped inputs
2  no usable images
3  output exists and --force was not provided
4  invalid option conflict
```

For exit `2`, tell the user no usable images were found and include the top
reason. For exit `3`, ask once whether to overwrite or choose a new path.
