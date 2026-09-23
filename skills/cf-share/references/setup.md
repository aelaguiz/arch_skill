# CF Share Setup

One-time setup for a new machine or teammate, plus a receipt of what
infrastructure exists so it never has to be re-derived.

## What exists

- Cloudflare account: FunCountry, account id `cec2277a8b3429743f0ea1ddc3c1b72f`.
- R2 bucket: `fc-share`, dedicated to ad-hoc team artifact sharing. Product
  buckets (`ps-content`, `ps-avatars`, ...) are separate; never mix.
- Public custom domain: `share.fun.country` (zone `fun.country`), attached to
  the bucket as an R2 custom domain. Objects are readable by anyone with the
  URL; there is no directory listing and unknown keys return 404.
- Shares are keyed `slug/relative-path` where the slug embeds random bytes
  (`YYYYMMDD-<12 hex>`), so links are unlisted but public.

## Requirements

- `curl` and `python3` on PATH, plus Pillow in the Python environment used by
  `cf_share.sh`. The script uses Pillow to render a distinct 1200×630 PNG
  preview card for each share. Check with `python3 -c 'from PIL import Image'`.
  If it is missing, create a small dedicated environment:

```bash
python3 -m venv ~/.config/cf-share/venv
~/.config/cf-share/venv/bin/python -m pip install Pillow
```

  Then put `CF_SHARE_PYTHON="$HOME/.config/cf-share/venv/bin/python"` in the
  secret env file below. An existing Python with Pillow needs no override.
- A Cloudflare API token with permission **Account -> Workers R2 Storage:
  Edit** on the FunCountry account. Nothing else is needed for upload,
  delete, and list.

## Get a token

Either:

- Ask Amir for the shared cf-share token, or
- If you have FunCountry Cloudflare access, create your own: dash.cloudflare.com
  -> My Profile -> API Tokens -> Create Token -> Custom token -> add
  permission `Account / Workers R2 Storage / Edit`, scope it to the FunCountry
  account. Copy the token value once; Cloudflare will not show it again.

## Create the secret file

```bash
mkdir -p ~/.config/cf-share
cat > ~/.config/cf-share/env <<'EOF'
CF_SHARE_API_TOKEN=<token value>
CF_SHARE_ACCOUNT_ID=cec2277a8b3429743f0ea1ddc3c1b72f
CF_SHARE_BUCKET=fc-share
CF_SHARE_BASE_URL=https://share.fun.country
# Optional if Pillow is installed in the dedicated environment:
# CF_SHARE_PYTHON="$HOME/.config/cf-share/venv/bin/python"
EOF
chmod 600 ~/.config/cf-share/env
```

The script also honors `CF_SHARE_ENV=<path>` if the file must live elsewhere.

## Verify the setup

```bash
echo '<html><head><title>CF Share preview test</title></head><body><h1>CF Share preview test</h1></body></html>' > /tmp/cf-share-test.html
bash scripts/cf_share.sh --description 'A harmless test of rich share links.' /tmp/cf-share-test.html
```

Expect `URL: https://share.fun.country/<slug>/cf-share-test.html` and
`verified HTTP 200: share page, Open Graph, X Card, 1200x630 PNG, artifact`.
The URL opens the original HTML with preview tags added in the uploaded copy.
Clean up with the printed `--delete <slug>` command when the test is no longer
needed.

## Troubleshooting

- `10000 Authentication error` / 403: the token is wrong, expired, or missing
  the R2 Storage Edit permission.
- HTML downloads instead of rendering: the object was uploaded without a
  Content-Type. Re-upload through the script; never PUT objects by hand
  without `-H "Content-Type: ..."`.
- A link shows an old preview after reusing `--slug`: Slack and other sharing
  services may cache the URL. Use a new slug for a fresh card, or use the
  service's preview debugger or refresh tool when available. Reposting the
  same URL in the same Slack conversation may not expand for an hour.
- `Pillow is required`: run the dedicated-environment commands above and set
  `CF_SHARE_PYTHON` in the env file.
- curl exit 56 on files over ~1 MB: something dropped the `-H "Expect:"`
  header the script sends; api.cloudflare.com resets 100-continue uploads.
- Files over ~250 MB: the REST endpoint caps object size around 300 MB. Use
  the R2 S3-compatible API with multipart upload for those rare cases.

## Infra receipt (how this was created, 2026-07-16)

Only needed if the bucket or domain ever has to be recreated. Requires a
broader token (R2 admin + DNS edit on `fun.country`):

```bash
# bucket
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"fc-share"}' \
  "https://api.cloudflare.com/client/v4/accounts/<account_id>/r2/buckets"
# public custom domain (auto-creates the DNS record and TLS cert)
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"domain":"share.fun.country","zoneId":"<fun.country zone id>","enabled":true,"minTLS":"1.2"}' \
  "https://api.cloudflare.com/client/v4/accounts/<account_id>/r2/buckets/fc-share/domains/custom"
```
