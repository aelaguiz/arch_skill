# Validation

Use this reference to validate the skill package and to test fal access without
leaking credentials.

## Package checks

After changing `skills/fal-ai-tools/`, run:

```bash
npx skills check
```

When install behavior or installed surfaces are intentionally validated, run:

```bash
make verify_install
```

## Key setup

Use `.env` as a source only. Alias keys without printing them:

```bash
set -a
. ./.env
set +a
export FAL_KEY="${FAL_KEY:-$FAI_API_KEY}"
test -n "${FAL_KEY:?FAL_KEY or FAI_API_KEY is required}"
```

Do not run `echo "$FAL_KEY"`, `printenv`, or any command that prints auth
headers.

## No-cost API checks

Model search:

```bash
curl -fsS -G "https://api.fal.ai/v1/models" \
  --data-urlencode "q=background removal" \
  --data-urlencode "status=active" \
  --data-urlencode "limit=12" \
  -H "Authorization: Key $FAL_KEY"
```

Pricing:

```bash
curl -fsS -G "https://api.fal.ai/v1/models/pricing" \
  --data-urlencode "endpoint_id=fal-ai/imageutils/rembg" \
  --data-urlencode "endpoint_id=fal-ai/birefnet/v2" \
  --data-urlencode "endpoint_id=fal-ai/bria/background/remove" \
  -H "Authorization: Key $FAL_KEY"
```

If MCP tools are available, run equivalent no-cost checks:

```text
search_models("background removal")
get_model_schema("fal-ai/birefnet/v2")
get_model_schema("fal-ai/bria/background/remove")
get_pricing("fal-ai/imageutils/rembg")
get_pricing("fal-ai/birefnet/v2")
get_pricing("fal-ai/bria/background/remove")
search_docs("retention errors fal Model API")
```

## One-off SDK validation

If `fal_client` is not installed in the active Python, use a temporary `uvx`
environment rather than adding a repo dependency:

```bash
uvx --from fal-client python - <<'PY'
import fal_client
print("fal_client import ok")
PY
```

Do not print credentials from this check.

## Paid smoke tests

Paid calls require user approval or an already approved budget. Before the call:

- check live schema
- check live pricing
- choose the smallest useful input
- set a hard spending cap for the run
- write outputs under a run artifact directory

## Receipt template

```text
Validation Receipt
- date: <UTC timestamp>
- model search: <ok|failed>, <details>
- schema lookup: <ok|failed>, <endpoint ids>
- pricing lookup: <ok|failed>, <endpoint ids and units>
- paid calls: <run|skipped>, <endpoint ids>
- output directory: <path>
- key handling: FAL_KEY was available and redacted
```
