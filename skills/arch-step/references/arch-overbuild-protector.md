# `overbuild-protector` Command Contract

## What this command does

- classify phase-plan work items into explicit scope buckets
- separate ship-blocking work from optional work, follow-ups, and known bug vectors
- in apply mode, rewrite the phase plan in place so the main checklist is mechanically scope-safe

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Section 0, Section 7, and helper-block expectations

## Inputs and knobs

- `MODE=report|apply`
  - default `report`
- `STRICT=0|1`
  - default `1`
- `FOCUS="<text>"`
  - optional bias toward a subset such as verification, tooling, or one phase

## Scope authority

Treat these as the scope contract when present:

- TL;DR
- Section 0.2 In scope
- Section 0.3 Out of scope
- Section 0.4 Definition of done
- `fallback_policy`

If those sections are vague, warn in the helper block but do not hard-block.

## Writes

- `arch_skill:block:overbuild_protector`
- in `MODE=apply`, the existing phase plan rewritten in place

## Hard rules

- docs-only; do not modify product code
- Section 7 remains the one authoritative execution checklist
- if no phase plan exists, stop and point to `phase-plan`; do not invent a new plan format
- use code and repo evidence only to validate parity or risk claims; do not invent obligations

## Work-item extraction

- prefer explicit checkbox items
- preserve stable task IDs if they exist
- if there are no checkboxes, treat each top-level `Work` bullet as a work item
- if the plan is too unstructured for reliable item extraction, classify at the phase level instead

## Classification buckets

- `A` Explicit ask:
  - directly requested by the user, TL;DR, or in-scope sections
- `B` North-Star necessary:
  - required to satisfy the claim, definition of done, or explicit invariants
  - common examples include call-site migrations, deletes or cleanup that remove parallel truth, correctness fixes, and minimal verification needed to trust the change
- `C` Parity necessary:
  - required to match an existing internal pattern or contract, with a real repo anchor
- `D` Risk mitigation necessary:
  - minimal work needed to avoid a concrete regression or correctness failure
- `E` Optional quality:
  - nice to have, but not required to ship the North Star
- `F` Scope creep:
  - expands UX scope or adds unjustified new work
- `G` Bug vector:
  - adds brittle gates, long-lived complexity, or wrong-by-default safety theater

Default reject examples for `G` unless explicitly approved:

- runtime fallbacks or shims when fallbacks are forbidden
- new deleted-code proof tests
- visual-constant or churn-heavy golden tests
- coverage gates or bespoke coverage infrastructure
- new remote-runner or distributed-execution wiring for local development tasks
- new generators or frameworks introduced just to save small amounts of time

Tie-breakers:

- `STRICT=1`:
  - ambiguity defaults to follow-up, not include
- `STRICT=0`:
  - ambiguity defaults to optional, not include
- parity is never assumed without a real anchor
- new tooling is follow-up unless `A-D` clearly applies

## Update rules

Write or update:

- `arch_skill:block:overbuild_protector`

Use this block shape:

```text
<!-- arch_skill:block:overbuild_protector:start -->
## Overbuild Protector (scope triage)

Summary:
- Mode: <report|apply>, Strict: <0|1>, Focus: <... or n/a>
- Items reviewed: <n>
- Include (ship-blocking): <n> (A: <n>, B: <n>, C: <n>, D: <n>)
- Optional (timeboxed): <n>
- Follow-ups (out of scope): <n>
- Rejected (bug vectors): <n>

Include (ship-blocking):
- <item> - Bucket <A|B|C|D> - Evidence: <doc sections> - Anchors: <paths/symbols if used>

Optional (timeboxed):
- <item> - Bucket <E> - Why optional: <...> - Evidence: <...>

Follow-ups (out of scope / intentionally deferred):
- <item> - Bucket <E|F> - Why deferred: <...> - Evidence: <...>

Rejected (bug vectors):
- <item> - Bucket <G> - Why reject: <...> - What to do instead: <smaller alternative>

Parity anchors used (if any):
- <path> - <pattern / contract>

Notes:
- Any scope-contract gaps that made classification lower-confidence:
  - <gap>
<!-- arch_skill:block:overbuild_protector:end -->
```

## Apply-mode rewrite rules

If `MODE=apply`:

- rewrite the existing phase plan in place
- keep Section 7 as the one checklist
- do not delete or rewrite already-completed checkbox items
- preserve stable task IDs
- remove follow-ups and rejected bug vectors from the phase plan
- keep optional work in the phase plan but label it clearly as optional, for example by prefixing `OPTIONAL:` or appending `(optional)`

## Stop condition

- if there is no authoritative phase plan, stop and point to `phase-plan`
- if the plan doc remains ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- otherwise stop after classification is recorded, and after the phase plan is rewritten when `MODE=apply`

## Console contract

- one-line North Star reminder
- one-line punchline
- `DOC_PATH` plus `MODE` and `STRICT`
- what was reclassified
- next action
