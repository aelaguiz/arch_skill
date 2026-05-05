# Background Removal

Use this reference for fal.ai image and video background-removal tasks. These
recipes are starting points, not a model catalog. Always check the live schema
and pricing before execution.

## Image recipes

### Simple remove background

Candidate endpoint:

```text
fal-ai/imageutils/rembg
```

Typical required input:

- `image_url`

Useful options from docs:

- `sync_mode`
- `crop_to_bbox`

Use when the user wants a straightforward transparent-background output and no
mask-specific control.

### BiRefNet quality and masks

Candidate endpoints:

```text
fal-ai/birefnet
fal-ai/birefnet/v2
```

Typical required input:

- `image_url`

Useful options from docs:

- model variant
- operating resolution
- `output_mask`
- `mask_only`
- `refine_foreground`
- `sync_mode`
- output format

Use when the user wants mask output, higher-quality subject separation,
foreground refinement, or model choice.

### Bria commercial-friendly removal

Candidate endpoint:

```text
fal-ai/bria/background/remove
```

Typical required input:

- `image_url`

Use when Bria's commercial-friendly positioning matters or when live tests show
it fits the image better. Pricing has historically been per generation, so check
current pricing before use.

### BEN image removal

Candidate endpoint:

```text
fal-ai/ben/v2/image
```

Typical required input:

- `image_url`

Use as a fast/high-quality alternative candidate. Inspect the schema before use
because model fields can drift.

## Video recipes

### BiRefNet video masks

Candidate endpoint:

```text
fal-ai/birefnet/v2/video
```

Typical required input:

- `video_url`

Useful options from docs:

- model variant
- operating resolution
- `output_mask`
- `refine_foreground`
- `sync_mode`
- output type
- video quality
- write mode

Use when the user wants mask video output or foreground refinement.

### Bria video background removal

Candidate endpoint:

```text
bria/video/background-removal
```

Typical required input:

- `video_url`

Useful options from docs:

- `background_color`
- output container and codec

Docs have described input limits such as under `4000x4000` and under `30s`.
Verify current limits from the live schema or docs before execution.

## Discovery candidates

Live search may surface other useful endpoints, such as Pixelcut or VEED
background-removal models. Treat them as candidates. Do not use them without
schema and pricing checks.

## Output receipt

For every background-removal run, report:

- endpoint id
- input image or video
- key options used
- whether mask output was requested
- output URL or local file path
- request or job id when available
- price unit and cost posture
- retention note
