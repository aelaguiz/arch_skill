---
name: cynical-code-review
description: "Run a prompt-only cynical code review over implemented code, a diff, branch, path set, completion claim, or optional plan-backed implementation by assuming the completion story may be misleading and hunting for code reality gaps: name-only completion, split-brain owners, side doors, partial unification, stale authority paths, stopped-short user workflows, overbuilt machinery, scope contamination, fake proof receipts, and docs/status/tests that mask broken code. Use when the user asks for a skeptical, adversarial, cynical, or implementation-integrity audit of code that may look done but be subtly wrong. Not for normal review, coverage-ledger exhaustive review, plan-readiness audit, maintainability-only thermonuclear review, implementation, repair, PR shipping, or external subprocess review."
metadata:
  short-description: "Skeptical implementation-integrity code review"
---

# Cynical Code Review

Use this skill when the user wants a skeptical implementation-integrity review
of code that may look complete while still being wrong underneath.

The job is to treat the implementation story as unproven, read current code
until the real authority paths are visible, find the places the work lied by
name, status, proof, or structure, save a findings-first review artifact, and
report the verdict plus path.

This skill does not implement, repair, commit, push, open PRs, route repair
waves, run external review subprocesses, or decide the user's broader workflow.

## Use When

- The user asks for a cynical, skeptical, adversarial, hostile, suspicious, or
  implementation-integrity code review.
- The user says a plan, phase, branch, diff, or completion claim was
  implemented but may have missed the point, stopped short, or only looked
  done.
- The user wants to find where code was implemented in name but not fact:
  duplicate truth, split-brain owners, side doors, old paths still live, partial
  unification, false simplification, or current code rationalized as design.
- The user says docs, status, tests, worklogs, labels, wrappers, or reviewer
  receipts may be lying about what the code really does.
- The user wants the audit run repeatedly after repairs to surface the next
  layer of code-reality issues.

## Do Not Use When

- The user wants a normal high-signal code review. Use the host agent's normal
  review response.
- The user wants exhaustive line-by-line, file-by-file, or coverage-ledger code
  review where coverage itself is the deliverable. Use
  `exhaustive-code-review`.
- The user wants a plan audited before work starts. Use `plan-audit`.
- The user wants code reviewed mainly against a plan artifact's architecture
  and quality bar, without investigating whether the completion story is
  truthful. Use `plan-audit implementation-audit`.
- The user wants only a harsh maintainability, spaghetti, file-size, or
  code-judo pass. Use `thermo-nuclear-code-quality-review`.
- The user wants an external Codex, Claude, Cursor, or Grok second opinion. Use
  the explicitly requested consult or delegation skill.
- The user wants fixes, implementation, PR shipping, or workflow orchestration.

## Non-Negotiables

- Review only. Do not edit reviewed files.
- Save the review artifact under
  `/tmp/cynical-code-review/<slug>-<timestamp>/` unless the user explicitly asks
  for a repo doc path.
- This is prompt-only doctrine. Do not build a rule engine, runner, controller,
  scorer, harness, script, or formal parameter interface.
- Maximize native parallel agents for broad review targets when available.
  Account for every launched lane before finalizing.
- Do not manually spawn `codex`, `claude`, `agent`, `grok`, or any other
  coding-harness executable.
- Do not invoke external agent, delegation, consult, or review skills as the
  review mechanism.
- Start from distrust: the implementation story, completion claim, names,
  wrappers, comments, status blocks, docs, tests, logs, and reviewer launches
  are claims, not proof.
- Current code behavior and structure are the authority for what exists.
  Human requests and explicit human approvals are the authority for scope.
  Plans, docs, worklogs, tests, and status surfaces help aim review; an
  agent-authored revision cannot retroactively authorize code.
- Apply `skills/_shared/scope-and-convergence.md`. For plan-, branch-,
  conductor-, PR-, or history-backed work with a recoverable baseline,
  reconstruct the initial human scope, pre-freeze convergence closure, later
  human approvals, plan/review waves, and final code. Unauthorized post-freeze
  growth or scope cycling is a `REQUIRED REPAIR` and forces `not-approved`,
  even when it works and tests pass. The normal repair target is subtraction.
- If provenance should be available but cannot be recovered, return
  `coverage-incomplete`. For a standalone code target with no plan, completion
  claim, or human-scope history, mark the provenance lane not applicable rather
  than inventing a baseline.
- Findings must be concrete current-code or requested-scope risks. Drop style
  preferences, generic maintainability advice, missing-test nits, and doc
  hygiene unless they expose a false implementation story.
- A clean review is allowed, but only after the likely ways the work could be
  lying have been checked and recorded honestly.

## First Move

1. Resolve the requested review target from natural language: current worktree,
   branch diff, commit range, explicit paths, plan scope, or completion claim.
2. Read local instructions and nearby review-relevant conventions.
3. Create the run directory under `/tmp/cynical-code-review/`.
4. Write the implementation story in plain English: what the work claims is now
   true, which source or plan says so if present, and what current code would
   have to do for that claim to be real.
5. When scope history exists, write its human baseline, initial closure and
   freeze anchor, explicit later approvals, and revision/review waves before
   accepting the latest plan as context.
6. Read `references/review-catalog.md`.
7. Read `references/output-contract.md`.
8. Read `references/agent-slices.md` before launching native parallel agents.
9. Read `references/examples.md` when the review involves completion claims,
   plan-backed implementation, unification, simplification, proof/status
   claims, or confusing peer review lanes.

## Workflow

1. Save the review target summary as `target.md`.
2. Build `suspicion-map.md`: implementation story, controlling source truth,
   proxy evidence, expected code behavior, old authority paths, duplicate truth
   risks, side doors, adjacent same-contract surfaces, user job, and likely
   scope contamination.
   For scope-backed work, start from the initial human scope, not the latest
   plan revision.
3. Map changed files, changed hunks, touched symbols, touched abstractions,
   visible behavior obligations, relevant old paths, and likely adjacent
   surfaces.
4. Use native parallel agents for independent read-only slices when the target
   is broad enough: claim mapping, old-path hunting, runtime flow tracing,
   split-brain hunting, user-job review, overbuild/scope review, and proof
   surface review.
5. Trace actual control flow, data flow, callers, readers, writers, lifecycle,
   persistence, generated artifacts, prompts, configs, and public entrypoints
   until the current authority path is visible.
6. Treat every attractive label as suspect: unified, canonical, owner, stable,
   complete, migrated, deleted, simplified, verified, ready, single source, and
   strict.
7. Review competing ways to accomplish the same goal: old APIs, sibling
   callers, direct writers, fallback readers, command aliases, duplicate
   helpers, compatibility flags, docs, examples, tests, fixtures, generated
   artifacts, prompt surfaces, and side doors.
8. Check whether the user's actual job works from the starting state that
   matters. A real surface that only supports a narrower internal job is not
   complete.
9. Check whether the implementation created machinery that hides the old
   problem: harnesses, policy layers, flag matrices, wrappers, fake
   abstractions, process receipts, or proof systems that add concepts without
   making the intended code behavior true.
10. Review proof surfaces only as code-reality claims. Changed tests, fixtures,
    docs, worklogs, examples, comments, prompts, logs, and status blocks matter
    when they prove the wrong thing, mask code gaps, keep old paths alive, or
    would mislead the next agent.
11. Run the Unauthorized Scope Ratchet Or Cycling pattern whenever scope
    provenance is recoverable. A reviewer discovery can be real and still lack
    authority; do not recommend another generalized system as the repair.
12. Use `references/review-catalog.md` to classify concrete risks. Use
    `references/examples.md` as illustrations of reasoning, not a lookup table.
13. Save `coverage.md`, `findings.md`, and `verdict.md`.
14. Return a short findings-first answer with the verdict and run directory.

## Output Expectations

The final chat reply includes:

- verdict: `approve`, `not-approved`, or `coverage-incomplete`
- required repairs, if any
- observations, if material
- run directory path
- one next action from the review, not a workflow prescription

The full saved artifact follows `references/output-contract.md`.

## Reference Map

- `references/review-catalog.md` - cynical implementation-integrity review
  patterns, what evidence to read, required-repair conditions, safe-difference
  guards, and example findings
- `references/agent-slices.md` - native parallel-agent slice guidance and
  accounting rules
- `references/output-contract.md` - required saved files, verdicts, finding
  shape, suspicion map, and final chat summary shape
- `references/examples.md` - concrete failure-pattern examples and stronger
  review moves derived from recurring agent-history failures
