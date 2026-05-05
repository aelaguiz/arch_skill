---
name: fal-ai-tools
description: "Use fal.ai MCP tools or direct fal SDK/API calls to discover or recommend models, inspect schemas and pricing, upload files, run/submit/stream inference jobs, poll results, and handle outputs, errors, cost, and retention. Use for fal.ai tasks such as background removal, image/video/audio/3D/vision generation or editing, and schema-aware request building. Prefer an installed fal.ai MCP server when available and fall back to fal_client or raw HTTP. Do not use for non-fal providers, generic media editing that will not call fal, account administration, or installing/configuring the fal MCP server."
---

# fal.ai Tools

Use this skill when the user wants to use fal.ai models or tools, including
background removal, media generation or editing, model discovery, schema lookup,
pricing checks, file upload, inference, polling, or result handling.

The skill is one provider workflow with multiple transport paths. Prefer fal
MCP tools when they are visible in the runtime; otherwise use `fal_client` or
raw HTTP. Do not make the user choose the transport.

## When to use

- The user wants to run or prepare a fal.ai model call.
- The user asks for background removal, image/video/audio/3D/vision generation
  or editing through fal.ai.
- The user needs to discover fal models, inspect a model schema, check pricing,
  upload files to fal CDN, submit a queued job, poll a result, or interpret a
  fal error.
- The user gives a media task in ordinary language and fal.ai is the intended
  provider.

## When not to use

- The provider is not fal.ai.
- The task is generic local image editing that will not call fal.
- The task is account administration, billing management, dashboard work, or
  installing/configuring the fal MCP server itself.
- The task is only rendering or displaying an already-generated asset in an app.

## Non-negotiables

- Never print, echo, copy, commit, paste, or summarize the value of `FAL_KEY`,
  `FAI_API_KEY`, or any fal credential.
- Before a paid call, inspect the model schema and pricing from the live API or
  MCP tools. Do not rely on remembered schemas or static price examples.
- Treat fal CDN URLs and generated output URLs as public unless the current docs
  prove otherwise.
- For long-running media jobs, prefer queued submission plus polling over a
  single blocking call.
- Do not freeze a static fal model catalog. Use discovery tools and schema
  lookup; curated recipes are examples, not routing tables.
- Return enough of a receipt for the user to understand what happened: model
  id, request or job id when available, input source, output URLs or local
  paths, cost posture, and retention/privacy note.

## First move

1. Restate the user's request as a concrete fal operation and identify the
   input media, desired output, and whether spending fal credits is involved.
2. Detect the available fal surface:
   - If MCP tools such as `search_models`, `get_model_schema`, `get_pricing`,
     `upload_file`, `run_model`, `submit_job`, or `check_job` are visible, use
     them.
   - Otherwise use `fal_client` if available.
   - Otherwise use raw HTTP against fal endpoints.
3. Confirm a key is available without printing it. fal expects `FAL_KEY`; if a
   project uses `FAI_API_KEY`, alias it in-process only.
4. Discover or choose the model, inspect its schema, check pricing, and decide
   whether the user has already approved any paid call.
5. Prepare input files as public URLs, fal CDN uploads, or presigned URLs.
6. Execute, poll, collect outputs, and return a concise receipt.

## Workflow

1. **Discover**: search or recommend models when the model is not already
   specified. Use user intent and media type to narrow candidates.
2. **Inspect**: fetch the exact model schema and required fields. Do not guess
   field names.
3. **Price**: fetch current pricing for the selected endpoint before paid work.
4. **Prepare files**: upload local files or use public/presigned URLs. Avoid
   data URIs except for tiny inputs explicitly supported by the schema.
5. **Run or submit**: use the shortest safe execution path. Use queued jobs and
   polling for long-running work.
6. **Handle errors**: separate validation/content errors from infrastructure
   errors, and retry only when the failure mode is retryable.
7. **Report**: return model id, request id, outputs, cost posture, retention
   posture, and any skipped checks.

## Output expectations

For completed calls, include:

- operation and endpoint id
- input files or URLs used
- schema/pricing checks performed
- request id or job id when available
- output URL or local saved path
- cost posture, such as unit price or estimated cost
- retention/privacy note
- failures or skipped steps, with the reason

If no call was run, say exactly which prerequisite blocked it: missing key,
missing input, missing schema support, pricing risk, provider unavailability, or
missing user approval for paid work.

## Reference map

- `references/fal-surfaces.md` - MCP tools, SDK fallback, HTTP fallback,
  endpoint hosts, auth, and key handling
- `references/operation-workflow.md` - discovery, schemas, pricing, request
  controls, inference modes, polling, results, and errors
- `references/files-privacy-retention.md` - file upload, public URLs, retention,
  storage controls, and secret hygiene
- `references/background-removal.md` - curated image and video background
  removal recipes and live-check reminders
- `references/validation.md` - no-cost checks, paid smoke-test rules, and
  receipt format
