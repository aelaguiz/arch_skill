# Integrating “pattern documentation via code comments” into our prompts

Date: 2026-02-02  
Scope: `arch_skill` prompts under `prompts/` (planning + implementation + review prompts).

## Why this matters

Our best long-term defense against drift isn’t more process — it’s **propagating the right mental model into the codebase**.

When we introduce a new SSOT, contract, or tricky behavior, the *next* engineer/agent will:

- grep for the entrypoint,
- read the top-level contract files,
- and then change something “obvious”.

If the code doesn’t teach the invariants/gotchas **at the point of use**, we’ll keep paying for it.

This is not “comment everything”. It’s:

> Put short, high-leverage comments in the places that future engineers will read, explaining the rules that must survive refactors.

Good examples exist in real systems: a single line like “phase is a mode signal, not proof snapback is active” can prevent days of future debugging.

---

## What “high-leverage comments” are (and are not)

### We want comments that propagate:
- **Architectural intent**: why this module exists and what it owns (SSOT boundaries).
- **Invariants**: what must always be true (and what to do if violated).
- **Gotchas / sharp edges**: what looks equivalent but is not (e.g., “mode signal vs worklet status”).
- **Extension rules**: how to add a new variant/case without reintroducing drift.
- **Cross-platform ground truth** (when relevant): “RN spec is X; Flutter must match Y; this is where to change it.”

### We explicitly do NOT want:
- Comments that restate the code (“increment i by 1”).
- Comment spam or per-line narration.
- Visual-constant commentary that becomes a maintenance trap (“this color must be exactly #…”) unless it’s a stable design token contract.
- Comments that encode temporary project state (“as of this PR…”) unless that’s the point (and it’s a deliberate migration note).

---

## When to add comments (decision rubric)

Add a comment when at least one is true:

1) **Non-obvious behavior**: a reasonable engineer could misunderstand it and ship a bug.
2) **Drift risk**: the change is a “central pattern” likely to be copy/pasted or reimplemented incorrectly elsewhere.
3) **Boundary seam**: cross-thread / async / cache / “multiple truths” area where ordering matters.
4) **Invariant enforcement**: clamping/validation exists for a reason; future changes could remove it.
5) **Public API / contract**: callers will use it without reading the implementation.

Skip comments when:
- the code is obvious and the type system already communicates intent,
- it’s purely aesthetic or likely to churn,
- the “comment” would be better as a test name, log message, or a small helper function name.

---

## Preferred comment formats (keep it short)

### For SSOT / contracts (doc comment above the type/function)

Use a small structured comment:

```
/// SSOT: <what this module owns>.
/// Invariant: <what must always be true>.
/// Gotcha: <what looks similar but is not>.
/// Extending: <how to add cases without drift>.
```

### For a single sharp edge (one-liner near the condition)

```
// NOTE: <non-obvious truth> (prevents <class of bug>).
```

---

## Prompt audit: where to bake this in

### 1) Planning prompts (to make it part of the North Star)
The plan is where we decide what must propagate forward. If the plan doesn’t mention documentation, implementation will treat it as optional.

Update:
- `arch-new` template and `arch-reformat` template:
  - add a “pattern propagation” principle: when we introduce a new contract/SSOT/gotcha, we add a doc comment in the canonical location.
  - add a per-phase “Docs/comments (propagation)” line (optional; only when needed).
- `arch-phase-plan*` templates:
  - same per-phase “Docs/comments” line so the plan explicitly calls out where the canonical comment should live.

### 2) Implementation prompts (to actually do it)
Implementation prompts should treat “comment the tricky bits” as part of drift-proofing, alongside deletes and SSOT enforcement.

Update:
- `arch-implement*`:
  - add a short “Pattern documentation (propagation comments)” rule:
    - comment only high-leverage bits,
    - prefer doc comments on SSOT/contract modules,
    - ensure comments describe invariants/gotchas/extension rules.

### 3) Review prompts (to enforce it without comment spam)
Reviewers should call out missing high-leverage comments, but should not demand “comment everything”.

Update:
- `arch-review-gate` and `arch-codereview`:
  - explicitly ask: “Are the new patterns/gotchas documented at the canonical boundary (doc comments)?”
  - also: “avoid comment spam; only request comments where they prevent likely misuse.”

---

## Rollout (safe and incremental)

1) Add the guidance to planning + implementation prompts first (`arch-new`, `arch-phase-plan*`, `arch-implement*`).
2) Add review enforcement next (`arch-review-gate`, `arch-codereview`).
3) Spot-check a few PRs:
   - Are we getting fewer “future agents will miss this” bugs?
   - Are comments staying small + high-value (no spam)?
   - Are we documenting at the canonical boundary (SSOT file), not scattered?

