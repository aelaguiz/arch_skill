# Examples And Anti-Examples

Use these to teach judgment, not to create lookup rules.

## Blocking: Ambiguous Replacement

Finding: `replace the old path` is outcome-changing ambiguity.

Why it matters: it could mean delete the old path, hide it behind a temporary
bridge, or keep it for one legacy entrypoint. Those choices change the delete
list, caller API, tests, docs, and side-door risk.

Required repair: name the intended compatibility posture and carry it through
requirements, target architecture, phase order, delete list, and proof.

## Blocking: Breadth-First Risk

Finding: the plan builds data model, service layer, UI shell, config, fixtures,
and tests in parallel, then integrates in the last phase.

Why it matters: the core architecture can be wrong from the start and only fail
after most work is spent.

Required repair: make the first phase prove one narrow real path through the
highest-risk seam, then widen from that proven base.

## Blocking: Parallel Owner Path

Finding: the plan adds a new writer beside an existing extendable owner.

Why it matters: future callers can choose between old and new writes, contracts
can drift, and bug fixes need to land twice.

Required repair: route writes through the canonical owner, migrate same-family
callers that must converge now, and delete or close the old write path.

## Blocking: Missing Audit Log Carry-Forward

Finding: the repeat audit claims the plan is clean, but the prior audit log has
an unresolved ambiguity with no decision owner or plan carry-through evidence.

Why it matters: the plan can be implemented from stale ambiguity even though
the audit loop already found it.

Required repair: carry the finding forward, resolve it through the decision
owner, update the plan, and only then mark it resolved.

## Clean Plan Pattern

A clean audit can return `ready` when:

- the North Star and done-state requirements are explicit
- constraints and non-constraints are named
- no real ambiguity remains
- all relevant code was read or ruled irrelevant
- existing patterns and owner paths are accounted for
- phase order is depth-first
- deletes and side-door closure are explicit
- proof targets the highest-risk seam
- the audit log is current when applicable
- every durable obligation traces to human scope or the pre-freeze minimal
  convergence closure

## Blocking: Audit-Created Scope

Finding: a plan-readiness auditor discovers a similar neighboring subsystem and
adds its cleanup to the plan because convergence would be cleaner.

Why it matters: audit is not scope authority. Similarity is weaker than a
directly competing same-contract path, and even a real adjacent path discovered
after freeze needs a human decision.

Required repair: remove the audit-created obligation. Before freeze, ask the
initial planning owner to inspect whether it belongs in the minimal closure.
After freeze, request explicit human approval.

## Blocking Implementation: Retroactive Plan Ratification

Finding: review wave three adds a database owner, the worker builds it, and a
later agent edits the plan to include it without human approval.

Why it matters: the code and plan are scope-cycling. A later plan edit cannot
ratify unauthorized built scope.

Required repair: record `unauthorized-built-scope`, return `not-approved`, and
subtract the database machinery unless a human decision owner explicitly
approves and re-freezes the expanded contract.

## Blocking Implementation-Audit Pattern

Finding: Phase 2 claims the old direct writer is replaced, but the old command
still calls it directly.

Why it matters: future callers can bypass the canonical owner, so the codebase
still has two live write paths and fixes can drift.

Required repair: route the old command through the canonical owner or delete
the command if the plan made it obsolete.

## Clean Implementation-Audit Pattern

A clean implementation-audit can return `approve` when:

- the requested scope is clear
- relevant changed and unchanged code was read
- old side doors in scope were searched
- planned deletes and caller migrations are reflected in code
- the canonical owner and SSOT are real in code
- changed tests, if relevant, were reviewed only as code
- no tests, builds, lint commands, or CI were run by the audit

## Anti-Example: Test Execution Policing

Bad finding: "CI logs were not attached, so the implementation is blocked."

Why it is bad: `implementation-audit` is plan-backed code review. It accepts
test-pass context when supplied, does not ask for logs, and does not make
missing test output a blocker.

## Anti-Example: Fake Ambiguity

Bad finding: "Should the code be maintainable?"

Why it is bad: the answer is obvious and does not change architecture. The
reviewer should instead name the actual maintainability risk, such as a custom
framework or caller-facing mode flag.

## Anti-Example: Workflow Policing

Bad finding: "This should have been an arch-step plan."

Why it is bad: `plan-audit` audits the plan format the user has. It can say the
plan lacks requirements, code truth, phase exits, or proof. It should not
dictate the user's workflow.

## Anti-Example: Deterministic Harness

Bad implementation idea: add a script that scores a plan as elegant or ready.

Why it is bad: the skill's job depends on judgment, repo reading, ambiguity
resolution, and architectural taste. Scripts may not own the verdict.
