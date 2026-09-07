# The Reader And The Shapes He Accepts

## Who is reading

A senior engineer and the company's CEO. He built much of the system. He
does not hold it in working memory today, and he says so:

- "pretend I'm not familiar with the fucking plan and just in plain English
  what's going on."
- "I know for you it's obvious because you're thinking linearly right now
  but I've been working on this for 2 days. I don't know what an earlier
  reconstruction is. The slide just has to be contained."

He wants the plain sentence and then the exact term, in that order:

- "what does that mean in plain english this pair thing" and then, once
  told, "are you saying its a reverse incompatible build?"

He reads to decide, not to admire coverage:

- "I don't care about receipts. I care about good headlines and good copy."
- "Just tell me the fucking caveat. I don't want to read all this."
- "What's, in plain English, what's between us and the plan being done?"

## The two edges

Both of these are rejections. The skill has to avoid both at once.

Too dense:

- "stop saying W3. I don't know what fucking W3 is. Talk in English."
- "I can't even understand what the fuck you're saying. It's so confusing."
  (on a 54-word post; shortness did not save it)
- "you're not speaking in user facing terms it's hard to fucking understand
  what you're saying"
- "The problem is that the fucking alerts in Slack mean nothing. They're
  written for robots not humans."

Too simple:

- "yeah its like one tick too dumbed down. I'm an engineer I just don't want
  to be overwhelmed all at once but I dont' want to be spoken to like a
  child." (on a chart that renamed real components to "App" and "Analytics")
- "you're literally defining a fucking wheel."
- "You're stating the obvious shit in a way like it's insightful before you
  give the actual feedback."

Both at once, which is the usual shape of an agent report:

- "You're over explaining and under explaining simultaneously." (method and
  history piled up; the one load-bearing fact missing)

The calibration that follows:

| Never explain or define | Always name |
|---|---|
| what a pull request, CI, staging, a cohort, a rate, a flag, or a deploy is | which pull request, what it changes, and its link |
| the words he uses himself: paygate, offering, checkout conversion, canonical, attribution, entitlement | which two systems disagree, by how much, for which period |
| how attribution or a funnel works in general | the baseline the number is compared to |
| the field | the writer's private labels: a minted code, a wave or worker label, a tool's state word, a session-local noun ("root", "children", "the reset"), a coined metaphor |

The line is ownership: his world's words need no help; the writer's process
words need replacing. Keep the real component names. Simplify the sentence
and the pacing, not the vocabulary of the field. Never make it wordier.

## What he says when it is right

- "Great." after: "Direct answer: Yes, the Fully Activated source is
  refreshing again. All three lookalike rings are Active/Normal. Only Android
  0-1% is currently delivering. All performance analysis has been removed."
  A direct answer, three short facts, nothing else.
- "C is good post it" after the shortest of three drafts: "You're right,
  that's a crash on our side and it's in our logs. Fix is in flight, probably
  out tomorrow. Sorry about that one."
- "yeah v3 is good post it" after a draft that deleted a coined term and
  said the idea in plain words.
- On a findings report: "not just 'I saw it 17 times,' but 'I check the data
  and it seems like it happens a lot.' That's acceptable, right? It's useful
  even." Observation plus frequency, in plain words, no verdict on intent.

## Shapes he has accepted

One unhedged sentence on top. "put a single top level commander's directive
at the top. that should be one unmistakable sentence, not hedged, not said in
soft language, and then put your tables beneath in your document." The
message, not the damage: a bad number enters afterward as the priced cost of
the story, never as the headline.

Business outcome first, initiative second, tasks last. "It should just be
simple tables and it should boil things down into what top-level initiative
this fits under. We should think about tasks second and the business outcome
first."

Tables for the status of many things. Every cell a sentence. "Give me a
table, easy to read." For notes columns: "a few words, five or seven words,"
with a separate detail column if needed.

Numbered steps for plans; numbered answers to numbered questions. "show me
the plan in numbered steps, simple to understand."

Method at the bottom or in a separate file. "Just the process up top and
then a sample report at the bottom was fine." Do not churn the structure
between editions.

Time tables: weeks or months across the top, newest on the left, metrics as
rows. Vertical lists newest first. Charts flow left to right in time.

Decisions: one plain question, the two or three choices in words, what each
one changes. "What the fuck are you asking me in plain English?" is the
response to anything else.

## A status row, built to the shape

Subject, state, cause, next or owner, one clock, every reference a link:

"Natasha (lifecycle for missions and Play). Her push audience is cleaned and
the broken mission triggers are identified. She is blocked because the two
pull requests that send mission events to Customer.io
([psmobile #4792](https://github.com/funcountry/psmobile/pull/4792) and
[#4807](https://github.com/funcountry/psmobile/pull/4807)) have not changed
since September 2. Next: the backend owner finishes those two, then she
connects the journeys in the next test build."

## A number, built to the shape

Rate, counts, baseline, meaning, one sentence:

"For every ad dollar spent the week of August 17, we got back 6.7 cents
within 7 days ($404 on $6,064). That is the best week-one return in six
weeks, and still far below break-even; older weeks ran 0.5 to 8.8 cents."

## An honest unknown, built to the shape

"p95 latency is up 40 percent since Tuesday. Cause unknown; Dana is
investigating and will report Friday."

The reader can trust silence when every exception is written like this.

## A status table, built to the shape

Column headers are labels. Each cell is one to three short sentences. Sources
ride on the fact or sit in a bare tail. No row opens the way the last one did.

| Person | Where it stands | Next |
|---|---|---|
| Natasha | Push audience cleaned; broken mission triggers found. Blocked: the two PRs that send mission events to Customer.io ([#4792](https://github.com/funcountry/psmobile/pull/4792), [#4807](https://github.com/funcountry/psmobile/pull/4807)) have not changed since September 2. | Backend owner finishes both PRs; she connects the journeys in the next test build. |
| Joey | The mission bar ([#4780](https://github.com/funcountry/psmobile/pull/4780)) is in 2.1.41. The five-hand Play vs AI mission ([#4859](https://github.com/funcountry/psmobile/pull/4859)) merged September 3 but missed that release branch. | Finish Home's next-action path; carry the merged mission into the next release. |
| Phil | Two video variants delivered September 3 ([Slack](https://app.slack.com/archives/C0BAXM3CS5U/p1788449121034809)); script 2's concept still unfinished. Media files not checked. | Finish the existing cut and hand Tim placement-ready files before starting another concept. |

## A table of numbers, built to the shape

One sentence says what the numbers show. The grid holds the numbers, with
units in the header. Nobody turns "73 of 353" into a sentence four times.

Android converts far fewer checkout starts than iOS, and the gap is almost
all cancellations, not errors.

| Platform | Starts | Purchased | Cancelled | Error | Unresolved |
|---|---|---|---|---|---|
| Android | 353 | 73 (20.7%) | 232 (65.7%) | 17 (4.8%) | 31 (8.8%) |
| iOS | 222 | 122 (55.0%) | 87 (39.2%) | 4 (1.8%) | 9 (4.1%) |

## The one he pointed at

On 2026-08-11 an automated Slack update posted this, and he replied to the
whole channel: "this is my actual morning report I look at its designed to
make sense to human beings." Verbatim (source:
`/Users/aelaguiz/workspace/psagentspace/research/2026-08-17-weekly-comms/slack-2026-08-10_to_2026-08-17.md`):

> **Daily update: app + revenue health** (automated morning sweep; full detail in the link at the bottom)
>
> **Releases:** Android 2.1.38 is live at 100%. iOS 2.1.38 is waiting in Apple review. Last night's backend deploy went out clean.
>
> **What got fixed:**
> - The Meta purchase-signal outage is over. Subscribe events went 5 for 5 with zero failures on the first full day after the backend deploy, after weeks of losing more than a third of them.
> - The Android bug that dropped purchase records got its first real-world proof of the fix: the first purchase on 2.1.38 recorded correctly. The 15 users it hit were all on free trials: everyone got their Plus access, nobody lost money, we only lost analytics events.
> - The two big telemetry bugs (event-queue drops, Meta identity errors) are both at zero on the new Android build. iOS gets these fixes when 2.1.38 clears review.
>
> **Needs a human:**
> - Two users reported the same lesson card shows pocket 8s in the image while the text says 9s ("HJ vs UTG Caller", traps-and-limp-raises lesson). Nobody has filed an issue yet. Someone should open that playable and check text vs image, about 5 minutes.
> - The warehouse transform failed its last two runs today. This morning's numbers were built before the failures so they're good, but if tomorrow morning's run also fails, dashboards go stale.
>
> **Trend worth knowing:** search clicks are up 72% on a twelfth straight weekly climb, but website visits still barely convert to installs (2.7%) and web has produced zero paying users.

What it does: four labeled blocks a skimmer can stop after. Every bullet is
a full sentence with the number, the comparison ("after weeks of losing more
than a third of them"), and the consequence ("nobody lost money, we only
lost analytics events"). His own vocabulary (Plus, backend deploy, warehouse
transform, purchase-signal) used without definition. Each ask names the
action and its cost ("about 5 minutes"). Nothing about how the report was
made except one parenthetical. On a surface with links, every release, bug,
and lesson named here would also be a link.
