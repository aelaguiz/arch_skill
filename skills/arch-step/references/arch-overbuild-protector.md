# `overbuild-protector` Command Contract

## What this command does

- compare the authoritative phase plan against the explicit scope contract already recorded in the artifact
- classify phase-plan work items into explicit scope buckets
- separate clearly required work from work explicitly outside the current code-completion boundary, product scope creep, architecture theater, and unresolved requiredness that must go back to the user
- in apply mode, rewrite the phase plan in place so the main checklist is mechanically scope-safe

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `skills/_shared/scope-and-convergence.md`
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
- Section 0 `Scope and Simplicity Contract`, including authorization anchors,
  frozen initial convergence closure, freeze boundary, and explicit human
  expansion entries in Section 10

If those sections are vague on a work item, do not reclassify it by taste. Record a blocker question in the helper block and stop when that gap affects Section 7 readiness.

The only automatic keep lanes are work directly required by human scope and
work already recorded in the pre-freeze minimal convergence closure. A real
correctness concern, pattern parity, or newly found competing path after freeze
may be important, but it becomes `new-scope-needs-human`, not required work.
Already-built unauthorized scope becomes subtraction work.

## Writes

- `arch_skill:block:overbuild_protector`
- in `MODE=apply`, the existing phase plan rewritten in place

## Hard rules

- docs-only; do not modify product code
- this command is remediation and reporting, not the only overbuild defense in the skill
- Section 7 remains the one authoritative execution checklist
- if no phase plan exists, stop and point to `phase-plan`; do not invent a new plan format
- use code and repo evidence only to validate convergence, parity, or risk claims; do not invent obligations
- for agent-backed systems, classify proposed tooling against prompt-first and capability-first alternatives before treating it as necessary
- treat docs-audit scripts, stale-term greps, absence checks, repo-structure tests, and CI cleanliness gates as architecture theater by default unless the user explicitly asked for that tooling class
- do not downgrade a work item to optional, deferred, or follow-up unless the existing artifact already makes that status explicit
- when requiredness is unclear, surface a blocker question instead of making a pruning decision on the agent's behalf

## Work-item extraction

- prefer explicit checklist items under `Checklist (must all be done)`
- otherwise prefer explicit checkbox items
- preserve stable task IDs if they exist
- if there is no checklist, treat each top-level `Work` bullet as a work item
- if the plan is too unstructured for reliable item extraction, classify at the phase level instead

## Classification buckets

- `A` Explicit ask:
  - directly requested by the user, TL;DR, or in-scope sections
- `B` Convergence necessary:
  - required to route the requested behavior through a canonical path, remove duplicate truth, or prevent a new parallel path
  - common examples include shared-path extraction, touched-area call-site migrations, deletes or cleanup that remove parallel truth, and clearly related adopters that must converge now to avoid drift
- `C` Anchored pattern or parity necessary:
  - required to match an existing internal pattern or contract, with a real repo anchor
- `D` Concrete regression or correctness risk necessary:
  - work needed to avoid a concrete regression, correctness failure, or refactor-induced behavior change
- `E` Optional quality:
  - explicitly outside the current code-completion boundary by user choice or existing plan text
- `F` Product scope creep:
  - expands requested UX or product capability beyond what the ask or Section 0 approved
- `G` Architecture theater / speculative infra:
  - adds new layers, surfaces, or complexity that are not required to ship the ask cleanly
- `Q` Blocker question:
  - requiredness is not derivable from repo truth plus the approved plan, so the user must decide before the plan can be called ready

Default reject examples for `F` or `G` unless explicitly approved:

- new user-visible commands, modes, or toggles
- template systems, plugin surfaces, or config layers not required by the ask
- dry-run or preview surfaces for a simple feature request
- runtime fallbacks or shims when fallbacks are forbidden
- new deleted-code proof tests
- visual-constant or churn-heavy golden tests
- coverage gates or bespoke coverage infrastructure
- docs/help audit scripts
- stale-term grep gates
- file-absence or folder-absence proof checks
- repo-structure or taxonomy-policing tests
- CI checks on keyword absence or comment cleanliness
- new remote-runner or distributed-execution wiring for local development tasks
- new generators or frameworks introduced just to save small amounts of time
- OCR pipelines when the runtime already has native vision
- fuzzy matcher or retrieval wrappers when grounded file access and synthesis are the intended path
- parser, wrapper, or orchestration layers whose main purpose is to make the model deterministic instead of improving prompt or capability use

Tie-breakers:

- `STRICT=1`:
  - ambiguity becomes a blocker question, not a downgrade
- `STRICT=0`:
  - ambiguity still becomes a blocker question
- convergence or parity is never assumed without a real anchor
- new tooling is never downgraded into follow-up by default; either it is explicitly outside the current code-completion boundary or it becomes a blocker question
- repo-policing heuristics are rejected unless the user explicitly asked for them
- tooling that substitutes for native capability or prompt work is rejected unless necessity is explicit

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
- Follow-ups (deferred): <n>
- Blocker questions: <n>
- Rejected (creep / theater): <n>

Include (ship-blocking):
- <item> - Bucket <A|B|C|D> - Evidence: <doc sections> - Anchors: <paths/symbols if used>

Optional (timeboxed):
- <item> - Bucket <E> - Why optional: <...> - Evidence: <...>

Follow-ups (out of scope / intentionally deferred):
- <item> - Bucket <E|F> - Why deferred: <...> - Evidence: <...>

Blocker questions:
- <item> - Bucket <Q> - Why user input is required: <...> - Evidence checked: <...>

Rejected (product creep / architecture theater):
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
- remove product scope creep and architecture theater from the phase plan
- keep optional work in the phase plan but label it clearly as optional, for example by prefixing `OPTIONAL:` or appending `(optional)`
- do not rewrite uncertain requiredness into optional or follow-up; leave it as a blocker question instead

## Stop condition

- if there is no authoritative phase plan, stop and point to `phase-plan`
- if the plan doc remains ambiguous after best effort, ask the user to choose from the top 2-3 candidates
- if blocker questions remain, stop with those questions instead of claiming the phase plan is now safely classified
- otherwise stop after classification is recorded, and after the phase plan is rewritten when `MODE=apply`

## Console contract

- one-line North Star reminder
- one-line punchline
- `DOC_PATH` plus `MODE` and `STRICT`
- what was reclassified
- next action
