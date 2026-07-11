# Audit Log Contract

For non-trivial file-backed audits, maintain a Markdown audit log beside the
plan:

```text
<PLAN_STEM>_PLAN_AUDIT.md
```

Example:

```text
docs/PAYMENTS_MIGRATION_PLAN.md
docs/PAYMENTS_MIGRATION_PLAN_AUDIT.md
```

The audit log is not a second plan. It is a durable review ledger used across
repeat audits while the plan is refined.

For inline or chat-only plans, return the audit in chat. Suggest a persistent
audit log only when the user wants looped refinement.

## Template

```markdown
# Plan Audit Log

Plan: <path>
Audit log: <path>
Current plan verdict: ready | not-ready | blocked-on-decision | inconclusive
Current implementation code review verdict: approve | not-approved | scope-inconclusive | not-run
Last reviewed: <date/time>
Scope: <whole plan | section | pasted plan | issue body>

## Current Required Plan Repairs

- [ ] PLA-001 - <title>
  - Lens:
  - Scope disposition:
  - Evidence:
  - Required plan repair:
  - Status: open | resolved | accepted-risk | out-of-scope | wrong
  - Resolution evidence:

## Current Observations / Out-Of-Scope Follow-Ups

<same shape, shorter>

## Current Implementation Findings

- [ ] IMP-001 - <title>
  - Lens:
  - Scope:
  - Scope disposition:
  - Plan expects:
  - Code reality:
  - Anchors:
  - Required implementation repair:
  - Status: open | resolved | accepted-risk | out-of-scope | wrong
  - Resolution anchor:

## Relevant Code Coverage Ledger

| Area | Files/symbols read | Why relevant | Reader | Status |
| --- | --- | --- | --- | --- |
| Canonical owner path |  |  |  | read/unknown |
| Caller families |  |  |  | read/unknown |
| Legacy and side-door paths |  |  |  | read/unknown |
| Adjacent same-contract paths |  |  |  | read/unknown |
| Comparable patterns |  |  |  | read/unknown |
| Contract/proof surfaces |  |  |  | read/unknown |

## Scope Provenance Anchors

- Human-authorized outcome: <plan/user anchor>
- Initial convergence closure: <plan anchor or none>
- Scope freeze: <anchor>
- Later human approvals: <anchors or none>

This section stores anchors, not a second copy of the scope contract.

## Required Lens Checklist

- [ ] Outcome North Star
- [ ] Scope provenance and minimal convergence
- [ ] Ambiguity and miscommunication
- [ ] Requirements, constraints, and simplicity
- [ ] Tiny-team maintainability
- [ ] Depth-first implementation risk
- [ ] Code-truth map
- [ ] Canonical owner and SSOT
- [ ] Existing pattern and convergence
- [ ] Caller, invariant, and state model
- [ ] Drift-proof coupling
- [ ] Elegance and code-judo
- [ ] Deletion and side-door closure
- [ ] Proof and phase exit
- [ ] Conditional lenses, if triggered

## Ambiguity And Decision Ledger

| ID | Ambiguity/constraint question | Interpretations | Impact | Required decision | Decision owner | Plan carry-through evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Pass History

### Pass <n> - <date/time>

- Mode: plan-readiness | implementation-audit
- Scope:
- Baseline reviewed:
- Test/CI context accepted, if supplied:
- Review-child accounting and context choices:
- Pre/post-dispatch repository-state check:
- Code areas read:
- Findings added:
- Findings resolved:
- Findings carried forward:
- Verdict:
- Next audit focus:
```

## Rules

- Read the latest audit log before every repeat audit.
- Keep stable finding IDs so repairs can be checked off instead of rediscovered.
- Do not erase old findings; mark them resolved, wrong, out of scope, or
  accepted-risk with evidence.
- If a repeat audit finds the same issue again, keep the original ID and add
  evidence instead of creating a duplicate.
- Check off an ambiguity or constraint decision only when a decision owner
  resolved it and the plan now carries that decision through affected sections.
- Do not mark a decision resolved because it was discussed in chat or listed in
  the audit log.
- Keep long child transcripts out of the main log. Link or summarize child
  artifacts.
- If the plan changes scope, add a pass entry explaining whether old findings
  still apply.
- Do not treat that pass entry, an audit finding, or an agent-authored plan edit
  as approval. Record the human decision anchor for post-freeze expansion.
- In `implementation-audit` mode, use `IMP-*` IDs for code review findings.
  Accept supplied test-pass status as context; do not record test execution as
  proof, ask for logs, or make the log a verification ledger.
- The audit log tracks review evidence and readiness state. It must not become
  a second implementation checklist or workflow controller.
