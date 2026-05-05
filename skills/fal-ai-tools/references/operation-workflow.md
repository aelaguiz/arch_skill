# Operation Workflow

Use this reference for model selection, schema handling, pricing, inference,
polling, and errors.

## Discovery

If the user did not name an endpoint, search or recommend models from the live
surface. Use the media type, desired output, quality constraints, and budget to
choose candidates.

Do not make a static catalog. Current examples are allowed only as starting
points. The live model registry is the source of truth.

## Schema check

Before building arguments, fetch the exact schema for the endpoint:

- MCP: `get_model_schema(<endpoint-id>)`
- Platform/docs lookup when MCP is unavailable
- model docs as a fallback source for field names

Verify required fields, file input names, enum values, output fields, sync
settings, mask options, and format controls. Do not infer field names from a
similar model.

## Pricing check

Before paid calls, fetch current pricing:

- MCP: `get_pricing(<endpoint-id>)`
- HTTP: `GET https://api.fal.ai/v1/models/pricing?endpoint_id=<endpoint-id>`

Tell the user the pricing unit when it matters, such as per image, per
generation, per megapixel, or per compute second. If the user did not approve a
paid call and the task is not clearly already authorized, stop and ask.

## Request controls

Use request controls only when they change the result:

- server-side start timeout: `X-Fal-Request-Timeout` or SDK `start_timeout`
- client wait timeout: SDK `client_timeout`
- runner affinity: `X-Fal-Runner-Hint` or SDK `hint`
- queue priority: `X-Fal-Queue-Priority: low|normal`
- no retry: `X-Fal-No-Retry`
- disable model fallback: `x-app-fal-disable-fallback`
- fail-fast queue length: `fal_max_queue_length` query parameter

Do not add every header by default. Use the smallest set needed for the task.

## Execution choice

- Use `run_model` or SDK `run` for short, direct calls where blocking is fine.
- Use `submit_job` plus `check_job` or SDK `submit` for long-running media,
  batch-like work, or when job tracking matters.
- Use SDK `subscribe` for simple queued work where a blocking local wait is
  acceptable.
- Use streaming or realtime only when the model and task need incremental
  results.

## Result handling

Normalize the output into a useful receipt:

- endpoint id
- request id or job id when available
- input URL or uploaded file URL
- output URL or downloaded local path
- pricing unit and cost posture
- retention or privacy note
- warnings about skipped schema/pricing checks

If the output URL should be downloaded for the user, save it under the chosen
run artifact directory and keep the remote URL in the receipt.

## Errors

Model validation and content errors commonly return a typed `detail` array. Use
`type` and `ctx` for program decisions, and show `msg` to the user.

Infrastructure errors commonly return `detail`, `error_type`, and
`X-Fal-Error-Type`.

Retry only when the failure is likely transient, such as a runner or timeout
failure. Do not blindly retry malformed inputs, missing required fields,
unsupported files, or content-policy failures.
