#!/usr/bin/env bash
# cf_share.sh - upload local files/dirs to the team Cloudflare R2 share bucket
# and print a public share URL. Also deletes a share by slug.
#
# usage:
#   cf_share.sh [--slug SLUG] [--entry NAME] [--title TEXT]
#               [--description TEXT] [--image FILE] <file-or-dir> [more paths...]
#   cf_share.sh --delete SLUG
#
# Secrets are read from $CF_SHARE_ENV (default ~/.config/cf-share/env):
#   CF_SHARE_API_TOKEN   Cloudflare API token with Workers R2 Storage: Edit
#   CF_SHARE_ACCOUNT_ID  Cloudflare account id
#   CF_SHARE_BUCKET      R2 bucket name (fc-share)
#   CF_SHARE_BASE_URL    public base URL (https://share.fun.country)
# Requires Pillow for a distinct 1200x630 social card (see references/setup.md).
#
# Known gotchas handled here (do not "simplify" them away):
#   - curl sends "Expect: 100-continue" for bodies >1KB; api.cloudflare.com
#     resets those connections (exit 56). We always send "Expect:".
#   - R2 serves the Content-Type set at upload; without it everything becomes
#     application/octet-stream and HTML downloads instead of rendering.
#   - The REST object endpoint caps a single object around 300 MB.
set -euo pipefail

ENV_FILE="${CF_SHARE_ENV:-$HOME/.config/cf-share/env}"
MAX_BYTES=$((250 * 1024 * 1024))
API="https://api.cloudflare.com/client/v4"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESERVED="__cf_share"

die() { echo "cf-share error: $*" >&2; exit 1; }

usage() {
  sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

[ $# -ge 1 ] || usage 1

load_env() {
  [ -f "$ENV_FILE" ] || die "missing secret file $ENV_FILE
Set it up per the cf-share skill references/setup.md (token with Workers R2 Storage: Edit)."
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  for v in CF_SHARE_API_TOKEN CF_SHARE_ACCOUNT_ID CF_SHARE_BUCKET CF_SHARE_BASE_URL; do
    [ -n "${!v:-}" ] || die "$v is not set in $ENV_FILE"
  done
  CF_SHARE_PYTHON="${CF_SHARE_PYTHON:-python3}"
  CF_SHARE_BASE_URL="${CF_SHARE_BASE_URL%/}"
  OBJ_BASE="$API/accounts/$CF_SHARE_ACCOUNT_ID/r2/buckets/$CF_SHARE_BUCKET/objects"
  AUTH=(-H "Authorization: Bearer $CF_SHARE_API_TOKEN")
}

urlencode_path() { # percent-encode each path segment, keep the slashes
  "$CF_SHARE_PYTHON" -c 'import sys, urllib.parse; print("/".join(urllib.parse.quote(s, safe="") for s in sys.argv[1].split("/")))' "$1"
}

content_type() {
  local f="$1" ext
  ext="${f##*.}"; ext="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"
  case "$ext" in
    html|htm) echo "text/html; charset=utf-8" ;;
    css)      echo "text/css; charset=utf-8" ;;
    js|mjs)   echo "text/javascript; charset=utf-8" ;;
    json|map) echo "application/json; charset=utf-8" ;;
    txt|log)  echo "text/plain; charset=utf-8" ;;
    md)       echo "text/markdown; charset=utf-8" ;;
    csv)      echo "text/csv; charset=utf-8" ;;
    xml)      echo "application/xml" ;;
    pdf)      echo "application/pdf" ;;
    png)      echo "image/png" ;;
    jpg|jpeg) echo "image/jpeg" ;;
    gif)      echo "image/gif" ;;
    svg)      echo "image/svg+xml" ;;
    webp)     echo "image/webp" ;;
    ico)      echo "image/x-icon" ;;
    mp4)      echo "video/mp4" ;;
    webm)     echo "video/webm" ;;
    mov)      echo "video/quicktime" ;;
    mp3)      echo "audio/mpeg" ;;
    wav)      echo "audio/wav" ;;
    woff)     echo "font/woff" ;;
    woff2)    echo "font/woff2" ;;
    ttf)      echo "font/ttf" ;;
    wasm)     echo "application/wasm" ;;
    zip)      echo "application/zip" ;;
    gz|tgz)   echo "application/gzip" ;;
    *)        file -b --mime-type "$f" 2>/dev/null || echo "application/octet-stream" ;;
  esac
}

delete_slug() {
  local slug="$1" keys deleted=0
  keys=$(curl -sS "${AUTH[@]}" "$OBJ_BASE?prefix=$(urlencode_path "$slug/")&per_page=1000" \
    | python3 -c 'import sys, json; [print(o["key"]) for o in json.load(sys.stdin).get("result", [])]')
  [ -n "$keys" ] || die "no objects found under slug '$slug'"
  while IFS= read -r key; do
    curl -sS -X DELETE "${AUTH[@]}" -o /dev/null "$OBJ_BASE/$(urlencode_path "$key")"
    deleted=$((deleted + 1))
  done <<< "$keys"
  echo "deleted $deleted object(s) under $CF_SHARE_BASE_URL/$slug/"
}

SLUG=""
ENTRY=""
TITLE=""
DESCRIPTION=""
IMAGE=""
DELETE_SLUG=""
PATHS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --slug)   [ -n "${2:-}" ] || die "--slug needs a value"; SLUG="$2"; shift 2 ;;
    --entry)  [ -n "${2:-}" ] || die "--entry needs a value"; ENTRY="$2"; shift 2 ;;
    --title)  [ -n "${2:-}" ] || die "--title needs a value"; TITLE="$2"; shift 2 ;;
    --description) [ -n "${2:-}" ] || die "--description needs a value"; DESCRIPTION="$2"; shift 2 ;;
    --image)  [ -n "${2:-}" ] || die "--image needs a file"; IMAGE="$2"; shift 2 ;;
    --delete) [ -n "${2:-}" ] || die "--delete needs a slug"; DELETE_SLUG="$2"; shift 2 ;;
    -h|--help) usage 0 ;;
    -*)       die "unknown flag $1" ;;
    *)        PATHS+=("$1"); shift ;;
  esac
done

load_env
if [ -n "$DELETE_SLUG" ]; then
  [[ "$DELETE_SLUG" =~ ^[a-zA-Z0-9][a-zA-Z0-9_-]*$ ]] || die "invalid share slug '$DELETE_SLUG'"
  delete_slug "$DELETE_SLUG"
  exit 0
fi
[ ${#PATHS[@]} -ge 1 ] || die "nothing to upload"
"$CF_SHARE_PYTHON" -c 'from PIL import Image' >/dev/null 2>&1 || die "Pillow is required to render share previews; see references/setup.md"
[ -z "$IMAGE" ] || [ -f "$IMAGE" ] || die "preview image does not exist: $IMAGE"

# Build "localfile<TAB>relative key" pairs. A directory arg contributes its
# contents relative to itself; a file arg contributes its basename. Dotfiles
# and .DS_Store are skipped.
PAIRS=()
for p in "${PATHS[@]}"; do
  if [ -d "$p" ]; then
    while IFS= read -r f; do
      PAIRS+=("$f"$'\t'"${f#"${p%/}"/}")
    done < <(find "${p%/}" -type f -not -path '*/.*' -not -name '.DS_Store' | sort)
  elif [ -f "$p" ]; then
    PAIRS+=("$p"$'\t'"$(basename "$p")")
  else
    die "no such file or directory: $p"
  fi
done
[ ${#PAIRS[@]} -ge 1 ] || die "no files found to upload"

# Select the entry before uploading, so an invalid --entry cannot publish a
# partial share. Generated files live under a reserved prefix.
for pair in "${PAIRS[@]}"; do
  rel="${pair#*$'\t'}"
  case "$rel" in "$RESERVED"/*) die "input uses reserved path $RESERVED/: $rel" ;; esac
done

ENTRY_REL=""
ENTRY_FILE=""
if [ -n "$ENTRY" ]; then
  for pair in "${PAIRS[@]}"; do
    f="${pair%%$'\t'*}"; rel="${pair#*$'\t'}"
    if [ "$rel" = "$ENTRY" ]; then ENTRY_REL="$rel"; ENTRY_FILE="$f"; break; fi
  done
  if [ -z "$ENTRY_REL" ]; then
    matches=0
    for pair in "${PAIRS[@]}"; do
      f="${pair%%$'\t'*}"; rel="${pair#*$'\t'}"
      if [ "$(basename "$rel")" = "$ENTRY" ]; then
        ENTRY_REL="$rel"; ENTRY_FILE="$f"; matches=$((matches + 1))
      fi
    done
    [ "$matches" -le 1 ] || die "--entry '$ENTRY' matches multiple files; pass its relative path"
  fi
  [ -n "$ENTRY_REL" ] || die "--entry '$ENTRY' did not match any input file"
fi
if [ -z "$ENTRY_REL" ]; then
  for pair in "${PAIRS[@]}"; do
    f="${pair%%$'\t'*}"; rel="${pair#*$'\t'}"
    if [ "$rel" = "index.html" ]; then ENTRY_REL="$rel"; ENTRY_FILE="$f"; break; fi
  done
fi
if [ -z "$ENTRY_REL" ]; then
  for pair in "${PAIRS[@]}"; do
    f="${pair%%$'\t'*}"; rel="${pair#*$'\t'}"
    rel_lower="$(printf '%s' "$rel" | tr '[:upper:]' '[:lower:]')"
    case "$rel_lower" in *.html|*.htm) ENTRY_REL="$rel"; ENTRY_FILE="$f"; break ;; esac
  done
fi
if [ -z "$ENTRY_REL" ]; then
  ENTRY_FILE="${PAIRS[0]%%$'\t'*}"
  ENTRY_REL="${PAIRS[0]#*$'\t'}"
fi

if [ -z "$SLUG" ]; then
  slug_source="$TITLE"
  if [ -z "$slug_source" ]; then
    slug_source="$(basename "$ENTRY_FILE")"
    case "$slug_source" in index.html|index.htm) slug_source="$(basename "$(dirname "$ENTRY_FILE")")" ;; esac
  fi
  slug_label="$("$CF_SHARE_PYTHON" -c 'import re,sys,unicodedata; s=unicodedata.normalize("NFKD",sys.argv[1]).encode("ascii","ignore").decode().lower(); s=re.sub("[^a-z0-9]+","-",s).strip("-"); print((s[:48].rstrip("-") or "artifact"))' "$slug_source")"
  SLUG="$(date +%Y%m%d)-$slug_label-$(openssl rand -hex 6)"
fi
[[ "$SLUG" =~ ^[a-zA-Z0-9][a-zA-Z0-9_-]*$ ]] || die "invalid share slug '$SLUG'"

DIRECT_URL="$CF_SHARE_BASE_URL/$(urlencode_path "$SLUG/$ENTRY_REL")"
CARD_URL="$CF_SHARE_BASE_URL/$SLUG/$RESERVED/card.png"
entry_lower="$(printf '%s' "$ENTRY_REL" | tr '[:upper:]' '[:lower:]')"
case "$entry_lower" in
  *.html|*.htm) MODE=html; SHARE_URL="$DIRECT_URL" ;;
  *) MODE=page; SHARE_URL="$CF_SHARE_BASE_URL/$SLUG/$RESERVED/index.html" ;;
esac

TMP_SHARE="$(mktemp -d "${TMPDIR:-/tmp}/cf-share.XXXXXX")"
trap 'rm -rf "$TMP_SHARE"' EXIT
PREP_ARGS=(prepare --entry "$ENTRY_FILE" --relative "$ENTRY_REL" --url "$SHARE_URL"
  --card-url "$CARD_URL" --direct-url "$DIRECT_URL" --base-url "$CF_SHARE_BASE_URL"
  --slug "$SLUG" --output-dir "$TMP_SHARE" --mode "$MODE"
  --title "$TITLE" --description "$DESCRIPTION" --image "$IMAGE")
for pair in "${PAIRS[@]}"; do PREP_ARGS+=(--file "${pair#*$'\t'}"); done
"$CF_SHARE_PYTHON" "$SCRIPT_DIR/share_preview.py" "${PREP_ARGS[@]}" || die "could not prepare preview"

uploaded=0
failed=0
upload_one() {
  local f="$1" rel="$2" size key ct ok=0 resp=""
  size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f")
  if [ "$size" -gt "$MAX_BYTES" ]; then
    echo "FAIL $rel ($((size / 1024 / 1024)) MB > 250 MB REST cap; use the R2 S3 API)" >&2
    return 1
  fi
  key="$SLUG/$rel"
  ct="$(content_type "$f")"
  for _ in 1 2; do
    resp=$(curl -sS -X PUT "${AUTH[@]}" -H "Content-Type: $ct" -H "Expect:" \
      --data-binary @"$f" "$OBJ_BASE/$(urlencode_path "$key")" 2>&1) || { sleep 1; continue; }
    if printf '%s' "$resp" | grep -q '"success": *true'; then ok=1; break; fi
    sleep 1
  done
  if [ "$ok" = 1 ]; then return 0; fi
  echo "FAIL $rel: $(printf '%s' "$resp" | head -c 300)" >&2
  return 1
}

for pair in "${PAIRS[@]}"; do
  f="${pair%%$'\t'*}"; rel="${pair#*$'\t'}"
  if [ "$MODE" = html ] && [ "$rel" = "$ENTRY_REL" ]; then f="$TMP_SHARE/entry.html"; fi
  if upload_one "$f" "$rel"; then uploaded=$((uploaded + 1)); else failed=$((failed + 1)); fi
done
[ "$failed" -eq 0 ] || die "$failed artifact file(s) failed under slug '$SLUG'; preview not verified"
[ "$uploaded" -ge 1 ] || die "all uploads failed"
upload_one "$TMP_SHARE/card.png" "$RESERVED/card.png" || die "preview card upload failed under slug '$SLUG'"
if [ "$MODE" = page ]; then
  upload_one "$TMP_SHARE/share.html" "$RESERVED/index.html" || die "share page upload failed under slug '$SLUG'"
fi

"$CF_SHARE_PYTHON" "$SCRIPT_DIR/share_preview.py" verify --info "$TMP_SHARE/info.json" || die "live preview verification failed under slug '$SLUG'"
echo "URL: $SHARE_URL"
echo "shared $uploaded artifact file(s) under $CF_SHARE_BASE_URL/$SLUG/"
[ "$SHARE_URL" = "$DIRECT_URL" ] || echo "file: $DIRECT_URL"
echo "delete later with: cf_share.sh --delete $SLUG"
