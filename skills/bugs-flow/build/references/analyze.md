# Bugs Flow Analyze Mode

Analyze mode: create or repair the bug doc, ingest the evidence, and make the issue either fix-ready or explicitly not ready.

## Goal

Create or repair the bug doc, ingest the evidence, and make the issue either fix-ready or explicitly not ready.

## Required work

- Normalize the bug doc structure.
- Capture the symptom, impact, and current status in TL;DR.
- Gather evidence: repro notes, logs, traces, or Sentry data, and code anchors.
- Write ranked hypotheses.
- End with one verdict: `fix-ready`, still `investigating`, or `blocked`.

## Fix-ready bar

Move to fix-ready only when:

- the likely root cause is concrete enough to code against
- the likely blast radius is understood
- there is a minimally credible verification plan

## Bad analyze behavior

- editing code 'just to test a hunch' without making the doc fix-ready
- turning the doc into a grab bag of every theory
- escalating to architecture planning because the bug touches multiple files
