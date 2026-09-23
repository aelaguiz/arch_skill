# CF Share rich previews: implementation plan

## Outcome and scope

Every new `cf-share` headline URL should tell a recipient what the artifact is before they click: a short human-readable label in the slug, plus a useful title, one-sentence description, and a distinct image in link previews. Opening the link should still reach the actual report or file. The skill must work for an HTML report with relative assets, a single screenshot, a PDF, and a mixed static bundle. Existing published URLs remain available; re-uploading an existing slug can update its bytes, but external preview caches may continue to show the older card.

The owning source is `skills/cf-share/` in `arch_skill`; `~/.agents/skills/cf-share/` is an installed copy. The skill owns the agent's judgment about safe content and editorial title/description. Its scripts own repeatable HTML, image, upload, and verification mechanics. A Slack app is out of scope because standard page metadata works across Slack and other consumers without per-workspace setup.

## Evidence behind the design

- [Slack's classic unfurl](https://docs.slack.dev/messaging/unfurling-links-in-messages/) crawls the URL for Open Graph and X Card metadata. [Slack's help page](https://slack.com/help/articles/204399343-Share-links-and-set-preview-preferences) says a link without preview data may not expand and lists workspace/user settings and repeated-link suppression as other causes.
- The [Open Graph protocol](https://ogp.me/) defines `og:title`, `og:type`, `og:image`, and `og:url`, with `og:description` and image dimensions/alt text available. [LinkedIn's sharing help](https://www.linkedin.com/help/linkedin/answer/a525063) also names Open Graph as a source for title, description, and image; its [image guidance](https://www.linkedin.com/help/linkedin/answer/a566445) recommends a roughly 1.91:1, 1200-pixel-wide image.
- [Cloudflare R2 objects](https://developers.cloudflare.com/r2/objects/) are individual keys in a flat bucket. The current public custom domain serves bytes at the object path, so object metadata alone cannot turn a PDF or PNG into an HTML page with social tags. The current script already sets `Content-Type`, which must stay correct.

## Work plan

1. **Establish a repeatable preview contract.** Extend the CLI with `--title`, `--description`, and `--image` inputs. Infer a title and description from HTML when available; require a description when the artifact has no descriptive text rather than publishing empty filler. Use a short title-derived slug label plus random bytes; the skill should curate generic or misleading inference. Keep each share public and unlisted, and avoid publishing sensitive details in the card.
2. **Generate the preview without changing source files.** Add a deterministic helper that renders a branded 1200×630 PNG card, optionally incorporating a chosen local image. For an HTML entry, upload a temporary copy with Open Graph, X Card, description, and canonical tags in `<head>`. Preserve the report's path and relative assets. For other entries, upload a small HTML share page with the same metadata and an obvious link or inline media view. Keep the original file URL available.
3. **Make upload and verification fail loudly.** Select the entry before upload, publish the card and share page under a reserved key, and return only a verified HTML headline URL. Verify the entry is HTTP 200, the page contains the expected title/description/image URLs, the card is a readable PNG, and the underlying file is still reachable. Report partial upload failures instead of handing out an incomplete share.
4. **Teach the reusable skill.** Update `SKILL.md` with the quality bar, how to choose an editorial title, description, and representative image, and what to send as the headline link. Update setup for the rendering dependency and preview troubleshooting. Keep the entry prompt short and the script's stdout compact. Inspect installed runtime copies and update only this skill's reviewed files.
5. **Prove the user experience.** Run package validation and fixture tests for HTML with assets, single image, PDF, escaping, and malformed metadata. Publish a harmless fresh test share through the real R2 path, inspect its live HTML and image, send its URL in Amir's Slack DM, and verify the rendered unfurl there. Record any platform-specific caveat accurately instead of promising every client will show an identical card.

## Completion criteria

- A fresh HTML report URL opens the report directly and has one coherent set of preview tags in its served `<head>`.
- A fresh non-HTML headline URL opens a readable share page, and the original file remains one click away or visible inline.
- The live image is 1200×630 PNG and is fetched successfully from its absolute HTTPS URL.
- The Slack test message shows the intended title and image; another consumer can read the same Open Graph tags. The skill's installed copy matches the reviewed source.

## Rollback

The change is additive to new uploads: existing R2 keys and URLs are left alone. Reverting the script and skill source restores the old upload behavior. The test share uses its own random slug, so it can be deleted independently if needed.

## Execution receipt, 2026-09-22

- Implemented in `skills/cf-share/SKILL.md`, `references/setup.md`, `scripts/cf_share.sh`, and the new `scripts/share_preview.py`. The deterministic helper is needed because the same metadata insertion, card rendering, and live validation must happen for every upload; prose alone cannot make a raw R2 object crawler-readable.
- Four focused helper tests passed: HTML metadata replacement without changing local source or relative assets; an image share page with escaped editorial text; a PDF share page with an inline view and direct link; and failure before upload when non-HTML has no description. `bash -n`, `shellcheck`, `git diff --check`, `npx skills check`, and `make verify_install` passed. The `npx` command also printed unrelated upstream skill deletion warnings and made no deletion.
- The live HTML share at [CF Share preview demo](https://share.fun.country/20260922-cf-share-preview-demo-5fe6b286d53a/index.html) returned HTTP 200 with the expected Open Graph and X Card fields, a 1200×630 PNG, and working CSS/image assets. Its slug now carries a title label plus 12 random hexadecimal characters.
- A harmless image-only share proved the non-HTML landing page, inline image, direct file URL, and live metadata. That test share was then deleted through `--delete`; the page returned HTTP 404 afterward.
- A separate live HTML test URL was posted in Amir's own Slack DM. Slack displayed “CF Share preview demo,” the selected description, “Fun Country Shares,” and the image thumbnail. Both task-created Slack browser tabs were closed; the pre-existing self-DM draft was preserved. This proves Slack's classic unfurl for the new metadata shape. Other clients may choose a different visual layout or suppress cached previews.
- The reviewed files were installed only for `cf-share` into `~/.agents/skills`, `~/.claude/skills`, `~/.gemini/skills` (with frontmatter removed per that runtime's installer), and the existing Hermes skill root. Byte comparisons passed for every installed file.
