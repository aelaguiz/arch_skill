# fal.ai Tools Skill Plan

Date: 2026-05-05

Status: plan only. The skill package is not implemented yet.

Target skill: `fal-ai-tools`

Consensus artifacts:
`.arch_skill/model-consensus/fal-ai-tools-skill-plan-20260505T123848Z/`

## Goal

Build a reusable prompt-first skill that lets an agent use fal.ai tools safely
and well. It should support background removal directly, while also making the
full fal.ai surface reachable through model discovery, schema lookup, pricing
lookup, file upload, inference, polling, and error handling.

The skill should prefer the fal MCP tools when they are available. If the MCP
server is not installed, the same skill should fall back to `fal_client` or raw
HTTP calls. The user should not need to know which runtime path is active.

## Consensus

The model-consensus run converged.

Participants:

- Model A: `"gpt 5.5 xhigh"` -> runtime `codex`, model `gpt-5.5`, effort
  `xhigh`, collaborator.
- Model B: `"opus 4.7 xhigh"` -> runtime `claude`, model
  `claude-opus-4-7`, effort `xhigh`, collaborator.

Final agreement:

- Use `fal-ai-tools` as the skill slug.
- Save this plan as `docs/FAL_AI_TOOLS_SKILL_PLAN_2026-05-05.md`.
- Create a prompt-first package with `SKILL.md` plus five references.
- Do not add `agents/openai.yaml` in v1.
- Do not add scripts, runners, launchers, controllers, or formal input schemas
  in v1.
- Put `fal-ai-tools` in the agents, Claude, and Gemini skill install lists.
- Use background-removal recipes as the only curated operation examples in v1.
- Use live model discovery, schema lookup, and pricing lookup for everything
  else.
- Use `.env` only as a secret source. The local key is `FAI_API_KEY`; fal
  expects `FAL_KEY`, so validation commands should alias it without printing
  the value.
- No paid inference runs by default. A paid smoke test requires explicit user
  approval.

Residual risks:

- fal model schemas, pricing, and model lists can drift. The skill must make
  live schema and pricing lookup mandatory before paid calls.
- MCP tool names can vary by local server name, such as `mcp__fal__*` versus
  `mcp__fal-ai__*`. The skill must detect available fal tools by capability
  instead of hardcoding a single tool prefix.

## Sources Scraped

Official fal.ai sources scraped or checked during planning:

- `https://fal.ai/docs/llms.txt`
- `https://fal.ai/docs/documentation/setting-up/authentication`
- `https://fal.ai/docs/documentation/setting-up/mcp`
- `https://fal.ai/docs/documentation/model-apis/inference`
- `https://fal.ai/docs/documentation/model-apis/inference/client-setup`
- `https://fal.ai/docs/documentation/model-apis/inference/queue`
- `https://fal.ai/docs/documentation/model-apis/fal-cdn`
- `https://fal.ai/docs/documentation/model-apis/common-parameters`
- `https://fal.ai/docs/documentation/model-apis/media-expiration`
- `https://fal.ai/docs/documentation/model-apis/errors`
- `https://fal.ai/docs/documentation/model-apis/pricing`
- `https://fal.ai/docs/platform-apis/v1/models`
- `https://fal.ai/docs/model-api-reference/image-generation-api/imageutils`
- `https://fal.ai/docs/model-api-reference/image-generation-api/birefnet`
- `https://fal.ai/docs/model-api-reference/image-generation-api/bria-background`
- `https://fal.ai/models/fal-ai/ben/v2/image/api`
- `https://fal.ai/docs/model-api-reference/video-generation-api/birefnet-v2`
- `https://fal.ai/docs/model-api-reference/video-generation-api/bria-video`

Live non-generating Platform API checks were also run with the local `.env`
key. No key value was printed.

## Source Facts

The skill should treat these as starting truth, then verify live before any
paid call.

- fal client libraries use `FAL_KEY` from the environment.
- raw Model API requests use `Authorization: Key $FAL_KEY`.
- the hosted MCP server uses `Authorization: Bearer <FAL_KEY>`.
- hosted MCP URL: `https://mcp.fal.ai/mcp`.
- documented MCP tools include `search_models`, `get_model_schema`,
  `get_pricing`, `search_docs`, `run_model`, `submit_job`, `check_job`,
  `upload_file`, and `recommend_model`.
- Model API inference uses `fal.run`, `queue.fal.run`, and
  `wss://ws.fal.run`.
- Platform APIs such as model search and pricing use
  `https://api.fal.ai/v1/...`.
- `run` is direct synchronous inference.
- `subscribe` blocks on a queued job.
- `submit` is the production-oriented async path with status/result polling or
  webhooks.
- fal model inputs use public URLs for media. Local files should be uploaded
  to the fal CDN or exposed through presigned URLs.
- fal CDN URLs are public. Private URLs that need auth headers are not valid
  model inputs.
- generated-media retention can be controlled with
  `X-Fal-Object-Lifecycle-Preference`.
- `X-Fal-Store-IO: 0` prevents JSON request payload storage, but output files
  still follow media retention rules.
- request payloads are stored for 30 days by default.
- model validation/content errors return a typed `detail` array.
- request/infrastructure errors return `detail`, `error_type`, and
  `X-Fal-Error-Type`.

## Live Planning Receipt

These checks were run during this planning pass. They did not run model
inference and did not print the key value.

- `.env` key presence: `FAI_API_KEY=<redacted>` exists.
- Platform model search:
  `GET https://api.fal.ai/v1/models?q=background%20removal&status=active&limit=12`
  returned 12 active background-removal results.
- Pricing lookup returned:
  `fal-ai/imageutils/rembg` -> USD `0.00111` per compute second.
- Pricing lookup returned:
  `fal-ai/birefnet/v2` -> USD `0.00111` per compute second.
- Pricing lookup returned:
  `fal-ai/bria/background/remove` -> USD `0.018` per generation.
- Pricing lookup returned:
  `fal-ai/birefnet/v2/video` -> USD `0.00111` per compute second.
- Paid smoke test: skipped.
- Key handling: `FAL_KEY` was aliased from `FAI_API_KEY`; no key value was
  logged in this plan.

Active background-removal endpoints observed in the live search:

- `pixelcut/background-removal`
- `veed/video-background-removal/fast`
- `bria/video/background-removal`
- `veed/video-background-removal`
- `veed/video-background-removal/green-screen`
- `fal-ai/birefnet/v2`
- `fal-ai/birefnet`
- `fal-ai/bria/background/remove`
- `fal-ai/birefnet/v2/video`
- `fal-ai/ben/v2/image`
- `fal-ai/ben/v2/video`
- `fal-ai/imageutils/rembg`

## Skill Package

Create:

```text
skills/fal-ai-tools/
  SKILL.md
  references/
    fal-surfaces.md
    operation-workflow.md
    files-privacy-retention.md
    background-removal.md
    validation.md
```

Do not create in v1:

- `scripts/`
- `agents/openai.yaml`
- `README.md`
- changelogs or process diaries inside the skill package
- runners, launchers, controllers, or formal parameter schemas

Reason: the work is provider-specific agent behavior, but fal already ships
the MCP server, SDKs, and HTTP APIs. A wrapper script would duplicate fal's
tools and make the skill more brittle without adding deterministic value.

## Trigger Description Draft

Use this in `skills/fal-ai-tools/SKILL.md` frontmatter, keeping it under the
runtime description cap:

```yaml
description: "Use fal.ai MCP tools or direct fal SDK/API calls to discover or recommend models, inspect schemas and pricing, upload files, run/submit/stream inference jobs, poll results, and handle outputs, errors, cost, and retention. Use for fal.ai tasks such as background removal, image/video/audio/3D/vision generation or editing, and schema-aware request building. Prefer an installed fal.ai MCP server when available and fall back to fal_client or raw HTTP. Do not use for non-fal providers, generic media editing that will not call fal, account administration, or installing/configuring the fal MCP server."
```

## SKILL.md Contract

`SKILL.md` should stay lean. It owns the runtime behavior and the first
decision path.

Include:

- When to use:
  use for fal.ai media and model tasks, including background removal, model
  search, schema lookup, pricing, file upload, inference, polling, and result
  handling.
- When not to use:
  do not use for non-fal providers, generic local media editing, fal account
  administration, MCP installation as the main task, or frontend work that only
  displays already-generated assets.
- Non-negotiables:
  never print, copy, commit, or paste `FAL_KEY` or `FAI_API_KEY`; always check
  schema and pricing before paid calls; use `submit_job` plus `check_job` for
  long-running media; treat fal CDN URLs as public; return model id, request
  id when available, cost posture, output URLs, and retention posture.
- First move:
  detect available fal MCP tools by capability and prefix; if none are
  available, check whether direct `fal_client` or raw HTTP can be used; confirm
  a key is available without printing it; restate the user's task in fal terms.
- Workflow:
  discover -> inspect schema -> check pricing -> prepare files -> choose
  execution path -> run or submit -> poll/collect -> interpret errors/results
  -> return a concise result.
- Output expectations:
  name the model used, inputs used, request/job id when present, result URLs,
  estimated or known cost posture, retention/privacy note, and any follow-up
  action needed.
- Reference map:
  point to the five references below.

## Reference Ownership

`references/fal-surfaces.md` owns:

- MCP server URL and setup notes as inert reference, not executed setup.
- MCP tool inventory and capability detection.
- direct SDK fallback with Python and JavaScript examples.
- raw HTTP fallback with auth header shapes.
- endpoint host distinctions: `fal.run`, `queue.fal.run`, `wss://ws.fal.run`,
  and `api.fal.ai/v1/...`.
- `FAL_KEY` versus local `FAI_API_KEY` aliasing.

`references/operation-workflow.md` owns:

- model discovery with `search_models` and `recommend_model`.
- schema lookup with `get_model_schema`.
- pricing lookup with `get_pricing`.
- request controls such as timeout, runner hints, queue priority, retry
  controls, and fallback controls.
- when to use `run_model`, `submit_job`, `check_job`, SDK `run`,
  `subscribe`, `submit`, `stream`, and realtime paths.
- result handling and typed error interpretation.

`references/files-privacy-retention.md` owns:

- local file upload to fal CDN.
- public URL requirements.
- private URL and auth-header limitations.
- data URI limits.
- generated-media retention controls.
- `X-Fal-Store-IO: 0`.
- secret hygiene in commands, logs, docs, and final replies.

`references/background-removal.md` owns:

- image background-removal recipes.
- video background-removal recipes.
- model tradeoffs and live-check reminders for:
  `fal-ai/imageutils/rembg`, `fal-ai/birefnet`, `fal-ai/birefnet/v2`,
  `fal-ai/bria/background/remove`, `fal-ai/ben/v2/image`,
  `fal-ai/birefnet/v2/video`, `bria/video/background-removal`, Pixelcut, and
  VEED endpoints.
- important schema fields such as `image_url`, `video_url`, `sync_mode`,
  `output_mask`, `mask_only`, `background_color`, output format/container, and
  duration/size limits where applicable.
- the rule that examples are not a catalog. The agent must still check live
  schemas and pricing.

`references/validation.md` owns:

- no-cost validation commands.
- MCP validation path when fal tools are installed.
- SDK/HTTP validation path when MCP is not installed.
- validation receipt template.
- optional paid smoke test recipe, gated by explicit user approval.

## Implementation Phases

### Phase 1: Skill Skeleton And Core Contract

Create the package:

- `skills/fal-ai-tools/SKILL.md`
- `skills/fal-ai-tools/references/fal-surfaces.md`
- `skills/fal-ai-tools/references/operation-workflow.md`

Update install and routing surfaces:

- add `fal-ai-tools` to `SKILLS`, `CLAUDE_SKILLS`, and `GEMINI_SKILLS` in
  `Makefile`.
- add `fal-ai-tools` to the `README.md` skill inventory.
- add install-path entries for agents, Claude, and Gemini in `README.md`.
- add a `fal-ai-tools` shipped-skill section in `README.md`.
- add an `AGENTS.md` routing line:
  use `$fal-ai-tools` when the user wants to use fal.ai tools, models, MCP,
  SDK/API calls, background removal, media generation/editing, model discovery,
  schema lookup, pricing, upload, inference, or result polling.

Verification after Phase 1:

```bash
npx skills check
```

### Phase 2: Files, Privacy, And Background Removal

Add:

- `skills/fal-ai-tools/references/files-privacy-retention.md`
- `skills/fal-ai-tools/references/background-removal.md`

Keep `background-removal.md` curated but small. Include current endpoint
examples because the user named background removal. Do not add recipe stubs for
every fal category in v1.

Verification after Phase 2:

```bash
npx skills check
```

### Phase 3: Validation Reference And Install Proof

Add:

- `skills/fal-ai-tools/references/validation.md`

Run:

```bash
npx skills check
make verify_install
```

Use `make verify_install` here because the implementation changed the installed
skill surface and the plan intentionally validates installation.

### Phase 4: Live No-Cost Validation

Use `.env` without printing the key:

```bash
set -a
. ./.env
set +a
export FAL_KEY="${FAL_KEY:-$FAI_API_KEY}"
test -n "${FAL_KEY:?FAL_KEY or FAI_API_KEY is required}"
```

Direct Platform API check:

```bash
curl -fsS -G "https://api.fal.ai/v1/models" \
  --data-urlencode "q=background removal" \
  --data-urlencode "status=active" \
  --data-urlencode "limit=12" \
  -H "Authorization: Key $FAL_KEY"
```

Pricing check:

```bash
curl -fsS -G "https://api.fal.ai/v1/models/pricing" \
  --data-urlencode "endpoint_id=fal-ai/imageutils/rembg" \
  --data-urlencode "endpoint_id=fal-ai/birefnet/v2" \
  --data-urlencode "endpoint_id=fal-ai/bria/background/remove" \
  -H "Authorization: Key $FAL_KEY"
```

If MCP tools are installed, run equivalent no-cost checks:

```text
search_models("background removal")
get_model_schema("fal-ai/birefnet/v2")
get_model_schema("fal-ai/bria/background/remove")
get_pricing("fal-ai/imageutils/rembg")
get_pricing("fal-ai/birefnet/v2")
get_pricing("fal-ai/bria/background/remove")
search_docs("retention errors fal Model API")
```

Append a validation receipt to the implementation notes or final response:

```text
Validation Receipt
- date: <UTC timestamp>
- model search: ok, <N> results
- schema lookup: ok, <model ids checked>
- pricing lookup: ok, <model ids checked>
- platform API: ok, HTTP 200
- key handling: FAL_KEY aliased from FAI_API_KEY; no key value emitted
- paid smoke test: skipped unless explicitly approved
```

### Phase 5: Optional Paid Smoke Test

Only run this if the user explicitly approves spending fal credits.

Recommended target:

- cheapest practical background-removal endpoint from live pricing, likely
  `fal-ai/imageutils/rembg` at the time of this plan.
- tiny public test image URL.
- `submit_job` plus `check_job` if using MCP; SDK `submit` plus status/result
  polling if using direct SDK.

Receipt must include:

- endpoint id
- request/job id
- output URL
- observed or estimated cost posture
- no key value logged

## Background Removal Recipe Baseline

The v1 recipe reference should start with these patterns, then force live
schema/pricing lookup before execution.

Image:

- `fal-ai/imageutils/rembg` for a simple remove-background path.
- `fal-ai/birefnet/v2` when mask output, foreground refinement, or model choice
  matters.
- `fal-ai/bria/background/remove` when the commercial-friendly Bria model is a
  better fit.
- `fal-ai/ben/v2/image` as a fast/high-quality alternative to evaluate live.

Video:

- `fal-ai/birefnet/v2/video` when mask video or refinement matters.
- `bria/video/background-removal` when output container and background color
  control matter.
- VEED and Pixelcut endpoints as candidates discovered by live search rather
  than hardwired defaults.

## Rejected Alternatives

- Static catalog of all fal models:
  rejected because it goes stale and makes the skill worse. Use
  `search_models`, `recommend_model`, `get_model_schema`, and `get_pricing`.
- Separate MCP and API skills:
  rejected because the user wants to use fal tools, not choose a transport.
  One skill should detect the available path.
- Background-removal-only skill:
  rejected because the user asked for fal tools such as background removal,
  not only background removal.
- A wrapper script:
  rejected because fal already provides MCP tools, SDKs, and HTTP APIs. Prompt
  guidance is enough for v1.
- `agents/openai.yaml` in v1:
  rejected because no UI metadata or invocation policy is needed yet.
- Paid inference during planning:
  rejected because the user asked for a plan and the safe checks can be
  non-generating.

## Definition Of Done For Implementation

Implementation is done when:

- `skills/fal-ai-tools/SKILL.md` exists with valid frontmatter and the final
  trigger description.
- the five references exist and are self-contained.
- `Makefile`, `README.md`, and `AGENTS.md` include `fal-ai-tools` in the right
  surfaces.
- the skill does not depend on archived commands, hidden local prompt packs, or
  current planning artifacts.
- `npx skills check` passes.
- `make verify_install` passes if the installed surface is intentionally
  validated.
- the final reply or implementation notes include a validation receipt.
- no secret value from `.env` appears in docs, logs, prompts, or final output.
