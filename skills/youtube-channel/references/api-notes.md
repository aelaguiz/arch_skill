# What YouTube's APIs can and can't do (October 2026)

What YouTube's reference and Help Center say, what Google's staff and developers report, and what this channel saw when the skill was tested on October 26, 2026. YouTube's pages and staff contradict each other in places, and they change; when a call behaves differently from this file, trust the call and fix the file. The full evidence, with sources and dates, is PS Brain's `specialists/youtube/research/2026-10-26-youtube-api-capabilities.md`.

## Contents

- [The channel's level decides what the API can do](#the-channels-level-decides-what-the-api-can-do)
- [Quota and limits](#quota-and-limits)
- [Uploads](#uploads)
- [Shorts](#shorts)
- [Video fields](#video-fields)
- [Thumbnails, captions, playlists](#thumbnails-captions-playlists)
- [Comments](#comments)
- [The channel page](#the-channel-page)
- [Analytics and reporting](#analytics-and-reporting)
- [Only in Studio](#only-in-studio)
- [Seen on this channel](#seen-on-this-channel)

## The channel's level decides what the API can do

YouTube grants features in three levels, and the API inherits them:

- **Standard:** uploads up to 15 minutes, playlists, comments.
- **Intermediate,** after the channel's one-time phone verification: videos over 15 minutes, custom thumbnails, live streaming. `channels.status.longUploadsStatus` reads `eligible` before verification and `allowed` after; `yt.py whoami` shows it. Before it, a video over 15 minutes is accepted by the upload and then rejected in processing (developer report, October 23, 2026).
- **Advanced,** from channel history or ID verification: clickable links in descriptions, pinned comments, title and thumbnail tests, multi-language features, and a higher daily upload limit.

Only the channel's Primary Owner can use the APIs on it. Poker Skill's channel belongs to the account the grant was made with, so that holds.

## Quota and limits

- Per Google Cloud project per day: 100 uploads in their own bucket, 100 searches in theirs, and 10,000 units for everything else. Quotas reset at midnight Pacific.
- Costs in the shared bucket: reads 1 unit; most writes 50 (`videos.update`, `thumbnails.set`, playlist and comment writes, `channels.update`, `watermarks.set`); `captions.insert` 400; `captions.update` 450; `captions.download` 200; `captions.list` 50. About 200 ordinary writes a day.
- The Analytics and Reporting APIs have their own quotas.
- Separately from quota, YouTube caps how many videos a channel uploads in 24 hours across the website, phones and the API. It publishes no number, and only advanced features raise it; developers hit it at 4 to 10 uploads a day in 2025 and 2026, and one project with a 600-upload quota still hit it on October 23, 2026 (`uploadLimitExceeded`).
- More quota takes YouTube's audit form; developers report weeks with no answer.

## Uploads

- **The private lock.** Uploads from API projects YouTube hadn't audited used to be locked private. Google's staff said on October 9 and 13, 2026 that the lock was lifted; other staff said on October 16 that apps in "External / Testing" status still get locked. Our OAuth client is internal to fun.country, and this channel's test upload on October 26 stayed unlisted as requested.
- **Protocol.** Resumable: the helper opens a session, sends 16 MB chunks, and on a dropped connection asks YouTube how much arrived and resumes from there. Files up to 256 GB.
- **Processing.** `status.uploadStatus` goes `uploaded` then `processed` (or `failed` with `failureReason`, `rejected` with `rejectionReason`); `processingDetails.processingStatus` goes `processing`, then `succeeded`, `failed` (`processingFailureReason`) or `terminated`. A 6-second clip took under a minute. `yt.py upload --wait` and `yt.py video <id>` show both.
- **Defaults.** API uploads don't take the channel's upload defaults from Studio, monetization included; `notifySubscribers` defaults to true in the API (the helper sends false unless `--notify`).
- **No replacing.** A video's file can't be swapped; a new cut is a new upload with its own id, views and comments.

## Shorts

- A video uploaded since October 15, 2024 that is square or vertical and at most three minutes long is a Short; no hashtag is needed, and no API field sets or reads it. Shorts upload at up to 1080p. A Short over one minute with any copyright claim is blocked worldwide.
- Google's staff, October 14, 2026: Shorts uploaded through the API need "a much higher, established level of channel trust and reputation" before the Shorts feed shows them, and "for videos where initial Shorts Feed traffic is critical, we recommend continuing to use the manual upload flow via YouTube Studio". The case behind it: one developer's API-uploaded Short drew 37 views (2.7% from the feed) against about 1,000 (90% from the feed) for a Studio upload the next day.
- `thumbnails.set` on a Short returns success and does nothing; Shorts thumbnails are set in Studio on a computer.
- The Analytics API sees Shorts: dimension `creatorContentType` and traffic source `SHORTS`.

## Video fields

- Title: at most 100 characters, no `<` or `>`, required whenever `snippet` is sent. Description: at most 5,000 bytes (the Help Center says characters), no `<` or `>`. Tags: 500 characters for the whole list, commas included, and a tag with a space counts its implied quotation marks.
- An update replaces each part it sends: a property left out of a sent part is deleted, privacy included. Only the made-for-kids and synthetic-content flags are left alone when omitted (since October 15, 2026). The helper reads, merges and sends only the parts that changed.
- `status.publishAt` schedules a release: the video must be private and never published, and a time in the past publishes at once. Setting privacy to public or unlisted cancels it. No report since October 13, 2026 confirms a scheduled release from an unaudited project firing; check a scheduled video after its time.
- `localizations` need `snippet.defaultLanguage`. `snippet.defaultAudioLanguage` exists on the resource but isn't in the reference's settable lists, and one tool's updates reset it to US English; set it, then read it back.
- `status.selfDeclaredMadeForKids` is the channel's declaration and `status.madeForKids` YouTube's result. `status.containsSyntheticMedia` is YouTube's disclosure of realistic altered or synthetic content; reads leave it out when false.
- Categories: `yt.py categories` (27 Education, 20 Gaming, 22 People & Blogs; test video 3 used 22).

## Thumbnails, captions, playlists

- Custom thumbnails need phone verification; without it `thumbnails.set` answers 403 "doesn't have permissions to upload and set custom video thumbnails". On a verified channel the same 403 right after an upload is a delay that clears on retry. JPEG or PNG; up to 50 MB since September 14, 2026; 1280×720 at least, 3840×2160 recommended.
- Captions: WebVTT, SRT, SBV, SCC or TTML with timings. Kind `asr` is YouTube's automatic track, `standard` an uploaded one. Downloading needs edit rights on the video; our automatic track downloads with word-level timings, and `--tlang` machine-translates. Captions uploaded through the API play on YouTube but don't appear in Studio's caption editor.
- Playlists: positions count from 0; an item has its own id. A video added has taken from 15 minutes to over 2 hours to show in the playlist's listing. A playlist's own cover image (square, through `/playlistImages` with `raw`) fails as HTTP 500 when it isn't square. Reading the channel's uploads as the owner can duplicate or skip videos, scheduled ones most, and stops near 20,000 items.

## Comments

- Threads are two levels deep: `comments.insert` replies only under a thread's top comment; a reply to a reply fails as `processingFailure`. Check a thread's `canReply` before replying.
- Only our own comments can be deleted; a viewer's comment comes down with `setModerationStatus` `rejected` (deleting it fails as `processingFailure`). `banAuthor` hides the author's future comments.
- Private videos take no comments. Pinning, hearting, comment settings, blocked words and comments on posts aren't in the API. Comment images (`snippet.imageUrl`) arrive in November 2026.

## The channel page

- `channels.update` sets one part per call. With `brandingSettings`: description (1,000 characters), keywords (500 characters in all, space-separated), country, default language, the trailer shown to visitors who aren't subscribed (a public or unlisted video of ours). The channel's name can't change (`channelTitleUpdateForbidden`); omitted properties in the part are deleted.
- A banner is a two-step job: `channelBanners.insert` (16:9, at least 2048×1152, up to 6 MB) returns a URL, then `brandingSettings.image.bannerExternalUrl` is set with `channels.update`, though that property isn't in the update's settable list. Untested on this channel.
- Home-tab shelves: `/channelSections` through `raw`, at most 10, of the types `singlePlaylist`, `multiplePlaylists`, `recentUploads`, `popularUploads`, `allPlaylists`, `multipleChannels`, `subscriptions`, `liveEvents`, `upcomingEvents`, `completedEvents`; private playlists can't be featured.
- Watermark: JPEG or PNG up to 10 MB, always in the upper right; `durationMs` at least 1,000.

## Analytics and reporting

- Analytics data typically arrives 48 to 72 hours late, by Pacific day; current counts for a video come from the Data API. Revenue metrics need the monetary scope and a Partner Program channel.
- Thumbnail impressions and click-through rate aren't available to a channel through the Analytics API; the Reporting API's reach reports (since January 15, 2026) carry them.
- The Reporting API: a new job produces files for the prior 30 days, then daily; files are kept 60 days; Google's staff call them the final source of truth where they differ from the Analytics API.
- Since late August 2026 a public view counts the moment playback starts, autoplay included; `engagedViews` keeps the stricter count.

## Only in Studio

Title and thumbnail tests (desktop, not Shorts), video-cut tests, end screens, cards, community posts, dubs and audio tracks in other languages, Shorts thumbnails and remix settings, comment settings and pinning, age restriction, paid-promotion disclosure, Premieres, monetization and mid-roll ads, the video editor, the channel's name, handle, picture and links, upload defaults, channel permissions, and verification.

## Seen on this channel

From the skill's live tests on October 26, 2026:

- The grant's scopes (`youtube`, `youtube.upload`, `youtube.force-ssl`, `yt-analytics.readonly`) were enough for every Data and Analytics call tried, including `reports.query`.
- An unlisted upload from project `poker-skill-a2d33` stayed unlisted; a 2.4 MB clip sent in 1 MB chunks resumed correctly between them.
- Reads lag writes: a tag edit's response showed the new tags at once while `videos.list` returned the old ones for about a minute; a channel keyword edit did the same.
- A `channels.update` that changed only the keywords also set the channel's default language to `en`, where it had been empty.
- `includeHistoricalChannelData=true` made every Analytics query fail with "The query is not supported"; the helper leaves it out. A query by month needs both dates on the first of a month.
- A country breakdown of the channel's whole history (368 views) covered 31 views; age and gender returned no rows.
- Setting the channel's own comment to `heldForReview` succeeded, yet it didn't appear in a `heldForReview` listing.
