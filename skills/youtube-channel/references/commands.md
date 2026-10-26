# yt.py commands

Run each as `python3 "{baseDir}/scripts/yt.py" <command>`; `<command> -h` prints its options. Every command prints a short summary; `--json-out <file>` (where offered) saves the full API response. Quota is in units of the project's daily 10,000, except uploads and searches, which have their own 100-a-day buckets.

## Contents

- [The channel](#the-channel)
- [Videos](#videos)
- [Captions](#captions)
- [Playlists](#playlists)
- [Comments](#comments)
- [Numbers](#numbers)
- [Other channels and lookups](#other-channels-and-lookups)
- [Anything else: raw](#anything-else-raw)

## The channel

| Command | What it does | Quota |
| --- | --- | --- |
| `whoami` | The signed-in channel, its counts, and the grant's scopes | 1 |
| `channel show` | Description, keywords, country, language, trailer for visitors who aren't subscribed | 1 |
| `channel update [--description-file f] [--keywords '...'] [--country US] [--language en] [--trailer <video id>] [--dry-run]` | Changes only what you pass; prints old and new | 51 |
| `channel banner --image banner.png` | Uploads a banner (16:9, at least 2048×1152, up to 6 MB; keep what matters in the middle 1235×338) and sets it; untested on this channel | 100 |
| `watermark set --image logo.png [--timing offsetFromEnd --offset-ms 15000 --duration-ms 15000]` / `watermark unset` | The branding watermark on every video | 50 |

Keywords are one space-separated string of at most 500 characters; quote a multi-word keyword inside it: `--keywords 'poker "learn poker" "poker strategy"'`. The channel description is at most 1,000 characters.

## Videos

| Command | What it does | Quota |
| --- | --- | --- |
| `videos [--limit 25] [--privacy all\|public\|unlisted\|private]` | Our videos, newest first, every privacy, with length and views | ~3 |
| `video <id>` | One video's full state: privacy and schedule, upload and processing status, failure or rejection reason, file size and shape, captions, numbers, category, languages, localizations, disclosure flags | 1 |
| `upload <file> --title ... [options]` | Resumable upload, then optional thumbnail, captions and playlist | 1 upload + 50 per extra |
| `update <id> [options] [--dry-run]` | Read, change only what you pass, write; prints each change | 1 + 50 |
| `thumbnail <id> <image>` | Custom thumbnail (JPEG or PNG, at least 1280×720, up to 50 MB); needs the channel's phone verification; ignored on Shorts | 50 |
| `delete <id> --confirm-title "<exact title>"` | Deletes a video for good | 50 |

Options shared by `upload` and `update`:

- `--title` (at most 100 characters, no `<` or `>`), `--description` or `--description-file` (at most 5,000 bytes), `--tags a,b,c` (replaces; the combined tags may be at most about 500 characters), `--category <id>` (`categories` lists them; 20 Gaming, 27 Education, 22 People & Blogs, 17 Sports, 24 Entertainment).
- `--language en` (the title and description's language; needed before `--localize`), `--audio-language en` (what is spoken).
- `--privacy private|unlisted|public`, `--publish-at <RFC 3339 UTC>` (forces private until then).
- `--made-for-kids` / `--no-made-for-kids` (upload defaults to not made for kids), `--synthetic` / `--no-synthetic` (YouTube's disclosure of realistic altered or synthetic content), `--embeddable` / `--no-embeddable`, `--public-stats` / `--no-public-stats`, `--license youtube|creativeCommon`.

Only on `upload`: `--notify` (tells subscribers; off by default), `--thumbnail <image>`, `--captions file[:lang[:name]]` (repeatable), `--playlist <id>`, `--wait` (polls every 15 seconds until processing ends; `--wait-timeout` seconds, default 1,200), `--dry-run` (prints the request without uploading).

Only on `update`: `--add-tags a,b`, `--clear-publish-at` (cancels a schedule; setting `--privacy unlisted` or `public` also cancels it), `--localize lang:title[:description-file]` (repeatable), `--remove-localization lang`, `--recording-date <RFC 3339>`.

Examples:

```bash
yt.py upload cut.mp4 --title "Why nobody has won the Main Event twice since 1988" \
  --description-file desc.txt --privacy unlisted --language en --audio-language en \
  --category 27 --no-made-for-kids --no-synthetic --captions cut.vtt:en --wait
yt.py update dQw4w9WgXcQ --title "New title" --dry-run
yt.py update dQw4w9WgXcQ --publish-at 2026-11-01T15:00:00Z
yt.py update dQw4w9WgXcQ --localize "es:Por qué nadie ha ganado dos veces:desc_es.txt"
```

## Captions

| Command | What it does | Quota |
| --- | --- | --- |
| `captions list <video id>` | Tracks on a video: id, language, kind (`asr` is YouTube's automatic track, `standard` is uploaded), draft, status, name | 50 |
| `captions upload <video id> --file f.vtt --language en [--name ""] [--draft]` | Adds a track (WebVTT, SRT, SBV, SCC, TTML with timings) | 400 |
| `captions upload <video id> --file f.vtt --replace <caption id>` | Replaces a track's content | 450 |
| `captions download <caption id> --out f.vtt [--format vtt\|srt\|sbv\|scc\|ttml] [--tlang es]` | Downloads one of our tracks, optionally machine-translated | 200 |
| `captions delete <caption id>` | Removes a track | 50 |

## Playlists

| Command | What it does | Quota |
| --- | --- | --- |
| `playlists` | Our playlists with privacy and video count | 1 |
| `playlist create --title ... [--description-file f] [--privacy private] [--language en]` | New playlist (private unless you say) | 50 |
| `playlist update <playlist id> [--title] [--description-file] [--privacy] [--language en] [--localize es:"Título"[:desc_es.txt]]` | Changes only what you pass; `--localize` adds a title (and description) in another language and needs the playlist's default language | 51 |
| `playlist items <playlist id>` | Items with their item ids and positions | 1 per 50 |
| `playlist add <playlist id> --video <id> [--position N]` | Adds a video (positions count from 0) | 50 |
| `playlist move <item id> --position N` | Moves an item | 51 |
| `playlist remove <item id>` | Removes an item (the item id, not the video id) | 50 |
| `playlist delete <playlist id> --confirm-title "<exact title>"` | Deletes a playlist | 50 |

## Comments

| Command | What it does | Quota |
| --- | --- | --- |
| `comments [--video <id>] [--status published\|heldForReview\|likelySpam] [--search words] [--since 2026-10-01] [--order time\|relevance] [--limit 50]` | Threads across the channel or on one video, newest first, with reply counts | 1 per 100 |
| `comment thread <thread id>` | A thread's top comment and every reply | 2+ |
| `comment reply <comment id> --text ...` or `--text-file` | Replies as the channel, under a thread's top comment only | 50 |
| `comment post <video id> --text ...` | A top-level comment as the channel | 50 |
| `comment edit <comment id> --text ...` | Edits one of our comments | 50 |
| `comment delete <comment id>` | Deletes a comment the channel wrote (a viewer's comment comes down with `moderate --status rejected`) | 50 |
| `comment moderate <id[,id]> --status published\|heldForReview\|rejected [--ban]` | Holds, publishes or removes viewers' comments; `--ban` also hides the author's future comments | 50 |

## Numbers

| Command | What it does | Quota |
| --- | --- | --- |
| `analytics --metrics ... --start YYYY-MM-DD --end YYYY-MM-DD [--dimensions ...] [--filters ...] [--sort=-views] [--max N] [--csv-out f.csv]` | YouTube Analytics `reports.query` for our channel; prints up to `--max-rows` rows | analytics quota, separate |
| `reporting types` | Report types the channel can schedule | — |
| `reporting jobs` | Jobs already scheduled | — |
| `reporting create-job <report type> [--name]` / `delete-job <job id>` | Starts or stops a daily bulk report | — |
| `reporting reports <job id> [--since <RFC 3339>]` | The job's available daily files | — |
| `reporting download <report id> --job <job id> --out f.csv` | Downloads one file | — |

Write a descending sort with `=` (`--sort=-views`), since a bare `-views` reads as an option. Which queries answer which question: [analytics.md](analytics.md).

## Other channels and lookups

| Command | What it does | Quota |
| --- | --- | --- |
| `public-channel @handle` or `<channel id>` | Any channel's counts, start date and uploads playlist | 1 |
| `public-videos id1,id2,...` | Public numbers for up to 50 videos per call | 1 |
| `search "query" [--type video\|channel\|playlist] [--order relevance\|date\|viewCount] [--max 10] [--published-after] [--region US] [--channel <id>] [--duration short\|medium\|long]` | Searches public YouTube | 1 search call |
| `categories [--region US]` | Assignable video categories | 1 |
| `languages` | Language codes for localizations and captions | 1 |

To list another channel's videos without spending searches, take its uploads playlist from `public-channel` and run `playlist items <uploads playlist id>`, then `public-videos` on the ids.

## Anything else: raw

```bash
yt.py raw GET /channelSections part=snippet,contentDetails mine=true
yt.py raw POST /channelSections part=snippet,contentDetails --body-file section.json
yt.py raw GET /reports ids=channel==MINE startDate=2026-10-01 endDate=2026-10-25 metrics=views --api analytics
```

`raw METHOD PATH key=value... [--api data|analytics|reporting] [--body-file f.json] [--json-out f.json]` calls any method with the grant and prints the response (truncated at `--max-chars`). A `PUT` replaces whole parts: read the resource first and send it back with your change.
