---
name: arch-epic
description: "Orchestrate a goal too large for one `$arch-step` plan by decomposing it into approved ordered sub-plans, running each through `$arch-step new`, `auto-plan`, `implement-loop`, and `audit-implementation`, then launching a fresh critic to catch scope drift before advancing. Use when the user asks to break up and run a multi-plan epic, continue an existing epic, or resume from an on-disk epic doc. Planning is progressive: sub-plan N+1 starts only after sub-plan N completes and passes the critic. Not for a single architecture plan (`$arch-step`), one-pass mini plan (`$arch-mini-plan`), small 1-3 phase feature (`$lilarch`), open-ended optimization (`$goal-loop`), read-only status routing (`$arch-flow`), or foreign-repo step orchestration (`$stepwise`)."
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
drift against the approved North Star. If the critic finds a must-have
discovery or a non-trivial scope change, the skill halts and asks the
user how to resolve it (extend, insert a new sub-plan, defer, or drop).
Otherwise it advances to the next sub-plan.

Progressive lazy planning: sub-plan N+1 is not planned until sub-plan
N is complete. The user approves the decomposition up front, then
approves each sub-plan's North Star when it comes up.

Resume is the only mode — every `$arch-epic` invocation re-reads the
epic doc and arch-step state from disk and picks up where things left
off. "Continue my epic", "pick up where we left off", "keep going on
<project>" all work.

The skill is a thoughtful wrapper — its job is to reduce user
orchestration burden. User involvement is bounded to four decision
points: the goal, the decomposition, per-sub-plan North Star (arch-step
handles that gate), and scope-change decisions when the critic flags
something material.

## When to use

- "This is too big for one arch-step plan. Help me break it into plans
  and run them in order."
- "Orchestrate these sub-plans: X, Y, Z. Check each one before moving
  to the next."
- "Continue my epic at `docs/EPIC_<slug>_<date>.md`."
- "Keep going on the <goal> epic."
- "Pick up where we left off on <project>."

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
  stops when arch-step stops.
- Per-sub-plan implementation runs through
  `$arch-step implement-loop`. `arch-epic` does NOT implement code
  itself.
- Epic critic runs once per sub-plan at sub-plan completion and
  returns structured JSON `EpicVerdict`. Critic is a separate
  subprocess (claude or codex).
- Both arch-step invocations and critic subprocesses run dangerous
  / skip-permissions / no-sandbox per repo convention.
- User supplies critic runtime + model + effort at invocation;
  skill asks once if missing; never silently defaults.
- Resume is re-entrant: any invocation against an existing epic doc
  re-reads on-disk state and continues. No dedicated `resume`
  command.

Must never happen:
- `arch-epic` editing the target repo's code directly. Sub-plans do
  that via arch-step's implement-loop.
- Silent scope changes. If the critic sees a dropped acceptance
  criterion or a silent addition without a Decision Log entry, the
  sub-plan fails.
- Auto-acting on materially-different-path detections without user
  approval when the choice is non-obvious. Only nice-to-have
  discoveries with `defer` or `drop` recommendations auto-apply;
  must-have or `extend_current`/`new_sub_plan` always halt.
- Parallel sub-plan planning. Only one sub-plan is active at a time.
- Heuristic keyword mapping for decomposition. Interpretation is
  prose reasoning, taught by `references/decomposition-principles.md`.
- A second "resume" command. The user types what they type; the
  skill figures it out from the epic doc + arch-step state files.

## First move

1. Capture the user's goal verbatim. Compute `sha256`.
2. Resolve or propose the epic doc path
   (`docs/EPIC_<TITLE>_<YYYY-MM-DD>.md`).
3. Read `references/model-and-effort.md`. If the user's prompt does
   not name runtime + model + effort for the critic, ask one
   consolidated question.
4. Read `references/decomposition-principles.md`. Draft the
   Decomposition (3–7 sub-plans, one-sentence descriptions,
   assertion-style gates, dependency-then-risk ordering).
5. Read `references/epic-doc-contract.md`. Write the epic doc.
6. Surface the Decomposition and ask the user to approve or adjust.

## Five modes (re-entrant; one per turn)

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
   flagged a scope change; user has replied with their decision.
   Apply (extend, insert, defer, drop), log, resume.
5. **`summary`** — user asked a status question. Render a table of
   sub-plan statuses and the most recent log entries. No state
   changes.

## Output expectations

- Epic doc at the user-named (or proposed) path.
- Per-sub-plan canonical arch-step DOC_PATHs under the repo's usual
  docs/ directory, owned by arch-step.
- Epic critic artifacts under
  `<orchestrator repo root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/`
  including the EpicVerdict JSON, the exact invocation.sh, and the
  subprocess stream log.
- Orchestration Log and Decision Log append-only in the epic doc.
- Console summary with the epic doc path, the per-sub-plan status
  table, and the current active sub-plan's next action.

## Reference map

- `references/workflow-contract.md` — five modes with inputs,
  outputs, failure modes, judgment-vs-determinism split.
- `references/epic-doc-contract.md` — epic doc shape, frontmatter,
  section structure, mutation rules, validation on load.
- `references/decomposition-principles.md` — when to split a goal
  into sub-plans. Prose reasoning with worked examples; no keyword
  tables.
- `references/arch-step-integration.md` — sub-plan Status →
  arch-step command mapping. What the skill invokes vs. what the
  hook drives vs. what the user does.
- `references/scope-change-discipline.md` — materially-different
  path vs noise. Auto-act rule for discovered items.
- `references/critic-contract.md` — EpicVerdict JSON schema and
  the four scope-drift checks.
- `references/critic-prompt.md` — verbatim critic prompt body with
  placeholders.
- `references/epic-verdict-schema.json` — JSON schema file used by
  Codex `--output-schema` (and inlined into Claude `--json-schema`).
- `references/model-and-effort.md` — how to elicit critic runtime +
  model + effort from the user; ask-once discipline.
- `references/resume-semantics.md` — how the skill re-derives state
  each turn from the epic doc + arch-step controller state files.
- `references/examples.md` — worked examples: happy path,
  scope-change insertion, nice-to-have auto-defer.

## The orchestration script

`scripts/run_arch_epic.py` is deterministic plumbing. Its one
subcommand spawns the critic subprocess and writes run-directory
artifacts. It does NOT interpret decomposition, draft the epic doc,
decide verdicts, or route sub-plan states — those live in the
orchestrator's prose reasoning.

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

Prints the verdict JSON path. Writes:
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/prompt.md`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/invocation.sh`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/stdout.final.json`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/stream.log`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/verdict.json`
- `<orch-root>/.arch_skill/arch-epic/critics/<slug>/run-<ts>/start_ts` / `end_ts` / `exit_code`
