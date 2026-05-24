# Output Contract

Return findings first. Keep the answer sparse enough to act on, but do not hide
coverage limits or unresolved decisions.

## Verdicts

- `ready`: The plan was audited properly, relevant code was read when needed,
  audit log is current when applicable, and no blocking findings remain.
- `not-ready`: The plan has blocking quality, architecture, code-truth,
  proof, side-door, or completion gaps.
- `blocked-on-decision`: A user or authorized decision owner must resolve
  ambiguity, constraints, compatibility, scope, or proof before the plan can be
  repaired.
- `inconclusive`: The audit could not inspect required plan or repo evidence.

## Recommended Shape

```markdown
# Plan Audit Verdict

VERDICT: ready | not-ready | blocked-on-decision | inconclusive
Confidence: high | medium | low
Scope reviewed: <plan | section | pasted plan | issue body>
Plan artifact: <path or description>
Audit log: <path or not applicable>

## Blocking Findings

1. <finding title>
   - Problem:
   - Why it matters:
   - Evidence:
     - <plan path:line, heading, or excerpt>
     - <code path:line or symbol when repo-backed>
   - Required plan repair:
   - Review lens:

## Non-Blocking Findings

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
- Do not turn the answer into workflow routing advice. The job is to improve
  the plan.
