# Bottom-Up Diagnostic Skill Plan

Date: 2026-08-15

Status: intention and historical-grounding source. The runtime implementation
lives in [`skills/bottom-up-diagnostic/`](../skills/bottom-up-diagnostic/).
This document records the problem, motivation, supporting Prime Agent examples,
and desired outcome without duplicating the runtime workflow contract.

## Core Intention

Create a reusable diagnostic capability for hard problems that biases the agent
toward the **disaggregated version of reality before the aggregated version**.

AI analysis commonly starts and stays at the level of aggregate metrics,
dashboards, summaries, and high-level hypotheses. The intended shift is to go
back underneath those abstractions: gather the actual observations that make up
the aggregate, make them inspectable, and understand what happened at the level
where it happened. Aggregation can follow when it helps explain the evidence,
but it should not replace seeing the evidence first.

The central idea is:

> Disaggregate first. Inspect the underlying reality. Aggregate only after the
> constituent evidence has been understood.

This is a way of thinking about diagnosis, not merely a request for a longer
analysis or a larger report.

## Problem Being Addressed

When an investigation is difficult, an AI often keeps reasoning at the same
high level even after that level has stopped producing answers. It interprets
aggregate movement, proposes plausible causes, and refines those hypotheses,
but can miss decisive facts hidden inside individual cases and sequences. The
analysis may sound coherent while remaining detached from what actually
happened.

The user then has to repeatedly force the investigation downward: retrieve the
raw data, split it apart, organize it, and inspect the pieces. That manual
correction is often what finally reveals the cause.

The cost of the current default is:

- important details remain invisible behind totals, averages, funnels, or
  summaries;
- plausible theories survive because they have not been confronted with the
  constituent evidence;
- the same high-level analysis is repeated without gaining new information;
- diagnosis takes longer and requires the user to keep redirecting the agent;
- apparent confidence can arrive before the underlying behavior is understood.

The missing capability is a dependable bias toward primary evidence and
first-principles decomposition when ordinary high-level analysis is not enough.

## Experiences Behind the Intention

A pay-gate drop-off investigation only reached the real explanation after the
underlying events were dumped, decomposed, and followed event by event and user
by user. The breakthrough did not come from another interpretation of the
aggregate funnel. It came from reconstructing and examining the individual
behavior that produced it.

The same need has appeared while debugging Meta events and payment gateways.
The recurring lesson is that the source material itself must be gathered and
combed through, rather than leaving the investigation at the level of reported
metrics or assumed flows.

Sometimes the evidence is visual rather than tabular. The equivalent move can
be literal: gather the screenshots, put them side by side, and look at what is
actually on the screen. The specific artifact is not the point. The point is to
make the underlying cases directly inspectable instead of reasoning about them
through a lossy summary.

These are grounding examples, not a prescribed workflow. The intended
capability should express the common diagnostic principle across telemetry,
logs, user journeys, payment behavior, visual behavior, and other kinds of hard
problems.

## Why Disaggregation Matters

Aggregates can show that something changed, but they often erase the structure
needed to explain why. Individual sequences can expose differences in timing,
ordering, state, path, cohort, missing steps, duplicated steps, or other
case-level behavior that disappears when everything is rolled up.

Organized evidence artifacts also externalize the investigation. They let the
agent and the user inspect the same underlying facts, challenge an inference,
and trace a conclusion back to what actually occurred. The artifact is
therefore part of the reasoning surface, not incidental presentation after the
reasoning is done.

## Historical Grounding from Prime Agent

These examples ground the intention in actual work. They show where the
investigation changed after the underlying cases became inspectable. They are
historical evidence for the need, not a specification of the future skill.

### Citation format

Prime Agent does not currently expose a documented durable URL for a historical
session. The honest local citation is therefore the Prime session ID, exact
JSONL transcript path, and stable one-based physical line numbers. No
`prime://` or other deep-link scheme is implied below.

### 1. Meta CAPI: the aggregate named the wrong failure

- **Session:** `019fe868-c815-7689-a00a-07baea26f5c4`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019fe868-c815-7689-a00a-07baea26f5c4.jsonl`
- **Relevant lines:** 598, 653, 659, 669, 717, 843, and 879

An aggregate daily sheet appeared to show that only about 42% of Subscribe
events carried the identity Meta needed and about 39% were delivered. Amir
stopped the analysis explicitly: “This is aggregated. I want disaggregated. I
don't want summaries. I want ... raw.”

The investigation then exported all 10,986 outbox records from the production
database, one row per event, and expanded each literal payload, match key,
response, error, and status into columns. After an exact environment join
removed sandbox rows, the raw records reversed the explanation: every built
payload carried `anon_id`.
The real loss was that many records never became payloads because a missing OS
version sent real purchases into terminal quarantine. The aggregate had
conflated missing payload construction, missing identity, historical ownership,
and sandbox traffic.

### 2. Paywall drop-off: inspect each journey before interpreting the funnel

- **Session:** `01a00028-cd6f-7251-b523-36e425a7341e`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/01a00028-cd6f-7251-b523-36e425a7341e.jsonl`
- **Relevant lines:** 8, 668, 855, 1171, and 1238
- **Continuation:** `01a000c7-f13b-77ed-ba9e-2f6d9126c333`, `/Users/aelaguiz/.prime/agent/sessions/01a000c7-f13b-77ed-ba9e-2f6d9126c333.jsonl`, especially lines 622, 904, 1456, 1496, and 1758

Amir first requested every frontend and backend event for every identity that
saw the paywall in builds 2.1.37 and 2.1.38, then said the work should analyze
each user's event stream and classify each paygate session. That produced
hundreds of thousands of raw events and 2,692 mature session-level journeys.

The case-level pass showed that 118 of 119 sessions with no canonical paygate
ending still emitted later app telemetry, usually within seconds. The problem
was therefore not simply that the app or event stream stopped. A later
warehouse-native recut and store-ledger reconciliation also exposed
non-equivalent event meanings and a commit-only metric that undercounted real
purchases. Finally, separating the actual intermediate screen events localized
the largest entry loss to the benefits-screen Continue → billing-screen
checkout edge, rather than the top of the paywall.

### 3. Meta event cost: sampled journeys proposed the wrong story

- **Session:** `019ffd1d-e766-76bf-a8b2-712d3650d682`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019ffd1d-e766-76bf-a8b2-712d3650d682.jsonl`
- **Relevant lines:** 153, 196, 226, 257, 301, 327, and 338

When NewTest event costs looked much worse than March, Amir moved the work from
Ads Manager totals to raw product → AppsFlyer → Meta hops, then asked for full
telemetry journeys for March and current users. A 21-user sample suggested that
Puzzle Path was consuming the session. Amir did not lock that attractive story;
he asked to dump the raw population and aggregate it again so the conclusion
could be checked.

The resulting `user_day0.csv` held one row for each of 5,078 new users, with no
duplicate identities. It falsified the sample story: Path-first users were a
small group and were more likely, not less likely, to reach the target. The
larger change was among daily-first users, who now played more puzzles but were
far less likely to take a second lesson. The full-population artifact changed
the diagnosis from “Path stole engagement” to a narrower second-lesson and
session-shape problem.

### 4. “Fifteen people were charged”: reconcile every purchase and entitlement

- **Session:** `019ff0cc-bbcd-778a-ba7d-52331b1dd347`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019ff0cc-bbcd-778a-ba7d-52331b1dd347.jsonl`
- **Relevant lines:** 8, 66, 126–128, 179, 396, 421, 633, 5709, and 5869

The incident arrived as an aggregate harm claim: Android had taken money from
15 people without recording their subscriptions. The investigation rebuilt the
exact 15-person cohort and checked every store transaction, revenue field, Plus
grant, current RevenueCat subscription, and missing client event.

The alarming interpretation reversed. All 15 were $0 trial starts, all 15 had
Plus access, and all 15 were missing conversion telemetry. This was attribution
harm rather than 15 customers needing refunds or entitlement repair. The later
backfill kept proof layers separate: all 17 requests were accepted, 14 were
visible exactly once, and three remained accepted but not exactly observable.
The session refused to turn HTTP acceptance into unsupported attribution proof.

### 5. AppsFlyer keyword zeros: reproduce one exact query boundary

- **Session:** `019fdcde-d4d1-74ff-87e8-8574ba6fb66b`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019fdcde-d4d1-74ff-87e8-8574ba6fb66b.jsonl`
- **Relevant lines:** 746, 752, and 1406

When Apple Ads keywords appeared to have no downstream AppsFlyer events, the
early analysis explained how the platforms might disagree and tried to
reproduce an old marketer view. Amir redirected it toward the authenticated
surface: “who cares about reproducing. Figure out how to get a clean view that
shows the right things.”

The controlled query changed one boundary at a time. Keywords grouped with LTV
event metrics returned `dimension-not-supported` and no rows; the otherwise
identical D0 query returned real registration, paygate, billing, commit, and
trial rows. The evidence supported a precise query incompatibility rather than
a broad claim that event ingestion was dead, while preserving that the unseen
original saved view could not be diagnosed with certainty.

### 6. Staging 429: reconstruct the requests instead of blaming the phone

- **Session:** `019ff2f1-3f92-7592-9d12-aca9c3288fb6`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019ff2f1-3f92-7592-9d12-aca9c3288fb6.jsonl`
- **Relevant lines:** 8, 933, 1043, and 2171

A generic account said a normal cold open probably grazed staging's per-IP
limit. Amir supplied the disconfirming case fact that this was the first staging
launch on that iPhone that day. The investigation then reconstructed the exact
request minute, backlog timestamps, engagement rows, producers, and limiter
boundary.

The relevant minute contained 140 requests, 112 of them erroneous engagement
writes created before the phone opened. Across the broader trace, internal QA
links had produced thousands of persisted marketing-engagement rows that were
draining behind a shared outward IP. The iPhone was collateral, not the backlog
producer. The trace also disproved an early “no retry backoff” explanation by
showing that backoff already existed.

### 7. Path migration: real rider rows overturned the synthetic answer

- **Session:** `019ff8f7-51ad-71f0-806a-50ffed3f0a94`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019ff8f7-51ad-71f0-806a-50ffed3f0a94.jsonl`
- **Relevant lines:** 2470, 3066, 3122, 4221, 4288, and 7568

The migration debate initially used architectural reasoning and synthetic rider
scenarios. Amir first asked how many active riders were actually affected, then
stopped a proposal for future monitoring with: “Just run the analysis now. Get
the data now and then go back to the panel with the data.”

Real completion sets changed the answer more than once. The final shipping-order
pass enumerated all 18,855 completion pairs across 2,033 riders and exposed a
large chapter-reopen cohort, harder-next-puzzle cases, and an arithmetically
impossible catalog promise that proxy analysis had hidden. That evidence
reopened a unanimous recommendation, produced a split decision, and let Amir
choose the actual rider outcome: “They stay where they are B.”

### 8. Engagement prediction: preserve the complete event field before choosing features

- **Session:** `019fffee-7ee6-77ab-ad6f-c8f21644df00`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019fffee-7ee6-77ab-ad6f-c8f21644df00.jsonl`
- **Relevant lines:** 85, 89, 280, 314, and 498

Before deciding which early behaviors might predict seven-day engagement, Amir
asked for all frontend and backend app telemetry from the previous 30 days,
unfiltered. The resulting artifact contained 9,235,321 event rows and occupied
46.86 GiB. It retained source overlap, duplicates, full payload JSON, and every
event family; time bounds were the only behavioral filter.

Only after that field of view existed did the work synthesize 250 candidate
first-24-hour features across 16 product and behavioral families. Imported
methodology did not get to irreversibly decide which signals were worth keeping
before the actual emitted data was visible.

### 9. Evidence Sheet failure: enumerate the whole live surface

- **Session:** `01a0006e-5755-75ab-be5b-d1a237502c90`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/01a0006e-5755-75ab-be5b-d1a237502c90.jsonl`
- **Relevant lines:** 8, 162, 232, 275, 284, and 1425

A scheduled workflow failure initially looked like one missing export field.
Amir asked why that single error killed the whole build and then required all
sheets to be analyzed. The investigation enumerated 121 exported tables, 38
data tabs plus the Index, 32 renderer families, every render boundary, and the
actual production deployment sequence.

That inventory showed the site had deployed successfully, while one pre-write
list comprehension prevented the first Sheets API request and froze every tab.
The eventual repair was closed against the same disaggregated surface: 39 tabs
rewritten through 39 atomic requests, followed by direct reads of every mapped
tab rather than acceptance of a generic green workflow badge.

### 10. Coaching: put the raw decision packet inside each example

- **Session:** `019fe70e-5d68-74ed-a982-add9d241916a`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019fe70e-5d68-74ed-a982-add9d241916a.jsonl`
- **Relevant lines:** 456, 464, 677, 699, and 728

Six polished production examples summarized policy splits and selected rollout
rows but hid the data needed to judge what a client-side coaching rebuild could
actually consume. Amir asked for the raw data in the six cases themselves, then
rejected a new high-level inventory because it moved the evidence away from the
place where the claim was being evaluated.

Each case was rebuilt with its full sanitized decision payload, every policy
and rollout row, all retained fields, and downloadable JSON. Inspecting those
packets exposed the real authority boundary: the live presentation selector
could be reproduced, but exact historical strategy grading could not be safely
rebuilt from the retained client payload alone.

### 11. Lesson quality: literal playable examples exposed contradictions

- **Session:** `019febbc-46cd-704b-a8d3-f4464445a014`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019febbc-46cd-704b-a8d3-f4464445a014.jsonl`
- **Relevant lines:** 1190, 1199, 1203, 1250, and 1289

A compressed “what works” report offered broad lesson-design conclusions but
not the real steps an author would need while building a lesson. Amir asked for
every playable kind, what to watch for, and examples of what each recommendation
looked like in actual content.

The rebuilt reference enumerated all 15 step kinds and quoted the real
headlines, coach lines, options, answer keys, and observed metrics. That detail
made defects visible that the summary concealed, including a 0.5% first-try
sizing step whose answer contradicted its own lesson rule and a squeeze example
whose coaching argued for Call while its key was Fold. A later field-level pass
also corrected “duration is unmeasurable”: `duration_sec` was dead, while
`duration_ms` was populated for all 31,068 completions.

### 12. Checkout cancellation: side-by-side visual timing reversed a false alarm

- **Session:** `019ff613-def3-77df-8151-49a1649dec97`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019ff613-def3-77df-8151-49a1649dec97.jsonl`
- **Relevant lines:** 1826–1829 and 1890

The agent called a 1.534-second cancellation too fast to be human and treated it
as recurrence evidence for an older checkout bug. Amir told it to stop guessing
and inspect the historical bug pack and device evidence.

The retained frames showed the native sheet visibly presenting in 536 ms and
fully visible in 672 ms, making a human dismissal within 1.534 seconds entirely
plausible. The current PostHog replay also lacked native Google Play pixels, so
it could not classify the event. The recurrence claim, escalation, and proposed
mitigation were withdrawn; the honest result remained `cancelled_ambiguous`.

### 13. Puzzle Archive: the frame sequence confirmed one claim and narrowed another

- **Session:** `019ff70e-e707-75fb-baa5-b94681f4bb17`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019ff70e-e707-75fb-baa5-b94681f4bb17.jsonl`
- **Relevant lines:** 898, 909, and 935

A physical-device capture showed that closing an Archive-launched puzzle
returned to Puzzles home, confirming the wrong destination. A retained video
and contact sheet also showed that long-pressing a locked future day briefly
opened a dark loader before returning home.

Looking at the sequence mattered because one earlier description called it a
“transient puzzle surface.” The actual pixels did not show a table or protected
puzzle content. The evidence therefore preserved the navigation defect while
narrowing the more dramatic claim to “opening loader appeared,” with the exact
internal branch still unproved because the expected log keys were absent.

### 14. FTL energy-gate failure: the video showed the test never reached the gate

- **Session:** `019ffb9b-c214-708d-908b-d12817dcf4a0`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/019ffb9b-c214-708d-908b-d12817dcf4a0.jsonl`
- **Relevant lines:** 41, 1064, and 1118

A named energy-gate test timed out and its logs made the lesson appear
unavailable. The raw JUnit structure and downloaded run video told a different
story: a playable “One Pair vs Two Pair” card and visible **Start Lesson**
button remained on screen throughout the wait.

The automation searched generic selectors and never targeted the rendered
lesson's dynamic entry control. It therefore never entered the lesson, reached
the energy gate, or opened checkout. The artifact changed a product-state or
monetization diagnosis into a harness-selector failure and also corrected a
misparsed test-result summary.

### 15. Play vs AI: appearance, actionability, and lifecycle frames isolated stale UI

- **Session:** `01a00311-2905-73ff-9ad4-be6e47fa0019`
- **Transcript:** `/Users/aelaguiz/.prime/agent/sessions/01a00311-2905-73ff-9ad4-be6e47fa0019.jsonl`
- **Relevant lines:** 8, 245, 247, and 255

A screenshot showed gray action buttons, but appearance alone could not prove
they were disabled. The device pass combined the original pixels with four
accessibility reads, a real tap, byte-identical before/after screenshots, and a
foreground-refresh comparison on the same decision.

The buttons were semantically disabled and ignored input; after foregrounding,
the unchanged decision immediately exposed ready controls. That A/B localized
the problem to stale presentation state rather than backend legality. Source
tracing then found a cache revision that omitted `heroControlsSettled`, recorded
honestly as a high-confidence code-grounded cause rather than a separately
instrumented runtime proof.

### What the history establishes

Across these cases, the decisive progress did not come from making the
aggregate explanation more elaborate. It came from exposing the constituent
reality in a form that could contradict the explanation: individual journeys,
raw payloads, exact transactions, per-rider counterfactuals, full surface
inventories, real content packets, request timelines, or literal frame
sequences.

The disaggregated evidence sometimes found the bug, sometimes localized it,
and sometimes proved that the proposed bug story was wrong. That last outcome
is equally important. The intended capability is not a mechanism for producing
more confident diagnoses; it is a mechanism for making the evidence capable of
overruling them.

## Desired Outcome

The desired outcome is a skill that can be invoked when a problem is hard,
ambiguous, or resistant to ordinary analysis, without the user having to restate
this philosophy each time.

Invoking it should reliably shift the investigation toward the actual evidence
beneath the abstraction. The agent should treat disaggregated observations as
the primary diagnostic material, organize them into artifacts that can be
examined, and ground any later synthesis in what those observations reveal.

Success would mean:

- the agent goes looking for the constituent evidence without needing repeated
  user correction;
- important variation and exceptional cases are less likely to be averaged
  away;
- the reasoning is anchored in artifacts that make the evidence inspectable;
- conclusions can be traced back to individual observations rather than only
  aggregate movement;
- the method transfers across data, event, journey, log, and visual
  investigations;
- aggregation remains available as a later explanatory step, after the
  underlying cases have been understood.

The intended result is fewer missed facts, less speculative looping, and a
higher chance of finding the real cause of a difficult problem.

## Boundary of This Document

This document captures **what is being sought and why**. The operational
contract, trigger boundaries, and execution guidance now live in
[`skills/bottom-up-diagnostic/SKILL.md`](../skills/bottom-up-diagnostic/SKILL.md).
