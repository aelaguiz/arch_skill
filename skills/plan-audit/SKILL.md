---
name: plan-audit
description: "Audit any planning document format before implementation or execution to improve plan quality against repo truth. Use when the user wants a plan, PRD, migration plan, architecture plan, checklist, issue-body plan, inline plan, or design doc audited for North Star outcome clarity, explicit done-state requirements, real ambiguity, constraints, tiny-team simplicity, depth-first implementation risk, elegant architecture, existing-pattern fit, drift-proofing, side doors, required deletes, proof gaps, and bug-vector reduction. Not for writing the plan, implementing it, reviewing a code diff, or choosing the user's workflow."
metadata:
  short-description: "Generic quality audit for planning docs"
---

# Plan Audit

Use this skill to audit an existing planning artifact in whatever format it
already uses. The job is to improve plan quality before work starts: make the
plan clearer, safer, simpler, more complete, more code-grounded, and easier to
implement without building the wrong thing.

The skill audits plans. It does not dictate the user's workflow.

## Doctrine-Only Constraint

This is a doctrine-only, prompt-first skill. It ships agent guidance,
references, metadata, and examples. It must not become a deterministic harness,
runner, controller, rule engine, scorer, checklist executor, grep gate,
automated architecture validator, or script-backed readiness judge.

The checklists are judgment aids. The audit log is a durable Markdown review
ledger beside the plan, not a state machine and not a second plan.

## Use When

- The user wants an existing plan, PRD, migration plan, architecture plan,
  checklist, issue-body plan, pasted plan, design doc, or strategy audited.
- The user wants stronger planning before implementation or execution.
- The user asks whether a plan is complete, clear, elegant, safe, simple,
  code-grounded, or ready.
- The user wants ambiguity, constraint, proof, side-door, delete, depth-first,
  drift, or existing-pattern risks found before work starts.

## Do Not Use When

- The user wants the plan written from scratch.
- The user wants implementation to start.
- The user wants a code diff, branch, PR, or completed implementation reviewed.
- The user asks which workflow or skill to use.

## Non-Negotiables

- Adapt to the plan's format. Do not require an arch-suite template, section
  numbering, or a specific checklist shape.
- Read the plan as written. Do not mentally repair it before auditing it.
- For repo-backed plans, read repo truth and all relevant code before approval.
- For non-trivial file-backed audits, create or update
  `<PLAN_STEM>_PLAN_AUDIT.md` beside the plan.
- For inline plans with no file path, return the audit in chat; suggest a
  persistent audit log only when the user wants repeat-audit tracking.
- Use parallel read-only agents for broad code reading when the user asks for
  them or local instructions allow them. The parent still owns synthesis.
- Do not mark ambiguity or constraint questions resolved until a decision owner
  resolves them and the plan carries the decision through.
- Findings must include consequence, evidence, and the concrete plan repair.

## First Move

1. Resolve the plan artifact: file path, pasted plan, issue text, doc section,
   PRD, checklist, or named planning artifact.
2. Read local instructions and repo context when the plan is repo-backed.
3. Resolve the audit log path for non-trivial file-backed audits and read the
   existing audit log if present.
4. Read `references/progressive-audit-order.md`.
5. Read the smallest additional references needed for the scope:
   - `references/architecture-quality-canon.md` for the quality bar
   - `references/review-lenses.md` for lens definitions
   - `references/audit-log-contract.md` for sidecar ledger rules
   - `references/proper-audit-checklist.md` before a readiness verdict
   - `references/child-prompt-contract.md` before parallel read-only children
   - `references/output-contract.md` before final output

## Workflow

1. Audit the artifact in its native format.
2. Extract the North Star, done-state requirements, requirements,
   non-requirements, constraints, non-constraints, assumptions, and complexity
   sources.
3. Identify real ambiguity and constraint questions that can change the built
   outcome.
4. For repo-backed plans, map and read all relevant code: owner paths, callers,
   comparable patterns, legacy paths, side doors, contracts, tests, docs,
   prompts, and generated artifacts.
5. Run the required lenses from `references/review-lenses.md`.
6. Challenge the plan for simpler architecture, fewer live concepts, better
   ownership, depth-first proof, delete work, and drift-proof coupling.
7. Update the audit log when applicable.
8. Return a findings-first verdict using `references/output-contract.md`.

## Output Expectations

Return a concise, findings-first audit:

- verdict: `ready`, `not-ready`, `blocked-on-decision`, or `inconclusive`
- plan artifact and audit log path when applicable
- blocking findings first
- non-blocking findings only when they matter
- real ambiguity and required decisions
- relevant code read and relevant code not yet read
- proper-audit checklist status
- the smallest next plan repair

Do not approve a plan while required code is unread, the audit log is stale, a
required lens could not inspect its scope, or an outcome-changing ambiguity or
constraint question remains unresolved or uncaptured in the plan.

## Reference Map

- `references/architecture-quality-canon.md` - strict plan-quality and code-quality doctrine
- `references/review-lenses.md` - required and conditional audit lenses
- `references/progressive-audit-order.md` - ordered pass for using the skill
- `references/audit-log-contract.md` - sidecar audit log shape and loop rules
- `references/proper-audit-checklist.md` - final "was this audited properly" check
- `references/child-prompt-contract.md` - read-only child prompts for broad audits
- `references/output-contract.md` - final verdict and finding format
- `references/examples.md` - examples and anti-examples that teach judgment
