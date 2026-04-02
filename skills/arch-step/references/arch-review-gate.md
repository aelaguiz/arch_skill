# `review-gate` Command Contract

## What this command does

- run a local idiomatic and completeness review against the plan and key repo anchors
- integrate the feedback you agree with into the main plan
- record the review outcome in one helper block

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for the plan sections most relevant to the current change

## Hard rules

- docs-only; do not modify code
- keep this review local
- do not use external reviewer CLIs or other-model consultations from this command
- read `DOC_PATH` plus the key code anchors needed to answer the review question
- if North Star or UX scope is contradictory, stop for a quick doc correction first

## Core review question

Ask the same question every time:

- `Is this idiomatic and complete relative to DOC_PATH? What is missing? Where does code or plan drift? Are there any SSOT or contract violations?`

If suggesting tests:

- suggest only high-signal, refactor-resistant checks
- reject negative-value tests such as deletion proofs, visual-constant noise, doc-driven gates, or mock-only interaction tests
- if an existing test suite is obviously negative value, call out deletion or rewrite

Also check:

- whether sharp edges or new SSOTs need short, high-leverage boundary comments

## Writes

- `arch_skill:block:review_gate`
- any real plan sections that should change after accepted review feedback

## Update rules

Integrate accepted changes into the main artifact first.

Then write or update:

- `arch_skill:block:review_gate`

Use this block shape:

```text
<!-- arch_skill:block:review_gate:start -->
## Review Gate
- Reviewers: self
- Question asked: "Is this idiomatic and complete relative to the plan?"
- Feedback summary:
  - <item>
- Integrated changes:
  - <item>
- Decision: proceed to next phase? (yes/no)
<!-- arch_skill:block:review_gate:end -->
```

Insert near the end before the Decision Log when possible.

## Quality bar

- identify plan drift, missing work, SSOT issues, and contract violations
- improve the main artifact rather than merely commenting on it
- keep the helper block short and decision-oriented

## Stop condition

- if the doc path remains truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if North Star or UX scope is contradictory, stop for a quick doc correction
- otherwise stop after the accepted review feedback is integrated and the helper block is current

## Console contract

- one-line North Star reminder
- one-line punchline
- what the review changed
- remaining risks
- next action
