# Adaptive Contact Sheet Builder Skill Plan

Date: 2026-05-15
Status: plan only. Do not build the skill package until explicitly asked.
Target repo for future package: `/Users/aelaguiz/workspace/arch_skill`
Example source repo reviewed: `/Users/aelaguiz/workspace/lessons_studio/psmobile`

## Request

Design a new prompt/skill for quickly making contact sheets from local images.
It should accept almost any practical number of images, choose reasonable grids,
default to labels, allow unlabeled output, and accept plain-English changes
without turning into an interview.

The main goal is convenience: throw image paths, folders, globs, or attached
image paths at the skill and get a useful sheet to look at quickly.

## Source Work

This plan was written after reading the relevant authoring doctrine and running
the requested model-consensus pass:

- `$skill-authoring`
- `$prompt-authoring`
- `$doctrine-learn`
- `$model-consensus`

Consensus participants:

- Model A: `opus 4.7 xhigh`, run through Claude CLI as `claude-opus-4-7`
- Model B: `gpt 5.5 xhigh`, run through Codex CLI as `gpt-5.5`

Consensus artifacts are under:

`/Users/aelaguiz/workspace/arch_skill/.arch_skill/model-consensus/adaptive-contact-sheet-builder-20260515T215902Z/`

Both models converged on the same core design: prompt-first skill, one local
Python/Pillow renderer script, no orchestration layer, no image generation, and
safe default output.

## Local Grounding

The psmobile example path exists at:

`/Users/aelaguiz/workspace/lessons_studio/psmobile/skills/theme_builder/experiments`

That folder contains many generated and comparative image artifacts. Examples
reviewed include:

- `skills/theme_builder/experiments/lighting_and_shadows/2026-05-15_shadow_pass_demo_pink_bob_right_45_v2/overview_shadow_passes_v2.png`
- `skills/theme_builder/experiments/beach_sample_path_0/2026-05-14_beach_chair_contact_sheet_v2/output/output.png`
- `skills/theme_builder/experiments/character_reference_experiments/2026-05-15_opponent_reference_style_normalize_silver_hair_green_dress_v2_text_identity/output/opponent_reference_sheet.png`

The existing `theme_builder` skill has a chair/theme contact-sheet step, but it
is not the same thing as this proposed skill. `theme_builder` belongs to
theme-specific image generation workflows. The new skill should only arrange
existing local images into sheets.

Machine prerequisites observed:

- `python3`: 3.14.4
- Pillow: 12.2.0
- ImageMagick `magick`: 7.1.2-21

Future implementation should depend only on Python plus Pillow in the shipped
runtime. ImageMagick is useful for validation, but should not be required for
the skill to run.

## Skill Name

Recommended slug:

`contact-sheet-builder`

Human name:

`Adaptive Contact Sheet Builder`

## Trigger

Use when the user wants to build a local contact sheet from existing image
files, folders, globs, or attached image paths.

Typical asks:

- "make a contact sheet from these"
- "show me these renders in a grid"
- "compare these before and after shots"
- "make this folder into a labeled sheet"
- "same but no labels"
- "make it 4 columns"
- "split this into pages"
- "make the labels shorter"

Do not use for:

- generating new images
- editing image content
- Figma boards
- slides/docs layout
- video or GIF contact sheets
- theme-specific generation flows like `theme_builder`
- provider-specific media APIs

## Package Shape

Recommended future package:

```text
skills/contact-sheet-builder/
  SKILL.md
  scripts/build_contact_sheet.py
  references/rendering-behavior.md
```

`references/rendering-behavior.md` should stay short. It is not a cookbook. It
should only hold stable rendering rules that would otherwise bloat `SKILL.md`:
defaults, label rules, pagination, exit codes, and font fallback.

If the final `SKILL.md` remains compact, the reference file can be folded into
`SKILL.md` and omitted from v1.

## Design Principle

The skill should behave like a convenience tool, not a workflow gate.

Default behavior:

1. Resolve the image inputs.
2. Choose a dense image-first layout.
3. Render the sheet.
4. Return the output path, image count, page count, and any skipped inputs.

Ask the user only when the skill cannot make a reasonable safe choice, such as
zero usable images or an output collision without overwrite permission.

## Prompt Contract

The skill prompt should make these roles clear:

- The agent interprets the user's plain-English request.
- The script renders pixels.
- The script should not guess semantic relationships like before/after pairs.
- The agent may order inputs, choose labels, choose columns, or add a title
  based on the user's request.
- The agent should not ask setup questions when defaults are enough.

Recommended `SKILL.md` sections:

1. Trigger
2. Quick behavior
3. Input resolution
4. Defaults
5. Plain-English changes
6. Script contract
7. Output receipt
8. Edge cases
9. Anti-cases

## Script Contract

Future script:

`scripts/build_contact_sheet.py`

Recommended CLI:

```bash
python3 scripts/build_contact_sheet.py PATH [PATH ...] \
  --out PATH_OR_DIR \
  --columns auto \
  --labels-from stem \
  --label-max 32
```

Recommended flags:

```text
PATH [PATH ...]                 Files, folders, or globs already expanded by the shell.
--out PATH_OR_DIR               Optional. Defaults to a unique temp run directory.
--columns auto|N                Default: auto.
--no-labels                     Turn labels off.
--labels-from stem|filename|parent|index
--labels CSV                    Optional exact labels, one per input.
--labels-file PATH              Optional exact labels from a text file, one per line.
--label-max N                   Default: 32.
--margin N                      Optional outer margin override; dynamic default 0.
--gutter N                      Optional cell gap override; dynamic default 2.
--title TEXT                    Optional sheet title.
--page-width N                  Optional fixed page width; enables page mode.
--page-height N                 Optional fixed page height; enables page mode.
--max-thumb-width N             Dynamic-mode thumbnail cap; default 2048.
--max-thumb-height N            Dynamic-mode thumbnail cap; default 2048.
--max-page-height N             Dynamic-mode pagination cap; default 12000.
--bg neutral|white|black|checker|#RRGGBB
--no-open                       Do not open generated sheets in Preview.
--force                         Only when the user explicitly said overwrite or replace.
```

Avoid in v1:

- PDF output
- JSON input mode
- a long layout cookbook
- bundled fonts
- ImageMagick dependency
- semantic before/after filename heuristics inside the script
- a deterministic runner, controller, or harness layer

## Defaults

Default output:

```text
/tmp/contact-sheet-builder/<UTC-timestamp>/contact_sheet.png
```

After a successful build, open generated sheet PNGs in macOS Preview by
default. Use `--no-open` for batch, headless, or "do not open it" requests.

If there are multiple pages:

```text
/tmp/contact-sheet-builder/<UTC-timestamp>/contact_sheet_page_001.png
/tmp/contact-sheet-builder/<UTC-timestamp>/contact_sheet_page_002.png
```

Write a manifest beside the output:

```text
/tmp/contact-sheet-builder/<UTC-timestamp>/manifest.json
```

If the user names an explicit file, write the manifest beside it:

```text
foo.png
foo.manifest.json
```

Default columns:

```text
n=1       -> 1 column
n=2       -> 2 columns
n=3..4    -> 2 columns
n=5..6    -> 3 columns
n>=7      -> 4 columns
```

Explicit user instructions always win:

- "4 columns" -> `--columns 4`
- "stack them" -> `--columns 1`
- "before and after" with two matched items -> `--columns 2`

Default canvas:

- dynamic image-first PNG
- `0px` outside margin and `2px` gutters by default
- no card boxes in the default dynamic layout
- preserve near-native image size up to `2048x2048`
- format: PNG
- split pages when adding the next row would exceed `--max-page-height`

Fixed page mode:

- use `--page-width` and `--page-height` when the user asks for a page-like
  overview
- missing fixed-page dimensions default to `2048x2560`
- split pages when adding the next row would overflow the fixed page height

Default labels:

- labels are on
- source is filename stem
- replace `_` and `-` with spaces for readability
- maximum label length is 32 characters by default
- wrap to at most two lines
- ellipsize labels that still do not fit
- prefix with parent folder only when duplicate stems would collide

Default image fitting:

- preserve aspect ratio
- contain-fit inside each cell
- do not crop unless a later version explicitly adds crop support
- composite transparent images onto a per-cell checker
- keep the sheet background neutral unless the user asks otherwise

## Input Resolution

The agent should accept:

- direct image paths
- folders
- shell globs
- attached local image paths
- mixed lists of files and folders

Supported image formats should follow Pillow support, with the common path
covering PNG, JPEG, WebP, TIFF, and BMP.

Folder handling:

- default to non-recursive folder reads unless the user says recursive or all
- sort by natural path order
- skip hidden files by default
- skip non-image files with warnings

This keeps a folder ask fast and predictable while still allowing larger sets
when the user asks for them.

## Plain-English Adaptation

The agent layer should map common edits to script flags without asking:

```text
"no labels"                  -> --no-labels
"use full filenames"         -> --labels-from filename
"use parent folder names"    -> --labels-from parent
"make it 3 columns"          -> --columns 3
"stack them"                 -> --columns 1
"before and after"           -> order inputs, pass two labels if obvious, --columns 2
"fixed page"                 -> set --page-width and --page-height
"white background"           -> --bg white
"black background"           -> --bg black
"title it X"                 -> --title X
"do not open it"             -> --no-open
"overwrite" or "replace"     -> --force
```

The skill should not ask "how many columns?" unless the user's instruction is
actually contradictory or impossible.

## Output Receipt

The script stdout should be short and machine-readable enough for the agent to
summarize:

```text
OK contact_sheet pages=3 images=42 skipped=2 labels=on columns=4 preview=opened out=/tmp/contact-sheet-builder/20260515T220000Z manifest=/tmp/contact-sheet-builder/20260515T220000Z/manifest.json
warning: skipped broken.jpg (not a valid image)
```

The agent's user-facing reply should be short:

```text
Built a labeled contact sheet: /tmp/contact-sheet-builder/20260515T220000Z/contact_sheet.png
Opened in Preview. 42 images, 3 pages, 2 skipped. Manifest: /tmp/contact-sheet-builder/20260515T220000Z/manifest.json
```

Do not paste the manifest unless the user asks for details.

## Manifest

The manifest should include:

- created timestamp
- command args
- output page paths
- page size
- column count
- labels on/off
- preview open status
- input paths used
- label assigned to each input
- skipped paths and reasons
- Pillow version

The manifest is the debug handle. It prevents the skill from making the normal
reply noisy.

## Exit Codes

Recommended script exit codes:

```text
0  success, including success with skipped inputs
2  no usable images
3  output exists and --force was not provided
4  invalid option conflict
```

For exit `2`, the agent should say no usable images were found and include the
top reasons from warnings.

For exit `3`, the agent should ask once whether to overwrite or choose a new
path.

## Edge Cases

Single image:

- render a one-cell labeled sheet
- do not reject it

Missing or broken inputs:

- skip and warn
- still build if at least one usable image remains

Large input set:

- paginate automatically
- do not ask first
- tell the user how many images and pages were rendered

Huge source files:

- use Pillow thumbnailing to avoid holding full-resolution copies longer than
  needed
- process page-by-page where practical

Transparent PNGs:

- show transparency with a checker inside the cell

Duplicate labels:

- add parent folder context only for the colliding labels

Explicit output path exists:

- block unless the user explicitly said overwrite or replace

Temp output durability:

- `/tmp` is convenient but not permanent
- if the user says the sheet is important, use a user-named output path or tell
  them the temp path may be cleaned later

## Anti-Cases

Do not route these to `contact-sheet-builder`:

- "generate a contact sheet of chair angles for this theme"
- "make a new set of image variants"
- "edit these images"
- "turn these into a Figma board"
- "make a slide deck from these images"
- "extract frames from this video"

The first case belongs to theme/image-generation skills such as `theme_builder`.
This new skill is only for arranging existing images.

## Validation Plan For The Future Build

Because this turn is plan-only, no script tests should run yet. When the skill
is built, validate it on this machine with temporary output under:

`/tmp/psmobile/<timestamp>/contact-sheet-builder/`

Use these smoke tests:

1. Labeled default sheet from a small psmobile experiment folder.
2. Same inputs with `--no-labels`.
3. Two-image before/after style sheet with `--columns 2` and explicit labels.
4. Mixed portrait and landscape inputs.
5. Single image input.
6. Missing path plus valid image paths, expecting success with warning.
7. Broken or non-image file plus valid images, expecting success with warning.
8. Existing explicit output path without `--force`, expecting exit `3`.
9. Existing explicit output path with `--force`, expecting overwrite.
10. Large folder input, expecting pagination.
11. Transparent PNG input, expecting checker-backed alpha.
12. Anti-case routing check: theme generation request should not use this skill.

After future skill package changes under `skills/contact-sheet-builder/`, run:

```bash
npx skills check
```

If only docs change, do not claim script or skill validation ran.

## Implementation Notes

Do not create the package until the user asks to build it.

When building:

1. Create `skills/contact-sheet-builder/SKILL.md`.
2. Create `skills/contact-sheet-builder/scripts/build_contact_sheet.py`.
3. Add `references/rendering-behavior.md` only if the rendering rules make
   `SKILL.md` too long.
4. Run focused script smoke tests against temporary outputs.
5. Run `npx skills check`.
6. Keep the final user reply short: output path, tests run, and any known
   limits.

## Rejected Alternatives

Rejected: ImageMagick as the runtime dependency.
Reason: Pillow is already available and keeps the skill self-contained.

Rejected: a controller, harness, or multi-step orchestration layer.
Reason: this is a convenience tool, not a workflow system.

Rejected: asking the user for columns, labels, and output path by default.
Reason: the main value is fast visual inspection.

Rejected: semantic filename heuristics inside the script.
Reason: the agent can interpret before/after intent better, and the script
should stay boring and predictable.

Rejected: writing output next to the first input by default.
Reason: it can dirty repos and create overwrite friction.

Rejected: PDF, GIF, video, Figma, or slide output in v1.
Reason: those are separate tools and would make the first version too broad.

## Residual Risks

- Temp outputs are convenient but not durable.
- Font fallback can make labels look plain on hosts without a good default font.
- Very wide panoramas may waste vertical space in a fixed page.
- Very large folders can produce many pages quickly.
- If labels are too aggressive, the sheet may feel noisy; `--no-labels` and
  `--label-max` should make that easy to adjust.

These risks are acceptable for v1 because the skill is meant to produce a fast
thing to inspect, not a final publication layout.
