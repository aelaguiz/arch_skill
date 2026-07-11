# ArcStep Goal Prompt Contract

Use this reference to write Markdown goal prompt files for ArcStep runs.

The prompt file should make a future goal-mode agent harder to fool. It should
tell the agent what outcome matters, which files control the details, which
ArcStep command owns the workflow, what false completion looks like, which
reviewers must sign off when they are already required, and how to stay aligned
with the plan while implementing.

## Source Truth Rule

The controlling ArcStep plan remains the source of truth. The goal prompt file
must not become a copied plan, shortened plan, alternate checklist, or private
replacement for the plan.

The goal prompt owns:

- mission
- source truth pointers
- ArcStep command to run
- false finish lines
- reviewer and auditor gates
- completion and persistence rules
- final report expectations

Linked source truth owns:

- full plan phases
- checklists and exit criteria
- command receipts
- detailed architecture
- implementation detail
- examples and fixtures
- reviewer prompt text
- long doctrine
- worklog history

Good source truth line:

```text
Use `docs/MY_PLAN.md` as controlling source truth for scope, phase obligations,
acceptance evidence, and implementation order. Do not copy it into this prompt
or create a second plan.
```

Point to that plan's Scope and Simplicity Contract and freeze anchor. Do not
copy them into the goal. All reviewer findings must be classified against that
contract before they become repair work.

Bad source truth line:

```text
Phase 1 must do A, B, C, D, E, F, and G; Phase 2 must do...
```

## Output Shape

Prefer this Markdown shape for substantial ArcStep goals:

```markdown
# Goal Prompt: [short outcome]

[One-sentence desired world state.]

Use `[DOC_PATH]` as controlling source truth for [short role labels]. Treat
[other named artifacts] as [context, worklog, reviewer evidence, or stale
history]. Do not restate those files or create a second plan.

Run `$arch-step [command] [DOC_PATH]` under the live ArcStep doctrine. If the
doc says a different ArcStep command is next, follow the doc and command
receipts rather than this prompt's guess.

False finish lines:
- [specific false completion pattern]
- [specific false completion pattern]

Alignment reminders:
- [short reminder that keeps the agent tied to source truth]
- [short reminder that makes the agent inspect deeper before closing]

Reviewer gate:
[Reviewer/auditor handling only if requested or already required.]

When the path is unclear, keep moving by rereading source truth, inspecting the
owning code or docs, forming sharper theories, and making the next direct
implementation or diagnostic move. Do not narrow the goal just because the
first pass was only name-complete, doc-complete, or status-complete.

Done means the current ArcStep frontier is satisfied, required repairs are
handled, no requested reviewer or worker is still pending, and the final report
ties exact files, commands, receipts, accepted repairs, reviewer outcomes when
present, and remaining risks back to source truth.
```

Do not force every heading when the prompt is small. The source truth,
alignment reminders, false-finish, reviewer, and done lines are the parts that
usually change behavior.

## Implementation Alignment Loop

Use this for implementation, repair, and mixed continuation goals. It is a
light reminder loop, not a harness or proof framework.

The goal prompt should teach the future agent to pause at natural transition
points and ask:

- What is the controlling source of truth right now?
- Did I reread it after the latest meaningful change?
- Am I obeying the plan's intent, or only satisfying a nearby label, status
  block, local checklist, or plausible file edit?
- Did I create a second source of truth by copying plan content into the goal,
  worklog, prompt, or status text?
- Did I implement the behavior, or only rename, wrap, comment, or document it?
- Am I rationalizing old code shape as intentional architecture instead of
  checking first principles against the plan?
- Did I stop after a convenient local fix while reachable approved work remains?
- Did I treat an agent-authored plan edit, goal edit, or reviewer finding as
  human approval for scope?
- Am I cycling through review repairs that grow implementation beyond the
  frozen contract?
- Am I building process, policy, harness, or ceremony when the next useful move
  is direct implementation, focused inspection, or a small diagnostic check?

Use only the reminders that fit the run. The prompt should make the agent go
deeper when it is drifting, not make it perform a new ritual.

## Run Types

### `auto-plan`

Use this when the desired outcome is an implementation-ready ArcStep plan.

The goal prompt should say:

- run `$arch-step auto-plan <DOC_PATH>`
- the plan doc is the planning ledger
- marker-only text is not completion
- receipts and readiness checks decide progress
- consistency or cold-read review must be treated as a gate when requested
- done does not include code implementation unless the user explicitly asked
  for a mixed run

Done means the plan is decision-complete under ArcStep doctrine, generated
receipts prove the stages ran, readiness passes for the exact `DOC_PATH`, and
any required plan reviewer agrees the plan is implementation-ready.

### `implement-loop` / `auto-implement`

Use this when the desired outcome is implemented code or docs from an approved
ArcStep plan.

The goal prompt should say:

- run `$arch-step implement-loop <DOC_PATH>` or `$arch-step auto-implement
  <DOC_PATH>`
- first require ArcStep readiness for that exact plan
- freshly reread the plan before claiming any phase or frontier is complete
- implement the approved ordered implementation frontier
- run ArcStep `audit-implementation`
- if audit or a required review rejects the result, classify the
  objection against the frozen scope contract: repair authorized work,
  subtract unauthorized work, or stop for a human scope decision
- never mark complete while reviewers, delegated workers, or required repairs
  are pending

Done means the approved frontier is implemented, ArcStep audit is clean, all
required reviewer findings are either fixed or explicitly dispositioned with
reasoning, required checks reran after repairs, and the final report ties the
work back to the controlling plan without copying it.

### `full-auto`

Use this only when the user explicitly wants ArcStep to route across planning
and implementation.

The goal prompt should say the future agent must respect ArcStep readiness
gates and must not bypass planning into implementation. It should also say that
if the canonical doc is not ready for implementation, the run stays in planning
until the real blocker or readiness gate is resolved.

## Agent and Reviewer Dispatch Briefs

Do not make a future goal-mode agent infer orchestration semantics from words
such as `fresh`, `parallel`, `fork`, or `resume`. Whenever the generated goal
actually hands work to another agent, put the dispatch decision in that
handoff paragraph. Keep it as compact prose, but make clear:

- the role's bounded job and the decision, artifact, or files it owns
- whether it runs as a same-host native child, a host-native background child,
  or an external process/session, and what benefit motivates an external lane
- whether it starts clean, receives only bounded recent chat context, or truly
  needs full parent context
- whether this is a new role, an exact-handle continuation, or a fresh
  replacement whose independence is the point
- its real isolation and capabilities, including read/write scope, workspace
  or worktree behavior, permissions, and any required browser or device access
- the topology: the parent owns fanout and integration; children do not create
  children unless the parent explicitly assigns a bounded nested scope and
  budget
- the evidence it must return so the parent can accept, repair, or reject the
  result, including file or section anchors, checks, findings, and a durable
  handle or receipt when continuation matters

Clean context is the normal choice for an independent reviewer, mapper, or
planner reading durable source truth. Use bounded context when a few recent
chat-only decisions are load-bearing, and full context only when the role
genuinely depends on the whole conversation. Context choice does not promise
filesystem or permission isolation.

For independent review or mapping, request a read-only capability when the
host exposes one, also say `do not edit or write`, and make the parent compare
current repo status or diff before accepting the return. An editful worker
needs a non-overlapping owner surface. If a reviewer sends authorized findings
back to an implementer, resume that exact implementer handle with the delta;
when the repair needs an independent signoff, create a new clean reviewer
rather than resuming the earlier critic.

Keep fanout proportional to genuinely independent work, available host slots,
collision risk, and the parent's ability to inspect every return. Generic goal
prompts should describe the transport and continuation semantics, not embed
provider CLI commands or flags. When an external provider, exact model/profile,
durable lifecycle, worktree isolation, automation surface, or receipt shape is
the useful difference, name that concrete benefit in the handoff and account
for the added process and integration cost.

Compact native-review example:

```text
Start a new clean same-host native completion reviewer over the controlling
plan, final diff, ArcStep audit block, and check receipts. Give it read-only
capability if the host exposes one and explicit no-edit/no-write guidance. It
may not create children. The parent records repo state before dispatch,
verifies it afterward, and integrates the result. Return a non-leading verdict,
evidence-anchored findings, checks performed, unresolved assumptions, and the
child handle. Authorized repairs go to the exact implementer; the next
independent signoff starts as a new clean reviewer.
```

Compact external-review example:

```text
Start a new clean external [provider/model/profile] review because [the
cross-provider, exact-model/profile, durable-session, isolation, automation,
or receipt benefit this run needs]. Give it the same bounded evidence and
read-only/no-write contract, keep integration parent-owned, and return its
verdict, anchored findings, checks, session handle, and receipt path. The goal
does not prescribe provider CLI syntax; use the owning review or delegation
skill to realize this transport.
```

These examples teach the decisions; do not force their wording or all fields
into goals that do not dispatch another agent.

## Reviewer Gates

Reviewer gates belong in the goal prompt when the user asks for a reviewer,
external auditor, strict review, fresh consult, or completion audit; when the
controlling plan already requires one; or when the goal is explicitly repairing
failed self-certification.

A good reviewer gate states:

- which reviewer or skill to use, if known
- the role's transport, starting context, continuation, capabilities,
  topology, and return evidence at the handoff point
- what evidence the reviewer receives
- that the reviewer must not be led toward the expected verdict
- what verdict is required
- that authorized rejection becomes repair input, while new scope needs a
  human decision and unauthorized built scope needs subtraction
- that completion is forbidden while the reviewer is still running

Example:

```text
Start a new clean same-host native strict reviewer as a blind completion review
of the controlling plan, final diff, ArcStep audit block, test receipts, and
this goal prompt. Use read-only capability when available, also say no edits or
writes, and keep fanout and integration with the parent. Return a verdict,
evidence-anchored findings, checks performed, unresolved assumptions, and the
child handle. Do not give the reviewer the desired verdict. Done requires
reviewer agreement that the goal is satisfied; if review rejects the result,
resume the exact implementer for repairs authorized by the frozen contract,
subtract unauthorized work, or ask the human decision owner before expansion.
Start the next independent signoff as a new clean reviewer.
```

Do not embed long reviewer prompts inside the goal file when a linked skill or
source doc owns the reviewer behavior.

## Common False Finish Lines

Use only the ones that fit the run:

- The agent read the plan once early, then implemented from memory.
- The agent copied plan content into the goal prompt and treated that copy as
  newer than the plan.
- The plan has headings or markers but missing generated ArcStep receipts.
- `auto-plan` stopped before readiness for the exact `DOC_PATH`.
- Implementation touched visible files but skipped the approved frontier.
- Names, wrappers, comments, docs, or status text changed, but the runtime owner
  path still behaves the old way.
- Existing split paths were treated as architecture before checking whether
  they are accidental history.
- A small implementation or diagnostic task grew into process, policy, or
  harness work the user did not ask for.
- A receipt or readiness label claims deeper work than actually happened.
- ArcStep audit found issues but the agent reported the findings instead of
  repairing them.
- A strict reviewer was launched but not finished.
- A reviewer rejected completion and the agent treated the rejection as a final
  report.
- An agent-authored plan revision or reviewer finding was treated as human
  scope authority.
- The goal kept repairing reviewer findings until implementation exceeded the
  frozen initial scope.
- Fixes landed after review but the relevant check did not rerun.
- The final report lists activity instead of evidence tied to source truth.

## Final Self-Check

Before shipping the prompt file, check:

- Does it name the desired world state first?
- Does it point to source truth rather than copying it?
- Does it preserve ArcStep as the workflow owner?
- Does it include only the likely alignment reminders and false finish lines?
- Does it make reviewer signoff part of done when needed?
- Does every actual agent/reviewer handoff make role, transport, starting
  context, continuation, isolation/capabilities, topology, and return evidence
  clear without provider CLI syntax?
- Does it forbid completion while required reviewers or repairs are pending?
- Could an agent honestly complete this prompt without satisfying the canonical
  plan? If yes, rewrite.
