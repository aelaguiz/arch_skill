---
name: bottom-up-diagnostic
description: "Run an evidence-first bottom-up diagnostic that materializes and inspects constituent cases before trusting an aggregate explanation. Use when the user wants raw events, users, transactions, requests, logs, journeys, screenshots, recordings, frames, or test attempts examined case by case, or when an investigation is stuck at dashboard totals, averages, samples, or plausible high-level theories. Save inspectable evidence artifacts, reconcile the population from them, and return a diagnosis whose confidence matches coverage. This owns the evidence pass; use bugs-flow for end-to-end bug repair, north-star-investigation for math-first experiment selection, and exhaustive-code-review for coverage-led code review."
metadata:
  short-description: "Inspect constituent evidence before diagnosis"
---

# Bottom-Up Diagnostic

Own one job: turn an aggregate-shaped question into inspectable constituent
evidence, then build a diagnosis that another investigator can audit.

## Mission And Stakes

Aggregates compress different mechanisms into one number. A missing event may
mean the event never happened, was never constructed, was rejected, was stored
under another identity, or was excluded by the query. A gray button may be
styling, disabled semantics, stale state, or a blocked backend action. Treating
those cases as interchangeable sends product, incident, data, and engineering
work toward the wrong fix.

This output becomes the evidence base for the next decision. Strong work lets a
reader open the artifacts, follow the important cases, reproduce the counts,
and see exactly what is proven, supported, refuted, and still unknown. Weak
work paraphrases a dashboard, promotes a sample or screenshot into a population
claim, or gives a confident root cause that the retained evidence cannot prove.

## Use When

Use this skill for asks such as:

- "Dump the raw event stream and trace the drop-off user by user before telling
  me what the funnel means."
- "Reconcile every affected purchase against the store record, entitlement,
  and telemetry instead of reasoning from the total."
- "Inspect the recording frame by frame and tell me what the pixels prove
  versus what the logs merely suggest."

Also use it when a plausible theory has survived only because nobody has
materialized the underlying cases, or when a sample and an aggregate disagree.

## Do Not Use When

- The broader job is an ordinary bug lifecycle from symptoms through repair and
  verification, without a missing disaggregated evidence pass. Use `bugs-flow`.
  This skill may supply the evidence pass inside that workflow.
- The job is to rank hypotheses and choose the fastest quantitative experiment
  under a math-first investigation loop. Use `north-star-investigation`.
- The deliverable is exhaustive code-review coverage over files, callers, and
  side doors. Use `exhaustive-code-review`.
- The answer is already available from one authoritative record and no
  aggregate or case-level ambiguity remains.

## Ground Truth And Proof

- Source records and directly inspectable artifacts are authoritative for what
  they contain or show, not automatically for what happened beyond their
  capture boundary. The user's desired outcome and explicit constraints are
  authoritative for the question. Starting explanations, including the
  caller's and agent's, are hypotheses that the cases may overturn.
- Preserve four proof levels: **observed** directly in a record or frame,
  **derived** by a reproducible transformation, **inferred** from the observed
  pattern, and **unknown** because the needed evidence is absent.
- Do not turn "not present in this source" into "did not happen." Name the
  source boundary and distinguish a missing observation from evidence of
  absence.
- Keep artifact paths, source anchors, query boundaries, time windows,
  identity rules, and exclusions with the evidence. A conclusion without a
  route back to its cases is not durable proof.
- Preserve awkward evidence when it changes interpretation: missing values,
  duplicates, contradictory rows, late arrivals, unresolved identities, and
  cases that do not fit the dominant pattern.

## First Move

1. Restate the decision-relevant question without embedding a cause.
2. Name the smallest useful atomic grain: one event, user journey, request,
   transaction, record, screenshot, frame interval, or test attempt.
3. Bound the evidence universe. Record the source, time window, population,
   identity rule, inclusion and exclusion rules, and expected count when known.
4. Choose a durable artifact that makes both raw evidence and case-level
   interpretation inspectable. Read
   [`references/evidence-artifacts.md`](references/evidence-artifacts.md) before
   constructing it.
5. Read
   [`references/worked-examples.md`](references/worked-examples.md) when the
   grain is unfamiliar, the first theory is attractive, or the proof boundary
   is easy to overstate.

Do not ask the user to choose a formal mode or fill a schema. Infer the grain
from the question and available evidence. Ask only for access or a fact whose
absence would materially change the evidence universe.

## Process

### 1. Materialize The Primary Evidence

Retrieve the rows, payloads, logs, records, files, screenshots, recordings, or
test artifacts that bear on the claim. Prefer the complete bounded population
when it is practical. Otherwise choose coverage that can expose variation and
state exactly what was and was not inspected.

Keep raw source fields alongside normalized or derived fields. When evidence
crosses systems, retain the join keys and system-specific meanings instead of
flattening non-equivalent statuses into one label. Save the artifact before
forming the final story.

### 2. Organize At The Natural Grain

Make each case independently inspectable. A useful case view normally lets the
reader answer:

- What is this case and where did it come from?
- What happened, in order?
- Which fields or frames are direct evidence?
- What is missing, contradictory, or unusual?
- How is the case classified, and why?

Inspect every case for a small bounded universe. For a large population, state
the total coverage, inspect the consequential cohorts and contradictions, and
make the remaining population available for reaggregation. A few convenient
anecdotes are not a population analysis.

### 3. Let Cases Revise The Theory

Compare the observed cases with the starting explanations. Seek the cases that
should exist if a theory is true, the near-misses that distinguish competing
mechanisms, and the contradictions that would force a narrower claim.

Separate mechanisms that an aggregate can collapse, such as an action not
occurring, an observation not being emitted, a payload not being constructed,
a request being rejected, or a query excluding valid rows. These are examples
of distinctions to investigate, not a finite classification menu.

When the detailed evidence disagrees with the initial story, update the story.
Do not reinterpret the cases to preserve a favored cause.

### 4. Reaggregate And Reconcile

Compute the totals, rates, cohorts, and outcomes again from the decomposed
artifact. Reconcile source population, extracted cases, classified cases,
unknown cases, duplicates, and exclusions. Explain every material mismatch.

Keep independent proof layers independent. An accepted request is not the same
as downstream visibility; a store transaction is not the same as an
entitlement or analytics event; a visible control is not the same as an
actionable control. Join them to answer the question without pretending they
are equivalent facts.

### 5. Stress-Test The Diagnosis

Before finalizing:

- inspect the strongest contradiction and at least one near-miss or negative
  case that separates the leading explanation from its nearest alternative;
- check whether the artifact represents the intended environment, identity,
  time boundary, and user state;
- check that every important numeric claim can be recomputed from the saved
  artifact;
- lower confidence or retrieve the next discriminating evidence when a causal
  step remains inferred rather than observed.

If the primary source is unavailable, use the next-best evidence path and name
its limit. If no available evidence can responsibly distinguish the leading
explanations, return a coverage gap and the smallest evidence acquisition that
would resolve it; do not invent a root cause.

### 6. Save The Evidence And Return The Diagnosis

Keep the primary artifact and any case ledger, contact sheet, reconciliation,
or query result at stable paths available to the user. The final answer should
point to them rather than replacing them with prose.

## Quality Bar

Strong diagnostic work:

- changes the grain of the investigation rather than decorating the aggregate;
- makes consequential cases and contradictions visible in artifacts;
- reconciles the final counts from those artifacts;
- distinguishes observation, derivation, inference, and unknowns;
- gives the next decision-maker a narrower, more defensible model of reality.

Weak work:

- retells dashboard totals with more prose;
- inspects only a hand-picked sample and generalizes silently;
- says screenshots or logs were checked without saving or indexing them;
- treats missing telemetry, HTTP acceptance, a green workflow, or a passing
  summary as proof of the user-visible outcome;
- names a root cause more strongly than the evidence permits.

## Output Contract

Adapt the headings to the investigation; do not fabricate empty sections. A
valid result includes:

1. **Question and scope** — the neutral question, atomic grain, evidence
   universe, time and identity boundaries, and coverage achieved.
2. **Evidence artifacts** — stable paths or links, source provenance, how to
   inspect them, and which columns, rows, cases, or frames carry the result.
3. **Case-level findings** — the recurring mechanisms, consequential cases,
   contradictions, and unknowns with source anchors.
4. **Reaggregation and reconciliation** — recomputed totals and an explanation
   for material differences from the original aggregate or claim.
5. **Diagnosis** — what is observed, derived, inferred, refuted, and still
   unknown. Confidence must match coverage and proof level.
6. **Next discriminating action** — only the smallest evidence read, query,
   instrumentation, or handoff that would materially reduce the remaining
   uncertainty. Do not silently turn this evidence skill into implementation.

A result is invalid if its key claims cannot be traced to the saved artifacts,
if its population math does not reconcile, or if it reports causal certainty
from correlation, missing data, or an unobserved system boundary.

## Completion Test

Finish only when:

- the atomic grain and evidence boundary are explicit;
- primary evidence is saved in an inspectable artifact;
- the necessary cases, including contradictions, were directly inspected;
- the population was reaggregated or the coverage limit was quantified;
- the diagnosis can survive the strongest observed counterexample;
- every material conclusion is labeled at the proof level the artifact earns;
- another investigator could follow the paths and reproduce the reasoning.

## Reference Map

- [`references/evidence-artifacts.md`](references/evidence-artifacts.md) — how
  to choose, build, inspect, and reconcile event, journey, transaction,
  request, visual, test-attempt, and population artifacts, with concrete sample
  tables
- [`references/worked-examples.md`](references/worked-examples.md) — fifteen
  end-to-end examples and compact anti-examples showing how case-level evidence
  can confirm, overturn, or narrow an attractive aggregate story
