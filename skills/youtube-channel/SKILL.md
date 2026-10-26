---
name: youtube-channel
description: "Run Poker Skill's YouTube channel (@pokerskill_) through YouTube's own Data, Analytics and Reporting APIs instead of YouTube Studio, with the bundled yt.py helper and the channel's signed-in grant. Upload and schedule videos and Shorts; change titles, descriptions, tags, privacy, languages, thumbnails, captions and playlists; read, answer and moderate comments; edit the channel page; pull the channel's analytics and bulk reports; look up other channels' public videos. Use when asked to upload, publish, unlist, schedule, retitle, caption, add to a playlist, reply to YouTube comments, get YouTube numbers, or do anything on our channel without the browser. Not for YouTube ads (Google Ads), making the video itself, or what only Studio does: title and thumbnail A/B tests, dubs, end screens, cards and community posts."
metadata:
  short-description: "Run our YouTube channel through YouTube's APIs"
---

# YouTube channel

This skill is the channel's hands. Everything YouTube Studio does that YouTube's APIs also do (uploads, schedules, every setting on a video, captions, playlists, comments, the channel page, analytics) goes through one helper:

```bash
python3 "{baseDir}/scripts/yt.py" <command> ...   # yt.py -h lists every command
python3 "{baseDir}/scripts/yt.py" whoami           # which channel the grant reaches, and its scopes
```

The helper signs in with the channel's grant (setup and what to do on another machine: [references/setup.md](references/setup.md)), handles YouTube's upload protocol and its edit semantics, and prints short summaries. `--json-out <file>` saves the full response when you need a field the summary leaves out; `--dry-run` on `upload`, `update` and `channel update` shows exactly what would change without sending it.

## What viewers can see is the channel owner's call

The channel speaks for Poker Skill in public, and on YouTube the public moment can't be taken back: subscribers get notified, the first hours shape how YouTube distributes a video, and a deleted video takes its views, comments and history with it for good. So the line that matters is between work nobody outside sees and anything a viewer would.

Work you do freely: uploading as **private** or **unlisted** (with `notifySubscribers` off, the helper's default) so the owner can watch it; editing anything on a private or unlisted video; captions, playlists and settings on those; reading anything; making and removing your own test objects.

The owner's yes first, in PS Brain through `$approvals` with the exact thing shown: making a video public or scheduling it to go public, changing a public video's title, description or thumbnail, any comment or reply posted as the channel, hiding or rejecting a viewer's comment that isn't plain spam, banning anyone, changing the channel page (description, keywords, banner, trailer, watermark), and deleting a video or a public playlist. A yes covers what it showed; a new title on a video he approved is a new ask. The words viewers read follow the house rules for public words (in PS Brain: `$word-list`, and the voice the channel's work already set), and a reply as the channel sounds like a person, never a template.

The cases look different each time. Unlisting an old video at the owner's request is his decision carried out, not a new one. Replying "thanks!" to a kind comment is still the brand speaking. Scheduling a release for tomorrow is going public, only later. Fixing a typo in a public title is a public change. The question before any write: would a viewer see this, and did the owner say yes to exactly this?

## Working with the helper

**Every edit reads first.** YouTube replaces a whole part of a resource on update (send `snippet` without `tags` and the tags are gone; send `status` without `privacyStatus` and the privacy resets), so `update`, `playlist update` and `channel update` read the current state, change only the fields you pass, and print each field's old and new value. Use `raw` for anything else, and do the same read-merge-write yourself before any `PUT`. The channel's banner can't be read back through the API, so after a `channel update` on a channel that has one, look at the channel page to see it survived.

**A read right after a write can lag.** For a minute or two after an edit, YouTube's reads may still show the old tags, keywords or settings while the write's own response shows the new ones, and a video added to a playlist has taken up to two hours to appear in its listing. Trust the response, and re-read later before calling an edit lost. Listing our videos through the channel's uploads can also repeat or skip one (scheduled videos most); `video <id>` is the sure read of one video.

**A video's file can't be replaced.** Fixing the picture or sound means a new upload; the old video keeps its views and comments, so whether to unlist or delete it is part of the owner's call above.

**Quota is shared and resets at midnight Pacific.** Each Google Cloud project gets 10,000 units a day for ordinary calls, plus separate buckets of 100 uploads and 100 searches. Reads cost 1 unit, most writes 50, a caption upload 400. A day of normal channel work fits easily; a loop that polls `search` or rewrites metadata on every video does not. YouTube also caps how many videos a channel can upload in a day, separately from quota (`uploadLimitExceeded`).

**Errors say what YouTube said.** The helper prints YouTube's reason and, for the common ones, what it means. Retry only what was transient; a `forbidden` on a feature the channel hasn't unlocked will fail the same way tomorrow.

## The usual jobs

**Publish a video.** Upload it private or unlisted with its title, description, language, category and the disclosure flags YouTube asks for (`--made-for-kids`/`--no-made-for-kids`, `--synthetic`/`--no-synthetic`), add captions and the playlist in the same command, and `--wait` until processing finishes:

```bash
python3 "{baseDir}/scripts/yt.py" upload video.mp4 --title "..." --description-file desc.txt \
  --privacy unlisted --language en --audio-language en --category 27 --no-made-for-kids --no-synthetic \
  --captions captions.vtt:en --playlist PL... --wait
```

Check the result with `yt.py video <id>` (processing state, file size and shape, captions, settings). Once the owner says yes, `update <id> --privacy public`, or `--publish-at 2026-11-01T15:00:00Z` to schedule (the helper keeps a scheduled video private until then, as YouTube requires).

An API upload ignores the defaults set in Studio for new uploads, so say on every upload what the video should carry: category, languages, the disclosure flags, the playlist. Two limits come from the channel itself: until it is phone-verified (`whoami` says whether videos over 15 minutes are allowed), a longer video is accepted and then rejected in processing, and custom thumbnails are refused.

**Shorts are different.** A square or vertical video of three minutes or less becomes a Short on its own; no API field sets or reads that. Google's staff say (October 2026) that Shorts uploaded through the API get little of the Shorts feed until the channel has built up trust, and one developer's side-by-side showed 37 views from an API upload against about 1,000 from Studio. So a Short whose first hours matter goes up through Studio in the browser; its thumbnail is set there too, since the API silently ignores thumbnails on Shorts. The API still edits it, captions it and reads its numbers afterwards.

**Change something on a video.** `update <id>` with only the fields that change: `--title`, `--description-file`, `--tags` or `--add-tags`, `--privacy`, `--publish-at` or `--clear-publish-at`, `--localize es:"Título":desc_es.txt` for another language's title and description, and the disclosure flags. Run it with `--dry-run` first when it touches a public video.

**Comments.** `comments` lists threads across the channel (or `--video <id>`, `--status heldForReview`, `--since`); `comment thread <id>` shows one with its replies; `comment reply`, `post`, `edit`, `delete` and `moderate` act on them. YouTube's threads are two levels deep: a reply goes under the thread's top comment, never under another reply. Only our own comments can be deleted; a viewer's comment comes down with `moderate --status rejected`. Pinning and hearting exist only in Studio. Reading is free; posting and moderating are the owner's call, as above.

**Numbers.** `analytics` queries YouTube Analytics for our channel: any metrics, dimensions and filters it allows, by Pacific day, typically 2 to 3 days behind. Live counts for a video come from `video` and `public-videos`. Thumbnail impressions and click-through rate come only from the Reporting API's daily files; a job starts with the 30 days before it was made, and files are kept 60 days, so read and save them before they expire. Where the two disagree, Google treats the Reporting files as final and the Analytics numbers as estimates. Before any number goes to a person, count it the way the project counts numbers (in PS Brain: `$canonical-data`, with the US and outside the US shown apart). Queries that answer the common questions, and which reporting jobs to keep running: [references/analytics.md](references/analytics.md).

**Other channels.** `public-channel @handle`, `public-videos <ids>` and `search` read anyone's public videos. Search draws on its own 100-a-day bucket, so search once and then work from the ids.

## Where the API stops

Title and thumbnail A/B tests, dubs and extra audio tracks, end screens, cards, community posts, Shorts thumbnails and remix settings, pinned and hearted comments, comment settings, age restrictions, Premieres, the video editor, monetization, the channel's name, handle and picture, and its verification all live only in YouTube Studio; do those in Studio through the browser (`$browseros`, the `Work` profile is signed in as the channel). Captions uploaded through the API play on YouTube but don't show in Studio's caption editor.

## References

- [references/commands.md](references/commands.md): every command with its options and an example, and what each costs in quota. Read when a job needs a command or option not shown above.
- [references/analytics.md](references/analytics.md): Analytics API queries for the common questions, the rules on which metrics and dimensions combine, and the Reporting API jobs. Read before pulling numbers.
- [references/api-notes.md](references/api-notes.md): what YouTube's APIs can and can't do as of October 2026, field limits, and the traps developers report. Read when something behaves unexpectedly or before relying on a field you haven't used.
- [references/setup.md](references/setup.md): the grant, its scopes, signing in again, using it on another machine, and revoking it. Read when `whoami` fails or on a new machine.
