# Evidence Artifacts

Use this reference after choosing the atomic grain and before building the
primary artifact. The patterns are starting shapes, not formal schemas. Add,
remove, or rename fields to preserve the real source semantics.

## What The Artifact Must Make Possible

A strong artifact lets another investigator:

1. identify the bounded population and source query;
2. open one case without reconstructing it from a dashboard;
3. distinguish raw fields from derived classifications;
4. find contradictions, unknowns, and exclusions;
5. recompute the claims in the diagnosis.

Prefer one stable case grain per table or view. Keep raw evidence beside derived
interpretation, or link it through a stable case key. Do not bury a raw payload,
frame, or log excerpt in chat where the next investigator cannot inspect it.

## Coverage Manifest

Put a short manifest beside every substantial artifact. Markdown, a `README`
inside a temporary artifact directory, or a metadata tab is enough.

```markdown
# Evidence Manifest

Question: Where do mature checkout journeys stop?
Atomic grain: one paygate session
Sources: frontend events, backend purchase events, store ledger
Window: 2026-08-01T00:00Z through 2026-08-07T00:00Z
Identity rule: canonical user id, then documented anonymous-id bridge
Expected population: 2,731 entries
Extracted: 2,731
Classified: 2,692 mature sessions
Excluded: 39 still inside the maturity window
Unknown: 7 sessions with unresolved identity joins
Raw fields: prefixed `raw_`
Derived fields: prefixed `derived_`
Artifacts: raw_events.parquet, session_ledger.csv, reconciliation.md
```

The manifest prevents three common failures: silent time-window drift, a sample
being mistaken for a population, and derived labels being mistaken for source
facts.

## Pattern 1: Ordered Event Or Journey Ledger

Use when sequence, missing transitions, identity stitching, or event semantics
matter. Keep one row per event in the raw artifact and one row per journey in a
case ledger.

```text
case_id | entry_at | ordered_evidence | observed_end | later_activity | derived_class | source_anchor
A17     | 10:02:01 | benefits>continue>billing | none | home_view +4s | checkout_edge_exit | events:881-889
A18     | 10:03:44 | benefits>continue>billing>trial | trial_start | lesson +22s | converted | events:890-904
A19     | 10:04:10 | benefits | none | none in 24h | benefits_exit | events:905-906
A20     | 10:05:08 | benefits>continue | none | settings +3s | billing_not_seen | events:907-912
```

Why this is stronger than a funnel:

- `A17` disproves "telemetry stopped" because later activity exists.
- `A19` and `A20` are not collapsed into the same no-conversion bucket.
- `source_anchor` makes each classification reviewable.
- The ledger can be grouped back into the funnel after the cases are understood.

Keep event timestamps, producer, raw name, raw payload, identity keys, and
normalization decisions in the linked raw artifact. Do not place only the
normalized journey string in the evidence pack.

## Pattern 2: Transaction And Entitlement Reconciliation

Use when an aggregate harm claim spans payment, access, attribution, refunds, or
multiple ledgers. One row should represent the decision-relevant unit—often one
person-purchase pair—not merely one webhook.

```text
case | store_record | charged_amount | entitlement | analytics_event | support_claim | derived_result
P01  | trial_start  | $0.00          | active      | missing         | "charged"     | telemetry_gap
P02  | trial_start  | $0.00          | active      | missing         | "charged"     | telemetry_gap
P03  | renewal      | $9.99          | active      | present         | "no access"   | claim_not_reproduced
P04  | renewal      | $9.99          | inactive    | present         | "no access"   | entitlement_gap
```

The row preserves separate proof layers. A store record can prove a transaction
without proving telemetry delivery. An active entitlement can refute an access
failure without proving attribution. The final diagnosis should state which
layer is harmed instead of calling all mismatches "purchase failures."

## Pattern 3: Request And Queue Trace

Use when one request appears to trigger a limit, timeout, duplicate, or backlog
incident. Reconstruct the surrounding requests and preserve both production time
and send time.

```text
request_id | sent_at  | produced_at | producer        | queue_age | result | retry_no | source
R771       | 12:03:04 | 09:11:22    | marketing_link  | 2h51m     | 200    | 2        | edge:4412
R772       | 12:03:04 | 09:11:24    | marketing_link  | 2h51m     | 200    | 2        | edge:4413
R773       | 12:03:05 | 12:03:05    | mobile_coldopen | 0s        | 429    | 0        | edge:4414
R774       | 12:03:06 | 08:54:10    | marketing_link  | 3h09m     | 200    | 3        | edge:4415
```

This trace changes the question from "why did this phone send too much?" to
"what occupied the shared boundary when the phone arrived?" It also lets the
investigator test a retry theory from actual retry numbers rather than assuming
backoff is absent.

Useful companion views:

- requests per producer and minute;
- queue age distribution;
- retry intervals by case;
- the exact limiter identity or shared boundary.

## Pattern 4: Visual Or Recording Evidence Index

Do not write only "watched the video." Save frames or a contact sheet and index
the moments that carry the claim. Pair pixels with semantic reads or real input
when appearance cannot prove behavior.

```text
frame | t_ms | visible_state          | action          | semantic_state | pixel_change | source
F01   | 0    | gray Fold/Call buttons | none            | disabled       | baseline     | run.mp4#0.000
F02   | 420  | gray Fold/Call buttons | tap Call        | disabled       | none          | run.mp4#0.420
F03   | 890  | app backgrounded       | foreground app  | n/a            | transition    | run.mp4#0.890
F04   | 1320 | colored Fold/Call      | none            | enabled        | changed       | run.mp4#1.320
```

What the index supports:

- observed: controls were gray, semantically disabled, and ignored the tap;
- observed: foregrounding changed the same decision to enabled controls;
- supported: presentation state was stale;
- not yet proved: the exact code field that failed to invalidate the state.

For timing claims, index first-visible, fully-visible, input, response, and end
frames. A total duration cannot tell whether a human had time to act unless the
relevant surface's presentation time is known.

## Pattern 5: Test-Attempt Timeline

Use when a named test failure may come from the product, setup, harness,
selector, environment, or assertion. Record the actual attempted journey rather
than reasoning from the test name.

```text
step | intended_state       | attempted_action       | observed_state              | reached? | evidence
1    | lesson card visible  | wait for generic card  | target card + Start Lesson  | yes      | video 0:00
2    | lesson entered       | tap selector "lesson" | no matching selector        | no       | junit action 14
3    | energy gate visible  | wait for checkout      | target card still visible   | no       | video 0:05-0:35
4    | assertion            | timeout                | never left catalog          | no       | junit failure
```

The product gate cannot be diagnosed from this attempt because the attempt never
reached it. The artifact does prove a harness-selector failure. Keep those two
conclusions separate.

For flaky or repeated tests, add attempt id, device/build binding, setup state,
and whether each required waypoint was visibly reached.

## Pattern 6: Population Recut After A Sample Story

Use one row per independent population unit—often user, account, rider, device,
or entity-day—when a compelling sample may not represent the whole field.

```text
entity | cohort       | first_action | target_reached | second_action | outcome | source_anchor
U001   | current      | path         | yes            | lesson        | retained | users:1
U002   | current      | daily        | yes            | puzzle        | churned  | users:2
U003   | comparison   | daily        | yes            | lesson        | retained | users:3
U004   | current      | daily        | no             | none          | churned  | users:4
```

Requirements that matter:

- prove the row key is unique at the chosen grain;
- retain cohort membership and denominator eligibility;
- keep missing outcomes explicit instead of dropping them;
- compare the sample pattern with its population prevalence and outcome;
- recalculate the original aggregate from this table.

The goal is not to produce a wider spreadsheet. It is to make the sample's
representativeness testable.

## Pattern 7: Evidence Packet Embedded With Each Example

Use when several polished examples or cases are being compared and the raw
inputs needed to judge each case would otherwise live elsewhere.

```text
case-03/
  summary.md
  raw-request.json
  raw-response.json
  decision-rows.csv
  frame-index.md
  provenance.txt
```

In `summary.md`, link each interpretation to the local raw file and name which
fields were retained, sanitized, or unavailable. This avoids a high-level
inventory that says the data exists but forces the reader to leave the case to
verify its claim.

An embedded packet is especially useful when the conclusion depends on an
authority boundary: the retained client payload may reproduce presentation but
not the server's original strategy judgment. The missing authority must remain
visible beside the example.

## Reaggregation And Conservation Checks

A bottom-up artifact should support explicit accounting. Adapt these equations
to the domain:

```text
expected population
= extracted cases + documented extraction gaps

extracted cases
= classified + unknown + excluded-after-extraction

source outcomes
= matched outcomes + unmatched source outcomes

accepted requests
= downstream-visible + downstream-not-visible + visibility-unknown
```

Do not force equality between non-equivalent systems. Instead, show the join:

```text
store transactions:        15
matched entitlement rows:  15
matched analytics events:   0
unresolved store joins:      0
```

That reconciliation proves an analytics gap while refuting a 15-person
entitlement gap. It does not prove why analytics was missing unless the payload
and delivery path are also observed.

## Artifact Review Questions

Before relying on an artifact, ask:

1. Can the key claim be traced to a row, frame, request, or raw packet?
2. Can every important count be recomputed from the artifact?
3. Are source fields distinguishable from derived classifications?
4. Are unknown, duplicate, contradictory, and excluded cases retained or
   accounted for?
5. Does the artifact bind the correct environment, identity, time window, and
   user state?
6. Could another investigator inspect the strongest counterexample without the
   original chat?

## Weak And Strong Shapes

Weak:

```text
Conversion fell 12%. Users probably dislike the new checkout.
```

Strong:

```text
Artifact: session_ledger.csv (2,692 mature sessions from 2,731 entries).
The largest loss is 418 sessions that saw benefits and emitted Continue but
never emitted billing-screen visibility. 403 had later app telemetry, so a
stopped event stream does not explain the cohort. Seven identity joins remain
unknown. This localizes the observed break to the Continue-to-billing edge; it
does not yet prove whether navigation, rendering, or event emission failed.
```

Weak:

```text
The workflow was green, so all tabs were updated.
```

Strong:

```text
The deployment succeeded, but direct reads show 39/39 tabs retain the old
version. The first write request was never issued. The green deployment receipt
proves site publication, not spreadsheet mutation.
```

The strong shapes name the artifact, coverage, direct observation, competing
explanation, and proof limit. Copy that reasoning structure, not the domain
wording or numbers.
