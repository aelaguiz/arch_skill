# `arch-loop` Controller Contract

Core doctrine and lifecycle live in `skills/_shared/controller-contract.md`.
This file documents only the `arch-loop`-specific state schema and the
external-evaluator verdict source. `arch-loop` is the single controller whose
terminal verdict comes from a fresh external Codex `gpt-5.4` `xhigh`
evaluator; that deviation is documented in the shared contract's Deviations
section.

## What this contract governs

- the runtime-aware controller state file for one armed `arch-loop` session
- the parent-pass writes and Stop-hook-owned writes allowed on that state
- the verdict lifecycle that the shared Stop hook uses to continue, wait/recheck, stop clean, stop blocked, or stop on a cap
- the named-audit evidence shape a parent pass must populate before the external evaluator can reach `clean`

The shared runner at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py` owns hook dispatch, state validation, cap enforcement, cadence scheduling, evaluator launch, and verdict handling. `arch-loop` does not introduce a separate controller binary.

## Required arm-time install

Arm-time ensure-install and dispatch-time loud verify are documented in `skills/_shared/controller-contract.md`. Before arming, run:

```bash
python3 ~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py \
  --ensure-installed --runtime <codex|claude>
```

Proceed only if it returns 0. The installer is idempotent and flock-guarded; it writes the canonical Stop entry (and the SessionStart entry on Claude) without races. The evaluator prompt must also exist at `<skills-root>/arch-loop/references/evaluator-prompt.md` (`<skills-root>` is `~/.agents/skills` when running from the installed runner or `skills/` when running from the repo source). The external evaluator is always Codex `gpt-5.4` `xhigh`, even when Claude hosts the Stop hook.

## State file path by runtime

- Codex: `.codex/arch-loop-state.<SESSION_ID>.json` (derive `SESSION_ID` from `CODEX_THREAD_ID`)
- Claude Code: `.claude/arch_skill/arch-loop-state.<SESSION_ID>.json` (resolve via `arch_controller_stop_hook.py --current-session`; abort with its error if the SessionStart cache is missing — never write an unsuffixed file)

One session may arm only one arch_skill controller kind at a time. The shared runner's duplicate-controller check fails loud if `arch-loop` and any other controller state, or two `arch-loop` state files, are armed for the same session.

## State schema (version 2)

```json
{
  "version": 2,
  "command": "arch-loop",
  "session_id": "<CODEX_THREAD_ID or runtime session id>",
  "runtime": "codex",
  "raw_requirements": "<literal user requirements>",
  "raw_requirements_hash": "<sha256 hex of raw_requirements UTF-8 bytes>",
  "audits_authoritative_fingerprint": "<sha256 hex of canonical audit tuples>",
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

- `version` (always `2` for this release; version `1` state is cleared with a one-line "re-arm required due to arch-loop schema upgrade")
- `command` (always `"arch-loop"`)
- `session_id`
- `runtime` (`"codex"` or `"claude"`)
- `raw_requirements` (literal user prose, never rewritten)
- `raw_requirements_hash` (parent writes this at arm; must equal `sha256(raw_requirements)` on every read)
- `created_at` (epoch seconds)
- `iteration_count` (starts at `0`, incremented by the Stop hook after each completed parent work pass)

### Optional (enforced when present)

- `audits_authoritative_fingerprint` (Stop-hook-owned; seeded on first hook dispatch, required on every continuation read; `sha256` over the canonical serialization of every audit's `(skill, target, requirement, status)` tuple sorted by `(skill, target)`)
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

The parent seeds each entry with `status: pending` at arm and may refresh `latest_summary` / `evidence_path` on every continuation pass. After the first Stop-hook dispatch, `status` is hook-owned: the runner copies it from the evaluator's JSON output, recomputes `audits_authoritative_fingerprint`, and rejects any parent-side edit to `(skill, target, requirement, status)` at the next read. A required audit with `status` other than `pass` or `inapplicable` prevents `clean`.

## Writes by actor

### Parent `arch-loop` pass

- creates or refreshes the runtime-specific state file before any work pass starts
- captures `raw_requirements` literally; never normalizes or shortens the user's request
- computes `raw_requirements_hash = sha256(raw_requirements_bytes_utf8)` at arm and writes it to state; never rewrites the hash across turns
- writes parsed caps/cadence into `deadline_at`, `interval_seconds`, `max_iterations`, and `cap_evidence`
- detects named audits and seeds `required_skill_audits` entries with `status: pending` at arm only; after the first Stop-hook dispatch, `status` is hook-owned and any parent-side edit is rejected at the next read
- runs named audits during the work pass and refreshes each entry's `latest_summary` and optional `evidence_path` (never `status`)
- writes `last_work_summary` and `last_verification_summary`
- never writes `last_evaluator_verdict`, `last_evaluator_summary`, `last_next_task`, `last_continue_mode`, `iteration_count`, `check_count`, `next_due_at`, `audits_authoritative_fingerprint`, or `required_skill_audits[].status` after the initial arm seed; the Stop hook owns those fields
- never clears the state file; only the Stop hook may delete state

### Stop hook

- validates `raw_requirements_hash` on every read; any mismatch clears state with `raw_requirements mutation detected`
- validates `audits_authoritative_fingerprint` on every continuation read; any mismatch clears state with `audit status mutation detected`
- increments `iteration_count` for a parent work pass that just completed
- increments `check_count` for each cadence-owned evaluator/check pass
- enforces `deadline_at` and `max_iterations` before launching the evaluator
- schedules `next_due_at` and sleeps until `min(next_due_at, deadline_at)` when cadence is armed and the last verdict was `wait_recheck`
- launches the fresh Codex `gpt-5.4` `xhigh` evaluator with the prompt at `references/evaluator-prompt.md`
- copies each evaluator `required_skill_audits[].status` and `evidence` pointer into the matching state entry (by `skill` name), recomputes `audits_authoritative_fingerprint`, and persists state before dispatching the verdict
- writes `last_evaluator_verdict`, `last_evaluator_summary`, `last_next_task`, `last_continue_mode`
- clears state on `clean`, `blocked`, timeout, max-iterations, or any controller failure (invalid state, missing evaluator prompt, failed child, invalid JSON, missing `evidence` on any `satisfied_requirements` or `required_skill_audits` entry)

## Lifecycle

### 1) Arm

- parent ensure-install returns 0, state file is written, one bounded work pass runs, named audits are refreshed, the turn ends naturally

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

- missing required field (`version`, `command`, `session_id`, `runtime`, `raw_requirements`, `raw_requirements_hash`, `created_at`, `iteration_count`)
- `version` other than `2` (version-`1` state is cleared with `re-arm required due to arch-loop schema upgrade`)
- `command` other than `"arch-loop"`
- `session_id` that does not match the current hook payload
- `sha256(raw_requirements) != raw_requirements_hash` (cleared with `raw_requirements mutation detected`)
- `audits_authoritative_fingerprint` missing or mismatched on a continuation read (cleared with `audit status mutation detected`)
- `interval_seconds <= 0`, `max_iterations <= 0`, or `deadline_at` earlier than `created_at`
- `required_skill_audits` entries with an unknown `status`
- `next_due_at` later than `deadline_at`

The shared runner reports the specific broken field so the user can repair and re-arm.

## Active-work vs wait/recheck distinction

- `parent_work` means the parent agent must take another bounded pass. The hook blocks with a continuation prompt naming `$arch-loop` and the next concrete `next_task`.
- `wait_recheck` means no parent work is useful until the next interval. The hook owns sleeping and rechecking; the parent thread is not woken. This mode is only legal when `interval_seconds` is armed.

The evaluator chooses the mode per verdict. Deterministic code never tries to infer mode from requirement text.
