# Skill Approval Side Doors Docket - 2026-06-13

## Bottom Line

The live skills surface has three high-priority sources of the exact failure:

- `skills/exhaustive-code-review/`
- `skills/codex-review-yolo/`
- `skills/plan-audit/` in `implementation-audit` mode

All three teach some form of `approve-with-notes`: "approved, but there are
still things to care about." That is the side door. If something matters before
the next state, the answer should be `not-approved` with the exact repair.
Competing-path and side-door detection is not a special mode; it is default
review behavior.

The best common repair is:

1. Make duplicate-path, side-door, stale-truth, and competing-owner detection
   part of the default review/planning/implementation path.
2. Make decision verdicts binary:
   - `approve`
   - `not-approved`
   - `coverage-incomplete` / `scope-inconclusive` only when the review cannot
     honestly inspect the requested scope
3. Replace `non-blocking findings` with one of:
   - `observations` for true informational facts
   - `out-of-scope follow-ups` for work the user or controlling plan already
     excluded from the current decision
   - `required repairs` for anything that must be fixed before approval
4. For every `not-approved`, require the smallest exact repair target.
5. Do not add a new mode, runner, artifact family, or invocation path to handle
   duplicate-path inventory. Strengthen the normal coverage, findings, and
   verdict contracts instead.

## Scope

Reviewed live source skill packages under `skills/`, excluding generated
`build/` mirrors and vendored packages. Focus was on status contracts, verdict
contracts, review/audit output shapes, "non-blocking" language, partial-result
states, and places where agents could turn an unfinished result into a soft
approval.

Historical planning docs under `docs/` contain older examples of
`pass-with-notes`, but those are not live runtime doctrine. They are not repair
targets for this docket unless a follow-up docs cleanup wants to retire stale
examples.

## Repair Standard

Use this standard for every affected skill:

| Situation | Correct output |
| --- | --- |
| User asks "is this approved / ready / complete?" and anything required is still wrong | `not-approved` plus exact required repair |
| User asks what duplicate paths, side doors, or stale truth exist | map those surfaces in the normal review artifact; no approval language unless the user asked for approval |
| Review cannot inspect required evidence | `coverage-incomplete` or `scope-inconclusive`, not approval |
| Issue is truly outside current scope because the user or controlling artifact said so | `observation` or `out-of-scope follow-up`, not `non-blocking finding` |
| Issue is manual-only proof and code is complete | keep it out of code approval; label as manual verification pending |
| Issue is code, schema, data, migration, prompt, docs-truth, side-door, or proof that the plan required | approval must fail |

## No-New-Modes Repair Plan

The repair must not add an `inventory mode`, `side-door mode`, or any other
new lane. The user should not need to ask for a special mode to get the core
behavior. If a review, plan audit, implementation audit, or plan-backed
implementation touches a behavior owner, schema, prompt, command, generated
artifact, docs truth, test contract, install surface, or shared runtime
contract, it must look for competing ways to accomplish the same goal by
default.

The default sweep is:

1. Identify the canonical owner for the behavior or truth being reviewed.
2. Search for old paths, sibling callers, direct writers, alternate readers,
   duplicated helpers, stale docs, stale prompts, generated artifacts, examples,
   tests, command aliases, and side doors that can still express or mutate the
   same thing.
3. Classify each competing path as one of:
   - `move now`
   - `delete now`
   - `leave different`
   - `named follow-up`
   - `user decision`
4. Treat unresolved in-scope competing paths as required repairs. They are not
   notes.
5. Allow `leave different` only when the contracts are genuinely different and
   the review names the difference.
6. Allow `named follow-up` only when the controlling user request, plan, phase,
   or destination map makes the work not due yet and names the later proof gate.
   A bare "later" is not enough.
7. Prove behavior preservation when callers move, old paths delete, or a
   shared owner absorbs local logic.

For `exhaustive-code-review`, keep the existing artifact shape:

```text
target.md
coverage.md
findings.md
verdict.md
```

Do not add `inventory.md`, `recommendations.md`, or a separate invocation mode.
Instead:

- `coverage.md` must say which competing paths, side doors, stale truth
  surfaces, and adjacent same-contract surfaces were checked.
- `findings.md` must put unresolved in-scope duplicate paths under required
  repairs.
- `verdict.md` must approve only when no required repairs remain and coverage
  is honest.

If the user asks a pure "what exists?" question, the agent can answer that
question directly inside the normal coverage/findings shape and avoid approval
language in the chat summary. That is natural-language targeting, not a new
mode.

Fresh Consult is the approval model to copy: if the answer is not a clean yes,
it fails. Review skills can keep one extra state for honest coverage failure,
but they should not keep a middle approval state.

The concrete implementation order is:

1. Patch `skills/exhaustive-code-review/` first:
   - remove `approve-with-notes`
   - remove `Non-Blocking Findings` from approval decisions
   - make competing-path and side-door coverage default
   - make unresolved in-scope duplicate paths required repairs
   - keep the existing four-file artifact shape
2. Patch `skills/codex-review-yolo/`:
   - replace `approve | approve-with-notes | not-approved`
   - use `approve | not-approved | inconclusive`
   - report required repairs separately from observations
3. Patch `skills/plan-audit` implementation-audit:
   - remove the middle approval state
   - make owner path, SSOT, side doors, stale docs/prompts, proof gaps, and
     duplicate truth required repairs when they affect plan faithfulness
4. Patch `skills/agent-delegate/` and `skills/plan-implement/` closure rules:
   - `partial` or `partially complete` cannot close the parent goal
   - unresolved in-scope duplicate-path work keeps the goal open
5. Touch public docs only where the live skill behavior changed.

The skill-authoring rule for this repair is: do not solve a default behavior
failure by adding a mode. Strengthen the owning prompt contract, keep the output
surface small, and remove the alternate path.

## Docket

### D1. `exhaustive-code-review` Has A Mixed Approval Verdict

- Severity: `P0`
- Owner files:
  - `skills/exhaustive-code-review/SKILL.md`
  - `skills/exhaustive-code-review/references/output-contract.md`
- Evidence:
  - `skills/exhaustive-code-review/SKILL.md:91` lists `approve-with-notes`.
  - `skills/exhaustive-code-review/SKILL.md:93` and
    `skills/exhaustive-code-review/SKILL.md:94` split blocking and
    non-blocking findings.
  - `skills/exhaustive-code-review/references/output-contract.md:78` through
    `skills/exhaustive-code-review/references/output-contract.md:82` define
    `approve-with-notes` as a successful exhaustive review with only
    non-blocking findings.
  - `skills/exhaustive-code-review/references/output-contract.md:90` repeats
    the mixed verdict in the artifact template.
  - `skills/exhaustive-code-review/references/output-contract.md:96` through
    `skills/exhaustive-code-review/references/output-contract.md:98` preserve
    a formal "Non-Blocking Findings" section.
- Why it matters:
  - This is the exact "approved except not approved" shape. It lets a review say
    the implementation is structurally okay while still naming real work.
  - The skill is often invoked for side doors, duplicate paths, partial
    migrations, proof drift, and stale truth surfaces. Those are usually not
    harmless notes. The current output contract gives agents a sanctioned place
    to downgrade them.
  - The user may ask for inventory, but the skill always drives toward a
    verdict plus approval category.
- Most elegant repair:
  - Change verdicts to `approve`, `not-approved`, and `coverage-incomplete`.
  - Remove `approve-with-notes`.
  - Rename findings to `Required Repairs` and `Observations`.
  - Rule: any actionable changed-scope risk is a required repair. Observations
    are only facts that do not affect the requested approval decision.
  - Do not add an inventory-only mode. The default review path must already
    inventory side doors, duplicate paths, stale truth, and competing owners in
    `coverage.md`; unresolved in-scope issues belong in `findings.md` as
    required repairs.
  - Keep the "clean review is allowed" rule, but make it mean `approve` only
    when there are no required repairs and coverage is honest.

### D2. `codex-review-yolo` Copies The Same `approve-with-notes` Contract

- Severity: `P0`
- Owner files:
  - `skills/codex-review-yolo/references/verdict-contract.md`
  - `skills/codex-review-yolo/references/prompt-template.md`
  - `skills/codex-review-yolo/SKILL.md`
- Evidence:
  - `skills/codex-review-yolo/references/verdict-contract.md:8` defines
    `VERDICT: approve | approve-with-notes | not-approved`.
  - `skills/codex-review-yolo/references/verdict-contract.md:18` says
    `approve-with-notes` means good enough, but notes should be triaged.
  - `skills/codex-review-yolo/references/verdict-contract.md:21` says
    `NON-BLOCKING` observations can wait.
  - `skills/codex-review-yolo/references/verdict-contract.md:33` through
    `skills/codex-review-yolo/references/verdict-contract.md:36` tell the
    parent to lead with the verdict and summarize non-blocking notes.
- Why it matters:
  - This is a reusable second-opinion review contract. Any skill or user that
    asks Codex for a hard review inherits the soft middle state.
  - Because the child is external/fresh, the parent is likely to relay its
    verdict shape. `approve-with-notes` becomes a normalized completion state.
  - The repair target is smaller here than in `exhaustive-code-review`: the
    skill already has a footer contract, so changing the enum and field names
    fixes most of the behavior.
- Most elegant repair:
  - Replace the footer with:

    ```text
    VERDICT: approve | not-approved | inconclusive
    REQUIRED REPAIRS: <bullets or "none">
    OBSERVATIONS: <bullets or "none">
    ASSESSMENT: <one paragraph>
    ```

  - Define `approve` as "no required repairs for the requested decision."
  - Define `not-approved` as "at least one required repair, missing required
    proof, or unresolved decision affects the requested approval."
  - Define `inconclusive` as "the review could not inspect the necessary
    artifact or scope."
  - Tell the parent: if `REQUIRED REPAIRS` is non-empty, report
    `not-approved`; do not soften.
  - Keep the "Codex can be wrong" override rule, but require the parent to name
    why a claimed repair is not actually required.

### D3. `plan-audit implementation-audit` Preserves A Middle Approval State

- Severity: `P0`
- Owner files:
  - `skills/plan-audit/SKILL.md`
  - `skills/plan-audit/references/output-contract.md`
  - `skills/plan-audit/references/implementation-audit-mode.md`
  - `skills/plan-audit/references/audit-log-contract.md`
- Evidence:
  - `skills/plan-audit/SKILL.md:135` and
    `skills/plan-audit/SKILL.md:136` list `approve-with-notes` for
    implementation audits.
  - `skills/plan-audit/SKILL.md:138` and
    `skills/plan-audit/SKILL.md:139` split blocking and non-blocking findings.
  - `skills/plan-audit/references/output-contract.md:21` through
    `skills/plan-audit/references/output-contract.md:25` define
    `approve-with-notes` for code review.
  - `skills/plan-audit/references/output-contract.md:142` repeats the mixed
    verdict in the implementation-audit template.
  - `skills/plan-audit/references/output-contract.md:164` through
    `skills/plan-audit/references/output-contract.md:166` preserve a formal
    "Non-Blocking Findings" section.
  - `skills/plan-audit/references/implementation-audit-mode.md:252` through
    `skills/plan-audit/references/implementation-audit-mode.md:259` repeat the
    same verdict enum and semantics.
- Why it matters:
  - This mode reviews code against a plan for owner path, SSOT, side-door
    closure, caller fit, drift, and elegance. Those categories are exactly
    where a "note" can hide unfinished architecture work.
  - The plan-readiness side is mostly cleaner: `ready` vs `not-ready` vs
    decision/inconclusive states. The implementation-audit side regresses to a
    softer code-review pattern.
  - The audit log can carry notes forward, which is useful, but the verdict
    should not bless code while the log still contains required repairs.
- Most elegant repair:
  - Keep plan-readiness verdicts as-is.
  - Change implementation-audit verdicts to:
    - `approve`
    - `not-approved`
    - `scope-inconclusive`
  - Replace "Blocking Findings" / "Non-Blocking Findings" with:
    - `Required Implementation Repairs`
    - `Observations / Out-Of-Scope Follow-Ups`
  - Rule: anything in owner path, duplicate truth, side doors, drift, caller
    contract, changed tests-as-code, docs/prompt drift, or elegance that should
    change before the implementation can be called plan-faithful is a required
    repair.
  - Keep audit-log notes, but make them non-approval data. A note can live in
    the log without creating `approve-with-notes`.

### D4. `arch-step` And `miniarch-step` Have Good Binary Code Verdicts But Risky `non-blocking` Vocabulary

- Severity: `P1`
- Owner files:
  - `skills/arch-step/references/arch-audit-implementation.md`
  - `skills/miniarch-step/references/arch-audit-implementation.md`
  - `skills/arch-step/references/arch-implement.md`
  - `skills/miniarch-step/references/arch-implement.md`
- Evidence:
  - `skills/arch-step/references/arch-audit-implementation.md:129` through
    `skills/arch-step/references/arch-audit-implementation.md:130` say only
    missing code-verifiable evidence can make the verdict `NOT COMPLETE`.
  - `skills/arch-step/references/arch-audit-implementation.md:199` and
    `skills/arch-step/references/arch-audit-implementation.md:200` define
    `Verdict (code): <COMPLETE|NOT COMPLETE>` plus manual QA as non-blocking.
  - `skills/arch-step/references/arch-audit-implementation.md:250` through
    `skills/arch-step/references/arch-audit-implementation.md:253` give the
    strongest binary rule: code is complete only when no required code work is
    missing.
  - `skills/arch-step/references/arch-implement.md:187` through
    `skills/arch-step/references/arch-implement.md:191` allow `Deferred` and
    `Manual QA (non-blocking)` phase annotations.
  - `miniarch-step` mirrors the same contract.
- Why it matters:
  - The binary code verdict is good and should be copied elsewhere.
  - The risky part is vocabulary. Agents may over-apply "non-blocking" to
    missing assertions, migrations, docs-truth, generated artifacts, or plan
    proof that are actually code-verifiable.
  - The user complaint example mentions missing focused assertions being treated
    as a note. This contract says tests/assertions are code-verifiable evidence,
    so the skill should not let that become manual QA.
- Most elegant repair:
  - Keep `Verdict (code): COMPLETE|NOT COMPLETE`.
  - Rename `Manual QA (non-blocking)` to `Manual Verification Pending` to avoid
    making "non-blocking" the reusable phrase.
  - Add a hard line: missing tests, assertions, migrations, schema state,
    generated artifacts, docs/prompt truth, side-door closure, and preservation
    proof are never manual QA just because they are not runtime code.
  - In implement mode, replace free-form `Deferred` with `Deferred by controlling
    artifact` and require the plan/user anchor that made it deferrable.

### D5. `agent-delegate` And `plan-implement` Use Partial Progress States That Need Parent-Side Closure Rules

- Severity: `P1`
- Owner files:
  - `skills/agent-delegate/references/delegate-prompt-and-output.md`
  - `skills/plan-implement/references/output-contract.md`
- Evidence:
  - `skills/agent-delegate/references/delegate-prompt-and-output.md:101`
    defines `STATUS: done | partial | blocked | failed`.
  - `skills/agent-delegate/references/delegate-prompt-and-output.md:112`
    through `skills/agent-delegate/references/delegate-prompt-and-output.md:119`
    define `partial` as useful work landed with in-scope work remaining.
  - `skills/plan-implement/references/output-contract.md:28` defines
    `Result: complete | partially complete | blocked | stopped at boundary`.
  - `skills/plan-implement/references/output-contract.md:75` defines
    `partially complete` as useful code landed while an in-scope outcome remains
    false or unreviewed.
- Why it matters:
  - These are not approval verdicts. They are progress reports.
  - They can still become a side door if the parent agent summarizes "partial"
    as essentially done, especially after a long worker run.
- Most elegant repair:
  - Add parent-side rule: a `partial` or `partially complete` child result must
    never close the user goal.
  - Require the parent to name:
    - unresolved in-scope work
    - whether the next move is repair, continue, ask, or stop at an explicit
      boundary
    - the exact owner file, phase, or worker scope for the continuation
  - Keep the statuses; they are honest when used as progress, not approval.

### D6. `figma-best-practices` Uses `Partial` As Evidence Grading

- Severity: `P2`
- Owner files:
  - `skills/figma-best-practices/SKILL.md`
  - `skills/figma-best-practices/references/figma-audit-toolkit.md`
- Evidence:
  - `skills/figma-best-practices/SKILL.md:86` through
    `skills/figma-best-practices/SKILL.md:87` allow `Evidence only`,
    `Blocked`, or another bounded verdict when proof is unavailable.
  - `skills/figma-best-practices/SKILL.md:144` and
    `skills/figma-best-practices/SKILL.md:145` list `Pass`, `Partial`, `Fail`,
    `Evidence only`, `Blocked`, `Not inspected`, and `Out of scope`.
  - `skills/figma-best-practices/references/figma-audit-toolkit.md:79` through
    `skills/figma-best-practices/references/figma-audit-toolkit.md:90`
    define the evidence verdicts.
- Why it matters:
  - This is mostly legitimate because Figma audits often grade evidence tiers,
    not ship approval.
  - It becomes dangerous when the user asks "is this ready?" or "does this
    match source?" and the model treats `Partial` as a soft pass.
- Most elegant repair:
  - Keep `Partial` only for evidence grading.
  - Add: `Partial` is not approval and must name the missing proof or missing
    artifact work before the requested confidence can be reached.
  - For readiness questions, map `Partial` to `not-ready` unless the user asked
    only for triage.

### D7. `audit-loop`, `audit-loop-sim`, And `comment-loop` Are Mostly Safe Models

- Severity: `watch`
- Owner files:
  - `skills/audit-loop/references/review.md`
  - `skills/audit-loop/references/ledger-contract.md`
  - `skills/audit-loop-sim/references/review.md`
  - `skills/audit-loop-sim/references/ledger-contract.md`
  - `skills/comment-loop/references/review.md`
  - `skills/comment-loop/references/ledger-contract.md`
- Evidence:
  - `skills/audit-loop/references/review.md:37` through
    `skills/audit-loop/references/review.md:39` use `CONTINUE`, `CLEAN`, and
    `BLOCKED`.
  - `skills/audit-loop/references/review.md:58` through
    `skills/audit-loop/references/review.md:65` define `CLEAN` only when no
    credible unresolved audit pass remains.
  - `skills/audit-loop/references/ledger-contract.md:62` through
    `skills/audit-loop/references/ledger-contract.md:70` make the controller
    verdict exact and require a next area or stop reason.
  - `skills/comment-loop/references/review.md:35` through
    `skills/comment-loop/references/review.md:37` use the same pattern.
- Why it matters:
  - These skills already avoid the worst pattern. Work remaining maps to
    `CONTINUE`, not "clean with notes."
  - `SKIP` is still a possible side door if agents use it too casually, but the
    ledger requires a reason and consequence/proof evaluation.
- Most elegant repair:
  - No urgent verdict enum repair.
  - Copy this pattern into review skills: use `CONTINUE` for credible remaining
    work; use `CLEAN` only when no credible high-value work remains.
  - In any follow-up edit, tighten `SKIP` wording to require explicit user,
    plan, or consequence-based justification.

### D8. `fresh-consult` Is The Cleanest Approval Model

- Severity: `copy`
- Owner files:
  - `skills/fresh-consult/SKILL.md`
  - `skills/fresh-consult/references/consult-prompt-and-output.md`
- Evidence:
  - `skills/fresh-consult/references/consult-prompt-and-output.md:8` through
    `skills/fresh-consult/references/consult-prompt-and-output.md:10` define
    strict yes/no behavior.
  - `skills/fresh-consult/references/consult-prompt-and-output.md:68` defines
    `VERDICT: pass | fail`.
  - `skills/fresh-consult/references/consult-prompt-and-output.md:77` through
    `skills/fresh-consult/references/consult-prompt-and-output.md:81` say
    anything short of a clean yes fails.
  - `skills/fresh-consult/references/consult-prompt-and-output.md:87` through
    `skills/fresh-consult/references/consult-prompt-and-output.md:90` require
    low confidence to fail and require evidence read.
- Why it matters:
  - This is the right model for completion/approval checks.
  - It directly rejects pass-with-caveats behavior.
- Most elegant repair:
  - Use this semantics as the shared approval standard for
    `exhaustive-code-review`, `codex-review-yolo`, and `plan-audit
    implementation-audit`.
  - Keep one difference: review skills can use `coverage-incomplete` when the
    requested scope cannot be inspected, while consults use `fail` for low
    confidence.

### D9. `stepwise` Separates Observation From Repair Correctly

- Severity: `copy`
- Owner files:
  - `skills/stepwise/references/critic-contract.md`
- Evidence:
  - `skills/stepwise/references/critic-contract.md:3` through
    `skills/stepwise/references/critic-contract.md:10` define the critic as
    observation-only and leave diagnosis/repair to Stepwise.
  - `skills/stepwise/references/critic-contract.md:82` defines
    `pass`, `fail`, or `abstain`.
  - `skills/stepwise/references/critic-contract.md:120` through
    `skills/stepwise/references/critic-contract.md:129` define those outcomes
    without a pass-with-notes state.
  - `skills/stepwise/references/critic-contract.md:154` through
    `skills/stepwise/references/critic-contract.md:168` prevent the critic from
    prescribing repairs or softening failures.
- Why it matters:
  - It shows how to handle the user's other complaint: sometimes the user wants
    inventory or observation, not a judge inventing the workflow.
  - The critic does not approve-with-notes, and it does not author repairs. The
    owner workflow reads the observation and decides the next repair.
- Most elegant repair:
  - Copy this split into inventory-heavy review skills:
    - inventory/critic artifact reports observations
    - parent or owning workflow decides repair
    - approval verdict appears only when the user asked for approval

### D10. `skill-flow` Has The Right Observation-Verdict Guard

- Severity: `copy`
- Owner files:
  - `skills/skill-flow/references/parallel-walk-protocol.md`
- Evidence:
  - `skills/skill-flow/references/parallel-walk-protocol.md:73` through
    `skills/skill-flow/references/parallel-walk-protocol.md:77` require the
    child walker to return an honest smell that is explicitly not a verdict.
  - `skills/skill-flow/references/parallel-walk-protocol.md:141` through
    `skills/skill-flow/references/parallel-walk-protocol.md:168` define the
    audit-only/read-only contract and leave findings to the parent.
- Why it matters:
  - This is the right pattern when the user asks for a suite inventory.
  - It prevents walkers from turning inventory into approval.
- Most elegant repair:
  - Reuse this language in `exhaustive-code-review` default review behavior:
    "per-surface observations are not verdicts; parent synthesis owns findings;
    approval is only emitted when the user asked for an approval decision." Do
    not introduce a separate inventory mode.

### D11. `arch-mini-plan` And `bugs-flow` Use Non-Approval Readiness States

- Severity: `watch`
- Owner files:
  - `skills/arch-mini-plan/references/one-pass-plan.md`
  - `skills/bugs-flow/references/analyze.md`
- Evidence:
  - `skills/arch-mini-plan/references/one-pass-plan.md:38` through
    `skills/arch-mini-plan/references/one-pass-plan.md:41` end with a readiness
    handoff, not approval-with-notes.
  - `skills/bugs-flow/references/analyze.md:16` through
    `skills/bugs-flow/references/analyze.md:20` use `fix-ready`, still
    `investigating`, or `blocked`.
- Why it matters:
  - These are not current offenders.
  - They should stay framed as readiness/routing states, not "approved enough"
    states.
- Most elegant repair:
  - No urgent enum repair.
  - If touched later, add "not a completion approval" wording where useful.

## Cross-Skill Root Cause

The repeated failure comes from mixing three different jobs into one output
shape:

1. **Approval:** Can the artifact advance?
2. **Inventory:** What exists, what is duplicated, where are the side doors?
3. **Triage:** Which findings are worth fixing now?

`approve-with-notes` is what happens when those jobs are collapsed. It lets the
model preserve the social comfort of "approved" while still saying something is
wrong. Agents then optimize for a clean-sounding closeout instead of forcing the
repair.

## Global Repair Rule

Add this doctrine to the affected review skills, either directly or through a
small shared reference if the repo wants one:

```text
Approval is binary. If the user asked whether the work is approved, ready, or
complete, return approval only when there are no required repairs for the
requested scope. Any required repair makes the verdict not-approved. Do not use
"approve with notes", "pass with notes", "mostly ready", or equivalent language.

Inventory is evidence, not a mode. Every serious review should map the relevant
surfaces, owners, side doors, duplicate paths, proof gaps, observations, and
recommended repairs by default. If the user asked a pure "what exists?"
question, answer it in the normal review artifact shape and avoid approval
language instead of creating a separate invocation path.

Observations are not findings that must be fixed before approval. If a note
would lower code quality, leave a side door, weaken proof, preserve duplicate
truth, or contradict the controlling plan, it is a required repair.
```

## Recommended Repair Order

1. Patch `exhaustive-code-review` first. It is the current incident and the
   highest-leverage source for suite-wide review language.
2. Patch `codex-review-yolo` second because it exports the same verdict footer
   into external Codex reviews.
3. Patch `plan-audit implementation-audit` third because plan-backed code review
   is another high-frequency approval surface.
4. Tighten `arch-step` / `miniarch-step` vocabulary around manual verification
   so "non-blocking" cannot spread to code-verifiable gaps.
5. Add parent-side closure rules for `agent-delegate` and `plan-implement`
   partial states.
6. Optional cleanup: align README summaries after the skill contracts change.

## Suggested Acceptance Bar For The Repair Pass

- No live skill source uses `approve-with-notes` or `pass-with-notes`.
- No review skill has a `Non-Blocking Findings` section for approval decisions.
- Competing-path, side-door, and stale-truth coverage is part of the default
  review path; no new mode or artifact family is introduced for it.
- Approval decisions are binary, with `inconclusive` only for missing coverage.
- Required repairs always include the exact owner file/layer and repair target.
- `npx skills check` passes after skill package edits.
