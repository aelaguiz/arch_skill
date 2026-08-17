# Worked Examples And Anti-Examples

These examples are distilled from real investigations with product-specific
identity and history removed. They teach the reasoning move, not a lookup table.
A new investigation still has to discover its own grain, evidence, mechanisms,
and proof limits.

Each example uses the same compact lens:

- **Question** — the decision-relevant ask
- **Attractive story** — plausible, but not yet proved
- **Artifact** — what made the cases inspectable
- **Case evidence** — what direct inspection changed
- **Bounded diagnosis** — the strongest claim the evidence earned
- **Lesson** — why the move transfers

## 1. Event Delivery: Missing Identity Was Really Missing Construction

- **Question:** Why did only a minority of purchase events appear to carry the
  identity needed by the destination?
- **Attractive story:** the app failed to attach the anonymous identity.
- **Artifact:** all 10,986 outbox rows, one per event, with literal payload,
  match key, response, error, status, environment, and source anchor.
- **Case evidence:** every constructed production payload carried the identity.
  The missing population consisted largely of records that never became
  payloads because one required device field sent them to terminal quarantine.
- **Bounded diagnosis:** payload construction loss, not identity omission in
  built payloads. Sandbox and historical-owner rows were separate mechanisms.
- **Lesson:** a percentage named after a field can still combine construction,
  filtering, environment, and delivery failures. Inspect the rows on both sides
  of the payload boundary.

## 2. Funnel Drop-Off: The Missing Ending Did Not Mean The Session Stopped

- **Question:** Where do mature checkout journeys actually stop?
- **Attractive story:** sessions without the canonical ending represent app or
  telemetry termination.
- **Artifact:** raw frontend and backend events plus a ledger of 2,692 mature
  session journeys, with later activity and store reconciliation.
- **Case evidence:** 118 of 119 journeys lacking a canonical paygate ending
  emitted later app telemetry, usually seconds later. Separating intermediate
  screens localized the largest loss to one Continue-to-billing edge.
- **Bounded diagnosis:** the dominant observed break was one transition, while
  a stopped event stream was refuted for almost the entire unresolved cohort.
  The artifact did not alone distinguish navigation failure from screen-event
  failure.
- **Lesson:** "no terminal event" is not a mechanism. Inspect what happened
  immediately before and after each missing ending.

## 3. Sampled Journeys: The Full Population Reversed The Story

- **Question:** Why did a target event become more expensive in the current
  acquisition cohort?
- **Attractive story:** a new path consumed sessions and suppressed the target,
  based on 21 sampled users.
- **Artifact:** one unique row for each of 5,078 new users with entry route,
  first-day sequence, target outcome, and comparison cohort.
- **Case evidence:** path-first users were a small group and were more likely to
  reach the target. The larger shift was among daily-first users, who played
  more puzzles but were much less likely to take a second lesson.
- **Bounded diagnosis:** a second-lesson and session-shape problem, not evidence
  that the new path stole engagement.
- **Lesson:** use samples to discover possible mechanisms, not to assign their
  prevalence. Recut the population at the independent user grain before
  generalizing.

## 4. Feature Discovery: Preserve The Field Before Choosing Signals

- **Question:** Which first-day behaviors might predict seven-day engagement?
- **Attractive story:** imported methodology can decide in advance which event
  families are worth retaining.
- **Artifact:** 9.2 million raw event rows with complete payloads, source
  overlap, duplicates, and every event family; only the time boundary filtered
  behavior.
- **Case evidence:** once the emitted field was visible, 250 candidate features
  across 16 families could be derived without treating an early modeling choice
  as irreversible data loss.
- **Bounded diagnosis:** this pass established the available predictor field,
  not which features were causal or production-worthy.
- **Lesson:** disaggregation sometimes precedes hypothesis formation. Preserve
  the real field of view before a framework decides what cannot matter.

## 5. Purchase Incident: "Charged" Was The Wrong Harm Layer

- **Question:** Did fifteen people pay without receiving access?
- **Attractive story:** fifteen customers need refunds or entitlement repair.
- **Artifact:** one row per person-purchase pair reconciling store transaction,
  amount, revenue field, entitlement grant, current subscription, client event,
  and support claim.
- **Case evidence:** all fifteen were $0 trial starts, all had active access,
  and all lacked conversion telemetry. In a later backfill, 17 requests were
  accepted, 14 were visible exactly once, and three remained visibility-unknown.
- **Bounded diagnosis:** attribution harm, not observed payment or entitlement
  harm. Request acceptance did not prove downstream attribution.
- **Lesson:** reconcile every authority separately. A purchase, price,
  entitlement, analytics event, and user report answer different questions.

## 6. Analytics Query: Change One Boundary At A Time

- **Question:** Did downstream events disappear for one marketing dimension?
- **Attractive story:** the platform stopped ingesting the events.
- **Artifact:** two authenticated queries identical except for the event-metric
  boundary, with raw responses and request parameters saved side by side.
- **Case evidence:** the keyword-plus-lifetime-value query returned
  `dimension-not-supported` and no rows. The otherwise identical day-zero query
  returned registration, paygate, billing, commit, and trial rows.
- **Bounded diagnosis:** a precise query incompatibility. The unseen historical
  saved view remained undiagnosed, and event ingestion was not broadly dead.
- **Lesson:** an empty result can be a query-boundary result. Reproduce one
  controlled contrast before explaining a whole system.

## 7. Rate Limit Incident: The Visible Client Was Collateral

- **Question:** Why did the first mobile launch of the day receive a rate-limit
  response?
- **Attractive story:** a normal cold open grazed the phone's request limit or
  retried without backoff.
- **Artifact:** the exact request minute plus producer timestamps, queue ages,
  limiter identity, engagement rows, and retry intervals.
- **Case evidence:** the minute contained 140 requests; 112 were old engagement
  writes produced before the phone opened. Thousands of persisted rows from
  internal links were draining behind a shared outward identity. Retry timing
  showed backoff already existed.
- **Bounded diagnosis:** a shared backlog exhausted the boundary and the phone
  was collateral. "No retry backoff" was refuted.
- **Lesson:** reconstruct the requests competing at the actual boundary. The
  request that receives the error need not be the request that created the load.

## 8. Migration Decision: Real Entity Pairs Reopened A Synthetic Consensus

- **Question:** Where should active users land after a catalog migration?
- **Attractive story:** architectural reasoning and synthetic scenarios were
  sufficient to choose the mapping.
- **Artifact:** all 18,855 completion pairs across 2,033 active entities,
  preserving current location, completed content, next content difficulty, and
  candidate destination.
- **Case evidence:** the population exposed a large reopen cohort,
  harder-next-item cases, and an arithmetically impossible catalog promise that
  proxy scenarios had hidden.
- **Bounded diagnosis:** the unanimous synthetic recommendation did not fit the
  real population; the actual policy decision had to be reopened.
- **Lesson:** when a design decision claims to protect real users, enumerate the
  real affected states before treating synthetic riders as representative.

## 9. Multi-Surface Export: A Green Deployment Hid Zero Writes

- **Question:** Why did one export failure freeze the reporting surface?
- **Attractive story:** one missing field broke one sheet.
- **Artifact:** inventory of 121 exported tables, 39 live tabs, 32 renderer
  families, every render/write boundary, deployment receipts, and direct reads
  of each tab.
- **Case evidence:** the site deployed, but a pre-write comprehension failed
  before the first Sheets API request and froze every tab. After repair, 39
  atomic requests and 39 direct reads closed the same surface.
- **Bounded diagnosis:** successful publication did not prove data mutation;
  one shared pre-write boundary stopped the entire live sheet set.
- **Lesson:** enumerate the whole affected surface and verify the target system
  directly. A green adjacent workflow is not proof of the desired side effect.

## 10. Decision Examples: Put The Raw Packet Beside The Claim

- **Question:** Can a client-side rebuild reproduce the behavior shown by six
  polished examples?
- **Attractive story:** selected rollout rows and high-level summaries contain
  enough retained information.
- **Artifact:** each example bundled its sanitized request, every policy and
  rollout row, retained fields, response, and downloadable raw JSON.
- **Case evidence:** the packets could reproduce the live presentation
  selector, but they did not retain enough authority to reconstruct exact
  historical strategy grading.
- **Bounded diagnosis:** presentation was reproducible; strategy truth was not.
- **Lesson:** evidence must live where the example is judged. An inventory that
  says raw data exists elsewhere makes the central claim harder to falsify.

## 11. Content Quality: Literal Playable Fields Exposed Contradictions

- **Question:** What actually works across the available lesson-step types?
- **Attractive story:** broad design conclusions and aggregate completion
  metrics are sufficient guidance for authors.
- **Artifact:** all 15 playable step types with literal headline, coaching,
  options, answer key, duration field, and observed outcome metrics.
- **Case evidence:** one sizing example had a 0.5% first-try rate and contradicted
  its own rule; another coached Call while its key said Fold. A field-level pass
  showed one duration field was dead while another was populated for all 31,068
  completions.
- **Bounded diagnosis:** the summary concealed both content contradictions and
  a measurement-field error.
- **Lesson:** when the work product is an example, inspect the literal fields a
  user sees and acts on. Abstract recommendations cannot expose internal
  disagreement inside one playable case.

## 12. Checkout Timing: Saved Frames Reversed A False Recurrence Claim

- **Question:** Was a 1.534-second checkout cancellation too fast to be human?
- **Attractive story:** the timing proved recurrence of an older checkout bug.
- **Artifact:** historical device frames indexed at sheet-presenting,
  fully-visible, and cancellation moments, plus the current replay's capture
  limitations.
- **Case evidence:** the native sheet began presenting at 536 ms and was fully
  visible at 672 ms, leaving ample time for a human dismissal. The current
  replay did not capture native store pixels, so it could not classify the
  cancellation.
- **Bounded diagnosis:** `cancelled_ambiguous`; recurrence and mitigation claims
  were withdrawn.
- **Lesson:** total duration is not visible decision time. Inspect the frames
  that establish when the actionable surface actually appeared.

## 13. Navigation Video: Preserve The Defect, Narrow The Drama

- **Question:** What happened after opening and closing locked content?
- **Attractive story:** protected content briefly rendered before the app
  returned to the wrong destination.
- **Artifact:** physical-device video and contact sheet covering the long press,
  loader, close action, and returned screen.
- **Case evidence:** closing returned to the wrong home, and a dark loader
  briefly appeared. No frame showed a table or protected content. Expected log
  keys were absent.
- **Bounded diagnosis:** the navigation defect was observed; the stronger claim
  narrowed to "opening loader appeared," while the internal branch remained
  unproved.
- **Lesson:** direct evidence can confirm one part of a report while narrowing
  another. Do not discard the real defect just because the dramatic wording was
  unsupported.

## 14. Named Product Test: The Attempt Never Reached The Product Gate

- **Question:** Why did an energy-gate test time out?
- **Attractive story:** the lesson or monetization gate was unavailable.
- **Artifact:** raw test-result structure, action log, selector attempts, and
  downloaded run video aligned on one timeline.
- **Case evidence:** the target lesson card and visible Start Lesson button
  remained on screen throughout. The automation searched generic selectors,
  never activated the dynamic entry control, and never entered the lesson.
- **Bounded diagnosis:** harness-selector failure; the run provided no evidence
  about the downstream energy gate or checkout.
- **Lesson:** a test name is an intention, not a journey receipt. Prove each
  required waypoint was reached before assigning failure to the named target.

## 15. Gray Controls: Combine Pixels, Semantics, Input, And Lifecycle

- **Question:** Were gray action buttons merely styled differently or actually
  unusable?
- **Attractive story:** appearance alone proves disabled controls, or backend
  legality caused the state.
- **Artifact:** original screenshot, accessibility reads, a real tap,
  before/after pixel comparison, and the same decision after foregrounding.
- **Case evidence:** controls were semantically disabled and ignored input.
  Foregrounding immediately exposed ready controls without changing the
  decision. Source tracing found one omitted cache revision field.
- **Bounded diagnosis:** stale presentation state was directly supported; the
  exact code cause was high-confidence and code-grounded, not separately
  instrumented runtime proof.
- **Lesson:** combine independent evidence types when one surface cannot answer
  the question. Keep the observed UI mechanism separate from the inferred code
  cause.

## Compact Anti-Examples

### Dashboard Paraphrase

Weak:

```text
Delivery is 39%, so identity quality is poor.
```

Why it fails: the denominator may combine unbuilt payloads, sandbox traffic,
quarantine, rejected requests, and delivered events. No case is inspectable.

Stronger move: export the bounded records, preserve construction and delivery
states separately, inspect the missing cohort, then recompute the rate.

### Sample As Population

Weak:

```text
Most of the 21 users I checked took the new path, so it caused the cohort drop.
```

Why it fails: the sample can suggest a mechanism but says nothing reliable
about prevalence or comparative outcome.

Stronger move: build one unique row per population unit and test whether the
sample pattern is common and outcome-negative.

### "Looked At The Video"

Weak:

```text
The video confirms a flash of protected content.
```

Why it fails: there is no retained frame index, and "flash" may describe a
loader, transition, stale frame, or actual content.

Stronger move: save the relevant frames, label what pixels are visible, align
input and timing, and narrow the noun to what the frames show.

### Acceptance As Outcome

Weak:

```text
All requests returned 200, so the backfill succeeded.
```

Why it fails: transport acceptance does not prove downstream visibility,
uniqueness, attribution, or user-visible state.

Stronger move: reconcile accepted requests against the downstream authority and
keep visibility-unknown cases explicit.

### Test Name As Coverage

Weak:

```text
The checkout test failed, so checkout is broken.
```

Why it fails: the attempt may never have reached checkout.

Stronger move: reconstruct the actual test journey and prove each prerequisite
state from action logs and visible evidence.

## How To Transfer These Examples

Use the examples to ask better questions:

- What cases were compressed into this number or label?
- What artifact would let a skeptical reader inspect one case?
- What attractive story would the strongest contradiction overturn?
- What independent authority must be reconciled rather than treated as the
  same fact?
- What does the evidence prove directly, and where does inference begin?

Do not copy the example's columns, thresholds, labels, or diagnosis into a new
domain. The reusable move is to choose the natural grain, retain the primary
evidence, inspect the cases, reconcile the population, and stop at the proof
boundary.
