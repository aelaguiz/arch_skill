---
name: exhaustive-code-review
description: "Run a prompt-only exhaustive code review over a branch, diff, path set, plan scope, or completion claim by maximizing native parallel agents, reading touched files/hunks/abstractions/callers/side doors/proof/docs/generated/prompt surfaces, and saving a findings-first review artifact to disk. Use when the user asks for exhaustive, meticulous, line-by-line, file-by-file, abstraction-by-abstraction, feature-by-feature, or coverage-ledger review. Not for normal high-signal review, plan-backed `plan-audit implementation-audit`, maintainability-only thermonuclear review, implementation, repair, PR shipping, or external subprocess review."
metadata:
  short-description: "Exhaustive prompt-only code review saved to disk"
---

# Exhaustive Code Review

Use this skill when the user wants a meticulous code review where coverage is
part of the deliverable. The job is to review the requested code scope, save the
review artifact to disk, and report the verdict plus path.

This skill does not dictate the user's workflow. It does not implement, repair,
commit, push, open PRs, route repair waves, run an external review subprocess,
or decide what workflow the user should use next.

## Use When

- The user asks for exhaustive, meticulous, line-by-line, file-by-file,
  abstraction-by-abstraction, feature-by-feature, or coverage-ledger code
  review.
- The user wants a full branch, current diff, commit range, explicit path set,
  plan scope, or completion claim reviewed with every relevant touched surface
  accounted for.
- The user specifically cares about split-brain abstractions, bypassed
  centralized owners, partial migrations, side doors, drift surfaces, stale
  docs/prompts/generated artifacts, or proof that tests the wrong thing.

## Do Not Use When

- The user wants a normal high-signal general review. Use the host agent's
  normal review response.
- The user wants implemented code reviewed mainly against a plan artifact. Use
  `plan-audit implementation-audit`.
- The user wants only a harsh maintainability pass. Use
  `thermo-nuclear-code-quality-review`.
- The user wants an external Codex/Claude/Cursor second opinion. Use the
  appropriate consult or delegation skill.
- The user wants fixes, implementation, PR shipping, or workflow orchestration.

## Non-Negotiables

- Review only. Do not edit reviewed files.
- Save the review artifact under `/tmp/exhaustive-code-review/<slug>-<timestamp>/`.
- Maximize usage of native parallel agents.
- Do not manually spawn `codex`, `claude`, `agent`, or other coding-harness
  executables.
- Do not invoke external agent/delegation/review skills as the review mechanism.
- Do not build a rule engine, runner, controller, scorer, harness, or script.
- Read repo truth directly: changed files, local instructions, relevant callers,
  owners, tests, docs, schemas, generated artifacts, prompts, examples, and
  configs.
- Findings must be concrete. Drop style preferences, generic advice, and
  "maybe centralize this" comments unless they name real changed-code risk.
- Competing-path, side-door, stale-truth, and competing-owner detection is
  default review behavior, not a special mode. If a live duplicate path affects
  the requested scope, treat it as a required repair unless the review can name
  the genuinely different contract or controlling out-of-scope anchor.
- A clean review is allowed. Do not invent findings to justify the run.

## First Move

1. Resolve the requested review target from normal language: current worktree,
   branch diff, commit range, explicit paths, plan scope, or completion claim.
2. Read local instructions and nearby review-relevant conventions.
3. Create the run directory under `/tmp/exhaustive-code-review/`.
4. Read `references/review-catalog.md`.
5. Read `references/output-contract.md`.

## Workflow

1. Build the review target summary and save it as `target.md`.
2. Map the changed files, changed hunks, touched symbols, touched abstractions,
   visible features or behavior obligations, and likely adjacent surfaces.
3. Maximize usage of native parallel agents.
4. Review every touched file and changed hunk. Read surrounding code when the
   hunk depends on a function, class, module, caller, lifecycle, or contract.
5. Review touched abstractions: canonical owner, old and new paths, callers,
   readers, writers, side doors, invariants, and drift surfaces.
6. Review competing ways to accomplish the same goal: old APIs, sibling callers,
   direct writers, alternate readers, duplicate helpers, command aliases,
   generated artifacts, docs, prompts, examples, tests, and side doors. Classify
   each in-scope competing path as a required repair, observation, genuinely
   different contract, or named out-of-scope follow-up.
7. Review touched behavior: entrypoints, success paths, failure paths, state,
   persistence, user-visible or externally observable effects, and proof.
8. Review live truth surfaces: tests, fixtures, docs, examples, comments,
   schemas, generated artifacts, prompts, agent instructions, config, package
   metadata, stable IDs, telemetry names, and install commands when they
   describe or consume changed behavior.
9. Use the review catalog to identify concrete risks.
10. Save `coverage.md`, `findings.md`, and `verdict.md`.
11. Return a short findings-first answer with the verdict and run directory.

## Output Expectations

The final chat reply includes:

- verdict: `approve`, `not-approved`, or `coverage-incomplete`
- required repairs, if any
- observations, if material
- run directory path
- one next action from the review, not a workflow prescription

The full saved artifact follows `references/output-contract.md`.

## Reference Map

- `references/review-catalog.md` - concrete review patterns, evidence to read,
  required-repair conditions, safe-difference guards, and example findings
- `references/output-contract.md` - required saved files, verdicts, finding
  shape, and final chat summary shape
