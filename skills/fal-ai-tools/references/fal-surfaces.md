# fal Surfaces

Use this reference to choose how to talk to fal.ai. Prefer the most capable
available surface, but keep the user-facing workflow the same.

## Surface priority

1. **fal MCP tools** when visible in the host runtime.
2. **`fal_client` SDK** when MCP tools are unavailable.
3. **raw HTTP** when neither MCP nor the SDK is available.

Do not hardcode the MCP tool prefix. The server name can change the local tool
names, such as `mcp__fal__*` versus `mcp__fal-ai__*`. Detect by capability:
`search_models`, `get_model_schema`, `get_pricing`, `upload_file`,
`run_model`, `submit_job`, and `check_job`.

## MCP surface

Hosted server:

```text
https://mcp.fal.ai/mcp
```

The docs describe a stateless MCP server that receives the key per request. The
useful tools are:

- `search_models`
- `recommend_model`
- `get_model_schema`
- `get_pricing`
- `search_docs`
- `upload_file`
- `run_model`
- `submit_job`
- `check_job`

Use `run_model` for short calls and `submit_job` plus `check_job` for
long-running media jobs. Use `upload_file` for local files.

## SDK surface

Python SDK examples should assume `FAL_KEY` is already available:

```python
import fal_client

url = fal_client.upload_file("/absolute/path/to/input.png")
result = fal_client.subscribe(
    "fal-ai/imageutils/rembg",
    arguments={"image_url": url},
    with_logs=True,
)
```

Use `subscribe()` when the user wants a simple blocking flow. Use `submit()`,
status polling, and result retrieval for longer work or when a receipt needs a
job id.

JavaScript examples should follow the same shape with `@fal-ai/client`.

## HTTP surface

Use raw HTTP when MCP and SDK access are unavailable or when validating no-cost
Platform APIs.

Model inference hosts:

- `https://fal.run/<endpoint-id>`
- `https://queue.fal.run/<endpoint-id>`
- `wss://ws.fal.run/<endpoint-id>`

Platform API host:

- `https://api.fal.ai/v1/...`

HTTP Model API auth:

```text
Authorization: Key $FAL_KEY
```

Hosted MCP auth:

```text
Authorization: Bearer <FAL_KEY>
```

## Key handling

fal clients expect `FAL_KEY`. Some local projects may store the same credential
as `FAI_API_KEY`. Alias it only inside the running shell:

```bash
set -a
. ./.env
set +a
export FAL_KEY="${FAL_KEY:-$FAI_API_KEY}"
test -n "${FAL_KEY:?FAL_KEY or FAI_API_KEY is required}"
```

Never print the key. Do not use `echo "$FAL_KEY"`, `printenv`, or logs that
include headers. When writing receipts, say only that the key was available and
redacted.
