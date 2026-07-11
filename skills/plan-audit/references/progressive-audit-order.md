# Progressive Audit Order

Use this as the main execution path. It works for any planning document format:
formal docs, PRDs, issue bodies, migration plans, checklists, pasted plans, and
repo-specific plan shapes.

The order matters. Do not jump to style comments, workflow routing, or local
code smells before proving the plan's target and repo truth.

## Mode Gate

If the user asks to review code already written for a plan, use
`implementation-audit` mode and follow
`references/implementation-audit-mode.md` instead of this plan-readiness order.

Implementation-audit is code review against a plan. It does not run unit
tests, integration tests, build commands, lint commands, or CI; it does not ask
for test logs; and it does not investigate whether a completion claim is
truthful.

## 1. Resolve The Plan Artifact

- Resolve the plan source: file path, pasted plan, issue body, doc section,
  PRD, checklist, or named planning artifact.
- For file-backed non-trivial audits, resolve `AUDIT_LOG_PATH` as
  `<PLAN_STEM>_PLAN_AUDIT.md` beside the plan.
- Read local instructions and repo verification rules when repo-backed.
- If the audit log exists, read it before starting.

## 2. Read The Plan As Written

- Identify scope, requested behavior, stop boundary, phase boundaries, claimed
  verification, and current unresolved notes.
- Audit the artifact on disk or in the prompt. Do not silently repair it in
  your head.

## 3. Extract The Outcome Contract

- Find the North Star.
- Find explicit done-state requirements.
- Find requirements, non-requirements, constraints, non-constraints,
  assumptions, and complexity sources.
- Mark missing outcome-contract pieces before judging detailed architecture.
- Recover the original human-authorized outcome and explicit later human
  approvals. Identify the initial minimal convergence closure and the point at
  which implementation scope froze. Reject the latest plan text as circular
  authority when it cannot trace an obligation to one of those anchors.

## 4. Identify Real Ambiguity

- Name wording that can produce different outcomes.
- Check whether repo truth resolves it.
- Keep only ambiguity that changes requirements, constraints, compatibility,
  deletion, proof, phase order, or user-facing outcome.
- Assign a decision owner when a real ambiguity or constraint question remains.

## 5. Build The Relevant-Code Map

For repo-backed plans, list the code and contract surfaces the plan depends on:

- named files, symbols, modules, commands, routes, prompts, generated
  artifacts, fixtures, schemas, config, tests, docs, and instructions
- old and new concepts
- comparable existing patterns
- adjacent same-contract or same-behavior surfaces that may need to converge
- side doors and alternate entrypoints

Split broad read-only code mapping across native subagents or parallel-agent
features provided by the current coding harness whenever available. Record the
reason if native subagents are unavailable, prohibited by local instructions, or
unnecessary because the audit is too small to split.

## 6. Read All Relevant Code

Read the surfaces needed to validate the plan:

- canonical owner path
- proposed target owner path
- public and representative internal callers
- legacy paths that should delete or converge
- adjacent live paths that expose the same contract or behavior
- comparable pattern families
- contract surfaces that can drift
- tests and proof surfaces
- docs, prompts, examples, and instructions that can route humans or agents
  toward old behavior

Record areas read and unknowns in the audit log for file-backed audits. Do not
approve while relevant-code coverage is unknown.

## 7. Synthesize Code Truth

- Write down current architecture anchors.
- Write down target architecture claims.
- Identify where the plan matches code, where it is stale, and where it is
  guessing.
- Identify whether the plan can complete while adjacent live surfaces remain
  split between old and new behavior.
- Separate repo facts from reviewer inference.

## 8. Run Required Lenses

Run the lenses from `review-lenses.md`:

- outcome North Star
- ambiguity and miscommunication
- requirements, constraints, and simplicity pressure
- tiny-team maintainability
- depth-first implementation risk
- code-truth map
- canonical owner and SSOT
- existing pattern and convergence
- caller, invariant, and state model
- drift-proof coupling
- elegance and code-judo
- deletion and side-door closure
- proof and phase exit
- scope provenance and minimal convergence
- conditional lenses when triggered

## 9. Challenge The Architecture

Ask:

- Can this be simpler without breaking stated requirements?
- Can the same outcome be achieved with fewer live concepts?
- Should an existing pattern be extended or made canonical?
- What can be deleted, privatized, merged, or made unreachable?
- Which adjacent same-contract surfaces were already included by initial
  architecture before freeze? Do not answer this question by expanding the
  plan from the audit.
- What complexity exists only because the plan assumes a false constraint?

## 10. Check Implementation Risk

- Confirm the plan is depth-first or has a real reason it cannot be.
- Confirm the first implementation slice proves a narrow integrated path.
- Confirm the highest-risk seam is crossed early.
- Confirm each later phase widens from a proven base.
- Confirm proof gates are integration-level where integration is the risk.

## 11. Classify Findings

- Blocking: unsafe, ambiguous, under-read, overbuilt, not convergent, not
  provable, or not ready.
- Non-blocking: useful improvement that does not affect implementation safety,
  architecture, proof, drift, or completion.
- Wrong or out of scope: reject with a short reason in the audit log when
  applicable.
- Give every material finding a scope disposition from the shared doctrine.
  A pre-freeze planning gap routes back to the planning owner for architecture
  inspection. A post-freeze gap routes to a human decision. Neither route lets
  the auditor write the expansion into required scope.

## 12. Update The Audit Log

For non-trivial file-backed audits:

- add a new pass entry
- update current verdict
- add new findings with stable IDs
- update relevant-code coverage
- carry unresolved findings forward
- check off resolved findings only with evidence
- check off ambiguity or constraint decisions only when the decision owner has
  resolved them and the plan carries the decision through

## 13. Return The Verdict

- Lead with blocking findings.
- Report the audit log path when applicable.
- Name the smallest next plan repair.
- Do not call the plan ready until the proper-audit checklist is complete and
  all blocking findings are resolved.

The skill improves plans. It does not choose the user's planning workflow.
