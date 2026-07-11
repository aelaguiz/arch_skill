---
name: arch-epic
description: "Orchestrate a goal too large for one `$arch-step` plan by decomposing it into approved ordered sub-plans, then running them through interactive handoffs, same-session `auto-plan` / `auto-implement` drivers, or explicit role-based spawned harness mode. Use when the user asks to break up and run a multi-plan epic, continue/resume an epic doc, plan every sub-plan before implementation, or automatically implement the approved epic end to end. Same-session auto commands reuse arch-step receipt gates and implement-loop; spawned harness mode uses planner, implementation worker, and critic roles. Not for a single architecture plan (`$arch-step`), one-pass mini plan (`$arch-mini-plan`), small feature (`$lilarch`), read-only status (`$arch-flow`), or foreign-repo step orchestration (`$stepwise`)."
metadata:
  short-description: "Multi-plan orchestrator wrapping arch-step with decomposition approval, progressive North-Star gates, and a per-sub-plan scope-drift critic"
---

# arch-epic

Wraps `$arch-step` to orchestrate goals too big for one canonical plan.
The skill takes a prose goal, proposes a plain-English decomposition
whose count follows proof gates rather than a preset range, gets user approval, and then drives
each sub-plan through arch-step's `new` → `auto-plan` → `implement-loop`
→ `audit-implementation` arc. After each sub-plan completes, a fresh
Claude, Codex, or Grok critic subprocess inspects the shipped work for scope
drift against the approved North Star. If the critic finds missing authorized
work, post-freeze proposed expansion, or unauthorized built scope, the skill
halts. It may resume ordinary missing work, but it never enlarges scope from
the critic. A human decides whether to approve expansion and re-freeze, or keep
the boundary and require subtraction/redesign.
Otherwise it advances to the next sub-plan.

The normal lane is interactive and re-entrant: arch-epic invokes or observes
arch-step commands in the visible session one transition at a time.

The same-session automatic commands are explicit and opt-in:
`auto-plan` is a strict sequential driver over real `$arch-step auto-plan
<SUBPLAN_DOC_PATH>` runs. It handles one approved sub-plan at a time, requires
the generated ArcStep receipt gate to report ready for that exact DOC_PATH, and
only then marks the sub-plan `planned` before moving to the next one.
`auto-implement` is a strict sequential driver over real `$arch-step
auto-implement <SUBPLAN_DOC_PATH>` runs. It handles one planned sub-plan at a
time, lets ArcStep own the full implement/prove/audit loop, runs the epic
critic only after ArcStep's implementation audit says `Verdict (code):
COMPLETE`, and marks the sub-plan `complete` only after that critic passes.

The spawned harness lane is also explicit and opt-in. After the user approves the
decomposition, arch-epic asks for a role-based execution table:
`epic_planner`, `implementation_worker`, and `critic`.
It resolves shorthand such as `opus 4.7 xhigh`, `luna high`, `terra xhigh`, or
`fugu-ultra xhigh` to runnable model ids or Codex profiles using the shared
resolver doctrine, pins the resolved
policy, then drives sub-plans depth-first with spawned child harnesses whose
hooks are disabled for subprocess isolation. Spawned workers apply arch-step
doctrine directly from disk; they do not invoke nested `auto-plan`,
`implement-loop`, or other automatic continuation commands.

Spawned planner and implementation worker sessions are resumable. If a
fresh critic finds in-scope unfinished work, arch-epic resumes the same
planner or implementation session with the critic's observation and artifact
evidence. The critic never prescribes repair steps, and ordinary repair does
not start a separate repair-worker session.

Progressive lazy planning is the default for interactive and spawned-harness
work: sub-plan N+1 is not planned until sub-plan N is complete. Same-session
`auto-plan` is the deliberate exception: it plans all approved sub-plans first,
but still plans exactly one sub-plan at a time and stops before implementation.
The user approves the decomposition up front, then approves each sub-plan's
North Star when it comes up in interactive mode. In spawned-harness mode,
spawned critics check North Star and Epic Requirement Coverage gates instead of
asking the user on every sub-plan.

Resume is the only mode — every `$arch-epic` invocation re-reads the
epic doc and sub-plan docs from disk and picks up where things left
off. "Continue my epic", "pick up where we left off", "keep going on
<project>" all work.

The skill is a thoughtful wrapper — its job is to reduce user
orchestration burden. In interactive mode, user involvement is bounded
to the goal, decomposition, per-sub-plan North Star, and material
scope-preservation decisions. In spawned-harness mode, the user approves the
decomposition and role table up front; spawned critics replace
per-sub-plan North-Star pauses unless a material ambiguity or scope
change requires the user.

## When to use

- "This is too big for one arch-step plan. Help me break it into plans
  and run them in order."
- "Orchestrate these sub-plans: X, Y, Z. Check each one before moving
  to the next."
- "Continue my epic at `docs/EPIC_<slug>_<date>.md`."
- "Keep going on the <goal> epic."
- "Pick up where we left off on <project>."
- "Automatically implement this approved epic end to end."
- "Auto-plan every sub-plan before we implement any of them."
- "Run `arch-epic auto-implement` on this approved epic."
- "Run the epic automatically and ask me which models to use for the
  planner, implementation worker, and critics."

## When not to use

- Single architecture plan, including single-plan automatic planning through
  implementation: use `$arch-step full-auto` or `$miniarch-step full-auto`.
- One-pass mini plan that hands off to implement: use `$arch-mini-plan`.
- 1–3 phase feature flow: use `$lilarch`.
- Open-ended optimization with bet-and-learn iteration: use `$goal-loop`.
- Read-only routing across arch artifacts: use `$arch-flow`.
- Stepped orchestration in a foreign repo with a per-step critic: use
  `$stepwise`.
- One-shot review of a diff, branch, or completion claim: use
  ordinary host review or `$codex-review-yolo`.
- Work that fits in a single orchestrator turn.

## Non-negotiables

Must happen every run:
- Pin `raw_goal` verbatim with `sha256` in the epic doc. Any silent
  rewrite clears the decomposition-approved flag.
- Produce a one-sentence-per-sub-plan decomposition and get user
  approval before planning any sub-plan.
- Treat the raw human goal and approved decomposition as the epic baseline.
  Decomposition approval does not authorize hidden infrastructure in later
  sub-plans. Apply `skills/_shared/scope-and-convergence.md`.
- Each sub-plan inherits its approved epic boundary, records its own initial
  minimal convergence closure during initial architecture, and freezes that
  closure before implementation. After freeze, only explicit human approval
  may add a path, obligation, sub-plan, mechanism, or proof category.
- Each sub-plan is its own full `$arch-step` canonical DOC_PATH.
  The epic doc does NOT contain plan internals (no Sections 0–10,
  no call-site audit).
- Progressive planning: in interactive and spawned-harness modes, invoke
  `$arch-step new` or planner harness work for sub-plan N+1 only after sub-plan
  N is `complete` per the epic critic. In same-session `auto-plan`, assign or
  create only the scaffold needed for the next sub-plan's canonical DOC_PATH,
  then invoke or continue the real `$arch-step auto-plan <SUBPLAN_DOC_PATH>`
  flow for that exact DOC_PATH. Creation, scaffold repair, copied sections, or
  marker-looking text are never readiness proof.
- In same-session `auto-plan`, update a sub-plan Status to `planned` only after
  `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc
  <SUBPLAN_DOC_PATH>` exits 0 for that exact DOC_PATH. If the gate is not ready,
  keep or set the sub-plan to `planning` and continue or report the exact
  `$arch-step auto-plan <SUBPLAN_DOC_PATH>` command.
- Per-sub-plan North Star approval uses `$arch-step`'s existing
  North-Star gate. `arch-epic` does not re-invent it — it just
  stops when arch-step stops. In spawned-harness mode, this gate is replaced
  by a fresh North-Star critic harness after the user-approved
  decomposition and role table are pinned. In same-session `auto-plan`, the
  approved decomposition can stand in for per-sub-plan user approval only when
  the sub-plan North Star is a direct, unambiguous expansion of the approved
  epic scope; otherwise stop and ask.
- Per-sub-plan implementation runs through
  `$arch-step implement-loop` in interactive mode and real `$arch-step
  auto-implement <SUBPLAN_DOC_PATH>` in same-session `auto-implement`.
  Same-session `auto-implement` is not complete after one invocation; it keeps
  the selected sub-plan at `implementing` and continues the ArcStep
  implement/prove/audit loop until `arch_skill:block:implementation_audit` says
  `Verdict (code): COMPLETE` or a true blocker stops progress. In
  spawned-harness mode, spawned implementation workers execute the approved
  sub-plan directly from arch-step doctrine and the sub-plan doc; the top-level
  orchestrator still does not edit target code itself.
- Epic critic runs once per sub-plan at sub-plan completion and
  returns structured JSON `EpicVerdict`. Critic is a separate
  subprocess (`claude`, `codex`, or `grok`).
- Both arch-step invocations and critic subprocesses run dangerous
  / skip-permissions / no-sandbox per repo convention.
- User supplies execution policy at invocation or at the role-table
  gate. Interactive mode needs critic runtime + model + effort.
  Spawned-harness mode needs role execution for `epic_planner`,
  `implementation_worker`, and `critic`. The skill asks once for
  missing role values. An omitted model on a Codex role defaults to
  `gpt-5.6-sol`; runtime and effort never silently default. Existing policies
  with legacy `repair_worker` values may load, but ordinary critic
  failures resume the original planner or implementation worker session.
  Same-session `auto-plan` needs no role table. Same-session
  `auto-implement` uses the same critic runtime/model/effort policy as the
  interactive completion critic.
- Resume is re-entrant: any invocation against an existing epic doc
  re-reads on-disk state and continues. No dedicated `resume`
  command.

Must never happen:
- `arch-epic` editing the target repo's code directly. Sub-plans do
  that via arch-step's implement-loop in interactive mode or spawned
  implementation workers in spawned-harness mode.
- Scope reduction. The epic scope is the epic scope. If the critic
  sees a dropped, narrowed, or silently removed requirement from the raw
  goal, approved Decomposition, North Star, Epic Requirement Coverage,
  Section 7, acceptance criteria, or verification obligations, the
  sub-plan fails. A requirement assigned to a named later sub-plan is
  preserved scope, not a failure for the current sub-plan. Agent-written
  Decision Log entries are evidence, not approval to reduce scope.
- Scope expansion by an agent, critic, review, or Decision Log. The same
  symmetry applies to additions: initial sub-plan architecture may record the
  smallest evidenced same-contract closure before freeze; any later addition
  or new sub-plan needs explicit human approval. A Decision Log entry proves a
  change was recorded, not that it was authorized.
- Auto-acting on materially-different-path detections without user approval.
  Material scope discoveries always halt. The human may approve expansion via
  `extend_current` or `new_sub_plan`, or keep the frozen boundary and require
  subtraction/redesign. No critic recommendation is self-authorizing.
- Letting critics author repair steps. Critics report verdict,
  failed checks, evidence, and scope discoveries only. The parent
  routes the result, and the resumed planner or implementation worker
  owns the reasoning for the next attempt.
- Spawning a separate repair worker for ordinary in-scope critic
  failures. Same-role resume is the default repair path; a new role
  session is only for unrecoverable session loss or explicit user
  override.
- Parallel planning or parallel implementation. Same-session `auto-plan` may
  plan every sub-plan before implementation, but it still handles one sub-plan
  at a time in decomposition order. Implementation always runs one sub-plan at
  a time and advances only after the epic critic passes.
- Marking a same-session `auto-plan` sub-plan `planned` from a consistency
  marker, plausible Section 3-7 content, prior stored status, or ArcEpic-authored
  setup. The ArcStep generated receipt gate is the proof.
- Same-session `auto-implement` starting while any non-complete sub-plan is not
  `planned`. Plan all sub-plans first with `auto-plan`.
- Marking a same-session `auto-implement` sub-plan `complete` from stored
  Status, worklog optimism, local proof, one `$arch-step auto-implement`
  invocation, or ArcStep audit alone. ArcStep audit COMPLETE must come first,
  then the epic critic must return `pass`.
- Running the epic critic while the sub-plan implementation audit is missing,
  NOT COMPLETE, reopened, or otherwise not clean. Continue or report
  `$arch-step auto-implement <SUBPLAN_DOC_PATH>` for that sub-plan instead.
- Two-second child polling. Spawned-harness mode defaults to 180-second waits
  while waiting for spawned harnesses unless the user explicitly pins a
  different cadence in the role policy.
- Calling a slow planner or worker "hung" just because it has no final
  artifact after a few minutes. Spawned children often run for 5+ minutes;
  broad `xhigh` or `max` planner/worker runs can reasonably take 20-40
  minutes. Use process state plus `events.jsonl`, `stderr.log`,
  `stream.log`, `heartbeat.json`, and `monitor.json`; treat recent
  thinking/tool/output stream activity as progress.
- Terminating a child before the long-run floors expire unless there is
  clear failure evidence. Default expectations are: poll every 180s,
  call a run `quiet` only after 900s without stream activity, and call
  it `needs_attention` only after 1800s without stream activity or after
  the pinned max runtime.
- Passing raw model shorthand to subprocesses. Resolve it first using
  shared model-resolution doctrine; preserve exact family/version or
  ask for the runnable ID.
- Heuristic keyword mapping for decomposition. Interpretation is
  prose reasoning, taught by `references/decomposition-principles.md`.
- A second "resume" command. The user types what they type; the
  skill figures it out from the epic doc + sub-plan docs.

## First move

1. Capture the user's goal verbatim. Compute `sha256`.
2. Resolve or propose the epic doc path
   (`docs/EPIC_<TITLE>_<YYYY-MM-DD>.md`).
3. Read `references/model-and-effort.md`. If the user is starting
   the interactive lane and did not name runtime + model + effort for
   the critic, ask one consolidated question. If the user explicitly
   asked for same-session `auto-plan`, defer critic choices because no critic
   runs during planning. If the user explicitly asked for same-session
   `auto-implement`, ask for missing critic choices before the first epic
   critic runs. If the user explicitly asked for role-based spawned-harness
   execution, defer execution choices to the role-table gate after
   decomposition approval.
4. Read `references/decomposition-principles.md`. Draft the
   Decomposition (one-sentence descriptions, assertion-style gates,
   dependency-then-risk ordering, and count chosen from real proof
   boundaries rather than a target range).
5. Read `skills/_shared/scope-and-convergence.md`.
6. Read `references/epic-doc-contract.md`. Write the epic doc.
7. Surface the Decomposition and ask the user to approve or adjust.

## Modes (re-entrant; one per turn)

Detail per mode lives in `references/workflow-contract.md`.

1. **`start`** — epic doc does not yet exist. Propose path, apply the Codex
   model default, ask for other critic execution values if missing, draft the
   Decomposition, and surface it for approval.
2. **`approve-decomposition`** — epic doc has
   `sub_plans_approved: false`. Apply user adjustments, flip flag,
   set `status: active`.
3. **`run`** — main orchestration pass. Routes per
   `references/arch-step-integration.md` to the next arch-step
   command for the first non-complete sub-plan or runs the critic.
4. **`resume-scope-change`** — epic is `halted` after a critic flagged a
   scope issue; a human has replied. Apply the explicit choice: approve and
   re-freeze an `extend_current`/`new_sub_plan` expansion, or keep scope and
   route subtraction/redesign. Log the human decision and resume.
5. **`summary`** — user asked a status question. Render a table of
   sub-plan statuses and the most recent log entries. No state
   changes.
6. **`auto-plan`** — same-session planning driver after decomposition
   approval. Sets up the next sub-plan DOC_PATH, drives real `$arch-step
   auto-plan <SUBPLAN_DOC_PATH>` for that exact doc, runs the ArcStep readiness
   gate, marks it `planned` only when the gate exits 0, then repeats for the
   next sub-plan in decomposition order. It stops before implementation.
7. **`auto-implement`** — same-session implementation driver. Requires every
   non-complete sub-plan to be `planned`, then runs each in order through real
   `$arch-step auto-implement <SUBPLAN_DOC_PATH>` until ArcStep audit is
   COMPLETE, runs the epic critic, and marks the sub-plan `complete` only after
   critic `pass`.
8. **`auto-run`** — explicit spawned-harness lane after decomposition
   approval. Resolve/pin the role execution table, initialize the
   auto run directory, then drive one active sub-plan depth-first
   through resumable planner and implementation worker sessions plus
   fresh critic harnesses.

## Output expectations

- Epic doc at the user-named (or proposed) path.
- Per-sub-plan canonical arch-step DOC_PATHs under
  `docs/epic/<EPIC_SLUG_WITH_DATE>/PHASE_<NN>_<SUBPLAN_SLUG>_<YYYY-MM-DD>.md`,
  owned by arch-step.
- Same-session `auto-plan` leaves non-complete sub-plans at Status `planned`
  only when their exact DOC_PATH passes the `arch-step` generated receipt gate.
- Epic critic artifacts under
  `<orchestrator repo root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/`
  including the EpicVerdict JSON, the exact invocation.sh, and the
  subprocess stream log.
- Spawned-harness automatic artifacts under
  `<orchestrator repo root>/.arch_skill/arch-epic/auto/<epic-slug>/run-<ts>/`
  including `state.json`, `execution_policy.json`, worker prompts,
  worker session IDs, latest worker-attempt pointers, critic verdicts, child `events.jsonl`,
  `stderr.log`, `stream.log`, `heartbeat.json`, `monitor.json`, and
  `report.md`.
- Orchestration Log and Decision Log append-only in the epic doc.
- Console summary with the epic doc path, the per-sub-plan status
  table, and the current active sub-plan's next action.

## Reference map

- `references/workflow-contract.md` — re-entrant modes with inputs,
  outputs, failure modes, judgment-vs-determinism split.
- `references/epic-doc-contract.md` — epic doc shape, frontmatter,
  section structure, mutation rules, validation on load.
- `references/decomposition-principles.md` — when to split a goal
  into sub-plans. Prose reasoning with worked examples; no keyword
  tables.
- `skills/_shared/depth-first-planning.md` — destination map, first
  working slice, expansion map, proof gates, and scope-cut distinction
  shared with arch-step and miniarch-step.
- `references/arch-step-integration.md` — sub-plan Status →
  arch-step command mapping. What the skill invokes vs. what the
  user or native goal-mode continuation does.
- `references/scope-change-discipline.md` — approved scope lock,
  materially-different path vs noise, and preservation-only scope
  decisions.
- `references/critic-contract.md` — EpicVerdict JSON schema and
  scope-drift / requirement-coverage checks.
- `references/critic-prompt.md` — verbatim critic prompt body with
  placeholders.
- `references/auto-harness-prompts.md` — role-specific prompt
  contracts for spawned planner, implementation, same-session
  continuation, and critic harnesses.
- `references/epic-verdict-schema.json` — JSON schema file used by
  Codex `--output-schema`, inlined into Claude `--json-schema`, and appended
  to Grok critic prompts before post-validation.
- `references/model-and-effort.md` — role-based execution policy,
  model shorthand resolution, exact-version preservation, and ask-once
  discipline.
- `references/resume-semantics.md` — how the skill re-derives state
  each turn from the epic doc + sub-plan docs.
- `references/examples.md` — worked examples: happy path,
  scope-change insertion, harmless observations ignored.

## The orchestration script

`scripts/run_arch_epic.py` is deterministic plumbing. It resolves
spawned-harness execution policy, creates run directories, spawns and
resumes workers, spawns structured critics, and writes artifacts. It
does NOT interpret decomposition, draft the epic doc, decide verdicts,
or route sub-plan states — those live in the orchestrator's prose
reasoning.

```
python3 scripts/run_arch_epic.py critic-spawn \
  --epic-doc <path> \
  --sub-plan-name "<name>" \
  --sub-plan-doc-path <path> \
  --prompt-file <path> \
  --schema-file references/epic-verdict-schema.json \
  --runtime claude|codex|grok \
  --model <model> \
  --effort <effort> \
  [--codex-profile <profile>] \
  [--orchestrator-root <dir>]
```

Spawned-harness examples:

```
python3 scripts/run_arch_epic.py resolve-execution \
  --policy-file /tmp/arch-epic-auto-policy.json

python3 scripts/run_arch_epic.py auto-init \
  --epic-doc docs/EPIC_BIG_GOAL_2026-04-26.md \
  --policy-file /tmp/arch-epic-auto-policy.json

python3 scripts/run_arch_epic.py worker-spawn \
  --run-dir .arch_skill/arch-epic/auto/big-goal/run-2026-04-26T00-00-00Z \
  --target-repo . \
  --role implementation_worker \
  --sub-plan-name "Build the core service" \
  --prompt-file /tmp/worker.prompt.md \
  --run-mode auto

python3 scripts/run_arch_epic.py worker-resume \
  --run-dir .arch_skill/arch-epic/auto/big-goal/run-2026-04-26T00-00-00Z \
  --target-repo . \
  --role implementation_worker \
  --sub-plan-name "Build the core service" \
  --prompt-file /tmp/continue.prompt.md \
  --session-id <session-id-from-session_id.txt> \
  --try-k 2 \
  --run-mode auto

python3 scripts/run_arch_epic.py child-status \
  --try-dir <printed-child-run-dir> \
  --json

python3 scripts/run_arch_epic.py child-tail \
  --try-dir <printed-child-run-dir> \
  --lines 80

python3 scripts/run_arch_epic.py child-finalize \
  --try-dir <printed-child-run-dir>
```

Foreground child runs print the session ID or verdict path after completion.
Detached child runs print the child run directory immediately; use
`child-status`, `child-tail`, and `child-finalize` to monitor and finalize
them. Writes:
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/prompt.md`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/invocation.sh`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/stdout.final.json`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/events.jsonl`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/stderr.log`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/stream.log`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/heartbeat.json`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/monitor.json`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/verdict.json`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/start_ts` / `end_ts` / `exit_code`
