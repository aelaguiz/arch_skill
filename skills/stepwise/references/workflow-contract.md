# Workflow contract: the five phases in detail

The skill runs five phases in order. Each phase has concrete inputs,
concrete outputs, and concrete failure modes. Judgment lives in model
prose; determinism lives in `scripts/run_stepwise.py`. This file names
which is which at every step.

## Phase 1 — Intake and interpretation

**Inputs**
- Verbatim user prompt.
- Current working directory (treated as the orchestrator repo root).
- The orchestrator's own session id (used only for run-directory collision
  safety; not for resumption).

**Outputs** (all written into `state.json`)
- `raw_instructions` + `raw_instructions_sha256`.
- `target_repo_path` (absolute, resolved).
- `target_process` — the named process or the explicit intent.
- `profile` — `strict` | `balanced` | `lenient`, per
  `strictness-profiles.md`.
- `forced_checks` — list of check names forced on regardless of profile.
- `stop_discipline` — `halt_and_ask` | `skip_and_continue` |
  `escalate_to_user`.
- `per_step_retry_cap` — integer derived from the profile.
- `sub_session_runtime_default` — `claude` or `codex`.
- `models` — step_model, step_effort, critic_model, critic_effort.
  Asked if missing, per `model-and-effort.md`.

**Where judgment lives:** the agent's prose reasoning. Read the prompt,
decide profile and forced checks, resolve target repo, fill in model
choices (ask if missing). Announce the interpretation before Phase 2.

**Where determinism lives:** the run-directory creation and the hash
computation. Both are script concerns.

**Failure modes**
- Target repo cannot be resolved → ask.
- Genuinely contradictory signals (strict + lenient in the same prompt
  with no tie-breaker) → ask.
- Missing model/effort values → ask (one consolidated question).
- User's prompt names no process and no default is inferable → ask.

Do not proceed to Phase 2 with unresolved gaps. "I'll figure it out in
the next phase" is how heuristic drift starts.

## Phase 2 — Process grounding and manifest drafting

**Inputs**
- State from Phase 1.

**Outputs**
- `doctrine_paths` — the specific files the step sub-sessions should
  read. Usually `<target>/CLAUDE.md`, `<target>/AGENTS.md` (if present),
  and the SKILL.md for the named process.
- `manifest.json` — the full step manifest per `manifest-schema.md`.

**Where judgment lives:** the agent reads the doctrine and drafts the
manifest. This is the most load-bearing piece of prose in the skill.
The manifest must name real artifacts (no invented files) and real
skills (no hallucinated commands). If the doctrine is ambiguous, the
agent asks rather than guesses.

**Where determinism lives:** reading the doctrine files (Read tool) and
writing `manifest.json` to the run directory (script-backed I/O).

**Failure modes**
- Named process does not exist in the target repo's doctrine → ask.
- A sub-step in the doctrine has no verifiable artifact → ask.
- Doctrine contradicts itself across files → surface the contradiction.

## Phase 3 — Plan confirmation

**Inputs**
- Interpretation announcement from Phase 1.
- Manifest from Phase 2.

**Outputs**
- User confirmation (`confirmed: true`) or adjustments.

**Where judgment lives:** nowhere new. This phase just prints and waits
(or prints and proceeds, by profile).

**Gate behavior by profile**
- `strict`: always pause. Wait for explicit "go".
- `balanced`: print and pause once. Proceed on any affirmative reply.
- `lenient`: print and proceed. User can still interrupt.

**The plan is always printed.** Lenient does not mean invisible.

**Failure modes**
- User rejects → re-enter Phase 1 or Phase 2 with adjusted inputs.
  Do not try to "fix" the manifest in-place without rerunning the
  phase that generated it.

## Phase 4 — Step execution loop

For each step `n` from 1 to N:

### 4a. Spawn step sub-session

**Inputs**
- StepDescriptor for step `n`.
- `models.step_model`, `models.step_effort`.
- `target_repo_path`.

**Actions (script-backed)**
- Compose the initial step prompt per `step-prompt-contract.md`.
- Build the invocation per `session-resume.md` for the chosen runtime.
- Run the subprocess. Close stdin (`< /dev/null`).
- Capture: exit code, stdout, the final-message file (`-o`), and the
  session id.
- Write all of the above to `steps/<n>/try-1/`.

**Failure modes**
- Subprocess crashes (non-zero exit) → retry policy treats this as
  a FAIL with crash evidence, subject to the same cap logic.
- Session id not captured (unexpected output shape) → the step cannot
  be resumed. Mark `steps/<n>/try-1/session_id.txt` with
  `UNRECOVERABLE` and skip to the stop_discipline on next critic FAIL.

### 4b. Spawn critic sub-session

**Inputs**
- The descriptor, the per-step doctrine paths, the try's artifacts
  and transcript, the `critic_contract_ref`, the profile.

**Actions (script-backed)**
- Render the critic prompt per `critic-prompt.md`.
- Build the invocation per `session-resume.md` for the critic (Claude
  with `--json-schema`, or Codex with `--output-schema` and
  `--ephemeral`).
- Run the subprocess. Close stdin.
- Parse the StepVerdict from the structured output field (Claude) or
  the `-o` file (Codex).
- Write prompt, invocation, raw output, and parsed verdict into
  `steps/<n>/try-<k>/critic/`.

**Failure modes**
- Critic subprocess crashes → retry the critic once. If it crashes
  again, record BLOCKED for the step and apply stop_discipline.
- Critic output does not parse against the schema → fail loud. Do
  not guess at the verdict; record schema-parse-failure in the
  critic directory and BLOCK.
- Critic writes to disk (detected by diffing target repo before/after
  the critic call) → fail loud. Critics are read-only by contract.

### 4c. Act on the verdict

- `verdict=pass` → mark step `pass` (or `pass-after-retry` if `k>1`).
  Advance to step `n+1`.
- `verdict=fail` + retries remaining → compose the resume prompt per
  `step-prompt-contract.md`. Build the resume invocation per
  `session-resume.md` (`claude -r <id>` or `codex exec resume <id>`).
  Run. Repeat 4b on the new attempt.
- `verdict=fail` + retries exhausted → apply `stop_discipline`:
  - `halt_and_ask`: mark step `blocked`. Stop the loop. Jump to
    Phase 5 with remaining steps marked `pending`.
  - `skip_and_continue`: mark step `skipped`. Advance.
  - `escalate_to_user`: print the verdict, ask the user how to
    proceed. Their decision selects `halt_and_ask` or
    `skip_and_continue` semantics for this step only.
- `verdict=abstain` → fail loud. Ask the user what to do.

**Where judgment lives:** step 4c's decision is mechanical (cap
arithmetic) once the verdict is in hand. The critic's verdict is the
authority. The orchestrator does not overrule it.

## Phase 5 — Report

**Inputs**
- `state.json`, `manifest.json`, per-step verdicts.

**Outputs**
- `report.md` in the run directory.
- A short console summary to the user: run-id, per-step status table,
  one notable critic finding (the most instructive failure, if any),
  what is pending if halted.

**Where judgment lives:** picking "the most instructive critic finding"
from the set of fails. Short prose, based on the verdict summaries.

**Where determinism lives:** the status table and the file I/O.

**No certification language.** The report states what happened. It
does not claim the work is "complete" or "approved"; that is for the
user to decide after reading it.

## What spans all phases

- The run directory is created at the start of Phase 1 and appended to
  throughout.
- `raw_instructions_sha256` and `models_sha256` are checked at the start
  of each subprocess. A mismatch means the user mutated critical state
  mid-run; abort with a loud error and let them re-invoke.
- The orchestrator never edits target-repo files directly. If it finds
  itself tempted ("the step almost worked, I'll just fix this one
  thing"), it stops and writes a new step instead.
