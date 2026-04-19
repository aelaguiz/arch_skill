# `auto-plan` Command Contract

## What this command does

- take one approved canonical mini full-arch doc through the planning arc automatically
- arm one hook-backed multi-turn planning controller over `research`, `deep-dive`, and `phase-plan`
- run only the first stage from the parent `auto-plan` pass, then rely on the installed Stop hook to feed one literal next command per later turn
- use the installed runtime-native continuation support to move stage to stage
- stop after `phase-plan` is complete and hand off cleanly to `implement-loop`
- keep `DOC_PATH` and controller state aligned while the controller is armed

## Planning North Star

Running `auto-plan` should end in one of two honest states:

- `ready`:
  - research grounding is present
  - one deep-dive pass is present
  - the authoritative phase plan is present
  - no unresolved decisions remain in the authoritative artifact
  - no implementation has started
  - the final message says the doc is decision-complete and ready for `implement-loop`
- `blocked`:
  - the controller state is cleared
  - the blocker or early stop is explicit
  - the run stops instead of silently pretending the planning arc finished

User-facing invocation is just `auto-plan`. Do not run the Stop hook yourself. After the controller is armed, just end the turn and let the installed Stop hook run. The quality bar for this controller is one stage per turn: the parent `auto-plan` pass runs only `research`, ends its turn, then the Stop hook feeds the next literal command on later turns. If the installed runtime support for real automatic sequencing is absent or disabled, this command must fail loud instead of pretending prompt-only chaining is the same feature.

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Section 3, Section 4, Section 5, Section 6, Section 7, and `planning_passes`
- `arch-research.md`
- `arch-deep-dive.md`
- `arch-phase-plan.md`

## Inputs and `DOC_PATH` resolution

- treat the user ask as steering plus any planning preferences
- if the ask includes a `docs/<...>.md` path, use it
- otherwise resolve `DOC_PATH` from the normal `miniarch-step` defaults
- if the current session just created or most recently updated one canonical full-arch doc, prefer that doc
- if the doc path is truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates

## Writes

- `DOC_PATH`
- `planning_passes`
- the host-aware miniarch-step auto-plan controller state path:
  - Codex: `.codex/miniarch-step-auto-plan-state.<SESSION_ID>.json`
  - Claude Code: `.claude/arch_skill/miniarch-step-auto-plan-state.<SESSION_ID>.json` when session id is available before the first Stop-hook turn, otherwise `.claude/arch_skill/miniarch-step-auto-plan-state.json` as a legacy single-slot fallback until the first Stop-hook turn claims it into the session-scoped path

## Required runtime preflight

Before arming the controller, verify all of these:

- the active host runtime is Codex or Claude Code
- the active host runtime has the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex` in Codex or `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude` in Claude Code
- the installed shared runner exists at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`
- in Codex, `codex features list` shows `codex_hooks` enabled
- the target doc exists and frontmatter `status` is `active` or `complete`

If any check fails, name the broken prerequisite and stop.

Do not downgrade to prompt-only same-session chaining.
Do not preflight against a copied hook file under `~/.codex/hooks/`; that is not the install contract.

## Active planning-state contract

Resolve the controller state path for the active host runtime after preflight and `DOC_PATH` resolution:

- Codex: derive `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/miniarch-step-auto-plan-state.<SESSION_ID>.json`
- Claude Code: prefer `.claude/arch_skill/miniarch-step-auto-plan-state.<SESSION_ID>.json` when the session id is available before the first Stop-hook turn; otherwise create `.claude/arch_skill/miniarch-step-auto-plan-state.json` only as a legacy single-slot fallback and let the first Stop-hook turn claim it into the session-scoped path

Minimal shape:

```json
{
  "version": 1,
  "command": "miniarch-step-auto-plan",
  "session_id": "<SESSION_ID>",
  "doc_path": "docs/<PLAN>.md"
}
```

Lifecycle:

- create or refresh it after preflight and `DOC_PATH` resolution
- write the current `doc_path` into the state file at arm time
- write `session_id` at arm time when the host runtime exposes it before the first Stop-hook turn; otherwise let the first Stop-hook turn claim it
- leave it armed while automatic planning is active
- treat `DOC_PATH` as the only planning-progress ledger
- treat the state file as armed controller state for one doc and one session, not as a progress ledger
- on reruns, let the Stop hook reconcile from doc truth and continue from the first incomplete stage
- only the Stop hook may delete it after controller state is armed, including successful completion, blockers, ambiguity, and other early stops
- parent stages must not run `rm` or guess a controller state path after arming; stop honestly and let the Stop hook clear the matching state

## Hard Rules

- docs-only; do not modify code
- this command is a bounded controller over `research`, `deep-dive`, and `phase-plan`; do not invent a second planning surface
- `auto-plan` is one command; if the required runtime continuation support is absent or disabled, fail loud
- if a planning stage in this controller explicitly uses parallel agents, spawn those agents with model `gpt-5.4-mini` and reasoning effort `xhigh`
- use the same `DOC_PATH` for every stage in the controller
- the installed runtime continuation path owns stage-to-stage continuation
- the initial parent `auto-plan` pass must run only `research`, then end its turn naturally
- rerunning `auto-plan` on a partially complete doc is legal; re-arm the controller and let the Stop hook resume from the first incomplete stage in `DOC_PATH`
- later planning stages are hook-owned only; the parent pass must not self-run `deep-dive` or `phase-plan` in the same turn
- the parent pass must not clear successful controller state, claim the planning arc is complete, or emit the `implement-loop` handoff
- planning stages stay in the same visible thread across separate turns; do not hide them in silent child planning runs or collapse them into one long same-turn chain
- if a stage stops before it updates the required canonical outputs, stop and report that truth plainly; the Stop hook clears the matching armed state
- if any stage uncovers an unresolved decision that repo truth cannot settle, stop and ask the exact blocker question instead of continuing; the Stop hook clears the matching armed state
- after successful `phase-plan`, the Stop hook clears the armed miniarch-step auto-plan state, stops, and says the doc is decision-complete and ready for `implement-loop`

## Wrong Pattern

- arm state, run `research`, then immediately self-run `deep-dive` and `phase-plan` in the same assistant turn, then disarm the controller as if the hook had owned continuation

## Right Pattern

- arm state, run exactly one stage, end the turn naturally, let the Stop hook feed the next literal command, and repeat until the hook clears state after successful `phase-plan`

## Stage Completion Signals

Use these signals before the Stop hook continues automatically:

- `research`:
  - `arch_skill:block:research_grounding` is present
- `deep-dive`:
  - `arch_skill:block:current_architecture` is present
  - `arch_skill:block:target_architecture` is present
  - `arch_skill:block:call_site_audit` is present
  - `planning_passes` marks `deep_dive_pass_1: done <YYYY-MM-DD>`
- `phase-plan`:
  - `arch_skill:block:phase_plan` is present
  - the plan has no unresolved architecture-shaping decisions
  - Section 7 phases have exhaustive checklists and exit criteria for the approved scope

## Controller Procedure

1. Read `DOC_PATH` fully and run the same alignment checks required by the planning commands it will invoke.
2. Run the runtime preflight. If the active runtime's hook entry, the installed runner, or the Codex feature gate is unavailable, fail loud.
3. Resolve the active runtime controller state path, then create or refresh the armed miniarch-step auto-plan state for this session and `DOC_PATH`.
4. Use `DOC_PATH` as the planning ledger:
   - if the doc has no planning progress yet, run one truthful `research` pass and stop there
   - if the doc already has partial progress, do not rerun completed stages; let the Stop hook continue from the first incomplete stage
   - if the doc is already complete through `phase-plan`, stop ready for `implement-loop`
5. Let the installed runtime try to stop. The Stop hook should:
   - no-op when no active auto-plan state matches the current session
   - read the doc and find the first incomplete stage
   - if the first incomplete stage is `deep-dive`, feed `Use $miniarch-step deep-dive <DOC_PATH>`
   - if the first incomplete stage is `phase-plan`, feed `Use $miniarch-step phase-plan <DOC_PATH>`
   - after `phase-plan` is complete, clear state and stop with the `implement-loop` handoff message
6. On each hook-driven continuation, run the literal next planning command against the same `DOC_PATH`, keep the controller state armed, and stop naturally after that one stage finishes.
7. If a stage ends early, does not update the required canonical outputs, uncovers a blocker question, or the next move is no longer credible, stop and report that state plainly; the Stop hook clears the matching armed state.

## Console Contract

- one-line North Star reminder
- one-line punchline
- ordinary stage output should stay visible because the planning commands run in the same Codex thread across separate turns
- the final stop message should name `DOC_PATH` and say it is decision-complete and ready for `implement-loop`, or print the exact blocker question that stopped the controller
