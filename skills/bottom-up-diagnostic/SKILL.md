---
name: bottom-up-diagnostic
description: "Run a bottom-up diagnostic that disaggregates a hard problem into inspectable primary evidence before explaining it with aggregates. Use when the user asks to dump and inspect raw events, users, transactions, requests, journeys, logs, screenshots, or frames case by case; or when an investigation is stuck at dashboards, summaries, or plausible high-level theories. Produce evidence artifacts, inspect them directly, reaggregate from them, and return a bounded diagnosis. Not for carrying an ordinary bug through its full analyze/fix/review lifecycle, exhaustive code review, or a math-first experiment loop."
metadata:
  short-description: "Disaggregate evidence before diagnosing"
---

# Bottom-Up Diagnostic

Use this skill to change the grain of a difficult investigation. Move beneath
metrics, dashboards, summaries, and plausible stories; expose the constituent
cases; inspect what actually happened; then synthesize only what that evidence
supports.

The aggregate can locate a problem. It does not, by itself, explain the
mechanism.

## Use When

- The user explicitly asks for a bottom-up, bottoms-up, disaggregated, raw-data,
  case-by-case, user-by-user, event-by-event, or frame-by-frame investigation.
- A hard diagnosis keeps producing high-level theories without resolving the
  underlying behavior.
- A funnel, ratio, alert, cohort, failure count, or summary claim needs to be
  checked against the cases that produced it.
- The primary evidence is visual and needs screenshots, recordings, or frames
  organized so the actual pixels can be inspected together.

## Do Not Use When

- The user wants an ordinary bug investigation carried through repair and
  verification without asking for this disaggregated evidence pass. Use
  `bugs-flow`; invoke this skill inside that workflow when the bottom-up pass is
  the missing method.
- The main job is a quantified hypothesis loop that chooses one
  highest-information experiment at a time. Use `north-star-investigation`.
- The user wants exhaustive review of code rather than diagnosis of observed
  behavior. Use `exhaustive-code-review`.

This skill can supply the evidence pass inside a broader bug, incident, product,
or investigation workflow. The broader workflow still owns planning, repair,
and delivery.

## Core Stance

- **Disaggregate before aggregating.** Start from the observations underneath
  the summary, not from a more elaborate interpretation of the summary.
- **Make the evidence inspectable.** The CSV, timeline, case packet, inventory,
  contact sheet, or frame sequence is part of the reasoning surface, not an
  attachment produced after the reasoning is done.
- **Match the grain to the claim.** Diagnose a user claim with users, a delivery
  claim with individual deliveries, a route claim with journeys, and a visual
  claim with pixels and interaction state.
- **Let the evidence overrule the story.** A useful pass may find the cause,
  narrow it, separate several mechanisms, or prove that the proposed bug story
  is wrong.
- **Keep proof boundaries visible.** Missing evidence, incomplete coverage, and
  unobservable steps remain part of the result.

Use the domain's existing data, browser, device, history, or repository tools.
This skill owns the order and quality of the diagnostic reasoning, not the
transport used to retrieve evidence.

## First Move

1. State the exact question and the aggregate or high-level claim currently
   being interpreted.
2. Name the atomic unit that can answer it: for example a user, event, request,
   transaction, session, item, screen, frame, or test case.
3. Bound the evidence universe by the real question: source, cohort, time
   window, version, environment, and relevant identity or join keys.
4. Create an evidence workspace using the target repo's existing artifact
   convention. If none exists, use a clearly named local directory and report
   its path.
5. Begin acquiring the underlying evidence. Do not spend the opening pass
   polishing hypotheses that the raw cases can settle.

## Workflow

### 1. Materialize the primary evidence

Gather the complete bounded universe when practical. Preserve the fields needed
to reconstruct what happened: source, identity, timestamps, order, state,
payload or properties, result, and relevant provenance.

Record the extraction boundary alongside the artifact: query or retrieval
method, time window, filters, exclusions, deduplication, source counts, and any
known capture gaps. Keep missing payloads, nulls, duplicates, failures, and
outliers visible unless the question justifies excluding them.

When the claim crosses systems, retrieve the independent authorities needed to
separate mechanisms. A client event, backend projection, store transaction,
vendor response, and rendered screen may describe different parts of the same
journey; one rollup is not a substitute for the others.

For visual evidence, preserve the sequence and context. Use before/after
screenshots, recordings, extracted frames, or contact sheets as appropriate,
and distinguish what the pixels show from what logs, accessibility state, or
source code imply.

### 2. Organize the evidence at its natural grain

Turn the source material into artifacts that make individual cases easy to
inspect. Choose the shape from the evidence rather than a fixed template:
per-user or per-session timelines, one-row-per-event tables, request traces,
transaction reconciliations, case packets, surface inventories, or visual
sequences are all valid.

Keep a small evidence index containing the artifacts, row or case counts,
coverage, join keys, and known gaps. Preserve a route back to the source record
so a conclusion can be checked without rerunning the entire investigation.

### 3. Inspect the cases before summarizing them

Actually open and examine the artifacts. Walk the relevant cases in order,
compare healthy and failing paths, and inspect exceptions rather than reading
only totals produced by the extraction code.

A sample can generate a theory. It does not automatically prove the theory for
the population. When the decision depends on prevalence or a cohort-wide
mechanism, test the theory against the full eligible universe when practical;
otherwise state the exact inspected coverage and keep the conclusion scoped to
it.

### 4. Reaggregate from the decomposed artifact

Recompute the headline metric or claim from the materialized cases. Compare it
with the original aggregate and with any independent authority. Explain
mismatches instead of averaging them away.

Separate distinct mechanisms before counting them together: observed absence is
not the same as capture failure; accepted is not the same as recorded or
attributed; a named test is not proof that its advertised journey ran; a still
image proves appearance, not necessarily actionability.

If the detailed evidence contradicts the initial theory, replace the theory and
update the artifact. Do not preserve a compelling narrative after its cases
have falsified it.

### 5. Return a bounded diagnosis

Synthesize only after the evidence has been inspected and reconciled. State:

- what the constituent cases show;
- what changed from the original aggregate story;
- whether the evidence found, narrowed, split, or rejected the suspected cause;
- the coverage and independent witnesses supporting the conclusion; and
- what remains unobserved or uncertain.

Do not silently turn diagnosis into repair. If the user also requested a fix,
hand the evidence bundle and bounded conclusion to the owning bug or
implementation workflow.

## Evidence Artifact Expectations

The artifact set should make these facts easy to find without requiring a fixed
file layout:

- diagnostic question and bounded evidence universe;
- source provenance, retrieval boundary, and coverage;
- disaggregated cases in an inspectable form;
- inspection notes, anomalies, and falsified interpretations;
- reaggregation and independent reconciliation; and
- final diagnosis with explicit proof limits.

## Completion Test

Before calling the diagnostic complete, confirm that:

- the underlying cases were inspected, not merely exported;
- another reader can trace the diagnosis back to source-level evidence;
- the reaggregated result can be reconciled with the original claim; and
- the conclusion is no broader than the observed coverage.

## Output Expectations

Lead with the diagnostic change: what the bottom-up evidence revealed that the
high-level view did not. Then provide the diagnosis, artifact path, evidence
coverage, and proof limits. If the evidence is incomplete, name the missing
source or unobserved step directly rather than filling it with a theory.
