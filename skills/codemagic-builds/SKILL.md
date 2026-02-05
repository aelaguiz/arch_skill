---
name: codemagic-builds
description: "Codemagic CI/CD build monitoring and build control via the Codemagic REST API (status dashboards by environment and platform, in-progress build summaries, failure/error summaries, starting builds, and canceling builds). Use when a request mentions Codemagic builds, workflows, apps, build failures, build logs, or downloading/updating the Codemagic API v3 OpenAPI schema from the Codemagic Swagger UI."
metadata:
  short-description: "Query and manage Codemagic builds"
---

# Codemagic Builds

## Quick start

(All paths below are relative to this skill folder unless noted.)


1) Set auth + base URL (avoid pasting tokens in chat):

If the user needs to generate an API token, tell them:

1. go to codemagic.io and sign in
2. Select Teams -> Individual account (see image)
3. Select Integrations -> Codemagic API token (see image)

Then ask them to copy the token and set it as `CODEMAGIC_API_TOKEN` (preferred) or share it.

- `CODEMAGIC_API_TOKEN` (required)
- `CM_API_BASE_URL` (optional; default: `https://api.codemagic.io`)
- `CM_API_AUTH` (optional; `x-auth-token` (default) or `bearer`)

2) Download the latest API v3 schema (OpenAPI JSON) when you need the most up-to-date endpoints:

- Run `scripts/codemagic_fetch_openapi.py`.

3) Use `scripts/codemagic.py` to:

- Summarize builds in progress
- Summarize failures (best-effort error extraction)
- Start new builds
- Cancel running builds
- Produce an environment × platform dashboard

## Workflow

### 1) Keep the API reference fresh

If the user says “latest API”, “v3”, “schema”, or you’re unsure about an endpoint shape, refresh the schema:

- `python3 scripts/codemagic_fetch_openapi.py --out references/codemagic-openapi.json`

If schema download fails (site changes, auth, etc.), fall back to using `scripts/codemagic.py request ...` to probe endpoints and ask the user for the correct base URL.

### 2) Configure environment × platform mapping (recommended)

For reliable “status per environment and app type (android/ios)”, create a matrix file (example path: `codemagic.matrix.json`):

```json
{
  "environments": {
    "staging": {
      "android": {"appId": "...", "workflowId": "..."},
      "ios": {"appId": "...", "workflowId": "..."}
    },
    "production": {
      "android": {"appId": "...", "workflowId": "..."},
      "ios": {"appId": "...", "workflowId": "..."}
    }
  }
}
```

If the user doesn’t have `appId`/`workflowId` yet, use the API schema to locate “apps”/“workflows” endpoints, or use `scripts/codemagic.py request GET /apps` (or the v3 equivalent) to discover IDs.

### 3) Report status + in-progress summary

- Dashboard by env/platform: `python3 scripts/codemagic.py dashboard --matrix codemagic.matrix.json`
- In-progress builds: `python3 scripts/codemagic.py builds in-progress --limit 20`

### 4) High-signal build listing (minimal)

- Minimal list (newest first): `python3 scripts/codemagic.py builds list --output minimal --limit 20`
- Filter by app/workflow: `python3 scripts/codemagic.py builds list --output minimal --app-id <APP_ID> --workflow-id <WORKFLOW_ID>`
- Filter by file workflow + time: `python3 scripts/codemagic.py builds list --output minimal --file-workflow-id <FILE_WORKFLOW_ID> --since 2026-02-04T00:00:00Z`

### 5) Inspect build steps + logs

- Steps + log URLs: `python3 scripts/codemagic.py builds get --build-id <BUILD_ID> --steps`
- Tail log lines: `python3 scripts/codemagic.py builds get --build-id <BUILD_ID> --step-logs --tail 120`
- Target a step: `python3 scripts/codemagic.py builds get --build-id <BUILD_ID> --step-logs --step-name-contains \"archive\"`

### 6) Summarize build errors

- Recent failures: `python3 scripts/codemagic.py builds failures --limit 20`

Error summaries are best-effort and derived from build metadata fields (e.g., status, failing step, error message). If the API exposes a logs endpoint, use `scripts/codemagic.py request` to fetch logs and summarize the relevant failure chunk.

### 7) Start/cancel builds

- Start a build:
  - `python3 scripts/codemagic.py builds start --app-id <APP_ID> --workflow-id <WORKFLOW_ID> --branch <BRANCH>`
- Cancel a build:
  - `python3 scripts/codemagic.py builds cancel --build-id <BUILD_ID>`

If the API uses a different cancel route in v3, locate it in `references/codemagic-openapi.json` and re-run using `scripts/codemagic.py request`.

### 8) Manage app env vars

- List apps: `python3 scripts/codemagic.py apps list`
- List vars: `python3 scripts/codemagic.py apps vars list --app-id <APP_ID>`
- Add var: `python3 scripts/codemagic.py apps vars add --app-id <APP_ID> --group flutter_build --key API_URL --value https://... --secure`
- Delete var: `python3 scripts/codemagic.py apps vars delete --app-id <APP_ID> --var-id <VAR_ID>`

**Codemagic limitation:** updating an env var can require delete + recreate (treat “add” as create-only if updates aren’t supported).

**Group guidance:** use a dedicated group (e.g., `shorebird`) when variables are tool-specific; reuse existing `flutter_*` groups when they already exist for build/runtime config to avoid duplicate group sprawl.

### 9) Raw requests (quiet JSON)

- `python3 scripts/codemagic.py request GET /builds --query limit=5 --quiet`

## Resources

- `scripts/codemagic_fetch_openapi.py`: Download the Codemagic API v3 schema as a JSON “bundle” (the full OpenAPI document).
- `scripts/codemagic.py`: Query builds, summarize in-progress/failures, start/cancel builds, and run a dashboard.
- `references/codemagic-rest-api.md`: Auth/base URL notes + practical tips.
