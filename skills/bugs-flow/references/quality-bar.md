# Bugs Flow Quality Bar

## Evidence

- Strong:
  - concrete logs, traces, stack frames, or repros
  - code anchors tied to the evidence
- Weak:
  - hand-wavy story about what "probably" happened
  - no distinction between measured and inferred facts

## Fix-ready state

- Strong:
  - likely root cause is actionable
  - blast radius is bounded
  - verification plan is specific
- Weak:
  - three equally likely hypotheses and no decision
  - "we'll know after we patch it"

## Fix quality

- Strong:
  - smallest credible localized change
  - no silent fallback
  - obvious call sites updated
- Weak:
  - bug fix that quietly changes product behavior
  - compatibility shim with no removal plan

## Verification

- Strong:
  - reproduces or covers the actual failure mode
  - records concrete evidence in the doc
- Weak:
  - generic test run with no relationship to the bug
  - declaring success because the app did not crash once
