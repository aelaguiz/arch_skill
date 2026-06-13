---
name: plan-audit
description: "Audit any planning document format before work starts, or run plan-backed implementation-audit code review after code exists. Use when the user wants a plan, PRD, migration plan, architecture plan, checklist, issue body, inline plan, or design doc audited for North Star clarity, done-state requirements, ambiguity, constraints, tiny-team simplicity, depth-first risk, elegant architecture, existing-pattern fit, drift-proofing, side doors, deletes, proof gaps, and bug-vector reduction; or wants implemented code reviewed against that plan for code shape, ownership, SSOT, side-door closure, drift, caller fit, and elegance. Not for writing plans, implementing code, generic diff/PR review, choosing workflows, running tests, proving CI, or spawning review harnesses."
metadata:
  short-description: "Generic plan audit and plan-backed code review"
---

# Plan Audit

Use this skill to audit an existing planning artifact in whatever format it
already uses. It has two modes:

- `plan-readiness`: improve plan quality before work starts.
- `implementation-audit`: review implemented code against the plan after code
  exists.

The plan-readiness job is to make the plan clearer, safer, simpler, more
complete, more code-grounded, and easier to implement without building the
wrong thing.

The implementation-audit job is plan-backed code review: check whether the
implemented code fits the plan's architecture and quality bar without adding
duplicate truth, side doors, drift, bad caller shape, or unnecessary
complexity.

The skill audits plans. It does not dictate the user's workflow.

## Doctrine-Only Constraint

This is a doctrine-only, prompt-first skill. It ships agent guidance,
references, metadata, and examples. It must not become a deterministic harness,
runner, controller, rule engine, scorer, checklist executor, grep gate,
automated architecture validator, test runner, proof collector, truth arbiter,
or script-backed readiness judge.

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
- The user wants code already written for a plan reviewed against that plan's
  promises, phase scope, owner path, side-door closure, drift risks, caller
  shape, and elegance.

## Do Not Use When

- The user wants the plan written from scratch.
- The user wants implementation to start.
- The user wants a generic code diff, branch, or PR reviewed without a plan
  artifact. Use the host agent's normal review response for that.
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
- Use native subagents or parallel-agent features provided by the current
  coding harness for broad repo-backed audits whenever available. Treat this as
  required acceleration for independent read-only audit slices unless local
  instructions prohibit it or the audit is too small to split. The parent still
  owns synthesis.
- Do not mark ambiguity or constraint questions resolved until a decision owner
  resolves them and the plan carries the decision through.
- Findings must include consequence, evidence, and the concrete plan repair.
- In `implementation-audit` mode, do not run unit tests, integration tests,
  build commands, lint commands, or CI; do not ask for test logs; do not verify
  whether tests really ran; and do not investigate whether a completion claim
  is truthful.
- In `implementation-audit` mode, accept supplied test-pass claims as context.
  You may read changed test files as code when they matter to code review, but
  test execution remains out of scope.

## First Move

1. Resolve the plan artifact: file path, pasted plan, issue text, doc section,
   PRD, checklist, or named planning artifact.
2. Read local instructions and repo context when the plan is repo-backed.
3. Resolve the audit log path for non-trivial file-backed audits and read the
   existing audit log if present.
4. Decide the mode from the user's ask:
   - `plan-readiness` for pre-implementation plan quality audit.
   - `implementation-audit` for plan-backed code review after code exists.
5. For `implementation-audit`, read
   `references/implementation-audit-mode.md` and follow that mode contract.
6. For `plan-readiness`, read `references/progressive-audit-order.md`.
7. Read the smallest additional references needed for the scope:
   - `references/architecture-quality-canon.md` for the quality bar
   - `references/review-lenses.md` for lens definitions
   - `references/audit-log-contract.md` for sidecar ledger rules
   - `references/proper-audit-checklist.md` before a readiness verdict
   - `references/child-prompt-contract.md` before native subagent prompts
   - `references/output-contract.md` before final output

## Workflow

If the user asks for `implementation-audit`, use
`references/implementation-audit-mode.md`. Do not use the plan-readiness
workflow below.

1. Audit the artifact in its native format.
2. Extract the North Star, done-state requirements, requirements,
   non-requirements, constraints, non-constraints, assumptions, and complexity
   sources.
3. Identify real ambiguity and constraint questions that can change the built
   outcome.
4. For repo-backed plans, map and read all relevant code: owner paths, callers,
   comparable patterns, legacy paths, side doors, contracts, tests, docs,
   prompts, and generated artifacts. Use native subagents for broad independent
   read-only slices when available.
5. Run the required lenses from `references/review-lenses.md`.
6. Challenge the plan for simpler architecture, fewer live concepts, better
   ownership, depth-first proof, delete work, and drift-proof coupling.
7. Update the audit log when applicable.
8. Return a findings-first verdict using `references/output-contract.md`.

## Output Expectations

Return a concise, findings-first audit:

- plan-readiness verdict: `ready`, `not-ready`, `blocked-on-decision`, or
  `inconclusive`
- implementation-audit verdict: `approve`, `not-approved`, or
  `scope-inconclusive`
- plan artifact and audit log path when applicable
- required repairs first
- observations or out-of-scope follow-ups only when they matter
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
- `references/implementation-audit-mode.md` - plan-backed code review mode after implementation
- `references/audit-log-contract.md` - sidecar audit log shape and loop rules
- `references/proper-audit-checklist.md` - final "was this audited properly" check
- `references/child-prompt-contract.md` - native subagent prompts for broad audits
- `references/output-contract.md` - final verdict and finding format
- `references/examples.md` - examples and anti-examples that teach judgment
