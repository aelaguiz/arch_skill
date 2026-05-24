# Plan Implement Speed And Review Doctrine

Status: proposal document only. Do not treat this as implemented behavior.

Date: 2026-05-24

Working skill name: `plan-implement`

Related skills:

- `plan-audit`
- `plan-swarm`
- `agent-delegate`
- `code-review`
- `thermo-nuclear-code-quality-review`

## 0. Doctrine-Only Constraint

This proposal is for a doctrine-only, prompt-first implementation skill.

The future skill should be built as agent guidance: `SKILL.md`, reference docs,
prompt contracts, ledger rules, examples, and output expectations.

Do not turn this into:

- a deterministic harness
- a runner
- a controller
- a workflow engine
- a checklist executor
- a test scheduler
- a CI verifier
- a code-review subprocess launcher
- a scorer
- a state machine
- a script that decides whether implementation is complete

The value is judgment plus organization. The agent still reads code, chooses
the next move, writes code, verifies impact, reviews the result, and decides
what evidence is enough. The artifacts only keep that thinking from being lost
or repeated.

## 1. User Problem

Implementation from a plan often slows down for avoidable reasons:

- the agent rereads the same plan sections after every compaction
- the agent forgets which code surfaces were already inspected
- tests or checks are rerun because nobody recorded what made the prior proof
  fresh or stale
- code review happens only at the end, when findings are most expensive to
  repair
- side doors and legacy paths are rediscovered multiple times
- the plan, audit log, and actual code drift apart
- a final summary has to reconstruct the story from memory instead of reading
  durable breadcrumbs

The goal is not more ceremony. The goal is to go faster by avoiding duplicated
thinking, duplicated searches, duplicated proof, and late discovery.

## 2. North Star

Build a lightweight implementation skill that lets an agent execute an existing
plan faster and finish cleaner by keeping the plan, worklog, audit log, proof
memory, and ongoing code review aligned while it works.

The core question is:

```text
How do we implement the next plan slice with the least wasted rereading,
rerunning, and late review, while preserving the plan's architecture bar?
```

When this skill is working well:

- the agent can resume after compaction in under a minute
- the next useful implementation move is obvious
- already-read code does not need to be rediscovered unless it changed
- already-passing proof is reused unless a real invalidator exists
- plan-audit implementation findings are found while repair is still cheap
- the plan carries real decisions and completion state
- the worklog tells the implementation story without becoming a second plan
- final review is confirmation and cleanup, not the first serious audit

## 3. Mechanism Choice

This should be a skill, not only a one-shot prompt, because the behavior is
repeated and easy to lose under compaction. The skill should teach a durable
working style:

- read the plan and audit log before touching code
- keep a small worklog beside the plan
- update the plan only when source-of-truth facts change
- update the audit log when review findings open or close
- track proof freshness so tests are not rerun by habit
- use native subagents or parallel-agent features for independent read, review,
  or implementation slices when the current coding harness supports them

It should be prompt-only. A deterministic runner would make this slower and
more brittle, because the hard part is not command execution; the hard part is
choosing what matters, what changed, what proof is stale, and what review
finding actually blocks the plan.

## 4. Peer Boundary

### `plan-audit`

`plan-audit` audits a plan before work starts and reviews implemented code
against the plan after code exists. It does not implement code.

`plan-implement` would use `plan-audit` doctrine while coding. It should call
on the same concepts: North Star, done-state requirements, code truth, owner
path, SSOT, side doors, deletes, drift, caller shape, and elegance.

### `plan-swarm`

`plan-swarm` is a heavier phase orchestrator. It coordinates external worker
sessions through delegation, tracks workers, batches repair waves, and gates
phase closure through arbiter and thermonuclear review.

`plan-implement` should be lighter. It should help the current coding agent
work from a plan with less waste. It may encourage native subagents inside the
current harness, but it should not require external child CLIs, worker ledgers,
arbiter gates, or phase-swarm ceremony.

Use `plan-swarm` when the user explicitly wants a delegated parallel
implementation swarm. Use `plan-implement` when the user wants a normal
implementation loop that is faster, more resumable, and review-aware.

### `agent-delegate`

`agent-delegate` is for explicitly launching external subprocess workers.
`plan-implement` should not manually spawn `codex`, `claude`, or `agent`
executables and should not route ordinary acceleration through external
delegation. Native subagents provided by the current coding harness are
different and should be encouraged when helpful.

### `code-review` And `thermo-nuclear-code-quality-review`

These are dedicated review skills. `plan-implement` should not silently turn
every task into a formal review gate. It should do lightweight continuous
review as work lands, and then use heavier review only when the user asks,
local doctrine requires it, or the plan's risk justifies it.

## 5. Source Of Truth Model

The skill should keep three artifacts distinct.

### Plan Doc

The plan remains the source of truth for:

- North Star
- done-state requirements
- constraints and non-constraints
- scope and stop boundary
- phase order
- implementation promises
- deletes and side-door closure
- proof expectations
- decisions that changed the intended outcome
- completion status when the plan format has checkboxes or phase state

Update the plan when the truth changes. Do not hide source-of-truth decisions
in the worklog.

Good plan updates:

- mark a plan item complete with a code/proof anchor when it is truly closed
- carry an ambiguity decision through affected requirements, architecture,
  phase order, delete list, and proof strategy
- correct a stale phase boundary after the user or authorized agent resolves it
- add a required delete or side-door closure discovered from code truth
- remove a fake constraint that was making the implementation too complex

Bad plan updates:

- rewriting the plan as a running diary
- checking off tasks because files changed but the outcome is not true
- hiding unresolved ambiguity in a note
- turning the plan into a command log

### Plan Audit Log

The existing `<PLAN_STEM>_PLAN_AUDIT.md` remains the review ledger.

Use it for:

- unresolved `PLA-*` plan-readiness findings
- `IMP-*` implementation-audit findings
- ambiguity and decision carry-through
- relevant-code coverage that affects readiness or implementation approval
- code-review verdicts against the plan

Do not use it as a task board, proof ledger, or implementation diary.

### Implementation Worklog

Create or update a lightweight worklog beside the plan:

```text
<PLAN_STEM>_IMPLEMENTATION_LOG.md
```

The worklog is a resumability and speed artifact. It answers:

- what scope is active
- what is done
- what changed
- what is currently being worked
- what code was read and when it becomes stale
- what proof passed and when it becomes stale
- what review happened while implementing
- what remains blocked or unclear

It is not a second plan. It should stay short enough that a compacted agent can
read it quickly.

## 6. Worklog Contract

The worklog should be plain Markdown. No hidden state, no JSON state machine,
no generated tables unless a table is the clearest human form.

Recommended shape:

```markdown
# Plan Implementation Log

Plan: <path>
Audit log: <path or none>
Active scope: <phase | section | whole plan | user-defined stop boundary>
Last updated: <date/time>
Current checkpoint: <commit/hash/worktree/diff handle if useful>

## Resume Snapshot

- Current state:
- Next useful move:
- Do not redo unless stale:
- Known blockers:
- Native subagents used or useful next:

## Scope Ledger

| Item | Plan anchor | Status | Code anchor | Proof | Review |
| --- | --- | --- | --- | --- | --- |

## Code Read Ledger

| Area | Files/symbols read | Why relevant | Fresh until | Notes |
| --- | --- | --- | --- | --- |

## Proof Freshness Ledger

| Proof | Scope covered | Result/context | Fresh until | Rerun trigger |
| --- | --- | --- | --- | --- |

## Continuous Review Ledger

| Finding | Source | Status | Repair anchor | Notes |
| --- | --- | --- | --- | --- |

## Side Doors And Deletes

| Surface | Expected state | Current state | Status | Anchor |
| --- | --- | --- | --- | --- |

## Decision Carry-Through

| Decision | Owner | Plan carry-through | Code carry-through | Status |
| --- | --- | --- | --- | --- |

## Pass Notes

### <date/time> - <short pass title>

- Intent:
- Changed:
- Read:
- Proof:
- Review:
- Next:
```

The `Resume Snapshot` is the most important section. It should be updated at
meaningful boundaries so the next agent turn does not need to reconstruct the
world from scratch.

## 7. Update Discipline

The skill should update artifacts at boundaries, not after every micro-edit.

Update the worklog:

- before first implementation in a non-trivial plan scope
- after finishing a meaningful slice
- after discovering a side door, stale plan fact, or complexity source
- after running or accepting proof
- after native subagent review returns useful findings
- before compaction risk, long-running work, or stopping
- before claiming the scope is complete

Update the audit log:

- when a `PLA-*` finding becomes relevant during implementation
- when an `IMP-*` code-review finding is opened
- when an `IMP-*` finding is repaired
- when code truth changes a previous audit conclusion
- before final implementation-audit verdict

Update the plan:

- when a real decision is resolved and must become source truth
- when the plan's completion state changes
- when code truth proves a plan section stale
- when the smallest correct implementation requires changing the stated scope
  and the decision owner accepts that change

Do not update all three artifacts for every event. Use the owning artifact:
plan for source truth, audit log for review findings, worklog for speed and
resumability.

## 8. Progressive Implementation Order

The skill should teach this loop.

### 1. Resolve Scope

Read:

- the user request
- the plan artifact
- the active phase or stop boundary
- the existing plan audit log if present
- the implementation worklog if present
- local instructions
- current worktree status

Name the current scope in plain language. Do not silently widen.

### 2. Extract The Next Narrow Slice

Choose the smallest depth-first slice that moves the plan toward its North
Star and crosses a meaningful seam.

Prefer slices that:

- prove owner path and caller shape early
- delete or close one real side door
- make one requirement true end to end
- reduce concept count
- keep proof targeted

Avoid slices that:

- build a wide scaffold before integration
- add helpers, modes, wrappers, or config without proving the core path
- defer the risky seam until the end

### 3. Build The Local Truth Cache

Before editing, record only the useful current facts:

- relevant plan anchors
- code areas read
- legacy paths or side doors found
- comparable patterns
- proof already fresh
- proof likely needed after this slice
- review lenses likely to matter

This cache lives in the worklog so it survives compaction.

### 4. Use Native Parallelism Where It Saves Time

When the current coding harness provides native subagents or parallel-agent
features, use them for independent work that would otherwise be serial:

- mapping relevant code areas
- finding old paths and side doors
- comparing existing patterns
- reviewing already-changed code against one implementation-audit lens
- checking docs/prompts/examples drift
- inspecting changed tests as code
- implementing independent low-collision slices when the host supports safe
  native parallel editing

The parent agent still owns synthesis, source-of-truth updates, and final
claims.

Do not manually spawn separate coding-harness executables such as `codex`,
`claude`, or `agent` for ordinary acceleration. Do not invoke skills whose main
effect is to shell out to those binaries unless the user explicitly asks for
that kind of delegation.

### 5. Implement The Slice

Work like a normal senior engineer:

- read the owning code
- prefer existing patterns
- make the smallest code change that makes the plan truth real
- delete old paths instead of leaving compatibility junk when the plan calls
  for replacement
- keep callers simple
- keep invariants in code or API shape, not memory
- avoid speculative abstractions

### 6. Review While The Work Is Warm

After a meaningful slice lands, run a quick plan-backed implementation review
before widening.

Use `plan-audit` implementation-audit lenses, especially:

- plan-code fit
- requirement traceability
- canonical owner and SSOT
- existing pattern fit
- deletion and side-door closure
- drift-proof coupling
- caller invariant state
- elegance and code-judo
- tiny-team maintainability
- changed tests as code
- docs/prompts/examples drift when triggered

For broad changes, split lenses across native subagents. For small changes,
the parent can review directly.

Open real findings as `IMP-*` in the audit log when they matter beyond the
immediate fix. Repair trivial self-review issues directly and note them in the
worklog only if they affect resumability.

### 7. Verify Impact, Not Habit

Verification should follow the plan and the changed/impacted surfaces.

Run or assign checks when they buy confidence:

- the plan requires them
- the slice changed behavior that needs proof
- a caller or integration seam could break
- generated artifacts, schemas, config, prompts, or docs could drift
- prior proof is stale because touched code invalidated it
- a review finding requires proof after repair

Reuse prior proof when:

- the same behavior was already proven
- no touched file, dependency, config, generated artifact, or caller path could
  invalidate it
- the plan does not require fresh proof
- no review finding makes it suspect

Do not rerun tests just because the agent forgot what happened. Read the proof
freshness ledger first.

### 8. Close The Slice

Before moving wider:

- update the worklog resume snapshot
- mark the scope item status with code and proof anchors
- update audit findings if any opened or closed
- update the plan when source truth changed
- name what proof remains fresh and what would stale it
- name the next useful move

The slice is closed when the code state, plan state, review state, and proof
state agree.

### 9. Widen From Proven Ground

Only add the next caller, variant, mode, platform, or polish layer after the
core slice is implemented, reviewed, and sufficiently proven.

This is the implementation version of depth-first planning: add complexity only
after the previous layer is real.

### 10. Finalize The Scope

At the requested stop boundary:

- read the worklog resume snapshot
- read open audit findings
- confirm plan items in scope are either closed or explicitly not closed
- run a final lightweight implementation-audit pass over the requested scope
- update the plan, audit log, and worklog so they tell the same story
- report remaining gaps honestly

The final report should be short because the artifacts already hold the detail.

## 9. Proof Freshness Doctrine

The skill should treat proof like cached knowledge with explicit invalidators.

Every proof entry should answer:

- what was checked
- what plan obligation or impacted behavior it covers
- what result or context is being trusted
- what changes would make it stale

Examples:

```text
Proof: `uv run pytest tests/test_command_service.py`
Covered: command metadata routes through canonical service
Fresh until: command service, metadata schema, adapter registration, or caller
routes change
Rerun trigger: changes to those files, a review finding about command routing,
or a plan requirement for fresh proof
```

```text
Proof: supplied CI pass from user
Covered: broad regression context only
Fresh until: local changes after that CI pass
Rerun trigger: new commits after CI, changed shared infrastructure, or release
gate requiring current CI
```

This does not mean the agent blindly avoids testing. It means tests are run for
a reason and not rerun because memory was lost.

## 10. Continuous Review Doctrine

The implementation skill should make code review cheaper by starting it early.

Good review timing:

- after the first narrow integrated slice
- after changing a central owner
- after deleting or migrating a side door
- after touching schemas, generated artifacts, prompts, docs, examples, or
  config
- before widening to more callers
- before marking a phase or plan section done

Parallel review is especially useful when:

- one native subagent can inspect side doors while the parent continues repair
- one native subagent can compare existing patterns while another reviews
  drift-prone contracts
- one native subagent can read changed tests as code while the parent checks
  caller shape
- one native subagent can review docs/prompts/examples drift while the parent
  implements the next code repair

Review findings should be handled while the relevant files are still fresh.
That is the speed win.

## 11. Native Subagent Doctrine

The future skill should strongly encourage native subagents, not external
binary spawning.

Native subagents are useful because they share the host harness's model of the
workspace, permissions, and conversation. They can do independent reading or
review without the parent manually creating another CLI process.

Use native subagents when:

- the code map is broad
- side-door search spans many directories
- review lenses are independent
- one surface can be reviewed while another is being implemented
- changed tests, docs, prompts, config, and code can be inspected in parallel
- the task is large enough that parallel reading saves real time

Do not use native subagents when:

- the task is tiny
- scopes would overlap and cause more synthesis cost than savings
- the parent has not stated the plan scope
- the subagent would need missing context that costs more to explain than the
  work itself
- local instructions prohibit subagent use

Parent responsibilities:

- give each subagent one tight job
- tell subagents not to edit unless explicitly assigned
- require file and symbol anchors
- dedupe findings
- reject out-of-scope findings
- update the worklog and audit log
- keep final claims owned by the parent

## 12. Suggested Native Subagent Prompts

These are examples, not required forms.

### Code Map Subagent

```text
You are helping implement this plan faster by mapping one code surface.

Plan: <path>
Active scope: <phase/section>
Surface: <owner path | callers | side doors | docs/prompts | tests as code>

Read code directly. Do not edit files. Return:
- files/symbols read
- current owner path
- likely side doors or duplicate truth
- comparable patterns
- what should be reread if it changes
- blockers or surprises

Use native parallel-agent features if helpful. Do not manually spawn separate
coding-harness executables.
```

### Continuous Review Subagent

```text
You are doing one read-only plan-backed implementation review while work is in
progress.

Plan: <path>
Audit log: <path>
Implementation log: <path>
Scope: <phase/section/slice>
Lens: <plan-audit implementation-audit lens>

Read the current code directly. Do not edit files. Do not run tests. Do not ask
for logs. Return only findings for this lens:
- title
- blocking or non-blocking
- problem
- plan anchor
- code anchor
- required repair
- coverage limits

If clean for this lens, say so plainly.
```

### Proof Freshness Subagent

```text
You are checking proof freshness, not rerunning proof.

Plan: <path>
Implementation log: <path>
Changed files: <paths>
Prior proof entries: <entries>

Read code only as needed. Do not run tests. Return:
- which prior proof remains fresh
- which proof is stale and why
- smallest high-value proof to run next
- proof that would be low-value or duplicate
```

## 13. Completion Semantics

The skill should avoid fuzzy "done" claims.

A plan item can be marked complete when:

- the code state makes the required outcome true
- old paths and side doors in scope are deleted, migrated, or explicitly
  classified
- review findings for that item are resolved, rejected with rationale, or out
  of scope
- proof is run, supplied, or explicitly reused with a freshness rationale
- source-of-truth decisions are carried into the plan
- the worklog names the code/proof/review anchors

A scope can be reported complete when:

- all in-scope plan items are complete or explicitly not complete
- the audit log has no unresolved blocking `PLA-*` or `IMP-*` findings for the
  requested scope
- the proof freshness ledger does not contain stale required proof
- relevant code coverage is either read or explicitly out of scope
- the next agent can resume without rereading everything

## 14. Anti-Patterns

### Ceremony That Slows The Work

Bad: updating three ledgers after every small edit.

Better: update the owning artifact at meaningful boundaries.

### Second Plan

Bad: the worklog becomes a new task plan with requirements that conflict with
the source plan.

Better: the worklog records execution state. Plan changes go into the plan.

### Test Rerun Treadmill

Bad: rerunning the same suite after every compaction because no one remembers
whether it passed.

Better: record proof freshness and rerun only when stale or plan-required.

### Final-Big-Review-Only

Bad: implement everything, then discover at the end that the owner path,
caller shape, or deletes were wrong.

Better: review the first narrow slice, repair, then widen.

### Subagent Stampede

Bad: launching overlapping native subagents that all read the same files and
return duplicate findings.

Better: split by owner path, side doors, docs/prompts drift, changed tests as
code, or one review lens.

### External Harness Creep

Bad: the skill shells out to `codex`, `claude`, or `agent` because parallelism
sounds useful.

Better: use native subagents when available; use external delegation only when
the user explicitly asks for that mode.

### Trusting Logs Over Code

Bad: saying a plan item is done because the worklog says it is done.

Better: treat the worklog as a pointer. Read code anchors before final claims.

## 15. Proposed Skill Package Shape

If implemented, the lean package should be:

```text
skills/plan-implement/
  SKILL.md
  agents/openai.yaml
  references/
    artifact-contract.md
    progressive-implementation-loop.md
    proof-freshness.md
    continuous-review.md
    native-subagent-contract.md
    output-contract.md
    examples.md
```

No `scripts/` directory.

### `SKILL.md`

Owns:

- trigger boundary
- North Star
- source-of-truth split
- non-negotiables
- first move
- main loop
- output expectations

### `artifact-contract.md`

Defines:

- plan update rules
- audit log update rules
- implementation worklog shape
- what each artifact must never become

### `progressive-implementation-loop.md`

Defines:

- resolve scope
- choose next narrow slice
- implement
- review while warm
- verify impact
- update artifacts
- widen from proven ground

### `proof-freshness.md`

Defines:

- how to record proof
- how to decide freshness
- rerun triggers
- examples of proof reuse
- avoidance of duplicate test effort

### `continuous-review.md`

Defines:

- when to run plan-backed review during implementation
- how to open and close `IMP-*` findings
- how to use `plan-audit` implementation lenses without becoming a formal
  code-review runner

### `native-subagent-contract.md`

Defines:

- when native subagents save time
- read-only review prompt examples
- safe implementation parallelism guidance
- parent synthesis rules
- ban on manually spawning external coding harness binaries

### `output-contract.md`

Defines:

- status update shape
- final implementation summary
- explicit open gaps
- artifacts updated
- proof reused or run
- review findings opened or closed

### `examples.md`

Shows:

- clean worklog update
- proof freshness entry
- continuous review finding
- plan decision carry-through
- anti-examples for ceremony, duplicate proof, and second-plan drift

## 16. Proposed Trigger Description

Draft frontmatter description:

```yaml
description: "Implement an existing plan or plan phase faster by keeping the plan, audit log, implementation worklog, proof freshness, and ongoing plan-backed code review aligned while coding. Use when the user wants to execute a plan with less duplicate rereading, fewer repeated tests, compaction-safe progress, native subagent acceleration when available, and continuous review against plan-audit quality doctrine. Not for creating plans, generic code review, external worker swarms, deterministic runners, CI verification, or manually spawning coding-harness executables."
```

This keeps the trigger centered on implementation speed and completeness, not
workflow delegation.

## 17. First Runtime Draft

The future `SKILL.md` should start close to this:

```markdown
# Plan Implement

Use this skill when the user wants code implemented from an existing plan,
phase, section, or checklist while preserving plan truth, review state, proof
freshness, and resumability.

The job is to go faster by wasting less motion: fewer repeated code reads,
fewer duplicate tests, fewer late review surprises, and less context loss after
compaction.

This is doctrine-only and prompt-first. Do not create scripts, runners,
controllers, deterministic state machines, or external coding-harness
subprocesses. Use native subagents or parallel-agent features provided by the
current coding harness when they help with independent read, review, or safe
implementation slices.
```

## 18. Definition Of Done For Building The Skill

The skill is ready to ship when:

- it is clearly lighter than `plan-swarm`
- it clearly uses `plan-audit` doctrine instead of duplicating it
- it has no scripts or deterministic harnesses
- it does not prescribe the user's workflow beyond implementation hygiene
- it explains the plan/audit/worklog split without ambiguity
- it teaches proof freshness so checks are not rerun by memory failure
- it encourages native subagents for acceleration without external CLI spawning
- it explains continuous review during implementation
- it makes compaction recovery a first-class outcome
- it keeps final output short because artifacts carry the detailed story
- it passes `npx skills check` if that check is available in the repo
- docs/routing are updated only if the skill is actually added

## 19. ELI10 Summary

This skill would be the "work from the plan without losing your place" skill.

It should make the agent do three simple things:

1. Keep a tiny map of what it already read, changed, tested, and reviewed.
2. Review each useful chunk while it is still easy to fix.
3. Only redo work when something actually changed enough to make the old work
   stale.

That is how it goes faster. Not by adding bureaucracy, and not by launching a
giant external swarm by default. It goes faster because the agent stops paying
the same thinking cost over and over.
