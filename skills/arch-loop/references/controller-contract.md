# `arch-loop` Controller Contract

## What this contract governs

- the runtime-aware controller state file for one armed `arch-loop` session
- the parent-pass writes and Stop-hook-owned writes allowed on that state
- the verdict lifecycle that the shared Stop hook uses to continue, wait/recheck, stop clean, stop blocked, or stop on a cap
- the named-audit evidence shape a parent pass must populate before the external evaluator can reach `clean`

The shared runner at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py` owns hook dispatch, state validation, cap enforcement, cadence scheduling, evaluator launch, and verdict handling. `arch-loop` does not introduce a separate controller binary.

## Runtime preflight (required before arming)

- the active host runtime is Codex or Claude Code
- the active host runtime has the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex` in `~/.codex/hooks.json` (Codex) or `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude` in `~/.claude/settings.json` (Claude Code)
- the installed runner exists at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`
- in Codex, `codex features list` shows `codex_hooks` enabled
- in Claude Code, hook-suppressed child runs via `claude -p --settings '{"disableAllHooks":true}'` work with the machine's normal Claude auth (required only when a Claude child is the named audit runner; the external evaluator is always Codex)
- the evaluator prompt exists at `<skills-root>/arch-loop/references/evaluator-prompt.md` where `<skills-root>` is `~/.agents/skills` when running from the installed runner or `skills/` when running from the repo source

If any prerequisite is missing, name the broken item and stop. Do not downgrade to prompt-only repetition and do not preflight against a copied hook file under `~/.codex/hooks/`.

## State file path by runtime

- Codex: `.codex/arch-loop-state.<SESSION_ID>.json` (derive `SESSION_ID` from `CODEX_THREAD_ID`)
- Claude Code: `.claude/arch_skill/arch-loop-state.<SESSION_ID>.json` when the session id is available before the first Stop-hook turn; otherwise `.claude/arch_skill/arch-loop-state.json` until the first Stop-hook turn claims session ownership

One session may arm multiple arch_skill auto controllers of different kinds, but not two `arch-loop` state files. The shared runner's duplicate-controller check fails loud if two `arch-loop` state files are armed for the same session.

## State schema (version 1)

```json
{
  "version": 1,
  "command": "arch-loop",
  "session_id": "<CODEX_THREAD_ID or runtime session id>",
  "runtime": "codex",
  "raw_requirements": "<literal user requirements>",
  "created_at": 1770000000,
  "deadline_at": 1770018000,
  "interval_seconds": 1800,
  "next_due_at": 1770001800,
  "max_iterations": 5,
  "iteration_count": 0,
  "check_count": 0,
  "cap_evidence": [
    {
      "type": "runtime",
      "source_text": "max runtime 5h",
      "normalized": "deadline_at=1770018000"
    },
    {
      "type": "cadence",
      "source_text": "every 30 minutes",
      "normalized": "interval_seconds=1800"
    }
  ],
  "required_skill_audits": [
    {
      "skill": "agent-linter",
      "target": "skills/arch-loop",
      "requirement": "clean bill of health",
      "status": "pending",
      "latest_summary": "",
      "evidence_path": ""
    }
  ],
  "last_work_summary": "",
  "last_verification_summary": "",
  "last_evaluator_verdict": "",
  "last_evaluator_summary": "",
  "last_next_task": "",
  "last_continue_mode": ""
}
```

### Required fields

- `version` (always `1` for this release)
- `command` (always `"arch-loop"`)
- `session_id`
- `runtime` (`"codex"` or `"claude"`)
- `raw_requirements` (literal user prose, never rewritten)
- `created_at` (epoch seconds)
- `iteration_count` (starts at `0`, incremented by the Stop hook after each completed parent work pass)

### Optional (enforced when present)

- `deadline_at` (epoch seconds)
- `interval_seconds` (positive integer; required when `continue_mode=wait_recheck`)
- `next_due_at` (epoch seconds; maintained by the Stop hook during cadence waits)
- `max_iterations` (positive integer)
- `check_count` (starts at `0`, incremented by the Stop hook after each cadence-owned evaluator/check pass)
- `cap_evidence` (list of `{type, source_text, normalized}` entries; `type` is `runtime`, `cadence`, or `iterations`)
- `required_skill_audits` (list of named-audit evidence entries; see below)
- `last_work_summary`, `last_verification_summary`, `last_evaluator_verdict`, `last_evaluator_summary`, `last_next_task`, `last_continue_mode`

### Named-audit evidence entry

Each required audit preserves the requirement source and its current status:

- `skill`: skill name without the `$` prefix (for example `"agent-linter"`)
- `target`: artifact or scope to audit (path, slug, or brief description)
- `requirement`: success condition copied from `raw_requirements`
- `status`: one of `pending`, `pass`, `fail`, `missing`, `inapplicable`
- `latest_summary`: short human-readable result string
- `evidence_path`: optional path to a longer artifact when the audit output is too long to inline

The parent agent runs named skills during work passes and updates evidence. The external evaluator verifies that evidence before allowing `clean`. A required audit with `status` other than `pass` or `inapplicable` prevents `clean`.

## Writes by actor

### Parent `arch-loop` pass

- creates or refreshes the runtime-specific state file before any work pass starts
- captures `raw_requirements` literally; never normalizes or shortens the user's request
- writes parsed caps/cadence into `deadline_at`, `interval_seconds`, `max_iterations`, and `cap_evidence`
- detects named audits and seeds `required_skill_audits` as `pending`
- runs named audits during the work pass and updates each entry's `status`, `latest_summary`, and optional `evidence_path`
- writes `last_work_summary` and `last_verification_summary`
- never writes `last_evaluator_verdict`, `last_evaluator_summary`, `last_next_task`, `last_continue_mode`, `iteration_count`, `check_count`, or `next_due_at`; the Stop hook owns those fields
- never clears the state file; only the Stop hook may delete state

### Stop hook

- increments `iteration_count` for a parent work pass that just completed
- increments `check_count` for each cadence-owned evaluator/check pass
- enforces `deadline_at` and `max_iterations` before launching the evaluator
- schedules `next_due_at` and sleeps until `min(next_due_at, deadline_at)` when cadence is armed and the last verdict was `wait_recheck`
- launches the fresh Codex `gpt-5.4` `xhigh` evaluator with the prompt at `references/evaluator-prompt.md`
- writes `last_evaluator_verdict`, `last_evaluator_summary`, `last_next_task`, `last_continue_mode`
- clears state on `clean`, `blocked`, timeout, max-iterations, or any controller failure (invalid state, missing evaluator prompt, failed child, invalid JSON)

## Lifecycle

### 1) Arm

- parent preflight succeeds, state file is written, one bounded work pass runs, named audits are refreshed, the turn ends naturally

### 2) Stop hook evaluation

- validates the state file and session id (if either fails, the hook clears state and stops loudly)
- if `deadline_at` is already past, the hook clears state and stops with a timeout summary (no further evaluator run)
- if `iteration_count >= max_iterations` and the last verdict was `continue` with `parent_work`, the hook clears state and stops with a max-iterations summary
- if `next_due_at` is present and in the future, the hook sleeps until `min(next_due_at, deadline_at)` before launching the evaluator
- the hook launches the evaluator and parses the structured JSON verdict

### 3) Verdict handling

- `clean`: clear state and stop naturally with the evaluator summary
- `blocked`: clear state and stop loudly with the `blocker` field
- `continue` with `continue_mode: parent_work`:
  - require `next_task`
  - if `max_iterations` is present and the next pass would exceed it, clear state and stop with a max-iterations summary that includes the evaluator's unsatisfied requirements
  - otherwise persist `last_evaluator_summary`, `last_next_task`, `last_continue_mode`, keep state armed, and block with a continuation prompt that tells the parent agent to invoke `$arch-loop` against the existing state and perform `next_task`
- `continue` with `continue_mode: wait_recheck`:
  - require `interval_seconds` in state (fail loud if unarmed cadence)
  - require `next_task` (names the next read-only check/evaluation)
  - set `next_due_at = now + interval_seconds`
  - verify `next_due_at` still fits inside `deadline_at` and the installed hook timeout; if not, clear state and stop with a hook-timeout-fit or timeout summary
  - persist `last_evaluator_summary`, `last_next_task`, `last_continue_mode`, increment `check_count`, keep state armed, and continue the hook-owned wait/recheck cycle without waking the parent
- controller failure (invalid JSON, missing verdict, `continue` without `continue_mode`, `continue` without `next_task`, `wait_recheck` without `interval_seconds`, `blocked` without `blocker`, `clean` with missing required audit evidence): clear state and stop loudly with the failure reason

### 4) Continuation invocation by the parent

- the parent reads the armed state file instead of asking the user to restate requirements
- it treats `last_next_task` as guidance, not a replacement for `raw_requirements`
- it does one bounded work pass, refreshes named-audit evidence, and ends the turn naturally
- if `last_continue_mode` was `wait_recheck`, the parent does not act as the parent pass until the hook decides parent work is useful or the loop stops

## Cap enforcement rules

- runtime caps: `deadline_at = created_at + duration_seconds`. Past deadline stops the loop before another evaluator run.
- iteration caps: `max_iterations` limits completed parent work passes. Reaching the cap with an unsatisfied `continue` stops the loop.
- cadence: `interval_seconds` defines the wait window between hook-owned evaluator/check passes. The evaluator decides when to switch from `wait_recheck` to `parent_work` (active work is useful) or `clean` (condition met).
- hook-timeout fit: the next `next_due_at` must fit inside the installed Stop-hook timeout. The shared runner inherits the installed hook timeout from the host runtime (the repo installer sets `90000` seconds). If a requested cadence/deadline cannot fit, the arm must fail loud before state is written.

## Invalid-state behavior

The Stop hook treats any of the following as invalid state and clears it rather than guessing:

- missing required field (`version`, `command`, `session_id`, `runtime`, `raw_requirements`, `created_at`, `iteration_count`)
- `version` other than `1`
- `command` other than `"arch-loop"`
- `session_id` that does not match the current hook payload (after normal legacy-path reconciliation)
- `interval_seconds <= 0`, `max_iterations <= 0`, or `deadline_at` earlier than `created_at`
- `required_skill_audits` entries with an unknown `status`
- `next_due_at` later than `deadline_at`

The shared runner reports the specific broken field so the user can repair and re-arm.

## Active-work vs wait/recheck distinction

- `parent_work` means the parent agent must take another bounded pass. The hook blocks with a continuation prompt naming `$arch-loop` and the next concrete `next_task`.
- `wait_recheck` means no parent work is useful until the next interval. The hook owns sleeping and rechecking; the parent thread is not woken. This mode is only legal when `interval_seconds` is armed.

The evaluator chooses the mode per verdict. Deterministic code never tries to infer mode from requirement text.
