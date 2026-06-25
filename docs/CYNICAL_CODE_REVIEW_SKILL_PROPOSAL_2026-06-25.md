# Cynical Code Review Skill Proposal

Date: 2026-06-25

Status: proposal document. Follow-up implementation landed as
`skills/cynical-code-review/` on 2026-06-25.

## Objective

Create a new doctrine-only review skill, proposed name:
`cynical-code-review`.

The skill's job is to audit implemented code from a hostile starting
assumption: the completion claim may be misleading, names may be lying, docs
may be laundering unfinished work, tests may prove the wrong thing, and the
code may contain subtle old paths, duplicate truths, side doors, stopped-short
behavior, or new complexity hidden under good-looking labels.

This should be a code-reality review skill. It can use plans, docs, worklogs,
completion claims, checkboxes, and test claims as evidence to aim the review,
but the approval bar is current code behavior and current code structure.

It should not become a proof harness, runner, deterministic controller,
checklist executor, screenshot ritual, test-coverage nag, or doc hygiene pass.

## Source Material Read

- `skills/exhaustive-code-review/SKILL.md`
- `skills/exhaustive-code-review/references/review-catalog.md`
- `skills/exhaustive-code-review/references/output-contract.md`
- `skills/plan-audit/SKILL.md`
- `skills/plan-audit/references/implementation-audit-mode.md`
- `vendor/cursor/plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`
- `skills/codex-review-yolo/SKILL.md`
- `docs/agent_history_failure_examples_2026-06-25/README.md`
- `docs/agent_history_failure_examples_2026-06-25/COPIED_EXAMPLES.md`
- `docs/AGENT_HISTORY_RECURRING_FAILURE_PATTERNS_2026-06-25.md`
- `$prompt-authoring` references for prompt shape, high-leverage sections, and
  anti-heuristic prompt design.
- `$skill-authoring` references for skill scope, peer boundaries, trigger
  descriptions, prompt-first packaging, and validation.

## Existing `exhaustive-code-review` Analysis

`exhaustive-code-review` is already strong at coverage accounting.

It owns:

- review-only operation
- current branch, diff, path set, plan scope, or completion claim review
- native parallel-agent acceleration
- changed files and hunks
- touched abstractions, callers, readers, writers, side doors, and owners
- tests, fixtures, docs, prompts, schemas, generated artifacts, configs, and
  other live truth surfaces when relevant
- saved review artifacts under `/tmp/exhaustive-code-review/...`
- verdicts of `approve`, `not-approved`, or `coverage-incomplete`

Its review catalog already names several patterns the new skill cares about:

- split-brain or bifurcated abstraction
- missed centralized owner
- partial migration
- name-only completion or false simplification
- wrong-layer logic
- thin or fake abstraction
- drift-prone proof
- stale truth surface
- boundary, lifecycle, and error gaps
- caller contract and invariant leaks
- agent, prompt, or skill surface regression
- security and trust boundary regression

The important gap is not that `exhaustive-code-review` lacks the right words.
The gap is posture and center of gravity.

`exhaustive-code-review` is neutral and coverage-led. It asks, "Did we cover
the requested code scope thoroughly?" It allows a clean review and treats plan
scope or completion claims as possible targets, but it does not make distrust
of the completion story the primary mission.

The user's desired review is different. It asks:

```text
Where did this implementation fool us?
Where did it look complete while the real code still missed the point?
Where did we split truth, keep an old authority path, add ceremony, or stop
short under a good name?
```

That is close to `exhaustive-code-review`, but the difference is large enough
to justify a sibling skill.

## Why This Should Be A New Skill

Do not simply turn `exhaustive-code-review` into the cynical reviewer.

Reasons:

1. `exhaustive-code-review` has a clean existing lane: exhaustive coverage is
   the deliverable.
2. The new skill has a different user-language trigger: "assume we were
   tricked," "audit the implemented plan," "find where we lied to ourselves,"
   "implemented in name not fact," "split brain," "side doors," "stopped
   short," and "this looks done but I do not trust it."
3. `plan-audit implementation-audit` already owns plan-backed code review when
   the main question is plan fit. The new skill should be plan-friendly but not
   plan-required.
4. `thermo-nuclear-code-quality-review` owns maintainability, spaghetti,
   file-size, abstraction quality, and code-judo simplification. The new skill
   should care about implementation integrity, not broad maintainability alone.
5. A separate skill lets the trigger metadata say the dangerous thing plainly:
   assume the implementation story is probably lying until current code proves
   otherwise.

The new skill can reuse mechanics from `exhaustive-code-review`, especially
artifact shape, native parallel agents, concrete findings, and no-harness
constraints. But its mission should be separate.

## Proposed Skill Name

Recommended name:

```text
cynical-code-review
```

Why:

- It matches the user's real trigger language.
- It is short, literal, and memorable.
- It is distinct from `exhaustive-code-review`.
- It communicates posture without needing a long phrase like
  `implementation-integrity-review`.

Possible subtitle in the body:

```text
Skeptical implementation integrity review.
```

Rejected alternative:

```text
implementation-integrity-review
```

That name is cleaner, but it hides the main behavior change. The whole point is
that this review should distrust attractive implementation stories.

## Proposed Trigger Description

Draft frontmatter description:

```yaml
description: "Run a prompt-only cynical code review over implemented code, a diff, branch, path set, completion claim, or optional plan-backed implementation by assuming the completion story may be misleading and hunting for code reality gaps: name-only completion, split-brain owners, side doors, partial unification, stale authority paths, stopped-short behavior, overbuilt machinery, scope contamination, and docs/status/tests that mask broken code. Use when the user asks for a skeptical, adversarial, cynical, or implementation-integrity audit of code that may look done but be subtly wrong. Not for normal code review, coverage-ledger exhaustive review, plan-readiness audit, maintainability-only thermonuclear review, implementation, repair, PR shipping, or external subprocess review."
```

This is under the usual 1024-character runtime cap.

## Canonical User Asks

The skill should trigger for asks like:

- "This plan was implemented. Audit the code and assume we missed the point."
- "Run a cynical review and find where we implemented it in name but not fact."
- "Look for all the ways this completion claim is lying: split brain, side
  doors, old paths, stopped-short behavior, duplicate truths."
- "I do not care about test/doc nits. Find the broken shit in the code we
  actually wrote."
- "Audit this implementation repeatedly until we surface the subtle code
  problems."

The skill should not trigger for:

- "Review this diff" with no request for exhaustive, cynical, plan, or
  implementation-integrity behavior. Use normal review.
- "Do an exhaustive line-by-line coverage review." Use `exhaustive-code-review`.
- "Audit this plan before implementation." Use `plan-audit plan-readiness`.
- "Review implemented code against this plan's architecture." Use
  `plan-audit implementation-audit` when the user wants formal plan-backed
  audit rather than an adversarial completion-story attack.
- "Run a thermonuclear maintainability review." Use
  `thermo-nuclear-code-quality-review`.
- "Get an external/fresh Codex opinion." Use `codex-review-yolo` or the
  explicitly requested consult/delegation skill.

## Peer Boundaries

### Versus Normal Code Review

Normal code review is findings-first and high-signal. It should catch obvious
bugs, regressions, and missing tests when they matter.

`cynical-code-review` is for distrust of the implementation story itself. It
does not ask only "what bugs are in the diff?" It asks "what did the diff make
look true without making it true?"

### Versus `exhaustive-code-review`

`exhaustive-code-review` owns coverage. It should be used when the user wants
line-by-line, file-by-file, abstraction-by-abstraction coverage and an artifact
showing what was reviewed.

`cynical-code-review` owns implementation-integrity skepticism. Coverage still
matters, but it is organized around suspicion: old authority paths, claims,
side doors, duplicate truth, scope contamination, and stopped-short behavior.

When both seem relevant:

- If the user says "exhaustive" or "coverage ledger," use
  `exhaustive-code-review`.
- If the user says "assume we are being tricked," "I do not believe this is
  done," "implemented in name not fact," "lying docs/status," or "find how this
  code missed the point," use `cynical-code-review`.

### Versus `plan-audit implementation-audit`

`plan-audit implementation-audit` owns reviewing code against a plan's
architecture and quality bar. It maintains or updates a sidecar plan audit log
when applicable. It explicitly does not investigate whether a completion claim
is truthful.

`cynical-code-review` can use a plan, but it does not require one and does not
own plan-readiness or plan-log maintenance. It treats plan text, worklogs,
checkboxes, and completion notes as claims that help aim code review. The
question is not "is the plan good?" The question is "does current code make
the claimed outcome real, or did we fool ourselves?"

### Versus `thermo-nuclear-code-quality-review`

`thermo-nuclear-code-quality-review` owns harsh maintainability review:
spaghetti growth, file size, abstraction quality, code-judo simplification,
type boundary cleanliness, and structural elegance.

`cynical-code-review` can flag overbuilt machinery or fake abstractions when
they hide an incomplete implementation, but it is not a general maintainability
rubric. Its blocker is not "this could be more elegant." Its blocker is "this
implementation story is false or incomplete in current code."

### Versus `codex-review-yolo`

`codex-review-yolo` is an external subprocess review from a fresh Codex CLI
context.

`cynical-code-review` should use native parallel agents inside the host runtime
when available. It should not manually spawn `codex`, `claude`, `agent`, or
`grok`; it should not become an external review launcher.

## Evidence Pack Lessons To Encode

The failure corpus should not be copied into the runtime skill. The runtime
skill should encode the durable review behavior.

### E01, E02: Completion Authority Drift

Lesson:

Treat "done" as unproven. A status block, local frontier, reviewer launch, or
plan note does not prove code completion.

Skill behavior:

- Start by writing the completion claim in plain English.
- Identify the code paths that would have to make the claim true.
- Treat any untriaged reviewer, old authority path, or missing code path as a
  possible false completion signal.

### E03: Docs/Status Substituted For Code

Lesson:

Docs can describe proof, but they cannot replace code behavior.

Skill behavior:

- Read docs/status/worklogs only as claims and scope guides.
- Flag docs/status only when they hide or contradict current code reality.
- Do not generate doc hygiene findings when the problem is code.

### E04: Plan Reread Not A Gate

Lesson:

For plan-backed code, memory is not enough. The controlling plan must be
reread, and each due requirement must map to current code behavior.

Skill behavior:

- If a plan is supplied, reread it before reviewing the code.
- Extract only the intent and due obligations needed to aim code review.
- Do not copy the plan into a second source of truth.

### E05: Goal Prompt As Duplicate Truth

Lesson:

Coordination artifacts become dangerous when they duplicate the source plan.

Skill behavior:

- Treat prompt/doc duplication as relevant only when it creates a code-risking
  alternate authority.
- Avoid making the review artifact a new plan or source of truth.

### E06, E09: Implemented In Name, Not Fact

Lesson:

Names, wrappers, comments, and phase labels are claims. They are not proof.

Skill behavior:

- Trace new "unified," "canonical," "stable," "owner," "single source," or
  "complete" names through actual call flow and data flow.
- Ask what old path was deleted, delegated, or made unreachable.
- Block when the new name coexists with the old behavior.

### E07: Source-Truth Cataloging

Lesson:

Repeated failures come from not cataloging authority paths and competing
patterns before judging completion.

Skill behavior:

- Build a suspicion map: intended authority, old authority, direct side doors,
  duplicate readers/writers, adjacent same-contract paths, and proof surfaces.
- Review convergence, not just changed files.

### E08: Scratch Output Instead Of Durable Docs

Lesson:

Important analysis must land where the user asked.

Skill behavior:

- Save the review artifact in a named run directory.
- If the user asks for repo docs, save there; otherwise use `/tmp` like
  `exhaustive-code-review`.

### E10, E11: Historical Splits Rationalized

Lesson:

Existing code variation is often historical drift, not architecture.

Skill behavior:

- Treat existing splits as suspects until a real product, runtime, or
  compatibility reason proves they should stay.
- Do not accept "this class is different" as evidence. Show the contract
  difference or flag the split.

### E12: Branch And Live-Process Confusion

Lesson:

Review can aim at the wrong code if checkout, branch, diff, or running source
are confused.

Skill behavior:

- Bind the review target to cwd, branch/diff/paths, and any named runtime or
  live process source when relevant.
- If those disagree, use `coverage-incomplete` rather than pretending the
  review covered reality.

### E13, E17: User Workflow Missed

Lesson:

The code can contain a real surface and still fail the user's job from the
starting state that matters.

Skill behavior:

- State the user's job in plain English.
- Check whether current code lets that job happen from the relevant starting
  state.
- Block when the implementation only supports a narrower internal job.

### E14, E15, E16: Harness Or Policy Overbuild

Lesson:

Agents turn direct fixes into frameworks, policies, and ceremony.

Skill behavior:

- Flag new code machinery that exists to make the work look rigorous but does
  not solve the root code problem.
- Prefer findings like "this new mechanism hides the old split" over generic
  "too much abstraction" commentary.
- Do not make the cynical review itself a harness.

### E18: Visible Evidence Discounted

Lesson:

External reality outranks an internally consistent explanation.

Skill behavior:

- Do not turn this into mandatory visual proof.
- Encode only the general principle: if user-facing behavior is the target,
  internal math/logs/tests cannot overrule the visible or externally observable
  failure.

### E19: Scope Contamination

Lesson:

The implementation can accidentally change adjacent behavior while solving the
named work.

Skill behavior:

- Identify adjacent same-file or same-owner surfaces that should not have
  changed.
- Flag unrelated behavior changes as required repairs when current code shows
  scope drift.

### E20, E21: Fake Process Receipts

Lesson:

Process labels and readiness receipts can be theater.

Skill behavior:

- Treat "ready," "complete," "verified," "all phases," and similar claims as
  review inputs, not truth.
- Flag only code-relevant receipt lies: where a readiness claim hides missing
  code, old live paths, duplicate truth, or stopped-short behavior.

### E22: Parallel-Agent Evidence Mishandled

Lesson:

Parallel agents only help if each evidence lane returns or is explicitly
accounted for.

Skill behavior:

- Use native parallel agents for independent read-only suspicion slices when
  available.
- Do not finalize until each lane has a result, a no-finding report, a named
  coverage gap, or a recorded failure.

### E23: Wrong Skill Or Wrong Mode

Lesson:

The agent must perform the requested audit, not talk about routing.

Skill behavior:

- If this skill loads, start the review.
- Keep peer-boundary explanation short and only when needed.

## Proposed Package Shape

Minimum package:

```text
skills/cynical-code-review/
  SKILL.md
  references/
    integrity-review-catalog.md
    agent-slices.md
    output-contract.md
```

Optional:

```text
skills/cynical-code-review/
  agents/
    openai.yaml
```

Do not add:

- `scripts/`
- runners
- controllers
- harnesses
- formal schemas
- command wrappers
- generated checklist executors
- in-skill process diaries

## Proposed `SKILL.md` Contract

The entrypoint should be lean and self-contained.

Recommended sections:

1. Frontmatter with `name`, `description`, and short metadata.
2. Title: `Cynical Code Review`.
3. Mission:
   - Review implemented code under the assumption that the completion story may
     be subtly wrong.
   - Find code-reality gaps, not pedantic process gaps.
4. Use When.
5. Do Not Use When.
6. Non-Negotiables:
   - Review only.
   - Do not edit reviewed files.
   - Save artifact under `/tmp/cynical-code-review/<slug>-<timestamp>/`
     unless the user asks for a repo doc.
   - Use native parallel agents for broad independent read-only slices when
     available.
   - Do not manually spawn external coding-harness executables.
   - Do not invoke external delegation or review skills as the mechanism.
   - Do not build a runner, harness, controller, scorer, or script.
   - Findings must be concrete current-code issues.
   - Missing tests alone are not findings.
   - Docs/status/tests matter only when they mask or contradict code reality.
7. First Move:
   - Resolve review target.
   - Write the completion claim or implementation story in plain English.
   - Identify controlling plan/source if supplied.
   - Create run directory.
   - Read references.
8. Workflow:
   - Build target summary.
   - Build suspicion map.
   - Assign native agent slices when useful.
   - Trace plan/claim to code.
   - Hunt old authority paths and side doors.
   - Check user job from starting state.
   - Check overbuild, scope contamination, and fake abstractions.
   - Review docs/tests only as code-reality claim surfaces.
   - Save artifact and return verdict.
9. Output Expectations.
10. Reference Map.

## Proposed `integrity-review-catalog.md`

This reference should adapt the existing `exhaustive-code-review` catalog, but
focus it around deception patterns rather than general review patterns.

Recommended lenses:

### Completion Story Versus Code Reality

Ask what the implementation says is done and what code would have to exist for
that to be true.

Block when the code does not make the claim true.

### Name-Only Completion

Treat new names, wrappers, comments, and status labels as claims. Trace the
runtime path.

Block when the old behavior remains live under a new name.

### Old Authority Still Live

Find old readers, writers, commands, APIs, routes, prompts, generated
artifacts, fixtures, configs, and fallback paths.

Block when old authority can still affect real behavior.

### Duplicate Truth And Split Brain

Find two live sources for the same concept, invariant, state, route, or
decision.

Block when callers can choose between them or they can drift.

### Partial Unification Or Partial Migration

Find adjacent same-contract surfaces not moved to the new model.

Block when the implementation claims convergence but only one path changed.

### Historical Split Rationalization

Treat existing divergence as suspect. Require a real product, runtime, or
compatibility reason to keep it.

Block when the review can name no real contract difference.

### Stopped-Short User Job

State the user job and starting state. Trace whether code supports it.

Block when the code implements a narrower or happier internal job.

### Overbuilt Machinery Hiding Root Problem

Look for frameworks, policies, flags, wrappers, or proof systems that create
new live concepts without making the intended code behavior real.

Block when machinery increases complexity while leaving the old gap.

### Scope Contamination

Find adjacent behavior changed as a side effect.

Block when unrelated behavior drifted in the requested implementation scope.

### Test Or Proof Receipt As Misdirection

Read changed tests as code only when relevant.

Block when tests or fixtures assert the new label, duplicate production logic,
or make impossible states look valid while code behavior remains wrong.

Do not block merely because a test is missing.

### Docs Or Status As Misdirection

Read docs/status/worklogs as claims.

Block only when they mask current code gaps, teach a live old code path, or
make the implementation appear complete when code says otherwise.

Do not emit doc hygiene findings.

### Agent/Prompt/Skill Code Surfaces

Required when changed code touches skills, agents, prompts, install behavior,
or runtime instruction surfaces.

Block when the code creates duplicate runtime truths, replaces judgment with
unjustified scaffolding, or makes the live skill surface disagree with source.

## Proposed `agent-slices.md`

The skill should use native parallel agents when broad code review can be split
into independent read-only lanes. The parent owns synthesis.

Useful slices:

- `claim_mapper`: map the user's completion story or plan intent to current
  code obligations.
- `old_path_hunter`: search for legacy authority paths, old callers, aliases,
  fallback readers/writers, commands, routes, generated artifacts, fixtures,
  and configs.
- `runtime_flow_tracer`: trace the actual changed control flow and data flow
  from entrypoint to owner.
- `split_brain_hunter`: find duplicate owners, duplicate state, duplicate
  schema, duplicate prompt doctrine, and same-contract siblings.
- `user_job_reviewer`: check whether the code supports the actual user job
  from the starting state that matters.
- `overbuild_scope_reviewer`: find new machinery, side effects, adjacent
  surface drift, fake abstractions, and unnecessary frameworks created by the
  implementation.
- `proof_surface_reviewer`: read tests/docs/status/prompts only for claims
  that mask or contradict current code behavior.

Each slice should return:

```text
result: findings | no-findings | coverage-gap | failed
files-read:
code-paths-traced:
findings:
coverage-gaps:
```

This is a prose contract, not a machine schema. The parent should not finalize
until every launched slice is accounted for.

## Proposed `output-contract.md`

Save artifacts under:

```text
/tmp/cynical-code-review/<scope-slug>-<timestamp>/
```

Required files:

```text
target.md
suspicion-map.md
coverage.md
findings.md
verdict.md
```

### `target.md`

Record:

- user's review request in their words
- resolved code target: worktree, diff, branch, commit range, path set, plan
  scope, or completion claim
- controlling plan/source truth if supplied
- local instructions read
- important exclusions or unresolved target ambiguity

### `suspicion-map.md`

Record:

- the implementation story or completion claim
- code behavior that would have to exist for it to be true
- controlling source truth, if any
- old authority paths to check
- duplicate truth risks
- side doors and adjacent same-contract surfaces
- user job and starting state
- proof surfaces that may be misleading

### `coverage.md`

Record:

- touched files and changed hunks reviewed
- relevant unchanged owners and callers reviewed
- old paths, side doors, and adjacent same-contract surfaces reviewed
- user workflow or behavior path reviewed
- docs/tests/status/prompts reviewed only where they claim code truth
- native parallel agent slices launched and final state for each
- known coverage gaps

### `findings.md`

Findings should use the same basic shape as `exhaustive-code-review`, but with
implementation-integrity wording:

```markdown
### [REQUIRED REPAIR|OBSERVATION] <short title>

- File: <repo-relative path>
- Symbol / line: <symbol or line>
- Claim being tested: <completion story, plan obligation, or implementation claim>
- Risk: <concrete code reality problem>
- Evidence: <files, flow, child report, command output, or source anchor read>
- Repair target: <what must change, without writing the patch>
- Cynical review pattern: <catalog lens>
```

Rules:

- A required repair must be a current-code problem in the requested scope.
- Missing tests alone are not findings.
- Docs/status-only issues are observations unless they hide or contradict code
  reality in a way that can mislead future implementation.
- Style, naming, and generic maintainability nits are out of scope unless they
  help preserve a false implementation story.
- Empty findings are valid, but the review must still show honest coverage.

### `verdict.md`

Use one verdict:

- `approve`: cynical review completed, suspicion lanes were covered honestly,
  and no required code repairs remain in the requested scope.
- `not-approved`: one or more required code repairs exist.
- `coverage-incomplete`: the review could not honestly inspect the code needed
  to test the implementation story.

Recommended shape:

```markdown
# Cynical Code Review Verdict

VERDICT: approve | not-approved | coverage-incomplete

## Required Repairs

<findings or "No required repairs.">

## Observations

<observations or "No observations.">

## Suspicion Summary

- Claim reviewed:
- Biggest false-completion risks checked:
- Old authority paths:
- Duplicate truth / side doors:
- User job from starting state:
- Proof/doc/status surfaces:

## Coverage Summary

- Scope reviewed:
- Native parallel agents:
- Files/hunks/abstractions covered:
- Code paths traced:
- Coverage gaps:

## Next Action

<one exact repair, rerun, or coverage action>
```

## Attitude And Tone

The skill should be blunt, skeptical, and code-grounded.

It should assume:

- the implementation may be prettier than it is true
- names may be laundering old behavior
- docs/status/tests may be proxies
- existing splits may be accidental
- "complete" probably means "the easy visible layer was done" until proven
  otherwise

It should not be performatively hostile. The value is rigorous distrust, not
insults.

Good tone:

```text
The new `UnifiedLaneStore` name does not make lane identity unified. The visible route still derives its lane key locally while prewarm reads from the old scene id path, so the same handoff still has two authorities.
```

Bad tone:

```text
This code is bad and needs more tests.
```

## What Not To Include

Do not include:

- required screenshots or visual proof loops
- mandatory test runs
- missing-test findings as the default output
- documentation hygiene findings
- broad maintainability feedback unless it exposes a false implementation story
- a persistent review database
- formal scoring
- fixed checklists that replace judgment
- a deterministic script
- a runner or controller
- a harness
- external model subprocess invocation
- patch suggestions as code blocks

## Future Implementation Plan

When implementing later:

1. Add `skills/cynical-code-review/SKILL.md` with the proposed trigger
   description and lean runtime contract.
2. Add `references/integrity-review-catalog.md` with the deception-oriented
   code review lenses.
3. Add `references/agent-slices.md` with native parallel-agent slice guidance.
4. Add `references/output-contract.md` with the saved artifact contract.
5. Add `agents/openai.yaml` only if display metadata or a default prompt
   materially improves invocation.
6. Update `README.md` and any skill inventory docs if this becomes a shipped
   skill.
7. Run `npx skills check` after adding the skill package.
8. Review the package manually against `$skill-authoring`:
   - description under cap
   - nearest-peer boundary clear
   - no scripts or harnesses
   - references are directly useful
   - examples do not become rules
9. Run at least these trigger checks by inspection:
   - "Audit this implemented plan and assume we missed the point" should select
     `cynical-code-review`.
   - "Do an exhaustive line-by-line review of this branch" should select
     `exhaustive-code-review`.
   - "Audit this plan before implementation" should select `plan-audit`.
   - "Run thermonuclear maintainability review" should select
     `thermo-nuclear-code-quality-review`.

## Recommended Decision

Implement a new prompt-only skill named `cynical-code-review`.

Do not mutate `exhaustive-code-review` into this. Keep
`exhaustive-code-review` as the coverage-led review lane and let
`cynical-code-review` own adversarial implementation-integrity review.

The evidence pack should be used as the design corpus, not as runtime baggage:
the new skill should encode the durable anti-failure posture and review lenses,
then point the agent back to current code instead of carrying transcript
history into every run.
