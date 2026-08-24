---
name: bottom-up-diagnostic
description: "Run case-level statistical analysis of a bounded population by materializing raw observations, inspecting variation, cohorts, and outliers, and reaggregating results instead of trusting totals or averages. Use for funnels, telemetry, transactions, user behavior, experiments, operations, or other quantitative questions where conclusions must be grounded in constituent rows or cases. It may surface evidence of a software defect, but it does not own diagnosis, reproduction, repair, or verification; use bugs-flow when the goal is to diagnose or fix errors, regressions, crashes, Sentry issues, or other broken software behavior. Not for code review or math-first experiment selection."
metadata:
  short-description: "Case-level statistics, not bug diagnosis"
---

# Bottom-Up Population Analysis

Own one job: turn an aggregate statistical question into inspectable
constituent observations, then reaggregate them into a population conclusion
that another analyst can audit.

## Mission And Stakes

Totals, averages, and dashboards can compress different cohorts, mechanisms,
and data-quality problems into one number. A missing event may mean the action
did not occur, the observation was not constructed, the request was rejected,
the record used another identity, or the query excluded it. Treating those
cases as interchangeable produces false statistical conclusions.

This output becomes the evidence base for the next product, operational, or
engineering decision. Strong work lets a reader open the artifacts, follow the
important cases, reproduce the counts, and see exactly what is observed,
derived, inferred, and still unknown. Weak work paraphrases a dashboard,
promotes a convenient sample into a population claim, or treats a statistical
anomaly as a diagnosed software cause.

## Use When

Use this skill for asks such as:

- "Dump the raw event population and trace the drop-off user by user before
  telling me what the funnel means."
- "Reconcile every purchase behind this revenue total against the store,
  entitlement, and telemetry records."
- "Break this average down by cohort and inspect the outliers before deciding
  whether the change is real."

Also use it when a sample and an aggregate disagree, when a population-level
claim cannot be audited from its constituent observations, or when statistical
analysis may reveal a cohort or pattern worth handing to a product or bug
workflow.

## Do Not Use When

- The root ask is to diagnose, reproduce, repair, or verify a software error,
  regression, crash, Sentry issue, failed test, or broken user flow. Use
  `bugs-flow`, even when logs, screenshots, events, or several affected users
  are available. That workflow may use a bottom-up population analysis as one
  evidence method without changing ownership.
- The evidence is one user's journey, one recording, one stack trace, or one
  failing request and the goal is to explain why the software broke. Use
  `bugs-flow`.
- The job is to rank hypotheses and choose the fastest quantitative experiment
  under a math-first investigation loop. Use `north-star-investigation`.
- The deliverable is exhaustive code-review coverage over files, callers, and
  side doors. Use `exhaustive-code-review`.
- The answer is already available from one authoritative record and no
  aggregate, cohort, or case-level ambiguity remains.

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

1. Restate the statistical or population question without embedding a software
   cause.
2. Name the smallest independent grain that can be counted or compared: one
   event, user, journey, request, transaction, record, entity-day, or other
   population unit.
3. Bound the evidence universe. Record the source, time window, population,
   identity rule, inclusion and exclusion rules, and expected count when known.
4. Choose a durable artifact that makes both raw observations and case-level
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

### 3. Let Cases Revise The Statistical Explanation

Compare the observed cases with the starting explanations. Seek the cases that
should exist if an explanation is true, the near-misses that distinguish
competing mechanisms, and the contradictions that would force a narrower
population claim.

Separate mechanisms that an aggregate can collapse, such as an action not
occurring, an observation not being emitted, a payload not being constructed,
a request being rejected, or a query excluding valid rows. These are examples
of distinctions to analyze, not a finite classification menu.

When the detailed evidence disagrees with the initial story, update the story.
Do not reinterpret the cases to preserve a favored cause. If the pattern points
to a software defect, report the affected cohort and evidence boundary, then
hand diagnosis, reproduction, repair, and verification to `bugs-flow`.

### 4. Reaggregate And Reconcile

Compute the totals, rates, cohorts, and outcomes again from the decomposed
artifact. Reconcile source population, extracted cases, classified cases,
unknown cases, duplicates, and exclusions. Explain every material mismatch.

Keep independent proof layers independent. An accepted request is not the same
as downstream visibility; a store transaction is not the same as an
entitlement or analytics event; a visible control is not the same as an
actionable control. Join them to answer the question without pretending they
are equivalent facts.

### 5. Stress-Test The Population Conclusion

Before finalizing:

- inspect the strongest contradiction and at least one near-miss or negative
  case that separates the leading explanation from its nearest alternative;
- check whether the artifact represents the intended environment, identity,
  time boundary, and population state;
- check that every important numeric claim can be recomputed from the saved
  artifact;
- lower confidence or retrieve the next discriminating evidence when a causal
  step remains inferred rather than observed.

If the primary source is unavailable, use the next-best evidence path and name
its limit. If no available evidence can responsibly distinguish the leading
explanations, return a coverage gap and the smallest evidence acquisition that
would resolve it. Do not convert an anomaly into a diagnosed software cause.

### 6. Save The Evidence And Return The Population Analysis

Keep the primary artifact and any case ledger, cohort table, reconciliation,
or query result at stable paths available to the user. The final answer should
point to them rather than replacing them with prose.

## Quality Bar

Strong population analysis:

- changes the grain of the analysis rather than decorating the aggregate;
- makes consequential cohorts, cases, outliers, and contradictions visible in
  artifacts;
- reconciles the final counts from those artifacts;
- distinguishes observation, derivation, inference, and unknowns;
- gives the next decision-maker a narrower, more defensible model of the
  population.

Weak work:

- retells dashboard totals with more prose;
- inspects only a hand-picked sample and generalizes silently;
- says raw observations were checked without saving or indexing them;
- treats missing telemetry, HTTP acceptance, a green workflow, or a passing
  summary as proof of a population outcome;
- claims a software root cause instead of reporting a statistical bug signal
  and handing it to `bugs-flow`.

## Output Contract

Adapt the headings to the analysis; do not fabricate empty sections. A valid
result includes:

1. **Question and scope** — the neutral statistical question, population grain,
   evidence universe, time and identity boundaries, and coverage achieved.
2. **Evidence artifacts** — stable paths or links, source provenance, how to
   inspect them, and which columns, rows, cohorts, or cases carry the result.
3. **Case-level findings** — the recurring patterns, consequential cohorts,
   outliers, contradictions, and unknowns with source anchors.
4. **Reaggregation and reconciliation** — recomputed totals, rates, or
   distributions and an explanation for material differences from the original
   aggregate or claim.
5. **Population conclusion** — what is observed, derived, inferred, refuted,
   and still unknown. Confidence must match coverage and proof level.
6. **Next analytical action or handoff** — only the smallest evidence read,
   query, or instrumentation that would materially reduce uncertainty. If the
   result is a credible software-defect signal, hand it to `bugs-flow`; do not
   diagnose or repair it here.

A result is invalid if its key claims cannot be traced to the saved artifacts,
if its population math does not reconcile, if it reports causal certainty from
correlation or missing data, or if it becomes a software bug-fix workflow.

## Completion Test

Finish only when:

- the atomic grain and evidence boundary are explicit;
- primary evidence is saved in an inspectable artifact;
- the necessary cases, including contradictions, were directly inspected;
- the population was reaggregated or the coverage limit was quantified;
- the population conclusion can survive the strongest observed counterexample;
- every material conclusion is labeled at the proof level the artifact earns;
- another investigator could follow the paths and reproduce the reasoning.

## Reference Map

- [`references/evidence-artifacts.md`](references/evidence-artifacts.md) — how
  to choose, build, inspect, and reconcile event, journey, transaction, request,
  visual-observation, repeated-attempt, and population artifacts, with concrete
  sample tables
- [`references/worked-examples.md`](references/worked-examples.md) — worked
  examples and compact anti-examples showing how case-level evidence
  can confirm, overturn, or narrow an attractive aggregate story
