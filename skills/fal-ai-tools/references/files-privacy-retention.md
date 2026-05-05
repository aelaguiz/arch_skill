# Files, Privacy, And Retention

Use this reference when a fal task needs local files, generated media, or
privacy-sensitive handling.

## Input files

fal model inputs usually need URLs. Valid options:

- public URL
- fal CDN upload URL
- presigned URL that fal workers can fetch without extra headers

Private URLs that require custom auth headers are not valid model inputs. Upload
the file to fal CDN or create a presigned URL instead.

For local files, prefer fal CDN upload:

```python
import fal_client

url = fal_client.upload_file("/absolute/path/to/input.png")
```

Data URIs may work for some small inputs, but they are not the default. Avoid
them for large files and any model that does not clearly support them.

## Output files

Generated output URLs and fal CDN URLs should be treated as public. If the user
needs local copies, download them into the run artifact directory and report
both the local path and remote URL.

## Retention controls

Use the current fal docs as source truth before making privacy claims.

Known controls from the docs:

- `X-Fal-Object-Lifecycle-Preference` controls generated-media expiration.
- `X-Fal-Store-IO: 0` prevents JSON request payload storage.
- CDN output files still follow media retention behavior even when request JSON
  storage is disabled.
- request payloads are stored for 30 days by default.

Use these controls only when they fit the user's request. Do not imply that they
make public media URLs private.

## Secret hygiene

Never print, store, or paste credential values. Avoid commands that expose the
key through process output. Redact headers in receipts and logs.

Good receipt language:

```text
key handling: FAL_KEY was available and redacted
```

Bad receipt language:

```text
Authorization: Key ...
```

Do not put fal keys into docs, prompts, model inputs, screenshots, issue
comments, PR bodies, or generated artifacts.
