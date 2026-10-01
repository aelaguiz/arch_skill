---
name: cf-share
description: "Share or update local static artifacts through public, unguessable Cloudflare R2 links with readable previews and fresh content. Preserve an existing URL when requested, without caching pages or assets. Use for an HTML report, screenshot, PDF, video, or static bundle when the user wants a link to send. Not for product content deployment, private material, or claude.ai Artifacts."
metadata:
  short-description: "Share fresh artifacts at new or stable public URLs"
---

# CF Share

Publish a local artifact at `https://share.fun.country/<slug>/...` so a recipient can recognize it from the URL and link preview, then open the content. New slugs include a short title label plus random bytes. A share is unlisted but **public to anyone with its URL**. Check the artifact and its proposed preview text/image for secrets or private data before upload; confirm with the user if exposure is plausible.

An update is complete when the recipient gets the current page and everything it loads. Preserve the exact headline URL when the user asks to keep a link: reuse its slug and entry path. Otherwise create a new share. The helper sends `Cache-Control: no-store` on every uploaded file, purges this upload's CDN URLs when reusing a slug, and checks public bytes for every object. Changing the report URL is not a repair for a requested stable link.

The headline URL must be an HTML page with a useful title, one-sentence description, and distinct image. The upload script makes a 1200×630 PNG card and adds Open Graph and X Card tags. An HTML report keeps its direct URL and relative assets. For an image, PDF, video, or other file, the headline URL opens a share page with inline media when appropriate and a direct file link. Local media and document embeds get a content version in their query string so a browser cannot reuse an old playback buffer; headline and direct download URLs stay stable.

## When to use

- The user wants a local report, screenshot, PDF, video, or static bundle shared or updated by link.
- Another workflow produced an artifact and the user wants a URL to send in Slack or elsewhere.

Do not use this bucket for app or product content (such as the `ps-content` CDN), material that must stay private, or a claude.ai Artifact.

## Publish

1. Inspect the artifact and its dependencies. Upload the containing directory when HTML loads sibling files; freshness covers CSS imports, images, fonts, scripts, fetched data, and linked documents as well as the entry page. Pick the intended entry with `--entry`. For a stable link, take `--slug` and the entry path from the existing URL and keep them unchanged. HTTP headers govern uploaded objects; externally hosted resources and an artifact's own service worker or application cache need inspection and correction at their owning source. If scripts assign media URLs dynamically, version those references in the artifact too; the helper versions static HTML embeds.
2. Write the preview as a recipient would read it: identify the actual subject in `--title`, give the reason to open it in `--description`, and use `--image` for a relevant local screenshot or figure when one exists. The script can infer fields from HTML and filenames, but requires `--description` when the page has no descriptive text. Inspect its printed `preview:` and `summary:` lines; replace generic or misleading inference. The chosen image is composited into the card and need not be a separate uploaded artifact.
3. Upload and use the printed `URL:` as the headline link:

```bash
bash "{baseDir}/scripts/cf_share.sh" \
  --title "Specific artifact title" \
  --description "One sentence about what a reader will find." \
  --image /path/to/representative.png \
  /path/to/report-or-directory
```

The editorial flags are optional when the inferred preview is already accurate. For example, updating `https://share.fun.country/existing-slug/reports/index.html` uses `--slug existing-slug --entry reports/index.html` with the bundle root. A non-HTML share keeps its generated `__cf_share/index.html` headline and the original file path. The preview card gets a new filename when its rendered content changes. `--delete <slug>` removes a share when requested.

4. Give the recipient the headline URL with its title. For a non-HTML artifact, provide the printed `file:` URL only when direct download or embedding is specifically useful. If the user asked you to post it somewhere, use the appropriate messaging workflow after verifying the URL.

## Completion check

The script makes ordinary GET requests at the exact public URLs, checks `no-store` and CDN cache status, and compares every served object with the uploaded bytes, including generated HTML and the card. It also checks Open Graph/X Card values and PNG dimensions. Do not hand out a URL if verification fails; repair the reported URL while preserving a requested stable link. When updating an interactive report, open or reload that same link normally and check the changed content and assets in the browser too.

Server headers cannot evict copies already stored in a recipient's browser before this policy existed, or force Slack and other services to rebuild an existing unfurl. Read [references/setup.md](references/setup.md) for those migration and preview cases. For a requested Slack share, inspect the posted message's actual unfurl when possible.

For credentials, the optional Python environment, and troubleshooting, read [references/setup.md](references/setup.md). The secret env file is `~/.config/cf-share/env` by default (`CF_SHARE_ENV` overrides it); do not hunt for other Cloudflare credentials if it is missing.
