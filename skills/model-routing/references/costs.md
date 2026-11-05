# What each setting costs

Read November 5, 2026, from the published price pages of OpenAI (API and Codex) and Anthropic. Prices change; `$model-eval` refreshes this file, and nothing in `SKILL.md` depends on an exact figure here.

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
| Fable 5.1 | $10 | $0.25 | $50 | |

Fast costs 2 times standard on purchased credits and 2.5 times on included usage; the rows above show 2 times. Claude cache writes cost 1.25 times input for five minutes and 2 times for an hour. One Codex credit is $0.04.

Codex and Claude draw on separate pools of accounts, so their costs compare only as list prices. What a pool can really give depends on how much of it other agents are using.

## What a typical helper run costs

A typical run is the median Opus 5.5 medium helper run across 88 real tasks from the October 27 back-test: $1.71. The other measured settings scale it by what they cost on the same tasks, at list price and standard speed.

| Setting | Share of a typical run | About |
|---|---:|---:|
| Sol 6.1 low | 0.21 | $0.36 |
| Sol 6.1 medium | 0.27 | $0.46 |
| Sonnet 5.5 low | 0.30 | $0.51 |
| Sol 6.1 high | 0.34 | $0.58 |
| Sol 6.1 xhigh | 0.40 | $0.68 |
| Sonnet 5.5 medium | 0.43 | $0.74 |
| Opus 5.5 low | 0.50 | $0.86 |
| Opus 5.5 medium | 1.00 | $1.71 |
| Opus 5.5 high | 1.19 | $2.03 |
| Sonnet 5.5 max | 1.90 | $3.25 |
| Opus 5.5 xhigh | 1.99 | $3.40 |
| Opus 5.5 max | 3.33 | $5.69 |

Terra and Astra have never been back-tested. Worked from Sol's token use at their prices, Terra at xhigh comes to about $0.34 a run and Astra at xhigh about $3.40, and each is an estimate until `$model-eval` measures it. Multiply a Codex row by 2 to 2.5 for Fast: Sol at xhigh on Fast is about $1.37 to $1.71, close to Opus at medium.

## Multiply by runs

A run's price is the smaller half of the sum. A setting at $3.40 that runs once costs $3.40. The same setting checking in every half hour on a build that lasts a week runs 336 times and costs about $1,100. Sol at high on that timer costs about $190, and skipping the check-ins where nothing changed costs less again.

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

From a Claude parent, crossing adds about 2 seconds of setup and up to a cent of reading. From a Codex parent it adds about 17 seconds of briefing, 2 of setup, and 2 to 3 cents, because the parent writes the brief to a file, starts the helper in a second call and polls while it runs.

These are floors: each parent was handed a one-line command with the account and model already chosen. Four jobs show a direction, and fixed overheads weigh less on longer work. The helpers' cost and speed are for jobs of a minute or two.
