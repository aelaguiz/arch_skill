# Integrating `docs/testing_guide.md` into our prompts (and killing low‑value tests)

Date: 2026-01-31  
Scope: `arch_skill` prompts in `prompts/` (plus any prompt templates that shape “test plans”).

## Why this doc exists

We are currently getting the **worst failure mode of AI testing**: coverage-driven, low-signal, high-maintenance tests (“is this deleted file referenced?”, “is this image still yellow?”). These create churn, slow PRs, and provide near-zero regression protection.

`docs/testing_guide.md` is the policy antidote: **value-driven testing + restraint**. The goal here is to make that judgment *default behavior* in our prompts, so the agent:

- writes tests **only when they buy real confidence**,  
- chooses the **right level** of test (unit vs widget vs integration),  
- and is willing to **delete negative-value tests** instead of cargo-cult updating them.

This doc audits where our prompts currently under-specify test judgment, and proposes concrete prompt changes to bake in the guide.

---

## Evidence from real FLUTTER plans (psmobileX)

I skimmed real plan docs under:

- `~/workspace/psmobile/docs/FLUTTER/**`
- `~/workspace/psmobile2/docs/FLUTTER/**`
- `~/workspace/psmobile3/docs/FLUTTER/**`
- `~/workspace/psmobile4/docs/FLUTTER/**`
- `~/workspace/psmobile5/docs/FLUTTER/**`
- `~/workspace/psmobile6/docs/FLUTTER/**`

Key observation: a lot of those docs match our `arch-new` template structure almost verbatim (`0.4 Definition of done`, phased plan with `Test plan (smallest signal)`, and `# 8) Test Strategy`). That means **our prompts absolutely shape “test decisions” upstream**, even before implementation.

Concrete examples (repo-relative to each `psmobileX`):

- `docs/FLUTTER/DONE/TESTING_OVERREACH_AUDIT_2026-01-20.md` inventories exactly the kinds of negative-value tests we keep seeing:
  - golden snapshot suites
  - screenshot pack “parity” tests
  - **doc-driven preflight gates** (tests that read docs / enforce doc inventories)
- `docs/FLUTTER/DONE/TESTING_OVERREACH_REMOVAL_2026-01-20.md` explicitly calls out removing “doc-driven gates” and not replacing them with new harnesses.
- `docs/FLUTTER/PLANS/DEV_PLAYGROUND_FOR_EXHAUSTIVE_FLUTTER_COMPONENT_REVIEW_2026-01-29.md` shows a common drift pattern:
  - plans that start as “small guardrail” can naturally slide into adding more `test/preflight/*` gate tests as “executable specs”.

So the fix isn’t just “teach implement to not write dumb tests”. We also need to adjust:

1) the language in planning templates (so we don’t encode “tests as proof” everywhere), and  
2) reviewer prompts (so reviewers don’t demand more brittle gates).

## Core principles to bake into prompts (from `docs/testing_guide.md`)

### 1) Optimize for confidence per maintenance hour
The objective isn’t “more tests” or “higher coverage”. It’s:

> Catch important bugs cheaply, and avoid tests that break for unrelated reasons.

### 2) Prefer the cheapest “high-signal” proof
In many PRs, the best evidence is **existing checks**:

- typecheck / compile
- lint / format
- a small, already-existing targeted test suite
- a minimal manual QA checklist (for subjective UI)

### 3) Negative-value tests are worse than no tests
The guide’s “seven deadly sins” should be encoded as explicit **hard nos** in code-writing prompts:

- tests that “prove” deleted code isn’t used (compiler/static analysis already does this)
- tests of visual constants (colors, spacing, exact margins)
- tests of trivial model existence / getters / setters
- snapshot tests of internal state / implementation details
- goldens on unstable UI (unless UI is locked down + goldens are already a stable practice)
- tests that require `Future.delayed` / timing hacks
- order-dependent tests

Also (psmobile-specific but broadly applicable): **doc-driven gates** are often negative value.
If a “test” is really “parse a markdown inventory and assert the repo matches it”, treat that as a smell. Prefer:
- compiler/typecheck,
- repo search checks during review,
- or a purpose-built lint/static check only when it’s truly stable and high-value.

### 4) Test behavior, not implementation details
If a refactor breaks the test without changing user-facing behavior, the test is wrong.

### 5) Right tool for the job (Flutter pyramid, generalized)
Flutter framing maps well to other stacks:

- **Unit** tests: pure logic / transforms / state transitions (cheap + durable)
- **Widget/component** tests: user interaction behavior (tap/submit/empty state/disabled state)
- **Integration/E2E** tests: critical flows only (auth/checkout/core loops), because they’re expensive and flaky

### 6) Prefer real objects/fakes over heavy mocking
Heavy mocking is a smell and tends to produce tests that “verify mocks work”.

---

## A shared “testing rubric” we should embed in prompts

This is the decision logic that should guide *every* prompt that can write tests.

### When to write tests (high-value triggers)
Write or extend tests when at least one is true:

1) **Bug fix**: a real bug exists and can be reproduced → add a regression test at the cheapest level that would have caught it.
2) **New or changed business logic / state transitions**: add unit tests (or bloc/cubit tests) for edge cases + error handling.
3) **User-facing behavior at an integration point**: add widget/component tests that assert observable behavior (loading state, disabled button, empty state, retry behavior).
4) **Critical user journey**: add/extend an integration test only if the repo already supports stable E2E for this surface *and* the flow is a true “core path”.

### When NOT to write tests (default skip cases)
Skip new tests when:

- change is a refactor with no behavior change and existing tests already cover it
- change is “delete dead code” / cleanup / rename and compiler + typecheck prove correctness
- change is purely visual/aesthetic or design-tweak in an unstable UI (prefer manual QA)
- tests would be brittle or expensive relative to the risk

### What tests to delete or rewrite (and when)
If a test is clearly “negative value” (breaks on refactor, asserts constants, tests deletions, etc.), our prompts should allow:

- **delete it** (preferred) or rewrite it to a behavior-level assertion,
- as long as we run the relevant checks after and note it in the PR (“removed brittle test that asserted X constant; replaced with Y behavior test / manual checklist”).

Important: we should not go “test hunting” in unrelated areas. Do this when:

- the test blocks the current PR (failing/flaky), or
- you’re already modifying the feature and the test is obviously nonsense.

---

## Prompt audit: where to integrate these rules

Below is an audit of prompts that influence test creation (directly or indirectly), and exactly what to change.

### A) Code-writing prompts (highest priority)

#### `prompts/arch-implement.md`
Current: says “add only minimal tests/instrumentation” but doesn’t explicitly forbid negative-value tests. This is the main opening for “stupid tests”.

Proposed change:
- Add a **Testing Discipline (value-driven)** block near the existing “Verification policy (autonomy-first)” section.
- Include explicit “DO NOT write” examples mirroring the guide (deleted code, visual constants, trivial getters, mock-only tests, flaky timing).
- Add explicit permission to **delete negative-value tests** that block progress, with justification.

#### `prompts/arch-implement-agent.md`
Same issue as `arch-implement.md`.

Proposed change:
- Same Testing Discipline block, plus a reminder for subagents: don’t propose/implement pointless tests; prefer smallest checks; remove brittle tests when encountered.

#### `prompts/arch-open-pr.md`
Current: FAST mode runs lint/typecheck/compile + relevant tests, avoids full-suite. This is good.

Proposed change:
- Add a short rule: if FAST checks fail due to a clearly negative-value test, prefer deleting/rewriting that test instead of “fixing it” to keep it passing.
- Require compile/build to be **per-active-app** in monorepos (already added) + record commands in PR.

#### `prompts/qa-autopilot.md` and `prompts/maestro-autopilot.md`
These can generate/modify E2E/UI automation. The testing guide’s main warning still applies: avoid brittle assertions and avoid “visual constant” testing.

Proposed change:
- Add a short “High-signal assertions only” rule:
  - assert user-visible behavior (screen reached, key text present, button disabled/enabled, toast shown)
  - avoid pixel/color/margin assertions unless the repo has a stable golden discipline
  - avoid delays; prefer waiting on real conditions (ids, network idle, deterministic signals)

### B) Planning prompts (shape test plans before code exists)

These prompts influence how agents *think* about verification. If phase plans demand “tests” with no judgment, the implement prompt will dutifully invent nonsense.

#### `prompts/arch-new.md` (plan template)
Current: “Definition of done” is good but could better encode “restraint”.

Proposed change:
- In the plan template’s “Evidence plan”, add one line: “Avoid negative-value tests (see: deleted code / visual constants / trivial getters / brittle snapshots / doc-driven gates). Prefer compile/typecheck/lint + a small behavior test only when needed.”
- Consider changing the template wording from “explicit test plan” → “explicit verification plan (tests optional)”.

#### `prompts/arch-phase-plan.md` (+ `prompts/arch-phase-plan-agent.md`)
Current: phase plan includes “explicit test plan”, but doesn’t define what a good test plan is.

Proposed change:
- Rename semantics in the template from “Test plan” → “Verification plan (smallest signal)”.
- Add a rule: each phase’s verification must be the smallest signal that would catch real regressions; tests are not required if compile/typecheck is sufficient.
- Add “DO NOT” bullets (no deletion tests, no visual constants, no mock-only tests).

#### `prompts/arch-plan-enhance.md` / `prompts/arch-reformat.md`
Current: says “prefer existing tests/checks; avoid verification bureaucracy”.

Proposed change:
- Add a short negative-value test list so “avoid bureaucracy” doesn’t translate into “write the easiest test imaginable”.

### C) Review/audit prompts (stop reviewers from demanding bad tests)

#### `prompts/arch-review-gate.md`
Current: asks reviewers for idiomatic + completeness relative to plan.

Proposed change:
- Add reviewer instruction: if suggesting tests, suggest only high-signal, refactor-resistant tests; explicitly call out and recommend deleting negative-value tests.

#### `prompts/arch-codereview.md` (Claude CLI)
Current: asks for test coverage recommendations (already “relevant only, not full-suite”).

Proposed change:
- Add a line to the Claude prompt: “Do not recommend negative-value tests (deleted code checks, visual constants, trivial getters, mock-only tests). Prefer compile + behavior tests.”
  - This keeps Claude from “helpfully” suggesting useless coverage.

#### `prompts/arch-audit-implementation.md` (+ agent variant)
Current: verifies deletes/cleanup and evidence exists. This is fine, but we should ensure it doesn’t create pressure to invent tests to “prove deletions”.

Proposed change:
- Add a rule: “Verification of deletes is via search/static analysis, not tests.”

---

## Suggested “Testing Discipline” snippet (copy/paste into code-writing prompts)

This is the minimal block to add to `arch-implement*` (and optionally `arch-open-pr`).

**Testing discipline (value-driven; avoid negative-value tests):**
- Default: prefer existing checks (typecheck/compile/lint + existing targeted tests). Do not add tests unless they buy real confidence.
- Write tests when:
  - a bug was found (add a regression test at the cheapest level),
  - new logic/state transitions were introduced,
  - user-visible interaction behavior changed (behavior-level assertions).
- Do NOT write tests that:
  - “prove” deleted code isn’t referenced,
  - assert visual constants (colors/margins/pixel values),
  - test trivial getters/setters/models/framework behavior,
  - assert only mock interactions (`verify(mock.foo()).called(1)` with no behavior),
  - require `Future.delayed` or depend on ordering.
- If you encounter an existing negative-value test that blocks progress, prefer deleting or rewriting it to test real behavior (note it in the PR).

---

## Rollout plan (how I’d implement this safely)

1) Update the highest-leverage prompts first:
   - `arch-implement.md`, `arch-implement-agent.md`, `arch-phase-plan.md`, `arch-open-pr.md`
2) Update reviewers to stop demanding nonsense:
   - `arch-review-gate.md`, `arch-codereview.md`
3) Update automation prompts (Maestro/QA) with “behavior not pixels” guardrails.
4) After rollout, spot-check:
   - Do we still get low-value tests added?
   - Are we deleting brittle tests when appropriate?
   - Are PRs still getting sufficient confidence signals?

If you want, I can apply the prompt edits in a follow-up change once you sign off on this integration plan.
