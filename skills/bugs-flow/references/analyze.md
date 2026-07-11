# Bugs Flow Analyze Mode

## Goal

Create or repair the bug doc, ingest the evidence, and make the issue either fix-ready or explicitly not ready.

## Required work

1. Normalize the bug doc structure.
2. Capture the symptom, impact, and current status in TL;DR.
3. Gather evidence:
   - repro notes
   - logs, traces, or Sentry data
   - code anchors
4. Write ranked hypotheses.
5. Identify the narrowest shared cause. Record the initial minimal convergence
   closure only for directly competing same-contract paths that must move
   together, or explicit `none`; exclude nearby cleanup and improvements.
6. End with one verdict:
   - `fix-ready`
   - still `investigating`
   - `blocked`

## Fix-ready bar

Move to fix-ready only when:

- the likely root cause is concrete enough to code against
- the likely blast radius is understood
- there is a minimally credible verification plan
- the human-authorized corrected behavior, smallest sufficient fix, closure or
  `none`, enough proof, do-not-build boundary, accepted residual risk, and
  pre-fix scope freeze are explicit

## Bad analyze behavior

- editing code "just to test a hunch" without making the doc fix-ready
- turning the doc into a grab bag of every theory
- escalating to architecture planning because the bug touches multiple files
