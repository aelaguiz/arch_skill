# What each setting costs

Read November 10, 2026, from the published price pages of OpenAI (API and Codex), Anthropic and Google. Prices change; `$model-eval` refreshes this file, and nothing in `SKILL.md` depends on an exact figure here.

## Price per million tokens, list

| Model | Input | Cached input | Output | Notes |
|---|---:|---:|---:|---|
| Terra 6.1 | $1 | $0.05 | $5 | |
| Terra 6.1 on Fast | $2 | $0.10 | $10 | |
| Sol 6.1 | $2 | $0.10 | $10 | |
| Sol 6.1 on Fast | $4 | $0.20 | $20 | |
| Astra 6.0 | $10 | $1 | $50 | |
| Astra 6.0 on Fast | $20 | $2 | $100 | |
| Luna | $0.10 | $0.01 | $0.50 | Never tested on helper work |
| Haiku 5.5 | $0.10 | $0.01 | $0.50 | 5 times this above 100k-token prompts |
| Sonnet 5.5 | $2 | $0.10 | $10 | |
| Opus 5.5 | $4 | $0.20 | $20 | |
| Fable 5.2 | $8 | $0.20 | $40 | |
| Fable 5.1 | $10 | $0.25 | $50 | Superseded by Fable 5.2 |
| Gemini 4 Carbon (standard, from Dec 1) | $4 | $0.20 | $20 | $0 cache write |
| Gemini 4 Carbon (intro, through Nov 30) | $2 | $0.10 | $10 | $0 cache write |
| Gemini 4 Argon (standard, from Dec 1) | $4 | $0.20 | $20 | $0 cache write |
| Gemini 4 Argon (intro, through Nov 30) | $2 | $0.10 | $10 | $0 cache write |

Fast costs 2 times standard on purchased credits and 2.5 times on included usage; the rows above show 2 times. Claude cache writes cost 1.25 times input for five minutes and 2 times for an hour. Google charges nothing for cache writes; in `agy --output-format stream-json`, `input_tokens` is uncached input and `output_tokens` already includes `thinking_tokens`. One Codex credit is $0.04.

Codex, Claude and Antigravity draw on separate pools of accounts, so their costs compare only as list prices. What a pool can really give depends on how much of it other agents are using.

## What a typical helper run costs

A typical run is the median Opus 5.5 medium helper run across 88 real tasks from the October 27 back-test: $1.71. The other measured settings scale it by what they cost on the same tasks, at list price and standard speed.

| Model | Low | Medium | High | Xhigh | Max |
|---|---:|---:|---:|---:|---:|
| Terra 6.1 | ~$0.18 | ~$0.23 | ~$0.29 | $0.21 | not run |
| Terra 6.1 on Fast | ~$0.45 | ~$0.58 | ~$0.73 | $0.53 | not run |
| Sol 6.1 | $0.36 | $0.46 | $0.58 | $0.68 | not run |
| Sol 6.1 on Fast | $0.90 | $1.15 | $1.45 | $1.70 | not run |
| Astra 6.0 | ~$1.80 | ~$2.30 | ~$2.90 | $3.10 | not run |
| Astra 6.0 on Fast | ~$4.50 | ~$5.75 | ~$7.25 | $7.75 | not run |
| Opus 5.5 | $0.85 | $1.71 | $2.03 | $3.40 | $5.69 |
| Sonnet 5.5 | $0.51 | $0.74 | not run | not run | $3.25 |
| Haiku 5.5 | ~$0.25 | not run | not run | not run | not run |
| Fable 5.2 | ~$1.21 | ~$2.43 | $3.61 | $5.40 | ~$8.08 |
| Fable 5.1 | ~$1.80 | ~$3.59 | ~$4.27 | ~$7.15 | ~$11.96 |
| Gemini 4 Carbon (standard) | not run | $2.80 | $4.07 | not offered | not offered |
| Gemini 4 Carbon (intro, Nov) | not run | $1.40 | $2.04 | not offered | not offered |
| Gemini 4 Argon (standard) | not run | not run | $1.68 | not offered | not offered |
| Luna | not run | not run | not run | not run | not run |

A ~ marks a cell worked out from price, because no run measured it. Those run high: Terra 6.1's lower levels sit above its measured xhigh. Fast rows use 2.5 times, the rate on included usage; on purchased credits it's 2 times. Codex also offers an ultra level, which has never been run on helper work.

Terra 6.1 at xhigh and Astra 6.0 at xhigh were measured November 5, 2026, against Opus 5.5 at medium on the same real tasks: Terra 6.1 on 4 tasks, 0.06 to 0.14 times, in about the same time; Astra 6.0 on 3 tasks, 1.61 to 2.17 times, in about 2.5 times as long. So few tasks give a direction, and both came in below the estimate worked from Sol 6.1's tokens, which said 0.20 and 1.99. Five more tasks put Opus 5.5 at high at 1.14. Sol 6.1 at xhigh on Fast comes close to Opus 5.5 at medium. On four stored builds of 2 to 12 minutes, Terra 6.1 at xhigh cost $0.77 in all, Sol 6.1 at xhigh $2.44, Opus 5.5 at medium $8.59, Astra 6.0 at high $9.66, and Gemini 4 Carbon at high $14.12 at standard rates ($7.06 in November, with two builds timing out).

Gemini 4 Carbon was measured November 10, 2026, on five stored multi-file tasks against Opus 5.5 at medium and Opus 5.5 at xhigh. At medium it cost a median 1.64 times Opus 5.5 at medium at standard rates (0.82 times at November introductory rates), and 42% less in total than Opus 5.5 at xhigh ($15.07 standard, $7.53 intro, against $26.16), because `agy` ran 35 to 138 tool steps and sent 275k to 442k uncached input tokens a task. On two of those tasks Gemini 4 Argon at high cost 0.87 to 1.09 times Opus 5.5 at medium at standard rates. On five saved reviewer control looks, a cold look on Gemini 4 Carbon at high averaged $2.77 at standard rates ($1.38 in November).

## Multiply by runs

A run's price is the smaller half of the sum, and a reviewer that keeps its thread costs more than a fresh run, because each look carries everything before it. A median Astra 6.0 xhigh look on a live timer cost $7.43 against about $3 for a fresh run. Checking in every half hour on a build that lasts a week, that's 336 looks and about $2,500. Sol 6.1 at high on that timer would be about $350 to $500, a seventh of Astra 6.0's cost on a cold look and a fifth by price per token, and skipping the check-ins where nothing changed costs less again. Measured live since, on one timer at list price: Sol 6.1 at high's first six looks averaged $0.40, against $3.85 for the first six on Astra 6.0 at xhigh, and Astra 6.0's reached $9.49 late in its thread. So Sol 6.1's figure may come in lower, but its thread hasn't grown yet. A cold look cost $0.15 on Terra 6.1 at xhigh and $1.12 on Opus 5.5 at high.

## What crossing families adds

Measured November 5, 2026: 28 runs on four small jobs with checkable answers, seven routes, standard speed. Every answer was right, and no launch failed. Each parent was a real session that briefed a helper, waited, read the answer and acted on it. Medians:

| Route | Briefing s | Setup s | Helper s | Reading s | Helper's cost |
|---|---:|---:|---:|---:|---:|
| Claude parent, native Opus 5.5 medium | 16 | 0.0 | 41 | 11 | $0.26 |
| Claude parent, native Sonnet 5.5 medium | 10 | 0.0 | 25 | 9 | $0.10 |
| Claude parent, external Sol 6.1 high | 12 | 2.3 | 56 | 12 | $0.10 |
| Claude parent, external Terra 6.1 xhigh | 12 | 1.9 | 41 | 10 | $0.03 |
| Codex parent, native Sol 6.1 high | 12 | 0.2 | 34 | 10 | $0.04 |
| Codex parent, native Terra 6.1 xhigh | 13 | 0.2 | 27 | 12 | $0.03 |
| Codex parent, external Opus 5.5 medium | 29 | 1.8 | 36 | 12 | $0.21 |
| Claude parent, external Gemini 4 Carbon medium | 16 | ~2 | 224 | 9 | $0.50 ($0.25 Nov) |
| Codex parent, external Gemini 4 Carbon medium | 41 | ~2 | 156 | 13 | $0.42 ($0.21 Nov) |

From a Claude parent, crossing adds about 2 seconds of setup and up to a cent of reading. From a Codex parent it adds about 17 to 28 seconds of briefing, 2 of setup, and 2 to 3 cents, because the parent writes the brief to a file or inline shell call, starts the helper and reads the stream. On the four November 10 runs to `agy` (two small jobs from each parent), every answer was right and `agy` itself took 115 to 226 seconds, three to nine times as long as Sonnet 5.5, Sol 6.1 or Terra 6.1 on the same jobs.

These are floors: each parent was handed a one-line command with the account and model already chosen. Four jobs show a direction, and fixed overheads weigh less on longer work. The helpers' cost and speed are for jobs of a minute or two.

That test also found Sol 6.1 at high and Terra 6.1 at xhigh taking about twice as long on two reading jobs when a Claude parent briefed them. It turned out to be mostly the brief. Given the identical brief, one run each, native runs took 1.6 to 2.1 times as long as on their own parent's brief, and three of four gaps between native and crossed closed to 7 seconds or less. What a brief asks for seems to matter as much as how long it is.
