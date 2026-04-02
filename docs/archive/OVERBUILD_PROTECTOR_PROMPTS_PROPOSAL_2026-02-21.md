# Overbuild Protector (Optional) - Prompt Proposal

Date: 2026-02-21
Scope: `arch_skill` architecture planning docs (`docs/<...>.md`) produced by the `arch-*` flow prompts (especially `arch-new` -> `arch-phase-plan` -> `arch-implement(-agent)`), with the explicit goal of preventing overbuilding and scope creep (especially when executing plans with smaller models/agents).

## TL;DR

Add an optional, re-entrant "overbuild protector" planning pass that can be run as a single command:

- `/prompts:arch-overbuild-protector DOC_PATH [MODE=report|apply] [STRICT=0|1]`
- Future (optional): `/prompts:arch-overbuild-protector-agent DOC_PATH ...` (uses read-only subagents to ground parity claims and find existing repo patterns)

It reads the existing plan doc and produces a deterministic scope classification for each planned work item (especially Phase Plan tasks), sorting them into buckets such as:

- Explicit Ask (directly requested)
- North-Star Necessary (required to satisfy the falsifiable claim / acceptance evidence)
- Parity Necessary (required to match codebase conventions or existing integration contracts)
- Risk Mitigation Necessary (required to avoid regressions / data loss / security/perf cliffs)
- Optional Quality (nice-to-have; not ship-blocking)
- Scope Creep (out of scope; move to follow-ups)
- Bug Vector (reject unless explicitly approved; high risk / long-lived complexity)

Default behavior is conservative:
- If an item cannot be justified by Explicit Ask / North-Star / Parity / Risk, it does not get to be "in scope by default".
- Ambiguous "good ideas" get moved to Follow-ups (out of scope), not treated as mandatory.
- The pass is designed to be safe to run without manual intervention: it does not block execution, it clarifies and (optionally) rewrites the plan so smaller agents do not "helpfully" expand it.

This pass does not replace existing plan audits:
- `arch-plan-audit` is about completeness + idiomatic + call-site coverage.
- This proposal is about scope discipline and overbuild prevention.

---

## Why This Exists

Smaller models/agents frequently overbuild because they:
- conflate "could be useful" with "must be done now",
- treat tooling/automation/coverage as universally required,
- invent infrastructure (remote runners, harnesses, generators, config systems) that was not asked for,
- and accumulate "check spirals" (verification bureaucracy) instead of shipping the requested outcome.

Concrete example failure mode:
- Ask: "build a fixture builder"
- Overbuild: remote execution wiring, coverage analysis generators, new CLI frameworks, bespoke reporting dashboards, etc.

The outcome is negative:
- It expands scope, adds bug vectors, increases future maintenance, and delays shipping.
- It also makes it harder to reason about correctness because more surface area changes at once.

We want a sanctioned, explicit scope triage controller so that:
- the plan becomes self-defending against overbuild,
- the user can opt into a deterministic classification pass at any time,
- and execution agents can follow the "in scope" checklist without improvising.

---

## Non-Goals (Explicit)

This pass is not allowed to:
- Implement any code (planning-only).
- "Improve architecture" for its own sake (that's `arch-plan-enhance`).
- Add new verification harnesses by default (screenshots, goldens, coverage gates, deleted-code tests).
- Create long-lived runtime fallbacks/shims (still governed by `fallback_policy`, default forbidden).
- Turn into a second checklist (single SSOT rule still applies).

---

## Where It Fits In The arch_skill Flow

Recommended placement (regular flow):
1) `arch-new` (North Star confirmed)
2) `arch-research` / `arch-deep-dive`
3) `arch-phase-plan`
4) Optional: `arch-plan-enhance`
5) Optional: `arch-fold-in` (if binding specs exist)
6) `arch-overbuild-protector` (optional; this proposal)
7) Optional: `arch-phase-plan-granularize` (microtasking for small agents)
8) `arch-implement(-agent)`

Re-entrancy:
- You can re-run the overbuild protector after granularize too (to ensure microtasking did not smuggle in scope creep).

Mini / lilarch:
- This can be run whenever there is a Phase Plan block.

---

## Core Concept: Two Outputs, Not One Bucket

To be deterministic, we split classification into two orthogonal dimensions:

1) Justification (why does this exist?)
2) Disposition (what happens to it?)

This prevents confusion like:
"this is a good idea" (justification unclear) being treated as "in scope" (disposition include).

### 1) Justification (one of these must be true to be ship-blocking)

J1: Explicit Ask
- Directly requested by the user blurb / TL;DR / in-scope UX surfaces.

J2: North-Star Necessary
- Required to satisfy the falsifiable claim and/or the Definition of Done evidence.
- Common examples: call-site migrations, deletes to avoid parallel truths, correctness fixes, minimal verification.

J3: Parity Necessary
- Required to match an existing codebase convention or integration contract.
- Parity must be evidenced: cite a concrete anchor (file path, existing harness name, existing pattern).

J4: Risk Mitigation Necessary
- Required to avoid known failure modes: data loss, security exposure, correctness regression, perf cliff, migration safety.
- Risk claims must be evidenced (doc constraint or code reality).

If none apply, the justification is:

J5: Optional Quality
- Nice-to-have, "would be neat", or "best practice", but not required to ship the defined outcome.

### 2) Disposition (what we do with it by default)

D1: Include (ship-blocking)
- Keep in Phase Plan as required work.

D2: Include (optional / timeboxed)
- Keep in plan but explicitly mark as optional; do not block shipping.

D3: Follow-up (out of scope)
- Move to a "Follow-ups (out of scope)" section with anchors.

D4: Reject (bug vector)
- Remove from plan; record as explicitly rejected unless user overrides with approval.

---

## The Buckets (What The Command Produces)

For usability, the prompt surfaces buckets as a single label per item.

Bucket A - Explicit Ask (D1 Include)
Definition:
- Directly requested or directly implied by the explicitly listed in-scope UX surfaces / technical scope.
Evidence sources (must cite at least one):
- `# TL;DR`
- `0.2 In scope`
- `0.4 Definition of done`
Default behavior:
- Keep in Phase Plan.
Example:
- "Add a fixture builder with ergonomic constructors for test data."

Bucket B - North-Star Necessary (D1 Include)
Definition:
- Without this item, the falsifiable claim likely fails or acceptance evidence cannot be gathered.
Common necessary items (often forgotten):
- Deletes/cleanup to prevent parallel sources of truth.
- Migration sequencing to avoid partial cutovers.
- Smallest credible verification signal (existing tests / build checks).
Default behavior:
- Keep in Phase Plan.
Example:
- "Migrate all call sites to new SSOT, then delete old store."

Bucket C - Parity Necessary (D1 Include)
Definition:
- Required to conform to existing repo conventions or to integrate into existing systems.
Hard requirement:
- Must cite an internal ground-truth anchor (path/symbol) proving the parity constraint exists.
Default behavior:
- Keep in Phase Plan.
Example:
- "Register fixtures via `tests/fixtures/index.ts` because the test harness imports from there."

Bucket D - Risk Mitigation Necessary (D1 Include, but minimal)
Definition:
- Required to avoid a concrete regression vector (data corruption, security, perf, build failures).
Guardrail:
- Must be minimal. Risk mitigation cannot become a new product scope.
Default behavior:
- Keep in Phase Plan, but prefer the smallest credible mitigation.
Example:
- "Add a migration to backfill required field before switching reads."

Bucket E - Optional Quality (D2 Optional or D3 Follow-up)
Definition:
- Improves maintainability or developer ergonomics but not required to ship the North Star.
Default behavior:
- If it's low risk and tiny: keep as optional/timeboxed.
- Otherwise: move to follow-ups (out of scope).
Example:
- "Refactor naming to be more consistent across the module."

Bucket F - Scope Creep (D3 Follow-up)
Definition:
- Expands user-visible UX or technical scope beyond what the plan doc declares in-scope.
- Or introduces new systems/harnesses not justified by North Star/parity/risk.
Default behavior:
- Move to follow-ups with anchors; do not implement now.
Example:
- "Add remote runner support so fixtures can execute on a server."

Bucket G - Bug Vector (D4 Reject)
Definition:
- Adds long-lived complexity, new failure modes, or brittle verification gates, without being necessary.
Default behavior:
- Reject; the overbuild protector explicitly says "do not do this" unless the user overrides.
Common bug vectors:
- New runtime shims/fallbacks (when `fallback_policy: forbidden`).
- New "deleted code not referenced" tests.
- Visual-constant/golden tests (pixels/margins/colors) in churny UI.
- Coverage gates / bespoke coverage reporting (unless already required by repo policy and evidenced).
- New codegen frameworks introduced to save a few minutes.

---

## Deterministic Classification Rules (The "If I Run It Blind" Contract)

The point of this pass is that you can run it without a debate every time.

Rule 0: The plan doc is authoritative for scope
Authoritative sources (in order):
1) `0) Holistic North Star` (in-scope / out-of-scope, definition of done)
2) Explicit constraints (no fallbacks, minimal verification)
3) Phase Plan tasks

If the doc is too vague to classify, the overbuild protector should:
- warn "scope contract is underspecified; expect false positives/negatives"
- still proceed conservatively (see Rule 4)

Rule 1: Every Phase Plan checkbox must have a justification
If a task is in Phase Plan but does not map to:
- Explicit Ask, or
- North-Star necessary, or
- Parity necessary (with evidence), or
- Risk mitigation necessary (with evidence),
then it cannot be ship-blocking.

Rule 2: Parity requires a code anchor (no invented parity)
You cannot claim parity unless you can cite:
- a file path,
- a symbol,
- or an existing harness/pattern that proves it is required.
No anchor -> not parity -> likely optional or scope creep.

Rule 3: New tooling is out-of-scope unless explicitly requested
Unless the North Star explicitly requires it, new tooling defaults to follow-up:
- remote runners
- coverage analysis tooling
- bespoke generators
- new CI gates
- new dashboards

Rule 4: Ambiguity defaults to "Follow-up", not "Include"
If it's unclear whether an item is required, the safe default for overbuild prevention is:
- move to follow-ups and keep the core checklist tight

This is intentionally biased toward under-building rather than scope creep.
The assumption is that a well-written North Star + acceptance criteria should list what "required" means.

Rule 5: Negative-value verification is treated as a bug vector
Even when framed as "risk mitigation", avoid verification bureaucracy that creates drift:
- brittle UI goldens
- doc-driven inventory gates
- "deleted code proofs"

If a test/harness already exists and is in use, integrate minimally.
If not, prefer an existing fast check or a short manual checklist.

---

## What The Prompt Writes Into DOC_PATH

Proposed new block marker:
- `<!-- arch_skill:block:overbuild_protector:start --> ... <!-- arch_skill:block:overbuild_protector:end -->`

Insert format (example):

```md
<!-- arch_skill:block:overbuild_protector:start -->
## Overbuild Protector (scope triage)

Summary:
- Items reviewed: <n>
- Include (ship-blocking): <n> (Explicit Ask: <n>, North-Star: <n>, Parity: <n>, Risk: <n>)
- Optional (timeboxed): <n>
- Follow-ups (out of scope): <n>
- Rejected (bug vectors): <n>

Decisions applied (MODE=apply only):
- Moved <items> from Phase Plan -> Follow-ups
- Marked <items> as Optional (non-blocking)
- Rejected <items> with reasons

Follow-ups (out of scope):
- <item> - reason - anchor(s)

Rejected (bug vectors):
- <item> - reason - what to do instead

Notes:
- Parity anchors used:
  - `<path>` - <pattern>
<!-- arch_skill:block:overbuild_protector:end -->
```

Mode behavior:

MODE=report (default):
- Writes the block with classifications and recommendations.
- Does not rewrite Phase Plan.

MODE=apply:
- Writes the block.
- Also edits Phase Plan in-place:
  - Keeps only D1 items as blocking checkboxes.
  - Moves D3 items into "Follow-ups (out of scope)" section.
  - Removes/rejects D4 items (but records them explicitly).
  - Marks D2 items clearly as optional/timeboxed so execution agents do not treat them as mandatory.

---

## Examples (How Items Get Classified)

These examples are meant to define the default behavior.

Example 1: "Build a fixture builder"

Requested:
- "I need a fixture builder for tests in this repo."

Planned items:
1) Implement `FixtureBuilder` with ergonomic defaults.
2) Wire it into the existing test harness.
3) Add a remote runner so fixtures can execute on a server.
4) Add a coverage analysis generator and publish HTML reports.
5) Add a small doc snippet showing usage.

Classification:
- (1) Explicit Ask -> Include
- (2) Parity Necessary (only if harness exists; must cite import point) -> Include
- (3) Scope Creep -> Follow-up
- (4) Bug Vector (tooling + gates + maintenance) -> Reject (unless explicitly approved)
- (5) Optional Quality -> Optional (timeboxed) or Follow-up (depending on size)

Example 2: "Add endpoint X"

Planned items:
1) Add endpoint and handler.
2) Update OpenAPI spec.
3) Add distributed tracing pipeline.
4) Add caching layer to "improve perf".

Classification:
- (1) Explicit Ask -> Include
- (2) Parity Necessary if repo uses OpenAPI as contract (must cite) -> Include
- (3) Scope Creep unless explicitly required -> Follow-up
- (4) Bug Vector unless perf risk is proven and mitigation is minimal -> Reject or Follow-up

Example 3: "Refactor to SSOT"

Planned items:
1) Introduce new SSOT module.
2) Migrate call sites in batches.
3) Keep old code path as runtime fallback "just in case".
4) Delete old SSOT.

Classification:
- (1) North-Star Necessary -> Include
- (2) North-Star Necessary -> Include
- (3) Bug Vector (fallback_policy forbidden) -> Reject
- (4) North-Star Necessary (avoid parallel truth) -> Include

Example 4: "Make UI component parity with existing app"

Planned items:
1) Implement component to match design tokens used elsewhere.
2) Add pixel-perfect screenshot tests.
3) Add new design token system.

Classification:
- (1) Parity Necessary (must cite token system) -> Include
- (2) Bug Vector unless harness already exists and is stable -> Reject or Follow-up
- (3) Scope Creep (new system) -> Follow-up

Example 5: "Fix bug Y"

Planned items:
1) Fix root cause.
2) Add smallest regression test in existing suite.
3) Rewrite module for cleanliness.

Classification:
- (1) Explicit Ask -> Include
- (2) Risk Mitigation Necessary if feasible in existing suite -> Include (minimal)
- (3) Optional Quality -> Follow-up (unless it is necessary to fix correctly)

Example 6: "Add minimal logging for debugging"

Planned items:
1) Add 1-3 targeted logs at boundary.
2) Add full log ingestion service and dashboard.

Classification:
- (1) Explicit Ask -> Include
- (2) Scope Creep / Bug Vector -> Follow-up or Reject (depending on complexity)

---

## Proposed Prompt Index + Flow Integration

If adopted, add to router index:
- `skills/arch-skill/resources/PROMPT_INDEX.md`:
  - "Overbuild protector / scope triage: `/prompts:arch-overbuild-protector <DOC_PATH>`"

Optional: update `arch-flow` checklist (as OPTIONAL) between Phase Plan and Implement:
- "Overbuild protector (optional): `/prompts:arch-overbuild-protector DOC_PATH MODE=apply`"

This makes the stage "sanctioned" and easy to reach, but still optional by default.

---

## Open Decisions (What We Should Agree On)

These are the knobs that determine how deterministic the system is:

1) Default bias: underbuild vs overbuild.
   - This proposal: default bias is "avoid overbuild", so ambiguity -> follow-up.
2) Bug vector list: which items are auto-rejected vs merely follow-ups.
3) Parity proof standard: what counts as an acceptable "parity anchor".
4) Apply mode: whether MODE=apply should be default or require explicit MODE=apply.

If these are agreed, we can implement the prompt(s) with a tight, mechanical procedure.
