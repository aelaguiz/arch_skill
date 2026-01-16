---
description: Start a new architecture doc from the canonical template (single-doc rule).
argument-hint: TITLE="<title>" DATE=YYYY-MM-DD
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Create a new architecture document in `docs/` using the template below.
Name the file yourself using this rule:
- `docs/<TITLE_SCREAMING_SNAKE>_<DATE>.md`
- TITLE_SCREAMING_SNAKE = TITLE uppercased, spaces → `_`, punctuation removed.
Example: TITLE="PSV2 — Foo — Architecture Plan" DATE=2026-01-16
→ `docs/PSV2_FOO_ARCHITECTURE_PLAN_2026-01-16.md`
Apply the **single-document rule**: all planning and decisions live in this doc.
Do not create additional planning docs.
Write the filled template into the new doc file. Do not paste the full document to the console.

DOCUMENT CONTENT FORMAT (write to the new doc file):

---
title: "<PROJECT> — <CHANGE> — Architecture Plan"
date: <YYYY-MM-DD>
status: draft | active | complete
owners: [<name>, ...]
reviewers: [<name>, ...]
doc_type: architectural_change | parity_plan | phased_refactor | new_system
related:
  - <links to other docs, PRs, designs>
---

# TL;DR

- **Outcome:** <one sentence, falsifiable>
- **Problem:** <one sentence>
- **Approach:** <one sentence>
- **Plan:** <phases in 1–2 lines>
- **Non-negotiables:** <3–7 bullets>

---

# 0) Holistic North Star

## 0.1 The claim (falsifiable)
> <If we do X, then Y is true, measured by Z, by date/condition W>

## 0.2 In scope
- <explicitly list what this plan covers>

## 0.3 Out of scope
- <explicitly list what this plan will NOT do>

## 0.4 Definition of done (acceptance tests)
- <observable acceptance criteria, not vibes>
- Metrics / thresholds:
  - <metric>: <threshold>, measured via <harness>

## 0.5 Stop-the-line invariants
- <if these fail, we stop and fix before continuing>
- Example: “No silent fallbacks.” “No dual sources of truth.” “No undefined behavior.”

---

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)
1) <#1>
2) <#2>
3) <#3>

## 1.2 Constraints
- Correctness:
- Performance:
- Offline / latency:
- Compatibility / migration:
- Operational / observability:

## 1.3 Architectural principles (rules we will enforce)
- <e.g., fail-loud boundaries, DI rules, no business logic in UI, etc.>

## 1.4 Known tradeoffs (explicit)
- <tradeoff> → chosen direction + why
- Alternatives rejected + why

---

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today
- <system overview in 5–10 bullets>
- Primary flows / control paths:
  - <flow A>
  - <flow B>

## 2.2 What’s broken / missing (concrete)
- Symptoms:
- Root causes (hypotheses):
- Why now:

## 2.3 Constraints implied by the problem
- <constraints derived from reality, not preference>

---

# 3) Research Grounding (external + internal “ground truth”)

## 3.1 External anchors (papers, systems, prior art)
- <source> — <what we borrow / what we reject> — <why it applies>

## 3.2 Internal ground truth (code as spec)
- **Authoritative behavior anchors (do not reinvent):**
  - `<path>` — <what it defines>
- **Existing patterns we will reuse:**
  - `<path>` — <pattern>

## 3.3 Open questions from research
- Q1:
- Q2:
- What evidence would settle them:

---

# 4) Current Architecture (as-is)

## 4.1 On-disk structure
```text
<tree of relevant dirs/files>
```

## 4.2 Control paths (runtime)

* Flow A:

  * Step 1 → Step 2 → Step 3
* Flow B:

  * ...

## 4.3 Object model + key abstractions

* Key types:
* Ownership boundaries:
* Public APIs:

  * `Foo.doThing(args) -> Result`

## 4.4 Observability + failure behavior today

* Logs:
* Metrics:
* Failure surfaces:
* Common failure modes:

## 4.5 UI surfaces (ASCII mockups, if UI work)

```ascii
<ASCII mockups for current UI states, if relevant>
```

---

# 5) Target Architecture (to-be)

## 5.1 On-disk structure (future)

```text
<new/changed tree>
```

## 5.2 Control paths (future)

* Flow A (new):
* Flow B (new):

## 5.3 Object model + abstractions (future)

* New types/modules:
* Explicit contracts:
* Public APIs (new/changed):

  * `Foo.doThingV2(args) -> Result`
  * Migration notes:

## 5.4 Invariants and boundaries

* Fail-loud boundaries:
* Single source of truth:
* Determinism contracts (time/randomness):
* Performance / allocation boundaries:

## 5.5 UI surfaces (ASCII mockups, if UI work)

```ascii
<ASCII mockups for target UI states, if relevant>
```

---

# 6) Call-Site Audit (exhaustive change inventory)

## 6.1 Change map (table)

| Area     | File   | Symbol / Call site | Current behavior | Required change | Why         | New API / contract | Tests impacted |
| -------- | ------ | ------------------ | ---------------- | --------------- | ----------- | ------------------ | -------------- |
| <module> | <path> | <fn/cls>           | <today>          | <diff>          | <rationale> | <new usage>        | <tests>        |

## 6.2 Migration notes

* Deprecated APIs:
* Compatibility shims (if any):
* Delete list (what must be removed):

---

# 7) Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; every phase has exit criteria + explicit test plan.

## Phase 0 — Baseline gates

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

## Phase 1 — <foundation>

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

## Phase N — <end state + cleanup>

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

---

# 8) Test Strategy (beyond per-phase tests)

## 8.1 Unit tests (contracts)

* What invariants are unit-locked:

## 8.2 Integration tests (flows)

* Critical flows:
* Failure injection:

## 8.3 E2E / device tests (realistic)

* Scenarios:
* Artifacts captured:

---

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

* Flags / gradual rollout:
* Backward compatibility:

## 9.2 Telemetry changes

* New events:
* New properties:
* Dashboards / alerting:

## 9.3 Operational runbook

* Debug checklist:
* Common failure modes + fixes:

---

# 10) Decision Log (append-only)

## <YYYY-MM-DD> — <decision title>

* Context:
* Options:
* Decision:
* Consequences:
* Follow-ups:


---

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- Created doc: <path>
- <other summary item>
Open questions:
- <open question, if any>
