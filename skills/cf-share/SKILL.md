---
name: cf-share
description: "Share local static artifacts through public, unguessable Cloudflare R2 links with readable link previews: a specific title, description, and image for Slack and other Open Graph consumers. Use for an HTML report, screenshot, PDF, video, or static bundle when the user wants a link to send. Not for product content deployment, private material, or claude.ai Artifacts."
metadata:
  short-description: "Share artifacts with rich public link previews"
---

# CF Share

Publish a local artifact at `https://share.fun.country/<slug>/...` so a recipient can recognize it from the URL and link preview, then open the content. New slugs include a short title label plus random bytes. A share is unlisted but **public to anyone with its URL**. Check the artifact and its proposed preview text/image for secrets or private data before upload; confirm with the user if exposure is plausible.

The headline URL must be an HTML page with a useful title, one-sentence description, and distinct image. The upload script makes a 1200×630 PNG card and adds Open Graph and X Card tags. An HTML report keeps its direct URL and relative assets. For an image, PDF, video, or other file, the headline URL opens a share page with inline media when appropriate and a direct file link.

## When to use

- The user wants a local report, screenshot, PDF, video, or static bundle shared by link.
- Another workflow produced an artifact and the user wants a URL to send in Slack or elsewhere.

Do not use this bucket for app or product content (such as the `ps-content` CDN), material that must stay private, or a claude.ai Artifact.

## Publish

1. Inspect the artifact. If HTML references sibling CSS, images, scripts, or documents, upload the containing directory so relative links work. Pick the intended entry with `--entry` when the default `index.html` or first HTML file is wrong.
2. Write the preview as a recipient would read it: identify the actual subject in `--title`, give the reason to open it in `--description`, and use `--image` for a relevant local screenshot or figure when one exists. The script can infer fields from HTML and filenames, but requires `--description` when the page has no descriptive text. Inspect its printed `preview:` and `summary:` lines; replace generic or misleading inference. The chosen image is composited into the card and need not be a separate uploaded artifact.
3. Upload and use the printed `URL:` as the headline link:

```bash
bash "{baseDir}/scripts/cf_share.sh" \
  --title "Specific artifact title" \
  --description "One sentence about what a reader will find." \
  --image /path/to/representative.png \
  /path/to/report-or-directory
```

The editorial flags are optional when the inferred preview is already accurate. `--entry <relative-name>` selects the main artifact; `--slug <slug>` republishes at an existing path. A republished URL may show an older card in services that cache previews, so use a fresh slug when an immediately updated preview matters. `--delete <slug>` removes a share when requested.

4. Give the recipient the headline URL with its title. For a non-HTML artifact, provide the printed `file:` URL only when direct download or embedding is specifically useful. If the user asked you to post it somewhere, use the appropriate messaging workflow after verifying the URL.

## Completion check

The script verifies HTTP 200 for the headline HTML page, the original artifact, and the card; it also checks the served Open Graph/X Card values and the PNG dimensions. Do not hand out a URL if verification fails. A successful technical check cannot force every client to display a preview: Slack can suppress repeated links in one conversation, and workspace or user settings can hide previews. For a requested Slack share, inspect the posted message's actual unfurl when possible.

For credentials, the optional Python environment, and troubleshooting, read [references/setup.md](references/setup.md). The secret env file is `~/.config/cf-share/env` by default (`CF_SHARE_ENV` overrides it); do not hunt for other Cloudflare credentials if it is missing.
