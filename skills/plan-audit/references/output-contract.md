# Output Contract

Return findings first. Keep the answer sparse enough to act on, but do not hide
coverage limits or unresolved decisions.

## Verdicts

Plan-readiness verdicts:

- `ready`: The plan was audited properly, relevant code was read when needed,
  audit log is current when applicable, and no required repairs remain.
- `not-ready`: The plan has blocking quality, architecture, code-truth,
  proof, side-door, or completion gaps.
- `blocked-on-decision`: A user or authorized decision owner must resolve
  ambiguity, constraints, compatibility, scope, or proof before the plan can be
  repaired.
- `inconclusive`: The audit could not inspect required plan or repo evidence.

Implementation-audit code review verdicts:

- `approve`: No required code review repairs remain in the requested scope.
- `not-approved`: Required code review repairs exist in the requested scope.
- `scope-inconclusive`: The review target cannot be resolved or required code
  surfaces cannot be read.

## Recommended Shape

```markdown
# Plan Audit Verdict

VERDICT: ready | not-ready | blocked-on-decision | inconclusive
Confidence: high | medium | low
Scope reviewed: <plan | section | pasted plan | issue body>
Plan artifact: <path or description>
Audit log: <path or not applicable>

## Required Plan Repairs

1. <finding title>
   - Problem:
   - Why it matters:
   - Evidence:
     - <plan path:line, heading, or excerpt>
     - <code path:line or symbol when repo-backed>
   - Required plan repair:
   - Review lens:

## Observations / Out-Of-Scope Follow-Ups

<same shape, shorter>

## Stronger Architecture Move

<when applicable: simpler reframing, evidence, and tradeoff>

## North Star And Done-State Requirements

- North Star outcome:
- Done-state truths:
- User-facing or outcome-facing requirements:
- Code-quality requirements:
- Task-shaped requirements to rewrite:
- Outcome that remains unproven:

## Real Ambiguity And Required Decisions

- Ambiguous outcome, requirement, or constraint:
- Plausible interpretations:
- Architecture impact:
- Repo truth that resolves it:
- Decision owner:
- Required decision:
- Plan carry-through required:
- Plan carry-through evidence:

## Relevant Code Coverage

- Code areas read:
- Relevant code not yet read:
- Coverage blockers:

## Depth-First Implementation Risk

- First integrated slice:
- Highest-risk seam:
- Proof required before widening:
- Breadth-first scaffolding risks:
- Widening sequence:

## Deletion, Drift, And Side Doors

- Delete now:
- Close or migrate:
- Explicitly out of scope:
- Drift risks:
- Needs decision:

## Proof And Phase-Exit Gaps

- Integration proof needed:
- Low-value tests to avoid:
- Behavior-preservation proof:
- Phase-exit gap:

## Coverage Notes

- Lenses run:
- Lenses not run:
- Audit log updated:
- Proper-audit checklist status:
- What was not checked:

## Recommended Next Move

<one exact plan repair or decision>
```

## Rules

- Do not include placeholder sections with filler.
- Do not invent findings because the skill was invoked.
- Do not approve if a required lens could not inspect its scope.
- Do not approve if relevant code has not been read or ruled irrelevant.
- Do not approve if the audit log is missing or stale for a non-trivial
  file-backed audit.
- Do not approve if ambiguity or constraint decisions are unresolved or not
  carried through the plan.
- Do not use `optional`, `nice-to-have`, or `deferred` to soften work that
  blocks plan readiness.
- Do not use a middle approval state. If a required repair remains, the verdict
  is not approved.
- Do not turn the answer into workflow routing advice. The job is to improve
  the plan.

## Implementation-Audit Shape

Use this shape when the mode is `implementation-audit`:

```markdown
# Plan Implementation Audit Verdict

VERDICT: approve | not-approved | scope-inconclusive
Confidence: high | medium | low
Mode: implementation-audit
Scope reviewed: <full | through phase n | phase n | section>
Plan artifact: <path>
Audit log: <path or not applicable>
Baseline reviewed: <worktree | diff | commit range | branch diff | unknown>
Test/CI context: <accepted if supplied | not supplied | not reviewed by this mode>

## Required Implementation Repairs

1. <finding title>
   - Problem:
   - Why it blocks code review approval:
   - Plan expects:
   - Code reality:
   - Anchors:
     - <plan path:line or heading>
     - <code path:line or symbol>
   - Required implementation repair:
   - Review lens:

## Observations / Out-Of-Scope Follow-Ups

<same shape, shorter>

## Scope Review

- Claimed scope:
- Code reviewed:
- Code blockers:
- Test/CI assumptions accepted:
- Phase status recommendations:

## Architecture And Elegance

- Canonical owner:
- SSOT status:
- Duplicate truth or parallel paths:
- Simpler code-judo move:
- Tiny-team maintainability risk:

## Deletes, Side Doors, And Drift

- Required deletes satisfied:
- Old paths still live:
- Side doors still callable:
- Drift-prone shared dependencies:
- Docs/prompts/examples/instructions drift:

## Relevant Code Coverage

- Code areas read:
- Relevant code not yet read:
- Native subagents/lenses run:
- Coverage blockers:

## Recommended Next Move

<one exact implementation repair, plan reconciliation, or code review step>
```

Implementation-audit rules:

- Do not run unit tests, integration tests, build commands, lint commands, or
  CI.
- Do not ask for test logs or command output.
- Do not block on missing test output, screenshots, or manual validation.
- Do not investigate whether a completion claim is truthful.
- Accept supplied test-pass claims as context and keep reviewing code.
- Read changed test files only as code when relevant.
- Treat in-scope duplicate truth, side doors, stale docs/prompts, proof gaps,
  caller-contract leaks, or planned elegance gaps as required repairs, not
  observations.
