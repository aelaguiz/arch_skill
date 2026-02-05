# Codemagic REST API notes (for the agent)

## Base URLs

Codemagic has multiple “API surfaces” in the wild.

- Legacy/commonly-documented REST API base (often used in docs/examples): `https://api.codemagic.io`
- Swagger UI for the v3 schema: `https://codemagic.io/api/v3/schema#/` (use `https://codemagic.io/api/v3/schema` when fetching the HTML)

Because the v3 schema UI is JS-driven and may change, prefer:

1) Downloading the OpenAPI JSON using `scripts/codemagic_fetch_openapi.py`.
2) Using the downloaded schema to confirm the correct v3 base path and endpoints.

## Auth headers

Common patterns:

- `x-auth-token: <token>` (documented in older Codemagic REST API docs)
- `Authorization: Bearer <token>` (common for modern APIs; use only if confirmed in the v3 schema)

`scripts/codemagic.py` supports both via `CM_API_AUTH`.

## Practical workflow

- If an endpoint 404s:
  - Verify `CM_API_BASE_URL` (does it already include `/api/v3`?)
  - Consult `references/codemagic-openapi.json` (freshly downloaded)
  - Use `scripts/codemagic.py request` to probe a candidate path

- If you need a “JSON bundle” of the API spec:
  - In this skill, “bundle” means the full OpenAPI JSON document downloaded from the schema UI’s configured spec URL.

