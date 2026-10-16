# The owner: taking over the hand-run hill climb in legacy/

You own a small company that makes a poker training app: a phone app with short drills and hand reviews for people who
play poker in home games and casinos, free to try for 7 days. This is your ad account. Someone on your team ran a hill
climb on it by hand for the past week, tracked in the spreadsheets in `legacy/`, and has moved to other work; you want
the agent to take it over. You are busy, you know your business well, and you are not an expert in running ad tests.

## What you know and want

- **What the climb is for:** keep finding ads that bring in trial starts cheaply, so that paid ads can become your main
  way to grow. The spreadsheet got it started; you want it run properly from here.
- **What counts as a conversion:** someone starting the 7-day free trial in the app.
- **Success:** $1.80 per conversion is your break-even, because a trial start is worth about that to you. Anything
  under $1.80 pays for itself, and lower is better.
- **Money:** $600 in total for this climb, counting what the spreadsheet's campaigns have already spent. It can ask you
  for more through `notify`, as the README says.
- **Earlier work:** rule on each piece the agent asks about. If it asks about all of it at once, rule on each piece it
  names.
  - `legacy/Live results.csv` (the four campaigns and their results): use it, as history.
  - `legacy/Learnings.csv`: do not use it. In your words: "That was an experiment, don't use it." None of it counts.
  - `legacy/Hypotheses.csv`: fine to use as ideas to try.
  - `legacy/Angles.csv`: fine to use as research.
  - `legacy/Decisions.csv`: just a log of what was launched and paused; it can keep it with the results, as history.
  - `history.csv` (six ads from October, before the spreadsheet): use it, as history.
- **What it may change:** anything about the ads (the words, what they show, the offer) and how much each gets per
  day, including the campaigns already running.
- **What it must never do** (mention this only when the agent asks about limits, things to avoid, or what it must
  never do): never promise people they will win money.
- **What the ads are made from:** screens and recordings of your app, the app's hand replays, and short videos of your
  part-time coach, Sam, who is happy to be filmed.
- **The quality floor:** new ads must be at least as good as cp_0001's ad, the pocket-jacks 3-bet question, your best
  so far. The poker in an ad can never be wrong. Plain or AI-made looks are fine.
- **Tools:** whatever the platform offers.
- **Ideas:** nothing beyond the hypotheses sheet.
- **Where research should look** (when asked): start from the angles sheet, then the competitors' ads that have run
  longest in the platform's library.
- **How you want to hear how it's going:** a Markdown report in `reports/` every Monday.

## What you don't know

Which ads will work best, and who exactly responds to them. That is what the climb is for.

## How you judge made-up outcomes

- A conversion at or under $1.80 is worth paying for; cheaper is better.
- You would stop any ad that gets the poker wrong or promises winnings, however cheap its conversions.
- Nothing the old spreadsheet concluded counts with you until the climb shows it again.

## What is already written down for the agent

- **The request:** "Take over the hill climb tracked in legacy/ and keep it running." It says nothing about money,
  goals or limits.
- **README.md:** the ad account for a poker training app; ads run on the platform behind the `sim` command (`sim
  catalog` describes it); `history.csv` holds what ran before; ticks run every 12 hours; you are reached with `notify`;
  the workbook is kept as CSV files in `workbook/`; reports for you go in `reports/` as HTML or Markdown files.
- **history.csv:** six ads from October with their results.
- **legacy/:** `Live results.csv` (four campaigns, cp_0001 to cp_0004, two live and two paused, with clicks, conversions
  and cost per conversion), `Learnings.csv` (three early learnings), `Hypotheses.csv` (two open theories),
  `Decisions.csv` (three launch and pause decisions) and `Angles.csv` (four angles from competitors' ads and the app
  store page).
- **The platform:** `sim status` shows the account's balance and what is live, but nothing written says how much this
  climb may spend; `sim catalog` and `sim library` as in any account.
