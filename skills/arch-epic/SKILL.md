---
name: arch-epic
description: "Orchestrate a goal too large for one `$arch-step` plan by decomposing it into approved ordered sub-plans, then running them depth-first through interactive arch-step handoffs or an explicit automatic harness mode. Use when the user asks to break up and run a multi-plan epic, continue an existing epic, resume from an epic doc, or automatically implement the approved epic end to end. Automatic mode asks for role-based agent/model choices for planner, implementation worker, repair worker, and critics, then uses fresh Claude/Codex harnesses with streamed progress, detached long-run monitoring, and a few-minute child-wait cadence. Not for a single architecture plan (`$arch-step`), one-pass mini plan (`$arch-mini-plan`), small feature (`$lilarch`), generic completion loops (`$arch-loop`), read-only status (`$arch-flow`), or foreign-repo step orchestration (`$stepwise`)."
metadata:
  short-description: "Multi-plan orchestrator wrapping arch-step with decomposition approval, progressive North-Star gates, and a per-sub-plan scope-drift critic"
---

# arch-epic

Wraps `$arch-step` to orchestrate goals too big for one canonical plan.
The skill takes a prose goal, proposes a plain-English decomposition
(3–7 sub-plans, one sentence each), gets user approval, and then drives
each sub-plan through arch-step's `new` → `auto-plan` → `implement-loop`
→ `audit-implementation` arc. After each sub-plan completes, a fresh
Claude or Codex critic subprocess inspects the shipped work for scope
drift against the approved North Star. If the critic finds a requirement
needed to preserve approved scope or a non-trivial scope change, the skill
halts and asks the user how to preserve the scope by extending the current
sub-plan or inserting a new sub-plan.
Otherwise it advances to the next sub-plan.

The normal lane is interactive and re-entrant: arch-epic invokes or observes
arch-step commands in the visible session one transition at a time.

The automatic lane is explicit and opt-in. After the user approves the
decomposition, arch-epic asks for a role-based execution table:
`epic_planner`, `implementation_worker`, `repair_worker`, and `critic`.
It resolves shorthand such as `opus 4.7 xhigh` or `gpt 5.5 high` to
runnable model IDs using the shared resolver doctrine, pins the resolved
policy, then drives sub-plans depth-first with spawned hook-suppressed
Claude/Codex harnesses. Automatic workers apply arch-step doctrine directly
from disk; they do not arm nested `auto-plan`, `implement-loop`, or
`arch-loop` controllers.

Progressive lazy planning: sub-plan N+1 is not planned until sub-plan
N is complete. The user approves the decomposition up front, then
approves each sub-plan's North Star when it comes up in interactive
mode. In automatic mode, spawned critics check North Star and Epic
Requirement Coverage gates instead of asking the user on every sub-plan.

Resume is the only mode — every `$arch-epic` invocation re-reads the
epic doc and arch-step state from disk and picks up where things left
off. "Continue my epic", "pick up where we left off", "keep going on
<project>" all work.

The skill is a thoughtful wrapper — its job is to reduce user
orchestration burden. In interactive mode, user involvement is bounded
to the goal, decomposition, per-sub-plan North Star, and material
scope-preservation decisions. In automatic mode, the user approves the
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
- "Run the epic automatically and ask me which models to use for the
  planner, workers, repair, and critics."

## When not to use

- Single architecture plan: use `$arch-step`.
- One-pass mini plan that hands off to implement: use `$arch-mini-plan`.
- 1–3 phase feature flow: use `$lilarch`.
- Open-ended optimization with bet-and-learn iteration: use `$goal-loop`.
- Requirement-satisfaction loop against a free-form auditor: use
  `$arch-loop`.
- Read-only routing across arch artifacts: use `$arch-flow`.
- Stepped orchestration in a foreign repo with a per-step critic: use
  `$stepwise`.
- One-shot review of a diff, branch, or completion claim: use
  `$code-review` or `$codex-review-yolo`.
- Work that fits in a single orchestrator turn.

## Non-negotiables

Must happen every run:
- Pin `raw_goal` verbatim with `sha256` in the epic doc. Any silent
  rewrite clears the decomposition-approved flag.
- Produce a one-sentence-per-sub-plan decomposition and get user
  approval before planning any sub-plan.
- Each sub-plan is its own full `$arch-step` canonical DOC_PATH.
  The epic doc does NOT contain plan internals (no Sections 0–10,
  no call-site audit).
- Progressive planning: invoke `$arch-step new` for sub-plan N+1
  only after sub-plan N is `complete` per the epic critic.
- Per-sub-plan North Star approval uses `$arch-step`'s existing
  North-Star gate. `arch-epic` does not re-invent it — it just
  stops when arch-step stops. In automatic mode, this gate is replaced
  by a fresh North-Star critic harness after the user-approved
  decomposition and role table are pinned.
- Per-sub-plan implementation runs through
  `$arch-step implement-loop` in interactive mode. In automatic mode,
  spawned implementation workers execute the approved sub-plan directly
  from arch-step doctrine and the sub-plan doc; the top-level
  orchestrator still does not edit target code itself.
- Epic critic runs once per sub-plan at sub-plan completion and
  returns structured JSON `EpicVerdict`. Critic is a separate
  subprocess (claude or codex).
- Both arch-step invocations and critic subprocesses run dangerous
  / skip-permissions / no-sandbox per repo convention.
- User supplies execution policy at invocation or at the role-table
  gate. Interactive mode needs critic runtime + model + effort.
  Automatic mode needs role execution for `epic_planner`,
  `implementation_worker`, `repair_worker`, and `critic`. The skill
  asks once for missing role values and never silently defaults.
- Resume is re-entrant: any invocation against an existing epic doc
  re-reads on-disk state and continues. No dedicated `resume`
  command.

Must never happen:
- `arch-epic` editing the target repo's code directly. Sub-plans do
  that via arch-step's implement-loop in interactive mode or spawned
  implementation workers in automatic mode.
- Scope reduction. The epic scope is the epic scope. If the critic
  sees a dropped, narrowed, parked, or moved requirement from the raw
  goal, approved Decomposition, North Star, Epic Requirement Coverage,
  Section 7, acceptance criteria, or verification obligations, the
  sub-plan fails. Agent-written Decision Log entries are evidence, not
  approval to reduce scope.
- Auto-acting on materially-different-path detections without user
  approval. Material scope discoveries always halt and preserve scope
  through `extend_current` or `new_sub_plan`. There is no automatic
  defer/drop path and no supported scope-reduction lane inside
  arch-epic auto mode.
- Parallel or breadth-first sub-plan planning. Only one sub-plan is
  active at a time, and sub-plan N+1 starts only after sub-plan N is
  complete and has no blocking critic findings.
- Two-second child polling. Automatic mode defaults to 180-second waits
  while waiting for spawned harnesses unless the user explicitly pins a
  different cadence in the role policy.
- Calling a slow planner or worker "hung" just because it has no final
  artifact after a few minutes. Automatic children often run for 5+ minutes;
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
  skill figures it out from the epic doc + arch-step state files.

## First move

1. Capture the user's goal verbatim. Compute `sha256`.
2. Resolve or propose the epic doc path
   (`docs/EPIC_<TITLE>_<YYYY-MM-DD>.md`).
3. Read `references/model-and-effort.md`. If the user is starting
   the interactive lane and did not name runtime + model + effort for
   the critic, ask one consolidated question. If the user explicitly
   asked for automatic end-to-end execution, defer execution choices
   to the automatic role-table gate after decomposition approval.
4. Read `references/decomposition-principles.md`. Draft the
   Decomposition (3–7 sub-plans, one-sentence descriptions,
   assertion-style gates, dependency-then-risk ordering).
5. Read `references/epic-doc-contract.md`. Write the epic doc.
6. Surface the Decomposition and ask the user to approve or adjust.

## Six modes (re-entrant; one per turn)

Detail per mode lives in `references/workflow-contract.md`.

1. **`start`** — epic doc does not yet exist. Propose path, ask for
   critic model/effort if missing, draft Decomposition, surface for
   approval.
2. **`approve-decomposition`** — epic doc has
   `sub_plans_approved: false`. Apply user adjustments, flip flag,
   set `status: active`.
3. **`run`** — main orchestration pass. Routes per
   `references/arch-step-integration.md` to the next arch-step
   command for the first non-complete sub-plan, or waits for a
   hook-backed controller, or runs the critic.
4. **`resume-scope-change`** — epic is `halted` after a critic
   flagged a scope change; user has replied with their preservation
   decision. Apply `extend_current` or `new_sub_plan`, log, resume.
5. **`summary`** — user asked a status question. Render a table of
   sub-plan statuses and the most recent log entries. No state
   changes.
6. **`auto-run`** — explicit automatic lane after decomposition
   approval. Resolve/pin the role execution table, initialize the
   auto run directory, then drive one active sub-plan depth-first
   through planner, implementation, repair, and critic harnesses.

## Output expectations

- Epic doc at the user-named (or proposed) path.
- Per-sub-plan canonical arch-step DOC_PATHs under
  `docs/epic/<EPIC_SLUG_WITH_DATE>/PHASE_<NN>_<SUBPLAN_SLUG>_<YYYY-MM-DD>.md`,
  owned by arch-step.
- Epic critic artifacts under
  `<orchestrator repo root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/`
  including the EpicVerdict JSON, the exact invocation.sh, and the
  subprocess stream log.
- Automatic-mode artifacts under
  `<orchestrator repo root>/.arch_skill/arch-epic/auto/<epic-slug>/run-<ts>/`
  including `state.json`, `execution_policy.json`, worker prompts,
  worker session IDs, critic verdicts, child `events.jsonl`,
  `stderr.log`, `stream.log`, `heartbeat.json`, `monitor.json`, and
  `report.md`.
- Orchestration Log and Decision Log append-only in the epic doc.
- Console summary with the epic doc path, the per-sub-plan status
  table, and the current active sub-plan's next action.

## Reference map

- `references/workflow-contract.md` — six modes with inputs,
  outputs, failure modes, judgment-vs-determinism split.
- `references/epic-doc-contract.md` — epic doc shape, frontmatter,
  section structure, mutation rules, validation on load.
- `references/decomposition-principles.md` — when to split a goal
  into sub-plans. Prose reasoning with worked examples; no keyword
  tables.
- `references/arch-step-integration.md` — sub-plan Status →
  arch-step command mapping. What the skill invokes vs. what the
  hook drives vs. what the user does.
- `references/scope-change-discipline.md` — approved scope lock,
  materially-different path vs noise, and preservation-only scope
  decisions.
- `references/critic-contract.md` — EpicVerdict JSON schema and
  scope-drift / requirement-coverage checks.
- `references/critic-prompt.md` — verbatim critic prompt body with
  placeholders.
- `references/auto-harness-prompts.md` — role-specific prompt
  contracts for automatic planner, implementation, repair, and critic
  harnesses.
- `references/epic-verdict-schema.json` — JSON schema file used by
  Codex `--output-schema` (and inlined into Claude `--json-schema`).
- `references/model-and-effort.md` — role-based execution policy,
  model shorthand resolution, exact-version preservation, and ask-once
  discipline.
- `references/resume-semantics.md` — how the skill re-derives state
  each turn from the epic doc + arch-step controller state files.
- `references/examples.md` — worked examples: happy path,
  scope-change insertion, harmless observations ignored.

## The orchestration script

`scripts/run_arch_epic.py` is deterministic plumbing. It resolves
automatic-mode execution policy, creates run directories, spawns and
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
  --runtime claude|codex \
  --model <model> \
  --effort <effort> \
  [--orchestrator-root <dir>]
```

Automatic-mode examples:

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
