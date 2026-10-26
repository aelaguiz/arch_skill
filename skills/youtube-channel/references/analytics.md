# Numbers from YouTube

Three sources, each for a different question:

- **The Analytics API** (`yt.py analytics`): our channel's views, watch time, retention, traffic sources, geography, devices, audience and subscribers, by any Pacific day range. Typically 2 to 3 days behind, so the last days of a range come back missing or low.
- **The Data API's counts** (`yt.py video`, `public-videos`): a video's view, like and comment counts right now, for our videos or anyone's.
- **The Reporting API** (`yt.py reporting`): daily bulk CSV files, including what the Analytics API won't give a channel, such as thumbnail impressions and their click-through rate (the Analytics API answers "The query is not supported" for them). A new job produces files for the 30 days before it was created and then one per day; files are kept 60 days, so save what you need before then. Google's staff call these files the final numbers and the Analytics API's estimates.

Before a number goes to a person, count it the way the project counts numbers (in PS Brain, `$canonical-data`): say what it counts, over which days and compared with what, and show the US and outside the US apart.

## Contents

- [How a query is built](#how-a-query-is-built)
- [Queries for the common questions](#queries-for-the-common-questions)
- [The US and outside the US](#the-us-and-outside-the-us)
- [Reporting API jobs](#reporting-api-jobs)
- [What a view is](#what-a-view-is)

## How a query is built

`yt.py analytics --metrics m1,m2 --start YYYY-MM-DD --end YYYY-MM-DD [--dimensions d1,d2] [--filters f] [--sort=-m1] [--max N]` runs `reports.query` with `ids=channel==MINE`. YouTube accepts only certain combinations of dimensions, metrics and filters (its "channel reports"); anything else returns `The query is not supported`. When that happens, drop a dimension or metric, or add the filter the report needs (`video==ID` for retention, `insightTrafficSourceType==YT_SEARCH` for search terms), rather than guessing again. Some reports require `--sort` and a `--max`. Filters join with `;` (`country==US;video==ID`), and a filter on several values separates them with commas (`video==ID1,ID2`).

## Queries for the common questions

Each is a starting point; change the dates, metrics and filters.

How the channel did, day by day:

```bash
yt.py analytics --metrics views,engagedViews,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost \
  --dimensions day --sort day --start 2026-10-01 --end 2026-10-25
```

Rows come back in no particular order unless you sort, and days with no views are left out rather than shown as zero. For `--dimensions month`, both `--start` and `--end` must fall on the first day of a month (`--start 2026-01-01 --end 2026-10-01` covers January through October).

Which videos drew the most watch time:

```bash
yt.py analytics --metrics estimatedMinutesWatched,views,averageViewDuration,averageViewPercentage \
  --dimensions video --sort=-estimatedMinutesWatched --max 25 --start 2026-10-01 --end 2026-10-25
```

How long one video holds viewers (100 points along the video; `audienceWatchRatio` is the share of viewers still watching at each point, `relativeRetentionPerformance` compares it with videos of similar length):

```bash
yt.py analytics --metrics audienceWatchRatio,relativeRetentionPerformance --dimensions elapsedVideoTimeRatio \
  --filters video==VIDEO_ID --start 2026-10-01 --end 2026-10-25 --max-rows 100 --csv-out retention.csv
```

Where viewers came from, and what they searched for:

```bash
yt.py analytics --metrics views,estimatedMinutesWatched --dimensions insightTrafficSourceType \
  --sort=-views --start 2026-10-01 --end 2026-10-25
yt.py analytics --metrics views --dimensions insightTrafficSourceDetail \
  --filters insightTrafficSourceType==YT_SEARCH --sort=-views --max 25 --start 2026-10-01 --end 2026-10-25
```

Shorts against long videos (the rows come back as `shorts`, `videoOnDemand`, `liveStream`, and `creatorContentTypeUnspecified` for activity tied to no video, such as subscribers gained on the channel page; views from the Shorts feed show as the traffic source `SHORTS`):

```bash
yt.py analytics --metrics views,estimatedMinutesWatched,subscribersGained --dimensions creatorContentType \
  --start 2026-10-01 --end 2026-10-25
```

Subscribers against everyone else, devices, and who watches:

```bash
yt.py analytics --metrics views,averageViewDuration --dimensions subscribedStatus --start ... --end ...
yt.py analytics --metrics views,estimatedMinutesWatched --dimensions deviceType --start ... --end ...
yt.py analytics --metrics viewerPercentage --dimensions ageGroup,gender --start ... --end ...
```

A small channel gets few rows: YouTube leaves out a breakdown (a country, an age group, a search term) when too few viewers fall in it, so the parts may not add up to the total. On October 26, 2026, our channel's whole history (368 views) gave country rows for only 31 views (17 Philippines, 14 US) and no age or gender rows at all. Say how much of the total the rows cover beside any breakdown, and never treat a missing row as zero.

## The US and outside the US

Query by country and split the rows:

```bash
yt.py analytics --metrics views,estimatedMinutesWatched,subscribersGained --dimensions country \
  --sort=-views --start 2026-10-01 --end 2026-10-25 --csv-out by_country.csv
```

The US row is the US and the other rows are outside the US. The rows can cover only part of the total (above), so report the share of views they cover, and don't call the uncovered rest "outside the US": YouTube withheld its country, it didn't place it abroad. The Reporting API's daily files (below) also carry a country on each row; when the split matters, compare how much of the total they cover. For one video, add `--filters video==ID`. YouTube's country here is where the viewer watched from, which is not the same rule as the app's region in PS Brain's `$canonical-data` (a device's time zone at first open); say which one a number uses.

## Reporting API jobs

`yt.py reporting types` lists what the channel can schedule; `reporting jobs` lists what is running. The ones worth keeping running for a channel like ours:

- `channel_basic_a3`: views, watch time, likes, subscribers by video, day, country and more.
- `channel_combined_a3`: the same with traffic source, device and playback location.
- `channel_reach_basic_a1` and `channel_reach_combined_a1`: thumbnail impressions and click-through rate, which the Analytics API doesn't give a channel.
- `channel_traffic_source_a3`: traffic sources with their detail, including search terms.
- `channel_demographics_a1`: age and gender.

All six have been running for Poker Skill's channel since October 26, 2026 (`reporting jobs` lists them); create another with `yt.py reporting create-job <type>`. Files appear within one to two days of a job's creation, starting with the 30 days before it. Then `reporting reports <job id>` lists the daily files and `reporting download <report id> --job <job id> --out f.csv` saves one.

What the files are like: one CSV per Pacific day, unsorted, no totals; a day with no data is a header row alone. YouTube may issue a newer file for a day already delivered (same dates, later creation time); the newer one replaces the older. Search terms and countries below YouTube's privacy threshold are summed into a row with `NULL` (or `ZZ` for country). Columns can be added at any time, so read them by the header, never by position. A grant with only the Analytics scope has produced files holding nothing but headers; this channel's grant also has the `youtube` scope, so check the first files have rows.

## What a view is

Since late August 2026, YouTube's public view count (`viewCount`, and `views` in most reports) counts a view the moment a video starts to play, autoplay included. `engagedViews` counts plays past the first frame or started by a tap or click, which is what YouTube uses for monetization thresholds, click-through rate and average view duration. Compare like with like: a jump in views around late August 2026 can be the definition, not the audience.
