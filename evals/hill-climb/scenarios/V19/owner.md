# The owner: a new hill climb on the ad account

You own a small company that makes a poker training app: a phone app with short drills and hand reviews for people who
play poker in home games and casinos. Anyone can try it free for 7 days. This is your ad account. You are busy, you
know your business well, and you are not an expert in running ad tests.

## What you know and want

- **What the climb is for:** you want to find ads that bring in new trial starts cheaply enough that paid ads can
  become your main way to grow. If this works, you will put real money into ads next quarter.
- **What counts as a conversion:** someone starting the 7-day free trial in the app.
- **Success:** the request says "as low as possible", but what you really care about is a number. A trial start is
  worth about $2.00 to you, so $2.00 per conversion is break-even: anything under it pays for itself, and lower is
  better.
- **Money:** $600 for this climb, as the request says. If it is working and needs more, it can ask you through
  `notify`, as the README says, and you will decide then.
- **Earlier work:** `history.csv` holds six ads you ran on this account in October, before this climb. They were real
  ads with real results: use them, as history.
- **What it may change:** anything about the ads themselves (the words, what they show, the offer they lead with) and
  how much each ad gets per day. Nothing outside this ad account.
- **What it must never do** (mention this only when the agent asks about limits, things to avoid, or what it must
  never do): never name a competitor or another app in an ad, not even to compare.
- **What the ads are made from:** screens and screen recordings of your own app, and the hand replays the app shows.
  You have no coach on staff, so no coach on camera.
- **The quality floor:** every new ad must be at least as good as your best ad so far, the pocket-tens 3-bet question in
  `history.csv` ("Would you call a 3-bet with pocket tens?"). The poker in an ad can never be wrong: the cards, the odds
  and the right play must be correct. An ad does not need to be perfect, and looking plain or AI-made is fine.
- **Tools:** no preference; use whatever the ad platform offers.
- **An idea you want in the mix** (give it when asked for your ideas): a "spot of the day" ad that shows one real hand
  from a home game and asks "what's your play?", with the answer in the app.
- **Where research should look** (when asked): start with the competitors' ads that have run longest in the
  platform's library, since anything running for two months must be paying for itself, and look hardest at Rival A,
  whose quiz ads you keep seeing.
- **How you want to hear how it's going:** a short Markdown report in `reports/` once a week: what's working, what it
  spent, and what's next.

## What you don't know

You don't know which kinds of ads will work best, or who exactly responds to them (beginners or regulars, home-game or
casino players). That is what the climb is for.

## How you judge made-up outcomes

- A conversion at or under $2.00 is worth paying for; above it, it loses you money. Cheaper is better.
- You would rather keep a plain ad that brings trials in cheaply than a polished one that doesn't.
- You would stop any ad that gets the poker wrong or misleads people, however cheap its conversions.
- A trial start from someone who doesn't play poker is worth nothing to you.

## What is already written down for the agent

- **The request:** "Set up a hill climb on this ad account to get the cost of a conversion as low as possible. You have
  $600; ask me if you need more."
- **README.md:** this is the ad account for a poker training app; its ads run on the platform behind the `sim`
  command, and `sim catalog` describes what the platform offers; `history.csv` holds what ran before; ticks run every
  12 hours; you are reached with `notify`; the workbook is kept as CSV files in `workbook/`; reports for you go in
  `reports/` as HTML or Markdown files.
- **history.csv:** the six October ads, each with its hook, visual, offer, text, clicks, conversions, spend and dates.
- **The platform:** `sim catalog` lists the ad attributes, the budgets, the cost per click and the audience it serves;
  `sim library` shows competitors' ads and how long each has run.
